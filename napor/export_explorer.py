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
        hostile=[dict(id=e[0], date=e[1].isoformat(), actor=e[2], kind=data.event_kind[e[0]], pts=INT.points_for(e), deadly=bool(INT._deadly(e)), title=e[5]) for e in INT.HOSTILE],
        phases=[dict(name=p[0], start=p[1].isoformat(), end=min(p[2], last).isoformat()) for p in T.PHASES if p[1] <= last],
        baseline=O.baseline_hold(), n_events=len([e for e in data.events if e[0] not in data.MERGED]),
        chain=dict(n=chain.get("chains"), longer=round(1 - chain["share_stopped_after_one_reply"], 3) if chain else None),
        patriots=O.PATRIOTS_PER_SALVO, options=[])
    out["week_events"] = [ev(e[0]) | dict(actor=e[2]) for e in sorted(data.events, key=lambda e: e[1])
                          if e[0] not in data.MERGED and (last - e[1]).days <= 6 and N.counts(e[0])]
    now_file = os.path.join(HERE, "napor_now.json")
    out["now"] = json.load(open(now_file)) if os.path.exists(now_file) else None
    open_fc = [f for f in F.load() if f["outcome"] is None]
    for o in O.OPTIONS:
        k = o["key"]; r = rows[k]; m = O.measured_signals(k); rp = O.risk_profile(k)
        cases = []
        if o["match"]:
            for c in [c for c in O.census if O.us_side(c[0]) and o["match"](c[0])]:
                prs = [p for p in O.pairs if p[1] == c[0]]
                counted = c[2] in ("R-strong", "R-weak", "R-proxy", "N")
                cases.append(dict(**ev(c[0]), cls=c[2], replied=(c[2] != "N") if counted else None,
                                  replies=[dict(id=p[2], days=(EV[p[2]][1] - EV[p[1]][1]).days, hurt=p[4] == "Y", kinetic=data.event_kind[p[2]] == "Kinetic", title=EV[p[2]][5], actor=EV[p[2]][2], date=EV[p[2]][1].isoformat(), dmg=EV[p[2]][7] or "") for p in prs], note=c[3],
                                  civ=O.CIVILIAN_HARM.get(c[0])))
        elif k in ("B", "H"):
            for i in O.option_cases(k):
                cases.append(dict(**ev(i), cls=None, replied=None, replies=[], civ=None, note=None))
        for c in cases:
            day = EV[c["id"]][1]
            full7 = (last - day).days >= 7
            c["strike7"] = bool(O._window(O._irstrike, day, 1, 7)) if full7 else None
            # Talks: yes as soon as one is logged; "no" only once the full 14 days have passed (otherwise still open).
            # (The workbook counts a partly-open window as "no", which undercounts recent cases.)
            talks = bool(O._window(O._talks, day, 1, 14))
            c["talks14"] = True if talks else (False if (last - day).days >= 14 else None)
            brief = lambda ids: [dict(id=j, date=EV[j][1].isoformat(), title=EV[j][5], actor=EV[j][2], dmg=EV[j][7] or "") for j in ids]
            c["dmg"] = EV[c["id"]][7] or ""
            c["strike_ev"] = brief(O._window(O._irstrike, day, 1, 7))
            c["talk_ev"] = brief(O._window(O._talks, day, 1, 14))
            c["ship_b_ev"] = brief(O._window(O._ship, day, -7, -1))
            c["ship_a_ev"] = brief(O._window(O._ship, day, 1, 7))
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
            forecasts=[dict(id=f["id"], question=f["question"], p=f["probability"], deadline=f["deadline"], made_on=f["made_on"]) for f in open_fc if f["option"] == k]))
    # Every logged US move of each kind (not only the census cases), for "what did the US do next" on past dates.
    _CONC = ("proposal", "talks", "ceasefire announcement", "ceasefire (", "ceasefire statement")
    census_ids = {c[0] for c in O.census}
    def kind_of(e):
        t = e[0]; k = data.event_kind[t]
        if k == "Sanctions": return ["C"]
        if k == "Maritime": return ["D"]
        if k == "Posture": return ["H"]
        if k == "Diplomatic": return ["B"] if any(w in e[3].lower() for w in _CONC) else []
        if k == "Kinetic":
            if O.is_shipping_strike(t): return ["E"]
            if t in census_ids:
                cat = [c[1] for c in O.census if c[0] == t][0]
                return ["G"] if cat == "Personnel/Casualty" else ["F"]
            return ["F", "G"]
        return []
    for o in out["options"]:
        o["uses"] = []
    byk = {o["key"]: o for o in out["options"]}
    for e in sorted(data.events, key=lambda e: e[1]):
        if not O.us_side(e[0]) or not O._usable(e):
            continue
        ks = kind_of(e)
        for k in ks:
            byk[k]["uses"].append(dict(id=e[0], date=e[1].isoformat(), title=e[5], unsorted=len(ks) > 1))
    for o in out["options"]:
        o["last_used"] = max([c["date"] for c in o["cases"]] + [u["date"] for u in o["uses"]], default=None)
    out["history"] = update_history(out)
    return out


