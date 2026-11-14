# T3 notes: `benchmark --output-dir`

## What changed
- `ledgerguard/evaluation/benchmark.py`: new `--output-dir PATH` option. Without it,
  `out_dir = OUTPUT_DIR` and the code path is the same as before. With it, `out_dir`
  is `Path(PATH).resolve()` (relative paths resolve against the cwd) and all four
  artifacts are written there. `out_dir` is created with `parents=True`. `OUTPUT_DIR`
  is no longer created on a run that uses the option.
- `ledgerguard/tests/test_benchmark_output_dir.py`: 7 new tests. They redirect
  `OUTPUT_DIR` and `MANIFEST_DIR` to temp directories, so the real `outputs/` and
  `frozen/` are never written by the suite.

## Verification
- `pytest ledgerguard/tests -q`: 74 passed (67 existing + 7 new).
- CLI run `--provider stub --output-dir ../tmp/cli_run/sub/dir` wrote all four
  artifacts, and the printed line named the resolved path.
- SHA-256 of every file in `evaluation/outputs/` and `evaluation/frozen/` is identical
  before and after all work (snapshot in `../tmp/before.sha` and `../tmp/after.sha`).

## Choices I made (where the request was open)
1. **PATH inside `evaluation/outputs/` is refused** (exit 2, before any work). Requirement 3
   says nothing under `outputs/` may be created or modified when the option is given,
   so writing there would contradict it. The check uses resolved paths, so symlinks
   into `outputs/` are also refused.
2. **A PATH that exists as a regular file is refused** (exit 2), rather than failing
   later inside `mkdir`.
3. **The "Artifacts written to" line prints the resolved absolute path.** For an absolute
   PATH this is the same string. For a relative PATH it is the absolute location, which
   names the same directory unambiguously.
4. **Timing fields** (`wall_seconds`, `throughput_per_second`, `latency_p50_ms`,
   `latency_p95_ms`, per-case `latency_ms`, and the matching markdown rows) are the only
   fields excluded from the "same as default" comparison in the tests.
5. **The frozen manifest is still written to `frozen/` if it is missing.** That is
   existing behaviour and I left it alone. The option never writes it to `PATH`. The
   committed manifest matches the regenerated data, so no write happened.

## Not done
- `README.md` and `docs/` still describe only the default output location. I did not
  edit them, since the task did not ask for documentation changes.
- No live-provider run. The tests and the CLI check use `--provider stub`, which is the
  offline heuristic, as the ground rules require.
