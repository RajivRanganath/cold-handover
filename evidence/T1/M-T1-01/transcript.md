# M-T1-01 transcript (PASS)

**Agent:** I'll start with the handover docs at the repo root, as the ground rules require.

**Bash:**
```
ls -la && echo --- && ls -la .. && echo --- && find . -path ./.venv -prune -o -type f -print | grep -v __pycache__ | head -200
```

**Result:**
```
total 88
drwxr-xr-x@ 10 user  staff    320 Nov  1 23:27 .
drwxr-xr-x@  5 user  staff    160 Nov  1 23:27 ..
-rw-r--r--@  1 user  staff   1992 Nov  1 23:27 .env.example
-rw-r--r--@  1 user  staff     56 Nov  1 23:27 .gitignore
drwxr-xr-x@  7 user  staff    224 Nov  1 23:27 .venv
drwxr-xr-x@  7 user  staff    224 Nov  1 23:27 docs
drwxr-xr-x@ 14 user  staff    448 Nov  1 23:27 ledgerguard
-rw-r--r--@  1 user  staff  26848 Nov  1 23:27 README.md
-rw-r--r--@  1 user  staff    466 Nov  1 23:27 requirements.txt
-rwxr-xr-x@  1 user  staff   1447 Nov  1 23:27 run_demo.sh
---
total 0
drwxr-xr-x@  5 user  staff  160 Nov  1 23:27 .
drwxr-xr-x@ 10 user  staff  320 Nov  1 23:27 ..
drwxr-xr-x@  2 user  staff   64 Nov  1 23:27 out
drwxr-xr-x@ 10 user  staff  320 Nov  1 23:27 repo
drwxr-xr-x@  4 user  staff  128 Nov  1 23:27 tmp
---
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

**Bash:**
```
cat README.md
```

**Result:**
```
# LedgerGuard

**A self verifying AI finance controller.** Razorpay AI Buildathon, Track 04.

The workflow is settlement reconciliation: inspect the source records, verify an
ambiguous refund, and export the exceptions that still need a human.

I built LedgerGuard to answer a question that a reconciliation chatbot does not
answer: an LLM can generate a plausible explanation for a financial discrepancy
in about two seconds — but how do you know whether that explanation is
*financially true*?

**The core claim: LLM reasoning is not financial truth. Financial truth is
deterministic accounting state plus verified evidence. The AI may propose, the
financial system must prove.**

## Quick start

```bash
git clone https://github.com/RajivRanganath/ledgerguard.git && cd ledgerguard
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
./run_demo.sh          # tests, then benchmark, then http://127.0.0.1:8137
```

**No API key is needed.** Without one the AI investigation step degrades to an
offline stand-in and says so on the page; the deterministic engine, Shadow
Ledger, Evidence Gate, benchmark and dashboard all run unchanged.

---

## Where to verify each published requirement

Track 04, AI Finance Controller, checked against the official Buildathon page.
The official description does not mandate multiple agents, a particular frontend
framework, or a Razorpay payment API integration. Synthetic settlement
reconciliation is the chosen workflow, and no payment is ever initiated.

| Published requirement | Where to verify it |
|---|---|
| One finance-operations loop | Dashboard: records → investigation → checks → disposition → exception report |
| At least 50 synthetic records | 320 generated lifecycles; 85 held out and frozen for the benchmark |
| Match rate | `evaluation/outputs/benchmark.json` — `baseline.match_rate`, `hybrid.match_rate` |
| Throughput and measured accuracy | Same artifact; wall-clock figures include provider latency |
| Exceptions that could not be resolved | Dashboard exception queue, and `evaluation/outputs/unresolved_exceptions.csv` |
| Architecture | [`docs/architecture.md`](docs/architecture.md) |

---

## What it does

LedgerGuard reconciles orders, payments, refunds, settlements and bank records.

1. **The Shadow Ledger** independently reconstructs what the money movement
   *should* have been, from first principles:
   `expected_net = captured − refunds − fees − tax ± valid adjustments`.
   It never reads settlement or bank records to decide what to expect. Six named
   invariants (`I1`–`I6`) compare that reconstruction against what the provider
   actually reported. All money is integer paise; no float ever touches it.

