# M-T2-01 transcript (PASS)

**Agent:** I'll start with the handover documentation at the repository root, then the reconciliation code.

**Bash:**
```
ls -la && find . -path ./.venv -prune -o -type f -print | grep -v __pycache__ | grep -v '\.git/' | head -200
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
cat README.md | head -400; echo ----; wc -l docs/*.md; ls ../; ls ../out ../tmp 2>&1
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
... [15809 more characters in transcript.jsonl]
```

**Agent:** This is not a git repo, so I'll snapshot the artifact directories before running anything, to verify them unchanged at the end. Then I'll read the architecture doc and the matcher.

**Bash:**
```
mkdir -p ../tmp/orig && cp -a ledgerguard ../tmp/orig/ && cd ledgerguard && find . -name __pycache__ -prune -o -type f -print | sort > /dev/null; cd ..; (cd ledgerguard/evaluation && shasum -a 256 outputs/* frozen/* > ../../../tmp/orig/artifact_sums.txt); cat ../tmp/orig/artifact_sums.txt | head -30; echo ----; cat docs/architecture.md
```

**Result:**
```
7ffa151674c19541ac0b4cf9a8618b4c5a8eef664afd9ab81321961848cecd03  outputs/ablation.json
fc84418ada9f206e10f07170d5c3e362c531474c13abefed04eadabf32c6cda2  outputs/ablation.md
249e3bce69daeb83386d9575e66bf4177d4db885a8864ab6b32d80b5717d8536  outputs/benchmark.json
aa667ebea4ccd41fa0bdff898182200d3bf282ef0b888cabd7b5a215d82edd22  outputs/benchmark.md
8dc1212f1c93e7c1bf34d92923c1d31f15b7096a0b39e4c2afa4e167f4eda9d4  outputs/calibration.json
bbfc6509ce38c53329da95bde380675d231fcfbb15efd4428252aae3eef32d12  outputs/calibration.md
a5552fcb48631411cb08fae4e34987295cca132334d6c31d86601f73e538455b  outputs/cases.json
c52561e7f550a9c66a045bd6aaebd91f8883f120a624bf773d2a3dfae1753c7d  outputs/decision_log.json
ac427b5c78460109ba2fb3914c2d04310e80089ea245dcf44f426bc2da5562a7  outputs/drift.json
b3ceedf8b7067eb970ee33a6f7802ea154a10aa6fcbabe903b7880a0cd5634dc  outputs/drift.md
3699ea28a60eed7b419b027283ae1a9a3875eeb7c43e674adddfc0d195aa50c1  outputs/evidence_ledger.csv
1fbca2999ea5f5b76d810ac2955beb5fca7bc5af165320a752be60dbe4b96100  outputs/model_comparison.json
b877b4cdb9f9dfc33ff7ad0e82915e3e6fad2b84ccd8e3e9170943758834ff4d  outputs/model_comparison.md
ccc33093b532b19e326ed4ac8f8d16d29645807f3fe97841a10dc7d242f57917  outputs/no_gate_ablation.json
b2aa14f8b312f1a735663b70b69137f2df190ab9ef731c51c31def8d05bd14e4  outputs/no_gate_ablation.md
c58809b7c6b57a77dd33ce948b09988c6c9ded01bacb052b2f4f9b2d5193d6d7  outputs/reconciliation_report.csv
7a9f6520bbeb849b4e6f1f15a78f39a608583c6776c7c310457ed053a82dd41c  outputs/reconciliation_report.md
530301222288c5c487d56e9029f570bd01720e1fdbd306c90b9f71c71488cd4b  outputs/scale.json
227f79916be1cbe13addb7096e2f0f453660e2dc4ef83e4081ff8bcbee2ef9cf  outputs/scale.md
af74f00254d9a8cee944bccdf9fd8940c2a318c0bfd5c6965dbfc5a221e00711  outputs/unresolved_exceptions.csv
06f71351dd21bdcdb30705986832111987fe71ff6d6787ed2a198c88de50a53f  frozen/holdout_20260905_320.json
----
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

### `led
... [10325 more characters in transcript.jsonl]
```

**Bash:**
```
cd ledgerguard && cat reconciliation/matcher.py; echo ----; cat reconciliation/exceptions.py
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
... [14777 more characters in transcript.jsonl]
```

**Agent:** The matcher is clear. Now I need every place that consumes settlements, since the requirement covers all settlement-matching steps.

**Bash:**
```
cd ledgerguard && cat ledger/shadow_ledger.py; echo ----; grep -rn "settlement" --include=*.py . | grep -v tests/ | grep -v "^./ledger/shadow_ledger.py" | grep -v "^./reconciliation/matcher.py" | grep -iv "settlement_date\|settlement_id\b" | head -120; echo ----; grep -n "status" ledger/models.py
```

**Result:**
```
(eval):cd:1: no such file or directory: ledgerguard
----
(eval):1: no matches found: --include=*.py
----
57:    status: OrderStatus = OrderStatus.PAID
66:    status: PaymentStatus = PaymentStatus.CAPTURED
78:    status: RefundStatus = RefundStatus.PROCESSED
94:    status: SettlementStatus = SettlementStatus.PROCESSED
141:    status: ExceptionStatus = ExceptionStatus.OPEN
```

**Bash:**
```
pwd; cat ledger/shadow_ledger.py; echo ----; grep -rn "settlement" *.py */*.py | grep -v "^tests/" | grep -v "^ledger/shadow_ledger.py" | grep -v "^reconciliation/matcher.py" | head -150
```

**Result:**
```
<attempt>/work/repo/ledgerguard
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
        other_adjustments:
... [16223 more characters in transcript.jsonl]
```

**Agent:** Two things stand out: the `settlements_by_payment` index feeds most consumers, and `find_duplicates` reads `batch.settlements` directly, so both need the status filter. Next I'll check the status enum, the pipeline/safety handling of `MISSING_SETTLEMENT`, and whether the frozen holdout contains any non-processed settlements.

**Bash:**
```
sed -n 1,100p ledger/models.py; echo ----; cat pipeline.py | head -150; echo ----; sed -n 1,60p evidence/safety.py; echo; grep -n "MISSING_SETTLEMENT\|def decide" -A6 evidence/safety.py | head -80
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
    
... [6454 more characters in transcript.jsonl]
```

**Agent:** The safety path already escalates `MISSING_SETTLEMENT` without AI, so requirement 7 holds by construction as long as the new case keeps that exception type. Next: whether the generator or holdout ever emits non-processed settlements, and how the existing tests build batches.

**Bash:**
```
grep -rn "SettlementStatus\|status=" synthetic/*.py | head; echo ----; grep -rln "SettlementStatus\|PENDING\|pending" ledgerguard 2>/dev/null; grep -rn "SettlementStatus" tests/ | head; echo ----; grep -o '"status": *"[a-z]*"' evaluation/frozen/holdout_20260905_320.json | sort | uniq -c; echo; ls tests; sed -n 1,60p tests/test_p0_core.py
```

**Result:**
```
synthetic/generator.py:28:    SettlementStatus,
synthetic/generator.py:160:            status=OrderStatus.PAID,
synthetic/generator.py:170:            status=PaymentStatus.CAPTURED,
synthetic/generator.py:187:                    status=RefundStatus.PROCESSED,
synthetic/generator.py:208:            status=SettlementStatus.PROCESSED,
----
----

__init__.py
rehearsal_check.py
test_dashboard_startup.py
test_evidence_download.py
test_fallback.py
test_p0_core.py
test_p1_compound.py
test_p1_extended.py
test_p2_evaluation.py
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
```

**Agent:** The frozen holdout file has no `"status"` pattern match, so I'll check its raw content for non-processed statuses directly, and run the existing test suite to get a baseline.

**Bash:**
```
cd <attempt>/work/repo && grep -c -i '"pending"\|"failed"' ledgerguard/evaluation/frozen/holdout_20260905_320.json; head -c 600 ledgerguard/evaluation/frozen/holdout_20260905_320.json; echo; ls -la ledgerguard/evaluation/frozen/; echo ----; timeout 900 .venv/bin/python -m pytest ledgerguard/tests -q -p no:cacheprovider 2>&1 | tail -15
```

**Result:**
```
0
{
  "seed": 20260905,
  "count": 320,
  "generator_version": "1.0.0",
  "holdout_lifecycle_ids": [
    "LC0001",
    "LC0004",
    "LC0006",
    "LC0007",
    "LC0012",
    "LC0013",
    "LC0017",
    "LC0019",
    "LC0020",
    "LC0024",
    "LC0029",
    "LC0033",
    "LC0034",
    "LC0035",
    "LC0037",
    "LC0048",
    "LC0052",
    "LC0062",
    "LC0068",
    "LC0071",
    "LC0075",
    "LC0079",
    "LC0080",
    "LC0084",
    "LC0091",
    "LC0094",
    "LC0100",
    "LC0101",
    "LC0107",
    "LC0108",
    "LC0109",
    "LC0116",
    "LC0117",
    "LC0118",
    "LC0120",
    "LC0122
total 8
drwxr-xr-x@  3 user  staff    96 Nov  1 23:13 .
drwxr-xr-x@ 17 user  staff   544 Nov  1 23:13 ..
-rw-r--r--@  1 user  staff  1388 Nov  1 23:13 holdout_20260905_320.json
----
(eval):1: command not found: timeout
```

**Bash:**
```
.venv/bin/python -m pytest ledgerguard/tests -q -p no:cacheprovider 2>&1 | tail -15
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

**Agent:** Baseline: 67 tests pass. The generator only ever emits `PROCESSED` settlements, so the holdout is unaffected by construction, and I'll confirm that empirically later. Now I'll find every direct read of `batch.settlements` so none is missed.

**Bash:**
```
grep -rn "\.settlements\b" --include=*.py . | grep -v "\.venv" | grep -v "/tests/"; echo ----; grep -rn "settlements_by_payment\|settlements_for\|bank_entries_for_settlement" --include=*.py . | grep -v .venv
```

**Result:**
```
(eval):1: no matches found: --include=*.py
----
(eval):1: no matches found: --include=*.py
```

**Bash:**
```
grep -rn "\.settlements\b" ledgerguard --include='*.py' | grep -v "/tests/"; echo ----; grep -rn "settlements_by_payment\|settlements_for\|bank_entries_for_settlement" ledgerguard --include='*.py'
```

**Result:**
```
ledgerguard/reconciliation/matcher.py:130:        batch.settlements, lambda s: s.settlement_id, _settlement_signature
ledgerguard/ledger/shadow_ledger.py:95:        for s in self.batch.settlements:
ledgerguard/ledger/shadow_ledger.py:192:            "settlements": len(self.batch.settlements),
ledgerguard/synthetic/generator.py:109:            b.settlements += s
ledgerguard/evaluation/scale.py:58:        + len(batch.settlements) + len(batch.bank_entries)
----
ledgerguard/reconciliation/matcher.py:196:    settlements = ledger.settlements_for(payment.payment_id)
ledgerguard/reconciliation/matcher.py:304:    bank = ledger.bank_entries_for_settlement(settlement)
ledgerguard/ledger/shadow_ledger.py:77:    settlements_by_payment: dict[str, list[Settlement]] = field(default_factory=dict)
ledgerguard/ledger/shadow_ledger.py:97:                self.settlements_by_payment.setdefault(pid, []).append(s)
ledgerguard/ledger/shadow_ledger.py:162:    def settlements_for(self, payment_id: str) -> list[Settlement]:
ledgerguard/ledger/shadow_ledger.py:163:        return self.settlements_by_payment.get(payment_id, [])
ledgerguard/ledger/shadow_ledger.py:165:    def bank_entries_for_settlement(self, settlement: Settlement) -> list[BankEntry]:
ledgerguard/evaluation/ablation.py:173:        settlements = ledger.settlements_for(payment.payment_id)
ledgerguard/evaluation/ablation.py:178:        entries = ledger.bank_entries_for_settlement(settlement)
ledgerguard/evaluation/ablation.py:201:    settlements = ledger.settlements_for(payment.payment_id)
ledgerguard/evaluation/ablation.py:203:    entries = ledger.bank_entries_for_settlement(settlement) if settlement else []
ledgerguard/evaluation/ablation.py:296:        settlements = ledger.settlements_for(payment.payment_id)
```

**Agent:** Only two places read raw settlements: the `ShadowLedger` index and `find_duplicates`. Everything else goes through `settlements_for`. The `totals()` count is informational, not a matching step, so I'll leave it alone. Now the ledger change.

**Edit:**
```
<attempt>/work/repo/ledgerguard/ledger/shadow_ledger.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/ledger/shadow_ledger.py has been updated successfully.
```

**Edit:**
```
<attempt>/work/repo/ledgerguard/ledger/shadow_ledger.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/ledger/shadow_ledger.py has been updated successfully.
```

**Edit:**
```
<attempt>/work/repo/ledgerguard/ledger/shadow_ledger.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/ledger/shadow_ledger.py has been updated successfully.
```

**Edit:**
```
<attempt>/work/repo/ledgerguard/ledger/shadow_ledger.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/ledger/shadow_ledger.py has been updated successfully.
```

**Agent:** Now the matcher: the duplicate pre-pass should see processed settlements only, and the no-processed branch gets the evidence key.

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

**Agent:** Code changes are in. Before writing tests, I want an empirical check that the holdout results are unchanged. I need to see how the benchmark loads the frozen batch so I can run it without writing outputs.

**Bash:**
```
grep -n "def \|frozen\|build_dataset\|sha\|OUTPUT\|write" ledgerguard/evaluation/benchmark.py | head -80
```

**Result:**
```
7:same frozen holdout, and writes every artifact under evaluation/outputs/.
31:from ..synthetic.fault_injector import build_dataset, split
36:OUTPUT_DIR = Path(__file__).parent / "outputs"
37:MANIFEST_DIR = Path(__file__).parent / "frozen"
40:def manifest_path(seed: int, count: int) -> Path:
41:    """One frozen manifest per dataset configuration.
44:    can never silently overwrite the holdout an earlier result was scored on.
49:def batch_digest(dataset: Dataset) -> str:
50:    return hashlib.sha256(dataset.batch().model_dump_json().encode()).hexdigest()
53:def freeze_or_verify_holdout(holdout: Dataset, seed: int, count: int) -> dict:
60:        "holdout_batch_sha256": batch_digest(holdout),
68:                "The holdout for this seed was frozen earlier and the regenerated "
71:                "delete the manifest deliberately and say so in the write-up.\n"
72:                f"  frozen sha256:      {existing.get('holdout_batch_sha256')}\n"
73:                f"  regenerated sha256: {manifest['holdout_batch_sha256']}"
77:    path.write_text(json.dumps(manifest, indent=2) + "\n")
81:def _row(label: str, baseline, hybrid, fmt=str) -> str:
85:def render_markdown(base: Metrics, hyb: Metrics, manifest: dict) -> str:
86:    def inr(paise: int) -> str:
94:        f"batch SHA-256 `{manifest['holdout_batch_sha256'][:16]}`.",
149:def write_unresolved_csv(report: RunReport, dataset: Dataset, path: Path) -> int:
154:        writer = csv.writer(fh)
155:        writer.writerow(
177:            writer.writerow(
195:def export_cases(report: RunReport, dataset: Dataset, path: Path) -> None:
235:    path.write_text(json.dumps(payload, indent=2, default=str) + "\n")
238:def main(argv: list[str] | None = None) -> int:
244:        help="which slice to score (default: the frozen holdout)",
254:    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
256:    full = build_dataset(seed=args.seed, count=args.count)
277:    (OUTPUT_DIR / "benchmark.md").write_text(md)
278:    (OUTPUT_DIR / "benchmark.json").write_text(
287:                    "batch_sha256": batch_digest(scored),
300:    n_unresolved = write_unresolved_csv(
301:        hybrid_report, scored, OUTPUT_DIR / "unresolved_exceptions.csv"
303:    export_cases(hybrid_report, scored, OUTPUT_DIR / "cases.json")
337:    print(f"\nArtifacts written to {OUTPUT_DIR}")
```

**Bash:**
```
sed -n 238,276p ledgerguard/evaluation/benchmark.py; grep -n "def split\|def holdout\|def dev\|class Dataset" -A4 ledgerguard/synthetic/fault_injector.py | head -40
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
    args = parser.parse_args(argv)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    full = build_dataset(seed=args.seed, count=args.count)
    dev, holdout = split(full)
    manifest = freeze_or_verify_holdout(holdout, args.seed, args.count)
    scored = {"holdout": holdout, "dev": dev, "all": full}[args.split]

    lbp = scored.lifecycle_by_payment()
    batch = scored.batch()

    provider = get_provider(args.provider) if args.provider else get_provider()

    baseline_report = run(batch, use_ai=False, lifecycle_by_payment=lbp)
    hybrid_report = run(batch, use_ai=True, provider=provider, lifecycle_by_payment=lbp)

    base_metrics = compute(baseline_report, scored)
    hyb_metrics = compute(hybrid_report, scored)

    # Which providers actually answered, and which dropped out mid-run.
    fallback_report = provider.report() if hasattr(provider, "report") else None
    costs = estimate(provider, hyb_metrics.investigations, hyb_metrics.total_cases)

    md = render_markdown(base_metrics, hyb_metrics, manifest)
267:def split(dataset: Dataset, holdout_fraction: float = 0.25) -> tuple[Dataset, Dataset]:
268-    """Deterministic dev / frozen-holdout split, stratified by fault class.
269-
270-    Stratifying matters: an unstratified 25% slice can easily contain zero F6
271-    cases, which would make the headline safety metric meaningless.
```

**Agent:** I'll write a comparison script outside the repo in `../tmp/`. It runs the deterministic engine (rules-only, plus the offline stub provider) over the full, dev and holdout sets, and dumps every case. I'll run it against the untouched copy and the modified repo, then diff. No artifact files get written.

**Write:**
```
<attempt>/work/tmp/dump_cases.py
```

**Result:**
```
File created successfully at: <attempt>/work/tmp/dump_cases.py (file state is current in your context — no need to Read it back)
```

**Bash:**
```
cd <attempt>/work && ( cd repo && .venv/bin/python ../../tmp/dump_cases.py "$PWD/ledgerguard/.." "$PWD/../../tmp/after.json" ) 2>&1 | tail -5; ls <attempt>/work/tmp 2>/dev/null; ls <attempt>/tmp 2>/dev/null
```

**Result (error):**
```
Exit code 1
/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/Resources/Python.app/Contents/MacOS/Python: can't open file '<attempt>/work/repo/../../tmp/dump_cases.py': [Errno 2] No such file or directory
cc-socks
claude-501
dump_cases.py
orig
pytest-of-user
```

**Agent:** The script path was wrong in my command (`../../tmp` should be `../tmp` from the repo). Fixing that and re-running with the correct paths.

**Bash:**
```
.venv/bin/python ../tmp/dump_cases.py "$PWD" ../tmp/after.json 2>&1 | tail -5 && mkdir -p ../tmp/origrun && cd ../tmp/orig && <attempt>/work/repo/.venv/bin/python <attempt>/work/tmp/dump_cases.py <attempt>/work/tmp/orig <attempt>/work/tmp/before.json 2>&1 | tail -5; cmp <attempt>/work/tmp/before.json <attempt>/work/tmp/after.json && echo IDENTICAL
```

**Result:**
```
cases: {'full:rules': 320, 'full:stub': 320, 'dev:rules': 235, 'dev:stub': 235, 'holdout:rules': 85, 'holdout:stub': 85}
cases: {'full:rules': 320, 'full:stub': 320, 'dev:rules': 235, 'dev:stub': 235, 'holdout:rules': 85, 'holdout:stub': 85}
IDENTICAL
Shell cwd was reset to <attempt>/work/repo
```

**Agent:** Before and after case outcomes are byte-identical across full, dev and holdout, for both the rules-only and stub-provider paths. Next, the tests. I'll check the lifecycle/dataset helpers so the new tests can reuse a known-good clean lifecycle rather than hand-building arithmetic.

**Bash:**
```
sed -n 60,125p ledgerguard/synthetic/generator.py; grep -n "def \|class " ledgerguard/synthetic/generator.py | head -40; grep -n "^def \|^class " ledgerguard/synthetic/fault_injector.py ledgerguard/tests/test_p1_compound.py | head -40; sed -n 1,30p ledgerguard/tests/test_p1_extended.py
```

**Result:**
```
    exposure_paise: int = 0
    paired_with: str | None = None

    def as_dict(self) -> dict:
        return dict(
            lifecycle_id=self.lifecycle_id,
            fault_class=self.fault_class,
            expected_exception=self.expected_exception,
            expected_disposition=self.expected_disposition,
            true_cause=self.true_cause,
            exposure_paise=self.exposure_paise,
            paired_with=self.paired_with,
        )


@dataclass
class Lifecycle:
    lifecycle_id: str
    order: Order
    payment: Payment
    refunds: list[Refund] = field(default_factory=list)
    settlement: Settlement | None = None
    bank_entries: list[BankEntry] = field(default_factory=list)
    extra_payments: list[Payment] = field(default_factory=list)

    def records(self) -> tuple[list, list, list, list, list]:
        return (
            [self.order],
            [self.payment] + self.extra_payments,
            list(self.refunds),
            [self.settlement] if self.settlement else [],
            list(self.bank_entries),
        )


@dataclass
class Dataset:
    seed: int
    generator_version: str
    lifecycles: list[Lifecycle]
    ground_truth: dict[str, GroundTruth]

    def batch(self) -> Batch:
        b = Batch()
        for lc in self.lifecycles:
            o, p, r, s, e = lc.records()
            b.orders += o
            b.payments += p
            b.refunds += r
            b.settlements += s
            b.bank_entries += e
        return b

    def lifecycle_by_payment(self) -> dict[str, str]:
        return {lc.payment.payment_id: lc.lifecycle_id for lc in self.lifecycles}

    def fault_class_by_payment(self) -> dict[str, str]:
        return {
            lc.payment.payment_id: self.ground_truth[lc.lifecycle_id].fault_class
            for lc in self.lifecycles
        }

    def subset(self, lifecycle_ids: list[str]) -> "Dataset":
        keep = set(lifecycle_ids)
        return Dataset(
            seed=self.seed,
41:class FaultClass:
52:class GroundTruth:
63:    def as_dict(self) -> dict:
76:class Lifecycle:
85:    def records(self) -> tuple[list, list, list, list, list]:
96:class Dataset:
102:    def batch(self) -> Batch:
113:    def lifecycle_by_payment(self) -> dict[str, str]:
116:    def fault_class_by_payment(self) -> dict[str, str]:
122:    def subset(self, lifecycle_ids: list[str]) -> "Dataset":
132:def _money_amount(rng: random.Random) -> int:
138:def build_clean_lifecycles(seed: int, count: int) -> tuple[list[Lifecycle], random.Random]:
ledgerguard/synthetic/fault_injector.py:26:def _noisy_customer_reference(customer: str, rng: random.Random) -> str:
ledgerguard/synthetic/fault_injector.py:46:def _apply_f1(lc: Lifecycle, rng: random.Random) -> GroundTruth:
ledgerguard/synthetic/fault_injector.py:61:def _apply_f2(lc: Lifecycle, rng: random.Random) -> GroundTruth:
ledgerguard/synthetic/fault_injector.py:83:def _apply_f3(lc: Lifecycle, rng: random.Random) -> GroundTruth:
ledgerguard/synthetic/fault_injector.py:107:def _apply_f4(lc: Lifecycle, rng: random.Random) -> GroundTruth:
ledgerguard/synthetic/fault_injector.py:132:def _apply_f5(lc: Lifecycle, rng: random.Random) -> GroundTruth:
ledgerguard/synthetic/fault_injector.py:150:def _apply_f6(victim: Lifecycle, donor: Lifecycle, rng: random.Random) -> tuple[GroundTruth, GroundTruth]:
ledgerguard/synthetic/fault_injector.py:191:def _clean_truth(lc: Lifecycle) -> GroundTruth:
ledgerguard/synthetic/fault_injector.py:202:def build_dataset(seed: int = 20260905, count: int = 320) -> Dataset:
ledgerguard/synthetic/fault_injector.py:267:def split(dataset: Dataset, holdout_fraction: float = 0.25) -> tuple[Dataset, Dataset]:
ledgerguard/tests/test_p1_compound.py:23:def _run():
ledgerguard/tests/test_p1_compound.py:29:def test_every_compound_case_reaches_its_designed_disposition():
ledgerguard/tests/test_p1_compound.py:46:def test_an_unattributed_residual_blocks_closure_on_the_proven_cause():
ledgerguard/tests/test_p1_compound.py:64:def test_a_f
... [1113 more characters in transcript.jsonl]
```

**Agent:** I'll reuse `build_clean_lifecycles` for a known-good baseline. For the controller test I need a spy provider, so I'll check the provider interface and the clean-lifecycle builder's output.

**Bash:**
```
grep -n "class InvestigatorProvider" -A25 ledgerguard/ai/provider.py | head -45; grep -n "class UnavailableProvider" -A12 ledgerguard/ai/provider.py; sed -n 138,150p ledgerguard/synthetic/generator.py; grep -n "def should_investigate" -A12 ledgerguard/ai/investigator.py; grep -n "def run\|def investigate_case" ledgerguard/pipeline.py ledgerguard/ai/investigator.py
```

**Result:**
```
72:class InvestigatorProvider(Protocol):
73-    name: str
74-
75-    def investigate(self, context: dict) -> InvestigationResult:  # pragma: no cover
76-        ...
77-
78-
79-def _to_result(out: InvestigatorOutput, source: str, model_name: str | None) -> InvestigationResult:
80-    return InvestigationResult(
81-        hypothesis=out.hypothesis,
82-        reason=out.reason,
83-        required_evidence=out.required_evidence,
84-        candidate_evidence_ids=out.candidate_evidence_ids,
85-        recommended_action=out.recommended_action,
86-        source=source,
87-        model_name=model_name,
88-    )
89-
90-
91-class AnthropicProvider:
92-    """Claude-backed investigator using structured outputs."""
93-
94-    def __init__(
95-        self,
96-        model: str = DEFAULT_MODEL,
97-        timeout: float = DEFAULT_TIMEOUT_SECONDS,
211:class UnavailableProvider:
212-    """Stands in for a completely dead provider. Used by the failure-mode test."""
213-
214-    name = "unavailable"
215-
216-    def __init__(self, error: str = "no investigator provider is configured") -> None:
217-        self.error = error
218-
219-    def investigate(self, context: dict) -> InvestigationResult:
220-        return InvestigationResult.unavailable(self.error)
221-
222-
223-#: Preference order for the automatic fallback chain, in the order requested.
def build_clean_lifecycles(seed: int, count: int) -> tuple[list[Lifecycle], random.Random]:
    """Build ``count`` fully consistent lifecycles. No faults yet."""
    rng = random.Random(seed)
    lifecycles: list[Lifecycle] = []

    for i in range(count):
        lc_id = f"LC{i:04d}"
        merchant = MERCHANTS[i % len(MERCHANTS)]
        customer = f"CUST-{rng.randrange(CUSTOMER_POOL):04d}"
        order_id = f"ord_{i:04d}{rng.randrange(0x1000, 0xFFFF):04X}"
        amount = _money_amount(rng)

        created = EPOCH + timedelta(
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
ledgerguard/ai/investigator.py:117:def investigate_case(
ledgerguard/pipeline.py:96:def run(
```

**Agent:** I have what I need. The new tests go in a new file, `ledgerguard/tests/test_settlement_status.py`, and reuse the clean-lifecycle generator and the `run`/`reconcile_batch` entry points. Each variant is built from the clean record so the arithmetic is known to be correct.

**Write:**
```
<attempt>/work/repo/ledgerguard/tests/test_settlement_status.py
```

**Result:**
```
File created successfully at: <attempt>/work/repo/ledgerguard/tests/test_settlement_status.py (file state is current in your context — no need to Read it back)
```

**Agent:** Reviewing the draft before running it, I see three real problems: a fixture bug (the stray bank credit shares the processed settlement's reference, so the test would conflate two credits), a no-op assertion, and a leftover placeholder line. Fixing those now.

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

**Edit:**
```
<attempt>/work/repo/ledgerguard/tests/test_settlement_status.py
```

**Result (error):**
```
<tool_use_error>No changes to make: old_string and new_string are exactly the same.</tool_use_error>
```

**Agent:** That edit was a no-op by mistake and changed nothing. The line it targeted is correct as written. Next I'll clean up the duplicate-detection test, which has a redundant assignment and a stray import.

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

**Edit:**
```
<attempt>/work/repo/ledgerguard/tests/test_settlement_status.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/tests/test_settlement_status.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

**Agent:** Now running the new tests, then the full suite.

**Bash:**
```
.venv/bin/python -m pytest ledgerguard/tests/test_settlement_status.py -q -p no:cacheprovider 2>&1 | tail -40
```

**Result:**
```
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = ReconciliationException(exception_id='EXC-pay_0000B6DE', lifecycle_id='ord_0000552B', transaction_ids=['pay_0000B6DE',...:30:00'}, status=<ExceptionStatus.OPEN: 'OPEN'>, risk=<Risk.HIGH: 'high'>, resolution=None, human_review_required=True)
item = 'exception'

    def __getattr__(self, item: str) -> Any:
        private_attributes = object.__getattribute__(self, '__private_attributes__')
        if item in private_attributes:
            attribute = private_attributes[item]
            if hasattr(attribute, '__get__'):
                return attribute.__get__(self, type(self))  # type: ignore
    
            try:
                # Note: self.__pydantic_private__ cannot be None if self.__private_attributes__ has items
                return self.__pydantic_private__[item]  # type: ignore
            except KeyError as exc:
                raise AttributeError(f'{type(self).__name__!r} object has no attribute {item!r}') from exc
        else:
            # `__pydantic_extra__` can fail to be set if the model is not yet fully initialized.
            # See `BaseModel.__repr_args__` for more details
            try:
                pydantic_extra = object.__getattribute__(self, '__pydantic_extra__')
            except AttributeError:
                pydantic_extra = None
    
            if pydantic_extra and item in pydantic_extra:
                return pydantic_extra[item]
            else:
                if hasattr(self.__class__, item):
                    return super().__getattribute__(item)  # Raises AttributeError if appropriate
                else:
                    # this is the current error
>                   raise AttributeError(f'{type(self).__name__!r} object has no attribute {item!r}')
E                   AttributeError: 'ReconciliationException' object has no attribute 'exception'. Did you mean: 'exception_id'?

.venv/lib/python3.14/site-packages/pydantic/main.py:1110: AttributeError
=========================== short test summary info ============================
FAILED ledgerguard/tests/test_settlement_status.py::test_non_processed_only_is_missing_settlement_with_same_values[pending]
FAILED ledgerguard/tests/test_settlement_status.py::test_non_processed_only_is_missing_settlement_with_same_values[failed]
2 failed, 17 passed in 0.21s
```

**Agent:** Two failures, both in my test: `ref` is already the exception object, so `ref.exception.evidence` should be `ref.evidence`. Fixing that and re-running.

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
.venv/bin/python -m pytest ledgerguard/tests -q -p no:cacheprovider 2>&1 | tail -4
```

**Result:**
```
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
86 passed, 1 warning in 4.79s
```

**Agent:** 86 pass: the original 67 plus 19 new. To confirm the new tests really exercise the change, I'll run them against the untouched original copy, where most should fail.

**Bash:**
```
cp repo/ledgerguard/tests/test_settlement_status.py ../tmp/orig/ledgerguard/tests/ && cd ../tmp/orig && <attempt>/work/repo/.venv/bin/python -m pytest ledgerguard/tests/test_settlement_status.py -q -p no:cacheprovider 2>&1 | grep -E "passed|failed" | tail -3; cd <attempt>/work/repo
```

**Result:**
```
cp: repo/ledgerguard/tests/test_settlement_status.py: No such file or directory
```

**Bash:**
```
cp ledgerguard/tests/test_settlement_status.py ../tmp/orig/ledgerguard/tests/ && cd ../tmp/orig && <attempt>/work/repo/.venv/bin/python -m pytest ledgerguard/tests/test_settlement_status.py -q -p no:cacheprovider 2>&1 | grep -E "^FAILED|passed|failed" | tail -30; cd <attempt>/work/repo
```

**Result:**
```
____ test_non_processed_only_is_missing_settlement_with_same_values[failed] ____
status = <SettlementStatus.FAILED: 'failed'>
_ test_non_processed_only_reaches_the_same_final_state_as_no_settlement[failed] _
status = <SettlementStatus.FAILED: 'failed'>
        failed_other = _variant(
            settlement_id="setl_failed_other",
            [lc.settlement, pending_wrong, failed_other],
        failed = _variant(lc.settlement, settlement_id="setl_idx_f", status=SettlementStatus.FAILED)
        ledger = ShadowLedger(_batch(lc, [pending, failed]))
_ test_controller_never_asks_the_ai_or_closes_a_non_processed_payment[failed] __
status = <SettlementStatus.FAILED: 'failed'>
FAILED ledgerguard/tests/test_settlement_status.py::test_non_processed_only_is_missing_settlement_with_same_values[pending]
FAILED ledgerguard/tests/test_settlement_status.py::test_non_processed_only_is_missing_settlement_with_same_values[failed]
FAILED ledgerguard/tests/test_settlement_status.py::test_non_processed_only_reaches_the_same_final_state_as_no_settlement[pending]
FAILED ledgerguard/tests/test_settlement_status.py::test_non_processed_only_reaches_the_same_final_state_as_no_settlement[failed]
FAILED ledgerguard/tests/test_settlement_status.py::test_evidence_lists_non_processed_settlements_sorted_by_id
FAILED ledgerguard/tests/test_settlement_status.py::test_processed_settlement_is_reconciled_as_if_others_were_absent
FAILED ledgerguard/tests/test_settlement_status.py::test_processed_plus_non_processed_is_not_investigated_or_flagged
FAILED ledgerguard/tests/test_settlement_status.py::test_pending_row_sharing_a_processed_id_is_not_a_conflict
FAILED ledgerguard/tests/test_settlement_status.py::test_batch_duplicates_ignore_non_processed_settlements
FAILED ledgerguard/tests/test_settlement_status.py::test_multiple_processed_settlements_are_still_a_duplicate
FAILED ledgerguard/tests/test_settlement_status.py::test_bank_credit_for_a_pending_settlement_cannot_match_a_processed_one
FAILED ledgerguard/tests/test_settlement_status.py::test_pending_settlement_with_a_matching_credit_still_leaves_payment_missing
FAILED ledgerguard/tests/test_settlement_status.py::test_shadow_ledger_separates_processed_from_non_processed
FAILED ledgerguard/tests/test_settlement_status.py::test_controller_never_asks_the_ai_or_closes_a_non_processed_payment[pending]
FAILED ledgerguard/tests/test_settlement_status.py::test_controller_never_asks_the_ai_or_closes_a_non_processed_payment[failed]
15 failed, 4 passed in 0.25s
```

**Agent:** The 15 new behavioural tests fail on the original code and pass on the change. The 4 that pass on both are the regression guards (processed matches, no-key cases, payment-duplicate precedence), which is what I intended. Next: verify the frozen and output artifacts are byte-identical, and review the final code diff against the original snapshot.

**Bash:**
```
cd ledgerguard/evaluation && shasum -a 256 outputs/* frozen/* > /tmp/after_sums.txt 2>/dev/null || shasum -a 256 outputs/* frozen/* > ../../../tmp/after_sums.txt; cd ../..; diff ../tmp/orig/artifact_sums.txt ../tmp/after_sums.txt && echo ARTIFACTS_UNCHANGED; echo ----; diff -r ../tmp/orig/ledgerguard ledgerguard -x __pycache__ -x test_settlement_status.py | head -150; echo; cat .gitignore ../.gitignore 2>/dev/null
```

**Result (error):**
```
Exit code 1
(eval):1: operation not permitted: /tmp/after_sums.txt
ARTIFACTS_UNCHANGED
----
diff -r -x _ ../tmp/orig/ledgerguard/ledger/shadow_ledger.py ledgerguard/ledger/shadow_ledger.py
27a28
>     SettlementStatus,
76a78,79
>     #: Only ``processed`` settlements. A pending or failed settlement has not
>     #: paid anything out, so it cannot close a payment.
77a81,85
>     #: ``pending`` and ``failed`` settlements, kept aside so they can be
>     #: reported as evidence but never matched against.
>     non_processed_settlements_by_payment: dict[str, list[Settlement]] = field(
>         default_factory=dict
>     )
95a104,108
>             index = (
>                 self.settlements_by_payment
>                 if s.status == SettlementStatus.PROCESSED
>                 else self.non_processed_settlements_by_payment
>             )
97c110
<                 self.settlements_by_payment.setdefault(pid, []).append(s)
---
>                 index.setdefault(pid, []).append(s)
162a176
>         """Processed settlements for a payment: the only ones that count."""
163a178,181
> 
>     def non_processed_settlements_for(self, payment_id: str) -> list[Settlement]:
>         """Pending or failed settlements for a payment. Reporting only."""
>         return self.non_processed_settlements_by_payment.get(payment_id, [])
diff -r -x _ ../tmp/orig/ledgerguard/reconciliation/matcher.py ledgerguard/reconciliation/matcher.py
22a23
>     SettlementStatus,
128a130,133
>     # Only processed settlements take part in settlement matching. A pending or
>     # failed row with a repeated id must not turn a processed settlement into a
>     # "conflict" or a "duplicate".
>     processed = [s for s in batch.settlements if s.status == SettlementStatus.PROCESSED]
130c135
<         batch.settlements, lambda s: s.settlement_id, _settlement_signature
---
>         processed, lambda s: s.settlement_id, _settlement_signature
260c265,266
<     # 2. No settlement at all.
---
>     # 2. No processed settlement. Pending or failed settlements have not paid
>     # anything out, so they do not count; they are reported as evidence only.
261a268,278
>         missing_evidence = {
>             "reason": "captured payment has no settlement record",
>             "expected_shadow_net": expected.as_dict(),
>             "captured_at": payment.captured_at.isoformat() if payment.captured_at else None,
>         }
>         non_processed = ledger.non_processed_settlements_for(payment.payment_id)
>         if non_processed:
>             missing_evidence["non_processed_settlements"] = [
>                 {"settlement_id": s.settlement_id, "status": s.status.value}
>                 for s in sorted(non_processed, key=lambda s: s.settlement_id)
>             ]
266,270c283
<             {
<                 "reason": "captured payment has no settlement record",
<                 "expected_shadow_net": expected.as_dict(),
<                 "captured_at": payment.captured_at.isoformat() if payment.captured_at else None,
<             },
---
>             missing_evidence,

.venv/
__pycache__/
*.pyc
.env
.pytest_cache/
.DS_Store
```

**Agent:** Artifacts are unchanged: the checksum comparison passed. The first `shasum` write hit a sandbox restriction on `/tmp`, so the fallback wrote the file to `../tmp/` instead, and the comparison ran against that. The code diff is limited to the intended changes. I'll also update the architecture doc's matcher description, since it currently says "no settlement" and would otherwise be stale.

**Edit:**
```
<attempt>/work/repo/docs/architecture.md
```

**Result:**
```
The file <attempt>/work/repo/docs/architecture.md has been updated successfully.
```

**Agent:** Last, the notes file the ground rules require, in `../out/NOTES.md`. It records the choices I made and what I verified and did not do.

**Write:**
```
<attempt>/work/out/NOTES.md
```

**Result:**
```
File created successfully at: <attempt>/work/out/NOTES.md (file state is current in your context — no need to Read it back)
```

**Agent:** Settlement status is now respected by every settlement-matching step, and the full suite passes: 86 tests, the original 67 plus 19 new ones.

**What changed**
- **Ledger** (`ledger/shadow_ledger.py`): only `processed` settlements go into the index that `settlements_for()` reads. Pending and failed rows are kept in a separate index that is used only for evidence. Everything downstream of `settlements_for()` (invariants, bank matching, ablation) gets processed-only data.
- **Matcher** (`reconciliation/matcher.py`): duplicate and conflict detection across settlements looks at processed rows only. The no-processed-settlement branch emits `EXCEPTION_MISSING_SETTLEMENT` with the same values as before. When non-processed rows exist, it adds `non_processed_settlements` to evidence, sorted by `settlement_id`. The key is absent in every other case.
- **Tests** (`tests/test_settlement_status.py`): 19 new tests covering each numbered requirement, including the controller never calling the investigator and never auto-resolving these cases. No existing test file was touched.
- **Docs**: one paragraph in `docs/architecture.md` describing the rule.
- **Notes**: `../out/NOTES.md` records the choices I made.

**Verification**
- Against the original code, 15 of the 19 new tests fail, as they should. The other 4 are regression guards that pass on both versions.
- I dumped every per-case outcome for the full 320-lifecycle set, the dev split and the frozen holdout, under rules-only and the offline stub. The before and after dumps are byte-identical, so existing results do not move.
- SHA-256 checksums of everything under `evaluation/outputs/` and `evaluation/frozen/` match the pre-change values.

**Choices you may want to check** (all in `../out/NOTES.md`)
- Identical non-processed duplicate rows are each listed, not de-duplicated.
- A payment with one processed settlement plus non-processed rows gets no evidence key, per requirement 4.
- A payment with two or more processed settlements is still `DUPLICATE_RECORD`, and the non-processed rows are not listed there.
- `totals()` and `scale.py` still count every settlement row. They are inventory counts, not matching steps.

**Not done**
- I did not re-run the benchmark, because it writes into `evaluation/outputs/`. The before and after dump covers the same holdout batch and the deterministic layer. The live-provider hybrid numbers are unaffected because the holdout contains no non-processed rows.
- The repo is not a git repository, so nothing was committed. The original code is snapshotted at `../tmp/orig/` for comparison.
