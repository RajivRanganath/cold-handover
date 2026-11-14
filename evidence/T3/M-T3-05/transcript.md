# M-T3-05 transcript (PASS)

**Agent:** I'll start with the handover documentation at the repository root, then read the benchmark module.

**Bash:**
```
ls -la && ls -la ledgerguard/evaluation ledgerguard/evaluation/outputs ledgerguard/evaluation/frozen 2>&1 | head -80
```

**Result:**
```
total 88
drwxr-xr-x@ 10 user  staff    320 Nov  1 23:22 .
drwxr-xr-x@  5 user  staff    160 Nov  1 23:22 ..
-rw-r--r--@  1 user  staff   1992 Nov  1 23:22 .env.example
-rw-r--r--@  1 user  staff     56 Nov  1 23:22 .gitignore
drwxr-xr-x@  7 user  staff    224 Nov  1 23:22 .venv
drwxr-xr-x@  7 user  staff    224 Nov  1 23:22 docs
drwxr-xr-x@ 14 user  staff    448 Nov  1 23:22 ledgerguard
-rw-r--r--@  1 user  staff  26848 Nov  1 23:22 README.md
-rw-r--r--@  1 user  staff    466 Nov  1 23:22 requirements.txt
-rwxr-xr-x@  1 user  staff   1447 Nov  1 23:22 run_demo.sh
ledgerguard/evaluation:
total 208
-rw-r--r--@  1 user  staff      0 Nov  1 23:22 __init__.py
drwxr-xr-x@ 17 user  staff    544 Nov  1 23:22 .
drwxr-xr-x@ 14 user  staff    448 Nov  1 23:22 ..
-rw-r--r--@  1 user  staff  15897 Nov  1 23:22 ablation.py
-rw-r--r--@  1 user  staff    681 Nov  1 23:22 baseline.py
-rw-r--r--@  1 user  staff  16017 Nov  1 23:22 benchmark.py
-rw-r--r--@  1 user  staff   6945 Nov  1 23:22 calibration.py
-rw-r--r--@  1 user  staff   3854 Nov  1 23:22 cost.py
-rw-r--r--@  1 user  staff   6225 Nov  1 23:22 drift.py
drwxr-xr-x@  3 user  staff     96 Nov  1 23:22 frozen
-rw-r--r--@  1 user  staff   7063 Nov  1 23:22 metrics.py
-rw-r--r--@  1 user  staff   7211 Nov  1 23:22 model_comparison.py
-rw-r--r--@  1 user  staff   6449 Nov  1 23:22 no_gate_ablation.py
drwxr-xr-x@ 22 user  staff    704 Nov  1 23:22 outputs
-rw-r--r--@  1 user  staff   6679 Nov  1 23:22 replay.py
-rw-r--r--@  1 user  staff   7159 Nov  1 23:22 report.py
-rw-r--r--@  1 user  staff   5606 Nov  1 23:22 scale.py

ledgerguard/evaluation/frozen:
total 8
drwxr-xr-x@  3 user  staff    96 Nov  1 23:22 .
drwxr-xr-x@ 17 user  staff   544 Nov  1 23:22 ..
-rw-r--r--@  1 user  staff  1388 Nov  1 23:22 holdout_20260905_320.json

ledgerguard/evaluation/outputs:
total 992
drwxr-xr-x@ 22 user  staff     704 Nov  1 23:22 .
drwxr-xr-x@ 17 user  staff     544 Nov  1 23:22 ..
-rw-r--r--@  1 user  staff    6742 Nov  1 23:22 ablation.json
-rw-r--r--@  1 user  staff    1622 Nov  1 23:22 ablation.md
-rw-r--r--@  1 user  staff    6707 Nov  1 23:22 benchmark.json
-rw-r--r--@  1 user  staff    1975 Nov  1 23:22 benchmark.md
-rw-r--r--@  1 user  staff     829 Nov  1 23:22 calibration.json
-rw-r--r--@  1 user  staff    1656 Nov  1 23:22 calibration.md
-rw-r--r--@  1 user  staff  240238 Nov  1 23:22 cases.json
-rw-r--r--@  1 user  staff  148905 Nov  1 23:22 decision_log.json
-rw-r--r--@  1 user  staff    2427 Nov  1 23:22 drift.json
-rw-r--r--@  1 user  staff    1602 Nov  1 23:22 drift.md
-rw-r--r--@  1 user  staff   15987 Nov  1 23:22 evidence_ledger.csv
-rw-r--r--@  1 user  staff    3445 Nov  1 23:22 model_comparison.json
-rw-r--r--@  1 user  staff    1513 Nov  1 23:22 model_comparison.md
-rw-r--r--@  1 user  staff    1203 Nov  1 23:22 no_gate_ablation.json
-rw-r--r--@  1 user  staff    1771 Nov  1 23:22 no_gate_ablation.md
-rw-r--r--@  1 user  staff   19177 Nov  1 23:22 reconciliation_report.csv
-rw-r--r--@  1 user  staff     800 Nov  1 23:22 reconciliation_report.md
-rw-r--r--@  1 user  staff    1268 Nov  1 23:22 scale.json
-rw-r--r--@  1 user  staff     935 Nov  1 23:22 scale.md
-rw-r--r--@  1 user  staff    6659 Nov  1 23:22 unresolved_exceptions.csv
```