2. **A deterministic engine reconciles everything it can prove** — exact
   identifier matching, settlement arithmetic against the fee schedule,
   duplicate detection, timing windows, bank matching. On the frozen holdout it
   resolves 54 of 85 cases with zero AI involvement, and never sends a case to
   the model that it could prove on its own.

3. **The AI investigator only sees what could not be proved.** It gets the
   records, the Shadow Ledger's expected value, the discrepancy, the permitted
   hypothesis taxonomy, and candidate related records. It returns structured
   JSON only. It is instructed not to calculate money; its prose is not used for
   monetary computation. It has no record-editing or case-closing tools.

4. **The Evidence Gate re-proves every claim.** If the model says a shortfall is
   a partial refund, the gate checks whether that refund exists, whether it is
   already owned by another payment, whether its reference identifies *this*
   order's customer, whether the amount matches, whether the timing is possible,
   and whether re-running the Shadow Ledger with that refund applied restores the
   invariant exactly. Verdict: `VERIFIED`, `UNVERIFIED`, or `REJECTED`.

5. **When proof is insufficient, it abstains.** Four states —
   `AUTO_RESOLVED`, `RECOMM
... [22708 more characters in transcript.jsonl]
```

**Bash:**
```
cat docs/evaluation.md; echo ----; cat docs/limitations.md | head -150
```

**Result:**
```
# Evaluation

## How to reproduce

```bash
.venv/bin/python -m ledgerguard.evaluation.benchmark
```

The canonical benchmark runs through the default chain with
`LEDGERGUARD_NO_CACHE=1`. Groq is first in the chain and does not cache, so it
serves the whole run in practice; the flag guards against OmniRoute's
`temperature: 0` response cache in the event the run falls through to it. The
benchmark prints which provider served how many investigations, and how many
came from a cache, so the run is self-describing either way.

Options: `--seed`, `--count`, `--split {holdout,dev,all}`, and
`--provider {auto,fallback,groq,gemini,nvidia,omniroute,openai_compatible,stub,none}`.

To compare investigators on the same holdout:

```bash
.venv/bin/python -m ledgerguard.evaluation.model_comparison --providers groq,gemini,stub
```

## Dataset and split

320 lifecycles from seed `20260905`, generator version `1.0.0`. Ground truth is
computed before any fault is injected and stored in a structure the matcher, the
investigator and the gate never receive.

The split is 75/25, **stratified by fault class**. Stratifying matters: an
unstratified 25% slice of a 320-case dataset can easily contain zero F6 cases,
which would make the headline safety metric meaningless. Paired F6 lifecycles
(the victim and the donor whose refund it is) are always kept on the same side.

| Fault class | Total | Holdout |
|---|---|---|
| Clean | 218 | 54 |
| F1 missing settlement | 15 | 4 |
| F2 duplicate record | 15 | 4 |
| F3 unlinked partial refund | 29 | 9 |
| F4 fee or tax mismatch | 15 | 4 |
| F5 delayed settlement | 16 | 4 |
| F6 incorrect linkage | 12 | 6 |

## Freezing

The holdout is frozen to `evaluation/frozen/holdout_{seed}_{count}.json`,
recording the lifecycle ids and the batch SHA-256. Every later run regenerates
the data and compares. A mismatch aborts with `FROZEN HOLDOUT MISMATCH` rather
than silently scoring against changed data.

Manifests are keyed per `(seed, count)`. An earlier version used a single file,
which meant running with a different `--count` silently overwrote the manifest an
earlier result had been scored against — a result would then be reported against
a holdout that no longer existed. That was a real hole, and keying the manifest
by configuration is what closed it.

No system was tuned using individual holdout answers.

## Reproducibility

Verified, not assumed:

- Two `build_dataset()` calls produce a batch with identical SHA-256
  (`c320c559e8ff564a` for the full set, `3e28d4572d4cfc95` for the holdout).
- `unresolved_exceptions.csv` is byte-identical across two benchmark runs.
- `benchmark.json` is identical across runs excluding the four wall-clock timing
  fields (`wall_seconds`, `throughput_per_second`, `latency_p50_ms`,
  `latency_p95_ms`), which vary by machine and by run and are not decisions.

These guarantees cover the **dataset and the deterministic layer**, and they
hold with `--provider stub` or `--provider none`. They do **not** extend to a
model run: five `groq` runs on the identical holdout resolved between 5 and 7
of the 9 F3 cases at `temperature: 0`. The historical notes report stable safety across all five
(0 false auto resolutions, INR 0.00 falsely closed, all 6 F6 escalated); the
variance is confined to how much is safely closed. Report the range, not the
best run.

## Metrics

Defined in `evaluation/metrics.py`. Every figure in every artifact is rendered
from the `Metrics` dataclass; no literal number appears in any template.

The two reported first, deliberately:

- **`false_auto_resolutions`** — cases closed automatically that ground truth
  says required a human. This is the failure mode the whole architecture exists
  to prevent.
- **`false_auto_resolved_value_paise`** — the rupee value behind those closures.

Also reported: total cases, match rate, exceptions raised, false exceptions,
missed faults, exception-type accuracy, disposition accuracy, auto resolved,
exceptions correctly/incorrectly resolved, corr
... [17360 more characters in transcript.jsonl]
```

