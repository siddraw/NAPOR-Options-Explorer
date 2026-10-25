"""Houthis: build and write everything the page needs for the Houthis / Red Sea tab.

Writes (paths relative to the repo):
  explorer/data/houthis.json          - the page loads this
  explorer/data/houthis-history.json  - weekly snapshots (also embedded in houthis.json)
  explorer/theaters.json              - this theater's entry (id, name, status, data path, as-of date) is added or updated
Same shape as explorer/data/iran.json. Run by export_explorer.py (python3 export_explorer.py houthis).
"""
import datetime as dt
import json
import os

import export_explorer as X          # shared helpers: risk_index, pooled_rates, check, wilson (no Iran data is read here)
import backtest_risk as BR
import theaters as TH_REG
from theaters.houthis import backtest as BT, cases as K, config as C

EXPLORER = TH_REG.EXPLORER
DATA_FILE = os.path.join(EXPLORER, "data", C.THEATER_ID + ".json")
HISTORY_FILE = os.path.join(EXPLORER, "data", C.THEATER_ID + "-history.json")
HERE = os.path.dirname(os.path.abspath(__file__))


def sources_for(ids):
    """Outlet links and credibility for every event the page mentions (Houthi media marked as claims)."""
    out = {}
    for i in sorted(ids):
        if i not in K.EV:
            continue
        seen, links = set(), []
        for r in K.reports_for(i):
            if not r["url"] or r["outlet"] in seen:
                continue
            seen.add(r["outlet"])
            links.append(dict(o=r["outlet"], u=r["url"], claim=r["kind"].endswith("(claim only)")))
        out[str(i)] = dict(cred=K.CRED[i], links=links)
    return out


def context_periods():
    """Constraint periods from the research file, in the shape the page reads (notes per option letter)."""
    out = []
    for n, (a, b, text, ids) in enumerate(sorted(K.CONSTRAINTS, key=lambda c: c[0])):
        label = text.split(":")[0][:70]
        out.append(dict(key=f"c{n}", label=label, start=a.isoformat(), start_event=ids[0] if ids else None,
                        end=(b.isoformat() if b < K.LAST else None), end_event=None, notes={k: text for k in C.CONSTRAINT_OPTIONS}))
    return out


def build():
    cb = K.all_cases()
    rows = K.option_rows(cb)
    uses = K.uses()
    chain = K.chain_stats() or {}
    series, d = [], K.FIRST
    while d <= K.LAST:
        series.append([d.isoformat(), K.intensity_before(d + dt.timedelta(days=1))])
        d += dt.timedelta(days=1)
    cur = series[-1][1]
    peak = max(p for _, p in series)
    from napor_intensity import BANDS, band
    out = dict(
        theater=C.THEATER, asof=K.LAST.isoformat(), generated=dt.date.today().isoformat(), phase=K.phase_of(K.LAST),
        intensity=dict(pts=cur, band=band(cur), bands=[[lo, nm] for lo, nm in BANDS], peak=peak,
                       share_days_below=round(sum(1 for _, p in series if p < cur) / len(series), 3), window_days=14),
        series=series,
        hostile=[dict(id=e[0], date=e[1].isoformat(), actor=e[2], kind=K.KIND[e[0]], pts=K.points_for(e), deadly=bool(K.INT._deadly(e)), title=e[5]) for e in K.HOSTILE],
        phases=[dict(name=p[0], start=p[1].isoformat(), end=min(p[2], K.LAST).isoformat()) for p in K.PHASES if p[1] <= K.LAST],
        baseline=K.baseline_hold(), n_events=len([e for e in K.EVENTS if K.counts(e[0])]),
        chain=dict(n=chain.get("chains"), longer=round(1 - chain["share_stopped_after_one_reply"], 3) if chain else None),
        options=[])
    out["week_events"] = [K.ev(e[0]) | dict(actor=e[2]) for e in K.EVENTS if (K.LAST - e[1]).days <= 6 and K.counts(e[0])]
    now_file = os.path.join(HERE, C.NOW_FILE)
    out["now"] = json.load(open(now_file)) if os.path.exists(now_file) else None
    for o in C.OPTIONS:
        k = o["key"]; r = rows[k]; fl = C.FLAGS[k]; m = r["signals"]
        lines, evid = K.risk_lines(k, cb, rows)
        cases = cb[k]
        opt = dict(
            key=k, name=o["name"], what=o["what"], evidence=evid, **fl,
            official=dict(reply=r["reply"], fast=r["fast"], casualties=r["casualties"], strikes=m.get("strikes_after"), talks=m.get("talks"), shipping=m.get("shipping")),
            cases=cases, risks=lines, pros=C.PROS[k], harms=C.HARMS[k], unknown=C.UNKNOWNS[k], forecasts=[], uses=uses[k])
        if C.MIN_CASES:
            opt["too_few"] = len(cases) < C.MIN_CASES        # the page shows "too few cases" instead of a risk index
        opt["last_used"] = max([c["date"] for c in cases if not c.get("week")] + [u["date"] for u in uses[k]], default=None)
        out["options"].append(opt)
    out["context"] = context_periods()
    bt, _ = BT.run(cb)
    json.dump(bt, open(BT.JSON_FILE, "w"), indent=1, default=str)
    out["report_card"] = dict(forecasts=[], backtest=bt, political_proposal=bt["political_proposal"])
    dw = bt["weighting"]["decision"]
    out["estimate"] = dict(shrink=bt["decision"]["adopt"], m=BR.M_MAIN,
                           weighting=dict(scheme=dw["scheme"], param=dw["param"], name=dw["name"], adopt=dw["adopt"], best_candidate=dw["best_candidate"],
                                          gain=dw["gain"], worse_by_cat=dw["worse_by_cat"], rule=dw["rule"]))
    ids = set()
    for o in out["options"]:
        for c in o["cases"]:
            if not c.get("week"):
                ids.add(c["id"])
            for key in ("replies", "strike_ev", "talk_ev", "ship_a_ev", "ship_b_ev", "hurt_ev"):
                ids.update(x["id"] for x in c.get(key) or [])
        ids.update(u["id"] for u in o["uses"])
    ids.update(e["id"] for e in out["week_events"])
    out["sources"] = sources_for(ids)
    out["history"] = update_history(out)
    return out


