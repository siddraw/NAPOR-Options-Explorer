"""
Shared data for the Iran war event database.

Both build.py (the Excel workbook) and matcher.py (the event matcher) import
from here, so there is exactly one copy of the history - no risk of the
spreadsheet and the matcher ever disagreeing about what happened.
"""
import datetime as dt


def d(y, m, day):
    return dt.date(y, m, day)


# ---------------------------------------------------------------------------
# EVENT LOG
# Columns: ID, Date, Actor, Action Type, Target, Detail, Trigger ID, Severity, Confidence, Source
# ---------------------------------------------------------------------------
events = [
(1,  d(2026,2,27), "US",        "Authorization",         "Iran",            "Trump authorizes Operation Epic Fury aboard Air Force One", None, "n/a", "High", "Wikipedia: 2026 Iran war"),
(2,  d(2026,2,28), "US/Israel", "Strike (war start)",     "Iran",            "Operation Epic Fury: ~900 strikes in 12hrs; Khamenei and senior officials killed; strike near Minab naval base hits girls' school", None, "Khamenei + senior officials killed; 148-168 killed at school (mostly girls)", "High", "Wikipedia: 2026 Iran war"),
(3,  d(2026,2,28), "US",        "Strike",                 "Iran",            "Sinks IRIS Bayandor, IRIS Naghdi, IRIS Shahid Bagheri (contested claims)", 2,    "3 vessels claimed (contested)", "Medium", "Wikipedia: List of ships attacked"),
(4,  d(2026,2,28), "Iran",      "Blockade start",         "Strait of Hormuz","IRGC declares no ships permitted through the Strait - blockade phase 1", 2,    "Ship traffic drops ~70%", "High", "Wikipedia: 2026 Strait of Hormuz crisis"),
(5,  d(2026,2,28), "Iran",      "Retaliation strike",     "Israel/Gulf",     "Operation True Promise IV: Tel Aviv, Kuwait Int'l Airport, Manama (5th Fleet HQ), Al Udeid AB Qatar, Jordan (49 intercepted)", 2, "1 killed, 27 injured (Tel Aviv)", "High", "Wikipedia: 2026 Iranian strikes on Arab countries"),
(6,  d(2026,3,1),  "Iran",      "Retaliation strike",     "Jordan/Gulf",     "Strikes THAAD radar in Jordan/UAE/Saudi, Manama, Kuwait airport, Abu Dhabi, Riyadh, Erbil", 2, "1 AN/TPY-2 radar destroyed", "High", "Wikipedia: 2026 Iranian strikes on Jordan"),
(7,  d(2026,3,1),  "Iran",      "Retaliation strike",     "Kuwait",          "Strikes Camp Arifjan / Port of Shuaiba", None, "6 US KIA - first confirmed US deaths of the war", "High", "Wikipedia: List of U.S. service members killed"),
(8,  d(2026,3,1),  "US",        "Strike",                 "Iran",            "Sinks IRIS Jamaran (Chabahar) and IRIS Makran (Bandar Abbas)", None, "2 frigates", "Medium", "Wikipedia: List of ships attacked"),
(9,  d(2026,3,2),  "Iran",      "Retaliation strike",     "Bahrain/Kuwait",  "Strikes tanker Stena Imperative at Bahrain port; US embassy Kuwait struck", None, "1 killed, 2 injured", "High", "Wikipedia: 2026 Iran war"),
(10, d(2026,3,3),  "US/Israel", "Strike",                 "Iran",            "Destroys SNSC HQ, Expediency Discernment Council building; strikes alleged underground site 'Min Zadai'", None, "n/a", "High", "Wikipedia: 2026 Iran war"),
(11, d(2026,3,3),  "Iran",      "Retaliation strike",     "Saudi Arabia",    "CIA annex at US embassy Riyadh hit by Iranian drones", 10, "n/a", "Medium", "Wikipedia: 2026 Iran war"),
(12, d(2026,3,4),  "Iran",      "Retaliation strike",     "Qatar/Saudi",     "Strikes Al Udeid AB and Aramco's Ras Tanura refinery", None, "n/a - trigger: same-day US/Israeli intensification announcement", "High", "Wikipedia: 2026 Iran war"),
(13, d(2026,3,4),  "US",        "Strike",                 "Iran",            "USS Charlotte submarine sinks IRIS Dena ~40nm off Sri Lanka", None, "104 killed, 32 wounded", "High", "Wikipedia: 2026 Iran war"),
(14, d(2026,3,10), "Iran",      "Blockade escalation",    "Strait of Hormuz","Mine-laying detected; Iranian strike rate falls ~92% (read as stockpile depletion)", None, "16 minelayers later claimed destroyed by US", "Medium", "Wikipedia: 2026 Strait of Hormuz crisis"),
(15, d(2026,3,19), "US",        "Strike",                 "Strait of Hormuz","Sustained aerial campaign begins vs Iranian vessels/drones; CENTCOM claims 8,000+ targets, 130 vessels struck to date", None, "Bandar Lengeh: 16 boats burned", "High", "Wikipedia: 2026 Iran war"),
(16, d(2026,3,21), "US",        "Strike",                 "Iran",            "Second bunker-buster strike on Natanz", None, "n/a", "High", "Wikipedia: 2026 Iran war"),
(17, d(2026,3,21), "Iran",      "Retaliation strike",     "Israel",          "Strikes Dimona and Arad, claiming to target the Negev Nuclear Research Center", 16, "0 killed, 175 injured combined", "High", "Wikipedia: 2026 Iran war"),
(18, d(2026,3,21), "US",        "Ultimatum",              "Iran",            "Trump: 48-hour ultimatum to reopen Strait or face power-plant strikes", None, "n/a", "High", "Wikipedia: 2026 Iran war"),
(19, d(2026,3,25), "US",        "Diplomatic proposal",    "Iran",            "US delivers a 15-point ceasefire proposal", None, "Rejected by Iran", "High", "Wikipedia: 2026 Iran war ceasefire"),
(20, d(2026,3,26), "Israel",    "Assassination strike",   "Iran",            "Kills IRGC Navy commander Tangsiri (blockade architect) and intel chief Rezaei, Bandar Abbas", None, "2 senior officials killed", "High", "Wikipedia: 2026 Strait of Hormuz campaign"),
(21, d(2026,3,27), "Iran",      "Retaliation strike",     "Saudi Arabia",    "Strikes Prince Sultan Air Base", 20, "15-29 US soldiers injured; refueling aircraft + E-3 Sentry damaged", "High", "Wikipedia: 2026 Iran war"),
(22, d(2026,3,27), "Iran",      "Blockade escalation",    "Strait of Hormuz","Total closure 'to/from' US/Israel/allied ports declared", None, "20,000 mariners / 2,000 ships stranded", "High", "Wikipedia: 2026 Iran war"),
(23, d(2026,3,30), "US",        "Strike",                 "Iran",            "First B-52 overflights of Iran; bombers hit Isfahan ammo depot/airbase", None, "n/a", "Medium", "Wikipedia: 2026 Iran war"),
(24, d(2026,3,31), "Pakistan/China", "Diplomatic proposal","Iran/US",        "China-Pakistan '5-point initiative' ceasefire proposal", None, "n/a", "Medium", "Wikipedia: 2026 Iran war ceasefire"),
(25, d(2026,4,2),  "US",        "Strike",                 "Iran",            "Destroys B1 bridge (Tehran-Karaj) during a family holiday gathering below", None, "8 killed, 95 wounded; called possible war crime by experts", "High", "Wikipedia: 2026 Iran war"),
(26, d(2026,4,3),  "Iran",      "Air defense",            "US",              "Shoots down US F-15E and A-10 over Iran", None, "Both crews rescued", "High", "Wikipedia: 2026 US F-15E rescue operation"),
(27, d(2026,4,5),  "Pakistan",  "Diplomatic proposal",    "Iran/US",         "Pakistan proposes 45-day two-phase ceasefire framework; Iran rejects, counters with 10-point plan", None, "Rejected", "High", "Wikipedia: 2026 Iran war ceasefire"),
(28, d(2026,4,7),  "US/Iran",   "Ceasefire announcement", "-",               "Two-week ceasefire announced via VP Vance / Pakistan channel", None, "n/a", "High", "Wikipedia: 2026 Iran war ceasefire"),
(29, d(2026,4,8),  "US/Iran/Pakistan", "Ceasefire signed","-",               "Formal ceasefire: Strait reopening, two-phase talks, enrichment constraints, sanctions relief, frozen-asset release", None, "n/a", "High", "Wikipedia: 2026 Iran war ceasefire"),
(30, d(2026,4,8),  "Israel",    "Ceasefire violation",    "Lebanon",         "Operation Eternal Darkness: 100 airstrikes on Lebanon within hours of the ceasefire taking effect", 29, "n/a", "High", "Wikipedia: 2026 Iran war ceasefire"),
(31, d(2026,4,8),  "Iran",      "Blockade re-escalation", "Strait of Hormuz","Iran restricts/resumes blockade, citing the Lebanon strikes as a ceasefire violation", 30, "n/a", "High", "Wikipedia: 2026 Iran war ceasefire"),
(32, d(2026,4,8),  "UAE",       "Strike (covert)",        "Iran",            "UAE strikes Lavan Island oil refinery (only revealed later via WSJ/Bloomberg, May 11)", None, "Output crippled for months", "Medium", "Wikipedia: 2026 Lavan Island attack"),
(33, d(2026,4,11), "US",        "Blockade-adjacent action","Strait of Hormuz","US Navy destroyers transit the Strait for the first time since the war began (mine-clearance framing)", None, "Iran calls it a ceasefire violation", "High", "Wikipedia: 2026 Strait of Hormuz campaign"),
(34, d(2026,4,11), "US/Iran/Pakistan", "Diplomatic talks","-",               "Islamabad Talks: 21 hours of negotiation, collapse without agreement", None, "Failed - Araghchi: 'inches away' but accused US of moving goalposts", "High", "Wikipedia: Islamabad Talks"),
(35, d(2026,4,13), "US",        "Blockade start",         "Iran",            "US naval blockade of Iran begins", 34, "n/a", "High", "Wikipedia: 2026 United States naval blockade of Iran"),
(36, d(2026,4,18), "Iran",      "Blockade re-escalation", "Strait of Hormuz","Iran announces the Strait closed again, citing continuation of the US blockade", 35, "n/a", "High", "Wikipedia: 2026 Strait of Hormuz crisis"),
(37, d(2026,4,19), "US",        "Seizure",                "Iranian shipping","Seizes/disables tankers Touska, MT Tifani, Majestic X over several days", None, "3 vessels", "High", "Wikipedia: 2026 United States naval blockade of Iran"),
(38, d(2026,4,22), "Iran",      "Seizure (retaliation)",  "Shipping",        "IRGC seizes container ships MSC Epaminondas and MSC Francesca", 37, "Tit-for-tat for US tanker seizures", "High", "Wikipedia: 2026 Strait of Hormuz crisis"),
(39, d(2026,5,1),  "Iran",      "Incursion",              "Kuwait",          "Bubiyan Island raid attempt: 6 IRGC troops by fishing boat, 4 detained, 2 escape", None, "1 Kuwaiti security official injured", "Medium", "Wikipedia: 2026 Bubiyan Island raid"),
(40, d(2026,5,3),  "US",        "Operation",              "Strait of Hormuz","Operation Project Freedom: Navy escort mission for stranded ships; sinks 7 small boats; paused May 6", None, "n/a", "High", "Wikipedia: Operation Project Freedom"),
(41, d(2026,5,7),  "Iran",      "Strike",                 "US Navy",         "Missiles, drones and small boats attack 3 US destroyers transiting the Strait", None, "No US casualties reported", "High", "Wikipedia: 7 May 2026 United States strikes on Iran"),
(42, d(2026,5,7),  "US",        "Retaliation strike",     "Iran",            "Strikes IRGC facilities and missile sites near Bandar Abbas/Qeshm Island", 41, "n/a", "High", "Wikipedia: 7 May 2026 United States strikes on Iran"),
(43, d(2026,6,8),  "US/Iran",   "Ceasefire (renewed)",    "-",               "A ceasefire takes effect; Israel and Iran had not exchanged fire since", None, "n/a", "Medium", "Al Jazeera, Jun 9"),
(44, d(2026,6,9),  "Israel",    "Strike (ceasefire violation)", "Iran",      "Strikes kill members of Iran's air-defense units", 43, "2+ killed", "High", "Al Jazeera / NPR"),
(45, d(2026,6,9),  "Iran",      "Retaliation",            "US",              "Downs a US Apache helicopter over the Strait (US says a Shahed drone did it)", 44, "Both crew rescued", "Medium", "NPR / Al Jazeera / CBS"),
(46, d(2026,6,9),  "US",        "Retaliation strike",     "Iran",            "Self-defense strikes on Qeshm Island, Sirik, Jask, Bandar Abbas radar/missile-defense sites", 45, "No casualties reported", "High", "NPR"),
(47, d(2026,6,10), "Iran",      "Retaliation strike",     "Jordan/Kuwait/Bahrain", "Strikes Muwaffaq Salti AB plus bases in Kuwait and Bahrain", 46, "IRGC claims 4 targets destroyed; Jordan says all 5 missiles intercepted (disputed)", "High", "Wikipedia: 2026 Iranian strikes on Jordan"),
(48, d(2026,6,11), "Iran",      "Retaliation strike",     "Jordan",          "12 ballistic missiles at a Jordan base near Azraq", 47, "Jordan: 20 intercepted, no damage", "High", "Wikipedia: 2026 Iranian strikes on Jordan"),
(49, d(2026,6,12), "US/Iran",   "Ceasefire terms",        "-",               "New 60-day ceasefire terms agreed", None, "n/a", "High", "Wikipedia: 2026 Iran war ceasefire"),
(50, d(2026,6,17), "US/Iran",   "Ceasefire (MOU signed)", "-",               "Islamabad Memorandum: Trump and Pezeshkian sign a 14-point MOU - ends blockade, reopens Strait, sanctions relief", None, "n/a", "High", "Wikipedia: 2026 Iran war ceasefire / Islamabad Talks"),
(51, d(2026,6,18), "US",        "Blockade end",           "Iran",            "US naval blockade of Iran officially ends", 50, "n/a", "High", "Wikipedia: 2026 United States naval blockade of Iran"),
(52, d(2026,6,19), "Israel",    "Ceasefire violation",    "Lebanon",         "Israeli strikes continue in southern Lebanon despite renewed ceasefire announcement", None, "n/a", "Medium", "Wikipedia: 2026 Strait of Hormuz crisis"),
(53, d(2026,6,20), "Iran",      "Blockade re-escalation", "Strait of Hormuz","Iran claims the Strait closed again, citing Israeli ceasefire violations in Lebanon", 52, "n/a", "High", "Wikipedia: 2026 Strait of Hormuz crisis"),
(54, d(2026,6,25), "Iran",      "MOU violation",          "Shipping",        "Drone attack on a cargo container ship in the Strait - first MOU violation, ~1 week after signing", None, "No injuries", "High", "NPR"),
(55, d(2026,6,26), "US",        "Retaliation strike",     "Iran",            "~1 hour of retaliatory strikes on missile/drone sites and coastal radar", 54, "n/a", "High", "NPR"),
(56, d(2026,6,27), "Iran",      "Retaliation strike",     "Bahrain/Kuwait",  "Strikes a tanker and attacks Bahrain/Kuwait (intercepted)", 55, "Intercepted; both sides then pause the exchange", "High", "Al Jazeera"),
(57, d(2026,7,7),  "Iran",      "MOU violation (major)",  "Shipping",        "Strikes three vessels in the Strait - second, larger MOU violation", None, "Strait traffic drops from 49 to 25 vessels/day", "High", "ABC News"),
(58, d(2026,7,7),  "US",        "Sanctions response",     "Iran",            "Revokes Iran's oil-export license (non-kinetic first response)", 57, "n/a", "High", "ABC News"),
(59, d(2026,7,7),  "US",        "Ceasefire declared over","-",               "Trump declares the ceasefire 'over' at the NATO summit", 57, "n/a", "High", "ABC News"),
(60, d(2026,7,8),  "US",        "Strike (major escalation)","Iran",          "90 targets across southern/northeastern Iran incl. two bridges - second consecutive night, marked jump in intensity", 59, "n/a", "High", "ABC News"),
(61, d(2026,7,9),  "Iran",      "Retaliation strike",     "Jordan",          "10 ballistic missiles at Muwaffaq Salti AB", 60, "8 intercepted, no damage", "High", "Wikipedia: 2026 Iranian strikes on Jordan"),
(62, d(2026,7,12), "Iran",      "Retaliation strike (5 countries)", "Oman/Qatar/Kuwait/Bahrain/Jordan", "Simultaneous strikes framed as retaliation for a '3rd round of US strikes within a week' (~140 sites)", 60, "Qatar: 3 wounded incl. a child", "High", "Al Jazeera"),
(63, d(2026,7,12), "Iran",      "Blockade re-escalation", "Strait of Hormuz","Declares the Strait 'closed until the end of US interference'", 62, "n/a", "High", "Al Jazeera"),
(64, d(2026,7,14), "Iran",      "Retaliation strike",     "Bahrain",         "Strikes Juffair Base; claims a Patriot radar destroyed", None, "n/a", "Medium", "Wikipedia: 2026 Iranian strikes on Arab countries"),
(65, d(2026,7,17), "Iran",      "Retaliation strike",     "Jordan",          "Attack on Muwaffaq Salti AB - deadliest Jordan-strike day of the war", None, "2 US KIA, 1 missing, 4 medevac'd", "High", "Wikipedia: 2026 Iranian strikes on Jordan / NPR"),
(66, d(2026,7,19), "Iran",      "Retaliation strike",     "Jordan",          "King Hussein International Airport near Aqaba, 'severe damage' claimed to US planes", None, "Disputed damage assessment", "Medium", "Wikipedia: 2026 Iranian strikes on Jordan"),
(67, d(2026,7,20), "Iran",      "Retaliation strike",     "Jordan",          "Destroys a missile-defense radar and an F-15 at a Jordan base", None, "n/a", "Medium", "Wikipedia: 2026 Iranian strikes on Jordan"),
(68, d(2026,8,19), "Analyst",   "Strategic assessment",   "-",               "Trita Parsi assessment: Iran now believes it holds the military advantage, considers shifting from reaction to offense", None, "Analysis, not an event", "Medium", "Wikipedia: Analysis of the 2026 Iran war"),
(69, d(2026,8,25), "US",        "Mine-clearance",         "Strait of Hormuz","Navy clears mines from the Traffic Separation Scheme; 100+ suspected mines found/removed", None, "n/a", "High", "Wikipedia: 2026 Strait of Hormuz crisis"),
(70, d(2026,8,30), "US",        "Strike",                 "Iran",            "Strikes 2 IRGC rocket launchers on Larak Island, said to be preparing sea mines", None, "Iran reports unspecified casualties", "High", "Wikipedia: 2026 Larak Island attack"),
(71, d(2026,8,31), "Iran",      "Retaliation strike",     "Jordan",          "'Punishment of the Aggressor': strikes King Hussein AB and Al Azraq AB", 70, "8 intercepted per Jordan, no injuries (disputed)", "High", "Wikipedia: 2026 Larak Island attack / ...Jordan"),
(72, d(2026,8,31), "Iran/Accident","Mine incident",        "Strait of Hormuz","Tanker Sidr hits mines and catches fire, undercutting the Aug 25 mine-clearance claim", None, "1 tanker damaged", "Medium", "Wikipedia: 2026 Strait of Hormuz crisis"),
(73, d(2026,9,1),  "US",        "Strike",                 "Iran",            "New strike wave: Kenerak, Bandar Abbas, Qeshm Island", 71, "n/a - trigger: ongoing mine-laying/shipping attacks", "High", "Wikipedia: September 2026 United States strikes on Iran"),
(74, d(2026,9,1),  "US",        "Strike (controversial)", "Iran",            "Kuhestak/Sirik wedding strike, part of the same wave as #73", 73, "4-5 killed incl. 2 children, 50+ wounded", "High", "Wikipedia: 2026 Sirik wedding airstrike"),
(75, d(2026,9,1),  "Iran",      "Retaliation strike",     "Jordan",          "Strikes Camp Titin and Prince Hassan AB", 74, "'Several aircraft' destroyed, claimed", "High", "Wikipedia: 2026 Iranian strikes on Jordan"),
(76, d(2026,9,2),  "Iran",      "Retaliation strike (major)", "Jordan",      "Larger wave - described as 'most extensive response since the ceasefire began'", 75, "n/a", "High", "Wikipedia: 2026 Iranian strikes on Jordan"),
(77, d(2026,9,5),  "US",        "Strike",                 "Iranian shipping","Strikes 3 Iranian crude tankers (MT Kylo and others)", None, "3 tankers disabled - trigger: IRGC missiles at US warships", "High", "USNI News"),
(78, d(2026,9,8),  "Iran",      "Strike",                 "US Navy",         "IRGC fires ballistic missiles at a US warship for the second time in two days", None, "Evaded, no casualties", "High", "Defense News"),
(79, d(2026,9,9),  "US",        "Retaliation strike",     "Iranian shipping","Destroys 5 Iranian crude oil tankers under a new 'tanker for tanker' policy", 78, "5 tankers destroyed", "High", "Axios / Defense News"),
(80, d(2026,9,9),  "Iran",      "Retaliation strike",     "Jordan",          "Strikes Muwaffaq Salti AB: 1 A-10 loses a wing, ~8 F-15s lightly damaged", 79, "1 A-10 + 8 F-15 damaged; ~30 Patriot interceptors expended", "High", "Defense News"),
(81, d(2026,9,23), "Iran",      "Diplomatic proposal",    "US",              "FM Araghchi's 7-day roadmap at UNGA: ceasefire, blockade lift, Strait reopens on day 7", None, "Pending at time of writing", "High", "Al Jazeera"),
(82, d(2026,9,26), "US",        "Diplomatic rejection",   "Iran",            "Trump rejects the proposal; officials say he expects to resume bombing after the November midterms", 81, "n/a", "High", "CBS News / WSJ"),
(83, d(2026,9,27), "Iran (suspected)/UK", "Terror plot (foiled)", "United Kingdom", "5 suspects arrested near RAF Fairford (a base used to stage Iran-war bombing runs), allegedly planning to do 'big damage'; Rubio says a 'foreign actor' was involved, Trump says an Iranian-linked motive is suspected", None, "No casualties - plot reportedly disrupted before execution; suspects later released on bail, which Trump publicly criticized the UK over", "Low", "Times of Israel / CNN / Al Jazeera, Sept 27-29"),
(84, d(2026,9,28), "Iran (unclear/disputed)", "Strike (shipping)", "Strait of Hormuz","At least 3 commercial vessels struck by projectiles in the Hormuz region; IRGC says 'military conflict' continues there daily", None, "No casualties reported", "Low", "Al Jazeera liveblog, Sept 30"),
(85, d(2026,9,28), "US",        "Sanctions response",     "Iran",            "Treasury imposes new sanctions on 10 individuals/entities for supporting Iran's military supply chain", None, "n/a", "High", "CBS News liveblog"),
(86, d(2026,9,29), "US",        "Diplomatic proposal (counter-offer)", "Iran","US sends a formal counter-proposal via Qatari mediators responding to Iran's 7-day roadmap; US insists nuclear talks be included", 82, "Pending Iranian review as of Sept 30", "High", "Al Jazeera liveblog / CBS News liveblog"),
(87, d(2026,10,1), "US",        "Sanctions response",     "Iran",            "Treasury imposes sweeping new sanctions on Iran's automotive and rail industries and a shadow banking network tied to Russia - called 'some of the last significant elements' of Iran's IRGC-linked industrial base", None, "n/a", "High", "CBS News live updates, Oct 1 (matcher live test)"),
(88, d(2026,10,1), "US",        "Diplomatic statement",   "Iran",            "Trump tells TIME Iran is 'ready to fold up'; says military action could resume after the Nov midterms if talks fail; says he doesn't believe lasting peace with Iran is possible", None, "n/a - rhetoric, not a formal proposal/action", "Medium", "CBS News / TIME interview, Oct 1 (matcher live test)"),
(89, d(2026,10,1), "US",        "Force posture",          "Middle East region","3 ships carrying 7,000+ sailors and 2,000 Marines deploy to the region; projected to push US presence above 20,000 personnel plus hundreds of aircraft by month's end", None, "n/a - posture change, not a strike", "High", "CBS News live updates, Oct 1 (matcher live test)"),
]

