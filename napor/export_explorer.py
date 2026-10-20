"""NAPOR: export everything the Options Explorer page needs to explorer/data.json.

Run weekly by the maintenance agent after build.py (see AGENT.md). Safe to run any time.
The page (explorer/index.html) never hard-codes numbers; it reads data.json.
"""
import json, os, sys, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import data, napor_options as O, napor_ids as N, napor_threads as T, napor_intensity as INT, napor_forecasts as F

EV = O.EV
last = max(e[1] for e in data.events)
first = min(e[1] for e in data.events)
TRIG = ("C", "D", "E", "F", "G")


def ev(i):
    e = EV[i]
    return dict(id=i, date=e[1].isoformat(), actor=e[2], kind=e[3], title=e[5], cred=round(N.event_credibility(i), 2))


def build():
    rows = {r["key"]: r for r in O.option_rows()}
    chain = T.chain_stats() or {}
    series = []
    d = first
    while d <= last:
        series.append([d.isoformat(), INT.intensity_before(d + dt.timedelta(days=1))])
        d += dt.timedelta(days=1)
    cur = series[-1][1]
    peak = max(p for _, p in series)
    out = dict(
        asof=last.isoformat(), generated=dt.date.today().isoformat(), phase=O.CURRENT_PHASE,
        intensity=dict(pts=cur, band=INT.band(cur), bands=[[lo, nm] for lo, nm in INT.BANDS], peak=peak,
                       share_days_below=round(sum(1 for _, p in series if p < cur) / len(series), 3), window_days=INT.WINDOW_DAYS),
        series=series,
        hostile=[dict(id=e[0], date=e[1].isoformat(), actor=e[2], kind=data.event_kind[e[0]], pts=INT.points_for(e), title=e[5]) for e in INT.HOSTILE],
        phases=[dict(name=p[0], start=p[1].isoformat(), end=min(p[2], last).isoformat()) for p in T.PHASES if p[1] <= last],
        baseline=O.baseline_hold(), n_events=len([e for e in data.events if e[0] not in data.MERGED]),
        chain=dict(n=chain.get("chains"), longer=round(1 - chain["share_stopped_after_one_reply"], 3) if chain else None),
        patriots=O.PATRIOTS_PER_SALVO, options=[])
    open_fc = [f for f in F.load() if f["outcome"] is None]
    for o in O.OPTIONS:
        k = o["key"]; r = rows[k]; m = O.measured_signals(k); rp = O.risk_profile(k)
        cases = []
        if o["match"]:
            for c in [c for c in O.census if O.us_side(c[0]) and o["match"](c[0])]:
                prs = [p for p in O.pairs if p[1] == c[0]]
                counted = c[2] in ("R-strong", "R-weak", "N")
                cases.append(dict(**ev(c[0]), cls=c[2], replied=(c[2] != "N") if counted else None,
                                  replies=[dict(id=p[2], days=(EV[p[2]][1] - EV[p[1]][1]).days, hurt=p[4] == "Y", title=EV[p[2]][5]) for p in prs],
                                  civ=O.CIVILIAN_HARM.get(c[0])))
        elif k in ("B", "H"):
            for i in O.option_cases(k):
                cases.append(dict(**ev(i), cls=None, replied=None, replies=[], civ=None))
        for c in cases:
            day = EV[c["id"]][1]
            full7 = (last - day).days >= 7
            c["strike7"] = bool(O._window(O._irstrike, day, 1, 7)) if full7 else None
            # Talks: yes as soon as one is logged; "no" only once the full 14 days have passed (otherwise still open).
            # (The workbook counts a partly-open window as "no", which undercounts recent cases.)
            talks = bool(O._window(O._talks, day, 1, 14))
            c["talks14"] = True if talks else (False if (last - day).days >= 14 else None)
            c["ship_b"] = len(O._window(O._ship, day, -7, -1))
            c["ship_a"] = len(O._window(O._ship, day, 1, 7)) if full7 else None
            c["civ"] = c["civ"] if c["id"] in O.CIVILIAN_HARM else None
            c["phase"] = T.event_phase[c["id"]]
            c["pts_at"] = INT.intensity_before(day)
            c["band_at"] = INT.band(c["pts_at"])
        cases.sort(key=lambda x: x["date"])
        out["options"].append(dict(
            key=k, name=o["name"], what=o["what"], evidence=rp["Evidence strength"], trigger=k in TRIG,
            official=dict(reply=r["reply"], fast=r["fast"], casualties=r["casualties"], strikes=m.get("strikes_after"), talks=m.get("talks"), shipping=m.get("shipping")),
            cases=cases, risks=[rp[c] for c in O.RISK_CATEGORIES], pros=O.PROS[k], harms=O.HARMS[k], unknown=O.UNKNOWNS[k],
            forecasts=[dict(id=f["id"], question=f["question"], p=f["probability"], deadline=f["deadline"]) for f in open_fc if f["option"] == k]))
    return out


def check(out):
    """The page recomputes every number from the cases; make sure it agrees with the workbook's own counts."""
    bad = []
    for o in out["options"]:
        cs, off = o["cases"], o["official"]
        def kn(s):
            import re
            m = re.search(r"(\d+) of (\d+)", s or ""); return (int(m[1]), int(m[2])) if m else None
        if o["trigger"]:
            got = (sum(1 for c in cs if c["replied"] is True), sum(1 for c in cs if c["replied"] is not None))
            if got != kn(off["reply"]): bad.append((o["key"], "reply", got, off["reply"]))
        if off["strikes"]:
            got = (sum(1 for c in cs if c["strike7"] is True), sum(1 for c in cs if c["strike7"] is not None))
            if got != kn(off["strikes"]): bad.append((o["key"], "strikes", got, off["strikes"]))
        # talks14 is deliberately NOT compared: the page leaves a still-open 14-day window out instead of counting it as "no".
    return bad


if __name__ == "__main__":
    out = build()
    bad = check(out)
    dest = os.path.join(HERE, "..", "explorer", "data.json")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w") as f:
        json.dump(out, f, separators=(",", ":"), default=str)
    print("wrote", os.path.normpath(dest), "| asof", out["asof"], "| intensity", out["intensity"]["pts"], out["intensity"]["band"])
    print("MISMATCH vs workbook counts:" if bad else "page counts match workbook counts", bad or "")
