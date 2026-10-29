"""North Korea theater: wording, options, flags and rules, all in one place.

The research files (events_pre2017.py for Mar 1993 - Aug 2017, events.py from Aug 31, 2017) hold the facts and are read only. This file holds the decisions the engine needs:
which options exist, what counts as an act by the other side, which outlets are claims only, how each of the five
risk categories is defined for North Korea, which weeks count as "hold" weeks, and the analyst notes the page shows.

The five categories, exactly as defined for this tab (the page shows these words; the rules are in theaters/common.py):
  people      anyone hurt in a North Korean reply (a launch, test or provocation) within 7 days of the US move
  escalation  a North Korean missile launch, nuclear test or provocation within 7 days. A threatening statement that the
              log files as a "provocation" (#2045, #2049, #2051) counts; a statement alone with no act is a provocation here
              only because the log says so.
  military    the reply was a ballistic missile or ICBM (the logged action type or the cited headline says ballistic, ICBM,
              IRBM or SRBM). Satellite rockets, cruise missiles, "projectiles", a nuclear test, drones and statements do not count.
  economic    NOT MEASURED. The log has no clear measure of sanctions relief, trade or prices, and NAPOR does not force a
              shipping measure onto North Korea. The page shows "not measured" and leaves the category out of the index.
  political   no talks within 14 days (rule changed 2026-10-26 with Sidd's approval): no logged Diplomatic row whose action type names talks, a
              meeting, a proposal, a ceasefire or a deal (a summit, a meeting, or an offer to meet) in the 14 days after the move. Statements and threats do not count.
"""
import datetime as dt
import re

THEATER_ID = "northkorea"


def d(y, m, day):
    return dt.date(y, m, day)


