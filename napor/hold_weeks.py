"""NAPOR: past cases for option A ("Hold: no new action").

A hold case is a week of the 2026 war in which the US logged NO move of kinds C-H (sanctions,
naval pressure, strikes, posture changes). Each case starts on a Monday; the week M..M+7 must be free
of logged US C-H moves, so nothing the US did can explain what followed in the 7-day window.
The five outcomes are then measured exactly as for the other options, counted from the Monday:
  escalation - Iran or an Iran-backed group struck (kinetic) within 7 days
  people     - a hostile act in those 7 days hurt anyone (set BY HAND below from the logged damage text)
  military   - an Iranian/proxy kinetic strike in those 7 days (same test as "the reply was kinetic"
               for D-G, which does not check the weapon either)
  economic   - attacks on shipping in the 7 days after > the 7 days before
  political  - no talks (a meeting, proposal, ceasefire or deal; not statements or threats) within 14 days

Left out on purpose:
  - Feb 28 - Apr 7 (daily open war) and Jul 7 - Jul 25 (nightly US campaign logged as one row): US
    activity was continuous but under-logged, so a "quiet" week there is a logging gap, not a hold.
  - Pre-war weeks: pre-war logging is too sparse to tell a hold from a gap.
  - UNCERTAIN weeks below: an allowed outlet reports a US move that is not in the log.
Caveat shown on the page: most hold weeks have few or no logged events at all, so they show what the
LOG records in quiet weeks; an unlogged event would change them.

Weekly agent: when a new hold week appears, `missing_flags()` lists it. Read the damage text of the
listed events and add an entry to PEOPLE_HURT (True/False, evidence event IDs, one-line note). Until
then the week counts everywhere except "people hurt" (shown as "not counted yet").
"""
import datetime as dt
import data
import napor_options as O

START = dt.date(2026, 2, 28)
EXCLUDED = [(dt.date(2026, 2, 28), dt.date(2026, 4, 7), "daily open war (US strikes continuous, logged as a few rows)"),
            (dt.date(2026, 7, 7), dt.date(2026, 7, 25), "nightly US campaign logged as one row")]
UNCERTAIN = {
    "2026-08-17": "AP (Aug 21) reports Trump warning of an 'economic D-Day' against Iran, with sweeping new sanctions expected that week; "
                  "they are not in the log, so this week may not be a true hold "
                  "(https://www.nashuatelegraph.com/news/local-news/2026/08/21/trump-warns-of-economic-d-day-against-iran-but-tehran-is-well-acquainted-with-sanctions/).",
}

# Set by hand from the logged damage text of every hostile act in the 7 days after the Monday.
# monday: (anyone hurt?, evidence event IDs, note)
PEOPLE_HURT = {
    "2026-04-20": (False, [38], "IRGC seized two container ships (#38): no casualties (AFP, Reuters)."),
    "2026-05-11": (False, [], "No hostile act logged."),
    "2026-05-18": (False, [], "No hostile act logged."),
    "2026-05-25": (False, [], "No hostile act logged."),
    "2026-06-01": (False, [116], "Iran and Israel traded fire Jun 6-7 (#116): no casualty figures in the source read."),
    "2026-06-29": (False, [], "No hostile act logged."),
    "2026-07-27": (False, [], "No hostile act logged."),
    "2026-08-03": (False, [], "No hostile act logged."),
    "2026-08-10": (False, [], "No hostile act logged."),
    "2026-09-14": (False, [], "No hostile act logged."),
    "2026-09-21": (False, [84], "Projectiles hit at least 3 commercial ships (#84): no casualties reported."),
}

US_MOVE_KINDS = ("Sanctions", "Maritime", "Kinetic", "Posture")   # options C-H


def us_move(e):
    """A logged move by the US itself (not Israel alone) of kinds C-H."""
    return e[2].lower().startswith("us") and O._usable(e) and data.event_kind[e[0]] in US_MOVE_KINDS


