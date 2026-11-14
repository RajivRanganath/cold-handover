"""Copy a reviewed, redacted subset of measured evidence into public-evidence/. Private runs/ is untouched.

Redactions (recorded in public-evidence/REDACTIONS.md):
- absolute paths under the home directory -> "~" ; attempt directory -> "<attempt>"
- rate_limit_event lines (account usage-window data) dropped from transcripts
- session / request / uuid identifiers dropped
- macOS username in `ls -l` listings ("USERNAME  staff") -> "user  staff"; encoded config paths "-Users-USERNAME-" -> "-Users-user-"; pytest temp dir "pytest-of-USERNAME" -> "pytest-of-user"
Nothing else is removed. Failed attempts are included exactly like passed ones.
"""
import difflib, json, re, shutil
from pathlib import Path

W = Path("/path/to/tms-work")
SNAP, PUB = W / "snapshot", W / "public-evidence"
HOME = "/path/to/home"
TOKEN = "".join((W / "agent-home/claude-oauth-token").read_text().split())
DROP_KEYS = {"session_id", "uuid", "request_id"}
SKIP = (".venv", "__pycache__", ".pytest_cache")


def redact(text: str, attempt: Path) -> str:
    text = text.replace(str(attempt), "<attempt>").replace(HOME, "~")
    text = re.sub(r"\bUSERNAME(\s+staff)", r"user\1", text).replace("-Users-USERNAME-", "-Users-user-").replace("pytest-of-USERNAME", "pytest-of-user")
    assert TOKEN not in text
    return text


def strip(o):
    if isinstance(o, dict):
        return {k: strip(v) for k, v in o.items() if k not in DROP_KEYS}
    if isinstance(o, list):
        return [strip(v) for v in o]
    return o


def transcript_md(events, attempt):
    out = []
    for e in events:
        if e.get("type") == "assistant":
            for b in e["message"].get("content", []):
                if b.get("type") == "text" and b["text"].strip():
                    out.append("**Agent:** " + b["text"].strip())
                elif b.get("type") == "tool_use":
                    i = b.get("input") or {}
                    body = i.get("command") or i.get("file_path") or json.dumps(i)
                    out.append(f"**{b['name']}:**\n```\n{body}\n```")
        elif e.get("type") == "user":
            for b in e["message"].get("content", []):
                if isinstance(b, dict) and b.get("type") == "tool_result":
                    c = b.get("content")
                    c = c if isinstance(c, str) else "\n".join(x.get("text", "") for x in c if isinstance(x, dict))
                    c = c if len(c) < 4000 else c[:4000] + f"\n... [{len(c) - 4000} more characters in transcript.jsonl]"
                    out.append(("**Result (error):**" if b.get("is_error") else "**Result:**") + f"\n```\n{c}\n```")
    return redact("\n\n".join(out), attempt)


def patch(repo: Path, attempt: Path) -> str:
    chunks = []
    files = {p.relative_to(repo).as_posix() for p in repo.rglob("*") if p.is_file()}
    files |= {p.relative_to(SNAP).as_posix() for p in SNAP.rglob("*") if p.is_file()}
    for f in sorted(files):
        if any(s in f.split("/") for s in SKIP):
            continue
        a, b = SNAP / f, repo / f
        old = a.read_text(errors="replace").splitlines(True) if a.exists() else []
        new = b.read_text(errors="replace").splitlines(True) if b.exists() else []
        if old != new:
            chunks += difflib.unified_diff(old, new, f"a/{f}", f"b/{f}")
    return redact("".join(chunks), attempt)


if PUB.exists():
    shutil.rmtree(PUB)
PUB.mkdir()
rows = json.loads((W / "results/attempts.json").read_text())
for r in rows:
    a, dst = W / "runs" / r["label"], PUB / r["task"] / r["label"]
    dst.mkdir(parents=True)
    events = [json.loads(l) for l in (a / "events.jsonl").read_text().splitlines() if l.startswith("{")]
    kept = [strip(e) for e in events if e.get("type") != "rate_limit_event"]
    (dst / "transcript.jsonl").write_text(redact("\n".join(json.dumps(e) for e in kept) + "\n", a))
    (dst / "transcript.md").write_text(f"# {r['label']} transcript ({r['outcome']})\n\n" + transcript_md(kept, a) + "\n")
    shutil.copy(a / "prompt.md", dst / "prompt.md")
    (dst / "agent_changes.patch").write_text(patch(a / "work/repo", a))
    for f in (a / "work/out").glob("*"):
        if f.is_file():
            (dst / f"out_{f.name}").write_text(redact(f.read_text(errors="replace"), a))
    if (a / "eval.json").exists():
        (dst / "evaluation.json").write_text(redact((a / "eval.json").read_text(), a))
    (dst / "record.json").write_text(json.dumps({k: v for k, v in r.items() if k != "start"} | {"start_utc": r.get("start")}, indent=2) + "\n")

shutil.copy(W / "results/results.md", PUB / "results.md")
shutil.copy(W / "results/attempts.json", PUB / "attempts.json")
for t in ("T1", "T2", "T3", "T4"):
    shutil.copy(W / f"tasks/{t}/prompt.md", PUB / t / "task_prompt.md")
(PUB / "protocol-lock.md").write_text((W / "protocol/protocol-lock.md").read_text().replace(HOME, "~"))
(PUB / "protocol-lock-round2.md").write_text((W / "protocol-r2/protocol-lock.md").read_text().replace(HOME, "~"))
(PUB / "REDACTIONS.md").write_text(
    "# Redactions applied to public-evidence/\n" + __doc__.split("REDACTIONS.md):")[1] +
    "\nNot included: credentials (verified absent), the private planning conversation, evaluator source and hidden tests "
    "(kept private so the tasks stay reusable; available on request), the owner's other repositories.\n")
leftover = [p for p in PUB.rglob("*") if p.is_file() and (HOME in p.read_text(errors="ignore") or TOKEN in p.read_text(errors="ignore"))]
print("files:", sum(1 for p in PUB.rglob("*") if p.is_file()), "| leftover home paths/tokens:", leftover or "none")
