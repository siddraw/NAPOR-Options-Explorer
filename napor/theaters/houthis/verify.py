"""Houthis: independent recount of every percentage the page shows for this tab.

Recomputes each option's five risk-category numbers straight from the research files and config.py WITHOUT using
cases.py or export.py (so a mistake in the case builder cannot hide). Writes explorer/verify-houthis.json; the Node
page test compares it with what the page computes in the browser, at the as-of date and at look-back dates.

Per option and category it records [k, n, sum_wy, sum_w]: k of n are the plain counts; sum_w is the sum of the recency
weights of the counted cases and sum_wy the same sum over the cases that count as risk (weights as in verify_explorer.py).
Estimate = (sum_wy + 2 x pooled) / (sum_w + 2) when the written decision rule adopted it, else the plain k / n.
"""
import datetime as dt
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
import data
import napor_ids as N
from theaters.houthis import events_early as E, events_late as L, config as C

OUT = os.path.join(HERE, "..", "..", "..", "explorer", "verify-houthis.json")
BT_JSON = os.path.join(HERE, "backtest_risk.json")
M = 2
CATS = ("people", "escalation", "military", "economic", "political")
REPLY = ("R-strong", "R-weak", "R-proxy")
COUNTED = REPLY + ("N",)
ERA = dt.date(2026, 1, 1)

EVL = sorted(E.EVENTS + L.EVENTS, key=lambda e: (e[1], e[0]))
EV = {e[0]: e for e in EVL}
SRC = {**E.SOURCES, **L.SOURCES}
VERD = {**E.VERDICT, **L.VERDICT}
PARTLY = set(E.PARTLY) | set(L.PARTLY)
OPT = {**E.US_OPTION, **L.US_OPTION}
WINDOWS = list(E.WINDOWS) + list(L.WINDOWS)
LAST = max(e[1] for e in EVL)
DAY = dt.timedelta(days=1)


def kind(i):
    return C.KIND_OVERRIDE.get(i) or data.act_kind(EV[i][3], EV[i][5])


def cred(i):
    reps = [dict(outlet=N.outlet_name(s["outlet"]), kind=N.source_kind(s["outlet"], C.CLAIM_MEDIA, C.CLAIM_LABEL), seen=s.get("seen", "")) for s in SRC.get(i, [])]
    chk = "Not supported" if VERD.get(i) == "not_confirmed" else ("Partly verified" if i in PARTLY else "Verified")
    return N.credibility_of(reps, chk)


GOOD = {e[0] for e in EVL if cred(e[0]) >= 0.5}
CENSUS = [c for c in list(E.CENSUS) + list(L.CENSUS) if c[0] in GOOD and EV[c[0]][2].lower().startswith("us")]
PAIRS = [p for p in list(E.PAIRS) + list(L.PAIRS) if p[1] in GOOD and p[2] in GOOD]


def weighting_in_force():
    try:
        d = json.load(open(BT_JSON))
        return (d["weighting"]["decision"]["scheme"], d["weighting"]["decision"]["param"]), bool(d["decision"]["adopt"])
    except Exception:                                  # noqa: BLE001
        return ("none", None), False


def weight(scheme, param, asof, day):
    if scheme == "none":
        return 1.0
    if scheme == "era":
        return float(param) if day < ERA else 1.0
    if scheme == "halflife":
        return 0.5 ** ((asof - day).days / param)
    raise ValueError(scheme)


def add(acc, w, risk):
    acc[1] += 1; acc[3] += w
    if risk:
        acc[0] += 1; acc[2] += w


