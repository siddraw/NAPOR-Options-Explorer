"""China (Taiwan Strait and South China Sea) theater: wording, options, flags and rules, all in one place.

The research files (events_pre2019.py for May 1995 - Dec 2018, events.py from Jan 2019) hold the facts and are read only. This file holds the decisions the engine needs.

SMALL NUMBERS: Taiwan-specific US moves are few. Since the log was extended back to 1995, B (talks) has 21 counted cases, D (transits and
FONOPs) 15, E 9 and F 7; C, G and H have one or two. The page says so on every option (see THEATER["small_n"]).

The five categories, exactly as defined for this tab (the page shows these words; the rules are in theaters/common.py):
  people      anyone hurt in a Chinese reply within 7 days of the US move
  escalation  a PLA named drill, a spike in aircraft entering Taiwan's air defense zone (ADIZ), a coast-guard confrontation or a Chinese
              counter-sanction within 7 days. A clear link means a dated action that China or an allowed
              outlet ties to the US move (or a clear step up on a named day); routine daily PLA flights and "tracked and monitored" shadowing
              are background, not a reply.
  military    the reply was a live-fire or named large-scale drill (the logged action type says "Large-scale drills" or "live fire")
  economic    Chinese counter-sanctions or trade measures against US firms or the US within 14 days of the move (a Chinese action of kind
              Sanctions, for example a sanctions list or an export ban). The window is 14 days, not 7, so a case counts only after 14 days of news.
  political   no talks within 14 days: no logged Diplomatic row whose action type names talks, a meeting,
              a proposal, a ceasefire or a deal (a call, summit or senior meeting) in the 14 days after the move. Statements and threats do not count.
"""
import datetime as dt
import re

THEATER_ID = "china"


def d(y, m, day):
    return dt.date(y, m, day)


