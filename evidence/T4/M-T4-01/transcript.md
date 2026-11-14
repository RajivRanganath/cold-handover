# M-T4-01 transcript (PASS)

**Agent:** I'll start with the handover docs at the repo root, as the ground rules require.

**Bash:**
```
ls -la && find . -path ./.venv -prune -o -type f -print | grep -v __pycache__ | head -300
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
cat docs/architecture.md docs/limitations.md | head -400; echo ----; wc -l docs/*.md ledgerguard/reconciliation/*.py ledgerguard/ledger/*.py ledgerguard/evidence/*.py ledgerguard/pipeline.py ledgerguard/qa.py
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
... [19071 more characters in transcript.jsonl]
```

**Agent:** The docs point at a `residual_paise` guard in `safety.py` as the thing that should stop a case like this. Next I'll read the safety gate, invariants and matcher.

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
cat -n ledgerguard/ledger/invariants.py
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
... [4884 more characters in transcript.jsonl]
```

**Agent:** The evidence points at the `residual_paise` calculation. I'll check where it's used and where I1 failures get classified, and take a snapshot of the untouched repo so I can diff and verify artifacts later.

**Bash:**
```
cd <attempt>/work && mkdir -p ../tmp out && cp -R repo ../tmp/orig_repo_snapshot && rm -rf ../tmp/orig_repo_snapshot/.venv && cd repo && grep -rn "residual\|FEE_MISMATCH\|I1_\|fee_mismatch" --include=*.py --include=*.html . | grep -v "\.venv" 
```

**Result:**
```
mkdir: ../tmp: Operation not permitted
```

**Bash:**
```
cd <attempt>/work && ls -la .. && pwd && ls -la
```

**Result (error):**
```
Exit code 1
ls: ..: Operation not permitted
total 0
```

**Bash:**
```
pwd; ls -la; echo; ls -la <attempt>/work/repo | head -5
```

**Result:**
```
<attempt>/work/repo
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