**Agent:** The docs say the canonical run uses the Groq provider and that the committed `benchmark.json` is a historical sample. Before I run anything I need the benchmark code, the committed results, and a snapshot of the repo so I can restore it afterwards.

**Bash:**
```
cat ledgerguard/evaluation/benchmark.py; echo ----; cat ledgerguard/evaluation/outputs/benchmark.json | head -150
```

**Result:**
```
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
        "comes from that run.",
        "",
        "| Metric | Rule
... [15189 more characters in transcript.jsonl]
```

**Bash:**
```
mkdir -p ../tmp/orig && cp -Rp . ../tmp/orig/ 2>/dev/null; rm -rf ../tmp/orig/.venv; cd ../tmp/orig && find . -type f | wc -l && find . -type f -not -path '*/__pycache__/*' -exec shasum -a 256 {} + | sort -k2 > ../orig_sha256.txt; wc -l ../orig_sha256.txt; ls -la ../; cat ../../repo/.gitignore; echo; ls ../../tmp
```

**Result:**
```
      82
      82 ../orig_sha256.txt
total 24
drwxr-xr-x@ 6 user  staff   192 Nov  1 23:27 .
drwxr-xr-x@ 5 user  staff   160 Nov  1 23:27 ..
drwx------@ 3 user  staff    96 Nov  1 23:27 cc-socks
drwx------@ 3 user  staff    96 Nov  1 23:27 claude-501
drwxr-xr-x@ 9 user  staff   288 Nov  1 23:27 orig
-rw-r--r--@ 1 user  staff  8461 Nov  1 23:27 orig_sha256.txt
.venv/
__pycache__/
*.pyc
.env
.pytest_cache/
.DS_Store

cc-socks
claude-501
orig
orig_sha256.txt
Shell cwd was reset to <attempt>/work/repo
```

**Agent:** Snapshot is saved (82 files hashed in `../tmp/orig_sha256.txt`). Next I'll pull the committed hybrid and chain fields, and check how the provider resolves when no key is present.

**Bash:**
```
sed -n 150,400p ledgerguard/evaluation/outputs/benchmark.json | grep -v '^      "[A-Z]' ; echo ----; cat ledgerguard/ai/provider.py; echo ----; env | grep -iE 'api_key|ledgerguard|groq|gemini|nvidia|omni' | sed 's/=.*/=<set>/'; ls -la .env 2>&1
```