# ---------------------------------------------------------------------------
# ACTION-REACTION PAIRS (subset with a clearly identified trigger -> response,
# where response time is short enough to be meaningful, i.e. hours to ~5 days)
# Columns: Pair ID, Trigger ID, Response ID, Trigger Category, Response Caused Casualties, Notes
#
# Trigger Category codes what kind of cost the TRIGGER imposed on the side
# that then responded - this is the factor being weighed:
#   Personnel/Casualty   - the trigger killed or injured people
#   Military/Property    - kinetic strike, but only equipment/infrastructure hit
#   Economic/Blockade    - shipping, seizures, sanctions, oil-revenue moves
#   Political/Diplomatic - ceasefire declarations, failed talks, proposals
# ---------------------------------------------------------------------------
pairs = [
(1,  2,  5,  "Personnel/Casualty", "Y", "Iran's opening retaliation wave, same day as the initial US/Israeli strikes that killed Khamenei and, per Iranian officials, 168-175 at a school"),
(2,  10, 11, "Military/Property",  "N", "Retaliation against a symbolic/soft target (embassy annex) rather than in kind"),
(3,  16, 17, "Military/Property",  "Y", "Iran hits Israeli nuclear-adjacent sites in response to a US strike on Natanz"),
(4,  20, 21, "Personnel/Casualty", "Y", "Retaliation for Israel's strike that it says killed the IRGC Navy commander and its intelligence chief (Iran confirmed only the commander, Mar 30)"),
(5,  30, 31, "Political/Diplomatic","N", "Iran treats an Israeli action as breaking a US-brokered ceasefire"),
(6,  34, 35, "Political/Diplomatic","N", "Failed talks preceded the US blockade decision"),
(7,  35, 36, "Economic/Blockade",  "N", "Iran reopens hostilities citing the new US blockade"),
(8,  37, 38, "Economic/Blockade",  "N", "Direct tit-for-tat ship seizures"),
(9,  41, 42, "Military/Property",  "N", "US strikes back same day after its destroyers are attacked (no casualties)"),
(10, 44, 45, "Personnel/Casualty", "N", "Iran/US disagree on mechanism, but timing ties this to the preceding Israeli strike that killed air-defense personnel"),
(11, 45, 46, "Military/Property",  "N", "US retaliates for the downed Apache within hours (crew survived)"),
(12, 46, 47, "Military/Property",  "N", "Iran retaliates against Jordan for the US's Qeshm/Sirik counterstrikes"),
(13, 54, 55, "Economic/Blockade",  "N", "First MOU violation (drone hits a cargo ship, no injuries) draws a same-week US retaliatory strike"),
(14, 55, 56, "Military/Property",  "N", "Iran answers the US retaliation with fire at Bahrain/Kuwait (Axios says both sides then agreed to halt Jun 29; AP mentions no pause)"),
(15, 57, 58, "Economic/Blockade",  "N", "US chooses a non-kinetic (sanctions) response to a major MOU violation"),
(16, 59, 60, "Political/Diplomatic","N", "Ceasefire declared over, followed immediately by the most intense US strike wave since April"),
(17, 60, 61, "Military/Property",  "N", "Iran hits Jordan the day after the 90-target US strike wave"),
(18, 60, 62, "Military/Property",  "Y", "A second, five-country Iranian response to the same US escalation, days later"),
(19, 70, 71, "Personnel/Casualty", "N", "Larak Island strike (Iran reports unspecified casualties) draws 'Punishment of the Aggressor' response within a day"),
(20, 74, 75, "Personnel/Casualty", "N", "Sirik/Kuhestak strike (about 4-5 killed per Iranian figures, which vary) draws an Iranian missile salvo at Jordan within a day"),
(21, 75, 76, "Military/Property",  "N", "Iran follows up with a larger second wave the next day, after a strike that destroyed aircraft but killed no one"),
(22, 78, 79, "Military/Property",  "N", "US retaliates against Iranian tankers after IRGC targets a US warship twice (missiles evaded, no casualties)"),
(23, 79, 80, "Economic/Blockade",  "N", "Iran hits back at Jordan within roughly a day of the US destroying 5 Iranian crude carriers (crews were told to abandon ship first)"),
(24, 81, 82, "Political/Diplomatic","N", "US rejects Iran's ceasefire roadmap days after it is proposed"),
(25, 82, 86, "Political/Diplomatic","N", "Despite the flat rejection, the US comes back with a formal counter-proposal 3 days later via Qatari mediators - talks continue rather than collapsing"),
]