def update_history(out):
    hist = json.load(open(HISTORY_FILE)) if os.path.exists(HISTORY_FILE) else []
    W, T = X.weighting_of(out), dt.date.fromisoformat(out["asof"])
    pool = X.pooled_rates(out["options"], W, T)
    snap = dict(asof=out["asof"], intensity=out["intensity"]["pts"], band=out["intensity"]["band"], events=out["n_events"],
                options={o["key"]: dict(n=len(o["cases"]), index=X.risk_index(o, o["cases"]),
                                        estimate=X.risk_index(o, o["cases"], pool=pool, weighting=W, T=T) if out["estimate"]["shrink"] else None) for o in out["options"]},
                status={k: dict(status=v["status"], label=v["label"]) for k, v in ((out.get("now") or {}).get("options") or {}).items()},
                status_as_of=(out.get("now") or {}).get("as_of"))
    hist = [h for h in hist if h["asof"] != snap["asof"]] + [snap]
    hist.sort(key=lambda h: h["asof"])
    return hist[-60:]


def write(out):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        f.write(json.dumps(out, separators=(",", ":"), default=str))
    with open(HISTORY_FILE, "w") as f:
        json.dump(out["history"], f, indent=1)
    TH_REG.register(dict(id=C.THEATER_ID, name=C.THEATER["name"], status=C.THEATER["status"], data="data/" + C.THEATER_ID + ".json", asof=out["asof"]), out["generated"])


def recount_diff(out):
    """Compare [k, n, sum_wy, sum_w] per option and category with the independent recount (tolerance 1e-9)."""
    from theaters.houthis import verify
    W, T = X.weighting_of(out), dt.date.fromisoformat(out["asof"])
    ver, diff = verify.recount(weighting=W, asof=T), []
    for o in out["options"]:
        if not o["cases"]:
            continue
        sc = X.category_scores(o, o["cases"], W, T)
        for c in X.CATS:
            if sc[c].get("assumed"):
                continue
            mine = [sc[c]["k"], sc[c]["n"], sc[c]["swy"], sc[c]["sw"]]
            theirs = ver[o["key"]][c]
            if any(abs(a - b) > 1e-9 for a, b in zip(mine, theirs)):
                diff.append((o["key"], c, mine, theirs))
    return diff


def run():
    """Build, write and self-check the Houthi theater. Returns the list of problems (empty = PASS)."""
    out = build()
    bad = [b for b in X.check(out) if b[2] != (0, 0)]       # an option with no counted cases says "No past cases", which has no x of n to compare
    write(out)
    print("wrote", os.path.normpath(DATA_FILE), "(+ history, theaters.json) | asof", out["asof"], "| intensity", out["intensity"]["pts"], out["intensity"]["band"])
    print("MISMATCH vs workbook counts:" if bad else "page counts match the log's own counts", bad or "")
    diff = recount_diff(out)
    print("MISMATCH vs independent recount:" if diff else "risk rates match the independent recount", diff or "")
    print("cases per option:", {o["key"]: len(o["cases"]) for o in out["options"]}, "| too few cases:", [o["key"] for o in out["options"] if o.get("too_few")])
    return bad + diff
