"""Houthis / Red Sea: the event table and the past cases behind every option, in the shape the page uses.

Built from the read-only research files (events_early.py, events_late.py) and config.py. Everything here is a
function of those inputs, so a fix to the research files flows through on the next run. This module is the model
for new theaters: same names, same shapes as napor_cases.py / napor_options.py / hold_weeks.py, but no Iran state.

Rules copied from the Iran engine (so the numbers mean the same thing):
  - an event counts only with credibility >= 0.50 (napor_ids.credibility_of: full-text allowed outlet 0.80, two outlets
    0.96, claim-only outlet 0.30; "Partly verified" x 0.8; a row marked not_confirmed is capped at 0.20)
  - option C-G cases are the Trigger Census rows with a counted status (R-strong, R-weak, R-proxy, N) of that option
  - B and H cases are every counted US move with that letter; A cases are hold weeks
  - the outcome windows are the same: reply ~5 days, attack 7 days, shipping attacks 7 days before/after, talks 14 days
"""
import datetime as dt
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
import data                      # only for act_kind(), the shared word list that sorts an action type into a kind
import napor_ids as N
import napor_intensity as INT    # only for the shared bands and the "someone died" test
from theaters.houthis import events_early as E, events_late as L
from theaters.houthis import config as C

REPLY = ("R-strong", "R-weak", "R-proxy")
COUNTED = REPLY + ("N",)

# ---- the raw tables, early and late files joined -----------------------------------------------------------
EVENTS = sorted(E.EVENTS + L.EVENTS, key=lambda e: (e[1], e[0]))
EV = {e[0]: e for e in EVENTS}
SOURCES = {**E.SOURCES, **L.SOURCES}
VERDICT = {**E.VERDICT, **L.VERDICT}
PARTLY = set(E.PARTLY) | set(L.PARTLY)
US_OPTION = {**E.US_OPTION, **L.US_OPTION}
CENSUS_RAW = list(E.CENSUS) + list(L.CENSUS)
PAIRS_RAW = list(E.PAIRS) + list(L.PAIRS)
WINDOWS = list(E.WINDOWS) + list(L.WINDOWS)
START_ACTS = set(E.START_ACTS) | set(L.START_ACTS)
PHASES = sorted(list(E.PHASES) + list(L.PHASES), key=lambda p: p[1])
CHAIN_NAMES = {**E.CHAIN_NAMES, **L.CHAIN_NAMES}
CONSTRAINTS = list(getattr(L, "CONSTRAINTS", None) or []) + list(getattr(E, "CONSTRAINTS", None) or [])
LAST = max(e[1] for e in EVENTS)
FIRST = min(e[1] for e in EVENTS)
FLAGS = C.FLAGS
CATS = ["people", "escalation", "military", "economic", "political"]

KIND = {e[0]: C.KIND_OVERRIDE.get(e[0], data.act_kind(e[3], e[5])) for e in EVENTS}


# ---- credibility ---------------------------------------------------------------------------------------------
def reports_for(eid):
    out = []
    for s in SOURCES.get(eid, []):
        out.append(dict(event_id=eid, outlet_raw=s["outlet"], outlet=N.outlet_name(s["outlet"]),
                        kind=N.source_kind(s["outlet"], C.CLAIM_MEDIA, C.CLAIM_LABEL),
                        headline=s.get("headline", ""), published=s.get("published", ""), url=s.get("url", ""), seen=s.get("seen", "")))
    return out


def check_of(eid):
    if VERDICT.get(eid) == "not_confirmed":
        return "Not supported"
    return "Partly verified" if eid in PARTLY else "Verified"


CRED = {e[0]: N.credibility_of(reports_for(e[0]), check_of(e[0])) for e in EVENTS}


def counts(eid):
    return CRED.get(eid, 0) >= N.INCLUDE_AT


census = [c for c in CENSUS_RAW if counts(c[0])]
pairs = [p for p in PAIRS_RAW if counts(p[1]) and counts(p[2])]
dropped = dict(census=[c[0] for c in CENSUS_RAW if not counts(c[0])], pairs=[p[0] for p in PAIRS_RAW if p not in pairs])

# ---- who is who and what counts -------------------------------------------------------------------------------
usable = lambda e: counts(e[0])
us_side = lambda tid: C.us_side(EV[tid][2])
phase_names = [p[0] for p in PHASES]


