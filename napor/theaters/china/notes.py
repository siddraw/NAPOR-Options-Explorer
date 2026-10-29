"""China / Taiwan: analyst notes (judgement, not data; the page labels every line that way). Facts cite event IDs from events.py.
Numbers are small on every option: see THEATER["small_n"] in config.py."""

PROS = {
    "A": "Adds no new US act for China to answer. Not measured: hold weeks are not built for China (see the note on option A).",
    "B": "No direct casualties. Talks and leader meetings are logged from Oct 1995 to Jul 2026 (for example #3503, #3516, #3547, #3565, #3035, #3039, #3060, #3061); none of the 21 counted cases was followed by a Chinese drill or counter-sanction within 7 days.",
    "C": "Targets Chinese defense and chip supply without a military clash. The log has the Sep 2018 sanctions on China's Equipment Development Department (#3561), the Oct 2022 chip controls (#3030) and the Aug 2020 Entity List round (#3014, not counted).",
    "D": "Asserts passage rights with no shots fired. The 15 counted transits and FONOPs since 2015 drew protests and shadowing, apart from two close passes at sea: the Decatur on Sep 30, 2018 (#3562, #3563) and the Chung-Hoon on Jun 3, 2023 (#3033, #3034).",
    "E": "Equips Taiwan. The log has 9 counted sales: 2001, 2008, 2010, Dec 2015, 2017, Jul 2019, Oct 2020, Feb 2022 and Dec 2025 (#3517, #3524, #3527, #3539, #3548, #3007, #3019, #3023, #3056). China announced counter-sanctions, or said it would, after the 2015, 2019, 2020, 2022 and 2025 sales; after the 2001, 2008, 2010 and 2017 sales it answered with protests and, in 2008 and 2010, suspended military exchanges.",
    "F": "Signals US support for Taiwan's leaders: the Lee Teng-hui visa in 1995, the Trump-Tsai call in 2016, the Azar and Krach visits in 2020, Pelosi in 2022, Tsai-McCarthy in 2023 and Lai's New York stop in 2023 (#3500, #3545, #3012, #3017, #3025, #3031, #3037).",
    "G": "Shows allied cooperation. The log has one case, the first multilateral maritime activity on Apr 7, 2024 (#3040).",
    "H": "The 2 counted cases are the Nov 2011 announcement of US troops for northern Australia (#3530) and the Nov 2013 B-52 flight through China's new air defense zone (#3532).",
}
HARMS = {
    "A": "Chinese drills and coast-guard confrontations went on with no US move (for example #3042, #3043 and #3044 in 2024). Whether holding back changes what China does cannot be measured from this log.",
    "B": "Talks have not stopped pressure around them. Chinese live-fire drills and a coast-guard water-cannon confrontation were logged on Jul 23, 2026, a day after the Rubio-Wang Yi talks (#3061, #3062, #3063); nothing links them to the talks. The political cost of talking is not measured.",
    "C": "China's answer to the Oct 2022 chip controls in the log was words: its foreign ministry criticised them and no counter-measure was reported (#3030, AP). Harm to ordinary people from export controls is not measured.",
    "D": "Close encounters at sea can turn dangerous: the Chinese destroyer Lanzhou came within about 45 yards of the Decatur on Sep 30, 2018 (#3562, #3563), and another destroyer crossed the Chung-Hoon's bow at about 150 yards on Jun 3, 2023 (#3033, #3034). Most other transits drew a protest and shadowing.",
    "E": "China announced counter-sanctions, or said it would, within 14 days of 5 of the 9 counted sales, and within 7 days of 3 (#3539, #3007, #3019). The vow after the Dec 2015 sale named no firm. After the Dec 2025 sale it also held the Justice Mission 2025 drills 11 days later, which USNI says protested the sales (#3057, #3058).",
    "F": "Visits drew the strongest answers in the log: drills in six zones after the Pelosi visit (#3026), drills around Taiwan after Tsai-McCarthy (#3032) and after Lai's stopovers (#3038). 5 of the 7 counted cases drew a Chinese military action within 7 days; the 1995 visa (#3500) and the Dec 2016 call (#3545) did not, although the 1995 missile tests came 60 days after the visa (#3501, #3502).",
    "G": "One case, so no rate. The PLA announced combat patrols the same day as the first allied activity (#3040, #3041).",
    "H": "China patrolled its air defense zone four days after the B-52 flight (#3532, #3533); the report ties the patrol to the zone, not to the flight. The Australia announcement drew words only (#3530).",
}
UNKNOWNS = {
    "A": "No hold weeks are built, so nothing here measures what China does when the US does nothing.",
    "B": "21 counted cases, and no Chinese drill or counter-sanction was found within 7 days of any. Most 1995-2011 rows rest on a CRS chronology or an official archive page, and 1997-2000 and 2002-2007 are thinly logged. Leader contact the log does not hold (a Trump-Xi meeting on Oct 30, 2025 was searched for and not found in an allowed outlet) would lower the political number.",
    "C": "Only 2 counted cases (#3561, #3030). The Aug 2020 Entity List round (#3014) is unclear: whether a Chinese missile launch the same day was a reply is not settled.",
    "D": "9 other transits and FONOPs are not counted: known only from a list or a report with no Chinese reaction read, or unclear (#3002, #3003, #3004, #3016, #3028, #3054, #3541, #3542, #3564). Most 2022-2023 FONOPs and many 2016-2018 operations (for example the Jan 2018 Hopper FONOP) are missing from the log.",
    "E": "7 more US moves are not counted (#3029, #3036, #3045, #3506, #3519, #3521, #3529): the reply window was unclear or not searched. China's Dec 5, 2024 counter-sanctions on 13 firms were reported only by an outlet that is not allowed, so they are not counted.",
    "F": "Lai's Nov-Dec 2024 transit (#3046) is unclear: Taiwan's defense ministry reported the largest Chinese maritime movements on day 10, outside the 7-day window. The Jan 2021 lifting of contact limits (#3022) and the Mar 2018 Taiwan Travel Act (#3552) were not searched for a reaction.",
    "G": "One case; no rate can be read.",
    "H": "Two cases, so no rate can be read. The two-carrier operations of Jul 2020 (#3011) and the carrier groups sent toward Taiwan in Mar 1996 (#3505) are unclear, so they are not counted.",
}
