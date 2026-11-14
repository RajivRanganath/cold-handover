# M-T4-04 transcript (PASS)

**Agent:** I'll start with the handover docs at the repository root, as the ground rules require.

**Bash:**
```
ls -la && ls -la .. && find . -path ./.venv -prune -o -type f -print | grep -v __pycache__ | head -200
```

**Result:**
```
total 88
drwxr-xr-x@ 10 user  staff    320 Nov 15 00:39 .
drwxr-xr-x@  5 user  staff    160 Nov 15 00:39 ..
-rw-r--r--@  1 user  staff   1992 Nov 15 00:39 .env.example
-rw-r--r--@  1 user  staff     56 Nov 15 00:39 .gitignore
drwxr-xr-x@  7 user  staff    224 Nov 15 00:39 .venv
drwxr-xr-x@  7 user  staff    224 Nov 15 00:39 docs
drwxr-xr-x@ 14 user  staff    448 Nov 15 00:39 ledgerguard
-rw-r--r--@  1 user  staff  26848 Nov 15 00:39 README.md
-rw-r--r--@  1 user  staff    466 Nov 15 00:39 requirements.txt
-rwxr-xr-x@  1 user  staff   1447 Nov 15 00:39 run_demo.sh
total 0
drwxr-xr-x@  5 user  staff  160 Nov 15 00:39 .
drwxr-xr-x@ 10 user  staff  320 Nov 15 00:40 ..
drwxr-xr-x@  2 user  staff   64 Nov 15 00:39 out
drwxr-xr-x@ 10 user  staff  320 Nov 15 00:39 repo
drwxr-xr-x@  4 user  staff  128 Nov 15 00:40 tmp
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
cat docs/architecture.md docs/limitations.md docs/evaluation.md
```

**Result:**
```
<persisted-output>
Output too large (36.5KB). Full output saved to: <attempt>/claude-config/projects/-Users-user-Desktop-tms-work-runs-M-T4-04-work-repo/fe0f4e26-7fad-408d-bc24-8fe1a0a62628/tool-results/b0ykfb5zo.txt

Preview (first 2KB):
# Architecture

## The one-sentence version

Deterministic accounting decides what is true; the AI only proposes candidate
explanations for what the accounting could not decide; an independent gate
re-derives every proposal from records before it can change any state.

## Data flow

```
                         Batch (orders, payments, refunds, settlements, bank)
                                            |
                              +-------------+-------------+
                              |                           |
                      ShadowLedger                   deterministic
                  (expected movement)                  matcher
                              |                           |
                              +------------+--------------+
                                           |
                                  6 invariants I1..I6
                                           |
                             +-------------+--------------+
                             |                            |
                     provable outcome              genuinely ambiguous
                (MATCHED / typed exception)       (UNEXPLAINED_SHORTFALL,
                             |                     BANK_MISMATCH, ...)
                             |                            |
                             |                    AI investigator
                             |                  (structured JSON only)
                             |                            |
                             |                     Evidence Gate
                             |               (7 deterministic checks)
                             |                            |
                             |                  uniqueness pass
                             +-------------+--------------+
                                           |
                                  safety / action gate
                       AUTO_RESOLVED | RECOMMEND_REVIEW
...
</persisted-output>
```

**Bash:**
```
cat docs/architecture.md | sed -n 40,400p
```

**Result:**
```
                       HUMAN_REVIEW_REQUIRED | UNRESOLVED
```

## Components

### `ledger/money.py`
Every monetary value is an `int` count of paise. `Decimal` appears only inside
rate application, and the result is quantised back to an integer with
`ROUND_HALF_UP` at the paise boundary — the single place a derived money value
is allowed to round. `apply_rate` raises on a non-`int` input, so a float can
never enter the money path by accident.

Fee model: 2% platform fee on the captured amount, 18% GST on that fee.

### `ledger/shadow_ledger.py`
Indexes a batch and reconstructs, per captured payment:

```
expected_net = gross − fees − tax − valid_refunds + valid_adjustments
```

A refund counts as *valid* only if it is `PROCESSED` **and** carries an explicit
`payment_id` linking it to this payment. Refunds with no linkage are held
separately as `orphan_refunds` and are never silently absorbed.

`expected_for_payment(payment, extra_refunds=[...])` is the hypothetical form:
"if this refund really did belong to this payment, would the ledger balance?"
It mutates nothing. This is the mechanism the Evidence Gate uses for its
decisive check, and the reason the AI can influence *which* record is tested
without influencing *how* the test is computed.

### `ledger/invariants.py`
Six named predicates, each independently testable:

| | Invariant | Catches |
|---|---|---|
| I1 | settlement arithmetic is internally consistent | corrupted settlement rows |
| I2 | fees and tax match the independent fee schedule | fee/tax overcharge (F4) |
| I3 | observed net equals the Shadow Ledger's net | any unexplained shortfall (F3, F6) |
| I4 | settlement gross equals the captured amount | capture/settlement mismatch |
| I5 | settlement date falls inside T+2 ±1d | delayed settlement (F5) |
| I6 | one bank credit equals the settlement net | missing/duplicated bank credit (F2) |

I2 is what catches a settlement that is internally consistent but wrong — a fee
overcharge keeps I1 holding, so only an independently computed fee schedule
finds it.

### `reconciliation/matcher.py`
Runs before the model, always. Duplicate pre-pass over the whole batch, then one
case per captured payment: no settlement → `MISSING_SETTLEMENT`; more than one →
`DUPLICATE_RECORD`; otherwise run all six invariants and map the failures to a
specific exception type, most severe first.

The duplicate pre-pass compares **content, not just identifiers**. Two rows
sharing a `payment_id` are only a duplicate when every other field agrees; if
they disagree they are two contradictory versions of one payment, which the
batch cannot adjudicate, and the case is escalated rather than collapsed. The
same rule applies to settlements. Bank entries carry no identifier that survives
the trip between systems, so they are matched on content alone. The distinction
matters because `DUPLICATE_RECORD` is one of only three exception types the
safety gate closes without a human — it closes on the strength of the copies
being the same record, so "the same record" has to be something that was
actually checked.

`exceptions.py` splits the taxonomy into `DETERMINISTICALLY_PROVEN` (never
reaches the model) and `NEEDS_INVESTIGATION`. On the frozen holdout, 16 of the
31 exceptions are proven outright and never cost a model call.

### `ai/`
`InvestigatorProvider.investigate(context) -> InvestigationResult`
(`ai/provider.py`) is the entire surface the rest of the system depends on, so
the controller is model independent. `investigate_case(ledger, case, provider)`
in `ai/investigator.py` is the only caller: it builds the context, enforces the
timeout, type-checks whatever comes back, and strips any evidence id the model
did not receive as a candidate. A provider that raises, and a provider that
returns the wrong type, both become `unavailable` rather than an exception the
batch has to survive.

`ai/errors.py` carries one distinction the chain builder depends on:
`ProviderNotConfigured` means "no key, or the endpoint is 
... [6411 more characters in transcript.jsonl]
```

**Bash:**
```
cat docs/limitations.md; ls -la ../out ../tmp; cat ../out/NOTES.md 2>/dev/null | head -50
```