def phase_of(day):
    for name, a, b, _ in PHASES:
        if a <= day <= b:
            return name
    return "Before the record starts"


def _window(f, day, a, b):
    return [e[0] for e in EVENTS if f(e) and day + dt.timedelta(days=a) <= e[1] <= day + dt.timedelta(days=b)]


def _attack(e):
    """A hostile act by the Houthis: a strike or an attack/seizure at sea (a threat or a declaration is not one)."""
    return usable(e) and C.adversary_side(e[2]) and KIND[e[0]] in C.ATTACK_KINDS


def _ship(e):
    """An attack on shipping by the Houthis (Houthi actors only)."""
    return usable(e) and C.adversary_side(e[2]) and KIND[e[0]] == "Maritime"


def _talks(e):
    """Same rule as the live Iran rule: any diplomatic event (any side, statements included)."""
    return usable(e) and KIND[e[0]] == "Diplomatic"


# ---- chains (back-and-forth) ----------------------------------------------------------------------------------
def _chains():
    links = set()
    for e in EVENTS:
        if e[6] and e[6] in EV and counts(e[0]) and counts(e[6]):
            links.add((e[6], e[0]))
    for p in pairs:
        links.add((p[1], p[2]))
    par = {}
    def find(x):
        par.setdefault(x, x)
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    for a, b in links:
        par[find(a)] = find(b)
    groups = {}
    for a, b in links:
        groups.setdefault(find(a), set()).update({a, b})
    return sorted((sorted(g, key=lambda i: (EV[i][1], i)) for g in groups.values()), key=lambda ids: (EV[ids[0]][1], ids[0]))


def _side(i):
    a = EV[i][2]
    return "Houthis" if C.adversary_side(a) else "US" if C.us_side(a) else None


THREADS = []
for _n, _ids in enumerate(_chains(), start=1):
    _sides = [_side(i) for i in _ids if _side(i)]
    THREADS.append(dict(thread_id=f"H{_n:02d}", name=CHAIN_NAMES.get(_ids[0], "Unnamed chain"), events=_ids, start=EV[_ids[0]][1], end=EV[_ids[-1]][1],
                        days=(EV[_ids[-1]][1] - EV[_ids[0]][1]).days, n=len(_ids), rounds=sum(1 for x, y in zip(_sides, _sides[1:]) if x != y),
                        hostile_acts=sum(1 for i in _ids if KIND[i] in ("Kinetic", "Maritime"))))


def chain_stats():
    mil = [t for t in THREADS if t["hostile_acts"] >= 1]
    if not mil:
        return {}
    r = [t["rounds"] for t in mil]
    return dict(chains=len(mil), max_rounds=max(r), share_stopped_after_one_reply=round(sum(1 for x in r if x <= 1) / len(r), 2))


# ---- war intensity (same points and bands as the Iran page; every logged US strike and Houthi attack) -------------
HOSTILE = [e for e in EVENTS if usable(e) and KIND[e[0]] in ("Kinetic", "Maritime")]


def points_for(e):
    return (2 if KIND[e[0]] == "Kinetic" else 1) + (2 if INT._deadly(e) else 0)


def intensity_before(day, window=INT.WINDOW_DAYS):
    start = day - dt.timedelta(days=window)
    return sum(points_for(e) for e in HOSTILE if start <= e[1] < day)


def baseline_hold():
    """Houthi attacks on shipping per week in the current phase (what happens with no new US move)."""
    start = [p for p in PHASES if p[0] == phase_of(LAST)][-1][1]
    acts = [e for e in EVENTS if e[1] >= start and _ship(e)]
    weeks = max(1, ((LAST - start).days + 1) / 7)
    return dict(n=len(acts), weeks=round(weeks, 1), per_week=round(len(acts) / weeks, 1), ids=[e[0] for e in acts])


# ---- hold weeks (option A) --------------------------------------------------------------------------------------
def _in_window(day):
    return any(a <= day <= b for a, b in WINDOWS)


def is_us_move(e):
    """A logged move by the US itself of kinds C-H (by its option letter, or by its kind of act)."""
    if not (usable(e) and C.us_side(e[2])):
        return False
    return US_OPTION.get(e[0], "B") in "CDEFGH" or KIND[e[0]] in C.US_MOVE_KINDS


