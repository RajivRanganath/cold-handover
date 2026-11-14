# M-T1-02 transcript (PASS)

**Agent:** I'll start by reading the handover documentation at the repository root, as the ground rules require.

**Bash:**
```
ls -la && find . -path ./.venv -prune -o -type f -print | grep -v __pycache__ | head -200
```

**Result:**
```
total 88
drwxr-xr-x@ 10 user  staff    320 Nov  1 23:29 .
drwxr-xr-x@  5 user  staff    160 Nov  1 23:29 ..
-rw-r--r--@  1 user  staff   1992 Nov  1 23:29 .env.example
-rw-r--r--@  1 user  staff     56 Nov  1 23:29 .gitignore
drwxr-xr-x@  7 user  staff    224 Nov  1 23:29 .venv
drwxr-xr-x@  7 user  staff    224 Nov  1 23:29 docs
drwxr-xr-x@ 14 user  staff    448 Nov  1 23:29 ledgerguard
-rw-r--r--@  1 user  staff  26848 Nov  1 23:29 README.md
-rw-r--r--@  1 user  staff    466 Nov  1 23:29 requirements.txt
-rwxr-xr-x@  1 user  staff   1447 Nov  1 23:29 run_demo.sh
./requirements.txt
./README.md
./run_demo.sh
./.gitignore
./.env.example
./docs/architecture.md
./docs/limitations.md
./docs/model_comparison.md
./docs/analyses.md
./docs/evaluation.md
./ledgerguard/__init__.py
./ledgerguard/pipeline.py
./ledgerguard/qa.py
./ledgerguard/reconciliation/matcher.py
./ledgerguard/reconciliation/__init__.py
./ledgerguard/reconciliation/exceptions.py
./ledgerguard/ledger/shadow_ledger.py
./ledgerguard/ledger/models.py
./ledgerguard/ledger/__init__.py
./ledgerguard/ledger/money.py
./ledgerguard/ledger/invariants.py
./ledgerguard/evidence/__init__.py
./ledgerguard/evidence/safety.py
./ledgerguard/evidence/verifier.py
./ledgerguard/frontend/index.html
./ledgerguard/tests/test_p0_core.py
./ledgerguard/tests/test_p2_evaluation.py
./ledgerguard/tests/test_p1_compound.py
./ledgerguard/tests/__init__.py
./ledgerguard/tests/test_p1_extended.py
./ledgerguard/tests/test_fallback.py
./ledgerguard/tests/test_evidence_download.py
./ledgerguard/tests/rehearsal_check.py
./ledgerguard/tests/test_dashboard_startup.py
./ledgerguard/backend/__init__.py
./ledgerguard/backend/app.py
./ledgerguard/ai/provider.py
./ledgerguard/ai/openai_compatible.py
./ledgerguard/ai/__init__.py
./ledgerguard/ai/schemas.py
./ledgerguard/ai/errors.py
./ledgerguard/ai/investigator.py
./ledgerguard/ai/fallback.py
./ledgerguard/synthetic/fault_injector.py
./ledgerguard/synthetic/adversarial.py
./ledgerguard/synthetic/__init__.py
./ledgerguard/synthetic/generator.py
./ledgerguard/synthetic/compound.py
./ledgerguard/evaluation/metrics.py
./ledgerguard/evaluation/benchmark.py
./ledgerguard/evaluation/baseline.py
./ledgerguard/evaluation/ablation.py
./ledgerguard/evaluation/drift.py
./ledgerguard/evaluation/__init__.py
./ledgerguard/evaluation/no_gate_ablation.py
./ledgerguard/evaluation/replay.py
./ledgerguard/evaluation/model_comparison.py
./ledgerguard/evaluation/cost.py
./ledgerguard/evaluation/scale.py
./ledgerguard/evaluation/report.py
./ledgerguard/evaluation/calibration.py
./ledgerguard/evaluation/frozen/holdout_20260905_320.json
./ledgerguard/evaluation/outputs/reconciliation_report.csv
./ledgerguard/evaluation/outputs/scale.json
./ledgerguard/evaluation/outputs/calibration.json
./ledgerguard/evaluation/outputs/no_gate_ablation.json
./ledgerguard/evaluation/outputs/scale.md
./ledgerguard/evaluation/outputs/reconciliation_report.md
./ledgerguard/evaluation/outputs/ablation.json
./ledgerguard/evaluation/outputs/calibration.md
./ledgerguard/evaluation/outputs/benchmark.json
./ledgerguard/evaluation/outputs/model_comparison.md
./ledgerguard/evaluation/outputs/drift.json
./ledgerguard/evaluation/outputs/benchmark.md
./ledgerguard/evaluation/outputs/model_comparison.json
./ledgerguard/evaluation/outputs/cases.json
./ledgerguard/evaluation/outputs/unresolved_exceptions.csv
./ledgerguard/evaluation/outputs/evidence_ledger.csv
./ledgerguard/evaluation/outputs/drift.md
./ledgerguard/evaluation/outputs/decision_log.json
./ledgerguard/evaluation/outputs/no_gate_ablation.md
./ledgerguard/evaluation/outputs/ablation.md
```

**Read:**
```
<attempt>/work/repo/README.md
```

