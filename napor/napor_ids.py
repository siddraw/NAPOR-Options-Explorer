"""NAPOR - ID system (step 1).

Two kinds of ID:
  Report ID (R0001, R0002, ...)  one per news story / official statement.
  Event ID  (1, 2, 3, ...)       one per real-world event.
Every report points to exactly one event. Three newspapers covering one attack = three
reports, ONE event. That keeps the log free of duplicates and lets us count how many
independent outlets back each event (more independent outlets = more trustworthy).

New stories come in through intake():
  - looks like an event we already have  -> attach the report to that event
  - might be an event we already have    -> put it in the review queue for a human
  - looks new                            -> put it in the review queue as a NEW event
Nothing is added to the event log automatically yet: the matcher is right only about
half the time on headlines (see test_resolver.py), so a human confirms.
"""
import json, os, re, datetime as dt
from data import events, events_raw, event_audit, MERGED
from audit_sources import SOURCES
import resolver

HERE = os.path.dirname(os.path.abspath(__file__))
QUEUE_FILE = os.path.join(HERE, "napor_review_queue.json")

# MERGED (duplicate -> surviving event) now lives in data.py so every module uses the same map.

# My suggested call on each look-alike pair. A person confirms before anything is merged,
# because merging changes the statistics.
SUGGEST = {
 (98, 102): "Different events: two separate Houthi attacks on Riyadh (Oct 8 and Oct 10).",
 (101, 103): "Different events: two separate IRGC claims (NV Sunshine Oct 9; mine strike Oct 10).",
 (66, 67): "Different events: separate IRGC claims (Aqaba Jul 19; radar and F-15 Jul 21).",
 (3, 8): "Keep both: same opening wave, but different ships hit.",
 (73, 74): "Keep both, linked: #74 is one strike inside the #73 wave, logged separately because it caused casualties.",
}

STATE_MEDIA = {"Tasnim", "IRNA", "Press TV", "Fars", "Mehr"}
OFFICIAL = {"CENTCOM", "NAVCENT", "DoD", "Pentagon", "White House", "Treasury", "OFAC", "UKMTO", "IAEA", "UN", "State Department", "Petra", "Army.mil"}


def outlet_name(raw):
    """'AFP (via Ahram Online)' -> 'AFP'; 'AAP (...) via Newcastle Herald' -> 'AAP'."""
    s = re.sub(r"\s*\(.*?\)", "", raw or "")
    s = re.split(r"\s+via\s+", s)[0]
    return s.strip()


# Official or primary sources (approved 2026-10-29): .gov and .mil pages, legislative records, courts and the Justice Department,
# the UN and other international bodies, a foreign government's own ministry for what it did or said, official archives.
# The ones above are named in OFFICIAL; these are the rest. They score like an allowed outlet (0.80) only when the page read is
# the official page itself. A label with "via" means a mirror or copy hosts it (for example "CRS report (via everycrsreport.com)"):
# that keeps the 0.60 of an outlet that is not on the list.
OFFICIAL_PRIMARY = {"Congressional Record", "Congress", "CRS report", "Justice Department", "DOJ", "Commerce", "KEDO", "INDOPACOM",
                    "Japan Ministry of Defense", "Ministry of", "NATO", "OAS", "GAO", "Federal Register", "Presidential Library"}


def is_copy(raw):
    """True when the label says the page read is a copy on another site ("AP (via KPAX)")."""
    return bool(re.search(r"\bvia\b", raw or "", re.I))


def display_label(raw):
    """Short label the page shows for a source: 'AP (via KPAX; byline X)' -> 'AP (via KPAX)'. Without 'via' it is just the outlet name."""
    name = outlet_name(raw).rstrip(" ,")
    m = re.search(r"\bvia\b\s+([^;)]+)", raw or "", re.I)
    return f"{name} (via {m.group(1).strip()})" if m else name


def source_kind(raw, claim_media=None, claim_label="Iranian state media (claim only)"):
    """Kind of outlet. claim_media / claim_label are per theater (Iran: state media; Houthis: al-Masirah, Saba)."""
    n = outlet_name(raw)
    media = STATE_MEDIA if claim_media is None else claim_media
    if n in media or any(n.startswith(x) for x in media):
        return claim_label
    if any(n.startswith(x) for x in OFFICIAL):
        return "Official statement"
    if any(n.startswith(x) for x in OFFICIAL_PRIMARY) and not is_copy(raw):
        return "Official statement"
    return "Independent outlet"


