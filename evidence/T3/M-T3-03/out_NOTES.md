# T3 notes: `benchmark --output-dir PATH`

## What changed
- `ledgerguard/evaluation/benchmark.py`: new `--output-dir PATH` option. When
  given, `benchmark.md`, `benchmark.json`, `cases.json` and
  `unresolved_exceptions.csv` are written to `PATH`, and the
  "Artifacts written to" line prints that path. Without the option, `OUTPUT_DIR`
  is used exactly as before.
- `ledgerguard/tests/test_benchmark_output_dir.py`: 12 new tests.
- `docs/evaluation.md`: one line added to the options list.

## Choices made where the request was open
- **Paths inside `evaluation/outputs/` are refused** (exit code 2, usage error).
  Requirement 3 forbids writing under that directory, so honouring
  `--output-dir evaluation/outputs/x` was not possible. Resolved paths are
  compared, so symlinks into that directory are also refused.
- **The printed path is the resolved absolute path**, so a relative `PATH` prints
  where the files actually went.
- `PATH` is created (with parents) before the run starts, not after it succeeds.
- The default path is unchanged: `OUTPUT_DIR` is still created at start-up.

## Verification
- Full suite: `79 passed` (67 pre-existing, unchanged, plus 12 new).
- Real CLI run, offline with `--provider stub`, into `../tmp/cli_run/nested`.
  It passed the frozen-manifest check against the committed
  `evaluation/frozen/holdout_20260905_320.json`, wrote the four artifacts, and
  exited 0.
- SHA-256 of every file under `evaluation/outputs/` and `evaluation/frozen/`
  was recorded before and after the work. The two lists are identical.
- The default command was deliberately not run in the repo, because it would
  overwrite the committed `outputs/` files (wall-clock fields and live-provider
  results). The default-path equivalence is tested in a sandbox instead.

## Equivalence test
Runs the default path and the `--output-dir` path with the same seed and count
(`424242`/`40`, stub provider). Compares contents after removing the wall-clock
fields: `wall_seconds`, `throughput_per_second`, `latency_p50_ms`,
`latency_p95_ms`, `latency_ms`. The markdown rows "Wall time", "Throughput" and
"Investigation latency" are removed as well. The CSV is compared byte for byte.
A live model run is not reproducible, so it is not covered by this test.

## Not done / out of scope
- No live-provider run was attempted (no API keys, per the ground rules).
- `docs/evaluation.md` is the only doc touched. The README still describes the
  default output location, which is still correct.
- The other evaluation scripts (`scale`, `drift`, `ablation`, ...) still write
  only to `outputs/`. The request covered the benchmark only.
