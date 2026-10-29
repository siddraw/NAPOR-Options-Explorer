"""Iran theater: wording the page uses, option flags and the independent-recount hooks.
The Iran data and rules live in the original modules (data.py, napor_options.py, napor_cases.py, ...); this package
only wraps them so the top-level scripts can treat every theater the same way."""
import datetime as dt
import napor_options as O
from napor_cases import FLAGS            # per-option flags (trigger / military / us_move / is_hold / salvo)

THEATER_ID = "iran"
# Words the page uses for this theater, so a future theater renders with its own wording.
THEATER = dict(
    id=THEATER_ID, name="Iran", status="active", title="Iran war",
    sub="The options the US has right now in the Iran war, and what followed the last times the US did something like each one.",
    adversary="Iran", actor="Iran or an Iran-backed group", actor_short="Iran or proxy",
    proxy_note="Proxy = a militia Iran arms in Iraq or Syria. Before 2026, Iran mostly answered the US through these groups; those replies count and are labelled \"proxy\".",
    salvo=dict(count=O.PATRIOTS_PER_SALVO, weapon="Patriots", when="Sep 8-9"),
    hold_note="Hold cases are weeks of the 2026 war with no logged US sanctions, naval, strike or posture move (Feb 28-Apr 7 and Jul 7-25 left out: US activity there was continuous but logged as a few rows; pre-war weeks left out: too sparsely logged). Most hold weeks have few or no logged events, so they show what the log records in quiet weeks.",
    not_measured="Oil prices, strain with allies and harm to ordinary Iranians are not measured.",
    presets=[["1979-11-04", "Embassy seized"], ["1988-04-18", "Praying Mantis"], ["2006-12-23", "First UN sanctions"], ["2015-07-14", "Nuclear deal"],
             ["2018-05-08", "US leaves the deal"], ["2020-01-03", "Soleimani strike"], ["2025-06-22", "US strikes nuclear sites"], ["2026-02-28", "2026 war starts"],
             ["2026-04-08", "First ceasefire"], ["2026-06-17", "Interim deal"], ["2026-07-08", "July campaign"], ["2026-09-10", "Holding pattern"]],
    spark_from="1979-11-01", thin_before="2019-05-01",
    under_logged="The log is a sample. It starts at the Nov 1979 embassy takeover, but 1981-86, 1988-94, 1997-2001, 2003-05 and 2008-09 are thinly logged: before 2019 it holds the big crises, sanctions rounds, UN votes and talks, not every incident, and the Tanker War is logged as a few key clashes. Many pre-1990 rows rest on Washington Post archive pages. Some stretches are logged as one row (for example the nightly US strikes of Jul 9-25, 2026), so \"none logged\" is not proof nothing happened.",
)


