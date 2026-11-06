"""Action tags (the "Your own option" matcher): every counted case is tagged, tags are valid and never describe outcomes,
and the page data carries the tags and the matcher's word lists."""
import pytest

import action_tags as A
from conftest import THEATER_IDS, load_export

OUTCOME_WORDS = ("retaliat", "casualt", "killed", "escalat", "response", "reply", "replied", "damage", "died", "injur", "fatal")


def counted(out):
    return [c for o in out["options"] for c in o["cases"] if not c.get("week")]


@pytest.mark.parametrize("tid", THEATER_IDS)
def test_every_counted_case_has_valid_tags(tid):
    tags = A.load_tags(tid)
    assert tags is not None, f"napor/tags/{tid}.py is missing"
    assert A.check(tid, tags, A.counted_case_ids(load_export(tid))) == []


@pytest.mark.parametrize("tid", THEATER_IDS)
def test_tags_have_no_outcome_fields_or_words(tid):
    for i, row in A.load_tags(tid).items():
        assert set(row) <= set(A.FIELDS) | {"why"}, f"{tid} #{i}: extra field {set(row) - set(A.FIELDS) - {'why'}}"
        for f in A.FIELDS:
            for v in (row[f] if f == "target" else [row[f]]):
                assert not any(w in v for w in OUTCOME_WORDS), f"{tid} #{i}: {f}={v}"


@pytest.mark.parametrize("tid", THEATER_IDS)
def test_page_data_has_matcher_and_tags(tid):
    out = load_export(tid)
    m = out["matcher"]
    assert m["fields"] == A.FIELDS and m["widen"] == A.WIDEN_ORDER and set(m["vocab"]) == set(A.FIELDS)
    assert m["labels"] == A.LABELS and m["synonyms"] == A.SYNONYMS
    cases = counted(out)
    assert cases
    for c in cases:
        assert set(c["tags"]) - {"why"} == set(A.FIELDS), c["id"]
        assert isinstance(c["tags"]["target"], list)
        assert c["tags"].get("why", "x") != ""            # `why` is written only when it has text
    for o in out["options"]:
        for c in o["cases"]:
            if c.get("week"):
                assert "tags" not in c