# ---- wording the page uses ------------------------------------------------------------------------------
THEATER = dict(
    id=THEATER_ID, name="China / Taiwan", status="active", title="China / Taiwan Strait and South China Sea",
    sub="The options the US has toward China over Taiwan and the South China Sea, and what followed the last times the US did something like each one.",
    adversary="China", actor="China", actor_short="China",
    proxy_note="Every reply here is an act by China itself (the PLA, the coast guard or the foreign ministry). Xinhua, Global Times, CGTN, PLA Daily and the Chinese defense and foreign ministries are used only as labelled claims of what China says. Routine PLA activity near Taiwan is background, not a reply, unless an allowed outlet ties it to a US move or it is a clear step up on a named day.",
    salvo=None,
    hold_note="Option A is not built for China. A hold week would be a week with no US transit, arms sale, visit, sanction or talks, but the log is a sample of named events (2021 holds one row, and most FONOPs and allied drills are missing), and routine PLA flights near Taiwan happen almost daily and are not logged. A week that looks quiet may only be a week where nothing was logged, so NAPOR does not invent hold weeks.",
    not_measured="Oil and chip prices, shipping and trade volumes, harm to ordinary Taiwanese and strain with allies are not measured. Only Chinese counter-sanctions and trade measures are.",
    presets=[["1995-05-22", "Lee Teng-hui visa"], ["1996-03-10", "Carriers sent toward Taiwan"], ["2001-04-24", "Largest arms sale in a decade"], ["2015-10-27", "First Lassen FONOP"],
             ["2019-07-08", "$2.2B arms sale"], ["2020-08-09", "Azar visit to Taipei"], ["2022-08-02", "Pelosi visit"], ["2023-04-05", "Tsai-McCarthy meeting"],
             ["2024-12-10", "Largest maritime deployment"], ["2025-12-29", "Justice Mission 2025 drills"]],
    under_logged="The log is a sample of named events. It starts in May 1995, but 1997-2000, 2002-2007, 2012 and 2014 are thinly logged: the 1995-2018 years hold the big crises, summits, arms sales and tariff rounds, not the routine patrols and transits. Many 1995-2008 rows rest on a CRS chronology or the Congressional Record. 2021 and 2022-2023 US FONOPs are mostly missing, routine PLA flights are not logged, and some Chinese counter-sanctions were found only on outlets that are not allowed, so \"none logged\" is not proof nothing happened.",
    spark_from="1995-05-01", thin_before="2019-01-01", claim_note="Chinese state media (Xinhua, Global Times, CGTN, PLA Daily)",
    small_n="Small numbers: Taiwan-specific US moves are few. Most options here have only a handful of counted cases (the exact number is on each option), and options with fewer than 3 show \"too few cases\" instead of a percentage. Even the larger ones (D) are mostly cases where China answered with words and shadowing. Read every rate as a hint, not a forecast.",
    # ---- per-theater words and rules the page reads (defaults on the page are the Iran / Houthi words) ----
    reply_days=7,
    intensity=dict(name="PLA activity level", note="PLA activity level counts logged Chinese drills, patrols, median-line crossings, coast-guard confrontations and missile launches in the 14 days before each date: 2 points each, +2 if someone died. Counter-sanctions are not counted. Routine daily PLA flights are not logged, so quiet stretches are understated."),
    base=dict(noun="Chinese military and coast-guard actions", short="Chinese actions", kinds=["Kinetic"]),
    act=dict(verb="took a logged military or coast-guard action or a counter-sanction within 7 days", row="takes a military, coast-guard or counter-sanction action within 7 days", col="Action ≤7d", none="No such action"),
    econ=dict(mode="events", days=14, name="Economic harm", label="China answers with counter-sanctions or trade measures within 14 days"),
    cats=dict(
        people=dict(name="Harm to people", short="People hurt",
                    other="Share of past cases where anyone was reported hurt in a Chinese reply the log links to the move (or in the US move itself).",
                    hold="Share of hold weeks in which a Chinese action in the 7 days after hurt anyone.",
                    rule=dict(other="Counts when anyone was reported hurt in a Chinese reply the log links to the move. Linked replies are usually within 7 days; for #3056 (Dec 2025 arms sale) the linked replies came on days 8 and 11 and are still checked here.",
                              hold="Counts when a Chinese action in the 7 days after the Monday hurt anyone.")),
        escalation=dict(name="Escalation", short="Escalation",
                        trigger="Share of past cases followed within 7 days by a named PLA drill, a spike in aircraft entering Taiwan's air defense zone, a coast-guard confrontation or a Chinese counter-sanction that China or an allowed outlet ties to the US move. Routine flights and shadowing do not count.",
                        other="Share of past cases followed within 7 days by any logged Chinese military or coast-guard action (a drill, patrol, median-line crossing, close pass, deployment, missile launch or coast-guard confrontation) or counter-sanction (timing only).",
                        hold="Share of hold weeks followed within 7 days by any logged Chinese military or coast-guard action (a drill, patrol, median-line crossing, close pass, deployment, missile launch or coast-guard confrontation) or counter-sanction (timing only).",
                        rule=dict(trigger="Counts when China replied within 7 days with a named PLA drill, an air-defense-zone spike, a coast-guard confrontation or a counter-sanction that China or an allowed outlet ties to the US move. Routine flights and shadowing do not count.",
                                  other="Counts when the log holds any logged Chinese military or coast-guard action (a drill, patrol, median-line crossing, close pass, deployment, missile launch or coast-guard confrontation) or counter-sanction in the 7 days after the move (timing only, not shown to be a reply). Unlike the reply rule, a patrol or close pass counts here.")),
        military=dict(name="Military cost", short="Military cost",
                      reply="Share of past cases where China's reply was a live-fire drill or a named large-scale drill.",
                      strike="Share of hold weeks with a live-fire or named large-scale Chinese drill in the 7 days after.",
                      none="No direct military cost expected from the move itself, so this counts as 0%.",
                      rule=dict(reply="Counts when a Chinese reply the log links to the move was a live-fire or named large-scale drill. Combat patrols, median-line crossings, a close pass at sea and a coast-guard confrontation do not. Linked replies are usually within 7 days, but not always: the Justice Mission 2025 drills came 11 days after the Dec 18, 2025 arms sale (#3056) and count here, although the escalation category (7 days) counts #3056 as no reply.",
                                strike="Counts when a live-fire or named large-scale Chinese drill took place in the 7 days after the Monday.")),
        economic=dict(name="Economic harm", short="Economic",
                      other="Share of past cases followed within 14 days by Chinese counter-sanctions or trade measures against US firms or the US (timing only, not shown to be caused by the US move).",
                      rule="Counts when China announced counter-sanctions or trade measures against US firms or the US within 14 days after the move."),
        political=dict(name="Political / diplomatic", short="Political",
                       other="Share of past cases NOT followed within 14 days by talks or a meeting between the US and China (a call, a summit or a senior meeting). Statements and threats do not count.",
                       rule="Counts when no talks or meeting between the US and China (a call, a summit or a senior meeting) was logged within 14 days after the move. Statements, threats and appeals do not count as talks."),
    ),
)

