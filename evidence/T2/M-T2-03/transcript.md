# M-T2-03 transcript (PASS)

**Agent:** I'll start with the handover documentation at the repository root, then the settlement-matching code.

**Bash:**
```
ls -la && find . -path ./.venv -prune -o -type f -print | grep -v __pycache__ | head -200
```

**Result:**
```
total 88
drwxr-xr-x@ 10 user  staff    320 Nov  1 23:13 .
drwxr-xr-x@  5 user  staff    160 Nov  1 23:13 ..
-rw-r--r--@  1 user  staff   1992 Nov  1 23:13 .env.example
-rw-r--r--@  1 user  staff     56 Nov  1 23:13 .gitignore
drwxr-xr-x@  7 user  staff    224 Nov  1 23:13 .venv
drwxr-xr-x@  7 user  staff    224 Nov  1 23:13 docs
drwxr-xr-x@ 14 user  staff    448 Nov  1 23:13 ledgerguard
-rw-r--r--@  1 user  staff  26848 Nov  1 23:13 README.md
-rw-r--r--@  1 user  staff    466 Nov  1 23:13 requirements.txt
-rwxr-xr-x@  1 user  staff   1447 Nov  1 23:13 run_demo.sh
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
cat README.md | head -400 && echo ---- && cat docs/architecture.md
```

**Result:**
```
<persisted-output>
Output too large (31.4KB). Full output saved to: <attempt>/claude-config/projects/-Users-user-Desktop-tms-work-runs-M-T2-03-work-repo/ac4eeaab-a9e3-4cd6-be1a-d6435728e16e/tool-results/b6uah1nqc.txt

Preview (first 2KB):
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
...
</persisted-output>
```

**Bash:**
```
cat ledgerguard/reconciliation/matcher.py && echo ---- && cat ledgerguard/reconciliation/exceptions.py && echo ---- && cat ledgerguard/ledger/invariants.py && echo ---- && cat ledgerguard/ledger/models.py
```

**Result:**
```
<persisted-output>
Output too large (30KB). Full output saved to: <attempt>/claude-config/projects/-Users-user-Desktop-tms-work-runs-M-T2-03-work-repo/ac4eeaab-a9e3-4cd6-be1a-d6435728e16e/tool-results/b7w01i9o3.txt

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
cat ledgerguard/ledger/models.py; echo ----; cat ledgerguard/reconciliation/exceptions.py
```

**Result:**
```
"""Financial data model.

All money fields are integer paise (see ledger/money.py). Pydantic models are
used so that ingestion of external / malformed data fails loudly rather than
silently producing a wrong ledger.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class OrderStatus(str, Enum):
    CREATED = "created"
    PAID = "paid"
    ATTEMPTED = "attempted"


class PaymentStatus(str, Enum):
    CAPTURED = "captured"
    AUTHORIZED = "authorized"
    FAILED = "failed"
    REFUNDED = "refunded"


class RefundStatus(str, Enum):
    PROCESSED = "processed"
    PENDING = "pending"
    FAILED = "failed"


class SettlementStatus(str, Enum):
    PROCESSED = "processed"
    PENDING = "pending"
    FAILED = "failed"


class CreditDebit(str, Enum):
    CREDIT = "credit"
    DEBIT = "debit"


class _Record(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=False)


class Order(_Record):
    order_id: str
    merchant_id: str
    amount: int                      # paise
    currency: str = "INR"
    created_at: datetime
    status: OrderStatus = OrderStatus.PAID
    customer_reference: str


class Payment(_Record):
    payment_id: str
    order_id: Optional[str]
    amount: int                      # paise, captured amount
    currency: str = "INR"
    status: PaymentStatus = PaymentStatus.CAPTURED
    method: str = "upi"
    captured_at: Optional[datetime]
    fee: int                         # paise, platform fee charged
    tax: int                         # paise, GST on fee
    reference: str


class Refund(_Record):
    refund_id: str
    payment_id: Optional[str]        # may be absent -> "orphan" refund
    amount: int                      # paise
    status: RefundStatus = RefundStatus.PROCESSED
    created_at: datetime
    reference: str


class Settlement(_Record):
    settlement_id: str
    merchant_id: str
    payment_ids: list[str] = Field(default_factory=list)
    gross_amount: int                # paise, sum of captured payments
    fees: int                        # paise
    tax: int                         # paise
    refund_adjustments: int          # paise, positive number that is deducted
    other_adjustments: int = 0       # paise, signed
    net_amount: int                  # paise, as reported by the provider
    settlement_date: datetime
    status: SettlementStatus = SettlementStatus.PROCESSED
    reference: str


class BankEntry(_Record):
    bank_entry_id: str
    amount: int                      # paise, always positive
    credit_or_debit: CreditDebit = CreditDebit.CREDIT
    date: datetime
    reference: str
    description: str = ""


class ExceptionType(str, Enum):
    MISSING_SETTLEMENT = "EXCEPTION_MISSING_SETTLEMENT"
    DUPLICATE_RECORD = "EXCEPTION_DUPLICATE_RECORD"
    FEE_MISMATCH = "EXCEPTION_FEE_MISMATCH"
    UNEXPLAINED_SHORTFALL = "EXCEPTION_UNEXPLAINED_SHORTFALL"
    DELAYED_SETTLEMENT = "EXCEPTION_DELAYED_SETTLEMENT"
    BANK_MISMATCH = "EXCEPTION_BANK_MISMATCH"
    AMBIGUOUS_REFERENCE = "EXCEPTION_AMBIGUOUS_REFERENCE"


class ExceptionStatus(str, Enum):
    OPEN = "OPEN"
    AUTO_RESOLVED = "AUTO_RESOLVED"
    RECOMMEND_REVIEW = "RECOMMEND_REVIEW"
    HUMAN_REVIEW_REQUIRED = "HUMAN_REVIEW_REQUIRED"
    UNRESOLVED = "UNRESOLVED"


class Risk(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ReconciliationException(_Record):
    exception_id: str
    lifecycle_id: str
    transaction_ids: list[str]
    exception_type: ExceptionType
    detected_by: str                 # "deterministic_matcher" | "shadow_ledger"
    expected_value: Optional[int]    # paise
    observed_value: Optional[int]    # paise
    difference: Optional[int]        # paise, expected - observed
    evidence: dict = Field(default_factory=dict)
    status: ExceptionStatus = ExceptionStatus.OPEN
    risk: Risk = Risk.MEDIUM
    resolution: Optional[str] = None
... [3410 more characters in transcript.jsonl]
```