**Bash:**
```
ls *.md 2>/dev/null; for f in *.md; do echo "=== $f"; cat "$f"; done 2>/dev/null | head -300
```

**Result:**
```
README.md
=== README.md
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
   
... [11179 more characters in transcript.jsonl]
```

**Bash:**
```
cat ledgerguard/evaluation/benchmark.py; echo ====; ls ledgerguard; ls ledgerguard/tests 2>/dev/null; ls docs; grep -rn "benchmark" docs/*.md | head -30
```

**Result (error):**
```
Exit code 1
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
        "| M
... [6039 more characters in transcript.jsonl]
```

**Agent:** The middle of the file was truncated, so I'll read that section, then look for the tests and docs that reference the benchmark.

**Bash:**
```
sed -n 95,200p ledgerguard/evaluation/benchmark.py; echo ====; find . -path ./.venv -prune -o -name "*test*" -print | head -50; echo ====; ls docs; grep -rln "OUTPUT_DIR\|outputs/" --include=*.py --include=*.md --include=*.sh . --exclude-dir=.venv | head -40
```

**Result (error):**
```
Exit code 1
        "",
        f"Investigator for the hybrid run: `{hyb.provider}`.",
        "",
        "Generated by `python -m ledgerguard.evaluation.benchmark`. Every figure below "
        "comes from that run.",
        "",
        "| Metric | Rules only | LedgerGuard |",
        "|---|---|---|",
        _row("Total cases", base.total_cases, hyb.total_cases),
        _row("Total captured value", base.total_value_paise, hyb.total_value_paise, inr),
        _row("Matched (no exception)", base.matched, hyb.matched),
        _row("Match rate", base.match_rate, hyb.match_rate, lambda v: f"{v:.1%}"),
        _row("Exceptions raised", base.exceptions, hyb.exceptions),
        _row("False exceptions (clean case flagged)", base.false_exceptions, hyb.false_exceptions),
        _row("Missed faults (fault case matched)", base.missed_faults, hyb.missed_faults),
        _row("Exception type correct (of exceptions raised)", base.exception_type_correct, hyb.exception_type_correct),
        _row("Disposition accuracy", base.accuracy, hyb.accuracy, lambda v: f"{v:.1%}"),
        "| | | |",
        _row("Auto resolved", base.auto_resolved, hyb.auto_resolved),
        _row("Exceptions correctly resolved", base.exceptions_correctly_resolved, hyb.exceptions_correctly_resolved),
        _row("Exceptions incorrectly resolved", base.exceptions_incorrectly_resolved, hyb.exceptions_incorrectly_resolved),
        _row("Correct abstentions", base.correct_abstentions, hyb.correct_abstentions),
        _row("Unnecessary abstentions", base.unnecessary_abstentions, hyb.unnecessary_abstentions),
        _row("Human review required", base.human_review_required, hyb.human_review_required),
        _row("Unresolved", base.unresolved, hyb.unresolved),
        _row("Value left unresolved", base.unresolved_value_paise, hyb.unresolved_value_paise, inr),
        "| | | |",
        f"| **False auto resolutions** | **{base.false_auto_resolutions}** | **{hyb.false_auto_resolutions}** |",
        f"| **Value falsely auto resolved** | **{inr(base.false_auto_resolved_value_paise)}** | "
        f"**{inr(hyb.false_auto_resolved_value_paise)}** |",
        "| | | |",
        _row("Wall time (s)", base.wall_seconds, hyb.wall_seconds),
        _row("Throughput (cases/s)", base.throughput_per_second, hyb.throughput_per_second),
        _row("Investigations run", base.investigations, hyb.investigations),
        _row("Investigations per 100 records", base.investigations_per_100_records, hyb.investigations_per_100_records),
        _row("Model calls per 100 records", base.model_calls_per_100_records, hyb.model_calls_per_100_records),
        _row("Investigation latency p50 (ms)", base.latency_p50_ms, hyb.latency_p50_ms),
        _row("Investigation latency p95 (ms)", base.latency_p95_ms, hyb.latency_p95_ms),
        "",
        "## Per fault class",
        "",
        "| Fault class | n | rules only correct | LedgerGuard correct | LedgerGuard auto resolved | LedgerGuard false auto |",
        "|---|---|---|---|---|---|",
    ]
    for fault_class in sorted(set(base.per_fault_class) | set(hyb.per_fault_class)):
        b = base.per_fault_class.get(fault_class, {})
        h = hyb.per_fault_class.get(fault_class, {})
        lines.append(
            f"| {fault_class} | {h.get('n', b.get('n', 0))} | {b.get('correct', 0)} | "
            f"{h.get('correct', 0)} | {h.get('auto_resolved', 0)} | {h.get('false_auto', 0)} |"
        )
    return "\n".join(lines) + "\n"


def write_unresolved_csv(report: RunReport, dataset: Dataset, path: Path) -> int:
    """The honest failure surface: everything the controller refused to close."""
    truth = {lc.payment.payment_id: lc.lifecycle_id for lc in dataset.lifecycles}
    rows = 0
    with path.open("w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(
            [
                "case_id",
                "lifecycle_id",
                "exception_type",
                "state",
                "related_tr
... [1498 more characters in transcript.jsonl]
```

