"""The "Your own option" matcher (version 2, word meaning + hard rules) must stay accurate on the answer key's TEST half,
beat the old key-word matcher (v1) by a clear margin, and never return anything for the "nothing like this" queries."""
import json
import os

import pytest

import bench_matcher as B
from conftest import REPO, EXPLORER


@pytest.fixture(scope="module")
def v2():
    return B.run_v2()


def test_test_half_meets_the_floor(v2):
    fl = json.load(open(B.FLOOR))
    t = B.score(B.load_bench(), v2, "test")
    assert t["f1"] >= fl["test_f1"] and t["p5"] >= fl["test_p5"] and t["none"] >= fl["test_none"], t


def test_v2_beats_v1_on_test_by_a_clear_margin(v2):
    bench = B.load_bench()
    v1 = json.load(open(B.V1))["results"]
    a, b = B.score(bench, v1, "test"), B.score(bench, v2, "test")
    assert b["f1"] - a["f1"] >= 0.10 and b["p5"] > a["p5"], (a, b)


def test_nothing_like_this_queries_return_nothing(v2):
    for q in B.load_bench():
        if q["none"]:
            assert v2[q["id"]] == [], q["id"]


def test_never_more_than_the_maximum(v2):
    from action_tags import MATCH
    assert all(len(v) <= MATCH["max_cases"] for v in v2.values())


def test_vector_file_is_small_and_complete():
    p = os.path.join(EXPLORER, "matcher_vectors.json")
    assert os.path.getsize(p) <= 3.5e6
    v = json.load(open(p))
    assert len(v["words"].split(" ")) == v["n"] and len(v["w"]) > 0
    import build_vectors
    assert build_vectors.covered(v) == [], "new case words: run napor/build_vectors.py"
