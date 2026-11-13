"""Negation ("not") in the "Your own option" matcher. The word model cannot be told "not", so the matcher has an explicit rule layer
(napor/matcher_ref.py find_negations / split_negation; the page's JavaScript is the twin and tests/test_matcher_parity.py checks both agree).

Two sets of phrasings:
  EXAMPLES  the phrasings the rules were written and tuned with.
  HELD-OUT  tests/matcher_negation_heldout.json, written BEFORE the rules and never used to tune them.
The strict checks (a negated action is never read as a move; a say/declare sentence stays a statement) must hold for every phrasing; the overall
pass rate on the held-out set must stay at or above HELDOUT_FLOOR (first run: 33 of 34, the one miss is a cue-table gap: "talk" is not a talks cue)."""
import json
import os

import pytest

import matcher_ref as R
from conftest import REPO

EXAMPLES = [
    {"id": "e-01", "theater": "iran", "text": "do not strike Iranian nuclear sites", "hold": True, "never": ["strike", "raid"]},
    {"id": "e-02", "theater": "iran", "text": "avoid sending more carriers", "hold": True, "never": ["deployment"]},
    {"id": "e-03", "theater": "northkorea", "text": "talk to North Korea without new sanctions", "hold": False, "never": ["sanctions"]},
    {"id": "e-04", "theater": "iran", "text": "negotiate instead of striking", "hold": False, "moves": ["talks"], "never": ["strike", "raid"]},
    {"id": "e-05", "theater": "iran", "text": "won't rule out strikes", "hold": False, "moves": ["strike"]},
    {"id": "e-06", "theater": "venezuela", "text": "do not capture Maduro", "hold": True, "never": ["raid", "legal"]},
    {"id": "e-07", "theater": "china", "text": "don't sell arms to Taiwan", "hold": True, "never": ["arms"]},
    {"id": "e-08", "theater": "china", "text": "sell arms to Taiwan but don't announce it", "hold": False, "moves": ["arms"], "never": ["statement"]},
    {"id": "e-09", "theater": "northkorea", "text": "do not hold joint drills with South Korea", "hold": True, "never": ["drill"]},
    {"id": "e-10", "theater": "venezuela", "text": "no boat strikes", "hold": True, "never": ["strike"]},
    {"id": "e-11", "theater": "iran", "text": "stop bombing but do not leave the region", "hold": False, "moves": ["talks"], "never": ["withdrawal"]},
    {"id": "e-12", "theater": "china", "text": "no new tariffs on China", "hold": True, "never": ["sanctions"]},
    {"id": "e-13", "theater": "houthis", "text": "escort ships but avoid striking Yemen", "hold": False, "moves": ["naval"], "never": ["strike"]},
    {"id": "e-14", "theater": "iran", "text": "refuse to negotiate with Iran", "hold": True, "never": ["talks"]},
    {"id": "e-15", "theater": "iran", "text": "hold off on new sanctions", "hold": True, "never": ["sanctions"]},
    {"id": "e-16", "theater": "iran", "text": "stay out of the war", "hold": True},
    {"id": "e-17", "theater": "iran", "text": "keep troops in Iraq and do not withdraw", "hold": False, "never": ["withdrawal"]},
    {"id": "e-18", "theater": "venezuela", "text": "negotiate with Caracas rather than strike boats", "hold": False, "moves": ["talks"], "never": ["strike"]},
    {"id": "e-19", "theater": "northkorea", "text": "offer talks, not new sanctions", "hold": False, "moves": ["talks"], "never": ["sanctions"]},
    {"id": "e-20", "theater": "iran", "text": "do not rule out a strike", "hold": False, "moves": ["strike"]},
    {"id": "e-21", "theater": "china", "text": "not ruling out new sanctions", "hold": False, "moves": ["sanctions"]},
    {"id": "e-22", "theater": "iran", "text": "say the US will not strike Iran", "statement": True},
    {"id": "e-23", "theater": "iran", "text": "declare it will not seek regime change", "statement": True},
    {"id": "e-24", "theater": "houthis", "text": "withdraw troops, do not send reinforcements", "hold": False, "moves": ["withdrawal"], "never": ["deployment"]},
    {"id": "e-25", "theater": "venezuela", "text": "sanction officials instead of sending warships", "hold": False, "moves": ["sanctions"], "never": ["deployment", "naval"]},
    {"id": "e-26", "theater": "iran", "text": "do nothing for now", "hold": True},
    {"id": "e-27", "theater": "northkorea", "text": "take no action", "hold": True},
    {"id": "e-28", "theater": "china", "text": "neither strike nor sanction China", "hold": True, "never": ["strike", "sanctions"]},
    {"id": "e-29", "theater": "iran", "text": "don't deploy a carrier to the Gulf", "hold": True, "never": ["deployment"]},
    {"id": "e-30", "theater": "venezuela", "text": "no strikes, just sanctions", "hold": False, "moves": ["sanctions"], "never": ["strike"]},
    {"id": "e-31", "theater": "houthis", "text": "We would not send ground troops into Yemen", "hold": True, "never": ["deployment", "raid"]}
]
HELDOUT = json.load(open(os.path.join(REPO, "tests", "matcher_negation_heldout.json")))["items"]
HELDOUT_FLOOR = 0.90


@pytest.fixture(scope="module")
def ths():
    return R.load_all()[1]


