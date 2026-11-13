"""The fixed move rules of the "Your own option" matcher (action_tags.CUES): they read clear move words correctly,
keep opposites apart, and the page data carries them with the theater's neutral words and the tuning numbers."""
import pytest

import action_tags as A
import matcher_ref as R
from conftest import THEATER_IDS, load_export

M = dict(A.page_vocab("iran"))
_T = {}


def _ths():
    if not _T:
        _T.update(R.load_all(with_model=False)[1])
    return _T


def moves(text, names=False):
    return R.read_move(R.tokens(text), M, names)["moves"]


@pytest.mark.parametrize("text,want", [
    ("pull troops out of Iraq", ["withdrawal"]),
    ("withdraw forces from the region", ["withdrawal"]),
    ("reduce the number of troops", ["withdrawal"]),
    ("send more troops to the Middle East", ["deployment"]),
    ("sell Patriot batteries to Jordan", ["arms"]),
    ("approve an arms sale to Taiwan", ["arms"]),
    ("kill an IRGC general", ["strike", "raid"]),
    ("assassinate the supreme leader", ["strike", "raid"]),
    ("lift sanctions on Iran", ["sanctions", "talks"]),
    ("ease sanctions", ["sanctions", "talks"]),
    ("impose new sanctions on banks", ["sanctions"]),
    ("ban buying Iranian oil", ["sanctions"]),
    ("list the Guard as a terrorist organization", ["sanctions", "legal"]),
    ("seize a tanker at sea", ["naval"]),
    ("escort ships through the Strait", ["naval"]),
    ("stop bombing the Houthis", ["talks"]),
    ("call the president", ["talks", "visit"]),
    ("launch a cyber attack", ["cyber"]),
    ("hold joint drills", ["drill"]),
    ("bomb radar sites", ["strike"]),
    ("leave the nuclear deal", []),
])
def test_clear_phrases_read_as_expected(text, want):
    r = R.read_move(R.tokens(text), M)
    assert r["moves"] == [m for m in A.VOCAB["move"] if m in want], text
    assert r["tier"] is not None, text


def test_no_cue_means_no_filter():
    assert R.read_move(R.tokens("ban a social media app"), M)["tier"] is None
    assert R.read_move(R.tokens("zzzz qqqq"), M)["tier"] is None


def test_pulling_out_is_never_a_deployment():
    assert "deployment" not in moves("pull troops out of Iraq")
    assert "withdrawal" not in moves("send troops to Iraq")


def test_negation_is_not_read_as_a_move():
    rd = R.read_spec(dict(desc="do not strike Iran"), _ths()["iran"])
    assert rd["neg"] and rd["cue"]["moves"] == []
    rd = R.read_spec(dict(desc="say the US does not support Taiwan independence"), _ths()["iran"])
    assert not rd["neg"]                           # a "not" after "say" is part of what is said


def test_cues_use_only_known_moves_and_tiers():
    for c in A.CUES:
        assert c["p"] in (0, 1, 2) and set(c["moves"]) <= set(A.VOCAB["move"]) and c["phrases"]
        for p in c["phrases"]:
            assert p.strip() == p and "  " not in p


@pytest.mark.parametrize("tid", THEATER_IDS)
def test_page_data_has_cues_neutral_and_params(tid):
    m = load_export(tid)["matcher"]
    assert m["cues"] == A.CUES and m["params"] == A.MATCH and m["neutral"] == A.NEUTRAL[tid] and m["neutral"]


def test_theater_names_are_neutral_not_ignored():
    for tid in THEATER_IDS:
        mm = A.page_vocab(tid)
        r = R.scan_box("Iranian Houthi chinese venezuelan north korean", "where", _ths()[tid])
        assert not set(mm["neutral"]) & set(r["ignored"])
