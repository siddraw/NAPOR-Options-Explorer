"""Walk-forward backtest of the risk assessment itself (what the page shows).

For every past case, in date order, predict each of its five category outcomes using ONLY cases whose
outcome window for that category had fully closed before the case's date (no hindsight), then score the
prediction against what happened with the Brier score: (forecast - outcome)^2, averaged.
0 = perfect, 0.25 = always saying 50%. Lower is better.

Methods compared:
  raw      - the option's own rate k/n (what the page shows)
  shrunk   - (k + m * p_pool) / (n + m): the option's rate pulled toward the pooled rate, m = 2 (also 1, 4)
  pooled   - the same category's rate across ALL options known at the time (ignores option type)
  half     - always 50%
  w_<name> - recency weights (see napor_cases.CANDIDATES): the same shrunk estimate (m=2) but every past
             case counts w = weight(T - case date), T = the date being predicted. w_none equals shrunk2.
Rows dated on/after 2026-01-01 are also scored on their own ("2026-only"). A prediction is skipped when the option had no closed past case for that category yet ("no history").

Also: calibration bins, a learning curve (Brier by period), an out-of-sample split (fit on 1979-2025,
score 2026) and a robustness table for the escalation rate under rule variants.
Run: python3 backtest_risk.py   (prints tables, writes backtest_risk.json)
"""
import datetime as dt
import json
import os
import data
import napor_options as O
import napor_cases as NC

HERE = os.path.dirname(os.path.abspath(__file__))
CATS = NC.CATS
MS = (1, 2, 4)
M_MAIN = 2


def rows_from_cases(cases_by_key, flags=None):
    """One row per (case, category) with a final outcome: (date, closes_on, option, category, outcome 0/1).
    flags: option letter -> flag dict (default: the Iran flags; every theater passes its own)."""
    flags = flags or NC.FLAGS
    rows = []
    for k, cases in cases_by_key.items():
        fl = flags[k]
        for c in cases:
            d = dt.date.fromisoformat(c["date"])
            for cat in CATS:
                ok, y = NC.outcome(fl, c, cat)
                if ok:
                    rows.append(dict(date=d, closes=d + dt.timedelta(days=NC.window_days(fl, cat)), opt=k, cat=cat, y=1 if y else 0, id=c["id"]))
    rows.sort(key=lambda r: (r["date"], r["opt"], str(r["id"]), r["cat"]))
    return rows


def predict(train, r, ms=MS):
    """Forecasts for row r from the training rows (all must have closed before r's date)."""
    same_rows = [t for t in train if t["opt"] == r["opt"] and t["cat"] == r["cat"]]
    pool_rows = [t for t in train if t["cat"] == r["cat"]]
    same = [t["y"] for t in same_rows]
    pool = [t["y"] for t in pool_rows]
    if not same or not pool:
        return None
    k, n = sum(same), len(same)
    pp = sum(pool) / len(pool)
    out = dict(raw=k / n, pooled=pp, half=0.5, n=n, k=k, p_pool=pp)
    for m in ms:
        out[f"shrunk{m}"] = (k + m * pp) / (n + m)
    T = r["date"]
    for name, (scheme, param) in NC.CANDIDATES.items():
        ws = [NC.case_weight(scheme, param, T, t["date"]) for t in same_rows]
        wp = [NC.case_weight(scheme, param, T, t["date"]) for t in pool_rows]
        swy = sum(w * t["y"] for w, t in zip(ws, same_rows))
        ppw = sum(w * t["y"] for w, t in zip(wp, pool_rows)) / sum(wp)
        out["w_" + name] = (swy + M_MAIN * ppw) / (sum(ws) + M_MAIN)
    return out


def walk_forward(rows):
    preds, skipped = [], 0
    for r in rows:
        train = [t for t in rows if t["closes"] < r["date"]]          # outcome final before this case's date
        p = predict(train, r)
        if p is None:
            skipped += 1
            continue
        preds.append(dict(r, **p))
    return preds, skipped


METHODS = ["raw", "shrunk1", "shrunk2", "shrunk4", "pooled", "half"]
WMETHODS = ["w_" + c for c in NC.CANDIDATES]
ALLM = METHODS + WMETHODS
Y2026 = dt.date(2026, 1, 1)


def brier(ps, m):
    return round(sum((p[m] - p["y"]) ** 2 for p in ps) / len(ps), 4) if ps else None


