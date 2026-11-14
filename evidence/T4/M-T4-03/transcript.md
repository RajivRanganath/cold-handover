# M-T4-03 transcript (PASS)

**Agent:** I'll start with the handover documentation at the repository root, as the ground rules require.

**Bash:**
```
ls -la && find . -path ./.venv -prune -o -type f -print | grep -v __pycache__ | head -200
```

**Result:**
```
total 88
drwxr-xr-x@ 10 user  staff    320 Nov 15 00:31 .
drwxr-xr-x@  5 user  staff    160 Nov 15 00:31 ..
-rw-r--r--@  1 user  staff   1992 Nov 15 00:31 .env.example
-rw-r--r--@  1 user  staff     56 Nov 15 00:31 .gitignore
drwxr-xr-x@  7 user  staff    224 Nov 15 00:31 .venv
drwxr-xr-x@  7 user  staff    224 Nov 15 00:31 docs
drwxr-xr-x@ 14 user  staff    448 Nov 15 00:31 ledgerguard
-rw-r--r--@  1 user  staff  26848 Nov 15 00:31 README.md
-rw-r--r--@  1 user  staff    466 Nov 15 00:31 requirements.txt
-rwxr-xr-x@  1 user  staff   1447 Nov 15 00:31 run_demo.sh
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

**Bash:**
```
wc -l docs/*.md && cat docs/architecture.md docs/limitations.md
```

**Result:**
```
     143 docs/analyses.md
     234 docs/architecture.md
     240 docs/evaluation.md
     217 docs/limitations.md
     144 docs/model_comparison.md
     978 total
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
| I6 | one bank credit equals the settlement net | 
... [21302 more characters in transcript.jsonl]
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

**Agent:** The architecture doc points at the likely area: `evidence/safety.py` has a `residual_paise` guard meant to stop a fee-mismatch close when money is still unattributed. Next I'll read the safety gate, matcher, invariants and ledger.

**Bash:**
```
cat -n ledgerguard/evidence/safety.py
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
    8
... [8424 more characters in transcript.jsonl]
```

**Bash:**
```
cat -n ledgerguard/reconciliation/matcher.py
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
   105	        by_id.setdefault(key(record), []
... [14677 more characters in transcript.jsonl]
```

**Bash:**
```
cat -n ledgerguard/ledger/invariants.py; cat -n ledgerguard/ledger/shadow_ledger.py
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
    97	# I4 ---------------------------------------------------------
... [13285 more characters in transcript.jsonl]
```

**Agent:** The likely bug is in the `FEE_MISMATCH` residual calculation in `reconciliation/matcher.py`. It computes the "corrected" net from the settlement's own components, not its reported net, so a settlement whose reported net is short of its components can show zero residual. I'll confirm this against the fault injector, the other users of `residual_paise`, the tests, and the benchmark runner before changing anything.

**Bash:**
```
grep -rn "residual\|FEE_MISMATCH\|fee_mismatch" --include=*.py ledgerguard | grep -v "/.venv/" ; echo ---; grep -n "def \|F4\|fee" ledgerguard/synthetic/fault_injector.py | head -120
```

**Result:**
```
(eval):1: no matches found: --include=*.py
---
15:from ..ledger.money import gst_on_fee, platform_fee
26:def _noisy_customer_reference(customer: str, rng: random.Random) -> str:
46:def _apply_f1(lc: Lifecycle, rng: random.Random) -> GroundTruth:
61:def _apply_f2(lc: Lifecycle, rng: random.Random) -> GroundTruth:
83:def _apply_f3(lc: Lifecycle, rng: random.Random) -> GroundTruth:
107:def _apply_f4(lc: Lifecycle, rng: random.Random) -> GroundTruth:
108:    """Fee or tax mismatch: provider charged off-schedule fees."""
111:    s.fees += delta
112:    s.tax = gst_on_fee(s.fees)
113:    correct_tax = gst_on_fee(platform_fee(s.gross_amount))
115:        s.gross_amount - s.fees - s.tax - s.refund_adjustments + s.other_adjustments
122:        fault_class=FaultClass.F4_FEE_TAX_MISMATCH,
132:def _apply_f5(lc: Lifecycle, rng: random.Random) -> GroundTruth:
150:def _apply_f6(victim: Lifecycle, donor: Lifecycle, rng: random.Random) -> tuple[GroundTruth, GroundTruth]:
168:        s.gross_amount - s.fees - s.tax - s.refund_adjustments + s.other_adjustments
191:def _clean_truth(lc: Lifecycle) -> GroundTruth:
202:def build_dataset(seed: int = 20260905, count: int = 320) -> Dataset:
239:    # ---- F1, F2, F4, F5 spread over the remaining budget.
267:def split(dataset: Dataset, holdout_fraction: float = 0.25) -> tuple[Dataset, Dataset]:
```

**Bash:**
```
grep -rn "residual\|FEE_MISMATCH" --include=*.py ledgerguard | grep -v "\.venv"; echo ---; sed -n 100,131p ledgerguard/synthetic/fault_injector.py; echo ---; cat ledgerguard/evaluation/benchmark.py | head -150
```

**Result:**
```
(eval):1: no matches found: --include=*.py
---
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
                "delete the manifest del
... [4582 more characters in transcript.jsonl]
```

**Agent:** The F4 injector keeps the settlement internally consistent (net recomputed from the new fees), so the fee-only path has zero residual under a corrected formula too. Next I'll grep for other `residual` users (quoting the glob this time), then run the existing test suite as a baseline.

**Bash:**
```
grep -rn 'residual' ledgerguard --include='*.py' ; grep -rln 'FEE_MISMATCH\|fee_mismatch' ledgerguard --include='*.py'; echo ---; .venv/bin/python -m pytest ledgerguard/tests -q 2>&1 | tail -15
```

**Result:**
```
ledgerguard/reconciliation/matcher.py:367:        evidence["residual_paise"] = expected.net_amount - corrected_net
ledgerguard/evidence/safety.py:114:    residual = exc.evidence.get("residual_paise") or 0
ledgerguard/evidence/safety.py:118:        if residual:
ledgerguard/evidence/safety.py:128:                    f"{to_rupees_str(abs(residual))} INR unattributed, with no record "
ledgerguard/evidence/safety.py:131:                missing_evidence=["explanation for the residual deduction"],
ledgerguard/tests/test_p1_compound.py:6:    money; any unattributed residual blocks closure, while a second finding that
ledgerguard/tests/test_p1_compound.py:46:def test_an_unattributed_residual_blocks_closure_on_the_proven_cause():
ledgerguard/tests/test_p1_compound.py:51:    residual = outcome.case.exception.evidence["residual_paise"]
ledgerguard/tests/test_p1_compound.py:52:    assert residual == to_paise("650.00"), residual
ledgerguard/tests/test_p1_compound.py:57:    # C5 is the same shape with the residual explained by a refund that belongs
ledgerguard/tests/test_p1_compound.py:60:    assert c5.case.exception.evidence["residual_paise"] == to_paise("900.00")
ledgerguard/tests/test_p1_compound.py:70:    assert not outcome.case.exception.evidence.get("residual_paise")
ledgerguard/reconciliation/exceptions.py
ledgerguard/reconciliation/matcher.py
ledgerguard/ledger/models.py
ledgerguard/evidence/safety.py
ledgerguard/tests/test_p2_evaluation.py
ledgerguard/tests/test_p0_core.py
ledgerguard/synthetic/fault_injector.py
---
...................................................................      [100%]
=============================== warnings summary ===============================
.venv/lib/python3.14/site-packages/fastapi/testclient.py:1
  <attempt>/work/repo/.venv/lib/python3.14/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
67 passed, 1 warning in 13.70s
```

**Agent:** All 67 tests pass at baseline. The compound tests pin specific residual values, so I need to see how they build their fixtures before changing the formula.

**Bash:**
```
cat -n ledgerguard/tests/test_p1_compound.py; echo ---; cat -n ledgerguard/synthetic/compound.py | head -200
```

**Result:**
```
     1	"""Compound failure cases.
     2	
     3	Two faults in one lifecycle. These exist to pin one rule:
     4	
     5	    a proven cause licenses closing a case only if it accounts for all of the
     6	    money; any unattributed residual blocks closure, while a second finding that
     7	    is itself benign does not.
     8	
     9	Both halves matter. Without the first, the controller closes on the fault it
    10	recognised and leaves real money unexplained. Without the second, it escalates
    11	every case that has more than one finding and abstention stops meaning anything.
    12	"""
    13	
    14	from __future__ import annotations
    15	
    16	from ledgerguard.ai.provider import HeuristicProvider
    17	from ledgerguard.evidence.safety import AUTO_RESOLVED, HUMAN_REVIEW_REQUIRED
    18	from ledgerguard.ledger.money import to_paise
    19	from ledgerguard.pipeline import run
    20	from ledgerguard.synthetic.compound import build_compound_batch
    21	
    22	
    23	def _run():
    24	    batch, cases = build_compound_batch()
    25	    report = run(batch, use_ai=True, provider=HeuristicProvider())
    26	    return {o.case.payment_id: o for o in report.outcomes}, {c.case_id: c for c in cases}
    27	
    28	
    29	def test_every_compound_case_reaches_its_designed_disposition():
    30	    outcomes, cases = _run()
    31	    assert len(cases) == 5, "three to five compound cases were planned"
    32	
    33	    wrong = []
    34	    for case in cases.values():
    35	        got = outcomes[case.payment_id].state
    36	        if got != case.expected_disposition:
    37	            wrong.append((case.case_id, case.name, got, case.expected_disposition))
    38	    assert not wrong, wrong
    39	
    40	    # No compound case may ever be closed against ground truth.
    41	    for case in cases.values():
    42	        if case.expected_disposition == HUMAN_REVIEW_REQUIRED:
    43	            assert outcomes[case.payment_id].state != AUTO_RESOLVED, case.case_id
    44	
    45	
    46	def test_an_unattributed_residual_blocks_closure_on_the_proven_cause():
    47	    """C2: the fee overcharge is proven; INR 650.00 is still missing."""
    48	    outcomes, _ = _run()
    49	    outcome = outcomes["pay_C2"]
    50	
    51	    residual = outcome.case.exception.evidence["residual_paise"]
    52	    assert residual == to_paise("650.00"), residual
    53	    assert outcome.state == HUMAN_REVIEW_REQUIRED
    54	    assert "unattributed" in outcome.decision.reason
    55	    assert "650.00" in outcome.decision.reason
    56	
    57	    # C5 is the same shape with the residual explained by a refund that belongs
    58	    # to a different customer -- still blocked, and for the same reason.
    59	    c5 = outcomes["pay_C5"]
    60	    assert c5.case.exception.evidence["residual_paise"] == to_paise("900.00")
    61	    assert c5.state == HUMAN_REVIEW_REQUIRED
    62	
    63	
    64	def test_a_fully_attributed_case_still_closes_and_reports_the_second_finding():
    65	    """C3: duplicate credit plus a delay. Nothing unexplained, so it closes."""
    66	    outcomes, _ = _run()
    67	    outcome = outcomes["pay_C3"]
    68	
    69	    assert outcome.state == AUTO_RESOLVED
    70	    assert not outcome.case.exception.evidence.get("residual_paise")
    71	    # The delay was not the classification, and must still be surfaced.
    72	    assert "I5_settlement_within_window" in outcome.case.exception.evidence["secondary_findings"]
    73	    assert "I5_settlement_within_window" in outcome.decision.reason
    74	
    75	
    76	def test_a_resolved_shortfall_does_not_swallow_a_concurrent_delay():
    77	    """C1: the refund genuinely explains the gap, but the case is also late."""
    78	    outcomes, _ = _run()
    79	    outcome = outcomes["pay_C1"]
    80	
    81	    assert outcome.state == AUTO_RESOLVED
    82	    assert outcome.verification.verdict == "VERIFIED"
    83	    assert "I5_settlement_within_window" in outcome.case.
... [9616 more characters in transcript.jsonl]
```

**Agent:** The compound fixtures have fee and net consistent with each other, so the old and corrected formulas agree on every case the suite pins. They diverge only when the settlement's reported net does not match its own components, which is the reported case. Before editing, I'll reproduce the bug through the real `pipeline.run` path with a settlement shaped like the report: fees and tax exact, reported net 250 short.

**Bash:**
```
mkdir -p ../tmp/repro && cat > ../tmp/repro/repro_250.py <<'EOF'
import sys
sys.path.insert(0, sys.argv[1])
from datetime import datetime, timedelta
from ledgerguard.ledger.models import Order, Payment, Settlement, BankEntry, CreditDebit, Batch
from ledgerguard.ledger.money import platform_fee, gst_on_fee, to_paise
from ledgerguard.pipeline import run

T0 = datetime(2026, 7, 15, 10, 0, 0)
amount = to_paise("10000.00")
fee = platform_fee(amount); tax = gst_on_fee(fee)
captured = T0 + timedelta(minutes=5)
order = Order(order_id="ord_X", merchant_id="mch_X", amount=amount, created_at=T0, customer_reference="CUST-X")
payment = Payment(payment_id="pay_X", order_id="ord_X", amount=amount, captured_at=captured,
                  fee=fee, tax=tax, reference="PAY/ord_X")
settled_on = captured + timedelta(days=2)
# fees and tax exactly per schedule; reported net is 250.00 short of gross - fees - tax
net = amount - fee - tax - to_paise("250.00")
s = Settlement(settlement_id="setl_X", merchant_id="mch_X", payment_ids=["pay_X"], gross_amount=amount,
               fees=fee, tax=tax, refund_adjustments=0, other_adjustments=0, net_amount=net,
               settlement_date=settled_on, reference="STL/setl_X")
b = BankEntry(bank_entry_id="bnk_X", amount=net, credit_or_debit=CreditDebit.CREDIT, date=settled_on, reference=s.reference)
batch = Batch(orders=[order], payments=[payment], refunds=[], settlements=[s], bank_entries=[b])
rep = run(batch, use_ai=False)
for o in rep.outcomes:
    print(o.case.exception.exception_type.value, "| state:", o.state)
    print("residual:", o.case.exception.evidence.get("residual_paise"))
    print("reason:", o.decision.reason)
EOF
.venv/bin/python -I ../tmp/repro/repro_250.py "$(pwd)" 2>&1 | tail -20
```

**Result:**
```
EXCEPTION_FEE_MISMATCH | state: AUTO_RESOLVED
residual: 0
reason: Fee and tax reconciled against the independent fee schedule; the exact variance is quantified.
```

**Agent:** Reproduced: the settlement auto-closes as `FEE_MISMATCH` with residual 0. The cause is that `matcher.py:360-367` builds `corrected_net` from the settlement's gross, fee, tax, and refund fields rather than from its reported `net_amount`. Whenever those fields are internally consistent, that equals the expected net and the residual is zero, which hides a net that is short of its own components.

Before editing I'll snapshot a pristine copy of the repo under `../tmp/` to get benchmark baselines, so the repo's own `outputs/` and `frozen/` directories never get regenerated.

**Bash:**
```
cd .. && mkdir -p tmp/baseline && rsync -a --exclude .venv --exclude __pycache__ repo/ tmp/baseline/ && cd tmp/baseline && (time <attempt>/work/repo/.venv/bin/python -m ledgerguard.evaluation.benchmark > ../bench_baseline.log 2>&1); tail -5 ../bench_baseline.log; cd <attempt>/work/repo && .venv/bin/python -c "print(1)" && grep -n "provider" ledgerguard/evaluation/benchmark.py | head -20
```

**Result:**
```
<attempt>/work/repo/.venv/bin/python -m  >    1.11s user 0.25s system 82% cpu 1.648 total
Artifacts written to <attempt>/work/tmp/baseline/ledgerguard/evaluation/outputs
  benchmark.md, benchmark.json, cases.json
  unresolved_exceptions.csv (10 rows)

NOTE: the hybrid run used the offline heuristic stub, not a model. Configure a provider key (GROQ_API_KEY, GEMINI_API_KEY, NVIDIA_API_KEY or OMNIROUTE_API_KEY) and rerun to measure against a real investigator.
1
27:from ..ai.provider import get_provider
96:        f"Investigator for the hybrid run: `{hyb.provider}`.",
247:        "--provider",
264:    provider = get_provider(args.provider) if args.provider else get_provider()
267:    hybrid_report = run(batch, use_ai=True, provider=provider, lifecycle_by_payment=lbp)
272:    # Which providers actually answered, and which dropped out mid-run.
273:    fallback_report = provider.report() if hasattr(provider, "report") else None
274:    costs = estimate(provider, hyb_metrics.investigations, hyb_metrics.total_cases)
313:                f"  FAILED {failure['operation']} via {failure['provider']}: "
340:    if hyb_metrics.provider == "heuristic_stub":
343:            "Configure a provider key (GROQ_API_KEY, GEMINI_API_KEY, NVIDIA_API_KEY "
```

**Agent:** The baseline ran on the offline stub, which is deterministic, so I can diff the fixed code's benchmark against it. Now the fix. The matcher should measure the residual from the settlement's reported net, after correcting only the proven fee variance.

**Edit:**
```
<attempt>/work/repo/ledgerguard/reconciliation/matcher.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/reconciliation/matcher.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

**Agent:** Next, the gate. A `FEE_MISMATCH` close should also require a proven fee variance: if fees and tax match the schedule exactly, the fee classification has no proven cause and nothing should close it. I'll update `safety.py` so the decision text stays accurate in that case.

**Edit:**
```
<attempt>/work/repo/ledgerguard/evidence/safety.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/evidence/safety.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

**Bash:**
```
.venv/bin/python -I ../tmp/repro/repro_250.py "$(pwd)" 2>&1 | tail -20; echo ---; .venv/bin/python -m pytest ledgerguard/tests -q 2>&1 | tail -3
```

**Result:**
```
EXCEPTION_FEE_MISMATCH | state: HUMAN_REVIEW_REQUIRED
residual: 25000
reason: Fee and tax equal the fee schedule exactly, so no fee variance is proven and the fee classification has no cause. The settlement's reported net does not equal its own gross less fees, tax and refunds, and no record explains the difference. Against the shadow ledger, 250.00 INR is unattributed.
---

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
67 passed, 1 warning in 6.67s
```

**Agent:** The reproduction now lands in `HUMAN_REVIEW_REQUIRED`, and the message reports 250.00 INR unattributed. (The raw residual of 25000 is in paise, which is 250.00 INR.) All 67 existing tests still pass. Next I'll check the holdout: run the benchmark on a copy of the fixed code and diff it against the baseline copy.

**Bash:**
```
cd <attempt>/work && mkdir -p tmp/fixed && rsync -a --exclude .venv --exclude __pycache__ repo/ tmp/fixed/ && cd tmp/fixed && <attempt>/work/repo/.venv/bin/python -m ledgerguard.evaluation.benchmark > ../bench_fixed.log 2>&1; echo exit=$?; cd .. && diff -r --exclude='*.log' -q baseline/ledgerguard/evaluation/outputs fixed/ledgerguard/evaluation/outputs; echo "--- benchmark.md diff:"; diff baseline/ledgerguard/evaluation/outputs/benchmark.md fixed/ledgerguard/evaluation/outputs/benchmark.md; echo "--- frozen diff:"; diff -r baseline/ledgerguard/evaluation/frozen fixed/ledgerguard/evaluation/frozen && echo frozen-same; grep -i "false auto\|Value falsely" fixed/ledgerguard/evaluation/outputs/benchmark.md
```

**Result:**
```
exit=0
Files baseline/ledgerguard/evaluation/outputs/benchmark.json and fixed/ledgerguard/evaluation/outputs/benchmark.json differ
Files baseline/ledgerguard/evaluation/outputs/benchmark.md and fixed/ledgerguard/evaluation/outputs/benchmark.md differ
Files baseline/ledgerguard/evaluation/outputs/cases.json and fixed/ledgerguard/evaluation/outputs/cases.json differ
--- benchmark.md diff:
33,34c33,34
< | Wall time (s) | 0.01 | 0.014 |
< | Throughput (cases/s) | 8218.5 | 6184.6 |
---
> | Wall time (s) | 0.014 | 0.019 |
> | Throughput (cases/s) | 6246.4 | 4391.2 |
38,39c38,39
< | Investigation latency p50 (ms) | 0.0 | 0.03 |
< | Investigation latency p95 (ms) | 0.0 | 0.08 |
---
> | Investigation latency p50 (ms) | 0.0 | 0.04 |
> | Investigation latency p95 (ms) | 0.0 | 0.09 |
--- frozen diff:
frozen-same
| **False auto resolutions** | **0** | **0** |
| **Value falsely auto resolved** | **INR 0.00** | **INR 0.00** |
| Fault class | n | rules only correct | LedgerGuard correct | LedgerGuard auto resolved | LedgerGuard false auto |
Shell cwd was reset to <attempt>/work/repo
```

**Agent:** The only textual differences in `benchmark.md` are wall-clock timings. `cases.json` also differs, so I need to check whether that is timing or real disposition changes.

**Bash:**
```
cd <attempt>/work/tmp && <attempt>/work/repo/.venv/bin/python -I -c "
import json,difflib
def norm(path):
    return json.dumps(json.load(open(path)), indent=1, sort_keys=True).splitlines()
for f in ['cases.json','benchmark.json']:
    a=norm('baseline/ledgerguard/evaluation/outputs/'+f); b=norm('fixed/ledgerguard/evaluation/outputs/'+f)
    d=[l for l in difflib.unified_diff(a,b,lineterm='',n=0) if l[:1] in '+-' and not l.startswith(('+++','---'))]
    print(f, 'changed lines:', len(d))
    print('\n'.join(d[:40]))
"; diff baseline/ledgerguard/evaluation/outputs/unresolved_exceptions.csv fixed/ledgerguard/evaluation/outputs/unresolved_exceptions.csv && echo unresolved-csv-same
```

**Result:**
```
cases.json changed lines: 20
-   "latency_ms": 0.08,
+   "latency_ms": 0.12,
-   "latency_ms": 0.04,
+   "latency_ms": 0.05,
-   "latency_ms": 0.03,
+   "latency_ms": 0.04,
-   "latency_ms": 0.03,
+   "latency_ms": 0.04,
-   "latency_ms": 0.05,
+   "latency_ms": 0.06,
-   "latency_ms": 0.04,
+   "latency_ms": 0.03,
-   "latency_ms": 0.03,
+   "latency_ms": 0.04,
-   "latency_ms": 0.03,
+   "latency_ms": 0.04,
-   "latency_ms": 0.04,
+   "latency_ms": 0.05,
-   "latency_ms": 0.03,
+   "latency_ms": 0.04,
benchmark.json changed lines: 12
-  "throughput_per_second": 8218.5,
+  "throughput_per_second": 6246.4,
-  "wall_seconds": 0.01
+  "wall_seconds": 0.014
-  "latency_p50_ms": 0.03,
-  "latency_p95_ms": 0.08,
+  "latency_p50_ms": 0.04,
+  "latency_p95_ms": 0.09,
-  "throughput_per_second": 6184.6,
+  "throughput_per_second": 4391.2,
-  "wall_seconds": 0.014
+  "wall_seconds": 0.019
unresolved-csv-same
Shell cwd was reset to <attempt>/work/repo
```

**Agent:** Every difference in the holdout outputs is a wall-clock or latency field; the dispositions, money, and unresolved list are byte-identical. The holdout is only one slice, though, so I'll also compare every case across the full 320-lifecycle dataset, the compound cases, and the adversarial pair, on both the deterministic path and the default AI path.

**Bash:**
```
cat > <attempt>/work/tmp/repro/dispositions.py <<'EOF'
import sys, json
root = sys.argv[1]
sys.path.insert(0, root)
from ledgerguard.synthetic.fault_injector import build_dataset
from ledgerguard.synthetic.compound import build_compound_batch
from ledgerguard.synthetic.adversarial import build_adversarial_batch
from ledgerguard.pipeline import run
from ledgerguard.ai.provider import HeuristicProvider
from ledgerguard.ledger.models import Batch

def rows(report):
    out = {}
    for o in report.outcomes:
        out[o.case.case_id] = [o.case.status, o.state, o.decision.resolution, o.exposure_paise]
    return out

result = {}
ds = build_dataset(seed=20260905, count=320)
batch = ds.batch()
lbp = {lc.payment_id: lc.lifecycle_id for lc in ds.lifecycles} if hasattr(ds.lifecycles[0], 'payment_id') else None
result['full_det'] = rows(run(batch, use_ai=False))
result['full_ai'] = rows(run(batch, use_ai=True, provider=HeuristicProvider()))
cb, _ = build_compound_batch()
result['compound_ai'] = rows(run(cb, use_ai=True, provider=HeuristicProvider()))
json.dump(result, sys.stdout, sort_keys=True, default=str)
EOF
cd <attempt>/work && grep -n "^def \|^class " repo/ledgerguard/synthetic/adversarial.py | head; grep -n "def batch\|payment_id" repo/ledgerguard/synthetic/generator.py | head -5
```

**Result:**
```
46:def _leg(
99:def build_adversarial_batch() -> Batch:
102:    def batch(self) -> Batch:
114:        return {lc.payment.payment_id: lc.lifecycle_id for lc in self.lifecycles}
118:            lc.payment.payment_id: self.ground_truth[lc.lifecycle_id].fault_class
167:            payment_id=f"pay_{i:04d}{rng.randrange(0x1000, 0xFFFF):04X}",
185:                    payment_id=payment.payment_id,
Shell cwd was reset to <attempt>/work/repo
```

**Bash:**
```
cd <attempt>/work && python3 - <<'EOF'
import re
p='tmp/repro/dispositions.py'
s=open(p).read()
s=s.replace("lbp = {lc.payment_id: lc.lifecycle_id for lc in ds.lifecycles} if hasattr(ds.lifecycles[0], 'payment_id') else None\n","")
s=s.replace("from ledgerguard.synthetic.adversarial import build_adversarial_batch\n","from ledgerguard.synthetic.adversarial import build_adversarial_batch\n")
s=s.replace("json.dump(result","result['adversarial_ai'] = rows(run(build_adversarial_batch(), use_ai=True, provider=HeuristicProvider()))\njson.dump(result")
open(p,'w').write(s)
EOF
for v in baseline fixed; do tmp/../repo/.venv/bin/python -I tmp/repro/dispositions.py tmp/$v > tmp/disp_$v.json 2>tmp/disp_$v.err; echo "$v exit=$?"; done; tail -3 tmp/disp_fixed.err; .venv 2>/dev/null; repo/.venv/bin/python -I -c "
import json
a=json.load(open('tmp/disp_baseline.json')); b=json.load(open('tmp/disp_fixed.json'))
for sec in a:
    diffs=[(k,a[sec][k],b[sec].get(k)) for k in a[sec] if a[sec][k]!=b[sec].get(k)]
    print(sec, 'cases:', len(a[sec]), 'changed:', len(diffs))
    for d in diffs: print('  ',d)
    from collections import Counter
    print('  states fixed:', Counter(v[1] for v in b[sec].values()))
"
```

**Result (error):**
```
Exit code 1
baseline exit=1
fixed exit=1
    out[o.case.case_id] = [o.case.status, o.state, o.decision.resolution, o.exposure_paise]
                                                   ^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'resolution'
Traceback (most recent call last):
  File "<string>", line 3, in <module>
    a=json.load(open('tmp/disp_baseline.json')); b=json.load(open('tmp/disp_fixed.json'))
  File "/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/lib/python3.14/json/__init__.py", line 298, in load
    return loads(fp.read(),
        cls=cls, object_hook=object_hook,
        parse_float=parse_float, parse_int=parse_int,
        parse_constant=parse_constant, object_pairs_hook=object_pairs_hook, **kw)
  File "/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/lib/python3.14/json/__init__.py", line 352, in loads
    return _default_decoder.decode(s)
           ~~~~~~~~~~~~~~~~~~~~~~~^^^
  File "/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/lib/python3.14/json/decoder.py", line 345, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/lib/python3.14/json/decoder.py", line 363, in raw_decode
    raise JSONDecodeError("Expecting value", s, err.value) from None
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

**Agent:** Matched cases have no `Decision`, so the script needs a guard. Fixing that and re-running.

**Bash:**
```
cd <attempt>/work && sed -i 's/o.decision.resolution, o.exposure_paise\]/(o.decision.resolution if o.decision else None), o.exposure_paise]/; s/\[o.case.status, o.state,/[o.case.status, o.state if o.decision else "MATCHED",/' tmp/repro/dispositions.py && for v in baseline fixed; do repo/.venv/bin/python -I tmp/repro/dispositions.py tmp/$v > tmp/disp_$v.json 2>tmp/disp_$v.err; echo "$v exit=$?"; done; tail -3 tmp/disp_fixed.err; repo/.venv/bin/python -I -c "
import json
from collections import Counter
a=json.load(open('tmp/disp_baseline.json')); b=json.load(open('tmp/disp_fixed.json'))
for sec in a:
    diffs=[(k,a[sec][k],b[sec].get(k)) for k in a[sec] if a[sec][k]!=b[sec].get(k)]
    print(sec, 'cases:', len(a[sec]), 'changed:', len(diffs))
    for d in diffs: print('  ',d)
    print('  states fixed:', dict(Counter(v[1] for v in b[sec].values())))
"
```

**Result (error):**
```
Exit code 1
sed: 1: "tmp/repro/dispositions.py": undefined label 'mp/repro/dispositions.py'
    out[o.case.case_id] = [o.case.status, o.state, o.decision.resolution, o.exposure_paise]
                                                   ^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'resolution'
Traceback (most recent call last):
  File "<string>", line 4, in <module>
    a=json.load(open('tmp/disp_baseline.json')); b=json.load(open('tmp/disp_fixed.json'))
  File "/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/lib/python3.14/json/__init__.py", line 298, in load
    return loads(fp.read(),
        cls=cls, object_hook=object_hook,
        parse_float=parse_float, parse_int=parse_int,
        parse_constant=parse_constant, object_pairs_hook=object_pairs_hook, **kw)
  File "/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/lib/python3.14/json/__init__.py", line 352, in loads
    return _default_decoder.decode(s)
           ~~~~~~~~~~~~~~~~~~~~~~~^^^
  File "/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/lib/python3.14/json/decoder.py", line 345, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/lib/python3.14/json/decoder.py", line 363, in raw_decode
    raise JSONDecodeError("Expecting value", s, err.value) from None
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

**Agent:** The `sed` expression got mangled by the shell, so I'll make the edit in Python instead.

**Bash:**
```
cd <attempt>/work && python3 - <<'EOF'
p='tmp/repro/dispositions.py'
s=open(p).read()
s=s.replace("out[o.case.case_id] = [o.case.status, o.state, o.decision.resolution, o.exposure_paise]",
 "out[o.case.case_id] = [o.case.status, (o.state if o.decision else 'MATCHED'), (o.decision.resolution if o.decision else None), o.exposure_paise]")
open(p,'w').write(s)
EOF
for v in baseline fixed; do repo/.venv/bin/python -I tmp/repro/dispositions.py tmp/$v > tmp/disp_$v.json 2>tmp/disp_$v.err; echo "$v exit=$?"; done; tail -3 tmp/disp_fixed.err; repo/.venv/bin/python -I -c "
import json
from collections import Counter
a=json.load(open('tmp/disp_baseline.json')); b=json.load(open('tmp/disp_fixed.json'))
for sec in a:
    diffs=[(k,a[sec][k],b[sec].get(k)) for k in a[sec] if a[sec][k]!=b[sec].get(k)]
    print(sec, 'cases:', len(a[sec]), 'changed:', len(diffs))
    for d in diffs: print('  ',d)
    print('  states fixed:', dict(Counter(v[1] for v in b[sec].values())))
"
```

**Result:**
```
baseline exit=0
fixed exit=0
adversarial_ai cases: 2 changed: 0
  states fixed: {'HUMAN_REVIEW_REQUIRED': 1, 'AUTO_RESOLVED': 1}
compound_ai cases: 5 changed: 0
  states fixed: {'AUTO_RESOLVED': 2, 'HUMAN_REVIEW_REQUIRED': 3}
full_ai cases: 320 changed: 0
  states fixed: {'MATCHED': 218, 'AUTO_RESOLVED': 75, 'HUMAN_REVIEW_REQUIRED': 27}
full_det cases: 320 changed: 0
  states fixed: {'MATCHED': 218, 'HUMAN_REVIEW_REQUIRED': 56, 'AUTO_RESOLVED': 46}
Shell cwd was reset to <attempt>/work/repo
```

**Agent:** Across all 320 generated lifecycles (both the deterministic and AI paths), the 12 compound-and-adversarial cases, and the holdout, no disposition changes. The fix only affects settlements whose reported net disagrees with their own components, and the generator never produces one. Next I'll add regression tests in a new file (existing tests stay untouched).

**Write:**
```
<attempt>/work/repo/ledgerguard/tests/test_fee_residual.py
```

**Result:**
```
File created successfully at: <attempt>/work/repo/ledgerguard/tests/test_fee_residual.py (file state is current in your context — no need to Read it back)
```

**Bash:**
```
.venv/bin/python -m pytest ledgerguard/tests/test_fee_residual.py -q 2>&1 | tail -25; echo ---; .venv/bin/python -m pytest ledgerguard/tests -q 2>&1 | tail -2
```

**Result:**
```
.....                                                                    [100%]
5 passed in 0.41s
---
-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
72 passed, 1 warning in 6.96s
```

**Agent:** All 72 tests pass. To confirm the new tests actually catch the bug, I'll run them against the unmodified baseline copy, where they should fail.

**Bash:**
```
cd <attempt>/work && cp repo/ledgerguard/tests/test_fee_residual.py tmp/baseline/ledgerguard/tests/ && cd tmp/baseline && <attempt>/work/repo/.venv/bin/python -m pytest ledgerguard/tests/test_fee_residual.py -q 2>&1 | grep -E "passed|failed|FAILED"
```

**Result:**
```
FAILED ledgerguard/tests/test_fee_residual.py::test_reported_case_fees_exact_net_short_is_not_auto_closed
FAILED ledgerguard/tests/test_fee_residual.py::test_fee_overcharge_plus_unexplained_shortfall_is_not_auto_closed
FAILED ledgerguard/tests/test_fee_residual.py::test_fee_overcharge_that_fully_explains_the_gap_still_auto_closes
FAILED ledgerguard/tests/test_fee_residual.py::test_internal_arithmetic_break_with_no_fee_variance_is_not_closed_as_a_fee
4 failed, 1 passed in 0.54s
Shell cwd was reset to <attempt>/work/repo
```

**Agent:** Four of the five fail on baseline, as they should. The R1/R2 failures currently trip on a missing new evidence key before reaching the behavioural assertion, so I'll move the fee-variance checks after the behavioural ones.

**Bash:**
```
python3 - <<'EOF'
p='ledgerguard/tests/test_fee_residual.py'
s=open(p).read()
old1='''    assert outcome.case.exception.exception_type.value == "EXCEPTION_FEE_MISMATCH"
    assert outcome.case.exception.evidence["fee_variance_paise"] == 0
    assert outcome.case.exception.evidence["residual_paise"] == to_paise("250.00")
    assert outcome.state == HUMAN_REVIEW_REQUIRED
    assert outcome.state != AUTO_RESOLVED
    assert outcome.decision.resolution is None
    assert "250.00" in outcome.decision.reason
    assert "unattributed" in outcome.decision.reason
'''
new1='''    assert outcome.case.exception.exception_type.value == "EXCEPTION_FEE_MISMATCH"
    assert outcome.case.exception.evidence["residual_paise"] == to_paise("250.00")
    assert outcome.state == HUMAN_REVIEW_REQUIRED
    assert outcome.state != AUTO_RESOLVED
    assert outcome.decision.resolution is None
    assert "250.00" in outcome.decision.reason
    assert "unattributed" in outcome.decision.reason
    assert outcome.case.exception.evidence["fee_variance_paise"] == 0
'''
old2='''    assert outcome.case.exception.exception_type.value == "EXCEPTION_FEE_MISMATCH"
    assert outcome.case.exception.evidence["fee_variance_paise"] > 0
    assert outcome.case.exception.evidence["residual_paise"] == to_paise("250.00")
    assert outcome.state == HUMAN_REVIEW_REQUIRED
    assert "250.00" in outcome.decision.reason
'''
new2='''    assert outcome.case.exception.exception_type.value == "EXCEPTION_FEE_MISMATCH"
    assert outcome.case.exception.evidence["residual_paise"] == to_paise("250.00")
    assert outcome.state == HUMAN_REVIEW_REQUIRED
    assert "250.00" in outcome.decision.reason
    assert outcome.case.exception.evidence["fee_variance_paise"] > 0
'''
assert s.count(old1)==1 and s.count(old2)==1
s=s.replace(old1,new1).replace(old2,new2)
open(p,'w').write(s)
EOF
cp ledgerguard/tests/test_fee_residual.py ../tmp/baseline/ledgerguard/tests/ && .venv/bin/python -m pytest ledgerguard/tests -q 2>&1 | tail -1; cd ../tmp/baseline && <attempt>/work/repo/.venv/bin/python -m pytest ledgerguard/tests/test_fee_residual.py -q 2>&1 | grep -E "^E  |passed|failed" | head -12
```

**Result:**
```
72 passed, 1 warning in 8.14s
E       AssertionError: assert 0 == 25000
E        +  where 25000 = to_paise('250.00')
E       AssertionError: assert 0 == 25000
E        +  where 25000 = to_paise('250.00')
E       KeyError: 'fee_variance_paise'
E       KeyError: 'fee_variance_paise'
4 failed, 1 passed in 0.57s
Shell cwd was reset to <attempt>/work/repo
```

**Agent:** The four baseline failures are now behavioural (`0 == 25000`), and the other two fail on the new evidence key, as expected. The "changed on disk" notice is just my own Python rewrite of that file, so the current content is the intended version.

Next I'll confirm the repo's benchmark artifacts were not touched. The benchmark only ran in the `tmp/` copies, but the test suite could write files, so I'll check modification times.

**Bash:**
```
find ledgerguard/evaluation/outputs ledgerguard/evaluation/frozen -type f -newer ledgerguard/__init__.py | head; echo "newer-count: $(find ledgerguard/evaluation/outputs ledgerguard/evaluation/frozen -type f -newer ledgerguard/__init__.py | wc -l)"; ls -la --time-style=full-iso ledgerguard/evaluation/outputs | head -4; cat .gitignore; find . -path ./.venv -prune -o -name __pycache__ -print | head -3
```

**Result:**
```
ledgerguard/evaluation/frozen/holdout_20260905_320.json
ledgerguard/evaluation/outputs/drift.md
ledgerguard/evaluation/outputs/decision_log.json
ledgerguard/evaluation/outputs/no_gate_ablation.md
ledgerguard/evaluation/outputs/ablation.md
ledgerguard/evaluation/outputs/reconciliation_report.csv
ledgerguard/evaluation/outputs/scale.json
ledgerguard/evaluation/outputs/calibration.json
ledgerguard/evaluation/outputs/no_gate_ablation.json
ledgerguard/evaluation/outputs/scale.md
newer-count:       21
ls: unrecognized option `--time-style=full-iso'
usage: ls [-@ABCFGHILOPRSTUWXabcdefghiklmnopqrstuvwxy1%,] [--color=when] [-D format] [file ...]
.venv/
__pycache__/
*.pyc
.env
.pytest_cache/
.DS_Store
./ledgerguard/__pycache__
./ledgerguard/reconciliation/__pycache__
./ledgerguard/ledger/__pycache__
```

**Agent:** Twenty-one files look newer than `__init__.py`, which may just be extraction timestamps. I'll check their actual modification times against the extraction time.

**Bash:**
```
stat -f '%Sm  %N' -t '%Y-%m-%d %H:%M:%S' ledgerguard/__init__.py ledgerguard/evaluation/frozen/* ledgerguard/evaluation/outputs/* | sort | head -40; echo; stat -f '%Sm %N' -t '%Y-%m-%d %H:%M:%S' ledgerguard/tests/test_p0_core.py ledgerguard/reconciliation/matcher.py
```

**Result:**
```
2026-11-15 00:31:48  ledgerguard/__init__.py
2026-11-15 00:31:48  ledgerguard/evaluation/frozen/holdout_20260905_320.json
2026-11-15 00:31:49  ledgerguard/evaluation/outputs/ablation.json
2026-11-15 00:31:49  ledgerguard/evaluation/outputs/ablation.md
2026-11-15 00:31:49  ledgerguard/evaluation/outputs/benchmark.json
2026-11-15 00:31:49  ledgerguard/evaluation/outputs/benchmark.md
2026-11-15 00:31:49  ledgerguard/evaluation/outputs/calibration.json
2026-11-15 00:31:49  ledgerguard/evaluation/outputs/calibration.md
2026-11-15 00:31:49  ledgerguard/evaluation/outputs/cases.json
2026-11-15 00:31:49  ledgerguard/evaluation/outputs/decision_log.json
2026-11-15 00:31:49  ledgerguard/evaluation/outputs/drift.json
2026-11-15 00:31:49  ledgerguard/evaluation/outputs/drift.md
2026-11-15 00:31:49  ledgerguard/evaluation/outputs/evidence_ledger.csv
2026-11-15 00:31:49  ledgerguard/evaluation/outputs/model_comparison.json
2026-11-15 00:31:49  ledgerguard/evaluation/outputs/model_comparison.md
2026-11-15 00:31:49  ledgerguard/evaluation/outputs/no_gate_ablation.json
2026-11-15 00:31:49  ledgerguard/evaluation/outputs/no_gate_ablation.md
2026-11-15 00:31:49  ledgerguard/evaluation/outputs/reconciliation_report.csv
2026-11-15 00:31:49  ledgerguard/evaluation/outputs/reconciliation_report.md
2026-11-15 00:31:49  ledgerguard/evaluation/outputs/scale.json
2026-11-15 00:31:49  ledgerguard/evaluation/outputs/scale.md
2026-11-15 00:31:49  ledgerguard/evaluation/outputs/unresolved_exceptions.csv

2026-11-15 00:31:48 ledgerguard/tests/test_p0_core.py
2026-11-15 00:34:48 ledgerguard/reconciliation/matcher.py
```

**Agent:** All artifacts carry the extraction timestamp (00:31:48–49), so nothing in the repo's `outputs/` or `frozen/` was regenerated. The only writes happened in `tmp/` copies. Now I'll write the notes file, checking first whether `../out/` already has a NOTES.md.

**Bash:**
```
cd <attempt>/work && mkdir -p out && ls -la out; cd repo && git diff --no-index --stat ../tmp/baseline/ledgerguard/reconciliation/matcher.py ledgerguard/reconciliation/matcher.py 2>/dev/null | tail -1; diff ../tmp/baseline/ledgerguard/evidence/safety.py ledgerguard/evidence/safety.py | head -50
```

**Result:**
```
total 0
drwxr-xr-x@ 2 user  staff   64 Nov 15 00:31 .
drwxr-xr-x@ 5 user  staff  160 Nov 15 00:31 ..
 1 file changed, 15 insertions(+), 12 deletions(-)
117a118,143
>         if exc_type is ExceptionType.FEE_MISMATCH and not exc.evidence.get("fee_variance_paise"):
>             # Fee and tax equal the schedule, so there is no fee variance to
>             # prove. The classification therefore has no cause behind it, and
>             # the case is a settlement whose own arithmetic does not balance.
>             # Nothing in the batch explains that, so it must not close.
>             gap = (
>                 f" Against the shadow ledger, {to_rupees_str(abs(residual))} INR "
>                 "is unattributed."
>                 if residual
>                 else ""
>             )
>             return Decision(
>                 case_id=case.case_id,
>                 state=HUMAN_REVIEW_REQUIRED,
>                 reason=(
>                     "Fee and tax equal the fee schedule exactly, so no fee variance "
>                     "is proven and the fee classification has no cause. The settlement's "
>                     "reported net does not equal its own gross less fees, tax and refunds, "
>                     "and no record explains the difference." + gap
>                 ),
>                 missing_evidence=["explanation for the settlement arithmetic break"],
>                 suggested_action=(
>                     "Obtain the line-level settlement detail from the provider and "
>                     "identify the deduction before closing."
>                 ),
>             )
```

**Agent:** Nothing is in `../out/` yet, so I'll write the notes file now.

**Write:**
```
<attempt>/work/out/NOTES.md
```

**Result:**
```
File created successfully at: <attempt>/work/out/NOTES.md (file state is current in your context — no need to Read it back)
```

**Edit:**
```
<attempt>/work/out/NOTES.md
```

**Result:**
```
The file <attempt>/work/out/NOTES.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

**Agent:** The fix is in. A settlement whose reported net is short of its own gross, fees, tax and refunds no longer auto-closes as a fee mismatch. The 250.00 case now escalates to `HUMAN_REVIEW_REQUIRED` and reports the INR 250.00 as unattributed.

**Cause:** In `ledgerguard/reconciliation/matcher.py`, the fee-mismatch residual was computed from the settlement's own gross, refund and adjustment fields rather than its reported `net_amount`. When those fields were internally consistent, the residual came out zero, so the short net went unseen.

**Fix:**
- `matcher.py`: the residual now starts from the reported net, corrected by the fee variance. The fee variance is also stored as evidence. For internally consistent settlements this equals the old formula, so the compound cases' residuals (650.00 and 900.00) are unchanged.
- `evidence/safety.py`: a `FEE_MISMATCH` close also requires a non-zero fee variance. Without one, the fee cause is unproven and the case escalates. This is my reading of the documented "proven cause must account for all the money" principle, and it covers a settlement whose breakdown is wrong while its net still matches the ledger. The residual change alone already escalates the reported case.

**Verification:**
- Test suite: 67 passed before, 72 passed after. The five new tests are in `ledgerguard/tests/test_fee_residual.py`, and no existing test was modified. Four of the five fail on the unmodified code. The fifth is a guard that passes on both versions.
- Frozen holdout: I ran the benchmark on the unmodified and fixed code in copies under `../tmp/`. The offline stub is deterministic, and the only differences are timing fields. Dispositions, money and the unresolved list are identical. Every case across the 320-lifecycle dataset, the compound cases and the adversarial pair also matches.
- Repo artifacts: nothing under `evaluation/outputs/` or `evaluation/frozen/` was regenerated. All still carry their extraction timestamps.

**Limits:**
- The committed benchmark came from live model runs, which I cannot reproduce offline, so my comparison uses the stub. It shows the fix changes no output on this dataset, but it does not reproduce the committed live numbers.
- An internal-arithmetic break with fees exact is still labelled `FEE_MISMATCH`. It now escalates regardless, but a precise label would need a new exception type, which would change the taxonomy and the frozen per-type metrics, so I left it.

The explanation and reasoning are in `../out/NOTES.md`.
