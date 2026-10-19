"""Event resolver: decides whether a new report is a NEW event or another report of an
event we already have (same idea as track association in a sensor-fusion system).

How it works, in plain terms:
  1. Turn every event into a fingerprint: date, who acted, which places, what kind of act,
     and its key words/numbers.
  2. Compare a new report to every existing event and give a similarity score (0 to 1).
  3. Score high  -> SAME event: attach the report to the existing ID (a second source
                    makes the event more trustworthy).
     Score middle -> POSSIBLE match: a human should look.
     Score low   -> NEW event: give it the next ID.
Rule-based, not machine learning. The thresholds were tuned on this log, so treat them as a
starting point.
"""
import re, datetime as dt
from data import events

SAME, MAYBE = 0.62, 0.48       # score cut-offs

PLACES = {
 "jordan": ["jordan", "muwaffaq", "salti", "azraq", "aqaba", "king hussein", "prince hassan", "titin", "tabrin"],
 "bahrain": ["bahrain", "juffair", "manama", "fifth fleet", "5th fleet", "isa air", "sheikh isa", "salman"],
 "kuwait": ["kuwait", "arifjan", "ali al salem", "shuaiba", "bubiyan", "buehring"],
 "qatar": ["qatar", "udeid", "doha"],
 "uae": ["uae", "emirates", "abu dhabi", "fujairah", "ruwais", "dubai", "sader", "dhafra"],
 "saudi": ["saudi", "riyadh", "ras tanura", "prince sultan", "aramco", "bahri"],
 "israel": ["israel", "tel aviv", "dimona", "arad", "haifa", "negev"],
 "iraq": ["iraq", "erbil", "baghdad"],
 "lebanon": ["lebanon", "beirut", "hezbollah", "bekaa"],
 "hormuz": ["hormuz", "strait", "gulf of oman", "oman"],
 "natanz": ["natanz"], "isfahan": ["isfahan"], "tehran": ["tehran", "karaj"],
 "bandar_abbas": ["bandar abbas", "qeshm", "konarak", "kenerak", "jask", "sirik", "minab", "bandar lengeh", "lengeh"],
 "larak": ["larak"], "kharg": ["kharg"], "lavan": ["lavan"],
}
SIDES = {"us": ["us", "u.s.", "centcom", "american", "trump", "pentagon", "navy"],
         "israel": ["israel", "idf", "israeli"],
         "iran": ["iran", "irgc", "iranian", "tehran"]}
FAMILY = {
 "strike":   ["strike", "struck", "hit", "attack", "missile", "drone", "bomb", "retaliat", "intercept", "destroy", "raid", "salvo", "wave"],
 "maritime": ["seiz", "tanker", "vessel", "ship", "blockade", "mine", "closure", "closed", "boarded", "transit", "escort"],
 "diplomacy":["ceasefire", "talks", "memorandum", "mou", "deal", "proposal", "plan", "negotiat", "agreement", "truce"],
 "statement":["announce", "says", "claims", "assessment", "warns", "threat", "interview"],
}
STOP = set("the and with for from that this into over after before their there been were was has have will its than then they them also more most some such only near about between while which when where who whom what other new first second again still just like claims claimed says said".split())


def _norm(t): return re.sub(r"[^a-z0-9. ]", " ", (t or "").lower())

def _places(t):
    """Place tags: the country/region AND any specific site named (so two attacks on different
    Jordanian bases look different, while two reports of one attack look the same)."""
    t = _norm(t); out = set()
    for k, al in PLACES.items():
        hit = [a for a in al if re.search(r"\b" + re.escape(a) + r"\b", t)]
        if hit:
            out.add(k)
            if len(al) > 1 and k not in ("hormuz",):
                out.update(f"{k}:{a}" for a in hit if a != k)
    return out

def _sides(t):
    t = _norm(t); out = set()
    for k, al in SIDES.items():
        if any(re.search(r"\b" + re.escape(a) + r"\b", t) for a in al): out.add(k)
    return out

def _family(t):
    t = _norm(t)
    scores = {k: sum(1 for w in ws if w in t) for k, ws in FAMILY.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] else "other"

def _words(t):
    return {w for w in _norm(t).split() if len(w) > 3 and w not in STOP and not w.isdigit()}

def _nums(t):
    return set(re.findall(r"\b\d[\d,]*\b", (t or "").replace(",", "")))

