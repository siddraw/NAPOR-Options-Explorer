"""NAPOR source-gap check: every event must have at least one linked source from an allowed outlet or an
official/primary source. An event without one cannot be classified or counted (link rule, 2026-10-28).

Owner rule (2026-11-02): a missing source is a BUG, found and worked every week, not discovered by accident.
  - Any event with no usable source that is not listed below -> FAIL (find a source, or list it with the search date).
  - Any listed gap whose last search is more than 8 days old -> FAIL (search again this week and update the date).
  - Any listed gap that now has a source -> FAIL (remove it from the list).
Listed gaps stay out of every count (credibility 0) until a credible source is found.

Run:  python3 source_gaps.py        (exit code 0 = PASS, 1 = FAIL)
"""
import datetime as dt
import importlib
import sys

import napor_ids as N

# theater -> {event id: (date last searched, what was searched and why nothing counts)}
KNOWN_GAPS = {
    "iran": {
        67: ("2026-11-09", "IRGC claim of a destroyed radar and F-15 at a US base in Jordan (Jul 21). Only Sputnik (blocked), "
                           "Al Mayadeen and regional sites carry it; AFP covers other Jordan strikes (Jul 16, Jul 22) but not this claim. "
                           "Searched again Nov 9: still only blocked or non-allowed sites (a Jul 18 Jerusalem Post page on other IRGC "
                           "Jordan claims names no F-15 or radar)."),
    },
}
MAX_AGE_DAYS = 8
THEATER_IDS = ["iran", "houthis", "northkorea", "china", "venezuela"]


def theater_events(tid):
    """(event rows, reports_for, credibility) for one theater."""
    if tid == "iran":
        import data
        return [e for e in data.events if e[0] not in data.MERGED], N.reports_for, N.event_credibility
    K = importlib.import_module(f"theaters.{tid}.cases")
    return list(K.EVENTS), K.reports_for, (lambda i: K.CRED[i])


def usable(r):
    return N.report_weight(r) > 0


def scan(today=None):
    today = today or dt.date.today()
    fails, info = [], []
    for tid in THEATER_IDS:
        evs, reps, cred = theater_events(tid)
        gaps = {e[0] for e in evs if not any(usable(r) for r in reps(e[0]))}
        known = KNOWN_GAPS.get(tid, {})
        for i in sorted(gaps - set(known)):
            fails.append(f"{tid} #{i}: no usable source (find an allowed or official source, or list it in KNOWN_GAPS with today's search date)")
        for i, (searched, why) in sorted(known.items()):
            if i not in gaps:
                fails.append(f"{tid} #{i}: now has a usable source; remove it from KNOWN_GAPS")
                continue
            age = (today - dt.date.fromisoformat(searched)).days
            if age > MAX_AGE_DAYS:
                fails.append(f"{tid} #{i}: last searched {searched} ({age} days ago); search again and update the date")
            info.append(f"{tid} #{i}: open gap, last searched {searched}. {why}")
        weak = sorted(e[0] for e in evs if e[0] not in gaps and cred(e[0]) < N.INCLUDE_AT)
        if weak:
            info.append(f"{tid}: {len(weak)} sourced event(s) below the 0.50 cut (left out of counts): {', '.join('#' + str(i) for i in weak[:15])}{' ...' if len(weak) > 15 else ''}")
    return fails, info


if __name__ == "__main__":
    fails, info = scan()
    for line in info:
        print("  [GAP] " + line)
    for line in fails:
        print("  [FAIL] " + line)
    print("Source gaps: " + ("PASS" if not fails else f"FAIL ({len(fails)})"))
    sys.exit(1 if fails else 0)
