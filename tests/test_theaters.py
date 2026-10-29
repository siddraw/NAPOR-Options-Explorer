"""Per-theater checks on the event logs, the exported page data and the existing self-checks.

Every test runs once per theater listed in explorer/theaters.json (iran, houthis, northkorea, china, venezuela).
Nothing here writes a file: the exported data is read from explorer/data/<id>.json, and the checks call the project's own functions."""
import datetime as dt
import importlib

import pytest

import backtest_risk as BR
import napor_ids as N
from conftest import THEATER_IDS, load_export

REQUIRED_KEYS = ("theater", "asof", "generated", "phase", "intensity", "series", "hostile", "phases", "options",
                 "history", "report_card", "sources", "estimate")
OPTION_KEYS = ("key", "name", "what", "trigger", "military", "us_move", "is_hold", "salvo", "cases", "risks", "official")
LETTERS = list("ABCDEFGH")


class Log:
    """One theater's event log, however the theater stores it: rows, sources and credibility."""

    def __init__(self, tid):
        self.tid = tid
        if tid == "iran":
            import data
            import napor_options as O
            self.mod = O
            self.events = [e for e in data.events if e[0] not in data.MERGED]       # merged duplicates keep their row but are not events
            self.cred = N.event_credibility
            self.reports = N.reports_for
            self.census = O.census
            self.pairs = O.pairs
            self.census_all, self.pairs_all = data.census, data.pairs
            self.flags = None
        else:
            K = importlib.import_module(f"theaters.{tid}.cases")
            C = importlib.import_module(f"theaters.{tid}.config")
            self.mod = K
            self.events = list(K.EVENTS)
            self.cred = lambda i: K.CRED[i]
            self.reports = K.reports_for
            self.census, self.pairs = K.census, K.pairs
            self.census_all, self.pairs_all = K.CENSUS_RAW, K.PAIRS_RAW
            self.flags = C.FLAGS

    def cases(self):
        if self.tid == "iran":
            return BR.all_cases()
        return self.mod.all_cases()


@pytest.fixture(scope="module", params=THEATER_IDS)
def log(request):
    return Log(request.param)


# ---- b. exported data file: required keys, options A-H in fixed order ------------------------------------
def test_export_has_required_keys(log):
    out = load_export(log.tid)
    missing = [k for k in REQUIRED_KEYS if k not in out]
    assert not missing, f"{log.tid}: missing keys {missing}"
    assert out["theater"]["id"] == log.tid


def test_export_options_are_A_to_H_in_fixed_order(log):
    out = load_export(log.tid)
    keys = [o["key"] for o in out["options"]]
    assert keys == LETTERS, f"{log.tid}: options must be A-H in letter order, got {keys}"
    for o in out["options"]:
        missing = [k for k in OPTION_KEYS if k not in o]
        assert not missing, f"{log.tid} option {o['key']}: missing {missing}"
        assert o["military"] in ("reply", "strike", "none")


def test_option_order_is_not_sorted_by_risk(log):
    """The list must stay A-H even when the risk indexes would put it in another order (the page never ranks)."""
    import export_explorer as X
    out = load_export(log.tid)
    idx = [(X.risk_index(o, o["cases"]), o["key"]) for o in out["options"] if o["cases"]]
    by_risk = [k for _, k in sorted(idx, key=lambda t: (t[0], t[1]))]
    assert [o["key"] for o in out["options"]] == LETTERS
    if len(idx) > 2:
        assert by_risk != [k for _, k in idx], f"{log.tid}: risk order happens to equal letter order; the test cannot tell"


def test_theaters_json_lists_the_exported_file(log):
    import json
    import os
    from conftest import EXPLORER
    reg = json.load(open(os.path.join(EXPLORER, "theaters.json")))
    entry = [t for t in reg["theaters"] if t["id"] == log.tid][0]
    assert entry["data"] == f"data/{log.tid}.json"
    assert os.path.exists(os.path.join(EXPLORER, entry["data"]))


# ---- c. every event has a source, every URL is https ---------------------------------------------------
# Known gap, kept visible on purpose: Iran #67 (an IRGC claim) has no source recorded at all. Its credibility is 0.0, so the
# 0.50 cut keeps it out of every count. Any other event without a source, or this one gaining a count, fails the test.
UNSOURCED_AND_EXCLUDED = {"iran": {67}}


def test_every_event_has_at_least_one_source(log):
    bare = {e[0] for e in log.events if not log.reports(e[0])}
    allowed = UNSOURCED_AND_EXCLUDED.get(log.tid, set())
    assert bare <= allowed, f"{log.tid}: events with no source: {sorted(bare - allowed)}"
    assert all(log.cred(i) < N.INCLUDE_AT for i in bare), f"{log.tid}: an unsourced event is being counted"


def test_every_source_url_starts_with_https(log):
    bad = []
    for e in log.events:
        for r in log.reports(e[0]):
            url = r.get("url", "")
            if url:
                if not url.startswith("https://"):
                    bad.append((e[0], url))
            elif log.tid != "iran" or "name only" not in r.get("seen", ""):
                bad.append((e[0], "(no URL)"))          # only Iran's flagged "named in original row" reports may lack a URL
    assert not bad, f"{log.tid}: bad source URLs: {bad[:10]}"


