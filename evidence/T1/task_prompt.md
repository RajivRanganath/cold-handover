# Task T1: reproduce the offline benchmark

Reproduce LedgerGuard's benchmark on its frozen holdout, offline, with no model API key, and report what it produced.

Write `../out/answers.json` with exactly these keys:

- `scored_lifecycles` (integer): how many lifecycles were scored.
- `holdout_batch_sha256` (string): the full SHA-256 of the scored holdout batch.
- `hybrid_provider` (string): the investigator name your run recorded for the hybrid system, exactly as written in the run's output.
- `baseline` and `hybrid` (objects), each with these keys taken from your run, with the same names and units as the benchmark's JSON output: `accuracy`, `auto_resolved`, `human_review_required`, `false_auto_resolutions`, `unresolved_value_paise`.
- `artifacts_written` (list of strings): the repository-relative paths of every file the benchmark command creates or overwrites when run on this repository, sorted.
- `committed_results_provider` (string): the investigator recorded for the hybrid system in the benchmark results that were committed to the repository *before* you ran anything, exactly as written there.

Constraint: when you finish, every file that existed under `repo/` when you started must be byte-for-byte identical to its original state (`.venv/` and Python cache directories excepted). The repository has no git history to restore from.

## Ground rules (same for every task)

- The repository is at `repo/` (current directory). A virtualenv with the project dependencies is already installed at `repo/.venv`; use `.venv/bin/python`. There is no network package installation and no API key, and you must not create or set one.
- Before changing anything, read the handover documentation at the repository root.
- Put any file you are asked to produce in `../out/`. Do not create files elsewhere outside `repo/` except under `../tmp/`.
- Do not modify or delete existing test files. You may add new tests.
- Nobody is available to answer questions. If something is ambiguous, make the most reasonable choice, and record it in `../out/NOTES.md` together with anything you could not finish.
- When you are done, stop. Your work will be checked independently.
