# Task T2: respect settlement status — notes

## Result

Only `processed` settlements now settle a payment. `pending` and `failed`
settlements are ignored by the duplicate pre-pass, the multiple-settlement
check, the invariants and bank matching. A payment with no processed settlement
is `EXCEPTION_MISSING_SETTLEMENT`, with the same expected value, observed 0 and
final state as a payment with no settlement at all. When non-processed
settlements exist, its evidence gains `non_processed_settlements`.

Test suite: 84 passed (67 existing, 17 new in
`ledgerguard/tests/test_settlement_status.py`). Against the pre-change code, 14 of
the 17 new tests fail; the other 3 are controls for unchanged behaviour.

## Files changed

- `ledgerguard/ledger/shadow_ledger.py` — the settlement index holds only
  processed settlements. Non-processed ones go to a separate
  `non_processed_settlements_by_payment` index, read via
  `non_processed_settlements_for()`.
- `ledgerguard/reconciliation/matcher.py` — the duplicate pre-pass considers
  only processed settlements. The no-settlement branch adds
  `non_processed_settlements` when the list is non-empty.
- `ledgerguard/tests/test_settlement_status.py` — new tests (no existing test
  file was touched).
- `docs/architecture.md` — one paragraph on the settlement-status rule.

## Choices I made

- **Shape of the evidence list.** One entry per non-processed settlement record,
  not deduplicated. Sorted by `settlement_id`, with ties kept in batch order.
  Each entry is `{"settlement_id", "status"}`, with status `"pending"` or
  `"failed"`.
- **Missing-settlement case shape.** `settlement` stays `None` and
  `transaction_ids` stays as today (payment and order ids only). The
  non-processed settlement ids are not added to `transaction_ids`, so the case
  is identical to the no-settlement case apart from the evidence key.
- **Duplicate precedence.** Payment-level duplicates (same `payment_id`, both
  identical and conflicting) still return before the settlement checks. No
  `non_processed_settlements` key appears in those cases.
- **Pending copy of a processed settlement.** Excluded from the duplicate
  pre-pass, so it cannot create a `DUPLICATE_RECORD` or a `content_conflict`.
- **Decision text.** The safety gate's `MISSING_SETTLEMENT` wording is
  unchanged.
- **`ShadowLedger.totals()`.** Still counts every settlement record. This is a
  count of ingested records, not a matching step, so I left it alone.

## Verification

- Frozen holdout: the generator only emits `PROCESSED` settlements, so the
  holdout batch hash is unchanged. I ran the benchmark with `--provider none`
  on a copy of the code before and after the change (the benchmark writes to a
  fixed output directory, so I ran it on copies). `benchmark.json`,
  `cases.json`, `unresolved_exceptions.csv` and `benchmark.md` are identical
  except for the wall-clock timing fields (throughput, latency).
- Protected artifacts: SHA-256 checksums of all 21 files under
  `ledgerguard/evaluation/outputs/` and `ledgerguard/evaluation/frozen/` match
  before and after. No artifact was regenerated in the repository.

## Not done

- The canonical benchmark (`--provider groq` / `fallback`) was not re-run. It
  needs API keys, which I must not set, and live model output is not
  reproducible anyway. The offline `--provider none` comparison above is the
  evidence for requirement 6.
- `ledgerguard.tests.rehearsal_check` was not run. It needs a live server on
  port 8137, and the demo beats do not involve pending or failed settlements.
