# M-T4-05 transcript (PASS)

**Agent:** I'll start with the handover docs at the repo root, as the ground rules require.

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
Output too large (36.5KB). Full output saved to: <attempt>/claude-config/projects/-Users-user-Desktop-tms-work-runs-M-T4-05-work-repo/a552eb42-b078-4643-82e6-2f19b11649f0/tool-results/bxg9af55z.txt

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
cat docs/architecture.md | tail -n +40; echo ----; cat docs/limitations.md | head -150
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
... [15616 more characters in transcript.jsonl]
```

**Agent:** The architecture doc names a `residual_paise` guard in `evidence/safety.py` that should block a fee-mismatch close when money is still unattributed. That's the likely place. Reading the core code now.

**Bash:**
```
cat ledgerguard/evidence/safety.py
```

**Result:**
```
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
        return Decision(
            case_id=case.case_id
... [6646 more characters in transcript.jsonl]
```

**Bash:**
```
cat ledgerguard/reconciliation/matcher.py
```

**Result:**
```
"""Deterministic reconciliation engine.

Ordinary software runs first. Exact identifier matching, exact settlement
arithmetic against the Shadow Ledger, duplicate detection, timing windows and
bank matching all happen here. Anything provable at this layer never reaches
the model.

The matcher produces exactly one case per captured payment.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ..ledger.invariants import InvariantResult, check_all
from ..ledger.models import (
    Batch,
    ExceptionType,
    Payment,
    PaymentStatus,
    ReconciliationException,
    Settlement,
)
from ..ledger.shadow_ledger import ExpectedSettlement, ShadowLedger
from .exceptions import make_exception

MATCHED = "MATCHED"


@dataclass
class CaseResult:
    case_id: str
    payment_id: str
    order_id: str | None
    status: str                                  # MATCHED or an ExceptionType value
    expected: ExpectedSettlement
    settlement: Settlement | None
    invariants: list[InvariantResult] = field(default_factory=list)
    exception: ReconciliationException | None = None

    @property
    def is_exception(self) -> bool:
        return self.status != MATCHED

    def failing_invariants(self) -> list[InvariantResult]:
        return [i for i in self.invariants if not i.holds]


@dataclass
class BatchDuplicates:
    payment_ids: set[str] = field(default_factory=set)
    settlement_ids: set[str] = field(default_factory=set)
    bank_signatures: dict[tuple, list[str]] = field(default_factory=dict)
    #: Ids that appear more than once carrying *different* content. Sharing an
    #: identifier is not the same finding as being the same record, and the two
    #: must not resolve the same way -- see ``_id_groups``.
    payment_conflicts: set[str] = field(default_factory=set)
    settlement_conflicts: set[str] = field(default_factory=set)


def _payment_signature(p: Payment) -> tuple:
    """Everything about a payment except its identifier."""
    return (
        p.order_id,
        p.amount,
        p.currency,
        p.status,
        p.method,
        p.captured_at,
        p.fee,
        p.tax,
        p.reference,
    )


def _settlement_signature(s: Settlement) -> tuple:
    """Everything about a settlement except its identifier."""
    return (
        s.merchant_id,
        s.gross_amount,
        s.fees,
        s.tax,
        s.refund_adjustments,
        s.other_adjustments,
        s.net_amount,
        s.settlement_date,
        s.status,
        s.reference,
        tuple(s.payment_ids),
    )


def _id_groups(records, key, signature) -> tuple[set[str], set[str]]:
    """Split repeated identifiers into true duplicates and content conflicts.

    A record ingested twice is a duplicate: the identifier and every other
    field agree, so suppressing the second copy is provable. Two records that
    share an identifier but disagree on content are *not* a duplicate -- they
    are two contradictory versions of the same entity, and which one is real
    cannot be proved from the batch. Collapsing them would close a case on a
    content match that never happened.
    """
    by_id: dict[str, list[tuple]] = {}
    for record in records:
        by_id.setdefault(key(record), []).append(signature(record))
    duplicates, conflicts = set(), set()
    for record_id, signatures in by_id.items():
        if len(signatures) < 2:
            continue
        if len(set(signatures)) == 1:
            duplicates.add(record_id)
        else:
            conflicts.add(record_id)
    return duplicates, conflicts


def find_duplicates(batch: Batch) -> BatchDuplicates:
    """Pre-pass: identifier and content level duplicate detection.

    Every record type is compared on content, not only on identifier. Payments
    and settlements are grouped by id and then split by signature; bank entries
    carry no reliable identifier across systems, so they are matched on content
    alone.
    """
    dup = BatchDuplicat
... [11807 more characters in transcript.jsonl]
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

**Agent:** The bug looks like it's in the `residual_paise` computation in `matcher.py`. `corrected_net` is built only from gross, schedule fees/tax and adjustments, and never from the settlement's reported `net_amount`, so a shortfall in the reported net can't show up in it. Checking the shadow ledger, the fault injector and the existing tests before concluding.

**Bash:**
```
cat ledgerguard/ledger/shadow_ledger.py; echo ----; cat ledgerguard/ledger/money.py; echo ----; grep -n "residual\|FEE\|fee" -i ledgerguard/synthetic/fault_injector.py | head -80
```

**Result:**
```
"""The Shadow Ledger.

An independent reconstruction of what the financial movement *should* have
been, computed from first principles out of orders, payments and refunds.

It never reads settlement or bank records to decide what to expect -- that is
the whole point. Settlements and bank entries are the *observed* side; the
Shadow Ledger is the *expected* side, and reconciliation is the comparison.

The AI investigator can call ``expected_for_payment`` to inspect output, but
has no path to change how the number is produced.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta

from .models import (
    Batch,
    BankEntry,
    Order,
    Payment,
    PaymentStatus,
    Refund,
    RefundStatus,
    Settlement,
)
from .money import gst_on_fee, platform_fee

# Provider settlement window: money captured on day T is expected to settle on
# T+2, and we allow a one day tolerance either side for weekends/holidays.
SETTLEMENT_LAG_DAYS = 2
SETTLEMENT_WINDOW_TOLERANCE_DAYS = 1

# Bank credit is expected on the settlement date, allowing one day of float.
BANK_CREDIT_TOLERANCE_DAYS = 1


@dataclass(frozen=True)
class ExpectedSettlement:
    """What the Shadow Ledger says a payment should settle for."""

    payment_id: str
    gross_amount: int
    fees: int
    tax: int
    refund_adjustments: int
    other_adjustments: int
    net_amount: int
    refund_ids: tuple[str, ...] = ()
    window_start: datetime | None = None
    window_end: datetime | None = None

    def as_dict(self) -> dict:
        return {
            "payment_id": self.payment_id,
            "gross_amount": self.gross_amount,
            "fees": self.fees,
            "tax": self.tax,
            "refund_adjustments": self.refund_adjustments,
            "other_adjustments": self.other_adjustments,
            "net_amount": self.net_amount,
            "refund_ids": list(self.refund_ids),
        }


@dataclass
class ShadowLedger:
    """Indexes a batch and computes expected financial movement."""

    batch: Batch
    orders_by_id: dict[str, Order] = field(default_factory=dict)
    payments_by_id: dict[str, Payment] = field(default_factory=dict)
    refunds_by_id: dict[str, Refund] = field(default_factory=dict)
    refunds_by_payment: dict[str, list[Refund]] = field(default_factory=dict)
    settlements_by_payment: dict[str, list[Settlement]] = field(default_factory=dict)
    bank_by_reference: dict[str, list[BankEntry]] = field(default_factory=dict)
    orphan_refunds: list[Refund] = field(default_factory=list)

    def __post_init__(self) -> None:
        self._index()

    def _index(self) -> None:
        for o in self.batch.orders:
            self.orders_by_id.setdefault(o.order_id, o)
        for p in self.batch.payments:
            self.payments_by_id.setdefault(p.payment_id, p)
        for r in self.batch.refunds:
            self.refunds_by_id.setdefault(r.refund_id, r)
            if r.payment_id:
                self.refunds_by_payment.setdefault(r.payment_id, []).append(r)
            else:
                self.orphan_refunds.append(r)
        for s in self.batch.settlements:
            for pid in s.payment_ids:
                self.settlements_by_payment.setdefault(pid, []).append(s)
        for b in self.batch.bank_entries:
            self.bank_by_reference.setdefault(b.reference, []).append(b)

    # ---------------------------------------------------------------- expected

    def valid_refunds_for(self, payment_id: str) -> list[Refund]:
        """Refunds that are *provably* linked to this payment and processed."""
        return [
            r
            for r in self.refunds_by_payment.get(payment_id, [])
            if r.status == RefundStatus.PROCESSED
        ]

    def expected_for_payment(
        self,
        payment: Payment,
        extra_refunds: list[Refund] | None = None,
        other_adjustments: int = 0,
    ) -> ExpectedSettlement:
        """Reconstruct the
... [5618 more characters in transcript.jsonl]
```

**Agent:** The root cause is now clear. `residual_paise` is computed as `expected.net_amount - corrected_net`, and `corrected_net` is rebuilt from gross, schedule fees and adjustments. The settlement's reported `net_amount` never enters the calculation, so a shortfall in the reported net is invisible to the guard. Before changing anything I'll check the existing tests, the benchmark plumbing, and whether the holdout contains any fee-mismatch cases that would be affected.

**Bash:**
```
cd ledgerguard && grep -rn "residual\|FEE_MISMATCH\|fee_mismatch" --include=*.py . | grep -v "^./evaluation/outputs"; echo ----; sed -n 95,190p synthetic/fault_injector.py
```

**Result:**
```
(eval):1: no matches found: --include=*.py
----
        fault_class=FaultClass.F3_UNLINKED_PARTIAL_REFUND,
        expected_exception=ExceptionType.UNEXPLAINED_SHORTFALL.value,
        expected_disposition=AUTO,
        true_cause=(
            f"Shortfall is genuinely explained by refund {refund.refund_id} "
            f"({refund.amount} paise), which belongs to payment {lc.payment.payment_id} "
            "but lost its linkage during ingestion."
        ),
        exposure_paise=refund.amount,
    )


def _apply_f4(lc: Lifecycle, rng: random.Random) -> GroundTruth:
    """Fee or tax mismatch: provider charged off-schedule fees."""
    s = lc.settlement
    delta = rng.randrange(2000, max(3000, int(s.gross_amount * 0.012)), 100)
    s.fees += delta
    s.tax = gst_on_fee(s.fees)
    correct_tax = gst_on_fee(platform_fee(s.gross_amount))
    s.net_amount = (
        s.gross_amount - s.fees - s.tax - s.refund_adjustments + s.other_adjustments
    )
    for e in lc.bank_entries:
        e.amount = s.net_amount
    overcharge = delta + (s.tax - correct_tax)
    return GroundTruth(
        lifecycle_id=lc.lifecycle_id,
        fault_class=FaultClass.F4_FEE_TAX_MISMATCH,
        expected_exception=ExceptionType.FEE_MISMATCH.value,
        expected_disposition=AUTO,
        true_cause=(
            f"Fee overcharged by {delta} paise plus GST; total overcharge {overcharge} paise."
        ),
        exposure_paise=overcharge,
    )


def _apply_f5(lc: Lifecycle, rng: random.Random) -> GroundTruth:
    """Delayed settlement: correct amounts, outside the expected window."""
    from datetime import timedelta

    delay = rng.randrange(5, 13)
    lc.settlement.settlement_date += timedelta(days=delay)
    for e in lc.bank_entries:
        e.date = lc.settlement.settlement_date
    return GroundTruth(
        lifecycle_id=lc.lifecycle_id,
        fault_class=FaultClass.F5_DELAYED_SETTLEMENT,
        expected_exception=ExceptionType.DELAYED_SETTLEMENT.value,
        expected_disposition=AUTO,
        true_cause=f"Settlement arrived {delay} days late; all amounts are correct.",
        exposure_paise=0,
    )


def _apply_f6(victim: Lifecycle, donor: Lifecycle, rng: random.Random) -> tuple[GroundTruth, GroundTruth]:
    """Incorrect linkage -- the adversarial case.

    ``donor`` is given a genuine F3 (its own refund is unlinked). ``victim``
    is given an unexplained deduction of *exactly the same amount* with no
    refund of its own anywhere in the system.

    From the outside the two exceptions are indistinguishable: same shape,
    same size, one plausible orphan refund that fits both by amount. Only the
    customer linkage separates them, and only the Evidence Gate checks it.
    """
    donor_truth = _apply_f3(donor, rng)
    refund = donor.refunds[0]
    amount = refund.amount

    s = victim.settlement
    s.refund_adjustments += amount
    s.net_amount = (
        s.gross_amount - s.fees - s.tax - s.refund_adjustments + s.other_adjustments
    )
    for e in victim.bank_entries:
        e.amount = s.net_amount

    victim_truth = GroundTruth(
        lifecycle_id=victim.lifecycle_id,
        fault_class=FaultClass.F6_INCORRECT_LINKAGE,
        expected_exception=ExceptionType.UNEXPLAINED_SHORTFALL.value,
        expected_disposition=HUMAN,
        true_cause=(
            f"Settlement deducted {amount} paise with no refund for payment "
            f"{victim.payment.payment_id}. Refund {refund.refund_id} matches the amount "
            f"exactly but belongs to customer {donor.order.customer_reference} "
            f"(payment {donor.payment.payment_id}). Not resolvable from available evidence."
        ),
        exposure_paise=amount,
        paired_with=donor.lifecycle_id,
    )
    donor_truth.paired_with = victim.lifecycle_id
    return victim_truth, donor_truth
```

**Bash:**
```
cd <attempt>/work/repo && grep -rn "residual\|FEE_MISMATCH\|fee_mismatch\|F4" --include=*.py ledgerguard | grep -v "outputs/"; echo ----; grep -n "def \|outputs\|write" ledgerguard/evaluation/benchmark.py | head -80
```

**Result:**
```
(eval):1: no matches found: --include=*.py
----
7:same frozen holdout, and writes every artifact under evaluation/outputs/.
36:OUTPUT_DIR = Path(__file__).parent / "outputs"
40:def manifest_path(seed: int, count: int) -> Path:
44:    can never silently overwrite the holdout an earlier result was scored on.
49:def batch_digest(dataset: Dataset) -> str:
53:def freeze_or_verify_holdout(holdout: Dataset, seed: int, count: int) -> dict:
71:                "delete the manifest deliberately and say so in the write-up.\n"
77:    path.write_text(json.dumps(manifest, indent=2) + "\n")
81:def _row(label: str, baseline, hybrid, fmt=str) -> str:
85:def render_markdown(base: Metrics, hyb: Metrics, manifest: dict) -> str:
86:    def inr(paise: int) -> str:
149:def write_unresolved_csv(report: RunReport, dataset: Dataset, path: Path) -> int:
154:        writer = csv.writer(fh)
155:        writer.writerow(
177:            writer.writerow(
195:def export_cases(report: RunReport, dataset: Dataset, path: Path) -> None:
235:    path.write_text(json.dumps(payload, indent=2, default=str) + "\n")
238:def main(argv: list[str] | None = None) -> int:
277:    (OUTPUT_DIR / "benchmark.md").write_text(md)
278:    (OUTPUT_DIR / "benchmark.json").write_text(
300:    n_unresolved = write_unresolved_csv(
```

**Bash:**
```
grep -rn -e residual -e FEE_MISMATCH -e fee_mismatch -e F4 ledgerguard --exclude-dir=outputs --exclude-dir=__pycache__ ; echo ----; sed -n 1,80p ledgerguard/evaluation/benchmark.py | sed -n 1,40p; sed -n 238,300p ledgerguard/evaluation/benchmark.py
```

**Result:**
```
ledgerguard/reconciliation/matcher.py:143:    ExceptionType.FEE_MISMATCH: {
ledgerguard/reconciliation/matcher.py:169:        return ExceptionType.FEE_MISMATCH, failing["I2_fees_and_tax_match_schedule"]
ledgerguard/reconciliation/matcher.py:171:        return ExceptionType.FEE_MISMATCH, failing["I1_settlement_arithmetic_consistent"]
ledgerguard/reconciliation/matcher.py:352:    elif exc_type is ExceptionType.FEE_MISMATCH:
ledgerguard/reconciliation/matcher.py:367:        evidence["residual_paise"] = expected.net_amount - corrected_net
ledgerguard/reconciliation/exceptions.py:22:    ExceptionType.FEE_MISMATCH,
ledgerguard/reconciliation/exceptions.py:54:    ExceptionType.FEE_MISMATCH: Risk.MEDIUM,
ledgerguard/ledger/models.py:110:    FEE_MISMATCH = "EXCEPTION_FEE_MISMATCH"
ledgerguard/evidence/safety.py:30:    ExceptionType.FEE_MISMATCH: "Fee and tax reconciled against the independent fee schedule; the exact variance is quantified.",
ledgerguard/evidence/safety.py:114:    residual = exc.evidence.get("residual_paise") or 0
ledgerguard/evidence/safety.py:118:        if residual:
ledgerguard/evidence/safety.py:128:                    f"{to_rupees_str(abs(residual))} INR unattributed, with no record "
ledgerguard/evidence/safety.py:131:                missing_evidence=["explanation for the residual deduction"],
ledgerguard/tests/test_p2_evaluation.py:119:    assert shifted.dominant_exception == "EXCEPTION_FEE_MISMATCH"
ledgerguard/tests/test_p0_core.py:205:        FaultClass.F4_FEE_TAX_MISMATCH: "EXCEPTION_FEE_MISMATCH",
ledgerguard/tests/test_p1_compound.py:6:    money; any unattributed residual blocks closure, while a second finding that
ledgerguard/tests/test_p1_compound.py:46:def test_an_unattributed_residual_blocks_closure_on_the_proven_cause():
ledgerguard/tests/test_p1_compound.py:51:    residual = outcome.case.exception.evidence["residual_paise"]
ledgerguard/tests/test_p1_compound.py:52:    assert residual == to_paise("650.00"), residual
ledgerguard/tests/test_p1_compound.py:57:    # C5 is the same shape with the residual explained by a refund that belongs
ledgerguard/tests/test_p1_compound.py:60:    assert c5.case.exception.evidence["residual_paise"] == to_paise("900.00")
ledgerguard/tests/test_p1_compound.py:70:    assert not outcome.case.exception.evidence.get("residual_paise")
ledgerguard/backend/app.py:299:        (FaultClass.F4_FEE_TAX_MISMATCH, None),
ledgerguard/synthetic/generator.py:46:    F4_FEE_TAX_MISMATCH = "F4_FEE_TAX_MISMATCH"
ledgerguard/synthetic/compound.py:151:        ("F4", "F6"), "pay_C2", HUMAN,
ledgerguard/synthetic/compound.py:188:        ("F4", "F6"), "pay_C5", HUMAN,
ledgerguard/synthetic/fault_injector.py:122:        fault_class=FaultClass.F4_FEE_TAX_MISMATCH,
ledgerguard/synthetic/fault_injector.py:123:        expected_exception=ExceptionType.FEE_MISMATCH.value,
ledgerguard/synthetic/fault_injector.py:239:    # ---- F1, F2, F4, F5 spread over the remaining budget.
----
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
from ..eviden
... [2973 more characters in transcript.jsonl]
```

**Agent:** Existing compound tests assert specific `residual_paise` values (650.00, 900.00). I'll read those tests and the compound generator, since they pin the current semantics.

**Bash:**
```
cd <attempt>/work/repo/ledgerguard && cat tests/test_p1_compound.py; echo ----; sed -n 1,80p synthetic/compound.py
```

**Result:**
```
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
            wrong.append((case.case_id, case.name, got, case.expected_disposition))
    assert not wrong, wrong

    # No compound case may ever be closed against ground truth.
    for case in cases.values():
        if case.expected_disposition == HUMAN_REVIEW_REQUIRED:
            assert outcomes[case.payment_id].state != AUTO_RESOLVED, case.case_id


def test_an_unattributed_residual_blocks_closure_on_the_proven_cause():
    """C2: the fee overcharge is proven; INR 650.00 is still missing."""
    outcomes, _ = _run()
    outcome = outcomes["pay_C2"]

    residual = outcome.case.exception.evidence["residual_paise"]
    assert residual == to_paise("650.00"), residual
    assert outcome.state == HUMAN_REVIEW_REQUIRED
    assert "unattributed" in outcome.decision.reason
    assert "650.00" in outcome.decision.reason

    # C5 is the same shape with the residual explained by a refund that belongs
    # to a different customer -- still blocked, and for the same reason.
    c5 = outcomes["pay_C5"]
    assert c5.case.exception.evidence["residual_paise"] == to_paise("900.00")
    assert c5.state == HUMAN_REVIEW_REQUIRED


def test_a_fully_attributed_case_still_closes_and_reports_the_second_finding():
    """C3: duplicate credit plus a delay. Nothing unexplained, so it closes."""
    outcomes, _ = _run()
    outcome = outcomes["pay_C3"]

    assert outcome.state == AUTO_RESOLVED
    assert not outcome.case.exception.evidence.get("residual_paise")
    # The delay was not the classification, and must still be surfaced.
    assert "I5_settlement_within_window" in outcome.case.exception.evidence["secondary_findings"]
    assert "I5_settlement_within_window" in outcome.decision.reason


def test_a_resolved_shortfall_does_not_swallow_a_concurrent_delay():
    """C1: the refund genuinely explains the gap, but the case is also late."""
    outcomes, _ = _run()
    outcome = outcomes["pay_C1"]

    assert outcome.state == AUTO_RESOLVED
    assert outcome.verification.verdict == "VERIFIED"
    assert "I5_settlement_within_window" in outcome.case.exception.evidence["secondary_findings"]
    assert "I5_settlement_within_window" in outcome.decision.reason


def test_a_matching_orphan_refund_cannot_offset_a_settlement_that_never_arrived():
    """C4: no settlement exists, so there is nothing to net the refund against."""
    outcomes, _ = _run()
    outcome = outcomes["pay_C4"]

    assert outcome.case.exception.exception_type.value == "EXCEPTION_MISSING_SETTLEMENT"
    assert outcome.state == HUMAN_REVIEW_REQUIRED
    assert outcome.investigation is None, "a missing settlement is proven, not investigated"
    # The who
... [2259 more characters in transcript.jsonl]
```

**Bash:**
```
sed -n 80,260p synthetic/compound.py
```

**Result:**
```
    if not settle:
        return order, payment, None, []

    charged_fee = fee + fee_overcharge
    charged_tax = gst_on_fee(charged_fee)
    net = amount - charged_fee - charged_tax - refund_adjustment
    settled_on = captured + timedelta(days=2 + days_late)
    settlement = Settlement(
        settlement_id=f"setl_{tag}",
        merchant_id=order.merchant_id,
        payment_ids=[payment.payment_id],
        gross_amount=amount,
        fees=charged_fee,
        tax=charged_tax,
        refund_adjustments=refund_adjustment,
        other_adjustments=0,
        net_amount=net,
        settlement_date=settled_on,
        reference=f"STL/setl_{tag}",
    )
    entries = [
        BankEntry(
            bank_entry_id=f"bnk_{tag}",
            amount=net,
            credit_or_debit=CreditDebit.CREDIT,
            date=settled_on,
            reference=settlement.reference,
        )
    ]
    if duplicate_bank_credit:
        entries.append(entries[0].model_copy(update={"bank_entry_id": f"bnk_{tag}D"}))
    return order, payment, settlement, entries


def build_compound_batch() -> tuple[Batch, list[CompoundCase]]:
    orders, payments, refunds, settlements, entries = [], [], [], [], []
    cases: list[CompoundCase] = []

    def add(leg, refund=None):
        o, p, s, e = leg
        orders.append(o)
        payments.append(p)
        if s:
            settlements.append(s)
        entries.extend(e)
        if refund:
            refunds.append(refund)

    # --- C1: late settlement AND an unlinked partial refund -----------------
    # Both faults are real. The refund is genuinely this payment's, so the
    # discrepancy is resolvable -- but the delay must not disappear because the
    # shortfall was classified first.
    r1 = to_paise("900.00")
    add(_leg("C1", "CUST-C1", to_paise("6000.00"), refund_adjustment=r1, days_late=7),
        Refund(refund_id="rfnd_C1", payment_id=None, amount=r1,
               created_at=T0 + timedelta(days=1), reference="ADJ/CUST-C1/partial"))
    cases.append(CompoundCase(
        "C1", "delayed settlement + unlinked partial refund",
        ("F5", "F3"), "pay_C1", AUTO,
        "The refund genuinely belongs to this payment and restores the ledger. "
        "Resolvable -- but the 7 day delay is a second finding that must still "
        "be reported, not silently absorbed.",
    ))

    # --- C2: fee overcharge AND an unexplained deduction --------------------
    # The fee variance is provable. The extra deduction is not. Closing on the
    # proven cause alone would leave real money unexplained.
    add(_leg("C2", "CUST-C2", to_paise("9000.00"),
             fee_overcharge=to_paise("40.00"), refund_adjustment=to_paise("650.00")))
    cases.append(CompoundCase(
        "C2", "fee overcharge + unexplained deduction",
        ("F4", "F6"), "pay_C2", HUMAN,
        "The fee overcharge is deterministically proven, but correcting it does "
        "not close the gap: INR 650.00 is still deducted with no refund record "
        "anywhere. One proven cause does not license closing the case.",
    ))

    # --- C3: duplicate bank credit AND a late settlement --------------------
    add(_leg("C3", "CUST-C3", to_paise("4500.00"), days_late=6,
             duplicate_bank_credit=True))
    cases.append(CompoundCase(
        "C3", "duplicate bank credit + delayed settlement",
        ("F2", "F5"), "pay_C3", AUTO,
        "Both faults are individually provable and neither leaves money "
        "unexplained: the duplicate is suppressed and the delay is timing only.",
    ))

    # --- C4: missing settlement, with a tempting orphan refund --------------
    # Nothing settled at all, and an unlinked refund of a plausible size sits in
    # the batch. It must not be netted against a settlement that never arrived.
    add(_leg("C4", "CUST-C4", to_paise("7000.00"), settle=False),
        Refund(refund_id="rfnd_C4", payment_id=None, amount=to_paise("1200.00"),
               created_at=T0 + timedelta(days
... [1336 more characters in transcript.jsonl]
```

**Agent:** The compound tests pin 650.00 (C2) and 900.00 (C5). Those are reconstructed with a self-consistent `net_amount`, so my reasoning says the corrected formula gives the same values. I'll verify that with a run rather than assume it.

Before editing I need two things: a checksum snapshot of `outputs/` and `frozen/` (no git here, so I can't diff), and a check on whether the test suite writes into those directories.

**Bash:**
```
find evaluation/outputs evaluation/frozen -type f -exec shasum -a 256 {} \; | sort > <attempt>/work/tmp/artifacts_before.sha256; cat <attempt>/work/tmp/artifacts_before.sha256; echo ----; grep -rn -e "OUTPUT_DIR" -e "outputs" -e "benchmark.main\|benchmark import\|main(" tests/ | head -40; echo ----; cat pipeline.py | head -150
```

**Result:**
```
06f71351dd21bdcdb30705986832111987fe71ff6d6787ed2a198c88de50a53f  evaluation/frozen/holdout_20260905_320.json
1fbca2999ea5f5b76d810ac2955beb5fca7bc5af165320a752be60dbe4b96100  evaluation/outputs/model_comparison.json
227f79916be1cbe13addb7096e2f0f453660e2dc4ef83e4081ff8bcbee2ef9cf  evaluation/outputs/scale.md
249e3bce69daeb83386d9575e66bf4177d4db885a8864ab6b32d80b5717d8536  evaluation/outputs/benchmark.json
3699ea28a60eed7b419b027283ae1a9a3875eeb7c43e674adddfc0d195aa50c1  evaluation/outputs/evidence_ledger.csv
530301222288c5c487d56e9029f570bd01720e1fdbd306c90b9f71c71488cd4b  evaluation/outputs/scale.json
7a9f6520bbeb849b4e6f1f15a78f39a608583c6776c7c310457ed053a82dd41c  evaluation/outputs/reconciliation_report.md
7ffa151674c19541ac0b4cf9a8618b4c5a8eef664afd9ab81321961848cecd03  evaluation/outputs/ablation.json
8dc1212f1c93e7c1bf34d92923c1d31f15b7096a0b39e4c2afa4e167f4eda9d4  evaluation/outputs/calibration.json
a5552fcb48631411cb08fae4e34987295cca132334d6c31d86601f73e538455b  evaluation/outputs/cases.json
aa667ebea4ccd41fa0bdff898182200d3bf282ef0b888cabd7b5a215d82edd22  evaluation/outputs/benchmark.md
ac427b5c78460109ba2fb3914c2d04310e80089ea245dcf44f426bc2da5562a7  evaluation/outputs/drift.json
af74f00254d9a8cee944bccdf9fd8940c2a318c0bfd5c6965dbfc5a221e00711  evaluation/outputs/unresolved_exceptions.csv
b2aa14f8b312f1a735663b70b69137f2df190ab9ef731c51c31def8d05bd14e4  evaluation/outputs/no_gate_ablation.md
b3ceedf8b7067eb970ee33a6f7802ea154a10aa6fcbabe903b7880a0cd5634dc  evaluation/outputs/drift.md
b877b4cdb9f9dfc33ff7ad0e82915e3e6fad2b84ccd8e3e9170943758834ff4d  evaluation/outputs/model_comparison.md
bbfc6509ce38c53329da95bde380675d231fcfbb15efd4428252aae3eef32d12  evaluation/outputs/calibration.md
c52561e7f550a9c66a045bd6aaebd91f8883f120a624bf773d2a3dfae1753c7d  evaluation/outputs/decision_log.json
c58809b7c6b57a77dd33ce948b09988c6c9ded01bacb052b2f4f9b2d5193d6d7  evaluation/outputs/reconciliation_report.csv
ccc33093b532b19e326ed4ac8f8d16d29645807f3fe97841a10dc7d242f57917  evaluation/outputs/no_gate_ablation.json
fc84418ada9f206e10f07170d5c3e362c531474c13abefed04eadabf32c6cda2  evaluation/outputs/ablation.md
----
tests/rehearsal_check.py:147:def main() -> int:
tests/rehearsal_check.py:168:    sys.exit(main())
----
"""End to end controller run.

    deterministic reconciliation
      -> AI investigation, but only for what could not be proved
      -> Evidence Gate
      -> uniqueness pass
      -> safety and action gate

Running with ``use_ai=False`` gives the rules-only baseline: identical
deterministic layer, no investigation step. That is the comparison the
benchmark makes.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field

from .ai.investigator import Investigation, investigate_case, should_investigate
from .ai.provider import InvestigatorProvider, UnavailableProvider, get_provider
from .ai.schemas import InvestigationResult
from .evidence.safety import Decision, HUMAN_REVIEW_REQUIRED, decide
from .evidence.verifier import (
    VerificationOutcome,
    resolve_evidence_conflicts,
    verify,
)
from .ledger.models import Batch
from .ledger.shadow_ledger import ShadowLedger
from .reconciliation.matcher import CaseResult, reconcile_batch


@dataclass
class CaseOutcome:
    case: CaseResult
    investigation: Investigation | None = None
    verification: VerificationOutcome | None = None
    decision: Decision | None = None

    @property
    def case_id(self) -> str:
        return self.case.case_id

    @property
    def state(self) -> str:
        if not self.case.is_exception:
            return "MATCHED"
        return self.decision.state if self.decision else HUMAN_REVIEW_REQUIRED

    @property
    def exposure_paise(self) -> int:
        exc = self.case.exception
        if exc is None or exc.difference is None:
            return 0
        return abs(exc.difference)


@dataclass
class RunReport:
    system: str
    provider_name: str
    outcomes: list[CaseOutcome] = field(d
... [3232 more characters in transcript.jsonl]
```

**Agent:** Nothing in the test suite writes to `outputs/` (the only hit is a `main()` in the rehearsal script, which I'll check later). Next I'll capture the pre-fix deterministic decisions for all 320 lifecycles and the holdout, so I can diff them after the change. I'll also reproduce the reported ₹250 case directly.

**Bash:**
```
mkdir -p <attempt>/work/tmp/scripts && cat > <attempt>/work/tmp/scripts/snapshot.py <<'EOF'
import json, sys
from ledgerguard.synthetic.fault_injector import build_dataset, split
from ledgerguard.pipeline import run

out = sys.argv[1]
full = build_dataset(seed=20260905, count=320)
dev, holdout = split(full)
res = {}
for label, ds in [("full", full), ("holdout", holdout)]:
    lbp = ds.lifecycle_by_payment()
    rep = run(ds.batch(), use_ai=False, lifecycle_by_payment=lbp)
    rows = []
    for o in rep.outcomes:
        exc = o.case.exception
        rows.append({
            "case": o.case_id,
            "type": exc.exception_type.value if exc else "MATCHED",
            "state": o.state,
            "residual": (exc.evidence.get("residual_paise") if exc else None),
            "reason": o.decision.reason if o.decision else None,
        })
    res[label] = rows
json.dump(res, open(out, "w"), indent=1, sort_keys=True, default=str)
print({k: len(v) for k, v in res.items()})
EOF
cd <attempt>/work/repo && PYTHONPATH=. .venv/bin/python ../tmp/scripts/snapshot.py ../tmp/before.json && cat > ../tmp/scripts/repro.py <<'EOF'
from datetime import datetime, timedelta
from ledgerguard.ledger.models import *
from ledgerguard.ledger.money import platform_fee, gst_on_fee, to_paise
from ledgerguard.pipeline import run
T0 = datetime(2026, 7, 15, 10, 0)
amt = to_paise("10000.00"); fee = platform_fee(amt); tax = gst_on_fee(fee)
ref = to_paise("0")
net = amt - fee - tax - 0 - to_paise("250.00")   # 250 short, fees per schedule
captured = T0 + timedelta(minutes=5)
batch = Batch(
    orders=[Order(order_id="o1", merchant_id="m", amount=amt, created_at=T0, customer_reference="C1")],
    payments=[Payment(payment_id="p1", order_id="o1", amount=amt, captured_at=captured, fee=fee, tax=tax, reference="PAY/o1")],
    refunds=[],
    settlements=[Settlement(settlement_id="s1", merchant_id="m", payment_ids=["p1"], gross_amount=amt, fees=fee, tax=tax,
        refund_adjustments=0, other_adjustments=0, net_amount=net, settlement_date=captured+timedelta(days=2), reference="STL/s1")],
    bank_entries=[BankEntry(bank_entry_id="b1", amount=net, credit_or_debit=CreditDebit.CREDIT, date=captured+timedelta(days=2), reference="STL/s1")],
)
r = run(batch, use_ai=False)
for o in r.outcomes:
    print(o.case_id, o.case.exception.exception_type.value, o.state, o.case.exception.evidence.get("residual_paise"))
    print("  ", o.decision.reason)
EOF
PYTHONPATH=. .venv/bin/python ../tmp/scripts/repro.py
```

**Result:**
```
{'full': 320, 'holdout': 85}
p1 EXCEPTION_FEE_MISMATCH AUTO_RESOLVED 0
   Fee and tax reconciled against the independent fee schedule; the exact variance is quantified.
```

**Agent:** Reproduced: a settlement 250 short, with fees and tax on schedule, is `AUTO_RESOLVED` with `residual_paise = 0`. Applying the fix in the residual computation:

**Edit:**
```
<attempt>/work/repo/ledgerguard/reconciliation/matcher.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/reconciliation/matcher.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

**Bash:**
```
PYTHONPATH=. .venv/bin/python ../tmp/scripts/repro.py && PYTHONPATH=. .venv/bin/python ../tmp/scripts/snapshot.py ../tmp/after.json && cmp ../tmp/before.json ../tmp/after.json && echo IDENTICAL_DECISIONS; .venv/bin/python -c "
import json
b=json.load(open('../tmp/before.json'));a=json.load(open('../tmp/after.json'))
for k in b:
    d=[(x['case'],x['state'],y['state']) for x,y in zip(b[k],a[k]) if x!=y]
    print(k,'differences:',len(d),d[:10])
"
```

**Result:**
```
p1 EXCEPTION_FEE_MISMATCH HUMAN_REVIEW_REQUIRED 25000
   Fee and tax reconciled against the independent fee schedule; the exact variance is quantified. Correcting it still leaves 250.00 INR unattributed, with no record explaining it. A second, unproven discrepancy is present.
{'full': 320, 'holdout': 85}
IDENTICAL_DECISIONS
full differences: 0 []
holdout differences: 0 []
```

**Agent:** The fix is confined as intended. Across all 320 lifecycles and the 85-case holdout, the deterministic decisions, residuals and reason text are byte-identical to before. The only changed case is the reported one. I'll confirm that FEE_MISMATCH never reaches the investigator, since that's what makes the holdout AI results provider-independent, and check how the existing test files are written.

**Bash:**
```
grep -n "def should_investigate" -A12 ledgerguard/ai/investigator.py; echo ----; sed -n 1,40p ledgerguard/tests/test_p1_extended.py
```

**Result:**
```
32:def should_investigate(case: CaseResult) -> bool:
33-    """Only genuinely ambiguous exceptions are worth a model call."""
34-    if not case.is_exception or case.exception is None:
35-        return False
36-    return case.exception.exception_type in NEEDS_INVESTIGATION
37-
38-
39-def build_context(ledger: ShadowLedger, case: CaseResult) -> dict:
40-    """The exact payload the investigator sees. No ground truth, ever."""
41-    exc = case.exception
42-    payment = ledger.payments_by_id[case.payment_id]
43-    order = ledger.orders_by_id.get(payment.order_id or "")
44-    settlement = case.settlement
----
"""P1 extended coverage.

The five P0 tests protect the core argument. These protect the things most
likely to rot quietly underneath it: duplicate handling, timing windows,
generator reproducibility, and every way a model or an upstream record can be
malformed.

Nothing here touches the network. Providers are stubbed.
"""

from __future__ import annotations

from datetime import datetime, timedelta

import httpx
import pytest
from pydantic import ValidationError

from ledgerguard.ai.provider import HeuristicProvider
from ledgerguard.ai.schemas import (
    REASON_MAX_CHARS,
    InvestigationResult,
    InvestigatorOutput,
)
from ledgerguard.evidence.safety import AUTO_RESOLVED, HUMAN_REVIEW_REQUIRED
from ledgerguard.ledger.models import (
    BankEntry,
    Batch,
    CreditDebit,
    ExceptionType,
    Order,
    Payment,
    Settlement,
)
from ledgerguard.ledger.money import gst_on_fee, platform_fee, to_paise
from ledgerguard.pipeline import run
from ledgerguard.reconciliation.matcher import MATCHED, find_duplicates, reconcile_batch
from ledgerguard.synthetic.fault_injector import build_dataset, split
from ledgerguard.synthetic.generator import FaultClass
```

**Write:**
```
<attempt>/work/repo/ledgerguard/tests/test_residual_fee_shortfall.py
```

**Result:**
```
File created successfully at: <attempt>/work/repo/ledgerguard/tests/test_residual_fee_shortfall.py (file state is current in your context — no need to Read it back)
```

**Agent:** Now the full test suite, then the artifact checksum comparison.

**Bash:**
```
timeout 900 .venv/bin/python -m pytest ledgerguard/tests -q 2>&1 | tail -30; echo ----; find ledgerguard/evaluation/outputs ledgerguard/evaluation/frozen -type f -exec shasum -a 256 {} \; | sort > ../tmp/artifacts_after_tests.sha256; diff ../tmp/artifacts_before.sha256 ../tmp/artifacts_after_tests.sha256 && echo ARTIFACTS_UNCHANGED
```

**Result (error):**
```
Exit code 1
(eval):1: command not found: timeout
----
1,21c1,21
< 06f71351dd21bdcdb30705986832111987fe71ff6d6787ed2a198c88de50a53f  evaluation/frozen/holdout_20260905_320.json
< 1fbca2999ea5f5b76d810ac2955beb5fca7bc5af165320a752be60dbe4b96100  evaluation/outputs/model_comparison.json
< 227f79916be1cbe13addb7096e2f0f453660e2dc4ef83e4081ff8bcbee2ef9cf  evaluation/outputs/scale.md
< 249e3bce69daeb83386d9575e66bf4177d4db885a8864ab6b32d80b5717d8536  evaluation/outputs/benchmark.json
< 3699ea28a60eed7b419b027283ae1a9a3875eeb7c43e674adddfc0d195aa50c1  evaluation/outputs/evidence_ledger.csv
< 530301222288c5c487d56e9029f570bd01720e1fdbd306c90b9f71c71488cd4b  evaluation/outputs/scale.json
< 7a9f6520bbeb849b4e6f1f15a78f39a608583c6776c7c310457ed053a82dd41c  evaluation/outputs/reconciliation_report.md
< 7ffa151674c19541ac0b4cf9a8618b4c5a8eef664afd9ab81321961848cecd03  evaluation/outputs/ablation.json
< 8dc1212f1c93e7c1bf34d92923c1d31f15b7096a0b39e4c2afa4e167f4eda9d4  evaluation/outputs/calibration.json
< a5552fcb48631411cb08fae4e34987295cca132334d6c31d86601f73e538455b  evaluation/outputs/cases.json
< aa667ebea4ccd41fa0bdff898182200d3bf282ef0b888cabd7b5a215d82edd22  evaluation/outputs/benchmark.md
< ac427b5c78460109ba2fb3914c2d04310e80089ea245dcf44f426bc2da5562a7  evaluation/outputs/drift.json
< af74f00254d9a8cee944bccdf9fd8940c2a318c0bfd5c6965dbfc5a221e00711  evaluation/outputs/unresolved_exceptions.csv
< b2aa14f8b312f1a735663b70b69137f2df190ab9ef731c51c31def8d05bd14e4  evaluation/outputs/no_gate_ablation.md
< b3ceedf8b7067eb970ee33a6f7802ea154a10aa6fcbabe903b7880a0cd5634dc  evaluation/outputs/drift.md
< b877b4cdb9f9dfc33ff7ad0e82915e3e6fad2b84ccd8e3e9170943758834ff4d  evaluation/outputs/model_comparison.md
< bbfc6509ce38c53329da95bde380675d231fcfbb15efd4428252aae3eef32d12  evaluation/outputs/calibration.md
< c52561e7f550a9c66a045bd6aaebd91f8883f120a624bf773d2a3dfae1753c7d  evaluation/outputs/decision_log.json
< c58809b7c6b57a77dd33ce948b09988c6c9ded01bacb052b2f4f9b2d5193d6d7  evaluation/outputs/reconciliation_report.csv
< ccc33093b532b19e326ed4ac8f8d16d29645807f3fe97841a10dc7d242f57917  evaluation/outputs/no_gate_ablation.json
< fc84418ada9f206e10f07170d5c3e362c531474c13abefed04eadabf32c6cda2  evaluation/outputs/ablation.md
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
> ac427b5c78460109ba2fb3914c2d04310e80089ea245dcf44f426bc2da5562a7  ledgerguard/evaluation/outputs/drift.json
> af74f00254d9a8cee944bccdf9fd8940c2a318c0bfd5c6965dbfc5a221e00711  ledgerguard/evaluation/outputs/unresolved_exceptions.csv
> b2aa14f8b312f1a735663b70b69137f2df190ab9ef731c51c31def8d05bd14e4  ledgerguard/evaluation/outputs/no_gate_ablation.md
> b3ceedf8b7067eb970ee33a6f7802ea154a10aa6fcbabe903b7880a0cd5634dc  ledgerguard/evaluation/outputs/drift.md
> b877b4cdb
... [695 more characters in transcript.jsonl]
```

**Agent:** `timeout` isn't available in this zsh, and the checksum list differs only in its path prefix because the snapshot ran from inside `ledgerguard/`. The hashes themselves all match. I'll rerun the tests without `timeout` and compare the checksums with normalized paths.

**Bash:**
```
.venv/bin/python -m pytest ledgerguard/tests -q 2>&1 | tail -30; echo ----; (cd ledgerguard && find evaluation/outputs evaluation/frozen -type f -exec shasum -a 256 {} \; | sort) > ../../tmp/artifacts_after_tests.sha256; diff ../../tmp/artifacts_before.sha256 ../../tmp/artifacts_after_tests.sha256 && echo ARTIFACTS_UNCHANGED
```

**Result (error):**
```
Exit code 2
........................................................................ [100%]
=============================== warnings summary ===============================
.venv/lib/python3.14/site-packages/fastapi/testclient.py:1
  <attempt>/work/repo/.venv/lib/python3.14/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
72 passed, 1 warning in 8.07s
----
(eval):1: no such file or directory: ../../tmp/artifacts_after_tests.sha256
diff: ../../tmp/artifacts_before.sha256: No such file or directory
```

**Agent:** All 72 tests pass. The non-zero exit came from my relative path, not from a test. I'll redo the checksum comparison with absolute paths and run the new file on its own.

**Bash:**
```
W=<attempt>/work; (cd $W/repo/ledgerguard && find evaluation/outputs evaluation/frozen -type f -exec shasum -a 256 {} \; | sort) > $W/tmp/artifacts_after_tests.sha256; diff $W/tmp/artifacts_before.sha256 $W/tmp/artifacts_after_tests.sha256 && echo ARTIFACTS_UNCHANGED; cd $W/repo && .venv/bin/python -m pytest ledgerguard/tests/test_residual_fee_shortfall.py -v 2>&1 | grep -E "PASS|FAIL|passed|failed"
```

**Result:**
```
ARTIFACTS_UNCHANGED
ledgerguard/tests/test_residual_fee_shortfall.py::test_reported_case_is_not_auto_closed_when_fees_are_on_schedule PASSED [ 20%]
ledgerguard/tests/test_residual_fee_shortfall.py::test_the_same_shortfall_is_not_closed_with_the_investigator_either PASSED [ 40%]
ledgerguard/tests/test_residual_fee_shortfall.py::test_an_overpayment_of_the_same_size_is_also_unexplained PASSED [ 60%]
ledgerguard/tests/test_residual_fee_shortfall.py::test_a_fee_overcharge_with_a_shortfall_blocks_on_the_shortfall PASSED [ 80%]
ledgerguard/tests/test_residual_fee_shortfall.py::test_a_fully_explained_fee_overcharge_still_auto_closes PASSED [100%]
============================== 5 passed in 0.11s ===============================
```

**Agent:** Everything checks out: the artifact checksums match the pre-change snapshot, and the 5 new tests pass. I'll write the notes file the task asks for.

**Write:**
```
<attempt>/work/out/NOTES.md
```

**Result:**
```
File created successfully at: <attempt>/work/out/NOTES.md (file state is current in your context — no need to Read it back)
```

**Agent:** I wrote "21 outputs" in the notes, but the checksum list has 20 output files plus the frozen manifest. Correcting that.

**Edit:**
```
<attempt>/work/out/NOTES.md
```

**Result:**
```
The file <attempt>/work/out/NOTES.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

**Agent:** A settlement reported ₹250 below its own arithmetic was auto-closed as a fee mismatch because the residual check that should have caught the missing money was computed from the wrong figure. The fix is in place and verified, and the artifacts are unchanged.

**Cause:** In `ledgerguard/reconciliation/matcher.py`, the `residual_paise` for a fee mismatch was built from gross, schedule fees and adjustments, never from the net the provider actually paid. A shortfall in the reported net was therefore invisible to the guard in `evidence/safety.py`. The fee check passed because fees were on schedule.

**Fix:** The residual is now computed from the reported net, after adding back the fee variance, and compared with the Shadow Ledger's expectation. The safety gate itself was already correct, so I left it alone. The reported case now goes to `HUMAN_REVIEW_REQUIRED` with "250.00 INR unattributed" in the reason. This follows the project's documented rule that a proven cause must not close a case that still has unexplained money.

**Verification:**
- **Holdout unchanged:** I captured the deterministic decision for every case (state, type, residual, reason) across all 320 lifecycles and the 85-case holdout, before and after. They are identical. Fee-mismatch cases never reach the investigator, so the AI-dependent holdout results are unaffected too.
- **Tests:** all 72 pass, including the existing compound tests that pin residuals of 650.00 and 900.00. I added `ledgerguard/tests/test_residual_fee_shortfall.py` with 5 tests covering the reported case, an overpayment of the same size, a shortfall combined with a fee overcharge, and a regression check that a fully explained overcharge still closes.
- **Artifacts:** SHA-256 checksums of all 20 files under `evaluation/outputs/` and the frozen manifest match the pre-change snapshot.

**Not done:** I did not regenerate the benchmark. It runs against Groq, there is no key here, and regenerating in place would overwrite the protected files. The holdout equality rests on the deterministic snapshot instead.

**Notes:** The explanation, reasoning and the open wording question are in `../out/NOTES.md`. The escalation reason still opens with "Fee and tax reconciled…", which a reader could take as a claim the whole case reconciles. I left it because an existing test pins part of that wording.
