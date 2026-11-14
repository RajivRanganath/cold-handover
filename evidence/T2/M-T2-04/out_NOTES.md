# Task T2: respect settlement status — notes

## What changed

- `ledgerguard/ledger/shadow_ledger.py`
  - Settlements are indexed by status. Only `processed` ones go into
    `settlements_by_payment`, so `settlements_for()` returns processed settlements
    only. Every consumer that goes through it (the matcher, and
    `evaluation/ablation.py`) inherits the filter.
  - Pending and failed settlements go into a separate index,
    `non_processed_settlements_by_payment`, read via the new
    `non_processed_settlements_for()`. They are used for evidence only.
- `ledgerguard/reconciliation/matcher.py`
  - `find_duplicates` computes settlement duplicates and content conflicts over
    processed settlements only, so a non-processed record can never make a
    settlement a duplicate or a conflict.
  - Missing-settlement branch: when the payment has non-processed settlements, the
    evidence gains `non_processed_settlements`, a list of
    `{"settlement_id", "status"}` sorted by `settlement_id` (ties broken by
    status). The key is absent in every other case. `reason`, `expected_value`,
    `observed_value`, the transaction ids and the final state are unchanged.
- `ledgerguard/tests/test_settlement_status.py` — 16 new tests covering requirements
  1–5 and 7, plus the bank-matching and duplicate-index cases.

No changes to the investigator, safety gate, or pipeline were needed:
`MISSING_SETTLEMENT` is already in `DETERMINISTICALLY_PROVEN`, never
`NEEDS_INVESTIGATION`, and already routes to `HUMAN_REVIEW_REQUIRED` in `decide()`.
An end-to-end test with a spy provider asserts the investigator is never called
and that the outcome is never `AUTO_RESOLVED`.

## Choices made (ambiguities)

1. **Duplicate-payment cases attach processed settlements only.** Previously a
   payment-level duplicate case could carry a pending or failed settlement's id in
   `transaction_ids`. It now behaves as if that settlement were absent. This only
   changes output for batches that contain non-processed settlements.
2. **The new key is only added to `EXCEPTION_MISSING_SETTLEMENT`.** Requirement 3
   was read as applying to that case only. Payment duplicates keep their precedence,
   so they carry no such key.
3. **The `reason` text is left as it was** in the missing-settlement case, even when
   non-processed settlements exist, so the only added information is the new key.

## Verification

- Full suite: `.venv/bin/python -m pytest ledgerguard/tests -q` → **83 passed**
  (67 existing, unmodified, plus 16 new).
- Holdout (requirement 6): all 81 settlements in the regenerated frozen holdout are
  `processed`, so every new filter is a no-op there. The deterministic outputs
  `reconciliation_report.csv`, `decision_log.json` and `evidence_ledger.csv` are
  byte-identical after regeneration, and the rules-only baseline metrics in
  `benchmark.json` match.

## Not finished / caveats

- **The hybrid benchmark numbers could not be reproduced here.** Regenerating
  `benchmark.json`, `cases.json` and `unresolved_exceptions.csv` gave different
  hybrid results: no API key is available, so the run fell back to
  `heuristic_stub` (`model_calls` 0 instead of 15; accuracy 1.0 vs 0.9765). The
  committed artifacts were produced with the live provider chain. The inputs and
  deterministic outputs are unchanged, so the difference is most likely the
  provider, but I did not re-run the pre-change code under the same no-key
  conditions to prove it.
- **Artifacts restored.** `ledgerguard/evaluation/outputs/` and
  `ledgerguard/evaluation/frozen/` were regenerated for checking, then restored from
  a snapshot. SHA-256 checksums of every file match the pre-change state (checked
  after the final test run).
- The repository is not a git repository, so nothing was committed.
