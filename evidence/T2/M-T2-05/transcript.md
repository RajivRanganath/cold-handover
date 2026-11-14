# M-T2-05 transcript (PASS)

**Agent:** I'll start with the handover docs at the repo root, as the task requires.

**Bash:**
```
ls -la && find . -path ./.venv -prune -o -type f -print | grep -v __pycache__ | head -200
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
cat README.md | head -400
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
... [15592 more characters in transcript.jsonl]
```

**Bash:**
```
cat docs/architecture.md docs/evaluation.md docs/limitations.md | head -400
```

**Result:**
```
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
overcharge keeps I1 holding, so only an ind
... [16055 more characters in transcript.jsonl]
```

**Bash:**
```
cd ledgerguard && cat reconciliation/matcher.py reconciliation/exceptions.py ledger/invariants.py ledger/models.py
```

**Result:**
```
<persisted-output>
Output too large (30KB). Full output saved to: <attempt>/claude-config/projects/-Users-user-Desktop-tms-work-runs-M-T2-05-work-repo/6f911ab6-4c62-4b56-a690-d40aebc20291/tool-results/bzgc9oiox.txt

Preview (first 2KB):
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
...
</persisted-output>
```

**Bash:**
```
cat reconciliation/matcher.py
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
cat reconciliation/exceptions.py ledger/invariants.py ledger/models.py
```

**Result:**
```
"""Exception construction and the exception taxonomy exposed to the AI."""

from __future__ import annotations

from ..ledger.models import ExceptionType, ReconciliationException, Risk

#: The only hypotheses the AI investigator is permitted to return.
PERMITTED_HYPOTHESES = [
    "unlinked_partial_refund",
    "fee_or_tax_variance",
    "duplicate_deduction",
    "timing_difference",
    "unexplained_deduction",
    "insufficient_evidence",
]

#: Exception types the deterministic engine can already prove the cause of.
#: These never reach the AI investigator.
DETERMINISTICALLY_PROVEN = {
    ExceptionType.MISSING_SETTLEMENT,
    ExceptionType.DUPLICATE_RECORD,
    ExceptionType.FEE_MISMATCH,
    ExceptionType.DELAYED_SETTLEMENT,
}

#: Exception types that are genuinely ambiguous and warrant investigation.
NEEDS_INVESTIGATION = {
    ExceptionType.UNEXPLAINED_SHORTFALL,
    ExceptionType.AMBIGUOUS_REFERENCE,
    ExceptionType.BANK_MISMATCH,
}

#: Which hypotheses have an evidence battery that actually explains a given
#: exception type.
#:
#: Verifying a hypothesis against the records is necessary but not sufficient:
#: a battery can pass while explaining the wrong discrepancy. The refund
#: battery reconstructs the *settlement* net (E7), so it can prove an
#: UNEXPLAINED_SHORTFALL. It says nothing about why a *bank* credit disagrees
#: with a settlement, so it must never close a BANK_MISMATCH -- otherwise a
#: coincidentally-matching orphan refund could auto-resolve a bank-side fault
#: on evidence that never addressed it.
ADMISSIBLE_HYPOTHESES: dict[ExceptionType, set[str]] = {
    ExceptionType.UNEXPLAINED_SHORTFALL: {"unlinked_partial_refund"},
    ExceptionType.BANK_MISMATCH: set(),
    ExceptionType.AMBIGUOUS_REFERENCE: set(),
}

_RISK_BY_TYPE = {
    ExceptionType.MISSING_SETTLEMENT: Risk.HIGH,
    ExceptionType.UNEXPLAINED_SHORTFALL: Risk.HIGH,
    ExceptionType.BANK_MISMATCH: Risk.HIGH,
    ExceptionType.DUPLICATE_RECORD: Risk.MEDIUM,
    ExceptionType.FEE_MISMATCH: Risk.MEDIUM,
    ExceptionType.AMBIGUOUS_REFERENCE: Risk.MEDIUM,
    ExceptionType.DELAYED_SETTLEMENT: Risk.LOW,
}


def make_exception(
    *,
    case_id: str,
    lifecycle_id: str,
    transaction_ids: list[str],
    exception_type: ExceptionType,
    detected_by: str,
    expected_value: int | None,
    observed_value: int | None,
    evidence: dict,
) -> ReconciliationException:
    difference = None
    if expected_value is not None and observed_value is not None:
        difference = expected_value - observed_value
    return ReconciliationException(
        exception_id=f"EXC-{case_id}",
        lifecycle_id=lifecycle_id,
        transaction_ids=transaction_ids,
        exception_type=exception_type,
        detected_by=detected_by,
        expected_value=expected_value,
        observed_value=observed_value,
        difference=difference,
        evidence=evidence,
        risk=_RISK_BY_TYPE.get(exception_type, Risk.MEDIUM),
    )
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
         
... [10862 more characters in transcript.jsonl]
```

