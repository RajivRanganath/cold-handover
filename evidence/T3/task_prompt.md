# Task T3: let the benchmark write somewhere else

Running `python -m ledgerguard.evaluation.benchmark` always writes its artifacts into `ledgerguard/evaluation/outputs/`. Add an option so that a run can write them to another directory instead.

Requirements:

1. Add `--output-dir PATH` to `python -m ledgerguard.evaluation.benchmark`.
2. When it is given, every artifact the benchmark writes (`benchmark.md`, `benchmark.json`, `cases.json`, `unresolved_exceptions.csv`) goes to `PATH`, which is created, including missing parent directories, if it does not exist. A relative `PATH` is resolved against the current working directory.
3. When it is given, nothing under `ledgerguard/evaluation/outputs/` is created or modified.
4. The frozen-holdout manifest behaviour does not change: it is still read from and verified against `ledgerguard/evaluation/frozen/`, and is never written to `PATH`.
5. The artifact contents are the same as a default run would produce, apart from fields that measure wall-clock time.
6. The line the command prints after "Artifacts written to" names `PATH`.
7. Without the option, behaviour is exactly as today.

Keep every existing test passing and add tests for the option. Files under `ledgerguard/evaluation/outputs/` and `ledgerguard/evaluation/frozen/` must be unchanged when you finish.

## Ground rules (same for every task)

- The repository is at `repo/` (current directory). A virtualenv with the project dependencies is already installed at `repo/.venv`; use `.venv/bin/python`. There is no network package installation and no API key, and you must not create or set one.
- Before changing anything, read the handover documentation at the repository root.
- Put any file you are asked to produce in `../out/`. Do not create files elsewhere outside `repo/` except under `../tmp/`.
- Do not modify or delete existing test files. You may add new tests.
- Nobody is available to answer questions. If something is ambiguous, make the most reasonable choice, and record it in `../out/NOTES.md` together with anything you could not finish.
- When you are done, stop. Your work will be checked independently.