**Result:**
```
1	# LedgerGuard
2	
3	**A self verifying AI finance controller.** Razorpay AI Buildathon, Track 04.
4	
5	The workflow is settlement reconciliation: inspect the source records, verify an
6	ambiguous refund, and export the exceptions that still need a human.
7	
8	I built LedgerGuard to answer a question that a reconciliation chatbot does not
9	answer: an LLM can generate a plausible explanation for a financial discrepancy
10	in about two seconds — but how do you know whether that explanation is
11	*financially true*?
12	
13	**The core claim: LLM reasoning is not financial truth. Financial truth is
14	deterministic accounting state plus verified evidence. The AI may propose, the
15	financial system must prove.**
16	
17	## Quick start
18	
19	```bash
20	git clone https://github.com/RajivRanganath/ledgerguard.git && cd ledgerguard
21	python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
22	./run_demo.sh          # tests, then benchmark, then http://127.0.0.1:8137
23	```
24	
25	**No API key is needed.** Without one the AI investigation step degrades to an
26	offline stand-in and says so on the page; the deterministic engine, Shadow
27	Ledger, Evidence Gate, benchmark and dashboard all run unchanged.
28	
29	---
30	
31	## Where to verify each published requirement
32	
33	Track 04, AI Finance Controller, checked against the official Buildathon page.
34	The official description does not mandate multiple agents, a particular frontend
35	framework, or a Razorpay payment API integration. Synthetic settlement
36	reconciliation is the chosen workflow, and no payment is ever initiated.
37	
38	| Published requirement | Where to verify it |
39	|---|---|
40	| One finance-operations loop | Dashboard: records → investigation → checks → disposition → exception report |
41	| At least 50 synthetic records | 320 generated lifecycles; 85 held out and frozen for the benchmark |
42	| Match rate | `evaluation/outputs/benchmark.json` — `baseline.match_rate`, `hybrid.match_rate` |
43	| Throughput and measured accuracy | Same artifact; wall-clock figures include provider latency |
44	| Exceptions that could not be resolved | Dashboard exception queue, and `evaluation/outputs/unresolved_exceptions.csv` |
45	| Architecture | [`docs/architecture.md`](docs/architecture.md) |
46	
47	---
48	
49	## What it does
50	
51	LedgerGuard reconciles orders, payments, refunds, settlements and bank records.
52	
53	1. **The Shadow Ledger** independently reconstructs what the money movement
54	   *should* have been, from first principles:
55	   `expected_net = captured − refunds − fees − tax ± valid adjustments`.
56	   It never reads settlement or bank records to decide what to expect. Six named
57	   invariants (`I1`–`I6`) compare that reconstruction against what the provider
58	   actually reported. All money is integer paise; no float ever touches it.
59	
60	2. **A deterministic engine reconciles everything it can prove** — exact
61	   identifier matching, settlement arithmetic against the fee schedule,
62	   duplicate detection, timing windows, bank matching. On the frozen holdout it
63	   resolves 54 of 85 cases with zero AI involvement, and never sends a case to
64	   the model that it could prove on its own.
65	
66	3. **The AI investigator only sees what could not be proved.** It gets the
67	   records, the Shadow Ledger's expected value, the discrepancy, the permitted
68	   hypothesis taxonomy, and candidate related records. It returns structured
69	   JSON only. It is instructed not to calculate money; its prose is not used for
70	   monetary computation. It has no record-editing or case-closing tools.
71	
72	4. **The Evidence Gate re-proves every claim.** If the model says a shortfall is
73	   a partial refund, the gate checks whether that refund exists, whether it is
74	   already owned by another payment, whether its reference identifies *this*
75	   order's customer, whether the amount matches, whether the timing is possible,
76	   and whether re-running
... [24789 more characters in transcript.jsonl]
```

**Bash:**
```
cat run_demo.sh && cat .gitignore && cat .env.example && cat requirements.txt && find . -path ./.venv -prune -o -type f -print0 | xargs -0 shasum -a 256 > <attempt>/work/tmp_manifest_before.txt 2>/dev/null; mkdir -p ../tmp; cp /dev/null /dev/null; wc -l ../tmp_manifest_before.txt 2>/dev/null; ls -la ..
```

**Result:**
```
#!/usr/bin/env bash
# Reliable local demo. One command, no arguments.
set -euo pipefail
cd "$(dirname "$0")"

PY=.venv/bin/python
if [ ! -x "$PY" ]; then
  echo "Creating virtualenv..."
  python3 -m venv .venv
  .venv/bin/pip install -q --upgrade pip
  .venv/bin/pip install -q -r requirements.txt
fi

echo "Running the P0 test suite..."
$PY -m pytest ledgerguard/tests -q

echo
echo "Regenerating the benchmark from the frozen holdout..."
$PY -m ledgerguard.evaluation.benchmark >/dev/null
echo "  -> ledgerguard/evaluation/outputs/benchmark.md"

echo
echo "Starting the dashboard..."
$PY -m uvicorn ledgerguard.backend.app:app --port 8137 --log-level warning &
SERVER_PID=$!
trap 'kill $SERVER_PID 2>/dev/null' EXIT

# The server runs the controller once at startup. With a live investigator that
# is ~17 sequential model calls (15 holdout exceptions plus the adversarial
# pair), so warm it before announcing readiness rather
# than letting the first page load block for minutes mid-demo.
echo "Warming up (this runs the controller once; with a live model it takes a few minutes)..."
until curl -sf http://127.0.0.1:8137/api/health >/dev/null 2>&1; do
  kill -0 $SERVER_PID 2>/dev/null || { echo "server exited during warmup"; exit 1; }
  sleep 2
done

echo
echo "Verifying every demo beat..."
$PY -m ledgerguard.tests.rehearsal_check | tail -5

echo
echo "LedgerGuard dashboard: http://127.0.0.1:8137"
echo "Ctrl-C to stop."
wait $SERVER_PID
.venv/
__pycache__/
*.pyc
.env
.pytest_cache/
.DS_Store
# LedgerGuard reads one API key and runs without any of them.
#
# With no key set, the AI investigator falls back to an offline stand-in and
# every run report says so. The deterministic engine, Shadow Ledger, Evidence
# Gate, benchmark and dashboard all work unchanged.
#
# Set as many as you have. With more than one configured, the default `auto`
# provider builds a FALLBACK CHAIN in this order and fails over automatically
# when a provider runs out of quota, is rate limited, or starts returning
# unparseable output:
#
#   groq -> gemini -> nvidia -> omniroute -> offline stub
#
# Within each provider it also rotates between model routes (13 routes total).
# OmniRoute sits last and is the deepest link: it fronts Mistral, NVIDIA and
# Groq under its own separate credentials, so it survives the direct keys above
# running out.
#
# All four are FREE TIERS. No paid API key is used anywhere in this project, and
# none is needed to reproduce any published number.

GROQ_API_KEY=gsk_your-key-here             # openai/gpt-oss-120b
# GEMINI_API_KEY=your-key-here              # gemini-2.5-flash
# NVIDIA_API_KEY=nvapi-your-key-here        # openai/gpt-oss-120b
# OMNIROUTE_API_KEY=sk-your-key-here        # local `omniroute` CLI on :20128,
#                                           # fronts OpenRouter/OpenCode/Mistral/...

# Optional overrides.
# LEDGERGUARD_PROVIDER=fallback    # groq|gemini|nvidia|omniroute|
#                                  # openai_compatible|fallback|stub|none|auto
# LEDGERGUARD_NO_CACHE=1           # omit temperature, to defeat OmniRoute's
#                                  # temperature-0 response cache
# LEDGERGUARD_MODEL=               # override the provider's default model
# LEDGERGUARD_REASONING_EFFORT=low # for reasoning models on OpenAI-compatible hosts

# Any other OpenAI-compatible host:
# LEDGERGUARD_PROVIDER=openai_compatible
# LEDGERGUARD_BASE_URL=https://your-host/v1
# LEDGERGUARD_API_KEY=your-key-here
# LEDGERGUARD_MODEL=your-model
# Runtime
fastapi>=0.115
httpx>=0.27          # every OpenAI-compatible and Gemini provider, and the
                     # OmniRoute reachability probe, call it directly
pydantic>=2.9
uvicorn>=0.30

# Not installed by default. `AnthropicProvider` is kept as the reference
# implementation of the provider interface, but this project runs on free tiers
# only and never calls it. Its import is lazy, so nothing else needs it.
# anthropic>=1.0.0

# Tests
pytest>=8.0
cp: /dev/null and /dev/null are identic
... [385 more characters in transcript.jsonl]
```

