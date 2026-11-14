# Task T1 notes

## What was run
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m ledgerguard.evaluation.benchmark` (no arguments, from `repo/`).
- No API key variables were set, no `.env` exists, and OmniRoute was not reachable on localhost:20128, so `get_provider()` fell back to the offline `heuristic_stub`. The run printed: "the hybrid run used the offline heuristic stub, not a model."
- The test suite and the dashboard were not run (not part of this task).

## Results from this run (stub, not a model)
- Holdout: 85 lifecycles, batch SHA-256 `3e28d4572d4cfc95a7ebd5ad1a04531475e0044e63eb1c732e38e303866f20fa` (matches the frozen manifest; no mismatch error).
- Baseline accuracy 0.8941, hybrid accuracy 1.0. Hybrid auto-resolved 21, human review 10, false auto resolutions 0.
- These differ from the committed results (hybrid accuracy 0.9765, 19 auto-resolved, from the `fallback(groq->...)` run). That is expected: the committed numbers come from a live model and this run used the naive offline stub.

## Repo integrity
- Before running, I copied `repo/` (excluding nothing) to `work/tmp/repo_orig_backup/`.
- The run overwrote four files in `ledgerguard/evaluation/outputs/`. I saved the new versions to `work/tmp/run_outputs/` and restored the originals from the backup.
- Verification: SHA-256 of every file in `ledgerguard/evaluation/frozen/` and `ledgerguard/evaluation/outputs/` matches the hashes recorded before the run. A recursive diff against the backup (excluding nothing) shows no differences.
- `PYTHONDONTWRITEBYTECODE=1` was set so no `__pycache__` was created.
- Because I restored the committed artifacts, the repo still shows the committed (live-model) numbers. The stub numbers exist only in `work/tmp/run_outputs/`.

## Artifact list
- The benchmark writes `benchmark.md`, `benchmark.json`, `cases.json` and `unresolved_exceptions.csv` under `ledgerguard/evaluation/outputs/`. It reads `frozen/holdout_20260905_320.json` and only writes it if missing (it exists, so it is only verified).

## Ambiguities and choices
- "hybrid_provider" is the value from this run (`heuristic_stub`). "committed_results_provider" is taken from the committed `benchmark.json` (`hybrid.provider`); the committed `benchmark.md` says the same thing.
- Accuracy is reported as the fraction used in `benchmark.json` (0.8941, 1.0), not as a percentage.
- Pycache and `.pytest_cache` are excluded from `artifacts_written`, as the ground rules allow.
- Scratch files are in `work/tmp/` (`repo_orig_backup`, `run_outputs`, `orig_hashes.txt`, `restored_hashes.txt`).
