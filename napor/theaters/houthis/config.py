"""Houthis / Red Sea theater: wording, options, flags and rules, all in one place.

The research files (events_early.py, events_late.py) hold the facts and are read only. This file holds the
decisions the engine needs: which options exist, what counts as an attack by the other side, which outlets are
claims only, which weeks count as "hold" weeks, and the analyst notes the page shows.
"""
import datetime as dt

THEATER_ID = "houthis"


def d(y, m, day):
    return dt.date(y, m, day)


# ---- wording the page uses ------------------------------------------------------------------------------
THEATER = dict(
    id=THEATER_ID, name="Houthis / Red Sea", status="active", title="Houthis / Red Sea",
    sub="The options the US has toward the Houthis in Yemen and the Red Sea, and what followed the last times the US did something like each one.",
    adversary="the Houthis", actor="the Houthis or another Iran-backed group", actor_short="Houthis or proxy",
    proxy_note="Iran arms the Houthis, so seizures of Iranian arms bound for them are option E. A reply by another Iran-backed group would be labelled \"proxy\"; none is logged here.",
    salvo=None,
    hold_note="Hold cases are weeks, from Nov 20, 2023 on, with no logged US sanctions, naval, strike or posture move. Weeks inside the long stretches of fighting (Jan 12, 2024 - Jan 19, 2025 and Mar 15 - May 6, 2025) are left out, because US activity there was continuous. Most hold weeks fall in 2025-2026 and most have no logged event at all. The log for 2025-2026 records only major events, so a week where \"nothing happened\" may only be a week where nothing was logged. Read option A as a rough sketch, and do not compare it number-for-number with options that rest on a few well-reported cases.",
    not_measured="Oil and freight prices, ship insurance costs, harm to ordinary Yemenis and strain with Saudi Arabia are not measured.",
    presets=[["2016-10-13", "First US strikes (radar sites)"], ["2023-11-19", "Galaxy Leader seized"], ["2024-01-12", "First US-UK strikes"],
             ["2025-03-15", "Operation Rough Rider"], ["2025-05-06", "US-Houthi ceasefire"], ["2026-10-10", "Riyadh airport attack"]],
    under_logged="Some stretches are logged more thinly than others (2025-2026 far less than 2024), so \"none logged\" is not proof nothing happened.",
    spark_from="2016-10-01", claim_note="Houthi media (al-Masirah, Saba)",
    # Exact rule for the political corner (what theaters/common.py counts; changed 2026-10-26 with Sidd's approval): only logged talks, a meeting,
    # a proposal, a ceasefire or a deal. Statements, threats and appeals do not count.
    cats=dict(political=dict(
        other="Share of past cases NOT followed within 14 days by logged talks, a meeting, a formal proposal, a ceasefire or a deal between the US and the Houthis (directly or through a mediator such as Oman). Statements, threats and appeals do not count.",
        hold="Share of hold weeks NOT followed within 14 days by logged talks, a meeting, a formal proposal, a ceasefire or a deal between the US and the Houthis (directly or through a mediator such as Oman). Statements, threats and appeals do not count.",
        rule="Counts when no talks, meeting, negotiation, formal proposal (such as a UN resolution), ceasefire or deal between the US and the Houthis, directly or through a mediator such as Oman, was logged in the 14 days after. Public statements, threats and appeals do not count as talks (for example Trump's Jul 21 and Jul 23, 2026 warnings), so a threat alone does not stop a case from counting as a risk on this corner. Changed on 2026-10-26 with Sidd's approval.")),
)

# A tab needs at least this many counted cases to show a risk index; below it the page says "too few cases".
MIN_CASES = 3

# ---- options (letters are fixed; the page lists them in this order, never sorted) ------------------------
OPTIONS = [
    dict(key="A", name="Hold: no new action",
         what="Keep the current course: no new US strikes, sanctions, naval or posture move toward the Houthis."),
    dict(key="B", name="Diplomatic move",
         what="Talks or a ceasefire effort with the Houthis (for example through Oman), or a diplomatic step such as a UN resolution."),
    dict(key="C", name="New sanctions or designations",
         what="Treasury sanctions on Houthi finance, arms and oil networks, or a terrorist designation of the Houthis."),
    dict(key="D", name="Naval defense and escort",
         what="Warships protect shipping and shoot down Houthi missiles and drones aimed at ships (for example Operation Prosperity Guardian)."),
    dict(key="E", name="Block Iranian arms shipments",
         what="Board and seize Iranian weapons on their way to the Houthis."),
    dict(key="F", name="Strike Houthi military sites (equipment, not people)",
         what="Hit radar, missile, drone and storage sites in Yemen, aiming at equipment."),
    dict(key="G", name="Strike that risks killing leaders or personnel",
         what="Strikes on Houthi leaders, units or sites where people are likely to be killed."),
    dict(key="H", name="Change force posture (deploy or withdraw)",
         what="Send or move ships, aircraft, troops or advisers in the region, or pull some back."),
]