**Agent:** The manifest landed one level above `../tmp/`, which the ground rules don't allow. I'll move it into `../tmp/` and then read the benchmark code to see what it writes.

**Bash:**
```
cd <attempt>/work && mv tmp_manifest_before.txt tmp/ && ls tmp out && cd repo && cat ledgerguard/evaluation/benchmark.py
```

**Result:**
```
out:

tmp:
cc-socks
claude-501
tmp_manifest_before.txt
"""One-command benchmark.

    python -m ledgerguard.evaluation.benchmark

Regenerates the dataset from its seed, freezes (or re-verifies) the holdout
manifest, runs the rules-only baseline and the full hybrid controller over the
same frozen holdout, and writes every artifact under evaluation/outputs/.

Every number in every artifact comes from these two runs; nothing is typed in
by hand. Rerunning with the same seed reproduces the deterministic path exactly
-- same dispositions, same money, same unresolved rows, byte for byte, with only
wall-clock timing fields differing. The AI-investigated path is not reproducible
in that sense: the same prompt to the same model can yield a different
hypothesis, so a live rerun can land on a different accuracy. Runs are labelled
with the investigator that produced them for exactly this reason.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from dataclasses import asdict
from pathlib import Path

from ..ai.provider import get_provider
from ..evidence.safety import AUTO_RESOLVED
from ..ledger.money import to_rupees_str
from ..pipeline import RunReport, run
from ..synthetic.fault_injector import build_dataset, split
from ..synthetic.generator import Dataset
from .cost import estimate
from .metrics import Metrics, compute

OUTPUT_DIR = Path(__file__).parent / "outputs"
MANIFEST_DIR = Path(__file__).parent / "frozen"


def manifest_path(seed: int, count: int) -> Path:
    """One frozen manifest per dataset configuration.

    Keyed by config so that running the benchmark with a different seed or size
    can never silently overwrite the holdout an earlier result was scored on.
    """
    return MANIFEST_DIR / f"holdout_{seed}_{count}.json"


def batch_digest(dataset: Dataset) -> str:
    return hashlib.sha256(dataset.batch().model_dump_json().encode()).hexdigest()


def freeze_or_verify_holdout(holdout: Dataset, seed: int, count: int) -> dict:
    """Write the holdout manifest once; afterwards, verify nothing drifted."""
    manifest = {
        "seed": seed,
        "count": count,
        "generator_version": holdout.generator_version,
        "holdout_lifecycle_ids": sorted(lc.lifecycle_id for lc in holdout.lifecycles),
        "holdout_batch_sha256": batch_digest(holdout),
    }
    path = manifest_path(seed, count)
    if path.exists():
        existing = json.loads(path.read_text())
        if existing != manifest:
            raise SystemExit(
                "FROZEN HOLDOUT MISMATCH.\n"
                "The holdout for this seed was frozen earlier and the regenerated "
                "data no longer matches it. Scoring against a changed holdout is "
                "not a valid measurement. Investigate the generator change, or "
                "delete the manifest deliberately and say so in the write-up.\n"
                f"  frozen sha256:      {existing.get('holdout_batch_sha256')}\n"
                f"  regenerated sha256: {manifest['holdout_batch_sha256']}"
            )
        return existing
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def _row(label: str, baseline, hybrid, fmt=str) -> str:
    return f"| {label} | {fmt(baseline)} | {fmt(hybrid)} |"


def render_markdown(base: Metrics, hyb: Metrics, manifest: dict) -> str:
    def inr(paise: int) -> str:
        return f"INR {to_rupees_str(paise)}"

    lines = [
        "# Benchmark: rules only vs LedgerGuard",
        "",
        f"Frozen holdout, seed `{manifest['seed']}`, generator `{manifest['generator_version']}`, "
        f"{len(manifest['holdout_lifecycle_ids'])} lifecycles, "
        f"batch SHA-256 `{manifest['holdout_batch_sha256'][:16]}`.",
        "",
        f"Investigator for the hybrid run: `{hyb.provider}`.",
        "",
        "Generated by `python -m ledgerguard.evaluation.benchmark`. Every figure below "
        "come
... [12071 more characters in transcript.jsonl]
```

**Agent:** The benchmark overwrites four files under `outputs/`, so I need to back those up before running. Next I'll check the provider selection with no key set and find any other file writes, including caches.

**Bash:**
```
grep -rn "write_text\|write_bytes\|open(\|mkdir\|\.write(\|cache\|tempfile\|\.csv\b" ledgerguard --include=*.py | grep -v "/tests/" ; echo ----; cat ledgerguard/ai/provider.py | head -150; echo ----; cat ledgerguard/evaluation/outputs/benchmark.json | head -60
```

**Result:**
```
(eval):1: no matches found: --include=*.py
----
"""AI provider interface.

The rest of LedgerGuard depends on exactly one function shape:

    investigate(context: dict) -> InvestigationResult

Several implementations ship. ``AnthropicProvider`` calls Claude through the
Anthropic SDK, ``OpenAICompatibleProvider`` and ``GeminiProvider`` (in
``openai_compatible.py``) cover every other host, and ``FallbackProvider`` (in
``fallback.py``) chains them so one running out of quota does not end the run.
``HeuristicProvider`` is an offline stand-in that lets the whole pipeline,
benchmark and demo run with no API key present -- it is deliberately naive,
because a naive investigator is exactly what the Evidence Gate has to survive.
Every result records which provider produced it; the benchmark report prints
that, so a stub run is never mistaken for a model run.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Protocol

from .errors import ProviderNotConfigured
from .schemas import InvestigationResult, InvestigatorOutput, RequiredEvidence

def _load_dotenv() -> None:
    """Read .env from the repo root if present. Never overrides a real env var."""
    path = Path(__file__).resolve().parent.parent.parent / ".env"
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip())


_load_dotenv()

DEFAULT_MODEL = "claude-opus-5"
DEFAULT_TIMEOUT_SECONDS = 45.0
DEFAULT_MAX_TOKENS = 2000

SYSTEM_PROMPT = """You are the exception investigator inside LedgerGuard, a payments \
reconciliation controller.

A deterministic engine has already reconciled everything it could prove. You only \
ever see exceptions it could not resolve. Your job is to propose the single most \
likely explanation and point at the specific records that would prove it. You are \
not the decision maker: an independent Evidence Gate re-checks every claim you make \
against the actual records, and it will reject you if the evidence does not hold.

Rules you must follow:
- Never perform monetary arithmetic. The expected values you are given were computed \
by an independent Shadow Ledger; use them, do not recompute them.
- Never invent an identifier. Every id in candidate_evidence_ids must appear verbatim \
somewhere in the context you were given.
- Never force a resolution. If the available records do not contain enough evidence to \
prove an explanation, return hypothesis "insufficient_evidence" and \
recommended_action "review".
- A candidate refund matching the discrepancy on amount is not proof of linkage. Say \
what relationship would have to hold for your hypothesis to be true, and let the gate \
check it.
- recommended_action "resolve" is a request, not a decision. Use it only when you \
believe every required_evidence item can be verified from the records shown."""


class InvestigatorProvider(Protocol):
    name: str

    def investigate(self, context: dict) -> InvestigationResult:  # pragma: no cover
        ...


def _to_result(out: InvestigatorOutput, source: str, model_name: str | None) -> InvestigationResult:
    return InvestigationResult(
        hypothesis=out.hypothesis,
        reason=out.reason,
        required_evidence=out.required_evidence,
        candidate_evidence_ids=out.candidate_evidence_ids,
        recommended_action=out.recommended_action,
        source=source,
        model_name=model_name,
    )


class AnthropicProvider:
    """Claude-backed investigator using structured outputs."""

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        timeout: float = DEFAULT_TIMEOUT_SECONDS,
        max_tokens: int = DEFAULT_MAX_TOKENS,
    ) -> None:
        import anthropic

        self.name = f"anthropic:{model}"
        self.model
... [3195 more characters in transcript.jsonl]
```

