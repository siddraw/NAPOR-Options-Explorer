"""The page's JavaScript matcher and napor/matcher_ref.py (Python) must give the same ranked case ids and nearly the
same scores. Runs the page in a headless browser (node + playwright); skipped when those are not installed."""
import json
import os
import shutil
import subprocess
import tempfile

import pytest

from conftest import REPO, EXPLORER

import matcher_ref as R
import matcher_regress as G

HAVE = shutil.which("node") is not None and shutil.which("npm") is not None


def node_path():
    return subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()


def specs():
    bench = json.load(open(os.path.join(REPO, "tests", "matcher_bench.json")))
    out = [dict(id=q["id"], theater=q["theater"], spec=dict(desc=q["text"])) for q in bench]
    out += json.load(open(os.path.join(REPO, "tests", "matcher_parity_extra.json")))
    for fn in ("matcher_negation_heldout.json",):          # every held-out negation phrasing is also a parity query
        out += [dict(id=q["id"], theater=q["theater"], spec=dict(desc=q["text"])) for q in json.load(open(os.path.join(REPO, "tests", fn)))["items"]]
    return out


def run_js(sp):
    with tempfile.TemporaryDirectory() as tmp:
        qf, of = os.path.join(tmp, "q.json"), os.path.join(tmp, "o.json")
        json.dump(sp, open(qf, "w"))
        r = subprocess.run(["node", os.path.join(REPO, "napor", "parity_matcher.js"), EXPLORER, qf, of], capture_output=True, text=True,
                           env=dict(os.environ, NODE_PATH=node_path()))
        if "Cannot find module 'playwright'" in r.stderr:
            pytest.skip("playwright not installed")
        assert r.returncode == 0, r.stderr[-800:]
        js = json.load(open(of))
    assert js["errs"] == []
    return js["res"]


_TH = {}


def theaters(nomodel):
    if nomodel not in _TH:
        _TH[nomodel] = R.load_all(with_model=not nomodel)[1]
    return _TH[nomodel]


def compare(sp, js):
    bad = []
    for q in sp:
        py = G.view(q["spec"], theaters(bool(q.get("nomodel")))[q["theater"]])
        d = G.diff(py, js[q["id"]])
        if d:
            bad.append((q["id"], q["spec"], d[:2]))
    return bad


@pytest.mark.skipif(not HAVE, reason="node/playwright not installed")
def test_js_and_python_matchers_agree():
    sp = specs()
    assert len(sp) >= 100
    bad = compare(sp, run_js(sp))
    assert not bad, bad[:5]


@pytest.mark.skipif(not HAVE, reason="node/playwright not installed")
def test_js_and_python_agree_without_the_model():
    """The word-meaning model did not load: the rules and the key words still work, and both sides give the same answer."""
    sp = [dict(q, id="nm-" + q["id"], nomodel=True) for q in specs()[::3]]
    bad = compare(sp, run_js(sp))
    assert not bad, bad[:5]


@pytest.mark.skipif(not HAVE, reason="node/playwright not installed")
def test_regress_suite_in_python_and_javascript():
    """tests/matcher_regress.json: every entry passes in the Python reference and in the page, and both give the same answer."""
    ents = G.load()
    assert len(ents) >= 150 and sum(1 for e in ents if e.get("holdout")) >= 0.2 * len(ents)
    sp = [dict(id=e["id"], theater=e["theater"], spec=G.spec_of(e), nomodel=bool(e.get("nomodel"))) for e in ents]
    js = run_js(sp)
    bad, py_bad, js_bad = compare(sp, js), [], []
    ths = theaters(False)
    for e, q in zip(ents, sp):
        py = G.view(q["spec"], theaters(q["nomodel"])[q["theater"]])
        if G.check(e, G.as_result(py)): py_bad.append((e["id"], e["desc"], G.check(e, G.as_result(py))))
        if G.check(e, G.as_result(js[e["id"]])): js_bad.append(e["id"])
    assert not bad, bad[:5]
    assert set(i for i, *_ in py_bad) == set(js_bad)
    rate = 1 - len(py_bad) / len(ents)
    floor = json.load(open(os.path.join(REPO, "tests", "matcher_floor.json"))).get("regress", 0.0)
    assert rate >= floor, (rate, floor, py_bad[:6])


def fuzz_inputs(seed=20261113, n=1200):
    """Random boxes + descriptions (words from the cue lists, case titles, typos, numbers, hyphens, apostrophes, curly quotes, emoji, non-English text)."""
    import random
    rnd = random.Random(seed)
    words = ["strike", "bomb", "bombed", "sanctions", "sanctoins", "lift", "stop", "not", "don't", "never", "without", "troops", "withdraw", "talks", "deal", "ceasefire", "drills", "exercises",
             "navy", "destroyer", "strait", "tanker", "seize", "oil", "drone", "missile", "nuclear", "sites", "leaders", "kill", "capture", "Maduro", "Fordow", "Hormuz", "Kharg", "THAAD", "OFAC", "designate",
             "covert", "secretly", "openly", "big", "small", "allies", "coast", "inside", "campaign", "single", "says", "will", "the", "of", "and", "or", "N/A", "none", "x", "ab", "iran", "houthis", "china",
             "taiwan", "korea", "venezuela", "carrier", "group", "visit", "meet", "arms", "sell", "cyber", "hack", "embassy", "close", "tariffs", "labor", "strike!", "re-open", "state-owned", "o'neil", "d\u2019accord",
             "\U0001f4a5", "\u00e9t\u00e9", "\u4e2d\u56fd", "caf\u00e9", "123", "---", "\u201cquoted\u201d", "(maybe)", "a/b", "&amp;", "<b>"]
    out, i = [], 0
    ths = ["iran", "houthis", "northkorea", "china", "venezuela"]
    while len(out) < n:
        i += 1
        spec = dict(desc=" ".join(rnd.choice(words) for _ in range(rnd.randint(0, 9))) + rnd.choice(["", ".", ", but not " + rnd.choice(words), "\u2026"]))
        for f in ("move", "target", "where", "scale", "who", "open"):
            if rnd.random() < 0.35:
                spec[f] = ", ".join(rnd.choice(words) for _ in range(rnd.randint(1, 3)))
        out.append(dict(id="fz-%d" % i, theater=rnd.choice(ths), spec=spec, nomodel=(i % 7 == 0)))
    return out


@pytest.mark.skipif(not HAVE, reason="node/playwright not installed")
def test_fuzz_parity_1200_random_inputs():
    """A seeded random sweep: the page and the Python reference agree on every field for 1200 inputs (boxes + description, emoji, hyphens, curly quotes, typos, non-English words)."""
    sp = fuzz_inputs()
    bad = compare(sp, run_js(sp))
    assert not bad, bad[:5]