**Bash:**
```
cat ledger/shadow_ledger.py; echo ----; cat pipeline.py
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
... [9261 more characters in transcript.jsonl]
```

**Agent:** The core flow is clear. Next I'll find every other place that reads settlements, and check how the generator and the benchmark touch them.

**Bash:**
```
grep -rn "settlement" --include=*.py . | grep -v "tests/" | grep -iv "settlement_date\|settlement_id\b" | head -150; echo ----; grep -rn "SettlementStatus\|status=\|\.status" --include=*.py synthetic/ | head -60
```

**Result:**
```
(eval):1: no matches found: --include=*.py
----
(eval):1: no matches found: --include=*.py
```

**Bash:**
```
grep -rn "settlement" --include='*.py' . | grep -v "/tests/" | head -200
```

**Result:**
```
qa.py:112:def _missing_settlements(report: RunReport) -> tuple[str, list[str]]:
qa.py:120:        f"{len(cases)} captured payments have no settlement record, "
qa.py:144:    _Query("missing_settlements", ("missing settlement", "never settled", "not settled"),
qa.py:145:           "payments with no settlement", _missing_settlements),
reconciliation/matcher.py:3:Ordinary software runs first. Exact identifier matching, exact settlement
reconciliation/matcher.py:37:    settlement: Settlement | None
reconciliation/matcher.py:52:    settlement_ids: set[str] = field(default_factory=set)
reconciliation/matcher.py:58:    settlement_conflicts: set[str] = field(default_factory=set)
reconciliation/matcher.py:76:def _settlement_signature(s: Settlement) -> tuple:
reconciliation/matcher.py:77:    """Everything about a settlement except its identifier."""
reconciliation/matcher.py:86:        s.settlement_date,
reconciliation/matcher.py:121:    and settlements are grouped by id and then split by signature; bank entries
reconciliation/matcher.py:129:    dup.settlement_ids, dup.settlement_conflicts = _id_groups(
reconciliation/matcher.py:130:        batch.settlements, lambda s: s.settlement_id, _settlement_signature
reconciliation/matcher.py:144:        "I1_settlement_arithmetic_consistent",
reconciliation/matcher.py:148:    ExceptionType.DUPLICATE_RECORD: {"I6_bank_credit_matches_settlement"},
reconciliation/matcher.py:149:    ExceptionType.DELAYED_SETTLEMENT: {"I5_settlement_within_window"},
reconciliation/matcher.py:154:    ExceptionType.BANK_MISMATCH: {"I6_bank_credit_matches_settlement"},
reconciliation/matcher.py:170:    if "I1_settlement_arithmetic_consistent" in failing:
reconciliation/matcher.py:171:        return ExceptionType.FEE_MISMATCH, failing["I1_settlement_arithmetic_consistent"]
reconciliation/matcher.py:176:    if "I6_bank_credit_matches_settlement" in failing:
reconciliation/matcher.py:177:        inv = failing["I6_bank_credit_matches_settlement"]
reconciliation/matcher.py:181:    if "I5_settlement_within_window" in failing:
reconciliation/matcher.py:182:        return ExceptionType.DELAYED_SETTLEMENT, failing["I5_settlement_within_window"]
reconciliation/matcher.py:196:    settlements = ledger.settlements_for(payment.payment_id)
reconciliation/matcher.py:201:    def build(exc_type, expected_value, observed_value, evidence, settlement, invs):
reconciliation/matcher.py:206:            + ([settlement.settlement_id] if settlement else []),
reconciliation/matcher.py:219:            settlement=settlement,
reconciliation/matcher.py:241:            settlements[0] if settlements else None,
reconciliation/matcher.py:256:            settlements[0] if settlements else None,
reconciliation/matcher.py:260:    # 2. No settlement at all.
reconciliation/matcher.py:261:    if not settlements:
reconciliation/matcher.py:267:                "reason": "captured payment has no settlement record",
reconciliation/matcher.py:275:    # 3. More than one settlement claims the same payment.
reconciliation/matcher.py:276:    if len(settlements) > 1:
reconciliation/matcher.py:280:        signatures = {_settlement_signature(s) for s in settlements}
reconciliation/matcher.py:282:            s.settlement_id in duplicates.settlement_conflicts for s in settlements
reconciliation/matcher.py:286:                "multiple settlements reference the same payment with conflicting content"
reconciliation/matcher.py:288:                else "multiple settlements reference the same payment"
reconciliation/matcher.py:290:            "settlement_ids": [s.settlement_id for s in settlements],
reconciliation/matcher.py:293:            evidence["content_conflict"] = "settlement"
reconciliation/matcher.py:297:            sum(s.net_amount for s in settlements),
reconciliation/matcher.py:299:            settlements[0],
reconciliation/matcher.py:303:    settlement = settlements[0]
reconciliation/matcher.py:304:    bank = ledger.bank_entries_for_settlement(settlement)
reconciliati
... [14036 more characters in transcript.jsonl]
```