**Agent:** The committed `benchmark.json` is the source for `committed_results_provider`, so I'll record it before anything runs. I'll also look at how `get_provider` picks a provider with no key, and rerun the write-site search.

**Bash:**
```
cp ledgerguard/evaluation/outputs/benchmark.json ../tmp/committed_benchmark.json && grep -n '"provider"\|"investigator\|"name"\|"chain"\|"served_by"' ledgerguard/evaluation/outputs/benchmark.json | head; echo ----; sed -n 150,400p ledgerguard/ai/provider.py | grep -n "def get_provider" -A60; echo ----; grep -rn "write_text\|write_bytes\|open(\|mkdir\|tempfile" ledgerguard --include=*.py | grep -v tests/; echo ----; env | grep -c "API_KEY" ; env | grep -o "^[A-Z_]*API_KEY\|^LEDGERGUARD[A-Z_]*" 
```

**Result:**
```
105:    "provider": "none",
193:    "provider": "fallback(groq->gemini->nvidia->omniroute)",
279:  "investigator_chain": {
280:    "chain": [
286:    "served_by": {
----
164:def get_provider(kind: str | None = None) -> InvestigatorProvider:
165-    """Select an investigator provider.
166-
167-    ``kind`` (or LEDGERGUARD_PROVIDER) may be:
168-      groq | gemini | nvidia | omniroute | openai_compatible
169-                          -- one specific provider (anthropic and cerebras are
170-                             still constructible but are not used here)
171-      fallback            -- chain every configured provider, failing over
172-      stub                -- the offline stand-in
173-      none                -- a dead provider, for testing degradation
174-      auto                -- fallback across everything configured, else the stub
175-
176-    A provider that is named explicitly but cannot be configured is an error,
177-    not a silent downgrade: a run that was meant to measure a model must never
178-    quietly report stub numbers instead.
179-    """
180-    kind = (kind or os.environ.get("LEDGERGUARD_PROVIDER") or "auto").lower()
181-    if kind == "none":
182-        return UnavailableProvider()
183-    if kind == "stub":
184-        return HeuristicProvider()
185-
186-    if kind not in ("auto", "fallback"):
187-        return _build(kind)
188-
189-    from .fallback import FallbackProvider
190-
191-    chain = build_chain()
192-    if not chain:
193-        if kind == "fallback":
194-            raise ValueError("no providers are configured, so no chain can be built")
195-        return HeuristicProvider()
196-    if len(chain) == 1 and kind == "auto":
197-        return chain[0]
198-    return FallbackProvider(chain)
----
(eval):1: no matches found: --include=*.py
----
0
```

**Agent:** The committed file records the hybrid provider as a fallback chain, and no API keys are set in the environment. I'll confirm the exact committed string and rerun the write-site search with a corrected command.

**Bash:**
```
sed -n 100,108p ledgerguard/evaluation/outputs/benchmark.json; sed -n 188,196p ledgerguard/evaluation/outputs/benchmark.json; sed -n 279,300p ledgerguard/evaluation/outputs/benchmark.json; echo ----; grep -rn -e "write_text" -e "write_bytes" -e "open(" -e "mkdir" -e "tempfile" -e "\.write(" ledgerguard | grep -v "/tests/"; echo ----; grep -n "def build_chain" -A30 ledgerguard/ai/provider.py | head -45
```

