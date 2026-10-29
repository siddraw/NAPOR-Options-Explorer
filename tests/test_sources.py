"""Source labels must name the site the link points to.

Approved rule (2026-10-29): label and link only the source the event was read from. If the outlet label names a
well-known outlet (AP, Reuters, Al Jazeera, CENTCOM, ...) the URL must be on that outlet's own site. A copy read on
another site is fine, but the label must say so with "via" (for example "AP (via KPAX)").

The test walks every source in every theater (audit_sources.py, data.py, prewar*.py, theaters/*/events*.py) and the
review queue, and fails on any label that names a known outlet, points at a different domain and has no "via".
Run `python tests/test_sources.py` to print the mismatches.
"""
import importlib
import json
import os
import re
import sys
from urllib.parse import urlparse

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAPOR = os.path.join(REPO, "napor")
if NAPOR not in sys.path:
    sys.path.insert(0, NAPOR)

# Every module that holds source entries (dicts with 'outlet' and 'url').
MODULES = ["audit_sources", "data", "prewar", "prewar_early",
           "theaters.houthis.events_2014", "theaters.houthis.events_early", "theaters.houthis.events_late",
           "theaters.northkorea.events", "theaters.northkorea.events_pre2017",
           "theaters.china.events", "theaters.china.events_pre2019",
           "theaters.venezuela.events", "theaters.venezuela.events_pre2019"]

# Leading outlet name in a label -> domains that count as that outlet's own site (includes the legit aliases).
# Order matters: the first pattern that matches the start of the label is used.
OUTLET_DOMAINS = [
    (r"Bloomberg Government", ["bgov.com", "bloomberg.com"]),
    (r"(?:AP|Associated Press)\b", ["apnews.com", "associatedpress.com", "ap.org"]),
    (r"Reuters", ["reuters.com"]),
    (r"AFP", ["afp.com"]),
    (r"AAP", ["aap.com.au"]),
    (r"BBC", ["bbc.com", "bbc.co.uk"]),
    (r"NPR", ["npr.org"]),
    (r"PBS", ["pbs.org"]),
    (r"(?:The )?New York Times|NYT", ["nytimes.com", "nyti.ms"]),
    (r"Wall Street Journal|WSJ", ["wsj.com"]),
    (r"(?:The )?Washington Post", ["washingtonpost.com"]),
    (r"Bloomberg", ["bloomberg.com"]),
    (r"Financial Times", ["ft.com"]),
    (r"CBS News", ["cbsnews.com"]),
    (r"ABC News", ["abcnews.go.com", "abcnews.com"]),
    (r"NBC News", ["nbcnews.com"]),
    (r"CNN", ["cnn.com"]),
    (r"Al Jazeera", ["aljazeera.com", "aljazeera.net"]),
    (r"Al Arabiya", ["alarabiya.net"]),
    (r"Axios", ["axios.com"]),
    (r"Politico", ["politico.com"]),
    (r"Times of Israel", ["timesofisrael.com"]),
    (r"Haaretz", ["haaretz.com"]),
    (r"Israel Hayom", ["israelhayom.com"]),
    (r"USNI News", ["usni.org"]),
    (r"Defense News", ["defensenews.com"]),
    (r"Breaking Defense", ["breakingdefense.com"]),
    (r"The War Zone", ["twz.com", "thedrive.com"]),
    (r"Stars and Stripes", ["stripes.com"]),
    (r"Army Times", ["armytimes.com"]),
    (r"TIME\b|Time\b", ["time.com"]),
    (r"Boston Globe", ["bostonglobe.com"]),
    (r"Euronews", ["euronews.com"]),
    (r"Tasnim", ["tasnimnews.com", "tasnimnews.ir"]),
    (r"IRNA", ["irna.ir"]),
    # official and primary sources
    (r"Treasury", ["treasury.gov"]),
    (r"State Department", ["state.gov"]),
    (r"White House", ["whitehouse.gov", "archives.gov", "reaganlibrary.gov"]),
    (r"CENTCOM", ["centcom.mil"]),
    (r"NAVCENT", ["cusnc.navy.mil", "navy.mil", "centcom.mil"]),
    (r"INDOPACOM", ["pacom.mil", "indopacom.mil"]),
    (r"DoD|Army\.mil", ["defense.gov", "war.gov", "army.mil", "af.mil", "navy.mil", "usfk.mil", "centcom.mil"]),
    (r"Justice Department", ["justice.gov"]),
    (r"UN\b", ["un.org"]),
    (r"IAEA", ["iaea.org"]),
    (r"Congress", ["congress.gov", "govinfo.gov"]),
    (r"CRS", ["congress.gov", "crsreports.congress.gov"]),
    (r"KEDO", ["kedo.org"]),
    (r"Commerce", ["bis.gov", "commerce.gov"]),
    (r"Japan Ministry of Defense", ["mod.go.jp"]),
    (r"Petra", ["petra.gov.jo"]),
]
OUTLET_DOMAINS = [(re.compile(p), d) for p, d in OUTLET_DOMAINS]


