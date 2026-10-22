"""NAPOR weekly build: one command that runs every check, in order, and says PASS or FAIL.

Run from napor/:  python3 weekly_build.py
Exit code 0 = PASS (safe to publish), 1 = FAIL (do not publish; fix the first failing step).
Steps: build.py -> recalc (0 formula errors) -> backtest.py -> backtest_risk.py -> test_resolver.py
       -> export_explorer.py (+ its two self-checks) -> verify_explorer.py -> page-data validator.
"""
import datetime as dt
import json
import math
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
RECALC = "/mnt/skills/public/xlsx/scripts/recalc.py"
PY = sys.executable
results = []


def step(name, cmd, must_contain=(), must_not_contain=(), check=None):
    try:
        p = subprocess.run(cmd, cwd=HERE, capture_output=True, text=True, timeout=900)
        out = p.stdout + p.stderr
    except Exception as e:                       # noqa: BLE001
        results.append((name, False, f"could not run: {e}")); return ""
    ok = p.returncode == 0 and all(s in out for s in must_contain) and not any(s in out for s in must_not_contain)
    detail = ""
    if check:
        ok2, detail = check(out)
        ok = ok and ok2
    if not ok and not detail:
        detail = (out.strip().splitlines() or ["(no output)"])[-1][:200]
    results.append((name, ok, detail))
    return out


def recalc_check(out):
    try:
        j = json.loads(out[out.index("{"):out.rindex("}") + 1])
        return j.get("total_errors") == 0, f"total_errors {j.get('total_errors')}"
    except Exception:                            # noqa: BLE001
        return False, "could not read recalc output"


def walk(x, path="$"):
    """Yield (path, value) for every number in the JSON."""
    if isinstance(x, dict):
        for k, v in x.items():
            yield from walk(v, f"{path}.{k}")
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from walk(v, f"{path}[{i}]")
    elif isinstance(x, float):
        yield path, x


def validate():
    """Schema and sanity checks on the exported page data."""
    problems, warnings = [], []
    ex = os.path.join(REPO, "explorer")
    try:
        th = json.load(open(os.path.join(ex, "theaters.json")))
        files = [t["data"] for t in th["theaters"]]
    except Exception as e:                       # noqa: BLE001
        return [f"theaters.json unreadable: {e}"], warnings
    for rel in files:
        path = os.path.join(ex, rel)
        try:
            raw = open(path).read()
            d = json.loads(raw)
        except Exception as e:                   # noqa: BLE001
            problems.append(f"{rel}: unreadable ({e})"); continue
        if "NaN" in raw or "Infinity" in raw:
            problems.append(f"{rel}: contains NaN/Infinity")
        for k in ("theater", "asof", "generated", "phase", "intensity", "series", "hostile", "phases", "options", "history", "report_card", "sources", "estimate"):
            if k not in d:
                problems.append(f"{rel}: missing key '{k}'")
        if d.get("generated") != dt.date.today().isoformat():
            problems.append(f"{rel}: generated {d.get('generated')} is not today")
        keys = [o.get("key") for o in d.get("options", [])]
        if keys != sorted(keys):
            problems.append(f"{rel}: options not in fixed letter order ({keys})")
        for o in d.get("options", []):
            for f in ("trigger", "military", "us_move", "is_hold", "salvo", "cases", "name"):
                if f not in o:
                    problems.append(f"{rel}: option {o.get('key')} missing flag '{f}'")
            if o.get("military") not in ("reply", "strike", "none"):
                problems.append(f"{rel}: option {o.get('key')} has bad military flag {o.get('military')}")
            for c in o.get("cases", []):
                for f in ("id", "date", "strike7", "talks14", "ship_b", "ship_a", "replies", "strike_ev", "talk_ev", "ship_a_ev", "phase", "band_at"):
                    if f not in c:
                        problems.append(f"{rel}: option {o['key']} case {c.get('id')} missing '{f}'"); break
                if c.get("week") and c.get("hurt7") is None and c.get("strike7") is not None:
                    warnings.append(f"hold week {c['date']} has no hand-set people-hurt flag (add it to hold_weeks.PEOPLE_HURT)")
        for p, v in walk(d.get("report_card", {})):
            if math.isnan(v) or math.isinf(v):
                problems.append(f"{rel}: {p} is NaN/inf")
        for o in d.get("options", []):
            for c in o.get("cases", []):
                if c.get("cred") is not None and not (0 <= c["cred"] <= 1):
                    problems.append(f"{rel}: case {c['id']} credibility out of 0-1")
        bt = d.get("report_card", {}).get("backtest", {})
        for cat, row in (bt.get("brier") or {}).items():
            for m, v in row.items():
                if m != "n" and v is not None and not (0 <= v <= 1):
                    problems.append(f"{rel}: Brier {cat}/{m} = {v} out of 0-1")
        hist = d.get("history") or []
        if not hist or hist[-1].get("asof") != d.get("asof"):
            problems.append(f"{rel}: history not appended for asof {d.get('asof')}")
        for h in hist[-1:]:
            for k, v in (h.get("options") or {}).items():
                for f in ("index", "estimate"):
                    if v.get(f) is not None and not (0 <= v[f] <= 1):
                        problems.append(f"{rel}: history {k}.{f} = {v[f]} out of 0-1")
    for rel in ("data.json",):
        if not os.path.exists(os.path.join(ex, rel)):
            problems.append(f"explorer/{rel} (fallback) missing")
    return problems, warnings


if __name__ == "__main__":
    print(f"NAPOR weekly build, {dt.date.today().isoformat()}\n")
    step("build.py (workbook)", [PY, "build.py"], must_contain=("Saved.",))
    if os.path.exists(RECALC):
        step("recalc: 0 formula errors", [PY, RECALC, "NAPOR_iran_war.xlsx"], check=recalc_check)
    else:
        results.append(("recalc: 0 formula errors", False, f"{RECALC} not found"))
    step("backtest.py (reply prediction)", [PY, "backtest.py"], must_contain=("TEST 1", "TEST 2"))
    step("backtest_risk.py (risk numbers)", [PY, "backtest_risk.py"], must_contain=("No-hindsight check (fake future case appended): PASS",))
    step("test_resolver.py (matcher)", [PY, "test_resolver.py"], must_contain=("headlines.",))
    step("export_explorer.py + self-checks", [PY, "export_explorer.py"],
         must_contain=("page counts match workbook counts", "risk rates match the independent recount"), must_not_contain=("MISMATCH",))
    step("verify_explorer.py (independent recount)", [PY, "verify_explorer.py"])
    probs, warns = validate()
    results.append(("page-data validator", not probs, "; ".join(probs[:5]) + (f" (+{len(probs) - 5} more)" if len(probs) > 5 else "")))
    print("Checklist:")
    for name, ok, detail in results:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" - {detail}" if detail else ""))
    for w in warns:
        print(f"  [WARN] {w}")
    allok = all(ok for _, ok, _ in results)
    print("\nRESULT:", "PASS - publish explorer/index.html with the files listed in AGENT.md" if allok else "FAIL - do not publish; fix the first failing step")
    sys.exit(0 if allok else 1)