def table(ps):
    out = {"overall": {m: brier(ps, m) for m in ALLM} | {"n": len(ps)}}
    for cat in CATS:
        sub = [p for p in ps if p["cat"] == cat]
        out[cat] = {m: brier(sub, m) for m in ALLM} | {"n": len(sub)}
    return out


def calibration(ps, m, edges=(0, .2, .4, .6, .8, 1.0001)):
    out = []
    for lo, hi in zip(edges, edges[1:]):
        b = [p for p in ps if lo <= p[m] < hi]
        if b:
            out.append(dict(lo=lo, hi=min(hi, 1), n=len(b), predicted=round(sum(p[m] for p in b) / len(b), 3),
                            observed=round(sum(p["y"] for p in b) / len(b), 3)))
    return out


def period(d):
    if d.year < 2026:
        if d.year <= 1994: return "1979-94"
        if d.year <= 2008: return "1995-2008"
        if d.year <= 2018: return "2009-18"
        return "2019-20" if d.year <= 2020 else ("2021-23" if d.year <= 2023 else "2024-25")
    return "2026 H1" if d.month <= 6 else "2026 H2"


def learning_curve(ps, periods=None):
    """periods: (keys in order, function date -> key). Default: the Iran periods."""
    keys, fn = periods or (["1979-94", "1995-2008", "2009-18", "2019-20", "2021-23", "2024-25", "2026 H1", "2026 H2"], period)
    out = []
    for k in keys:
        sub = [p for p in ps if fn(p["date"]) == k]
        if sub:
            out.append(dict(period=k, n=len(sub), **{m: brier(sub, m) for m in ("raw", "shrunk2", "pooled", "half")}))
    return out


def out_of_sample(rows, cut=dt.date(2025, 12, 31), label=None):
    train = [t for t in rows if t["closes"] <= cut]
    test = [r for r in rows if r["date"] > cut]
    ps, skipped = [], 0
    for r in test:
        p = predict(train, r)
        if p is None:
            skipped += 1
            continue
        ps.append(dict(r, **p))
    res = dict(train_rows=len(train), test_rows=len(test), scored=len(ps), skipped=skipped,
               brier={m: brier(ps, m) for m in METHODS})
    if label:
        res["train_label"] = label            # shown on the page instead of "2019-2025" (theaters with another record start)
    return res, ps


def robustness(ctx=None):
    """Escalation (reply) rate per trigger option under rule variants. Census judgement = ~5-day window."""
    if ctx is not None and ctx.robustness is not None:
        return ctx.robustness()
    EV = O.EV
    out = []
    variants = [
        ("As published (a clear link, timing only, or a reply by an ally group all count; ~5 days)", lambda st, prs, day: st in NC.REPLY, True),
        ("Replies by an ally group do not count", lambda st, prs, day: st in ("R-strong", "R-weak"), True),
        ("Timing-only replies do not count", lambda st, prs, day: st in ("R-strong", "R-proxy"), True),
        ("Only replies with a clear link count", lambda st, prs, day: st == "R-strong", True),
        ("Reply within 3 days (logged reply dates)", lambda st, prs, day: st in NC.REPLY and any(p_days <= 3 for p_days in prs), "lag"),
        ("Within 7 days: also any Iran/proxy strike (timing only)", lambda st, prs, day: st in NC.REPLY or bool(O._window(O._irstrike, day, 1, 7)), True),
    ]
    for key in ("C", "D", "E", "F", "G"):
        o = [x for x in O.OPTIONS if x["key"] == key][0]
        rows = [c for c in O.census if O.us_side(c[0]) and o["match"](c[0]) and c[2] in NC.COUNTED]
        res = dict(key=key, name=o["name"], cells=[])
        for label, f, mode in variants:
            k = n = 0
            for tid, _, st, _ in rows:
                day = EV[tid][1]
                lags = [(EV[p[2]][1] - day).days for p in O.pairs if p[1] == tid]
                if mode == "lag" and st in NC.REPLY and not lags:
                    continue            # reply judged in the census but no logged reply date: left out of this variant
                n += 1
                k += 1 if f(st, lags, day) else 0
            res["cells"].append(dict(variant=label, k=k, n=n))
        out.append(res)
    short = ["As published", "No ally group", "No timing only", "Clear link only", "Within 3 days", "Within 7 days, any strike"]
    return dict(variants=[v[0] for v in variants], short=short, rows=out)


