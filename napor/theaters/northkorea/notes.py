"""North Korea: analyst notes (judgement, not data; the page labels every line that way). Facts cite event IDs from events.py."""

PROS = {
    "A": "Adds no new US act for North Korea to answer. In the log, hold weeks since Jan 2025 were followed by a North Korean launch in only 2 of 69 weeks (#2055, #2063), but the log is a sample, so that is a floor, not a rate.",
    "B": "No direct casualties. After the Singapore summit (#2005) and the DMZ meeting (#2011) no North Korean launch is logged within 7 days, and Trump has repeated the offer to meet Kim (#2056, #2069).",
    "C": "Financial pressure with no direct casualties and no risk to US forces. Treasury rounds are logged in Feb 2018, Mar 2019, Jan 2022, Nov 2025 and Mar 2026 (#2004, #2007, #2016, #2060, #2066).",
    "D": "Keeps the allied forces practiced. The log has Freedom Shield, Ulchi Freedom Shield and the trilateral Freedom Edge (#2033, #2043, #2052, #2064, #2068, #2071), and two rounds were scaled down when talks were in the air (#2012, #2068).",
    "E": "Cuts off a source of money without a military clash: the log has the seizure of the coal ship Wise Honest (#2010) and the tanker Courageous (#2015).",
    "F": "Adds warning time against launches: the trilateral missile-warning data link went live on Dec 19, 2023 (#2037).",
    "G": "Shows allied strength without moving ground forces. The log has bombers, carriers and submarines (#2001, #2021, #2030, #2041, #2048, #2050, #2061).",
    "H": "No direct harm. Summit pledges and defense-chief visits tie the allies together (#2019, #2032, #2058).",
}
HARMS = {
    "A": "Launches and provocations went on without a new US move (for example #2063 on Jan 4, 2026). Whether holding back changes what North Korea does cannot be measured from this log.",
    "B": "Talks have not ended launches. The Hanoi summit ended without a deal (#2006) and launches came back on May 4, 2019 (#2008). Trump's Aug 19, 2026 offer (#2069) was followed the next day by about 10 short-range missiles (#2070). The political cost of meeting Kim is not measured.",
    "C": "North Korea replied to 3 of 4 counted sanctions rounds within 7 days, and AP reports a North Korean statement tying the Jan 2022 launch to the sanctions (#2016, #2017). Harm to ordinary North Koreans from sanctions is not measured.",
    "D": "North Korea warned that the drills could derail diplomacy (#2012) and launched or provoked within 7 days after all 7 counted rounds. Several rounds fell in the same weeks as other US moves, so \"after\" is not \"because of\".",
    "E": "Only 1 counted case, and the Justice Department announced the Wise Honest seizure hours after a North Korean launch (#2009, #2010). Enforcement is under-logged: the log has many more Treasury rounds than seizures.",
    "F": "No counted case, so no measured outcome. The data-sharing announcement (#2037) came a day after an ICBM launch (#2036), so it is a US reply to North Korea rather than a trigger.",
    "G": "North Korea launched or issued a threat after all 7 counted deployments, within 2 days in 5 of them. Its defense ministry called the Feb 2025 submarine visit \"hysteria for confrontation\" (#2049) and Kim Yo Jong warned the allies not to test its will (#2051). Both are North Korean claims reported by allowed outlets.",
    "H": "Pledges and visits (#2019, #2032, #2058) were followed by a launch or artillery fire within 7 days in all 3 counted cases, but each fell in a week with other US moves.",
}
UNKNOWNS = {
    "A": "The log is a sample. Three weeks inside the hold period are marked uncertain because an allowed outlet reports a US drill the log does not hold, and a hold week followed by an unlogged North Korean launch is counted as quiet. Whether holding back changes launches is not in the data.",
    "B": "Only 4 counted cases. North Korea's own view of an offer reaches NAPOR only through statements (claims) reported by allowed outlets.",
    "C": "The log holds 5 of many Treasury rounds, so 4 counted cases is a thin sample. Rounds often come within days of other US moves, so a launch cannot be pinned on one of them.",
    "D": "Drill rounds inside the Sep-Nov 2022 dense-launch stretch are left out as unclear (#2023, #2026). Whether North Korea launches in drill weeks anyway is not separated from a reply.",
    "E": "Only 1 counted case. The other seizure (#2015) was not checked for a North Korean act within 7 days.",
    "F": "No counted case. The reported move of THAAD parts out of Korea in Mar 2026 (#2065) could not be confirmed and is not counted; the data-sharing row (#2037) was not checked for a reply.",
    "G": "Most deployments came with joint drills or other US moves in the same week, so their effects cannot be separated. Two (#2038, #2054) were not checked for a North Korean act.",
    "H": "Only 3 counted cases; one more (#2029) was not checked for a reply.",
}