**Bash:**
```
cat ledgerguard/ledger/shadow_ledger.py; echo ----; cat ledgerguard/ledger/invariants.py
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
... [10497 more characters in transcript.jsonl]
```

**Agent:** The core logic is in `matcher.py` and `shadow_ledger.py`. Before designing, I need every place that reads settlements, since "every settlement-matching step" may include code outside the matcher.

**Bash:**
```
grep -rn "settlement" --include=*.py ledgerguard | grep -v "tests/" | grep -iv "settlement_id\b" | grep -n "" | head -150; echo ----; grep -rn "settlements_for\|settlements_by_payment\|SettlementStatus\|\.status" --include=*.py ledgerguard | grep -v tests/
```

**Result:**
```
(eval):1: no matches found: --include=*.py
----
(eval):1: no matches found: --include=*.py
```

**Bash:**
```
grep -rn "settlements_for\|settlements_by_payment\|SettlementStatus\|settlements\b" --include=*.py ledgerguard | grep -v "tests/" ; echo ----; grep -rn "SettlementStatus\|status=\|\.status\b" --include=*.py ledgerguard | grep -v tests/ | grep -i "settl\|pending\|failed"
```

**Result:**
```
(eval):1: no matches found: --include=*.py
----
(eval):1: no matches found: --include=*.py
```

**Bash:**
```
grep -rn "settlements_for\|settlements_by_payment\|SettlementStatus\|settlements" ledgerguard --include='*.py' | grep -v "ledgerguard/tests/"; echo ----; grep -rn "pending\|failed\|PENDING\|FAILED" ledgerguard --include='*.py' | grep -v "ledgerguard/tests/"
```

**Result:**
```
ledgerguard/qa.py:112:def _missing_settlements(report: RunReport) -> tuple[str, list[str]]:
ledgerguard/qa.py:144:    _Query("missing_settlements", ("missing settlement", "never settled", "not settled"),
ledgerguard/qa.py:145:           "payments with no settlement", _missing_settlements),
ledgerguard/reconciliation/matcher.py:121:    and settlements are grouped by id and then split by signature; bank entries
ledgerguard/reconciliation/matcher.py:130:        batch.settlements, lambda s: s.settlement_id, _settlement_signature
ledgerguard/reconciliation/matcher.py:196:    settlements = ledger.settlements_for(payment.payment_id)
ledgerguard/reconciliation/matcher.py:241:            settlements[0] if settlements else None,
ledgerguard/reconciliation/matcher.py:256:            settlements[0] if settlements else None,
ledgerguard/reconciliation/matcher.py:261:    if not settlements:
ledgerguard/reconciliation/matcher.py:276:    if len(settlements) > 1:
ledgerguard/reconciliation/matcher.py:280:        signatures = {_settlement_signature(s) for s in settlements}
ledgerguard/reconciliation/matcher.py:282:            s.settlement_id in duplicates.settlement_conflicts for s in settlements
ledgerguard/reconciliation/matcher.py:286:                "multiple settlements reference the same payment with conflicting content"
ledgerguard/reconciliation/matcher.py:288:                else "multiple settlements reference the same payment"
ledgerguard/reconciliation/matcher.py:290:            "settlement_ids": [s.settlement_id for s in settlements],
ledgerguard/reconciliation/matcher.py:297:            sum(s.net_amount for s in settlements),
ledgerguard/reconciliation/matcher.py:299:            settlements[0],
ledgerguard/reconciliation/matcher.py:303:    settlement = settlements[0]
ledgerguard/ledger/shadow_ledger.py:77:    settlements_by_payment: dict[str, list[Settlement]] = field(default_factory=dict)
ledgerguard/ledger/shadow_ledger.py:95:        for s in self.batch.settlements:
ledgerguard/ledger/shadow_ledger.py:97:                self.settlements_by_payment.setdefault(pid, []).append(s)
ledgerguard/ledger/shadow_ledger.py:162:    def settlements_for(self, payment_id: str) -> list[Settlement]:
ledgerguard/ledger/shadow_ledger.py:163:        return self.settlements_by_payment.get(payment_id, [])
ledgerguard/ledger/shadow_ledger.py:192:            "settlements": len(self.batch.settlements),
ledgerguard/ledger/models.py:36:class SettlementStatus(str, Enum):
ledgerguard/ledger/models.py:94:    status: SettlementStatus = SettlementStatus.PROCESSED
ledgerguard/ledger/models.py:152:    settlements: list[Settlement] = Field(default_factory=list)
ledgerguard/synthetic/adversarial.py:123:        settlements=[a_settlement, b_settlement],
ledgerguard/synthetic/generator.py:28:    SettlementStatus,
ledgerguard/synthetic/generator.py:109:            b.settlements += s
ledgerguard/synthetic/generator.py:208:            status=SettlementStatus.PROCESSED,
ledgerguard/synthetic/compound.py:115:    orders, payments, refunds, settlements, entries = [], [], [], [], []
ledgerguard/synthetic/compound.py:123:            settlements.append(s)
ledgerguard/synthetic/compound.py:199:            settlements=settlements,
ledgerguard/evaluation/ablation.py:173:        settlements = ledger.settlements_for(payment.payment_id)
ledgerguard/evaluation/ablation.py:174:        if not settlements:
ledgerguard/evaluation/ablation.py:177:        settlement = settlements[0]
ledgerguard/evaluation/ablation.py:201:    settlements = ledger.settlements_for(payment.payment_id)
ledgerguard/evaluation/ablation.py:202:    settlement = settlements[0] if settlements else None
ledgerguard/evaluation/ablation.py:230:        "settlements": [
ledgerguard/evaluation/ablation.py:240:            for s in settlements
ledgerguard/evaluation/ablation.py:296:        settlements = ledger.settlements_for(payment.payment_id)
ledgerguard/evaluation/ablation.py:297:        exposure = payment.amount if not 
... [3235 more characters in transcript.jsonl]
```

