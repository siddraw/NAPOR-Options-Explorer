"""NAPOR step 2: war phases and chains.

PHASE  - what state the war was in on a given day. People behave differently in open war
         than in a ceasefire or a quiet holding pattern, so risk numbers should be counted
         within the right phase. The phase boundaries are judgement calls based on the logged
         events (each boundary names the event that marks it).

CHAIN  - a back-and-forth: events linked by "this was a reply to that". Each chain gets a
         thread ID (T01, T02, ...). If a chain keeps growing, a tit-for-tat is building.
"""
from collections import defaultdict
from data import d, events, pairs, MERGED, event_kind
import prewar as _pre

# (phase type, start, end, what marks the start)
PHASES = list(_pre.PHASES) + [
    ("Open war",           d(2026, 2, 28), d(2026, 4, 7),  "#2 Operation Epic Fury opens the war"),
    ("Fragile ceasefire",  d(2026, 4, 8),  d(2026, 7, 7),  "#28 two-week ceasefire (Apr 7-8); renewed Jun 8 (#43); interim deal Jun 17 (#50)"),
    ("Open war",           d(2026, 7, 8),  d(2026, 7, 25), "#59 Trump declares the ceasefire over; #60 90-target strike wave"),
    ("Low-intensity war",  d(2026, 7, 26), d(2026, 9, 9),  "End of the nightly US campaign; no ceasefire, occasional exchanges (#70-#80)"),
    ("Holding pattern",    d(2026, 9, 10), d(2026, 12, 31), "No direct US-Iran strikes since Sep 9; talks (#81-#99); Trump: no strikes before Nov 3 (#97)"),
]


def phase_of(day):
    for name, a, b, _ in PHASES:
        if a <= day <= b:
            return name
    return "Before the war"


EV = {e[0]: e for e in events}
event_phase = {e[0]: phase_of(e[1]) for e in events}

# ---------------------------------------------------------------------------
# Chains
# ---------------------------------------------------------------------------
_links = set()
for e in events:
    if e[6] and e[0] not in MERGED:
        _links.add((MERGED.get(e[6], e[6]), e[0]))
for p in pairs:
    _links.add((p[1], p[2]))

_par = {}
def _find(x):
    _par.setdefault(x, x)
    while _par[x] != x:
        _par[x] = _par[_par[x]]
        x = _par[x]
    return x
for a, b in _links:
    _par[_find(a)] = _find(b)
_groups = defaultdict(set)
for a, b in _links:
    _groups[_find(a)] |= {a, b}
_chains = sorted((sorted(g, key=lambda i: (EV[i][1], i)) for g in _groups.values()), key=lambda ids: (EV[ids[0]][1], ids[0]))

# Chain names, keyed by the chain's first event (so adding older events never shifts a name).
NAMES = {
    2: "Opening campaign and Iran's first retaliation",
    10: "Strikes on Tehran leadership sites -> drones on US embassy in Riyadh",
    16: "Natanz -> Iranian missiles toward Dimona/Arad",
    20: "IRGC Navy chief killed -> Prince Sultan AB strike",
    28: "April ceasefire -> Israeli strikes in Lebanon -> Strait restricted",
    34: "Failed Islamabad talks -> US blockade -> Strait closed again",
    37: "Ship seizures, tit-for-tat",
    41: "US destroyers attacked -> US strikes near Bandar Abbas",
    43: "June 8-11 flare-up (air-defense crews killed -> Apache downed -> US strikes -> Jordan)",
    50: "Interim deal signed -> US blockade ends",
    52: "Israeli strikes in Lebanon -> Strait closed again",
    54: "First interim-deal violation -> US strikes -> Iran fires at Kuwait/Bahrain",
    57: "Deal collapses -> July US campaign -> Iranian retaliation",
    70: "Larak Island -> Jordan -> Sep 1 strike wave -> Jordan",
    78: "Missiles at a US warship -> tankers destroyed -> Jordan base hit",
    81: "Autumn diplomacy: 7-day plan -> rejection -> counter-offer",
    83: "RAF Fairford plot -> US bombers withdrawn",
    97: "No-strike pledge before the midterms -> reported strike plans",
    98: "Houthi missile strikes on Riyadh (separate front, context)",
}
NAMES.update(_pre.CHAIN_NAMES)
_WAR_START = d(2026, 2, 27)

THREADS = []
event_thread = {}
_count = {"P": 0, "T": 0}
for ids in _chains:
    _pfx = "P" if EV[ids[0]][1] < _WAR_START else "T"     # P = before the 2026 war, T = during it
    _count[_pfx] += 1
    tid = f"{_pfx}{_count[_pfx]:02d}"
    name = NAMES.get(ids[0], "Unnamed chain")
    kinds = [event_kind[i] for i in ids]
    # rounds = how many times the acting side switched between US/Israel and Iran
    def side(i):
        a = EV[i][2].lower()
        if a.startswith("iran") or "iran-backed" in a or "iranian-made" in a: return "Iran"
        if a.startswith(("us", "israel")): return "US/Israel"
        return None
    sides = [side(i) for i in ids if side(i)]
    rounds = sum(1 for x, y in zip(sides, sides[1:]) if x != y)
    hostile = sum(1 for k in kinds if k in ("Kinetic", "Maritime"))
    THREADS.append(dict(thread_id=tid, name=name, events=ids, start=EV[ids[0]][1], end=EV[ids[-1]][1],
                        days=(EV[ids[-1]][1] - EV[ids[0]][1]).days, n=len(ids), rounds=rounds, hostile_acts=hostile,
                        phase=event_phase[ids[0]], last_actor=EV[ids[-1]][2]))
    for i in ids:
        event_thread[i] = tid


def chain_stats():
    """For back-and-forth chains with at least one hostile act: how many side-switches before it stopped."""
    mil = [t for t in THREADS if t["hostile_acts"] >= 1 and "context" not in t["name"]]
    if not mil:
        return {}
    r = [t["rounds"] for t in mil]
    return dict(chains=len(mil), avg_rounds=round(sum(r) / len(r), 2), max_rounds=max(r),
                share_stopped_after_one_reply=round(sum(1 for x in r if x <= 1) / len(r), 2),
                avg_days=round(sum(t["days"] for t in mil) / len(mil), 1))


if __name__ == "__main__":
    for t in THREADS:
        print(t["thread_id"], t["start"], f"{t['days']}d", f"n={t['n']}", f"rounds={t['rounds']}", t["phase"], "|", t["name"], t["events"])
    print(chain_stats())
    from collections import Counter
    print(Counter(event_phase.values()))