def recount(weighting=None, asof=None):
    """Numbers as they looked on `asof` (default: the latest news): only cases dated on or before it, only events logged by it.
    A window that has not finished by then counts only once the answer is already "yes" (a reply, an attack, talks), as the page does."""
    (scheme, param) = weighting or weighting_in_force()[0]
    T = dt.date.fromisoformat(asof) if isinstance(asof, str) else (asof or LAST)
    known = [e for e in EVL if e[1] <= T and e[0] in GOOD]
    usd = lambda i: EV[i][2].lower().startswith("us")
    hou = lambda i: C.adversary_side(EV[i][2])
    def win(day, a, b, test):
        return [e for e in known if day + a * DAY <= e[1] <= day + b * DAY and test(e[0])]
    attack = lambda i: hou(i) and kind(i) in ("Kinetic", "Maritime")
    ship = lambda i: hou(i) and (kind(i) == "Maritime" or i in C.SHIP_ATTACK_EXTRA)
    talk = lambda i: kind(i) == "Diplomatic"
    done = lambda day, n: day + n * DAY <= T
    strike7 = lambda day: True if win(day, 1, 7, attack) else (False if done(day, 7) else None)
    talks14 = lambda day: True if win(day, 1, 14, talk) else (False if done(day, 14) else None)
    new = lambda: [[0, 0, 0.0, 0.0] for _ in range(5)]
    out = {}
    for o in C.OPTIONS:
        k = o["key"]; fl = C.FLAGS[k]
        ppl, esc, mil, eco, pol = new()
        if fl["is_hold"]:
            rows = [("W", m) for m in hold_mondays() if m <= T]
        elif fl["trigger"]:
            rows = [(c[0], EV[c[0]][1]) for c in CENSUS if OPT.get(c[0]) == k and c[2] in COUNTED]
        else:
            rows = [(i, EV[i][1]) for i in sorted(GOOD) if OPT.get(i) == k and usd(i) and (LAST - EV[i][1]).days >= 7]
        rows = [(i, day) for i, day in rows if day <= T]
        for tid, day in rows:
            w = weight(scheme, param, T, day)
            s7 = strike7(day)
            if fl["is_hold"]:
                if s7 is not None:
                    add(esc, w, s7); add(mil, w, s7)
                flag = C.PEOPLE_HURT.get(day.isoformat()) or ((False, [], "") if not [e for e in EVL if e[0] in GOOD and day + DAY <= e[1] <= day + 7 * DAY and attack(e[0])] else None)
                if done(day, 7) and flag is not None:
                    add(ppl, w, bool(flag[0]))
            else:
                prs = [p for p in PAIRS if p[1] == tid and EV[p[2]][1] <= T]
                if s7 is not None:
                    add(ppl, w, any(p[4] == "Y" for p in prs))
                if fl["trigger"]:
                    st = [c[2] for c in CENSUS if c[0] == tid][0]
                    rep = (st in REPLY) if done(day, 5) else (True if prs else None)
                    if rep is not None:
                        add(esc, w, rep)
                        if fl["military"] == "reply":
                            add(mil, w, any(kind(p[2]) == "Kinetic" for p in prs))
                elif s7 is not None:
                    add(esc, w, s7)
            if done(day, 7):
                add(eco, w, len(win(day, 1, 7, ship)) > len(win(day, -7, -1, ship)))
            t14 = talks14(day)
            if t14 is not None:
                add(pol, w, t14 is False)
        out[k] = dict(people=ppl, escalation=esc, military=mil, economic=eco, political=pol, n=len(rows))
    return out


def hold_mondays():
    """Mondays from Nov 20, 2023 whose week (Monday to the next Monday) is outside the fighting windows and has no US move of kinds C-H."""
    us_kinds = C.US_MOVE_KINDS
    out, m = [], C.HOLD_START
    while m <= LAST - 7 * DAY:
        a, b = m, m + 7 * DAY
        skip = any(not (b < x or a > y) for x, y in WINDOWS) or m.isoformat() in C.UNCERTAIN
        skip = skip or any(a <= e[1] <= b and e[0] in GOOD and EV[e[0]][2].lower().startswith("us")
                           and (OPT.get(e[0], "B") in "CDEFGH" or kind(e[0]) in us_kinds) for e in EVL)
        if not skip:
            out.append(m)
        m += 7 * DAY
    return out


def estimates(out, shrink):
    opts = list(out)
    assumed = lambda k, c: c == "military" and C.FLAGS[k]["military"] == "none"
    pool = {}
    for c in CATS:
        swy = sum(out[k][c][2] for k in opts if not assumed(k, c))
        sw = sum(out[k][c][3] for k in opts if not assumed(k, c))
        pool[c] = swy / sw if sw else None
    est = {}
    for k in opts:
        est[k] = {}
        for c in CATS:
            a = out[k][c]
            if assumed(k, c):
                est[k][c] = 0.0
            elif not a[1]:
                est[k][c] = None
            else:
                est[k][c] = (a[2] + M * pool[c]) / (a[3] + M) if (shrink and pool[c] is not None) else a[0] / a[1]
    return est, pool


LOOKBACKS = ("2016-10-14", "2023-12-31", "2024-06-30", "2025-05-06", "2026-09-10")      # past dates the page test also checks (no hindsight)


def run():
    (scheme, param), shrink = weighting_in_force()
    rc = recount((scheme, param), LAST)
    est, pool = estimates(rc, shrink)
    for k in rc:
        rc[k]["estimate"] = est[k]
    lbs = {}
    for iso in LOOKBACKS:
        r = recount((scheme, param), iso)
        e, pl = estimates(r, shrink)
        for k in r:
            r[k]["estimate"] = e[k]
        lbs[iso] = dict(asof=iso, pooled=pl, options=r)
    out = dict(asof=LAST.isoformat(), weighting=dict(scheme=scheme, param=param), shrink=shrink, m=M, pooled=pool, options=rc, lookbacks=lbs)
    json.dump(out, open(OUT, "w"), indent=1)
    print(f"as of {LAST} | recency weighting: {scheme} {param if param is not None else ''} | estimate shrunk: {shrink}".rstrip())
    for k, v in rc.items():
        print(k, {c: [v[c][0], v[c][1], round(v[c][2], 4), round(v[c][3], 4)] for c in CATS}, "n", v["n"])
    return []
