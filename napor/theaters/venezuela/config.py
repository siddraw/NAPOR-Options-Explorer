"""Venezuela / Caribbean theater: wording, options, flags and rules, all in one place.

The event files (events_pre2019.py for Feb 1999 - Jan 10, 2019 and events.py from Jan 23, 2019, both written separately) hold the facts and are read only. rules.py joins them and gives this tab's view of them (see below). This file holds
the decisions the engine needs: which options exist, what counts as an act by the other side, which outlets are claims only, how each of the
five risk categories is defined here, which weeks count as "hold" weeks, and the analyst notes the page shows (notes.py).

SMALL NUMBERS: only 8 of about 70 US boat strikes are logged one by one, most Venezuelan replies are statements (which do not count as an
escalation reply here), and option G (raids or operations against leaders) has one case (the Jan 2-3, 2026 Maduro capture). The page says so
on every option (THEATER["small_n"]). Options with fewer than 3 counted cases show "too few cases" instead of a percentage.

The five categories, exactly as defined for this tab (the page shows these words; the rules are in theaters/common.py):
  people      anyone killed or hurt in the US action itself OR in a Venezuelan reply, as the logged source reports it. Boat-strike deaths count.
  escalation  a hostile act by Venezuela or an armed group within 7 days of the move: an attack, harassment of US assets, or a military
              mobilization announced as a response. Words alone do not count. A diplomatic step or an economic step is not a hostile act here
              (economic steps have their own category). Taken from the list of past cases as seen through rules.py: a row the event file marks
              as a reply keeps that status only if such an act is logged 0-7 days after the move; otherwise it counts as N.
  military    the reply was armed action: an attack on, or armed harassment of, US forces or assets (the logged action type starts with
              "Attack", "Harassment" or "Strike"). A mobilization announcement, a militia call-up or a national exercise does not.
  economic    Venezuelan counter-measures within 14 days of the move: an oil or gas cut-off, an airline ban, or the expulsion of firms or diplomats
              (a Venezuelan act whose action type starts with "Economic act" or "Diplomatic break"). Timing only: the log does not show the
              US move caused it. Only 3 such acts are logged (#4002, #4029, #4041).
  political   no talks or deal within 14 days (rule changed 2026-10-26): no logged US move of option B (talks, an oil deal or license,
              a prisoner swap, restored ties, an embassy reopening) in the 14 days after the move. Statements and threats do not count.
"""
import datetime as dt

from theaters.venezuela import acts

THEATER_ID = "venezuela"


def d(y, m, day):
    return dt.date(y, m, day)


