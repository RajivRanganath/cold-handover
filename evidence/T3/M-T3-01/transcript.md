# M-T3-01 transcript (PASS)

**Agent:** I'll start with the handover docs at the repo root, then the benchmark module.

**Bash:**
```
ls -la && ls -la ledgerguard/evaluation ledgerguard/evaluation/outputs ledgerguard/evaluation/frozen 2>&1 | head -80
```

**Result:**
```
total 88
drwxr-xr-x@ 10 user  staff    320 Nov  1 23:25 .
drwxr-xr-x@  5 user  staff    160 Nov  1 23:25 ..
-rw-r--r--@  1 user  staff   1992 Nov  1 23:25 .env.example
-rw-r--r--@  1 user  staff     56 Nov  1 23:25 .gitignore
drwxr-xr-x@  7 user  staff    224 Nov  1 23:25 .venv
drwxr-xr-x@  7 user  staff    224 Nov  1 23:25 docs
drwxr-xr-x@ 14 user  staff    448 Nov  1 23:25 ledgerguard
-rw-r--r--@  1 user  staff  26848 Nov  1 23:25 README.md
-rw-r--r--@  1 user  staff    466 Nov  1 23:25 requirements.txt
-rwxr-xr-x@  1 user  staff   1447 Nov  1 23:25 run_demo.sh
ledgerguard/evaluation:
total 208
-rw-r--r--@  1 user  staff      0 Nov  1 23:25 __init__.py
drwxr-xr-x@ 17 user  staff    544 Nov  1 23:25 .
drwxr-xr-x@ 14 user  staff    448 Nov  1 23:25 ..
-rw-r--r--@  1 user  staff  15897 Nov  1 23:25 ablation.py
-rw-r--r--@  1 user  staff    681 Nov  1 23:25 baseline.py
-rw-r--r--@  1 user  staff  16017 Nov  1 23:25 benchmark.py
-rw-r--r--@  1 user  staff   6945 Nov  1 23:25 calibration.py
-rw-r--r--@  1 user  staff   3854 Nov  1 23:25 cost.py
-rw-r--r--@  1 user  staff   6225 Nov  1 23:25 drift.py
drwxr-xr-x@  3 user  staff     96 Nov  1 23:25 frozen
-rw-r--r--@  1 user  staff   7063 Nov  1 23:25 metrics.py
-rw-r--r--@  1 user  staff   7211 Nov  1 23:25 model_comparison.py
-rw-r--r--@  1 user  staff   6449 Nov  1 23:25 no_gate_ablation.py
drwxr-xr-x@ 22 user  staff    704 Nov  1 23:25 outputs
-rw-r--r--@  1 user  staff   6679 Nov  1 23:25 replay.py
-rw-r--r--@  1 user  staff   7159 Nov  1 23:25 report.py
-rw-r--r--@  1 user  staff   5606 Nov  1 23:25 scale.py

ledgerguard/evaluation/frozen:
total 8
drwxr-xr-x@  3 user  staff    96 Nov  1 23:25 .
drwxr-xr-x@ 17 user  staff   544 Nov  1 23:25 ..
-rw-r--r--@  1 user  staff  1388 Nov  1 23:25 holdout_20260905_320.json

ledgerguard/evaluation/outputs:
total 992
drwxr-xr-x@ 22 user  staff     704 Nov  1 23:25 .
drwxr-xr-x@ 17 user  staff     544 Nov  1 23:25 ..
-rw-r--r--@  1 user  staff    6742 Nov  1 23:25 ablation.json
-rw-r--r--@  1 user  staff    1622 Nov  1 23:25 ablation.md
-rw-r--r--@  1 user  staff    6707 Nov  1 23:25 benchmark.json
-rw-r--r--@  1 user  staff    1975 Nov  1 23:25 benchmark.md
-rw-r--r--@  1 user  staff     829 Nov  1 23:25 calibration.json
-rw-r--r--@  1 user  staff    1656 Nov  1 23:25 calibration.md
-rw-r--r--@  1 user  staff  240238 Nov  1 23:25 cases.json
-rw-r--r--@  1 user  staff  148905 Nov  1 23:25 decision_log.json
-rw-r--r--@  1 user  staff    2427 Nov  1 23:25 drift.json
-rw-r--r--@  1 user  staff    1602 Nov  1 23:25 drift.md
-rw-r--r--@  1 user  staff   15987 Nov  1 23:25 evidence_ledger.csv
-rw-r--r--@  1 user  staff    3445 Nov  1 23:25 model_comparison.json
-rw-r--r--@  1 user  staff    1513 Nov  1 23:25 model_comparison.md
-rw-r--r--@  1 user  staff    1203 Nov  1 23:25 no_gate_ablation.json
-rw-r--r--@  1 user  staff    1771 Nov  1 23:25 no_gate_ablation.md
-rw-r--r--@  1 user  staff   19177 Nov  1 23:25 reconciliation_report.csv
-rw-r--r--@  1 user  staff     800 Nov  1 23:25 reconciliation_report.md
-rw-r--r--@  1 user  staff    1268 Nov  1 23:25 scale.json
-rw-r--r--@  1 user  staff     935 Nov  1 23:25 scale.md
-rw-r--r--@  1 user  staff    6659 Nov  1 23:25 unresolved_exceptions.csv
```