# ---- wording the page uses ------------------------------------------------------------------------------
THEATER = dict(
    id=THEATER_ID, name="North Korea", status="active", title="North Korea",
    sub="The options the US has toward North Korea, and what followed the last times the US (often with South Korea and Japan) did something like each one.",
    adversary="North Korea", actor="North Korea", actor_short="North Korea",
    proxy_note="Every reply here is an act by North Korea itself. KCNA and Rodong Sinmun are used only as labelled claims of what North Korea says; launches are dated by South Korea's Joint Chiefs of Staff or Japan's Defense Ministry as reported by an allowed outlet.",
    salvo=None,
    hold_note="Hold cases are weeks from Jan 20, 2025 on (the start of the second Trump term) with no logged US sanctions, drill, deployment, missile-defense or posture move. Weeks inside the Sep 12 - Oct 12, 2026 dense-launch stretch and two weeks of Ulchi Freedom Shield 2025 and one week of Freedom Edge 2025 (US moves that an allowed outlet reports but the log does not hold) are left out. The log is a sample, not a full list: it says that many launches and some US moves are missing, so a week that looks quiet may only be a week where nothing was logged. Read option A as a rough sketch and do not compare it number-for-number with options that rest on a few well-reported cases.",
    not_measured="Economic effects (sanctions relief, trade, prices) are not measured for North Korea; that category is left out of the index. Strain with South Korea, Japan and China is not measured either.",
    presets=[["1994-10-18", "Agreed Framework"], ["2006-10-09", "First nuclear test"], ["2013-04-03", "Kaesong closed, THAAD to Guam"], ["2016-09-09", "Fifth nuclear test"],
             ["2017-09-03", "Sixth nuclear test"], ["2018-06-12", "Singapore summit"], ["2019-06-30", "DMZ meeting"], ["2022-11-02", "23 missiles in one day"],
             ["2023-07-18", "Submarine visits Busan"], ["2025-11-07", "Launch after carrier and DMZ visits"], ["2026-08-17", "Scaled-down Ulchi Freedom Shield"]],
    under_logged="The log is a sample. It starts in March 1993, but 1995-97, 2004, 2007-08, 2011 and 2014-15 are thinly logged, and the 1993-2015 years hold only a few Treasury rounds and short-range launches. 2020 and most of 2021 are empty, and many launches from 2022 on are missing, so \"none logged\" is not proof nothing happened.",
    spark_from="1993-03-01", thin_before="2017-08-31", claim_note="North Korean state media (KCNA, Rodong Sinmun)",
    # ---- per-theater words and rules the page reads (defaults on the page are the Iran / Houthi words) ----
    reply_days=7,
    intensity=dict(name="Tension level", note="Tension level counts logged North Korean launches, tests and provocations (not threatening statements) in the 14 days before each date: 2 points each, +2 if someone died. The log is a sample, so quiet stretches are understated."),
    base=dict(noun="North Korean launches and provocations", short="launches or provocations", kinds=["Kinetic"]),
    act=dict(verb="launched, tested or provoked within 7 days", row="launches, tests or provokes within 7 days", col="Act ≤7d", none="No launch, test or provocation"),
    econ=dict(mode="none", name="Economic", text="Not measured. The log has no clear measure of sanctions relief, trade or prices for North Korea, so this category is left out of the index instead of being filled with a made-up number."),
    cats=dict(
        people=dict(name="Harm to people", short="People hurt",
                    other="Share of past cases where anyone was reported hurt in a North Korean reply (a launch, test or provocation) within 7 days.",
                    hold="Share of hold weeks in which a North Korean launch, test or provocation in the 7 days after hurt anyone.",
                    rule=dict(other="Counts when anyone was reported hurt in a North Korean reply (a launch, test or provocation) within 7 days of the US move.",
                              hold="Counts when a North Korean launch, test or provocation in the 7 days after the Monday hurt anyone. Checked by hand from each logged event's damage text.")),
        escalation=dict(name="Escalation", short="Escalation",
                        trigger="Share of past cases followed by a North Korean missile launch, nuclear test or provocation within 7 days. Some of these replies are threatening statements the log files as provocations (for example #2049), not launches.",
                        other="Share of past cases followed by a North Korean missile launch, nuclear test or provocation within 7 days (timing only). A threatening statement the log files as a provocation counts.",
                        hold="Share of hold weeks followed by a North Korean missile launch, nuclear test or provocation within 7 days (timing only). A threatening statement the log files as a provocation counts.",
                        rule=dict(trigger="Counts when North Korea launched a missile, tested a nuclear weapon or provoked within 7 days (a clear link or timing only). A threatening statement the log files as a provocation counts.",
                                  other="Counts when North Korea launched, tested or provoked anywhere within 7 days (timing only, not shown to be a reply). A threatening statement the log files as a provocation counts.")),
        military=dict(name="Military cost", short="Military cost",
                      reply="Share of past cases where North Korea's reply was a ballistic missile or ICBM.",
                      strike="Share of hold weeks with a North Korean ballistic missile or ICBM launch in the 7 days after.",
                      none="No direct military cost expected from the move itself, so this counts as 0%.",
                      rule=dict(reply="Counts when the reply was a ballistic missile or ICBM. A satellite rocket, a cruise missile, \"projectiles\", a nuclear test, drones and statements do not count.",
                                strike="Counts when a North Korean ballistic missile or ICBM was launched in the 7 days after the Monday.")),
        economic=dict(name="Economic harm", short="Economic",
                      other="Not measured for North Korea. There is no clear measure of sanctions relief, trade or prices in the log, so this category is shown as \"not measured\" and left out of the index.",
                      rule="Not measured. Nothing is counted for this category."),
        political=dict(name="Political / diplomatic", short="Political",
                       other="Share of past cases NOT followed within 14 days by talks (a summit, a meeting or an offer to meet) between the US and North Korea. Statements and threats do not count.",
                       rule="Counts when no talks (a summit, a meeting or an offer to meet) between the US and North Korea were logged within 14 days after the move. Statements, threats and appeals do not count as talks. Rule changed on 2026-10-26."),
    ),
)

# A tab needs at least this many counted cases to show a risk index; below it the page says "too few cases".
MIN_CASES = 3