**Agent:** The `====` separators are tripping zsh's `=` expansion, so I'll use plain labels instead. Next, the tests and any other references to the output directory.

**Bash:**
```
find . -path ./.venv -prune -o \( -name "test_*.py" -o -name "*_test.py" -o -name "conftest.py" \) -print; echo; grep -rn "OUTPUT_DIR\|MANIFEST_DIR\|evaluation.benchmark\|outputs/" --include=*.py --include=*.md --include=*.sh . --exclude-dir=.venv | grep -v "^./ledgerguard/evaluation/outputs" | head -60; echo; cat run_demo.sh; cat .gitignore; cat requirements.txt
```

**Result:**
```
./ledgerguard/tests/test_p0_core.py
./ledgerguard/tests/test_p2_evaluation.py
./ledgerguard/tests/test_p1_compound.py
./ledgerguard/tests/test_p1_extended.py
./ledgerguard/tests/test_fallback.py
./ledgerguard/tests/test_evidence_download.py
./ledgerguard/tests/test_dashboard_startup.py

(eval):1: no matches found: --include=*.py

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
```

**Bash:**
```
cd ledgerguard/tests && grep -n "benchmark\|outputs\|OUTPUT" *.py | head -60; echo "---p2 head"; sed -n 1,60p test_p2_evaluation.py
```

**Result:**
```
rehearsal_check.py:6:the adversarial pair, the benchmark comparison, and a non-empty unresolved list
rehearsal_check.py:124:    # 3:20 benchmark
rehearsal_check.py:125:    b, h = state["benchmark"]["baseline"], state["benchmark"]["hybrid"]
test_p1_extended.py:456:    The frozen manifest is what makes the benchmark a measurement rather than a
test_p1_extended.py:460:    from ledgerguard.evaluation import benchmark as bm
test_p1_extended.py:521:    provider that raises for any other reason is a defect, and a benchmark that
---p2 head
"""P2 evaluation machinery.

These protect the analyses themselves. An ablation that silently stops ablating,
or a replay that passes because it compares an object to itself, is worse than
not having one -- it produces a confident number with nothing behind it.

Offline only: every arm here runs on the deterministic stub.
"""

from __future__ import annotations

import json
from decimal import Decimal

from ledgerguard.ai.provider import HeuristicProvider
from ledgerguard.evaluation.ablation import (
    arm_no_shadow_ledger,
    score,
    _states_from_report,
)
from ledgerguard.evaluation.calibration import _bucketise
from ledgerguard.evaluation.cost import CostEstimate
from ledgerguard.evaluation.drift import evaluate as drift_evaluate
from ledgerguard.evaluation.replay import capture, diff, replay
from ledgerguard.evaluation.report import write_reconciliation_report
from ledgerguard.evaluation.scale import measure
from ledgerguard.pipeline import run
from ledgerguard.qa import ask
from ledgerguard.synthetic.fault_injector import build_dataset, split


def _holdout_run(gate: bool = True):
    full = build_dataset()
    _dev, holdout = split(full)
    batch = holdout.batch()
    report = run(
        batch, use_ai=True, provider=HeuristicProvider(),
        lifecycle_by_payment=holdout.lifecycle_by_payment(),
        use_evidence_gate=gate,
    )
    return holdout, batch, report


# ------------------------------------------------------------------- ablation
def test_removing_the_evidence_gate_causes_measurable_false_closures():
    """The ablation must actually ablate. This is the whole safety claim."""
    holdout, _batch, with_gate = _holdout_run(gate=True)
    _h, _b, without_gate = _holdout_run(gate=False)

    on = score("hybrid", "full", _states_from_report(with_gate), holdout)
    off = score("no_gate", "gate off", _states_from_report(without_gate), holdout)

    assert on.false_auto == 0, "the full system must not close anything falsely"
    assert on.false_auto_value_paise == 0
    assert off.false_auto > 0, "gate-off must produce false closures, or it is not ablating"
    assert off.false_auto_value_paise > 0
    assert off.auto_resolved > on.auto_resolved, "gate-off must close strictly more"
    assert off.accuracy < on.accuracy
```

**Bash:**
```
cd <attempt>/work/repo && sed -n 440,540p ledgerguard/tests/test_p1_extended.py; echo "-- rehearsal"; sed -n 1,40p ledgerguard/tests/rehearsal_check.py | head -60; grep -n "outputs\|benchmark.json" ledgerguard/tests/rehearsal_check.py ledgerguard/backend/*.py | head
```

