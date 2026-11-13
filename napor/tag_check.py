"""NAPOR tag check: every counted US-action case in every theater must carry valid action tags.

Run from napor/:  python3 tag_check.py     Exit code 0 = PASS, 1 = FAIL (the weekly agent must tag the case).
Tags live in napor/tags/<theater>.py and describe what the US did, never what followed (see action_tags.py)."""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import action_tags as A
import non_us_actors as NU
import theaters


US_FIRST = re.compile(r"^\s*(u\.?s\.?|united states)(\b|/)", re.I)
# a case title that starts with a non-US government as the one who acts (the actor field can be wrong or generic)
NON_US_SUBJECT = re.compile(r"^\s*(the\s+)?(israel(i)?|idf|mossad|saudi|uae|emirati|qatar(i)?|uk|british|britain|japan(ese)?|south korea(n)?|australia(n)?|canada|canadian|"
                            r"france|french|german(y)?|nato|eu|european union|taiwan(ese)?|philippine(s)?|pakistan(i)?|turkey|turkish|oman(i)?|egypt(ian)?|india(n)?|colombia(n)?|"
                            r"trinidad|guyana)\b", re.I)


def non_us_actors(tid, out):
    """Counted cases whose actor is not the US need a recorded US link (non_us_actors.LINKS); excluded ones must not be counted."""
    fails = []
    links, excl = (NU.LINKS.get(tid) or {}), (NU.EXCLUDED.get(tid) or {})
    cases = {c["id"]: c for o in out["options"] for c in o["cases"] if not c.get("week")}
    for i, c in sorted(cases.items()):
        if i in excl:
            fails.append(f"{tid} #{i}: is in non_us_actors.EXCLUDED (no US link) but is still a counted case")
            continue
        if not US_FIRST.match(c["actor"]) or NON_US_SUBJECT.match(c["title"]):
            l = links.get(i)
            if not l:
                fails.append(f"{tid} #{i} ({c['actor']}): counted case with a non-US actor and no recorded US link (add it to non_us_actors.LINKS with the link from the log's sources, or exclude it with EXCLUDED)")
            elif len(str(l.get("link", "")).strip()) < 20:
                fails.append(f"{tid} #{i}: non_us_actors.LINKS entry needs a plain `link` line (what the US link is)")
    for name, d in (("LINKS", links), ("EXCLUDED", excl)):
        for i in d:
            if i not in cases and name == "LINKS":
                fails.append(f"{tid} #{i}: non_us_actors.LINKS names an event that is not a counted case")
    for i in set(links) & set(excl):
        fails.append(f"{tid} #{i}: is both in LINKS and EXCLUDED")
    return fails


def scan():
    fails = []
    for tid in theaters.registered():
        path = os.path.join(HERE, "..", "explorer", "data", tid + ".json")
        out = json.load(open(path))
        tags = A.load_tags(tid)
        if tags is None:
            fails.append(f"{tid}: no tag file (create napor/tags/{tid}.py with TAGS = {{...}})")
            continue
        fails += A.check(tid, tags, A.counted_case_ids(out))
        fails += non_us_actors(tid, out)
        for i, c in ((c["id"], c) for o in out["options"] for c in o["cases"] if not c.get("week")):
            if "tags" not in c:
                fails.append(f"{tid} #{i}: page data has no tags (run export_explorer.py {tid})")
    return sorted(set(fails))


if __name__ == "__main__":
    fails = scan()
    for f in fails:
        print("  [FAIL] " + f)
    print("Tag check: " + ("PASS" if not fails else f"FAIL ({len(fails)})"))
    sys.exit(1 if fails else 0)
