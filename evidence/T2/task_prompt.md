# Task T2: respect settlement status

`Settlement.status` can be `processed`, `pending` or `failed`, but reconciliation currently ignores it. A pending or failed settlement has not paid anything out, so it must not be able to close a payment.

Change LedgerGuard so that:

1. Only settlements with status `processed` count as settling a payment. Settlements with status `pending` or `failed` are ignored by every settlement-matching step: multiple-settlement detection, the invariants, and bank matching.
2. A captured payment with no `processed` settlement is reported as `EXCEPTION_MISSING_SETTLEMENT`, exactly as a payment with no settlement is today (same `expected_value`, `observed_value` of 0, same final state).
3. If that payment also has one or more non-processed settlements, its exception's `evidence` must include `non_processed_settlements`: a list of `{"settlement_id": <str>, "status": <"pending" or "failed">}` objects sorted by `settlement_id`. Leave the key out in every other case.
4. A payment with one `processed` settlement and any number of non-processed ones is reconciled against the processed one only, exactly as if the others were absent.
5. Payment-level duplicate handling (the same `payment_id` ingested more than once) keeps its current precedence and behaviour.
6. Nothing changes for batches in which every settlement is `processed`. In particular, the benchmark's results on the frozen holdout must be unchanged.
7. The full end-to-end controller must still never send these cases to the AI investigator and must never auto-resolve them.

Keep every existing test passing. Add tests for the new behaviour. Do not leave regenerated benchmark artifacts in the repository: files under `ledgerguard/evaluation/outputs/` and `ledgerguard/evaluation/frozen/` must be unchanged when you finish.

## Ground rules (same for every task)

- The repository is at `repo/` (current directory). A virtualenv with the project dependencies is already installed at `repo/.venv`; use `.venv/bin/python`. There is no network package installation and no API key, and you must not create or set one.
- Before changing anything, read the handover documentation at the repository root.
- Put any file you are asked to produce in `../out/`. Do not create files elsewhere outside `repo/` except under `../tmp/`.
- Do not modify or delete existing test files. You may add new tests.
- Nobody is available to answer questions. If something is ambiguous, make the most reasonable choice, and record it in `../out/NOTES.md` together with anything you could not finish.
- When you are done, stop. Your work will be checked independently.