**Result:**
```
        expected_value=100, observed_value=90, evidence={},
    )
    case = CaseResult(
        case_id="pay_U", payment_id="pay_U", order_id="ord_U",
        status=exc.exception_type.value,
        expected=ExpectedSettlement("pay_U", 0, 0, 0, 0, 0, 0),
        settlement=None, exception=exc,
    )
    decision = decide(case, None, None)
    assert decision.state == UNRESOLVED
    assert decision.state != AUTO_RESOLVED


def test_frozen_holdout_mismatch_is_refused(tmp_path, monkeypatch):
    """A holdout that drifted must abort scoring, not be silently re-frozen.

    The frozen manifest is what makes the benchmark a measurement rather than a
    claim. If the generator changes and this check stops firing, every published
    number quietly becomes a score against a different dataset.
    """
    from ledgerguard.evaluation import benchmark as bm

    monkeypatch.setattr(bm, "MANIFEST_DIR", tmp_path)
    full = build_dataset(seed=424242, count=40)
    _dev, holdout = split(full)

    first = bm.freeze_or_verify_holdout(holdout, 424242, 40)
    assert first["holdout_batch_sha256"]
    # Re-verifying the identical holdout is a no-op, not a rewrite.
    assert bm.freeze_or_verify_holdout(holdout, 424242, 40) == first

    drifted = split(build_dataset(seed=525252, count=40))[1]
    with pytest.raises(SystemExit) as excinfo:
        bm.freeze_or_verify_holdout(drifted, 424242, 40)
    assert "FROZEN HOLDOUT MISMATCH" in str(excinfo.value)


def test_hypothesis_must_be_admissible_for_the_exception_it_would_close():
    """A passing evidence battery must not close an exception it never explains.

    The refund battery reconstructs the settlement net. A bank-side discrepancy
    is a different discrepancy, so `unlinked_partial_refund` must not be
    verifiable against it even if every individual check would pass.
    """
    from ledgerguard.evidence.verifier import UNVERIFIED, verify
    from ledgerguard.ledger.shadow_ledger import ExpectedSettlement, ShadowLedger
    from ledgerguard.reconciliation.exceptions import ADMISSIBLE_HYPOTHESES, make_exception
    from ledgerguard.reconciliation.matcher import CaseResult

    assert "unlinked_partial_refund" not in ADMISSIBLE_HYPOTHESES[ExceptionType.BANK_MISMATCH]

    exc = make_exception(
        case_id="pay_B", lifecycle_id="LC", transaction_ids=["pay_B"],
        exception_type=ExceptionType.BANK_MISMATCH,
        detected_by="deterministic_matcher",
        expected_value=1000, observed_value=900, evidence={},
    )
    case = CaseResult(
        case_id="pay_B", payment_id="pay_B", order_id="ord_B",
        status=exc.exception_type.value,
        expected=ExpectedSettlement("pay_B", 0, 0, 0, 0, 0, 0),
        settlement=None, exception=exc,
    )
    result = InvestigationResult(
        hypothesis="unlinked_partial_refund",
        reason="the amounts line up",
        candidate_evidence_ids=["rfnd_X"],
        recommended_action="resolve",
        source="model",
    )
    outcome = verify(ShadowLedger(Batch()), case, result)
    assert outcome.verdict == UNVERIFIED
    assert "not an admissible explanation" in outcome.note
    # The battery must not have run at all -- no checks were weighed.
    assert outcome.checks == []


def test_a_broken_provider_is_reported_not_silently_dropped():
    """A configured-but-broken provider must not look like an absent one.

    A missing key is a legitimate way to run on a subset and stays quiet. A
    provider that raises for any other reason is a defect, and a benchmark that
    silently ran on fewer providers than intended is not the run it claims.
    """
    from ledgerguard.ai import provider as prov

    def _boom(kind: str):
        if kind == "groq":
            raise AttributeError("simulated defect")
        raise prov.ProviderNotConfigured(f"{kind} is not configured")

    original = prov._build
    try:
        prov._build = _boom
        chain = prov.build_chain(["groq", "gemini"])
    finally:
        prov._build = origi
... [1425 more characters in transcript.jsonl]
```

**Agent:** Before editing, I'll snapshot the protected directories and check whether any other code path writes under `outputs/` (requirement 3 depends on that).

**Bash:**
```
mkdir -p ../tmp ../out && (find ledgerguard/evaluation/outputs ledgerguard/evaluation/frozen -type f -exec shasum -a 256 {} \; | sort > ../tmp/protected_before.sha256) && wc -l ../tmp/protected_before.sha256; echo "-- writers"; grep -rn "outputs\|OUTPUT_DIR\|cache" ledgerguard --include=*.py | grep -v "tests/" | grep -iv "^ledgerguard/evaluation/outputs" | head -40
```

**Result:**
```
      21 ../tmp/protected_before.sha256
-- writers
(eval):1: no matches found: --include=*.py
```

**Bash:**
```
grep -rn "outputs\|OUTPUT_DIR\|cache" ledgerguard --include='*.py' | grep -v "/tests/" | head -50
```