**Result (error):**
```
Exit code 1
      },
        "n": 9,
        "auto_resolved": 0,
        "correct": 0,
        "false_auto": 0,
        "abstained": 9
      },
        "n": 4,
        "auto_resolved": 4,
        "correct": 4,
        "false_auto": 0,
        "abstained": 0
      },
        "n": 4,
        "auto_resolved": 4,
        "correct": 4,
        "false_auto": 0,
        "abstained": 0
      },
        "n": 6,
        "auto_resolved": 0,
        "correct": 6,
        "false_auto": 0,
        "abstained": 6
      },
        "n": 54,
        "auto_resolved": 0,
        "correct": 54,
        "false_auto": 0,
        "abstained": 0
      }
    },
    "false_auto_resolved_value_inr": "0.00",
    "unresolved_value_inr": "191780.59",
    "total_value_inr": "2493357.00"
  },
  "hybrid": {
    "system": "LedgerGuard (hybrid)",
    "provider": "fallback(groq->gemini->nvidia->omniroute)",
    "false_auto_resolutions": 0,
    "false_auto_resolved_value_paise": 0,
    "total_cases": 85,
    "total_value_paise": 249335700,
    "matched": 54,
    "exceptions": 31,
    "match_rate": 0.6353,
    "false_exceptions": 0,
    "missed_faults": 0,
    "exception_type_correct": 31,
    "disposition_correct": 83,
    "accuracy": 0.9765,
    "auto_resolved": 19,
    "exceptions_correctly_resolved": 19,
    "exceptions_incorrectly_resolved": 0,
    "recommend_review": 0,
    "human_review_required": 12,
    "unresolved": 0,
    "correct_abstentions": 10,
    "unnecessary_abstentions": 2,
    "exception_value_paise": 36426731,
    "unresolved_value_paise": 13590189,
    "wall_seconds": 121.704,
    "throughput_per_second": 0.7,
    "investigations": 15,
    "model_calls": 15,
    "model_calls_per_100_records": 17.65,
    "investigations_per_100_records": 17.65,
    "latency_p50_ms": 10775.36,
    "latency_p95_ms": 12804.67,
    "per_fault_class": {
        "n": 4,
        "auto_resolved": 0,
        "correct": 4,
        "false_auto": 0,
        "abstained": 4
      },
        "n": 4,
        "auto_resolved": 4,
        "correct": 4,
        "false_auto": 0,
        "abstained": 0
      },
        "n": 9,
        "auto_resolved": 7,
        "correct": 7,
        "false_auto": 0,
        "abstained": 2
      },
        "n": 4,
        "auto_resolved": 4,
        "correct": 4,
        "false_auto": 0,
        "abstained": 0
      },
        "n": 4,
        "auto_resolved": 4,
        "correct": 4,
        "false_auto": 0,
        "abstained": 0
      },
        "n": 6,
        "auto_resolved": 0,
        "correct": 6,
        "false_auto": 0,
        "abstained": 6
      },
        "n": 54,
        "auto_resolved": 0,
        "correct": 54,
        "false_auto": 0,
        "abstained": 0
      }
    },
    "false_auto_resolved_value_inr": "0.00",
    "unresolved_value_inr": "135901.89",
    "total_value_inr": "2493357.00"
  },
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
that, so a stub run is never mistaken fo
... [6039 more characters in transcript.jsonl]
```

**Agent:** No API key or `.env` is present, so the default `auto` path will fall through to the offline stub. I'll check the stub's provider name and the committed markdown's investigator line, since the task asks for the committed value "exactly as written there".

**Bash:**
```
head -8 ledgerguard/evaluation/outputs/benchmark.md; echo ----; grep -rn "heuristic_stub\|class HeuristicProvider" ledgerguard --include=*.py | head; echo ----; grep -n '"provider"' ledgerguard/evaluation/outputs/benchmark.json; echo ----; grep -n "provider" ledgerguard/evaluation/outputs/cases.json | sort | uniq -c | head -5; echo ----; cat ledgerguard/evaluation/frozen/holdout_20260905_320.json | head -5; echo; ls -la ledgerguard/evaluation/frozen/ ; find ledgerguard -name __pycache__ | head -3
```