def verdict(it, ths):
    """-> list of problems (empty = the phrasing is read as expected)."""
    th = ths[it["theater"]]
    m = R.match(dict(desc=it["text"]), th)
    rd, mv, bad = m["rd"], set(m["moves"]), []
    if it.get("statement"):
        if rd["neg"] or m["hold"]:
            bad.append("a say/declare sentence must stay a statement")
        return bad
    if bool(m["hold"]) != bool(it.get("hold")):
        bad.append(f"hold={m['hold']}")
    if it.get("hold"):
        if mv:
            bad.append(f"moves {sorted(mv)} read for a hold")
    elif not set(it.get("moves", [])) <= mv:
        bad.append(f"moves {sorted(mv)} lack {it.get('moves')}")
    if mv & set(it.get("never", [])):
        bad.append(f"negated action read as a move: {sorted(mv & set(it['never']))}")
    return bad


def test_there_are_enough_phrasings_across_five_theaters():
    both = EXAMPLES + HELDOUT
    assert len(EXAMPLES) >= 25 and len(HELDOUT) >= 25
    assert {x["theater"] for x in both} == set(R.THEATERS)


def test_examples_all_pass(ths):
    fails = {x["id"]: verdict(x, ths) for x in EXAMPLES if verdict(x, ths)}
    assert not fails, fails


def test_heldout_pass_rate(ths):
    fails = {x["id"]: verdict(x, ths) for x in HELDOUT if verdict(x, ths)}
    rate = 1 - len(fails) / len(HELDOUT)
    print(f"held-out: {len(HELDOUT) - len(fails)} of {len(HELDOUT)} ({rate:.0%}); misses: {fails}")
    assert rate >= HELDOUT_FLOOR, fails


def test_a_negated_action_is_never_read_as_a_move_on_either_set(ths):
    """The safety property: nothing the viewer said the US would NOT do may become a move filter. Held-out misses may only be missing moves."""
    for x in EXAMPLES + HELDOUT:
        if x.get("never"):
            m = R.match(dict(desc=x["text"]), ths[x["theater"]])
            assert not set(m["moves"]) & set(x["never"]), (x["id"], x["text"], m["moves"])


def test_say_or_declare_stays_a_statement(ths):
    for t in ["say the US does not support Taiwan independence", "declare that the US will not strike Iran", "publicly pledge never to invade"]:
        rd = R.read_spec(dict(desc=t), ths["iran"].matcher, set())
        assert not rd["neg"], t


def test_the_united_states_is_not_a_say_word(ths):
    rd = R.read_spec(dict(desc="the United States would not strike"), ths["iran"].matcher, set())
    assert rd["neg"] and rd["refrain"]


def test_double_negatives_are_positive(ths):
    for t, mv in [("won't rule out strikes", "strike"), ("do not rule out a strike", "strike"), ("not ruling out new sanctions", "sanctions"), ("we will not refuse talks", "talks")]:
        m = R.match(dict(desc=t), ths["iran"])
        assert not m["hold"] and mv in m["moves"] and not m["rd"]["neg"], t


def test_not_only_is_not_a_negation(ths):
    assert not R.match(dict(desc="not only sanction Iran but also strike it"), ths["iran"])["rd"]["neg"]


def test_scope_stops_at_a_comma_or_but(ths):
    m = R.match(dict(desc="do not strike, impose sanctions"), ths["iran"])
    assert m["moves"] == ["sanctions"] and not m["hold"]
    m = R.match(dict(desc="impose sanctions but no strikes"), ths["iran"])
    assert m["moves"] == ["sanctions"]
    strikes = {x["id"] for x in ths["iran"].cases if x["tags"]["move"] == "strike"}
    assert not strikes & {c["id"] for c in m["cases"]}


def test_only_negated_means_the_us_holds_back_and_uses_the_hold_weeks(ths):
    for tid in R.THEATERS:
        th = ths[tid]
        m = R.match(dict(desc="do not strike anyone"), th)
        assert m["hold"] and m["moves_from"] == "hold"
        assert [c["id"] for c in m["cases"]] == [w["id"] for w in sorted(th.holds, key=lambda w: (w["date"], w["id"]))]
        assert all(c["strength"] == "loose" for c in m["cases"])
        assert m["reason"] == (None if th.holds else "nothing")
    assert len(ths["iran"].holds) == 11 and ths["china"].holds == []


def test_hold_weeks_are_the_cases_option_a_counts(ths):
    for tid in R.THEATERS:
        d = json.load(open(os.path.join(REPO, "explorer", "data", tid + ".json")))
        a = [o for o in d["options"] if o.get("is_hold")][0]
        assert {c["id"] for c in a["cases"] if c.get("week")} == {w["id"] for w in ths[tid].holds}


def test_negated_words_are_not_searched(ths):
    a = R.match(dict(desc="negotiate with Iran"), ths["iran"])
    b = R.match(dict(desc="negotiate with Iran rather than bombing strike missile attack"), ths["iran"])
    assert [c["id"] for c in a["cases"]] == [c["id"] for c in b["cases"]]


def test_boxes_win_over_a_negated_description(ths):
    m = R.match(dict(move="sanctions", desc="do not strike"), ths["iran"])
    assert not m["hold"] and m["moves"] == ["sanctions"] and m["rd"]["neg"]


def test_a_bare_not_reads_nothing(ths):
    m = R.match(dict(desc="do not"), ths["iran"])
    assert not m["hold"] and m["cases"] == [] and m["reason"] == "negation"


def test_requests_the_log_has_no_cases_for_return_nothing(ths):
    for tid, t in [("iran", "leave the nuclear deal"), ("iran", "sell Patriot batteries to Jordan")]:
        assert R.match(dict(desc=t), ths[tid])["cases"] == []