def hostile(e):
    """A hostile act by Iran, an Iran-backed group or an unidentified attacker (not the US/Israel, not the Houthis)."""
    return O._usable(e) and not O.us_side(e[0]) and data.event_kind[e[0]] in ("Kinetic", "Maritime")


def _days(m, a, b):
    return m + dt.timedelta(days=a), m + dt.timedelta(days=b)


def weeks(last=None):
    """Every Monday from the war start to 7 days before the latest news, with its verdict."""
    last = last or max(e[1] for e in data.events)
    m = START + dt.timedelta(days=(7 - START.weekday()) % 7)
    out = []
    while m <= last - dt.timedelta(days=7):
        a, b = _days(m, 0, 7)
        why = None
        for x, y, reason in EXCLUDED:
            if not (b < x or a > y):
                why = "excluded: " + reason
        moves = [e[0] for e in data.events if a <= e[1] <= b and us_move(e)]
        if not why and moves:
            why = "US move logged: " + ", ".join(f"#{i}" for i in moves)
        if not why and m.isoformat() in UNCERTAIN:
            why = "uncertain: " + UNCERTAIN[m.isoformat()]
        logged = [e[0] for e in data.events if a <= e[1] <= b and e[0] not in data.MERGED]
        out.append(dict(monday=m, hold=why is None, why=why, logged=logged))
        m += dt.timedelta(days=7)
    return out


def hold_mondays(last=None):
    return [w["monday"] for w in weeks(last) if w["hold"]]


def missing_flags(last=None):
    return [m.isoformat() for m in hold_mondays(last) if m.isoformat() not in PEOPLE_HURT]


def cases(last=None):
    """Hold cases in the same shape the page uses for every other option's cases."""
    last = last or max(e[1] for e in data.events)
    EV = O.EV
    brief = lambda ids: [dict(id=j, date=EV[j][1].isoformat(), title=EV[j][5], actor=EV[j][2], dmg=EV[j][7] or "") for j in ids]
    out = []
    for w in weeks(last):
        if not w["hold"]:
            continue
        m = w["monday"]; iso = m.isoformat()
        st = O._window(O._irstrike, m, 1, 7)
        talks = O._window(O._talks, m, 1, 14)
        hos = [e[0] for e in data.events if hostile(e) and m + dt.timedelta(days=1) <= e[1] <= m + dt.timedelta(days=7)]
        flag = PEOPLE_HURT.get(iso)
        out.append(dict(
            id="W" + iso, week=True, date=iso, actor="US (no new move)", kind="Hold", cred=None,
            title=f"Week of {m.strftime('%b')} {m.day}: no new US sanctions, naval, strike or posture move logged ({len(w['logged'])} event{'' if len(w['logged']) == 1 else 's'} logged that week)",
            cls=None, replied=None, replies=[], note=None, civ=None,
            strike7=bool(st), mil7=bool(st),
            hurt7=(flag[0] if flag else None), hurt_ev=brief(flag[1]) if flag else brief(hos), hurt_note=(flag[2] if flag else "Not set by hand yet."),
            talks14=True if talks else (False if (last - m).days >= 14 else None),
            dmg="", strike_ev=brief(st), talk_ev=brief(talks),
            ship_b_ev=brief(O._window(O._ship, m, -7, -1)), ship_a_ev=brief(O._window(O._ship, m, 1, 7)),
            ship_b=len(O._window(O._ship, m, -7, -1)), ship_a=len(O._window(O._ship, m, 1, 7)),
            logged=len(w["logged"])))
    return out


if __name__ == "__main__":
    for w in weeks():
        print(w["monday"], "HOLD" if w["hold"] else "    ", (w["why"] or "")[:110], "| logged:", len(w["logged"]))
    cs = cases()
    print(f"\n{len(cs)} hold weeks. Missing people-hurt flags: {missing_flags() or 'none'}")
    for c in cs:
        print(c["date"], "strike7", c["strike7"], "hurt", c["hurt7"], "ship", c["ship_b"], "->", c["ship_a"], "talks14", c["talks14"])
