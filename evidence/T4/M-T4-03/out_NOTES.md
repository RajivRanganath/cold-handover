# Task T4: a short payment was closed automatically

## Summary

A settlement arrived INR 250.00 short of what its own gross, fees, tax and
refunds add up to, with fees and tax exactly per the fee schedule. LedgerGuard
closed it `AUTO_RESOLVED` as `EXCEPTION_FEE_MISMATCH`. The fee classification had
no proven cause behind it, and the residual check that should have caught the
missing money could not see it.

Fixed: the case now escalates to `HUMAN_REVIEW_REQUIRED` and reports the INR
250.00 as unattributed. Nothing that was closed correctly before changes.

## The cause

`ledgerguard/reconciliation/matcher.py`, the `FEE_MISMATCH` branch of
`reconcile_payment`. The residual is the part of the money that a proven fee
variance does not explain. It was computed as:

```python
corrected_net = (
    settlement.gross_amount
    - expected.fees - expected.tax
    - settlement.refund_adjustments
    + settlement.other_adjustments
)
evidence["residual_paise"] = expected.net_amount - corrected_net
```

`corrected_net` is rebuilt from the settlement's own gross, refund and adjustment
fields. It never reads the settlement's reported `net_amount`. So whenever those
fields add up to the expected net, the residual is zero, even if the reported net
is short. That is exactly the reported case: fees and tax match the schedule (no
fee variance), refunds match the ledger, and the reported net is INR 250.00 below
its own components. The check corrected a number that was not the one in dispute
and reported nothing.

Reproduced through `pipeline.run(batch, use_ai=False)` before the fix:

```
EXCEPTION_FEE_MISMATCH | state: AUTO_RESOLVED
residual: 0
reason: Fee and tax reconciled against the independent fee schedule; the exact variance is quantified.
```

The same bug also lets a real fee overcharge hide a shortfall. A settlement with
an INR 40.00 overcharge and a further INR 250.00 short net was also auto-closed
before the fix, for the same reason.

## The fix

Two changes, both small.

1. **`matcher.py`: measure the residual from the reported net.** The fee variance
   is now `observed fee + tax - expected fee + tax`. The corrected net is the
   reported `net_amount` plus that variance. The residual is the expected net minus
   that. The fee variance is also stored as `evidence["fee_variance_paise"]`.
   When the settlement's components are internally consistent, this is algebraically
   identical to the old formula, which is why the existing compound cases
   (`residual_paise` 650.00 and 900.00) are unchanged.

2. **`evidence/safety.py`: a fee classification needs a proven fee variance.** A
   `FEE_MISMATCH` closes only if the fee variance is non-zero and the residual is
   zero. A zero fee variance means the fees match the schedule, so the fee cause
   is not proven, and the case escalates with a reason that says so. This covers a
   settlement whose internal arithmetic is broken while its net still matches the
   ledger. Its breakdown is wrong, but nothing is missing against the ledger. This
   second rule is my reading of the documented principle that a proven cause must
   account for the case. It is not strictly needed for the reported case, which the
   residual change alone already escalates.

### Why this is the right behaviour

It follows the project's own documented principles, not a new rule:

- `docs/architecture.md`, `evidence/safety.py`: a proven cause licenses closure only
  if it accounts for all of the money. `residual_paise` exists for that purpose.
  It was built to block exactly this kind of case, and it failed silently.
- `README.md` and `docs/architecture.md`: "Financial truth is deterministic accounting
  state plus verified evidence." A settlement that does not add up to its own fields
  has an unproven cause, and the controller must not assert one.
- `docs/architecture.md`, `safety.py`: "Abstention is a designed outcome, not a
  failure." Escalating the case is the intended outcome. Nothing here needs the AI
  or a new heuristic.

The fee variance also cannot be dismissed as zero-when-unknown. If it were
inferred, the reported fee-mismatch label would be asserting a cause the batch does
not contain.

## Verification

Commands were run from `repo/` with `.venv/bin/python`.

- **Test suite.** Baseline: 67 passed. After the fix: 72 passed, with the 5 new
  tests in `ledgerguard/tests/test_fee_residual.py`. No existing test was modified.
- **New tests against the unmodified code.** Four of the five fail on the baseline,
  as they should: the reported case, the overcharge-plus-shortfall case, the fee
  overcharge that fully explains the gap (failing on a new evidence key, so it proves
  nothing about behaviour on its own), and the internal-break case. The fifth,
  consistent overcharge plus a INR 650.00 refund, is a guard on existing behaviour
  and passes on both versions.
- **Frozen holdout.** I ran `python -m ledgerguard.evaluation.benchmark` in two
  copies under `../tmp/`: one of the unmodified code and one of the fixed code. Both
  used the offline stub, which is deterministic. The only differences are wall-clock
  and latency fields. `benchmark.md`, `benchmark.json`, `cases.json` and
  `unresolved_exceptions.csv` are otherwise identical. Disposition accuracy, false
  auto resolutions (0), value falsely auto resolved (INR 0.00), and the unresolved
  list did not change.
- **Every generated case.** I compared every per-case status, state, resolution and
  exposure across the full 320-lifecycle dataset (deterministic and AI-path runs),
  the five compound cases and the adversarial pair, baseline versus fixed. No case
  changed. The generator never produces a settlement whose reported net disagrees
  with its own components, so the bug is latent in the generated data.
- **Repository artifacts.** Nothing in `ledgerguard/evaluation/outputs/` or
  `ledgerguard/evaluation/frozen/` was regenerated. All of them still carry the
  extraction timestamp, 00:31:48 to 00:31:49. All benchmark runs wrote to `../tmp/`
  copies.

## Choices and limits

- **Committed artifacts are not regenerated.** The committed benchmark and report
  were produced by live model runs, which are not reproducible offline. My
  before-and-after comparison therefore uses the deterministic stub. It shows the
  fix changes no output on this dataset. It does not reproduce the committed live
  numbers, and I did not try to.
- **Classification unchanged.** An I1-only break (fees exact) is still labelled
  `FEE_MISMATCH`, since `_classify` maps I1 to it and I changed nothing there. The
  label is imprecise, and the case now escalates regardless. A cleaner label would
  need a new exception type. That would touch the taxonomy and the frozen
  per-type metrics, so I left it alone.
- **Documentation not edited.** `docs/architecture.md` already describes the residual
  principle correctly, so it needed no change.
- **Not finished.** Nothing blocked. There is no open item in this task.
