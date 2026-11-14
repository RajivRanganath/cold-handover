# T1 notes: offline benchmark reproduction

## What was run
- `.venv/bin/python -m ledgerguard.evaluation.benchmark` (defaults, no arguments).
- No API key was set (`GROQ_API_KEY`, `GEMINI_API_KEY`, `NVIDIA_API_KEY`, `OMNIROUTE_API_KEY`, `ANTHROPIC_API_KEY` all unset), there is no `.env`, and no `--provider` was passed. `get_provider()` therefore resolved to the offline `HeuristicProvider`, so the hybrid run is labelled `heuristic_stub`. It is not a model run.
- The frozen holdout manifest `evaluation/frozen/holdout_20260905_320.json` already existed. The run verified it and did not rewrite it. The regenerated batch hash matches the frozen value.

## Results from this run
- 85 scored lifecycles, batch SHA-256 `3e28d4572d4cfc95a7ebd5ad1a04531475e0044e63eb1c732e38e303866f20fa`.
- Baseline (rules only): accuracy 0.8941, auto_resolved 12, human_review_required 19, false_auto_resolutions 0, unresolved_value_paise 19178059.
- Hybrid (`heuristic_stub`): accuracy 1.0, auto_resolved 21, human_review_required 10, false_auto_resolutions 0, unresolved_value_paise 12189954.
- The hybrid's accuracy and auto-resolution figures here come from the naive offline stub. They do not reproduce the committed model-run numbers, and they say nothing about a live model.

## Committed results (read before running anything)
- `evaluation/outputs/benchmark.json` records `hybrid.provider` as `fallback(groq->gemini->nvidia->omniroute)`, so `committed_results_provider` is that string. The committed `benchmark.md` gives the same investigator on its line 5.
- The committed `benchmark.json` also contains the stale `investigator_chain.chain` entry for NVIDIA, as `docs/evaluation.md` already records. I did not touch it.

## Artifacts
- The benchmark overwrites four files: `benchmark.json`, `benchmark.md`, `cases.json` and `unresolved_exceptions.csv`. The list is sorted in `answers.json`.
- The frozen manifest is written only when absent, so it was not written here.
- Python writes `__pycache__/` directories inside `repo/` when it imports the package. These are excluded by the ground rules, and I left them in place. They are not in `artifacts_written`, because they are an interpreter side effect and not benchmark output.

## Determinism check
- A second run produced byte-identical `cases.json`, `unresolved_exceptions.csv`, and `benchmark.json` metrics once the four timing fields were excluded.
- `benchmark.md` differed only in its `Wall time`, `Throughput`, and latency rows, as expected.

## Repository restored
- Before running, I snapshotted all 82 non-venv files with SHA-256. I restored the four overwritten committed outputs from a pre-run copy. The whole tree now matches the snapshot, and the only additions are `__pycache__` directories.
- The run's output copies are kept under `../tmp/run1/` and `../tmp/rerun2/`. They are not part of the deliverable.

## Not done / limits
- No live model run, by design (no key and offline constraint). The `hybrid_provider` value and the hybrid figures describe the stub only.
- `answers.json` numbers come from my run. The committed artifacts in the repo remain the originals.