**Bash:**
```
grep -rn "SettlementStatus\|settlement.*status\|status.*settlement\|pending\|PENDING\|FAILED" --include='*.py' . | head -80
```

**Result:**
```
ledger/models.py:26:    FAILED = "failed"
ledger/models.py:32:    PENDING = "pending"
ledger/models.py:33:    FAILED = "failed"
ledger/models.py:36:class SettlementStatus(str, Enum):
ledger/models.py:38:    PENDING = "pending"
ledger/models.py:39:    FAILED = "failed"
ledger/models.py:94:    status: SettlementStatus = SettlementStatus.PROCESSED
ai/openai_compatible.py:540:            # going to start; retire it rather than spending the whole run on it.
synthetic/generator.py:28:    SettlementStatus,
synthetic/generator.py:208:            status=SettlementStatus.PROCESSED,
evaluation/benchmark.py:313:                f"  FAILED {failure['operation']} via {failure['provider']}: "
evaluation/replay.py:9:has to be answerable in August, from the record, without the answer depending on
evaluation/replay.py:167:        print(f"\nREPLAY FAILED: {len(mismatches)} mismatches")
```

**Agent:** The generator only ever emits `processed` settlements, so the holdout data cannot change from this work. Next I'll check the gating path (`should_investigate`, `decide`), the QA helper, and the test helpers I'll reuse.

**Bash:**
```
cd <attempt>/work/repo/ledgerguard; grep -n "def should_investigate" -A 25 ai/investigator.py; echo ----; sed -n 100,135p qa.py; echo ----; sed -n 1,60p evidence/safety.py; echo ----; sed -n 130,170p evidence/safety.py
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
45-
46-    difference = exc.difference
47-
48-    candidates = []
49-    if exc.exception_type is ExceptionType.UNEXPLAINED_SHORTFALL and difference:
50-        for r in ledger.candidate_orphan_refunds(difference):
51-            candidates.append(
52-                {
53-                    "record_type": "refund",
54-                    "refund_id": r.refund_id,
55-                    "amount": r.amount,
56-                    "status": r.status.value,
57-                    "created_at": r.created_at.isoformat(),
----


def _match_rate(report: RunReport) -> tuple[str, list[str]]:
    matched = sum(1 for o in report.outcomes if o.state == MATCHED)
    total = len(report.outcomes)
    pct = (matched / total * 100) if total else 0
    return (
        f"{matched} of {total} payments reconciled with no exception ({pct:.1f}%).",
        [],
    )


def _missing_settlements(report: RunReport) -> tuple[str, list[str]]:
    cases = [
        o for o in report.outcomes
        if o.case.exception
        and o.case.exception.exception_type.value == "EXCEPTION_MISSING_SETTLEMENT"
    ]
    total = sum(o.exposure_paise for o in cases)
    return (
        f"{len(cases)} captured payments have no settlement record, "
        f"INR {to_rupees_str(total)} outstanding.",
        [o.case_id for o in cases],
    )


def _rejected_hypotheses(report: RunReport) -> tuple[str, list[str]]:
    cases = [
        o for o in report.outcomes
        if o.verification and o.verification.verdict == "REJECTED"
    ]
    return (
        f"The Evidence Gate rejected {len(cases)} proposed explanations. "
        "Each was disproved on a linkage check, not on amount.",
        [o.case_id for o in cases],
    )
----
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
    ExceptionType.MISSING_SETTLEMENT: "Captured funds have no settlement
... [2396 more characters in transcript.jsonl]
```