total 88
drwxr-xr-x@ 10 user  staff    320 Nov 15 00:31 .
drwxr-xr-x@  5 user  staff    160 Nov 15 00:31 ..
-rw-r--r--@  1 user  staff   1992 Nov 15 00:31 .env.example
-rw-r--r--@  1 user  staff     56 Nov 15 00:31 .gitignore
```

**Agent:** The sandbox won't let me list or write the parent `work/` directory. I'll check whether `../out` and `../tmp` are reachable at all.

**Bash:**
```
ls -ld <attempt>/work/out <attempt>/work/tmp 2>&1; ls -ld <attempt>/work 2>&1; echo $TMPDIR
```

**Result:**
```
drwxr-xr-x@ 2 user  staff   64 Nov 15 00:31 <attempt>/work/out
drwxr-xr-x@ 4 user  staff  128 Nov 15 00:33 <attempt>/work/tmp
drwxr-xr-x@ 5 user  staff  160 Nov 15 00:31 <attempt>/work
<attempt>/work/tmp
```

**Agent:** The paths were fine, my earlier `cd` into `work/` was the mistake. From `repo/`, `../tmp` and `../out` both exist. Taking the snapshot again from there.

**Bash:**
```
cp -R . ../tmp/orig_repo_snapshot && rm -rf ../tmp/orig_repo_snapshot/.venv && ls ../tmp/orig_repo_snapshot && grep -rn "residual\|FEE_MISMATCH\|fee_mismatch\|window_undecidable" --include=*.py --include=*.html . | grep -v "\.venv"
```

**Result:**
```
docs
ledgerguard
README.md
requirements.txt
run_demo.sh
(eval):1: no matches found: --include=*.py
```

**Bash:**
```
grep -rn -e residual -e FEE_MISMATCH -e fee_mismatch -e I1_ --include=*.py --include=*.html --include=*.md . | grep -v "\.venv"
```

**Result:**
```
(eval):1: no matches found: --include=*.py
```

**Bash:**
```
grep -rn -e residual -e FEE_MISMATCH -e fee_mismatch -e I1_ ledgerguard docs README.md | grep -v "\.pyc"
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
ledgerguard/reconciliation/exceptions.py:22:    ExceptionType.FEE_MISMATCH,
ledgerguard/reconciliation/exceptions.py:54:    ExceptionType.FEE_MISMATCH: Risk.MEDIUM,
ledgerguard/ledger/models.py:110:    FEE_MISMATCH = "EXCEPTION_FEE_MISMATCH"
ledgerguard/evidence/safety.py:30:    ExceptionType.FEE_MISMATCH: "Fee and tax reconciled against the independent fee schedule; the exact variance is quantified.",
ledgerguard/evidence/safety.py:114:    residual = exc.evidence.get("residual_paise") or 0
ledgerguard/evidence/safety.py:118:        if residual:
ledgerguard/evidence/safety.py:128:                    f"{to_rupees_str(abs(residual))} INR unattributed, with no record "
ledgerguard/evidence/safety.py:131:                missing_evidence=["explanation for the residual deduction"],
ledgerguard/tests/test_p2_evaluation.py:119:    assert shifted.dominant_exception == "EXCEPTION_FEE_MISMATCH"
ledgerguard/ledger/invariants.py:50:        name="I1_settlement_arithmetic_consistent",
ledgerguard/ledger/invariants.py:181:    "I1_settlement_arithmetic_consistent",
ledgerguard/tests/test_p0_core.py:205:        FaultClass.F4_FEE_TAX_MISMATCH: "EXCEPTION_FEE_MISMATCH",
ledgerguard/tests/test_p1_compound.py:6:    money; any unattributed residual blocks closure, while a second finding that
ledgerguard/tests/test_p1_compound.py:46:def test_an_unattributed_residual_blocks_closure_on_the_proven_cause():
ledgerguard/tests/test_p1_compound.py:51:    residual = outcome.case.exception.evidence["residual_paise"]
ledgerguard/tests/test_p1_compound.py:52:    assert residual == to_paise("650.00"), residual
ledgerguard/tests/test_p1_compound.py:57:    # C5 is the same shape with the residual explained by a refund that belongs
ledgerguard/tests/test_p1_compound.py:60:    assert c5.case.exception.evidence["residual_paise"] == to_paise("900.00")
ledgerguard/tests/test_p1_compound.py:70:    assert not outcome.case.exception.evidence.get("residual_paise")
ledgerguard/synthetic/fault_injector.py:123:        expected_exception=ExceptionType.FEE_MISMATCH.value,
ledgerguard/evaluation/outputs/drift.md:12:| `fee_rate_2.25pct` | platform fee 2.00% -> 2.25% | 218 | 0 | 218 | 100.0% | FEE_MISMATCH |
ledgerguard/evaluation/outputs/drift.md:13:| `fee_rate_2.5pct` | platform fee 2.00% -> 2.50% | 218 | 0 | 218 | 100.0% | FEE_MISMATCH |
ledgerguard/evaluation/outputs/drift.md:14:| `fee_rate_1.75pct` | platform fee 2.00% -> 1.75% (in our favour) | 218 | 0 | 218 | 100.0% | FEE_MISMATCH |
ledgerguard/evaluation/outputs/reconciliation_report.csv:12:pay_0029AD38,ord_0029B12F,pay_0029AD38,AUTO_RESOLVED,EXCEPTION_FEE_MISMATCH,89164.00,87059.73,86429.61,-630.12,setl_0029167F,2026-06-27,I2_fees_and_tax_match_schedule; I3_net_matches_shadow_ledger,,,,,,Fee and tax reconciled against the independent fee schedule; the exact variance is quantified.,No action; classified and closed by the deterministic engine.
ledgerguard/evaluation/outputs/reconciliation_report.csv:16:pay_0037DAA0,ord_0037B003,pay_0037DAA0,AUTO_RESOLVED,EXCEPTION_FEE_MISMATCH,10655.00,10403.54,10256.04,-147.50,setl_00373C9A,2026-06-23,I2_fees_and_tax_match_schedule; I3_net_matches_shadow_ledger,,,,,,Fee and tax reconciled against the independent fee schedule; the exact variance is quantified.,No action; cla
... [11114 more characters in transcript.jsonl]
```

**Agent:** The residual guard is tested in `test_p1_compound.py` and described in `docs/evaluation.md`. I'll read both, along with the compound generator they exercise.

**Bash:**
```
cat -n ledgerguard/tests/test_p1_compound.py; echo ----; sed -n 160,240p docs/evaluation.md
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
... [5603 more characters in transcript.jsonl]
```

**Agent:** C2 and C5 pin a residual of exactly 650.00 and 900.00, so my fix must keep those values. Next I'll look at how the generator builds settlements, to confirm which invariant fails in the reported shape.

**Bash:**
```
cat -n ledgerguard/synthetic/compound.py | sed -n 1,200p
```

**Result:**
```
     1	"""Hand-designed compound failure cases.
     2	
     3	The generated fault taxonomy injects one fault per lifecycle. Real
     4	reconciliation failures are not that tidy: a settlement can be both late and
     5	short, or carry a fee overcharge *and* an unexplained deduction. Compound cases
     6	are where a controller that classifies by "first failing invariant" quietly
     7	closes a case on one proven cause while a second, unproven one is still open.
     8	
     9	These five are built by hand rather than generated, because the point is not
    10	volume -- it is that each one probes a specific way the single-cause assumption
    11	can break.
    12	
    13	Kept out of the generator on purpose: adding them to the seeded dataset would
    14	change the frozen holdout and invalidate every published number.
    15	"""
    16	
    17	from __future__ import annotations
    18	
    19	from dataclasses import dataclass
    20	from datetime import datetime, timedelta
    21	
    22	from ..ledger.models import (
    23	    BankEntry,
    24	    Batch,
    25	    CreditDebit,
    26	    Order,
    27	    Payment,
    28	    Refund,
    29	    Settlement,
    30	)
    31	from ..ledger.money import gst_on_fee, platform_fee, to_paise
    32	
    33	T0 = datetime(2026, 7, 15, 10, 0, 0)
    34	
    35	AUTO = "AUTO_RESOLVED"
    36	HUMAN = "HUMAN_REVIEW_REQUIRED"
    37	
    38	
    39	@dataclass(frozen=True)
    40	class CompoundCase:
    41	    case_id: str
    42	    name: str
    43	    faults: tuple[str, ...]
    44	    payment_id: str
    45	    expected_disposition: str
    46	    why: str
    47	
    48	
    49	def _leg(
    50	    tag: str,
    51	    customer: str,
    52	    amount: int,
    53	    *,
    54	    fee_overcharge: int = 0,
    55	    refund_adjustment: int = 0,
    56	    days_late: int = 0,
    57	    settle: bool = True,
    58	    duplicate_bank_credit: bool = False,
    59	):
    60	    """One lifecycle, with each fault applied independently and explicitly."""
    61	    order = Order(
    62	        order_id=f"ord_{tag}",
    63	        merchant_id="mch_CMPD",
    64	        amount=amount,
    65	        created_at=T0,
    66	        customer_reference=customer,
    67	    )
    68	    fee = platform_fee(amount)
    69	    tax = gst_on_fee(fee)
    70	    captured = T0 + timedelta(minutes=5)
    71	    payment = Payment(
    72	        payment_id=f"pay_{tag}",
    73	        order_id=order.order_id,
    74	        amount=amount,
    75	        captured_at=captured,
    76	        fee=fee,
    77	        tax=tax,
    78	        reference=f"PAY/{order.order_id}",
    79	    )
    80	    if not settle:
    81	        return order, payment, None, []
    82	
    83	    charged_fee = fee + fee_overcharge
    84	    charged_tax = gst_on_fee(charged_fee)
    85	    net = amount - charged_fee - charged_tax - refund_adjustment
    86	    settled_on = captured + timedelta(days=2 + days_late)
    87	    settlement = Settlement(
    88	        settlement_id=f"setl_{tag}",
    89	        merchant_id=order.merchant_id,
    90	        payment_ids=[payment.payment_id],
    91	        gross_amount=amount,
    92	        fees=charged_fee,
    93	        tax=charged_tax,
    94	        refund_adjustments=refund_adjustment,
    95	        other_adjustments=0,
    96	        net_amount=net,
    97	        settlement_date=settled_on,
    98	        reference=f"STL/setl_{tag}",
    99	    )
   100	    entries = [
   101	        BankEntry(
   102	            bank_entry_id=f"bnk_{tag}",
   103	            amount=net,
   104	            credit_or_debit=CreditDebit.CREDIT,
   105	            date=settled_on,
   106	            reference=settlement.reference,
   107	        )
   108	    ]
   109	    if duplicate_bank_credit:
   110	        entries.append(entries[0].model_copy(update={"bank_entry_id": f"bnk_{tag}D"}))
   111	    return order, payment, settlement, entries
   112	
   113	
   114	def build_compound_batch() -> tupl
