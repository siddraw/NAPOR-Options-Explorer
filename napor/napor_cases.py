"""NAPOR: the past cases behind every option, in the shape the page uses.

Shared by export_explorer.py (writes the page data) and backtest_risk.py (scores the page's own
method). verify_explorer.py deliberately does NOT import this: it recounts everything on its own.

Per-option flags (the page reads these instead of hard-coding option letters):
  trigger    - escalation = "Iran or an Iran-backed group replied within ~5 days" (Trigger Census);
               otherwise escalation = "struck within 7 days" (timing only)
  military   - "reply":  the reply was a kinetic strike (D-G)
               "strike": a kinetic strike by Iran or an Iran-backed group within 7 days (A, hold weeks)
               "none":   no direct military cost expected from the move itself (counts as 0%)
  us_move    - a US move of kinds C-H (used to decide whether "Hold" was the course on a date)
  is_hold    - option A: cases are weeks with no logged US move, not acts
  salvo      - show the interceptor estimate (reply rate x interceptors per salvo)
"""
import datetime as dt
import data
import napor_options as O
import napor_ids as N
import napor_threads as T
import napor_intensity as INT
import hold_weeks

EV = O.EV
LAST = max(e[1] for e in data.events)
TRIG = ("C", "D", "E", "F", "G")

FLAGS = {
    "A": dict(trigger=False, military="strike", us_move=False, is_hold=True, salvo=False),
    "B": dict(trigger=False, military="none", us_move=False, is_hold=False, salvo=False),
    "C": dict(trigger=True, military="none", us_move=True, is_hold=False, salvo=False),
    "D": dict(trigger=True, military="reply", us_move=True, is_hold=False, salvo=True),
    "E": dict(trigger=True, military="reply", us_move=True, is_hold=False, salvo=True),
    "F": dict(trigger=True, military="reply", us_move=True, is_hold=False, salvo=True),
    "G": dict(trigger=True, military="reply", us_move=True, is_hold=False, salvo=True),
    "H": dict(trigger=False, military="none", us_move=True, is_hold=False, salvo=False),
}

REPLY = ("R-strong", "R-weak", "R-proxy")
COUNTED = REPLY + ("N",)


def ev(i):
    e = EV[i]
    return dict(id=i, date=e[1].isoformat(), actor=e[2], kind=e[3], title=e[5], cred=round(N.event_credibility(i), 2))


def _brief(ids):
    return [dict(id=j, date=EV[j][1].isoformat(), title=EV[j][5], actor=EV[j][2], dmg=EV[j][7] or "") for j in ids]


def option_cases(key, last=LAST):
    o = [x for x in O.OPTIONS if x["key"] == key][0]
    cases = []
    if FLAGS[key]["is_hold"]:
        cases = hold_weeks.cases(last)
    elif o["match"]:
        for c in [c for c in O.census if O.us_side(c[0]) and o["match"](c[0])]:
            prs = [p for p in O.pairs if p[1] == c[0]]
            counted = c[2] in COUNTED
            cases.append(dict(**ev(c[0]), cls=c[2], replied=(c[2] != "N") if counted else None,
                              replies=[dict(id=p[2], days=(EV[p[2]][1] - EV[p[1]][1]).days, hurt=p[4] == "Y", kinetic=data.event_kind[p[2]] == "Kinetic",
                                            title=EV[p[2]][5], actor=EV[p[2]][2], date=EV[p[2]][1].isoformat(), dmg=EV[p[2]][7] or "") for p in prs],
                              note=c[3], civ=O.CIVILIAN_HARM.get(c[0])))
    else:
        for i in O.option_cases(key):
            cases.append(dict(**ev(i), cls=None, replied=None, replies=[], civ=None, note=None))
    for c in cases:
        if not c.get("week"):
            day = EV[c["id"]][1]
            full7 = (last - day).days >= 7
            c["strike7"] = bool(O._window(O._irstrike, day, 1, 7)) if full7 else None
            # Talks: yes as soon as one is logged; "no" only once the full 14 days have passed (otherwise still open).
            talks = bool(O._window(O._talks, day, 1, 14))
            c["talks14"] = True if talks else (False if (last - day).days >= 14 else None)
            c["dmg"] = EV[c["id"]][7] or ""
            c["strike_ev"] = _brief(O._window(O._irstrike, day, 1, 7))
            c["talk_ev"] = _brief(O._window(O._talks, day, 1, 14))
            c["ship_b_ev"] = _brief(O._window(O._ship, day, -7, -1))
            c["ship_a_ev"] = _brief(O._window(O._ship, day, 1, 7))
            c["ship_b"] = len(O._window(O._ship, day, -7, -1))
            c["ship_a"] = len(O._window(O._ship, day, 1, 7)) if full7 else None
            c["civ"] = c["civ"] if c["id"] in O.CIVILIAN_HARM else None
            c["phase"] = T.event_phase[c["id"]]
        else:
            day = dt.date.fromisoformat(c["date"])
            c["phase"] = T.phase_of(day)
        c["pts_at"] = INT.intensity_before(day)
        c["band_at"] = INT.band(c["pts_at"])
    cases.sort(key=lambda x: x["date"])
    return cases


# ---- the five risk categories, one definition shared by the export and the backtest ----
CATS = ["people", "escalation", "military", "economic", "political"]
WINDOW = {"people": 7, "economic": 7, "political": 14}   # days until a category's outcome is final


def window_days(flags, cat):
    if cat == "escalation":
        return 5 if flags["trigger"] else 7
    if cat == "military":
        return 5 if flags["military"] == "reply" else 7
    return WINDOW[cat]


def outcome(flags, c, cat):
    """(counted?, risk?) for one case and category - the same rule the page applies."""
    if cat == "people":
        if c["strike7"] is None or (c.get("week") and c.get("hurt7") is None):
            return False, None
        return True, bool(c["civ"]) or any(r["hurt"] for r in c["replies"]) or c.get("hurt7") is True
    if cat == "escalation":
        if flags["trigger"]:
            return (c["replied"] is not None), c["replied"] is True
        return (c["strike7"] is not None), c["strike7"] is True
    if cat == "military":
        if flags["military"] == "reply":
            return (c["replied"] is not None), any(r["kinetic"] for r in c["replies"])
        if flags["military"] == "strike":
            return (c["strike7"] is not None), c.get("mil7") is True
        return False, None
    if cat == "economic":
        return (c["ship_a"] is not None), (c["ship_a"] is not None and c["ship_a"] > c["ship_b"])
    if cat == "political":
        return (c["talks14"] is not None), c["talks14"] is False
    raise KeyError(cat)


def category_scores(flags, cases):
    sc = {}
    for cat in CATS:
        if cat == "military" and flags["military"] == "none":
            sc[cat] = dict(k=0, n=0, assumed=True)
            continue
        got = [outcome(flags, c, cat) for c in cases]
        sc[cat] = dict(k=sum(1 for b, f in got if b and f), n=sum(1 for b, _ in got if b))
    return sc
