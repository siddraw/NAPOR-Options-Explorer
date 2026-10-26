"""Venezuela / Caribbean: the research file (events.py, read only) seen through this tab's escalation rule.

The research file marks a Venezuelan statement as a reply (census R-weak) when it answers a US move within days. This tab's rule is
stricter: only a HOSTILE ACT counts as an escalation reply (an attack, harassment of US assets, or a military mobilization announced
within 7 days of the move; words alone, a diplomatic step and an economic step do not; economic steps are measured in their own corner).
So this view of the file changes the census and the pairs and nothing else:
  CENSUS  a row the file marks R-strong or R-weak is kept only if a counted hostile act by Venezuela or an armed group is logged 0-7 days
          after the move; otherwise it becomes "N" and the note says what the file had. Rows marked N or Unclear stay as they are.
  PAIRS   only trigger -> reply links whose reply is a hostile act are kept (statements are not replies here), plus one derived link for
          each kept census row that the file did not pair (ids 4901 and up), so the case pop-up lists the act that made it count.
  CENSUS  also: a row still marked N whose 7-day window has not closed at the last logged event becomes "Unclear" (not counted yet).
Nothing is added to or removed from EVENTS, SOURCES, US_OPTION, WINDOWS, START_ACTS or PHASES. cases.py and verify.py both read this
view, so the page numbers and the independent recount use the same rows."""
import datetime as dt

import napor_ids as N
from theaters.venezuela import events as E
from theaters.venezuela import acts
from theaters.venezuela import config as C

EVENTS, SOURCES, VERDICT, US_OPTION = E.EVENTS, E.SOURCES, E.VERDICT, E.US_OPTION
PARTLY, WINDOWS, START_ACTS, PHASES = E.PARTLY, E.WINDOWS, E.START_ACTS, E.PHASES
CHAIN_NAMES, CRED_ESTIMATE = E.CHAIN_NAMES, E.CRED_ESTIMATE

_EV = {e[0]: e for e in EVENTS}


def _cred(eid):
    reps = [dict(outlet=N.outlet_name(s["outlet"]), kind=N.source_kind(s["outlet"], C.CLAIM_MEDIA, C.CLAIM_LABEL), seen=s.get("seen", "")) for s in SOURCES.get(eid, [])]
    chk = "Not supported" if VERDICT.get(eid) == "not_confirmed" else ("Partly verified" if eid in PARTLY else "Verified")
    return N.credibility_of(reps, chk)


def _hostile_after(eid):
    """Counted hostile acts by Venezuela or an armed group logged 0-7 days after the move."""
    day = _EV[eid][1]
    return [e[0] for e in EVENTS if acts.adversary_side(e[2]) and acts.is_hostile(e[3]) and _cred(e[0]) >= N.INCLUDE_AT
            and dt.timedelta(0) <= e[1] - day <= dt.timedelta(days=7)]


_REPLY = ("R-strong", "R-weak", "R-proxy")
CENSUS, _kept = [], {}
for _c in E.CENSUS:
    _h = _hostile_after(_c[0]) if _c[2] in _REPLY else []
    if _c[2] in _REPLY and not _h:
        CENSUS.append((_c[0], _c[1], "N", f"Not counted as an escalation reply here: no attack, harassment or mobilization within 7 days (the research file marks it {_c[2]}; words or a non-hostile step). {_c[3]}"))
    else:
        CENSUS.append(_c)
        if _c[2] in _REPLY:
            _kept[_c[0]] = _h

# A move with fewer than 7 days of news after it has no finished reply window yet: it is listed in the census as "Unclear" (not counted) until the
# window closes, as the page and the independent recount do. (The shared case builder would otherwise count it as "no reply" at once.)
_LAST = max(e[1] for e in EVENTS)
CENSUS = [(c[0], c[1], "Unclear", "Window still open: fewer than 7 days of news after this move, so it is not counted yet. " + c[3])
          if c[2] == "N" and (_LAST - _EV[c[0]][1]).days < 7 else c for c in CENSUS]

PAIRS = [p for p in E.PAIRS if acts.is_hostile(_EV[p[2]][3]) and acts.adversary_side(_EV[p[2]][2])]
_paired = {p[1] for p in PAIRS}
_n = 4900
for _tid, _hs in sorted(_kept.items()):
    if _tid not in _paired:
        for _r in _hs:
            _n += 1
            PAIRS.append((_n, _tid, _r, "Military/Property", "N", "Linked by this tab's rule: a hostile act within 7 days of the move (see the census note)"))