**Bash:**
```
ls *.md 2>/dev/null; ls ../ ; ls ../out ../tmp 2>&1
```

**Result:**
```
README.md
out
repo
tmp
../out:

../tmp:
cc-socks
claude-501
```

**Bash:**
```
ls -R docs; cat ledgerguard/evaluation/benchmark.py
```

**Result:**
```
analyses.md
architecture.md
evaluation.md
limitations.md
model_comparison.md
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
        "Generated by `python -m ledgerguard.evaluation.benchmark`. Every figure
... [12093 more characters in transcript.jsonl]
```

**Agent:** The benchmark module is clear. Next I'll check where `OUTPUT_DIR` is used elsewhere, which tests cover the benchmark, and how the test suite runs.

**Bash:**
```
grep -rn "OUTPUT_DIR\|evaluation.benchmark\|benchmark import\|MANIFEST_DIR\|manifest_path" --include=*.py --include=*.md --include=*.sh . | grep -v "^./.venv"; echo ---; grep -rln "benchmark" ledgerguard --include=*.py | grep -i test; ls ledgerguard; find . -path ./.venv -prune -o -name "test*" -print | head -50
```

**Result:**
```
(eval):1: no matches found: --include=*.py
---
(eval):1: no matches found: --include=*.py
__init__.py
ai
backend
evaluation
evidence
frontend
ledger
pipeline.py
qa.py
reconciliation
synthetic
tests
./ledgerguard/tests
./ledgerguard/tests/test_p0_core.py
./ledgerguard/tests/test_p2_evaluation.py
./ledgerguard/tests/test_p1_compound.py
./ledgerguard/tests/test_p1_extended.py
./ledgerguard/tests/test_fallback.py
./ledgerguard/tests/test_evidence_download.py
./ledgerguard/tests/test_dashboard_startup.py
```

**Bash:**
```
grep -rn "OUTPUT_DIR\|evaluation.benchmark\|benchmark import\|MANIFEST_DIR\|manifest_path" . --exclude-dir=.venv | head -40; echo ---; grep -n "benchmark" ledgerguard/tests/*.py | head -60
```

