"""NAPOR: war-intensity scale.

How hot was the war in the 14 days BEFORE a given day? Uses only events that had already
happened, so it can be used in real time (unlike the phase labels, which were drawn with
hindsight).

Points in the 14-day window:
  2 points  for each direct strike between the US/Israel and Iran (either direction)
  1 point   for each attack on shipping, seizure or blockade move
  +2 points for each of those events that killed someone
Bands (points in 14 days):  0 Quiet | 1-5 Low | 6-11 Medium | 12+ High
Proxy fronts (Houthi strikes on Saudi Arabia) are left out.

Caveat: this counts LOGGED events. Big campaigns (the opening war, the July nightly strikes)
are logged as one or a few rows each, so the score understates how intense those weeks were.
"""
import datetime as dt
from collections import OrderedDict
import data
import napor_ids as N

WINDOW_DAYS = 14
BANDS = [(0, "Quiet"), (1, "Low"), (6, "Medium"), (12, "High")]


def _hostile(e):
    eid = e[0]
    if eid in data.MERGED or not N.counts(eid):
        return False
    if e[2].lower().startswith("houthi"):
        return False
    return data.event_kind[eid] in ("Kinetic", "Maritime")


def _deadly(e):
    s = (e[7] or "").lower()
    return any(w in s for w in ("killed", "dead", "deaths", "kia", "killed in action")) and "no deaths" not in s and "no casualties" not in s


def points_for(e):
    p = 2 if data.event_kind[e[0]] == "Kinetic" else 1
    if _deadly(e):
        p += 2
    return p


HOSTILE = [e for e in data.events if _hostile(e)]


def intensity_before(day, window=WINDOW_DAYS):
    """Points from hostile events in the `window` days before `day` (not counting `day` itself)."""
    start = day - dt.timedelta(days=window)
    return sum(points_for(e) for e in HOSTILE if start <= e[1] < day)


def band(points):
    name = BANDS[0][1]
    for lo, nm in BANDS:
        if points >= lo:
            name = nm
    return name


def weekly_table():
    """Monday-to-Sunday weeks: points scored inside each week, and the band of the 14 days up to its end."""
    first = min(e[1] for e in data.events)
    last = max(e[1] for e in data.events)
    wk = first - dt.timedelta(days=first.weekday())
    rows = []
    while wk <= last:
        end = wk + dt.timedelta(days=6)
        inside = [e for e in HOSTILE if wk <= e[1] <= end]
        pts = sum(points_for(e) for e in inside)
        rows.append(dict(week_start=wk, week_end=end, events=len(inside), points=pts,
                         kinetic=sum(1 for e in inside if data.event_kind[e[0]] == "Kinetic"),
                         shipping=sum(1 for e in inside if data.event_kind[e[0]] == "Maritime"),
                         deadly=sum(1 for e in inside if _deadly(e)),
                         band_14d=band(intensity_before(end + dt.timedelta(days=1)))))
        wk += dt.timedelta(days=7)
    return rows


event_intensity = {e[0]: intensity_before(e[1]) for e in data.events}


if __name__ == "__main__":
    for r in weekly_table():
        print(r["week_start"], r["points"], r["kinetic"], r["shipping"], r["deadly"], r["band_14d"])
    today = max(e[1] for e in data.events) + dt.timedelta(days=1)
    print("Now:", intensity_before(today), band(intensity_before(today)))