def build_reports():
    """Give every logged citation a report ID, pointing at its (surviving) event."""
    rows = []
    for eid in sorted(SOURCES):
        for s in sorted(SOURCES[eid], key=lambda x: (x.get("published") or "", x.get("outlet") or "")):
            rows.append(dict(event_id=MERGED.get(eid, eid), logged_under=eid, outlet_raw=s["outlet"],
                             outlet=outlet_name(s["outlet"]), kind=source_kind(s["outlet"]),
                             headline=s.get("headline", ""), published=s.get("published", ""),
                             url=s.get("url", ""), seen=s.get("seen", "")))
    # Events that were never re-checked still name credible outlets in the original row, but
    # without a headline or link. Record them as reports, flagged so nobody mistakes them for
    # checked citations.
    KNOWN = ["Al Jazeera", "NPR", "CBS News", "ABC News", "USNI News", "Times of Israel", "CNN", "WSJ", "TIME", "AP", "Reuters"]
    have = {r["logged_under"] for r in rows}
    for e in events_raw:
        if e[0] in have or event_audit[e[0]]["check"] != "Not re-checked":
            continue
        for name in [k for k in KNOWN if re.search(r"\b" + re.escape(k) + r"\b", e[9])]:
            rows.append(dict(event_id=MERGED.get(e[0], e[0]), logged_under=e[0], outlet_raw=name + " (named in original row)",
                             outlet=name, kind=source_kind(name), headline="(not recorded)", published="",
                             url="", seen="name only - not re-checked"))
    rows.sort(key=lambda r: (r["event_id"], r["published"] or "9999"))
    for i, r in enumerate(rows, start=1):
        r["report_id"] = f"R{i:04d}"
    return rows


REPORTS = build_reports()


def reports_for(eid):
    return [r for r in REPORTS if r["event_id"] == eid]


def corroboration(eid):
    """How many DIFFERENT outlets back this event, split by kind."""
    rs = reports_for(eid)
    indep = {r["outlet"] for r in rs if r["kind"] == "Independent outlet"}
    official = {r["outlet"] for r in rs if r["kind"] == "Official statement"}
    claims = {r["outlet"] for r in rs if r["kind"].endswith("(claim only)")}
    return dict(reports=len(rs), independent=len(indep), official=len(official), claim_only=len(claims))


# ---------------------------------------------------------------------------
# Credibility (0 to 1)
#
# Each REPORT gets:  source score  x  fit score  = weight
#   source score - how trustworthy the outlet type is
#       credible outlet or official/primary source (read on its own page) 0.80, other outlet or a mirror of an official page 0.60,
#       Iranian state media 0.30 (it can only show what Iran claims)
#   fit score    - how sure we are this story is about THIS event
#       story read in full 1.00, only the headline seen 0.80,
#       outlet named but story not saved 0.65; a new story the matcher filed
#       on its own gets the matcher's similarity score instead
#   Reports with weight under 0.30 do not count toward the event.
#
# Each EVENT combines its reports, counting each outlet once (its best report), as
#   1 - (1 - w1) x (1 - w2) x ...
# i.e. "the chance that not every one of these outlets got it wrong". One full-text
# credible story = 0.80; two different outlets = 0.96; Iranian state media alone = 0.30.
# Then the source check adjusts it: Partly verified x 0.8; Not supported -> at most 0.20.
#
# LINK RULE (approved 2026-10-28): a report with no https link has weight 0, so an event with no linked
# report has credibility 0 and is always below the cut.
# RULE: an event is used in the statistics only if its credibility is 0.50 or more.
# 0.50-0.65 is used but flagged "use with caution".
# ---------------------------------------------------------------------------
ALLOWED = {"AP", "Reuters", "AFP", "BBC", "NPR", "PBS NewsHour", "PBS", "The New York Times", "NYT", "WSJ", "Washington Post",
           "Bloomberg", "Financial Times", "CBS News", "ABC News", "NBC News", "CNN", "Al Jazeera", "Axios", "Politico",
           "Times of Israel", "Haaretz", "USNI News", "Defense News", "Breaking Defense", "The War Zone", "Stars and Stripes",
           "AAP", "TIME", "Bloomberg Government"}
INCLUDE_AT = 0.50
CAUTION_BELOW = 0.65
MIN_REPORT_WEIGHT = 0.30


def source_score(r):
    if r["kind"].endswith("(claim only)"): return 0.30
    if r["kind"] == "Official statement": return 0.80
    return 0.80 if r["outlet"] in ALLOWED else 0.60


def fit_score(r):
    seen = (r.get("seen") or "").lower()
    if "matcher" in seen: return r.get("match_score", 0.5)
    if seen.startswith("full"): return 1.00
    if seen.startswith("snippet"): return 0.80
    return 0.65


def has_link(r):
    """Link rule (owner-approved 2026-10-28): a report counts only if it has a working https link."""
    return str(r.get("url") or "").strip().lower().startswith("https://")


def report_weight(r):
    if not has_link(r): return 0.0              # name-only report: zero credit
    return round(source_score(r) * fit_score(r), 3)


