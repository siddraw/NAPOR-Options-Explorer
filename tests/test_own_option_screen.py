"""Screen and flow rules of "Your own option", checked in a real headless browser (node + playwright; skipped when not installed):
the too-few-cases rule (fewer than 3 counted cases shows "Too few cases", no index), personal options listed in Compare as "yours"
but never in the Report card, Tab kept inside an open popup with Escape and focus return, Cancel in edit mode, and the wording rules
(plural agreement, no "undefined" or empty brackets)."""
import json
import re
import shutil
import subprocess

import pytest

from conftest import REPO, EXPLORER

HAVE = shutil.which("node") is not None and shutil.which("npm") is not None


def node_path():
    return subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()


@pytest.mark.skipif(not HAVE, reason="node/playwright not installed")
def test_screen_and_flow_rules():
    import os
    r = subprocess.run(["node", os.path.join(REPO, "napor", "ui_check_own_option_flow.js"), EXPLORER], capture_output=True, text=True,
                       env=dict(os.environ, NODE_PATH=node_path()), timeout=400)
    if "Cannot find module 'playwright'" in r.stderr:
        pytest.skip("playwright not installed")
    assert r.returncode == 0, r.stderr[-800:]
    out = json.loads(r.stdout)
    assert out["fails"] == [], out["fails"]
    assert out["pass"] >= 40


def test_page_source_has_the_rules():
    """Cheap source checks that hold even without a browser: the 3-case minimum, the plural helper, the 12-closest note and the 'not' sentence."""
    src = open(f"{EXPLORER}/index.html", encoding="utf-8").read()
    assert re.search(r"const MINC\s*=\s*3\b", src)
    assert re.search(r"const plural\s*=", src)
    assert "closest are used." in src and re.search(r"MAXC\s*=", src)
    assert "what the US would not do" in src
    assert "Too few cases" in src
