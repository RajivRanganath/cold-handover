# Task T4: a short payment was closed automatically

## What happened

A settlement arrived INR 250.00 short of what its own gross, fees, tax and
refunds add up to. Its fee and tax were exactly per the fee schedule. LedgerGuard
closed the case `AUTO_RESOLVED` as `EXCEPTION_FEE_MISMATCH`, and nothing in the
case explained the missing INR 250.00.

## Cause

The auto-close gate for a fee mismatch is the `residual_paise` guard. It asks:
after correcting the proven fee variance, does any money remain unexplained?
If so, the case must escalate.

`reconciliation/matcher.py` computed that residual by rebuilding a net from the
settlement's **components** (gross, refunds, adjustments, fees on schedule):

```
corrected_net = gross - expected_fees - expected_tax - refund_adjustments + other_adjustments
residual      = expected.net - corrected_net
```

It never read the settlement's reported `net_amount`. In the reported case the
components agree with the Shadow Ledger, so `residual = 0`, and the INR 250.00
was in the reported net only. The settlement breaks invariant **I1** (components
do not sum to the reported net). The classifier maps an I1 failure to
`FEE_MISMATCH` (`_classify`), so the case reached the deterministic auto-close
branch with a residual of zero and closed.

The gap was never tested. The compound fixtures (C2, C5) always keep net
consistent with components, so the guard was only ever exercised with I1 holding.

I reproduced it on the original code: fee and tax per schedule, net short by
INR 250.00, result `AUTO_RESOLVED`, `residual=0`.

## Fix

Two changes, both in the deterministic layer:

1. **`reconciliation/matcher.py`**: alongside the existing component residual
   (`residual_paise`, unchanged), compute a **net residual** from what the
   provider actually paid:

   ```
   fee_variance = observed(fees + tax) - expected(fees + tax)
   net_residual = expected.net - (settlement.net + fee_variance)
   ```

   Also record `fee_variance_paise`.

2. **`evidence/safety.py`**: block auto-close if *either* residual is non-zero.
   The escalation reason now says the fee variance is zero when it is, instead of
   describing a fee reconciliation that did not happen.

Reported case, after the fix: `HUMAN_REVIEW_REQUIRED`, with the reason "Fee and tax
match the independent fee schedule, so the fee variance is zero. Correcting it
still leaves 250.00 INR unattributed, with no record explaining it."

## Why this is the right fix

The project's own principles require it:

- **"The AI may propose, the financial system must prove"** and **"when proof is
  insufficient, it abstains"** (README). A close needs the cause to account for
  all the money, not only the part that was proved.
- **"A proven cause licenses closing a case only if it accounts for all of the
  money; any unattributed residual blocks closure"** (`synthetic/compound.py`,
  `tests/test_p1_compound.py`). The residual guard is that rule. The bug was that
  it measured the wrong quantity.
- The money that is actually missing is the shortfall in the **reported net**
  against the Shadow Ledger. Measuring the residual from the components instead
  let an arithmetic break in the settlement pass as a clean reconciliation.

Why the two views together, and why this is a guarantee and not a patch: if
either residual is zero, then the reported net equals the components with fees
on schedule. In that case I1 holds. Contrapositive: **whenever I1 fails, at least
one residual is non-zero and closure is blocked.** So no `FEE_MISMATCH` with a
broken settlement can auto-close.

It changes nothing that closes correctly today. When I1 holds, the two residuals
are algebraically identical (`observed_net + fee_variance` equals
`gross - expected_fees - expected_tax - refunds + adjustments`), so every
consistent settlement behaves exactly as before. This is pinned by a test over
the full 320-lifecycle dataset.

## Verification

- **Reproduction**: the reported case returned `AUTO_RESOLVED`, `residual=0` on
  the original code, and `HUMAN_REVIEW_REQUIRED` after the fix.
- **Tests**: `ledgerguard/tests/test_short_settlement.py`, six new tests:
  - the reported case is not auto-closed, and the reason names INR 250.00;
  - the missing money is measured from the reported net (net residual 25000 paise,
    component residual 0);
  - a proven fee overcharge with a consistent net still closes;
  - a fee overcharge plus a separate INR 250 net shortfall is blocked;
  - components that disagree with the shadow ledger, with the net matching it,
    still block (the component view is needed here);
  - on all 320 generated lifecycles, consistent fee mismatches have identical
    residual views.
  Against the original code, the bug and fee-variance tests fail (the bug test
  returns `AUTO_RESOLVED`).
- **Full suite**: 73 passed (67 before, plus 6 new). No existing test was
  modified.
- **Holdout behaviour unchanged**: I ran the deterministic pipeline, rules-only
  and with the offline heuristic provider, over the frozen holdout (85 cases) and
  over all 320 lifecycles, with the original and fixed code. Per-case state,
  exception type and exposure are byte-identical in both runs. The frozen holdout
  digest verified as before.
- **Artifacts untouched**: SHA-256 of all 21 files under
  `ledgerguard/evaluation/outputs/` and `ledgerguard/evaluation/frozen/` matches
  the snapshot taken before any edit. I did not run the benchmark, because it
  overwrites `outputs/` and the committed numbers come from a live Groq run that
  I cannot repeat without an API key.
- The generator never produces a settlement with a broken net (0 of 320 lifecycles
  break I1), so the published benchmark numbers are not affected by this fix.

## Judgement calls and limits

- **I left the classification as `FEE_MISMATCH`.** An I1-only break is not really
  a fee mismatch, since the fee variance is zero. I considered reclassifying it as
  `UNEXPLAINED_SHORTFALL`, but that would send the case to the AI investigator,
  where a coincidental refund of the same amount could be verified and closed. That
  is a new closure path and a larger behaviour change than the bug needs. The
  outcome is now safe, and the reason text is accurate. Reclassifying I1 breaks
  is a reasonable follow-up, but it should be a separate change with its own
  holdout analysis.
- **I did not regenerate benchmark artifacts**, per the instruction. The holdout
  equivalence above is measured with the deterministic engine and the offline
  stub, not the committed Groq run. For the AI path, identical dispositions were
  observed under the stub. A live run would need the API key, which I did not
  have.
- Docs: `docs/architecture.md` still describes the `residual_paise` guard
  correctly. I did not add a line about the net view there.
- Cache directories created by my test runs were removed. Nothing else in the repo
  was changed except `evidence/safety.py`, `reconciliation/matcher.py` and the new
  test file.
