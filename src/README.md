# Source

The code that ran the experiment and built this site. These are reference copies: absolute paths are replaced with `/path/to/tms-work` and `/path/to/home`, and the local username with `USERNAME`, so the scripts need those values set before they run.

| Path | Purpose |
|---|---|
| `harness/run_attempt.sh` | Runs one round-1 attempt: fresh repository copy, empty configuration, sandbox, then the hidden evaluator |
| `harness/run_attempt_r2.sh` | Round-2 copy; differs only in the Claude Code version and evaluator path |
| `harness/run_schedule.sh` | Runs the frozen attempt schedule with three workers |
| `harness/sandbox.sb.tmpl`, `harness/shims/` | macOS sandbox profile that limits an attempt to its own folder |
| `harness/aggregate.py` | Builds the results tables from the recorded runs |
| `harness/build_public_evidence.py` | Redacts and copies the evidence for publication |
| `harness/build_site_data.py` | Builds the site's data file from the verified evidence |
| `harness/render_evidence.py` | Renders transcripts, diffs and verdicts as readable pages |
| `harness/build_site.py` | Builds the case study and assembles the live demo |
| `demo/demo.js`, `demo/lg_demo.py` | Browser bridge that runs LedgerGuard through Pyodide |
| `protocol/` | The frozen protocol and schedule for each round |

The evaluator and its hidden tests are not included, so that the tasks remain reusable.
