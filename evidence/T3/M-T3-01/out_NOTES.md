# T3 notes: `--output-dir` for the benchmark

## What changed
- `ledgerguard/evaluation/benchmark.py`: new `--output-dir PATH` option. Without it,
  `out_dir = OUTPUT_DIR` and the behaviour is the same as before. With it, the path is
  resolved (relative paths against the CWD), created with parents, and all four artifacts
  (`benchmark.md`, `benchmark.json`, `cases.json`, `unresolved_exceptions.csv`) are written
  there. The final line prints the resolved absolute path.
- `ledgerguard/tests/test_benchmark_output_dir.py`: 7 new tests (offline, stub provider,
  small seed/count, `OUTPUT_DIR` and `MANIFEST_DIR` redirected into `tmp_path`).
- `docs/evaluation.md`: options line mentions the new flag.

## Choices I made (not specified in the task)
- **Refusing a path inside `evaluation/outputs/`.** Requirement 3 says nothing under that
  directory may be created or modified when the option is given, so a PATH inside it is
  rejected with a `SystemExit` before any work is done. Nothing else is restricted; a PATH
  inside `frozen/` is allowed (only the artifacts go there; the manifest logic is unchanged).
- **Printed path is the resolved absolute path**, not the string as typed, so a relative
  PATH is printed unambiguously.
- `~` is not expanded by the code; the shell does that before the argument arrives.
- A PATH that exists as a regular file raises the usual `FileExistsError` from `mkdir`.
  I did not add a nicer message.

## Verification
- Full suite: `.venv/bin/python -m pytest -q ledgerguard/tests` → 74 passed (67 existing + 7 new).
- Content equivalence: a default run and an `--output-dir` run with the same seed/count
  produce identical `benchmark.md` (minus the wall-time / throughput / latency lines),
  identical `benchmark.json` and `cases.json` (minus `wall_seconds`, `throughput_per_second`,
  `latency_p50_ms`, `latency_p95_ms`, `latency_ms`), and an identical unresolved CSV.
- CLI check at the real default seed/count (`--provider stub --output-dir ../tmp/cli_check`)
  succeeded and verified against the committed frozen manifest.
- `ledgerguard/evaluation/outputs/` and `ledgerguard/evaluation/frozen/` SHA-256 hashes were
  taken before and after and are identical. The canonical default run was deliberately NOT
  executed against the real `outputs/`, because it would rewrite the committed artifacts.

## Not done / caveats
- The provider-backed (non-stub) hybrid run was not exercised; there is no API key, and the
  change does not touch provider code.
- The other evaluation scripts (`ablation`, `scale`, `drift`, ...) still write to
  `outputs/` only; the task asked for the benchmark alone.
