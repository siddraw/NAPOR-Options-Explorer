"""Independent recount of every percentage the Options Explorer shows.

Recomputes each option's five risk-category rates straight from data.py (census, pairs, events),
without using export_explorer.py or napor_cases.py, and writes them to explorer/verify.json. The page test compares
these with what the page computes in the browser. Run: python3 verify_explorer.py

Per option and category it records [k, n, sum_wy, sum_w]: k of n are the plain counts; sum_w is the sum of the
recency weights of the counted cases and sum_wy the same sum over the cases that count as risk. The weights are
computed here (not imported): none = 1; era25/era50 = 0.25/0.5 before 2026-01-01, else 1; hl<H> = 0.5 ** (age in
days / H), age measured from the as-of date. The weighting in force is read from backtest_risk.json (the written
decision rule), or can be passed in. Estimate = (sum_wy + 2 x pooled) / (sum_w + 2), pooled = sum_wy / sum_w
over all options (military categories assumed 0 are left out of the pool and shown as 0).
"""
import json, os, datetime as dt
import data, napor_options as O

HERE = os.path.dirname(os.path.abspath(__file__))
EV = {e[0]: e for e in data.events}
LAST = max(e[1] for e in data.events)
REPLY = ("R-strong", "R-weak", "R-proxy"); COUNTED = REPLY + ("N",)
M = 2
ERA = dt.date(2026, 1, 1)
CATS = ("people", "escalation", "military", "economic", "political")


def weight(scheme, param, asof, day):
    """Recency weight of a case dated `day` when the estimate is made on `asof` (written out again on purpose)."""
    if scheme == "none":
        return 1.0
    if scheme == "era":
        return float(param) if day < ERA else 1.0
    if scheme == "halflife":
        return 0.5 ** ((asof - day).days / param)
    raise ValueError(scheme)


def weighting_in_force():
    try:
        d = json.load(open(os.path.join(HERE, "backtest_risk.json")))["weighting"]["decision"]
        return d["scheme"], d["param"]
    except Exception:                                  # noqa: BLE001
        return "none", None


def within(day, a, b, test):
    return any(test(e) for e in data.events if day + dt.timedelta(days=a) <= e[1] <= day + dt.timedelta(days=b))


def recount(weighting=None, asof=None):
  scheme, param = weighting or weighting_in_force()
  asof = dt.date.fromisoformat(asof) if isinstance(asof, str) else (asof or LAST)
  if asof < LAST:
      return recount_at(scheme, param, asof)
  out = {}
  for o in O.OPTIONS:
      k = o["key"]
      if o["match"]:
          rows = [c for c in data.census if O.us_side(c[0]) and o["match"](c[0])]
      elif k in ("B", "H"):
          rows = [(i, None, None, None) for i in O.option_cases(k)]
      else:
          out[k] = recount_hold(scheme, param, asof)
          continue
      ppl, esc, mil, eco, pol = [0, 0, 0.0, 0.0], [0, 0, 0.0, 0.0], [0, 0, 0.0, 0.0], [0, 0, 0.0, 0.0], [0, 0, 0.0, 0.0]
      for tid, _, st, _ in rows:
          day = EV[tid][1]; full7 = (LAST - day).days >= 7; w = weight(scheme, param, asof, day)
          prs = [p for p in data.pairs if p[1] == tid]
          if full7:
              add(ppl, w, (tid in O.CIVILIAN_HARM) or any(p[4] == "Y" for p in prs))
          if o["match"] and k in ("C", "D", "E", "F", "G"):
              if st in COUNTED:
                  add(esc, w, st in REPLY)
                  if k in ("D", "E", "F", "G"):
                      add(mil, w, any(data.event_kind[p[2]] == "Kinetic" for p in prs))
          elif full7:
              add(esc, w, within(day, 1, 7, O._irstrike))
          if full7:
              b = sum(1 for e in data.events if O._ship(e) and day - dt.timedelta(days=7) <= e[1] <= day - dt.timedelta(days=1))
              a = sum(1 for e in data.events if O._ship(e) and day + dt.timedelta(days=1) <= e[1] <= day + dt.timedelta(days=7))
              add(eco, w, a > b)
          talks = within(day, 1, 14, O._talks)
          if talks or (LAST - day).days >= 14:
              add(pol, w, not talks)
      out[k] = dict(people=ppl, escalation=esc, military=mil, economic=eco, political=pol, n=len(rows))
  return out


def add(acc, w, risk):
    """acc = [k, n, sum_wy, sum_w]: one more counted case with weight w; risk = does it count as risk."""
    acc[1] += 1; acc[3] += w
    if risk:
        acc[0] += 1; acc[2] += w


