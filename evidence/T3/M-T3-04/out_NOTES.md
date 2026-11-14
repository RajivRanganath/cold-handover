# T3: benchmark `--output-dir` — notes

## What changed
- `ledgerguard/evaluation/benchmark.py`
  - New option `--output-dir PATH` (default: unset, so behaviour is unchanged).
  - `main()` picks one target directory (`out_dir`) and writes all four artifacts
    (`benchmark.md`, `benchmark.json`, `cases.json`, `unresolved_exceptions.csv`)
    there. The `mkdir` now targets `out_dir`, not `OUTPUT_DIR`, so an option run
    never touches `outputs/`.
  - The "Artifacts written to" line prints `out_dir`, i.e. `PATH` exactly as typed.
  - Frozen manifest logic is unchanged: read and verified in `evaluation/frozen/`.
- `ledgerguard/tests/test_benchmark_output_dir.py`: 9 new tests. All of them
  redirect `OUTPUT_DIR` and `MANIFEST_DIR` into `tmp_path`.
- `docs/evaluation.md`: the options list mentions the new flag.

## Choices made (no one was available to ask)
1. **`PATH` inside `evaluation/outputs/` is refused** with `SystemExit`, before any
   work runs. Requirement 3 forbids creating or modifying anything under
   `outputs/`, and writing into a subdirectory of it would do that. The refusal
   is the only literal reading that satisfies the spec.
2. **Relative `PATH`** is resolved by the OS against the current directory when
   writing. The printed line shows the path as typed.
3. **Artifact equivalence** (req. 5) is tested by comparing a default run with an
   option run on the same seed. Timing fields are stripped: `wall_seconds`,
   `throughput_per_second`, `latency_p50_ms`, `latency_p95_ms`, `latency_ms`, plus
   the markdown rows "Wall time", "Throughput", "Investigation latency".
   `unresolved_exceptions.csv` is compared byte for byte.

## Existing behaviour I did not change (flagged)
- A run whose `(seed, count)` has no manifest yet **creates** one in
  `evaluation/frozen/`. This is the existing "freeze once" behaviour, and it still
  applies with `--output-dir`. A run with a fresh seed or count therefore writes to
  `frozen/`. This is not a write to `PATH`, but it is a write to `frozen/`. I hit
  this myself with a manual run (seed 424242, count 40) and deleted the stray
  manifest it created. The tests avoid it by redirecting `MANIFEST_DIR`.
- `docs/evaluation.md` still says `--output-dir` is an option of the benchmark
  only. The other evaluation scripts have no such flag, and I left them alone.

## Verification
- Baseline before the change: 67 tests passed.
- After the change: 76 passed (67 existing, all still passing, plus 9 new).
- `ledgerguard/evaluation/outputs/` and `ledgerguard/evaluation/frozen/`: file
  checksums (SHA-256) were captured before any change and match after all runs.
  The only difference found during the work was the stray manifest above, which
  I deleted.
- Manual CLI run `--output-dir ../tmp/cli_run` produced the four files.

## Not done
- Nothing outstanding. The live (non-stub) provider path was not exercised, since
  there is no API key. The change is in the orchestration layer and does not
  touch the provider path.