def decide(tab):
    raw, sh = tab["overall"]["raw"], tab["overall"]["shrunk2"]
    worse = {c: round(tab[c]["shrunk2"] - tab[c]["raw"], 4) for c in CATS if tab[c]["n"] and tab[c]["raw"] is not None}
    adopt = raw is not None and sh is not None and raw - sh >= 0.005 and all(v <= 0.01 for v in worse.values())
    return dict(adopt=adopt, m=M_MAIN, gain=round(raw - sh, 4) if raw is not None else None, worse_by_cat=worse,
                rule="Show the NAPOR estimate if it beats the raw x of n by at least 0.005 overall and is not worse by more than 0.01 in any category.")


def decide_weighting(tab):
    """Adopt the recency weight with the lowest overall Brier only if it beats w_none by >= 0.003 overall AND is not
    worse than w_none by more than 0.01 in any category; otherwise keep none. Ties go to the milder weight."""
    ov = {c: tab["overall"]["w_" + c] for c in NC.CANDIDATES}
    best = min(NC.CANDIDATES, key=lambda c: (ov[c], NC.MILDNESS.index(c)))
    gain = round(ov["none"] - ov[best], 4)
    worse = {cat: round(tab[cat]["w_" + best] - tab[cat]["w_none"], 4) for cat in CATS
             if tab[cat]["n"] and tab[cat]["w_" + best] is not None}
    adopt = best != "none" and gain >= 0.003 - 1e-9 and all(v <= 0.01 + 1e-9 for v in worse.values())
    name = best if adopt else "none"
    scheme, param = NC.CANDIDATES[name]
    return dict(scheme=scheme, param=param, name=name, adopt=adopt, best_candidate=best, gain=gain, worse_by_cat=worse,
                rule="Adopt the recency weight with the lowest overall Brier only if it beats no weighting by at least 0.003 overall "
                     "and is not worse by more than 0.01 in any category; otherwise keep no recency weighting.")


def weighting_report(ps, tab, dec):
    t26 = table([p for p in ps if p["date"] >= Y2026])
    cands = []
    for name, (scheme, param) in NC.CANDIDATES.items():
        m = "w_" + name
        cands.append(dict(name=name, scheme=scheme, param=param, overall=tab["overall"][m], y2026=t26["overall"][m],
                          by_cat={c: tab[c][m] for c in CATS}, by_cat_2026={c: t26[c][m] for c in CATS}))
    return dict(candidates=cands, n=tab["overall"]["n"], n_2026=t26["overall"]["n"], decision=dec), t26


# ---- Political category: rule changed 2026-10-26 (approved by Sidd) ----
# New rule ("talks only, within 14 days", tested in round 2 as P2): risk = no actual talks, meeting, negotiation, proposal, ceasefire or deal
# between the US and the adversary (directly or through a mediator) logged within 14 days. Statements, threats and appeals do not count.
# The old rule counted any Diplomatic event, statements included. It is still computed here so the Report Card can show old vs new.
CONC = O.TALK_WORDS      # same words as the "B" move in the export


def political_rows(cases_by_key, window, legacy=False, ctx=None):
    """Political-category rows: risk = no matching event within `window` days after the case.
    legacy=False: the live rule (talks only, O._talks / theater _talks). legacy=True: the pre-2026-10-26 rule (any Diplomatic event)."""
    if ctx is not None:
        last, evs = ctx.last, ctx.talk_dates(legacy)
    else:
        last = NC.LAST
        evs = [e[1] for e in data.events if (O._diplo(e) if legacy else O._talks(e))]
    rows = []
    for k, cases in cases_by_key.items():
        for c in cases:
            d = dt.date.fromisoformat(c["date"])
            found = any(d + dt.timedelta(days=1) <= x <= d + dt.timedelta(days=window) for x in evs)
            if found or (last - d).days >= window:
                rows.append(dict(date=d, closes=d + dt.timedelta(days=window), opt=k, cat="political", y=0 if found else 1, id=c["id"]))
    rows.sort(key=lambda r: (r["date"], r["opt"], str(r["id"]), r["cat"]))
    return rows