**Result:**
```
run_demo.sh:19:$PY -m ledgerguard.evaluation.benchmark >/dev/null
README.md:232:python -m ledgerguard.evaluation.benchmark --provider groq
README.md:302:`python -m ledgerguard.evaluation.benchmark --provider fallback` prints exactly
README.md:332:.venv/bin/python -m ledgerguard.evaluation.benchmark
README.md:375:From `python -m ledgerguard.evaluation.benchmark`:
README.md:451:python -m ledgerguard.evaluation.benchmark          # rules only vs hybrid
docs/analyses.md:8:| Benchmark | `evaluation.benchmark` | `benchmark.{md,json}` | Does the AI layer earn its place on top of the rules? |
docs/evaluation.md:6:.venv/bin/python -m ledgerguard.evaluation.benchmark
ledgerguard/backend/app.py:21:from ..evaluation.benchmark import batch_digest
ledgerguard/tests/test_p1_extended.py:462:    monkeypatch.setattr(bm, "MANIFEST_DIR", tmp_path)
ledgerguard/evaluation/ablation.py:38:OUTPUT_DIR = Path(__file__).parent / "outputs"
ledgerguard/evaluation/ablation.py:411:    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
ledgerguard/evaluation/ablation.py:413:    (OUTPUT_DIR / "ablation.md").write_text(md)
ledgerguard/evaluation/ablation.py:414:    (OUTPUT_DIR / "ablation.json").write_text(
ledgerguard/evaluation/ablation.py:421:    print(f"Artifacts written to {OUTPUT_DIR}")
ledgerguard/frontend/index.html:664:      runs. Every figure is computed by <code>python -m ledgerguard.evaluation.benchmark</code>.</p>
ledgerguard/evaluation/replay.py:34:OUTPUT_DIR = Path(__file__).parent / "outputs"
ledgerguard/evaluation/replay.py:153:    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
ledgerguard/evaluation/replay.py:154:    path = OUTPUT_DIR / "decision_log.json"
ledgerguard/evaluation/report.py:29:OUTPUT_DIR = Path(__file__).parent / "outputs"
ledgerguard/evaluation/report.py:46:    report: RunReport, output_dir: Path = OUTPUT_DIR
ledgerguard/evaluation/report.py:170:    print((OUTPUT_DIR / "reconciliation_report.md").read_text())
ledgerguard/evaluation/report.py:171:    print(f"Artifacts written to {OUTPUT_DIR}")
ledgerguard/evaluation/no_gate_ablation.py:28:OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
ledgerguard/evaluation/no_gate_ablation.py:29:COMPARISON = OUTPUT_DIR / "model_comparison.json"
ledgerguard/evaluation/no_gate_ablation.py:30:ABLATION = OUTPUT_DIR / "ablation.json"
ledgerguard/evaluation/no_gate_ablation.py:151:    (OUTPUT_DIR / "no_gate_ablation.json").write_text(json.dumps(r, indent=2) + "\n")
ledgerguard/evaluation/no_gate_ablation.py:153:    (OUTPUT_DIR / "no_gate_ablation.md").write_text(md)
ledgerguard/evaluation/no_gate_ablation.py:155:    print(f"Artifacts written to {OUTPUT_DIR}")
ledgerguard/evaluation/scale.py:32:OUTPUT_DIR = Path(__file__).parent / "outputs"
ledgerguard/evaluation/scale.py:144:    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
ledgerguard/evaluation/scale.py:146:    (OUTPUT_DIR / "scale.md").write_text(md)
ledgerguard/evaluation/scale.py:147:    (OUTPUT_DIR / "scale.json").write_text(
ledgerguard/evaluation/benchmark.py:3:    python -m ledgerguard.evaluation.benchmark
ledgerguard/evaluation/benchmark.py:36:OUTPUT_DIR = Path(__file__).parent / "outputs"
ledgerguard/evaluation/benchmark.py:37:MANIFEST_DIR = Path(__file__).parent / "frozen"
ledgerguard/evaluation/benchmark.py:40:def manifest_path(seed: int, count: int) -> Path:
ledgerguard/evaluation/benchmark.py:46:    return MANIFEST_DIR / f"holdout_{seed}_{count}.json"
ledgerguard/evaluation/benchmark.py:62:    path = manifest_path(seed, count)
ledgerguard/evaluation/benchmark.py:76:    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
---
ledgerguard/tests/rehearsal_check.py:6:the adversarial pair, the benchmark comparison, and a non-empty unresolved list
ledgerguard/tests/rehearsal_check.py:124:    # 3:20 benchmark
ledgerguard/tests/rehearsal_check.py:125:    b, h = state["benchmark"]["baseline"], state["benchmark"]["hybrid"]
ledgerguard/tests/test_p1_extended.py:456:    The frozen manifest is what makes the benchmark a measurement rather than a
led
... [215 more characters in transcript.jsonl]
```