**Result:**
```
# Limitations

Stated plainly, because a controller that cannot describe its own boundaries is
not a controller.

## What the model results do and do not establish

The hybrid column is now a real measurement — `groq:openai/gpt-oss-120b`, 15
live investigations, 15 of 15 completed. Four separate limitations apply to it.

**Model output is not reproducible.** Five runs on the identical frozen holdout
gave 95.3%–97.7% disposition accuracy at `temperature: 0`. Any single
accuracy figure from a model run is a sample, not a measurement, and I report the
range rather than the best one. The deterministic layer *is* reproducible, and
the safety figures (0 false auto resolutions, INR 0.00 falsely closed, 6/6 F6
escalated) held across all five runs.

**Four vendors measured, not one.** `docs/model_comparison.md` runs
`gemini-2.5-flash`, `gpt-oss-20b` via Groq, `mistral-medium-3-5` via OmniRoute
and `gpt-oss-120b` via NVIDIA over the same frozen holdout, uncached, plus the
offline stub and the rules-only baseline — every provider in the automatic
chain, each on its own free tier. Not one of them falsely auto-resolved
anything: INR 0.00 in every row. That is a far better-supported claim than any
single accuracy figure. Deliberately out of scope: any paid API. Cerebras was in the
chain early on and was removed when its key began returning HTTP 402
`payment required`; it has not been in the automatic order since, and none
of the numbers published here were ever produced by it. NVIDIA was unmeasurable for most of this
build and is not any more -- see below.

**What the safety result does and does not prove.** Two separate claims live
here and I do not merge them. That the investigator *cannot* close a case is
architectural: `decide()` reaches `AUTO_RESOLVED` only from a deterministic
proven cause or a `VERIFIED` gate verdict, and the model's recommended action
can only downgrade a close, never create one. That holds for any model, and I
stress-tested it rather than assuming it — an investigator fabricating a record
id on every case closed nothing on the invented evidence, and an invalid key
degraded its cases to human review without stopping the batch. That *no
investigator falsely closed anything* is empirical, and its denominator is
small: 6 wrong-linkage cases on one 85-lifecycle holdout, 5 investigators, 30
attempts. Six adversarial cases in one fault taxonomy is evidence, not a
guarantee, and the limiting factor is the taxonomy rather than the gate.

**The offline stub ties for highest, and that is a caution about the dataset.**
It reaches 100% -- level with Gemini -- because this fixture's ambiguity is
exactly the shape its single heuristic assumes. It is well-matched, not competent. If a naive amount-matcher
tops the table, headline accuracy on this data is close to meaningless — which is
why false auto resolutions and rupee exposure are the reported headline instead.

**Cost was not measured.** All providers used here were free tiers, which is
also why the latency figures (p50 10.8s, p95 12.8s in the committed benchmark,
with rate-limit retries included) are not representative of a paid tier. No cost-per-100-records figure
is claimed.

**Free tiers only, by design — so no paid frontier model is measured here.**
Every investigator in this repository runs on a free tier: Groq, Gemini, NVIDIA
NIM, and the local OmniRoute router. No paid API key is used, and none is
required to reproduce any number in this repository. That is a deliberate
constraint, not a missing piece: the architectural claim is that the Evidence
Gate holds *regardless* of how good the investigator is, and a claim of that
shape is better supported by four ordinary free-tier models than by one
expensive one.

`AnthropicProvider` remains implemented because the provider interface is meant
to be model-independent and it is the reference implementation of that
interface. It is not in the chain and no Claude column is published. The one
data point that exists is an anecdote
... [9067 more characters in transcript.jsonl]
```

**Agent:** The docs point at the key guard: `residual_paise` in `evidence/safety.py`. Next I'll read the safety, matcher, invariant and exception code.

**Bash:**
```
cd repo && cat ledgerguard/evidence/safety.py && cat ledgerguard/reconciliation/matcher.py
```

**Result (error):**
```
Exit code 1
(eval):cd:1: no such file or directory: repo
```

**Bash:**
```
cd repo && cat ledgerguard/ledger/invariants.py ledgerguard/reconciliation/exceptions.py
```

**Result (error):**
```
Exit code 1
(eval):cd:1: no such file or directory: repo
```

**Bash:**
```
pwd; cd <attempt>/work/repo && cat ledgerguard/evidence/safety.py ledgerguard/reconciliation/matcher.py
```

**Result:**
```
<attempt>/work/repo
"""Safety and action gate.

Turns a verification outcome into one of four states. The bias is deliberate:
abstention is a correct answer, and the gate is not scored on how many
exceptions it closes.

"Auto resolved" here means the reconciliation exception is classified and
closed inside LedgerGuard. It never means money moves.
"""

from __future__ import annotations

from dataclasses import dataclass

from ..ai.schemas import InvestigationResult
from ..ledger.models import ExceptionStatus, ExceptionType
from ..ledger.money import to_rupees_str
from ..reconciliation.matcher import CaseResult
from .verifier import REJECTED, UNVERIFIED, VERIFIED, VerificationOutcome

AUTO_RESOLVED = ExceptionStatus.AUTO_RESOLVED.value
RECOMMEND_REVIEW = ExceptionStatus.RECOMMEND_REVIEW.value
HUMAN_REVIEW_REQUIRED = ExceptionStatus.HUMAN_REVIEW_REQUIRED.value
UNRESOLVED = ExceptionStatus.UNRESOLVED.value

#: Exception types the deterministic layer proves outright: the cause is known
#: exactly, so the exception can be classified and closed without a human.
_DETERMINISTIC_AUTO_CLOSE = {
    ExceptionType.DUPLICATE_RECORD: "Duplicate ingestion proven by identifier and content match; the duplicate is suppressed, not paid.",
    ExceptionType.FEE_MISMATCH: "Fee and tax reconciled against the independent fee schedule; the exact variance is quantified.",
    ExceptionType.DELAYED_SETTLEMENT: "All amounts reconcile exactly; the only discrepancy is timing against the expected settlement window.",
}

#: Proven, but the resolution is outside the system's authority to close.
_DETERMINISTIC_ESCALATE = {
    ExceptionType.MISSING_SETTLEMENT: "Captured funds have no settlement record. The money is outstanding; LedgerGuard cannot close this, it can only report it.",
}


@dataclass
class Decision:
    case_id: str
    state: str
    reason: str
    resolution: str | None = None
    missing_evidence: list[str] = None            # type: ignore[assignment]
    suggested_action: str = ""

    def __post_init__(self) -> None:
        if self.missing_evidence is None:
            self.missing_evidence = []

    @property
    def is_auto_resolved(self) -> bool:
        return self.state == AUTO_RESOLVED

    @property
    def needs_human(self) -> bool:
        return self.state in (HUMAN_REVIEW_REQUIRED, RECOMMEND_REVIEW, UNRESOLVED)


def decide(
    case: CaseResult,
    investigation: InvestigationResult | None = None,
    verification: VerificationOutcome | None = None,
) -> Decision:
    exc = case.exception
    assert exc is not None, "decide() is only called for exceptions"
    exc_type = exc.exception_type

    if (
        exc_type is ExceptionType.DELAYED_SETTLEMENT
        and exc.evidence.get("window_undecidable")
    ):
        # Amounts reconcile, but the expected settlement window could not be
        # computed at all, so the timing check never ran. Closing this as a
        # routine delay would assert a verification that did not happen.
        return Decision(
            case_id=case.case_id,
            state=HUMAN_REVIEW_REQUIRED,
            reason=(
                "Amounts reconcile exactly, but the payment has no capture "
                "timestamp, so the expected settlement window is undecidable. "
                "The timing check could not be run, and is not assumed to pass."
            ),
            missing_evidence=["payment.captured_at"],
            suggested_action=(
                "Recover the capture timestamp from the provider, then re-run "
                "reconciliation for this payment."
            ),
        )

    conflict = exc.evidence.get("content_conflict")
    if conflict:
        # Two records share an identifier and disagree on content. "Duplicate"
        # is the one classification that closes on the strength of the copies
        # being the same record -- and here they demonstrably are not. Which
        # version is real is not derivable from the batch.
    
... [22507 more characters in transcript.jsonl]
```

**Bash:**
```
cat ledgerguard/ledger/invariants.py ledgerguard/reconciliation/exceptions.py
```