def weeks(last=None):
    """Every Monday from HOLD_START to 7 days before the latest news, with its verdict."""
    last = last or LAST
    m = C.HOLD_START
    out = []
    while m <= last - dt.timedelta(days=7):
        a, b = m, m + dt.timedelta(days=7)
        why = None
        for x, y in WINDOWS:
            if not (b < x or a > y):
                why = f"excluded: continuous fighting {x.isoformat()} to {y.isoformat()}"
        moves = [e[0] for e in EVENTS if a <= e[1] <= b and is_us_move(e)]
        if not why and moves:
            why = "US move logged: " + ", ".join(f"#{i}" for i in moves)
        if not why and m.isoformat() in C.UNCERTAIN:
            why = "uncertain: " + C.UNCERTAIN[m.isoformat()]
        out.append(dict(monday=m, hold=why is None, why=why, logged=[e[0] for e in EVENTS if a <= e[1] <= b]))
        m += dt.timedelta(days=7)
    return out


def hold_mondays(last=None):
    return [w["monday"] for w in weeks(last) if w["hold"]]


def hold_hurt_candidates(last=None):
    """For each hold week: the Houthi attacks in the 7 days after, with their logged damage text (to set PEOPLE_HURT by hand)."""
    out = {}
    for m in hold_mondays(last):
        out[m.isoformat()] = [(i, EV[i][5][:60], EV[i][7]) for i in _window(_attack, m, 1, 7)]
    return out


def missing_flags(last=None):
    return [m.isoformat() for m in hold_mondays(last) if m.isoformat() not in C.PEOPLE_HURT and _window(_attack, m, 1, 7)]


# ---- cases ------------------------------------------------------------------------------------------------------
def ev(i):
    e = EV[i]
    return dict(id=i, date=e[1].isoformat(), actor=e[2], kind=e[3], title=e[5], cred=round(CRED[i], 2))


def _brief(ids):
    return [dict(id=j, date=EV[j][1].isoformat(), title=EV[j][5], actor=EV[j][2], dmg=EV[j][7] or "") for j in ids]


def hold_cases(last):
    out = []
    for w in weeks(last):
        if not w["hold"]:
            continue
        m = w["monday"]; iso = m.isoformat()
        st = _window(_attack, m, 1, 7)
        talks = _window(_talks, m, 1, 14)
        flag = C.PEOPLE_HURT.get(iso) or ((False, [], "No hostile act logged.") if not st else None)
        out.append(dict(
            id="W" + iso, week=True, date=iso, actor="US (no new move)", kind="Hold", cred=None,
            title=f"Week of {m.strftime('%b')} {m.day}: no new US sanctions, naval, strike or posture move logged ({len(w['logged'])} event{'' if len(w['logged']) == 1 else 's'} logged that week)",
            cls=None, replied=None, replies=[], note=None, civ=None,
            strike7=bool(st), mil7=bool(st),
            hurt7=(flag[0] if flag else None), hurt_ev=_brief(flag[1]) if flag else _brief(st), hurt_note=(flag[2] if flag else "Not set by hand yet."),
            talks14=True if talks else (False if (last - m).days >= 14 else None),
            dmg="", strike_ev=_brief(st), talk_ev=_brief(talks),
            ship_b_ev=_brief(_window(_ship, m, -7, -1)), ship_a_ev=_brief(_window(_ship, m, 1, 7)),
            ship_b=len(_window(_ship, m, -7, -1)), ship_a=len(_window(_ship, m, 1, 7)),
            logged=len(w["logged"])))
    return out


def option_ids(key):
    """Counted US moves with this option letter (B and H: all of them; C-G: only those that are Trigger Census cases, below)."""
    return [i for i, k in sorted(US_OPTION.items(), key=lambda kv: (EV[kv[0]][1], kv[0])) if k == key and counts(i) and us_side(i)]


