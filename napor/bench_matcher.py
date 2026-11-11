"""NAPOR: accuracy check of the "Your own option" matcher against the answer key tests/matcher_bench.json.

The key was written by hand from the case titles, independent of the tags: for each query a viewer might type
("pull troops out of Iraq") it lists the past cases that really are the SAME KIND of US action. The key has a DEV half
(used to set the tuning numbers in action_tags.MATCH) and a TEST half (never used for tuning). Six queries are
admittedly loose (the key itself says the log has no exact match) and are reported separately; nobody tunes on them.

Numbers per half (queries where something should be found):
  precision@5   of the first 5 cases returned, the share the key lists (fewer than 5 returned: share of those returned)
  recall@10     share of the key's cases that are in the first 10 returned
  F1            of the whole returned set against the key (the page returns at most 12 cases)
  none-correct  of the queries where the key says the log has NOTHING like it, the share where nothing was returned

Run from napor/:
  python3 bench_matcher.py                 print the table (v2, the word-meaning matcher; v1 from tests/matcher_v1_baseline.json)
  python3 bench_matcher.py --check         weekly build: exit 1 if the TEST half falls below tests/matcher_floor.json
  python3 bench_matcher.py --v1            re-run the old version-1 matcher in a headless browser (needs node + playwright)
  python3 bench_matcher.py --write-docs    also write docs/MATCHER_ACCURACY.md
"""
import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import matcher_ref as R

BENCH = os.path.join(REPO, "tests", "matcher_bench.json")
FLOOR = os.path.join(REPO, "tests", "matcher_floor.json")
V1 = os.path.join(REPO, "tests", "matcher_v1_baseline.json")
DOC = os.path.join(REPO, "docs", "MATCHER_ACCURACY.md")
LOOSE = ["iran-03", "iran-04", "iran-10", "iran-06", "houthis-08", "venezuela-06"]


def load_bench():
    return json.load(open(BENCH))


def run_v2(queries=None, params=None):
    """query id -> ranked case ids from the Python reference."""
    model, ths = R.load_all()
    out = {}
    for q in queries or load_bench():
        r = R.match(dict(desc=q["text"]), ths[q["theater"]], params)
        out[q["id"]] = [c["id"] for c in r["cases"]]
    return out


def score(bench, results, split, loose=False):
    """Mean precision@5, recall@10, F1 and none-correct over the queries of one split (loose queries counted only when loose=True)."""
    P, Rc, F, N = [], [], [], []
    for q in bench:
        if q["split"] != split or (q["id"] in LOOSE) != loose:
            continue
        ids = results.get(q["id"], [])
        if q["none"]:
            N.append(1.0 if not ids else 0.0)
            continue
        E = set(q["expect"])
        P.append(len(set(ids[:5]) & E) / min(5, len(ids)) if ids else 0.0)
        Rc.append(len(set(ids[:10]) & E) / len(E))
        h = len(set(ids) & E)
        p, r = (h / len(ids) if ids else 0.0), h / len(E)
        F.append(2 * p * r / (p + r) if p + r else 0.0)
    m = lambda x: sum(x) / len(x) if x else None
    return dict(n=len(P), n_none=len(N), p5=m(P), r10=m(Rc), f1=m(F), none=m(N))


def run_v1():
    """The old page's matcher (git HEAD before the upgrade) driven in a headless browser, description box only."""
    import shutil
    bench = load_bench()
    base = subprocess.run(["git", "-C", REPO, "rev-list", "-1", "--grep=Own-option popup: capital N/A", "HEAD"], capture_output=True, text=True).stdout.strip() or "HEAD"
    with tempfile.TemporaryDirectory() as tmp:
        site = os.path.join(tmp, "site"); os.makedirs(os.path.join(site, "data"))
        for rel in ["index.html", "theaters.json", "data.json"] + ["data/%s.json" % t for t in R.THEATERS]:
            blob = subprocess.run(["git", "-C", REPO, "show", "%s:explorer/%s" % (base, rel)], capture_output=True, check=True).stdout
            open(os.path.join(site, rel), "wb").write(blob)
        qf, of = os.path.join(tmp, "q.json"), os.path.join(tmp, "o.json")
        json.dump(bench, open(qf, "w"))
        env = dict(os.environ, NODE_PATH=subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip())
        subprocess.run(["node", os.path.join(HERE, "bench_matcher_v1.js"), site, qf, of], check=True, env=env)
        res = json.load(open(of))
    out = {k: v["ids"] for k, v in res.items()}
    json.dump(dict(note="Version 1 (word-reader) matcher, run in a headless browser on the old page, query text in the Description box only; ids in the order the page listed them (by date).",
                   commit=base[:7], results=out), open(V1, "w"), indent=0, sort_keys=True)
    return out


def fmt(x):
    return "n/a" if x is None else "%.2f" % x


