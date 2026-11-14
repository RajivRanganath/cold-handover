# Task T1 notes: offline benchmark reproduction

## What was run
- Command: `.venv/bin/python -m ledgerguard.evaluation.benchmark` (no `--provider`, no `--seed`/`--count`/`--split`, i.e. the documented defaults: seed 20260905, count 320, holdout split).
- No provider key was set and there is no `.env`. The default `auto` provider therefore built an empty chain (the omniroute reachability probe on localhost:20128 also did not succeed) and fell back to `HeuristicProvider`, which reports itself as `heuristic_stub`. The run's own output says so: "the hybrid run used the offline heuristic stub, not a model".
- Exit code 0. The frozen holdout check passed (manifest `holdout_20260905_320.json` unchanged, batch SHA-256 `3e28d4572d4cfc95...` matched).
- The run's stdout is kept at `../tmp/run_stdout.txt`; the regenerated outputs are at `../tmp/run_outputs/`.

## Choices made
- **Canonical command.** `docs/evaluation.md` and the README describe `--provider groq` / the default chain for the published numbers. Those need network and keys, which this task rules out, so I ran the default with no provider flag. The hybrid numbers here are therefore stub numbers, not model numbers.
- **`hybrid_provider`** is taken from this run's output: `heuristic_stub`.
- **`committed_results_provider`** is taken from the committed `benchmark.json` (`hybrid.provider`) and the committed `benchmark.md` header, which both read `fallback(groq->gemini->nvidia->omniroute)`. These were read before I ran anything.
- **Units.** `accuracy` is a fraction (0.8941, 1.0), as in the JSON. `unresolved_value_paise` is integer paise, as in the JSON.
- **`artifacts_written`** lists the four files the benchmark rewrote under `ledgerguard/evaluation/outputs/`: `benchmark.json`, `benchmark.md`, `cases.json`, `unresolved_exceptions.csv`. The frozen manifest is only written when absent, and it was present, so it was not rewritten. Python `__pycache__` files were also created by the import, but these are cache directories and are outside the constraint and the artifact list.

## Restoring the repo
- Before running I copied the repo (excluding `.venv`) to `../tmp/orig/` and hashed all 82 files (`../tmp/orig_sha256.txt`).
- The run rewrote the four output files above. I restored them from the snapshot with `cp -p`.
- Re-hashing the whole tree (excluding `.venv` and `__pycache__`) matches the original hashes for all 82 files.

## Observations and caveats
- The committed `benchmark.json` hybrid (groq/fallback, 97.7% accuracy, 19 auto-resolved) cannot be reproduced offline. Those numbers are not comparable to this run's stub numbers.
- The committed `benchmark.json` `investigator_chain.chain` still lists the stale NVIDIA model `nvidia/llama-3.1-nemotron-70b-instruct`. This was already documented in `docs/evaluation.md` and I did not change it.
- The stub reaches 100% accuracy on this holdout (`docs/limitations.md` already flags this). Its false auto resolutions are 0, the same as the committed model run.
- I did not run the pytest suite; the task did not ask for it.
- The `.venv` interpreter was run with `-I` only for reading JSON; the benchmark itself was run as the repo's module.