def estimates(out):
    """Estimate per option and category from the [k, n, sum_wy, sum_w] numbers (same formula as the page)."""
    opts = [k for k in out if k != "n"]
    pool = {}
    for c in CATS:
        swy = sum(out[k][c][2] for k in opts if k in out and not ASSUMED_MIL(k, c))
        sw = sum(out[k][c][3] for k in opts if not ASSUMED_MIL(k, c))
        pool[c] = swy / sw if sw else None
    est = {}
    for k in opts:
        est[k] = {}
        for c in CATS:
            a = out[k][c]
            if ASSUMED_MIL(k, c):
                est[k][c] = 0.0
            elif not a[1]:
                est[k][c] = None
            else:
                est[k][c] = (a[2] + M * pool[c]) / (a[3] + M) if pool[c] is not None else a[0] / a[1]
    return est, pool


# Options with no direct military cost expected from the move itself (their military category is an assumed 0).
NO_MIL = ("B", "C", "H")
ASSUMED_MIL = lambda k, c: c == "military" and k in NO_MIL


def hold_mondays():
    """Mondays of the 2026 war whose week has no logged US move of kinds C-H (option A cases). Needs all events."""
    import hold_weeks as HW
    us_kinds = ("Sanctions", "Maritime", "Kinetic", "Posture")
    usable = lambda e: e[0] not in data.MERGED and O.N.counts(e[0]) and not e[2].lower().startswith("houthi")
    m = dt.date(2026, 3, 2)          # first Monday after the war began (Feb 28, 2026)
    assert m.weekday() == 0 and m - HW.START < dt.timedelta(days=7)
    out = []
    while m <= LAST - dt.timedelta(days=7):
        a, b = m, m + dt.timedelta(days=7)
        skip = any(not (b < x or a > y) for x, y, _ in HW.EXCLUDED) or m.isoformat() in HW.UNCERTAIN
        skip = skip or any(a <= e[1] <= b and e[2].lower().startswith("us") and usable(e) and data.event_kind[e[0]] in us_kinds for e in data.events)
        if not skip:
            out.append(m)
        m += dt.timedelta(days=7)
    return out


def recount_at(scheme, param, T):
    """The same numbers as they looked on past date T: only cases dated on or before T, only events logged by T.
    A window that has not finished by T counts only once the answer is already "yes" (a reply, a strike, talks),
    as the page does. Which cases exist (census, hold weeks) is as published."""
    import hold_weeks as HW
    day1 = dt.timedelta(days=1)
    known = [e for e in data.events if e[1] <= T]
    win = lambda day, a, b, test: any(test(e) for e in known if day + dt.timedelta(days=a) <= e[1] <= day + dt.timedelta(days=b))
    done = lambda day, n: day + dt.timedelta(days=n) <= T
    def ship(day, a, b):
        return sum(1 for e in known if O._ship(e) and day + dt.timedelta(days=a) <= e[1] <= day + dt.timedelta(days=b))
    def strike7(day):
        return True if win(day, 1, 7, O._irstrike) else (False if done(day, 7) else None)
    def talks14(day):
        return True if win(day, 1, 14, O._talks) else (False if done(day, 14) else None)
    new = lambda: [[0, 0, 0.0, 0.0] for _ in range(5)]
    out = {}
    for o in O.OPTIONS:
        k = o["key"]
        ppl, esc, mil, eco, pol = new()
        if o["match"]:
            rows = [c for c in data.census if O.us_side(c[0]) and o["match"](c[0])]
        elif k in ("B", "H"):
            rows = [(i, None, None, None) for i in O.option_cases(k)]
        else:
            rows = None
        if rows is not None:
            cases = [(EV[r[0]][1], r) for r in rows if EV[r[0]][1] <= T]
            for day, (tid, _, st, _) in cases:
                w = weight(scheme, param, T, day)
                prs = [p for p in data.pairs if p[1] == tid and EV[p[2]][1] <= T]
                s7 = strike7(day)
                if s7 is not None:
                    add(ppl, w, (tid in O.CIVILIAN_HARM) or any(p[4] == "Y" for p in prs))
                if o["match"] and k in ("C", "D", "E", "F", "G"):
                    rep = None if st not in COUNTED else ((st in REPLY) if done(day, 5) else (True if prs else None))
                    if rep is not None:
                        add(esc, w, rep)
                        if k in ("D", "E", "F", "G"):
                            add(mil, w, any(data.event_kind[p[2]] == "Kinetic" for p in prs))
                elif s7 is not None:
                    add(esc, w, s7)
                if done(day, 7):
                    add(eco, w, ship(day, 1, 7) > ship(day, -7, -1))
                t14 = talks14(day)
                if t14 is not None:
                    add(pol, w, t14 is False)
            out[k] = dict(people=ppl, escalation=esc, military=mil, economic=eco, political=pol, n=len(cases))
        else:
            mons = [m for m in hold_mondays() if m <= T]
            for m in mons:
                w = weight(scheme, param, T, m)
                s7 = strike7(m)
                if s7 is not None:
                    add(esc, w, s7); add(mil, w, s7)
                flag = HW.PEOPLE_HURT.get(m.isoformat())
                if done(m, 7) and flag is not None:
                    add(ppl, w, bool(flag[0]))
                if done(m, 7):
                    add(eco, w, ship(m, 1, 7) > ship(m, -7, -1))
                t14 = talks14(m)
                if t14 is not None:
                    add(pol, w, t14 is False)
            out[k] = dict(people=ppl, escalation=esc, military=mil, economic=eco, political=pol, n=len(mons))
    return out


