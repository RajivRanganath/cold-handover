# T4 — a short payment was closed automatically

## Summary

A settlement arrived INR 250.00 short of what its own gross, fees, tax and
refunds add up to. Its fees and tax were exactly per schedule. LedgerGuard closed
the case `AUTO_RESOLVED` as `EXCEPTION_FEE_MISMATCH`, and nothing in the output
mentioned the missing INR 250.00. The cause was a gap in the residual check: it
never compared against the amount the provider actually reported. The fix adds a
second guard that compares the settlement's reported net against its own figures,
and it blocks closure on either guard.

## Cause

The matcher runs the six invariants. Here I1 (settlement arithmetic:
`gross − fees − tax − refunds + adj == net`) fails by 250.00. I2 (fees and tax
against schedule) holds. I3 (reported net against the Shadow Ledger) also fails.
`_classify` takes I2, then I1, so the case is `FEE_MISMATCH`. I3 is listed under
`FEE_MISMATCH`'s explained invariants, so it is not a secondary finding either.

The only check that could have caught the missing money was `residual_paise`
(`reconciliation/matcher.py`, `FEE_MISMATCH` branch). It was computed as:

```
corrected_net = gross − expected_fees − expected_tax − settlement.refund_adjustments + settlement.other_adjustments
residual      = expected.net − corrected_net
```

`corrected_net` is rebuilt from the settlement's **components**. The reported
`net_amount` is never read. When the fees and tax are on schedule and the
reported net is 250.00 short of its components, `corrected_net` equals the Shadow
Ledger's expected net, the residual is 0, and the safety gate (`evidence/safety.py`)
closed the case as a proven fee variance with nothing left over.

Reproduced on the untouched code: a gross of INR 10,000.00, fees per schedule, and a
reported net 250.00 short gives `AUTO_RESOLVED` (see the new tests below).

## Fix

**`reconciliation/matcher.py`**

- `residual_paise` is now measured against the net the provider actually paid, with
  the fee variance added back:
  `residual = expected.net − (settlement.net + (fees+tax observed − fees+tax expected))`.
- New evidence field `arithmetic_gap_paise` = the settlement's own components
  (corrected for fee variance) minus its reported net. This is the I1 gap. Positive
  means the reported net is below what its components add up to.

**`evidence/safety.py`**

- A deterministic close (`DUPLICATE_RECORD`, `FEE_MISMATCH`, `DELAYED_SETTLEMENT`) is
  blocked when either `residual_paise` or `arithmetic_gap_paise` is non-zero. This is
  a new helper, `_unexplained_money_decision`, which states the direction and size
  of the gap. The residual wording is kept, so C2's messages are unchanged.
- Escalation reasons no longer say "fee and tax reconciled" when the fee variance
  was zero, which was false for this case.

**`docs/architecture.md`**: the guard table lists `arithmetic_gap_paise`.

**Tests**: `ledgerguard/tests/test_t4_unexplained_net.py` (5 tests, new file; no
existing test was modified).

## Why this is the right behaviour

The documented principles point the same way:

- "Financial truth is deterministic accounting state plus verified evidence." Money
  that is short of the settlement's own arithmetic is not proven to be a fee.
- "A proven cause is not the same as a fully explained case" (`architecture.md`,
  the residual guard). A fee variance licenses closure only when it accounts for
  all of the money.
- "Abstention is a designed outcome." When proof is incomplete the case goes to a
  human, with the exposure attached.

So the case should escalate as `HUMAN_REVIEW_REQUIRED` with INR 250.00 shown as
unexplained. It now does.

I also considered the simpler fix of measuring the residual against the reported
net alone. That is wrong on its own. Take a settlement whose deduction is 250.00
more than its net implies, while the reported net happens to equal the ledger's
expectation. The net-only residual is 0, and the case would close as a fee
mismatch. The reported case, and this one, are both settlements that contradict
their own figures, so the arithmetic guard is needed as well. The test
`test_offsetting_components_do_not_close_even_when_the_net_matches_the_ledger`
pins this. The old code escalated it, and the fixed code still escalates it.

## Behaviour that must not change: evidence

- **Test suite**: 67 existing tests pass unchanged, and the 5 new tests pass.
  Run with `.venv/bin/python -m pytest ledgerguard/tests -q`: 72 passed.
- **New tests against the original code**: 4 of 5 fail (the 5th passes because it
  checks a clean settlement). The reported case comes out `AUTO_RESOLVED`.
- **Identity by construction**: when the reported net is internally consistent
  (I1 holds), `residual_paise` is the same as the old formula. The new
  `arithmetic_gap_paise` is 0. So every case that does not contradict its own
  arithmetic gets the same answer as before. The only cases that change are those
  where I1 fails, and those are the cases that were wrongly closed.
- **Frozen holdout**: benchmark run on an untouched copy and on the fixed copy,
  both with `--provider none` (deterministic, no model calls). `benchmark.json`
  and `unresolved_exceptions.csv` are identical except for wall-clock timing fields.
  Holdout rules-only: 12 auto resolved, 0 false, INR 0.00 falsely resolved, both
  before and after.
- **Wider sweep**: every decision compared before and after, on 8 seeds of the full
  320-lifecycle generator and on the compound batch, with and without the
  investigator path (heuristic provider). 8 × 320 × 2 = 5,120 decisions, plus 10 for the
  compound batch. **Zero changed.**
  The generator never emits an internally inconsistent settlement, so the sweep
  cannot show the new guard firing. The new tests cover that gap.
- **Compound cases**: C2 and C5 still escalate with the same residuals (650.00,
  900.00). C1 and C3 still close.

## Artifacts

Checked by SHA-256 before and after: all 21 files under
`ledgerguard/evaluation/outputs/` and `ledgerguard/evaluation/frozen/` are
unchanged. The benchmark was run only in scratch copies under `../tmp/` (`before/`,
`after/`), never in `repo/`.

## What I could not do, and limitations

- **I did not regenerate the committed live-model benchmark.** The committed
  `benchmark.md` and `cases.json` come from live Groq runs. There are no API keys
  here, so model output cannot be reproduced. The model-dependent figures (accuracy,
  closed counts from the investigator) therefore cannot be re-verified. The change
  does not touch the investigator, the Evidence Gate or the disposition of any
  AI-investigated case. I checked the deterministic arms only, which is what the
  change affects. For the holdout F3 and F6 rows the investigator path was checked
  with the heuristic provider only.
- **The fault taxonomy has no internally inconsistent settlement.** The F4 injector
  recomputes `net_amount` after changing fees, and the other injectors keep the
  arithmetic consistent. So the holdout never exercised this path, and the frozen
  numbers are unchanged for that reason. This is also why the bug went unnoticed.
  Adding an "I1-breaking" fault class would change the frozen holdout and invalidate
  published numbers, so I did not add one.
- **Wording**: the new escalation text for the arithmetic gap is my own. The
  residual wording is the old one. Both are checked by tests.
- **Repository**: `repo/` is not a git repository, so there is no commit. No
  commit or PR was requested.
