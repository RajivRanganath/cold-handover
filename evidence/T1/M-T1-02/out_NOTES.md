# T1 notes: offline benchmark reproduction

## What was run
- `.venv/bin/python -m ledgerguard.evaluation.benchmark` from `repo/`, no arguments, no API key.
- Exit 0, no stderr. Holdout frozen manifest `ledgerguard/evaluation/frozen/holdout_20260905_320.json` verified (not rewritten).
- No `.env` file exists and no provider key is set in the environment, so `get_provider()` resolved to the offline `heuristic_stub`.

## Results from this run
- Hybrid investigator: `heuristic_stub`. This is not a model. The hybrid numbers are the offline stand-in's numbers.
- Baseline (rules only): accuracy 0.8941, auto_resolved 12, human_review_required 19, false_auto_resolutions 0, unresolved_value_paise 19178059.
- Hybrid (heuristic_stub): accuracy 1.0, auto_resolved 21, human_review_required 10, false_auto_resolutions 0, unresolved_value_paise 12189954.
- `investigator_chain` in `benchmark.json` is `null` for this run, because the stub has no router report.

## Differences from the README and the committed artifact
- The README and the committed `benchmark.json` record the hybrid as `fallback(groq->gemini->nvidia->omniroute)`, a live model chain, with 97.7% accuracy and 19 exceptions correctly resolved. This offline run does not reproduce those numbers, and the README's "19 correctly resolved" is not what this run produced. The hybrid row here should not be compared with the README's hybrid row.
- The rules-only baseline matches the README (89.4%, 12 correct resolutions, INR 191,780.59 unresolved).

## Files
- `artifacts_written` lists the four files the benchmark overwrites under `ledgerguard/evaluation/outputs/`: `benchmark.json`, `benchmark.md`, `cases.json`, `unresolved_exceptions.csv`. The frozen manifest is only written when missing, and it already existed, so it is not listed.
- Python bytecode caches (`__pycache__/*.pyc`) were created by the run and are excluded from `artifacts_written`, as Python cache files. They were removed afterwards.

## Restoring the repo
- Before running, I backed up `outputs/` and `frozen/` to `../tmp/backup/` and recorded SHA-256s (`../tmp/backup/sha_before.txt`).
- After the run I restored the four overwritten files from the backup. The run's own output is kept at `../tmp/new_run/`.
- Verified: every file that existed under `repo/` at the start matches its original SHA-256 (the manifest in `../tmp/tmp_manifest_before.txt`). Only `.venv/` is excluded from the check. No `.pytest_cache` was created, because the test suite was not run.

## Not done
- The test suite (`pytest`) was not run. It is not required for T1, and running it would write `.pytest_cache` into `repo/`.
- No live-model run was attempted, per the no-key constraint.