**Agent:** The only writers of `settlements_for` are the matcher and `evaluation/ablation.py`. Next I'll read the controller, the existing tests, and the frozen holdout's settlement statuses. I'll also snapshot the output directories so I can prove later that they're unchanged.

**Bash:**
```
mkdir -p ../tmp ../out && cp -R ledgerguard/evaluation/outputs ../tmp/outputs_orig && cp -R ledgerguard/evaluation/frozen ../tmp/frozen_orig && find ledgerguard/evaluation/outputs ledgerguard/evaluation/frozen -type f -exec shasum -a 256 {} \; | sort > ../tmp/checksums_before.txt && cat ../tmp/checksums_before.txt | wc -l; cd ledgerguard/evaluation/frozen && .././../../.venv/bin/python -I -c "
import json,collections
d=json.load(open('holdout_20260905_320.json'))
print(type(d), list(d.keys())[:20] if isinstance(d,dict) else len(d))
" ; cd ../../..; grep -o '"status": *"[a-z_]*"' ledgerguard/evaluation/frozen/holdout_20260905_320.json | sort | uniq -c
```

**Result:**
```
      21
<class 'dict'> ['seed', 'count', 'generator_version', 'holdout_lifecycle_ids', 'holdout_batch_sha256']
```

**Agent:** The holdout file stores only seeds and IDs, and the generator only emits `PROCESSED` settlements, so the benchmark batches contain no non-processed settlements. Now the controller and the test conventions.

**Bash:**
```
cat ledgerguard/pipeline.py | head -300; echo ----; grep -n "MISSING\|DETERMINISTICALLY\|NEEDS_INV\|auto\|AUTO" ledgerguard/pipeline.py ledgerguard/ai/*.py ledgerguard/evidence/*.py | head -60
```

**Result:**
```
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
    outcomes: list[CaseOutcome] = field(default_factory=list)
    ledger: ShadowLedger | None = None
    wall_seconds: float = 0.0
    investigations: int = 0
    model_calls: int = 0
    investigation_latencies_ms: list[float] = field(default_factory=list)

    def by_case_id(self) -> dict[str, CaseOutcome]:
        return {o.case_id: o for o in self.outcomes}


def _accept_without_proof(case: CaseResult, result: InvestigationResult) -> VerificationOutcome:
    """The ablation stand-in for the Evidence Gate: believe the investigator.

    Used only by the ablation study, to measure what the gate is actually
    preventing. It records zero checks, so nothing about it can be mistaken for
    verification after the fact.
    """
    from .evidence.verifier import UNVERIFIED, VERIFIED

    trusted = result.hypothesis != "insufficient_evidence" and result.source in (
        "model",
        "heuristic_stub",
    )
    return VerificationOutcome(
        case_id=case.case_id,
        hypothesis=result.hypothesis,
        verdict=VERIFIED if trusted else UNVERIFIED,
        checks=[],
        claimed_evidence_ids=list(result.candidate_evidence_ids),
        note="ABLATION: Evidence Gate disabled; the investigator was taken at its word",
    )


def run(
    batch: Batch,
    use_ai: bool = True,
    provider: InvestigatorProvider | None = None,
    lifecycle_by_payment: dict[str, str] | None = None,
    use_evidence_gate: bool = True,
) -> RunReport:
    started = time.perf_counter()
    cases, ledger = reconcile_batch(batch, lifecycle_by_payment)

    if use_ai:
        provider = provider or get_provider()
    else:
        provider = UnavailableProvider("rules-only baseline: AI investigation disabled")

    outcomes: list[CaseOutcome] = []
    verifications: dict[str, VerificationOutcome] = {}
    investigations = 0
    model_calls = 0
    latencies: list[float] = []

    for case in cases:
        if not case.is_exception:
            outcomes.append(CaseOutcome(case=case))
            continue

        inv: Investigation | None = None
        ver: VerificationOutcome | None = None

        if should_investigate(case):
            if use_ai:
                inv = investigate_case(ledger, case, provider)
                investigations += 1
                m
... [4682 more characters in transcript.jsonl]
```

**Bash:**
```
cat ledgerguard/evidence/safety.py; echo ----; sed -n 1,60p ledgerguard/ai/investigator.py
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
... [8770 more characters in transcript.jsonl]
```

**Agent:** The controller already routes `MISSING_SETTLEMENT` to human review and never to the investigator, so that path needs no change. Next I'll run the existing test suite to get a baseline.

**Bash:**
```
cat run_demo.sh; cd <attempt>/work/repo && timeout 900 .venv/bin/python -m pytest -q ledgerguard/tests 2>&1 | tail -30
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
(eval):1: command not found: timeout
```

