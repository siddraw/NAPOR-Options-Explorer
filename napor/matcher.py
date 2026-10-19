"""
Event matcher for the Iran war forecasting project.

WHAT THIS DOES, IN PLAIN TERMS
-------------------------------
You feed it a short piece of text describing something that just happened
(a headline, a news summary, whatever). It:

  1. Checks whether this is even an Iran/US-war-relevant event at all.
  2. Guesses WHO acted (US/Israel side vs. Iran side) and WHAT KIND of cost
     it imposed - the same 4 buckets already used in the spreadsheet:
       Personnel/Casualty, Military/Property, Economic/Blockade, Political/Diplomatic
  3. Searches the 86-event history for the most similar past events, and
     shows what historically followed them (if they were ever a "trigger").
  4. Pulls the real base-rate numbers for that category straight out of the
     Action-Reaction Pairs data (same numbers as the Factor Analysis sheet,
     computed here in Python so there's no copy/paste risk of drifting from
     the spreadsheet).

This is a RULE-BASED matcher (keyword lists + simple scoring), not a
machine-learning model. With only 86 events and 25 pairs, a hand-built rule
set is more honest than training a model that would just be memorizing
noise. It is meant to narrow things down and hand you the relevant history
fast, not to make the final call by itself.

HOW TO USE IT
-------------
    from matcher import analyze, print_report
    report = analyze("Iran fires missiles at a US destroyer in the Strait of Hormuz")
    print_report(report)

Or just run this file directly - it will test itself on a few sample
headlines at the bottom.
"""
import re
import datetime as dt
from data import events, pairs, census, event_audit

# ---------------------------------------------------------------------------
# STEP 0: look events up by ID, and work out response time between two IDs
# ---------------------------------------------------------------------------
_EVENTS_BY_ID = {row[0]: row for row in events}


def event_by_id(eid):
    return _EVENTS_BY_ID.get(eid)


def date_of(eid):
    row = event_by_id(eid)
    return row[1] if row else None


# ---------------------------------------------------------------------------
# STEP 1: is this even relevant to the Iran/US war at all?
# ---------------------------------------------------------------------------
RELEVANCE_KEYWORDS = [
    "iran", "iranian", "irgc", "tehran", "khamenei", "pezeshkian", "araghchi",
    "qeshm", "bandar abbas", "natanz", "isfahan", "chabahar", "hormuz",
    "strait of hormuz", "larak", "sirik", "jask",
    # the US/Israel side and common basing countries this war has involved
    "centcom", "pentagon", "u.s. navy", "us navy", "israel", "israeli", "idf",
    "jordan", "bahrain", "kuwait", "qatar", "saudi", "muwaffaq salti",
    "al udeid", "prince hassan", "king hussein",
]


def is_relevant(text):
    t = text.lower()
    return any(kw in t for kw in RELEVANCE_KEYWORDS)


# ---------------------------------------------------------------------------
# STEP 2: who acted, and what kind of cost did it impose?
# (priority order mirrors how the real Action-Reaction Pairs were coded:
#  an explicit casualty count wins even if blockade/diplomatic words are also
#  present, because that's how the historical data was actually tagged.)
# ---------------------------------------------------------------------------
CASUALTY_WORDS = [
    "killed", "kills", "dead", "death", "casualties", "wounded", "injured",
    "injures", "kia", "fatalities", "fatal", "died",
]
ECONOMIC_WORDS = [
    "tanker", "oil", "sanction", "blockade", "seize", "seizure", "seized",
    "shipping", "vessel", "embargo", "export license", "strait closed",
    "closes the strait", "mine", "minelay",
]
POLITICAL_WORDS = [
    "ceasefire", "talks", "negotiat", "proposal", "roadmap", "mediator",
    "ultimatum", "mou", "memorandum", "diplomatic", "reject", "counter-offer",
    "counter offer", "truce",
]
US_SIDE_WORDS = ["u.s.", "us ", "america", "centcom", "pentagon", "israel", "israeli", "idf"]
IRAN_SIDE_WORDS = ["iran", "irgc", "tehran"]


def has_casualties(text):
    t = text.lower()
    return any(w in t for w in CASUALTY_WORDS)


def guess_actor_side(text):
    t = text.lower()
    us_hit = any(w in t for w in US_SIDE_WORDS)
    iran_hit = any(w in t for w in IRAN_SIDE_WORDS)
    if us_hit and not iran_hit:
        return "US/Israel"
    if iran_hit and not us_hit:
        return "Iran"
    if us_hit and iran_hit:
        return "Both/unclear"
    return "Unknown"