MONTHS = [
    ("Feb 2026", d(2026,2,1), d(2026,2,28)),
    ("Mar 2026", d(2026,3,1), d(2026,3,31)),
    ("Apr 2026", d(2026,4,1), d(2026,4,30)),
    ("May 2026", d(2026,5,1), d(2026,5,31)),
    ("Jun 2026", d(2026,6,1), d(2026,6,30)),
    ("Jul 2026", d(2026,7,1), d(2026,7,31)),
    ("Aug 2026", d(2026,8,1), d(2026,8,31)),
    ("Sep 2026", d(2026,9,1), d(2026,9,30)),
    ("Oct 2026 (to Oct 26)", d(2026,10,1), d(2026,10,31)),
]


# ---------------------------------------------------------------------------
# TRIGGER CENSUS - fixes the selection bias in the pairs table.
#
# The pairs table only contains trigger->response links that were FOUND, so any
# rate computed from it is "how fast, given a reply happened". The census lists
# every countable hostile act (strikes, seizures, blockade moves, sanctions) and
# records whether the other side hit back within ~5 days, including the ones
# where nothing followed.
#
# Status codes:
#   R-strong   a reply is in the log with an explicit link (all 25 pairs, plus #71->#73)
#   R-weak     a distinct hostile act followed inside 5 days, but only timing links it
#   N          checked against outside sources: no reply found (pause, talks, or rhetoric only)
#   Unclear    sources conflict or are too thin to call
#   Unverified not checked yet - left out of the rates until it is
# Columns: Trigger ID, Category (cost imposed on the other side), Status, Evidence / note
# ---------------------------------------------------------------------------
census = [
(2,  "Personnel/Casualty", "R-strong",  "Opening wave; Iran's big retaliation came the same day (pair 1). The act that started the war counts; the rest of Feb 28-Mar 4 is excluded."),
(14, "Economic/Blockade",  "Unverified","Mine-laying, Mar 10. US reply within 5 days not checked yet."),
(15, "Military/Property",  "Unverified","Start of the sustained US campaign, Mar 19. Reply not checked yet."),
(16, "Military/Property",  "R-strong",  "Natanz strike -> Iran hits Dimona/Arad (pair 3)."),
(17, "Military/Property",  "Unverified","Iran hits Dimona/Arad, Mar 21. Israeli/US reply not checked yet."),
(20, "Personnel/Casualty", "R-strong",  "Assassination of IRGC Navy chief -> Iran hits Prince Sultan AB next day (pair 4)."),
(21, "Personnel/Casualty", "Unverified","Iran hits Prince Sultan AB, Mar 27 (15-29 US injured). US reply not checked yet."),
(22, "Economic/Blockade",  "Unverified","Total strait closure, Mar 27. US reply not checked yet."),
(23, "Military/Property",  "Unclear",   "B-52 strikes, Mar 30. Iran hit a Kuwaiti tanker Mar 31 and fired missiles Apr 1-2, but no source links them to this; they read as the ongoing campaign."),
(25, "Personnel/Casualty", "R-weak",    "Tehran-Karaj bridge strike, Apr 2 (8 killed). Iran threatened Gulf bridges and fired missiles at Israel that evening (The War Zone); no source frames it as a reply. An earlier Kuwait-refinery lead came from a weak source and was dropped."),
(31, "Economic/Blockade",  "Unverified","Iran resumes blockade, Apr 8. US reply not checked yet."),
(33, "Economic/Blockade",  "N",         "US destroyers transit the Strait, Apr 11-12. Iran only issued warnings; no kinetic action found Apr 11-16."),
(35, "Economic/Blockade",  "R-strong",  "US blockade begins -> Iran closes the Strait again (pair 7)."),
(36, "Economic/Blockade",  "Unverified","Iran closes the Strait again, Apr 18. US reply not checked yet."),
(37, "Economic/Blockade",  "R-strong",  "US tanker seizures -> Iran seizes two container ships (pair 8)."),
(38, "Economic/Blockade",  "Unverified","Iran seizes two container ships, Apr 22. US reply not checked yet."),
(39, "Military/Property",  "Unverified","Bubiyan Island raid, May 1. Reply not checked yet."),
(40, "Military/Property",  "Unverified","Operation Project Freedom, May 3. Reply not checked yet (Iran attacked destroyers May 7, no source links it)."),
(41, "Military/Property",  "R-strong",  "Iran attacks 3 US destroyers -> US strikes back same day (pair 9)."),
(42, "Military/Property",  "Unclear",   "US strikes near Bandar Abbas, May 7. UAE intercepted Iranian missiles May 8, but Iran did not claim it and no source links it."),
(44, "Personnel/Casualty", "R-strong",  "Israeli strike kills air-defense crews -> Iran downs a US Apache (pair 10)."),
(45, "Military/Property",  "R-strong",  "Apache downed -> US self-defense strikes within hours (pair 11)."),
(46, "Military/Property",  "R-strong",  "US self-defense strikes -> Iran hits Jordan/Kuwait/Bahrain (pair 12)."),
(47, "Military/Property",  "R-weak",    "Iranian strikes, Jun 10. CENTCOM 'self-defense' strikes on Bandar Abbas/Minab/Sirik followed Jun 11; timing link only."),
(48, "Military/Property",  "Unclear",   "12 missiles at Jordan, Jun 11 (intercepted). The Jun 11 US strikes may have come before it, so the order is unclear."),
(53, "Economic/Blockade",  "Unverified","Iran closes the Strait again, Jun 20. US reply not checked yet."),
(54, "Economic/Blockade",  "R-strong",  "First MOU violation -> US retaliatory strikes next day (pair 13)."),
(55, "Military/Property",  "R-strong",  "US retaliatory strikes -> Iran hits Bahrain/Kuwait (pair 14)."),
(56, "Military/Property",  "N",         "Iran hits a tanker and Bahrain/Kuwait, Jun 27-28. Both sides stood down and talks continued; no attacks found Jun 29-Jul 6."),
(57, "Economic/Blockade",  "R-strong",  "Major MOU violation -> US revokes oil license, then ends ceasefire (pair 15)."),
(58, "Economic/Blockade",  "N",         "US revokes Iran's oil-export license, Jul 7. Iran called it a 'material breach' but took no distinct action tied to it."),
(60, "Military/Property",  "R-strong",  "90-target US strike wave -> Iran hits Jordan next day and five countries days later (pairs 17-18). The act that started the nightly campaign counts; the rest of Jul 7-25 is excluded."),
(70, "Personnel/Casualty", "R-strong",  "Larak Island strike -> 'Punishment of the Aggressor' next day (pair 19)."),
(71, "Military/Property",  "R-strong",  "Iran strikes King Hussein/Azraq, Aug 31 -> US strike wave Sep 1 (event 73 names this as its trigger)."),
(74, "Personnel/Casualty", "R-strong",  "Sirik wedding strike (4-5 killed) -> same-day Iranian strike on Jordan (pair 20)."),
(75, "Military/Property",  "R-strong",  "Camp Titin strike -> larger Iranian wave next day (pair 21)."),
(76, "Military/Property",  "R-weak",    "Major Iranian wave, Sep 2. CENTCOM struck IRGC sites Sep 4 and tankers Sep 5; timing link only."),
(77, "Economic/Blockade",  "R-weak",    "US strikes 3 tankers, Sep 5. Iran fired ballistic missiles at a US warship Sep 6-7 (CENTCOM); not framed as a reply."),
(78, "Military/Property",  "R-strong",  "Iran fires at US warship -> US destroys 5 tankers (pair 22)."),
(79, "Economic/Blockade",  "R-strong",  "US destroys 5 tankers -> Iran hits Jordan base (pair 23)."),
(80, "Military/Property",  "N",         "Iran hits Muwaffaq Salti AB, Sep 9 (aircraft damaged, ~30 interceptors used). No US strikes on Iran found Sep 10-Oct 6; Trump said bombing may resume after the midterms."),
(85, "Economic/Blockade",  "N",         "US sanctions, Sep 29 (date corrected from Sep 28). About 12 tankers were hit Sep 29-Oct 5, but no source ties them to the sanctions. Window overlaps #87."),
(87, "Economic/Blockade",  "N",         "US sanctions on auto/rail/shadow banking, Oct 1. Only rhetoric found through Oct 6. Window overlaps #85."),
]

# Events deliberately NOT counted in the census, and why (shown on the sheet).
census_exclusions = [
    "Opening phase, Feb 28 - Mar 4 (events 3-13): nonstop two-way fighting, so every act has a 'reply' by default, which would inflate the rate. Event 2, the act that started the war, is counted.",
    "Nightly US campaign, Jul 7-25 (events 61-67): same reason. Events 57 and 60, which started it, are counted. Event 65 (US troops killed Jul 17) was followed by a US strike on Jul 18 that officials said was to 'punish' the IRGC, but it is excluded here for consistency.",
    "Diplomatic and ceasefire moves (events 18, 19, 24, 27-30, 34, 43, 49-52, 59, 81, 82, 86, 88): their 'reply' is a formal answer, which this log does not track reliably. Not covered yet.",
    "Covert, defensive, accidental or not hostile (events 1, 26, 32, 68, 69, 72, 83, 89): covert acts the other side could not respond to, a defensive shootdown, an accident, an analyst note, a mine-clearing mission, a foiled plot, and a troop deployment.",
    "Disputed attribution (event 84, low confidence) and same-wave duplicates (event 73, same wave as event 74).",
]