**Bash:**
```
cd <attempt>/work/repo/ledgerguard; sed -n 1,80p tests/test_p1_extended.py; echo ----; sed -n 140,170p tests/test_p1_extended.py; echo ----; sed -n 395,430p tests/test_p1_extended.py; echo; grep -n "def \|^from\|^import" tests/test_p1_compound.py | head -40
```

**Result:**
```
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

T0 = datetime(2026, 6, 10, 10, 0, 0)


def _cases_by_fault(dataset, results):
    fault = dataset.fault_class_by_payment()
    out: dict[str, list] = {}
    for r in results:
        out.setdefault(fault[r.payment_id], []).append(r)
    return out


# --------------------------------------------------------------- duplicates
def test_duplicate_payment_and_bank_entry_are_both_detected():
    """Both duplicate shapes must be caught, and neither may be double counted."""
    dataset = build_dataset()
    results, _ = reconcile_batch(dataset.batch(), dataset.lifecycle_by_payment())
    by_fault = _cases_by_fault(dataset, results)

    dupes = by_fault[FaultClass.F2_DUPLICATE_RECORD]
    assert dupes, "generator produced no duplicate cases"
    assert all(
        c.status == ExceptionType.DUPLICATE_RECORD.value for c in dupes
    ), [(c.payment_id, c.status) for c in dupes]

    # The injector produces two distinct duplicate shapes; both must be present,
    # otherwise a regression in one is invisible.
    reasons = {c.exception.evidence.get("reason", "") for c in dupes}
    assert any("payment_id appears more than once" in r for r in reasons), reasons
    assert any("share reference" in r for r in reasons), reasons

    # A duplicated payment must collapse into exactly one case, not two.
    batch = dataset.batch()
    payment_ids = [c.payment_id for c in results]
    assert len(payment_ids) == len(set(payment_ids)), "a payment produced two cases"
    assert len(batch.payments) > len(results), "no duplicate rows in the batch to collapse"


def test_find_duplicates_distinguishes_id_from_content_duplication():
    fee = platform_fee(100000)
    payment = Payment(
----
        o for o in run(exact, use_ai=False).outcomes
        if o.case.payment_id == clean.payment_id
    )
    assert closed.state == AUTO_RESOLVED


def test_two_settlements_that_disagree_are_never_collapsed_into_one():
    """Same payment, two settlements, different nets. Which is real is unproven."""
    dataset = build_dataset()
    _dev, holdout = split(dataset)
    batch = holdout.batch()

    original = batch.settlements[0]
    rival = original.model_copy(
        update={
            "settlement_id": original.settlement_id + "X",
            "net_amount": original.net_amount - 5000,
        }
    )
    tampered = batch.model_copy(
        update={"settlements": list(batch.settlements) + [rival]}
    )

    outcome = next(
        o for o in run(tampered, use_ai=False).outcomes
        if o.case.payment_id == original.payment_ids[0]
    )
    assert outcome.case.exception.evidence["content_conflict"] == "settlement"
    assert outcome.state == HUMAN_REVIEW_REQUIRED


----
        order_id="ord_N", merchant_id="m", amount=amount, created_at=T0,
        customer_reference="CUST-N",
    )
    payment = Paym
... [2052 more characters in transcript.jsonl]
```

**Agent:** Before editing I want a baseline: the test status, and checksums of the protected artifact directories so I can prove they're unchanged at the end. I'll also check whether the benchmark can write somewhere other than `outputs/`.

**Bash:**
```
cd <attempt>/work/repo; mkdir -p ../tmp ../out; find ledgerguard/evaluation/outputs ledgerguard/evaluation/frozen -type f -exec shasum -a 256 {} \; | sort > ../tmp/artifacts_before.sha; cat ../tmp/artifacts_before.sha | wc -l; grep -n "outputs\|OUT\|argparse\|add_argument" ledgerguard/evaluation/benchmark.py | head -40; echo ----; .venv/bin/python -m pytest ledgerguard/tests -q 2>&1 | tail -15
```

