# Cold Handover

Can a software project be picked up by someone who has never seen it and has nobody to ask? This repository tests that question with a controlled experiment: a fresh AI agent, real engineering tasks, and hidden checks.

**Live site:** https://rajivranganath.github.io/cold-handover/
**Live demo:** https://rajivranganath.github.io/cold-handover/ledgerguard/

## Result

A fresh agent completed four predefined tasks, five times each, using the original repository and documentation. All 20 attempts passed.

The project under test is [LedgerGuard](https://github.com/RajivRanganath/ledgerguard), a payment-settlement reconciliation controller.

| Task | Description | Passed | Median time |
|---|---|---|---|
| T1 | Reproduce the benchmark offline and leave the repository byte-for-byte unchanged | 5 of 5 | 1 min 19 s |
| T2 | Fix a specified bug: a failed or pending settlement could close a payment | 5 of 5 | 3 min 49 s |
| T3 | Add an `--output-dir` option to the benchmark (held out until measurement) | 5 of 5 | 2 min 05 s |
| T4 | Diagnose and fix an unspecified bug from an operator's report | 5 of 5 | 6 min 01 s |

T1 to T3 give the agent explicit requirements. T4 raises the difficulty: it was added in a second round and gives only an operator's report of an edge case the audit itself surfaced (a settlement that arrived short of its own arithmetic was closed as a fee mismatch). The agent had to find the cause and choose the right behaviour from the project's documented principles. All five attempts did, and all five also handled a harder variant that the report never mentioned.

## Method

- **Subject:** LedgerGuard at commit `0540a80` (5 September 2026), exported unchanged.
- **Agent:** Claude Code with Claude Haiku 5.5.
- **Conditions per attempt:** fresh copy of the repository, empty configuration, no memory, web tools disabled, a sandbox limited to the attempt's own folder, and nobody available to answer questions.
- **Tasks and checks:** written and frozen before the measured attempts of each round. File hashes are recorded in a protocol lock.
- **Scoring:** hidden tests and comparisons the agent could not see. Every attempt also had to keep the 67 original tests passing and leave the committed benchmark results unchanged.
- **Controls:** for each task, the unmodified repository fails the checks and a reference solution passes them.
- **Verification:** all 20 verdicts were re-evaluated from scratch and matched.

## Scope

What the result supports, and where it stops:

- **Supported:** a small, efficient model completed specified changes, a held-out extension and an unspecified diagnosis on this repository, repeatably, with no help.
- **Sample:** one repository, one agent configuration, five attempts per task. The figures are descriptive, not statistical.
- **Agent, not human:** it measures agent task completion. Human onboarding is a separate question.
- **Code and documentation together:** the agent had both, so the result reflects the repository as a whole and does not isolate the documentation.
- **Next step:** every task passed, so harder and more ambiguous tasks are the natural extension.
- **Versions:** round 2 ran on Claude Code 2.1.325 and round 1 on 2.1.316. The model, repository snapshot and sandbox were the same.
- **Pilots:** excluded from the counts. Two ran before round 1 and two before round 2 (one of which never started).

The site lists the full disclosures.

## Live demo

The original LedgerGuard Python package runs in the browser through Pyodide. There is no server and no API key. It uses LedgerGuard's offline stand-in investigator, not a live model.

- Edit the synthetic test data (remove a settlement, remove a bank credit, add a fee, mark a settlement as failed) and rerun.
- Commands can be spoken, typed or chosen from dropdowns. Voice uses the browser's speech recognition (Chrome, Edge, Safari).
- To see an agent's change take effect: enter `mark the settlement for case 4 as failed`, and the original code closes the case. Then enter `use the agent's fix`, which loads the patch from attempt M-T2-03, and the case is sent for review instead.

## Repository contents

| Path | Contents |
|---|---|
| `index.html` | Case study: design decisions, method, all attempts, limitations |
| `ledgerguard/` | Live demo: the original dashboard, the package (original and with the M-T2-03 patch) and the browser bridge |
| `evidence/` | For each of the 20 attempts: transcript, code diff, the agent's notes and the checker's verdict. Usernames, home paths and session identifiers are redacted |
| `src/` | The experiment harness and the scripts that built this site (see `src/README.md`) |

The evaluator and its hidden tests are not published, so that the tasks remain reusable.

## Run locally

```
python3 -m http.server 8000
```

Open http://localhost:8000. A local server is required because the demo loads files with `fetch`.