**Bash:**
```
.venv/bin/python -m pytest -q ledgerguard/tests 2>&1 | tail -30
```

**Result:**
```
...................................................................      [100%]
=============================== warnings summary ===============================
.venv/lib/python3.14/site-packages/fastapi/testclient.py:1
  <attempt>/work/repo/.venv/lib/python3.14/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
67 passed, 1 warning in 5.22s
```

**Agent:** Baseline is 67 passing. Next I'll look at how existing tests build batches so the new tests match their style.

**Bash:**
```
sed -n 1,120p ledgerguard/tests/test_p0_core.py; echo ----; grep -n "^def \|MISSING" ledgerguard/tests/*.py | head -120
```

**Result:**
```
"""The five core P0 tests.

Each one protects something that would otherwise break silently:

1. financial arithmetic is exact
2. the Shadow Ledger invariant separates a good lifecycle from a corrupted one
3. the Evidence Gate accepts a correctly linked refund
4. the Evidence Gate rejects a refund that matches on amount but belongs to
   a different payment  (the adversarial case)
5. insufficient evidence produces abstention, never a forced auto resolution
"""

from __future__ import annotations

from datetime import datetime, timedelta

import pytest

from ledgerguard.ledger.invariants import (
    check_all,
    fees_and_tax_match_schedule,
    net_matches_shadow_ledger,
    settlement_arithmetic_consistent,
)
from ledgerguard.ledger.models import (
    BankEntry,
    Batch,
    CreditDebit,
    Order,
    Payment,
    Refund,
    Settlement,
)
from ledgerguard.ledger.money import gst_on_fee, platform_fee, to_paise, to_rupees_str
from ledgerguard.ledger.shadow_ledger import ShadowLedger

T0 = datetime(2026, 6, 10, 10, 0, 0)


# --------------------------------------------------------------------------- 1
def test_1_financial_arithmetic_is_exact():
    """A known example must produce the exact expected result, in paise.

    Order of INR 1,234.56, 2% platform fee, 18% GST on the fee, partial
    refund of INR 300.00.

        gross   123456 paise
        fee       2469 paise   (123456 * 0.02 = 2469.12 -> 2469)
        tax        444 paise   (2469 * 0.18 = 444.42   -> 444)
        refund   30000 paise
        net      90543 paise
    """
    gross = to_paise("1234.56")
    assert gross == 123456

    fee = platform_fee(gross)
    tax = gst_on_fee(fee)
    assert fee == 2469, f"fee drifted: {fee}"
    assert tax == 444, f"tax drifted: {tax}"

    refund = to_paise("300.00")
    net = gross - fee - tax - refund
    assert net == 90543
    assert to_rupees_str(net) == "905.43"

    # Everything stays an exact integer; no float ever touches the money path.
    for value in (gross, fee, tax, refund, net):
        assert isinstance(value, int)

    # Half-up rounding at the paise boundary, not banker's rounding.
    assert platform_fee(25) == 1          # 0.50 -> 1
    assert platform_fee(75) == 2          # 1.50 -> 2


def _lifecycle(amount: int = 500000, refund_amount: int | None = None):
    """A single, fully consistent lifecycle built by hand."""
    order = Order(
        order_id="ord_TEST01",
        merchant_id="mch_TEST",
        amount=amount,
        created_at=T0,
        customer_reference="CUST-0001",
    )
    fee = platform_fee(amount)
    tax = gst_on_fee(fee)
    payment = Payment(
        payment_id="pay_TEST01",
        order_id=order.order_id,
        amount=amount,
        captured_at=T0 + timedelta(minutes=3),
        fee=fee,
        tax=tax,
        reference=f"PAY/{order.order_id}",
    )
    refunds = []
    if refund_amount:
        refunds.append(
            Refund(
                refund_id="rfnd_TEST01",
                payment_id=payment.payment_id,
                amount=refund_amount,
                created_at=T0 + timedelta(days=1),
                reference=f"RFND/{order.order_id}",
            )
        )
    refund_total = sum(r.amount for r in refunds)
    net = amount - fee - tax - refund_total
    settled_on = payment.captured_at + timedelta(days=2)
    settlement = Settlement(
        settlement_id="setl_TEST01",
        merchant_id=order.merchant_id,
        payment_ids=[payment.payment_id],
        gross_amount=amount,
        fees=fee,
        tax=tax,
        refund_adjustments=refund_total,
        other_adjustments=0,
        net_amount=net,
        settlement_date=settled_on,
        reference="STL/setl_TEST01",
----
ledgerguard/tests/test_dashboard_startup.py:11:def test_concurrent_dashboard_requests_share_one_initialization(monkeypatch):
ledgerguard/tests/test_fallback.py:15:def _success(model: str = "served-model") -> InvestigationResult:
ledgerguard/tests/test_fallback.py:49:de
... [7409 more characters in transcript.jsonl]
```

**Bash:**
```
sed -n 120,175p ledgerguard/tests/test_p1_extended.py; echo ----; sed -n 1,30p ledgerguard/tests/test_p1_extended.py; echo ----; sed -n 80,100p ledgerguard/tests/test_p1_compound.py; echo ----; sed -n 120,140p ledgerguard/tests/test_p0_core.py
```