# ---- NAPOR risk index (equal weights): same formula as the page, used here only for the weekly history ----
CATS = ["people", "escalation", "military", "economic", "political"]


def wilson(k, n, z=1.96):
    if not n: return None
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); m = z * (p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5
    return max(0, (c - m) / d), min(1, (c + m) / d)


def category_scores(o, cases):
    def rate(base, flag):
        b = [c for c in cases if base(c)]
        return dict(k=sum(1 for c in b if flag(c)), n=len(b))
    sc = {}
    sc["people"] = rate(lambda c: c["strike7"] is not None, lambda c: bool(c["civ"]) or any(r["hurt"] for r in c["replies"]))
    sc["escalation"] = (rate(lambda c: c["replied"] is not None, lambda c: c["replied"] is True) if o["trigger"]
                        else rate(lambda c: c["strike7"] is not None, lambda c: c["strike7"] is True))
    if o["key"] in ("D", "E", "F", "G"):
        sc["military"] = rate(lambda c: c["replied"] is not None, lambda c: any(r["kinetic"] for r in c["replies"]))
    else:
        sc["military"] = dict(k=0, n=0, assumed=True)
    sc["economic"] = rate(lambda c: c["ship_a"] is not None, lambda c: c["ship_a"] > c["ship_b"])
    sc["political"] = rate(lambda c: c["talks14"] is not None, lambda c: c["talks14"] is False)
    return sc


def risk_index(o, cases, w=None):
    if not cases: return None
    sc = category_scores(o, cases); w = w or {c: 1 for c in CATS}
    num = tot = 0
    for c in CATS:
        s = sc[c]
        if s["n"] or s.get("assumed"):
            p = s["k"] / s["n"] if s["n"] else 0
            num += w[c] * p; tot += w[c]
    return round(num / tot, 3) if tot else None


def update_history(out):
    path = os.path.join(HERE, "..", "explorer", "history.json")
    hist = json.load(open(path)) if os.path.exists(path) else []
    snap = dict(asof=out["asof"], intensity=out["intensity"]["pts"], band=out["intensity"]["band"], events=out["n_events"],
                options={o["key"]: dict(n=len(o["cases"]), index=risk_index(o, o["cases"])) for o in out["options"]},
                status={k: dict(status=v["status"], label=v["label"]) for k, v in ((out.get("now") or {}).get("options") or {}).items()},
                status_as_of=(out.get("now") or {}).get("as_of"))
    hist = [h for h in hist if h["asof"] != snap["asof"]] + [snap]
    hist.sort(key=lambda h: h["asof"])
    return hist[-60:]


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
    with open(os.path.join(os.path.dirname(dest), "history.json"), "w") as f:
        json.dump(out["history"], f, indent=1)
    print("wrote", os.path.normpath(dest), "| asof", out["asof"], "| intensity", out["intensity"]["pts"], out["intensity"]["band"])
    print("MISMATCH vs workbook counts:" if bad else "page counts match workbook counts", bad or "")
    # Independent recount of the five risk-category rates (verify_explorer.py) vs the page's formula.
    import verify_explorer
    ver, diff = verify_explorer.recount(), []
    for o in out["options"]:
        if not o["cases"]:
            continue
        sc = category_scores(o, o["cases"])
        for c in CATS:
            if not sc[c].get("assumed") and [sc[c]["k"], sc[c]["n"]] != ver[o["key"]][c]:
                diff.append((o["key"], c, [sc[c]["k"], sc[c]["n"]], ver[o["key"]][c]))
    print("MISMATCH vs independent recount:" if diff else "risk rates match the independent recount", diff or "")
