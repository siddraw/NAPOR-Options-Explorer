"""Regression suite for the "Your own option" matcher (tests/matcher_regress.json): the inputs the four testers typed, each with what a
reasonable reader expects. `result(entry, ths)` runs the Python reference and gives a plain dict; the page's JavaScript gives the same
dict (napor/parity_matcher.js); `check(entry, res)` lists what is wrong. About a quarter of the entries are `holdout`: written before the
fixes and never used to tune anything.

Expectation keys (all optional): moves (all must be read), exclude_moves (not read, and no listed case has one), hold, none, reason,
include_ids, exclude_ids, max_cases, band (allowed Relevance bands), no_move_loose (no move read -> every case Loose), box_read
({box: [values]} must be read), conflict (a box and the words disagree). `nomodel` entries are also run without the word model."""
import json
import os

import matcher_ref as R

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, "..", "tests", "matcher_regress.json")
BLANK = dict(move="", target="", where="", scale="", who="", open="", desc="")


def load():
    return json.load(open(PATH))


def spec_of(e):
    return {**BLANK, **e.get("boxes", {}), "desc": e.get("desc", "")}


def result(e, ths):
    th = ths[e["theater"]]
    m = R.match(spec_of(e), th)
    rd = m["rd"]
    ids = [c["id"] for c in m["cases"]]
    st = [c["strength"] for c in m["cases"]]
    rel = R.relevance(rd, th, ids, st, m["dropped"]) if ids else None
    return dict(ids=ids, strength=st, moves=m["moves"], hold=bool(m["hold"]), reason=m["reason"], sets=rd["sets"], conflict=bool(rd.get("conflict")),
                band=rel and rel["band"], case_moves=[th.by_id[i]["tags"]["move"] if "tags" in th.by_id[i] else "week" for i in ids])


def check(e, r):
    x, bad = e["expect"], []
    if "moves" in x and not set(x["moves"]) <= set(r["moves"]): bad.append("moves %s not in read %s" % (x["moves"], r["moves"]))
    if "exclude_moves" in x:
        both = set(x["exclude_moves"]) & (set(r["moves"]) | set(r["case_moves"]))
        if both: bad.append("moves %s must not appear (read %s, cases %s)" % (sorted(both), r["moves"], sorted(set(r["case_moves"]))))
    if "hold" in x and bool(x["hold"]) != r["hold"]: bad.append("hold should be %s" % x["hold"])
    if "none" in x and bool(x["none"]) == bool(r["ids"]): bad.append("none should be %s but %d cases" % (x["none"], len(r["ids"])))
    if "reason" in x and x["reason"] != r["reason"]: bad.append("reason %s != %s" % (r["reason"], x["reason"]))
    if "include_ids" in x and not set(x["include_ids"]) <= set(r["ids"]): bad.append("missing ids %s (got %s)" % (sorted(set(x["include_ids"]) - set(r["ids"])), r["ids"][:8]))
    if "exclude_ids" in x and set(x["exclude_ids"]) & set(r["ids"]): bad.append("ids %s must not be listed" % sorted(set(x["exclude_ids"]) & set(r["ids"])))
    if "max_cases" in x and len(r["ids"]) > x["max_cases"]: bad.append("%d cases > %d" % (len(r["ids"]), x["max_cases"]))
    if "band" in x and r["band"] is not None and r["band"] not in x["band"]: bad.append("band %s not in %s" % (r["band"], x["band"]))
    if x.get("no_move_loose") and not r["moves"] and any(s != "loose" for s in r["strength"]): bad.append("no move read but a case is rated better than Loose")
    for f, vs in (x.get("box_read") or {}).items():
        if not set(vs) <= set(r["sets"].get(f, [])): bad.append("box %s read as %s, wanted %s" % (f, r["sets"].get(f), vs))
    if x.get("conflict") and not r["conflict"]: bad.append("no box/words conflict reported")
    return bad


# ---------------------------------------------------------------- Python / JavaScript parity (napor/parity_matcher.js gives the same dict)
def view(spec, th):
    """Everything the page's matcher decides for one input, as plain data (the JavaScript twin returns exactly this shape)."""
    m = R.match({**BLANK, **spec}, th)
    rd = m["rd"]
    ids = [c["id"] for c in m["cases"]]
    rel = R.relevance(rd, th, ids, [c["strength"] for c in m["cases"]], m["dropped"]) if ids else None
    return dict(
        ids=ids, sims=[c["sim"] for c in m["cases"]], strength=[c["strength"] for c in m["cases"]], missed=[list(c["missed"]) for c in m["cases"]],
        dropped=list(m["dropped"]), kept=list(m["kept"]), moves=list(m["moves"]), moves_from=m["moves_from"], reason=m["reason"], hold=bool(m["hold"]),
        ranked=bool(m["ranked"]), ordered=bool(m["ordered"]), neg=bool(rd["neg"]), negs=list(rd["negs"]), refrain=bool(rd["refrain"]),
        boxes_context=bool(rd["boxes_context"]), conflict=bool(rd["conflict"]), ptoks=list(rd["ptoks"]), fixes=[list(x) for x in rd["fixes"]], unread=list(rd["unread"]),
        sets={k: list(v) for k, v in rd["sets"].items()},
        fields={f: dict(vals=list(d["vals"]), ignored=list(d["ignored"]), neg=list(d["neg"]), excl=bool(d["excl"]), negated=bool(d["negated"]), used=list(d["used"])) for f, d in rd["fields"].items()},
        rev=[[r["text"], list(r["moves"])] for r in rd["rev"]], lex=[list(x) for x in rd["lex"]], typed=bool(rd["typed"]), any=bool(rd["sets"]) or bool(rd["dtoks"]),
        cue=dict(moves=list(rd["cue"]["moves"]), tier=rd["cue"]["tier"], relief=bool(rd["cue"]["relief"])), covered_words=list(rd["covered_words"]),
        case_moves=[th.by_id[i]["tags"]["move"] if "tags" in th.by_id[i] else "week" for i in ids],
        rel=rel and {k: rel[k] for k in ("n", "close", "pct", "band", "kw_total", "kw_found", "kw_missing", "words")})


def as_result(v):
    """The dict `check` reads, made from a `view` dict (from either side)."""
    return dict(ids=v["ids"], strength=v["strength"], moves=v["moves"], hold=v["hold"], reason=v["reason"], sets=v["sets"], conflict=v["conflict"],
                band=v["rel"] and v["rel"]["band"], case_moves=v["case_moves"])


def diff(py, js, tol=1e-3):
    """What differs between the Python view and the JavaScript one (empty list = same)."""
    bad = []
    for k in py:
        if k == "sims":
            if len(py[k]) != len(js[k]) or any((a is None) != (b is None) or (a is not None and abs(a - b) > tol) for a, b in zip(py[k], js[k])):
                bad.append(("sims", py[k][:3], js[k][:3]))
        elif py[k] != js.get(k):
            bad.append((k, py[k], js.get(k)))
    return bad
