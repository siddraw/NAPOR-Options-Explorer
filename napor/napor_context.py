"""NAPOR: things in force on a given date that limit which US options are open.

Used to work out each option's availability on PAST dates (the weekly agent writes the
current week's availability by hand in napor_now.json). Every period starts and ends with a
logged event, so a date only "knows" about a period once its start event has happened.
"""
import data

EV = {e[0]: e for e in data.events}

# (key, label, start event, end event or None, {option: note})
PERIODS = [
    ("cf2025", "Israel-Iran ceasefire", 257, 2,
     {o: "Strikes on Iran itself would break the June 2025 ceasefire (#257); strikes on Iran-backed groups elsewhere stayed possible."
      for o in ("E", "F", "G")}),
    ("cf2026", "2026 ceasefire", 28, 59,
     {o: "Would break the ceasefire in force since Apr 7 (#28)." for o in ("E", "F", "G")}),
    ("pledge", "No-strike pledge before the midterms", 97, None,
     {"F": "Ruled out by Trump's pledge of no attacks on Iran before Nov 3 (#97).",
      "G": "Ruled out by Trump's pledge of no attacks on Iran before Nov 3 (#97).",
      "E": "Trump's pledge covers attacks on Iran before Nov 3 (#97); whether strikes at sea count is not settled."}),
]
PLEDGE_END = "2026-11-03"


def export():
    out = []
    for key, label, a, b, notes in PERIODS:
        out.append(dict(key=key, label=label, start=EV[a][1].isoformat(), start_event=a,
                        end=(EV[b][1].isoformat() if b else (PLEDGE_END if key == "pledge" else None)), end_event=b, notes=notes))
    return out