**Result:**
```
ledgerguard/ai/provider.py:92:    """Claude-backed investigator using structured outputs."""
ledgerguard/ai/provider.py:225:#: Groq first: fastest of the reliable ones (~1.4s) and it does not cache.
ledgerguard/ai/provider.py:231:#:   (p50 ~53s uncached) and caches temperature-0 responses.
ledgerguard/backend/app.py:12:from functools import lru_cache
ledgerguard/backend/app.py:49:    # lru_cache alone permits duplicate computations on concurrent cache misses.
ledgerguard/backend/app.py:52:        return _cached_state()
ledgerguard/backend/app.py:55:@lru_cache(maxsize=1)
ledgerguard/backend/app.py:56:def _cached_state() -> dict:
ledgerguard/backend/app.py:57:    """Run the controller once, on the frozen holdout, and cache the result."""
ledgerguard/backend/app.py:323:    """Export the exact cached dashboard run, never rerun an investigator.
ledgerguard/backend/app.py:364:    # Revalidate every load. Without this the browser serves a cached page, so an
ledgerguard/backend/app.py:367:    return FileResponse(FRONTEND, headers={"Cache-Control": "no-cache"})
ledgerguard/ai/openai_compatible.py:281:        #: Responses the host served from its own cache rather than the model.
ledgerguard/ai/openai_compatible.py:282:        #: OmniRoute caches temperature-0 requests and does not honour
ledgerguard/ai/openai_compatible.py:283:        #: Cache-Control: no-cache, so repeated runs over a deterministic
ledgerguard/ai/openai_compatible.py:286:        self.cache_hits = 0
ledgerguard/ai/openai_compatible.py:417:        if str(response.headers.get("x-omniroute-cache-hit", "")).lower() == "true":
ledgerguard/ai/openai_compatible.py:418:            self.cache_hits += 1
ledgerguard/ai/openai_compatible.py:471:            # OmniRoute caches temperature-0 requests and ignores
ledgerguard/ai/openai_compatible.py:472:            # Cache-Control: no-cache, so a deterministic dataset replays
ledgerguard/ai/openai_compatible.py:526:        if str(response.headers.get("x-omniroute-cache-hit", "")).lower() == "true":
ledgerguard/ai/openai_compatible.py:527:            self.cache_hits += 1
ledgerguard/evaluation/drift.py:34:OUTPUT_DIR = Path(__file__).parent / "outputs"
ledgerguard/evaluation/drift.py:163:    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
ledgerguard/evaluation/drift.py:165:    (OUTPUT_DIR / "drift.md").write_text(md)
ledgerguard/evaluation/drift.py:166:    (OUTPUT_DIR / "drift.json").write_text(
ledgerguard/evaluation/drift.py:170:    print(f"Artifacts written to {OUTPUT_DIR}")
ledgerguard/ai/fallback.py:171:            "cache_hits": {
ledgerguard/ai/fallback.py:172:                p.name.split(":", 1)[0]: p.cache_hits
ledgerguard/ai/fallback.py:174:                if getattr(p, "cache_hits", 0)
ledgerguard/evaluation/model_comparison.py:29:OUTPUT_DIR = Path(__file__).parent / "outputs"
ledgerguard/evaluation/model_comparison.py:170:    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
ledgerguard/evaluation/model_comparison.py:172:    (OUTPUT_DIR / "model_comparison.md").write_text(md)
ledgerguard/evaluation/model_comparison.py:173:    (OUTPUT_DIR / "model_comparison.json").write_text(
ledgerguard/evaluation/model_comparison.py:177:    print(f"Artifacts written to {OUTPUT_DIR}")
ledgerguard/evaluation/ablation.py:38:OUTPUT_DIR = Path(__file__).parent / "outputs"
ledgerguard/evaluation/ablation.py:411:    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
ledgerguard/evaluation/ablation.py:413:    (OUTPUT_DIR / "ablation.md").write_text(md)
ledgerguard/evaluation/ablation.py:414:    (OUTPUT_DIR / "ablation.json").write_text(
ledgerguard/evaluation/ablation.py:421:    print(f"Artifacts written to {OUTPUT_DIR}")
ledgerguard/evaluation/benchmark.py:7:same frozen holdout, and writes every artifact under evaluation/outputs/.
ledgerguard/evaluation/benchmark.py:36:OUTPUT_DIR = Path(__file__).parent / "outputs"
ledgerguard/evaluation/benchmark.py:254:    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
ledgerguard/evaluation/benchmark.py:277:    (OUTPUT_DIR 
... [669 more characters in transcript.jsonl]
```

**Agent:** Only `benchmark.py` writes the four artifacts, and the frozen manifest is written only when missing, so the change stays local. Next I'll check how `get_provider` handles `stub`, since the tests must never make a live model call.

**Bash:**
```
grep -n "def get_provider" -A30 ledgerguard/ai/provider.py | head -60; grep -n "\"stub\"\|'stub'" ledgerguard/ai/provider.py | head
```