**Result:**
```
    )

    dup = find_duplicates(tampered)
    assert clean.payment_id in dup.payment_conflicts
    assert clean.payment_id not in dup.payment_ids, "a conflict is not a duplicate"

    outcome = next(
        o for o in run(tampered, use_ai=False).outcomes
        if o.case.payment_id == clean.payment_id
    )
    assert outcome.state == HUMAN_REVIEW_REQUIRED
    assert outcome.decision.missing_evidence, "the human must be told what is missing"
    assert "disagree on content" in outcome.decision.reason

    # An exact re-ingestion of the same row is still provable, and still closes.
    exact = batch.model_copy(update={"payments": list(batch.payments) + [clean]})
    dup_exact = find_duplicates(exact)
    assert clean.payment_id in dup_exact.payment_ids
    assert not dup_exact.payment_conflicts
    closed = next(
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


# --------------------------------------------------------- delayed settlement
def test_delayed_settlement_is_timing_only_and_never_an_amount_exception():
    dataset = build_dataset()
    results, _ = reconcile_batch(dataset.batch(), dataset.lifecycle_by_payment())
    delayed = _cases_by_fault(dataset, results)[FaultClass.F5_DELAYED_SETTLEMENT]
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
----

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
    # The whole captured net is exposed, not the captured amount less the refund.
    assert outcome.exposure_paise == outcome.case.expected.net_amount
----
        reference="STL/setl_TEST01",
    )
    bank = BankEntry(
        bank_entry_id="bnk_TEST01",
        amount=net,
        cred
... [461 more characters in transcript.jsonl]
```

**Agent:** I have what I need to design this. The plan:

- **`shadow_ledger.py`**: index only `processed` settlements for `settlements_for`, which is what the matcher and the ablation read. Keep the non-processed ones in a separate index so the evidence key can see them.
- **`matcher.py`**: drop non-processed settlements from the duplicate pre-pass, and add `non_processed_settlements` evidence only to the missing-settlement exception.

I'll start with the Shadow Ledger index.

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