**Result:**
```
      21
7:same frozen holdout, and writes every artifact under evaluation/outputs/.
20:import argparse
36:OUTPUT_DIR = Path(__file__).parent / "outputs"
67:                "FROZEN HOLDOUT MISMATCH.\n"
239:    parser = argparse.ArgumentParser(description="LedgerGuard benchmark")
240:    parser.add_argument("--seed", type=int, default=20260905)
241:    parser.add_argument("--count", type=int, default=320)
242:    parser.add_argument(
246:    parser.add_argument(
254:    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
277:    (OUTPUT_DIR / "benchmark.md").write_text(md)
278:    (OUTPUT_DIR / "benchmark.json").write_text(
301:        hybrid_report, scored, OUTPUT_DIR / "unresolved_exceptions.csv"
303:    export_cases(hybrid_report, scored, OUTPUT_DIR / "cases.json")
337:    print(f"\nArtifacts written to {OUTPUT_DIR}")
344:            "or OMNIROUTE_API_KEY) and rerun to measure against a real investigator."
----
...................................................................      [100%]
=============================== warnings summary ===============================
.venv/lib/python3.14/site-packages/fastapi/testclient.py:1
  <attempt>/work/repo/.venv/lib/python3.14/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
67 passed, 1 warning in 5.18s
```

**Agent:** Baseline is 67 passing. The benchmark hardcodes its output directory, so to compare results without touching the protected artifacts I'll run it from a copy of the code. First I'll snapshot the pre-change code and record its benchmark output.

**Bash:**
```
cd <attempt>/work; rm -rf tmp/baseline && mkdir -p tmp/baseline && cp -R repo/ledgerguard tmp/baseline/ && cd tmp/baseline && <attempt>/work/repo/.venv/bin/python -c "import ledgerguard,sys;print(ledgerguard.__file__)" && <attempt>/work/repo/.venv/bin/python -m ledgerguard.evaluation.benchmark --provider none > ../bench_before_none.txt 2>&1; echo exit=$?; tail -5 ../bench_before_none.txt; cd ..; grep -c . bench_before_none.txt
```

**Result:**
```
<attempt>/work/tmp/baseline/ledgerguard/__init__.py
exit=0


Artifacts written to <attempt>/work/tmp/baseline/ledgerguard/evaluation/outputs
  benchmark.md, benchmark.json, cases.json
  unresolved_exceptions.csv (19 rows)
48
Shell cwd was reset to <attempt>/work/repo
```

**Agent:** Baseline recorded: 67 tests pass and the benchmark ran on the pre-change copy. Settlement logic lives in three places: the shadow ledger's index, the duplicate pre-pass, and the matcher's per-payment branches. I'll filter at the index so every downstream step sees only processed settlements, and expose the non-processed ones separately for the new evidence key.

**Edit:**
```
<attempt>/work/repo/ledgerguard/ledger/shadow_ledger.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/ledger/shadow_ledger.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

**Bash:**
```
cd <attempt>/work/repo/ledgerguard && grep -n "settlements_by_payment: dict\|for s in self.batch.settlements" -A 3 ledger/shadow_ledger.py
```

**Result:**
```
78:    settlements_by_payment: dict[str, list[Settlement]] = field(default_factory=dict)
79-    bank_by_reference: dict[str, list[BankEntry]] = field(default_factory=dict)
80-    orphan_refunds: list[Refund] = field(default_factory=list)
81-
--
96:        for s in self.batch.settlements:
97-            for pid in s.payment_ids:
98-                self.settlements_by_payment.setdefault(pid, []).append(s)
99-        for b in self.batch.bank_entries:
```

**Edit:**
```
<attempt>/work/repo/ledgerguard/ledger/shadow_ledger.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/ledger/shadow_ledger.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

**Edit:**
```
<attempt>/work/repo/ledgerguard/ledger/shadow_ledger.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/ledger/shadow_ledger.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

**Edit:**
```
<attempt>/work/repo/ledgerguard/ledger/shadow_ledger.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/ledger/shadow_ledger.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

**Agent:** Next, the matcher: the settlement duplicate pre-pass should only see processed settlements, and the no-settlement branch should add the new evidence key.

**Edit:**
```
<attempt>/work/repo/ledgerguard/reconciliation/matcher.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/reconciliation/matcher.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

**Edit:**
```
<attempt>/work/repo/ledgerguard/reconciliation/matcher.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/reconciliation/matcher.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