**Result:**
```
313:def get_provider(kind: str | None = None) -> InvestigatorProvider:
314-    """Select an investigator provider.
315-
316-    ``kind`` (or LEDGERGUARD_PROVIDER) may be:
317-      groq | gemini | nvidia | omniroute | openai_compatible
318-                          -- one specific provider (anthropic and cerebras are
319-                             still constructible but are not used here)
320-      fallback            -- chain every configured provider, failing over
321-      stub                -- the offline stand-in
322-      none                -- a dead provider, for testing degradation
323-      auto                -- fallback across everything configured, else the stub
324-
325-    A provider that is named explicitly but cannot be configured is an error,
326-    not a silent downgrade: a run that was meant to measure a model must never
327-    quietly report stub numbers instead.
328-    """
329-    kind = (kind or os.environ.get("LEDGERGUARD_PROVIDER") or "auto").lower()
330-    if kind == "none":
331-        return UnavailableProvider()
332-    if kind == "stub":
333-        return HeuristicProvider()
334-
335-    if kind not in ("auto", "fallback"):
336-        return _build(kind)
337-
338-    from .fallback import FallbackProvider
339-
340-    chain = build_chain()
341-    if not chain:
342-        if kind == "fallback":
343-            raise ValueError("no providers are configured, so no chain can be built")
332:    if kind == "stub":
```

**Agent:** I'll run the existing test suite first to record the baseline.

**Bash:**
```
time .venv/bin/python -m pytest ledgerguard/tests -q 2>&1 | tail -15
```

**Result:**
```
...................................................................      [100%]
=============================== warnings summary ===============================
.venv/lib/python3.14/site-packages/fastapi/testclient.py:1
  <attempt>/work/repo/.venv/lib/python3.14/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
67 passed, 1 warning in 5.21s
.venv/bin/python -m pytest ledgerguard/tests -q 2>&1  1.63s user 0.15s system 31% cpu 5.716 total
tail -15  0.00s user 0.00s system 0% cpu 5.716 total
```

**Agent:** Baseline is 67 passing. Now the change to `benchmark.py`: the new argument, the output-directory resolution, and a refusal for any `PATH` that is inside or equal to `outputs/`, since requirement 3 forbids touching that directory.

**Edit:**
```
<attempt>/work/repo/ledgerguard/evaluation/benchmark.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/evaluation/benchmark.py has been updated successfully.
```

**Edit:**
```
<attempt>/work/repo/ledgerguard/evaluation/benchmark.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/evaluation/benchmark.py has been updated successfully.
```

**Agent:** Next, point the writes and the printed line at `out_dir`, and add the `os` import.

**Edit:**
```
<attempt>/work/repo/ledgerguard/evaluation/benchmark.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/evaluation/benchmark.py has been updated successfully.
```

**Edit:**
```
<attempt>/work/repo/ledgerguard/evaluation/benchmark.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/evaluation/benchmark.py has been updated successfully.
```

**Edit:**
```
<attempt>/work/repo/ledgerguard/evaluation/benchmark.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/evaluation/benchmark.py has been updated successfully.
```

**Edit:**
```
<attempt>/work/repo/ledgerguard/evaluation/benchmark.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/evaluation/benchmark.py has been updated successfully.
```

**Agent:** The code change is in. Before writing tests that compare outputs, I need to know which fields are wall-clock timings, so I'll check what `Metrics.as_dict()` and `export_cases` emit.

**Bash:**
```
grep -n "wall\|latency\|throughput\|_ms\|seconds\|elapsed\|time" ledgerguard/evaluation/metrics.py ledgerguard/evaluation/benchmark.py ledgerguard/evaluation/cost.py | head -40; echo; sed -n '/^def export_cases/,/^def main/p' ledgerguard/evaluation/benchmark.py | head -40
```

**Result:**
```
ledgerguard/evaluation/benchmark.py:14:wall-clock timing fields differing. The AI-investigated path is not reproducible
ledgerguard/evaluation/benchmark.py:129:        _row("Wall time (s)", base.wall_seconds, hyb.wall_seconds),
ledgerguard/evaluation/benchmark.py:130:        _row("Throughput (cases/s)", base.throughput_per_second, hyb.throughput_per_second),
ledgerguard/evaluation/benchmark.py:134:        _row("Investigation latency p50 (ms)", base.latency_p50_ms, hyb.latency_p50_ms),
ledgerguard/evaluation/benchmark.py:135:        _row("Investigation latency p95 (ms)", base.latency_p95_ms, hyb.latency_p95_ms),
ledgerguard/evaluation/benchmark.py:225:                    "latency_ms": round(outcome.investigation.latency_ms, 2),
ledgerguard/evaluation/metrics.py:68:    # --- cost / throughput -------------------------------------------------
ledgerguard/evaluation/metrics.py:69:    wall_seconds: float = 0.0
ledgerguard/evaluation/metrics.py:70:    throughput_per_second: float = 0.0
ledgerguard/evaluation/metrics.py:75:    latency_p50_ms: float = 0.0
ledgerguard/evaluation/metrics.py:76:    latency_p95_ms: float = 0.0
ledgerguard/evaluation/metrics.py:176:    m.wall_seconds = round(report.wall_seconds, 3)
ledgerguard/evaluation/metrics.py:177:    m.throughput_per_second = (
ledgerguard/evaluation/metrics.py:178:        round(m.total_cases / report.wall_seconds, 1) if report.wall_seconds else 0.0
ledgerguard/evaluation/metrics.py:188:    m.latency_p50_ms = _percentile(report.investigation_latencies_ms, 50)
ledgerguard/evaluation/metrics.py:189:    m.latency_p95_ms = _percentile(report.investigation_latencies_ms, 95)

def export_cases(report: RunReport, dataset: Dataset, path: Path) -> None:
    """Full per-case detail, used by the dashboard and the demo."""
    truth = {lc.payment.payment_id: lc.lifecycle_id for lc in dataset.lifecycles}
    payload = []
    for outcome in report.outcomes:
        case = outcome.case
        entry = {
            "case_id": outcome.case_id,
            "lifecycle_id": truth.get(case.payment_id, ""),
            "payment_id": case.payment_id,
            "order_id": case.order_id,
            "state": outcome.state,
            "exception_type": case.exception.exception_type.value if case.exception else None,
            "expected": case.expected.as_dict(),
            "observed_settlement": (
                case.exception.evidence.get("observed_settlement") if case.exception else None
            ),
            "exposure_paise": outcome.exposure_paise,
            "invariants": [i.as_dict() for i in case.invariants],
            "investigation": (
                {
                    "hypothesis": outcome.investigation.result.hypothesis,
                    "reason": outcome.investigation.result.reason,
                    "recommended_action": outcome.investigation.result.recommended_action,
                    "candidate_evidence_ids": outcome.investigation.result.candidate_evidence_ids,
                    "source": outcome.investigation.result.source,
                    "model_name": outcome.investigation.result.model_name,
                    "latency_ms": round(outcome.investigation.latency_ms, 2),
                    # Set when the controller stripped ids the model invented. The
                    # strongest single sign of an LLM fabricating a record, so it
                    # belongs in the artifact, not only in an aggregate count.
                    "controller_note": outcome.investigation.result.error,
                }
                if outcome.investigation
                else None
            ),
            "verification": outcome.verification.as_dict() if outcome.verification else None,
            "decision": asdict(outcome.decision) if outcome.decision else None,
        }
        payload.append(entry)
```

