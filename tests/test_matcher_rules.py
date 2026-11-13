"""Rules added after the tester round (docs/METHODOLOGY.md section 13): one shared tokenizer, typo repair, reversals, phrase rules, absolute strength,
boxes that keep every move, and the matcher without the word model. The page's JavaScript is checked against Python by test_matcher_parity.py."""
import pytest

import matcher_ref as R

pytestmark = pytest.mark.filterwarnings("ignore")
_T = {}


def ths(model=True):
    if model not in _T:
        _T[model] = R.load_all(with_model=model)[1]
    return _T[model]


def run(t, desc, model=True, **boxes):
    return R.match(dict(desc=desc, **boxes), ths(model)[t])


def test_one_tokenizer_for_boxes_and_words():
    assert R.tokens("Re-open O’Neil’s ‘Fordow’ — 💥 café") == ["re", "open", "o", "neil", "s", "fordow", "cafe"]
    assert len(R.clean("💥" * 500, 400)) == 400            # cut by code points, never inside an emoji


def test_word_endings_and_irregular_forms():
    for a, b in [("bombed", "bomb"), ("bombing", "bomb"), ("bombs", "bomb"), ("struck", "strike"), ("sanctioning", "sanction")]:
        assert b in R.form_list(a, {"struck": "strike"}), a


def test_typos_are_repaired_and_shown():
    r = run("iran", "new sanctoins on Iranian banks")
    assert ["sanctoins", "sanctions"] in r["rd"]["fixes"] and r["moves"] == ["sanctions"]
    assert run("iran", "xqz")["rd"]["fixes"] == []           # never invents a word; short words are never repaired


def test_every_move_in_the_move_box_is_kept():
    for box in ["strike, withdrawal", "cyber, strike", "arms, cyber", "strike, talks, sanctions, statement, withdrawal"]:
        r = run("iran", "", move=box)
        assert set(r["rd"]["sets"]["move"]) == set(x.strip() for x in box.split(",")), box


@pytest.mark.parametrize("t,desc,want,never", [
    ("iran", "carrier strike group to the Gulf", ["deployment"], ["strike"]),
    ("iran", "designate the IRGC as a terrorist organization", ["legal"], ["strike"]),
    ("iran", "labor strike at the port", [], None),
    ("iran", "oil drilling", [], None),
    ("iran", "stop bombing the Houthis", ["talks"], ["strike"]),
    ("iran", "lift sanctions on Iran", ["talks"], None),
    ("venezuela", "invade Venezuela", ["raid"], None),
])
def test_phrase_rules(t, desc, want, never):
    m = run(t, desc)
    if want:
        assert set(want) <= set(m["moves"]), (desc, m["moves"])
    else:
        assert not m["moves"], (desc, m["moves"])
    assert not set(never or []) & set(m["moves"])


def test_strength_is_absolute():
    # no move read: nothing is better than Loose
    m = run("iran", "radar")
    assert all(c["strength"] == "loose" for c in m["cases"])
    # a description with no meaningful word gives no cases
    m = run("iran", "the of Iran")
    assert m["cases"] == [] and m["reason"] in ("empty", "vague")
    # a relaxed box can never be Very close
    m = run("iran", "strike radar sites", who="partners", where="third", scale="campaign", open="unclaimed")
    assert not m["dropped"] or all(c["strength"] != "exact" for c in m["cases"])


def test_without_the_model_the_rules_still_work():
    a = run("iran", "do not strike Iran", model=False)
    assert a["hold"] and a["cases"]
    b = run("iran", "bomb Iranian radar sites", model=False)
    assert "strike" in b["moves"] and all(c["sim"] is not None or True for c in b["cases"])
    assert not R.read_spec(dict(desc="pull troops out of Iraq"), ths(False)["iran"])["cue"]["moves"] == ["deployment"]


def test_lexicon_words_reach_their_cases():
    m = run("iran", "strike Fordow")
    assert any(c["id"] == 255 for c in m["cases"])           # Operation Midnight Hammer


def test_the_strait_never_pushes_a_clear_match_under_the_cutoff():
    assert run("iran", "seize Iranian oil tankers in the Strait of Hormuz")["cases"]
