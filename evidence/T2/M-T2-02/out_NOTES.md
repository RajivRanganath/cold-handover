# Task T2: respect settlement status — notes

## What changed

- `ledgerguard/ledger/shadow_ledger.py`
  - `settlements_by_payment` (used for all matching) now indexes only `processed` settlements.
  - New index `non_processed_settlements_by_payment` holds `pending` and `failed` settlements. It is read only through the new `non_processed_settlements_for()`, and only for evidence.
- `ledgerguard/reconciliation/matcher.py`
  - `find_duplicates` builds settlement duplicate and conflict sets from processed settlements only, so a pending or failed row cannot make another settlement a duplicate or a content conflict.
  - Missing-settlement branch: when a payment has no processed settlement, the exception keeps the same type, `expected_value`, `observed_value` of 0, reason text and state. If non-processed settlements exist, the evidence gets `non_processed_settlements`: `[{"settlement_id", "status"}, ...]` sorted by `(settlement_id, status)`. The key is absent in every other case.
- `ledgerguard/tests/test_t2_settlement_status.py`: 16 new tests. No existing test file was modified.

Multiple-settlement detection, the invariants and bank matching all go through the processed-only lists, so they ignore non-processed rows without further changes. The investigator and safety gate are untouched; `MISSING_SETTLEMENT` is already in the deterministic-escalate path and never reaches the investigator.

## Choices I made (ambiguities)

1. **One evidence entry per non-processed settlement record.** Identical duplicate pending rows are listed twice rather than collapsed. The spec did not say, and listing every record is the more transparent choice for an auditor.
2. **Payment-level duplicates keep their precedence.** The duplicate branches still run first, unchanged. Their `transaction_ids` now include only a processed settlement, where previously a pending or failed row could be listed there. For batches with only processed settlements nothing changes.
3. **`ledger.settlements_for()` is processed-only.** `evaluation/ablation.py` calls it, so the ablation's view of a payment with only pending rows now reports it as missing. This affects only batches that contain non-processed rows; the frozen holdout has none.
4. **Bank matching** looks up credits by settlement reference, as before. A pending row sharing a processed row's reference does not change the processed row's match, and a credit alone never settles a payment that has only a pending row.

## Verification

- Full suite: `.venv/bin/python -m pytest ledgerguard/tests -q` → **83 passed** (67 existing + 16 new).
- Artifacts: sha256 of every file under `ledgerguard/evaluation/outputs/` and `ledgerguard/evaluation/frozen/` was recorded before any change and compared after the final test run → **unchanged**. The test suite does not write those directories.
- Frozen holdout (requirement 6): the generator emits only `processed` settlements, so the holdout is unaffected by construction. I also ran `benchmark --provider none` on a scratch copy under `../tmp/scratch_new/` (no model keys set; the real `outputs/` was not written). Compared with the committed artifacts:
  - `dataset` and `holdout_manifest` are identical.
  - The `baseline` (rules-only) section is identical except for `wall_seconds` and `throughput_per_second`.
  - For all 85 cases, classification, `expected`, `observed_settlement`, `invariants` and `exposure_paise` are identical.
  - `decision`, `investigation`, `verification` and `state` differ for 15 investigated cases. This is expected: the committed hybrid run used a live model and this offline run had none. It is not a regression signal, and I did not regenerate the hybrid artifacts.

## Not done / not verified

- I did **not** run the live hybrid benchmark or any model-backed run, so the hybrid figures in the committed artifacts are not re-derived here.
- I did not run the new tests against the pre-change code to show they fail there. The reasoning is that they would fail (e.g. a pending-only payment matched before), but that is unverified.
- The benchmark-equivalence check compares against committed artifacts, not against a pre-change run on the same offline provider. The deterministic fields match, which is strong evidence, but it is not a same-run A/B comparison.