# ---- options (letters are fixed, as tagged in events.py; the page lists them in this order, never sorted) ------
OPTIONS = [
    dict(key="A", name="Hold: no new action",
         what="Keep the current course: no new US sanctions, drills, deployments, missile-defense moves or talks offer toward North Korea."),
    dict(key="B", name="Talks or summit offer",
         what="Offer to meet or talk with Kim Jong Un, or hold a summit or a meeting (for example Singapore, Hanoi, the DMZ)."),
    dict(key="C", name="New sanctions",
         what="Treasury or State sanctions on North Korean banks, IT-worker networks, shipping firms and procurement agents."),
    dict(key="D", name="Joint military drills",
         what="US-South Korea (and US-South Korea-Japan) exercises such as Freedom Shield, Ulchi Freedom Shield and Freedom Edge."),
    dict(key="E", name="Interdiction and ship-to-ship enforcement",
         what="Seize or stop ships and cargoes that break sanctions, for example coal shipments and oil transfers at sea."),
    dict(key="F", name="Missile-defense moves",
         what="THAAD in South Korea and the trilateral sharing of North Korean missile-warning data."),
    dict(key="G", name="Strategic-asset deployments",
         what="Send bombers, aircraft carriers or nuclear-powered submarines to the Korean Peninsula."),
    dict(key="H", name="Other force posture",
         what="Summit pledges on deterrence, defense-chief visits and other changes in alliance posture."),
]

# trigger: escalation = "North Korea replied within 7 days" (Trigger Census); otherwise "an act within 7 days" (timing only).
# military: "reply" = the reply was a ballistic missile or ICBM; "strike" = such a launch within 7 days (A); "none" = counted as 0%.
# reply_days / econ_days travel with the flags into the data file; the backtest uses them for the length of each outcome window.
# Closing window in days per category: when a case's outcome is final (read by napor_cases.window_days, the backtest and the page).
# Linked replies count at any lag; the longest logged lag is 6 days, so the 7-day reply window covers all. Economic is not measured.
CLOSE = dict(people=7, escalation=7, military=7, economic=7, political=14)
_W = dict(close=CLOSE, reply_days=7)
THEATER["close"] = CLOSE            # travels into the data file so the page masks past dates with the same windows
FLAGS = {
    "A": dict(trigger=False, military="strike", us_move=False, is_hold=True, salvo=False, **_W),
    "B": dict(trigger=True, military="reply", us_move=False, is_hold=False, salvo=False, **_W),
    "C": dict(trigger=True, military="reply", us_move=True, is_hold=False, salvo=False, **_W),
    "D": dict(trigger=True, military="reply", us_move=True, is_hold=False, salvo=False, **_W),
    "E": dict(trigger=True, military="reply", us_move=True, is_hold=False, salvo=False, **_W),
    "F": dict(trigger=True, military="reply", us_move=True, is_hold=False, salvo=False, **_W),
    "G": dict(trigger=True, military="reply", us_move=True, is_hold=False, salvo=False, **_W),
    "H": dict(trigger=True, military="reply", us_move=True, is_hold=False, salvo=False, **_W),
}
US_MOVE_KINDS = ("Sanctions", "Posture")     # kinds of act that make a week "not a hold week"
REPLY_DAYS = 7
ECON = dict(mode="none", days=7)             # the economic category is not measured for North Korea

# ---- sources and actors -----------------------------------------------------------------------------------
CLAIM_MEDIA = {"KCNA", "Rodong Sinmun", "Korean Central News Agency"}      # North Korean outlets: allowed only as labelled claims, scored 0.30
CLAIM_LABEL = "North Korean state media (claim only)"


def us_side(actor):
    return actor.lower().startswith("us")


def adversary_side(actor):
    """North Korea itself (including 'per JCS' and 'claimed' labels)."""
    return actor.lower().startswith("north korea")