def guess_trigger_category(text):
    t = text.lower()
    if has_casualties(t):
        return "Personnel/Casualty"
    if any(w in t for w in ECONOMIC_WORDS):
        return "Economic/Blockade"
    if any(w in t for w in POLITICAL_WORDS):
        return "Political/Diplomatic"
    return "Military/Property"


# ---------------------------------------------------------------------------
# STEP 3: find the most similar past events by keyword overlap
# ---------------------------------------------------------------------------
STOPWORDS = {
    "the", "a", "an", "of", "in", "on", "at", "to", "for", "and", "or", "by",
    "with", "from", "is", "are", "was", "were", "near", "over", "after",
    "its", "it", "has", "have", "had", "this", "that", "been", "be", "as",
    "than", "also", "into", "within", "while", "between",
}


def tokenize(text):
    words = re.findall(r"[a-z0-9]+", text.lower())
    return {w for w in words if w not in STOPWORDS and len(w) > 2}


def _event_tokens(row):
    (_eid, _date, actor, atype, target, detail, *_rest) = row
    return tokenize(f"{actor} {atype} {target} {detail}")


def find_similar_events(text, top_n=5):
    query_tokens = tokenize(text)
    scored = []
    for row in events:
        ev_tokens = _event_tokens(row)
        overlap = query_tokens & ev_tokens
        if overlap:
            scored.append((len(overlap), row, overlap))
    scored.sort(key=lambda x: x[0], reverse=True)
    results = []
    for score, row, overlap in scored[:top_n]:
        eid = row[0]
        # did this event later turn out to be a TRIGGER for something, per our pairs table?
        responses = [p for p in pairs if p[1] == eid]
        results.append({
            "event_id": eid,
            "date": row[1].isoformat(),
            "actor": row[2],
            "action_type": row[3],
            "target": row[4],
            "detail": row[5],
            "source_check": event_audit[eid]["check"],
            "match_score": score,
            "matched_words": sorted(overlap),
            "known_responses": [
                {
                    "response_event_id": p[2],
                    "response_date": date_of(p[2]).isoformat() if date_of(p[2]) else None,
                    "response_detail": event_by_id(p[2])[5] if event_by_id(p[2]) else None,
                    "response_time_days": (date_of(p[2]) - date_of(eid)).days
                    if date_of(p[2]) and date_of(eid) else None,
                    "trigger_category": p[3],
                    "response_caused_casualties": p[4],
                }
                for p in responses
            ],
        })
    return results


# ---------------------------------------------------------------------------
# STEP 4: base-rate stats for a trigger category, computed straight from the
# pairs list (same math as the Factor Analysis sheet, done here in Python so
# the matcher never needs to open Excel to answer "what usually happens?")
# ---------------------------------------------------------------------------
def _response_time_days(pair):
    _pid, trig_id, resp_id, _cat, _casualty, _note = pair
    td, rd = date_of(trig_id), date_of(resp_id)
    if td is None or rd is None:
        return None
    return (rd - td).days