**Result:**
```
    ],
    "holdout_batch_sha256": "3e28d4572d4cfc95a7ebd5ad1a04531475e0044e63eb1c732e38e303866f20fa"
  },
  "baseline": {
    "system": "Rules only (baseline)",
    "provider": "none",
    "false_auto_resolutions": 0,
    "false_auto_resolved_value_paise": 0,
    "total_cases": 85,
    "unresolved_value_inr": "191780.59",
    "total_value_inr": "2493357.00"
  },
  "hybrid": {
    "system": "LedgerGuard (hybrid)",
    "provider": "fallback(groq->gemini->nvidia->omniroute)",
    "false_auto_resolutions": 0,
    "false_auto_resolved_value_paise": 0,
    "total_cases": 85,
  "investigator_chain": {
    "chain": [
      "groq:openai/gpt-oss-120b",
      "gemini:gemini-2.5-flash",
      "nvidia:nvidia/llama-3.1-nemotron-70b-instruct",
      "omniroute:mistral/mistral-large-latest"
    ],
    "served_by": {
      "groq:openai/gpt-oss-120b": 15
    },
    "retired": {},
    "cache_hits": {},
    "routes_exhausted": {}
  }
}
----
ledgerguard/evaluation/no_gate_ablation.py:151:    (OUTPUT_DIR / "no_gate_ablation.json").write_text(json.dumps(r, indent=2) + "\n")
ledgerguard/evaluation/no_gate_ablation.py:153:    (OUTPUT_DIR / "no_gate_ablation.md").write_text(md)
ledgerguard/evaluation/drift.py:163:    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
ledgerguard/evaluation/drift.py:165:    (OUTPUT_DIR / "drift.md").write_text(md)
ledgerguard/evaluation/drift.py:166:    (OUTPUT_DIR / "drift.json").write_text(
ledgerguard/evaluation/scale.py:144:    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
ledgerguard/evaluation/scale.py:146:    (OUTPUT_DIR / "scale.md").write_text(md)
ledgerguard/evaluation/scale.py:147:    (OUTPUT_DIR / "scale.json").write_text(
ledgerguard/evaluation/ablation.py:411:    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
ledgerguard/evaluation/ablation.py:413:    (OUTPUT_DIR / "ablation.md").write_text(md)
ledgerguard/evaluation/ablation.py:414:    (OUTPUT_DIR / "ablation.json").write_text(
ledgerguard/evaluation/model_comparison.py:170:    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
ledgerguard/evaluation/model_comparison.py:172:    (OUTPUT_DIR / "model_comparison.md").write_text(md)
ledgerguard/evaluation/model_comparison.py:173:    (OUTPUT_DIR / "model_comparison.json").write_text(
ledgerguard/evaluation/benchmark.py:76:    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
ledgerguard/evaluation/benchmark.py:77:    path.write_text(json.dumps(manifest, indent=2) + "\n")
ledgerguard/evaluation/benchmark.py:153:    with path.open("w", newline="") as fh:
ledgerguard/evaluation/benchmark.py:235:    path.write_text(json.dumps(payload, indent=2, default=str) + "\n")
ledgerguard/evaluation/benchmark.py:254:    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
ledgerguard/evaluation/benchmark.py:277:    (OUTPUT_DIR / "benchmark.md").write_text(md)
ledgerguard/evaluation/benchmark.py:278:    (OUTPUT_DIR / "benchmark.json").write_text(
ledgerguard/evaluation/replay.py:153:    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
ledgerguard/evaluation/replay.py:155:    path.write_text(json.dumps(captured, indent=2, default=str) + "\n")
ledgerguard/evaluation/calibration.py:167:    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
ledgerguard/evaluation/calibration.py:168:    (OUTPUT_DIR / "calibration.md").write_text(md)
ledgerguard/evaluation/calibration.py:169:    (OUTPUT_DIR / "calibration.json").write_text(
ledgerguard/evaluation/report.py:48:    output_dir.mkdir(parents=True, exist_ok=True)
ledgerguard/evaluation/report.py:51:    with (output_dir / "reconciliation_report.csv").open("w", newline="") as fh:
ledgerguard/evaluation/report.py:106:    with (output_dir / "evidence_ledger.csv").open("w", newline="") as fh:
ledgerguard/evaluation/report.py:148:    (output_dir / "reconciliation_report.md").write_text("\n".join(md) + "\n")
----
279:def build_chain(order: list[str] | None = None) -> list[InvestigatorProvider]:
280-    """Every provider that is actually configured, in preference order.
281-
282-    A provider with no key is skipped quiet
... [1564 more characters in transcript.jsonl]
```

**Agent:** The write sites are clear: the benchmark overwrites four files in `outputs/`, and the frozen manifest is only written if missing. Before running, I'll back up the whole `outputs/` and `frozen/` directories to `../tmp/` so I can restore them exactly.

**Bash:**
```
cd <attempt>/work && mkdir -p tmp/backup && cp -Rp repo/ledgerguard/evaluation/outputs tmp/backup/outputs && cp -Rp repo/ledgerguard/evaluation/frozen tmp/backup/frozen && cd repo && shasum -a 256 ledgerguard/evaluation/outputs/* ledgerguard/evaluation/frozen/* > ../tmp/backup/sha_before.txt && cat ../tmp/backup/sha_before.txt && sed -n 1,40p ledgerguard/ai/provider.py >/dev/null && grep -n "def _build" -A25 ledgerguard/ai/provider.py | head -40
```

**Result:**
```
7ffa151674c19541ac0b4cf9a8618b4c5a8eef664afd9ab81321961848cecd03  ledgerguard/evaluation/outputs/ablation.json
fc84418ada9f206e10f07170d5c3e362c531474c13abefed04eadabf32c6cda2  ledgerguard/evaluation/outputs/ablation.md
249e3bce69daeb83386d9575e66bf4177d4db885a8864ab6b32d80b5717d8536  ledgerguard/evaluation/outputs/benchmark.json
aa667ebea4ccd41fa0bdff898182200d3bf282ef0b888cabd7b5a215d82edd22  ledgerguard/evaluation/outputs/benchmark.md
8dc1212f1c93e7c1bf34d92923c1d31f15b7096a0b39e4c2afa4e167f4eda9d4  ledgerguard/evaluation/outputs/calibration.json
bbfc6509ce38c53329da95bde380675d231fcfbb15efd4428252aae3eef32d12  ledgerguard/evaluation/outputs/calibration.md
a5552fcb48631411cb08fae4e34987295cca132334d6c31d86601f73e538455b  ledgerguard/evaluation/outputs/cases.json
c52561e7f550a9c66a045bd6aaebd91f8883f120a624bf773d2a3dfae1753c7d  ledgerguard/evaluation/outputs/decision_log.json
ac427b5c78460109ba2fb3914c2d04310e80089ea245dcf44f426bc2da5562a7  ledgerguard/evaluation/outputs/drift.json
b3ceedf8b7067eb970ee33a6f7802ea154a10aa6fcbabe903b7880a0cd5634dc  ledgerguard/evaluation/outputs/drift.md
3699ea28a60eed7b419b027283ae1a9a3875eeb7c43e674adddfc0d195aa50c1  ledgerguard/evaluation/outputs/evidence_ledger.csv
1fbca2999ea5f5b76d810ac2955beb5fca7bc5af165320a752be60dbe4b96100  ledgerguard/evaluation/outputs/model_comparison.json
b877b4cdb9f9dfc33ff7ad0e82915e3e6fad2b84ccd8e3e9170943758834ff4d  ledgerguard/evaluation/outputs/model_comparison.md
ccc33093b532b19e326ed4ac8f8d16d29645807f3fe97841a10dc7d242f57917  ledgerguard/evaluation/outputs/no_gate_ablation.json
b2aa14f8b312f1a735663b70b69137f2df190ab9ef731c51c31def8d05bd14e4  ledgerguard/evaluation/outputs/no_gate_ablation.md
c58809b7c6b57a77dd33ce948b09988c6c9ded01bacb052b2f4f9b2d5193d6d7  ledgerguard/evaluation/outputs/reconciliation_report.csv
7a9f6520bbeb849b4e6f1f15a78f39a608583c6776c7c310457ed053a82dd41c  ledgerguard/evaluation/outputs/reconciliation_report.md
530301222288c5c487d56e9029f570bd01720e1fdbd306c90b9f71c71488cd4b  ledgerguard/evaluation/outputs/scale.json
227f79916be1cbe13addb7096e2f0f453660e2dc4ef83e4081ff8bcbee2ef9cf  ledgerguard/evaluation/outputs/scale.md
af74f00254d9a8cee944bccdf9fd8940c2a318c0bfd5c6965dbfc5a221e00711  ledgerguard/evaluation/outputs/unresolved_exceptions.csv
06f71351dd21bdcdb30705986832111987fe71ff6d6787ed2a198c88de50a53f  ledgerguard/evaluation/frozen/holdout_20260905_320.json
240:def _build(kind: str) -> InvestigatorProvider:
241-    if kind == "anthropic":
242-        if not os.environ.get("ANTHROPIC_API_KEY"):
243-            raise ProviderNotConfigured("ANTHROPIC_API_KEY is not set")
244-        return AnthropicProvider(model=os.environ.get("LEDGERGUARD_MODEL", DEFAULT_MODEL))
245-    if kind == "gemini":
246-        from .openai_compatible import GeminiProvider
247-
248-        return GeminiProvider(model=os.environ.get("LEDGERGUARD_MODEL", "gemini-2.5-flash"))
249-    from .openai_compatible import PRESETS, OpenAICompatibleProvider
250-
251-    if kind == "omniroute":
252-        # Local router: a configured key proves nothing if the process is not
253-        # running, so reachability is part of "is this provider available".
254-        # Without this probe, auto-detection would select a dead endpoint and
255-        # every investigation would degrade to abstention.
256-        import httpx
257-
258-        try:
259-            httpx.get("http://localhost:20128/v1/models", timeout=3.0).raise_for_status()
260-        except Exception as exc:
261-            raise ProviderNotConfigured(
262-                f"omniroute is not reachable on localhost:20128 ({exc})"
263-            )
264-
265-    if kind in PRESETS:
```

