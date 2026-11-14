# Task T4: a short payment was closed automatically

## Summary

A settlement whose reported net was INR 250.00 below its own arithmetic
(gross − fees − tax − refunds + adjustments) was auto-closed as a fee mismatch.
The fee and tax were exactly on schedule, so the fee check passed, and the
guard that is supposed to stop a proven cause from closing a case that still has
unexplained money did not fire.

The fix is a one-block change in `ledgerguard/reconciliation/matcher.py`
(the `FEE_MISMATCH` branch of `reconcile_payment`). The residual that the
safety gate reads is now computed from the net the provider actually paid, not
from a net rebuilt from the Shadow Ledger's own inputs.

## Cause

`evidence/safety.py` refuses to auto-close a fee mismatch when
`evidence["residual_paise"]` is non-zero. That residual is set in `matcher.py`:

```python
corrected_net = gross - expected.fees - expected.tax - settlement.refund_adjustments + settlement.other_adjustments
evidence["residual_paise"] = expected.net_amount - corrected_net
```

`corrected_net` is built from the gross, the schedule fee and tax, and the
settlement's adjustments. It never reads `settlement.net_amount`, the figure the
provider reported as paid. So the residual measures only disagreement in the
refund and adjustment inputs. Any shortfall in the reported net is therefore
invisible to it.

Reproduced on a single hand-built lifecycle (gross INR 10,000.00, fees and tax
on schedule, reported net INR 250.00 low, deterministic path only): before the
fix the case was `EXCEPTION_FEE_MISMATCH`, `AUTO_RESOLVED`,
`residual_paise = 0`.

Invariant I1 (`settlement arithmetic is internally consistent`) fails for this
case, which is what routes it to `FEE_MISMATCH` in `_classify`. Fees and tax
pass I2. The missing money is the I1 discrepancy, and the residual check was the
only thing that could have caught it.

## Fix

```python
fee_variance = (settlement.fees + settlement.tax) - (expected.fees + expected.tax)
corrected_reported_net = settlement.net_amount + fee_variance
evidence["residual_paise"] = expected.net_amount - corrected_reported_net
```

Correcting the proven fee variance now means: take what was actually paid and
add back the over- or under-charged fee. Then compare that with what the Shadow
Ledger expects. Whatever is left is money the fee variance does not explain.

Algebra: with `d` = the I1 discrepancy (`derived − reported net`), the new
residual equals the old one plus `d`. The change therefore has no effect when
the settlement arithmetic is internally consistent, which is every case the
generator's F4 fault produces and every compound case except the one under test.
It only changes behaviour when money is missing relative to the settlement's own
arithmetic, which is the reported defect.

## Why this is the right fix

It follows the project's stated principles, not a new rule:

- `docs/architecture.md`, Safety gate: a proven cause is not a fully explained
  case. The residual guard exists to stop closure when "correcting the proven
  fee variance still leaves money unattributed." The code computed that
  quantity incorrectly; the intent was already documented.
- `README.md` core claim: "financial truth is deterministic accounting state
  plus verified evidence." The reported net is the provider's statement of what
  moved. Ignoring it when asking whether money is missing is not accounting.
- Proof and authority are separate (architecture doc). Here the defect is in the
  proof, not in authority: the case should not be closed as proven, so it goes to
  `HUMAN_REVIEW_REQUIRED` with the residual named and the reason text
  "Correcting it still leaves 250.00 INR unattributed".

I did not change the `safety.py` guard or add a new state. The guard was already
correct; its input was wrong.

Overpayments of the same size are also escalated, since `abs(residual)` is used
in the message and the test pins the sign.

## Verification

- **Reproduction:** the operator's case closes before the fix and escalates after.
- **Holdout and full dataset unchanged:** I captured every deterministic decision
  (case id, exception type, state, residual, reason text) for the 320-lifecycle
  dataset and the 85-case frozen holdout, before and after the change. The two
  snapshots are identical, so no existing case changed state, type, residual or
  reason. The fix changes only cases whose settlement arithmetic is internally
  inconsistent, and the generator produces none of those on this data.
- **Why the AI-dependent holdout numbers are also unaffected:** `should_investigate`
  only sends `UNEXPLAINED_SHORTFALL`, `AMBIGUOUS_REFERENCE` and `BANK_MISMATCH`
  to a model (`ai/investigator.py`). `FEE_MISMATCH` never reaches a provider, so
  its decision is identical under any provider, including the offline stub.
- **Test suite:** `pytest ledgerguard/tests` → 72 passed, including the existing
  compound tests that pin `residual_paise` = 650.00 (C2) and 900.00 (C5). Both
  are reproduced by the new formula, because those settlements have consistent
  arithmetic.
- **New tests:** `ledgerguard/tests/test_residual_fee_shortfall.py`, 5 tests:
  1. The reported case escalates, with residual 250.00 and the reason text.
  2. The same case is not closed by the investigator path either.
  3. A 250.00 overpayment also escalates.
  4. A fee overcharge plus a 250.00 shortfall blocks on the shortfall.
  5. A fully explained fee overcharge still auto-closes (regression guard).
- **Artifacts:** SHA-256 of every file under `ledgerguard/evaluation/outputs/`
  and `ledgerguard/evaluation/frozen/` was recorded before any change and
  re-checked after the test run. All 20 output files and the frozen manifest
  are byte-identical. I did not run `benchmark` or `report`, so nothing was
  regenerated.

## Choices and limits

- **Benchmark not regenerated.** The canonical benchmark runs against Groq and
  there is no API key here, and regenerating would overwrite the protected
  artifacts anyway. The equality claim above rests on the deterministic
  decision snapshot, which I argue (and checked) is the only input to these
  cases. If you want a byte-level check of `benchmark.json`, regenerate it in a
  scratch directory with `OUTPUT_DIR` redirected, not in place.
- **Reason text.** The escalation reason still begins with the existing
  sentence "Fee and tax reconciled against the independent fee schedule", then
  says money is unattributed. That sentence is accurate about the fee part, but a
  reader could take it as a claim that the whole case reconciles. I left the
  wording alone because the existing compound test pins the reason fragments
  "unattributed" and "650.00". This could be reworded in a follow-up.
- **Documentation.** `docs/` already describes the intended behaviour, so I did
  not edit it.
- **Not done:** no changes to the investigator, the Evidence Gate, the
  `DELAYED_SETTLEMENT` or `DUPLICATE_RECORD` paths, or the frozen holdout.
  `DUPLICATE_RECORD` and `DELAYED_SETTLEMENT` do not set a residual, so they
  are not affected by this defect.