def host_of(url):
    h = urlparse(url or "").netloc.lower()
    return h[4:] if h.startswith("www.") else h


def on_domain(host, domains):
    return any(host == d or host.endswith("." + d) for d in domains)


def label_problem(label, url):
    """None if the label is honest about the URL, else a short reason."""
    if not url or not label:
        return None
    if re.search(r"\bvia\b", label, re.I):
        return None
    for pat, domains in OUTLET_DOMAINS:
        m = pat.match(label)
        if m:
            host = host_of(url)
            if on_domain(host, domains):
                return None
            return f"label names {m.group(0)!r} but the link is on {host} and the label has no 'via'"
    return None


def _walk(obj, key, where, out, depth=0):
    if depth > 6:
        return
    if isinstance(obj, dict):
        if "outlet" in obj and "url" in obj:
            out.append((where, key, obj))
            return
        for k, v in obj.items():
            _walk(v, k if isinstance(k, int) else key, where, out, depth + 1)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            _walk(v, key, where, out, depth + 1)


def collect_sources():
    """Every (where, event id, source dict) in the repo's source tables and the review queue."""
    out = []
    for m in MODULES:
        mod = importlib.import_module(m)
        for name, val in vars(mod).items():
            if not name.startswith("__"):
                _walk(val, None, f"{m}.{name}", out)
    q = json.load(open(os.path.join(NAPOR, "napor_review_queue.json")))
    _walk(q, None, "napor_review_queue.json", out)
    return out


def mismatches():
    seen, rows = set(), []
    for where, key, s in collect_sources():
        why = label_problem(s["outlet"], s["url"])
        if why and (s["outlet"], s["url"]) not in seen:
            seen.add((s["outlet"], s["url"]))
            rows.append((key, s["outlet"], s["url"], why, where))
    return rows


# ---- the check itself works --------------------------------------------------------------------------
@pytest.mark.parametrize("label,url,ok", [
    ("New York Times", "https://www.nytimes.com/2026/01/05/x.html", True),
    ("New York Times", "https://www.bostonglobe.com/2026/01/05/x/", False),
    ("New York Times (via Boston Globe)", "https://www.bostonglobe.com/2026/01/05/x/", True),
    ("AP (via KPAX)", "https://www.kpax.com/x", True),
    ("AP", "https://www.kpax.com/x", False),
    ("Reuters (wire copy republished by The Star)", "https://www.thestar.com.my/x", False),
    ("AP", "https://apnews.com/article/x", True),
    ("BBC News", "https://www.bbc.co.uk/news/x", True),
    ("Treasury (press release)", "https://home.treasury.gov/news/x", True),
    ("Treasury (press release)", "https://content.govdelivery.com/x", False),
    ("CRS report", "https://www.everycrsreport.com/reports/RL1.html", False),
    ("CRS report (via everycrsreport.com)", "https://www.everycrsreport.com/reports/RL1.html", True),
    ("Some local paper", "https://example.com/x", True),
])
def test_label_check_behaves(label, url, ok):
    assert (label_problem(label, url) is None) == ok


# ---- the real data -----------------------------------------------------------------------------------
def test_sources_were_found():
    assert len(collect_sources()) > 2000


def test_every_outlet_label_matches_its_link():
    bad = mismatches()
    lines = [f"  event {k}: {o!r} -> {u}  ({why})" for k, o, u, why, _ in bad]
    assert not bad, "outlet label names a known outlet but the link is on another site (add 'via <site>' or fix the label):\n" + "\n".join(lines)


if __name__ == "__main__":
    for k, o, u, why, where in mismatches():
        print(f"{k}\t{o}\t{u}\t{where}")