**Bash:**
```
sed -n 440,540p ledgerguard/tests/test_p1_extended.py; echo ---; cat docs/evaluation.md | head -40; echo ---; cat ledgerguard/tests/test_p2_evaluation.py | head -60
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
... [3978 more characters in transcript.jsonl]
```

**Agent:** Before deciding how to route the writes, I want to know whether anything else in the run path writes under `outputs/` (for example a response cache), since requirement 3 forbids that.

**Bash:**
```
grep -rn "outputs\|CACHE_DIR\|cache_dir\|\.cache" ledgerguard --include=*.py | grep -v "tests/" | head -30; echo ---; cat .gitignore; echo ---; ls ledgerguard/evaluation/outputs | wc -l; shasum -a 256 ledgerguard/evaluation/outputs/* ledgerguard/evaluation/frozen/* > ../tmp/before_hashes.txt 2>/dev/null || (mkdir -p ../tmp && shasum -a 256 ledgerguard/evaluation/outputs/* ledgerguard/evaluation/frozen/* > ../tmp/before_hashes.txt); wc -l ../tmp/before_hashes.txt
```

**Result:**
```
(eval):1: no matches found: --include=*.py
---
.venv/
__pycache__/
*.pyc
.env
.pytest_cache/
.DS_Store
---
      20
      21 ../tmp/before_hashes.txt
```

**Bash:**
```
cd ledgerguard && grep -rn "outputs\|CACHE_DIR\|cache_dir\|\.cache" . --include=*.py | grep -v "tests/" | head -30; cd ..; echo; ls -la ledgerguard/evaluation/outputs | head -3; find ledgerguard -name "*.json" -path "*cache*" | head
```

**Result:**
```
(eval):1: no matches found: --include=*.py

total 992
drwxr-xr-x@ 22 user  staff     704 Nov  1 23:25 .
drwxr-xr-x@ 17 user  staff     544 Nov  1 23:25 ..
```

**Bash:**
```
cd ledgerguard && grep -rn "outputs\|CACHE_DIR\|cache_dir\|\.cache" . | grep "\.py:" | grep -v "tests/" | head -30; cd ..
```

**Result:**
```
ai/fallback.py:172:                p.name.split(":", 1)[0]: p.cache_hits
ai/provider.py:92:    """Claude-backed investigator using structured outputs."""
evaluation/no_gate_ablation.py:28:OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
evaluation/scale.py:32:OUTPUT_DIR = Path(__file__).parent / "outputs"
ai/openai_compatible.py:286:        self.cache_hits = 0
ai/openai_compatible.py:418:            self.cache_hits += 1
ai/openai_compatible.py:527:            self.cache_hits += 1
evaluation/ablation.py:38:OUTPUT_DIR = Path(__file__).parent / "outputs"
evaluation/drift.py:34:OUTPUT_DIR = Path(__file__).parent / "outputs"
evaluation/replay.py:5:and outputs of a run, re-run from the captured inputs alone, and assert the
evaluation/replay.py:34:OUTPUT_DIR = Path(__file__).parent / "outputs"
evaluation/benchmark.py:7:same frozen holdout, and writes every artifact under evaluation/outputs/.
evaluation/benchmark.py:36:OUTPUT_DIR = Path(__file__).parent / "outputs"
evaluation/model_comparison.py:29:OUTPUT_DIR = Path(__file__).parent / "outputs"
evaluation/report.py:29:OUTPUT_DIR = Path(__file__).parent / "outputs"
evaluation/calibration.py:35:OUTPUT_DIR = Path(__file__).parent / "outputs"
```

**Agent:** Only `benchmark.py` writes into `outputs/` on its path. I'll confirm the provider response cache is not file-based under the repo, and run the existing test suite for a baseline.

**Bash:**
```
grep -n "cache" ledgerguard/ai/openai_compatible.py | head -20; cd <attempt>/work/repo && .venv/bin/python -m pytest -q ledgerguard/tests 2>&1 | tail -15
```

