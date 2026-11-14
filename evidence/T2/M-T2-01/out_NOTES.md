# Task T2: settlement status — notes

## What changed

- `ledgerguard/ledger/shadow_ledger.py`
  - `settlements_by_payment` now indexes **only `processed`** settlements, so
    `settlements_for()` (used by the matcher, the invariants' inputs, bank matching
    and `evaluation/ablation.py`) never sees pending or failed rows.
  - New index `non_processed_settlements_by_payment` and accessor
    `non_processed_settlements_for()`, used only to build evidence.
- `ledgerguard/reconciliation/matcher.py`
  - `find_duplicates()` builds settlement duplicate/conflict sets from processed
    settlements only.
  - The no-processed-settlement branch (`MISSING_SETTLEMENT`) adds
    `non_processed_settlements` to evidence when at least one pending/failed
    settlement references the payment. Entries are `{"settlement_id", "status"}`,
    sorted by `settlement_id`. Nothing else about the exception changed (same
    `expected_value`, `observed_value` 0, transaction ids, risk, final state).
- `ledgerguard/tests/test_settlement_status.py` — 19 new tests (no existing test
  file was modified).
- `docs/architecture.md` — one paragraph in the matcher section describing the rule.

## Choices made where the brief was open

1. **Duplicate non-processed rows are each listed.** If the batch contains two
   identical pending rows for one payment, `non_processed_settlements` has two
   entries. I did not de-duplicate, because each entry describes a row the batch
   actually contains.
2. **Sort tie-break.** Sorting is by `settlement_id` alone (stable sort), so rows
   sharing an id keep batch order.
3. **A non-processed row sharing an id with a processed row is ignored**, not
   treated as a content conflict (rule 1). The processed row is reconciled
   normally.
4. **Payment with one processed plus non-processed rows:** no evidence key
   (rule 4 says "exactly as if absent").
5. **Payment with two or more processed settlements plus non-processed rows:**
   still `DUPLICATE_RECORD`, and the non-processed rows are not listed, since they
   take no part in that decision.
6. **`MISSING_SETTLEMENT` `transaction_ids` unchanged.** Non-processed settlement
   ids are not added there; they appear only in evidence.
7. **Reporting counts left alone.** `ShadowLedger.totals()` and
   `evaluation/scale.py` still count every settlement row in the batch. They are
   inventory counts, not matching steps.

## Verification

- `.venv/bin/python -m pytest ledgerguard/tests -q`: **86 passed** (67 existing
  + 19 new).
- The 19 new tests were also run against the original code: **15 fail** there, as
  they should. The other 4 are regression guards (processed still matches,
  no-key cases, payment-duplicate precedence) that pass on both versions.
- Behaviour on the data: I dumped every per-case outcome (status, state, exception
  type, expected/observed/difference, transaction ids, full evidence, settlement
  id) for the full 320-lifecycle set, the dev split and the frozen holdout, under
  rules-only and the offline stub investigator. The dumps from the original code
  and the modified code are **byte-identical**. The generator only emits
  `processed` settlements, so no existing batch changes.
- Artifacts: SHA-256 of every file under `ledgerguard/evaluation/outputs/` and
  `ledgerguard/evaluation/frozen/` is identical before and after.

## Not done / caveats

- **The benchmark was not re-run.** It writes into `evaluation/outputs/` and would
  break the "unchanged" requirement. The equivalence check above covers the same
  batch and the deterministic layer, but not the live-provider hybrid numbers,
  which were never affected by this change (the holdout has no non-processed
  rows).
- **The repository is not a git repository**, so there is no commit. The original
  code is kept as a snapshot at `../tmp/orig/` for comparison, and the scripts
  used for the before/after dump are in `../tmp/`.
- No open questions. The existing 67 tests and the frozen manifest hash are
  untouched.