**Result:**
```
"""Explicit Shadow Ledger invariants.

Each invariant is a named, independently testable predicate over a
(payment, expected settlement, observed settlement) triple. Nothing here is
heuristic and nothing here consults the AI.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta

from .models import BankEntry, CreditDebit, Payment, Settlement
from .money import gst_on_fee, platform_fee
from .shadow_ledger import BANK_CREDIT_TOLERANCE_DAYS, ExpectedSettlement


@dataclass(frozen=True)
class InvariantResult:
    name: str
    holds: bool
    expected: int | str | None
    observed: int | str | None
    detail: str

    @property
    def difference(self) -> int | None:
        if isinstance(self.expected, int) and isinstance(self.observed, int):
            return self.expected - self.observed
        return None

    def as_dict(self) -> dict:
        return {
            "name": self.name,
            "holds": self.holds,
            "expected": self.expected,
            "observed": self.observed,
            "difference": self.difference,
            "detail": self.detail,
        }


# I1 -------------------------------------------------------------------------
def settlement_arithmetic_consistent(s: Settlement) -> InvariantResult:
    """gross - fees - tax - refund_adjustments + other_adjustments == net."""
    derived = (
        s.gross_amount - s.fees - s.tax - s.refund_adjustments + s.other_adjustments
    )
    return InvariantResult(
        name="I1_settlement_arithmetic_consistent",
        holds=derived == s.net_amount,
        expected=derived,
        observed=s.net_amount,
        detail=(
            f"{s.settlement_id}: gross {s.gross_amount} - fees {s.fees} - tax {s.tax} "
            f"- refunds {s.refund_adjustments} + adj {s.other_adjustments} "
            f"= {derived}, reported net {s.net_amount}"
        ),
    )


# I2 -------------------------------------------------------------------------
def fees_and_tax_match_schedule(s: Settlement) -> InvariantResult:
    """Reported fees and tax equal the independently computed fee schedule."""
    exp_fee = platform_fee(s.gross_amount)
    exp_tax = gst_on_fee(exp_fee)
    holds = s.fees == exp_fee and s.tax == exp_tax
    return InvariantResult(
        name="I2_fees_and_tax_match_schedule",
        holds=holds,
        expected=exp_fee + exp_tax,
        observed=s.fees + s.tax,
        detail=(
            f"{s.settlement_id}: expected fee {exp_fee} + tax {exp_tax}, "
            f"observed fee {s.fees} + tax {s.tax}"
        ),
    )


# I3 -------------------------------------------------------------------------
def net_matches_shadow_ledger(
    expected: ExpectedSettlement, s: Settlement
) -> InvariantResult:
    """Observed settlement net equals the Shadow Ledger's reconstructed net."""
    return InvariantResult(
        name="I3_net_matches_shadow_ledger",
        holds=expected.net_amount == s.net_amount,
        expected=expected.net_amount,
        observed=s.net_amount,
        detail=(
            f"{s.settlement_id}: shadow ledger expects net {expected.net_amount} "
            f"for payment {expected.payment_id}, provider reported {s.net_amount}"
        ),
    )


# I4 -------------------------------------------------------------------------
def gross_matches_capture(expected: ExpectedSettlement, s: Settlement) -> InvariantResult:
    """Settlement gross equals the captured payment amount."""
    return InvariantResult(
        name="I4_gross_matches_capture",
        holds=expected.gross_amount == s.gross_amount,
        expected=expected.gross_amount,
        observed=s.gross_amount,
        detail=(
            f"{s.settlement_id}: captured {expected.gross_amount}, "
            f"settlement gross {s.gross_amount}"
        ),
    )


# I5 -------------------------------------------------------------------------
def settlement_within_window(
    expected: ExpectedSettlement, s: Settlement

... [6421 more characters in transcript.jsonl]
```

**Agent:** I think I see the cause. `reconcile_payment` computes `residual_paise` from the settlement's own gross and components, not from its reported net, so an arithmetic shortfall in net leaves the residual at zero. Before deciding, I'll check where else this logic appears and what the tests and generators depend on.

**Bash:**
```
grep -rn "residual\|FEE_MISMATCH\|I1_" --include=*.py --include=*.html . | grep -v .venv; echo ---; grep -n "def \|outputs\|frozen" ledgerguard/evaluation/benchmark.py | head -80
```

**Result:**
```
(eval):1: no matches found: --include=*.py
---
7:same frozen holdout, and writes every artifact under evaluation/outputs/.
36:OUTPUT_DIR = Path(__file__).parent / "outputs"
37:MANIFEST_DIR = Path(__file__).parent / "frozen"
40:def manifest_path(seed: int, count: int) -> Path:
41:    """One frozen manifest per dataset configuration.
49:def batch_digest(dataset: Dataset) -> str:
53:def freeze_or_verify_holdout(holdout: Dataset, seed: int, count: int) -> dict:
68:                "The holdout for this seed was frozen earlier and the regenerated "
72:                f"  frozen sha256:      {existing.get('holdout_batch_sha256')}\n"
81:def _row(label: str, baseline, hybrid, fmt=str) -> str:
85:def render_markdown(base: Metrics, hyb: Metrics, manifest: dict) -> str:
86:    def inr(paise: int) -> str:
149:def write_unresolved_csv(report: RunReport, dataset: Dataset, path: Path) -> int:
195:def export_cases(report: RunReport, dataset: Dataset, path: Path) -> None:
238:def main(argv: list[str] | None = None) -> int:
244:        help="which slice to score (default: the frozen holdout)",
```

**Bash:**
```
grep -rn "residual\|FEE_MISMATCH\|I1_" ledgerguard docs README.md | grep -v "\.venv" ; echo ---; sed -n 230,330p ledgerguard/evaluation/benchmark.py
```