# ===========================================================================
# SOURCE AUDIT LAYER
# The first draft of the Event Log cited Wikipedia for 62 of 89 events. Wikipedia
# is editable by anyone and is NOT accepted as a source here. Every one of those
# events was sent back to credible outlets (AP, Reuters, NPR, CBS, ABC, NBC, CNN,
# Al Jazeera, Axios, USNI News, The War Zone, Stars and Stripes, official statements).
# The raw rows above are left untouched for traceability; this layer applies what
# the credible sources actually say. Details: audit_sources.py (URLs per event).
#
# Source check values:
#   Verified            central claim confirmed by credible outlet(s)
#   Corrected           confirmed, but credible outlets differ from the first draft (see audit note)
#   Partly verified     the event is confirmed, some details are not
#   Not supported       searched; credible outlets do not support the row as logged
#   Pending             no credible source confirmed yet (not searched, or searched without success)
#   Date conflict       cites a credible outlet, but sources conflict on the date
#   Not re-checked      already cited a credible outlet; not independently re-checked
# ===========================================================================

# ---------------------------------------------------------------------------
# Catch-up, Oct 2-11 (credible-outlet research, Oct 11). No US/Israeli strike on Iran and no
# Iranian strike on a US base was found in this window. Houthi rows are context (separate front).
# ---------------------------------------------------------------------------
events.extend([
(90, d(2026,10,2), 'Iran (suspected)', 'Strike (shipping)', 'Strait of Hormuz', "Cluster of projectile and drone attacks on tankers in and near Hormuz, Oct 2-5; Reuters' maritime security sources counted at least 12 tanker attacks in Sep 28-Oct 5, the most of any week of the war", None, 'No deaths reported; damage not itemised (Reuters, USNI)', 'Medium', 'see audit'),
(91, d(2026,10,4), 'US', 'Force posture (withdrawal)', 'RAF Fairford, UK', 'Pentagon confirms all US bombers at RAF Fairford have returned to home bases; US officials told Reuters it was over a suspected Iranian drone-attack plot', 83, 'n/a', 'Medium', 'see audit'),
(92, d(2026,10,4), 'US', 'Force posture (withdrawal)', 'Middle East region', 'Carrier George H.W. Bush leaves CENTCOM for the Pacific (port call in Phuket Oct 4), leaving the George Washington as the only US carrier in the Middle East', None, 'n/a', 'Medium', 'see audit'),
(93, d(2026,10,5), 'Iran', 'Diplomatic rejection', 'US', "President Pezeshkian calls negotiations with Washington 'futile', saying the US attacked Iran three times after talks", 86, 'n/a', 'Medium', 'see audit'),
(94, d(2026,10,6), 'Unknown (Iran suspected)', 'Strike (shipping)', 'Strait of Hormuz', 'Panama-flagged tanker On Peace hit by a projectile while crossing the strait; India condemns the attack (possibly Oct 5)', None, "12 crew injured, 11 of them Indian (India's foreign ministry, via AFP and Al Jazeera)", 'Medium', 'see audit'),
(95, d(2026,10,6), 'US', 'Diplomatic demand', 'Iran', "VP Vance tells Reuters Iran must make a 'meaningful' cut to uranium enrichment to end the war - read by analysts as possibly softer than the earlier zero-enrichment demand", None, 'n/a', 'Medium', 'see audit'),
(96, d(2026,10,7), 'Unknown', 'Strike (shipping)', 'Qatar (inside the Gulf)', 'UKMTO reports a tanker struck off northern Qatar, well west of the strait', None, 'Not stated by allowed sources', 'Medium', 'see audit'),
(97, d(2026,10,8), 'US', 'Ceasefire statement', 'Iran', "Trump says on Truth Social the US 'will not be attacking Iran at any time prior to the Midterm Elections' (Nov 3), citing 'productive discussions'", None, 'n/a', 'Medium', 'see audit'),
(98, d(2026,10,8), 'Houthis (Iran-backed)', 'Strike (proxy front)', 'Saudi Arabia', "Houthis fire a ballistic missile at Riyadh's King Khalid airport, citing Saudi strikes on Sanaa and Hodeidah; part of the separate Saudi-Houthi front", None, '3 killed, several wounded (Saudi aviation authority, via Al Jazeera)', 'Medium', 'see audit'),
(99, d(2026,10,9), 'Iran', 'Diplomatic response pending', 'US', "FM Araghchi says Iran is reviewing the US counter-proposal and will answer 'within the next few days'; talks continue through mediators", 86, 'n/a', 'Medium', 'see audit'),
(100, d(2026,10,9), 'Unknown (no claim)', 'Strike (shipping)', 'UAE', 'Unidentified projectile hits the laden supertanker GEM NO.2 at anchor off the UAE, outside the Hormuz area; fire put out (UKMTO)', None, 'Fire; crew status and damage unknown (Reuters)', 'Medium', 'see audit'),
(101, d(2026,10,9), 'Iran (IRGC claim)', 'Strike (shipping) + threat', 'Strait of Hormuz', "IRGC Navy CLAIMS it hit the LPG carrier NV Sunshine on an 'illegal route' and warns ships using unauthorised passages", None, 'Engine-room fire (IRGC claim via Tasnim; unverified)', 'Medium', 'see audit'),
(102, d(2026,10,10), 'Houthis (Iran-backed)', 'Strike (proxy front)', 'Saudi Arabia', "Second, deadlier missile attack shuts Riyadh airport; Trump calls it 'terrible' and says he is weighing a response", 98, 'At least 12 killed incl. one American, 309 wounded (Saudi aviation authority via Al Jazeera; CNN: at least 12 killed)', 'Medium', 'see audit'),
(103, d(2026,10,10), 'Iran (IRGC claim)', 'Strike (shipping, claimed mine)', 'Strait of Hormuz', 'IRGC Navy CLAIMS an unnamed supertanker on an unauthorised route hit a naval mine and caught fire, and threatens other tankers', None, 'Fire (IRGC claim; unverified)', 'Medium', 'see audit'),
(104, d(2026,10,11), 'US', 'Blockade enforcement strike', 'Iranian shipping', 'CENTCOM releases footage of a fighter jet bombing the stern of a cargo ship it says was running the blockade of Iranian ports, disabling it (strike Oct 10 or 11)', None, 'Propulsion disabled; no casualty figure (CENTCOM, via Al Jazeera)', 'Medium', 'see audit'),
(105, d(2026,10,11), 'Unknown', 'Strike (shipping)', 'Strait of Hormuz', 'UKMTO: an unidentified projectile hits an outbound tanker in the strait; separately the UAE coastguard rescues 22 crew from a tanker fire of unknown cause', None, '22 crew rescued; no casualties reported (Al Jazeera citing UKMTO, UAE coastguard)', 'Medium', 'see audit'),
])

# ---------------------------------------------------------------------------
# Weekly update, Oct 19 (weekly agent; credible-outlet research covering Oct 12-18, plus two
# catch-up rows from Oct 6 and Oct 8 that were announced or found late). No US strike on Iranian
# territory and no Iranian strike on US forces or bases was found. Attacks on shipping hit a record:
# UKMTO counted 10-12 confirmed attacks in the week to Oct 16 (one row per incident cluster here,
# so the log under-counts single attacks). Houthi-Saudi front events this week are not logged
# (no Americans hurt; context only).
# ---------------------------------------------------------------------------
events.extend([
(106, d(2026,10,6), 'US', 'Strike (IRGC-linked boat)', 'IRGC-linked shipping (Gulf of Oman)', "US forces destroy an Iranian-affiliated dhow that CENTCOM says was 'conducting surveillance and targeting U.S. Navy ships' in the Gulf of Oman; crew removed first (announced Oct 14)", None, 'No casualties: crew removed before the boat was destroyed (CENTCOM, via Reuters/Times of Israel)', 'Medium', 'see audit'),
(107, d(2026,10,8), 'US', 'Sanctions response', 'Iran', "Treasury sanctions 17 companies and 17 'shadow fleet' tankers carrying Iranian oil (Operation Economic Outcast)", None, 'n/a', 'Medium', 'see audit'),
(108, d(2026,10,11), 'Iran', 'Diplomatic rejection', 'US', "Security chief Mohsen Rezaei says the US answer to Iran's seven conditions for reopening Hormuz is 'insufficient' and asks Washington to clarify points", 86, 'n/a', 'Medium', 'see audit'),
(109, d(2026,10,13), 'Iran (per CENTCOM)', 'Strike (shipping)', 'Strait of Hormuz', "Singapore-flagged container ship GFS Pride hit by a projectile in the strait and sinks; a tanker is hit the same day (UKMTO). Iran said a mine sank it; CENTCOM said an IRGC projectile", None, 'GFS Pride sank; all 21 crew evacuated (Singapore MPA via Reuters). No casualties reported on the tanker', 'Medium', 'see audit'),
(110, d(2026,10,15), 'US', 'Sanctions response', 'Iran', "Treasury sanctions 10 entities and 16 people in Iran's shadow-banking and exchange-house network, plus Iranian religious-charity networks; State sanctions a Cuban bank serving an Iranian bank", None, 'n/a', 'Medium', 'see audit'),
(111, d(2026,10,16), 'US', 'Diplomatic statement (reported war plans)', 'Iran', "CBS: White House and Pentagon have prepared plans for a strike on Iran that could use the 'mother of all bombs'; White House says Trump 'keeps all options on the table'. Trump (Newsmax, Oct 15) rules out nuclear use and ground troops, expects a deal after the Nov 3 midterms", 97, 'n/a', 'Medium', 'see audit'),
(112, d(2026,10,16), 'Unknown', 'Strike (shipping)', 'Saudi Arabia (inside the Gulf)', "Two tankers hit off Saudi Arabia, Oct 16-17: one by an unknown projectile, one by a rocket-propelled grenade from a small boat about 78 nautical miles northeast of Jubail", None, 'Hull damage; crew of the RPG-hit tanker reported safe (CBS, Al Jazeera)', 'Medium', 'see audit'),
(113, d(2026,10,17), 'Iran (IRGC claim)', 'Strike (shipping, claimed mine)', 'Strait of Hormuz', "IRGC CLAIMS two supertankers, each carrying about 2 million barrels, hit naval mines on an 'unauthorised' route and caught fire (Oct 17-18); CENTCOM says the strait is cleared of mines and ships are being hit by projectiles", None, 'Fires (IRGC claim via IRNA/Press TV; unverified). No names or casualties given', 'Medium', 'see audit'),
(114, d(2026,10,18), 'Unknown', 'Strike (shipping)', 'UAE', 'UKMTO: a tug is struck by two unknown projectiles off the UAE; damaged but continuing its route', None, 'Damage; no casualties reported (CBS citing UKMTO)', 'Medium', 'see audit'),
(115, d(2026,10,18), 'Iran', 'Diplomatic response pending', 'US', "FM Araghchi says Tehran is reviewing US 'comments' on its proposal; if the US complies, 'the Strait of Hormuz will reopen on the sixth day' and negotiations start on the seventh", 86, 'n/a', 'Medium', 'see audit'),
# Catch-up row (2026-10-22): found while building the Hold weeks; sourced in audit_sources.py.
(116, d(2026,6,7), 'Iran', 'Strike (exchange with Israel)', 'Israel', 'Iran and Israel trade fire over the weekend of Jun 6-7, the first exchange since the April ceasefire; Iran then agrees to halt attacks (see #43)', None, 'No casualty figures in the source read', 'Medium', 'see audit'),
])

