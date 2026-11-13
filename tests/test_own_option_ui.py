"""Playwright check of the real page: the Relevance numbers the viewer sees in the preview, in the option window and on the saved card are the
numbers napor/matcher_ref.py computes, and Relevance never changes a risk number. Skipped when node/playwright are not installed."""
import json
import os
import re
import shutil
import subprocess
import tempfile

import pytest

from conftest import REPO, EXPLORER

import matcher_ref as R

HAVE = shutil.which("node") is not None and shutil.which("npm") is not None
QUERIES = [
    ("u1", "iran", dict(desc="bomb Iranian radar sites")),
    ("u2", "iran", dict(desc="impose sanctions but no strikes")),
    ("u3", "iran", dict(desc="do not strike Iranian nuclear sites")),
    ("u4", "china", dict(desc="do nothing")),
    ("u5", "houthis", dict(move="naval", where="sea", desc="escort ships through the Red Sea")),
    ("u6", "venezuela", dict(move="strike", target="boats")),
    ("u7", "northkorea", dict(desc="hold joint drills with South Korea")),
    ("u8", "iran", dict(desc="leave the nuclear deal")),
]


def plural(n, one):
    return f"{n} {one}" if n == 1 else f"{n} {one}s"


def kw_line(total, found):
    """The key-word sentence the page shows (explorer/index.html relWords); the grammar follows the count."""
    if total == 1:
        lead = "Your 1 key word shows up" if found else "Your 1 key word does not show up"
    elif found == 0:
        lead = f"None of your {total} key words show up"
    else:
        lead = f"{found} of your {total} key words {'shows' if found == 1 else 'show'} up"
    return lead + " in the titles, kinds or tags of these cases."


def node_path():
    return subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()


@pytest.mark.skipif(not HAVE, reason="node/playwright not installed")
def test_relevance_in_the_window_matches_the_python_numbers():
    with tempfile.TemporaryDirectory() as tmp:
        qf, of = os.path.join(tmp, "q.json"), os.path.join(tmp, "o.json")
        json.dump([dict(id=i, theater=t, spec=s) for i, t, s in QUERIES], open(qf, "w"))
        r = subprocess.run(["node", os.path.join(REPO, "napor", "ui_check_own_option.js"), EXPLORER, qf, of], capture_output=True, text=True, env=dict(os.environ, NODE_PATH=node_path()))
        if "Cannot find module 'playwright'" in r.stderr:
            pytest.skip("playwright not installed")
        assert r.returncode == 0, r.stderr[-800:]
        js = json.load(open(of))
    assert js["errs"] == []
    _, ths = R.load_all()
    for i, t, spec in QUERIES:
        got = js["res"][i]
        m = R.match({**dict(move="", target="", where="", scale="", who="", open="", desc=""), **spec}, ths[t])
        if not m["cases"]:
            want = "has no weeks with no new US move for this conflict, so there is nothing to count" if m["hold"] else "has no past cases like this, so there is nothing to count"
            assert want in got["preview"], (i, got["preview"])
            assert "relbox" not in got or got.get("relbox") is None
            continue
        rel = R.relevance(m["rd"], ths[t], [c["id"] for c in m["cases"]], [c["strength"] for c in m["cases"]])
        if m["hold"]:                                   # hold weeks are never rated close: the page says N/A
            for where in ("preview", "relbox"):
                assert "Relevance: N/A for hold weeks" in got[where], (i, got[where])
            assert "Relevance: N/A for hold weeks" in got["card"], (i, got["card"])
            assert "key words" not in got["relbox"], (i, got["relbox"])
            continue
        if rel["band"] == "few":
            want = f"only {plural(rel['n'], 'counted case')}"
        else:
            want = f"Relevance: {rel['close']} of {rel['n']} counted cases {'is' if rel['close'] == 1 else 'are'} close or very close ({rel['pct']}%)"
        assert want in got["preview"], (i, want, got["preview"])
        assert want in got["relbox"], (i, want, got["relbox"])
        if rel["kw_total"]:
            kw = kw_line(rel["kw_total"], rel["kw_found"])
            assert kw in got["preview"] and kw in got["relbox"], (i, kw, got["relbox"])
        if rel["band"] != "few":
            assert {"strong": "Strong fit", "moderate": "Moderate fit", "weak": "Weak fit — read the numbers with care"}[rel["band"]] in got["relbox"]
            assert re.search(r"Relevance: (Strong|Moderate|Weak) fit \(%d%%\)" % rel["pct"], got["card"]), (i, got["card"])
        else:
            assert "too few" in got["card"]
        assert "not how risky it is" in got["relbox"]
        assert got["rel"]["close"] == rel["close"] and got["rel"]["n"] == rel["n"]
        assert got["risk"]["hold"] == bool(m["hold"])
        if got["risk"]["raw"] is not None:
            assert (f"Risk index {round(got['risk']['raw'] * 100)}%") in got["cardText"]
