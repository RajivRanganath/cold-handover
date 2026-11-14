# Task T2: respect settlement status — notes

## What changed

- `ledgerguard/ledger/shadow_ledger.py`
  - `settlements_by_payment` (read by `settlements_for`) now indexes only `processed` settlements.
  - New index `non_processed_by_payment` and accessor `non_processed_settlements_for(payment_id)` for pending and failed settlements. These are reported, never matched.
- `ledgerguard/reconciliation/matcher.py`
  - `find_duplicates` builds settlement id/conflict sets from processed settlements only.
  - Missing-settlement branch (step 2): when the payment has one or more non-processed settlements, adds `evidence["non_processed_settlements"]` as `[{"settlement_id", "status"}]`, sorted by `(settlement_id, status)`. The key is absent in every other case. `reason`, `expected_value`, `observed_value` and state are unchanged.
- `ledgerguard/tests/test_settlement_status.py` (new): 15 tests covering requirements 1–7.

No change was needed in the controller (`pipeline.py`, `ai/investigator.py`, `evidence/safety.py`). `EXCEPTION_MISSING_SETTLEMENT` is already in `DETERMINISTICALLY_PROVEN` and is not in `NEEDS_INVESTIGATION`, and it already maps to `HUMAN_REVIEW_REQUIRED`. A test asserts the investigator is never called and nothing auto-resolves.

## Choices I made (the spec left these open)

1. **`settlements_for` is now processed-only, globally.** `evaluation/ablation.py` also calls it, so the ablation baseline ignores non-processed settlements too. This matches "every settlement-matching step". It has no effect on any existing batch.
2. **Payment-level duplicates (requirement 5).** The precedence is unchanged: conflicting payment, then identical payment, then missing settlement. The settlement attached to the case in `transaction_ids` is now the processed one, or none. Previously it could have been a pending record. This only differs for batches that contain non-processed settlements. The duplicate cases do not get the `non_processed_settlements` key, because the spec limits it to the missing-settlement case.
3. **One list entry per non-processed record.** If the same pending id appears twice, it appears twice in the list. I did not dedupe.
4. **`content_conflict` for settlements** is now computed over processed settlements only. A pending record that shares an id with a processed one does not create a conflict.
5. **`reason` text is unchanged** in the missing-settlement case when non-processed settlements exist. Only the new key is added.

## Verification

- Test suite: 67 existing tests pass unchanged, plus 15 new tests. Total 82 passed.
- Frozen holdout / benchmark:
  - The generated dataset (320 lifecycles, 305 settlements) contains only `processed` settlements, so the holdout cannot reach the new branches. The `dataset` and `holdout_manifest` sections of the benchmark are identical to the original, and the frozen holdout check passes.
  - The rules-only `baseline` section is identical to the original apart from `wall_seconds` and `throughput_per_second`.
  - **Not reproduced: the `hybrid` section and `investigator_chain`.** The shipped artifacts were generated with a live model (`fallback(groq->gemini->nvidia->omniroute)`). This environment has no provider key, so a re-run uses the offline heuristic stub and gives different hybrid numbers. The differences come from the investigator, not from this change. I could not confirm the hybrid numbers unchanged here. Re-running with the original provider configuration would settle it.
  - I ran the benchmark in a scratch copy at `../tmp/repo_check`, not in the repo.
- Artifacts: checksums of all 21 files under `ledgerguard/evaluation/outputs/` and `ledgerguard/evaluation/frozen/` match the pre-task snapshot. Nothing was regenerated in the repo.

## Not finished / caveats

- Hybrid benchmark numbers could not be reproduced without a provider key (see above).
- No git repository here, so I could not diff against a pristine checkout. I took the before-state snapshot of the artifacts only, not of the source files.