# ---- wording the page uses ------------------------------------------------------------------------------
THEATER = dict(
    id=THEATER_ID, name="Venezuela / Caribbean", status="active", title="Venezuela and the Caribbean",
    sub="The options the US has toward Venezuela and the Caribbean drug-boat campaign, and what followed the last times the US did something like each one.",
    adversary="Venezuela or armed groups", actor="Venezuela or an armed group", actor_short="Venezuela",
    proxy_note="Every reply here is an act by Venezuela itself (its government, ministers or armed forces) or by an armed group. Venezuelan state media (Telesur, VTV) is used only as labelled claims of what the government says. Cuban, Russian and Trinidadian statements are not replies. After the Jan 3, 2026 capture of Maduro the interim government has cooperated with Washington; cooperative answers are not replies.",
    salvo=None,
    hold_note="Hold cases are weeks, from Aug 11, 2025 on (the first Monday after the Maduro bounty was doubled), with no logged US sanction, deployment, boat strike, land strike, raid, seizure or talks move. Weeks inside the two stretches of near-daily boat strikes (Oct 27 - Nov 15, 2025 and Dec 15, 2025 - Jan 2, 2026) are left out, and so are weeks where outlet counts show boat strikes that the log does not hold one by one (Sep 22 - Oct 6 and Dec 1, 2025, and Jan 26 - Jun 22, 2026). Be careful: about 70 boat strikes are known and only 8 are logged one by one, so even the weeks that remain may have had an unlogged strike. The log is a sample, so a quiet week may only be a week where nothing was logged. Read option A as a rough sketch and do not compare it number for number with options that rest on well-reported cases.",
    not_measured="Oil output and prices, migration, food and medicine supply, harm to ordinary Venezuelans from sanctions, and strain with Colombia, Cuba, Russia and Caribbean states are not measured. Only the five categories above are counted.",
    presets=[["2025-08-07", "Maduro bounty doubled"], ["2025-09-02", "First boat strike"], ["2025-10-24", "Carrier ordered to SOUTHCOM"],
             ["2025-12-16", "Tanker blockade ordered"], ["2026-01-03", "Maduro captured"], ["2026-04-01", "Rodriguez delisted"],
             ["2002-04-12", "2002 coup attempt"], ["2006-05-15", "US arms-sales ban"], ["2008-09-11", "Ambassadors expelled"],
             ["2015-03-09", "Emergency order"], ["2017-08-11", "'Military option' remark"]],
    under_logged="The log is a sample. 1999-2008 is thin and many of its rows rest on one Congressional Research Service report, 2009-2016 holds mostly expulsions and a few sanctions, and the Dec 2017 talks and the Nov 2017 sanctions are missing. 2020-2024 holds only a few key moves, only 8 of about 70 boat strikes are logged one by one, and Venezuelan state media was not opened, so \"none logged\" is not proof nothing happened.",
    spark_from="1999-02-01", thin_before="2019-01-01", claim_note="Venezuelan state media (Telesur, VTV)",
    small_n="Only 8 of about 70 boat strikes are logged one by one, most Venezuelan replies are statements (which do not count as an escalation reply here), and option G (raids or operations against leaders) has 1 case. Most options have only a handful of counted cases (the exact number is on each option), and options with fewer than 3 show \"too few cases\" instead of a percentage. Read every rate as a hint, not a forecast.",
    us_hurt="Anyone killed or hurt in the US action",
    # ---- per-theater words and rules the page reads (defaults on the page are the Iran / Houthi words) ----
    reply_days=7,
    intensity=dict(name="Tension level", note="Tension level counts logged hostile acts by Venezuela or an armed group (attacks, harassment of US assets, military mobilizations) in the 14 days before each date: 2 points each, +2 if someone died. Statements and economic steps are not counted. The log is a sample, so quiet stretches are understated."),
    base=dict(noun="Venezuelan hostile acts", short="Venezuelan acts", kinds=["Kinetic"]),
    act=dict(verb="took a hostile act (an attack, harassment or a mobilization) within 7 days", row="takes a hostile act within 7 days", col="Act ≤7d", none="No hostile act"),
    econ=dict(mode="events", days=14, name="Economic harm", label="Venezuela answers with a counter-measure (an oil or gas cut-off, an airline ban, expelling firms or diplomats) within 14 days"),
    cats=dict(
        people=dict(name="Harm to people", short="People hurt",
                    other="Share of past cases where the logged source reports anyone killed or hurt in the US action itself or in a Venezuelan reply the log links to the move.",
                    hold="Share of hold weeks in which a Venezuelan hostile act in the 7 days after hurt anyone.",
                    rule=dict(other="Counts when a logged source reports anyone killed or hurt in the US action itself (for example the people killed on a boat, as the source reports them; whether they were drug traffickers is not tested here) or in a Venezuelan reply the log links to the move. Linked replies are usually within 7 days; the longest logged lag is 18 days (#4031), so a case stays open for 18 days unless harm is already known.",
                              hold="Counts when a Venezuelan hostile act in the 7 days after the Monday hurt anyone.")),
        escalation=dict(name="Escalation", short="Escalation",
                        trigger="Share of past cases followed within 7 days by a hostile act from Venezuela or an armed group: an attack, harassment of US assets, or a military mobilization announced as a response. Words alone do not count.",
                        other="Share of past cases followed within 7 days by any logged Venezuelan hostile act (an attack, harassment or a mobilization; timing only).",
                        hold="Share of hold weeks followed within 7 days by a logged Venezuelan hostile act (an attack, harassment or a mobilization; timing only).",
                        rule=dict(trigger="Counts when Venezuela or an armed group took a hostile act within 7 days of the move: an attack, harassment of US assets, or a military mobilization announced as a response. A statement, a denunciation, a diplomatic step or an economic step does not count (a clear link or timing only, kept only when such an act is logged 0-7 days after the move). Several denunciations that the event file marks as weak replies are counted as no reply here.",
                                  other="Counts when the log holds any Venezuelan hostile act (an attack, harassment or a mobilization) in the 7 days after the move (timing only, not shown to be a reply).")),
        military=dict(name="Military cost", short="Military cost",
                      reply="Share of past cases where the Venezuelan reply was armed action: an attack on, or armed harassment of, US forces or assets.",
                      strike="Share of hold weeks with an armed Venezuelan attack or harassment of US assets in the 7 days after.",
                      none="No direct military cost expected from the move itself, so this counts as 0%.",
                      rule=dict(reply="Counts when a Venezuelan reply the log links to the move was armed action (an attack on, or armed harassment of, US forces or assets; so far only military aircraft flying near USS Jason Dunham on Sep 4, 2025, #4019). A mobilization announcement, a militia call-up, a national exercise and a statement do not count.",
                                strike="Counts when an armed Venezuelan attack or harassment of US assets took place in the 7 days after the Monday.")),
        economic=dict(name="Economic harm", short="Economic",
                      other="Share of past cases followed within 14 days by a Venezuelan counter-measure: an oil or gas cut-off, an airline ban, or the expulsion of firms or diplomats (timing only, not shown to be caused by the US move).",
                      rule="Counts when Venezuela announced a counter-measure (an oil or gas cut-off, an airline ban, or the expulsion of firms or diplomats) within 14 days after the move. Only 3 are logged (#4002, #4029, #4041); #4041 is dated by the Reuters report, not the day it took effect. The window starts the day after the move, so a same-day act (the 2019 expulsion order, #4002) is not counted."),
        political=dict(name="Political / diplomatic", short="Political",
                       other="Share of past cases NOT followed within 14 days by talks or a deal between the US and Venezuela (a call, a meeting, an oil deal or license, a prisoner swap, restored ties).  Statements and threats do not count.",
                       rule="Counts when no US talks or deal with Venezuela (a call, a meeting, an oil deal or license, a prisoner swap, restored ties or an embassy reopening, directly or through a mediator) were logged within 14 days after the move. Statements, threats and appeals do not count as talks. Rule changed on 2026-10-26."),
    ),
)