**Result:**
```
ledgerguard/reconciliation/matcher.py:143:    ExceptionType.FEE_MISMATCH: {
ledgerguard/reconciliation/matcher.py:144:        "I1_settlement_arithmetic_consistent",
ledgerguard/reconciliation/matcher.py:169:        return ExceptionType.FEE_MISMATCH, failing["I2_fees_and_tax_match_schedule"]
ledgerguard/reconciliation/matcher.py:170:    if "I1_settlement_arithmetic_consistent" in failing:
ledgerguard/reconciliation/matcher.py:171:        return ExceptionType.FEE_MISMATCH, failing["I1_settlement_arithmetic_consistent"]
ledgerguard/reconciliation/matcher.py:352:    elif exc_type is ExceptionType.FEE_MISMATCH:
ledgerguard/reconciliation/matcher.py:367:        evidence["residual_paise"] = expected.net_amount - corrected_net
ledgerguard/evidence/safety.py:30:    ExceptionType.FEE_MISMATCH: "Fee and tax reconciled against the independent fee schedule; the exact variance is quantified.",
ledgerguard/evidence/safety.py:114:    residual = exc.evidence.get("residual_paise") or 0
ledgerguard/evidence/safety.py:118:        if residual:
ledgerguard/evidence/safety.py:128:                    f"{to_rupees_str(abs(residual))} INR unattributed, with no record "
ledgerguard/evidence/safety.py:131:                missing_evidence=["explanation for the residual deduction"],
ledgerguard/reconciliation/exceptions.py:22:    ExceptionType.FEE_MISMATCH,
ledgerguard/reconciliation/exceptions.py:54:    ExceptionType.FEE_MISMATCH: Risk.MEDIUM,
ledgerguard/ledger/models.py:110:    FEE_MISMATCH = "EXCEPTION_FEE_MISMATCH"
ledgerguard/ledger/invariants.py:50:        name="I1_settlement_arithmetic_consistent",
ledgerguard/ledger/invariants.py:181:    "I1_settlement_arithmetic_consistent",
ledgerguard/tests/test_p1_compound.py:6:    money; any unattributed residual blocks closure, while a second finding that
ledgerguard/tests/test_p1_compound.py:46:def test_an_unattributed_residual_blocks_closure_on_the_proven_cause():
ledgerguard/tests/test_p1_compound.py:51:    residual = outcome.case.exception.evidence["residual_paise"]
ledgerguard/tests/test_p1_compound.py:52:    assert residual == to_paise("650.00"), residual
ledgerguard/tests/test_p1_compound.py:57:    # C5 is the same shape with the residual explained by a refund that belongs
ledgerguard/tests/test_p1_compound.py:60:    assert c5.case.exception.evidence["residual_paise"] == to_paise("900.00")
ledgerguard/tests/test_p1_compound.py:70:    assert not outcome.case.exception.evidence.get("residual_paise")
ledgerguard/tests/test_p0_core.py:205:        FaultClass.F4_FEE_TAX_MISMATCH: "EXCEPTION_FEE_MISMATCH",
ledgerguard/tests/test_p2_evaluation.py:119:    assert shifted.dominant_exception == "EXCEPTION_FEE_MISMATCH"
ledgerguard/synthetic/fault_injector.py:123:        expected_exception=ExceptionType.FEE_MISMATCH.value,
ledgerguard/evaluation/outputs/reconciliation_report.csv:12:pay_0029AD38,ord_0029B12F,pay_0029AD38,AUTO_RESOLVED,EXCEPTION_FEE_MISMATCH,89164.00,87059.73,86429.61,-630.12,setl_0029167F,2026-06-27,I2_fees_and_tax_match_schedule; I3_net_matches_shadow_ledger,,,,,,Fee and tax reconciled against the independent fee schedule; the exact variance is quantified.,No action; classified and closed by the deterministic engine.
ledgerguard/evaluation/outputs/reconciliation_report.csv:16:pay_0037DAA0,ord_0037B003,pay_0037DAA0,AUTO_RESOLVED,EXCEPTION_FEE_MISMATCH,10655.00,10403.54,10256.04,-147.50,setl_00373C9A,2026-06-23,I2_fees_and_tax_match_schedule; I3_net_matches_shadow_ledger,,,,,,Fee and tax reconciled against the independent fee schedule; the exact variance is quantified.,No action; classified and closed by the deterministic engine.
ledgerguard/evaluation/outputs/reconciliation_report.csv:36:pay_0120EB60,ord_01207C31,pay_0120EB60,AUTO_RESOLVED,EXCEPTION_FEE_MISMATCH,68636.00,67016.19,66348.31,-667.88,setl_0120DD92,2026-06-24,I2_fees_and_tax_match_schedule; I3_net_matches_shadow_ledger,,,,,,Fee and tax reconciled against the independent fee schedule; the exact variance is quantified.,No action; classi
... [15364 more characters in transcript.jsonl]
```

**Agent:** The compound-fault tests and `docs/evaluation.md` cover this residual logic directly, so I'll read those next, along with the compound generator.

**Bash:**
```
sed -n 170,215p docs/evaluation.md; echo ----; cat ledgerguard/tests/test_p1_compound.py; echo ----; cat ledgerguard/synthetic/compound.py
```

**Result:**
```
| C2 | F4 + F6 — fee overcharge + unexplained deduction | `HUMAN_REVIEW_REQUIRED` | `HUMAN_REVIEW_REQUIRED` | match |
| C3 | F2 + F5 — duplicate bank credit + delayed settlement | `AUTO_RESOLVED` | `AUTO_RESOLVED` | match |
| C4 | F1 + F3 — missing settlement + orphan refund, same customer | `HUMAN_REVIEW_REQUIRED` | `HUMAN_REVIEW_REQUIRED` | match |
| C5 | F4 + F6 — fee overcharge + wrong-linkage deduction | `HUMAN_REVIEW_REQUIRED` | `HUMAN_REVIEW_REQUIRED` | match |

Recorded from a run with the offline heuristic stub, and re-confirmed against a
live `fallback(groq->gemini->nvidia->omniroute)` run: 5 of 5 on both.

What the interesting ones actually exercise:

- **C1** closes on the refund and still reports the delay, rather than letting
  the resolved shortfall silently absorb a second finding.
- **C2 and C5** are the ones that matter. Both have a *deterministically proven*
  fee variance sitting on top of an unexplained deduction. Correcting the proven
  part leaves INR 650.00 (C2) and INR 900.00 (C5) unattributed, and the case is
  escalated on the residual. A proven cause does not license closing the case.
- **C4** refuses to net a same-customer orphan refund against a settlement that
  never arrived.

### What this does and does not demonstrate

It demonstrates that one proven fault does not license closing an unproven one —
the residual check is doing real work, and C2 and C5 would close incorrectly
without it.

It does **not** demonstrate that the fault taxonomy is deep. Three honest caveats:

1. **Five hand-built cases, designed by the same person who wrote the resolution
   rules.** 5 of 5 measures the rules against their author's intent, not against
   reality. A case I did not think of is not represented here.
2. **Four of the five never reach the investigator at all.** Layering a second
   fault usually surfaces a deterministic exception type first (`FEE_MISMATCH`,
   `DUPLICATE_RECORD`, `MISSING_SETTLEMENT`), which the engine proves without a
   model call. Only C1 was AI-investigated. So this set says much more about the
   deterministic layer than about the AI path.
3. **Only pairs.** No case layers three or more faults, and no case combines two
   faults that both require investigation — the shape most likely to break the
   residual logic, and the obvious next thing to build.

## Artifacts

| File | Contents |
|---|---|
| `outputs/benchmark.md` | the comparison table |
| `outputs/benchmark.json` | every metric for both systems, plus dataset provenance |
| `outputs/cases.json` | full per-case detail: invariants, investigation, verification, decision |
----
"""Compound failure cases.

Two faults in one lifecycle. These exist to pin one rule:

    a proven cause licenses closing a case only if it accounts for all of the
    money; any unattributed residual blocks closure, while a second finding that
    is itself benign does not.

Both halves matter. Without the first, the controller closes on the fault it
recognised and leaves real money unexplained. Without the second, it escalates
every case that has more than one finding and abstention stops meaning anything.
"""

from __future__ import annotations

from ledgerguard.ai.provider import HeuristicProvider
from ledgerguard.evidence.safety import AUTO_RESOLVED, HUMAN_REVIEW_REQUIRED
from ledgerguard.ledger.money import to_paise
from ledgerguard.pipeline import run
from ledgerguard.synthetic.compound import build_compound_batch


def _run():
    batch, cases = build_compound_batch()
    report = run(batch, use_ai=True, provider=HeuristicProvider())
    return {o.case.payment_id: o for o in report.outcomes}, {c.case_id: c for c in cases}


def test_every_compound_case_reaches_its_designed_disposition():
    outcomes, cases = _run()
    assert len(cases) == 5, "three to five compound cases were planned"

    wrong = []
    for case in cases.values():
        got = outcomes[case.payment_id].state
        if got != case.expected_disposition:
            wrong.append(
... [10198 more characters in transcript.jsonl]
```

**Agent:** Two findings so far:

- The existing compound fixtures (C2, C5) always keep the settlement's net consistent with its components, so no test exercises a settlement whose reported net is short of its own components. That's why the gap went unnoticed.
- `residual_paise` is computed from the settlement's gross and components, never from its reported `net_amount`. A shortfall in the net therefore leaves the residual at zero.

Before changing anything I'll snapshot the original repo and the artifact hashes, then run the existing tests for a baseline.

**Bash:**
```
cd <attempt>/work && mkdir -p ../tmp/orig && cp -R repo/ledgerguard ../tmp/orig/ && find repo/ledgerguard/evaluation/outputs repo/ledgerguard/evaluation/frozen -type f -exec shasum -a 256 {} \; | sort > ../tmp/artifacts_before.sha && cat ../tmp/artifacts_before.sha | wc -l && cd repo && (time .venv/bin/python -m pytest ledgerguard/tests -q 2>&1 | tail -15)
```

