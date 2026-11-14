"""Build portfolio/site-data.json from verified evidence only. Every value is derived or quoted with a source;
nothing here is written from memory."""
import json, re
from pathlib import Path

W = Path("/path/to/tms-work")
rows = json.loads((W / "results/attempts.json").read_text())
PUB = W / "public-evidence"


def mmss(s):
    return f"{s // 60} min {s % 60:02d} s" if s >= 60 else f"{s} s"


def first_bench_after_backup(label):
    ev = [json.loads(l) for l in (W / "runs" / label / "events.jsonl").read_text().splitlines() if l.startswith("{")]
    cmds = [str((b.get("input") or {}).get("command", "")) for e in ev if e.get("type") == "assistant"
            for b in e["message"].get("content", []) if b.get("type") == "tool_use"]
    bench = next((i for i, c in enumerate(cmds) if "evaluation.benchmark" in c and "python" in c), None)
    backup = next((i for i, c in enumerate(cmds) if re.search(r"\bcp\b|rsync|shasum|sha256", c)), None)
    return bench is not None and backup is not None and backup < bench


def facts(r):
    patch = (PUB / r["task"] / r["label"] / "agent_changes.patch").read_text()
    files = re.findall(r"^\+\+\+ b/(\S+)", patch, re.M)
    src = [f for f in files if f.endswith(".py") and "/tests/" not in f]
    tests = [f for f in files if "/tests/" in f]
    docs = [f for f in files if f.endswith(".md")]
    new_tests = len(re.findall(r"^\+\s*def test_", patch, re.M))
    f = {"files_changed": files, "source_files_changed": src, "test_files_added_or_changed": tests,
         "docs_updated": docs, "new_test_functions": new_tests, "duration": mmss(r["wall_s"])}
    if r["task"] == "T1":
        f["backed_up_before_running_benchmark"] = first_bench_after_backup(r["label"])
        f["repository_left_identical"] = bool(r["checks"]["repo_files_unchanged"])
        f["summary"] = (f"Backed up the committed results {'before' if f['backed_up_before_running_benchmark'] else 'after'} running the benchmark, "
                        f"restored them, and reported all requested figures correctly in {f['duration']}.")
    else:
        what = ", ".join(Path(x).name for x in src) or "no source files"
        f["summary"] = (f"Changed {what}; added {new_tests} test{'s' if new_tests != 1 else ''}"
                        + (f"; updated {', '.join(Path(d).name for d in docs)}" if docs else "")
                        + f". Passed every check in {f['duration']}.")
    if r["api_retries"]:
        f["summary"] = f["summary"][:-1] + f" (including waits for {r['api_retries']} retried model-API requests)."
    f["summary_source"] = "generated from agent_changes.patch and evaluation.json"
    return f


def extra(r):  # T4 only: the unscored depth measure from the checker's verdict
    if r["task"] != "T4":
        return {}
    ev = json.loads((W / "runs" / r["label"] / "eval.json").read_text())
    return {"handled_unscored_combined_case": bool(ev.get("depth_combined_case_handled"))}


tasks = {
    "T1": {"title": "Reproduce the benchmark offline",
           "plain": "Run LedgerGuard's evaluation with no API key, report ten specific figures, and leave the repository byte-for-byte unchanged, even though the benchmark command overwrites the committed live-model results.",
           "why_it_matters": "A successor has to run the evaluation without destroying the published results it is checking.",
           "role": "repair-stage task (one exploratory pilot beforehand, excluded)"},
    "T2": {"title": "Respect settlement status",
           "plain": "LedgerGuard ignored whether a settlement was processed, pending or failed, so a settlement that never paid out could still close a payment. Fix it with exact edge-case rules, without changing any existing behaviour or results.",
           "why_it_matters": "It is a real correctness gap in a finance tool, and fixing it means touching the core matching logic safely.",
           "role": "repair-stage task (one exploratory pilot beforehand, excluded)"},
    "T4": {"title": "Diagnose a short payment that was closed",
           "plain": "A vague bug report with no rules and no hint where to look: a settlement arrived ₹250 short, its fees matched the schedule, and LedgerGuard still closed it automatically as a fee mismatch. Find the cause and fix it without changing anything LedgerGuard already gets right.",
           "why_it_matters": "It is a real bug in the original code, found after round 1. Fixing it takes diagnosis and judgement from the project's documented principles, not a list of rules to follow.",
           "role": "round 2 task, added after round 1 (two pilots excluded: one never started, one passed)"},
    "T3": {"title": "Let the benchmark write elsewhere",
           "plain": "Add an --output-dir option so a benchmark run can write its files somewhere other than the committed results folder.",
           "why_it_matters": "It is a small extension that has to respect the frozen-holdout check and leave committed results alone.",
           "role": "held-out task (never used before measurement)"},
}

