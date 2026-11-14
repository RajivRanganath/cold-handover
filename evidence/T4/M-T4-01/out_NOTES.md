# T4: a short payment was closed automatically

## Summary

A settlement whose reported net was INR 250.00 below what its own gross, fees,
tax and refunds add up to was closed `AUTO_RESOLVED` as `EXCEPTION_FEE_MISMATCH`.
Fees and tax were exactly on the schedule, and nothing explained the 250.00.

Two defects in `ledgerguard/reconciliation/matcher.py` produced it. Both are
fixed, and a closure guard was added in `ledgerguard/evidence/safety.py` so that
no settlement which does not add up to itself can be closed automatically. The
reported shape now escalates to `HUMAN_REVIEW_REQUIRED`.

## The cause

I reproduced it with one lifecycle: payment 5,000.00, fee and tax exactly on the
schedule, settlement `net_amount` reduced by 250.00 with nothing else changed.
Before the fix, the case came out `EXCEPTION_FEE_MISMATCH`, `residual_paise = 0`,
and `AUTO_RESOLVED` under both rules-only and the hybrid run.

**Defect 1: the arithmetic break was classified as a fee mismatch.**
`_classify` checked I1 (`gross − fees − tax − refunds + adjustments == net`) and
mapped a failure to `FEE_MISMATCH`. I2 (fees and tax match the schedule) held in
this case, so the label asserted a fee problem that the deterministic layer had
just proved did not exist. I1 was also listed as "explained by" the fee mismatch,
so it never appeared as a secondary finding either.

**Defect 2: the residual guard could not see the break.** The guard exists so
that a proven cause (here a fee variance) does not license closing a case that
still has unexplained money. It computed the residual as

    corrected_net = gross − expected fees − expected tax − refunds + adjustments
    residual      = expected.net − corrected_net

`corrected_net` is rebuilt from the settlement's *components*, not taken from its
*reported net*. A settlement whose net contradicts its components therefore gets
residual 0, and the 250.00 disappears. This is the decisive defect: even with the
label wrong, a correct residual would have escalated the case.

## The fix

1. **Residual measured against the reported net** (`matcher.py`, `FEE_MISMATCH`
   branch):

       fee_variance = observed (fees + tax) − expected (fees + tax)
       residual     = expected.net − (settlement.net + fee_variance)

   When I1 holds this is algebraically identical to the old formula
   (`settlement.net + fee_variance` equals `corrected_net` exactly), so every
   residual that exists today is unchanged. It differs only where the reported net
   contradicts the components, which is the case that was missed. Pinned values
   C2 = 650.00 and C5 = 900.00 are unchanged.

2. **An I1 failure with I2 holding is no longer a fee mismatch.** It is
   classified `UNEXPLAINED_SHORTFALL`: money is missing and no cause is proved.
   I1 is removed from the `FEE_MISMATCH` explained-set and added to the
   `UNEXPLAINED_SHORTFALL` one, so it is the driver and not a secondary finding.
   The I2 and I3 fee paths are unchanged.

3. **Closure guard on arithmetic.** The matcher records
   `settlement_arithmetic_gap_paise` (derived − reported net; 0 when I1 holds).
   `safety.decide()` returns `HUMAN_REVIEW_REQUIRED` for any non-zero gap, placed
   before every auto-close route, so it applies to all classifications.

   The guard is deliberately stricter than the Evidence Gate. A same-customer
   orphan refund of exactly 250.00 *does* make the Shadow Ledger balance, so the
   gate verifies it (I verified this in a test: the verdict is `VERIFIED`). But the
   gate's check E7 only re-tests the same contradictory reported net, so a matching
   refund proves nothing about this row. The test
   `test_a_matching_orphan_refund_cannot_close_a_settlement_that_does_not_add_up`
   pins this.

## Why this is the right fix

It comes straight from the project's documented rules, in `docs/architecture.md`:

- Financial truth is deterministic accounting state plus verified evidence. A row
  that contradicts its own arithmetic has no accounting state to be true to.
- "A proven cause licenses closing a case only if it accounts for all of the
  money." The residual guard exists to enforce that, and it was measuring the
  wrong quantity.
- "Abstention is a designed outcome." When proof is missing, escalate.
- The label must be a claim the system proved. "Fee mismatch" is a claim about
  fees, and I2 showed the fees were right.

It is also the minimal change. It adds no exception type, no configuration and no
model involvement, and every case that closes today still closes the same way.

## What I checked

**Existing tests:** 67 of 67 pass before the new tests were added.

**New tests:** `ledgerguard/tests/test_p1_settlement_arithmetic.py`, 8 tests, all
pass. Seven of them fail on the unmodified code. The eighth, a late settlement with
consistent arithmetic still closing, passes on both. It is a regression guard.
Total suite: 75 passed.

**Holdout unchanged, checked per case.** The frozen holdout has 85 lifecycles and
its digest is still `3e28d4572d4cfc95`. I dumped every case's status, state,
resolution, verification verdict, residual and decision reason before and after the
change, for the rules-only baseline and for the hybrid run with the offline
heuristic. The two dumps are identical. The rules-only baseline auto-resolves 12
cases, as published. The hybrid auto-resolves 21 under the heuristic, and makes 15
investigations.

**Whole dataset unchanged.** The same comparison over all 320 generated lifecycles
and the 5 compound cases is also identical, both rules-only and hybrid.

**Why the holdout cannot move:** the new behaviour is reachable only when I1 fails.
Zero of the 85 holdout cases fail I1, because the fault injector keeps the
arithmetic consistent for every fault class. F4 and F6 change fees or refunds and
recompute the net, and F3 touches only the refund's linkage. So no holdout decision
can change.

**Artifacts untouched.** A recursive diff against an untouched snapshot shows
changes only to the two source files, `docs/architecture.md` and the new test file.
Nothing under `ledgerguard/evaluation/outputs/` or `ledgerguard/evaluation/frozen/`
differs. I did not run `python -m ledgerguard.evaluation.benchmark`, because it
rewrites `outputs/` and needs a live key. The frozen manifest was verified by digest
instead.

## Changes

- `ledgerguard/reconciliation/matcher.py`: `_classify`, `_EXPLAINED_BY`, residual
  computation, and the `settlement_arithmetic_gap_paise` evidence field.
- `ledgerguard/evidence/safety.py`: the arithmetic guard in `decide()`.
- `ledgerguard/tests/test_p1_settlement_arithmetic.py`: new tests.
- `docs/architecture.md`: the guard table and an I1 note.

## Decisions I made, and what I did not do

- **No new exception type.** I used the existing `UNEXPLAINED_SHORTFALL` for an
  I1-only failure. A new type would change the taxonomy that the investigator
  prompt and the risk tables are built on.
- **The guard applies to the investigator too.** A verified refund hypothesis does
  not close an arithmetically broken row. This is stricter than the gate, for the
  reason given above. It means an I1-broken row still makes a model call. I did not
  change `should_investigate`, to keep this change to the closure path. Making the
  call is wasted for these rows, and it is a possible follow-up.
- **Not re-run against a live provider.** The committed hybrid figures came from
  Groq. I have no key, so I could not regenerate them. The argument that they are
  unchanged is the one above: the new path is never reached on a holdout case.
- **Limitation.** The holdout contains no I1 breaks, so the benchmark cannot show
  this fix working. It is pinned by the unit tests and by the per-case comparison
  showing no holdout change. A future fault class that breaks settlement arithmetic
  should be added to the generator and to the holdout deliberately, with the frozen
  manifest handled as the docs describe.