def political_change(cases_by_key, tab, dec, ctx=None):
    """Old vs new Brier of the political category (and of the index) on the same date-ordered replay. The new rule is the live one."""
    est = "w_" + dec["name"]                                 # the estimate the page shows (shrunk2 when no weighting)
    meas = [c for c in CATS if tab[c][est] is not None]          # a category a theater does not measure (no predictions) is left out of the index
    others = [c for c in meas if c != "political"]
    out = []
    for label, legacy in (("Old rule: any diplomatic event within 14 days, statements and threats included", True),
                          ("New rule: only talks, a meeting, a proposal, a ceasefire or a deal within 14 days", False)):
        rows = political_rows(cases_by_key, 14, legacy, ctx)
        ps, skipped = walk_forward(rows)
        t = brier(ps, est)
        out.append(dict(label=label, legacy=legacy, rows=len(rows), predictions=len(ps), risk_cases=sum(r["y"] for r in rows), est=t,
                        index_brier=round((sum(tab[c][est] for c in others) + t) / (len(others) + 1), 4)))
    return dict(changed="2026-10-26", approved_by="Sidd", method=est, old=out[0], new=out[1],
                note="Brier of the estimate the page shows, same replay in date order (only rows closed before each date). Index Brier = average of the "
                     "category Brier scores. The two rules define the outcome differently, so a lower Brier means the new rule is easier to predict, "
                     "not that it is a better measure.")


def run(cases_by_key, ctx=None):
    """ctx = a theater context (see theaters/houthis/backtest.py); None = Iran."""
    rows = rows_from_cases(cases_by_key, ctx.flags if ctx else None)
    ps, skipped = walk_forward(rows)
    tab = table(ps)
    oos, _ = out_of_sample(rows, *( (ctx.oos_cut, ctx.oos_label) if ctx else (dt.date(2025, 12, 31), "1979-2025") ))
    dec_w = decide_weighting(tab)
    wrep, t26 = weighting_report(ps, tab, dec_w)
    return dict(
        generated=dt.date.today().isoformat(), rows=len(rows), predictions=len(ps), skipped_no_history=skipped,
        brier=tab, brier_2026=t26, calibration=dict(raw=calibration(ps, "raw"), shrunk2=calibration(ps, "shrunk2")),
        learning=learning_curve(ps, ctx.periods if ctx else None), out_of_sample=oos, robustness=robustness(ctx), decision=decide(tab),
        weighting=wrep, political_change=political_change(cases_by_key, tab, dec_w, ctx))


def all_cases():
    return {o["key"]: NC.option_cases(o["key"]) for o in O.OPTIONS}


def window_covers_lags(cases_by_key, flags=None):
    """The window a theater declares must reach the latest linked reply it can count (people, military)."""
    flags = flags or NC.FLAGS
    bad = []
    for k, cases in cases_by_key.items():
        fl = flags[k]
        for c in cases:
            lag = max([r["days"] for r in c.get("replies", [])] or [0])
            for cat, need in (("people", max(lag, 7)), ("military", lag)):
                if NC.outcome(fl, c, cat)[0] and need > NC.window_days(fl, cat):
                    bad.append((k, c["id"], cat, need, NC.window_days(fl, cat)))
    return bad


def no_hindsight_check(cases_by_key, flags=None):
    """Appending a fake future case must not change any earlier prediction, and every category's closing window must
    reach the latest reply lag that category can count (so no case is used while its outcome window is open)."""
    flags = flags or NC.FLAGS
    rows = rows_from_cases(cases_by_key, flags)
    base, _ = walk_forward(rows)
    fake_day = max(r["date"] for r in rows) + dt.timedelta(days=30)
    extra = [dict(date=fake_day, closes=fake_day + dt.timedelta(days=NC.window_days(flags[k], c)), opt=k, cat=c, y=1, id="FAKE")
             for k in cases_by_key for c in CATS]
    again, _ = walk_forward(sorted(rows + extra, key=lambda r: (r["date"], r["opt"], str(r["id"]), r["cat"])))
    again = [p for p in again if p["id"] != "FAKE"]
    key = lambda p: (p["date"], p["opt"], str(p["id"]), p["cat"])
    a = {key(p): tuple(p[m] for m in ALLM) for p in base}
    b = {key(p): tuple(p[m] for m in ALLM) for p in again}
    return a == b and not window_covers_lags(cases_by_key, flags), len(a)