# A tab needs at least this many counted cases to show a risk index; below it the page says "too few cases".
MIN_CASES = 3

# ---- options (letters are fixed, as tagged in events.py; the page lists them in this order, never sorted) ------
OPTIONS = [
    dict(key="A", name="Hold: no new action",
         what="Keep the current course: no new US sanction, deployment, boat strike, land strike, raid, seizure or talks move toward Venezuela."),
    dict(key="B", name="Talks or deals",
         what="Phone calls and talks, prisoner swaps, oil licenses and deals, and (after the capture) restored ties, an embassy and direct flights with the interim government."),
    dict(key="C", name="Sanctions, designations and indictments",
         what="Oil and sector sanctions, indictments and bounties, the Cartel de los Soles terrorist designation, and sanctions relief such as delistings."),
    dict(key="D", name="Boat strikes",
         what="Military strikes on boats said to be carrying drugs, in the Caribbean and the eastern Pacific."),
    dict(key="E", name="Naval and air deployments and posture",
         what="Warships, an amphibious group, F-35s, a carrier strike group, bomber shows of force and the Southern Spear operation."),
    dict(key="F", name="Land strikes",
         what="Strikes on targets on land, for example the Dec 2025 dock strike and the Jun 2026 strike on a Tren de Aragua compound."),
    dict(key="G", name="Raids or operations against leaders",
         what="Operations aimed at a country's leaders, for example the Jan 2-3, 2026 raid that captured Maduro."),
    dict(key="H", name="Other",
         what="Recognition of an opposition leader, airspace closure and aviation warnings, tanker seizures and a blockade order, and covert-action authorization."),
]

# trigger: escalation = "Venezuela or an armed group replied with a hostile act within 7 days" (the list of past cases as seen through rules.py).
# military: "reply" = the reply was armed action; "strike" = such an act within 7 days (A, hold weeks).
# Closing window in days per category: when a case's outcome is final (read by the case builder, the backtest and the page).
# People and military: linked replies count at any lag, and the longest logged lag of a linked reply is 18 days (#4027 -> #4031, the national
# exercise), so both close at 18 (the backtest check requires the window to reach that lag, even though the one armed reply, #4019, came on day 2).
# A case where harm in the US action is already known closes at once for people. Escalation is judged at reply_days (7), economic at 14, political at 14.
CLOSE = dict(people=18, escalation=7, military=18, economic=14, political=14)
_W = dict(close=CLOSE, reply_days=7, econ_days=14)
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
US_MOVE_KINDS = ("Sanctions", "Posture")     # kinds of act that make a week "not a hold week" (the option letters C-H do too)
REPLY_DAYS = 7
ECON = dict(mode="events", days=14, kinds=("Sanctions",))     # a Venezuelan counter-measure within 14 days (the "Sanctions" kind on the adversary's side)

