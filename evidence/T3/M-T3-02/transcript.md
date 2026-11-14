# M-T3-02 transcript (PASS)

**Agent:** I'll start with the handover documentation at the repo root, then the benchmark module.

**Bash:**
```
ls -la && ls ledgerguard/evaluation ledgerguard/evaluation/outputs ledgerguard/evaluation/frozen 2>&1; for f in *.md; do echo "=== $f"; cat "$f"; done
```

**Result:**
```
total 88
drwxr-xr-x@ 10 user  staff    320 Nov  1 23:31 .
drwxr-xr-x@  5 user  staff    160 Nov  1 23:31 ..
-rw-r--r--@  1 user  staff   1992 Nov  1 23:31 .env.example
-rw-r--r--@  1 user  staff     56 Nov  1 23:31 .gitignore
drwxr-xr-x@  7 user  staff    224 Nov  1 23:31 .venv
drwxr-xr-x@  7 user  staff    224 Nov  1 23:31 docs
drwxr-xr-x@ 14 user  staff    448 Nov  1 23:31 ledgerguard
-rw-r--r--@  1 user  staff  26848 Nov  1 23:31 README.md
-rw-r--r--@  1 user  staff    466 Nov  1 23:31 requirements.txt
-rwxr-xr-x@  1 user  staff   1447 Nov  1 23:31 run_demo.sh
ledgerguard/evaluation:
__init__.py
ablation.py
baseline.py
benchmark.py
calibration.py
cost.py
drift.py
frozen
metrics.py
model_comparison.py
no_gate_ablation.py
outputs
replay.py
report.py
scale.py

ledgerguard/evaluation/frozen:
holdout_20260905_320.json

ledgerguard/evaluation/outputs:
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
model_comparison.json
model_comparison.md
no_gate_ablation.json
no_gate_ablation.md
reconciliation_report.csv
reconciliation_report.md
scale.json
scale.md
unresolved_exceptions.csv
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
   i
... [23929 more characters in transcript.jsonl]
```

**Read:**
```
<attempt>/work/repo/ledgerguard/evaluation/benchmark.py
```