def test_no_wikipedia_citations(log):
    """docs/SOURCE_STANDARD.md: Wikipedia is never a citation."""
    bad = [(e[0], r["url"]) for e in log.events for r in log.reports(e[0]) if "wikipedia." in r.get("url", "").lower()]
    assert not bad


def test_iran_name_only_sources_are_flagged_not_hidden():
    """Iran rows that were never re-checked name an outlet but have no link. They must stay flagged as such, never pass as checked sources."""
    lg = Log("iran")
    nolink = [(e[0], r) for e in lg.events for r in lg.reports(e[0]) if not r.get("url")]
    assert all(r["seen"] == "name only - not re-checked" and r["headline"] == "(not recorded)" for _, r in nolink)


# ---- d. credibility below 0.50 is left out of the counts -------------------------------------------------
def test_cut_is_0_50():
    assert N.INCLUDE_AT == 0.50


def test_credibility_rules():
    full = dict(outlet="Reuters", kind="Independent outlet", seen="full text")
    claim = dict(outlet="IRNA", kind="Iranian state media (claim only)", seen="full text")
    assert N.credibility_of([full]) == 0.80
    assert N.credibility_of([full, dict(full, outlet="AP")]) == 0.96             # two different outlets
    assert N.credibility_of([full, dict(full, headline="again")]) == 0.80       # the same outlet counts once
    assert N.credibility_of([claim]) == 0.30                                     # a claim-only outlet alone is below the cut
    assert N.credibility_of([full], "Partly verified") == 0.64
    assert N.credibility_of([full], "Not supported") == 0.20
    assert N.credibility_of([]) == 0.0


def test_events_under_0_50_are_left_out_of_census_and_pairs(log):
    low = {e[0] for e in log.events if log.cred(e[0]) < N.INCLUDE_AT}
    in_census = {c[0] for c in log.census}
    in_pairs = {p[1] for p in log.pairs} | {p[2] for p in log.pairs}
    assert not (low & in_census), f"{log.tid}: census still uses {low & in_census}"
    assert not (low & in_pairs), f"{log.tid}: pairs still use {low & in_pairs}"


def test_census_and_pairs_dropped_are_exactly_the_low_ones(log):
    """A census row stays if and only if its event counts; a pair stays if and only if both of its events count."""
    counts = N.counts if log.tid == "iran" else log.mod.counts
    for c in log.census_all:
        assert (c in log.census) == counts(c[0]), f"{log.tid}: census row {c[0]}"
    for p in log.pairs_all:
        assert (p in log.pairs) == (counts(p[1]) and counts(p[2])), f"{log.tid}: pair {p[0]}"


def test_exported_cases_all_have_credibility_of_at_least_0_50(log):
    out = load_export(log.tid)
    low = []
    for o in out["options"]:
        for c in o["cases"]:
            if c.get("cred") is not None and c["cred"] < N.INCLUDE_AT:
                low.append((o["key"], c["id"], c["cred"]))
    assert not low, f"{log.tid}: counted cases under the cut: {low}"
    for key, s in out["sources"].items():
        assert 0 <= s["cred"] <= 1


def test_low_credibility_events_do_not_reach_the_hostile_list(log):
    out = load_export(log.tid)
    low = {e[0] for e in log.events if log.cred(e[0]) < N.INCLUDE_AT}
    assert not (low & {h["id"] for h in out["hostile"]})


# ---- e. no-hindsight check -------------------------------------------------------------------------------
def test_no_hindsight_check_passes(log):
    ok, n = BR.no_hindsight_check(log.cases(), log.flags)
    assert ok, f"{log.tid}: appending a future case changed an earlier prediction, or a closing window is too short"
    assert n > 0


def test_closing_windows_reach_the_longest_logged_reply(log):
    assert BR.window_covers_lags(log.cases(), log.flags) == []


# ---- f. independent recount equals the export ------------------------------------------------------------
def test_recount_equals_export(log):
    out = load_export(log.tid)
    if log.tid == "iran":
        import export_explorer
        diff = export_explorer.recount_diff(out)
    else:
        diff = importlib.import_module(f"theaters.{log.tid}.export").recount_diff(out)
    assert diff == [], f"{log.tid}: recount differs from export: {diff[:3]}"


def test_page_counts_match_the_logs_own_counts(log):
    import export_explorer as X
    bad = [b for b in X.check(load_export(log.tid)) if b[2] != (0, 0)]
    assert bad == []


# ---- continuous-fighting windows: no counted case sits inside one (start acts excepted) -------------------
def test_no_venezuela_case_is_dated_inside_an_exclusion_window():
    from theaters.venezuela import events as VE
    out = load_export("venezuela")
    starts = VE.START_ACTS
    bad = []
    for o in out["options"]:
        if o["is_hold"]:
            continue
        for c in o["cases"]:
            day = dt.date.fromisoformat(c["date"])
            if c["id"] not in starts and any(a <= day <= b for a, b in VE.WINDOWS):
                bad.append((o["key"], c["id"]))
    assert not bad, f"cases inside an exclusion window: {bad}"
    assert not {4032, 4044, 4046, 4048} & {c["id"] for o in out["options"] for c in o["cases"]}


def test_n_events_counts_only_events_at_0_50_or_more(log):
    out = load_export(log.tid)
    assert out["n_events"] == sum(1 for e in log.events if log.cred(e[0]) >= N.INCLUDE_AT)