def option_cases(key, last=LAST):
    cases = []
    if FLAGS[key]["is_hold"]:
        cases = hold_cases(last)
        if len(cases) < C.MIN_HOLD_WEEKS:
            cases = []                         # too few weeks: show "too few cases", do not invent weeks
    elif FLAGS[key]["trigger"]:
        for c in [c for c in census if us_side(c[0]) and US_OPTION.get(c[0]) == key]:
            prs = [p for p in pairs if p[1] == c[0]]
            counted = c[2] in COUNTED
            cases.append(dict(**ev(c[0]), cls=c[2], replied=(c[2] != "N") if counted else None,
                              replies=[dict(id=p[2], days=(EV[p[2]][1] - EV[p[1]][1]).days, hurt=p[4] == "Y", kinetic=KIND[p[2]] == "Kinetic",
                                            title=EV[p[2]][5], actor=EV[p[2]][2], date=EV[p[2]][1].isoformat(), dmg=EV[p[2]][7] or "") for p in prs],
                              note=c[3], civ=C.CIVILIAN_HARM.get(c[0])))
        cases = [c for c in cases if c["cls"] in COUNTED]      # unclear / unverified rows are listed in the census, not counted
    else:
        for i in option_ids(key):
            if (last - EV[i][1]).days >= 7:
                cases.append(dict(**ev(i), cls=None, replied=None, replies=[], civ=None, note=None))
    for c in cases:
        if not c.get("week"):
            day = EV[c["id"]][1]
            full7 = (last - day).days >= 7
            c["strike7"] = bool(_window(_attack, day, 1, 7)) if full7 else None
            talks = bool(_window(_talks, day, 1, 14))
            c["talks14"] = True if talks else (False if (last - day).days >= 14 else None)
            c["dmg"] = EV[c["id"]][7] or ""
            c["strike_ev"] = _brief(_window(_attack, day, 1, 7))
            c["talk_ev"] = _brief(_window(_talks, day, 1, 14))
            c["ship_b_ev"] = _brief(_window(_ship, day, -7, -1))
            c["ship_a_ev"] = _brief(_window(_ship, day, 1, 7))
            c["ship_b"] = len(c["ship_b_ev"])
            c["ship_a"] = len(c["ship_a_ev"]) if full7 else None
            c["civ"] = c["civ"] if c["id"] in C.CIVILIAN_HARM else None
            c["phase"] = phase_of(day)
        else:
            day = dt.date.fromisoformat(c["date"])
            c["phase"] = phase_of(day)
        c["pts_at"] = intensity_before(day)
        c["band_at"] = INT.band(c["pts_at"])
    cases.sort(key=lambda x: x["date"])
    return cases


def all_cases(last=LAST):
    return {o["key"]: option_cases(o["key"], last) for o in C.OPTIONS}


def uses():
    """Every counted US move of each kind, including those inside long fights (for "what did the US do next" on past dates)."""
    out = {o["key"]: [] for o in C.OPTIONS}
    for e in EVENTS:
        k = US_OPTION.get(e[0])
        if k in out and counts(e[0]) and us_side(e[0]):
            out[k].append(dict(id=e[0], date=e[1].isoformat(), title=e[5], unsorted=False))
    return out


# ---- measured signals and the plain-language risk lines (the page's "What the log says") ------------------------------
def wilson(k, n, z=1.96):
    if not n:
        return None
    p = k / n; den = 1 + z * z / n; c = (p + z * z / (2 * n)) / den
    h = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / den
    return max(0.0, c - h), min(1.0, c + h)


def option_rows(cases_by_key):
    """The same per-option numbers as napor_options.option_rows(), as strings."""
    chain = chain_stats()
    longer = 1 - chain["share_stopped_after_one_reply"] if chain else None
    rows = {}
    for o in C.OPTIONS:
        k = o["key"]; fl = FLAGS[k]; cs = cases_by_key[k]
        row = dict(key=k, n=len(cs))
        if fl["trigger"]:
            counted = [c for c in cs if c["replied"] is not None]
            kk, n = sum(1 for c in counted if c["replied"]), len(counted)
            ci = wilson(kk, n)
            row["reply"] = f"{kk} of {n} ({kk / n:.0%})" if n else "No past cases"
            row["reply_range"] = f"{ci[0]:.0%}-{ci[1]:.0%}" if ci else ""
            reps = [r for c in cs for r in c["replies"]]
            row["fast"] = f"{sum(1 for r in reps if r['days'] <= 2)} of {len(reps)}" if reps else "No past replies to measure"
            row["casualties"] = f"{sum(1 for r in reps if r['hurt'])} of {len(reps)}" if reps else "No past replies to measure"
            row["longer"] = f"~{longer:.0%} (all chains, n={chain['chains']})" if longer is not None and kk else "No past replies"
            row["phase_note"] = ""
        else:
            row.update(reply="Not measured", reply_range="", fast="Not measured", casualties="Not measured", longer="", phase_note="")
        out = [c for c in cs if not c.get("week")]
        if out:
            row["signals"] = dict(
                n=len(out),
                strikes_after=f"{sum(1 for c in out if c['strike7'])} of {sum(1 for c in out if c['strike7'] is not None)}",
                shipping=f"{sum(c['ship_b'] for c in out if c['ship_a'] is not None)} -> {sum(c['ship_a'] for c in out if c['ship_a'] is not None)}",
                talks=f"{sum(1 for c in out if c['talks14'])} of {sum(1 for c in out if c['talks14'] is not None)}")
        else:
            row["signals"] = dict(n=0)
        rows[k] = row
    return rows