**Agent:** Timing fields are `wall_seconds`, `throughput_per_second`, `latency_p50_ms`, `latency_p95_ms` and per-case `latency_ms`, plus the matching rows in `benchmark.md`. I'll normalise those out when comparing runs. Now the new test file, which patches `OUTPUT_DIR` and `MANIFEST_DIR` so nothing touches the real `outputs/` or `frozen/`.

**Write:**
```
<attempt>/work/repo/ledgerguard/tests/test_benchmark_output_dir.py
```

**Result:**
```
File created successfully at: <attempt>/work/repo/ledgerguard/tests/test_benchmark_output_dir.py (file state is current in your context — no need to Read it back)
```

**Agent:** The `_strip_timing_md` helper I wrote is convoluted. I'll simplify it to a single substring check.

**Edit:**
```
<attempt>/work/repo/ledgerguard/tests/test_benchmark_output_dir.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/tests/test_benchmark_output_dir.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

**Bash:**
```
.venv/bin/python -m pytest ledgerguard/tests/test_benchmark_output_dir.py -q 2>&1 | tail -30
```

**Result:**
```
.........                                                                [100%]
9 passed in 0.18s
```

**Agent:** All 9 new tests pass. Next I'll run the full suite, check `--help`, and do one real-data run against the actual frozen holdout using the offline stub, writing to a scratch directory. That confirms the real manifest verifies without being touched.

**Bash:**
```
.venv/bin/python -m pytest ledgerguard/tests -q 2>&1 | tail -3; .venv/bin/python -m ledgerguard.evaluation.benchmark --help | tail -8; time .venv/bin/python -m ledgerguard.evaluation.benchmark --provider stub --output-dir ../tmp/real_check/nested 2>&1 | tail -4; ls -la ../tmp/real_check/nested
```

**Result:**
```
-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
76 passed, 1 warning in 4.74s
  --count COUNT
  --split {holdout,dev,all}
                        which slice to score (default: the frozen holdout)
  --provider PROVIDER   auto | fallback | groq | gemini | nvidia | omniroute |
                        anthropic | cerebras | openai_compatible | stub | none
  --output-dir PATH     write the artifacts to PATH instead of
                        evaluation/outputs/ (created, with parents, if
                        missing). Must not be inside evaluation/outputs/.
  benchmark.md, benchmark.json, cases.json
  unresolved_exceptions.csv (10 rows)