def credibility_of(reports, check=""):
    """Credibility 0-1 from a list of report dicts (outlet, kind, seen) and the source-check label.
    Shared by every theater: event_credibility() below is the Iran wrapper."""
    best = {}
    for r in reports:
        w = report_weight(r)
        if w >= MIN_REPORT_WEIGHT:
            best[r["outlet"]] = max(best.get(r["outlet"], 0), w)
    p_all_wrong = 1.0
    for w in best.values():
        p_all_wrong *= (1 - w)
    c = min(0.99, 1 - p_all_wrong) if best else 0.0          # never claim certainty
    if check == "Partly verified": c *= 0.8
    elif check == "Date conflict": c *= 0.9
    elif check == "Not supported": c = min(c, 0.20)
    return round(c, 2)


def event_credibility(eid):
    if eid in MERGED: return None
    return credibility_of(reports_for(eid), event_audit[eid]["check"])


def credibility_label(c):
    if c is None: return "Merged"
    if c >= 0.80: return "High"
    if c >= INCLUDE_AT: return "Medium"
    return "Low"


def used_in_stats(eid):
    c = event_credibility(eid)
    if c is None: return "No - merged duplicate"
    if c < INCLUDE_AT: return "No - credibility below 0.50"
    if c < CAUTION_BELOW: return "Yes - use with caution"
    return "Yes"


def counts(eid):
    c = event_credibility(eid)
    return c is not None and c >= INCLUDE_AT


def filter_pairs(pairs):
    keep = [p for p in pairs if counts(p[1]) and counts(p[2])]
    dropped = [p for p in pairs if p not in keep]
    return keep, dropped


def filter_census(census):
    keep = [c for c in census if counts(c[0])]
    dropped = [c for c in census if c not in keep]
    return keep, dropped


# ---------------------------------------------------------------------------
# Intake: a new story arrives
# ---------------------------------------------------------------------------
def _load_queue():
    if os.path.exists(QUEUE_FILE):
        with open(QUEUE_FILE) as f:
            return json.load(f)
    return []


def intake(published, headline, outlet, url="", detail="", actor="", target="", save=True):
    """Decide what a new story is. Returns the decision; uncertain cases go to the review queue."""
    d = published if isinstance(published, dt.date) else dt.date.fromisoformat(published)
    text = f"{headline}. {detail}".strip()
    pool = [e for e in events if e[0] not in MERGED]          # never match to a merged duplicate
    res = resolver.resolve(d, actor, target, text, pool=pool, top=3)
    queue = _load_queue()
    next_r = f"R{len(REPORTS) + len(queue) + 1:04d}"
    item = dict(report_id=next_r, published=d.isoformat(), outlet=outlet, kind=source_kind(outlet),
                headline=headline, url=url, decision=res["decision"],
                matched_event=res["best_id"], proposed_new_event_id=res["next_id"] if res["decision"] == "NEW EVENT" else None,
                candidates=[dict(score=s, event_id=i, date=dte, detail=txt) for s, i, dte, txt in res["candidates"]],
                match_score=res["candidates"][0][0] if res["candidates"] else 0.0,
                seen="filed by matcher (not yet confirmed by a person)",
                status="attach (auto)" if res["decision"] == "SAME EVENT" else "needs human check",
                received=dt.date.today().isoformat())
    if save:
        queue.append(item)
        with open(QUEUE_FILE, "w") as f:
            json.dump(queue, f, indent=1)
    return item


def duplicate_watch(cutoff=0.60):
    """Pairs already in the log that might be one event logged twice (for a human to check)."""
    by = {e[0]: e for e in events}
    out = []
    for s, a, b, parts in resolver.scan_log([e for e in events if e[0] not in MERGED]):
        if s >= cutoff:
            out.append(dict(score=s, event_a=a, event_b=b, date_a=by[a][1].isoformat(), date_b=by[b][1].isoformat(),
                            detail_a=by[a][5], detail_b=by[b][5]))
    return out


if __name__ == "__main__":
    print(f"{len(REPORTS)} reports covering {len({r['event_id'] for r in REPORTS})} events")
    weak = [e[0] for e in events if e[0] not in MERGED and corroboration(e[0])["independent"] + corroboration(e[0])["official"] == 0]
    print("Events with no independent or official report:", weak)
    print("Possible duplicates to check:", [(d['event_a'], d['event_b'], d['score']) for d in duplicate_watch()])
    import collections
    from data import pairs, census
    cs = {e[0]: event_credibility(e[0]) for e in events}
    print("Credibility spread:", collections.Counter(credibility_label(c) for c in cs.values()))
    print("Below 0.50:", sorted((k, v) for k, v in cs.items() if v is not None and v < INCLUDE_AT))
    print("Use with caution (0.50-0.65):", sorted((k, v) for k, v in cs.items() if v is not None and INCLUDE_AT <= v < CAUTION_BELOW))
    print("Pairs dropped:", [p[0] for p in filter_pairs(pairs)[1]], " Census rows dropped:", [c[0] for c in filter_census(census)[1]])