# trigger: escalation = "the Houthis replied within ~5 days" (Trigger Census); otherwise "the Houthis attacked within 7 days".
# military: "reply" = the reply was a missile, drone or boat attack (D-G); "strike" = an attack within 7 days (A); "none" = counted as 0%.
FLAGS = {
    "A": dict(trigger=False, military="strike", us_move=False, is_hold=True, salvo=False),
    "B": dict(trigger=False, military="none", us_move=False, is_hold=False, salvo=False),
    "C": dict(trigger=True, military="none", us_move=True, is_hold=False, salvo=False),
    "D": dict(trigger=True, military="reply", us_move=True, is_hold=False, salvo=False),
    "E": dict(trigger=True, military="reply", us_move=True, is_hold=False, salvo=False),
    "F": dict(trigger=True, military="reply", us_move=True, is_hold=False, salvo=False),
    "G": dict(trigger=True, military="reply", us_move=True, is_hold=False, salvo=False),
    "H": dict(trigger=False, military="none", us_move=True, is_hold=False, salvo=False),
}
US_MOVE_KINDS = ("Sanctions", "Maritime", "Kinetic", "Posture")     # kinds of act that make a week "not a hold week"

# ---- sources and actors -----------------------------------------------------------------------------------
CLAIM_MEDIA = {"al-Masirah", "Saba"}                    # Houthi outlets: allowed only as labelled claims, scored 0.30
CLAIM_LABEL = "Houthi media (claim only)"


def us_side(actor):
    return actor.lower().startswith("us")


def adversary_side(actor):
    """The Houthis themselves (including 'per US', 'claimed' and 'Houthis suspected' labels). The Saudi-backed Yemeni
    government and the Yemeni National Resistance Forces are not the Houthis."""
    a = actor.lower()
    return a.startswith("houthi") or a.startswith("unknown (houthi")


ATTACK_KINDS = ("Kinetic", "Maritime")                  # a hostile act by the other side: a strike, or an attack/seizure at sea
# Houthi missile/drone strikes on commercial ships that the action-type words file as "Kinetic" (no "shipping" in the
# type). They count as attacks on shipping for the economic measure and stay "Kinetic" for the military measure.
# Attacks aimed only at US warships (#1001, #1002, #1004, #1022, #1308) are not attacks on shipping.
SHIP_ATTACK_EXTRA = {
    1013,   # ballistic missile at USS Mason and the tanker Central Park (CENTCOM)
    1017,   # Maersk Hangzhou hit (USNI)
    1019,   # 21 drones and missiles fired toward Red Sea shipping lanes (USNI)
    1023,   # US-owned Gibraltar Eagle hit (CENTCOM)
    1029,   # tanker Marlin Luanda hit (CENTCOM)
}

# The log's action-type words put a few rows in the wrong kind. Fixed by event ID, with the reason.
KIND_OVERRIDE = {
    1308: "Kinetic",   # Houthis CLAIM missiles and a drone at the Truman group; the US confirmed an attempted attack (USNI)
    1302: "Kinetic",   # claimed attack on the Truman group (not confirmed, so not counted anyway)
    1330: "Other",     # a threat to restart attacks, not an attack
    1336: "Other",     # Trump declines a Saudi request for strikes: no strike happened
}

