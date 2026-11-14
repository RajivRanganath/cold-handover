# Task T1 notes: offline benchmark reproduction

## What was run
- `.venv/bin/python -m ledgerguard.evaluation.benchmark` (default arguments), from `repo/`, no API key, exit 0, empty stderr.
- No key variables are set in the environment and there is no `.env`. Nothing listens on localhost:20128, so the OmniRoute probe failed and the provider chain was empty. `get_provider()` therefore selected the offline `heuristic_stub`.
- The frozen manifest `ledgerguard/evaluation/frozen/holdout_20260905_320.json` was verified and not rewritten. The regenerated holdout hash matches `3e28d4572d4cfc95...`.

## Results from this run (from `benchmark.json`)
| | Rules only (baseline) | Hybrid (`heuristic_stub`) |
|---|---|---|
| accuracy | 0.8941 | 1.0 |
| auto_resolved | 12 | 21 |
| human_review_required | 19 | 10 |
| false_auto_resolutions | 0 | 0 |
| unresolved_value_paise | 19178059 | 12189954 |

The hybrid row is not the committed result. The committed result used the live `fallback(groq->...)` chain (accuracy 0.9765, 19 auto-resolved, INR 135,901.89 unresolved). Without a key, this reproduction runs the offline stub, which is more accurate on the holdout's fault classes. The stub also closes the F3 cases that the live model only partly closed. The F6 wrong-linkage cases stayed escalated (0 auto-resolved, 0 false auto resolutions) in both systems, which is the safety claim the README makes.

## artifacts_written
The benchmark writes exactly these four files under `evaluation/outputs/`: `benchmark.json`, `benchmark.md`, `cases.json`, `unresolved_exceptions.csv`. I confirmed this by hashing the whole tree before and after the run. Those four files were the only changed files.

Python `__pycache__/*.cpython-314.pyc` files were also created by importing the package. I left them out of `artifacts_written` because the import system wrote them, not the benchmark logic. I deleted them during cleanup. The ground rules exempt cache directories from the byte-identical check anyway.

## Restoration
- Before running anything I copied the whole repo (excluding `.venv`) to `../tmp/repo_orig/`, and recorded SHA-256 hashes of all 82 original files in `../tmp/manifest_all_before.txt`.
- After the run I restored the four overwritten files from that copy with `cp -p`, and deleted the new `__pycache__` directories.
- Final check: the SHA-256 of every file under `repo/` (excluding `.venv`) matches the pre-run manifest exactly. Nothing extra remains.
- The run's own outputs are kept in `../tmp/run_outputs/` for reference. They are not in the repo.

## committed_results_provider
Read from the committed `evaluation/outputs/benchmark.json` (`hybrid.provider`) before any run. `benchmark.md` says the same thing. Both record `fallback(groq->gemini->nvidia->omniroute)`.

## Choices and caveats
- The question asks for "the investigator name your run recorded for the hybrid system". I used `heuristic_stub`, the name from this run's `benchmark.json` and its stdout.
- `hybrid_provider` is the stub name. The README's headline numbers (63.5% / 97.7%, 19 auto-resolved) came from a live model and are not reproduced offline.
- The `mkdir -p` I ran for a manifest check used a path outside the work directory. It left nothing behind. I checked that the target does not exist.
- Tests were not run; the task did not ask for them.
- Nothing was left unfinished.