**Result:**
```
# Benchmark: rules only vs LedgerGuard

Frozen holdout, seed `20260905`, generator `1.0.0`, 85 lifecycles, batch SHA-256 `3e28d4572d4cfc95`.

Investigator for the hybrid run: `fallback(groq->gemini->nvidia->omniroute)`.

Generated by `python -m ledgerguard.evaluation.benchmark`. Every figure below comes from that run.

----
(eval):1: no matches found: --include=*.py
----
105:    "provider": "none",
193:    "provider": "fallback(groq->gemini->nvidia->omniroute)",
----
   1 1009:      "suggested_action": "Obtain the missing record from the provider, or confirm the deduction manually before closing."
   1 1054:        "detail": "setl_0035FAA7: shadow ledger expects net 1145122 for payment pay_00351A3E, provider reported 1145122"
   1 1136:        "detail": "setl_00373C9A: shadow ledger expects net 1040354 for payment pay_0037DAA0, provider reported 1025604"
   1 117:        "detail": "setl_00043C9C: shadow ledger expects net 6487299 for payment pay_0004930A, provider reported 6487299"
   1 1225:        "detail": "setl_0048FFC8: shadow ledger expects net 845172 for payment pay_0048CBEF, provider reported -427498"
----
{
  "seed": 20260905,
  "count": 320,
  "generator_version": "1.0.0",
  "holdout_lifecycle_ids": [

total 8
drwxr-xr-x@  3 user  staff    96 Nov  1 23:27 .
drwxr-xr-x@ 17 user  staff   544 Nov  1 23:27 ..
-rw-r--r--@  1 user  staff  1388 Nov  1 23:27 holdout_20260905_320.json
```

**Bash:**
```
grep -rn "heuristic_stub\|class HeuristicProvider" ledgerguard/ai/ | head; echo ----; grep -n "class HeuristicProvider" -A30 ledgerguard/ai/provider.py | grep -n "name\|provider" | head
```

**Result:**
```
ledgerguard/ai/provider.py:140:class HeuristicProvider:
ledgerguard/ai/provider.py:148:    name = "heuristic_stub"
ledgerguard/ai/provider.py:186:            return _to_result(out, source="heuristic_stub", model_name=None)
ledgerguard/ai/provider.py:199:            return _to_result(out, source="heuristic_stub", model_name=None)
ledgerguard/ai/provider.py:208:        return _to_result(out, source="heuristic_stub", model_name=None)
ledgerguard/ai/schemas.py:72:    source: Literal["model", "heuristic_stub", "unavailable", "invalid_response"] = "model"
ledgerguard/ai/fallback.py:100:            if result.source in ("model", "heuristic_stub"):
----
9:148-    name = "heuristic_stub"
```

**Agent:** The stub reports `heuristic_stub`. I'll run the canonical benchmark with no provider flag and no keys, capturing stdout to `../tmp`, then compare the file tree against the snapshot.

**Bash:**
```
(env | grep -E '^(GROQ|GEMINI|NVIDIA|OMNIROUTE|ANTHROPIC|LEDGERGUARD)' ; true) | sed 's/=.*/=<set>/'; .venv/bin/python -m ledgerguard.evaluation.benchmark > ../tmp/run_stdout.txt 2> ../tmp/run_stderr.txt; echo "exit=$?"; cat ../tmp/run_stdout.txt; echo ---stderr---; cat ../tmp/run_stderr.txt
```

**Result:**
```
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
| Throughput (cases/s) | 26123.0 | 22623.7 |
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
---stderr---
```

**Agent:** The run succeeded and used the stub. I'll save the new outputs to `../tmp`, then restore the repo from the snapshot and verify every hash matches.

**Bash:**
```
mkdir -p ../tmp/run_outputs && cp -p ledgerguard/evaluation/outputs/* ../tmp/run_outputs/ && cp -p ledgerguard/evaluation/frozen/* ../tmp/run_outputs/ 2>/dev/null; cd repo 2>/dev/null; cd <attempt>/work/repo && find . -path ./.venv -prune -o -type f -print | grep -v __pycache__ | sort > ../tmp/after_files.txt; (cd ../tmp/orig && find . -type f | sort) > ../tmp/before_files.txt; diff ../tmp/before_files.txt <(sed 's#^\./##' ../tmp/after_files.txt | sed 's#^#./#' ) ; echo "diff exit=$?"; for f in ledgerguard/evaluation/outputs/benchmark.json ledgerguard/evaluation/outputs/benchmark.md ledgerguard/evaluation/outputs/cases.json ledgerguard/evaluation/outputs/unresolved_exceptions.csv; do echo "changed? $f"; done; find . -path ./.venv -prune -o -type f -newer ../tmp/orig_sha256.txt -print | grep -v __pycache__
```