# ---------------------------------------------------------------------------
# Weekly update, Oct 26 (weekly agent; credible-outlet research covering Oct 19-26). No US strike
# on Iranian territory or on ships at sea and no Iranian strike on US forces or bases was found.
# UKMTO-confirmed shipping attacks this week were fewer than the IRGC claims (two confirmed,
# Oct 20-21, against nine claimed Oct 22-23). One row per incident or claim cluster.
# ---------------------------------------------------------------------------
events.extend([
(117, d(2026,10,20), 'Unknown', 'Strike (shipping)', 'Iraq (northern Gulf)', 'UKMTO: an unknown projectile hits a tanker about 30 nautical miles southeast of Iraq\'s Faw port (Tuesday Oct 20, reported Oct 21)', None, 'No damage; crew reported safe (Reuters citing UKMTO)', 'Medium', 'see audit'),
(118, d(2026,10,21), 'Unknown', 'Strike (shipping)', 'Strait of Hormuz', 'UKMTO: a tanker 11 nautical miles off Bukha, Oman, at the Strait of Hormuz, is hit by an unknown projectile and catches fire; now at anchor', None, 'Fire; all crew reported safe (AFP citing UKMTO)', 'Medium', 'see audit'),
(119, d(2026,10,21), 'US', 'Sanctions response', 'Iran', "Treasury sanctions 4 entities, 5 people and 9 vessels in Iran's shadow-fleet oil network (Operation Economic Outcast)", None, 'n/a', 'Medium', 'see audit'),
(120, d(2026,10,21), 'US', 'Force posture (drawdown)', 'Middle East region', "State orders non-emergency staff and families out of Saudi Arabia (Oct 21), citing Houthi attacks, and on Oct 23 cuts staff at embassies in Jordan, Lebanon, Qatar and the UAE; US officials say the military is quietly reducing its footprint at Middle East posts, partly over direct threats from Iran", None, 'n/a', 'Medium', 'see audit'),
(121, d(2026,10,22), 'Iran (IRGC claim)', 'Strike (shipping, claimed)', 'Strait of Hormuz', "IRGC CLAIMS seven tankers were hit overnight into Oct 22 (four struck while transferring oil, three by mines) and warns the conflict 'will extend to' US bases if the US keeps helping tankers through; Trump says Iran is 'making up fake hits, mines'; CENTCOM says the mine claims are incorrect and Iran is using missiles and drones", None, 'Fires and damage (IRGC claim; unverified). No names or casualties given', 'Medium', 'see audit'),
(122, d(2026,10,23), 'US', 'Diplomatic statement (threat)', 'Iran', "Trump tells a Florida rally the US 'may do another little Epic Fury' and asks whether to 'finish it off' or let Iran 'wither' under the blockade and sanctions; Ambassador Tom Barrack says a strike 'this weekend' is 'Absolutely' possible", 97, 'n/a', 'Medium', 'see audit'),
(123, d(2026,10,23), 'Iran (IRGC claim)', 'Strike (shipping, claimed mine) + threat', 'Strait of Hormuz', "IRGC CLAIMS two supertankers hit mines; Iranian state TV says movement of 'non-compliant' ships through Hormuz has been halted and threatens 'much more forceful' action if US escorts resume", None, 'Not stated (IRGC claim; unverified)', 'Medium', 'see audit'),
(124, d(2026,10,24), 'US', 'Diplomatic statement (intelligence warning)', 'Iran', "Axios and the NYT report a memo from DNI Jay Clayton to Secretary Rubio saying Iran has 'substantially increased efforts to target US personnel' abroad, with plots at 'advanced stages'; Washington does not comment publicly", None, 'n/a', 'Medium', 'see audit'),
(125, d(2026,10,24), 'Iran', 'Diplomatic statement', 'US', "Armed forces chief Ali Abdollahi says US warships will not enter the Gulf 'under any circumstances'; Iran's ambassador to Pakistan says Tehran is still open to talks under the June Pakistan-brokered interim deal", None, 'n/a', 'Medium', 'see audit'),
(126, d(2026,10,25), 'US', 'Diplomatic statement', 'Iran', "Trump: 'do I make a deal with them, or do I finish them off?' and, asked about a strike, 'No. There will not be a strike today'", 97, 'n/a', 'Medium', 'see audit'),
(127, d(2026,10,25), 'Iran', 'Diplomatic contact (via intermediaries)', 'US', "Iran's foreign ministry says messages are still being passed to the US through intermediaries; FM Araghchi says that with or without war 'our policies remain the same'", 86, 'n/a', 'Medium', 'see audit'),
(128, d(2026,10,26), 'Saudi Arabia/Pakistan/Turkey', 'Diplomatic talks (regional)', 'Iran', "Saudi, Pakistani and Turkish officials meet in Tehran with Iran's security chief to discuss the fallout of the war and the fighting in Yemen; the US is not part of the meeting (a day after an eight-country foreign ministers' meeting in Istanbul on Oct 23 without the US or Iran)", None, 'n/a', 'Medium', 'see audit'),
])

# ---------------------------------------------------------------------------
# Pre-war record, May 2019 - Feb 27, 2026 (prewar.py). IDs 201+.
# ---------------------------------------------------------------------------
import prewar as _pre
events.extend(_pre.EVENTS)
pairs.extend(_pre.PAIRS)
census.extend(_pre.CENSUS)

# Census statuses that count, and the ones that mean "a reply came".
REPLY_STATUSES = ("R-strong", "R-weak", "R-proxy")
COUNTED_STATUSES = REPLY_STATUSES + ("N",)

import re as _re
from audit_sources import SOURCES as _SRC, VERDICT as _VERD