# ---- hold weeks (option A) -------------------------------------------------------------------------------
HOLD_START = d(2023, 11, 20)                             # first Monday after the Galaxy Leader seizure (Nov 19, 2023)
MIN_HOLD_WEEKS = 3                                       # fewer than this: option A shows "too few cases", no weeks are invented
UNCERTAIN = {                                            # Monday ISO date -> reason (an allowed outlet reports a US move missing from the log)
    "2023-11-20": "USS Mason and coalition ships answered the Central Park distress call and detained the hijackers on Nov 26 (CENTCOM, cited for #1013); a US naval-defense move that is not logged as its own row.",
    "2023-11-27": "USS Carney shot down three Houthi drones on Dec 3 while defending commercial ships (USNI, cited for #1014); a US naval-defense move that is not logged as its own row.",
}
# Set by hand from the logged damage text of every hostile act in the 7 days after the Monday (see hold_hurt_candidates()).
# monday: (anyone hurt?, evidence event IDs, note)
# A hold week with no Houthi attack logged in the 7 days after needs no entry: it is set to (False, [], "No hostile act logged.") automatically.
PEOPLE_HURT = {
    "2023-11-20": (False, [1013], "Ballistic missile lands about 10 nautical miles from USS Mason: no damage or injuries (CENTCOM)."),
    "2023-11-27": (False, [1014], "Missiles hit three commercial ships and USS Carney was targeted: minor to moderate damage, no casualties (CENTCOM)."),
    "2025-06-30": (True, [1320, 1321], "Eternity C attack: at least 4 killed early, at least 9 per USNI (Al Jazeera, USNI); Magic Seas crew rescued."),
    "2025-08-25": (False, [1325], "Missile missed the Scarlet Ray: no damage, crew safe (UKMTO via Times of Israel)."),
    "2025-09-22": (True, [1327], "Minervagracht: one crew member later died, one injured (AP, USNI)."),
    "2026-07-20": (False, [1333], "Saudi tanker Encelia hit by fire: no deaths reported (AFP via Ahram Online)."),
    "2026-10-05": (True, [1339, 1340], "Riyadh airport attacks: 3 Saudis killed on Oct 8, then 12 killed and 309 wounded on Oct 10 (Saudi civil aviation via Al Jazeera, NPR)."),
    "2026-10-19": (True, [1345, 1346], "Shaybah oilfield drone (Oct 20): 2 killed, 2 injured by debris, attacker not named by Saudi Arabia (CBS, Reuters); Dammam airport attack (Oct 21): 1 killed, 8 injured (Saudi civil aviation via Reuters). #1348 is a Houthi claim with no casualties stated."),
}

CIVILIAN_HARM = {}        # no civilian harm reported in an allowed outlet for any counted US move (Houthi casualty claims are not counted)

# ---- the backtest -----------------------------------------------------------------------------------------
OOS_CUT = d(2025, 12, 31)
OOS_LABEL = "2016-2025"


def period(day):
    if day < d(2023, 10, 1):
        return "2016-23"
    if day < d(2025, 1, 1):
        return "2024"
    if day < d(2025, 7, 1):
        return "2025 H1"
    return "2025 H2+"


PERIOD_KEYS = ["2016-23", "2024", "2025 H1", "2025 H2+"]

# ---- analyst notes (judgement, not data; every line is labelled that way on the page) -----------------------
PROS = {
    "A": "No new US act for the Houthis to answer. Keeps the May 2025 US-Houthi ceasefire in place; since May 6, 2025 the log shows no US strike on the Houthis and no Houthi attack on US forces.",
    "B": "No direct casualties. The May 6, 2025 Oman-brokered ceasefire ended the US bombing campaign, and US officials met Houthi officials in Muscat on Sep 12-13, 2026 (Reuters).",
    "C": "Financial pressure with no casualties and no risk to US forces. Rounds have come every few months (Jan, Apr, Jul and Sep 2025; Jan 2026).",
    "D": "Aims directly at the attacks on shipping. US and UK ships shot down 21 Houthi drones and missiles on Jan 9, 2024 without any injuries reported.",
    "E": "Takes weapons away before they reach Yemen: 150 missiles (2020), 2,116 rifles (2023) and 750+ tons of arms (Jul 2025, by Yemeni partners) are in the log.",
    "F": "Aims at the launch, radar and storage sites that make the attacks possible (the military effect is claimed by CENTCOM, not independently measured).",
    "G": "Can remove commanders and units; CENTCOM says Operation Rough Rider killed \"numerous Houthi leaders\" (a US claim, not independently measured).",
    "H": "No direct harm. Adding forces strengthens defense; the log has the Mar 2025 second carrier and US advisers in Saudi Arabia (Sep 2026).",
}
HARMS = {
    "A": "Houthi attacks on shipping and on Saudi Arabia can go on without a US move (the Jul 2025 sinkings of Magic Seas and Eternity C; the Oct 2026 Riyadh airport attacks). Whether holding back changes what the Houthis do cannot be measured from this log.",
    "B": "Talks have not always ended the attacks: attacks on shipping resumed in July 2025, two months after the US-Houthi ceasefire. Political costs of talking to a group the US designates as terrorist are not measured.",
    "C": "No measured effect on Houthi attacks; the log shows no Houthi attack on US forces in the days after any counted round. Harm to ordinary Yemenis from financial pressure is not measured.",
    "D": "Escort and defense put warships within range of Houthi missiles: the Houthis fired at US warships in 2016 and in 2023-2025. Crews on commercial ships were killed in several attacks (for example Mar 6, 2024).",
    "E": "Few cases, and the 2025 one was carried out by Yemeni forces, not US forces. The log shows no Houthi attack on US forces or shipping in the 5 days after any of them.",
    "F": "The Houthis fired at US warships or hit US-linked ships within days of the first strikes in 2016, 2024 and 2025. Strikes inside long stretches of fighting are logged as context and are not counted as cases.",
    "G": "Houthi media reported mass-casualty strikes in 2025 (the Ras Isa port and a Saada migrant center); AFP could not confirm the Saada claim. These sit inside the Mar-May 2025 fighting, so they are not counted cases.",
    "H": "Advisers and deployments can draw the US closer to a Saudi-Houthi war; the Houthis warned of a \"swift and painful response\" if the US joins (Oct 12, 2026). No Houthi attack on US forces followed the Sep 2026 advisers report in the log.",
}
UNKNOWNS = {
    "A": "No Houthi attack on US forces or on non-Saudi shipping is logged after Sep 29, 2025 (the Houthis signalled a pause on Nov 11, 2025); Houthi attacks on Saudi targets are logged from Jul 2026. Whether the pause with the US holds if the Saudi-Houthi fighting grows is not in the data.",
    "B": "Few diplomatic moves are logged, so there is no reliable reply rate for talks. What the Muscat meeting (Sep 12-13, 2026) produced is not reported.",
    "C": "The Jan 2025 and Mar 2025 designation steps came during a Houthi pause; the effect of each on later attacks cannot be told apart from the pause itself.",
    "D": "Every naval-defense row sits inside the Dec 2023 - Dec 2024 fighting, where a reply cannot be told apart from the fighting that was already going on, so no case is counted.",
    "E": "Only 3 counted cases, none drew a logged Houthi attack within 5 days. Seizures may be under-reported.",
    "F": "Only 3 counted cases: the strikes that opened a new round of fighting (2016, Jan 2024, Mar 2025). Later strikes are context only.",
    "G": "No counted case: the leader and casualty strikes (Dec 31, 2023; Apr 2025) all happened inside continuous fighting.",
    "H": "Only 2 posture cases. How the Houthis read deployments or advisers is not measured.",
}