# What kind of act each logged row is. The shared word list files "Missile launch" and "Nuclear test" as "Other", so this
# theater sorts rows by the words at the start of the action type.
def KIND_OF(e):
    a = e[3].lower()
    if a.startswith(("missile launch", "nuclear test", "provocation")):
        return "Kinetic"            # a launch, a test or a provocation by North Korea (a threatening statement filed as a provocation too)
    if a.startswith("diplomatic"):
        return "Diplomatic"
    if a.startswith(("sanction", "seizure")):
        return "Sanctions"
    if a.startswith(("force posture", "missile defense", "joint drills")):
        return "Posture"
    return "Other"


KIND_OVERRIDE = {}
ATTACK_KINDS = ("Kinetic",)                  # a hostile act by North Korea: a launch, a test or a provocation
BASELINE = "attack"                          # the "no new US move" baseline counts these acts per week (launches, tests and provocations, not statements)

_BALLISTIC = re.compile(r"ballistic|icbm|irbm|srbm")


def _headlines(eid):
    from theaters.northkorea import events, events_pre2017
    srcs = events.SOURCES.get(eid) or events_pre2017.SOURCES.get(eid, [])
    return " ".join(s.get("headline", "") for s in srcs).lower()


def MILITARY_REPLY(e):
    """A North Korean reply counts as military when it is a missile launch that the logged action type, or the cited headline,
    calls ballistic (ballistic missile, ICBM, IRBM, SRBM). A satellite rocket, 'projectiles', a cruise missile, a nuclear test, drones and
    statements do not count. (#2027, 23 missiles in one day: the cited NPR page does not say ballistic, so it does not count.)"""
    a = e[3].lower()
    return adversary_side(e[2]) and a.startswith("missile launch") and bool(_BALLISTIC.search(a) or _BALLISTIC.search(_headlines(e[0])))


def HOSTILE_TEST(e, kind):
    """Rows that add points to the tension scale: North Korean launches, tests and provocations, not threatening statements."""
    return adversary_side(e[2]) and kind == "Kinetic" and "statement" not in e[3].lower()


BASELINE_TEST = HOSTILE_TEST


# ---- hold weeks (option A) -------------------------------------------------------------------------------
HOLD_START = d(2025, 1, 20)                              # first Monday of the second Trump term
MIN_HOLD_WEEKS = 3                                       # fewer than this: option A shows "too few cases", no weeks are invented
UNCERTAIN = {                                            # Monday ISO date -> reason (an allowed outlet reports a US move missing from the log)
    "2025-08-18": "Ulchi Freedom Shield 25 began Aug 18, 2025 (INDOPACOM, Korea Times); a joint drill that is not logged as its own row.",
    "2025-08-25": "Ulchi Freedom Shield 25 ran through Aug 28, 2025 (INDOPACOM); a joint drill that is not logged as its own row.",
    "2025-09-15": "The trilateral Freedom Edge 2025 exercise wrapped up on Sep 19, 2025 (USNI News); a joint drill that is not logged as its own row.",
}
# Set by hand from the logged damage text of every hostile act in the 7 days after the Monday (see hold_hurt_candidates()).
# monday: (anyone hurt?, evidence event IDs, note)
# A hold week with no North Korean act logged in the 7 days after needs no entry: it is set to (False, [], "No hostile act logged.") automatically.
PEOPLE_HURT = {
    "2025-10-20": (False, [2055], "Several short-range ballistic missiles flew about 350 km: no damage or injuries logged (AP via News4Jax)."),
    "2025-12-29": (False, [2063], "At least two ballistic missiles landed outside Japan's exclusive economic zone: no damage logged (Japan Ministry of Defense)."),
}

CIVILIAN_HARM = {}        # no civilian harm reported in an allowed outlet for any counted US move

# ---- the backtest -----------------------------------------------------------------------------------------
OOS_CUT = d(2025, 12, 31)
OOS_LABEL = "1993-2025"


def period(day):
    if day < d(2010, 1, 1):
        return "1993-2009"
    if day < d(2017, 8, 31):
        return "2010-Aug17"
    if day < d(2020, 1, 1):
        return "2017-19"
    if day < d(2023, 1, 1):
        return "2020-22"
    if day < d(2025, 1, 1):
        return "2023-24"
    return "2025+"