def _wilson_ci(successes, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    phat = successes / n
    denom = 1 + z**2 / n
    center = (phat + z**2 / (2 * n)) / denom
    half = (z * ((phat * (1 - phat) / n + z**2 / (4 * n**2)) ** 0.5)) / denom
    return (max(0.0, center - half), min(1.0, center + half))


def census_stats(category):
    """Chance of ANY reply within ~5 days, from the Trigger Census (counts the
    hostile acts that drew no reply, which the pairs table cannot see).
    low = only clearly-linked replies count; best = linked + timing-only; high = also counts 'unclear'."""
    rows = [c for c in census if c[1] == category]
    strong = sum(1 for c in rows if c[2] == "R-strong")
    weak = sum(1 for c in rows if c[2] == "R-weak")
    none_ = sum(1 for c in rows if c[2] == "N")
    unclear = sum(1 for c in rows if c[2] == "Unclear")
    unverified = sum(1 for c in rows if c[2] == "Unverified")
    counted = strong + weak + none_
    if counted == 0:
        return None
    replied = strong + weak
    lo, hi = _wilson_ci(replied, counted)
    return {
        "acts_counted": counted,
        "got_reply": replied,
        "no_reply_found": none_,
        "unclear": unclear,
        "unverified_not_counted": unverified,
        "p_any_reply_low": round(strong / (counted + unclear), 3),
        "p_any_reply_best": round(replied / counted, 3),
        "p_any_reply_high": round((replied + unclear) / (counted + unclear), 3),
        "ci_95_low": round(lo, 3),
        "ci_95_high": round(hi, 3),
    }


def base_rate_for_category(category):
    group = [p for p in pairs if p[3] == category]
    n = len(group)
    if n == 0:
        return {"category": category, "n": 0}
    times = [_response_time_days(p) for p in group]
    times = [t for t in times if t is not None]
    within_1 = sum(1 for t in times if t <= 1)
    within_2 = sum(1 for t in times if t <= 2)
    causes_casualties = sum(1 for p in group if p[4] == "Y")
    share_1 = within_1 / n
    ci_low, ci_high = _wilson_ci(within_1, n)
    return {
        "category": category,
        "n": n,
        "mean_response_days": round(sum(times) / len(times), 2) if times else None,
        "share_within_1_day": round(share_1, 3),
        "ci_95_low": round(ci_low, 3),
        "ci_95_high": round(ci_high, 3),
        "share_within_2_days": round(within_2 / n, 3),
        "share_response_causes_casualties": round(causes_casualties / n, 3),
        "census": census_stats(category),   # None for categories the census doesn't cover
    }


# ---------------------------------------------------------------------------
# PUTTING IT TOGETHER
# ---------------------------------------------------------------------------
def analyze(text, top_n=5):
    relevant = is_relevant(text)
    report = {
        "input_text": text,
        "relevant_to_iran_war": relevant,
    }
    if not relevant:
        report["note"] = "No Iran/US-war keywords found - not matched against the database."
        return report

    category = guess_trigger_category(text)
    report["guessed_actor_side"] = guess_actor_side(text)
    report["guessed_trigger_category"] = category
    report["casualties_mentioned"] = has_casualties(text)
    report["similar_past_events"] = find_similar_events(text, top_n=top_n)
    report["base_rate_for_this_category"] = base_rate_for_category(category)
    return report


def print_report(report):
    print("=" * 78)
    print(f"INPUT: {report['input_text']}")
    if not report["relevant_to_iran_war"]:
        print("-> Not recognized as Iran/US-war related.", report.get("note", ""))
        print("=" * 78)
        return
    print(f"Guessed actor side:      {report['guessed_actor_side']}")
    print(f"Guessed trigger category: {report['guessed_trigger_category']}  "
          f"(casualty keywords found: {report['casualties_mentioned']})")
    print()
    print("Closest historical precedents:")
    for m in report["similar_past_events"]:
        flag = "" if m["source_check"] in ("Verified", "Corrected", "Partly verified", "Not re-checked") else f"  [SOURCE {m['source_check'].upper()}]"
        print(f"  #{m['event_id']} ({m['date']}) {m['actor']} -> {m['target']}: {m['detail'][:90]}{flag}")
        print(f"      matched on: {', '.join(m['matched_words'][:8])}")
        if m["known_responses"]:
            for r in m["known_responses"]:
                cas = "caused casualties" if r["response_caused_casualties"] == "Y" else "no casualties"
                print(f"      -> historically followed by #{r['response_event_id']} "
                      f"({r['response_time_days']} day(s) later, {cas}): {r['response_detail'][:90]}")
    br = report["base_rate_for_this_category"]
    print()
    print(f"Base rate for '{br['category']}' triggers (n={br['n']} historical pairs):")
    if br["n"] > 0:
        cs = br.get("census")
        if cs:
            print(f"  CHANCE OF ANY REPLY within ~5 days: {cs['p_any_reply_best']:.0%} "
                  f"(range {cs['p_any_reply_low']:.0%}-{cs['p_any_reply_high']:.0%}; "
                  f"{cs['got_reply']} of {cs['acts_counted']} past acts got one, "
                  f"{cs['unverified_not_counted']} more not yet checked)")
        else:
            print("  Chance of any reply: not measured for this category (diplomatic moves are not in the census)")
        print("  If a reply does come (these four numbers ignore the acts that got none):")
        print(f"  Mean response time: {br['mean_response_days']} days")
        print(f"  Responded within 1 day: {br['share_within_1_day']:.0%} "
              f"(95% CI {br['ci_95_low']:.0%}-{br['ci_95_high']:.0%})")
        print(f"  Responded within 2 days: {br['share_within_2_days']:.0%}")
        print(f"  Share of responses that caused casualties: {br['share_response_causes_casualties']:.0%}")
    print("=" * 78)


if __name__ == "__main__":
    test_headlines = [
        "Iran fires ballistic missiles at a US Navy destroyer transiting the Strait of Hormuz",
        "US Treasury announces new sanctions on Iranian oil shipments",
        "Iran and the US agree to resume ceasefire talks in Doha",
        "A local bakery in Ohio wins a county fair pie contest",
    ]
    for h in test_headlines:
        print_report(analyze(h))
        print()