_EDITS = {
 2:  dict(detail="Operation Epic Fury opens: Pentagon says 1,000+ targets hit in the first 24 hours; Khamenei and ~40 senior officials killed; a strike near Minab hits a girls' school",
          severity="Khamenei + ~40 senior officials killed (AP). Minab school: Iranian authorities say at least 175 killed (AP); Minab mayor says 168 (NBC) - Iranian figures; no nation has claimed the strike (AP)",
          note="School toll is 168-175 (Iranian figures), not 148-168. '~900 strikes in 12 hrs' was a US-only figure from an unnamed official (via Fox), so it was dropped for the Pentagon's 1,000+ in 24 hrs."),
 3:  dict(detail="US strikes hit Iran's navy from the first hours: drone carrier Shahid Bagheri attacked (CENTCOM); Bayandor and Naghdi reported sunk at Konarak (The War Zone)",
          severity="Only Shahid Bagheri confirmed hit by CENTCOM; Bayandor/Naghdi sinking per The War Zone, undated; Trump and CENTCOM claimed larger totals",
          note="First draft said three ships sunk Feb 28. Credible outlets support 'struck', with only some sinkings reported."),
 4:  dict(atype="Blockade (de facto)", detail="IRGC radios ships on VHF that 'no ship is allowed to pass'; Iran does not formally confirm a closure order (Reuters, citing UKMTO and EU Aspides); IRGC-linked Tasnim says the Strait is shut",
          severity="Reuters/Kpler: only 105 crossings Mar 1-18 vs ~120/day normal (>95% drop)",
          note="No formal IRGC declaration found; the '~70% drop' figure was not found and was replaced with Reuters/Kpler data."),
 5:  dict(note="Reuters confirms Iran fired missiles at Israel. The Tel Aviv casualty figures and the Gulf/Jordan target list are not yet confirmed by a credible outlet."),
 7:  dict(detail="Strike on a makeshift operations center at the port of Shuaiba, Kuwait", severity="6 US killed - the first US combat deaths of the war (CENTCOM, AP, CNN)",
          note="'Camp Arifjan' is not supported by the retrieved reporting and was dropped."),
 8:  dict(date=d(2026,2,28), detail="CENTCOM says the Iranian frigate Jamaran was struck at Chabahar at the start of Epic Fury and is 'sinking'; Makran struck at Bandar Abbas (USNI imagery), sinking not confirmed",
          severity="1 frigate sinking per CENTCOM; 1 damaged", note="Mar 1 was the CENTCOM report date; the Jamaran strike was Feb 28. Makran sinking is unconfirmed."),
 9:  dict(severity="Tanker hit by debris from an intercepted Iranian missile (Times of Israel, AFP); casualty details still to confirm from an allowed outlet (earlier log: 1 killed, 2 injured, reportedly ashore)",
          note="Tanker was hit by debris from an intercepted missile; casualties were reportedly shoreside shipyard workers, not crew."),
 11: dict(detail="Two Iranian drones hit the US embassy in Riyadh; limited fire and minor damage per Saudi Defense Ministry (AP)", severity="No casualties reported",
          note="'CIA annex' is not in the AP reporting and was dropped. Exact date unconfirmed (AP page dated Mar 2-3)."),
 13: dict(detail="A US submarine sinks IRIS Dena ~40nm off Sri Lanka (reported as USS Charlotte by CBS citing unnamed officials; the Pentagon did not name it)",
          severity="Sri Lankan navy: 87 bodies recovered, 32 rescued (Al Jazeera). Iran's army later claimed 104 killed (Reuters, Mar 8) - a claim",
          note="'104 killed, 32 wounded' is an Iranian claim; Sri Lanka reported 87 bodies and 32 rescued."),
 19: dict(date=d(2026,3,24), detail="US 15-point ceasefire plan is passed to Iran through Pakistani intermediaries (AP)", severity="Iran rejected it and offered a counter-plan (AP)",
          note="Delivered via Pakistan on or before Mar 24; Mar 25 was the AP publication date."),
 20: dict(detail="Israel says it killed IRGC Navy commander Tangsiri and the IRGC Navy's intelligence chief Rezaei in Bandar Abbas (Israeli claim, Mar 26); Iran confirmed Tangsiri's death on Mar 30",
          severity="Tangsiri's death confirmed by the IRGC Mar 30; no Iranian confirmation of Rezaei found (Al Jazeera, AFP, AP)",
          note="Rezaei is the IRGC Navy's intelligence chief, not Iran's national intelligence chief. 'Blockade architect' label dropped as unverified."),
 21: dict(severity="At least 15 US troops wounded, 5 seriously (AP, NPR, Al Jazeera); multiple KC-135 tankers damaged; E-3 AWACS damaged per unnamed sources (WSJ via Al Jazeera)",
          note="Credible outlets say at least 15 wounded; '29' looks like a cumulative count."),
 22: dict(detail="IRGC statement bans shipping to/from ports of countries aligned with the US/Israel (reported via Iranian state media; not confirmed by an allowed outlet). Al Jazeera says the Strait was already declared closed on Mar 2",
          severity="The '20,000 mariners / 2,000 ships' figure is an IMO number from Mar 25, before this date",
          note="Not a new 'total closure': Al Jazeera (Mar 16) says the Strait was declared closed Mar 2. The Mar 27 statement is sourced only to Iranian state media via non-allowed outlets."),
 23: dict(date=d(2026,3,31), detail="Joint Chiefs Chairman Caine announces the first overland B-52 missions (NYT, Mar 31); strikes on an Isfahan ammunition depot reported separately by the WSJ (not read directly)",
          note="Mar 31 is the announcement date. No outlet read ties the B-52s to Isfahan or says when the flights began."),
 25: dict(severity="8 killed, 95 wounded per Iran's Alborz deputy governor (AFP; not independently verified); Iranian state TV first reported 2 (Al Jazeera headline: 2 killed)",
          note="Casualty figures are Iranian claims and vary by outlet."),
 26: dict(detail="Iran shoots down a US F-15E over Iran (ABC); an A-10 is hit separately and crashes in an allied country, its pilot rescued",
          severity="F-15E: one crew member rescued, the other's status unknown when ABC reported on Apr 4; two rescue helicopters hit but landed safely",
          note="'Both crews rescued' is not confirmed by an allowed outlet; the A-10 did not go down over Iran."),
 27: dict(date=d(2026,4,6), detail="Pakistan-mediated 45-day ceasefire framework; Iran says it will not reopen the Strait for a temporary ceasefire and sends a 10-point response (Al Jazeera, Reuters)",
          severity="Iran did not accept; counter-proposal sent", note="Date is Apr 6, not Apr 5. Iran did not flatly reject talks."),
 28: dict(detail="Trump announces a two-week ceasefire on Truth Social after Pakistan's PM Sharif asks him to extend his deadline; Iran's Supreme National Security Council accepts (Reuters, AP). Apr 7 US time / Apr 8 Gulf time",
          note="No credible outlet names VP Vance as the channel; Pakistan's leaders are named."),
 29: dict(detail="UNSUPPORTED AS LOGGED: no credible outlet reports a formally signed ceasefire with these terms. AP describes the Apr 7-8 ceasefire as built on a disputed 10-point Iranian plan with differing Farsi and English versions. Likely a duplicate of #28",
          note="Searched; AP and Reuters report no signed document and none of the listed terms (sanctions relief, frozen-asset release). Row kept only because other rows point to it."),
 30: dict(detail="Israel strikes 100+ targets across Beirut, southern Lebanon and the Bekaa in about 10 minutes, within hours of the ceasefire (AP)",
          severity="Lebanon's health ministry: at least 112 killed in the first count, later 182 (AP)", note="'Operation Eternal Darkness' name appears only in Israeli outlets (ynet, i24), not in allowed ones, so it was dropped."),
 32: dict(severity="Major fire at the refinery; WSJ reportedly said a significant part of capacity was knocked out for several months (seen via a secondary summary only)",
          note="Event confirmed; details revealed May 11-12 (WSJ/Bloomberg). 'Crippled for months' is stronger than what could be read."),
 37: dict(target="Iranian shipping", detail="US disables the Iranian container ship Touska with gunfire from USS Spruance (Apr 19, USNI); tankers Tifani and Majestic X interdicted in the Indian Ocean around Apr 22-24 (dates not confirmed by an allowed outlet)",
          severity="3 vessels", note="Touska is a container ship, not a tanker. Tifani/Majestic X dates conflict across outlets (Apr 22-24)."),
 50: dict(atype="Ceasefire (interim MOU signed)", detail="Trump and Pezeshkian sign a 14-point interim memorandum electronically on Jun 17 (Iran's foreign ministry calls it the 'Islamabad Memorandum of Understanding'): fighting stops on all fronts incl. Lebanon; 60 days to negotiate; the US starts lifting the blockade at once and ends it within 30 days; Iran makes 'best efforts' for free passage through Hormuz; oil-sanctions waivers now, full relief only in a final deal",
          note="Confirmed by Reuters, Al Jazeera and NPR. Earlier wording said it 'ended the blockade and reopened the Strait' outright; it was phased. Iran later said (Aug 12) the deal never took effect."),
 52: dict(date=d(2026,6,20), detail="Israeli strikes in Lebanon continue overnight after an Israel-Hezbollah ceasefire took effect Jun 19 (Reuters, AFP)",
          severity="20+ killed (Reuters); AFP: 16 in Nabatieh and 7 near Sidon", note="Strikes came overnight into Saturday Jun 20, not Jun 19."),
 65: dict(severity="3 US dead: 2 killed in action plus 1 missing, later declared believed killed in action (Army/DoD, Jul 22); 4 medically evacuated",
          note="Toll is 3 dead, not '2 KIA + 1 missing'. The attack was Fri Jul 17; some outlets say Jul 18."),
 69: dict(detail="Mine clearance of the Traffic Separation Scheme; 100+ suspected mines found and removed (Axios: by private contractors; CENTCOM credits Navy divers, SEALs and air power)",
          note="Axios says private contractors did the removal, not the Navy alone."),
 70: dict(severity="Iranian state media (IRNA, a claim): at least 2 killed and several wounded; no US-confirmed casualty figure (CNN)", note="Casualty figure is an Iranian claim."),
 72: dict(actor="Disputed", atype="Tanker attack (cause disputed)", detail="Saudi (Bahri) tanker Sidr hit late Aug 31; a second tanker, Senegal Prosperity, reported hit by 3 projectiles the same night. IRGC says mines; CENTCOM calls that false; Saudi Arabia blames Iran; Iran denies",
          severity="2 Filipino crew killed (Bahri)", note="First draft framed this as an accident that undercut the mine-clearance claim and listed '1 tanker damaged'. Credible outlets show a disputed attack with 2 killed."),
 75: dict(severity="Jordan says it intercepted 10 of 13 Iranian missiles, 3 fell in open ground; US officials: no injuries or significant damage. IRGC claimed destroyed drones/aircraft and US deaths - unverified, denied by US and Jordan",
          note="Jordan reported it early Sep 2 local time (Sep 1 evening US time); date left as logged. The claim of 'several aircraft destroyed' is an IRGC claim that was denied."),
 76: dict(detail="LIKELY DUPLICATE OF #75: no credible outlet describes a separate, larger Iranian wave on Sep 2; the only Jordan attack found is the 13-missile salvo in #75 (Al Jazeera: 'heaviest exchange in more than a month')",
          note="The 'most extensive since the ceasefire' wording traces to a Persian-language outlet that fails the source standard. Pair 21 and census row 76 depend on this row and are flagged."),
 78: dict(note="Sources conflict on the date: CENTCOM is reported to date this Sep 8. Not yet confirmed from an allowed outlet."),
 79: dict(note="CENTCOM is reported to date the tanker strike Tuesday Sep 8 (log: Sep 9); likely a US-vs-Gulf or reporting-date difference. Not yet confirmed from an allowed outlet."),
 80: dict(severity="~20 missiles per Jordan (18 of 20 intercepted); 1 A-10 lost a wing and ~8 F-15s lightly damaged (CBS); more than 30 Patriot interceptors fired (CBS)",
          note="Jordan's statement is timestamped Sep 8 evening local time, so the log's Sep 9 may be a reporting date. CBS says 'more than 30' Patriots, not '~30'. Sourced via a non-allowed outlet quoting CBS; not yet read directly."),
}
_EDITS.update({
 14: dict(atype="Blockade escalation (mine-laying alleged)", detail="CENTCOM says US forces destroyed 16 Iranian minelayers near Hormuz on Mar 10; Trump said the US had 'no reports' of mines being laid. Pentagon: Iranian ballistic-missile launches down ~90%, drones ~83%",
          severity="16 minelayers claimed destroyed by CENTCOM the same day",
          note="Minelayers were claimed destroyed the same day, not later. The '~92%' figure looks like Israel's interception rate, not the fall in Iranian launches."),
 16: dict(actor="US/Israel (alleged)", atype="Strike (alleged)", detail="Iran reports an attack on Natanz and blames the US and Israel; the Israeli military denied involvement and the IAEA saw no rise in off-site radiation",
          severity="n/a - no casualty or damage figures from credible outlets",
          note="No allowed outlet says this was a US bunker-buster strike; it is confirmed only as Iran's report. Pair 3 rests on Iran treating it as the trigger."),
 17: dict(detail="Iran strikes toward Dimona and Arad and calls it a 'response' to Natanz; Iran did not claim to target the Negev research center",
          severity="No deaths; at least 180 wounded (Israel's Health Ministry, via Al Jazeera)", note="Wounded count is at least 180, not 175; Iran framed it as a response to Natanz, not as an attack on the research center."),
 38: dict(severity="No casualties (AFP, Reuters)", note="Reuters ties it to the US seizure of the Touska; the IRGC's own stated reasons were blockade and permit violations."),
 39: dict(severity="1 injured: a 'security official' (AP) or 'service member' (Al Jazeera); Iran says it was a navigation error",
          detail="Bubiyan Island raid attempt: 6 IRGC troops by fishing boat, 4 detained, 2 escape; Kuwait announced it on May 12", note="Incident May 1, announced May 12. Injured person is described differently by AP and Al Jazeera."),
 40: dict(date=d(2026,5,4), detail="Operation Project Freedom: announced May 3, began May 4; Navy escort mission for stranded ships; US says six boats sunk (Trump said seven); pause announced May 5 US time (May 6 Gulf time)",
          note="Operations began May 4 (announced May 3); pause announced May 5 US time. US says six boats sunk, Trump said seven."),
 41: dict(severity="No casualties; none of the 3 destroyers (Truxtun, Rafael Peralta, Mason) was struck (CENTCOM)", note="Confirmed. US vs Gulf time can put this on May 7 or 8."),
 42: dict(detail="US strikes sites near Bandar Abbas and Qeshm Island (CENTCOM did not name the IRGC)", note="Confirmed; the 'IRGC facilities and missile sites' wording was not supported."),
 47: dict(severity="AP: Jordan shot down 5 missiles aimed at Muwaffaq Salti AB. Axios: a US official counted at least 4 ballistic missiles plus drones across the three countries. IRGC claim of 21 targets is unverified",
          note="Rows 47 and 48 are separate waves, not an overlap. IRGC target claim is unverified."),
 48: dict(detail="Iranian missile wave at a Jordan base near Azraq; Jordan says it intercepted all 20 incoming missiles", severity="Jordan (official statement): 20 missiles intercepted; the IRGC's own claim of 12 is not cited",
          note="Only allowed source is Jordan's official statement; the '12 missiles' figure was an IRGC claim."),
 55: dict(note="NPR/AP place CENTCOM's ~10-target retaliation (for the Iranian drone hit on the tanker Kiku) on Jun 27 and Iran's Bahrain/Kuwait fire on Jun 28. The log's dates for #55/#56 are probably a day early; not yet corrected."),
 56: dict(note="NPR/AP place Iran's Bahrain/Kuwait fire on Jun 28, after CENTCOM's Jun 27 strikes; the log's date is probably a day early; not yet corrected. Axios: both sides agreed to halt attacks Jun 29."),
})
_EDITS.update({
 5:  dict(detail="Iran fires missiles at Israel, Kuwait and other Gulf targets; a missile hits a residential block in Tel Aviv; Kuwait International Airport is hit by a drone",
          severity="Tel Aviv: 1 killed, 27 injured (Times of Israel); Kuwait airport: minor injuries to staff",
          note="Tel Aviv casualty figures confirmed by Times of Israel (an Israeli outlet; its own pieces vary between 20 and 27 injured). The operation name 'True Promise IV' and the '49 intercepted over Jordan' detail were not found in any allowed outlet and were dropped from the wording."),
 6:  dict(detail="Iranian strikes on US/allied radar and base sites across the Gulf and Jordan; one THAAD AN/TPY-2 radar in Jordan 'apparently destroyed'; strikes on Manama, Kuwait airport, Abu Dhabi airport and Erbil reported the same day",
          severity="One radar (Jordan) apparently destroyed per CNN satellite-image analysis; The War Zone says it 'appears' destroyed; no US confirmation. UAE and Saudi radar damage unclear",
          note="'Destroyed' applies to one radar only and rests on imagery analysis, not a US statement. Manama, Kuwait airport, Abu Dhabi airport and Erbil are confirmed by Al Jazeera; Riyadh was not found in the sources read."),
 9:  dict(detail="Tanker Stena Imperative hit by suspected Iranian projectiles at a Bahrain port; smoke near the US embassy in Kuwait reported by a witness",
          severity="USNI: 1 shipyard worker killed and 2 injured ashore at the Bahrain port; crew unhurt. A strike on the Kuwait embassy itself is not confirmed",
          note="The '1 killed, 2 injured' figure belongs to the Bahrain port incident only. Attribution is 'suspected' Iranian (USNI). 'US embassy Kuwait struck' rested on a witness seeing smoke."),
 10: dict(actor="Israel (IDF)", detail="IDF says it struck Iran's Supreme National Security Council complex in Tehran (Mar 2-3) and destroyed a secret underground site on Tehran's outskirts where Iran moved its nuclear work (IDF claim)",
          severity="n/a - all details are IDF claims; site name spelled 'Minzadehei' by Times of Israel",
          note="Attributed to Israel, not the US. The IDF claims come via Times of Israel. The Expediency Council building appears only in Iran International (not an allowed outlet), so it is not claimed here."),
 12: dict(date=d(2026,3,3), detail="Iranian missile hits the US base at Al Udeid, Qatar (Mar 3); separately a drone attack on Saudi Aramco's Ras Tanura refinery causes a precautionary shutdown (Mar 2, Iran-attributed)",
          severity="Al Udeid: 2 missiles launched, 1 intercepted, 1 struck the base, no casualties (Qatar Defense Ministry). Ras Tanura: fire from drone-interception debris, some operations halted, no injuries (Saudi energy ministry / SPA)",
          note="The first draft lumped two events onto Mar 4. Al Udeid was hit Mar 3; Ras Tanura Mar 2. Iran has denied attacking Aramco, so that attribution rests on Gulf-state sources."),
 15: dict(date=d(2026,3,21), detail="CENTCOM (Adm. Cooper, Mar 21) says the US has struck 8,000+ targets, including 130 Iranian vessels, since Feb 28. Iran's Tasnim says at least 16 cargo vessels burned at Bandar Lengeh/Kong after a US-Israeli attack (Mar 20)",
          severity="8,000 targets / 130 vessels are CENTCOM claims for the whole war to date; the 16 burned boats are an Iranian claim and Iran calls them civilian cargo boats",
          note="This was not a campaign that 'began Mar 19': the figures cover the war so far. Re-dated to the Mar 21 CENTCOM briefing."),
 49: dict(date=d(2026,6,17), atype="Ceasefire (interim MOU signed)", detail="Pakistan's PM announces agreed text of a US-Iran memorandum on Jun 12; Trump and Pezeshkian sign the 14-point interim deal digitally on Jun 17, extending the ceasefire by 60 days (Reuters)",
          severity="n/a - Iran later said (Aug 12, via Reuters) the interim deal never took effect",
          note="'Terms agreed Jun 12' was only partly right: Jun 12 is when Pakistan announced the text; signing was Jun 17. This overlaps with event #50 (the same deal). Kept separate for now."),
 55: dict(note="Date confirmed: NPR (AP) and Al Jazeera put the roughly one-hour US strike on Fri Jun 26, after a projectile hit a container ship off Oman on Jun 25. A separate, larger CENTCOM round of about 10 targets followed on Jun 27 after the tanker Kiku was hit."),
 56: dict(detail="Tanker Kiku hit by a one-way drone near Hormuz (Jun 27, per CENTCOM; Iran has not confirmed); overnight Jun 27-28 the IRGC fires drones and missiles at Kuwait (intercepted) and Bahrain",
          severity="Kuwait: intercepted. Bahrain: AP gives only its condemnation. No casualties found",
          note="Split into tanker (Jun 27) and Gulf fire (overnight Jun 27-28). A pause afterwards is single-source: Axios (Jun 29) says both sides agreed to halt attacks, while AP's Jun 28 report mentions no pause and says the exchange strained the interim deal."),
 61: dict(detail="Iran's IRGC says it fired 10 ballistic missiles at the Azraq base in Jordan (Muwaffaq Salti AB is at Azraq); Jordan says it intercepted 8",
          severity="Jordan: 8 intercepted, falling fragments only, no casualties or material damage (the other 2 are not accounted for)",
          note="Confirmed by AFP and Reuters. Neither names Muwaffaq Salti, but it is the air base at Azraq."),
 64: dict(detail="IRGC claims strikes on US sites at Juffair, Bahrain (Jul 13) and says it destroyed a Patriot radar and other radars (Jul 14)",
          severity="IRGC claim only; no US or Bahraini confirmation or damage assessment found",
          note="Everything about damage is an Iranian claim (Tasnim). Not confirmed by AP, Reuters, AFP or CNN in what was read."),
 66: dict(detail="IRGC says ballistic missiles hit US aircraft at Aqaba airport (Jul 19); Jordan says it shot down 3 missiles and a 4th fell in open ground",
          severity="Damage is an IRGC claim only. Jordan and Israel report no damage or injuries (AFP)",
          note="Strike confirmed by AFP. 'King Hussein International Airport' appears in the sources only as 'Aqaba airport'. The US embassy said Aqaba was evacuated over a 'credible threat'; Jordan denied any evacuation."),
 67: dict(detail="IRGC claims it destroyed a missile-defense radar and an F-15 at a US base in Jordan (Jul 21). No US or Jordanian confirmation",
          severity="IRGC claim only",
          note="The claim exists only in non-allowed relays (Middle East Eye, APA citing Al Jazeera), so nothing here is verified. A different, later claim (Jul 23, AFP) names other equipment; do not conflate."),
 68: dict(note="Confirmed as published and attributed: Trita Parsi is quoted in a CNN analysis by Tim Lister (Aug 19). It is an opinion, not an event, and was read through a credited republication."),
 75: dict(note="Jordan reported the attack early Sep 2 local time (Sep 1 evening US time); date left as logged. The 'several aircraft destroyed' item is an IRGC claim that the US and Jordan denied. Event #76 is a duplicate of this event (two outlets describe one exchange)."),
 76: dict(detail="DUPLICATE OF #75: Al Jazeera's Sep 1 and Sep 2 stories describe one Iranian response (Jordan intercepted 10 of 13 missiles). No allowed outlet reports a separate, larger wave on Sep 2",
          note="Confirmed duplicate by two independent checks. The 'most extensive since the ceasefire' wording comes from a Persian-language outlet that fails the source standard. Excluded from all statistics. Pair 21 is permanently held out."),
 78: dict(note="Confirmed by CENTCOM's Sep 8 release: the IRGC targeted a US warship with ballistic missiles twice over the previous two days; it evaded both, no one hurt. Exact launch times are not published."),
 79: dict(date=d(2026,9,8), detail="CENTCOM destroys five IRGC crude oil carriers (four in the Gulf of Oman, one near Kharg Island) after the IRGC's missile attempts on a US warship",
          note="Date corrected from Sep 9 to Sep 8 (CENTCOM release, Reuters dateline, Al Jazeera 'late Tuesday'). The 'tanker for tanker' label was not found; Secretary of State Rubio said Iran 'is going to lose tankers'."),
 80: dict(severity="1 A-10 lost a wing, ~8 F-15s lightly damaged (CBS, anonymous US sources; CENTCOM had not confirmed). More than 30 Patriot interceptors fired per CBS; 'roughly 30' per a US official (Reuters/AAP). Jordan: 18 of 20 missiles intercepted",
          note="Sep 9 is right for Jordan local time (overnight Sep 8-9); in US time it began the evening of Sep 8. Damage details rest on anonymous US sources. The AAP/Reuters piece also cites CSIS: fewer than 850 Patriot interceptors left."),
})
_EDITS.update({
 84: dict(note="Caution (Oct 11 check): trade press says one ship was hit the evening of Sep 28 and three tankers on Sep 29, so this row may merge two days. Not yet checked against UKMTO."),
 101: dict(note="Iranian claim only (Tasnim); no allowed outlet confirms the hit."),
 103: dict(note="Iranian claim reported by Al Jazeera; the mine strike is not independently confirmed."),
 98: dict(note="Context row: Saudi-Houthi front, not a direct Iran-US act. Kept because an American was killed on Oct 10 and Trump said he is weighing a response."),
 102: dict(note="Context row: Saudi-Houthi front. One American killed; Trump said he is weighing a response. CNN read as a snippet only."),
 106: dict(note="Catch-up row: the strike was on Oct 6 but CENTCOM announced it only on Oct 14. Surveillance, not an attack, is what CENTCOM describes."),
 109: dict(note="UKMTO counted 10-12 confirmed attacks on ships in the week to Oct 16 (CBS, Al Jazeera); only the incidents with details are logged as rows. Attacker per CENTCOM (IRGC); Iran claimed a mine."),
 111: dict(note="Plans rest on unnamed sources (CBS); no decision reported. Trump's no-strike pledge before Nov 3 (#97) still stands."),
 113: dict(note="Iranian claim reported by Al Jazeera/AFP; CENTCOM disputes the mine account. Iran's army separately said two tankers caught fire in its 'prohibited zone' in the Gulf of Oman on Oct 15-16 (not logged; in the review queue)."),
})
_DATE_CONFLICT = set()
_NOT_SUPPORTED = {22, 29, 67, 76}
_PARTLY = {5, 6, 9, 10, 32, 64, 66, 101, 103, 113}
# Re-sourcing round, 2026-10-22: corrections found while re-checking low-credibility rows (see CHANGELOG).
_EDITS.update({
 43: dict(atype="Ceasefire (restored)", detail="Iran agrees to halt attacks on Israel after the two traded fire on Jun 6-7, the first exchange since the April ceasefire",
          note="Corrected (NPR, Jun 8): the old text said Israel and Iran 'had not exchanged fire since'; in fact they traded fire Jun 6-7 and Iran then agreed to stop."),
 46: dict(detail="US strikes Iranian air-defense, ground-control and surveillance radar sites near the Strait after Iran downs a US Apache (CENTCOM: 'proportional response')",
          note="Corrected (NPR, CENTCOM): the named towns (Qeshm, Sirik, Jask, Bandar Abbas) are not in the Jun 9 reports; Al Jazeera's Jun 10 live page puts the next day's strikes at Sirik, Bandar Abbas and Qeshm."),
 54: dict(detail="Iranian drones attack the container ship Ever Lovely near Oman in the Strait; Trump calls it a 'foolish violation' of the Jun 17 memorandum",
          note="Confirmed (Al Jazeera, Jun 26): four one-way attack drones per Trump, one hit the upper deck; no crew hurt."),
 57: dict(severity="Significant damage, no casualties (US official via Axios); no one claimed the attacks (Reuters)",
          note="Confirmed (Axios, Reuters): at least three commercial ships hit Jul 6-7. The old '49 to 25 vessels a day' traffic figure was not found in an allowed outlet and was dropped."),
 58: dict(detail="Treasury withdraws the general license allowing Iranian oil sales (wind-down to Jul 17) after the tanker attacks",
          note="Confirmed (Reuters via Honolulu Star-Advertiser, Jul 7)."),
 59: dict(note="Confirmed (NPR, published Jul 8): NPR dates Trump's remark to Tuesday, Jul 7, so the row date was moved from Jul 8 to Jul 7 (review, Oct 22)."),
 60: dict(detail="About 90 targets along Iran's coast (air defenses, coastal surveillance, missile and drone storage, naval and logistics sites), the second night in a row after ~80 on Jul 7 (CENTCOM)",
          note="Corrected (CENTCOM, Bloomberg): no allowed outlet puts bridges among the Jul 8 targets. The bridge strikes (two bridges in Hormozgan, 3 killed per Iranian state TV) were on Jul 16-17 (AFP), inside the nightly campaign that is excluded from the census."),
 85: dict(date=d(2026, 9, 29), note="Date corrected to Sep 29 (Al Jazeera; AP via PBS): Treasury announced the sanctions on Tuesday, Sep 29, not Sep 28."),
})