# ---- sources and actors -----------------------------------------------------------------------------------
CLAIM_MEDIA = {"Telesur", "TeleSUR", "VTV", "Venezolana de Televisión", "Venezolana de Television", "Venezuelan state media"}   # allowed only as labelled claims, scored 0.30
CLAIM_LABEL = "Venezuelan state media (claim only)"


def us_side(actor):
    return actor.lower().startswith("us")


def adversary_side(actor):
    """Venezuela itself (including 'per Pentagon' and 'per state media' labels) or an armed group. Cuba is not."""
    return acts.adversary_side(actor)


# The shared word list does not know these rows; this tab sorts them by the words at the start of the action type and, for US moves, by option letter.
def KIND_OF(e):
    from theaters.venezuela import rules as EV      # the two event files joined
    a = e[3]
    if adversary_side(e[2]):
        if acts.is_hostile(a):
            return "Kinetic"            # an attack, harassment of US assets or a military mobilization
        if acts.is_countermeasure(a):
            return "Sanctions"          # an oil or gas cut-off, an airline ban, or the expulsion of diplomats (the economic category)
        return "Other"                  # a statement, a denunciation or a concession
    if us_side(e[2]):
        opt = EV.US_OPTION.get(e[0])
        if opt == "B":
            return "Diplomatic"         # talks, a swap, an oil license or deal, restored ties
        if opt == "C":
            return "Sanctions"
        if opt in ("E", "H"):
            return "Posture"
        if opt in ("D", "F", "G"):
            return "Kinetic"
    return "Other"


KIND_OVERRIDE = {}
ATTACK_KINDS = ("Kinetic",)                  # a hostile act by Venezuela or an armed group (never a statement)
BASELINE = "attack"                          # the "no new US move" baseline counts hostile acts per week

# the military reply: armed action only
def MILITARY_REPLY(e):
    return adversary_side(e[2]) and acts.is_armed(e[3])


def HOSTILE_TEST(e, kind):
    """Rows that add points to the tension scale: Venezuelan hostile acts (not statements, not economic steps)."""
    return adversary_side(e[2]) and kind == "Kinetic"


BASELINE_TEST = HOSTILE_TEST


# ---- hold weeks (option A) -------------------------------------------------------------------------------
HOLD_START = d(2025, 8, 11)                              # first Monday after the Maduro bounty was doubled (Aug 7, 2025)
MIN_HOLD_WEEKS = 3                                       # fewer than this: option A shows "too few cases", no weeks are invented
# Monday ISO date -> reason (allowed outlets' own running counts show boat strikes that are not logged one by one; only 8 of about 70 are).
# A week is marked uncertain only where those counts show unlogged strikes in the stretch. Weeks the counts show as quiet stay hold weeks.
_REASON_2025 = "Outlet counts show boat strikes in this stretch that are not logged one by one: AP counted five boats destroyed by Oct 15, 2025 (#4024) against two logged strikes before it (#4017, #4022); NPR counted about 20 strikes by Nov 16 (#4033) and 25 by Dec 16 (#4044) against the logged ones. A strike may have fallen in this week."
_REASON_2026 = "AP counted 36 known strikes by Jan 23, 2026 (#4055) and more than 60 by Aug 24 (#4062), calling that strike the first in two months, so about two dozen boat strikes fell between late January and late June 2026 and only #4055 is logged. A strike may have fallen in this week."
UNCERTAIN = {"2025-09-22": _REASON_2025, "2025-09-29": _REASON_2025, "2025-10-06": _REASON_2025, "2025-12-01": _REASON_2025}
_m = d(2026, 1, 26)
while _m <= d(2026, 6, 22):
    UNCERTAIN[_m.isoformat()] = _REASON_2026
    _m += dt.timedelta(days=7)
# Set by hand from the logged damage text of every hostile act in the 7 days after the Monday (see hold_hurt_candidates()).
# monday: (anyone hurt?, evidence event IDs, note)
# A hold week with no Venezuelan hostile act logged in the 7 days after needs no entry: it is set to (False, [], "No hostile act logged.") automatically.
PEOPLE_HURT = {
    "2025-08-11": (False, [4012], "Maduro announces a militia plan and grounds drones on Aug 18: no damage or injuries (Al Jazeera)."),
}

