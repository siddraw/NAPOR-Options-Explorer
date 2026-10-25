"""NAPOR: export everything the Options Explorer page needs.

Writes (paths relative to the repo):
  explorer/theaters.json          - the list of theaters (one tab each; only Iran today)
  explorer/data/iran.json         - the Iran theater's data (the page loads this)
  explorer/data/iran-history.json - weekly snapshots (also embedded in iran.json)
  explorer/data.json              - same as data/iran.json, kept as a fallback during the move to theaters
Run weekly by the maintenance agent (see AGENT.md; weekly_build.py runs it). Safe to run any time.
The page (explorer/index.html) never hard-codes numbers or option letters; it reads these files.
"""
import json, os, re, sys, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import data, napor_options as O, napor_ids as N, napor_threads as T, napor_intensity as INT, napor_forecasts as F
import napor_cases as NC, backtest_risk as BR

EV = O.EV
last = max(e[1] for e in data.events)
first = min(e[1] for e in data.events)
EXPLORER = os.path.join(HERE, "..", "explorer")
THEATER_ID = "iran"
DATA_FILE = os.path.join(EXPLORER, "data", THEATER_ID + ".json")
HISTORY_FILE = os.path.join(EXPLORER, "data", THEATER_ID + "-history.json")

# Words the page uses for this theater, so a future theater renders with its own wording.
THEATER = dict(
    id=THEATER_ID, name="Iran", status="active", title="Iran war",
    sub="The options the US has right now in the Iran war, and what followed the last times the US did something like each one.",
    adversary="Iran", actor="Iran or an Iran-backed group", actor_short="Iran or proxy",
    proxy_note="Proxy = a militia Iran arms in Iraq or Syria. Before 2026, Iran mostly answered the US through these groups; those replies count and are labelled \"proxy\".",
    salvo=dict(count=O.PATRIOTS_PER_SALVO, weapon="Patriots", when="Sep 8-9"),
    hold_note="Hold cases are weeks of the 2026 war with no logged US sanctions, naval, strike or posture move (Feb 28-Apr 7 and Jul 7-25 left out: US activity there was continuous but logged as a few rows; pre-war weeks left out: too sparsely logged). Most hold weeks have few or no logged events, so they show what the log records in quiet weeks.",
    not_measured="Oil prices, strain with allies and harm to ordinary Iranians are not measured.",
    presets=[["2020-01-03", "Soleimani strike"], ["2025-06-22", "US strikes nuclear sites"], ["2026-02-28", "2026 war starts"],
             ["2026-04-08", "First ceasefire"], ["2026-06-17", "Interim deal"], ["2026-07-08", "July campaign"], ["2026-09-10", "Holding pattern"]],
    under_logged="Some stretches are logged as one row (for example the nightly US strikes of Jul 9-25, 2026), so \"none logged\" is not proof nothing happened.",
)


def ev(i):
    return NC.ev(i)


