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

HAVE = shutil.which("node") is not None and shutil.which("npm") is not None


def node_path():
    return subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()


def specs():
    bench = json.load(open(os.path.join(REPO, "tests", "matcher_bench.json")))
    out = [dict(id=q["id"], theater=q["theater"], spec=dict(desc=q["text"])) for q in bench]
    out += json.load(open(os.path.join(REPO, "tests", "matcher_parity_extra.json")))
    return out


@pytest.mark.skipif(not HAVE, reason="node/playwright not installed")
def test_js_and_python_matchers_agree():
    sp = specs()
    assert len(sp) >= 40
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
    model, ths = R.load_all()
    bad = []
    for q in sp:
        py = R.match({**dict(move="", target="", where="", scale="", who="", open="", desc=""), **q["spec"]}, ths[q["theater"]])
        j = js["res"][q["id"]]
        pid = [c["id"] for c in py["cases"]]
        if pid != j["ids"]:
            bad.append((q["id"], "ids", pid, j["ids"])); continue
        for c, s in zip(py["cases"], j["sims"]):
            if c["sim"] is not None and abs(c["sim"] - s) > 1e-3:
                bad.append((q["id"], "score", c["id"], c["sim"], s))
        if [c["strength"] for c in py["cases"]] != j["strength"]:
            bad.append((q["id"], "strength"))
    assert not bad, bad[:5]