... [4801 more characters in transcript.jsonl]
```

**Bash:**
```
cat -n ledgerguard/synthetic/fault_injector.py | sed -n 1,200p
```

**Result:**
```
     1	"""Controlled fault injection over clean lifecycles.
     2	
     3	Every injected fault records its ground truth: which lifecycle was corrupted,
     4	what the true cause is, what exception the controller *should* raise, and what
     5	the *safe* disposition is. "Safe disposition" is deliberately not "resolve
     6	everything" -- for two fault classes the correct behaviour is to abstain.
     7	"""
     8	
     9	from __future__ import annotations
    10	
    11	import random
    12	from copy import deepcopy
    13	
    14	from ..ledger.models import BankEntry, CreditDebit, ExceptionType, RefundStatus
    15	from ..ledger.money import gst_on_fee, platform_fee
    16	from .generator import Dataset, FaultClass, GroundTruth, Lifecycle, build_clean_lifecycles
    17	
    18	# Share of lifecycles that receive a fault.
    19	FAULT_RATE = 0.32
    20	
    21	AUTO = "AUTO_RESOLVED"
    22	HUMAN = "HUMAN_REVIEW_REQUIRED"
    23	NONE = "NONE"
    24	
    25	
    26	def _noisy_customer_reference(customer: str, rng: random.Random) -> str:
    27	    """A dirty free-text refund reference: the customer, never the order id.
    28	
    29	    This is what makes F3/F6 genuinely ambiguous for a structured matcher. The
    30	    matcher does exact ID matching only; a customer can have several orders, so
    31	    even parsing this string does not identify which payment the refund belongs
    32	    to. Selecting the payment is the investigator's job; proving the selection
    33	    is the Evidence Gate's job.
    34	    """
    35	    template = rng.choice(
    36	        [
    37	            "ADJ/{c}/partial",
    38	            "REF {c} - cust adj",
    39	            "chargeback-adj {c}",
    40	            "{c}/refund posted",
    41	        ]
    42	    )
    43	    return template.format(c=customer)
    44	
    45	
    46	def _apply_f1(lc: Lifecycle, rng: random.Random) -> GroundTruth:
    47	    """Missing settlement: payment captured, settlement and credit never arrived."""
    48	    exposure = lc.settlement.net_amount if lc.settlement else lc.payment.amount
    49	    lc.settlement = None
    50	    lc.bank_entries = []
    51	    return GroundTruth(
    52	        lifecycle_id=lc.lifecycle_id,
    53	        fault_class=FaultClass.F1_MISSING_SETTLEMENT,
    54	        expected_exception=ExceptionType.MISSING_SETTLEMENT.value,
    55	        expected_disposition=HUMAN,
    56	        true_cause="Captured payment was never settled; funds are outstanding.",
    57	        exposure_paise=exposure,
    58	    )
    59	
    60	
    61	def _apply_f2(lc: Lifecycle, rng: random.Random) -> GroundTruth:
    62	    """Duplicate record: the same event is ingested twice."""
    63	    if rng.random() < 0.5 and lc.bank_entries:
    64	        dup = deepcopy(lc.bank_entries[0])
    65	        dup.bank_entry_id = dup.bank_entry_id + "D"
    66	        lc.bank_entries.append(dup)
    67	        detail = f"Bank credit {lc.bank_entries[0].bank_entry_id} re-ingested as {dup.bank_entry_id}."
    68	        exposure = dup.amount
    69	    else:
    70	        lc.extra_payments.append(deepcopy(lc.payment))
    71	        detail = f"Payment {lc.payment.payment_id} appears twice in the batch."
    72	        exposure = lc.payment.amount
    73	    return GroundTruth(
    74	        lifecycle_id=lc.lifecycle_id,
    75	        fault_class=FaultClass.F2_DUPLICATE_RECORD,
    76	        expected_exception=ExceptionType.DUPLICATE_RECORD.value,
    77	        expected_disposition=AUTO,
    78	        true_cause=detail,
    79	        exposure_paise=exposure,
    80	    )
    81	
    82	
    83	def _apply_f3(lc: Lifecycle, rng: random.Random) -> GroundTruth:
    84	    """Unlinked partial refund.
    85	
    86	    The settlement correctly deducted a partial refund, but the refund record
    87	    lost its payment linkage and carries only a dirty customer reference. The
    88	    Shadow Ledger therefore expects a higher net than was paid out.
    
... [5087 more characters in transcript.jsonl]
```

**Agent:** F4 injection keeps I1 consistent, so the holdout's fee cases never exercise the path I suspect. I'll reproduce the reported shape directly: fees and tax on schedule, but the settlement's net 250 below its own components. First, the batch builder tail and the pipeline entry point.

**Bash:**
```
sed -n 194,230p ledgerguard/synthetic/compound.py; echo ----; cat -n ledgerguard/pipeline.py | sed -n 1,186p
```

**Result:**
```
    return (
        Batch(
            orders=orders,
            payments=payments,
            refunds=refunds,
            settlements=settlements,
            bank_entries=entries,
        ),
        cases,
    )
----
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
   100	    lifecy
... [3745 more characters in transcript.jsonl]
```

**Agent:** Now a reproduction script, kept in `../tmp` outside the repo. It builds one lifecycle with fees exactly on schedule and the settlement net 250 below its own components, then runs the pipeline.

**Bash:**
```
mkdir -p ../tmp/scripts && cat > ../tmp/scripts/repro.py <<'EOF'
from datetime import timedelta
from ledgerguard.ledger.models import Batch
from ledgerguard.ledger.money import to_paise
from ledgerguard.synthetic.compound import _leg
from ledgerguard.pipeline import run
from ledgerguard.ai.provider import HeuristicProvider
from ledgerguard.reconciliation.matcher import reconcile_batch

o, p, s, e = _leg("R1", "CUST-R1", to_paise("5000.00"))
short = to_paise("250.00")
s.net_amount -= short              # components say X, the reported net is 250 lower
for b in e:
    b.amount = s.net_amount
batch = Batch(orders=[o], payments=[p], refunds=[], settlements=[s], bank_entries=e)
cases, _ = reconcile_batch(batch)
c = cases[0]
print("status:", c.status)
print("evidence:", {k: c.exception.evidence.get(k) for k in ("residual_paise", "secondary_findings")})
print("invariants:", [(i.name, i.holds) for i in c.invariants])
for label, kw in [("rules-only", dict(use_ai=False)), ("hybrid-heuristic", dict(use_ai=True, provider=HeuristicProvider()))]:
    r = run(batch, **kw)
    o1 = r.outcomes[0]
    print(label, "->", o1.state, "|", o1.decision.reason if o1.decision else None)
EOF
cd <attempt>/work/repo && .venv/bin/python -I -c "import sys; sys.path.insert(0,'.'); exec(open('../tmp/scripts/repro.py').read())"
```

**Result:**
```
status: EXCEPTION_FEE_MISMATCH
evidence: {'residual_paise': 0, 'secondary_findings': []}
invariants: [('I1_settlement_arithmetic_consistent', False), ('I2_fees_and_tax_match_schedule', True), ('I3_net_matches_shadow_ledger', False), ('I4_gross_matches_capture', True), ('I5_settlement_within_window', True), ('I6_bank_credit_matches_settlement', True)]
rules-only -> AUTO_RESOLVED | Fee and tax reconciled against the independent fee schedule; the exact variance is quantified.
hybrid-heuristic -> AUTO_RESOLVED | Fee and tax reconciled against the independent fee schedule; the exact variance is quantified.
```

**Agent:** Reproduced: the short settlement comes out `AUTO_RESOLVED`, with `residual_paise` = 0. There are two defects in `matcher.py`:

1. **The residual ignores the settlement's own net.** `corrected_net` is rebuilt from gross, fees, tax, refunds and adjustments, so a row whose reported net is wrong by 250 yields residual 0.
2. **An arithmetic break is labelled a fee mismatch.** `_classify` maps an I1 failure to `FEE_MISMATCH` even when I2 says fees and tax are exact. The fee-mismatch closure path then runs on a case with no fee problem.

Before changing anything I need to know how the benchmark builds the holdout and whether any holdout case already hits the I1 path. That determines how I verify the "benchmark unchanged" requirement without overwriting artifacts.

**Bash:**
```
grep -n "^def \|^class \|open(\|write\|OUT\|frozen\|sha" ledgerguard/evaluation/benchmark.py | head -80; echo ----; grep -n "^def \|open(\|write_text\|OUT" ledgerguard/evaluation/baseline.py ledgerguard/evaluation/metrics.py ledgerguard/evaluation/report.py | head -40
```

**Result:**
```
7:same frozen holdout, and writes every artifact under evaluation/outputs/.
36:OUTPUT_DIR = Path(__file__).parent / "outputs"
37:MANIFEST_DIR = Path(__file__).parent / "frozen"
40:def manifest_path(seed: int, count: int) -> Path:
41:    """One frozen manifest per dataset configuration.
44:    can never silently overwrite the holdout an earlier result was scored on.
49:def batch_digest(dataset: Dataset) -> str:
50:    return hashlib.sha256(dataset.batch().model_dump_json().encode()).hexdigest()
53:def freeze_or_verify_holdout(holdout: Dataset, seed: int, count: int) -> dict:
60:        "holdout_batch_sha256": batch_digest(holdout),
67:                "FROZEN HOLDOUT MISMATCH.\n"
68:                "The holdout for this seed was frozen earlier and the regenerated "
71:                "delete the manifest deliberately and say so in the write-up.\n"
72:                f"  frozen sha256:      {existing.get('holdout_batch_sha256')}\n"
73:                f"  regenerated sha256: {manifest['holdout_batch_sha256']}"
77:    path.write_text(json.dumps(manifest, indent=2) + "\n")
81:def _row(label: str, baseline, hybrid, fmt=str) -> str:
85:def render_markdown(base: Metrics, hyb: Metrics, manifest: dict) -> str:
94:        f"batch SHA-256 `{manifest['holdout_batch_sha256'][:16]}`.",
149:def write_unresolved_csv(report: RunReport, dataset: Dataset, path: Path) -> int:
153:    with path.open("w", newline="") as fh:
154:        writer = csv.writer(fh)
155:        writer.writerow(
177:            writer.writerow(
195:def export_cases(report: RunReport, dataset: Dataset, path: Path) -> None:
235:    path.write_text(json.dumps(payload, indent=2, default=str) + "\n")
238:def main(argv: list[str] | None = None) -> int:
244:        help="which slice to score (default: the frozen holdout)",
254:    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
277:    (OUTPUT_DIR / "benchmark.md").write_text(md)
278:    (OUTPUT_DIR / "benchmark.json").write_text(
287:                    "batch_sha256": batch_digest(scored),
300:    n_unresolved = write_unresolved_csv(
301:        hybrid_report, scored, OUTPUT_DIR / "unresolved_exceptions.csv"
303:    export_cases(hybrid_report, scored, OUTPUT_DIR / "cases.json")
337:    print(f"\nArtifacts written to {OUTPUT_DIR}")
344:            "or OMNIROUTE_API_KEY) and rerun to measure against a real investigator."
----
ledgerguard/evaluation/baseline.py:18:def run_baseline(batch: Batch, lifecycle_by_payment: dict[str, str] | None = None) -> RunReport:
ledgerguard/evaluation/metrics.py:88:def _percentile(values: list[float], p: float) -> float:
ledgerguard/evaluation/metrics.py:96:def compute(report: RunReport, dataset: Dataset) -> Metrics:
ledgerguard/evaluation/report.py:29:OUTPUT_DIR = Path(__file__).parent / "outputs"
ledgerguard/evaluation/report.py:45:def write_reconciliation_report(
ledgerguard/evaluation/report.py:46:    report: RunReport, output_dir: Path = OUTPUT_DIR
ledgerguard/evaluation/report.py:51:    with (output_dir / "reconciliation_report.csv").open("w", newline="") as fh:
ledgerguard/evaluation/report.py:106:    with (output_dir / "evidence_ledger.csv").open("w", newline="") as fh:
ledgerguard/evaluation/report.py:148:    (output_dir / "reconciliation_report.md").write_text("\n".join(md) + "\n")
ledgerguard/evaluation/report.py:152:def main(argv: list[str] | None = None) -> int:
ledgerguard/evaluation/report.py:170:    print((OUTPUT_DIR / "reconciliation_report.md").read_text())
ledgerguard/evaluation/report.py:171:    print(f"Artifacts written to {OUTPUT_DIR}")
```

**Bash:**
```
sed -n 36,80p ledgerguard/evaluation/benchmark.py; echo ----; sed -n 238,275p ledgerguard/evaluation/benchmark.py; echo ----; grep -n "def \|holdout\|split" ledgerguard/evaluation/benchmark.py | sed -n 1,60p | tail -30
```

**Result:**
```
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


----
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

----
31:from ..synthetic.fault_injector import build_dataset, split
40:def manifest_path(seed: int, count: int) -> Path:
44:    can never silently overwrite the holdout an earlier result was scored on.
46:    return MANIFEST_DIR / f"holdout_{seed}_{count}.json"
49:def batch_digest(dataset: Dataset) -> str:
53:def freeze_or_verify_holdout(holdout: Dataset, seed: int, count: int) -> dict:
54:    """Write the holdout manifest once; afterwards, verify nothing drifted."""
58:        "generator_version": holdout.generator_version,
59:        "h
... [1530 more characters in transcript.jsonl]
```

**Agent:** The holdout manifest already exists, so the benchmark won't rewrite it. I'll write a read-only comparison script in `../tmp`. It runs the holdout through the deterministic baseline and the hybrid with the offline heuristic (fully deterministic), and dumps every case's outcome. I'll run it against the original snapshot and against my edited tree, then diff. I'm not calling the benchmark `main()`, which writes into `outputs/`.

**Bash:**
```
cat > ../tmp/scripts/dump_holdout.py <<'EOF'
"""Read-only: dump per-case outcomes for the frozen holdout. Writes only to argv[2]."""
import json, sys
root, out = sys.argv[1], sys.argv[2]
sys.path.insert(0, root)
from ledgerguard.synthetic.fault_injector import build_dataset, split
from ledgerguard.pipeline import run
from ledgerguard.ai.provider import HeuristicProvider
from ledgerguard.evaluation.benchmark import batch_digest
import ledgerguard
assert ledgerguard.__file__.startswith(root), ledgerguard.__file__

full = build_dataset(seed=20260905, count=320)
dev, holdout = split(full)
lbp = holdout.lifecycle_by_payment()
batch = holdout.batch()
rows = {}
for label, kw in [("baseline", dict(use_ai=False)),
                  ("hybrid_heuristic", dict(use_ai=True, provider=HeuristicProvider()))]:
    rep = run(batch, lifecycle_by_payment=lbp, **kw)
    rows[label] = [
        dict(case=o.case_id, status=o.case.status, state=o.state,
             resolution=(o.decision.resolution if o.decision else None),
             verdict=(o.verification.verdict if o.verification else None),
             hyp=(o.investigation.result.hypothesis if o.investigation else None),
             invs_failing=[i.name for i in o.case.failing_invariants()],
             residual=(o.case.exception.evidence.get("residual_paise") if o.case.exception else None),
             reason=(o.decision.reason if o.decision else None))
        for o in rep.outcomes
    ]
    rows[label + "_summary"] = dict(
        auto=sum(1 for o in rep.outcomes if o.state == "AUTO_RESOLVED"),
        investigations=rep.investigations, model_calls=rep.model_calls)
rows["digest"] = batch_digest(holdout)
json.dump(rows, open(out, "w"), indent=1, sort_keys=True, default=str)
print("cases", len(rows["baseline"]), "summary", rows["baseline_summary"], rows["hybrid_heuristic_summary"], "digest", rows["digest"][:16])
EOF
cd ../tmp/scripts && <attempt>/work/repo/.venv/bin/python -I dump_holdout.py <attempt>/work/tmp/orig_repo_snapshot <attempt>/work/tmp/before.json && cd <attempt>/work/repo && ../tmp/scripts/../../tmp/x 2>/dev/null; <attempt>/work/repo/.venv/bin/python -I -c "
import json
d=json.load(open('<attempt>/work/tmp/before.json'))
bad=[r for r in d['baseline'] if 'I1_settlement_arithmetic_consistent' in r['invs_failing']]
print('holdout cases with I1 failing:', len(bad))
"
```

**Result:**
```
cases 85 summary {'auto': 12, 'investigations': 0, 'model_calls': 0} {'auto': 21, 'investigations': 15, 'model_calls': 0} digest 3e28d4572d4cfc95
holdout cases with I1 failing: 0
```

**Agent:** The holdout digest matches the documented `3e28d4572d4cfc95`, the rules-only baseline auto-resolves 12 (matching the published figure), and no holdout case has an I1 failure. I'll check the exception taxonomy and the investigation gate before choosing the fix.

**Bash:**
```
sed -n 1,85p ledgerguard/reconciliation/exceptions.py; echo ----; grep -n "def should_investigate" -A 12 ledgerguard/ai/investigator.py
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
----
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

**Agent:** The taxonomy is clear: an unexplained shortfall is the right home for a settlement that is short with no cause. Here's the plan:

- **Residual (root cause 1):** measure it against the settlement's *reported* net, correcting only the fee variance. When I1 holds this is algebraically identical to today's formula, so every existing residual (C2's 650, C5's 900) is unchanged. It only differs when the settlement contradicts its own components.
- **Classification (root cause 2):** an I1 failure alone is no longer a fee mismatch. It becomes `UNEXPLAINED_SHORTFALL`, which means money missing with no cause proved.
- **Closure guard:** a settlement whose reported net differs from its own components never auto-closes, whatever the classification. This also stops the gate from closing it on a coincidentally matching orphan refund, because the gate's E7 check only re-tests the same contradictory net.

Holdout behaviour should not change, since no holdout case has an I1 failure. Starting with the matcher.

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

**Agent:** Next, the residual and the arithmetic-gap evidence in `reconcile_payment`.

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

**Agent:** Now the closure guard in `safety.py`, placed after the content-conflict check and ahead of every auto-close route.

**Edit:**
```
<attempt>/work/repo/ledgerguard/evidence/safety.py
```

**Result:**
```
The file <attempt>/work/repo/ledgerguard/evidence/safety.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

**Agent:** I'll tighten that comment, which reads awkwardly, then rerun the reproduction.

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
.venv/bin/python -I -c "import sys; sys.path.insert(0,'.'); exec(open('../tmp/scripts/repro.py').read())"
```

**Result:**
```
status: EXCEPTION_UNEXPLAINED_SHORTFALL
evidence: {'residual_paise': None, 'secondary_findings': []}
invariants: [('I1_settlement_arithmetic_consistent', False), ('I2_fees_and_tax_match_schedule', True), ('I3_net_matches_shadow_ledger', False), ('I4_gross_matches_capture', True), ('I5_settlement_within_window', True), ('I6_bank_credit_matches_settlement', True)]
rules-only -> HUMAN_REVIEW_REQUIRED | The settlement's reported net is 250.00 INR below what its own gross, fees, tax, refunds and adjustments add up to, and no record explains the difference. Not closed automatically, whatever the classification.
hybrid-heuristic -> HUMAN_REVIEW_REQUIRED | The settlement's reported net is 250.00 INR below what its own gross, fees, tax, refunds and adjustments add up to, and no record explains the difference. Not closed automatically, whatever the classification.
```

**Agent:** The reported shape now escalates under both rules-only and the hybrid, with the 250.00 shortfall named. Next, the full existing test suite.

**Bash:**
```
timeout 900 .venv/bin/python -m pytest ledgerguard/tests -q 2>&1 | tail -25
```

**Result:**
```
(eval):1: command not found: timeout
```

**Bash:**
```
.venv/bin/python -m pytest ledgerguard/tests -q -p no:cacheprovider 2>&1 | tail -25
```

**Result:**
```
...................................................................      [100%]
=============================== warnings summary ===============================
.venv/lib/python3.14/site-packages/fastapi/testclient.py:1
  <attempt>/work/repo/.venv/lib/python3.14/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
67 passed, 1 warning in 8.12s
```

**Agent:** All 67 existing tests pass. Some tests may write into `outputs/`, so I'll diff the repo against the snapshot now, then run the holdout comparison.

**Bash:**
```
cd <attempt>/work && diff -rq tmp/orig_repo_snapshot repo -x .venv -x __pycache__ -x .pytest_cache; echo "exit=$?"; cd repo && .venv/bin/python -I ../tmp/scripts/dump_holdout.py "$(pwd)" ../tmp/after.json && .venv/bin/python -I -c "
import json
b=json.load(open('../tmp/before.json')); a=json.load(open('../tmp/after.json'))
for k in ['baseline','hybrid_heuristic']:
    diffs=[(x['case'],{f:(x[f],y[f]) for f in x if x[f]!=y[f] and f!='reason'}) for x,y in zip(b[k],a[k]) if x!=y]
    print(k,'cases differing (excluding reason text):',[d for d in diffs if d[1]])
    print(k,'reason-text-only diffs:',sum(1 for x,y in zip(b[k],a[k]) if x!=y and {f for f in x if x[f]!=y[f]}=={'reason'}))
print('summaries before',b['baseline_summary'],b['hybrid_heuristic_summary'])
print('summaries after ',a['baseline_summary'],a['hybrid_heuristic_summary'])
print('digest same:', a['digest']==b['digest'])
"
```

**Result:**
```
Files tmp/orig_repo_snapshot/ledgerguard/evidence/safety.py and repo/ledgerguard/evidence/safety.py differ
Files tmp/orig_repo_snapshot/ledgerguard/reconciliation/matcher.py and repo/ledgerguard/reconciliation/matcher.py differ
exit=1
cases 85 summary {'auto': 12, 'investigations': 0, 'model_calls': 0} {'auto': 21, 'investigations': 15, 'model_calls': 0} digest 3e28d4572d4cfc95
baseline cases differing (excluding reason text): []
baseline reason-text-only diffs: 0
hybrid_heuristic cases differing (excluding reason text): []
hybrid_heuristic reason-text-only diffs: 0
summaries before {'auto': 12, 'investigations': 0, 'model_calls': 0} {'auto': 21, 'investigations': 15, 'model_calls': 0}
summaries after  {'auto': 12, 'investigations': 0, 'model_calls': 0} {'auto': 21, 'investigations': 15, 'model_calls': 0}
digest same: True
```

**Agent:** The holdout is unchanged: every per-case state, resolution, verdict, reason and the auto-resolved counts match exactly for both rules-only and the hybrid run. Only the two source files differ, and the `outputs/` and `frozen/` trees are untouched. I'll also compare all 320 generated lifecycles and the compound batch, so that the dev split and the other analyses are covered too.

**Bash:**
```
cat > ../tmp/scripts/dump_all.py <<'EOF'
import json, sys
root, out = sys.argv[1], sys.argv[2]
sys.path.insert(0, root)
from ledgerguard.synthetic.fault_injector import build_dataset
from ledgerguard.synthetic.compound import build_compound_batch
from ledgerguard.pipeline import run
from ledgerguard.ai.provider import HeuristicProvider
import ledgerguard
assert ledgerguard.__file__.startswith(root)
full = build_dataset(seed=20260905, count=320)
rows = {}
batch = full.batch(); lbp = full.lifecycle_by_payment()
cb, _ = build_compound_batch()
for name, b, l in [("all320", batch, lbp), ("compound", cb, None)]:
    for label, kw in [("baseline", dict(use_ai=False)), ("hybrid_heuristic", dict(use_ai=True, provider=HeuristicProvider()))]:
        rep = run(b, lifecycle_by_payment=l, **kw)
        rows[f"{name}/{label}"] = [dict(case=o.case_id, status=o.case.status, state=o.state,
            resolution=(o.decision.resolution if o.decision else None),
            verdict=(o.verification.verdict if o.verification else None),
            reason=(o.decision.reason if o.decision else None),
            residual=(o.case.exception.evidence.get("residual_paise") if o.case.exception else None))
            for o in rep.outcomes]
json.dump(rows, open(out, "w"), indent=1, sort_keys=True, default=str)
print({k: len(v) for k, v in rows.items()})
EOF
cd <attempt>/work/repo && ../../repo/.venv/bin/python -I ../tmp/scripts/dump_all.py <attempt>/work/tmp/orig_repo_snapshot ../tmp/all_before.json && .venv/bin/python -I ../tmp/scripts/dump_all.py "$(pwd)" ../tmp/all_after.json && cmp ../tmp/all_before.json ../tmp/all_after.json && echo IDENTICAL
```

**Result (error):**
```
Exit code 127
(eval):27: no such file or directory: ../../repo/.venv/bin/python
```

**Bash:**
```
.venv/bin/python -I ../tmp/scripts/dump_all.py <attempt>/work/tmp/orig_repo_snapshot ../tmp/all_before.json && .venv/bin/python -I ../tmp/scripts/dump_all.py "$(pwd)" ../tmp/all_after.json && cmp ../tmp/all_before.json ../tmp/all_after.json && echo IDENTICAL
```

**Result:**
```
{'all320/baseline': 320, 'all320/hybrid_heuristic': 320, 'compound/baseline': 5, 'compound/hybrid_heuristic': 5}
{'all320/baseline': 320, 'all320/hybrid_heuristic': 320, 'compound/baseline': 5, 'compound/hybrid_heuristic': 5}
IDENTICAL
```

**Agent:** All 320 generated lifecycles and the five compound cases are byte-identical before and after, both rules-only and hybrid, including residuals. So the change only affects settlements that contradict their own components.

Now the new tests. For the orphan-refund case I want the gate to actually reach VERIFIED, so the test proves the guard is what stops it. I'll check what the heuristic provider and existing fixtures give me first.

**Bash:**
```
grep -n "class HeuristicProvider" -A 40 ledgerguard/ai/provider.py | head -70; echo ----; grep -n "def \|Refund(" ledgerguard/tests/test_p0_core.py | head -40
```

**Result:**
```
140:class HeuristicProvider:
141-    """Offline stand-in. Deliberately naive: matches on amount, not on linkage.
142-
143-    This is not a model and is never reported as one. It exists so the pipeline
144-    runs without an API key, and so the adversarial case can be demonstrated
145-    against the *worst plausible* investigator rather than a lucky one.
146-    """
147-
148-    name = "heuristic_stub"
149-
150-    def investigate(self, context: dict) -> InvestigationResult:
151-        candidates = context.get("candidate_evidence", []) or []
152-        shortfall = context.get("discrepancy", {}).get("difference_paise")
153-        exc_type = context.get("exception", {}).get("type", "")
154-
155-        refund_matches = [
156-            c
157-            for c in candidates
158-            if c.get("record_type") == "refund" and c.get("amount") == shortfall
159-        ]
160-        if refund_matches:
161-            picked = refund_matches[0]
162-            out = InvestigatorOutput(
163-                hypothesis="unlinked_partial_refund",
164-                reason=(
165-                    f"Refund {picked['refund_id']} is for {picked['amount']} paise, exactly the "
166-                    f"unexplained shortfall, and carries no payment linkage. It most likely "
167-                    f"belongs to this payment and lost its link during ingestion."
168-                ),
169-                required_evidence=[
170-                    RequiredEvidence(
171-                        type="refund",
172-                        expected_relationship="refund belongs to this payment (customer and order must agree)",
173-                    ),
174-                    RequiredEvidence(
175-                        type="refund",
176-                        expected_relationship="refund.amount == shadow ledger shortfall",
177-                    ),
178-                    RequiredEvidence(
179-                        type="refund",
180-                        expected_relationship="refund.created_at is after capture and before settlement",
----
41:def test_1_financial_arithmetic_is_exact():
75:def _lifecycle(amount: int = 500000, refund_amount: int | None = None):
98:            Refund(
140:def test_2_shadow_ledger_invariants_separate_good_from_corrupted():
182:def test_2b_generated_clean_lifecycles_reconcile_without_exceptions():
223:def _adversarial_run():
246:def test_3_evidence_gate_accepts_a_correctly_linked_refund():
271:def test_4_evidence_gate_rejects_a_refund_belonging_to_another_payment():
310:def test_5_insufficient_evidence_abstains_and_never_force_resolves():
336:        def investigate(self, context):
346:        def investigate(self, context):
365:def test_5b_malformed_and_contested_evidence_degrade_safely():
```

**Bash:**
```
sed -n 75,135p ledgerguard/tests/test_p0_core.py; sed -n 246,270p ledgerguard/tests/test_p0_core.py
```

**Result:**
```
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
def test_3_evidence_gate_accepts_a_correctly_linked_refund():
    """Payment B's shortfall really is its own refund. The gate must prove it."""
    from ledgerguard.evidence.verifier import VERIFIED
    from ledgerguard.evidence.safety import AUTO_RESOLVED
    from ledgerguard.synthetic.adversarial import DONOR_PAYMENT_ID, ORPHAN_REFUND_ID

    outcome = _adversarial_run()[DONOR_PAYMENT_ID]

    assert outcome.investigation is not None, "an ambiguous shortfall must be investigated"
    assert outcome.investigation.result.hypothesis == "unlinked_partial_refund"

    ver = outcome.verification
    assert ver.verdict == VERIFIED, [c.as_dict() for c in ver.failed()]
    assert ver.claimed_evidence_ids == [ORPHAN_REFUND_ID]
    assert ver.passed_count == ver.total_count

    # The decisive check is the ledger re-derivation, not the model's say-so.
    restored = next(c for c in ver.checks if c.name == "E7_invariant_restored")
    assert restored.passed
    linkage = next(c for c in ver.checks if c.name == "E4_reference_identifies_this_customer")
    assert linkage.passed

    assert outcome.decision.state == AUTO_RESOLVED
```

**Agent:** I have what I need. The new test file builds its own small lifecycle rather than importing the private compound helper. It covers the reported shape under both rules-only and hybrid runs, the residual value, the reclassification, a clean fee overcharge still closing, the components-disagree-but-net-right case, and the orphan-refund case where the gate is shown to reach VERIFIED.

**Write:**
```
<attempt>/work/repo/ledgerguard/tests/test_p1_settlement_arithmetic.py
```

**Result:**
```
File created successfully at: <attempt>/work/repo/ledgerguard/tests/test_p1_settlement_arithmetic.py (file state is current in your context — no need to Read it back)
```

**Bash:**
```
.venv/bin/python -m pytest ledgerguard/tests/test_p1_settlement_arithmetic.py -q -p no:cacheprovider 2>&1 | tail -40
```

**Result:**
```
........                                                                 [100%]
8 passed in 0.79s
```

**Agent:** All 8 pass. To show they actually detect the defect, I'll run the same file against the original snapshot, where they should fail.

**Bash:**
```
cp ledgerguard/tests/test_p1_settlement_arithmetic.py ../tmp/orig_repo_snapshot/ledgerguard/tests/ && cd <attempt>/work/tmp/orig_repo_snapshot && <attempt>/work/repo/.venv/bin/python -m pytest ledgerguard/tests/test_p1_settlement_arithmetic.py -q -p no:cacheprovider 2>&1 | grep -E "passed|failed|FAILED"; cd <attempt>/work/repo
```

**Result:**
```
FAILED ledgerguard/tests/test_p1_settlement_arithmetic.py::test_the_reported_shape_is_not_classified_as_a_fee_mismatch
FAILED ledgerguard/tests/test_p1_settlement_arithmetic.py::test_the_reported_shape_is_never_auto_resolved_rules_only
FAILED ledgerguard/tests/test_p1_settlement_arithmetic.py::test_the_reported_shape_is_never_auto_resolved_with_the_investigator
FAILED ledgerguard/tests/test_p1_settlement_arithmetic.py::test_a_matching_orphan_refund_cannot_close_a_settlement_that_does_not_add_up
FAILED ledgerguard/tests/test_p1_settlement_arithmetic.py::test_components_that_disagree_with_a_correct_net_are_not_closed
FAILED ledgerguard/tests/test_p1_settlement_arithmetic.py::test_residual_is_the_unexplained_money_when_a_fee_overcharge_is_also_present
FAILED ledgerguard/tests/test_p1_settlement_arithmetic.py::test_a_clean_fee_overcharge_still_closes_with_zero_residual
7 failed, 1 passed in 0.72s
```

**Agent:** Seven of the eight fail on the original code, as they should. The eighth (late settlement still closes) is a regression guard that passes on both. The "clean fee overcharge" test fails on the original only because it reads a new evidence key, so its behavioural regression coverage comes from the 320-lifecycle comparison above.

Now I'll update the safety-guard table in `docs/architecture.md`, since it lists every guard and this adds one.

**Edit:**
```
<attempt>/work/repo/docs/architecture.md
```

**Result:**
```
The file <attempt>/work/repo/docs/architecture.md has been updated successfully.
```

**Edit:**
```
<attempt>/work/repo/docs/architecture.md
```

**Result:**
```
The file <attempt>/work/repo/docs/architecture.md has been updated successfully.
```

**Agent:** Next, the full suite including the new file, then a diff against the snapshot to confirm nothing under `outputs/` or `frozen/` changed.

**Bash:**
```
.venv/bin/python -m pytest ledgerguard/tests -q -p no:cacheprovider 2>&1 | tail -3; cd <attempt>/work && diff -rq tmp/orig_repo_snapshot repo -x .venv -x __pycache__ -x .pytest_cache -x test_p1_settlement_arithmetic.py; echo "---snapshot has pycache: $(find tmp/orig_repo_snapshot -name __pycache__ | wc -l)"; cat repo/.gitignore
```

**Result:**
```
-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
75 passed, 1 warning in 10.11s
Files tmp/orig_repo_snapshot/docs/architecture.md and repo/docs/architecture.md differ
Files tmp/orig_repo_snapshot/ledgerguard/evidence/safety.py and repo/ledgerguard/evidence/safety.py differ
Files tmp/orig_repo_snapshot/ledgerguard/reconciliation/matcher.py and repo/ledgerguard/reconciliation/matcher.py differ
---snapshot has pycache:        8
.venv/
__pycache__/
*.pyc
.env
.pytest_cache/
.DS_Store
Shell cwd was reset to <attempt>/work/repo
```

**Agent:** 75 tests pass (67 existing plus 8 new). The only changed files are the two source modules, the architecture doc, and the new test file. `outputs/` and `frozen/` are untouched. I'll review the final source diff once before writing the notes.

**Bash:**
```
cd <attempt>/work && diff -u tmp/orig_repo_snapshot/ledgerguard/reconciliation/matcher.py repo/ledgerguard/reconciliation/matcher.py; diff -u tmp/orig_repo_snapshot/ledgerguard/evidence/safety.py repo/ledgerguard/evidence/safety.py | head -80
```

**Result:**
```
--- tmp/orig_repo_snapshot/ledgerguard/reconciliation/matcher.py	2026-11-15 00:33:53
+++ repo/ledgerguard/reconciliation/matcher.py	2026-11-15 00:36:41
@@ -140,14 +140,17 @@
 #: Which invariants each classification actually accounts for. Anything else
 #: that failed is a secondary finding.
 _EXPLAINED_BY = {
+    # A fee schedule breach explains the net difference it causes. It does not
+    # explain a settlement whose reported net contradicts its own components:
+    # that is I1, and it is not a fee problem.
     ExceptionType.FEE_MISMATCH: {
-        "I1_settlement_arithmetic_consistent",
         "I2_fees_and_tax_match_schedule",
         "I3_net_matches_shadow_ledger",
     },
     ExceptionType.DUPLICATE_RECORD: {"I6_bank_credit_matches_settlement"},
     ExceptionType.DELAYED_SETTLEMENT: {"I5_settlement_within_window"},
     ExceptionType.UNEXPLAINED_SHORTFALL: {
+        "I1_settlement_arithmetic_consistent",
         "I3_net_matches_shadow_ledger",
         "I4_gross_matches_capture",
     },
@@ -167,12 +170,15 @@
     # even though it also shows up as a net difference.
     if "I2_fees_and_tax_match_schedule" in failing:
         return ExceptionType.FEE_MISMATCH, failing["I2_fees_and_tax_match_schedule"]
-    if "I1_settlement_arithmetic_consistent" in failing:
-        return ExceptionType.FEE_MISMATCH, failing["I1_settlement_arithmetic_consistent"]
     if "I4_gross_matches_capture" in failing:
         return ExceptionType.UNEXPLAINED_SHORTFALL, failing["I4_gross_matches_capture"]
     if "I3_net_matches_shadow_ledger" in failing:
         return ExceptionType.UNEXPLAINED_SHORTFALL, failing["I3_net_matches_shadow_ledger"]
+    # The settlement row contradicts its own components, with the fees and tax
+    # on schedule. Nothing proves a cause for the difference, so it is unexplained
+    # money, not a fee mismatch.
+    if "I1_settlement_arithmetic_consistent" in failing:
+        return ExceptionType.UNEXPLAINED_SHORTFALL, failing["I1_settlement_arithmetic_consistent"]
     if "I6_bank_credit_matches_settlement" in failing:
         inv = failing["I6_bank_credit_matches_settlement"]
         if "share reference" in inv.detail:
@@ -322,10 +328,19 @@
     explained = _EXPLAINED_BY.get(exc_type, set())
     secondary = [i.name for i in invariants if not i.holds and i.name not in explained]
 
+    # How far the settlement's reported net is from what its own components add
+    # up to. Zero when the row is internally consistent. The safety gate refuses
+    # to close any case where this is non-zero.
+    arithmetic = next(
+        i for i in invariants if i.name == "I1_settlement_arithmetic_consistent"
+    )
+    arithmetic_gap = 0 if arithmetic.holds else arithmetic.expected - arithmetic.observed
+
     evidence = {
         "reason": driver.detail if driver else "",
         "failed_invariants": [i.as_dict() for i in invariants if not i.holds],
         "secondary_findings": secondary,
+        "settlement_arithmetic_gap_paise": arithmetic_gap,
         "expected_shadow_net": expected.as_dict(),
         "observed_settlement": {
             "settlement_id": settlement.settlement_id,
@@ -352,19 +367,19 @@
     elif exc_type is ExceptionType.FEE_MISMATCH:
         expected_value = expected.fees + expected.tax
         observed_value = settlement.fees + settlement.tax
-        # A proven cause is not the same as a fully explained case. Correct the
-        # fee and tax back to schedule and ask whether the settlement now
-        # reconciles. Whatever is left over is money the fee variance does not
-        # account for, and it must not be closed on the strength of the part
-        # that was proved.
-        corrected_net = (
-            settlement.gross_amount
-            - expected.fees
-            - expected.tax
-            - settlement.refund_adjustments
-            + settlement.other_adjustments
+        # A proven cause is not the same as a fully explained case. Take the fee
+        # and tax v
... [2938 more characters in transcript.jsonl]
```

**Agent:** The diff is what I intended. I'll write the notes to `../out/NOTES.md`.

**Write:**
```
<attempt>/work/out/NOTES.md
```

**Result:**
```
File created successfully at: <attempt>/work/out/NOTES.md (file state is current in your context — no need to Read it back)
```

**Agent:** Before finishing, I'll confirm the manifest digest claim in the notes against the frozen file itself, not just the documented value.

**Bash:**
```
grep -o '"holdout_batch_sha256": "[0-9a-f]*"' ledgerguard/evaluation/frozen/holdout_20260905_320.json; .venv/bin/python -I -c "
import json; d=json.load(open('ledgerguard/evaluation/frozen/holdout_20260905_320.json')); print(d['holdout_batch_sha256'][:16])"
```

**Result:**
```
"holdout_batch_sha256": "3e28d4572d4cfc95a7ebd5ad1a04531475e0044e63eb1c732e38e303866f20fa"
3e28d4572d4cfc95
```

**Agent:** The digest matches the manifest. I'll drop one stray final bullet in the notes that doesn't describe anything I actually did.

**Edit:**
```
<attempt>/work/out/NOTES.md
```

**Result:**
```
The file <attempt>/work/out/NOTES.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

**Agent:** The short settlement is fixed. A settlement whose reported net is 250.00 below its own components now escalates to `HUMAN_REVIEW_REQUIRED` instead of closing as `AUTO_RESOLVED`. All 75 tests pass, including 8 new ones; 7 of the new ones fail on the original code.

**Cause:** two defects in `ledgerguard/reconciliation/matcher.py`.
- **The residual guard could not see the break.** It rebuilt the settlement's net from its components rather than reading the reported net. A row whose net contradicts its components therefore got residual 0, and the 250.00 vanished. This is what let the case close.
- **An arithmetic break was labelled a fee mismatch.** Fees and tax were on schedule, so the label claimed a fee problem the deterministic layer had just disproved.

**Fix:**
- The residual is now measured against the reported net, correcting only the fee variance. When the row adds up, this is algebraically identical to the old formula, so existing residuals (C2 = 650.00, C5 = 900.00) are unchanged.
- An arithmetic break with fees on schedule is classified `UNEXPLAINED_SHORTFALL`, not a fee mismatch.
- `safety.py` refuses to auto-close any settlement whose net does not match its own components, whatever the classification. This is stricter than the Evidence Gate on purpose: a same-customer orphan refund of exactly 250.00 does make the ledger balance and does verify, but it proves nothing about a row that contradicts itself. A test pins this.

**Unchanged behaviour:** I dumped every case's state, resolution, verdict, residual and reason before and after the change, for the holdout, all 320 lifecycles and the compound batch, under rules-only and the offline heuristic hybrid. The outputs are identical. The holdout digest still matches its manifest. No holdout case has an arithmetic break, so the new path is never reached there.

**Artifacts:** a recursive diff against an untouched snapshot shows changes only to the two source files, `docs/architecture.md` (guard table and an I1 note) and the new test file `ledgerguard/tests/test_p1_settlement_arithmetic.py`. Nothing under `outputs/` or `frozen/` changed.

**Not verified:**
- I did not re-run the live Groq benchmark. I have no key, and the benchmark rewrites `outputs/`. The argument that the committed hybrid figures are unchanged rests on the per-case comparison above.
- The holdout contains no arithmetic breaks, so the benchmark cannot show this fix working. Only the unit tests and the comparison cover it.

**Choices I made** (recorded in `../out/NOTES.md`):
- I used the existing `UNEXPLAINED_SHORTFALL` type rather than adding a new one.
- Arithmetically broken rows still trigger a model call, which is wasted. I left `should_investigate` alone to keep the change to the closure path.