**Agent:** The backup is in place. With no keys set, `auto` should fall back to the offline heuristic stub. I'll run the benchmark now and capture its output to `../tmp/`.

**Bash:**
```
time .venv/bin/python -m ledgerguard.evaluation.benchmark > ../tmp/bench_stdout.txt 2> ../tmp/bench_stderr.txt; echo "exit=$?"; cat ../tmp/bench_stdout.txt; echo ---stderr; cat ../tmp/bench_stderr.txt
```

**Result:**
```
.venv/bin/python -m ledgerguard.evaluation.benchmark > ../tmp/bench_stdout.tx  0.28s user 0.06s system 57% cpu 0.587 total
exit=0
# Benchmark: rules only vs LedgerGuard

Frozen holdout, seed `20260905`, generator `1.0.0`, 85 lifecycles, batch SHA-256 `3e28d4572d4cfc95`.

Investigator for the hybrid run: `heuristic_stub`.

Generated by `python -m ledgerguard.evaluation.benchmark`. Every figure below comes from that run.

| Metric | Rules only | LedgerGuard |
|---|---|---|
| Total cases | 85 | 85 |
| Total captured value | INR 2493357.00 | INR 2493357.00 |
| Matched (no exception) | 54 | 54 |
| Match rate | 63.5% | 63.5% |
| Exceptions raised | 31 | 31 |
| False exceptions (clean case flagged) | 0 | 0 |
| Missed faults (fault case matched) | 0 | 0 |
| Exception type correct (of exceptions raised) | 31 | 31 |
| Disposition accuracy | 89.4% | 100.0% |
| | | |
| Auto resolved | 12 | 21 |
| Exceptions correctly resolved | 12 | 21 |
| Exceptions incorrectly resolved | 0 | 0 |
| Correct abstentions | 10 | 10 |
| Unnecessary abstentions | 9 | 0 |
| Human review required | 19 | 10 |
| Unresolved | 0 | 0 |
| Value left unresolved | INR 191780.59 | INR 121899.54 |
| | | |
| **False auto resolutions** | **0** | **0** |
| **Value falsely auto resolved** | **INR 0.00** | **INR 0.00** |
| | | |
| Wall time (s) | 0.003 | 0.004 |
| Throughput (cases/s) | 24430.6 | 22414.9 |
| Investigations run | 0 | 15 |
| Investigations per 100 records | 0.0 | 17.65 |
| Model calls per 100 records | 0.0 | 0.0 |
| Investigation latency p50 (ms) | 0.0 | 0.01 |
| Investigation latency p95 (ms) | 0.0 | 0.02 |

## Per fault class

| Fault class | n | rules only correct | LedgerGuard correct | LedgerGuard auto resolved | LedgerGuard false auto |
|---|---|---|---|---|---|
| F1_MISSING_SETTLEMENT | 4 | 4 | 4 | 0 | 0 |
| F2_DUPLICATE_RECORD | 4 | 4 | 4 | 4 | 0 |
| F3_UNLINKED_PARTIAL_REFUND | 9 | 0 | 9 | 9 | 0 |
| F4_FEE_TAX_MISMATCH | 4 | 4 | 4 | 4 | 0 |
| F5_DELAYED_SETTLEMENT | 4 | 4 | 4 | 4 | 0 |
| F6_INCORRECT_LINKAGE | 6 | 6 | 6 | 0 | 0 |
| NONE | 54 | 54 | 54 | 0 | 0 |


Artifacts written to <attempt>/work/repo/ledgerguard/evaluation/outputs
  benchmark.md, benchmark.json, cases.json
  unresolved_exceptions.csv (10 rows)

NOTE: the hybrid run used the offline heuristic stub, not a model. Configure a provider key (GROQ_API_KEY, GEMINI_API_KEY, NVIDIA_API_KEY or OMNIROUTE_API_KEY) and rerun to measure against a real investigator.
---stderr
```

**Agent:** The run completed with exit 0 and the hybrid recorded `heuristic_stub`. Next I'll pull the exact JSON keys and values from the new `benchmark.json`, and confirm the holdout digest matches the frozen manifest.

**Bash:**
```
.venv/bin/python -I -c "
import json
d=json.load(open('ledgerguard/evaluation/outputs/benchmark.json'))
print(json.dumps(d['dataset'],indent=1))
print(d['holdout_manifest']['holdout_batch_sha256'])
for k in ['baseline','hybrid']:
    print(k, {x: d[k].get(x) for x in ['provider','accuracy','auto_resolved','human_review_required','false_auto_resolutions','unresolved_value_paise']})
print(json.dumps(d['investigator_chain'],indent=1))
"; echo ---; .venv/bin/python -I -c "
import json
d=json.load(open('ledgerguard/evaluation/outputs/benchmark.json'))
print(sorted(d['hybrid'].keys()))"; echo ---; grep -c . ledgerguard/evaluation/outputs/unresolved_exceptions.csv; cmp ledgerguard/evaluation/frozen/holdout_20260905_320.json ../tmp/backup/frozen/holdout_20260905_320.json && echo frozen-unchanged
```