PERIOD_KEYS = ["1993-2009", "2010-Aug17", "2017-19", "2020-22", "2023-24", "2025+"]
LOOKBACKS = ("1999-09-24", "2006-10-16", "2013-04-10", "2016-03-20", "2018-06-13", "2019-03-01", "2022-10-01", "2024-07-02", "2025-11-08")      # past dates the page test also checks (no hindsight)

# ---- plain-language risk lines (the page's "What the log says"; filled in by theaters/common.py) -----------------------
THREAD_PREFIX = "K"
RISK_TEXT = dict(
    people_trigger="Replies that hurt people: {hurt} of {n} logged{detail}. Civilian harm reported in the US act itself: none in an allowed outlet.",
    people_hold="North Korean launches and provocations have been logged at about {per_week} a week in the current phase. No new US act to answer.",
    people_sanctions="No direct casualties from the sanctions themselves. Harm to ordinary North Koreans from sanctions: not measured.",
    people_other="No direct casualties from the move itself.",
    esc_trigger="North Korea replied (a launch, test or provocation) within 7 days: {reply} (range {range}). Fast (within 2 days): {fast}. Back-and-forth past one reply: {longer}.",
    esc_hold="No new US trigger. North Korea launched or provoked in some weeks anyway (see the hold-week cases). Whether holding back changes what it does: not measured.",
    esc_timing="North Korea launched or provoked within 7 days after {strikes} past cases (timing only, not shown to be replies). Reply rate: not measured for this option.",
    no_cases="No past cases, so no measure.",
    mil_reply="A ballistic missile or ICBM followed within 7 days in {k} of {n} past cases. Losses of US or allied equipment in those replies: none logged.",
    mil_strike="Share of hold weeks with a North Korean ballistic missile or ICBM launch in the 7 days after (see the cases).",
    mil_none="No military cost expected from the move itself.",
    eco_cases="Economic effects (sanctions relief, trade, prices): not measured for North Korea. This category is left out of the index.",
    eco_baseline="Baseline: about {per_week} logged North Korean launches or provocations a week in the current phase. Economic effects: not measured for North Korea.",
    pol_cases="Talks (a summit, a meeting or an offer to meet) within 14 days after: {talks} (statements and threats do not count). Strain with South Korea, Japan and China: not measured.",
    pol_none="No past cases, so no measure. Strain with South Korea, Japan and China: not measured.",
)

# ---- analyst notes (judgement, not data; every line is labelled that way on the page) -----------------------
from theaters.northkorea.notes import PROS, HARMS, UNKNOWNS     # noqa: E402

# ---- constraint periods (limit which options are open) -------------------------------------------------------
# The log supports one: the summit and test-pause period. It shows two leader summits (#2005, #2006), a DMZ meeting (#2011), no nuclear
# test or ICBM launch between Nov 2017 (#2003) and Mar 2022 (#2018), only short-range launches in 2019 (#2008, #2009, #2013), and
# scaled-down drills when they resumed (#2012). It does not say the US ruled out drills or deployments, so the notes say so.
CONSTRAINTS = [
    (d(2018, 6, 12), d(2019, 8, 5), "Summit and test-pause period: two leader summits (#2005 Singapore, #2006 Hanoi) and a DMZ meeting (#2011). No nuclear test or ICBM launch is logged from Nov 2017 (#2003) to Mar 2022 (#2018).", [2005, 2006, 2011]),
]
CONSTRAINT_OPTIONS = ("D", "G")
CONSTRAINT_NOTES = {
    "2018-06-12": {
        "D": "During the Jun 2018 - Aug 2019 summit period the log shows no joint drill until the scaled-down August 2019 exercises (#2012). The log is a sample, so this is not proof that drills were ruled out.",
        "G": "During the Jun 2018 - Aug 2019 summit period the log shows no strategic-asset deployment (the next is the carrier visit of Sep 2022, #2021). The log is a sample, so this is not proof that deployments were ruled out.",
    },
}

NOW_FILE = "now.json"