def table(bench, v2, v1):
    rows = []
    for title, split, loose in (("Dev (used for tuning)", "dev", False), ("Test (never tuned on)", "test", False), ("Loose queries (reported only)", None, True)):
        for name, res in (("v1 key words", v1), ("v2 word meaning", v2)):
            if res is None:
                continue
            if split is None:
                s = dict(n=0, n_none=0, p5=[], r10=[], f1=[], none=None)
                parts = [score(bench, res, sp, True) for sp in ("dev", "test")]
                ns = sum(p["n"] for p in parts)
                avg = lambda k: sum((p[k] or 0) * p["n"] for p in parts) / ns if ns else None
                s = dict(n=ns, p5=avg("p5"), r10=avg("r10"), f1=avg("f1"), none=None)
            else:
                s = score(bench, res, split, loose)
            rows.append((title, name, s))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--v1", action="store_true")
    ap.add_argument("--write-docs", action="store_true")
    a = ap.parse_args()
    bench = load_bench()
    if a.v1:
        run_v1()
    v2 = run_v2(bench)
    v1 = json.load(open(V1))["results"] if os.path.exists(V1) else None
    if a.check:
        fl = json.load(open(FLOOR))
        t = score(bench, v2, "test")
        d = score(bench, v2, "dev")
        bad = []
        if t["f1"] < fl["test_f1"]: bad.append("test F1 %.3f is below the floor %.3f" % (t["f1"], fl["test_f1"]))
        if t["p5"] < fl["test_p5"]: bad.append("test precision@5 %.3f is below the floor %.3f" % (t["p5"], fl["test_p5"]))
        if t["none"] is not None and t["none"] < fl["test_none"]: bad.append("test none-correct %.2f is below the floor %.2f" % (t["none"], fl["test_none"]))
        print("Matcher accuracy: test F1 %.2f (floor %.2f), precision@5 %.2f (floor %.2f), none-correct %s; dev F1 %.2f" % (t["f1"], fl["test_f1"], t["p5"], fl["test_p5"], fmt(t["none"]), d["f1"]))
        for b in bad:
            print("  [FAIL] " + b)
        print("Matcher accuracy: " + ("PASS" if not bad else "FAIL"))
        sys.exit(1 if bad else 0)
    rows = table(bench, v2, v1)
    lines = ["| Queries | Matcher | n | precision@5 | recall@10 | F1 | none-correct |", "|---|---|---|---|---|---|---|"]
    for title, name, s in rows:
        lines.append("| %s | %s | %s | %s | %s | %s | %s |" % (title, name, s["n"], fmt(s["p5"]), fmt(s["r10"]), fmt(s["f1"]), fmt(s["none"]) if s["none"] is not None else "-"))
    print("\n".join(lines))
    nn = {sp: sum(1 for q in bench if q["split"] == sp and q["none"]) for sp in ("dev", "test")}
    print("none queries (the key says nothing in the log): dev %d, test %d" % (nn["dev"], nn["test"]))
    if a.write_docs:
        write_doc(lines, nn)


def write_doc(lines, nn):
    txt = """# Your own option: how accurate is the matcher?

Checked %s against the hand-written answer key `tests/matcher_bench.json` (65 things a viewer might type, each with the
past cases that really are the same kind of US action; written from the case titles, not from the tags).
The key has a **dev** half (used to set the tuning numbers) and a **test** half (never used for tuning). Six queries are
admittedly loose (the key itself says the log has no exact match) and are listed apart.

**v1** is the old key-word reader. **v2** is the word-meaning model plus hard rules (see `docs/METHODOLOGY.md` section 13).

%s

What the columns mean (all averages over queries; none-correct is only for the queries where the key says the log has
nothing like it: dev %d, test %d):

- **precision@5**: of the first 5 cases returned, the share the key lists. v1 lists cases by date, v2 best-first.
- **recall@10**: the share of the key's cases that are in the first 10 returned.
- **F1**: precision and recall of the whole returned set (v2 returns at most 12 cases; v1 returns every case whose tags fit).
- **none-correct**: the share of "nothing like this in the log" queries where the page returned nothing.

Honest limits: the key lists only 1 to 11 cases per query (most 2 to 4), so the numbers move a lot when a single case is
added or removed. The test half was scored after the tuning numbers were frozen; later edits did not change its score. The model understands words, not whole situations. The key is a person's judgement; a few of its
choices are debatable. Each theater's log is small (27 to 98 cases).

Re-run: `cd napor && python3 bench_matcher.py` (v2 only needs numpy). `python3 bench_matcher.py --v1` re-runs the old matcher in a
headless browser (needs node and playwright) and refreshes `tests/matcher_v1_baseline.json`. The weekly build runs
`python3 bench_matcher.py --check`, which fails if the test half falls below `tests/matcher_floor.json`.
""" % (dt.date.today().isoformat(), "\n".join(lines), nn["dev"], nn["test"])
    open(DOC, "w").write(txt)
    print("wrote docs/MATCHER_ACCURACY.md")


if __name__ == "__main__":
    main()