def sources_for(ids):
    """Outlet links and credibility for every event the page mentions (Iranian state media marked as claims)."""
    out = {}
    for i in sorted(ids):
        if i not in EV or i in data.MERGED:
            continue
        seen, links = set(), []
        for r in N.reports_for(i):
            if not r["url"] or r["outlet"] in seen:
                continue
            seen.add(r["outlet"])
            links.append(dict(o=r["outlet"], u=r["url"], claim=r["kind"].startswith("Iranian state media")))
        out[str(i)] = dict(cred=N.event_credibility(i), links=links)
    return out


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
        theater=THEATER,
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
    fcs = F.load()
    open_fc = [f for f in fcs if f["outcome"] is None]
    cases_by_key = {}
    for o in O.OPTIONS:
        k = o["key"]; r = rows[k]; m = O.measured_signals(k); rp = O.risk_profile(k)
        cases = NC.option_cases(k, last)
        cases_by_key[k] = cases
        fl = NC.FLAGS[k]
        out["options"].append(dict(
            key=k, name=o["name"], what=o["what"], evidence=rp["Evidence strength"] if not fl["is_hold"] else f"{len(cases)} hold weeks",
            **fl,
            official=dict(reply=r["reply"], fast=r["fast"], casualties=r["casualties"], strikes=m.get("strikes_after"), talks=m.get("talks"), shipping=m.get("shipping")),
            cases=cases, risks=[rp[c] for c in O.RISK_CATEGORIES], pros=O.PROS[k], harms=O.HARMS[k], unknown=O.UNKNOWNS[k],
            forecasts=[dict(id=f["id"], question=f["question"], p=f["probability"], deadline=f["deadline"], made_on=f["made_on"]) for f in open_fc if f["option"] == k]))
    # Every logged US move of each kind (not only the census cases), for "what did the US do next" on past dates.
    _CONC = BR.CONC
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
        if not e[2].lower().startswith("us") or not O._usable(e):   # the US itself (not Israel alone)
            continue
        ks = kind_of(e)
        for k in ks:
            byk[k]["uses"].append(dict(id=e[0], date=e[1].isoformat(), title=e[5], unsorted=len(ks) > 1))
    for o in out["options"]:
        o["last_used"] = max([c["date"] for c in o["cases"] if not c.get("week")] + [u["date"] for u in o["uses"]], default=None)
    import napor_context
    out["context"] = napor_context.export()
    # Report card: locked forecasts (open and resolved) and the backtest of the page's own method.
    out["report_card"] = dict(
        forecasts=[dict(id=f["id"], question=f["question"], p=f["probability"], made_on=f["made_on"], deadline=f["deadline"], option=f["option"],
                        outcome=f["outcome"], brier=f["brier"], note=f["resolution_note"], basis=f["basis"]) for f in fcs],
        backtest=BR.run(cases_by_key))
    bt = out["report_card"]["backtest"]
    dw = bt["weighting"]["decision"]
    # estimate.weighting: the recency weight the page applies to every case (scheme "none" = every case counts 1)
    out["estimate"] = dict(shrink=bt["decision"]["adopt"], m=BR.M_MAIN,
                           weighting=dict(scheme=dw["scheme"], param=dw["param"], name=dw["name"], adopt=dw["adopt"], best_candidate=dw["best_candidate"],
                                          gain=dw["gain"], worse_by_cat=dw["worse_by_cat"], rule=dw["rule"]))
    out["report_card"]["political_proposal"] = bt["political_proposal"]
    ids = set()
    for o in out["options"]:
        for c in o["cases"]:
            if not c.get("week"): ids.add(c["id"])
            for key in ("replies", "strike_ev", "talk_ev", "ship_a_ev", "ship_b_ev", "hurt_ev"):
                ids.update(x["id"] for x in c.get(key) or [])
        ids.update(u["id"] for u in o["uses"])
    ids.update(e["id"] for e in out["week_events"])
    out["sources"] = sources_for(ids)
    out["history"] = update_history(out)
    return out


# ---- NAPOR risk index (equal weights): same formula as the page, used here for the weekly history ----
CATS = NC.CATS