**Result:**
```
281:        #: Responses the host served from its own cache rather than the model.
282:        #: OmniRoute caches temperature-0 requests and does not honour
283:        #: Cache-Control: no-cache, so repeated runs over a deterministic
286:        self.cache_hits = 0
417:        if str(response.headers.get("x-omniroute-cache-hit", "")).lower() == "true":
418:            self.cache_hits += 1
471:            # OmniRoute caches temperature-0 requests and ignores
472:            # Cache-Control: no-cache, so a deterministic dataset replays
526:        if str(response.headers.get("x-omniroute-cache-hit", "")).lower() == "true":
527:            self.cache_hits += 1
...................................................................      [100%]
=============================== warnings summary ===============================
.venv/lib/python3.14/site-packages/fastapi/testclient.py:1
  <attempt>/work/repo/.venv/lib/python3.14/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
67 passed, 1 warning in 5.15s
```

**Agent:** Baseline is 67 passing. Before writing the tests I need the timing field names (for the "same apart from wall-clock" check) and how the `stub` provider is selected.

**Bash:**
```
grep -n "wall\|latency\|throughput\|def as_dict" ledgerguard/evaluation/metrics.py; echo ---; grep -n "def get_provider" -A25 ledgerguard/ai/provider.py | head -50; grep -n "stub" ledgerguard/ai/provider.py | head
```

**Result:**
```
68:    # --- cost / throughput -------------------------------------------------
69:    wall_seconds: float = 0.0
70:    throughput_per_second: float = 0.0
75:    latency_p50_ms: float = 0.0
76:    latency_p95_ms: float = 0.0
80:    def as_dict(self) -> dict:
176:    m.wall_seconds = round(report.wall_seconds, 3)
177:    m.throughput_per_second = (
178:        round(m.total_cases / report.wall_seconds, 1) if report.wall_seconds else 0.0
188:    m.latency_p50_ms = _percentile(report.investigation_latencies_ms, 50)
189:    m.latency_p95_ms = _percentile(report.investigation_latencies_ms, 95)
---
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
15:that, so a stub run is never mistaken for a model run.
148:    name = "heuristic_stub"
186:            return _to_result(out, source="heuristic_stub", model_name=None)
199:            return _to_result(out, source="heuristic_stub", model_name=None)
208:        return _to_result(out, source="heuristic_stub", model_name=None)
321:      stub                -- the offline stand-in
323:      auto                -- fallback across everything configured, else the stub
327:    quietly report stub numbers instead.
332:    if kind == "stub":
```

**Agent:** I have what I need. The plan:

- Keep the default path exactly as it is.
- With `--output-dir`, resolve the path, create it, and send all four writes there.
- Refuse a path inside `outputs/` up front, because requirement 3 forbids touching it.
- The manifest code is untouched, so it still reads and verifies against `frozen/`.

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

**Bash:**
```
.venv/bin/python - <<'EOF'
import re
p = "ledgerguard/evaluation/benchmark.py"
s = open(p).read()
head, sep, tail = s.partition("def main(")
n_before = tail.count("OUTPUT_DIR")
tail = tail.replace("(OUTPUT_DIR / ", "(out_dir / ").replace("write_unresolved_csv(\n        hybrid_report, scored, OUTPUT_DIR / ", "write_unresolved_csv(\n        hybrid_report, scored, out_dir / ").replace("export_cases(hybrid_report, scored, OUTPUT_DIR / ", "export_cases(hybrid_report, scored, out_dir / ").replace('print(f"\\nArtifacts written to {OUTPUT_DIR}")', 'print(f"\\nArtifacts written to {out_dir}")')
open(p, "w").write(head + sep + tail)
print("OUTPUT_DIR refs in main before:", n_before, "after:", tail.count("OUTPUT_DIR"))
EOF
grep -n "out_dir\|OUTPUT_DIR" ledgerguard/evaluation/benchmark.py
```