def report(res, cb, flags=None, tag=""):
    """Print the backtest tables for one theater (tag = theater id when it is not Iran)."""
    print(f"Risk-assessment backtest: {res['predictions']} predictions from {res['rows']} case-category outcomes "
          f"({res['skipped_no_history']} skipped: no closed past case of that option yet).")
    print("\nBrier score (lower is better; 0.25 = always 50%)")
    print("  " + "category".ljust(12) + "".join(m.rjust(9) for m in METHODS) + "      n")
    for cat in ["overall"] + CATS:
        t = res["brier"][cat]
        print("  " + cat.ljust(12) + "".join((f"{t[m]:.3f}" if t[m] is not None else "-").rjust(9) for m in METHODS) + f"{t['n']:7d}")
    d = res["decision"]
    print(f"\nDecision (m={d['m']}): shrinkage gain {d['gain']:+.4f}; worse by category {d['worse_by_cat']} -> "
          f"{'ADOPT shrunk value as NAPOR estimate' if d['adopt'] else 'KEEP raw x of n'}")
    w = res["weighting"]
    print(f"\nRecency weights (Brier of the NAPOR estimate; {w['n']} predictions, {w['n_2026']} dated 2026 or later)")
    print("  " + "candidate".ljust(8) + "overall".rjust(9) + "2026-only".rjust(11) + "".join(c.rjust(11) for c in CATS))
    for c in w["candidates"]:
        print("  " + c["name"].ljust(8) + f"{c['overall']:.4f}".rjust(9) + f"{c['y2026']:.4f}".rjust(11) + "".join((f"{c['by_cat'][k]:.4f}" if c['by_cat'][k] is not None else "-").rjust(11) for k in CATS))
    dw = w["decision"]
    print(f"Weighting decision: best by overall Brier = {dw['best_candidate']}; gain over no weighting {dw['gain']:+.4f}; worse by category {dw['worse_by_cat']} -> " +
          (f"ADOPT recency weight {dw['name']}" if dw["adopt"] else "KEEP no recency weighting"))
    pc = res["political_change"]
    print(f"\nPolitical category (rule changed {pc['changed']}, approved by {pc['approved_by']}; Brier of '{pc['method']}'; 0.25 = coin flip)")
    for r in (pc["old"], pc["new"]):
        print(f"  {r['label']}: {r['predictions']} predictions, risk in {r['risk_cases']} of {r['rows']} cases; Brier {r['est']:.4f}; index-level {r['index_brier']:.4f}")
    print("\nCalibration (raw): " + "; ".join(f"{b['lo']:.1f}-{b['hi']:.1f}: said {b['predicted']:.0%}, happened {b['observed']:.0%} (n={b['n']})" for b in res["calibration"]["raw"]))
    print("Calibration (shrunk m=2): " + "; ".join(f"{b['lo']:.1f}-{b['hi']:.1f}: said {b['predicted']:.0%}, happened {b['observed']:.0%} (n={b['n']})" for b in res["calibration"]["shrunk2"]))
    print("\nLearning curve: " + "; ".join(f"{l['period']} raw {l['raw']:.3f} / shrunk {l['shrunk2']:.3f} / pooled {l['pooled']:.3f} (n={l['n']})" for l in res["learning"]))
    o = res["out_of_sample"]
    print(f"\nOut of sample (fit {o.get('train_label', '1979-2025')}, score 2026): {o['scored']} scored, {o['skipped']} skipped; " +
          ", ".join(f"{m} {v:.3f}" for m, v in o["brier"].items() if v is not None))
    print("\nEscalation rate under rule variants:")
    for r in res["robustness"]["rows"]:
        print("  " + r["key"] + "  " + " | ".join(f"{c['k']}/{c['n']}" for c in r["cells"]))
    print("  columns: " + " | ".join(res["robustness"]["variants"]))
    ok, n = no_hindsight_check(cb, flags)
    print(f"\nNo-hindsight check (fake future case appended): {'PASS' if ok else 'FAIL'} ({n} earlier predictions unchanged)")


def main(argv):
    """python3 backtest_risk.py [theater ...]  (default: every theater in explorer/theaters.json)."""
    import theaters
    ids = argv or theaters.registered()
    ok = True
    for tid in ids:
        if tid == "iran":
            cb = all_cases()
            res = run(cb)
            json.dump(res, open(os.path.join(HERE, "backtest_risk.json"), "w"), indent=1, default=str)
            report(res, cb)
        else:
            import importlib
            print(f"\n===== {tid} =====")
            importlib.import_module(f"theaters.{tid}.backtest").run_and_report(report)


if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