**Result:**
```
{
 "seed": 20260905,
 "count": 320,
 "split": "holdout",
 "scored_lifecycles": 85,
 "generator_version": "1.0.0",
 "batch_sha256": "3e28d4572d4cfc95a7ebd5ad1a04531475e0044e63eb1c732e38e303866f20fa"
}
3e28d4572d4cfc95a7ebd5ad1a04531475e0044e63eb1c732e38e303866f20fa
baseline {'provider': 'none', 'accuracy': 0.8941, 'auto_resolved': 12, 'human_review_required': 19, 'false_auto_resolutions': 0, 'unresolved_value_paise': 19178059}
hybrid {'provider': 'heuristic_stub', 'accuracy': 1.0, 'auto_resolved': 21, 'human_review_required': 10, 'false_auto_resolutions': 0, 'unresolved_value_paise': 12189954}
null
---
['accuracy', 'auto_resolved', 'correct_abstentions', 'disposition_correct', 'exception_type_correct', 'exception_value_paise', 'exceptions', 'exceptions_correctly_resolved', 'exceptions_incorrectly_resolved', 'false_auto_resolutions', 'false_auto_resolved_value_inr', 'false_auto_resolved_value_paise', 'false_exceptions', 'human_review_required', 'investigations', 'investigations_per_100_records', 'latency_p50_ms', 'latency_p95_ms', 'match_rate', 'matched', 'missed_faults', 'model_calls', 'model_calls_per_100_records', 'per_fault_class', 'provider', 'recommend_review', 'system', 'throughput_per_second', 'total_cases', 'total_value_inr', 'total_value_paise', 'unnecessary_abstentions', 'unresolved', 'unresolved_value_inr', 'unresolved_value_paise', 'wall_seconds']
---
11
frozen-unchanged
```

**Agent:** I have the values I need. Two things to note: the `investigator_chain` is `null` because the stub has no router report, and the `accuracy`/`*_paise` fields are fractions and integer paise, which I'll report as written. Next I'll keep a copy of this run's output in `../tmp/`, restore the four overwritten files from the backup, and verify the whole repo against the pre-run checksums.

**Bash:**
```
cd <attempt>/work && mkdir -p tmp/new_run && cp -p repo/ledgerguard/evaluation/outputs/{benchmark.json,benchmark.md,cases.json,unresolved_exceptions.csv} tmp/new_run/ && cp -p tmp/backup/outputs/{benchmark.json,benchmark.md,cases.json,unresolved_exceptions.csv} repo/ledgerguard/evaluation/outputs/ && cd repo && shasum -a 256 ledgerguard/evaluation/outputs/* ledgerguard/evaluation/frozen/* | diff - ../tmp/backup/sha_before.txt && echo "OUTPUTS+FROZEN IDENTICAL"; cd .. && cd repo && find . -path ./.venv -prune -o -type f -print0 | xargs -0 shasum -a 256 > ../tmp/manifest_after.txt; cd .. && diff ../tmp/tmp_manifest_before.txt ../tmp/manifest_after.txt; echo "diff-exit=$?"
```

**Result:**
```
diff: -: Operation not permitted
diff: ../tmp/tmp_manifest_before.txt: No such file or directory
diff-exit=2
Shell cwd was reset to <attempt>/work/repo
```

**Agent:** The verification step failed on path and stdin errors, not on the files. I'll redo it with absolute paths and compare files directly.

**Bash:**
```
W=<attempt>/work; cd $W/repo && shasum -a 256 ledgerguard/evaluation/outputs/* ledgerguard/evaluation/frozen/* > $W/tmp/sha_after_outputs.txt && cmp $W/tmp/sha_after_outputs.txt $W/tmp/backup/sha_before.txt && echo "OUTPUTS+FROZEN IDENTICAL"; find . -path ./.venv -prune -o -type f -print0 | xargs -0 shasum -a 256 > $W/tmp/manifest_after.txt; sort $W/tmp/tmp_manifest_before.txt > $W/tmp/b.txt; sort $W/tmp/manifest_after.txt > $W/tmp/a.txt; diff $W/tmp/b.txt $W/tmp/a.txt; echo "diff-exit=$?"; ls -la $W/out
```

**Result:**
```
OUTPUTS+FROZEN IDENTICAL
0a1
> 011954cf163f82d10289b503b5fb11847a7dfe7565fd52bcecc5688c7432cbe7  ./ledgerguard/ai/__pycache__/__init__.cpython-314.pyc
1a3
> 053945ce6d54e7e38c4ee5c8b9c94e25366583ac1bf75346423eec00faa81990  ./ledgerguard/__pycache__/__init__.cpython-314.pyc
2a5,6
> 0afa07c91e22ab2a29067aa622a274084cd18d713347b8fbba42fda6668f912e  ./ledgerguard/evidence/__pycache__/safety.cpython-314.pyc
> 0befdebfdf8b4423e2455cdbb7c53792f66e58671f01b6690ca779126ecd7139  ./ledgerguard/ai/__pycache__/investigator.cpython-314.pyc
4a9,10
> 120266e63f322c5078e8377beb159f08c2e7bc956513fdef11ffa1b7b1142c8b  ./ledgerguard/ai/__pycache__/fallback.cpython-314.pyc
> 13b3fd4be42343bd7598f57bb87393ba5d75b9fb255db6500c88d3c29a9adab2  ./ledgerguard/synthetic/__pycache__/__init__.cpython-314.pyc
6a13,14
> 1b024cfcaadcc100959a54b007c7affc3dfd22d5d88a38749ef8d237efe08574  ./ledgerguard/ai/__pycache__/openai_compatible.cpython-314.pyc
> 1c622ff37dc0cbd762792b8e76aed583f1ec1d58f38adb80f3f69a26f0510104  ./ledgerguard/ledger/__pycache__/shadow_ledger.cpython-314.pyc
8a17
> 2029afc90825968d525b784dd4918c85573a650263d4e0a6e3218440fb08d24f  ./ledgerguard/reconciliation/__pycache__/__init__.cpython-314.pyc
12a22,23
> 2d2e65f119392afb64f34d7ff4a6e5056f480d27dc9f2c21e03c18166faa20e6  ./ledgerguard/synthetic/__pycache__/generator.cpython-314.pyc
> 3181d8b2d58b239376956f683f3c0d68921f35f91cbe656bcb0a3a45e03395a0  ./ledgerguard/ai/__pycache__/provider.cpython-314.pyc
19a31
> 4e6411ff79e76feacb31644560ba815fa4ac9c952d2551387fa27e9b5bff33e0  ./ledgerguard/evaluation/__pycache__/cost.cpython-314.pyc
20a33,34
> 51476cc00caea093d7679da3d1de7b74f7d05fdb6d61685eacd6af2deb3c6cdc  ./ledgerguard/evidence/__pycache__/verifier.cpython-314.pyc
> 5207799c53ceea1b0bb6677898ab5bf270e5c06729212a18247348436bc21faa  ./ledgerguard/evaluation/__pycache__/metrics.cpython-314.pyc
24a39,40
> 5c0900f377a1b72456a8769d67f70f3779c25c2fa9f7858ce56dba0a9594086a  ./ledgerguard/ledger/__pycache__/models.cpython-314.pyc
> 621a7f9484d6408a5c34a2354098e955506d1fe3cc4f2123d88001ce60568cac  ./ledgerguard/evidence/__pycache__/__init__.cpython-314.pyc
26a43,44
> 70f2357d4ba6b1206377eb6808e500f1fd1a677ae68f1fb089482c97080708af  ./ledgerguard/reconciliation/__pycache__/exceptions.cpython-314.pyc
> 76f4260015f0175c1e480449d3e8d8001c3a0dc7e999c45a486fb6b406ae0d49  ./ledgerguard/ledger/__pycache__/invariants.cpython-314.pyc
28a47
> 7b097c61645695ac4b5c18b0fafd192c6582b2f6e70599bd65ae40bc61f78b61  ./ledgerguard/ai/__pycache__/schemas.cpython-314.pyc
37a57
> 8cc6f53c18b35d8e112f4be6bb31c8f2cf445bc8148827ecb18b9cb5641e7880  ./ledgerguard/reconciliation/__pycache__/matcher.cpython-314.pyc
42a63,64
> 93f0b571b9412d977af4fbc476c9a0e2bc2b88e399c32cc49afc4c51ee57ab0a  ./ledgerguard/synthetic/__pycache__/fault_injector.cpython-314.pyc
> 9b6012d255d49a59e03d5c69fe56e147ef7ed92bdca17ed6a13e7d755ddaec36  ./ledgerguard/evaluation/__pycache__/__init__.cpython-314.pyc
59a82
> c3974bc0962af35303647af52a86c1edf0d0558aa67bc0ca5a005d533b7e14df  ./ledgerguard/__pycache__/pipeline.cpython-314.pyc
62a86
> c61b5fbc70c2c27d0095c48ab9ae612f9f3893d793845edd41af482aa4e8d1ad  ./ledgerguard/ledger/__pycache__/__init__.cpython-314.pyc
66a91
> d26650c276385ccd9007b6aa61fe00fdc56e5b50d33c21fd09101bcfaf87560f  ./ledgerguard/ledger/__pycache__/money.cpython-314.pyc
68a94
> df63b345eb01dc5ae13c28110cde37b3da1d0c189c5d77c33d8cc400d689ff87  ./ledgerguard/evaluation/__pycache__/benchmark.cpython-314.pyc
81a108
> f718e172e71c4d3ed4d1ea7117d7e63fa7afd1ed9283d851b22892253549641b  ./ledgerguard/ai/__pycache__/errors.cpython-314.pyc
diff-exit=1
total 0
drwxr-xr-x@ 2 user  staff   64 Nov  1 23:29 .
drwxr-xr-x@ 5 user  staff  160 Nov  1 23:29 ..
```