# ---- constraint periods (limit which options are open); notes are per option letter -------------------------
CONSTRAINT_OPTIONS = ("F", "G")

# ---- napor_now.json for this theater lives next to this file (written by the weekly agent) -------------------
NOW_FILE = "now.json"

# ---- plain-language risk lines (the page's "What the log says"; filled in by theaters/common.py) -----------------------
THREAD_PREFIX = "H"
LOOKBACKS = ("2016-10-14", "2023-12-31", "2024-06-30", "2025-05-06", "2026-09-10")      # past dates the page test also checks (no hindsight)
RISK_TEXT = dict(
    people_trigger="Replies that hurt people: {hurt} of {n} logged{detail}. Civilian harm reported in the US act itself: none in an allowed outlet.",
    people_hold="Ship crews: attacks on shipping have been logged at about {per_week} a week in the current phase. No new US act to answer.",
    people_sanctions="No direct casualties. Harm to ordinary Yemenis from sanctions: not measured.",
    people_other="No direct casualties from the move itself.",
    esc_trigger="The Houthis or a group they work with replied within ~5 days: {reply} (range {range}). Fast (within 2 days): {fast}. Back-and-forth past one reply: {longer}.",
    esc_hold="No new US trigger. The Houthis attacked in some weeks anyway (see the hold-week cases). Whether holding back changes what they do: not measured.",
    esc_timing="The Houthis attacked within 7 days after {strikes} past cases (timing only, not shown to be replies). Reply rate: not measured for this option.",
    no_cases="No past cases, so no measure.",
    mil_reply="A missile, drone or boat attack followed within ~5 days in {k} of {n} past cases. Losses of US equipment in those replies: none logged.",
    mil_strike="Share of hold weeks with a Houthi attack in the 7 days after (see the cases).",
    mil_none="No military cost expected from the move itself.",
    eco_cases="Attacks on shipping, 7 days before -> after past cases: {shipping} (total). Oil prices and freight costs: not measured.",
    eco_baseline="Baseline: about {per_week} logged attacks on shipping a week in the current phase. Oil prices and freight costs: not measured.",
    pol_cases="Talks within 14 days after: {talks} (statements and threats do not count). Strain with Saudi Arabia and the Gulf: not measured.",
    pol_none="No past cases, so no measure. Strain with Saudi Arabia and the Gulf: not measured.",
)
