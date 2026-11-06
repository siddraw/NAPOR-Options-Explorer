"""NAPOR tag check: every counted US-action case in every theater must carry valid action tags.

Run from napor/:  python3 tag_check.py     Exit code 0 = PASS, 1 = FAIL (the weekly agent must tag the case).
Tags live in napor/tags/<theater>.py and describe what the US did, never what followed (see action_tags.py)."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import action_tags as A
import theaters


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