_EDITS.update({
 44: dict(date=d(2026,6,8), note="Date corrected to Jun 8 (AFP via Al Arabiya, published Jun 9): the Israeli strikes were overnight into Monday Jun 8; Iranian state TV (a claim) said at least 2 air-defense personnel were killed (re-sourced Oct 28)."),
 45: dict(date=d(2026,6,8), note="Date corrected to Jun 8 (CBS, updated Jun 9): the Apache went down Monday Jun 8 and both crew were rescued about two hours later by an unmanned surface drone; CBS sources say a Shahed drone (re-sourced Oct 28)."),
 83: dict(detail="5 men in their 20s are arrested on Sep 27 on suspicion of explosives offences after three suspicious vehicles head toward RAF Fairford (a base used for US bombers); Rubio says it 'clearly involves the hands of a foreign actor', Trump says it 'might be' linked to Iran, and UK PM Burnham says there are 'strong indications that Iran played a part' (Iran denies)",
     note="Wording corrected (Stars and Stripes, Sep 30): the source does not say the men planned to do 'big damage'; it says they are suspected of planning a terrorist attack near the base. They were released on bail Sep 28 and Trump questioned the bail (re-sourced Oct 28)."),
 87: dict(detail="Treasury sanctions Iran's automotive and rail sectors and a shadow banking network, calling the targets 'some of the last significant elements of Iran's failing industrial infrastructure'",
     note="Wording corrected (Treasury press release, Oct 1): Treasury says 'failing industrial infrastructure', not 'IRGC-linked industrial base', and its release does not tie the banking network to Russia, so the Russia claim was dropped (re-sourced Oct 28)."),
})

_PENDING_TEXT = "PENDING - no credible source confirmed yet"


def _norm(outlet):
    return _re.sub(r"\s*\(.*\)\s*$", "", outlet).strip()


def _build_audit(rows):
    out_rows, audit = [], {}
    for row in rows:
        (eid, date_, actor, atype, target, detail, trig, sev, conf, src) = row
        v = _VERD.get(eid)
        srcs = _SRC.get(eid, [])
        e = _EDITS.get(eid, {})
        outlets = []
        for sc in srcs:
            key = (_norm(sc["outlet"]), sc["published"])
            if key not in outlets:
                outlets.append(key)
        distinct = {o for o, _ in outlets}
        if eid in _NOT_SUPPORTED:
            check = "Not supported"
        elif eid in _PARTLY:
            check = "Partly verified"
        elif eid in _DATE_CONFLICT:
            check = "Date conflict"
        elif v is None:
            check = "Not re-checked"
        elif v in ("confirmed", "corrected") and srcs:
            check = "Verified" if v == "confirmed" else "Corrected"
        else:
            check = "Pending"
        # new row values
        date_ = e.get("date", date_)
        actor = e.get("actor", actor)
        atype = e.get("atype", atype)
        target = e.get("target", target)
        detail = e.get("detail", detail)
        sev = e.get("severity", sev)
        if check in ("Verified", "Corrected", "Partly verified", "Not supported"):
            src = "; ".join(f"{o} {p}" for o, p in outlets) if outlets else "No credible source found (see audit note)"
        elif check == "Pending":
            src = _PENDING_TEXT
        # confidence follows the source check
        if check in ("Verified", "Corrected", "Partly verified"):
            conf = "High" if len(distinct) >= 2 and check != "Partly verified" else "Medium"
        elif check in ("Pending", "Not supported"):
            conf = "Low"
        elif check == "Date conflict":
            conf = "Medium"
        # A row backed only by Iranian state media is a claim, not a confirmation.
        if distinct and distinct <= {"Tasnim", "IRNA", "Press TV", "Fars"}:
            conf = "Low"
        audit[eid] = {"check": check, "note": e.get("note", "")}
        out_rows.append((eid, date_, actor, atype, target, detail, trig, sev, conf, src))
    return out_rows, audit


events_raw = events
events, event_audit = _build_audit(events_raw)


# ---------------------------------------------------------------------------
# Consequences of the source audit for pairs and the census
# ---------------------------------------------------------------------------
# Pair 21 (#75 -> #76) depends on event #76, which credible outlets do not support
# as a separate event (it looks like a duplicate of #75). It is held out of every
# statistic until that is resolved.
_PAIRS_HOLD = {21: "Event #76 is a confirmed duplicate of #75 (two credible-outlet checks), so this pair is permanently held out of all statistics."}
pairs_on_hold = [p for p in pairs if p[0] in _PAIRS_HOLD]
pairs = [p for p in pairs if p[0] not in _PAIRS_HOLD]