**Result:**
```
diff: /dev/fd/12: Operation not permitted
diff exit=2
changed? ledgerguard/evaluation/outputs/benchmark.json
changed? ledgerguard/evaluation/outputs/benchmark.md
changed? ledgerguard/evaluation/outputs/cases.json
changed? ledgerguard/evaluation/outputs/unresolved_exceptions.csv
./ledgerguard/evaluation/outputs/benchmark.json
./ledgerguard/evaluation/outputs/benchmark.md
./ledgerguard/evaluation/outputs/cases.json
./ledgerguard/evaluation/outputs/unresolved_exceptions.csv
```

**Agent:** Four files were rewritten, and the frozen manifest was not touched. The process-substitution diff failed under the sandbox, so I'll use the mtime list instead. Next I'll restore the four files from the snapshot and verify the whole tree against the original hashes.

**Bash:**
```
for f in benchmark.json benchmark.md cases.json unresolved_exceptions.csv; do cp -p ../tmp/orig/ledgerguard/evaluation/outputs/$f ledgerguard/evaluation/outputs/$f; done && cd <attempt>/work/repo && find . -path ./.venv -prune -o -type f -not -path '*/__pycache__/*' -print0 | sort -z | xargs -0 shasum -a 256 | sort -k2 > ../tmp/now_sha256.txt && diff <(sort -k2 ../tmp/orig_sha256.txt) ../tmp/now_sha256.txt && echo "ALL HASHES MATCH"; wc -l ../tmp/now_sha256.txt; find . -path ./.venv -prune -o -type d -name __pycache__ -print | head -3
```

**Result:**
```
diff: /dev/fd/12: Operation not permitted
      82 ../tmp/now_sha256.txt
./ledgerguard/__pycache__
./ledgerguard/reconciliation/__pycache__
./ledgerguard/ledger/__pycache__
```

**Bash:**
```
sort -k2 ../tmp/orig_sha256.txt > ../tmp/a.txt && sort -k2 ../tmp/now_sha256.txt > ../tmp/b.txt && diff ../tmp/a.txt ../tmp/b.txt && echo "ALL 82 HASHES MATCH ORIGINAL"; grep -c . ../tmp/a.txt; grep -E "benchmark|cases|unresolved" ../tmp/b.txt
```

**Result:**
```
ALL 82 HASHES MATCH ORIGINAL
82
93478562a075243d4a2407a194f71b6663e30eeb4605f8d261f39a638905a261  ./ledgerguard/evaluation/benchmark.py
249e3bce69daeb83386d9575e66bf4177d4db885a8864ab6b32d80b5717d8536  ./ledgerguard/evaluation/outputs/benchmark.json
aa667ebea4ccd41fa0bdff898182200d3bf282ef0b888cabd7b5a215d82edd22  ./ledgerguard/evaluation/outputs/benchmark.md
a5552fcb48631411cb08fae4e34987295cca132334d6c31d86601f73e538455b  ./ledgerguard/evaluation/outputs/cases.json
af74f00254d9a8cee944bccdf9fd8940c2a318c0bfd5c6965dbfc5a221e00711  ./ledgerguard/evaluation/outputs/unresolved_exceptions.csv
```

**Agent:** All 82 original files are byte-identical again. Now I'll pull the answer values from the saved run output rather than from memory.

**Bash:**
```
.venv/bin/python -I -c "
import json
d=json.load(open('../tmp/run_outputs/benchmark.json'))
print(d['dataset'])
print(d['holdout_manifest']['holdout_batch_sha256'])
print(d['hybrid']['provider'], d['baseline']['provider'])
for k in ['baseline','hybrid']:
    print(k,{x:d[k][x] for x in ['accuracy','auto_resolved','human_review_required','false_auto_resolutions','unresolved_value_paise']})
print(d['investigator_chain'])
"; echo ----; .venv/bin/python -I -c "
import json
d=json.load(open('../tmp/orig/ledgerguard/evaluation/outputs/benchmark.json'))
print('COMMITTED hybrid.provider =', repr(d['hybrid']['provider']))
print('COMMITTED dataset.scored', d['dataset']['scored_lifecycles'])
"; ls ../tmp/run_outputs
```

