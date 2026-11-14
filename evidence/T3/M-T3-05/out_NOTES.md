# T3 notes: `--output-dir` for the benchmark

## What changed
- `ledgerguard/evaluation/benchmark.py`: new `--output-dir PATH` option. When given,
  `benchmark.md`, `benchmark.json`, `cases.json` and `unresolved_exceptions.csv` are
  written there; the directory is created with parents. Without the option, `out_dir`
  is `OUTPUT_DIR`, so the default run is unchanged. The frozen manifest path
  (`MANIFEST_DIR`) is untouched.
- `ledgerguard/tests/test_benchmark_output_dir.py`: 9 new tests (all offline, on the
  stub investigator, with `OUTPUT_DIR` and `MANIFEST_DIR` patched to tmp paths).
- No existing test file was modified.

## Judgment calls
- **A `PATH` inside `evaluation/outputs/` (or equal to it) is refused** with exit
  code 2 and a message. Requirement 3 says nothing under `outputs/` may be created or
  modified when the option is given, so writing there would break it. Symlinks are
  resolved before the check.
- **Relative paths** are made absolute with `os.path.abspath` (no symlink resolution),
  and the "Artifacts written to" line prints that absolute path. Relative paths
  resolve against the current working directory.
- **Directory creation happens before the run**, as the default code already does. If
  the frozen-holdout check then aborts, an empty `PATH` may be left behind. The default
  run has the same behaviour.

## Verification
- `ledgerguard/tests`: 76 passed (67 existing + 9 new).
- Real frozen holdout (seed 20260905, 320 records), `--provider stub --output-dir
  ../tmp/real_check/nested`: the four artifacts were written there and the existing
  manifest verified without a mismatch.
- `shasum -a 256` of every file in `evaluation/outputs/` and `evaluation/frozen/`
  before and after the work: identical (`../tmp/protected_before.sha256` vs
  `../tmp/protected_after.sha256`).
- The equivalence test compares a default run with an `--output-dir` run after
  dropping wall-clock fields (`wall_seconds`, `throughput_per_second`,
  `latency_p50_ms`, `latency_p95_ms`, per-case `latency_ms`, and the matching
  `benchmark.md` rows). Those are the only fields that differ.

## Not done / not verified
- I did not run the default benchmark against a live provider (no keys; not needed to
  verify the option). The live hybrid numbers in `outputs/` were not regenerated.
- `README.md` still documents only the default output location. I did not change it.
