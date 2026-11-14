# Task T4: a short payment was closed automatically

A finance operator has reported a problem. Investigate it, find the cause, and fix it.

> "One settlement arrived ₹250 short of what its own gross, fees, tax and refunds add up to. The fees and tax on it were exactly per the fee schedule. LedgerGuard still marked the case AUTO_RESOLVED as a fee mismatch. Nothing explained the missing ₹250."

What a correct fix looks like:

1. LedgerGuard must not automatically close a case like the one reported, where money is missing and no cause has been proved. Work out the right behaviour from the project's own documented principles.
2. Cases that LedgerGuard closes correctly today must still close the same way. In particular, the benchmark's results on the frozen holdout must be unchanged.
3. In `../out/NOTES.md`, explain the cause you found and why your fix is the right one.

Keep every existing test passing. Add tests for the new behaviour. Do not leave regenerated benchmark artifacts in the repository: files under `ledgerguard/evaluation/outputs/` and `ledgerguard/evaluation/frozen/` must be unchanged when you finish.

## Ground rules (same for every task)

- The repository is at `repo/` (current directory). A virtualenv with the project dependencies is already installed at `repo/.venv`; use `.venv/bin/python`. There is no network package installation and no API key, and you must not create or set one.
- Before changing anything, read the handover documentation at the repository root.
- Put any file you are asked to produce in `../out/`. Do not create files elsewhere outside `repo/` except under `../tmp/`.
- Do not modify or delete existing test files. You may add new tests.
- Nobody is available to answer questions. If something is ambiguous, make the most reasonable choice, and record it in `../out/NOTES.md` together with anything you could not finish.
- When you are done, stop. Your work will be checked independently.