**Edit:**
```
<attempt>/work/repo/ledgerguard/reconciliation/matcher.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/reconciliation/matcher.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

**Agent:** I named the evidence dict `missing_evidence`, which collides with the gate's own "missing evidence" concept. Renaming it to `evidence`.

**Edit:**
```
<attempt>/work/repo/ledgerguard/reconciliation/matcher.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/reconciliation/matcher.py has been updated. All occurrences were successfully replaced. (file state is current in your context — no need to Read it back)
```

**Edit:**
```
<attempt>/work/repo/ledgerguard/reconciliation/matcher.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/reconciliation/matcher.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

**Edit:**
```
<attempt>/work/repo/ledgerguard/reconciliation/matcher.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/reconciliation/matcher.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

**Agent:** The matcher and index changes are in. Before writing tests I need the provider interface, so the end-to-end test can prove the investigator is never called.

**Bash:**
```
grep -n "class \|def investigate\|def __init__\|name = \|name:" ai/provider.py | head -40; grep -n "def platform_fee\|def gst_on_fee" ledger/money.py
```

**Result:**
```
72:class InvestigatorProvider(Protocol):
73:    name: str
75:    def investigate(self, context: dict) -> InvestigationResult:  # pragma: no cover
79:def _to_result(out: InvestigatorOutput, source: str, model_name: str | None) -> InvestigationResult:
91:class AnthropicProvider:
94:    def __init__(
102:        self.name = f"anthropic:{model}"
109:    def investigate(self, context: dict) -> InvestigationResult:
140:class HeuristicProvider:
148:    name = "heuristic_stub"
150:    def investigate(self, context: dict) -> InvestigationResult:
211:class UnavailableProvider:
214:    name = "unavailable"
216:    def __init__(self, error: str = "no investigator provider is configured") -> None:
219:    def investigate(self, context: dict) -> InvestigationResult:
48:def platform_fee(captured_paise: Paise) -> Paise:
53:def gst_on_fee(fee_paise: Paise) -> Paise:
```

**Agent:** I have what I need. Now the tests: a new file, since existing test files must stay untouched. They cover pending/failed-only payments, the evidence key's exact shape and ordering, processed-plus-noise cases, duplicate precedence, and an end-to-end check that these cases never reach the investigator. They also include a control where a processed settlement does reach it, so the spy is shown to work.

**Write:**
```
<attempt>/work/repo/ledgerguard/tests/test_settlement_status.py
```

**Result:**
```
File created successfully at: <attempt>/work/repo/ledgerguard/tests/test_settlement_status.py (file state is current in your context — no need to Read it back)
```

**Agent:** Running the new file, then the full suite.

**Bash:**
```
cd <attempt>/work/repo && .venv/bin/python -m pytest ledgerguard/tests/test_settlement_status.py -q 2>&1 | tail -30; .venv/bin/python -m pytest ledgerguard/tests -q 2>&1 | tail -3
```

**Result:**
```
.................                                                        [100%]
17 passed in 0.14s

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
84 passed, 1 warning in 4.70s
```

**Agent:** All 84 pass (67 existing and 17 new). Two more checks: the new tests should fail against the old code, which shows they actually exercise the change, and the benchmark should be identical on the frozen holdout.

**Bash:**
```
cd <attempt>/work && cp repo/ledgerguard/tests/test_settlement_status.py tmp/baseline/ledgerguard/tests/ && cd tmp/baseline && ../../repo/.venv/bin/python -m pytest ledgerguard/tests/test_settlement_status.py -q 2>&1 | tail -3; cd ../.. && rm -rf tmp/after && mkdir -p tmp/after && cp -R repo/ledgerguard tmp/after/ && cd tmp/after && ../../repo/.venv/bin/python -m ledgerguard.evaluation.benchmark --provider none > ../bench_after_none.txt 2>&1; echo exit=$?; cd ..; for f in benchmark.json cases.json unresolved_exceptions.csv benchmark.md; do echo "== $f"; diff baseline/ledgerguard/evaluation/outputs/$f after/ledgerguard/evaluation/outputs/$f | head -20; done
```

**Result:**
```
FAILED ledgerguard/tests/test_settlement_status.py::test_the_shadow_ledger_separates_processed_from_non_processed_settlements
FAILED ledgerguard/tests/test_settlement_status.py::test_reconcile_batch_gives_one_case_per_payment_with_non_processed_noise
14 failed, 3 passed in 0.23s
exit=0
== benchmark.json
129c129
<     "throughput_per_second": 27411.3,
---
>     "throughput_per_second": 27914.2,
217c217
<     "throughput_per_second": 28138.3,
---
>     "throughput_per_second": 28363.3,
223c223
<     "latency_p95_ms": 0.01,
---
>     "latency_p95_ms": 0.0,
== cases.json
3130c3130
<       "latency_ms": 0.01,
---
>       "latency_ms": 0.0,
== unresolved_exceptions.csv
== benchmark.md
34c34
< | Throughput (cases/s) | 27411.3 | 28138.3 |
---
> | Throughput (cases/s) | 27914.2 | 28363.3 |
39c39
< | Investigation latency p95 (ms) | 0.0 | 0.01 |
---
> | Investigation latency p95 (ms) | 0.0 | 0.0 |
Shell cwd was reset to <attempt>/work/repo
```

**Agent:** Against the old code, 14 of the 17 new tests fail. The 3 that pass are the controls showing unchanged behaviour, as intended. The benchmark diff is limited to wall-clock timing fields; every decision, exception, and count is identical. I'll add one sentence to the architecture doc, since it describes the matcher's settlement rule, then verify the protected artifacts.

**Edit:**
```
<attempt>/work/repo/docs/architecture.md
```

**Result:**
```
The file <attempt>/work/repo/docs/architecture.md has been updated successfully.
```

**Bash:**
```
find ledgerguard/evaluation/outputs ledgerguard/evaluation/frozen -type f -exec shasum -a 256 {} \; | sort > ../tmp/artifacts_after.sha; diff ../tmp/artifacts_before.sha ../tmp/artifacts_after.sha && echo "ARTIFACTS UNCHANGED"; find . -name "*.py" -newer ../tmp/artifacts_before.sha -not -path "./.venv/*"; ls ../out
```

**Result:**
```
ARTIFACTS UNCHANGED
./ledgerguard/reconciliation/matcher.py
./ledgerguard/ledger/shadow_ledger.py
./ledgerguard/tests/test_settlement_status.py
```

**Agent:** The protected artifacts are byte-identical and only the three intended files changed. I'll write the handover notes the task asks for.

**Write:**
```
<attempt>/work/out/NOTES.md
```

**Result:**
```
File created successfully at: <attempt>/work/out/NOTES.md (file state is current in your context — no need to Read it back)
```

**Agent:** Settlement status is now respected. Only `processed` settlements can settle a payment, and the full suite passes (84 tests: 67 existing, 17 new).

**What changed**
- **Index** (`ledger/shadow_ledger.py`): only processed settlements go into the index every matching step reads. Pending and failed ones go into a separate index, used only for the new evidence key.
- **Matcher** (`reconciliation/matcher.py`):
  - The duplicate pre-pass considers only processed settlements. A pending copy of a processed settlement cannot create a duplicate or a content conflict.
  - A payment with no processed settlement is `EXCEPTION_MISSING_SETTLEMENT`, with the same expected value, observed 0, and final state as before. If it has non-processed settlements, its evidence gains `non_processed_settlements`, sorted by `settlement_id`.
  - Payment-level duplicate handling runs first, as before.
- **Docs**: one paragraph added to `docs/architecture.md`.
- **Tests**: `ledgerguard/tests/test_settlement_status.py`. Against the old code, 14 of the 17 new tests fail; the other 3 are controls for unchanged behaviour. The tests also cover the controller: a pending or failed settlement never reaches the investigator and is never auto-resolved. A control shows the same shortfall as a processed settlement *is* investigated, so the spy is shown to work.

**Verification**
- **Benchmark**: I ran it offline (`--provider none`) on copies of the code before and after the change. The outputs are identical apart from wall-clock timing fields. The generator only emits processed settlements, so the frozen holdout is unaffected.
- **Artifacts**: SHA-256 checksums of all 21 files under `outputs/` and `frozen/` match before and after. Nothing was regenerated in the repository.

**Not done**
- The canonical benchmark (groq/fallback) was not re-run. It needs API keys, which I must not set, and live model output is not reproducible anyway.
- `rehearsal_check` was not run, since it needs a live server.

**Choices I made** (recorded in `../out/NOTES.md`)
- The evidence list has one entry per non-processed record, not deduplicated.
- Non-processed settlement ids are not added to `transaction_ids`, so the case matches the no-settlement case exactly apart from the evidence key.