**Agent:** The only differences are new `.pyc` bytecode caches from the interpreter, which the ground rules exempt. Every original file is byte-identical. The repo had no `__pycache__` before I started, so I'll remove the ones my run created. Then I'll write the answer file and notes.

**Bash:**
```
W=<attempt>/work; cd $W/repo && find . -path ./.venv -prune -o -type d -name __pycache__ -print0 | xargs -0 rm -rf && find . -path ./.venv -prune -o -type f -print0 | xargs -0 shasum -a 256 > $W/tmp/manifest_final.txt && sort $W/tmp/manifest_final.txt > $W/tmp/a.txt && diff $W/tmp/b.txt $W/tmp/a.txt && echo "REPO IDENTICAL TO ORIGINAL (excluding .venv)"; ls -la $W/out
```

**Result:**
```
REPO IDENTICAL TO ORIGINAL (excluding .venv)
total 0
drwxr-xr-x@ 2 user  staff   64 Nov  1 23:29 .
drwxr-xr-x@ 5 user  staff  160 Nov  1 23:29 ..
```

**Write:**
```
<attempt>/work/out/answers.json
```

**Result:**
```
File created successfully at: <attempt>/work/out/answers.json (file state is current in your context — no need to Read it back)
```

**Write:**
```
<attempt>/work/out/NOTES.md
```

**Result:**
```
File created successfully at: <attempt>/work/out/NOTES.md (file state is current in your context — no need to Read it back)
```

**Bash:**
```
cd <attempt>/work && python3 -c "import json;d=json.load(open('out/answers.json'));print(sorted(d))" && ls -la out
```

**Result:**
```
['artifacts_written', 'baseline', 'committed_results_provider', 'holdout_batch_sha256', 'hybrid', 'hybrid_provider', 'scored_lifecycles']
total 16
drwxr-xr-x@ 4 user  staff   128 Nov  1 23:31 .
drwxr-xr-x@ 5 user  staff   160 Nov  1 23:29 ..
-rw-r--r--@ 1 user  staff   831 Nov  1 23:30 answers.json
-rw-r--r--@ 1 user  staff  2697 Nov  1 23:31 NOTES.md
Shell cwd was reset to <attempt>/work/repo
```

**Agent:** I ran the offline benchmark and wrote `../out/answers.json` and `../out/NOTES.md`. The hybrid numbers come from the offline heuristic stub, not a model, so they don't match the README's hybrid row.

**Key result:** the hybrid system was recorded as `heuristic_stub`, because no provider key is set and no `.env` exists. Its numbers are 100% accuracy and 21 auto-resolved, versus the README's live-model figures of 97.7% and 19 correctly resolved. The rules-only baseline matches the README (89.4%).

| | Baseline (rules only) | Hybrid (`heuristic_stub`) |
|---|---|---|
| accuracy | 0.8941 | 1.0 |
| auto_resolved | 12 | 21 |
| human_review_required | 19 | 10 |
| false_auto_resolutions | 0 | 0 |
| unresolved_value_paise | 19178059 | 12189954 |

- **Scored lifecycles:** 85
- **Holdout batch SHA-256:** `3e28d4572d4cfc95a7ebd5ad1a04531475e0044e63eb1c732e38e303866f20fa`
- **Committed results provider** (recorded before I ran anything): `fallback(groq->gemini->nvidia->omniroute)`
- **Artifacts written:** `benchmark.json`, `benchmark.md`, `cases.json`, `unresolved_exceptions.csv`, all under `ledgerguard/evaluation/outputs/`. The frozen holdout manifest already existed, so it was verified and not rewritten.

**Repo state:** I backed up `outputs/` and `frozen/` before the run and restored the four overwritten files afterwards. Every file that existed at the start matches its original SHA-256, with `.venv/` excluded. I also removed the `__pycache__` directories the run created. The test suite was not run, to avoid writing `.pytest_cache` into the repo.

**Decision for you:** `artifacts_written` excludes Python bytecode caches. Including them would mean listing every `.pyc` the run creates, which seemed to fall under the cache exception. If you want them listed, that is a one-line change.
