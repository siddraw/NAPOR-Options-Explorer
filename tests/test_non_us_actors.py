"""Israeli-actions rule (Sidd, 2026-11-12): a non-US actor's action counts as a US case only when the log's own sources show a US link.
napor/non_us_actors.py records the links and the exclusions; tag_check.py fails the build when a counted case with a non-US actor has no recorded link."""
import non_us_actors as NU
import tag_check as T
from conftest import THEATER_IDS, load_export


def case(i, actor, title="x"):
    return dict(id=i, actor=actor, title=title, date="2026-01-01", cred=0.9)


def out_with(*cases):
    return dict(options=[dict(key="C", cases=list(cases))])


def test_the_real_data_passes_the_check():
    for tid in THEATER_IDS:
        assert T.non_us_actors(tid, load_export(tid)) == [], tid


def test_a_non_us_actor_without_a_link_fails():
    f = T.non_us_actors("zz", out_with(case(9999, "Israel", "Strikes on a base")))
    assert f and "no recorded US link" in f[0]


def test_a_title_that_starts_with_a_non_us_government_fails_even_if_the_actor_says_us():
    assert T.non_us_actors("zz", out_with(case(9998, "US", "Saudi Arabia hosts a meeting")))
    assert not T.non_us_actors("zz", out_with(case(9997, "US", "Operation opens")))


def test_a_us_actor_passes():
    assert T.non_us_actors("zz", out_with(case(9996, "US", "Treasury sanctions banks"), case(9995, "US/Israel", "x"), case(9994, "US (with UK)", "x"))) == []


def test_a_recorded_link_passes_and_needs_a_plain_line(monkeypatch):
    monkeypatch.setitem(NU.LINKS, "zz", {9994: dict(link="The US asked for it and announced it the same day.", sources="x")})
    assert T.non_us_actors("zz", out_with(case(9994, "Israel"))) == []
    monkeypatch.setitem(NU.LINKS, "zz", {9994: dict(link="", sources="x")})
    assert T.non_us_actors("zz", out_with(case(9994, "Israel")))


def test_an_excluded_case_must_not_be_counted(monkeypatch):
    monkeypatch.setitem(NU.EXCLUDED, "zz", {9993: dict(reason="no US link", sources="x")})
    assert "EXCLUDED" in T.non_us_actors("zz", out_with(case(9993, "Israel")))[0]


def test_iran_44_is_excluded_from_every_option_and_kept_as_a_context_event():
    assert 44 in NU.excluded("iran")
    for tid in THEATER_IDS:
        ids = {c["id"] for o in load_export(tid)["options"] for c in o["cases"]}
        assert not (NU.excluded(tid) & ids), tid
    import data
    assert any(e[0] == 44 for e in data.events)       # still in the event log
    assert "NOT A US CASE" in data._EDITS[44]["note"]


def test_every_link_and_exclusion_has_its_reason():
    for d in (NU.LINKS, NU.EXCLUDED):
        for tid, rows in d.items():
            for i, r in rows.items():
                assert len(r.get("link") or r.get("reason") or "") > 30 and r.get("sources"), (tid, i)