**Result (error):**
```
Exit code 1
mkdir: ../tmp: Operation not permitted
```

**Bash:**
```
cd <attempt>/work && ls && mkdir -p tmp/orig && cp -R repo/ledgerguard tmp/orig/ && find repo/ledgerguard/evaluation/outputs repo/ledgerguard/evaluation/frozen -type f -exec shasum -a 256 {} \; | sort > tmp/artifacts_before.sha && wc -l < tmp/artifacts_before.sha && cd repo && (time .venv/bin/python -m pytest ledgerguard/tests -q 2>&1 | tail -15)
```

**Result:**
```
out
repo
tmp
      21
...................................................................      [100%]
=============================== warnings summary ===============================
.venv/lib/python3.14/site-packages/fastapi/testclient.py:1
  <attempt>/work/repo/.venv/lib/python3.14/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
67 passed, 1 warning in 8.62s
.venv/bin/python -m pytest ledgerguard/tests -q 2>&1  5.47s user 0.50s system 57% cpu 10.407 total
tail -15  0.00s user 0.01s system 0% cpu 10.407 total
```

**Agent:** Baseline is 67 passing tests. Next I'll reproduce the reported case: fees and tax on schedule, reported net ₹250 short of its own components.

**Bash:**
```
mkdir -p <attempt>/work/tmp/scripts && cat > <attempt>/work/tmp/scripts/repro.py <<'EOF'
"""Reproduce: fees and tax per schedule, reported net INR 250 short of its own components."""
import sys
from datetime import datetime, timedelta
from ledgerguard.ledger.models import Batch, Order, Payment, Settlement, BankEntry, CreditDebit
from ledgerguard.ledger.money import gst_on_fee, platform_fee, to_paise
from ledgerguard.pipeline import run
from ledgerguard.ai.provider import HeuristicProvider

T0 = datetime(2026, 7, 15, 10, 0, 0)

def build(short_by: int):
    amount = to_paise("10000.00")
    fee = platform_fee(amount); tax = gst_on_fee(fee)
    captured = T0 + timedelta(minutes=5)
    order = Order(order_id="ord_R1", merchant_id="mch_R", amount=amount, created_at=T0, customer_reference="CUST-R1")
    payment = Payment(payment_id="pay_R1", order_id="ord_R1", amount=amount, captured_at=captured,
                      fee=fee, tax=tax, reference="PAY/ord_R1")
    net = amount - fee - tax - short_by       # reported net is short; components unchanged
    settled = captured + timedelta(days=2)
    s = Settlement(settlement_id="setl_R1", merchant_id="mch_R", payment_ids=["pay_R1"],
                   gross_amount=amount, fees=fee, tax=tax, refund_adjustments=0, other_adjustments=0,
                   net_amount=net, settlement_date=settled, reference="STL/setl_R1")
    bank = [BankEntry(bank_entry_id="bnk_R1", amount=net, credit_or_debit=CreditDebit.CREDIT,
                      date=settled, reference=s.reference)]
    return Batch(orders=[order], payments=[payment], refunds=[], settlements=[s], bank_entries=bank)

for short in (0, to_paise("250.00")):
    rep = run(build(short), use_ai=True, provider=HeuristicProvider())
    for o in rep.outcomes:
        ev = o.case.exception.evidence if o.case.exception else {}
        print(f"short={short}: state={o.state} type={o.case.status} residual={ev.get('residual_paise')} "
              f"secondary={ev.get('secondary_findings')}")
        print("   reason:", o.decision.reason)
EOF
cd <attempt>/work/repo && .venv/bin/python ../tmp/scripts/repro.py
```

**Result (error):**
```
Exit code 1
Traceback (most recent call last):
  File "<attempt>/work/repo/../tmp/scripts/repro.py", line 4, in <module>
    from ledgerguard.ledger.models import Batch, Order, Payment, Settlement, BankEntry, CreditDebit
ModuleNotFoundError: No module named 'ledgerguard'
```

**Bash:**
```
PYTHONPATH=. .venv/bin/python ../tmp/scripts/repro.py
```

**Result (error):**
```
Exit code 1
short=0: state=MATCHED type=MATCHED residual=None secondary=None
Traceback (most recent call last):
  File "<attempt>/work/repo/../tmp/scripts/repro.py", line 33, in <module>
    print("   reason:", o.decision.reason)
                        ^^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'reason'
```

**Bash:**
```
sed -i 's/        print("   reason:", o.decision.reason)/        print("   reason:", o.decision.reason if o.decision else None)/' ../tmp/scripts/repro.py && PYTHONPATH=. .venv/bin/python ../tmp/scripts/repro.py
```

**Result (error):**
```
Exit code 1
sed: 1: "../tmp/scripts/repro.py": invalid command code .
```

**Edit:**
```
<attempt>/work/tmp/scripts/repro.py
```

**Result:**
```
The file <attempt>/work/tmp/scripts/repro.py has been updated successfully.
```

**Bash:**
```
PYTHONPATH=. .venv/bin/python ../tmp/scripts/repro.py
```

**Result:**
```
short=0: state=MATCHED type=MATCHED residual=None secondary=None
   reason: None
short=25000: state=AUTO_RESOLVED type=EXCEPTION_FEE_MISMATCH residual=0 secondary=[]
   reason: Fee and tax reconciled against the independent fee schedule; the exact variance is quantified.
```

**Agent:** Reproduced: with the reported ₹250 shortfall, the case closes as `AUTO_RESOLVED` with `residual=0`. (The `25000` in the script is paise, so it is ₹250.)

The root cause is in `matcher.py` (`residual_paise`). The fix is to also measure the residual from the settlement's reported net. When the net and components agree, the two measures are algebraically identical, so existing closures should not change. I'll make that change in the matcher now.

**Edit:**
```
<attempt>/work/repo/ledgerguard/reconciliation/matcher.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/reconciliation/matcher.py has been updated successfully.
```

**Agent:** Next, the gate: it must block closure if either residual is nonzero, and the escalation reason must not claim a fee variance that doesn't exist.

**Edit:**
```
<attempt>/work/repo/ledgerguard/evidence/safety.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/evidence/safety.py has been updated successfully.
```

**Agent:** Now I'll rerun the reproduction and the full suite.

**Bash:**
```
PYTHONPATH=. .venv/bin/python ../tmp/scripts/repro.py && .venv/bin/python -m pytest ledgerguard/tests -q 2>&1 | tail -3
```

**Result:**
```
short=0: state=MATCHED type=MATCHED residual=None secondary=None
   reason: None
short=25000: state=HUMAN_REVIEW_REQUIRED type=EXCEPTION_FEE_MISMATCH residual=0 secondary=[]
   reason: Fee and tax match the independent fee schedule, so the fee variance is zero. Correcting it still leaves 250.00 INR unattributed, with no record explaining it. A second, unproven discrepancy is present.

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
67 passed, 1 warning in 6.33s
```

**Agent:** The reported case now escalates to `HUMAN_REVIEW_REQUIRED`, and the reason names the ₹250 unattributed. All 67 tests still pass.

Next I'll check requirement 2 directly. I'll run the deterministic pipeline on the frozen holdout with the original and fixed code and diff every case's disposition, without writing any artifacts. I'll use the offline heuristic provider so the AI path is deterministic too.