def recount_hold(scheme="none", param=None, asof=None):
    """Option A: weeks of the 2026 war with no logged US move of kinds C-H, recounted from data.py.
    Only the hand-set inputs (excluded stretches, uncertain weeks, people-hurt flags) come from hold_weeks.py."""
    import hold_weeks as HW
    us_kinds = ("Sanctions", "Maritime", "Kinetic", "Posture")
    usable = lambda e: e[0] not in data.MERGED and O.N.counts(e[0]) and not e[2].lower().startswith("houthi")
    asof = asof or LAST
    ppl, esc, mil, eco, pol = [0, 0, 0.0, 0.0], [0, 0, 0.0, 0.0], [0, 0, 0.0, 0.0], [0, 0, 0.0, 0.0], [0, 0, 0.0, 0.0]
    n = 0
    for m in hold_mondays():
        n += 1
        w = weight(scheme, param, asof, m)
        struck = within(m, 1, 7, O._irstrike)
        add(esc, w, struck)
        add(mil, w, struck)
        flag = HW.PEOPLE_HURT.get(m.isoformat())
        if flag is not None:
            add(ppl, w, bool(flag[0]))
        bb = sum(1 for e in data.events if O._ship(e) and m - dt.timedelta(days=7) <= e[1] <= m - dt.timedelta(days=1))
        aa = sum(1 for e in data.events if O._ship(e) and m + dt.timedelta(days=1) <= e[1] <= m + dt.timedelta(days=7))
        add(eco, w, aa > bb)
        talks = within(m, 1, 14, O._talks)
        if talks or (LAST - m).days >= 14:
            add(pol, w, not talks)
    return dict(people=ppl, escalation=esc, military=mil, economic=eco, political=pol, n=n)


LOOKBACKS = ("2025-06-22", "2026-04-08", "2026-06-17")      # past dates the page test also checks (look-back, no hindsight)

def run_iran():
    """Recount Iran, write explorer/verify.json, print the numbers. Returns [] (the match against the page is checked by export_explorer and the Node test)."""
    scheme, param = weighting_in_force()
    rc = recount(weighting=(scheme, param), asof=LAST)
    est, pool = estimates(rc)
    for k in rc:
        rc[k]["estimate"] = est[k]
    lbs = {}
    for iso in LOOKBACKS:
        r = recount(weighting=(scheme, param), asof=iso)
        e, pl = estimates(r)
        for k in r:
            r[k]["estimate"] = e[k]
        lbs[iso] = dict(asof=iso, pooled=pl, options=r)
    out = dict(asof=LAST.isoformat(), weighting=dict(scheme=scheme, param=param), m=M, pooled=pool, options=rc, lookbacks=lbs)
    json.dump(out, open(os.path.join(HERE, "..", "explorer", "verify.json"), "w"), indent=1)
    print(f"as of {LAST} | recency weighting: {scheme} {param if param is not None else ''}".rstrip())
    for k, v in rc.items():
        print(k, {c: [v[c][0], v[c][1], round(v[c][2], 4), round(v[c][3], 4)] for c in CATS}, "n", v["n"])
    return []


if __name__ == "__main__":
    # python3 verify_explorer.py [theater ...]   (default: every theater in explorer/theaters.json)
    import importlib, sys, theaters
    problems = []
    for tid in sys.argv[1:] or theaters.registered():
        print(f"\n[{tid}]")
        problems += run_iran() if tid == "iran" else importlib.import_module(f"theaters.{tid}.verify").run()
    sys.exit(1 if problems else 0)
