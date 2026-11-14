#!/usr/bin/env bash
# One attempt = fresh repo copy + empty CLAUDE_CONFIG_DIR + new `claude -p` session, inside a
# seatbelt read/write boundary. Round 2 copy of run_attempt.sh (only the Claude Code version and evaluator differ). Usage: run_attempt_r2.sh <T4> <A|B> <label> [wall_seconds]
set -uo pipefail
TASK=$1 COND=$2 LABEL=$3 WALL=${4:-1800}
W=/path/to/tms-work
A=$W/runs/$LABEL
MODEL=claude-haiku-5-5
CLAUDE_BIN=/path/to/home/.local/share/claude/versions/2.1.325
TOKEN_FILE=$W/agent-home/claude-oauth-token
[ -s "$TOKEN_FILE" ] || { echo "missing $TOKEN_FILE (run: claude setup-token)"; exit 5; }
[ -e "$A" ] && { echo "refusing: $A exists (never overwrite an attempt)"; exit 2; }
mkdir -p "$A/work/out" "$A/work/tmp" "$A/claude-config"

# 1. Fresh repo copy + frozen env, prepared before the session starts
cp -R "$W/snapshot" "$A/work/repo" && chmod -R u+w "$A/work/repo"
env -i HOME="$A" PATH=/opt/homebrew/bin:/usr/bin:/bin "$W/env/install.sh" "$A/work/repo" || { echo "env install failed"; exit 3; }
if [ "$COND" = B ]; then cp "$W/handover/HANDOVER.md" "$A/work/repo/HANDOVER.md" || exit 4; fi
cp "$W/tasks/$TASK/prompt.md" "$A/prompt.md"

# 2. Sandbox profile
anc=""; p="$A"; while [ "$p" != "/" ]; do p=$(dirname "$p"); anc="$anc (literal \"$p\")"; done
sed -e "s#@ANCESTORS@#$anc#" -e "s#@ATTEMPT@#$A#g" -e "s#@CLAUDE_BIN@#$CLAUDE_BIN#g" -e "s#@SHIMS@#$W/harness/shims#g" "$W/harness/sandbox.sb.tmpl" > "$A/sandbox.sb"

# 3. Run: empty config dir => no CLAUDE.md, memory, hooks, plugins, skills, MCP, history.
{ echo "task=$TASK condition=$COND label=$LABEL model=$MODEL wall_limit_s=$WALL"
  echo "claude=$($CLAUDE_BIN --version) snapshot_manifest_sha256=$(shasum -a 256 $W/snapshot.sha256 | cut -c1-64)"
  echo "prompt_sha256=$(shasum -a 256 $A/prompt.md | cut -c1-64)"
  [ "$COND" = B ] && echo "handover_sha256=$(shasum -a 256 $A/work/repo/HANDOVER.md | cut -c1-64)"
  echo "start=$(date -u +%FT%TZ)"; } > "$A/meta.txt"
T0=$(date +%s)
cd "$A/work/repo"
perl -e 'alarm shift; exec @ARGV' "$WALL" \
  sandbox-exec -f "$A/sandbox.sb" \
  env -i HOME="$A/work" PATH="$W/harness/shims:/opt/homebrew/bin:/usr/bin:/bin" LANG=en_US.UTF-8 TMPDIR="$A/work/tmp" \
    CLAUDE_CONFIG_DIR="$A/claude-config" CLAUDE_CODE_OAUTH_TOKEN="$(tr -d "[:space:]" < "$TOKEN_FILE")" \
    CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 CLAUDE_CODE_TMPDIR="$A/work/tmp" TMPPREFIX="$A/work/tmp/zsh" \
  "$CLAUDE_BIN" -p "$(cat "$A/prompt.md")" --model "$MODEL" \
    --output-format stream-json --verbose --no-session-persistence \
    --dangerously-skip-permissions --strict-mcp-config --disable-slash-commands --disallowedTools WebSearch WebFetch \
  < /dev/null > "$A/events.jsonl" 2> "$A/stderr.txt"
RC=$?
{ echo "end=$(date -u +%FT%TZ)"; echo "wall_s=$(( $(date +%s) - T0 ))"; echo "agent_exit=$RC"; [ $RC = 142 ] && echo "outcome_hint=TIMEOUT"; } >> "$A/meta.txt"
cd "$W"

# 4. Credential scan: the token must not appear in any transcript or output.
python3 - "$A" "$TOKEN_FILE" <<'P' >> "$A/meta.txt"
import sys, pathlib
A, raw = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]).read_text()
needles = {"".join(raw.split())} | {l.strip() for l in raw.splitlines() if len(l.strip()) > 24}
hits = [str(p.relative_to(A)) for p in A.rglob("*") if p.is_file() and ".venv" not in p.parts
        and any(n in p.read_text(errors="ignore") for n in needles)]
print("credential_leak_files=" + (",".join(hits) if hits else "none"))
P

# 5. Telemetry from the final result event
python3 - "$A/events.jsonl" <<'P' >> "$A/meta.txt"
import json, sys, collections
ev = [json.loads(l) for l in open(sys.argv[1]) if l.strip().startswith("{")]
init = next((e for e in ev if e.get("type") == "system" and e.get("subtype") == "init"), {})
res = next((e for e in reversed(ev) if e.get("type") == "result"), None)
tools = collections.Counter(b.get("name") for e in ev if e.get("type") == "assistant"
                            for b in (e.get("message") or {}).get("content", []) if b.get("type") == "tool_use")
print("session_model=" + str(init.get("model")) + " loaded_tools=" + str(len(init.get("tools", []))) +
      " mcp=" + str(init.get("mcp_servers")) + " plugins=" + str(init.get("plugins")))
print("tool_calls=" + json.dumps(dict(tools)))
retries = [e for e in ev if e.get("subtype") == "api_retry"]
print("api_retries=" + str(len(retries)) + " retry_errors=" + json.dumps(sorted({str(e.get("error_status")) + ":" + str(e.get("error")) for e in retries})))
rl = [e["rate_limit_info"] for e in ev if e.get("type") == "rate_limit_event"]
if rl: print("plan_window=" + json.dumps({k: rl[-1].get(k) for k in ("rateLimitType", "isUsingOverage", "overageStatus")}) + " utilization=" + str([r.get("unifiedWindows", {}).get("five_hour", {}).get("utilization") for r in rl]))
# usage below = final authoritative totals; per-message stream usage is a partial snapshot and is not summed
if res:
    print("result=" + json.dumps({k: res.get(k) for k in ("subtype", "is_error", "num_turns", "duration_ms", "duration_api_ms", "total_cost_usd")}))
    print("usage=" + json.dumps(res.get("usage")))
else:
    print("result=unavailable")
P

# 6. Independent evaluation, outside the sandbox, on a copy
if [ "$TASK" != T0 ]; then
  python3 "$W/evaluator/evaluate_r2.py" "$TASK" "$A/work" "$W/evaluator/scratch/$LABEL" > "$A/eval.json" 2>&1
  echo "eval_exit=$?" >> "$A/meta.txt"
fi
cat "$A/meta.txt"
