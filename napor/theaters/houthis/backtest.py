"""Houthis: walk-forward backtest of the page's own numbers (same method and decision rules as backtest_risk.py).

Writes napor/theaters/houthis/backtest_risk.json. verify.py and export.py read the written weighting decision from it.
"""
import json
import os
import types

import backtest_risk as BR
from theaters.houthis import cases as K, config as C

HERE = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(HERE, "backtest_risk.json")


def _robustness():
    """Escalation (reply) rate per trigger option under rule variants, from the Houthi census (same variants as Iran)."""
    variants = [
        ("As published (R-strong, R-weak, R-proxy count; ~5 days)", lambda st, lags: st in K.REPLY),
        ("Proxy replies do not count", lambda st, lags: st in ("R-strong", "R-weak")),
        ("Weak replies do not count", lambda st, lags: st in ("R-strong", "R-proxy")),
        ("Only strong replies count", lambda st, lags: st == "R-strong"),
        ("Reply within 3 days (logged reply dates)", lambda st, lags: st in K.REPLY and any(x <= 3 for x in lags)),
    ]
    out = []
    for o in C.OPTIONS:
        k = o["key"]
        if not C.FLAGS[k]["trigger"]:
            continue
        rows = [c for c in K.census if K.us_side(c[0]) and K.US_OPTION.get(c[0]) == k and c[2] in K.COUNTED]
        res = dict(key=k, name=o["name"], cells=[])
        for label, f in variants:
            kk = n = 0
            for tid, _, st, _ in rows:
                lags = [(K.EV[p[2]][1] - K.EV[tid][1]).days for p in K.pairs if p[1] == tid]
                if "3 days" in label and st in K.REPLY and not lags:
                    continue
                n += 1
                kk += 1 if f(st, lags) else 0
            res["cells"].append(dict(variant=label, k=kk, n=n))
        out.append(res)
    return dict(variants=[v[0] for v in variants], short=["As published", "No proxy", "No weak", "Strong only", "Within 3 days"], rows=out)


def _talk_dates(words):
    return [e[1] for e in K.EVENTS if K._talks(e) and (words is None or any(w in e[3].lower() for w in words))]


def context():
    return types.SimpleNamespace(flags=C.FLAGS, last=K.LAST, talk_dates=_talk_dates, robustness=_robustness,
                                 periods=(C.PERIOD_KEYS, C.period), oos_cut=C.OOS_CUT, oos_label=C.OOS_LABEL)


def run(cb=None):
    cb = cb or K.all_cases()
    return BR.run(cb, context()), cb


def run_and_report(report):
    res, cb = run()
    json.dump(res, open(JSON_FILE, "w"), indent=1, default=str)
    report(res, cb, C.FLAGS)
    return res


def weighting_in_force():
    try:
        d = json.load(open(JSON_FILE))["weighting"]["decision"]
        return d["scheme"], d["param"]
    except Exception:                                  # noqa: BLE001
        return "none", None