**Result:**
```
1	"""One-command benchmark.
2	
3	    python -m ledgerguard.evaluation.benchmark
4	
5	Regenerates the dataset from its seed, freezes (or re-verifies) the holdout
6	manifest, runs the rules-only baseline and the full hybrid controller over the
7	same frozen holdout, and writes every artifact under evaluation/outputs/.
8	
9	Every number in every artifact comes from these two runs; nothing is typed in
10	by hand. Rerunning with the same seed reproduces the deterministic path exactly
11	-- same dispositions, same money, same unresolved rows, byte for byte, with only
12	wall-clock timing fields differing. The AI-investigated path is not reproducible
13	in that sense: the same prompt to the same model can yield a different
14	hypothesis, so a live rerun can land on a different accuracy. Runs are labelled
15	with the investigator that produced them for exactly this reason.
16	"""
17	
18	from __future__ import annotations
19	
20	import argparse
21	import csv
22	import hashlib
23	import json
24	from dataclasses import asdict
25	from pathlib import Path
26	
27	from ..ai.provider import get_provider
28	from ..evidence.safety import AUTO_RESOLVED
29	from ..ledger.money import to_rupees_str
30	from ..pipeline import RunReport, run
31	from ..synthetic.fault_injector import build_dataset, split
32	from ..synthetic.generator import Dataset
33	from .cost import estimate
34	from .metrics import Metrics, compute
35	
36	OUTPUT_DIR = Path(__file__).parent / "outputs"
37	MANIFEST_DIR = Path(__file__).parent / "frozen"
38	
39	
40	def manifest_path(seed: int, count: int) -> Path:
41	    """One frozen manifest per dataset configuration.
42	
43	    Keyed by config so that running the benchmark with a different seed or size
44	    can never silently overwrite the holdout an earlier result was scored on.
45	    """
46	    return MANIFEST_DIR / f"holdout_{seed}_{count}.json"
47	
48	
49	def batch_digest(dataset: Dataset) -> str:
50	    return hashlib.sha256(dataset.batch().model_dump_json().encode()).hexdigest()
51	
52	
53	def freeze_or_verify_holdout(holdout: Dataset, seed: int, count: int) -> dict:
54	    """Write the holdout manifest once; afterwards, verify nothing drifted."""
55	    manifest = {
56	        "seed": seed,
57	        "count": count,
58	        "generator_version": holdout.generator_version,
59	        "holdout_lifecycle_ids": sorted(lc.lifecycle_id for lc in holdout.lifecycles),
60	        "holdout_batch_sha256": batch_digest(holdout),
61	    }
62	    path = manifest_path(seed, count)
63	    if path.exists():
64	        existing = json.loads(path.read_text())
65	        if existing != manifest:
66	            raise SystemExit(
67	                "FROZEN HOLDOUT MISMATCH.\n"
68	                "The holdout for this seed was frozen earlier and the regenerated "
69	                "data no longer matches it. Scoring against a changed holdout is "
70	                "not a valid measurement. Investigate the generator change, or "
71	                "delete the manifest deliberately and say so in the write-up.\n"
72	                f"  frozen sha256:      {existing.get('holdout_batch_sha256')}\n"
73	                f"  regenerated sha256: {manifest['holdout_batch_sha256']}"
74	            )
75	        return existing
76	    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
77	    path.write_text(json.dumps(manifest, indent=2) + "\n")
78	    return manifest
79	
80	
81	def _row(label: str, baseline, hybrid, fmt=str) -> str:
82	    return f"| {label} | {fmt(baseline)} | {fmt(hybrid)} |"
83	
84	
85	def render_markdown(base: Metrics, hyb: Metrics, manifest: dict) -> str:
86	    def inr(paise: int) -> str:
87	        return f"INR {to_rupees_str(paise)}"
88	
89	    lines = [
90	        "# Benchmark: rules only vs LedgerGuard",
91	        "",
92	        f"Frozen holdout, seed `{manifest['seed']}`, generator `{manifest['generator_version']}`, "
93	        f"{len(manifest['holdout_lifecycle_ids'])} lifecycles, "
94	        f"batch SHA-256 `{manifest['hold
... [13313 more characters in transcript.jsonl]
```

**Bash:**
```
ls docs ledgerguard/tests && grep -rn "outputs\|OUTPUT\|frozen\|FROZEN" ledgerguard --include=*.py | grep -v "^ledgerguard/evaluation/benchmark.py" | head -80
```

**Result:**
```
docs:
analyses.md
architecture.md
evaluation.md
limitations.md
model_comparison.md

ledgerguard/tests:
__init__.py
rehearsal_check.py
test_dashboard_startup.py
test_evidence_download.py
test_fallback.py
test_p0_core.py
test_p1_compound.py
test_p1_extended.py
test_p2_evaluation.py
(eval):1: no matches found: --include=*.py
```

**Agent:** The grep failed because zsh doesn't expand the `--include` glob. Retrying through bash, and checking whether any test or module calls the benchmark and would touch `outputs/`.

**Bash:**
```
bash -c 'grep -rn "OUTPUT_DIR\|benchmark\|MANIFEST_DIR\|outputs" ledgerguard --include="*.py" | grep -v "^ledgerguard/evaluation/benchmark.py"'; echo ---; bash -c 'grep -rln "benchmark" docs README.md run_demo.sh'; echo ---; cat run_demo.sh; echo ---; .venv/bin/python --version; shasum -a 256 ledgerguard/evaluation/outputs/* ledgerguard/evaluation/frozen/* > ../tmp_before.sha 2>/dev/null || (mkdir -p ../tmp && shasum -a 256 ledgerguard/evaluation/outputs/* ledgerguard/evaluation/frozen/* > ../tmp/before.sha); ls ../ ../tmp 2>/dev/null
```

**Result:**
```
ledgerguard/tests/test_p1_extended.py:456:    The frozen manifest is what makes the benchmark a measurement rather than a
ledgerguard/tests/test_p1_extended.py:460:    from ledgerguard.evaluation import benchmark as bm
ledgerguard/tests/test_p1_extended.py:462:    monkeypatch.setattr(bm, "MANIFEST_DIR", tmp_path)
ledgerguard/tests/test_p1_extended.py:521:    provider that raises for any other reason is a defect, and a benchmark that
ledgerguard/tests/rehearsal_check.py:6:the adversarial pair, the benchmark comparison, and a non-empty unresolved list
ledgerguard/tests/rehearsal_check.py:124:    # 3:20 benchmark
ledgerguard/tests/rehearsal_check.py:125:    b, h = state["benchmark"]["baseline"], state["benchmark"]["hybrid"]
ledgerguard/backend/app.py:21:from ..evaluation.benchmark import batch_digest
ledgerguard/backend/app.py:265:        "benchmark": {
ledgerguard/pipeline.py:11:benchmark makes.
ledgerguard/ai/provider.py:12:benchmark and demo run with no API key present -- it is deliberately naive,
ledgerguard/ai/provider.py:14:Every result records which provider produced it; the benchmark report prints
ledgerguard/ai/provider.py:92:    """Claude-backed investigator using structured outputs."""
ledgerguard/ai/openai_compatible.py:277:        #: the benchmark reports "tokens reported by the provider" rather than
ledgerguard/evaluation/ablation.py:38:OUTPUT_DIR = Path(__file__).parent / "outputs"
ledgerguard/evaluation/ablation.py:411:    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
ledgerguard/evaluation/ablation.py:413:    (OUTPUT_DIR / "ablation.md").write_text(md)
ledgerguard/evaluation/ablation.py:414:    (OUTPUT_DIR / "ablation.json").write_text(
ledgerguard/evaluation/ablation.py:421:    print(f"Artifacts written to {OUTPUT_DIR}")
ledgerguard/evaluation/drift.py:34:OUTPUT_DIR = Path(__file__).parent / "outputs"
ledgerguard/evaluation/drift.py:163:    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
ledgerguard/evaluation/drift.py:165:    (OUTPUT_DIR / "drift.md").write_text(md)
ledgerguard/evaluation/drift.py:166:    (OUTPUT_DIR / "drift.json").write_text(
ledgerguard/evaluation/drift.py:170:    print(f"Artifacts written to {OUTPUT_DIR}")
ledgerguard/evaluation/no_gate_ablation.py:5:This makes no model calls and runs no benchmark. It reads two artifacts that
ledgerguard/evaluation/no_gate_ablation.py:28:OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
ledgerguard/evaluation/no_gate_ablation.py:29:COMPARISON = OUTPUT_DIR / "model_comparison.json"
ledgerguard/evaluation/no_gate_ablation.py:30:ABLATION = OUTPUT_DIR / "ablation.json"
ledgerguard/evaluation/no_gate_ablation.py:37:            f"and does not generate them. Run the benchmark that produces it first."
ledgerguard/evaluation/no_gate_ablation.py:95:        "calls were made and no benchmark was re-run to produce this file.",
ledgerguard/evaluation/no_gate_ablation.py:151:    (OUTPUT_DIR / "no_gate_ablation.json").write_text(json.dumps(r, indent=2) + "\n")
ledgerguard/evaluation/no_gate_ablation.py:153:    (OUTPUT_DIR / "no_gate_ablation.md").write_text(md)
ledgerguard/evaluation/no_gate_ablation.py:155:    print(f"Artifacts written to {OUTPUT_DIR}")
ledgerguard/evaluation/replay.py:5:and outputs of a run, re-run from the captured inputs alone, and assert the
ledgerguard/evaluation/replay.py:34:OUTPUT_DIR = Path(__file__).parent / "outputs"
ledgerguard/evaluation/replay.py:153:    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
ledgerguard/evaluation/replay.py:154:    path = OUTPUT_DIR / "decision_log.json"
ledgerguard/evaluation/model_comparison.py:24:from .benchmark import freeze_or_verify_holdout
ledgerguard/evaluation/model_comparison.py:29:OUTPUT_DIR = Path(__file__).parent / "outputs"
ledgerguard/evaluation/model_comparison.py:148:    # benchmark uses instead of asserting it in the prose. A regenerated or
ledgerguard/evaluation/model_comparison.py:170:    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
ledgerguard/evaluation/model_comparison.py:172:    (OUTPUT_D
... [3038 more characters in transcript.jsonl]
```

**Agent:** Nothing else calls the benchmark's `main()`, and the test at `test_p1_extended.py:456` already patches `MANIFEST_DIR`. I also noticed my snapshot landed at `../tmp_before.sha`, outside the allowed `../tmp/` area, so I'll move it. Next I need the timing fields, the provider names, and the existing test style.

**Bash:**
```
mv ../tmp_before.sha ../tmp/before.sha; cd ledgerguard; bash -c 'grep -n "wall\|throughput\|latency\|seconds\|_ms\|elapsed\|time" evaluation/metrics.py evaluation/cost.py ai/fallback.py | head -60'; echo ---; grep -n "stub\|def get_provider" -A3 ai/provider.py | head -60; echo ---; sed -n 440,540p tests/test_p1_extended.py; echo ---; sed -n 1,30p tests/test_p1_extended.py
```

**Result:**
```
evaluation/metrics.py:68:    # --- cost / throughput -------------------------------------------------
evaluation/metrics.py:69:    wall_seconds: float = 0.0
evaluation/metrics.py:70:    throughput_per_second: float = 0.0
evaluation/metrics.py:75:    latency_p50_ms: float = 0.0
evaluation/metrics.py:76:    latency_p95_ms: float = 0.0
evaluation/metrics.py:176:    m.wall_seconds = round(report.wall_seconds, 3)
evaluation/metrics.py:177:    m.throughput_per_second = (
evaluation/metrics.py:178:        round(m.total_cases / report.wall_seconds, 1) if report.wall_seconds else 0.0
evaluation/metrics.py:188:    m.latency_p50_ms = _percentile(report.investigation_latencies_ms, 50)
evaluation/metrics.py:189:    m.latency_p95_ms = _percentile(report.investigation_latencies_ms, 95)
---
15:that, so a stub run is never mistaken for a model run.
16-"""
17-
18-from __future__ import annotations
--
148:    name = "heuristic_stub"
149-
150-    def investigate(self, context: dict) -> InvestigationResult:
151-        candidates = context.get("candidate_evidence", []) or []
--
186:            return _to_result(out, source="heuristic_stub", model_name=None)
187-
188-        if exc_type == "EXCEPTION_UNEXPLAINED_SHORTFALL":
189-            out = InvestigatorOutput(
--
199:            return _to_result(out, source="heuristic_stub", model_name=None)
200-
201-        out = InvestigatorOutput(
202-            hypothesis="insufficient_evidence",
--
208:        return _to_result(out, source="heuristic_stub", model_name=None)
209-
210-
211-class UnavailableProvider:
--
313:def get_provider(kind: str | None = None) -> InvestigatorProvider:
314-    """Select an investigator provider.
315-
316-    ``kind`` (or LEDGERGUARD_PROVIDER) may be:
--
321:      stub                -- the offline stand-in
322-      none                -- a dead provider, for testing degradation
323:      auto                -- fallback across everything configured, else the stub
324-
325-    A provider that is named explicitly but cannot be configured is an error,
326-    not a silent downgrade: a run that was meant to measure a model must never
327:    quietly report stub numbers instead.
328-    """
329-    kind = (kind or os.environ.get("LEDGERGUARD_PROVIDER") or "auto").lower()
330-    if kind == "none":
--
332:    if kind == "stub":
333-        return HeuristicProvider()
334-
335-    if kind not in ("auto", "fallback"):
---
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
    """A passing evidence battery must not clo
... [3415 more characters in transcript.jsonl]
```

**Agent:** Shell cwd is now `ledgerguard/`; I'll use absolute paths from here. The timing fields are `wall_seconds`, `throughput_per_second`, `latency_p50_ms`, `latency_p95_ms` (plus per-case `latency_ms` in `cases.json`).

My plan for `main()`:
- Add `--output-dir PATH`; when given, use `Path(PATH).resolve()` for every write and skip creating `outputs/`.
- Refuse a `PATH` that is `outputs/` or inside it, since requirement 3 forbids touching `outputs/` and the option cannot satisfy both otherwise.
- Keep the default path exactly as it is.

**Edit:**
```
<attempt>/work/repo/ledgerguard/evaluation/benchmark.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/evaluation/benchmark.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

**Edit:**
```
<attempt>/work/repo/ledgerguard/evaluation/benchmark.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/evaluation/benchmark.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

**Edit:**
```
<attempt>/work/repo/ledgerguard/evaluation/benchmark.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/evaluation/benchmark.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

**Edit:**
```
<attempt>/work/repo/ledgerguard/evaluation/benchmark.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/evaluation/benchmark.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

**Agent:** The implementation is in. Next I'll add a new test module. Every test redirects `OUTPUT_DIR` and `MANIFEST_DIR` to temp directories so the real `outputs/` and `frozen/` are never touched, and it uses `--provider stub` so there are no network calls.

**Write:**
```
<attempt>/work/repo/ledgerguard/tests/test_benchmark_output_dir.py
```

**Result:**
```
File created successfully at: <attempt>/work/repo/ledgerguard/tests/test_benchmark_output_dir.py (file state is current in your context — no need to Read it back)
```

**Agent:** Now the new tests, then the full suite, from the repo root.

**Bash:**
```
cd <attempt>/work/repo && .venv/bin/python -m pytest ledgerguard/tests/test_benchmark_output_dir.py -q 2>&1 | tail -30
```

**Result:**
```
.......                                                                  [100%]
7 passed in 0.67s
```

**Agent:** All 7 pass. The run is fast, so I want to confirm the comparison isn't vacuous. I'll run the full suite, then a real CLI run into `../tmp/` with the option, and check the real `outputs/` and `frozen/` hashes against the snapshot I took earlier.

**Bash:**
```
.venv/bin/python -m pytest ledgerguard/tests -q 2>&1 | tail -5; echo "--- CLI run"; .venv/bin/python -m ledgerguard.evaluation.benchmark --provider stub --output-dir ../tmp/cli_run/sub/dir | tail -4; echo "--- refused"; .venv/bin/python -m ledgerguard.evaluation.benchmark --provider stub --output-dir ledgerguard/evaluation/outputs/x 2>&1 | tail -2; echo "exit=$?"; ls ../tmp/cli_run/sub/dir; echo "--- hash check"; shasum -a 256 ledgerguard/evaluation/outputs/* ledgerguard/evaluation/frozen/* > ../tmp/after.sha; diff ../tmp/before.sha ../tmp/after.sha && echo IDENTICAL; ls ledgerguard/evaluation/outputs | wc -l; ls -la ledgerguard/evaluation/outputs | grep -c " x$"
```

**Result:**
```
  <attempt>/work/repo/.venv/lib/python3.14/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
74 passed, 1 warning in 4.95s
--- CLI run
  benchmark.md, benchmark.json, cases.json
  unresolved_exceptions.csv (10 rows)

NOTE: the hybrid run used the offline heuristic stub, not a model. Configure a provider key (GROQ_API_KEY, GEMINI_API_KEY, NVIDIA_API_KEY or OMNIROUTE_API_KEY) and rerun to measure against a real investigator.
--- refused
                                                  [--output-dir PATH]
python -m ledgerguard.evaluation.benchmark: error: --output-dir must not be <attempt>/work/repo/ledgerguard/evaluation/outputs or inside it; use the default run to write there
exit=0
benchmark.json
benchmark.md
cases.json
unresolved_exceptions.csv
--- hash check
IDENTICAL
      20
0
```

**Agent:** Full suite: 74 passed (67 existing + 7 new). The CLI run wrote all four artifacts to a nested relative path, and the refusal case exits 2 (the `exit=0` line came from `tail`, not Python). The before/after hashes of `outputs/` and `frozen/` are identical, and the file count in `outputs/` is still 20. Last step: the notes file.

**Bash:**
```
ls -la ../out/ 2>&1; cat > ../out/NOTES.md <<'EOF'
# T3 notes: `benchmark --output-dir`

## What changed
- `ledgerguard/evaluation/benchmark.py`: new `--output-dir PATH` option. Without it,
  `out_dir = OUTPUT_DIR` and the code path is the same as before. With it, `out_dir`
  is `Path(PATH).resolve()` (relative paths resolve against the cwd) and all four
  artifacts are written there. `out_dir` is created with `parents=True`. `OUTPUT_DIR`
  is no longer created on a run that uses the option.
- `ledgerguard/tests/test_benchmark_output_dir.py`: 7 new tests. They redirect
  `OUTPUT_DIR` and `MANIFEST_DIR` to temp directories, so the real `outputs/` and
  `frozen/` are never written by the suite.

## Verification
- `pytest ledgerguard/tests -q`: 74 passed (67 existing + 7 new).
- CLI run `--provider stub --output-dir ../tmp/cli_run/sub/dir` wrote all four
  artifacts, and the printed line named the resolved path.
- SHA-256 of every file in `evaluation/outputs/` and `evaluation/frozen/` is identical
  before and after all work (snapshot in `../tmp/before.sha` and `../tmp/after.sha`).

## Choices I made (where the request was open)
1. **PATH inside `evaluation/outputs/` is refused** (exit 2, before any work). Requirement 3
   says nothing under `outputs/` may be created or modified when the option is given,
   so writing there would contradict it. The check uses resolved paths, so symlinks
   into `outputs/` are also refused.
2. **A PATH that exists as a regular file is refused** (exit 2), rather than failing
   later inside `mkdir`.
3. **The "Artifacts written to" line prints the resolved absolute path.** For an absolute
   PATH this is the same string. For a relative PATH it is the absolute location, which
   names the same directory unambiguously.
4. **Timing fields** (`wall_seconds`, `throughput_per_second`, `latency_p50_ms`,
   `latency_p95_ms`, per-case `latency_ms`, and the matching markdown rows) are the only
   fields excluded from the "same as default" comparison in the tests.
5. **The frozen manifest is still written to `frozen/` if it is missing.** That is
   existing behaviour and I left it alone. The option never writes it to `PATH`. The
   committed manifest matches the regenerated data, so no write happened.

## Not done
- `README.md` and `docs/` still describe only the default output location. I did not
  edit them, since the task did not ask for documentation changes.
- No live-provider run. The tests and the CLI check use `--provider stub`, which is the
  offline heuristic, as the ground rules require.
EOF
echo written
```

**Result:**
```
total 0
drwxr-xr-x@ 2 user  staff   64 Nov  1 23:31 .
drwxr-xr-x@ 5 user  staff  160 Nov  1 23:32 ..
written
```

**Agent:** `python -m ledgerguard.evaluation.benchmark --output-dir PATH` now works. The full suite passes (74 tests: the 67 existing ones plus 7 new), and the committed `outputs/` and `frozen/` files are byte-identical to before.

**Changes**
- `ledgerguard/evaluation/benchmark.py`: the new option sends all four artifacts to `PATH`, creating missing parents. A relative `PATH` resolves against the current directory. Without the option, the code path is unchanged.
- `ledgerguard/tests/test_benchmark_output_dir.py`: 7 new tests. They redirect `OUTPUT_DIR` and `MANIFEST_DIR` to temp directories, so the suite never writes to the real `outputs/` or `frozen/`.
- `../out/NOTES.md`: choices and verification.

**Choices I made**
- **A `PATH` inside `outputs/` is refused** with exit code 2, because requirement 3 forbids touching that directory. Symlinks into it are refused too.
- **A `PATH` that is an existing file is refused** with exit code 2.
- **The "Artifacts written to" line prints the resolved absolute path.** For an absolute `PATH` this is the same string you passed.
- **The timing-field exclusions** in the "same as default" tests are `wall_seconds`, `throughput_per_second`, `latency_p50_ms`, `latency_p95_ms`, per-case `latency_ms`, and the matching markdown rows.

**Verification**
- A CLI run with `--provider stub` into a nested relative directory wrote all four artifacts.
- SHA-256 of every file in `outputs/` and `frozen/` matches the snapshot taken before any changes.

I did not update `README.md` or `docs/`, which still describe only the default location. I also did not run a live provider; the checks use the offline stub, as the ground rules require.