**Edit:**
```
<attempt>/work/repo/ledgerguard/ledger/shadow_ledger.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/ledger/shadow_ledger.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

**Agent:** Now the matcher: the duplicate pre-pass should only see processed settlements, and the missing-settlement branch should report the non-processed ones.

**Edit:**
```
<attempt>/work/repo/ledgerguard/reconciliation/matcher.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/reconciliation/matcher.py has been updated successfully.
```

**Edit:**
```
<attempt>/work/repo/ledgerguard/reconciliation/matcher.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/reconciliation/matcher.py has been updated successfully.
```

**Edit:**
```
<attempt>/work/repo/ledgerguard/reconciliation/matcher.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/reconciliation/matcher.py has been updated successfully.
```

**Agent:** Next I'll run the existing suite against the change, and check whether the benchmark can write somewhere other than `outputs/`.

**Bash:**
```
.venv/bin/python -m pytest -q ledgerguard/tests 2>&1 | tail -3; grep -n "outputs\|OUT\|def main\|argv\|argparse" ledgerguard/evaluation/benchmark.py | head -30
```

**Result:**
```
-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
67 passed, 1 warning in 4.78s
7:same frozen holdout, and writes every artifact under evaluation/outputs/.
20:import argparse
36:OUTPUT_DIR = Path(__file__).parent / "outputs"
67:                "FROZEN HOLDOUT MISMATCH.\n"
238:def main(argv: list[str] | None = None) -> int:
239:    parser = argparse.ArgumentParser(description="LedgerGuard benchmark")
252:    args = parser.parse_args(argv)
254:    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
277:    (OUTPUT_DIR / "benchmark.md").write_text(md)
278:    (OUTPUT_DIR / "benchmark.json").write_text(
301:        hybrid_report, scored, OUTPUT_DIR / "unresolved_exceptions.csv"
303:    export_cases(hybrid_report, scored, OUTPUT_DIR / "cases.json")
337:    print(f"\nArtifacts written to {OUTPUT_DIR}")
344:            "or OMNIROUTE_API_KEY) and rerun to measure against a real investigator."
```

**Agent:** The benchmark writes to a fixed `outputs/` path, so I won't run it in the repo. I'll check it in a scratch copy later. Before writing tests, I need the provider interface so I can assert the investigator is never called.

**Bash:**
```
grep -n "class \|def " ledgerguard/ai/provider.py | head -60; sed -n 298,316p ledgerguard/tests/test_p1_extended.py
```

**Result:**
```
29:def _load_dotenv() -> None:
72:class InvestigatorProvider(Protocol):
75:    def investigate(self, context: dict) -> InvestigationResult:  # pragma: no cover
79:def _to_result(out: InvestigatorOutput, source: str, model_name: str | None) -> InvestigationResult:
91:class AnthropicProvider:
94:    def __init__(
109:    def investigate(self, context: dict) -> InvestigationResult:
140:class HeuristicProvider:
150:    def investigate(self, context: dict) -> InvestigationResult:
211:class UnavailableProvider:
216:    def __init__(self, error: str = "no investigator provider is configured") -> None:
219:    def investigate(self, context: dict) -> InvestigationResult:
240:def _build(kind: str) -> InvestigatorProvider:
279:def build_chain(order: list[str] | None = None) -> list[InvestigatorProvider]:
313:def get_provider(kind: str | None = None) -> InvestigatorProvider:
def _stub_provider(exc: Exception):
    from ledgerguard.ai.openai_compatible import OpenAICompatibleProvider

    provider = OpenAICompatibleProvider(
        preset="openai_compatible",
        models=["stub-model"],
        api_key="k",
        base_url="http://stub.invalid/v1",
    )
    provider.max_retries = 0                 # keep the test instant

    class _Boom:
        def post(self, *a, **kw):
            raise exc

    provider._client = _Boom()
    return provider
```

**Agent:** I have the provider protocol. Now I'll write the new test file. It covers each numbered requirement, plus regressions for the duplicate path and the controller.

**Write:**
```
<attempt>/work/repo/ledgerguard/tests/test_settlement_status.py
```

**Result:**
```
File created successfully at: <attempt>/work/repo/ledgerguard/tests/test_settlement_status.py (file state is current in your context — no need to Read it back)
```

**Agent:** Before running, I'll tidy one test where I constructed the processed settlement's net twice, then run the new file.

**Edit:**
```
<attempt>/work/repo/ledgerguard/tests/test_settlement_status.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/tests/test_settlement_status.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

**Edit:**
```
<attempt>/work/repo/ledgerguard/tests/test_settlement_status.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/tests/test_settlement_status.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

**Bash:**
```
.venv/bin/python -m pytest -q ledgerguard/tests/test_settlement_status.py 2>&1 | tail -60; .venv/bin/python -m pytest -q ledgerguard/tests 2>&1 | tail -2
```

**Result:**
```
...............                                                          [100%]
15 passed in 0.11s
-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
82 passed, 1 warning in 4.67s
```

**Agent:** All 82 pass: the 67 originals plus 15 new. Next I'll confirm the benchmark is unchanged. I'll run it in a scratch copy so the repo's `outputs/` stays untouched, then diff against the original artifacts.

**Bash:**
```
rm -rf ../tmp/repo_check && mkdir -p ../tmp/repo_check && cp -R ledgerguard ../tmp/repo_check/ && cd ../tmp/repo_check && <attempt>/work/repo/.venv/bin/python -m ledgerguard.evaluation.benchmark > ../bench_stdout.txt 2>&1; echo exit=$?; tail -5 ../bench_stdout.txt; for f in benchmark.json benchmark.md cases.json unresolved_exceptions.csv; do cmp -s ledgerguard/evaluation/outputs/$f <attempt>/work/repo/ledgerguard/evaluation/outputs/$f && echo "same $f" || echo "DIFF $f"; done
```

**Result:**
```
exit=0
Artifacts written to <attempt>/work/tmp/repo_check/ledgerguard/evaluation/outputs
  benchmark.md, benchmark.json, cases.json
  unresolved_exceptions.csv (10 rows)

NOTE: the hybrid run used the offline heuristic stub, not a model. Configure a provider key (GROQ_API_KEY, GEMINI_API_KEY, NVIDIA_API_KEY or OMNIROUTE_API_KEY) and rerun to measure against a real investigator.
DIFF benchmark.json
DIFF benchmark.md
DIFF cases.json
DIFF unresolved_exceptions.csv
Shell cwd was reset to <attempt>/work/repo
```

**Agent:** The benchmark artifacts differ. This may just be timing fields, but I need to check before accepting it, so I'll look at the actual differences.

**Bash:**
```
cd <attempt>/work; diff tmp/repo_check/ledgerguard/evaluation/outputs/benchmark.json repo/ledgerguard/evaluation/outputs/benchmark.json | head -40; echo ----; diff tmp/repo_check/ledgerguard/evaluation/outputs/cases.json repo/ledgerguard/evaluation/outputs/cases.json | head -20; echo ----; diff tmp/repo_check/ledgerguard/evaluation/outputs/unresolved_exceptions.csv repo/ledgerguard/evaluation/outputs/unresolved_exceptions.csv | head; echo ----; diff tmp/repo_check/ledgerguard/evaluation/outputs/benchmark.md repo/ledgerguard/evaluation/outputs/benchmark.md | head -30
```

**Result:**
```
128,129c128,129
<     "wall_seconds": 0.003,
<     "throughput_per_second": 25172.1,
---
>     "wall_seconds": 0.004,
>     "throughput_per_second": 22395.4,
193c193
<     "provider": "heuristic_stub",
---
>     "provider": "fallback(groq->gemini->nvidia->omniroute)",
204,207c204,207
<     "disposition_correct": 85,
<     "accuracy": 1.0,
<     "auto_resolved": 21,
<     "exceptions_correctly_resolved": 21,
---
>     "disposition_correct": 83,
>     "accuracy": 0.9765,
>     "auto_resolved": 19,
>     "exceptions_correctly_resolved": 19,
210c210
<     "human_review_required": 10,
---
>     "human_review_required": 12,
213c213
<     "unnecessary_abstentions": 0,
---
>     "unnecessary_abstentions": 2,
215,217c215,217
<     "unresolved_value_paise": 12189954,
<     "wall_seconds": 0.004,
<     "throughput_per_second": 22259.3,
---
>     "unresolved_value_paise": 13590189,
>     "wall_seconds": 121.704,
>     "throughput_per_second": 0.7,
219,220c219,220
<     "model_calls": 0,
<     "model_calls_per_100_records": 0.0,
---
----
373,375c373,375
<       "hypothesis": "unlinked_partial_refund",
<       "reason": "Refund rfnd_01952574 is for 698810 paise, exactly the unexplained shortfall, and carries no payment linkage. It most likely belongs to this payment and lost its link during ingestion.",
<       "recommended_action": "resolve",
---
>       "hypothesis": "insufficient_evidence",
>       "reason": "The settlement shows a refund adjustment of 698,810 paise, which exactly matches the observed shortfall. A candidate refund record (rfnd_01952574) of the same amount exists, but it is not linked to the payment (payment_id is null) and no explicit linkage evidence is present in the provided records. Without proof that this refund is associated with pay_00121298, we cannot confirm the unlinked partial refund explanation.",
>       "recommended_action": "review",
379,382c379,381
<       "source": "heuristic_stub",
<       "model_name": null,
<       "latency_ms": 0.02,
<       "controller_note": null
---
>       "source": "model",
>       "model_name": "openai/gpt-oss-120b",
>       "latency_ms": 1483.35
386,435c385,389
<       "hypothesis": "unlinked_partial_refund",
<       "verdict": "REJECTED",
----
2c2
< pay_00121298,LC0012,EXCEPTION_UNEXPLAINED_SHORTFALL,HUMAN_REVIEW_REQUIRED,pay_00121298 ord_00123197 setl_0012D881,6988.10,E1_evidence_records_exist; E2_refund_is_processed; E3_refund_not_linked_elsewhere; E5_amount_equals_shortfall; E7_invariant_restored,E4_reference_identifies_this_customer; E6_timing_is_plausible,Evidence Gate rejected the hypothesis 'unlinked_partial_refund': refund reference 'ADJ/CUST-0007/partial' vs order customer 'CUST-0072' -> NO MATCH,Do not net this against the proposed refund. Identify the true counterparty of the deduction with the provider before closing.
---
> pay_00121298,LC0012,EXCEPTION_UNEXPLAINED_SHORTFALL,HUMAN_REVIEW_REQUIRED,pay_00121298 ord_00123197 setl_0012D881,6988.10,,no hypothesis was proposed,"The investigator found no explanation it could support from the available records: The settlement shows a refund adjustment of 698,810 paise, which exactly matches the observed shortfall. A candidate refund record (rfnd_01952574) of the same amount exists, but it is not linked to the payment (payment_id is null) and no explicit linkage evidence is present in the provided records. Without proof that this refund is associated with pay_00121298, we cannot confirm the unlinked partial refund explanation.","Obtain the missing record from the provider, or confirm the deduction manually before closing."
3a4
> pay_003478CC,LC0034,EXCEPTION_UNEXPLAINED_SHORTFALL,HUMAN_REVIEW_REQUIRED,pay_003478CC ord_0034877E setl_0034CA22,12726.70,,no hypothesis was proposed,"The investigator found no explanation it could support from the available records: The observed shortfall (1,272,670 paise) matches the amount of an unlinked refund (rfnd_003431D5), suggesting a possible unlinked_partial_refund. However, the recor
... [2040 more characters in transcript.jsonl]
```

**Agent:** The differences come from the investigator, not my change. The original artifacts were produced with a live model (`fallback(groq->...)`), and this environment has no keys, so the scratch run used the offline heuristic stub. The provider-independent parts are what I can compare directly. I'll check that the holdout batches contain no non-processed settlements, and that the rules-only baseline matches the original.

**Bash:**
```
cd <attempt>/work/tmp/repo_check && <attempt>/work/repo/.venv/bin/python -c "
import json,collections
from ledgerguard.synthetic.generator import *
import ledgerguard.evaluation.benchmark as b
import inspect
print([n for n in dir(b) if 'holdout' in n.lower() or 'dataset' in n.lower()])
" 2>&1 | tail -5; cd ../../repo && .venv/bin/python -c "
import json
a=json.load(open('<attempt>/work/repo/ledgerguard/evaluation/outputs/benchmark.json'))
b=json.load(open('<attempt>/work/tmp/repo_check/ledgerguard/evaluation/outputs/benchmark.json'))
print(list(a.keys()))
for k in a:
    print(k, 'SAME' if a[k]==b.get(k) else 'DIFF')
print(json.dumps(a.get('baseline',{}))[:600])
print(json.dumps(b.get('baseline',{}))[:600])
"
```

**Result:**
```
['Dataset', 'build_dataset', 'freeze_or_verify_holdout']
['dataset', 'holdout_manifest', 'baseline', 'hybrid', 'investigator_chain']
dataset SAME
holdout_manifest SAME
baseline DIFF
hybrid DIFF
investigator_chain DIFF
{"system": "Rules only (baseline)", "provider": "none", "false_auto_resolutions": 0, "false_auto_resolved_value_paise": 0, "total_cases": 85, "total_value_paise": 249335700, "matched": 54, "exceptions": 31, "match_rate": 0.6353, "false_exceptions": 0, "missed_faults": 0, "exception_type_correct": 31, "disposition_correct": 76, "accuracy": 0.8941, "auto_resolved": 12, "exceptions_correctly_resolved": 12, "exceptions_incorrectly_resolved": 0, "recommend_review": 0, "human_review_required": 19, "unresolved": 0, "correct_abstentions": 10, "unnecessary_abstentions": 9, "exception_value_paise": 3642
{"system": "Rules only (baseline)", "provider": "none", "false_auto_resolutions": 0, "false_auto_resolved_value_paise": 0, "total_cases": 85, "total_value_paise": 249335700, "matched": 54, "exceptions": 31, "match_rate": 0.6353, "false_exceptions": 0, "missed_faults": 0, "exception_type_correct": 31, "disposition_correct": 76, "accuracy": 0.8941, "auto_resolved": 12, "exceptions_correctly_resolved": 12, "exceptions_incorrectly_resolved": 0, "recommend_review": 0, "human_review_required": 19, "unresolved": 0, "correct_abstentions": 10, "unnecessary_abstentions": 9, "exception_value_paise": 3642
```

**Agent:** The `dataset` and `holdout_manifest` sections match exactly. The rules-only baseline differs only in what I need to strip out. I'll confirm the difference is timing-only, and count settlement statuses directly in the regenerated holdout batch.

**Bash:**
```
cd <attempt>/work/tmp/repo_check && grep -n "def build_dataset\|def split\|def freeze_or_verify_holdout\|def holdout" ledgerguard/evaluation/benchmark.py ledgerguard/synthetic/*.py | head; <attempt>/work/repo/.venv/bin/python -c "
import json, collections
from ledgerguard.evaluation.benchmark import build_dataset
from ledgerguard.ledger.models import SettlementStatus
ds = build_dataset()
print(type(ds))
_, holdout = __import__('ledgerguard.synthetic.generator', fromlist=['split']).split(ds) if False else (None, None)
b = ds.batch()
print('all settlements:', collections.Counter(s.status.value for s in b.settlements))
" 2>&1 | tail -5
```

**Result:**
```
ledgerguard/evaluation/benchmark.py:53:def freeze_or_verify_holdout(holdout: Dataset, seed: int, count: int) -> dict:
ledgerguard/synthetic/fault_injector.py:202:def build_dataset(seed: int = 20260905, count: int = 320) -> Dataset:
ledgerguard/synthetic/fault_injector.py:267:def split(dataset: Dataset, holdout_fraction: float = 0.25) -> tuple[Dataset, Dataset]:
<class 'ledgerguard.synthetic.generator.Dataset'>
all settlements: Counter({'processed': 305})
Shell cwd was reset to <attempt>/work/repo
```

**Agent:** All 305 settlements in the generated dataset are `processed`, so the holdout cannot exercise the new branches. Last, I'll confirm the rules-only baseline is identical apart from timing fields.

**Bash:**
```
.venv/bin/python -c "
import json
a=json.load(open('ledgerguard/evaluation/outputs/benchmark.json'))
b=json.load(open('../tmp/repo_check/ledgerguard/evaluation/outputs/benchmark.json'))
def strip(d):
    return {k:v for k,v in d.items() if 'wall' not in k and 'throughput' not in k and 'latenc' not in k}
print('baseline equal (ignoring timing):', strip(a['baseline'])==strip(b['baseline']))
print('dataset equal:', a['dataset']==b['dataset'], 'manifest equal:', a['holdout_manifest']==b['holdout_manifest'])
print('baseline keys diff:', {k for k in a['baseline'] if a['baseline'][k]!=b['baseline'].get(k)})
"
```

**Result:**
```
baseline equal (ignoring timing): True
dataset equal: True manifest equal: True
baseline keys diff: {'wall_seconds', 'throughput_per_second'}
```

**Agent:** The baseline matches apart from timing fields, and the dataset and holdout manifest match exactly. Now I'll confirm the repo's `outputs/` and `frozen/` are byte-identical to the snapshot taken before I started.

**Bash:**
```
find ledgerguard/evaluation/outputs ledgerguard/evaluation/frozen -type f -exec shasum -a 256 {} \; | sort > ../tmp/checksums_after.txt && cmp ../tmp/checksums_before.txt ../tmp/checksums_after.txt && echo "outputs/ and frozen/ UNCHANGED (21 files)"; ls -la | grep -i pytest; find . -name ".pytest_cache" -not -path "./.venv/*"
```

**Result:**
```
outputs/ and frozen/ UNCHANGED (21 files)
drwxr-xr-x@  6 user  staff    192 Nov  1 23:15 .pytest_cache
./.pytest_cache
```

**Agent:** The `.pytest_cache` came from my test runs, so I'll remove it. Then I'll write the notes file.

**Bash:**
```
rm -rf .pytest_cache && cat .gitignore
```

**Result:**
```
.venv/
__pycache__/
*.pyc
.env
.pytest_cache/
.DS_Store
```

**Write:**
```
<attempt>/work/out/NOTES.md
```

**Result:**
```
File created successfully at: <attempt>/work/out/NOTES.md (file state is current in your context — no need to Read it back)
```

**Agent:** Last step: one final full run with the cache provider disabled, so no cache is left behind.

**Bash:**
```
.venv/bin/python -m pytest -q -p no:cacheprovider ledgerguard/tests 2>&1 | tail -2; find ledgerguard/evaluation/outputs ledgerguard/evaluation/frozen -type f -exec shasum -a 256 {} \; | sort | cmp - ../tmp/checksums_before.txt && echo artifacts-unchanged
```

**Result:**
```
-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
82 passed, 1 warning in 4.74s
artifacts-unchanged
```

**Agent:** Reconciliation now ignores `pending` and `failed` settlements, and a payment with no `processed` settlement is reported as `EXCEPTION_MISSING_SETTLEMENT`. All 82 tests pass: the 67 existing ones unchanged, plus 15 new ones in `ledgerguard/tests/test_settlement_status.py`.

**What changed**
- **`ledger/shadow_ledger.py`**: `settlements_for` returns only processed settlements. A new `non_processed_settlements_for` holds pending and failed ones for reporting only.
- **`reconciliation/matcher.py`**:
  - Duplicate detection looks only at processed settlements.
  - A payment with no processed settlement gets `evidence["non_processed_settlements"]` when it has non-processed ones, sorted by `settlement_id`. The key is absent otherwise.
- **Controller**: no change needed. Missing-settlement cases were already escalated to human review and never sent to the investigator, and tests confirm that still holds.

**Choices I made** (also in `../out/NOTES.md`)
- `settlements_for` is processed-only everywhere, so the ablation baseline in `evaluation/ablation.py` follows the same rule. It has no effect on existing batches.
- For payment-level duplicates, the precedence is unchanged. The settlement attached to the case is now the processed one, not a pending one. The duplicate cases do not get the new evidence key.
- The list has one entry per non-processed record, so a repeated pending id appears twice.

**Benchmark and artifacts**
- The generated dataset contains only `processed` settlements, so the holdout cannot reach the new branches. The dataset and holdout manifest match the original exactly.
- The rules-only baseline matches apart from timing fields.
- **Not confirmed:** the hybrid benchmark section. The shipped artifacts were produced with a live model, and this environment has no provider key, so a re-run used the offline stub and gave different hybrid numbers. The investigator explains those differences, not this change, but I could not verify the hybrid numbers here.
- I ran the benchmark in a scratch copy, not the repo. All 21 files under `evaluation/outputs/` and `evaluation/frozen/` match their pre-task checksums.