_census_fix = {
 75: (75, "Military/Property", "Unverified", "Its only logged reply (#76) is held out as a likely duplicate of #75. Not counted until resolved."),
 76: (76, "Military/Property", "Unverified", "Event #76 is likely a duplicate of #75, so it is not counted. Earlier 'CENTCOM struck IRGC sites Sep 4' lead came from a weak source."),
}
census = [_census_fix.get(c[0], c) for c in census]

# Re-check results from credible outlets so far (status codes are NOT changed yet - see task list).
census_evidence = {
 14: "Re-checked (Times of Israel, citing CENTCOM): the US destroyed 16 Iranian minelayers on Mar 10, the same day. Would score R-strong.",
 15: "Re-checked: no credible source for the Mar 19 event itself; AP ties Iran's Mar 21 Dimona/Arad strike to Natanz (#16), not to this.",
 17: "Partly checked (AP, Mar 27): names no US strike as a reply; Mar 28-Apr 1 not yet checked.",
 21: "Partly checked (AP, Mar 27): names no US strike as a reply; Mar 28-Apr 1 not yet checked.",
 23: "Re-checked (Al Jazeera, Times of Israel): Iran hit a Kuwaiti tanker Mar 30-31 and fired at Israel Apr 1, but no outlet links them to this. Borderline N / R-weak.",
 25: "Re-checked (The War Zone): Iran threatened bridge strikes and fired at Israel that evening but did not frame it as a reply.",
}


# ---------------------------------------------------------------------------
# Census update, round 2 (credible-outlet re-checks) + continuous-war exclusion
# ---------------------------------------------------------------------------
_census_round2 = {
 42: (42, "Military/Property", "R-weak", "US strikes near Bandar Abbas/Qeshm, May 7. The UAE said it intercepted Iranian missiles and drones May 8 (Reuters), but Iran claimed no reply and CENTCOM disputed Iran's claimed counterattack. Weak call."),
 56: (56, "Military/Property", "R-strong", "Iran's tanker hit (Kiku) and Bahrain/Kuwait fire, Jun 27-28. NPR and AP: CENTCOM struck about 10 targets as retaliation; Iran's Bahrain/Kuwait fire on Jun 28 answered those strikes. Both sides agreed to halt Jun 29 (Axios)."),
 80: (80, "Military/Property", "N", "Iran hits Muwaffaq Salti AB, Sep 8-9. No credible report of any US strike on Iran Sep 10-Oct 6; WSJ and a Time interview say Trump expects to resume bombing after the midterms."),
}
census = [_census_round2.get(c[0], c) for c in census]
census_evidence.update({
 33: "Re-checked (Reuters Apr 12, USNI, The War Zone, NPR): only an IRGC warning; no Iranian attacks Apr 11-17.",
 42: "Re-checked (Reuters): weak. Reply is the UAE intercepting Iranian missiles May 8, which Iran did not claim.",
 56: "Re-checked (NPR, AP, Axios): CENTCOM struck ~10 targets in retaliation; Iran answered Jun 28; both sides halted Jun 29.",
 77: "Re-checked (CENTCOM): two IRGC missile attempts on a US warship before Sep 8; only Iran's own framing ties them to the Sep 5 strikes.",
 80: "Re-checked (WSJ via ANI, Time interview, Reuters/AAP): no US strike on Iran Sep 10-Oct 6.",
 85: "Re-checked (Reuters, UKMTO, AFP): tanker hits reported with no one blamed; no outlet links them to the sanctions.",
 87: "Re-checked (Reuters, UKMTO, AFP): tanker hits reported with no one blamed; no outlet links them to the sanctions.",
})

# ---------------------------------------------------------------------------
# Census update, round 3 (credible-outlet re-checks)
# ---------------------------------------------------------------------------
_census_round3 = {
 31: (31, "Economic/Blockade", "R-weak", "Iran keeps the Strait mostly shut after the Apr 8 ceasefire, citing Lebanon strikes. The US announced its blockade Apr 12 (in force Apr 13), but outlets tie it to the collapse of the Islamabad talks, not to Iran's restriction. Timing only."),
 36: (36, "Economic/Blockade", "R-weak", "Iran re-closes the Strait Apr 18 over the US blockade. The US seized the container ship Touska about Apr 19 (NPR), but NPR does not say it answers the closure; it is blockade enforcement that was already under way. Timing only."),
 40: (40, "Military/Property", "R-weak", "Project Freedom began May 4 (paused May 5). Iran hit the UAE, a tanker and a cargo ship May 4 (CBS, Al Jazeera), but Al Jazeera stops short of calling it retaliation. Timing only."),
 53: (53, "Economic/Blockade", "N", "Iran claims the Strait closed again, Jun 20. The US reply that day was verbal only (CENTCOM: Iran 'does not control' the Strait). US-Iran talks opened Jun 21; the next US strike was Jun 26 and outlets tie it to a Jun 25 ship attack."),
}
census = [_census_round3.get(c[0], c) for c in census]
census_evidence.update({
 31: "Re-checked (Times of Israel, NPR snippets, Al Jazeera): blockade came Apr 12-13, tied to failed talks. NPR pages were seen only as snippets.",
 36: "Re-checked (NPR, Al Jazeera): Touska seized about Apr 19; NPR does not link it to the closure.",
 40: "Re-checked (CBS, Al Jazeera): Iran attacked the UAE and ships May 4; no outlet calls it retaliation.",
 53: "Re-checked (Times of Israel, Al Jazeera, NPR): verbal reply only; talks Jun 21; next US strike Jun 26 tied to a Jun 25 ship attack.",
 22: "Re-checked: no allowed outlet carries the Mar 27 announcement itself, and it falls in the continuous-war window anyway.",
 39: "Re-checked (Al Jazeera, Israel Hayom): Kuwait kept the May 1 raid quiet until May 12. Kuwait's reply on May 12 was diplomatic only; no US response found.",
})
# Row 39: the raid was secret for 11 days, so 'a reply within 5 days' is not a fair test. Not counted.
_CENSUS_NOT_COUNTED = {39: "Bubiyan Island raid (May 1): Kuwait did not announce it until May 12, so no one could reply within 5 days. Kuwait's reply on May 12 was a protest and an ambassador summons, not a hostile act. Not counted."}
census = [c for c in census if c[0] not in _CENSUS_NOT_COUNTED]

# Weekly update, Oct 19: new US acts whose ~5-day window has closed (or is still open). They are
# logged as Unclear / Unverified so they do NOT change any rate until Sidd decides how to score
# them (see CHANGELOG 2026-10-19 and the suggestion in the weekly report). Proposed call in brackets.
census += [
 (104, "Economic/Blockade", "Unclear", "US jet disables a blockade runner, Oct 10-11. No Iranian attack on US forces, bases or US-flagged ships Oct 11-16 (forecast F001 resolved NO). But attacks on commercial shipping surged (GFS Pride sunk Oct 13), and Iran said it was stepping up strikes over the blockade and sanctions; no outlet ties them to this strike. [Proposed: N, as for #85/#87.]"),
 (106, "Military/Property", "Unclear", "US destroys an IRGC-linked surveillance dhow, Oct 6 (announced Oct 14). No Iranian attack on US forces found Oct 6-11; shipping attacks continued (#94, #96, #100, #101). No outlet links them. [Proposed: N.]"),
 (107, "Economic/Blockade", "Unclear", "US shadow-fleet sanctions, Oct 8. Shipping attacks continued Oct 9-13 (#100, #101, #103, #105, #109); no outlet ties them to these sanctions specifically. [Proposed: N, as for #85/#87.]"),
 (110, "Economic/Blockade", "Unclear", "US shadow-banking sanctions, Oct 15 (checked Oct 26). No Iranian attack on US forces, bases or US-flagged ships Oct 15-20. Shipping attacks continued (#112, #113, #114, #117); no outlet ties them to these sanctions. [Proposed: N, as for #85/#87.]"),
]
# Weekly update, Oct 26: new US sanctions whose window is still open.
census += [
 (119, "Economic/Blockade", "Unverified", "US shadow-fleet sanctions, Oct 21. Window runs to Oct 26; check next week. So far: IRGC claims of tanker hits Oct 22-23 (#121, #123) and a threat against US bases, no attack on US forces found."),
]

# Continuous-war rule: while both sides were striking each other daily, every act is
# automatically 'answered' by the next day's strikes, which would inflate the reply rate.
# Triggers inside these windows are moved out of the census; the acts that STARTED each
# stretch (#2, #57, #60) stay in.
_OPEN_WAR = [(d(2026, 2, 28), d(2026, 4, 7)), (d(2026, 7, 7), d(2026, 7, 25))] + _pre.WINDOWS
_START_ACTS = {2, 57, 60} | _pre.START_ACTS
_ev_date = {e[0]: e[1] for e in events}
census_open_war_excluded = [c for c in census if c[0] not in _START_ACTS
                            and any(a <= _ev_date[c[0]] <= b for a, b in _OPEN_WAR)]
census = [c for c in census if c not in census_open_war_excluded]
census_exclusions[0] = ("Continuous war, Feb 28 - Apr 7 (until the first ceasefire): both sides were striking each other every day, so every act has a 'reply' by default, "
                        "which would inflate the rate. Event 2, the act that started the war, is counted; later events in that stretch are not.")
census_exclusions[1] = ("Nightly US campaign, Jul 7-25 (events 58 and 61-67): same reason. Events 57 and 60, which started it, are counted. Event 65 (US troops killed Jul 17) was "
                        "followed by a US strike on Jul 18 that officials said was to 'punish' the IRGC, but it is excluded here for consistency.")
census_exclusions.append("Candidates moved out of the census by the continuous-war rule: " + ", ".join("#%d" % c[0] for c in census_open_war_excluded) + ".")
census_exclusions.append(" ".join(_CENSUS_NOT_COUNTED.values()))
census_exclusions.append("Pre-war continuous fighting: Oct 17, 2023 - Jan 29, 2024, Iran-backed militias attacked US forces almost daily, so US strikes in that stretch (#233, #234, #236, #237) are context only. "
                         "The twelve-day war (Jun 13-24, 2025) is treated the same way; the US strike that brought the US in (#255) is counted.")
census_exclusions.append("Pre-war rows not counted: #207 (defensive drone shootdown), #211/#231/#246/#259/#261 (deployments, measured separately), talks (#248-#252, #260, #262).")


# ---------------------------------------------------------------------------
# Kind of act, used by the Monthly Summary (and available to the matcher).
#   Kinetic    - strikes/attacks on territory, bases or forces
#   Maritime   - attacks on shipping, seizures, blockade moves, mines
#   Diplomatic - proposals, talks, ceasefires, statements, ultimatums
#   Sanctions  - economic penalties
#   Posture    - deployments and withdrawals
#   Other      - analysis, plots, everything else
# ---------------------------------------------------------------------------
def act_kind(atype, detail=""):
    a = (atype or "").lower(); t = (detail or "").lower()
    ship = any(w in t for w in ("ship", "tanker", "vessel", "cargo", "carrier"))
    if "sanction" in a: return "Sanctions"
    if "posture" in a or "deploy" in a or "withdrawal" in a: return "Posture"
    if any(w in a for w in ("shipping", "seizure", "blockade", "tanker", "mine")): return "Maritime"
    if "violation" in a and ship and "strike" not in a: return "Maritime"
    if any(w in a for w in ("strike", "retaliation", "assassination", "incursion", "operation", "raid", "violation", "air defense", "shootdown")): return "Kinetic"
    if any(w in a for w in ("diplomatic", "ceasefire", "ultimatum", "authorization", "talks", "mou", "proposal", "rejection", "statement", "demand")): return "Diplomatic"
    return "Other"

event_kind = {e[0]: act_kind(e[3], e[5]) for e in events}


# ---------------------------------------------------------------------------
# Merged duplicates (approved by Sidd). The duplicate row stays as a record of the mistake;
# its reports move to the surviving event, and anything that pointed at it is repointed.
# ---------------------------------------------------------------------------
MERGED = {76: 75, 49: 50, 29: 28}
_MERGE_NOTES = {
 76: "Merged into #75 (same Sep 1-2 attack on Jordan, reported over two days).",
 49: "Merged into #50 (same Jun 17 signing; Jun 12 was only Pakistan's announcement that the text was agreed).",
 29: "Merged into #28 (same Apr 7-8 ceasefire; no signed document or listed terms were ever reported).",
}
for _k, _n in _MERGE_NOTES.items():
    event_audit[_k]["note"] = (event_audit[_k]["note"] + " " + _n).strip()
events = [e if e[6] not in MERGED else e[:6] + (MERGED[e[6]],) + e[7:] for e in events]
_EV50 = event_audit[50]
_EV50["note"] = (_EV50["note"] + " Also covers former row #49: Pakistan announced the agreed text on Jun 12.").strip()
