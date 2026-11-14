"""Browser bridge for the LedgerGuard demo (runs inside Pyodide).

Reuses the original dashboard backend unchanged: fastapi is stubbed (there is no
server here), and the holdout split is wrapped so a visitor's edits are applied to
the frozen test batch before the original controller runs."""
import json, os, sys, types

os.environ["LEDGERGUARD_PROVIDER"] = "stub"  # offline stand-in investigator: no keys, no network


def _stub_fastapi():
    class FastAPI:
        def __init__(self, *a, **k): pass
        def add_middleware(self, *a, **k): pass
        def get(self, *a, **k): return lambda f: f
    for name in ("fastapi", "fastapi.middleware", "fastapi.middleware.cors", "fastapi.responses"):
        sys.modules[name] = types.ModuleType(name)
    sys.modules["fastapi"].FastAPI = FastAPI
    sys.modules["fastapi"].HTTPException = Exception
    sys.modules["fastapi.middleware.cors"].CORSMiddleware = object
    for n in ("FileResponse", "HTMLResponse", "Response"):
        setattr(sys.modules["fastapi.responses"], n, object)


_stub_fastapi()
from ledgerguard.backend import app as appmod  # noqa: E402
from ledgerguard.ledger.models import SettlementStatus  # noqa: E402

EDITS: list[dict] = []
_split = appmod.split


def _apply(holdout, e):
    lc = next((l for l in holdout.lifecycles if l.lifecycle_id == e["lc"]), None)
    if lc is None:
        raise ValueError(f"{e['lc']} is not in the test batch")
    p = int(round(float(e.get("rupees", 0)) * 100))
    s, banks = lc.settlement, lc.bank_entries
    if e["op"] == "drop_settlement":
        lc.settlement = None
    elif e["op"] == "drop_bank":
        lc.bank_entries = []
    elif e["op"] == "extra_fee":
        if s is None:
            raise ValueError(f"{e['lc']} has no settlement to change")
        s.fees += p
        s.net_amount -= p
        for b in banks:
            b.amount -= p
    elif e["op"] == "fail_settlement":
        if s is None:
            raise ValueError(f"{e['lc']} has no settlement to fail")
        s.status = SettlementStatus.FAILED
    else:
        raise ValueError(f"unknown edit {e['op']}")


def _split_with_edits(full):
    dev, holdout = _split(full)
    for e in EDITS:
        _apply(holdout, e)
    return dev, holdout


appmod.split = _split_with_edits


def state(edits_json: str = "[]") -> str:
    EDITS[:] = json.loads(edits_json)
    appmod._cached_state.cache_clear()
    return json.dumps(appmod._state(), default=str)


def case_ids() -> str:
    _, h = _split(appmod.build_dataset())
    return json.dumps([l.lifecycle_id for l in h.lifecycles])


if __name__ == "__main__":  # self-check: clean run, then each edit is caught on a clean case
    clean = json.loads(state())
    lc = next(c["lifecycle_id"] for c in clean["cases"] if c["state"] == "MATCHED")
    before = {c["lifecycle_id"]: c["state"] for c in clean["cases"]}
    for op in ("drop_settlement", "drop_bank", "extra_fee"):
        s = json.loads(state(json.dumps([{"op": op, "lc": lc, "rupees": 250}])))
        after = [c for c in s["cases"] if c["lifecycle_id"] == lc]
        print(op, lc, before[lc], "->", [(c["state"], c["exception_type"]) for c in after])
        assert all(c["state"] != "MATCHED" for c in after) or not after, op
    print("ok", len(clean["cases"]), clean["provider"])
    # Honesty check: a FAILED settlement on a MATCHED case. Run once per package; LG_EXPECT=fixed for the agent's fix.
    s = json.loads(state(json.dumps([{"op": "fail_settlement", "lc": lc}])))
    got = [c["state"] for c in s["cases"] if c["lifecycle_id"] == lc]
    closed = bool(got) and all(x in ("MATCHED", "AUTO_RESOLVED") for x in got)
    print("fail_settlement", os.environ.get("LG_EXPECT", "original"), lc, got, "closed" if closed else "refused")
    assert closed != (os.environ.get("LG_EXPECT") == "fixed"), "unexpected result for this package"
