# Protocol lock: baseline handover audit v1

Status: LOCKED 2026-11-01 (before any measured attempt). Changes after this point are recorded as deviations; the original stays.

## Design change (owner decision, 2026-11-01)
Both exploratory pilots (pilot-T1-A-001, pilot-T2-A-001) passed under the original documentation without needing owner knowledge. On the owner's instruction the experiment is now a **baseline handover audit**: no supplement, no condition B, no before/after comparison. The question becomes: *with only the historical README and the repository, how often does a fresh agent complete each predefined task?*

## Fixed inputs
- Source: github.com/RajivRanganath/ledgerguard @ 0540a8060194e1126444588e878ecea854f00cd9 (= upstream master on 2026-11-01), exported with `git archive`; original repository never modified.
- Snapshot manifest sha256: see `snapshot.sha256` (hash in locked-files.sha256). README (handover v1) sha256 8fc4c5b4847610edcffd4241b8070b738918811cf3c427bcc101acaf2035dbb3.
- Other docs available to the agent: docs/{analyses,architecture,evaluation,limitations,model_comparison}.md, .env.example. No AGENTS.md/CLAUDE.md in the snapshot.
- Tasks: T1 (reproduce offline benchmark without leaving committed results changed), T2 (respect settlement status), T3 (benchmark `--output-dir`). Prompts in `tasks/T{1,2,3}/prompt.md`, unchanged since drafting. T3 was never used in any pilot or repair activity.
- Evaluator: `evaluator/evaluate.py`, `evaluator/hidden_test_t2.py`, ground truth `evaluator/gt/*`. Controls before lock: untouched snapshot FAILS each task; reference solution PASSES each task; T1 attempt leaving outputs overwritten FAILS.
- Pre-lock evaluator corrections (both recorded in preflight.md): regression check runs only the 67 original test files; T2 benchmark comparison uses the same no-key default configuration as the ground truth, timing fields excluded.
- All locked file hashes: `protocol/locked-files.sha256`.

## Agent and environment
- Agent: Claude Code 2.1.316 (`claude -p`), model `claude-haiku-5-5`, default reasoning settings, tools as loaded by default except WebSearch/WebFetch disabled; no MCP, no slash commands/skills; `--dangerously-skip-permissions` inside an outer macOS seatbelt sandbox.
- Cold start per attempt: new repo copy, new empty CLAUDE_CONFIG_DIR (no CLAUDE.md, memory, hooks, plugins other than two Claude Code built-ins, history), `--no-session-persistence`, auth via long-lived token for the owner's existing subscription.
- Sandbox: reads and writes only inside the attempt's `work/` and `claude-config/` (plus read-only Claude binary and a `mktemp` shim). Verified by sandbox-check-002: writes outside denied, temp files work inside.
- Python 3.14.6, deps pinned by `env/constraints.txt`, pre-installed in `repo/.venv` before the session starts.
- Network: outbound network is not blocked (Claude Code needs the API). **Localhost is reachable** from the agent's shell — required because the project's own tests open local sockets. No API keys for LedgerGuard providers are present. Pilot T1 probed localhost:20128 (OmniRoute); nothing was listening. Disclosed as a limitation.
- Credential handling: token scanned for in every output after each attempt.

## Budgets and schedule
- Wall-clock limit 1800 s per attempt (pilots took 116 s and 819 s incl. a 9-minute API stall). No token cap is enforceable on a subscription; tokens/cost recorded from the final result event (list-price estimate, not billed; overage disabled on account).
- Trials: 5 per task, condition A only = 15 measured attempts. Order shuffled with seed 20261101 (`protocol/schedule.txt`), run by 3 concurrent workers.
- Owner questions: none possible; prompt says nobody is available. No coaching.

## Outcome rules (decided before measurement)
- PASS = evaluator exit 0 (every check true). Otherwise FAIL, with the failing checks recorded.
- TIMEOUT (wall limit hit) counts as FAIL; not rerun.
- INVALID only if (a) harness/env setup failed before the session started, or (b) the session ended with zero agent tool calls because of an authentication/provider error. Invalid attempts are kept and reported; one replacement may be run, labelled `<label>-R`.
- Failures are classified (documentation gap / repository defect / environment / agent error / ambiguous task / mixed) from transcript evidence; a stuck agent is not presumed to be a documentation gap.
- No task, check or budget changes after the first measured attempt starts.

## Excluded from measured counts
smoke-*, sandbox-check-*, pilot-T1-A-001, pilot-T2-A-001.

## Claims allowed
Per-task pass counts out of 5 for one model/agent configuration on one repository snapshot. Not: statistical significance, generalisation to other agents/repos, human onboarding effect, or any documentation-improvement effect.