# What the logged source reports about anyone killed or hurt in the US action itself (the page's "harm in the US action" line; the name is the engine's).
# These are the sources' numbers, as stated; the US claim that the boats carried drugs is not tested here.
CIVILIAN_HARM = {
    4017: "11 killed (Trump); no US forces harmed (Trump)",
    4022: "3 killed (Trump)",
    4023: "6 killed (Trump, per Axios)",
    4030: "14 killed in total, 1 survivor (Hegseth, per AP)",
    4043: "8 killed in total (AFP)",
    4049: "A few US service members injured (AP); Venezuelan officials say at least 24 security officers were killed (AP via NPR); Cuba says 32 of its personnel were killed (Cuban government claim)",
    4055: "2 killed, 1 survivor (SOUTHCOM, per AP)",
    4061: "Tren de Aragua leader Hector Guerrero Flores killed (Trump); no other deaths reported",
    4062: "2 killed (Pentagon, per AP)",
    4064: "4 killed (SOUTHCOM)",
}

# ---- the backtest -----------------------------------------------------------------------------------------
OOS_CUT = d(2025, 12, 31)
OOS_LABEL = "1999-2025"


def period(day):
    if day < d(2009, 1, 1):
        return "1999-2008"
    if day < d(2019, 1, 1):
        return "2009-18"
    if day < d(2025, 8, 1):
        return "2019-24"
    if day < d(2026, 1, 3):
        return "Buildup 2025"
    return "After capture"


PERIOD_KEYS = ["1999-2008", "2009-18", "2019-24", "Buildup 2025", "After capture"]
LOOKBACKS = ("2002-06-01", "2006-06-01", "2010-01-15", "2015-06-01", "2017-12-01", "2018-10-05", "2020-04-01", "2025-09-10", "2025-11-20", "2026-01-10", "2026-08-01")      # past dates the page test also checks (no hindsight)

# ---- plain-language risk lines (the page's "What the log says"; filled in by theaters/common.py) -----------------------
THREAD_PREFIX = "V"
RISK_TEXT = dict(
    people_trigger="Replies that hurt people: {hurt} of {n} logged{detail}. Harm in the US act itself is counted separately (see the cases).",
    people_hold="Venezuelan hostile acts (attacks, harassment, mobilizations) have been logged at about {per_week} a week in the current phase. No new US act to answer.",
    people_sanctions="No direct casualties from the sanctions, indictments or delistings themselves. Harm to ordinary Venezuelans from sanctions: not measured.",
    people_other="No direct casualties from the move itself.",
    esc_trigger="Venezuela or an armed group replied with a hostile act (an attack, harassment or a mobilization) within 7 days: {reply} (range {range}). Fast (within 2 days): {fast}. Back-and-forth past one reply: {longer}. Small numbers: read as a hint.",
    esc_hold="No new US trigger. Hold weeks are a rough sketch only (see the note on option A).",
    esc_timing="Venezuela took a logged hostile act within 7 days after {strikes} past cases (timing only, not shown to be replies). Reply rate: not measured for this option.",
    no_cases="No past cases, so no measure.",
    mil_reply="A linked reply was armed action (an attack or harassment of US assets) in {k} of {n} past cases. Losses of US equipment in those replies: none logged.",
    mil_strike="Share of hold weeks with an armed Venezuelan attack or harassment of US assets in the 7 days after (see the cases).",
    mil_none="No military cost expected from the move itself.",
    eco_cases="Venezuelan counter-measures (oil or gas cut-offs, airline bans, expulsions) within 14 days after past cases: {shipping}. Oil prices and output: not measured.",
    eco_baseline="Baseline: about {per_week} logged Venezuelan hostile acts a week in the current phase. Oil prices and output: not measured.",
    pol_cases="Talks or a deal within 14 days after: {talks} (statements and threats do not count). Strain with Colombia, Cuba, Russia and Caribbean states: not measured.",
    pol_none="No past cases, so no measure. Strain with Colombia, Cuba, Russia and Caribbean states: not measured.",
)

# ---- analyst notes (judgement, not data; every line is labelled that way on the page) -----------------------
from theaters.venezuela.notes import PROS, HARMS, UNKNOWNS     # noqa: E402

CONSTRAINT_OPTIONS = ()      # the log supports no constraint period for Venezuela
NOW_FILE = "now.json"