def wilson(k, n, z=1.96):
    if not n: return None
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); m = z * (p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5
    return max(0, (c - m) / d), min(1, (c + m) / d)


def weighting_of(out):
    wt = out["estimate"]["weighting"]
    return (wt["scheme"], wt["param"])


def category_scores(o, cases, weighting=("none", None), T=None):
    return NC.category_scores({k: o[k] for k in ("trigger", "military", "is_hold")}, cases, weighting, T)


def risk_index(o, cases, w=None, pool=None, weighting=("none", None), T=None):
    """Average of the measured corners. With pool (category -> pooled rate), corners are shrunk toward it:
    (sum of weighted risks + m p)/(sum of weights + m); with no recency weighting that is (k + m p)/(n + m)."""
    if not cases: return None
    sc = category_scores(o, cases, weighting, T); w = w or {c: 1 for c in CATS}
    num = tot = 0
    for c in CATS:
        s = sc[c]
        if s["n"] or s.get("assumed"):
            if s.get("assumed"):
                p = 0
            elif pool is not None and pool.get(c) is not None:
                p = (s["swy"] + BR.M_MAIN * pool[c]) / (s["sw"] + BR.M_MAIN)
            else:
                p = s["k"] / s["n"]
            num += w[c] * p; tot += w[c]
    return round(num / tot, 3) if tot else None


def pooled_rates(options, weighting=("none", None), T=None):
    """Weighted all-options rate per category: sum(w*y) / sum(w) over every option's counted cases (same weights)."""
    tot = {c: [0, 0] for c in CATS}
    for o in options:
        sc = category_scores(o, o["cases"], weighting, T)
        for c in CATS:
            if not sc[c].get("assumed"):
                tot[c][0] += sc[c]["swy"]; tot[c][1] += sc[c]["sw"]
    return {c: (k / n if n else None) for c, (k, n) in tot.items()}


def update_history(out):
    path = HISTORY_FILE if os.path.exists(HISTORY_FILE) else os.path.join(EXPLORER, "history.json")
    hist = json.load(open(path)) if os.path.exists(path) else []
    W, T = weighting_of(out), dt.date.fromisoformat(out["asof"])
    pool = pooled_rates(out["options"], W, T)
    snap = dict(asof=out["asof"], intensity=out["intensity"]["pts"], band=out["intensity"]["band"], events=out["n_events"],
                options={o["key"]: dict(n=len(o["cases"]), index=risk_index(o, o["cases"]),
                                        estimate=risk_index(o, o["cases"], pool=pool, weighting=W, T=T) if out["estimate"]["shrink"] else None) for o in out["options"]},
                status={k: dict(status=v["status"], label=v["label"]) for k, v in ((out.get("now") or {}).get("options") or {}).items()},
                status_as_of=(out.get("now") or {}).get("as_of"))
    hist = [h for h in hist if h["asof"] != snap["asof"]] + [snap]
    hist.sort(key=lambda h: h["asof"])
    return hist[-60:]


def check(out):
    """The page recomputes every number from the cases; make sure it agrees with the workbook's own counts."""
    bad = []
    def kn(s):
        m = re.search(r"(\d+) of (\d+)", s or ""); return (int(m[1]), int(m[2])) if m else None
    for o in out["options"]:
        cs, off = o["cases"], o["official"]
        if o["is_hold"]:
            continue                      # hold weeks are not in the workbook
        if o["trigger"]:
            got = (sum(1 for c in cs if c["replied"] is True), sum(1 for c in cs if c["replied"] is not None))
            if got != kn(off["reply"]): bad.append((o["key"], "reply", got, off["reply"]))
        if off["strikes"]:
            got = (sum(1 for c in cs if c["strike7"] is True), sum(1 for c in cs if c["strike7"] is not None))
            if got != kn(off["strikes"]): bad.append((o["key"], "strikes", got, off["strikes"]))
        # talks14 is deliberately NOT compared: the page leaves a still-open 14-day window out instead of counting it as "no".
    return bad


def write(out):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    blob = json.dumps(out, separators=(",", ":"), default=str)
    for dest in (DATA_FILE, os.path.join(EXPLORER, "data.json")):
        with open(dest, "w") as f:
            f.write(blob)
    with open(HISTORY_FILE, "w") as f:
        json.dump(out["history"], f, indent=1)
    theaters = dict(generated=out["generated"], default=THEATER_ID,
                    theaters=[dict(id=THEATER_ID, name=THEATER["name"], status=THEATER["status"], data="data/" + THEATER_ID + ".json", asof=out["asof"])])
    with open(os.path.join(EXPLORER, "theaters.json"), "w") as f:
        json.dump(theaters, f, indent=1)


def recount_diff(out):
    """Compare [k, n, sum_wy, sum_w] per option and category with the independent recount (tolerance 1e-9)."""
    import verify_explorer
    ver, diff = verify_explorer.recount(weighting=weighting_of(out), asof=out["asof"]), []
    W, T = weighting_of(out), dt.date.fromisoformat(out["asof"])
    for o in out["options"]:
        if not o["cases"]:
            continue
        sc = category_scores(o, o["cases"], W, T)
        for c in CATS:
            if sc[c].get("assumed"):
                continue
            mine = [sc[c]["k"], sc[c]["n"], sc[c]["swy"], sc[c]["sw"]]
            theirs = ver[o["key"]][c]
            if any(abs(a - b) > 1e-9 for a, b in zip(mine, theirs)):
                diff.append((o["key"], c, mine, theirs))
    return diff


if __name__ == "__main__":
    out = build()
    bad = check(out)
    write(out)
    print("wrote", os.path.normpath(DATA_FILE), "(+ data.json, theaters.json, history) | asof", out["asof"], "| intensity", out["intensity"]["pts"], out["intensity"]["band"])
    print("MISMATCH vs workbook counts:" if bad else "page counts match workbook counts", bad or "")
    diff = recount_diff(out)
    print("MISMATCH vs independent recount:" if diff else "risk rates match the independent recount", diff or "")
    sys.exit(1 if bad or diff else 0)
