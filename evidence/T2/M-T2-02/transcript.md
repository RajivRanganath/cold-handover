# M-T2-02 transcript (PASS)

**Agent:** I'll start with the handover documentation at the repository root, as the task requires.

**Bash:**
```
ls -la && find . -path ./.venv -prune -o -type f -print | grep -v __pycache__ | grep -v '\.git/' | head -200
```

**Result:**
```
total 88
drwxr-xr-x@ 10 user  staff    320 Nov  1 23:28 .
drwxr-xr-x@  5 user  staff    160 Nov  1 23:28 ..
-rw-r--r--@  1 user  staff   1992 Nov  1 23:28 .env.example
-rw-r--r--@  1 user  staff     56 Nov  1 23:28 .gitignore
drwxr-xr-x@  7 user  staff    224 Nov  1 23:28 .venv
drwxr-xr-x@  7 user  staff    224 Nov  1 23:28 docs
drwxr-xr-x@ 14 user  staff    448 Nov  1 23:28 ledgerguard
-rw-r--r--@  1 user  staff  26848 Nov  1 23:28 README.md
-rw-r--r--@  1 user  staff    466 Nov  1 23:28 requirements.txt
-rwxr-xr-x@  1 user  staff   1447 Nov  1 23:28 run_demo.sh
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

**Read:**
```
<attempt>/work/repo/README.md
```

**Read:**
```
<attempt>/work/repo/ledgerguard/reconciliation/matcher.py
```

**Result:**
```
1	"""Deterministic reconciliation engine.
2	
3	Ordinary software runs first. Exact identifier matching, exact settlement
4	arithmetic against the Shadow Ledger, duplicate detection, timing windows and
5	bank matching all happen here. Anything provable at this layer never reaches
6	the model.
7	
8	The matcher produces exactly one case per captured payment.
9	"""
10	
11	from __future__ import annotations
12	
13	from dataclasses import dataclass, field
14	
15	from ..ledger.invariants import InvariantResult, check_all
16	from ..ledger.models import (
17	    Batch,
18	    ExceptionType,
19	    Payment,
20	    PaymentStatus,
21	    ReconciliationException,
22	    Settlement,
23	)
24	from ..ledger.shadow_ledger import ExpectedSettlement, ShadowLedger
25	from .exceptions import make_exception
26	
27	MATCHED = "MATCHED"
28	
29	
30	@dataclass
31	class CaseResult:
32	    case_id: str
33	    payment_id: str
34	    order_id: str | None
35	    status: str                                  # MATCHED or an ExceptionType value
36	    expected: ExpectedSettlement
37	    settlement: Settlement | None
38	    invariants: list[InvariantResult] = field(default_factory=list)
39	    exception: ReconciliationException | None = None
40	
41	    @property
42	    def is_exception(self) -> bool:
43	        return self.status != MATCHED
44	
45	    def failing_invariants(self) -> list[InvariantResult]:
46	        return [i for i in self.invariants if not i.holds]
47	
48	
49	@dataclass
50	class BatchDuplicates:
51	    payment_ids: set[str] = field(default_factory=set)
52	    settlement_ids: set[str] = field(default_factory=set)
53	    bank_signatures: dict[tuple, list[str]] = field(default_factory=dict)
54	    #: Ids that appear more than once carrying *different* content. Sharing an
55	    #: identifier is not the same finding as being the same record, and the two
56	    #: must not resolve the same way -- see ``_id_groups``.
57	    payment_conflicts: set[str] = field(default_factory=set)
58	    settlement_conflicts: set[str] = field(default_factory=set)
59	
60	
61	def _payment_signature(p: Payment) -> tuple:
62	    """Everything about a payment except its identifier."""
63	    return (
64	        p.order_id,
65	        p.amount,
66	        p.currency,
67	        p.status,
68	        p.method,
69	        p.captured_at,
70	        p.fee,
71	        p.tax,
72	        p.reference,
73	    )
74	
75	
76	def _settlement_signature(s: Settlement) -> tuple:
77	    """Everything about a settlement except its identifier."""
78	    return (
79	        s.merchant_id,
80	        s.gross_amount,
81	        s.fees,
82	        s.tax,
83	        s.refund_adjustments,
84	        s.other_adjustments,
85	        s.net_amount,
86	        s.settlement_date,
87	        s.status,
88	        s.reference,
89	        tuple(s.payment_ids),
90	    )
91	
92	
93	def _id_groups(records, key, signature) -> tuple[set[str], set[str]]:
94	    """Split repeated identifiers into true duplicates and content conflicts.
95	
96	    A record ingested twice is a duplicate: the identifier and every other
97	    field agree, so suppressing the second copy is provable. Two records that
98	    share an identifier but disagree on content are *not* a duplicate -- they
99	    are two contradictory versions of the same entity, and which one is real
100	    cannot be proved from the batch. Collapsing them would close a case on a
101	    content match that never happened.
102	    """
103	    by_id: dict[str, list[tuple]] = {}
104	    for record in records:
105	        by_id.setdefault(key(record), []).append(signature(record))
106	    duplicates, conflicts = set(), set()
107	    for record_id, signatures in by_id.items():
108	        if len(signatures) < 2:
109	            continue
110	        if len(set(signatures)) == 1:
111	            duplicates.add(record_id)
112	        else:
113	            conflicts.add(record_id)
114	    return duplicates, conflicts
115	
116	
117	def find_duplicates(batch: Batch) -> BatchD
... [13344 more characters in transcript.jsonl]
```

**Read:**
```
<attempt>/work/repo/ledgerguard/ledger/invariants.py
```

**Result:**
```
1	"""Explicit Shadow Ledger invariants.
2	
3	Each invariant is a named, independently testable predicate over a
4	(payment, expected settlement, observed settlement) triple. Nothing here is
5	heuristic and nothing here consults the AI.
6	"""
7	
8	from __future__ import annotations
9	
10	from dataclasses import dataclass
11	from datetime import timedelta
12	
13	from .models import BankEntry, CreditDebit, Payment, Settlement
14	from .money import gst_on_fee, platform_fee
15	from .shadow_ledger import BANK_CREDIT_TOLERANCE_DAYS, ExpectedSettlement
16	
17	
18	@dataclass(frozen=True)
19	class InvariantResult:
20	    name: str
21	    holds: bool
22	    expected: int | str | None
23	    observed: int | str | None
24	    detail: str
25	
26	    @property
27	    def difference(self) -> int | None:
28	        if isinstance(self.expected, int) and isinstance(self.observed, int):
29	            return self.expected - self.observed
30	        return None
31	
32	    def as_dict(self) -> dict:
33	        return {
34	            "name": self.name,
35	            "holds": self.holds,
36	            "expected": self.expected,
37	            "observed": self.observed,
38	            "difference": self.difference,
39	            "detail": self.detail,
40	        }
41	
42	
43	# I1 -------------------------------------------------------------------------
44	def settlement_arithmetic_consistent(s: Settlement) -> InvariantResult:
45	    """gross - fees - tax - refund_adjustments + other_adjustments == net."""
46	    derived = (
47	        s.gross_amount - s.fees - s.tax - s.refund_adjustments + s.other_adjustments
48	    )
49	    return InvariantResult(
50	        name="I1_settlement_arithmetic_consistent",
51	        holds=derived == s.net_amount,
52	        expected=derived,
53	        observed=s.net_amount,
54	        detail=(
55	            f"{s.settlement_id}: gross {s.gross_amount} - fees {s.fees} - tax {s.tax} "
56	            f"- refunds {s.refund_adjustments} + adj {s.other_adjustments} "
57	            f"= {derived}, reported net {s.net_amount}"
58	        ),
59	    )
60	
61	
62	# I2 -------------------------------------------------------------------------
63	def fees_and_tax_match_schedule(s: Settlement) -> InvariantResult:
64	    """Reported fees and tax equal the independently computed fee schedule."""
65	    exp_fee = platform_fee(s.gross_amount)
66	    exp_tax = gst_on_fee(exp_fee)
67	    holds = s.fees == exp_fee and s.tax == exp_tax
68	    return InvariantResult(
69	        name="I2_fees_and_tax_match_schedule",
70	        holds=holds,
71	        expected=exp_fee + exp_tax,
72	        observed=s.fees + s.tax,
73	        detail=(
74	            f"{s.settlement_id}: expected fee {exp_fee} + tax {exp_tax}, "
75	            f"observed fee {s.fees} + tax {s.tax}"
76	        ),
77	    )
78	
79	
80	# I3 -------------------------------------------------------------------------
81	def net_matches_shadow_ledger(
82	    expected: ExpectedSettlement, s: Settlement
83	) -> InvariantResult:
84	    """Observed settlement net equals the Shadow Ledger's reconstructed net."""
85	    return InvariantResult(
86	        name="I3_net_matches_shadow_ledger",
87	        holds=expected.net_amount == s.net_amount,
88	        expected=expected.net_amount,
89	        observed=s.net_amount,
90	        detail=(
91	            f"{s.settlement_id}: shadow ledger expects net {expected.net_amount} "
92	            f"for payment {expected.payment_id}, provider reported {s.net_amount}"
93	        ),
94	    )
95	
96	
97	# I4 -------------------------------------------------------------------------
98	def gross_matches_capture(expected: ExpectedSettlement, s: Settlement) -> InvariantResult:
99	    """Settlement gross equals the captured payment amount."""
100	    return InvariantResult(
101	        name="I4_gross_matches_capture",
102	        holds=expected.gross_amount == s.gross_amount,
103	        expected=expected.gross_amount,
104	        observed=s.gross_amount,
105
... [4169 more characters in transcript.jsonl]
```

**Result:**
```
1	# LedgerGuard
2	
3	**A self verifying AI finance controller.** Razorpay AI Buildathon, Track 04.
4	
5	The workflow is settlement reconciliation: inspect the source records, verify an
6	ambiguous refund, and export the exceptions that still need a human.
7	
8	I built LedgerGuard to answer a question that a reconciliation chatbot does not
9	answer: an LLM can generate a plausible explanation for a financial discrepancy
10	in about two seconds — but how do you know whether that explanation is
11	*financially true*?
12	
13	**The core claim: LLM reasoning is not financial truth. Financial truth is
14	deterministic accounting state plus verified evidence. The AI may propose, the
15	financial system must prove.**
16	
17	## Quick start
18	
19	```bash
20	git clone https://github.com/RajivRanganath/ledgerguard.git && cd ledgerguard
21	python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
22	./run_demo.sh          # tests, then benchmark, then http://127.0.0.1:8137
23	```
24	
25	**No API key is needed.** Without one the AI investigation step degrades to an
26	offline stand-in and says so on the page; the deterministic engine, Shadow
27	Ledger, Evidence Gate, benchmark and dashboard all run unchanged.
28	
29	---
30	
31	## Where to verify each published requirement
32	
33	Track 04, AI Finance Controller, checked against the official Buildathon page.
34	The official description does not mandate multiple agents, a particular frontend
35	framework, or a Razorpay payment API integration. Synthetic settlement
36	reconciliation is the chosen workflow, and no payment is ever initiated.
37	
38	| Published requirement | Where to verify it |
39	|---|---|
40	| One finance-operations loop | Dashboard: records → investigation → checks → disposition → exception report |
41	| At least 50 synthetic records | 320 generated lifecycles; 85 held out and frozen for the benchmark |
42	| Match rate | `evaluation/outputs/benchmark.json` — `baseline.match_rate`, `hybrid.match_rate` |
43	| Throughput and measured accuracy | Same artifact; wall-clock figures include provider latency |
44	| Exceptions that could not be resolved | Dashboard exception queue, and `evaluation/outputs/unresolved_exceptions.csv` |
45	| Architecture | [`docs/architecture.md`](docs/architecture.md) |
46	
47	---
48	
49	## What it does
50	
51	LedgerGuard reconciles orders, payments, refunds, settlements and bank records.
52	
53	1. **The Shadow Ledger** independently reconstructs what the money movement
54	   *should* have been, from first principles:
55	   `expected_net = captured − refunds − fees − tax ± valid adjustments`.
56	   It never reads settlement or bank records to decide what to expect. Six named
57	   invariants (`I1`–`I6`) compare that reconstruction against what the provider
58	   actually reported. All money is integer paise; no float ever touches it.
59	
60	2. **A deterministic engine reconciles everything it can prove** — exact
61	   identifier matching, settlement arithmetic against the fee schedule,
62	   duplicate detection, timing windows, bank matching. On the frozen holdout it
63	   resolves 54 of 85 cases with zero AI involvement, and never sends a case to
64	   the model that it could prove on its own.
65	
66	3. **The AI investigator only sees what could not be proved.** It gets the
67	   records, the Shadow Ledger's expected value, the discrepancy, the permitted
68	   hypothesis taxonomy, and candidate related records. It returns structured
69	   JSON only. It is instructed not to calculate money; its prose is not used for
70	   monetary computation. It has no record-editing or case-closing tools.
71	
72	4. **The Evidence Gate re-proves every claim.** If the model says a shortfall is
73	   a partial refund, the gate checks whether that refund exists, whether it is
74	   already owned by another payment, whether its reference identifies *this*
75	   order's customer, whether the amount matches, whether the timing is possible,
76	   and whether re-running
... [24789 more characters in transcript.jsonl]
```

**Read:**
```
<attempt>/work/repo/ledgerguard/ledger/models.py
```

**Result:**
```
1	"""Financial data model.
2	
3	All money fields are integer paise (see ledger/money.py). Pydantic models are
4	used so that ingestion of external / malformed data fails loudly rather than
5	silently producing a wrong ledger.
6	"""
7	
8	from __future__ import annotations
9	
10	from datetime import datetime
11	from enum import Enum
12	from typing import Optional
13	
14	from pydantic import BaseModel, ConfigDict, Field
15	
16	
17	class OrderStatus(str, Enum):
18	    CREATED = "created"
19	    PAID = "paid"
20	    ATTEMPTED = "attempted"
21	
22	
23	class PaymentStatus(str, Enum):
24	    CAPTURED = "captured"
25	    AUTHORIZED = "authorized"
26	    FAILED = "failed"
27	    REFUNDED = "refunded"
28	
29	
30	class RefundStatus(str, Enum):
31	    PROCESSED = "processed"
32	    PENDING = "pending"
33	    FAILED = "failed"
34	
35	
36	class SettlementStatus(str, Enum):
37	    PROCESSED = "processed"
38	    PENDING = "pending"
39	    FAILED = "failed"
40	
41	
42	class CreditDebit(str, Enum):
43	    CREDIT = "credit"
44	    DEBIT = "debit"
45	
46	
47	class _Record(BaseModel):
48	    model_config = ConfigDict(extra="forbid", frozen=False)
49	
50	
51	class Order(_Record):
52	    order_id: str
53	    merchant_id: str
54	    amount: int                      # paise
55	    currency: str = "INR"
56	    created_at: datetime
57	    status: OrderStatus = OrderStatus.PAID
58	    customer_reference: str
59	
60	
61	class Payment(_Record):
62	    payment_id: str
63	    order_id: Optional[str]
64	    amount: int                      # paise, captured amount
65	    currency: str = "INR"
66	    status: PaymentStatus = PaymentStatus.CAPTURED
67	    method: str = "upi"
68	    captured_at: Optional[datetime]
69	    fee: int                         # paise, platform fee charged
70	    tax: int                         # paise, GST on fee
71	    reference: str
72	
73	
74	class Refund(_Record):
75	    refund_id: str
76	    payment_id: Optional[str]        # may be absent -> "orphan" refund
77	    amount: int                      # paise
78	    status: RefundStatus = RefundStatus.PROCESSED
79	    created_at: datetime
80	    reference: str
81	
82	
83	class Settlement(_Record):
84	    settlement_id: str
85	    merchant_id: str
86	    payment_ids: list[str] = Field(default_factory=list)
87	    gross_amount: int                # paise, sum of captured payments
88	    fees: int                        # paise
89	    tax: int                         # paise
90	    refund_adjustments: int          # paise, positive number that is deducted
91	    other_adjustments: int = 0       # paise, signed
92	    net_amount: int                  # paise, as reported by the provider
93	    settlement_date: datetime
94	    status: SettlementStatus = SettlementStatus.PROCESSED
95	    reference: str
96	
97	
98	class BankEntry(_Record):
99	    bank_entry_id: str
100	    amount: int                      # paise, always positive
101	    credit_or_debit: CreditDebit = CreditDebit.CREDIT
102	    date: datetime
103	    reference: str
104	    description: str = ""
105	
106	
107	class ExceptionType(str, Enum):
108	    MISSING_SETTLEMENT = "EXCEPTION_MISSING_SETTLEMENT"
109	    DUPLICATE_RECORD = "EXCEPTION_DUPLICATE_RECORD"
110	    FEE_MISMATCH = "EXCEPTION_FEE_MISMATCH"
111	    UNEXPLAINED_SHORTFALL = "EXCEPTION_UNEXPLAINED_SHORTFALL"
112	    DELAYED_SETTLEMENT = "EXCEPTION_DELAYED_SETTLEMENT"
113	    BANK_MISMATCH = "EXCEPTION_BANK_MISMATCH"
114	    AMBIGUOUS_REFERENCE = "EXCEPTION_AMBIGUOUS_REFERENCE"
115	
116	
117	class ExceptionStatus(str, Enum):
118	    OPEN = "OPEN"
119	    AUTO_RESOLVED = "AUTO_RESOLVED"
120	    RECOMMEND_REVIEW = "RECOMMEND_REVIEW"
121	    HUMAN_REVIEW_REQUIRED = "HUMAN_REVIEW_REQUIRED"
122	    UNRESOLVED = "UNRESOLVED"
123	
124	
125	class Risk(str, Enum):
126	    LOW = "low"
127	    MEDIUM = "medium"
128	    HIGH = "high"
129	
130	
131	class ReconciliationException(_Record):
132	    exception_id: str
133	    lifecycle_id: str
134	    transaction_ids: list[str]
135	    
... [949 more characters in transcript.jsonl]
```

**Read:**
```
<attempt>/work/repo/ledgerguard/ledger/shadow_ledger.py
```

**Result:**
```
1	"""The Shadow Ledger.
2	
3	An independent reconstruction of what the financial movement *should* have
4	been, computed from first principles out of orders, payments and refunds.
5	
6	It never reads settlement or bank records to decide what to expect -- that is
7	the whole point. Settlements and bank entries are the *observed* side; the
8	Shadow Ledger is the *expected* side, and reconciliation is the comparison.
9	
10	The AI investigator can call ``expected_for_payment`` to inspect output, but
11	has no path to change how the number is produced.
12	"""
13	
14	from __future__ import annotations
15	
16	from dataclasses import dataclass, field
17	from datetime import datetime, timedelta
18	
19	from .models import (
20	    Batch,
21	    BankEntry,
22	    Order,
23	    Payment,
24	    PaymentStatus,
25	    Refund,
26	    RefundStatus,
27	    Settlement,
28	)
29	from .money import gst_on_fee, platform_fee
30	
31	# Provider settlement window: money captured on day T is expected to settle on
32	# T+2, and we allow a one day tolerance either side for weekends/holidays.
33	SETTLEMENT_LAG_DAYS = 2
34	SETTLEMENT_WINDOW_TOLERANCE_DAYS = 1
35	
36	# Bank credit is expected on the settlement date, allowing one day of float.
37	BANK_CREDIT_TOLERANCE_DAYS = 1
38	
39	
40	@dataclass(frozen=True)
41	class ExpectedSettlement:
42	    """What the Shadow Ledger says a payment should settle for."""
43	
44	    payment_id: str
45	    gross_amount: int
46	    fees: int
47	    tax: int
48	    refund_adjustments: int
49	    other_adjustments: int
50	    net_amount: int
51	    refund_ids: tuple[str, ...] = ()
52	    window_start: datetime | None = None
53	    window_end: datetime | None = None
54	
55	    def as_dict(self) -> dict:
56	        return {
57	            "payment_id": self.payment_id,
58	            "gross_amount": self.gross_amount,
59	            "fees": self.fees,
60	            "tax": self.tax,
61	            "refund_adjustments": self.refund_adjustments,
62	            "other_adjustments": self.other_adjustments,
63	            "net_amount": self.net_amount,
64	            "refund_ids": list(self.refund_ids),
65	        }
66	
67	
68	@dataclass
69	class ShadowLedger:
70	    """Indexes a batch and computes expected financial movement."""
71	
72	    batch: Batch
73	    orders_by_id: dict[str, Order] = field(default_factory=dict)
74	    payments_by_id: dict[str, Payment] = field(default_factory=dict)
75	    refunds_by_id: dict[str, Refund] = field(default_factory=dict)
76	    refunds_by_payment: dict[str, list[Refund]] = field(default_factory=dict)
77	    settlements_by_payment: dict[str, list[Settlement]] = field(default_factory=dict)
78	    bank_by_reference: dict[str, list[BankEntry]] = field(default_factory=dict)
79	    orphan_refunds: list[Refund] = field(default_factory=list)
80	
81	    def __post_init__(self) -> None:
82	        self._index()
83	
84	    def _index(self) -> None:
85	        for o in self.batch.orders:
86	            self.orders_by_id.setdefault(o.order_id, o)
87	        for p in self.batch.payments:
88	            self.payments_by_id.setdefault(p.payment_id, p)
89	        for r in self.batch.refunds:
90	            self.refunds_by_id.setdefault(r.refund_id, r)
91	            if r.payment_id:
92	                self.refunds_by_payment.setdefault(r.payment_id, []).append(r)
93	            else:
94	                self.orphan_refunds.append(r)
95	        for s in self.batch.settlements:
96	            for pid in s.payment_ids:
97	                self.settlements_by_payment.setdefault(pid, []).append(s)
98	        for b in self.batch.bank_entries:
99	            self.bank_by_reference.setdefault(b.reference, []).append(b)
100	
101	    # ---------------------------------------------------------------- expected
102	
103	    def valid_refunds_for(self, payment_id: str) -> list[Refund]:
104	        """Refunds that are *provably* linked to this payment and processed."""
105	        return [
106	            r
107	            for r 
... [3712 more characters in transcript.jsonl]
```

**Read:**
```
<attempt>/work/repo/ledgerguard/reconciliation/exceptions.py
```

**Result:**
```
1	"""Exception construction and the exception taxonomy exposed to the AI."""
2	
3	from __future__ import annotations
4	
5	from ..ledger.models import ExceptionType, ReconciliationException, Risk
6	
7	#: The only hypotheses the AI investigator is permitted to return.
8	PERMITTED_HYPOTHESES = [
9	    "unlinked_partial_refund",
10	    "fee_or_tax_variance",
11	    "duplicate_deduction",
12	    "timing_difference",
13	    "unexplained_deduction",
14	    "insufficient_evidence",
15	]
16	
17	#: Exception types the deterministic engine can already prove the cause of.
18	#: These never reach the AI investigator.
19	DETERMINISTICALLY_PROVEN = {
20	    ExceptionType.MISSING_SETTLEMENT,
21	    ExceptionType.DUPLICATE_RECORD,
22	    ExceptionType.FEE_MISMATCH,
23	    ExceptionType.DELAYED_SETTLEMENT,
24	}
25	
26	#: Exception types that are genuinely ambiguous and warrant investigation.
27	NEEDS_INVESTIGATION = {
28	    ExceptionType.UNEXPLAINED_SHORTFALL,
29	    ExceptionType.AMBIGUOUS_REFERENCE,
30	    ExceptionType.BANK_MISMATCH,
31	}
32	
33	#: Which hypotheses have an evidence battery that actually explains a given
34	#: exception type.
35	#:
36	#: Verifying a hypothesis against the records is necessary but not sufficient:
37	#: a battery can pass while explaining the wrong discrepancy. The refund
38	#: battery reconstructs the *settlement* net (E7), so it can prove an
39	#: UNEXPLAINED_SHORTFALL. It says nothing about why a *bank* credit disagrees
40	#: with a settlement, so it must never close a BANK_MISMATCH -- otherwise a
41	#: coincidentally-matching orphan refund could auto-resolve a bank-side fault
42	#: on evidence that never addressed it.
43	ADMISSIBLE_HYPOTHESES: dict[ExceptionType, set[str]] = {
44	    ExceptionType.UNEXPLAINED_SHORTFALL: {"unlinked_partial_refund"},
45	    ExceptionType.BANK_MISMATCH: set(),
46	    ExceptionType.AMBIGUOUS_REFERENCE: set(),
47	}
48	
49	_RISK_BY_TYPE = {
50	    ExceptionType.MISSING_SETTLEMENT: Risk.HIGH,
51	    ExceptionType.UNEXPLAINED_SHORTFALL: Risk.HIGH,
52	    ExceptionType.BANK_MISMATCH: Risk.HIGH,
53	    ExceptionType.DUPLICATE_RECORD: Risk.MEDIUM,
54	    ExceptionType.FEE_MISMATCH: Risk.MEDIUM,
55	    ExceptionType.AMBIGUOUS_REFERENCE: Risk.MEDIUM,
56	    ExceptionType.DELAYED_SETTLEMENT: Risk.LOW,
57	}
58	
59	
60	def make_exception(
61	    *,
62	    case_id: str,
63	    lifecycle_id: str,
64	    transaction_ids: list[str],
65	    exception_type: ExceptionType,
66	    detected_by: str,
67	    expected_value: int | None,
68	    observed_value: int | None,
69	    evidence: dict,
70	) -> ReconciliationException:
71	    difference = None
72	    if expected_value is not None and observed_value is not None:
73	        difference = expected_value - observed_value
74	    return ReconciliationException(
75	        exception_id=f"EXC-{case_id}",
76	        lifecycle_id=lifecycle_id,
77	        transaction_ids=transaction_ids,
78	        exception_type=exception_type,
79	        detected_by=detected_by,
80	        expected_value=expected_value,
81	        observed_value=observed_value,
82	        difference=difference,
83	        evidence=evidence,
84	        risk=_RISK_BY_TYPE.get(exception_type, Risk.MEDIUM),
85	    )
86	
```

**Read:**
```
<attempt>/work/repo/ledgerguard/pipeline.py
```

**Result:**
```
1	"""End to end controller run.
2	
3	    deterministic reconciliation
4	      -> AI investigation, but only for what could not be proved
5	      -> Evidence Gate
6	      -> uniqueness pass
7	      -> safety and action gate
8	
9	Running with ``use_ai=False`` gives the rules-only baseline: identical
10	deterministic layer, no investigation step. That is the comparison the
11	benchmark makes.
12	"""
13	
14	from __future__ import annotations
15	
16	import time
17	from dataclasses import dataclass, field
18	
19	from .ai.investigator import Investigation, investigate_case, should_investigate
20	from .ai.provider import InvestigatorProvider, UnavailableProvider, get_provider
21	from .ai.schemas import InvestigationResult
22	from .evidence.safety import Decision, HUMAN_REVIEW_REQUIRED, decide
23	from .evidence.verifier import (
24	    VerificationOutcome,
25	    resolve_evidence_conflicts,
26	    verify,
27	)
28	from .ledger.models import Batch
29	from .ledger.shadow_ledger import ShadowLedger
30	from .reconciliation.matcher import CaseResult, reconcile_batch
31	
32	
33	@dataclass
34	class CaseOutcome:
35	    case: CaseResult
36	    investigation: Investigation | None = None
37	    verification: VerificationOutcome | None = None
38	    decision: Decision | None = None
39	
40	    @property
41	    def case_id(self) -> str:
42	        return self.case.case_id
43	
44	    @property
45	    def state(self) -> str:
46	        if not self.case.is_exception:
47	            return "MATCHED"
48	        return self.decision.state if self.decision else HUMAN_REVIEW_REQUIRED
49	
50	    @property
51	    def exposure_paise(self) -> int:
52	        exc = self.case.exception
53	        if exc is None or exc.difference is None:
54	            return 0
55	        return abs(exc.difference)
56	
57	
58	@dataclass
59	class RunReport:
60	    system: str
61	    provider_name: str
62	    outcomes: list[CaseOutcome] = field(default_factory=list)
63	    ledger: ShadowLedger | None = None
64	    wall_seconds: float = 0.0
65	    investigations: int = 0
66	    model_calls: int = 0
67	    investigation_latencies_ms: list[float] = field(default_factory=list)
68	
69	    def by_case_id(self) -> dict[str, CaseOutcome]:
70	        return {o.case_id: o for o in self.outcomes}
71	
72	
73	def _accept_without_proof(case: CaseResult, result: InvestigationResult) -> VerificationOutcome:
74	    """The ablation stand-in for the Evidence Gate: believe the investigator.
75	
76	    Used only by the ablation study, to measure what the gate is actually
77	    preventing. It records zero checks, so nothing about it can be mistaken for
78	    verification after the fact.
79	    """
80	    from .evidence.verifier import UNVERIFIED, VERIFIED
81	
82	    trusted = result.hypothesis != "insufficient_evidence" and result.source in (
83	        "model",
84	        "heuristic_stub",
85	    )
86	    return VerificationOutcome(
87	        case_id=case.case_id,
88	        hypothesis=result.hypothesis,
89	        verdict=VERIFIED if trusted else UNVERIFIED,
90	        checks=[],
91	        claimed_evidence_ids=list(result.candidate_evidence_ids),
92	        note="ABLATION: Evidence Gate disabled; the investigator was taken at its word",
93	    )
94	
95	
96	def run(
97	    batch: Batch,
98	    use_ai: bool = True,
99	    provider: InvestigatorProvider | None = None,
100	    lifecycle_by_payment: dict[str, str] | None = None,
101	    use_evidence_gate: bool = True,
102	) -> RunReport:
103	    started = time.perf_counter()
104	    cases, ledger = reconcile_batch(batch, lifecycle_by_payment)
105	
106	    if use_ai:
107	        provider = provider or get_provider()
108	    else:
109	        provider = UnavailableProvider("rules-only baseline: AI investigation disabled")
110	
111	    outcomes: list[CaseOutcome] = []
112	    verifications: dict[str, VerificationOutcome] = {}
113	    investigations = 0
114	    model_calls = 0
115	    latencies: list[float] = []
116	
117	    for case in cases:
118	        i
... [2861 more characters in transcript.jsonl]
```

**Read:**
```
<attempt>/work/repo/ledgerguard/evidence/safety.py
```

**Result:**
```
1	"""Safety and action gate.
2	
3	Turns a verification outcome into one of four states. The bias is deliberate:
4	abstention is a correct answer, and the gate is not scored on how many
5	exceptions it closes.
6	
7	"Auto resolved" here means the reconciliation exception is classified and
8	closed inside LedgerGuard. It never means money moves.
9	"""
10	
11	from __future__ import annotations
12	
13	from dataclasses import dataclass
14	
15	from ..ai.schemas import InvestigationResult
16	from ..ledger.models import ExceptionStatus, ExceptionType
17	from ..ledger.money import to_rupees_str
18	from ..reconciliation.matcher import CaseResult
19	from .verifier import REJECTED, UNVERIFIED, VERIFIED, VerificationOutcome
20	
21	AUTO_RESOLVED = ExceptionStatus.AUTO_RESOLVED.value
22	RECOMMEND_REVIEW = ExceptionStatus.RECOMMEND_REVIEW.value
23	HUMAN_REVIEW_REQUIRED = ExceptionStatus.HUMAN_REVIEW_REQUIRED.value
24	UNRESOLVED = ExceptionStatus.UNRESOLVED.value
25	
26	#: Exception types the deterministic layer proves outright: the cause is known
27	#: exactly, so the exception can be classified and closed without a human.
28	_DETERMINISTIC_AUTO_CLOSE = {
29	    ExceptionType.DUPLICATE_RECORD: "Duplicate ingestion proven by identifier and content match; the duplicate is suppressed, not paid.",
30	    ExceptionType.FEE_MISMATCH: "Fee and tax reconciled against the independent fee schedule; the exact variance is quantified.",
31	    ExceptionType.DELAYED_SETTLEMENT: "All amounts reconcile exactly; the only discrepancy is timing against the expected settlement window.",
32	}
33	
34	#: Proven, but the resolution is outside the system's authority to close.
35	_DETERMINISTIC_ESCALATE = {
36	    ExceptionType.MISSING_SETTLEMENT: "Captured funds have no settlement record. The money is outstanding; LedgerGuard cannot close this, it can only report it.",
37	}
38	
39	
40	@dataclass
41	class Decision:
42	    case_id: str
43	    state: str
44	    reason: str
45	    resolution: str | None = None
46	    missing_evidence: list[str] = None            # type: ignore[assignment]
47	    suggested_action: str = ""
48	
49	    def __post_init__(self) -> None:
50	        if self.missing_evidence is None:
51	            self.missing_evidence = []
52	
53	    @property
54	    def is_auto_resolved(self) -> bool:
55	        return self.state == AUTO_RESOLVED
56	
57	    @property
58	    def needs_human(self) -> bool:
59	        return self.state in (HUMAN_REVIEW_REQUIRED, RECOMMEND_REVIEW, UNRESOLVED)
60	
61	
62	def decide(
63	    case: CaseResult,
64	    investigation: InvestigationResult | None = None,
65	    verification: VerificationOutcome | None = None,
66	) -> Decision:
67	    exc = case.exception
68	    assert exc is not None, "decide() is only called for exceptions"
69	    exc_type = exc.exception_type
70	
71	    if (
72	        exc_type is ExceptionType.DELAYED_SETTLEMENT
73	        and exc.evidence.get("window_undecidable")
74	    ):
75	        # Amounts reconcile, but the expected settlement window could not be
76	        # computed at all, so the timing check never ran. Closing this as a
77	        # routine delay would assert a verification that did not happen.
78	        return Decision(
79	            case_id=case.case_id,
80	            state=HUMAN_REVIEW_REQUIRED,
81	            reason=(
82	                "Amounts reconcile exactly, but the payment has no capture "
83	                "timestamp, so the expected settlement window is undecidable. "
84	                "The timing check could not be run, and is not assumed to pass."
85	            ),
86	            missing_evidence=["payment.captured_at"],
87	            suggested_action=(
88	                "Recover the capture timestamp from the provider, then re-run "
89	                "reconciliation for this payment."
90	            ),
91	        )
92	
93	    conflict = exc.evidence.get("content_conflict")
94	    if conflict:
95	        # Two records share an identifier and disagree on content. "Duplic
... [7559 more characters in transcript.jsonl]
```

**Agent:** The core matching logic is clear. Next I'll find every other place that reads settlements, so no settlement-matching step is missed.

**Bash:**
```
grep -rn "settlements\|Settlement\b\|SettlementStatus\|settlement.*status\|\.status" ledgerguard --include=*.py | grep -v "/tests/" | grep -v "^ledgerguard/synthetic" | head -120; echo ---; grep -rn "SettlementStatus\|status=" ledgerguard/synthetic ledgerguard/tests | head -60
```

**Result:**
```
(eval):1: no matches found: --include=*.py
---
ledgerguard/synthetic/generator.py:28:    SettlementStatus,
ledgerguard/synthetic/generator.py:160:            status=OrderStatus.PAID,
ledgerguard/synthetic/generator.py:170:            status=PaymentStatus.CAPTURED,
ledgerguard/synthetic/generator.py:187:                    status=RefundStatus.PROCESSED,
ledgerguard/synthetic/generator.py:208:            status=SettlementStatus.PROCESSED,
ledgerguard/tests/test_p1_extended.py:444:        status=exc.exception_type.value,
ledgerguard/tests/test_p1_extended.py:499:        status=exc.exception_type.value,
```

**Bash:**
```
grep -rn "settlements\|SettlementStatus\|settlement\.status\|s\.status" ledgerguard --include='*.py' | grep -v "tests/" ; echo ---; grep -rn "settlements_for\|settlements_by_payment" ledgerguard
```

**Result:**
```
ledgerguard/qa.py:112:def _missing_settlements(report: RunReport) -> tuple[str, list[str]]:
ledgerguard/qa.py:144:    _Query("missing_settlements", ("missing settlement", "never settled", "not settled"),
ledgerguard/qa.py:145:           "payments with no settlement", _missing_settlements),
ledgerguard/ledger/shadow_ledger.py:77:    settlements_by_payment: dict[str, list[Settlement]] = field(default_factory=dict)
ledgerguard/ledger/shadow_ledger.py:95:        for s in self.batch.settlements:
ledgerguard/ledger/shadow_ledger.py:97:                self.settlements_by_payment.setdefault(pid, []).append(s)
ledgerguard/ledger/shadow_ledger.py:162:    def settlements_for(self, payment_id: str) -> list[Settlement]:
ledgerguard/ledger/shadow_ledger.py:163:        return self.settlements_by_payment.get(payment_id, [])
ledgerguard/ledger/shadow_ledger.py:192:            "settlements": len(self.batch.settlements),
ledgerguard/reconciliation/matcher.py:87:        s.status,
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
ledgerguard/ledger/models.py:36:class SettlementStatus(str, Enum):
ledgerguard/ledger/models.py:94:    status: SettlementStatus = SettlementStatus.PROCESSED
ledgerguard/ledger/models.py:152:    settlements: list[Settlement] = Field(default_factory=list)
ledgerguard/synthetic/compound.py:115:    orders, payments, refunds, settlements, entries = [], [], [], [], []
ledgerguard/synthetic/compound.py:123:            settlements.append(s)
ledgerguard/synthetic/compound.py:199:            settlements=settlements,
ledgerguard/synthetic/adversarial.py:123:        settlements=[a_settlement, b_settlement],
ledgerguard/synthetic/generator.py:28:    SettlementStatus,
ledgerguard/synthetic/generator.py:109:            b.settlements += s
ledgerguard/synthetic/generator.py:208:            status=SettlementStatus.PROCESSED,
ledgerguard/evaluation/scale.py:58:        + len(batch.settlements) + len(batch.bank_entries)
ledgerguard/evaluation/ablation.py:173:        settlements = ledger.settlements_for(payment.payment_id)
ledgerguard/evaluation/ablation.py:174:        if not settlements:
ledgerguard/evaluation/ablation.py:177:        settlement = settlements[0]
ledgerguard/evaluation/ablation.py:201:    settlements = ledger.settlements_for(payment.payment_id)
ledgerguard/evaluation/ablation.py:202:    settlement = settlements[0] if settlements else None
ledgerguard/evaluation/ablation.py:230:        "settlements": [
ledgerguard/evaluation/ablation.py:240:            for s in settlements
ledgerguard/evaluation/ablation
... [1165 more characters in transcript.jsonl]
```

**Agent:** Settlement reads are confined to `matcher.py`, `shadow_ledger.py` and the `ablation.py` evaluation. Before changing anything I'll snapshot the protected artifacts and check which tests and evaluation scripts write to them.

**Bash:**
```
find ledgerguard/evaluation/outputs ledgerguard/evaluation/frozen -type f | sort | xargs shasum -a 256 > /tmp/ledger_artifacts_before.sha 2>/dev/null || true; mkdir -p ../tmp ../out && find ledgerguard/evaluation/outputs ledgerguard/evaluation/frozen -type f | sort | xargs shasum -a 256 > ../tmp/artifacts_before.sha; cat ../tmp/artifacts_before.sha; echo ---; grep -rln "outputs\|write_text\|open(.*'w'" ledgerguard/tests ledgerguard/evaluation | head -30; echo ---; grep -rn "MISSING_SETTLEMENT\|missing_settlement" ledgerguard/tests | head -30; echo ---; cat ../out/NOTES.md 2>/dev/null; ls ../out ../tmp
```

**Result:**
```
(eval):1: operation not permitted: /tmp/ledger_artifacts_before.sha
06f71351dd21bdcdb30705986832111987fe71ff6d6787ed2a198c88de50a53f  ledgerguard/evaluation/frozen/holdout_20260905_320.json
7ffa151674c19541ac0b4cf9a8618b4c5a8eef664afd9ab81321961848cecd03  ledgerguard/evaluation/outputs/ablation.json
fc84418ada9f206e10f07170d5c3e362c531474c13abefed04eadabf32c6cda2  ledgerguard/evaluation/outputs/ablation.md
249e3bce69daeb83386d9575e66bf4177d4db885a8864ab6b32d80b5717d8536  ledgerguard/evaluation/outputs/benchmark.json
aa667ebea4ccd41fa0bdff898182200d3bf282ef0b888cabd7b5a215d82edd22  ledgerguard/evaluation/outputs/benchmark.md
8dc1212f1c93e7c1bf34d92923c1d31f15b7096a0b39e4c2afa4e167f4eda9d4  ledgerguard/evaluation/outputs/calibration.json
bbfc6509ce38c53329da95bde380675d231fcfbb15efd4428252aae3eef32d12  ledgerguard/evaluation/outputs/calibration.md
a5552fcb48631411cb08fae4e34987295cca132334d6c31d86601f73e538455b  ledgerguard/evaluation/outputs/cases.json
c52561e7f550a9c66a045bd6aaebd91f8883f120a624bf773d2a3dfae1753c7d  ledgerguard/evaluation/outputs/decision_log.json
ac427b5c78460109ba2fb3914c2d04310e80089ea245dcf44f426bc2da5562a7  ledgerguard/evaluation/outputs/drift.json
b3ceedf8b7067eb970ee33a6f7802ea154a10aa6fcbabe903b7880a0cd5634dc  ledgerguard/evaluation/outputs/drift.md
3699ea28a60eed7b419b027283ae1a9a3875eeb7c43e674adddfc0d195aa50c1  ledgerguard/evaluation/outputs/evidence_ledger.csv
1fbca2999ea5f5b76d810ac2955beb5fca7bc5af165320a752be60dbe4b96100  ledgerguard/evaluation/outputs/model_comparison.json
b877b4cdb9f9dfc33ff7ad0e82915e3e6fad2b84ccd8e3e9170943758834ff4d  ledgerguard/evaluation/outputs/model_comparison.md
ccc33093b532b19e326ed4ac8f8d16d29645807f3fe97841a10dc7d242f57917  ledgerguard/evaluation/outputs/no_gate_ablation.json
b2aa14f8b312f1a735663b70b69137f2df190ab9ef731c51c31def8d05bd14e4  ledgerguard/evaluation/outputs/no_gate_ablation.md
c58809b7c6b57a77dd33ce948b09988c6c9ded01bacb052b2f4f9b2d5193d6d7  ledgerguard/evaluation/outputs/reconciliation_report.csv
7a9f6520bbeb849b4e6f1f15a78f39a608583c6776c7c310457ed053a82dd41c  ledgerguard/evaluation/outputs/reconciliation_report.md
530301222288c5c487d56e9029f570bd01720e1fdbd306c90b9f71c71488cd4b  ledgerguard/evaluation/outputs/scale.json
227f79916be1cbe13addb7096e2f0f453660e2dc4ef83e4081ff8bcbee2ef9cf  ledgerguard/evaluation/outputs/scale.md
af74f00254d9a8cee944bccdf9fd8940c2a318c0bfd5c6965dbfc5a221e00711  ledgerguard/evaluation/outputs/unresolved_exceptions.csv
---
ledgerguard/evaluation/benchmark.py
ledgerguard/evaluation/drift.py
ledgerguard/evaluation/no_gate_ablation.py
ledgerguard/evaluation/model_comparison.py
ledgerguard/evaluation/scale.py
ledgerguard/evaluation/calibration.py
ledgerguard/evaluation/ablation.py
ledgerguard/evaluation/replay.py
ledgerguard/evaluation/report.py
---
ledgerguard/tests/test_p1_compound.py:92:    assert outcome.case.exception.exception_type.value == "EXCEPTION_MISSING_SETTLEMENT"
ledgerguard/tests/test_p0_core.py:202:        FaultClass.F1_MISSING_SETTLEMENT: "EXCEPTION_MISSING_SETTLEMENT",
---
../out:

../tmp:
artifacts_before.sha
cc-socks
claude-501
```

**Agent:** I have the pre-change hashes saved under `../tmp/`. Next I'll check whether the frozen holdout or the generated data contains any non-processed settlements, since that determines whether requirement 6 is trivially satisfied.

**Bash:**
```
grep -o '"status": *"[a-z_]*"' ledgerguard/evaluation/frozen/holdout_20260905_320.json | sort | uniq -c; echo ---; grep -c '"settlement_id"' ledgerguard/evaluation/frozen/holdout_20260905_320.json; echo ---; sed -n 1,80p ledgerguard/evaluation/benchmark.py | head -120; echo ---; grep -n "def \|write\|OUTPUT\|outputs" ledgerguard/evaluation/benchmark.py | head -60
```

**Result:**
```
---
0
---
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


---
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
154:        writer 
... [689 more characters in transcript.jsonl]
```

**Agent:** The frozen holdout file is only a manifest (seed, count, batch hash). The generator always emits `processed` settlements, so requirement 6 should hold automatically, and I'll verify it by running the benchmark in a scratch copy. Next I'll look at the existing test helpers so the new tests follow the same style.

**Bash:**
```
cd ledgerguard/tests && grep -n "^def \|^from\|^import" test_p1_extended.py | head -80; echo ---; sed -n 1,60p test_p1_extended.py; echo ---; grep -n "def \|^from\|^import" test_p1_compound.py | head -40; echo ---; sed -n 60,110p test_p1_compound.py
```

**Result:**
```
11:from __future__ import annotations
13:from datetime import datetime, timedelta
15:import httpx
16:import pytest
17:from pydantic import ValidationError
19:from ledgerguard.ai.provider import HeuristicProvider
20:from ledgerguard.ai.schemas import (
25:from ledgerguard.evidence.safety import AUTO_RESOLVED, HUMAN_REVIEW_REQUIRED
26:from ledgerguard.ledger.models import (
35:from ledgerguard.ledger.money import gst_on_fee, platform_fee, to_paise
36:from ledgerguard.pipeline import run
37:from ledgerguard.reconciliation.matcher import MATCHED, find_duplicates, reconcile_batch
38:from ledgerguard.synthetic.fault_injector import build_dataset, split
39:from ledgerguard.synthetic.generator import FaultClass
44:def _cases_by_fault(dataset, results):
53:def test_duplicate_payment_and_bank_entry_are_both_detected():
78:def test_find_duplicates_distinguishes_id_from_content_duplication():
100:def test_a_shared_id_with_different_content_is_a_conflict_not_a_duplicate():
146:def test_two_settlements_that_disagree_are_never_collapsed_into_one():
172:def test_delayed_settlement_is_timing_only_and_never_an_amount_exception():
188:def test_settlement_window_boundaries_are_inclusive():
218:def test_generator_is_reproducible_and_the_split_is_stable():
262:def test_malformed_model_output_becomes_invalid_never_a_resolution(raw):
272:def test_fenced_json_is_recovered_and_long_reasons_are_truncated():
287:def test_investigator_output_rejects_unbounded_candidate_lists():
298:def _stub_provider(exc: Exception):
317:def test_model_timeout_degrades_to_review_and_keeps_the_batch_running():
331:def test_connection_failure_is_reported_as_transport_not_as_bad_output():
347:def test_a_provider_returning_the_wrong_type_cannot_take_down_the_batch(returned):
373:def test_malformed_records_fail_loudly_at_ingestion():
390:def test_a_payment_with_no_capture_timestamp_is_handled_not_crashed():
429:def test_unknown_exception_type_reaches_unresolved_not_a_close():
453:def test_frozen_holdout_mismatch_is_refused(tmp_path, monkeypatch):
477:def test_hypothesis_must_be_admissible_for_the_exception_it_would_close():
517:def test_a_broken_provider_is_reported_not_silently_dropped():
599:def _live_provider(url: str, timeout: float = 30.0):
613:def test_a_real_hanging_provider_times_out_and_the_batch_survives():
638:def test_a_real_malformed_response_never_becomes_a_resolution(mode):
659:def test_a_real_malformed_response_degrades_the_whole_batch_to_review():
---
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
def test_duplicate_payment_and_ba
... [2899 more characters in transcript.jsonl]
```

**Bash:**
```
cd <attempt>/work/repo && sed -n 100,190p ledgerguard/tests/test_p1_extended.py
```

**Result:**
```
def test_a_shared_id_with_different_content_is_a_conflict_not_a_duplicate():
    """The claim "proven by identifier AND content match" has to be true.

    Two rows carrying one payment_id but disagreeing on the amount are not a
    re-ingestion, they are two contradictory versions of one payment. Closing
    that as a duplicate would suppress a row on the strength of a content check
    that failed -- an unproven auto close on the deterministic path, which is
    the exact failure the whole system exists to prevent.
    """
    dataset = build_dataset()
    _dev, holdout = split(dataset)
    batch = holdout.batch()

    clean = next(
        p for p in batch.payments
        if holdout.fault_class_by_payment()[p.payment_id] == FaultClass.NONE
    )
    conflicting = clean.model_copy(update={"amount": clean.amount * 3})
    tampered = batch.model_copy(
        update={"payments": list(batch.payments) + [conflicting]}
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
    assert delayed

    for case in delayed:
        assert case.status == ExceptionType.DELAYED_SETTLEMENT.value
        failing = {i.name for i in case.failing_invariants()}
        # Only the window invariant may break. If an amount invariant also
        # broke, the classification above is hiding a real money discrepancy.
        assert failing == {"I5_settlement_within_window"}, failing
        assert case.exception.evidence["days_late"] >= 1
        assert case.exception.difference == 0, "amounts must reconcile exactly"


def test_settlement_window_boundaries_are_inclusive():
    """T+2 with one day tolerance: T+1 and T+3 hold, T+4 does not."""
    from ledgerguard.ledger.invariants import settlement_within_window
```

**Agent:** Before editing, I'll run the existing suite to get a baseline. Then I'll check whether it writes into the protected artifact directories.

**Bash:**
```
timeout 900 .venv/bin/python -m pytest ledgerguard/tests -q -p no:cacheprovider 2>&1 | tail -15; find ledgerguard/evaluation/outputs ledgerguard/evaluation/frozen -type f | sort | xargs shasum -a 256 | diff - ../tmp/artifacts_before.sha && echo ARTIFACTS_UNCHANGED
```

**Result (error):**
```
Exit code 2
(eval):1: command not found: timeout
diff: -: Operation not permitted
xargs: shasum: terminated with signal 13; aborting
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
67 passed, 1 warning in 5.17s
```

**Bash:**
```
find ledgerguard/evaluation/outputs ledgerguard/evaluation/frozen -type f | sort | xargs shasum -a 256 > ../tmp/artifacts_after_baseline.sha && cmp ../tmp/artifacts_before.sha ../tmp/artifacts_after_baseline.sha && echo ARTIFACTS_UNCHANGED
```

**Result:**
```
ARTIFACTS_UNCHANGED
```

**Agent:** Baseline is 67 passing, and the test run leaves the artifacts untouched. Now the implementation. The ledger index is the single choke point for settlement lookups, so I'll split settlements there: only `processed` ones are indexed for matching, and the others go to a separate index used only for evidence.

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

**Agent:** Next, the matcher. Duplicate detection for settlements must only see `processed` rows, and the missing-settlement branch gets the evidence key.

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

**Agent:** The core change is in. Before writing tests I need the provider interface, so I can prove the investigator is never called for these cases rather than relying on a side effect.

**Bash:**
```
grep -n "class \|def " ledgerguard/ai/provider.py | head -40; sed -n 298,320p ledgerguard/tests/test_p1_extended.py; grep -n "def should_investigate" -A12 ledgerguard/ai/investigator.py
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


def test_model_timeout_degrades_to_review_and_keeps_the_batch_running():
    from ledgerguard.synthetic.adversarial import build_adversarial_batch

    provider = _stub_provider(httpx.TimeoutException("timed out"))
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
```

**Agent:** The provider contract is `investigate(context)`, so a recording stub will prove the investigator is never reached. Now I'll write the new test file. It covers each of the seven requirements and includes a property test that appends non-processed copies to every settlement in the dataset and requires no outcome to change.

**Write:**
```
<attempt>/work/repo/ledgerguard/tests/test_t2_settlement_status.py
```

**Result:**
```
File created successfully at: <attempt>/work/repo/ledgerguard/tests/test_t2_settlement_status.py (file state is current in your context — no need to Read it back)
```

**Agent:** The file is written, but a few things need tidying: a mid-file `import pytest`, one sloppy `or`-assertion, and some unused imports. Fixing those now.

**Edit:**
```
<attempt>/work/repo/ledgerguard/tests/test_t2_settlement_status.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/tests/test_t2_settlement_status.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

**Edit:**
```
<attempt>/work/repo/ledgerguard/tests/test_t2_settlement_status.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/tests/test_t2_settlement_status.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

**Edit:**
```
<attempt>/work/repo/ledgerguard/tests/test_t2_settlement_status.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/tests/test_t2_settlement_status.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

**Edit:**
```
<attempt>/work/repo/ledgerguard/tests/test_t2_settlement_status.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/tests/test_t2_settlement_status.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

**Bash:**
```
.venv/bin/python -m pytest ledgerguard/tests/test_t2_settlement_status.py -q -p no:cacheprovider 2>&1 | tail -60
```

**Result:**
```
................                                                         [100%]
16 passed in 0.33s
```

**Agent:** All 16 new tests pass. Next I need evidence for requirement 6 (the frozen holdout is unchanged). The committed artifacts came from live model runs, so I'll check how the benchmark CLI selects a provider before comparing anything.

**Bash:**
```
sed -n 238,275p ledgerguard/evaluation/benchmark.py; grep -n "investigator\|provider" ledgerguard/evaluation/outputs/benchmark.md | head; .venv/bin/python -c "import json;d=json.load(open('ledgerguard/evaluation/outputs/benchmark.json'));print(list(d.keys())[:20])"
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

['dataset', 'holdout_manifest', 'baseline', 'hybrid', 'investigator_chain']
```

**Agent:** The baseline (rules-only) section of `benchmark.json` is fully deterministic, and the frozen holdout is generated with `processed` settlements only. So I'll run the benchmark offline (`--provider none`) on a scratch copy of the modified repo, leaving the real `outputs/` untouched, and compare its deterministic results with the committed artifacts.

**Bash:**
```
cd <attempt>/work && rm -rf ../tmp/scratch_new && mkdir -p ../tmp/scratch_new && rsync -a --exclude .venv --exclude __pycache__ repo/ ../tmp/scratch_new/ && cd ../tmp/scratch_new && env -u GROQ_API_KEY -u GEMINI_API_KEY -u NVIDIA_API_KEY -u OMNIROUTE_API_KEY <attempt>/work/repo/.venv/bin/python -m ledgerguard.evaluation.benchmark --provider none > ../tmp/scratch_new_run.log 2>&1; echo exit=$?; tail -5 ../tmp/scratch_new_run.log; cd <attempt>/work/repo && <attempt>/work/repo/.venv/bin/python - <<'EOF'
import json
old = json.load(open('ledgerguard/evaluation/outputs/benchmark.json'))
new = json.load(open('../tmp/scratch_new/ledgerguard/evaluation/outputs/benchmark.json'))
print("baseline equal:", old['baseline'] == new['baseline'])
print("dataset equal:", old['dataset'] == new['dataset'])
print("manifest equal:", old['holdout_manifest'] == new['holdout_manifest'])
print("baseline keys sample:", list(old['baseline'])[:6])
EOF
```

**Result (error):**
```
Exit code 1
mkdir: ../tmp: Operation not permitted
exit=1
tail: ../tmp/scratch_new_run.log: No such file or directory
Traceback (most recent call last):
  File "<stdin>", line 3, in <module>
FileNotFoundError: [Errno 2] No such file or directory: '../tmp/scratch_new/ledgerguard/evaluation/outputs/benchmark.json'
```

**Agent:** The relative `../tmp` resolved differently from the `work/` directory, so I'll switch to absolute paths. Nothing was written by the failed attempt.

**Bash:**
```
W=<attempt>/work; R=$W/repo; T=$W/tmp; mkdir -p $T/scratch_new && rsync -a --exclude .venv --exclude __pycache__ $R/ $T/scratch_new/ && cd $T/scratch_new && env -u GROQ_API_KEY -u GEMINI_API_KEY -u NVIDIA_API_KEY -u OMNIROUTE_API_KEY $R/.venv/bin/python -m ledgerguard.evaluation.benchmark --provider none > $T/scratch_new_run.log 2>&1; echo exit=$?; tail -3 $T/scratch_new_run.log; $R/.venv/bin/python - <<EOF
import json
old = json.load(open('$R/ledgerguard/evaluation/outputs/benchmark.json'))
new = json.load(open('$T/scratch_new/ledgerguard/evaluation/outputs/benchmark.json'))
print("baseline equal:", old['baseline'] == new['baseline'])
print("dataset equal:", old['dataset'] == new['dataset'])
print("manifest equal:", old['holdout_manifest'] == new['holdout_manifest'])
EOF
ls $W/out $T | head
```

**Result:**
```
exit=0
Artifacts written to <attempt>/work/tmp/scratch_new/ledgerguard/evaluation/outputs
  benchmark.md, benchmark.json, cases.json
  unresolved_exceptions.csv (19 rows)
baseline equal: False
dataset equal: True
manifest equal: True
<attempt>/work/out:

<attempt>/work/tmp:
artifacts_after_baseline.sha
artifacts_before.sha
cc-socks
claude-501
pytest-of-user
scratch_new
scratch_new_run.log
Shell cwd was reset to <attempt>/work/repo
```

**Agent:** The dataset and manifest match, but the rules-only baseline section differs. I need to see whether that difference is timing noise or a real behaviour change before drawing any conclusion.

**Bash:**
```
W=<attempt>/work; R=$W/repo; T=$W/tmp; $R/.venv/bin/python - <<EOF
import json
old = json.load(open('$R/ledgerguard/evaluation/outputs/benchmark.json'))['baseline']
new = json.load(open('$T/scratch_new/ledgerguard/evaluation/outputs/benchmark.json'))['baseline']
def walk(a,b,p=''):
    if type(a)!=type(b): print('TYPE',p,repr(a)[:120],repr(b)[:120]); return
    if isinstance(a,dict):
        for k in sorted(set(a)|set(b)):
            if k not in a or k not in b: print('KEY',p+'/'+k, k in a, k in b); continue
            walk(a[k],b[k],p+'/'+k)
    elif isinstance(a,list):
        if len(a)!=len(b): print('LEN',p,len(a),len(b)); return
        for i,(x,y) in enumerate(zip(a,b)): walk(x,y,p+f'[{i}]')
    elif a!=b: print('VAL',p,repr(a)[:150],'|',repr(b)[:150])
walk(old,new)
EOF
```

**Result:**
```
VAL /throughput_per_second 22395.4 | 27184.8
VAL /wall_seconds 0.004 | 0.003
```

**Agent:** Only the wall-clock timing fields differ, so the deterministic baseline is identical. Next I'll compare per-case detail, which covers the exception evidence and classification, for every case that the committed run and the new run both recorded.

**Bash:**
```
W=<attempt>/work; R=$W/repo; T=$W/tmp; $R/.venv/bin/python - <<EOF
import json
old = json.load(open('$R/ledgerguard/evaluation/outputs/cases.json'))
new = json.load(open('$T/scratch_new/ledgerguard/evaluation/outputs/cases.json'))
print(type(old), list(old.keys())[:10] if isinstance(old,dict) else len(old))
cases_o = old['cases'] if isinstance(old,dict) and 'cases' in old else old
cases_n = new['cases'] if isinstance(new,dict) and 'cases' in new else new
print(len(cases_o), len(cases_n))
print(json.dumps(cases_o[0], indent=1)[:900])
EOF
```

**Result:**
```
<class 'list'> 85
85 85
{
 "case_id": "pay_0001DA30",
 "lifecycle_id": "LC0001",
 "payment_id": "pay_0001DA30",
 "order_id": "ord_0001BE49",
 "state": "MATCHED",
 "exception_type": null,
 "expected": {
  "payment_id": "pay_0001DA30",
  "gross_amount": 228500,
  "fees": 4570,
  "tax": 823,
  "refund_adjustments": 0,
  "other_adjustments": 0,
  "net_amount": 223107,
  "refund_ids": []
 },
 "observed_settlement": null,
 "exposure_paise": 0,
 "invariants": [
  {
   "name": "I1_settlement_arithmetic_consistent",
   "holds": true,
   "expected": 223107,
   "observed": 223107,
   "difference": 0,
   "detail": "setl_0001E873: gross 228500 - fees 4570 - tax 823 - refunds 0 + adj 0 = 223107, reported net 223107"
  },
  {
   "name": "I2_fees_and_tax_match_schedule",
   "holds": true,
   "expected": 5393,
   "observed": 5393,
   "difference": 0,
   "detail": "setl_0001E873: expected fee 4570 + tax 823, observed fee 4570 +
```

**Bash:**
```
W=<attempt>/work; R=$W/repo; T=$W/tmp; $R/.venv/bin/python - <<EOF
import json
old = json.load(open('$R/ledgerguard/evaluation/outputs/cases.json'))
new = json.load(open('$T/scratch_new/ledgerguard/evaluation/outputs/cases.json'))
from collections import Counter
diffkeys = Counter(); n=0
for a,b in zip(old,new):
    assert a['case_id']==b['case_id']
    for k in set(a)|set(b):
        if a.get(k)!=b.get(k):
            diffkeys[k]+=1
print("cases:",len(old),"diff counts per key:",dict(diffkeys))
# Show the deterministic exception-level fields for mismatches on the rules side
bad=[(a['case_id'],a['exception_type'],b['exception_type'],a['state'],b['state']) for a,b in zip(old,new) if a.get('exception_type')!=b.get('exception_type') or a.get('exposure_paise')!=b.get('exposure_paise') or a.get('invariants')!=b.get('invariants') or a.get('expected')!=b.get('expected')]
print("deterministic mismatches:",bad[:10], len(bad))
EOF
```

**Result:**
```
cases: 85 diff counts per key: {'decision': 15, 'investigation': 15, 'verification': 15, 'state': 7}
deterministic mismatches: [] 0
```

**Agent:** The deterministic fields (classification, expected values, invariants, observed settlement, exposure) match for all 85 holdout cases. The only differences are `decision`, `investigation`, `verification` and `state` on the 15 investigated cases, which the committed run took from a live model and this offline run could not. Now the full suite and the artifact check.

**Bash:**
```
R=<attempt>/work/repo; cd $R && .venv/bin/python -m pytest ledgerguard/tests -q -p no:cacheprovider 2>&1 | tail -3; find ledgerguard/evaluation/outputs ledgerguard/evaluation/frozen -type f | sort | xargs shasum -a 256 > ../tmp/artifacts_after.sha && cmp ../tmp/artifacts_before.sha ../tmp/artifacts_after.sha && echo ARTIFACTS_UNCHANGED
```

**Result:**
```
-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
83 passed, 1 warning in 4.96s
ARTIFACTS_UNCHANGED
```

**Agent:** The suite is at 83 passing (the 67 original plus 16 new), and the protected artifacts are unchanged. One last check: whether any exporter or the dashboard renders `evidence` in a way the new list-of-objects value could break.

**Bash:**
```
grep -rn "\.evidence" ledgerguard --include=*.py | grep -v tests/ | grep -v "matcher.py\|safety.py" | head -30; grep -n "evidence" ledgerguard/frontend/index.html | head -10
```

**Result:**
```
(eval):1: no matches found: --include=*.py
185:  /* ---- evidence checks --------------------------------------------------- */
380:      <div><div class="eyebrow">Finance operations / evidence-first reconciliation</div>
383:        <div class="actions"><a class="btn primary" href="#walkthrough">Explore the evidence <span aria-hidden="true">↗</span></a><a class="btn secondary" href="#exceptions">View exception queue</a></div>
424:    h += '<div style="margin-top:9px"><h3>Candidate evidence (unproven)</h3>';
502:    ${d.missing_evidence && d.missing_evidence.length
503:      ? `<div class="neutral" style="margin-top:8px">Missing: ${esc(d.missing_evidence.join(', '))}</div>` : ''}
685:    <div class="case-tools"><a class="btn primary" href="/api/evidence-download" download>Download this run's evidence ↓</a><span>JSON · all cases, named checks, metrics, provider and unresolved actions. No new model call.</span></div>
688:      a failure — every row says exactly what evidence was missing.</p>
703:    <h2 style="margin-bottom:0">The evidence walkthrough</h2>
717:    `<h3>Inspect what the evidence actually proves.</h3><div class="grid2">${d.checks.map(c=>`<div class="check ${c.passed?'pass':'fail'}"><span class="mark">${c.passed?'✓':'✕'}</span><span class="name">${esc(c.name)}</span><span class="why">${esc(c.detail)}</span></div>`).join('') || '<p>No checks were possible for this response.</p>'}</div>`,
```

**Bash:**
```
grep -rn "\.evidence\b" ledgerguard | grep -v "/tests/" | grep -v "matcher.py\|safety.py"
```

**Result:**
```
ledgerguard/pipeline.py:22:from .evidence.safety import Decision, HUMAN_REVIEW_REQUIRED, decide
ledgerguard/pipeline.py:23:from .evidence.verifier import (
ledgerguard/pipeline.py:80:    from .evidence.verifier import UNVERIFIED, VERIFIED
ledgerguard/qa.py:20:from .evidence.safety import AUTO_RESOLVED
ledgerguard/backend/app.py:23:from ..evidence.safety import AUTO_RESOLVED
ledgerguard/ai/investigator.py:70:            "reason": exc.evidence.get("reason", ""),
ledgerguard/ai/investigator.py:96:            "settlement": exc.evidence.get("observed_settlement"),
ledgerguard/ai/investigator.py:97:            "bank_entries": exc.evidence.get("bank_entries", []),
ledgerguard/ai/investigator.py:105:                i["name"] for i in exc.evidence.get("failed_invariants", [])
ledgerguard/evaluation/metrics.py:15:from ..evidence.safety import (
ledgerguard/evaluation/ablation.py:26:from ..evidence.safety import AUTO_RESOLVED, HUMAN_REVIEW_REQUIRED
ledgerguard/evaluation/replay.py:26:from ..evidence.safety import decide
ledgerguard/evaluation/replay.py:27:from ..evidence.verifier import resolve_evidence_conflicts, verify
ledgerguard/evaluation/report.py:25:from ..evidence.safety import AUTO_RESOLVED
ledgerguard/evaluation/report.py:96:                "; ".join(exc.evidence.get("secondary_findings", [])) if exc else "",
ledgerguard/evaluation/benchmark.py:28:from ..evidence.safety import AUTO_RESOLVED
ledgerguard/evaluation/benchmark.py:210:                case.exception.evidence.get("observed_settlement") if case.exception else None
```

**Agent:** Every consumer reads specific keys with `.get`, and the new key only appears on missing-settlement cases, which never reach the investigator. I'll record my choices and what I could not verify in `../out/NOTES.md`.

**Write:**
```
<attempt>/work/out/NOTES.md
```

**Result:**
```
File created successfully at: <attempt>/work/out/NOTES.md (file state is current in your context — no need to Read it back)
```

**Agent:** Settlement status is now respected: only `processed` settlements can settle a payment. The full suite passes (83 tests: the 67 existing plus 16 new), and the artifacts under `outputs/` and `frozen/` are byte-identical to their pre-change hashes.

**What changed**
- **`ledger/shadow_ledger.py`**: the index used for all matching holds only `processed` settlements. `pending` and `failed` rows go to a separate index that is read only for evidence.
- **`reconciliation/matcher.py`**:
  - Settlement duplicate and conflict detection sees only processed rows, so a pending or failed row cannot create a duplicate or conflict.
  - A captured payment with no processed settlement is `EXCEPTION_MISSING_SETTLEMENT`, with the same values and state as before. If it has non-processed rows, the evidence gains `non_processed_settlements`, sorted by `settlement_id`. The key is absent otherwise.
- **`tests/test_t2_settlement_status.py`**: 16 new tests covering each requirement, including a dataset-wide check that adding pending and failed copies of every settlement changes no outcome.

The investigator and safety gate are untouched. `MISSING_SETTLEMENT` already escalates deterministically, and the controller tests confirm the investigator is never called for these cases.

**Frozen holdout**: the generator emits only `processed` settlements. I ran the offline benchmark on a scratch copy. Its dataset, manifest and rules-only baseline match the committed artifacts, apart from timing fields. Classification, values, invariants and exposure are identical for all 85 cases.

**Choices and gaps** (details in `../out/NOTES.md`)
- Identical duplicate non-processed rows are each listed in the evidence, not collapsed.
- Payment-level duplicates keep their precedence. Their `transaction_ids` now only ever include a processed settlement.
- `ablation.py` uses the same processed-only lookup, which matters only for batches containing non-processed rows.
- I did not run the live model benchmark, so the hybrid figures in the committed artifacts are not re-derived. The 15 investigated cases differ in decision and state in the offline run, as expected.
- I did not run the new tests against the pre-change code to confirm they fail there.