**Bash:**
```
sed -n 1,35p ledgerguard/evaluation/benchmark.py | grep -n "import"; cat > ../tmp/scripts/holdout_dump.py <<'EOF'
"""Dump per-case dispositions for the frozen holdout (read-only; writes nothing in the repo)."""
import json, sys
from ledgerguard.synthetic.fault_injector import build_dataset
from ledgerguard.evaluation.benchmark import split
from ledgerguard.pipeline import run
from ledgerguard.ai.provider import HeuristicProvider

full = build_dataset(seed=20260905, count=320)
dev, holdout = split(full)
lbp = holdout.lifecycle_by_payment()
batch = holdout.batch()
rows = {}
for use_ai in (False, True):
    rep = run(batch, use_ai=use_ai, provider=HeuristicProvider() if use_ai else None,
              lifecycle_by_payment=lbp)
    for o in rep.outcomes:
        exc = o.case.exception
        rows.setdefault(o.case.payment_id, {})["ai" if use_ai else "rules"] = {
            "state": o.state,
            "type": exc.exception_type.value if exc else None,
            "exposure": o.exposure_paise,
        }
json.dump(rows, open(sys.argv[1], "w"), indent=1, sort_keys=True, default=str)
print("cases:", len(rows))
EOF
cd <attempt>/work/repo && PYTHONPATH=../tmp/orig .venv/bin/python ../tmp/scripts/holdout_dump.py ../tmp/orig_holdout.json && PYTHONPATH=. .venv/bin/python ../tmp/scripts/holdout_dump.py ../tmp/new_holdout.json && cmp ../tmp/orig_holdout.json ../tmp/new_holdout.json && echo IDENTICAL
```

**Result:**
```
18:from __future__ import annotations
20:import argparse
21:import csv
22:import hashlib
23:import json
24:from dataclasses import asdict
25:from pathlib import Path
27:from ..ai.provider import get_provider
28:from ..evidence.safety import AUTO_RESOLVED
29:from ..ledger.money import to_rupees_str
30:from ..pipeline import RunReport, run
31:from ..synthetic.fault_injector import build_dataset, split
32:from ..synthetic.generator import Dataset
33:from .cost import estimate
34:from .metrics import Metrics, compute
cases: 85
cases: 85
IDENTICAL
```

**Agent:** The holdout dispositions are identical. I'll confirm the "orig" run really imported the original code, and extend the comparison to all 320 lifecycles, since the fixed branch could in principle be hit by dev-split cases.

**Bash:**
```
PYTHONPATH=../tmp/orig .venv/bin/python -c "import ledgerguard,sys;print(ledgerguard.__file__)" && sed -e 's/^dev, holdout = split(full)/dev, holdout = split(full); holdout = full/' ../tmp/scripts/holdout_dump.py > ../tmp/scripts/all_dump.py && PYTHONPATH=../tmp/orig .venv/bin/python ../tmp/scripts/all_dump.py ../tmp/orig_all.json && PYTHONPATH=. .venv/bin/python ../tmp/scripts/all_dump.py ../tmp/new_all.json && cmp ../tmp/orig_all.json ../tmp/new_all.json && echo IDENTICAL_ALL_320
```

**Result:**
```
<attempt>/work/repo/ledgerguard/__init__.py
cases: 320
cases: 320
IDENTICAL_ALL_320
```

**Agent:** The import check was inconclusive: `python -c` puts the current directory first on `sys.path`. The `repro.py` script is a better probe, since the original code should show the bug.

**Bash:**
```
PYTHONPATH=../tmp/orig .venv/bin/python ../tmp/scripts/repro.py 2>&1 | grep short=25000 -A1
```

**Result:**
```
short=25000: state=AUTO_RESOLVED type=EXCEPTION_FEE_MISMATCH residual=0 secondary=[]
   reason: Fee and tax reconciled against the independent fee schedule; the exact variance is quantified.
```

**Agent:** The original code reproduces the bug, so the comparison is valid. The fix leaves all 320 lifecycle dispositions, including the AI-path outcomes, byte-identical.

Now the tests. I'll add a new test file covering the reported case, the component-only disagreement, a proven fee overcharge that must still close, and a guard that a consistent settlement's two residual views agree across the whole generated dataset.

**Write:**
```
<attempt>/work/repo/ledgerguard/tests/test_short_settlement.py
```

**Result:**
```
File created successfully at: <attempt>/work/repo/ledgerguard/tests/test_short_settlement.py (file state is current in your context — no need to Read it back)
```

