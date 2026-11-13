"""The Relevance figure of a personal option: how well the counted cases fit what the viewer typed. It is not a risk.
Pure functions in napor/matcher_ref.py (the page's JavaScript twin is checked by tests/test_matcher_parity.py and the Playwright run)."""
import pytest

import matcher_ref as R


@pytest.fixture(scope="module")
def ths():
    return R.load_all()[1]


@pytest.mark.parametrize("strengths,want", [
    (["exact"] * 7 + ["loose"] * 5, dict(n=12, close=7, pct=58, band="moderate")),
    (["exact", "close", "close", "loose"], dict(n=4, close=3, pct=75, band="strong")),            # exactly 75% is a strong fit
    (["close", "loose", "loose", "loose"], dict(n=4, close=1, pct=25, band="weak")),
    (["close", "loose"] * 2, dict(n=4, close=2, pct=50, band="moderate")),                         # exactly 50% is moderate
    (["close", "loose", "loose"], dict(n=3, close=1, pct=33, band="weak")),
    (["exact", "exact", "loose"], dict(n=3, close=2, pct=67, band="moderate")),
    (["exact"] * 8 + ["loose"] * 3, dict(n=11, close=8, pct=73, band="moderate")),
    (["exact"] * 3 + ["loose"], dict(n=4, close=3, pct=75, band="strong")),
    (["loose"] * 5, dict(n=5, close=0, pct=0, band="weak")),
    (["exact"] * 6, dict(n=6, close=6, pct=100, band="strong")),
    (["exact", "close"], dict(n=2, close=2, pct=None, band="few")),                                # under 3 cases: too few to judge
    (["exact"], dict(n=1, close=1, pct=None, band="few")),
    ([], dict(n=0, close=0, pct=None, band="few")),
])
def test_headline(strengths, want):
    assert R.relevance_headline(strengths) == want


def test_rounding_is_half_up_not_bankers():
    # 1 of 8 = 12.5% -> 13, 5 of 8 = 62.5% -> 63 (Python round() would give 12 and 62); JavaScript Math.round agrees with half-up
    assert R.relevance_headline(["close"] + ["loose"] * 7)["pct"] == 13
    assert R.relevance_headline(["close"] * 5 + ["loose"] * 3)["pct"] == 63


def test_stem_forms_match_plural_and_ing():
    assert R.stem_forms("strikes") & R.stem_forms("strike")
    assert R.stem_forms("bombing") & R.stem_forms("bombs")
    assert R.stem_forms("sanctioned") & R.stem_forms("sanction")
    assert not R.stem_forms("ship") & R.stem_forms("shop")
    assert not R.stem_forms("us") & R.stem_forms("u")      # a one- or two-letter stem is never used


def test_key_words_drop_small_words_theater_names_unknown_words_and_negated_words(ths):
    th = ths["iran"]
    rd = R.read_spec(dict(desc="impose new sanctions on Iranian banks but do not strike the zzzqqq"), th)
    w, forced = R.key_words(rd, th)
    assert w == ["impose", "sanctions", "banks"] and not forced          # new = filler, on/the = small, iranian = theater name, strike/zzzqqq = said the US would not do


def test_key_words_read_the_boxes_too_and_skip_ignored_box_words(ths):
    th = ths["iran"]
    rd = R.read_spec(dict(move="strike", target="radar, zzzqqq", desc=""), th)
    # a box word that was read as a setting is an exact rule, not a key word; a box word the page could not read is a key word that never counts as found
    assert R.key_words(rd, th) == (["zzzqqq"], {"zzzqqq"})
    assert R.key_words(rd, th, ["target"]) == (["radar", "zzzqqq"], {"radar", "zzzqqq"})


def test_key_words_found_with_stems():
    found, miss = R.relevance_words(["strikes", "bomb", "carrier"], [["us", "striking", "radar"], ["carriers", "arrive"]])
    assert (found, miss) == (2, ["bomb"])


def test_relevance_on_a_real_query_counts_only_the_counted_cases(ths):
    th = ths["iran"]
    m = R.match(dict(desc="bomb Iranian radar sites"), th)
    ids, st = [c["id"] for c in m["cases"]], [c["strength"] for c in m["cases"]]
    full = R.relevance(m["rd"], th, ids, st)
    assert full["n"] == len(ids) and full["kw_total"] == 3
    fewer = R.relevance(m["rd"], th, ids[:2], st[:2])           # the viewer removed cases: only the cases that are still counted are used
    assert fewer["n"] == 2 and fewer["band"] == "few" and fewer["pct"] is None


def test_hold_weeks_are_never_rated_close(ths):
    th = ths["iran"]
    m = R.match(dict(desc="do not strike Iran"), th)
    r = R.relevance(m["rd"], th, [c["id"] for c in m["cases"]], [c["strength"] for c in m["cases"]])
    assert m["hold"] and r["close"] == 0 and r["band"] == "weak" and r["kw_total"] == 0


def test_relevance_never_touches_the_matched_cases(ths):
    th = ths["iran"]
    a = R.match(dict(desc="new sanctions on banks"), th)
    before = [(c["id"], c["strength"], c["sim"]) for c in a["cases"]]
    R.relevance(a["rd"], th, [c["id"] for c in a["cases"]], [c["strength"] for c in a["cases"]])
    assert before == [(c["id"], c["strength"], c["sim"]) for c in a["cases"]]