# A tab needs at least this many counted cases to show a risk index; below it the page says "too few cases".
MIN_CASES = 3

# ---- options (letters are fixed, as tagged in events.py; the page lists them in this order, never sorted) ------
OPTIONS = [
    dict(key="A", name="Hold: no new action",
         what="Keep the current course: no new US transit, arms sale, visit, sanction or talks move toward China or Taiwan."),
    dict(key="B", name="Talks or leader contact",
         what="Leader calls, summits and senior meetings with China (for example Blinken-Xi, Biden-Xi, Trump-Xi)."),
    dict(key="C", name="Sanctions and export controls",
         what="Entity listings and export controls aimed at China's military and its suppliers, for example advanced-chip controls."),
    dict(key="D", name="Taiwan Strait transits and FONOPs",
         what="Navy ships sail through the Taiwan Strait, or challenge China's claims in the South China Sea (freedom-of-navigation operations)."),
    dict(key="E", name="Arms sales to Taiwan",
         what="Announced arms sales and military aid for Taiwan."),
    dict(key="F", name="High-level contact with Taiwan",
         what="Senior US visits to Taiwan, or meetings with Taiwan's leaders in the US."),
    dict(key="G", name="Exercises with allies",
         what="Joint exercises with allies in the region (for example the first multilateral maritime activity of Apr 2024)."),
    dict(key="H", name="Other force posture",
         what="Other deployments, for example two-carrier operations in the South China Sea."),
]

# trigger: escalation = "China replied within 7 days" (clear link or timing only); otherwise "a Chinese action within 7 days" (timing only).
# military: "reply" = the reply was a live-fire or named large-scale drill; "strike" = such a drill within 7 days (A); "none" = counted as 0%.
# Closing window in days per category: when a case's outcome is final (read by napor_cases.window_days, the backtest and the page).
# Linked replies (people, military) count at any lag; the longest logged lag is 11 days (#3056, Justice Mission 2025), so 11. Escalation is judged at reply_days (7), economic at ECON days (14), political at 14.
CLOSE = dict(people=11, escalation=7, military=11, economic=14, political=14)
_W = dict(close=CLOSE, reply_days=7, econ_days=14)
THEATER["close"] = CLOSE            # travels into the data file so the page masks past dates with the same windows
FLAGS = {
    "A": dict(trigger=False, military="strike", us_move=False, is_hold=True, salvo=False, **_W),
    "B": dict(trigger=False, military="none", us_move=False, is_hold=False, salvo=False, **_W),
    "C": dict(trigger=True, military="reply", us_move=True, is_hold=False, salvo=False, **_W),
    "D": dict(trigger=True, military="reply", us_move=True, is_hold=False, salvo=False, **_W),
    "E": dict(trigger=True, military="reply", us_move=True, is_hold=False, salvo=False, **_W),
    "F": dict(trigger=True, military="reply", us_move=True, is_hold=False, salvo=False, **_W),
    "G": dict(trigger=True, military="reply", us_move=True, is_hold=False, salvo=False, **_W),
    "H": dict(trigger=True, military="reply", us_move=True, is_hold=False, salvo=False, **_W),
}
US_MOVE_KINDS = ("Sanctions", "Posture")
REPLY_DAYS = 7
ECON = dict(mode="events", days=14, kinds=("Sanctions",))     # a Chinese counter-sanction or trade measure within 14 days

# ---- sources and actors -----------------------------------------------------------------------------------
CLAIM_MEDIA = {"Xinhua", "Global Times", "CGTN", "PLA Daily", "China Daily", "People's Daily", "Chinese Ministry"}   # allowed only as labelled claims, scored 0.30
CLAIM_LABEL = "Chinese state media (claim only)"


def us_side(actor):
    return actor.lower().startswith("us")


def adversary_side(actor):
    """China itself (the PLA, the coast guard, the foreign ministry), including 'as reported' and 'per Taiwan MND' labels."""
    return actor.lower().startswith("china")


# The shared word list files drills and patrols as "Other"; this theater sorts rows by the words at the start of the action type.
def KIND_OF(e):
    a = e[3].lower()
    if a.startswith(("counter-sanction", "counter-measure", "sanction", "export controls")):
        return "Sanctions"          # US sanctions and controls, and China's counter-sanctions and trade measures
    if a.startswith("talks"):
        return "Diplomatic"
    if adversary_side(e[2]):
        return "Kinetic"            # a drill, patrol, median-line crossing, coast-guard confrontation, deployment or missile launch by China
    if a.startswith("posture"):
        return "Posture"
    return "Other"


