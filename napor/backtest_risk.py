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
A prediction is skipped when the option had no closed past case for that category yet ("no history").

Also: calibration bins, a learning curve (Brier by period), an out-of-sample split (fit on 2019-2025,
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


def rows_from_cases(cases_by_key):
    """One row per (case, category) with a final outcome: (date, closes_on, option, category, outcome 0/1)."""
    rows = []
    for k, cases in cases_by_key.items():
        fl = NC.FLAGS[k]
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
    same = [t["y"] for t in train if t["opt"] == r["opt"] and t["cat"] == r["cat"]]
    pool = [t["y"] for t in train if t["cat"] == r["cat"]]
    if not same or not pool:
        return None
    k, n = sum(same), len(same)
    pp = sum(pool) / len(pool)
    out = dict(raw=k / n, pooled=pp, half=0.5, n=n, k=k, p_pool=pp)
    for m in ms:
        out[f"shrunk{m}"] = (k + m * pp) / (n + m)
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


def brier(ps, m):
    return round(sum((p[m] - p["y"]) ** 2 for p in ps) / len(ps), 4) if ps else None


def table(ps):
    out = {"overall": {m: brier(ps, m) for m in METHODS} | {"n": len(ps)}}
    for cat in CATS:
        sub = [p for p in ps if p["cat"] == cat]
        out[cat] = {m: brier(sub, m) for m in METHODS} | {"n": len(sub)}
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
        return "2019-20" if d.year <= 2020 else ("2021-23" if d.year <= 2023 else "2024-25")
    return "2026 H1" if d.month <= 6 else "2026 H2"


def learning_curve(ps):
    keys = ["2019-20", "2021-23", "2024-25", "2026 H1", "2026 H2"]
    out = []
    for k in keys:
        sub = [p for p in ps if period(p["date"]) == k]
        if sub:
            out.append(dict(period=k, n=len(sub), **{m: brier(sub, m) for m in ("raw", "shrunk2", "pooled", "half")}))
    return out


def out_of_sample(rows, cut=dt.date(2025, 12, 31)):
    train = [t for t in rows if t["closes"] <= cut]
    test = [r for r in rows if r["date"] > cut]
    ps, skipped = [], 0
    for r in test:
        p = predict(train, r)
        if p is None:
            skipped += 1
            continue
        ps.append(dict(r, **p))
    return dict(train_rows=len(train), test_rows=len(test), scored=len(ps), skipped=skipped,
                brier={m: brier(ps, m) for m in METHODS}), ps


def robustness():
    """Escalation (reply) rate per trigger option under rule variants. Census judgement = ~5-day window."""
    EV = O.EV
    out = []
    variants = [
        ("As published (R-strong, R-weak, R-proxy count; ~5 days)", lambda st, prs, day: st in NC.REPLY, True),
        ("Proxy replies do not count", lambda st, prs, day: st in ("R-strong", "R-weak"), True),
        ("Weak replies do not count", lambda st, prs, day: st in ("R-strong", "R-proxy"), True),
        ("Only strong replies count", lambda st, prs, day: st == "R-strong", True),
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
    short = ["As published", "No proxy", "No weak", "Strong only", "Within 3 days", "Within 7 days, any strike"]
    return dict(variants=[v[0] for v in variants], short=short, rows=out)


def decide(tab):
    raw, sh = tab["overall"]["raw"], tab["overall"]["shrunk2"]
    worse = {c: round(tab[c]["shrunk2"] - tab[c]["raw"], 4) for c in CATS if tab[c]["n"] and tab[c]["raw"] is not None}
    adopt = raw is not None and sh is not None and raw - sh >= 0.005 and all(v <= 0.01 for v in worse.values())
    return dict(adopt=adopt, m=M_MAIN, gain=round(raw - sh, 4) if raw is not None else None, worse_by_cat=worse,
                rule="Show the shrunk value if it beats raw by at least 0.005 overall and is not worse by more than 0.01 in any category.")


def run(cases_by_key):
    rows = rows_from_cases(cases_by_key)
    ps, skipped = walk_forward(rows)
    tab = table(ps)
    oos, _ = out_of_sample(rows)
    return dict(
        generated=dt.date.today().isoformat(), rows=len(rows), predictions=len(ps), skipped_no_history=skipped,
        brier=tab, calibration=dict(raw=calibration(ps, "raw"), shrunk2=calibration(ps, "shrunk2")),
        learning=learning_curve(ps), out_of_sample=oos, robustness=robustness(), decision=decide(tab))


def all_cases():
    return {o["key"]: NC.option_cases(o["key"]) for o in O.OPTIONS}


def no_hindsight_check(cases_by_key):
    """Appending a fake future case must not change any earlier prediction."""
    rows = rows_from_cases(cases_by_key)
    base, _ = walk_forward(rows)
    fake_day = max(r["date"] for r in rows) + dt.timedelta(days=30)
    extra = [dict(date=fake_day, closes=fake_day + dt.timedelta(days=w), opt=k, cat=c, y=1, id="FAKE")
             for k in cases_by_key for c, w in (("people", 7), ("escalation", 5), ("economic", 7), ("political", 14))]
    again, _ = walk_forward(sorted(rows + extra, key=lambda r: (r["date"], r["opt"], str(r["id"]), r["cat"])))
    again = [p for p in again if p["id"] != "FAKE"]
    key = lambda p: (p["date"], p["opt"], str(p["id"]), p["cat"])
    a = {key(p): tuple(p[m] for m in METHODS) for p in base}
    b = {key(p): tuple(p[m] for m in METHODS) for p in again}
    return a == b, len(a)


if __name__ == "__main__":
    cb = all_cases()
    res = run(cb)
    json.dump(res, open(os.path.join(HERE, "backtest_risk.json"), "w"), indent=1, default=str)
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
    print("\nCalibration (raw): " + "; ".join(f"{b['lo']:.1f}-{b['hi']:.1f}: said {b['predicted']:.0%}, happened {b['observed']:.0%} (n={b['n']})" for b in res["calibration"]["raw"]))
    print("Calibration (shrunk m=2): " + "; ".join(f"{b['lo']:.1f}-{b['hi']:.1f}: said {b['predicted']:.0%}, happened {b['observed']:.0%} (n={b['n']})" for b in res["calibration"]["shrunk2"]))
    print("\nLearning curve: " + "; ".join(f"{l['period']} raw {l['raw']:.3f} / shrunk {l['shrunk2']:.3f} / pooled {l['pooled']:.3f} (n={l['n']})" for l in res["learning"]))
    o = res["out_of_sample"]
    print(f"\nOut of sample (fit 2019-2025, score 2026): {o['scored']} scored, {o['skipped']} skipped; " +
          ", ".join(f"{m} {v:.3f}" for m, v in o["brier"].items() if v is not None))
    print("\nEscalation rate under rule variants:")
    for r in res["robustness"]["rows"]:
        print("  " + r["key"] + "  " + " | ".join(f"{c['k']}/{c['n']}" for c in r["cells"]))
    print("  columns: " + " | ".join(res["robustness"]["variants"]))
    ok, n = no_hindsight_check(cb)
    print(f"\nNo-hindsight check (fake future case appended): {'PASS' if ok else 'FAIL'} ({n} earlier predictions unchanged)")