NOTE: the hybrid run used the offline heuristic stub, not a model. Configure a provider key (GROQ_API_KEY, GEMINI_API_KEY, NVIDIA_API_KEY or OMNIROUTE_API_KEY) and rerun to measure against a real investigator.
.venv/bin/python -m ledgerguard.evaluation.benchmark --provider stub   2>&1  0.16s user 0.03s system 97% cpu 0.189 total
tail -4  0.00s user 0.00s system 1% cpu 0.189 total
total 520
drwxr-xr-x@ 6 user  staff     192 Nov  1 23:24 .
drwxr-xr-x@ 3 user  staff      96 Nov  1 23:24 ..
-rw-r--r--@ 1 user  staff    6368 Nov  1 23:24 benchmark.json
-rw-r--r--@ 1 user  staff    1941 Nov  1 23:24 benchmark.md
-rw-r--r--@ 1 user  staff  244525 Nov  1 23:24 cases.json
-rw-r--r--@ 1 user  staff    5027 Nov  1 23:24 unresolved_exceptions.csv
```

**Agent:** Full suite passes (76 = 67 existing + 9 new), and the real-holdout run wrote its four artifacts into the scratch directory. Now I'll verify that `outputs/` and `frozen/` are byte-identical to the snapshot taken before my changes.

**Bash:**
```
find ledgerguard/evaluation/outputs ledgerguard/evaluation/frozen -type f -exec shasum -a 256 {} \; | sort > ../tmp/protected_after.sha256; diff ../tmp/protected_before.sha256 ../tmp/protected_after.sha256 && echo "PROTECTED DIRS UNCHANGED"; find ledgerguard/evaluation/outputs ledgerguard/evaluation/frozen -newer ../tmp/protected_before.sha256 | head; ls ledgerguard/evaluation/outputs | wc -l; ls ledgerguard/evaluation/frozen
```

**Result:**
```
PROTECTED DIRS UNCHANGED
      20
holdout_20260905_320.json
```

**Agent:** Both protected directories are unchanged. I'll re-read the final `main()` head to check the resolution logic once more.

**Bash:**
```
sed -n '/^def main/,/^    full = /p' ledgerguard/evaluation/benchmark.py
```

**Result:**
```
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="LedgerGuard benchmark")
    parser.add_argument("--seed", type=int, default=20260905)
    parser.add_argument("--count", type=int, default=320)
    parser.add_argument(
        "--split", choices=["holdout", "dev", "all"], default="holdout",
        help="which slice to score (default: the frozen holdout)",
    )
    parser.add_argument(
        "--provider",
        default=None,
        help="auto | fallback | groq | gemini | nvidia | omniroute | "
        "anthropic | cerebras | openai_compatible | stub | none",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        metavar="PATH",
        help="write the artifacts to PATH instead of evaluation/outputs/ "
        "(created, with parents, if missing). Must not be inside evaluation/outputs/.",
    )
    args = parser.parse_args(argv)

    if args.output_dir is None:
        out_dir = OUTPUT_DIR
    else:
        out_dir = Path(os.path.abspath(args.output_dir))
        if out_dir.resolve() == OUTPUT_DIR.resolve() or OUTPUT_DIR.resolve() in out_dir.resolve().parents:
            parser.error(
                f"--output-dir must not be inside {OUTPUT_DIR}: that directory is "
                "reserved for the published artifacts"
            )
    out_dir.mkdir(parents=True, exist_ok=True)

    full = build_dataset(seed=args.seed, count=args.count)
```

**Agent:** The logic reads correctly. Last step: record the decisions and gaps in `../out/NOTES.md`.

**Write:**
```
<attempt>/out/NOTES.md
```

**Result (error):**
```
EPERM: operation not permitted, open '<attempt>'
```

**Agent:** That path was wrong: `../out` relative to `repo/` is `work/out/`, not the run root. I'll retry at the correct location.

**Bash:**
```
cd <attempt>/work && pwd && ls -d out tmp && ls out tmp | head
```

**Result:**
```
<attempt>/work
out
tmp
out:

tmp:
cc-socks
claude-501
protected_after.sha256
protected_before.sha256
pytest-of-user
real_check
Shell cwd was reset to <attempt>/work/repo
```

**Write:**
```
<attempt>/work/out/NOTES.md
```

**Result:**
```
File created successfully at: <attempt>/work/out/NOTES.md (file state is current in your context — no need to Read it back)
```

**Agent:** `python -m ledgerguard.evaluation.benchmark --output-dir PATH` now writes all four artifacts to `PATH`. The full suite passes (76 tests: the 67 existing plus 9 new), and `outputs/` and `frozen/` are byte-identical to their state before I started.

What changed:
- **`ledgerguard/evaluation/benchmark.py`**: the new option. Without it, `out_dir` is the existing `OUTPUT_DIR`, so the default run is unchanged. With it, the directory is created with parents, relative paths resolve against the working directory, and the "Artifacts written to" line prints the resolved path. The frozen manifest code is untouched.
- **`ledgerguard/tests/test_benchmark_output_dir.py`**: 9 new tests. They run offline on the stub investigator with `OUTPUT_DIR` and `MANIFEST_DIR` patched to temp paths. They cover nested creation, relative paths, the printed line, default behaviour, equivalence with a default run, the manifest going to `frozen/` (and still being verified), and the refusal cases.

Decisions to review:
- **A `PATH` inside `outputs/` (or equal to it) is refused** with exit code 2. Requirement 3 says nothing under `outputs/` may change, so writing there would break it.
- **Equivalence is checked after removing timing fields** (`wall_seconds`, `throughput_per_second`, the latency fields, and the matching `benchmark.md` rows). Everything else matches a default run exactly.
- **An empty `PATH` can be left behind** if the frozen-holdout check aborts. The default run already behaves this way.

I also ran the real frozen holdout with `--provider stub` into a scratch directory. The existing manifest verified without a mismatch. I did not run a live provider or regenerate the published numbers. `README.md` still describes only the default output location, and I left it alone.

Notes are in `work/out/NOTES.md`.