**Agent:** Reviewing the file before running it, I see two mistakes. The component-only test has the wrong shape (a refund with a matching net keeps I1 true, so it isn't a fee mismatch at all), and its assertion is a loose `or`. There is also an unused import. I'll fix both.

**Edit:**
```
<attempt>/work/repo/ledgerguard/tests/test_short_settlement.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/tests/test_short_settlement.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

**Edit:**
```
<attempt>/work/repo/ledgerguard/tests/test_short_settlement.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/tests/test_short_settlement.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

**Edit:**
```
<attempt>/work/repo/ledgerguard/tests/test_short_settlement.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/tests/test_short_settlement.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

**Edit:**
```
<attempt>/work/repo/ledgerguard/tests/test_short_settlement.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/tests/test_short_settlement.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

**Agent:** Now I'll run the new tests against the fixed code, and also against the original code. The bug-specific tests should fail on the original, which shows they actually detect the defect.

**Bash:**
```
.venv/bin/python -m pytest ledgerguard/tests/test_short_settlement.py -q 2>&1 | tail -30; echo ==== ORIGINAL; cp ledgerguard/tests/test_short_settlement.py ../tmp/orig/ledgerguard/tests/ && cd ../tmp/orig && PYTHONPATH=. <attempt>/work/repo/.venv/bin/python -m pytest ledgerguard/tests/test_short_settlement.py -q -p no:cacheprovider 2>&1 | grep -E "passed|failed|FAILED"
```

**Result:**
```
......                                                                   [100%]
6 passed in 0.63s
(eval):1: === not found
```

**Bash:**
```
cd <attempt>/work/tmp/orig && PYTHONPATH=. <attempt>/work/repo/.venv/bin/python -m pytest ledgerguard/tests/test_short_settlement.py -q -p no:cacheprovider 2>&1 | grep -E "passed|failed|FAILED"
```

**Result:**
```
(Bash completed with no output)
```

**Bash:**
```
cd <attempt>/work/tmp/orig && PYTHONPATH=. <attempt>/work/repo/.venv/bin/python -m pytest ledgerguard/tests/test_short_settlement.py -q -p no:cacheprovider 2>&1 | tail -40
```

**Result:**
```
ERROR: file or directory not found: ledgerguard/tests/test_short_settlement.py


no tests ran in 0.00s
Shell cwd was reset to <attempt>/work/repo
```

**Agent:** The earlier `cp` didn't run, so the file wasn't in the original snapshot. I'll copy it again and rerun.

**Bash:**
```
cd <attempt>/work && cp repo/ledgerguard/tests/test_short_settlement.py tmp/orig/ledgerguard/tests/ && cd tmp/orig && PYTHONPATH=. <attempt>/work/repo/.venv/bin/python -m pytest ledgerguard/tests/test_short_settlement.py -q -p no:cacheprovider 2>&1 | grep -E "passed|failed|FAILED|Error" | head -20
```

**Result:**
```
E       AssertionError: assert 'AUTO_RESOLVED' == 'HUMAN_REVIEW_REQUIRED'
ledgerguard/tests/test_short_settlement.py:93: AssertionError
E       KeyError: 'fee_variance_paise'
ledgerguard/tests/test_short_settlement.py:107: KeyError
E       KeyError: 'net_residual_paise'
ledgerguard/tests/test_short_settlement.py:117: KeyError
E       AssertionError: assert 'AUTO_RESOLVED' == 'HUMAN_REVIEW_REQUIRED'
ledgerguard/tests/test_short_settlement.py:125: AssertionError
E       KeyError: 'net_residual_paise'
ledgerguard/tests/test_short_settlement.py:138: KeyError
E           KeyError: 'net_residual_paise'
ledgerguard/tests/test_short_settlement.py:158: KeyError
FAILED ledgerguard/tests/test_short_settlement.py::test_reported_case_fee_on_schedule_net_short_is_not_auto_closed
FAILED ledgerguard/tests/test_short_settlement.py::test_the_missing_money_is_measured_from_the_reported_net
FAILED ledgerguard/tests/test_short_settlement.py::test_a_fee_overcharge_with_a_consistent_net_still_closes
FAILED ledgerguard/tests/test_short_settlement.py::test_a_fee_overcharge_plus_a_separate_net_shortfall_is_blocked
FAILED ledgerguard/tests/test_short_settlement.py::test_components_disagreeing_with_the_shadow_ledger_still_block_closure
FAILED ledgerguard/tests/test_short_settlement.py::test_a_consistent_settlement_has_identical_residual_views_across_the_dataset
6 failed in 0.63s
Shell cwd was reset to <attempt>/work/repo
```

**Agent:** On the original code, the bug test fails with `AUTO_RESOLVED`, which is the defect. The other failures there are `KeyError`s on the new evidence keys, as expected. Now the full suite, the artifact hash check, and a look at stray cache directories.

**Bash:**
```
.venv/bin/python -m pytest ledgerguard/tests -q -p no:cacheprovider 2>&1 | tail -2; find ledgerguard/evaluation/outputs ledgerguard/evaluation/frozen -type f -exec shasum -a 256 {} \; | sort > ../tmp/artifacts_after.sha; diff ../tmp/artifacts_before.sha ../tmp/artifacts_after.sha && echo ARTIFACTS_UNCHANGED; cat .gitignore; ls -a ../tmp/orig/ledgerguard | head; find . -name __pycache__ -maxdepth 3 -not -path "./.venv/*" | head; ls -a | grep pytest
```

**Result:**
```
-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
73 passed, 1 warning in 8.10s
1,21c1,21
< 06f71351dd21bdcdb30705986832111987fe71ff6d6787ed2a198c88de50a53f  repo/ledgerguard/evaluation/frozen/holdout_20260905_320.json
< 1fbca2999ea5f5b76d810ac2955beb5fca7bc5af165320a752be60dbe4b96100  repo/ledgerguard/evaluation/outputs/model_comparison.json
< 227f79916be1cbe13addb7096e2f0f453660e2dc4ef83e4081ff8bcbee2ef9cf  repo/ledgerguard/evaluation/outputs/scale.md
< 249e3bce69daeb83386d9575e66bf4177d4db885a8864ab6b32d80b5717d8536  repo/ledgerguard/evaluation/outputs/benchmark.json
< 3699ea28a60eed7b419b027283ae1a9a3875eeb7c43e674adddfc0d195aa50c1  repo/ledgerguard/evaluation/outputs/evidence_ledger.csv
< 530301222288c5c487d56e9029f570bd01720e1fdbd306c90b9f71c71488cd4b  repo/ledgerguard/evaluation/outputs/scale.json
< 7a9f6520bbeb849b4e6f1f15a78f39a608583c6776c7c310457ed053a82dd41c  repo/ledgerguard/evaluation/outputs/reconciliation_report.md
< 7ffa151674c19541ac0b4cf9a8618b4c5a8eef664afd9ab81321961848cecd03  repo/ledgerguard/evaluation/outputs/ablation.json
< 8dc1212f1c93e7c1bf34d92923c1d31f15b7096a0b39e4c2afa4e167f4eda9d4  repo/ledgerguard/evaluation/outputs/calibration.json
< a5552fcb48631411cb08fae4e34987295cca132334d6c31d86601f73e538455b  repo/ledgerguard/evaluation/outputs/cases.json
< aa667ebea4ccd41fa0bdff898182200d3bf282ef0b888cabd7b5a215d82edd22  repo/ledgerguard/evaluation/outputs/benchmark.md
< ac427b5c78460109ba2fb3914c2d04310e80089ea245dcf44f426bc2da5562a7  repo/ledgerguard/evaluation/outputs/drift.json
< af74f00254d9a8cee944bccdf9fd8940c2a318c0bfd5c6965dbfc5a221e00711  repo/ledgerguard/evaluation/outputs/unresolved_exceptions.csv
< b2aa14f8b312f1a735663b70b69137f2df190ab9ef731c51c31def8d05bd14e4  repo/ledgerguard/evaluation/outputs/no_gate_ablation.md
< b3ceedf8b7067eb970ee33a6f7802ea154a10aa6fcbabe903b7880a0cd5634dc  repo/ledgerguard/evaluation/outputs/drift.md
< b877b4cdb9f9dfc33ff7ad0e82915e3e6fad2b84ccd8e3e9170943758834ff4d  repo/ledgerguard/evaluation/outputs/model_comparison.md
< bbfc6509ce38c53329da95bde380675d231fcfbb15efd4428252aae3eef32d12  repo/ledgerguard/evaluation/outputs/calibration.md
< c52561e7f550a9c66a045bd6aaebd91f8883f120a624bf773d2a3dfae1753c7d  repo/ledgerguard/evaluation/outputs/decision_log.json
< c58809b7c6b57a77dd33ce948b09988c6c9ded01bacb052b2f4f9b2d5193d6d7  repo/ledgerguard/evaluation/outputs/reconciliation_report.csv
< ccc33093b532b19e326ed4ac8f8d16d29645807f3fe97841a10dc7d242f57917  repo/ledgerguard/evaluation/outputs/no_gate_ablation.json
< fc84418ada9f206e10f07170d5c3e362c531474c13abefed04eadabf32c6cda2  repo/ledgerguard/evaluation/outputs/ablation.md
---
> 06f71351dd21bdcdb30705986832111987fe71ff6d6787ed2a198c88de50a53f  ledgerguard/evaluation/frozen/holdout_20260905_320.json
> 1fbca2999ea5f5b76d810ac2955beb5fca7bc5af165320a752be60dbe4b96100  ledgerguard/evaluation/outputs/model_comparison.json
> 227f79916be1cbe13addb7096e2f0f453660e2dc4ef83e4081ff8bcbee2ef9cf  ledgerguard/evaluation/outputs/scale.md
> 249e3bce69daeb83386d9575e66bf4177d4db885a8864ab6b32d80b5717d8536  ledgerguard/evaluation/outputs/benchmark.json
> 3699ea28a60eed7b419b027283ae1a9a3875eeb7c43e674adddfc0d195aa50c1  ledgerguard/evaluation/outputs/evidence_ledger.csv
> 530301222288c5c487d56e9029f570bd01720e1fdbd306c90b9f71c71488cd4b  ledgerguard/evaluation/outputs/scale.json
> 7a9f6520bbeb849b4e6f1f15a78f39a608583c6776c7c310457ed053a82dd41c  ledgerguard/evaluation/outputs/reconciliation_report.md
> 7ffa151674c19541ac0b4cf9a8618b4c5a8eef664afd9ab81321961848cecd03  ledgerguard/evaluation/outputs/ablation.json
> 8dc1212f1c93e7c1bf34d92923c1d31f15b7096a0b39e4c2afa4e167f4eda9d4  ledgerguard/evaluation/outputs/calibration.json
> a5552fcb48631411cb08fae4e34987295cca132334d6c31d86601f73e538455b  ledgerguard/evaluation/outputs/cases.json
> aa667ebea4ccd41fa0bdff898182200d3bf282ef0b888cabd7b5a215d82edd22  ledgerguard/evaluation/outputs/benchmark.md
> ac427b5c78460109ba2fb3914c2d04310e80089ea245dcf44f426bc2da5562a7  
... [1549 more characters in transcript.jsonl]
```

**Agent:** The diff is only the `repo/` path prefix, since the "before" hashes were taken from the parent directory. I'll strip the prefix to confirm the per-file hashes match, then remove the cache directories my test runs created (they're gitignored).