**Result:**
```
OUTPUT_DIR refs in main before: 8 after: 3
38:OUTPUT_DIR = Path(__file__).parent / "outputs"
263:        out_dir = OUTPUT_DIR
265:        out_dir = Path(args.output_dir).resolve()
266:        if out_dir == OUTPUT_DIR.resolve() or OUTPUT_DIR.resolve() in out_dir.parents:
268:                f"--output-dir {out_dir} is inside evaluation/outputs/, which is "
272:    out_dir.mkdir(parents=True, exist_ok=True)
295:    (out_dir / "benchmark.md").write_text(md)
296:    (out_dir / "benchmark.json").write_text(
319:        hybrid_report, scored, out_dir / "unresolved_exceptions.csv"
321:    export_cases(hybrid_report, scored, out_dir / "cases.json")
355:    print(f"\nArtifacts written to {out_dir}")
```

**Agent:** The edit landed as intended: `main()` now writes only through `out_dir`, and the only remaining `OUTPUT_DIR` uses are the default assignment and the refusal check. Now I'll add a new test file. It uses a small seed and count, a temporary frozen dir, and a temporary `OUTPUT_DIR`, so it never touches the real `outputs/` or `frozen/`.

**Write:**
```
<attempt>/work/repo/ledgerguard/tests/test_benchmark_output_dir.py
```

**Result:**
```
File created successfully at: <attempt>/work/repo/ledgerguard/tests/test_benchmark_output_dir.py (file state is current in your context — no need to Read it back)
```