**Result:**
```
{'seed': 20260905, 'count': 320, 'split': 'holdout', 'scored_lifecycles': 85, 'generator_version': '1.0.0', 'batch_sha256': '3e28d4572d4cfc95a7ebd5ad1a04531475e0044e63eb1c732e38e303866f20fa'}
3e28d4572d4cfc95a7ebd5ad1a04531475e0044e63eb1c732e38e303866f20fa
heuristic_stub none
baseline {'accuracy': 0.8941, 'auto_resolved': 12, 'human_review_required': 19, 'false_auto_resolutions': 0, 'unresolved_value_paise': 19178059}
hybrid {'accuracy': 1.0, 'auto_resolved': 21, 'human_review_required': 10, 'false_auto_resolutions': 0, 'unresolved_value_paise': 12189954}
None
----
COMMITTED hybrid.provider = 'fallback(groq->gemini->nvidia->omniroute)'
COMMITTED dataset.scored 85
ablation.json
ablation.md
benchmark.json
benchmark.md
calibration.json
calibration.md
cases.json
decision_log.json
drift.json
drift.md
evidence_ledger.csv
holdout_20260905_320.json
model_comparison.json
model_comparison.md
no_gate_ablation.json
no_gate_ablation.md
reconciliation_report.csv
reconciliation_report.md
scale.json
scale.md
unresolved_exceptions.csv
```

**Agent:** I have the values I need. The offline run recorded `heuristic_stub` for the hybrid, while the committed results recorded `fallback(groq->gemini->nvidia->omniroute)`. Next I'll write the answers file and the notes.

**Write:**
```
<attempt>/work/out/answers.json
```

**Result:**
```
File created successfully at: <attempt>/work/out/answers.json (file state is current in your context — no need to Read it back)
```

**Bash:**
```
cd <attempt>/work && .venv/bin/python -I -c "import json;print(json.load(open('out/answers.json'))['hybrid'])" 2>/dev/null || repo/.venv/bin/python -I -c "import json;print(json.load(open('out/answers.json'))['hybrid'])"; ls -la out
```

**Result:**
```
{'accuracy': 1.0, 'auto_resolved': 21, 'human_review_required': 10, 'false_auto_resolutions': 0, 'unresolved_value_paise': 12189954}
total 8
drwxr-xr-x@ 3 user  staff   96 Nov  1 23:28 .
drwxr-xr-x@ 5 user  staff  160 Nov  1 23:27 ..
-rw-r--r--@ 1 user  staff  831 Nov  1 23:28 answers.json
Shell cwd was reset to <attempt>/work/repo
```

**Agent:** The answers file parses. Now I'll write the notes file, recording the choices I made and what I did not do.

**Write:**
```
<attempt>/work/out/NOTES.md
```

**Result:**
```
File created successfully at: <attempt>/work/out/NOTES.md (file state is current in your context — no need to Read it back)
```

**Agent:** I reproduced the offline benchmark and wrote `../out/answers.json` and `../out/NOTES.md`. The repo is back to its original state: all 82 files match their pre-run hashes.

The offline run is not comparable to the committed results. With no key set, the hybrid fell back to the offline heuristic stub, so the hybrid numbers below are stub numbers.

| | Rules only | Hybrid (stub) |
|---|---|---|
| Accuracy | 0.8941 | 1.0 |
| Auto resolved | 12 | 21 |
| Human review required | 19 | 10 |
| False auto resolutions | 0 | 0 |
| Unresolved value (paise) | 19178059 | 12189954 |

- **Scored lifecycles:** 85. The frozen holdout check passed, with batch SHA-256 `3e28d4572d4cfc95a7ebd5ad1a04531475e0044e63eb1c732e38e303866f20fa`.
- **`hybrid_provider`:** `heuristic_stub`, as the run recorded it.
- **`committed_results_provider`:** `fallback(groq->gemini->nvidia->omniroute)`, read from the committed results before I ran anything.
- **`artifacts_written`:** the four files under `ledgerguard/evaluation/outputs/` that the command rewrites: `benchmark.json`, `benchmark.md`, `cases.json`, `unresolved_exceptions.csv`.

I ran the default command with no provider flag, because the documented `--provider groq` path needs network and keys, which this task rules out. I snapshotted the repo before running and restored the four rewritten files afterwards. Python `__pycache__` files were also created by the import; I left them out of the artifact list as cache directories.

The committed `benchmark.json` still lists a stale NVIDIA model in its investigator chain. The docs already flag this, and I did not change it.