KIND_OVERRIDE = {}
ATTACK_KINDS = ("Kinetic", "Sanctions")      # a Chinese action that counts as escalation: a drill, patrol, confrontation or counter-sanction
BASELINE = "attack"                          # the "no new US move" baseline counts Chinese military and coast-guard actions (not counter-sanctions)

_LIVE = re.compile(r"large-scale drills|live-fire|live fire")


def MILITARY_REPLY(e):
    """A Chinese action counts as a military reply when its logged action type is a named large-scale drill or a live-fire drill.
    Combat patrols, median-line crossings, a close pass at sea and a coast-guard confrontation do not."""
    return adversary_side(e[2]) and bool(_LIVE.search(e[3].lower()))


def HOSTILE_TEST(e, kind):
    """Rows that add points to the activity scale: Chinese military and coast-guard actions (not counter-sanctions)."""
    return adversary_side(e[2]) and kind == "Kinetic"


BASELINE_TEST = HOSTILE_TEST


# ---- hold weeks (option A): not built, see THEATER["hold_note"] --------------------------------------------
HOLD_START = None
MIN_HOLD_WEEKS = 3
UNCERTAIN = {}
PEOPLE_HURT = {}
CIVILIAN_HARM = {}

# ---- the backtest -----------------------------------------------------------------------------------------
OOS_CUT = d(2025, 12, 31)
OOS_LABEL = "1995-2025"


def period(day):
    if day < d(2009, 1, 1):
        return "1995-2008"
    if day < d(2019, 1, 1):
        return "2009-18"
    if day < d(2021, 1, 1):
        return "2019-20"
    if day < d(2024, 1, 1):
        return "2021-23"
    if day < d(2026, 1, 1):
        return "2024-25"
    return "2026"


PERIOD_KEYS = ["1995-2008", "2009-18", "2019-20", "2021-23", "2024-25", "2026"]
LOOKBACKS = ("1996-03-20", "2001-05-01", "2009-04-01", "2016-01-15", "2018-10-05", "2019-05-01", "2020-11-01", "2022-08-10", "2024-01-01", "2025-12-20")      # past dates the page test also checks (no hindsight)

# ---- plain-language risk lines (the page's "What the log says"; filled in by theaters/common.py) -----------------------
THREAD_PREFIX = "C"
RISK_TEXT = dict(
    people_trigger="Replies that hurt people: {hurt} of {n} logged{detail}. Civilian harm reported in the US act itself: none in an allowed outlet.",
    people_hold="Chinese military and coast-guard actions and counter-sanctions have been logged at about {per_week} a week in the current phase. No new US act to answer.",
    people_sanctions="No direct casualties from the sanctions or export controls themselves. Harm to ordinary people from them: not measured.",
    people_other="No direct casualties from the move itself.",
    esc_trigger="China replied (a named drill, an air-defense-zone spike, a coast-guard confrontation or a counter-sanction tied to the move) within 7 days: {reply} (range {range}). Fast (within 2 days): {fast}. Back-and-forth past one reply: {longer}. Small numbers: read as a hint.",
    esc_hold="No new US trigger. Hold weeks are not built for China (the log is a sample of named events).",
    esc_timing="China took a logged military or coast-guard action (any kind, patrols included) or a counter-sanction within 7 days after {strikes} past cases (timing only, not shown to be replies). Reply rate: not measured for this option.",
    no_cases="No past cases, so no measure.",
    mil_reply="A linked reply was a live-fire or named large-scale drill in {k} of {n} past cases (one, #3056, came on day 11). Losses of US or allied equipment in those replies: none logged.",
    mil_strike="Share of hold weeks with a live-fire or named large-scale Chinese drill in the 7 days after (see the cases).",
    mil_none="No military cost expected from the move itself.",
    eco_cases="Chinese counter-sanctions or trade measures within 14 days after past cases: {shipping}. Oil, chip and trade prices: not measured.",
    eco_baseline="Baseline: about {per_week} logged Chinese actions and counter-sanctions a week in the current phase. Prices: not measured.",
    pol_cases="Talks or a meeting between the US and China within 14 days after: {talks} (statements and threats do not count). Strain with allies: not measured.",
    pol_none="No past cases, so no measure. Strain with allies: not measured.",
)

# ---- analyst notes (judgement, not data; every line is labelled that way on the page) -----------------------
from theaters.china.notes import PROS, HARMS, UNKNOWNS     # noqa: E402

CONSTRAINT_OPTIONS = ()      # the log supports no constraint period for China
NOW_FILE = "now.json"