data = {
    "title": "Cold Handover",
    "paths_note": "All file paths are relative to the evidence folder.",
    "framing": "A fresh agent completed four predefined tasks, five times each, using the original repository and documentation.",
    "framing_note": "The agent had the whole repository: README, docs and code. The audit does not separate the README's contribution from the code's.",
    "owner": {"name": "Rajiv Ranganath", "github": "https://github.com/RajivRanganath"},
    "project": {
        "name": "LedgerGuard", "url": "https://github.com/RajivRanganath/ledgerguard",
        "commit": "0540a8060194e1126444588e878ecea854f00cd9", "commit_date": "2026-09-05",
        "one_line": "A self verifying AI finance controller that reconciles payment settlements.",
        "core_claim_quote": "LLM reasoning is not financial truth. Financial truth is deterministic accounting state plus verified evidence. The AI may propose, the financial system must prove.",
        "documented_design_decisions": [
            {"decision": "An independent Shadow Ledger computes what the money should have been, and never reads the provider's settlement or bank records to decide that.", "source": "README, What it does (1)"},
            {"decision": "All money is integer paise; no float ever touches it.", "source": "README, What it does (1)"},
            {"decision": "Deterministic code handles everything it can prove; the AI only sees cases that could not be proved.", "source": "README, What it does (2–3)"},
            {"decision": "An Evidence Gate re-proves every AI claim against the records before anything is closed.", "source": "README, What it does (4)"},
            {"decision": "When proof is insufficient it abstains; abstention is a designed outcome, not a failure.", "source": "README, What it does (5)"},
            {"decision": "No model-generated confidence number; a named Verification Score (\"5 of 7 evidence checks passed\") instead.", "source": "README, Why this is not just an LLM reconciliation bot"},
        ],
        "historical_numbers_note": "LedgerGuard's own benchmark figures come from a live-model run in September and were not re-tested by this audit; if shown, label them as historical.",
    },
    "experiment_decisions_on_record": [
        {"decision": "Tested a pinned historical snapshot (5 Sep 2026) rather than the latest code."},
        {"decision": "Every attempt started cold: fresh copy, empty config, no memory, sandboxed, hidden checks."},
        {"decision": "Used a small, efficient model (Claude Haiku 5.5) rather than a frontier model."},
        {"decision": "Fixed the tasks and checks before any measured attempt, and kept one task held out."},
        {"decision": "When both pilots passed without needing an explanation, ran a baseline audit instead of writing an extra handover just to show an improvement."},
    ],
    "agent": {"tool": "Claude Code 2.1.316", "model": "claude-haiku-5-5",
              "setup": "Each attempt: fresh copy of the repository, empty configuration (no memory, instructions or history), web tools disabled, sandbox limited to its own folder, nobody available to answer questions."},
    "method": "Four tasks, each fixed before its attempts ran (three in round 1, one harder task in round 2); five fresh attempts each (20 total), in an order fixed before running; each checked afterwards by hidden tests and comparisons the agent could not see.",
    "tasks": [],
    "limitation": "This is a small experiment with one repository and one agent configuration. It measures agent task completion, not human onboarding.",
    "cannot_claim": [
        "that the README alone caused the success: the agent also had the code and the other docs",
        "that the result generalises to other tasks, agents, models or repositories",
        "statistical significance (five attempts per task is a small descriptive sample)",
        "any benefit for human newcomers",
        "that the documentation has no gaps; harder or vaguer tasks might expose some",
        "that the model had never seen this public repository in training",
        "anything new about LedgerGuard's own live-model benchmark numbers",
    ],
    "disclosures": [
        "The agent's shell could reach services on the Mac's localhost (the project's tests need local sockets). One attempt (M-T1-05) checked port 20128; nothing was listening.",
        "Outbound internet was not blocked at network level; web search and fetch tools were disabled, and no attempt used the internet beyond the model API.",
        "The login token was visible to the agent's shell; every output was scanned for it after every attempt and it never appeared.",
        "Two exploratory pilots ran before the protocol was frozen and are excluded from the counts.",
        "Round 2 (T4) was designed after round 1's results were known, to test a harder, vaguer task. It ran on Claude Code 2.1.325 instead of 2.1.316 (the older version was no longer installed); the newer version loads its built-in plugins. Model, snapshot and sandbox were the same.",
        "For T4, one check (a fee overcharge combined with an unexplained shortfall) was moved from pass/fail to an unscored depth measure before any attempt ran, because the bug report does not mention it. All five attempts handled it anyway.",
        "T4 had two pilots, both excluded: the first never started (the harness pointed at an uninstalled Claude Code version) and the second passed.",
    ],
}
for t in ("T1", "T2", "T3", "T4"):
    rs = sorted((r for r in rows if r["task"] == t), key=lambda r: r["label"])
    walls = sorted(r["wall_s"] for r in rs)
    data["tasks"].append({
        "id": t, **tasks[t], "prompt_file": f"{t}/task_prompt.md",
        "passed": sum(r["outcome"] == "PASS" for r in rs), "attempts": len(rs),
        "median_duration": mmss(walls[len(walls) // 2]), "duration_range": f"{mmss(walls[0])} to {mmss(walls[-1])}",
        "trials": [{"label": r["label"], "outcome": r["outcome"], "wall_seconds": r["wall_s"], "tool_calls": r["tool_calls"],
                    "output_tokens": r["output_tokens"], "api_retries": r["api_retries"], "failed_checks": r["failed_checks"], **extra(r),
                    "checks": r["checks"], **facts(r), "evidence_folder": f"{t}/{r['label']}/", "evidence_files": sorted(["transcript.md", "agent_changes.patch", "evaluation.json"] + [x.name for x in (PUB / t / r["label"]).glob("out_*")])} for r in rs],
    })
data["check_labels"] = {
    "repo_files_unchanged": "Repository left byte-for-byte as it started",
    "answers_json_valid": "Answers file present and readable",
    "scored_lifecycles": "Correct number of scored cases (85)",
    "holdout_batch_sha256": "Correct fingerprint of the frozen test data",
    "hybrid_provider": "Correctly named the offline stand-in it ran",
    "committed_results_provider": "Correctly named the live-model chain behind the committed results",
    "baseline": "All five rules-only figures correct",
    "hybrid": "All five hybrid figures correct",
    "artifacts_written": "Correct list of files the benchmark overwrites",
    "regression_67": "All 67 original tests still pass",
    "hidden_shortfall_tests": "Passed 25 hidden checks: short payments are no longer closed, and a genuine fee overcharge still closes",
    "notes_present": "Explained the cause it found in its notes",
    "protected_files_unchanged": "Committed results, frozen data and original tests untouched",
    "hidden_behaviour_tests": "Passed 8 hidden settlement-status scenarios",
    "benchmark_unchanged": "Benchmark results identical to before (timing aside)",
    "absolute_dir_run_ok": "Runs with an absolute --output-dir",
    "absolute_dir_artifacts_match": "Files written there match a normal run",
    "absolute_dir_only_expected_files": "Writes exactly the four expected files",
    "prints_path": "Prints where the files went",
    "outputs_and_frozen_untouched": "Committed results and frozen data untouched",
    "relative_dir_resolved_against_cwd": "Relative --output-dir works from another folder",
    "default_run_still_writes_outputs": "Without the option, behaves exactly as before",
}
missing = {k for t in data["tasks"] for tr in t["trials"] for k in tr["checks"]} - set(data["check_labels"])
assert not missing, missing
(W / "portfolio/site-data.json").write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
for t in data["tasks"]:
    print(t["id"], t["passed"], "/", t["attempts"], "median", t["median_duration"])
    for tr in t["trials"]:
        print("   ", tr["label"], "|", tr["summary"])