**Bash:**
```
cd <attempt>/work && sed 's#repo/##' tmp/artifacts_before.sha | sort > tmp/b.sha && sed 's#repo/##' tmp/artifacts_after.sha | sort > tmp/a.sha && diff tmp/b.sha tmp/a.sha && echo ARTIFACTS_UNCHANGED_21_FILES && cd repo && find . -name __pycache__ -not -path "./.venv/*" -exec rm -rf {} + ; rm -rf .pytest_cache; ls -a
```

**Result:**
```
ARTIFACTS_UNCHANGED_21_FILES
.
..
.env.example
.gitignore
.venv
docs
ledgerguard
README.md
requirements.txt
run_demo.sh
```

**Agent:** Artifacts are unchanged across all 21 files, and the caches are cleared. One more check: how often the generated data contains a settlement whose net breaks I1. That tells me whether the fix touches any generated case, and I'll fix a typo ("a INR") in a test docstring while I'm here.

**Bash:**
```
PYTHONPATH=. .venv/bin/python -c "
from ledgerguard.synthetic.fault_injector import build_dataset
from ledgerguard.reconciliation.matcher import reconcile_batch
d=build_dataset(seed=20260905,count=320)
res,_=reconcile_batch(d.batch(), d.lifecycle_by_payment())
i1=[c.case_id for c in res if any(i.name.startswith('I1_') and not i.holds for i in c.invariants)]
print('cases with I1 broken:', len(i1), i1[:5])
" && sed -i '' 's/claims a INR 250/claims an INR 250/' ledgerguard/tests/test_short_settlement.py && grep -n "an INR 250" ledgerguard/tests/test_short_settlement.py && rm -rf ledgerguard/__pycache__ ledgerguard/*/__pycache__ ledgerguard/tests/__pycache__ 2>/dev/null; true
```

**Result:**
```
cases with I1 broken: 0 []
[This command modified 1 file you've previously read: ledgerguard/tests/test_short_settlement.py. Call Read before editing.]
```

**Agent:** The count is zero: the generator never produces a settlement with a broken net, so no generated case changes. The sed step reported a conflict, so I'll check the test file's current state before editing.

**Bash:**
```
grep -n "INR 250 refund" ledgerguard/tests/test_short_settlement.py; ls ledgerguard/tests/ | head -20
```

**Result:**
```
132:    the settlement's components claim a INR 250 refund that is not in the batch.
__init__.py
rehearsal_check.py
test_dashboard_startup.py
test_evidence_download.py
test_fallback.py
test_p0_core.py
test_p1_compound.py
test_p1_extended.py
test_p2_evaluation.py
test_short_settlement.py
```

**Edit:**
```
<attempt>/work/repo/ledgerguard/tests/test_short_settlement.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/tests/test_short_settlement.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

**Agent:** Now I'll write the notes file the task asks for.

**Write:**
```
<attempt>/work/out/NOTES.md
```

**Result:**
```
File created successfully at: <attempt>/work/out/NOTES.md (file state is current in your context — no need to Read it back)
```

**Agent:** Final pass: the full suite after the typo fix, the artifact hash check, and cache cleanup.

**Bash:**
```
.venv/bin/python -m pytest ledgerguard/tests -q -p no:cacheprovider 2>&1 | tail -1 && cd .. && (cd repo && find ledgerguard/evaluation/outputs ledgerguard/evaluation/frozen -type f -exec shasum -a 256 {} \; | sed 's#\./##' | sort) > tmp/a2.sha && sed 's#^[0-9a-f]* *repo/##' /dev/null; diff <(awk '{print $1, $2}' tmp/artifacts_before.sha | sed 's#repo/##' | sort) <(awk '{print $1, $2}' tmp/a2.sha | sed 's#^\([0-9a-f]*\) *ledgerguard#\1 ledgerguard#' | sort) && echo ARTIFACTS_UNCHANGED && cd repo && find . -name __pycache__ -not -path "./.venv/*" -exec rm -rf {} + ; rm -rf .pytest_cache; git status 2>/dev/null; ls ../out
```

**Result (error):**
```
Exit code 1
73 passed, 1 warning in 9.60s
diff: /dev/fd/12: Operation not permitted
ls: ../out: No such file or directory
```

**Agent:** The test run passed (73). The hash check failed only because this shell blocks process substitution, not because of the artifacts. I'll redo the comparison with plain files.

**Bash:**
```
cd <attempt>/work && sed 's#^\([0-9a-f]*\)  repo/#\1  #' tmp/artifacts_before.sha | sort > tmp/b2.sha && (cd repo && find ledgerguard/evaluation/outputs ledgerguard/evaluation/frozen -type f -exec shasum -a 256 {} \; | sort) > tmp/a3.sha && diff tmp/b2.sha tmp/a3.sha && echo ARTIFACTS_UNCHANGED_21 ; cd repo && find . -name __pycache__ -not -path "./.venv/*" -exec rm -rf {} + ; rm -rf .pytest_cache; ls -a ../out; ls -a
```

**Result:**
```
ARTIFACTS_UNCHANGED_21
.
..
NOTES.md
.
..
.env.example
.gitignore
.venv
docs
ledgerguard
README.md
requirements.txt
run_demo.sh
```

**Agent:** A settlement whose reported net was ₹250 short of its own components was auto-closed because the auto-close check never looked at the reported net. It now escalates to human review. The full suite passes (73 tests: the original 67 plus 6 new).

**Cause:** The gate for a fee-mismatch close checks for unexplained money, the `residual_paise` guard. In `reconciliation/matcher.py` that residual was rebuilt from the settlement's gross, fees, refunds and adjustments, never from its reported `net_amount`. In the reported case the components agree with the shadow ledger, so the residual was zero. The ₹250 sat only in the reported net, which breaks invariant I1. The classifier labels an I1 break as `FEE_MISMATCH`, so the case went down the auto-close branch. The existing compound fixtures always keep net consistent with components, so this path was never tested.

**Fix:**
- `reconciliation/matcher.py`: alongside the component residual, compute a net residual from what the provider actually paid, adjusted for the fee variance. Also record `fee_variance_paise`.
- `evidence/safety.py`: block auto-close if either residual is non-zero. The escalation reason now states the fee variance is zero when it is, instead of describing a fee reconciliation that didn't happen.

The reported case now returns `HUMAN_REVIEW_REQUIRED` with "250.00 INR unattributed". The reproduction returns `AUTO_RESOLVED` on the original code.

**Why this is the right fix:** The README and `compound.py` say a proven cause closes a case only if it accounts for all the money, and that the model proposes while the financial system proves. The guard was supposed to enforce that and was measuring the wrong quantity. Also, whenever I1 fails, at least one of the two residuals is non-zero, so no broken settlement can auto-close as a fee mismatch. When I1 holds, the two residuals are algebraically identical, so consistent settlements behave exactly as before.

**Verification:**
- Six new tests in `ledgerguard/tests/test_short_settlement.py`. Against the original code, the bug test fails with `AUTO_RESOLVED`.
- I ran the deterministic pipeline on the frozen holdout and on all 320 lifecycles, with the original and fixed code. Per-case state, exception type and exposure are identical. The offline heuristic stands in for the AI path.
- All 21 files under `evaluation/outputs/` and `evaluation/frozen/` match their pre-edit SHA-256 hashes. I did not run the benchmark, because it overwrites `outputs/` and the committed numbers come from a live Groq run I can't repeat without an API key.
- The generator never produces a broken settlement (0 of 320 lifecycles), so the published numbers aren't affected.

**Judgement calls and limits** (also in `../out/NOTES.md`):
- I kept the `FEE_MISMATCH` label for I1-only breaks, even though the fee variance is zero. Reclassifying them as unexplained shortfalls would send them to the AI investigator, which could close them on a coincidental refund. That's a new closure path and should be a separate change with its own holdout analysis.
- The live benchmark artifacts were not regenerated, so the holdout equivalence is shown with the deterministic engine and the offline stub, not the committed Groq run.

No commits were made.