_DF = None
def _idf(w):
    """Rare words (wedding, Larak, Patriot) count for more than common ones (strikes, Iran)."""
    global _DF
    import math
    if _DF is None:
        from collections import Counter
        _DF = Counter(); n = 0
        for e in events:
            n += 1
            _DF.update(_words(f"{e[3]} {e[5]}"))
        _DF["__n"] = n
    return math.log((1 + _DF["__n"]) / (1 + _DF.get(w, 0))) + 0.1

def _wjac(a, b):
    if not (a or b): return 0.0
    inter = sum(_idf(w) for w in a & b); union = sum(_idf(w) for w in a | b)
    return inter / union if union else 0.0

def _jac(a, b):
    return len(a & b) / len(a | b) if (a | b) else 0.0


def fingerprint(date, actor, target, detail, atype=""):
    blob = f"{actor} {atype} {target} {detail}"
    return dict(date=date, sides=_sides(actor) or _sides(detail[:80]), places=_places(f"{target} {detail}"),
                family=_family(f"{atype} {detail}"), words=_words(f"{atype} {detail}"), nums=_nums(detail))


def similarity(a, b, report=False):
    """0..1 score. Two events more than 2 days apart can never match (time-zone slop is ~1 day).
    For a NEWS REPORT (a) the story may run up to 3 days after the event (b), so the window is wider."""
    delta = (a["date"] - b["date"]).days
    gap = abs(delta)
    if report:
        if delta < -1 or delta > 3: return 0.0, {}
        s_date = {-1: 0.7, 0: 1.0, 1: 0.9, 2: 0.7, 3: 0.45}[delta]
    else:
        if gap > 2: return 0.0, {}
        s_date = {0: 1.0, 1: 0.8, 2: 0.35}[gap]
    s_place = _jac(a["places"], b["places"]) if (a["places"] or b["places"]) else 0.3
    s_side = _jac(a["sides"], b["sides"]) if (a["sides"] and b["sides"]) else 0.3
    s_fam = 1.0 if a["family"] == b["family"] else 0.0
    s_text = 0.7 * _wjac(a["words"], b["words"]) + 0.3 * _jac(a["nums"], b["nums"])
    score = 0.28 * s_date + 0.24 * s_place + 0.10 * s_side + 0.14 * s_fam + 0.24 * min(1.0, s_text * 2.2)
    # Different sides acting (e.g. Iran vs US) means a cause and its reply, not one event.
    if a["sides"] and b["sides"] and not (a["sides"] & b["sides"]): score *= 0.6
    return round(score, 3), dict(date=s_date, place=round(s_place, 2), side=round(s_side, 2), kind=s_fam, text=round(s_text, 2))


def _fp_event(e):
    (eid, date_, actor, atype, target, detail, *_rest) = e
    return fingerprint(date_, actor, target, detail, atype)


def resolve(date, actor, target, detail, atype="", pool=None, top=3):
    """Compare ONE new report against the existing events. Returns a decision dict."""
    pool = pool if pool is not None else events
    new = fingerprint(date, actor, target, detail, atype)
    ranked = sorted(((similarity(new, _fp_event(e), report=True)[0], e[0], e) for e in pool), reverse=True)[:top]
    best_score, best_id, best_e = ranked[0] if ranked else (0, None, None)
    if best_score >= SAME:   decision = "SAME EVENT"
    elif best_score >= MAYBE: decision = "POSSIBLE MATCH - human should check"
    else:                     decision = "NEW EVENT"
    next_id = max(e[0] for e in pool) + 1
    return dict(decision=decision, best_id=best_id if decision != "NEW EVENT" else None, next_id=next_id,
                candidates=[(s, i, e[1].isoformat(), (e[5] or "")[:90]) for s, i, e in ranked])


def scan_log(pool=None):
    """Compare every event with every other and list likely duplicates already in the log."""
    pool = pool if pool is not None else events
    fps = {e[0]: _fp_event(e) for e in pool}
    found = []
    for i, a in enumerate(pool):
        for b in pool[i + 1:]:
            s, parts = similarity(fps[a[0]], fps[b[0]])
            if s >= MAYBE: found.append((s, a[0], b[0], parts))
    return sorted(found, reverse=True)


if __name__ == "__main__":
    by = {e[0]: e for e in events}
    print("Pairs in the log that look like the SAME event (score >= %.2f) or POSSIBLY the same (>= %.2f):\n" % (SAME, MAYBE))
    for s, a, b, parts in scan_log():
        tag = "SAME " if s >= SAME else "maybe"
        print(f"[{tag}] {s:.2f}  #{a} ({by[a][1]}) vs #{b} ({by[b][1]})  {parts}")
        print(f"        #{a}: {by[a][5][:95]}")
        print(f"        #{b}: {by[b][5][:95]}")