def strength(n):
    if n == 0: return "No data"
    if n <= 3: return "Very thin"
    if n <= 7: return "Thin"
    return "OK"


def risk_lines(key, cases_by_key, rows):
    """Five plain-language lines (one per category) plus the evidence strength, from the measured numbers only."""
    r, fl, cs = rows[key], FLAGS[key], cases_by_key[key]
    m = r["signals"]; bl = baseline_hold()
    reps = [x for c in cs for x in c["replies"]]
    hurt = [x for x in reps if x["hurt"]]
    L5 = []
    if fl["trigger"] and cs:
        L5.append(f"Replies that hurt people: {len(hurt)} of {len(reps)} logged" + (": " + "; ".join(f"#{x['id']} {x['dmg'][:70]}" for x in hurt) if hurt else "") + ". Civilian harm reported in the US act itself: none in an allowed outlet.")
    elif fl["is_hold"]:
        L5.append(f"Ship crews: attacks on shipping have been logged at about {bl['per_week']} a week in the current phase. No new US act to answer.")
    elif key == "C":
        L5.append("No direct casualties. Harm to ordinary Yemenis from sanctions: not measured.")
    else:
        L5.append("No direct casualties from the move itself.")
    if fl["trigger"] and cs:
        L5.append(f"The Houthis or a group they work with replied within ~5 days: {r['reply']} (range {r['reply_range'] or '-'}). Fast (within 2 days): {r['fast']}. Back-and-forth past one reply: {r['longer']}.")
    elif fl["is_hold"]:
        L5.append("No new US trigger. The Houthis attacked in some weeks anyway (see the hold-week cases). Whether holding back changes what they do: not measured.")
    elif m.get("n"):
        L5.append(f"The Houthis attacked within 7 days after {m['strikes_after']} past cases (timing only, not shown to be replies). Reply rate: not measured for this option.")
    else:
        L5.append("No past cases, so no measure.")
    if fl["military"] == "reply" and cs:
        k_ = sum(1 for c in cs if any(x["kinetic"] for x in c["replies"]))
        L5.append(f"A missile, drone or boat attack followed within ~5 days in {k_} of {len(cs)} past cases. Losses of US equipment in those replies: none logged.")
    elif fl["military"] == "strike":
        L5.append("Share of hold weeks with a Houthi attack in the 7 days after (see the cases).")
    else:
        L5.append("No military cost expected from the move itself.")
    if m.get("n"):
        L5.append(f"Attacks on shipping, 7 days before -> after past cases: {m['shipping']} (total). Oil prices and freight costs: not measured.")
    else:
        L5.append(f"Baseline: about {bl['per_week']} logged attacks on shipping a week in the current phase. Oil prices and freight costs: not measured.")
    if m.get("n"):
        L5.append(f"Talks or diplomatic moves within 14 days after: {m['talks']}. Strain with Saudi Arabia and the Gulf: not measured.")
    else:
        L5.append("No past cases, so no measure. Strain with Saudi Arabia and the Gulf: not measured.")
    ev_str = strength(r["n"]) if fl["trigger"] else (f"{r['n']} hold weeks" if fl["is_hold"] else (f"{m['n']} past cases (timing only)" if m.get("n") else "No data"))
    return L5, ev_str
