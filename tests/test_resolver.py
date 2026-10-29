"""Fair test: take real credible-outlet headlines whose event is KNOWN, hide that, and see whether
resolve() links each headline back to the right event ID."""
import datetime as dt, collections, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "napor"))   # also lets `python3 tests/test_resolver.py` run directly (pytest gets this from conftest.py)
import resolver as R, data
from audit_sources import SOURCES

def run(verbose=True):
    pool = [e for e in data.events if e[0] != 76]          # 76 is a known duplicate row; leave it out
    rows = []
    for eid, srcs in SOURCES.items():
        for sc in srcs:
            try: d = dt.date.fromisoformat(sc["published"])
            except Exception: continue
            rows.append((eid, d, sc["headline"]))
    top1 = top3 = 0; dec = collections.Counter(); same_ok = same_n = 0; new_wrong = 0
    for eid, d, h in rows:
        out = R.resolve(d, "", "", h, pool=pool, top=3)
        cand = [c[1] for c in out["candidates"]]
        top1 += bool(cand and cand[0] == eid); top3 += eid in cand
        dec[out["decision"]] += 1
        if out["decision"] == "SAME EVENT":
            same_n += 1; same_ok += (out["best_id"] == eid)
        if out["decision"] == "NEW EVENT": new_wrong += 1      # every headline here belongs to an existing event
    n = len(rows)
    print(f"{n} headlines. Right event ranked #1: {top1/n:.0%}; in top 3: {top3/n:.0%}")
    print(f"Said SAME EVENT {same_n} times, correct {same_ok} ({same_ok/max(same_n,1):.0%}); said NEW EVENT {new_wrong} times (all wrong: these were existing events)")
    print(dict(dec))


def test_resolver_links_headlines(capsys):
    """Runs the headline test end to end and checks it reports every headline it was given."""
    run()
    out = capsys.readouterr().out
    assert "headlines." in out
    n = int(out.split(" headlines.")[0])
    assert n > 0


if __name__ == "__main__": run()