**Agent:** I left a muddled line in the content-comparison test. I'll clean that up before running anything.

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
.venv/bin/python -m pytest -q ledgerguard/tests/test_benchmark_output_dir.py 2>&1 | tail -40
```

**Result:**
```
.......                                                                  [100%]
7 passed in 0.18s
```

**Agent:** All seven pass. A 0.18s run is fast for a full benchmark, so I'll confirm the comparison has real content behind it, then run the whole suite and check the protected directories are unchanged.

**Bash:**
```
.venv/bin/python -m pytest -q ledgerguard/tests 2>&1 | tail -3; .venv/bin/python - <<'EOF'
import json, tempfile, pathlib
from ledgerguard.evaluation import benchmark as bm
import ledgerguard.tests.test_benchmark_output_dir as t
d = pathlib.Path(tempfile.mkdtemp())
bm.MANIFEST_DIR = d/"frozen"; bm.OUTPUT_DIR = d/"o"
bm.main(["--seed","424242","--count","40","--provider","stub","--output-dir",str(d/"x")])
print("cases:", len(json.loads((d/"x/cases.json").read_text())), "unresolved csv bytes:", (d/"x/unresolved_exceptions.csv").stat().st_size)
print([l for l in (d/"x/benchmark.md").read_text().splitlines() if "Total cases" in l or "Wall" in l])
EOF
shasum -a 256 ledgerguard/evaluation/outputs/* ledgerguard/evaluation/frozen/* > ../tmp/after_hashes.txt; diff ../tmp/before_hashes.txt ../tmp/after_hashes.txt && echo "outputs/frozen UNCHANGED"
```

**Result:**
```
-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
74 passed, 1 warning in 4.78s
# Benchmark: rules only vs LedgerGuard

Frozen holdout, seed `424242`, generator `1.0.0`, 12 lifecycles, batch SHA-256 `579a97739dfa64ad`.

Investigator for the hybrid run: `heuristic_stub`.

Generated by `python -m ledgerguard.evaluation.benchmark`. Every figure below comes from that run.

| Metric | Rules only | LedgerGuard |
|---|---|---|
| Total cases | 12 | 12 |
| Total captured value | INR 196936.00 | INR 196936.00 |
| Matched (no exception) | 7 | 7 |
| Match rate | 58.3% | 58.3% |
| Exceptions raised | 5 | 5 |
| False exceptions (clean case flagged) | 0 | 0 |
| Missed faults (fault case matched) | 0 | 0 |
| Exception type correct (of exceptions raised) | 5 | 5 |
| Disposition accuracy | 75.0% | 100.0% |
| | | |
| Auto resolved | 0 | 3 |
| Exceptions correctly resolved | 0 | 3 |
| Exceptions incorrectly resolved | 0 | 0 |
| Correct abstentions | 2 | 2 |
| Unnecessary abstentions | 3 | 0 |
| Human review required | 5 | 2 |
| Unresolved | 0 | 0 |
| Value left unresolved | INR 16938.40 | INR 7131.10 |
| | | |
| **False auto resolutions** | **0** | **0** |
| **Value falsely auto resolved** | **INR 0.00** | **INR 0.00** |
| | | |
| Wall time (s) | 0.001 | 0.001 |
| Throughput (cases/s) | 17494.8 | 13560.6 |
| Investigations run | 0 | 5 |
| Investigations per 100 records | 0.0 | 41.67 |
| Model calls per 100 records | 0.0 | 0.0 |
| Investigation latency p50 (ms) | 0.0 | 0.01 |
| Investigation latency p95 (ms) | 0.0 | 0.02 |

## Per fault class

| Fault class | n | rules only correct | LedgerGuard correct | LedgerGuard auto resolved | LedgerGuard false auto |
|---|---|---|---|---|---|
| F3_UNLINKED_PARTIAL_REFUND | 3 | 0 | 3 | 3 | 0 |
| F6_INCORRECT_LINKAGE | 2 | 2 | 2 | 0 | 0 |
| NONE | 7 | 7 | 7 | 0 | 0 |


Artifacts written to <attempt>/work/tmp/tmpldi4w50l/x
  benchmark.md, benchmark.json, cases.json
  unresolved_exceptions.csv (2 rows)

NOTE: the hybrid run used the offline heuristic stub, not a model. Configure a provider key (GROQ_API_KEY, GEMINI_API_KEY, NVIDIA_API_KEY or OMNIROUTE_API_KEY) and rerun to measure against a real investigator.
cases: 12 unresolved csv bytes: 1356
['| Total cases | 12 | 12 |', '| Wall time (s) | 0.001 | 0.001 |']
outputs/frozen UNCHANGED
```

**Agent:** 74 pass (67 existing + 7 new), the synthetic run produces real content, and `outputs/` and `frozen/` hashes are identical to the snapshot. Last, I'll exercise the real CLI at the default seed and count against the committed frozen manifest, with the stub provider so there is no network. I'll check the refusal path too, then re-verify the protected directories.

**Bash:**
```
.venv/bin/python -m ledgerguard.evaluation.benchmark --provider stub --output-dir ../tmp/cli_check > ../tmp/cli_stdout.txt 2>&1; echo "exit=$?"; tail -5 ../tmp/cli_stdout.txt; ls ../tmp/cli_check; .venv/bin/python -m ledgerguard.evaluation.benchmark --provider stub --output-dir ledgerguard/evaluation/outputs/x 2>&1 | tail -2; echo "refuse exit=$?"; .venv/bin/python -m ledgerguard.evaluation.benchmark --help | sed -n '1,4p;/output-dir/,+3p'; shasum -a 256 ledgerguard/evaluation/outputs/* ledgerguard/evaluation/frozen/* > ../tmp/after2.txt; diff ../tmp/before_hashes.txt ../tmp/after2.txt && echo "outputs/frozen UNCHANGED"; ls ledgerguard/evaluation/outputs | grep -c x$
```

**Result:**
```
exit=0
Artifacts written to <attempt>/work/tmp/cli_check
  benchmark.md, benchmark.json, cases.json
  unresolved_exceptions.csv (10 rows)

NOTE: the hybrid run used the offline heuristic stub, not a model. Configure a provider key (GROQ_API_KEY, GEMINI_API_KEY, NVIDIA_API_KEY or OMNIROUTE_API_KEY) and rerun to measure against a real investigator.
benchmark.json
benchmark.md
cases.json
unresolved_exceptions.csv
--output-dir <attempt>/work/repo/ledgerguard/evaluation/outputs/x is inside evaluation/outputs/, which is the committed record of the canonical run. Choose another directory.
refuse exit=0
usage: python -m ledgerguard.evaluation.benchmark [-h] [--seed SEED]
                                                  [--count COUNT]
                                                  [--split {holdout,dev,all}]
                                                  [--provider PROVIDER]
                                                  [--output-dir PATH]

LedgerGuard benchmark

  --output-dir PATH     write the artifacts to PATH instead of
                        evaluation/outputs/ (created if missing; a relative
                        PATH is resolved against the current directory). The
                        frozen holdout manifest is not written here.
outputs/frozen UNCHANGED
0
```

**Agent:** The CLI works end to end, the refusal message shows, and the protected directories are unchanged. The `refuse exit=0` line only reflects `tail`'s exit status because of the pipe, so I won't claim an exit code for that case. Last, I'll add the new option to the evaluation docs' options line and write the notes file.

**Edit:**
```
<attempt>/work/repo/docs/evaluation.md
```

**Result:**
```
The file <attempt>/work/repo/docs/evaluation.md has been updated successfully.
```

**Bash:**
```
mkdir -p ../out && cat > ../out/NOTES.md <<'EOF'
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
EOF
cd <attempt>/work/repo && .venv/bin/python -m pytest -q ledgerguard/tests 2>&1 | tail -1; shasum -a 256 ledgerguard/evaluation/outputs/* ledgerguard/evaluation/frozen/* | diff ../tmp/before_hashes.txt - && echo "outputs/frozen UNCHANGED"
```

**Result (error):**
```
Exit code 2
74 passed, 1 warning in 4.77s
diff: -: Operation not permitted
```

**Agent:** Tests pass; the hash-check command failed only because of how I piped into `diff`. I'll rerun it through a file.

**Bash:**
```
shasum -a 256 ledgerguard/evaluation/outputs/* ledgerguard/evaluation/frozen/* > ../tmp/after3.txt && diff ../tmp/before_hashes.txt ../tmp/after3.txt && echo "outputs/frozen UNCHANGED"; ls -la ../out/; git -C . status 2>/dev/null | head -1; find ledgerguard/evaluation/outputs ledgerguard/evaluation/frozen -newer ../tmp/before_hashes.txt | head
```

**Result:**
```
outputs/frozen UNCHANGED
total 8
drwxr-xr-x@ 3 user  staff    96 Nov  1 23:28 .
drwxr-xr-x@ 5 user  staff   160 Nov  1 23:25 ..
-rw-r--r--@ 1 user  staff  2641 Nov  1 23:28 NOTES.md
```

**Agent:** `python -m ledgerguard.evaluation.benchmark` now takes `--output-dir PATH`. All four artifacts go to `PATH`, and the full suite passes: 74 tests, the 67 existing plus 7 new.

- **Default behaviour:** unchanged when the option is omitted.
- **Output dir:** created with parents if missing; a relative path resolves against the current directory. The "Artifacts written to" line prints the resolved absolute path.
- **Manifest:** still read and verified from `frozen/`, never written to `PATH`. A tampered manifest still aborts with the frozen-holdout error, and no artifacts are written.
- **Content:** a default run and an `--output-dir` run with the same seed produce identical outputs, apart from the wall-time, throughput and latency fields.
- **Protected dirs:** `outputs/` and `frozen/` have the same SHA-256 hashes as before I started.

I made one choice the task did not specify: a `PATH` inside `evaluation/outputs/` is refused with an error before any work starts. Requirement 3 forbids touching that directory, so I treated the refusal as the only way to honour it.

I did not run the canonical default command against the real `outputs/`, since it would rewrite the committed artifacts. The equivalence check used temporary directories instead. The hybrid run used the offline stub, since there is no API key, so the provider-backed path was not exercised.

Changes:
- `ledgerguard/evaluation/benchmark.py`: the new option and routing of writes through the chosen directory.
- `ledgerguard/tests/test_benchmark_output_dir.py`: 7 new tests, sandboxed in temporary directories.
- `docs/evaluation.md`: the options line now mentions the flag.

Decisions and caveats are in `../out/NOTES.md`.
