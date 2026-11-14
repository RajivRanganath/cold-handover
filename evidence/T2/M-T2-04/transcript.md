# M-T2-04 transcript (PASS)

**Agent:** I'll start with the handover docs at the repo root, then the settlement-matching code.

**Bash:**
```
ls -la && ls .. && find . -path ./.venv -prune -o -type f -print | grep -v __pycache__ | head -200
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
out
repo
tmp
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
cat README.md | head -400 && echo ---- && cat docs/architecture.md && echo ---- && ls ../out ../tmp 2>/dev/null; cat ../out/NOTES.md 2>/dev/null
```

**Result (error):**
```
Exit code 1
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
   `AUTO_RESOLV
... [6040 more characters in transcript.jsonl]
```

**Bash:**
```
cd <attempt>/work/repo/ledgerguard && wc -l reconciliation/*.py ledger/*.py pipeline.py && cat reconciliation/matcher.py
```

**Result:**
```
       0 reconciliation/__init__.py
      85 reconciliation/exceptions.py
     410 reconciliation/matcher.py
       0 ledger/__init__.py
     204 ledger/invariants.py
     153 ledger/models.py
      55 ledger/money.py
     195 ledger/shadow_ledger.py
     186 pipeline.py
    1288 total
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
    """Pre-pass: identifier and content level duplicate detect
... [12094 more characters in transcript.jsonl]
```

**Agent:** The matcher is clear. Next I need the ledger side (`settlements_for`, bank matching), the models, and the invariants.

**Bash:**
```
cat ledger/shadow_ledger.py && echo ---- && cat ledger/models.py
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
... [7481 more characters in transcript.jsonl]
```

**Bash:**
```
cat ledger/invariants.py && echo ---- && cat reconciliation/exceptions.py && echo ---- && cat pipeline.py
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

... [12652 more characters in transcript.jsonl]
```

**Bash:**
```
cd <attempt>/work/repo && grep -n -i "handover\|status\|settlement" README.md | head -80
```

**Result:**
```
5:The workflow is settlement reconciliation: inspect the source records, verify an
35:framework, or a Razorpay payment API integration. Synthetic settlement
51:LedgerGuard reconciles orders, payments, refunds, settlements and bank records.
56:   It never reads settlement or bank records to decide what to expect. Six named
61:   identifier matching, settlement arithmetic against the fee schedule,
349:| F1 | Missing settlement | 15 | escalate — the money is outstanding |
353:| F5 | Delayed settlement | 16 | auto close — amounts correct, timing wrong |
492:**P1 extended coverage** — duplicate shapes, settlement window boundaries,
```

**Agent:** The core change is clear: filter settlements by status in one place, and attach the non-processed evidence only in the missing-settlement branch. Before editing I need to find every other place that reads settlements, since requirement 1 covers "every settlement-matching step", and check whether the frozen holdout contains any non-processed settlements.

**Bash:**
```
cd <attempt>/work/repo/ledgerguard && grep -rn "settlement" --include=*.py . | grep -v "tests/" | grep -i "batch.settlements\|settlements_for\|settlements_by\|\.settlements\b\|SettlementStatus\|status" | head -80; echo ----; grep -rn "SettlementStatus\|status=.*pending\|SettlementStatus\.\(PENDING\|FAILED\)" --include=*.py . | head -40
```

**Result:**
```
(eval):1: no matches found: --include=*.py
----
(eval):1: no matches found: --include=*.py
```

**Bash:**
```
python3 -c "
import json
d=json.load(open('evaluation/frozen/holdout_20260905_320.json'))
print(type(d), list(d.keys())[:20] if isinstance(d,dict) else len(d))
" ; grep -o '"status": *"[a-z_]*"' evaluation/frozen/holdout_20260905_320.json | sort | uniq -c; grep -c "pending\|failed" evaluation/frozen/holdout_20260905_320.json
```

**Result:**
```
<class 'dict'> ['seed', 'count', 'generator_version', 'holdout_lifecycle_ids', 'holdout_batch_sha256']
0
```

**Agent:** The holdout file stores only seed and ids, so the batch is regenerated. I'll check whether the generator ever emits non-processed settlements, and find every settlement reader.

**Bash:**
```
grep -rn -e "settlements" -e "SettlementStatus" -e "status=" --include='*.py' . | grep -v "/tests/" | grep -v "payment.status\|refund.status" ; echo ----; grep -rln "settlement" --include='*.py' . 
```

**Result:**
```
qa.py:112:def _missing_settlements(report: RunReport) -> tuple[str, list[str]]:
qa.py:144:    _Query("missing_settlements", ("missing settlement", "never settled", "not settled"),
qa.py:145:           "payments with no settlement", _missing_settlements),
reconciliation/matcher.py:121:    and settlements are grouped by id and then split by signature; bank entries
reconciliation/matcher.py:130:        batch.settlements, lambda s: s.settlement_id, _settlement_signature
reconciliation/matcher.py:196:    settlements = ledger.settlements_for(payment.payment_id)
reconciliation/matcher.py:217:            status=exc_type.value,
reconciliation/matcher.py:241:            settlements[0] if settlements else None,
reconciliation/matcher.py:256:            settlements[0] if settlements else None,
reconciliation/matcher.py:261:    if not settlements:
reconciliation/matcher.py:276:    if len(settlements) > 1:
reconciliation/matcher.py:280:        signatures = {_settlement_signature(s) for s in settlements}
reconciliation/matcher.py:282:            s.settlement_id in duplicates.settlement_conflicts for s in settlements
reconciliation/matcher.py:286:                "multiple settlements reference the same payment with conflicting content"
reconciliation/matcher.py:288:                else "multiple settlements reference the same payment"
reconciliation/matcher.py:290:            "settlement_ids": [s.settlement_id for s in settlements],
reconciliation/matcher.py:297:            sum(s.net_amount for s in settlements),
reconciliation/matcher.py:299:            settlements[0],
reconciliation/matcher.py:303:    settlement = settlements[0]
reconciliation/matcher.py:313:            status=MATCHED,
ledger/shadow_ledger.py:77:    settlements_by_payment: dict[str, list[Settlement]] = field(default_factory=dict)
ledger/shadow_ledger.py:95:        for s in self.batch.settlements:
ledger/shadow_ledger.py:97:                self.settlements_by_payment.setdefault(pid, []).append(s)
ledger/shadow_ledger.py:162:    def settlements_for(self, payment_id: str) -> list[Settlement]:
ledger/shadow_ledger.py:163:        return self.settlements_by_payment.get(payment_id, [])
ledger/shadow_ledger.py:192:            "settlements": len(self.batch.settlements),
ledger/models.py:36:class SettlementStatus(str, Enum):
ledger/models.py:94:    status: SettlementStatus = SettlementStatus.PROCESSED
ledger/models.py:152:    settlements: list[Settlement] = Field(default_factory=list)
tests/test_p0_core.py:133:        settlements=[settlement],
tests/test_p1_extended.py:146:def test_two_settlements_that_disagree_are_never_collapsed_into_one():
tests/test_p1_extended.py:147:    """Same payment, two settlements, different nets. Which is real is unproven."""
tests/test_p1_extended.py:152:    original = batch.settlements[0]
tests/test_p1_extended.py:160:        update={"settlements": list(batch.settlements) + [rival]}
tests/test_p1_extended.py:414:        orders=[order], payments=[payment], settlements=[settlement],
tests/test_p1_extended.py:444:        status=exc.exception_type.value,
tests/test_p1_extended.py:499:        status=exc.exception_type.value,
synthetic/adversarial.py:123:        settlements=[a_settlement, b_settlement],
synthetic/generator.py:28:    SettlementStatus,
synthetic/generator.py:109:            b.settlements += s
synthetic/generator.py:160:            status=OrderStatus.PAID,
synthetic/generator.py:170:            status=PaymentStatus.CAPTURED,
synthetic/generator.py:187:                    status=RefundStatus.PROCESSED,
synthetic/generator.py:208:            status=SettlementStatus.PROCESSED,
synthetic/compound.py:115:    orders, payments, refunds, settlements, entries = [], [], [], [], []
synthetic/compound.py:123:            settlements.append(s)
synthetic/compound.py:199:            settlements=settlements,
evaluation/ablation.py:173:        settlements = ledger.settlements_for(payment.payment_id)
evaluation/ablation.py:174:        if not settlements:
evaluatio
... [1255 more characters in transcript.jsonl]
```

**Agent:** The generator only emits `processed` settlements, so the holdout should be unaffected. Next I'll check the verifier, investigator, and backend for settlement lookups that bypass the ledger's index.

**Bash:**
```
grep -n -i "settlement" evidence/verifier.py ai/investigator.py ai/schemas.py backend/app.py evidence/safety.py evaluation/benchmark.py evaluation/drift.py evaluation/report.py evaluation/ablation.py qa.py | head -120
```

**Result:**
```
ai/investigator.py:44:    settlement = case.settlement
ai/investigator.py:96:            "settlement": exc.evidence.get("observed_settlement"),
backend/app.py:107:                    "settlement": (
backend/app.py:109:                            "settlement_id": case.settlement.settlement_id,
backend/app.py:110:                            "gross_inr": to_rupees_str(case.settlement.gross_amount),
backend/app.py:111:                            "fees_inr": to_rupees_str(case.settlement.fees),
backend/app.py:112:                            "tax_inr": to_rupees_str(case.settlement.tax),
backend/app.py:114:                                case.settlement.refund_adjustments
backend/app.py:116:                            "net_inr": to_rupees_str(case.settlement.net_amount),
backend/app.py:117:                            "settlement_date": case.settlement.settlement_date.isoformat(),
backend/app.py:119:                        if case.settlement
backend/app.py:302:        (FaultClass.F1_MISSING_SETTLEMENT, None),
ai/schemas.py:29:    type: str                                 # refund | settlement | bank_entry | payment
evidence/verifier.py:38:#: How late after settlement a refund may still legitimately be booked into it.
evidence/verifier.py:112:    settlement = case.settlement
evidence/verifier.py:189:    if payment.captured_at is None or settlement is None:
evidence/verifier.py:190:        timing_ok, timing_detail = False, "capture or settlement timestamp unavailable"
evidence/verifier.py:192:        latest = settlement.settlement_date + timedelta(days=REFUND_BOOKING_TOLERANCE_DAYS)
evidence/verifier.py:196:            f"{payment.captured_at.date()} and settlement+{REFUND_BOOKING_TOLERANCE_DAYS}d "
evidence/verifier.py:204:    # settlement now balances exactly.
evidence/verifier.py:205:    if settlement is None:
evidence/verifier.py:206:        restored, detail = False, "no settlement to reconcile against"
evidence/verifier.py:209:        restored = rebuilt.net_amount == settlement.net_amount
evidence/verifier.py:212:            f"observed settlement net = {settlement.net_amount}"
evaluation/benchmark.py:209:            "observed_settlement": (
evaluation/benchmark.py:210:                case.exception.evidence.get("observed_settlement") if case.exception else None
evaluation/report.py:56:            "difference_inr", "settlement_id", "settlement_date",
evaluation/report.py:91:                to_rupees_str(case.settlement.net_amount) if case.settlement else "",
evaluation/report.py:93:                case.settlement.settlement_id if case.settlement else "",
evaluation/report.py:94:                case.settlement.settlement_date.date().isoformat() if case.settlement else "",
evaluation/drift.py:3:The Shadow Ledger's power comes from computing what a settlement *should* be.
evaluation/drift.py:5:platform fee, 18% GST on it, T+2 settlement -- and the provider is free to
evaluation/drift.py:77:    s = lc.settlement
evaluation/drift.py:83:        s.settlement_date = lc.payment.captured_at + timedelta(days=lag_days)
evaluation/drift.py:86:        e.date = s.settlement_date
evaluation/drift.py:129:    ("settlement_T3", "settlement lag T+2 -> T+3", {"lag_days": 3}),
evaluation/drift.py:130:    ("settlement_T4", "settlement lag T+2 -> T+4", {"lag_days": 4}),
qa.py:112:def _missing_settlements(report: RunReport) -> tuple[str, list[str]]:
qa.py:116:        and o.case.exception.exception_type.value == "EXCEPTION_MISSING_SETTLEMENT"
qa.py:120:        f"{len(cases)} captured payments have no settlement record, "
qa.py:144:    _Query("missing_settlements", ("missing settlement", "never settled", "not settled"),
qa.py:145:           "payments with no settlement", _missing_settlements),
evidence/safety.py:31:    ExceptionType.DELAYED_SETTLEMENT: "All amounts reconcile exactly; the only discrepancy is timing against the expected settlement window.",
evidence/safety.py:36:    ExceptionType.MISSING_SETTLEMENT: "Captured funds have no settlement record. Th
... [2903 more characters in transcript.jsonl]
```

**Agent:** Nothing outside the ledger reads settlements in a way that bypasses `settlements_for`, so the cleanest design is to filter at the ledger index. Before editing, I'll check the investigator gate, the safety decision for missing settlements, the benchmark entry point (it writes into `outputs/`), and the existing test style.

**Bash:**
```
grep -n "def should_investigate" -A 12 ai/investigator.py; echo ----; sed -n 40,175p evidence/safety.py; echo ----; grep -n "def \|OUTPUT\|outputs\|frozen\|write" evaluation/benchmark.py | head -80
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
            case_id=case.case_id,
            state=HUMAN_REVIEW_REQUIRED,
            reason=(
                f"Two {conflict} records share an identifier but disagree on content, "
                "so they are not copies of one another. Suppressing one would pick a "
                "version the batch does not prove."
            ),
            missing_evidence=[f"authoritative version of the {conflict} record"],
            suggested_action=(
                f"Re-fetch the {conflict} from the source system and re-ingest, then "
                "re-run reconciliation for this payment."
            ),
        )

    residual = exc.evidence.get("residual_paise") or 0
    secondary = exc.evidence.get("secondary_findings") or []

    if exc_type in _DETERMINISTIC_AUTO_CLOSE:
        if residual:
            # Money the proven cause does not account for. Closing here would be
            # closing a case on the strength of the part that was proved while
            # the rest stays unexplained -- the exact failure this system exists
            # to prevent.
            return Decision(
                case_id=case.case_id,
                state=HUMAN_REVIEW_REQ
... [4121 more characters in transcript.jsonl]
```

**Bash:**
```
sed -n 1,80p tests/test_p0_core.py; echo ----; sed -n 100,140p tests/test_p0_core.py; echo ----; cat ../run_demo.sh; echo ----; ls tests; sed -n 1,40p tests/test_p1_extended.py
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
----
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
    )
    bank = BankEntry(
        bank_entry_id="bnk_TEST01",
        amount=net,
        credit_or_debit=CreditDebit.CREDIT,
        date=settled_on,
        reference=settlement.reference,
    )
    batch = Batch(
        orders=[order],
        payments=[payment],
        refunds=refunds,
        settlements=[settlement],
        bank_entries=[bank],
    )
    return batch, payment, settlement, bank


# --------------------------------------------------------------------------- 2
def test_2_shadow_ledger_invariants_separate_good_from_corrupted():
----
#!/usr/bin/env bash
# Reliable local demo. One command, no arguments.
set -euo pipefail
cd "$(dirname "$0")"

PY=.venv/bin/python
if [ ! -x "$PY" ]; then
  echo "Creating virtualenv..."
  python3 -m
... [2608 more characters in transcript.jsonl]
```

**Agent:** The safety gate already routes `MISSING_SETTLEMENT` to human review and the investigator never sees it, so requirement 7 should hold without touching those modules. I'll snapshot the artifacts, run the existing suite to get a baseline, and then make the change.

**Bash:**
```
cd <attempt>/work/repo && mkdir -p ../tmp/snapshot && cp -R ledgerguard/evaluation/outputs ledgerguard/evaluation/frozen ../tmp/snapshot/ && (find ledgerguard/evaluation/outputs ledgerguard/evaluation/frozen -type f -exec shasum -a 256 {} \; | sort > ../tmp/snapshot_before.sha256) && .venv/bin/python -m pytest ledgerguard/tests -q 2>&1 | tail -15
```

**Result:**
```
...................................................................      [100%]
=============================== warnings summary ===============================
.venv/lib/python3.14/site-packages/fastapi/testclient.py:1
  <attempt>/work/repo/.venv/lib/python3.14/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
67 passed, 1 warning in 5.14s
```

**Agent:** Baseline is 67 passing. Now the change. I'm filtering at the ledger index so every consumer that goes through `settlements_for` (matcher, ablation) gets the same behaviour, keeping the non-processed records in a separate index for the evidence field only.

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

**Agent:** Next, the matcher: duplicate-settlement detection uses processed settlements only, and the missing-settlement branch gets the evidence key.

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

**Agent:** I changed the `reason` text in the non-processed branch. The spec only asks for the new key there, so I'll revert that and keep the reason identical to today's.

**Edit:**
```
<attempt>/work/repo/ledgerguard/reconciliation/matcher.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/reconciliation/matcher.py has been updated successfully.
```

**Agent:** Now the tests. I need the provider interface to write a spy that proves the investigator is never called end-to-end.

**Bash:**
```
cd <attempt>/work/repo/ledgerguard && grep -n "class \|def " ai/provider.py | head -40; grep -n "class InvestigatorProvider" -A 15 ai/provider.py
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
```

**Agent:** I have what I need. Writing the new test module, covering each numbered requirement plus the end-to-end guarantee with a spy provider.

**Write:**
```
<attempt>/work/repo/ledgerguard/tests/test_settlement_status.py
```

**Result:**
```
File created successfully at: <attempt>/work/repo/ledgerguard/tests/test_settlement_status.py (file state is current in your context — no need to Read it back)
```

**Agent:** I left a broken assertion and a stray helper class in the content-conflict test. Fixing both and simplifying the fee-mismatch fixture before running.

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
cd <attempt>/work/repo && .venv/bin/python -m pytest ledgerguard/tests -q 2>&1 | tail -40
```

**Result:**
```
........................................................................ [ 86%]
...........                                                              [100%]
=============================== warnings summary ===============================
.venv/lib/python3.14/site-packages/fastapi/testclient.py:1
  <attempt>/work/repo/.venv/lib/python3.14/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
83 passed, 1 warning in 4.75s
```

**Agent:** All 83 pass (67 existing + 16 new). Now requirement 6: I'll regenerate the benchmark, compare against the pre-change snapshot, and then restore the artifacts so the repo is left unchanged.

**Bash:**
```
.venv/bin/python -m ledgerguard.evaluation.benchmark >/dev/null 2>../tmp/bench_stderr.txt; echo exit=$?; for f in benchmark.json cases.json unresolved_exceptions.csv reconciliation_report.csv evidence_ledger.csv decision_log.json; do if cmp -s ledgerguard/evaluation/outputs/$f ../tmp/snapshot/outputs/$f; then echo "SAME $f"; else echo "DIFF $f"; fi; done; .venv/bin/python - <<'EOF'
import json
a=json.load(open('../tmp/snapshot/outputs/benchmark.json'))
b=json.load(open('ledgerguard/evaluation/outputs/benchmark.json'))
def strip(d):
    if isinstance(d,dict): return {k:strip(v) for k,v in d.items() if 'ms' not in k and 'wall' not in k and 'latenc' not in k and 'second' not in k}
    if isinstance(d,list): return [strip(x) for x in d]
    return d
print("benchmark.json equal excluding timing:", strip(a)==strip(b))
EOF
```

**Result:**
```
exit=0
DIFF benchmark.json
DIFF cases.json
DIFF unresolved_exceptions.csv
SAME reconciliation_report.csv
SAME evidence_ledger.csv
SAME decision_log.json
benchmark.json equal excluding timing: False
```

**Agent:** Some artifacts differ. I need to see whether that is timing noise or a real metric change.

**Bash:**
```
.venv/bin/python - <<'EOF'
import json
a=json.load(open('../tmp/snapshot/outputs/benchmark.json'))
b=json.load(open('ledgerguard/evaluation/outputs/benchmark.json'))
def walk(x,y,p=""):
    if type(x)!=type(y): print("TYPE",p,str(x)[:100],str(y)[:100]); return
    if isinstance(x,dict):
        for k in set(x)|set(y):
            if k not in x or k not in y: print("KEY",p+"/"+k); continue
            walk(x[k],y[k],p+"/"+k)
    elif isinstance(x,list):
        if len(x)!=len(y): print("LEN",p,len(x),len(y))
        for i,(u,v) in enumerate(zip(x,y)): walk(u,v,f"{p}[{i}]")
    elif x!=y: print("VAL",p,x,y)
walk(a,b)
EOF
diff ../tmp/snapshot/outputs/unresolved_exceptions.csv ledgerguard/evaluation/outputs/unresolved_exceptions.csv | head; diff <(python3 -m json.tool ../tmp/snapshot/outputs/cases.json) <(python3 -m json.tool ledgerguard/evaluation/outputs/cases.json) | head -20
```

**Result:**
```
VAL /hybrid/unresolved_value_paise 13590189 12189954
VAL /hybrid/unnecessary_abstentions 2 0
VAL /hybrid/provider fallback(groq->gemini->nvidia->omniroute) heuristic_stub
VAL /hybrid/throughput_per_second 0.7 22587.6
VAL /hybrid/per_fault_class/F3_UNLINKED_PARTIAL_REFUND/correct 7 9
VAL /hybrid/per_fault_class/F3_UNLINKED_PARTIAL_REFUND/abstained 2 0
VAL /hybrid/per_fault_class/F3_UNLINKED_PARTIAL_REFUND/auto_resolved 7 9
VAL /hybrid/latency_p95_ms 12804.67 0.02
VAL /hybrid/human_review_required 12 10
VAL /hybrid/unresolved_value_inr 135901.89 121899.54
VAL /hybrid/latency_p50_ms 10775.36 0.01
VAL /hybrid/accuracy 0.9765 1.0
VAL /hybrid/disposition_correct 83 85
VAL /hybrid/wall_seconds 121.704 0.004
VAL /hybrid/auto_resolved 19 21
VAL /hybrid/model_calls 15 0
VAL /hybrid/exceptions_correctly_resolved 19 21
VAL /hybrid/model_calls_per_100_records 17.65 0.0
TYPE /investigator_chain {'chain': ['groq:openai/gpt-oss-120b', 'gemini:gemini-2.5-flash', 'nvidia:nvidia/llama-3.1-nemotron- None
KEY /cost_estimate
VAL /baseline/throughput_per_second 22395.4 26152.8
VAL /baseline/wall_seconds 0.004 0.003
2c2
< pay_00121298,LC0012,EXCEPTION_UNEXPLAINED_SHORTFALL,HUMAN_REVIEW_REQUIRED,pay_00121298 ord_00123197 setl_0012D881,6988.10,,no hypothesis was proposed,"The investigator found no explanation it could support from the available records: The settlement shows a refund adjustment of 698,810 paise, which exactly matches the observed shortfall. A candidate refund record (rfnd_01952574) of the same amount exists, but it is not linked to the payment (payment_id is null) and no explicit linkage evidence is present in the provided records. Without proof that this refund is associated with pay_00121298, we cannot confirm the unlinked partial refund explanation.","Obtain the missing record from the provider, or confirm the deduction manually before closing."
---
> pay_00121298,LC0012,EXCEPTION_UNEXPLAINED_SHORTFALL,HUMAN_REVIEW_REQUIRED,pay_00121298 ord_00123197 setl_0012D881,6988.10,E1_evidence_records_exist; E2_refund_is_processed; E3_refund_not_linked_elsewhere; E5_amount_equals_shortfall; E7_invariant_restored,E4_reference_identifies_this_customer; E6_timing_is_plausible,Evidence Gate rejected the hypothesis 'unlinked_partial_refund': refund reference 'ADJ/CUST-0007/partial' vs order customer 'CUST-0072' -> NO MATCH,Do not net this against the proposed refund. Identify the true counterparty of the deduction with the provider before closing.
4d3
< pay_003478CC,LC0034,EXCEPTION_UNEXPLAINED_SHORTFALL,HUMAN_REVIEW_REQUIRED,pay_003478CC ord_0034877E setl_0034CA22,12726.70,,no hypothesis was proposed,"The investigator found no explanation it could support from the available records: The observed shortfall (1,272,670 paise) matches the amount of an unlinked refund (rfnd_003431D5), suggesting a possible unlinked_partial_refund. However, the records provided do not contain any linkage between this refund and payment pay_003478CC (e.g., a payment_id field or a documented association). Without that relationship, the hypothesis cannot be proven from the available evidence.","Obtain the missing record from the provider, or confirm the deduction manually before closing."
13d11
< pay_0279F905,LC0279,EXCEPTION_UNEXPLAINED_SHORTFALL,HUMAN_REVIEW_REQUIRED,pay_0279F905 ord_0279DC3C setl_027975BE,1275.65,,no hypothesis was proposed,"The investigator found no explanation it could support from the available records: The only record that could explain the 127,565 paise shortfall is refund rfnd_027971A8, which matches the settlement's refund_adjustments amount. However, the refund record does not contain a payment_id or any other field establishing a link to payment pay_0279F905, and no other records provide such linkage. Without proof that the refund is associated with this payment, the hypothesis cannot be verified.","Obtain the missing record from the provider, or confirm the deduction manually before closing."
diff: /dev/fd/11: Operation not permitted
```

**Agent:** The differences are not from my change. The snapshot was generated with live model providers, and this environment has no API key, so the hybrid run fell back to `heuristic_stub` (`model_calls` 15 → 0). The deterministic outputs (`reconciliation_report.csv`, `decision_log.json`, `evidence_ledger.csv`) are byte-identical, and the rules-only baseline metrics match. To be sure the holdout is unaffected, I'll confirm directly that every settlement in the regenerated holdout is `processed`, then restore the artifacts.

**Bash:**
```
grep -n "build_dataset\|split(" ledgerguard/evaluation/benchmark.py | head; .venv/bin/python - <<'EOF'
import inspect, collections
from ledgerguard.evaluation import benchmark as b
src = inspect.getsource(b.main)
print(src[:900])
EOF
```

**Result:**
```
31:from ..synthetic.fault_injector import build_dataset, split
256:    full = build_dataset(seed=args.seed, count=args.count)
257:    dev, holdout = split(full)
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
    scored = {"holdout": h
```

**Bash:**
```
.venv/bin/python - <<'EOF'
import collections
from ledgerguard.synthetic.fault_injector import build_dataset, split
from ledgerguard.reconciliation.matcher import reconcile_batch
full = build_dataset(seed=20260905, count=320)
dev, holdout = split(full)
batch = holdout.batch if hasattr(holdout, "batch") else None
print(type(holdout).__name__, [a for a in dir(holdout) if not a.startswith("_")][:20])
EOF
```

**Result:**
```
Dataset ['batch', 'fault_class_by_payment', 'generator_version', 'ground_truth', 'lifecycle_by_payment', 'lifecycles', 'seed', 'subset']
```

**Bash:**
```
.venv/bin/python - <<'EOF'
import collections
from ledgerguard.synthetic.fault_injector import build_dataset, split
from ledgerguard.reconciliation.matcher import reconcile_batch
full = build_dataset(seed=20260905, count=320)
dev, holdout = split(full)
b = holdout.batch
print("holdout settlement statuses:", collections.Counter(s.status.value for s in b.settlements))
print("holdout settlements:", len(b.settlements), "payments:", len(b.payments))
cases, _ = reconcile_batch(b, holdout.lifecycle_by_payment)
print("case statuses:", collections.Counter(c.status for c in cases))
EOF
```

**Result (error):**
```
Exit code 1
Traceback (most recent call last):
  File "<stdin>", line 7, in <module>
AttributeError: 'function' object has no attribute 'settlements'
```

**Bash:**
```
.venv/bin/python - <<'EOF'
import collections
from ledgerguard.synthetic.fault_injector import build_dataset, split
from ledgerguard.reconciliation.matcher import reconcile_batch
full = build_dataset(seed=20260905, count=320)
dev, holdout = split(full)
b = holdout.batch()
print("holdout settlement statuses:", collections.Counter(s.status.value for s in b.settlements))
print("holdout settlements:", len(b.settlements), "payments:", len(b.payments))
cases, _ = reconcile_batch(b, holdout.lifecycle_by_payment)
print("case statuses:", collections.Counter(c.status for c in cases))
EOF
```

**Result (error):**
```
Exit code 1
holdout settlement statuses: Counter({'processed': 81})
holdout settlements: 81 payments: 88
Traceback (most recent call last):
  File "<stdin>", line 9, in <module>
  File "<attempt>/work/repo/ledgerguard/reconciliation/matcher.py", line 423, in reconcile_batch
    lifecycle_by_payment.get(payment.payment_id),
    ^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'function' object has no attribute 'get'
```

**Agent:** All 81 holdout settlements are `processed`, so every new filter is a no-op on the holdout, and the new evidence key is only added when a non-processed record exists. Now I'll restore the artifacts from the snapshot and verify the checksums match the pre-change state.

**Bash:**
```
cp -R ../tmp/snapshot/outputs/. ledgerguard/evaluation/outputs/ && cp -R ../tmp/snapshot/frozen/. ledgerguard/evaluation/frozen/ && find ledgerguard/evaluation/outputs ledgerguard/evaluation/frozen -type f -exec shasum -a 256 {} \; | sort > ../tmp/snapshot_after.sha256 && diff ../tmp/snapshot_before.sha256 ../tmp/snapshot_after.sha256 && echo "ARTIFACTS IDENTICAL TO BEFORE"; find ledgerguard -name "*.pyc" -newer ../tmp/snapshot_before.sha256 | head -1 >/dev/null; find ledgerguard/evaluation -newer ../tmp/snapshot_before.sha256 -type f | head
```

**Result:**
```
ARTIFACTS IDENTICAL TO BEFORE
ledgerguard/evaluation/__pycache__/scale.cpython-314.pyc
ledgerguard/evaluation/__pycache__/replay.cpython-314.pyc
ledgerguard/evaluation/__pycache__/benchmark.cpython-314.pyc
ledgerguard/evaluation/__pycache__/report.cpython-314.pyc
ledgerguard/evaluation/__pycache__/drift.cpython-314.pyc
ledgerguard/evaluation/__pycache__/ablation.cpython-314.pyc
ledgerguard/evaluation/__pycache__/calibration.cpython-314.pyc
ledgerguard/evaluation/__pycache__/cost.cpython-314.pyc
ledgerguard/evaluation/__pycache__/__init__.cpython-314.pyc
ledgerguard/evaluation/__pycache__/metrics.cpython-314.pyc
```

**Agent:** Checksums match the pre-change state. Since the test suite could also write into `outputs/`, I'll run it one more time and re-verify, and check that the `__pycache__` directories are ignored.

**Bash:**
```
cat .gitignore; .venv/bin/python -m pytest ledgerguard/tests -q 2>&1 | tail -2; find ledgerguard/evaluation/outputs ledgerguard/evaluation/frozen -type f -exec shasum -a 256 {} \; | sort > ../tmp/snapshot_final.sha256 && diff ../tmp/snapshot_before.sha256 ../tmp/snapshot_final.sha256 && echo "ARTIFACTS STILL IDENTICAL"; .venv/bin/python -m pyflakes --version >/dev/null 2>&1 && .venv/bin/python -m pyflakes ledgerguard/tests/test_settlement_status.py ledgerguard/reconciliation/matcher.py ledgerguard/ledger/shadow_ledger.py || echo "(pyflakes unavailable)"
```

**Result:**
```
.venv/
__pycache__/
*.pyc
.env
.pytest_cache/
.DS_Store
-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
83 passed, 1 warning in 4.27s
ARTIFACTS STILL IDENTICAL
(pyflakes unavailable)
```

**Agent:** All 83 tests pass and the artifacts are back to their pre-change checksums. Last step: record the choices and caveats in `../out/NOTES.md`.

**Write:**
```
<attempt>/out/NOTES.md
```

**Result (error):**
```
EPERM: operation not permitted, open '<attempt>'
```

**Agent:** Wrong path: `../out` from the repo is `work/out`, not `M-T2-04/out`. Retrying at the correct location.

**Bash:**
```
ls -la <attempt>/work/ && mkdir -p <attempt>/work/out && ls -la <attempt>/work/out
```

**Result:**
```
total 0
drwxr-xr-x@  5 user  staff  160 Nov  1 23:13 .
drwxr-xr-x@ 10 user  staff  320 Nov  1 23:14 ..
drwxr-xr-x@  2 user  staff   64 Nov  1 23:13 out
drwxr-xr-x@ 11 user  staff  352 Nov  1 23:15 repo
drwxr-xr-x@ 10 user  staff  320 Nov  1 23:17 tmp
total 0
drwxr-xr-x@ 2 user  staff   64 Nov  1 23:13 .
drwxr-xr-x@ 5 user  staff  160 Nov  1 23:13 ..
```

**Write:**
```
<attempt>/work/out/NOTES.md
```

**Result:**
```
File created successfully at: <attempt>/work/out/NOTES.md (file state is current in your context — no need to Read it back)
```

**Agent:** Settlement status is now respected: only `processed` settlements can settle a payment, and the new evidence key is in place. The full suite passes (83 tests: the 67 existing tests, unmodified, plus 16 new ones).

**What changed**
- **`ledger/shadow_ledger.py`**: only processed settlements go into the index that `settlements_for()` reads. Pending and failed ones go into a separate index used only for evidence. Bank matching only ever looks up the processed settlement's reference, so it is covered too.
- **`reconciliation/matcher.py`**:
  - Settlement duplicate and conflict detection runs over processed settlements only.
  - A payment with no processed settlement is still `EXCEPTION_MISSING_SETTLEMENT` with the same values and state. When non-processed settlements exist, its evidence gains `non_processed_settlements`, sorted by `settlement_id`. The key is absent otherwise.
- **`tests/test_settlement_status.py`**: 16 new tests. They cover each requirement, and the end-to-end test uses a spy provider to confirm the investigator is never called and nothing is auto-resolved.

No changes were needed to the investigator, safety gate or pipeline, because `MISSING_SETTLEMENT` already routes to human review.

**Choices I made** (also in `../out/NOTES.md`)
- Payment-level duplicate cases now attach only processed settlements. Previously a pending or failed settlement's id could appear in their `transaction_ids`. This only affects batches with non-processed settlements.
- The `reason` text is unchanged in the missing-settlement case, so the new key is the only addition.

**Benchmark (requirement 6)**
- All 81 settlements in the regenerated frozen holdout are `processed`, so the new filters change nothing there.
- The deterministic outputs (`reconciliation_report.csv`, `decision_log.json`, `evidence_ledger.csv`) are byte-identical after regeneration, and the rules-only baseline metrics match.
- The hybrid numbers (`benchmark.json`, `cases.json`, `unresolved_exceptions.csv`) did not reproduce here. With no API key the run fell back to the heuristic provider (15 model calls became 0; accuracy 0.9765 became 1.0). The inputs are unchanged, so this is most likely the provider, but I did not re-run the pre-change code under the same conditions to prove it.

**Artifacts**: I regenerated the benchmark to compare, then restored `outputs/` and `frozen/` from a snapshot. SHA-256 checksums match the pre-change state after the final test run. The repo is not under git, so nothing was committed.
