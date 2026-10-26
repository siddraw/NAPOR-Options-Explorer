"""NAPOR North Korea: the US/allied-move and DPRK-reply record, Aug 2017 - Oct 12, 2026 (research file, W5).

Same shape as napor/prewar.py and napor/theaters/houthis/events_early.py. Event IDs and pair IDs
2001-2999 belong to this file (2001-2076 used).

Option letters used for US (and US-allied) moves, tagged in US_OPTION. A (hold) is not tagged.
  B  Talks / summit offers or meetings
  C  Sanctions / designations
  D  US-ROK / US-ROK-Japan joint drills
  E  Interdiction and enforcement of ship-to-ship transfers and sanctions-busting ships (seizures)
  F  Missile-defense moves (THAAD, trilateral missile-warning data sharing)
  G  Strategic-asset deployments (bombers, carriers, nuclear-powered submarine visits)
  H  Other force-posture or alliance-posture changes (summit pledges, defense-chief visits)
These letters follow the W5 research brief. docs/round_plan.md (wave 3, W5) lists E and G the other way
round (E strategic asset, G interdiction); the organizer should pick one before config.py is written.

Source rules (docs/SOURCE_STANDARD.md):
- Only allowed outlets and official statements (Treasury/OFAC, White House, INDOPACOM, Japan MoD).
  A wire story read on a syndicated page is labelled "AP (via ...)". seen="full text" means the page was
  read; seen="snippet" means only the search-result headline was seen.
- KCNA / Rodong Sinmun pages were NOT opened. What North Korea says is reached through an allowed outlet
  and written as "North Korea CLAIMS". If a KCNA page is added later its outlet string must be
  "KCNA (North Korean claim)" (claim-only, scored 0.30).
- DPRK launches are dated by South Korea's Joint Chiefs of Staff or Japan's Ministry of Defense as reported
  by the cited outlet. Where the cited page did not give the JCS/Japan date, the row is in PARTLY and
  the detail says how the date was set. Nuclear test 2002 is dated by Seoul/USGS (AP), not JCS.
- Statements that threaten action (2045, 2049, 2051) are logged as replies of kind "statement". They are
  facts about what was said, confirmed by the allowed outlet; the content is a North Korean claim.

Thin or open spots (the organizer should read these):
- Only 2 interdiction moves (E) and 5 sanctions moves (C) were confirmed. Many more Treasury rounds exist.
- Census "N" rows (2005, 2006, 2007, 2010, 2011) rest on AP/PBS context that the next DPRK launch came
  weeks later (first launch of 2019 on May 4, 2019, then May 9, then Jul 25). No full launch list was
  pulled for those windows. "Unverified" means the 7-day window was not searched at all.
- 2020 and most of 2021 are empty: no sourced event was found in the time available (the Jun 16, 2020
  liaison-office demolition page could not be fetched). Many launches in 2022-2026 are also missing
  (Jan 2022 had 7 launches; only the Jan 14 one is here). The log is a sample, not a full launch list.
- Jan 27, 2026 launch and Apr 19, 2026 launches were found only on outlets that are not allowed, so they are left out.
- Aug 2026 Ulchi Freedom Shield: PBS (AP) says the 11-day drill began Aug 17 and was cut about in half; AP via KLTV
  says it ended Aug 27, six days early. The two do not fit; the row uses the start date only.
- Dates inferred from a weekday are marked in the row detail and listed in PARTLY.
"""
import datetime as dt


def d(y, m, day):
    return dt.date(y, m, day)


def _s(headline, outlet, published, url, seen="snippet"):
    return {'headline': headline, 'outlet': outlet, 'published': published, 'seen': seen, 'url': url}


# Columns: ID, Date, Actor, Action Type, Target, Detail, Trigger ID, Severity, Confidence, Source
EVENTS = [
(2001, d(2017,8,31), "US (with South Korea)", "Force posture (strategic bombers, show of force)", "Korean Peninsula", "US B-1B bombers and F-35 stealth fighters fly over South Korea in a show of force, three days before the sixth nuclear test (AP gives 'the Thursday before the test'; Aug 31). North Korea strongly protested", None, "n/a", "Medium", "see audit"),
(2002, d(2017,9,3), "North Korea (per Seoul and USGS)", "Nuclear test (sixth)", "Punggye-ri test site", "Sixth nuclear test at 12:29 p.m. local time; Seoul puts the quake at magnitude 5.7 and USGS at 6.3. North Korea CLAIMS a hydrogen bomb of 'tens to hundreds of kilotons'. Dated by AP from Seoul and USGS, not by the JCS", 2001, "No injuries reported; yield disputed", "Medium", "see audit"),
(2003, d(2017,11,28), "North Korea (per Pentagon and JCS)", "Missile launch (ICBM, Hwasong-15)", "Sea off Japan's EEZ", "A new ICBM launched about 3:17 a.m. local time; the Pentagon's first read is an ICBM that splashed down in Japan's EEZ; the JCS confirmed the launch. First launch in about 2.5 months", None, "No damage", "Medium", "see audit"),
(2004, d(2018,2,23), "US (Treasury)", "Sanction (shipping network)", "North Korean and third-country shipping firms", "Treasury (OFAC) announces its 'largest North Korean sanctions package': 1 person, 27 entities and 28 vessels tied to coal exports and ship-to-ship transfers of refined petroleum", None, "n/a", "Medium", "see audit"),
(2005, d(2018,6,12), "US (Trump) and North Korea (Kim)", "Diplomatic talks (summit, Singapore)", "North Korea", "First US-DPRK leaders' summit on Sentosa Island, Singapore; joint statement commits both sides to new relations, a peace regime, work toward denuclearization and POW/MIA remains", None, "n/a", "Medium", "see audit"),
(2006, d(2019,2,28), "US (Trump) and North Korea (Kim)", "Diplomatic talks (summit, Hanoi, ended without a deal)", "North Korea", "Second Trump-Kim summit in Hanoi ends early with no deal; Trump says Kim wanted all sanctions lifted first and the US could not do that", None, "n/a", "Medium", "see audit"),
(2007, d(2019,3,21), "US (Treasury)", "Sanction (two shipping firms)", "Dalian Haibo International Freight, Liaoning Danxing International Forwarding", "Treasury designates two China-based shipping companies for helping North Korea evade sanctions, and updates a shipping advisory adding dozens of vessels suspected of ship-to-ship transfers or coal exports. (Trump said the next day he was withdrawing 'additional' sanctions; the press coverage that reports it was not read, so only the designation is logged)", None, "n/a", "Medium", "see audit"),
(2008, d(2019,5,4), "North Korea (per JCS)", "Missile launch (several projectiles)", "Sea off North Korea's east coast", "The JCS reports several projectiles flying up to about 125 miles; not yet confirmed as banned ballistic missiles. Amid stalled US-DPRK talks after the failed Hanoi summit", None, "No damage", "Medium", "see audit"),
(2009, d(2019,5,9), "North Korea (per JCS)", "Missile launch (two short-range missiles)", "Sea off North Korea's east coast", "Two suspected short-range missiles from Sino-ri and Kusong flew 260 and 167 miles, per the JCS", None, "No damage", "Medium", "see audit"),
(2010, d(2019,5,9), "US (Justice Department)", "Seizure (North Korean coal ship, Wise Honest)", "Wise Honest (North Korean bulk carrier)", "The Justice Department announces the US has seized the Wise Honest for illegally shipping North Korean coal and delivering heavy machinery to the North. The announcement came hours after the DPRK launch (2009); the ship itself had been held since 2018, so the timing is not a US reply", None, "n/a", "Medium", "see audit"),
(2011, d(2019,6,30), "US (Trump) and North Korea (Kim)", "Diplomatic talks (DMZ meeting)", "North Korea", "Trump and Kim shake hands at the DMZ in Panmunjom; Trump steps across, the first sitting US president in North Korea; 50-minute meeting; Trump says talks will restart in a few weeks", None, "n/a", "Medium", "see audit"),
(2012, d(2019,8,5), "US and South Korea", "Joint drills (scaled-down exercises begin)", "Korean Peninsula", "The US and South Korea begin scaled-down joint exercises; North Korea had warned the drills could derail nuclear diplomacy", None, "n/a", "Medium", "see audit"),
(2013, d(2019,8,6), "North Korea (per JCS)", "Missile launch (unidentified projectiles, twice)", "Sea off North Korea's east coast", "The JCS says North Korea fired unidentified projectiles twice from near its west coast across the country into eastern waters, a day after the drills began. AP's text says 'Tuesday' (Aug 6) while the page is dated Aug 5 (US time); logged Aug 6 Korea time. Followed a Jul 25 short-range ballistic launch and two rocket-artillery tests", 2012, "No damage", "Medium", "see audit"),
(2014, d(2021,3,21), "North Korea (per JCS and US officials)", "Missile launch (two cruise missiles)", "Sea off North Korea's west coast", "Two cruise missiles fired Sunday (Mar 21), per the JCS ('cruise missiles, not ballistic'); US officials call them short-range and not covered by UN bans. Biden: 'nothing much has changed'", None, "No damage", "Medium", "see audit"),
(2015, d(2021,7,30), "US (Justice Department)", "Seizure (oil tanker, M/T Courageous)", "Singapore-owned tanker in Cambodia", "The Justice Department announces forfeiture/seizure of the M/T Courageous, which satellite imagery showed transferring over $1.5 million of oil to a North Korean ship in 2019 (announced Friday, Jul 30)", None, "n/a", "Medium", "see audit"),
(2016, d(2022,1,12), "US (Treasury and State)", "Sanction (missile procurement agents)", "Five North Koreans (one in Russia, four in China) and others", "Treasury sanctions five North Korean nationals tied to weapons procurement, citing six ballistic missile launches since September 2021; State sanctions three more people and a Russian entity. Biden's first DPRK sanctions over the weapons programs", None, "n/a", "Medium", "see audit"),
(2017, d(2022,1,14), "North Korea (per JCS)", "Missile launch (two short-range ballistic missiles)", "Sea off North Korea's east coast", "Two SRBMs fired about 11 minutes apart from North Pyongan, flying about 430 km, the third launch that month. Hours before, North Korea CLAIMS (via its state media, as AP reports) the US sanctions show a 'confrontational stance' and warned of stronger action", 2016, "No damage", "Medium", "see audit"),
(2018, d(2022,3,24), "North Korea (per Seoul and Tokyo)", "Missile launch (ICBM, Hwasong-17)", "Sea off Japan", "North Korea fires an ICBM, its first since 2017, detected by the South Korean and Japanese militaries; state media reported it the next day. The US then announced new sanctions on five entities and people in Russia and North Korea (State spokesperson; exact date not given by AP)", None, "No damage", "Medium", "see audit"),
(2019, d(2022,5,21), "US (Biden) and South Korea (Yoon)", "Force posture (summit pledge on extended deterrence)", "Korean Peninsula", "At the Seoul summit Biden affirms 'extended deterrence' using nuclear, conventional and missile-defense capabilities and says the allies may expand the scale of joint exercises", None, "n/a", "Medium", "see audit"),
(2020, d(2022,5,25), "North Korea (per JCS)", "Missile launch (suspected ICBM and two SRBMs)", "Sea off North Korea's east coast", "Three missiles from Sunan hours after Biden ended his Asia trip: a suspected ICBM (about 360 km, 540 km apogee), one that failed after 20 km, and an SRBM (760 km). The US and South Korea fired two missiles in reply", 2019, "No damage", "Medium", "see audit"),
(2021, d(2022,9,23), "US", "Force posture (carrier strike group visits Busan)", "USS Ronald Reagan, Busan", "The USS Ronald Reagan carrier strike group arrives in Busan for joint exercises with South Korea; the launch (2022) came as it arrived", None, "n/a", "Medium", "see audit"),
(2022, d(2022,9,25), "North Korea (per JCS)", "Missile launch (short-range ballistic missile)", "Sea off North Korea's east coast", "An SRBM from Taechon flies about 600 km, apogee 60 km, per the JCS; it came as the Reagan arrived. Stripes: the 18th round of missile tests that year, a record. Start of the Sep 25 - Nov 2, 2022 dense-launch window", 2021, "No damage", "Medium", "see audit"),
(2023, d(2022,9,26), "US and South Korea", "Joint drills (four-day naval exercise)", "East Sea", "Combined naval exercise with the Reagan strike group, destroyers and a cruiser plus 20+ ships from both navies, anti-surface warfare focus, four days from Sep 26", None, "n/a", "Medium", "see audit"),
(2024, d(2022,9,28), "North Korea (per JCS and Japan)", "Missile launch (two short-range ballistic missiles)", "Sea off North Korea's east coast", "Two SRBMs from the Sunan area of Pyongyang flew about 360 km; JCS reported them between 18:10 and 18:20 local time; Japan's coast guard confirmed citing the defense ministry. Day before Vice President Harris arrived in Seoul", 2023, "No damage", "Medium", "see audit"),
(2025, d(2022,10,4), "North Korea (per Japan MoD)", "Missile launch (over Japan)", "Overflight of Japan (Aomori, Hokkaido)", "Japan's Defense Ministry says a ballistic missile was launched at 7:22 a.m. and passed over Japan at 7:29 a.m.; residents told to take cover. The ABC page shows Oct 4 and its metadata Oct 3 (UTC); logged Oct 4 Japan time", None, "No damage reported", "Medium", "see audit"),
(2026, d(2022,10,31), "US and South Korea", "Joint drills (large air exercise, Vigilant Storm)", "Korean Peninsula", "An annual South Korea-US air exercise begins, 240 aircraft and about 1,600 planned sorties (AFP-credited page says it 'began two days earlier' than Nov 2; the name Vigilant Storm is not on the page)", None, "n/a", "Medium", "see audit"),
(2027, d(2022,11,2), "North Korea (per South Korea's military)", "Missile launch (23 missiles in one day)", "Seas east and west of the peninsula", "At least 23 missiles, one landing about 100 miles from a South Korean island and triggering air-raid sirens there; the most in a single day", 2026, "No damage", "Medium", "see audit"),
(2028, d(2022,12,26), "North Korea (per JCS)", "Provocation (five drones cross the border)", "South Korean airspace, Seoul region", "Five North Korean drones cross into the South; one reaches the northern Seoul area; South Korea scrambles jets and fires warning shots. First drone incursion since 2017", None, "No injuries", "Medium", "see audit"),
(2029, d(2023,4,26), "US (Biden) and South Korea (Yoon)", "Force posture (Washington Declaration)", "Korean Peninsula", "The leaders create a nuclear consultative group and the US says it will deploy a ballistic-missile submarine to the western Pacific for the first time since the 1980s; the US will not redeploy tactical nuclear weapons to South Korea", None, "n/a", "Medium", "see audit"),
(2030, d(2023,7,18), "US", "Force posture (ballistic missile submarine visit)", "USS Kentucky, Busan", "The USS Kentucky docks at Busan, the first visit by a US ballistic missile submarine in about 42 years, on the day of the first Nuclear Consultative Group meeting. North Korea had warned against it as 'nuclear blackmail'", None, "n/a", "Medium", "see audit"),
(2031, d(2023,7,19), "North Korea (per JCS and Japan)", "Missile launch (two ballistic missiles)", "Sea off North Korea's east coast", "Two ballistic missiles early Wednesday (Jul 19 Korea time, hours after the Kentucky arrived): Japan says ranges of 550 and 600 km, 50 km apogee, outside Japan's EEZ. The launch followed a Hwasong-18 ICBM test nearly a week earlier", 2030, "No damage", "Medium", "see audit"),
(2032, d(2023,8,18), "US, Japan, South Korea", "Force posture (Camp David summit)", "Indo-Pacific", "The US, Japan and South Korea open a summit at Camp David to bolster trilateral security (read from a search-result headline/snippet only)", None, "n/a", "Medium", "see audit"),
(2033, d(2023,8,21), "US and South Korea", "Joint drills (Ulchi Freedom Shield begins)", "Korean Peninsula", "The 11-day annual US-South Korea exercise starts (start date taken from NPR: the Aug 24 launch came 'three days after' the start); North Korea's state media said the drills raise the risk of nuclear war", None, "n/a", "Medium", "see audit"),
(2034, d(2023,8,24), "North Korea (per JCS and Japan)", "Missile launch (satellite attempt, failed)", "Over the Yellow Sea and past Okinawa", "A rocket launched at 3:50 a.m. from Tongchang-ri; Japan issues a J-Alert as it flies over Okinawa; the JCS detects it; North Korea says the satellite attempt failed. Date taken from NPR's 'Thursday' and the exercise start", 2033, "No damage", "Medium", "see audit"),
(2035, d(2023,11,21), "North Korea (per JCS and Japan MoD)", "Missile launch (satellite rocket)", "Sohae launch site", "A satellite rocket is launched at 10:42 p.m.; the JCS says US, South Korean and Japanese Aegis ships tracked it; Japan's MoD says the rocket separated and fell outside its EEZ. USNI wrote it up Nov 22", None, "No damage", "Medium", "see audit"),
(2036, d(2023,12,18), "North Korea (per JCS)", "Missile launch (ICBM, Hwasong-18)", "Sea off North Korea's east coast", "An ICBM launch on a Monday; AP gives only the weekday, so Dec 18 is inferred from the Wednesday, Dec 20 drill. Preceded the trilateral bomber drill", None, "No damage", "Medium", "see audit"),
(2037, d(2023,12,19), "US, Japan, South Korea", "Missile defense (real-time missile-warning data sharing live)", "North Korean missile warnings", "The three defense chiefs say they have fully activated a real-time North Korea missile-warning system and will start a multi-year trilateral exercise plan in early 2024", None, "n/a", "Medium", "see audit"),
(2038, d(2023,12,20), "US, South Korea, Japan", "Force posture (B-1B bomber joins trilateral air drill)", "Off Jeju", "A US B-1B joins a trilateral air drill with South Korea and Japan, announced by the JCS two days after the ICBM", 2036, "n/a", "Medium", "see audit"),
(2039, d(2024,1,14), "North Korea (per JCS)", "Missile launch (solid-fuel IRBM with hypersonic warhead)", "Waters between the peninsula and Japan", "The JCS says the missile flew about 1,000 km; North Korea CLAIMS a successful solid-fuel hypersonic test", None, "No damage", "Medium", "see audit"),
(2040, d(2024,5,27), "North Korea (per South Korea's defense ministry and JCS)", "Missile launch (satellite rocket, failed)", "Yellow Sea", "A satellite rocket explodes about two minutes after liftoff (10:46 p.m.); the JCS says US, South Korean and Japanese Aegis destroyers were collecting launch data. Fourth satellite attempt in 12 months", None, "Debris over the Yellow Sea; no injuries", "Medium", "see audit"),
(2041, d(2024,6,22), "US", "Force posture (carrier strike group visits Busan)", "USS Theodore Roosevelt, Busan", "The USS Theodore Roosevelt carrier strike group arrives in Busan ahead of the first Freedom Edge exercise", None, "n/a", "Medium", "see audit"),
(2042, d(2024,6,26), "North Korea (per JCS)", "Missile launch (failed; claimed multiple-warhead test)", "East Sea", "The JCS says a missile launched at 5:30 a.m. from near Pyongyang exploded after about 155 miles and calls it a failed launch; North Korea CLAIMS a successful test of multiple warheads", 2041, "No damage", "Medium", "see audit"),
(2043, d(2024,6,27), "US, South Korea, Japan", "Joint drills (first Freedom Edge exercise)", "South of Jeju", "The first trilateral Freedom Edge exercise begins with the Theodore Roosevelt strike group, destroyers and a P-8", None, "n/a", "Medium", "see audit"),
(2044, d(2024,7,1), "North Korea (per JCS)", "Missile launch (two ballistic missiles)", "Northeast of Jangyon", "Two missiles launched 10 minutes apart; the first flew about 600 km, the second about 120 km and may have exploded. A day earlier North Korea CLAIMED it would respond with 'offensive and overwhelming' action to the drills. First launch in five days", 2043, "No damage", "Medium", "see audit"),
(2045, d(2024,10,10), "North Korea (Foreign Ministry and army, per Al Jazeera)", "Provocation (statement threatening action over drones)", "South Korea", "North Korea CLAIMS South Korean drones dropped leaflets over Pyongyang on Oct 3, 9 and 10 and says its forces are preparing 'all means of attack' and 'the safety lock on our trigger has now been released'. South Korea's defense minister said 'we have not done that'; the JCS could not confirm. The statements were made; the drone claim is unverified", None, "No injuries", "Medium", "see audit"),
(2046, d(2024,10,31), "North Korea (per South Korean military)", "Missile launch (ICBM, Hwasong-19)", "East Sea", "North Korea's longest-flying ICBM test so far (higher and longer than any earlier launch); South Korea's military says it may be solid-fuel. A military spokesperson (not the JCS by name) spoke", None, "No damage", "Medium", "see audit"),
(2047, d(2025,1,6), "North Korea (per JCS)", "Missile launch (hypersonic IRBM)", "Waters between the peninsula and Japan", "The JCS says the missile flew about 1,100 km while Secretary of State Blinken was in Seoul; North Korea CLAIMS 1,500 km, 12 times the speed of sound", None, "No damage", "Medium", "see audit"),
(2048, d(2025,2,10), "US", "Force posture (nuclear-powered attack submarine visit)", "USS Alexandria (SSN 757), Busan", "The USS Alexandria docks at Busan for resupply and crew rest, per South Korea's defense ministry", None, "n/a", "Medium", "see audit"),
(2049, d(2025,2,11), "North Korea (defense ministry, per KCNA via Al Jazeera)", "Provocation (statement threatening to punish)", "United States", "North Korea CLAIMS (KCNA) the submarine's presence is a 'clear expression of the US invariable hysteria for confrontation' and vows to punish 'provokers' (the quote's spelling in Al Jazeera)", 2048, "n/a", "Medium", "see audit"),
(2050, d(2025,3,2), "US", "Force posture (carrier strike group visits Busan)", "USS Carl Vinson, Busan", "The USS Carl Vinson carrier strike group makes a port call at Busan, the first carrier visit to a foreign port in Trump's second term", None, "n/a", "Medium", "see audit"),
(2051, d(2025,3,4), "North Korea (Kim Yo Jong, per KCNA via Stars and Stripes)", "Provocation (statement threatening action)", "United States, South Korea", "North Korea CLAIMS (Kim Yo Jong, KCNA) the carrier visit is 'aggravating the situation', says Washington and Seoul 'should not test the will and ability' of North Korea and that it will examine options that threaten 'the security of the enemy'", 2050, "n/a", "Medium", "see audit"),
(2052, d(2025,3,10), "US and South Korea", "Joint drills (Freedom Shield begins)", "Korean Peninsula", "The annual command-post exercise begins, the first big combined training of Trump's second term; North Korea warned of possible 'physical conflict'", None, "n/a", "Medium", "see audit"),
(2053, d(2025,3,10), "North Korea (per JCS)", "Missile launch (several close-range ballistic missiles)", "Sea from Hwanghae province", "The JCS reports several close-range ballistic missiles on the day the drills began, the fifth missile launch event that year", 2052, "No damage", "Medium", "see audit"),
(2054, d(2025,4,15), "US and South Korea", "Force posture (B-1B bomber drill)", "Korean Peninsula", "A US long-range B-1B joins a drill with South Korea as the North marks a key state anniversary; South Korea's defense ministry issued the statement (not the JCS)", None, "n/a", "Medium", "see audit"),
(2055, d(2025,10,22), "North Korea (per JCS)", "Missile launch (multiple short-range ballistic missiles)", "Northeast from south of Pyongyang", "Several SRBMs flew about 350 km; AP says they did not land in the sea. The launch came days before Trump's Asia trip and the APEC meetings", None, "No damage", "Medium", "see audit"),
(2056, d(2025,10,28), "US (Trump)", "Diplomatic talks (offer to meet Kim)", "North Korea", "Trump, visiting South Korea, repeats he wants to meet Kim, would extend his trip if a chance arose, and suggests sanctions relief could be discussed; North Korea had not responded directly (AP)", None, "n/a", "Medium", "see audit"),
(2057, d(2025,10,28), "North Korea (claim; JCS said it was analyzing)", "Missile launch (sea-to-surface cruise missiles, claimed)", "North Korea's western waters", "North Korea CLAIMS cruise missiles fired Tuesday flew for more than two hours; the JCS said only that it and the US were analyzing the weapons. Not confirmed with a JCS date or type", None, "n/a", "Medium", "see audit"),
(2058, d(2025,11,3), "US (Hegseth)", "Force posture (defense secretary visits the DMZ)", "DMZ / Joint Security Area", "Defense Secretary Hegseth and the South Korean defense minister visit the DMZ during Hegseth's Indo-Pacific trip; he later vows to carry out Trump's nuclear-submarine pledge to Seoul", None, "n/a", "Medium", "see audit"),
(2059, d(2025,11,3), "North Korea (per South Korea's military, as Al Jazeera mentions)", "Provocation (about 10 rounds of artillery into western waters)", "Waters off North Korea's west coast", "Al Jazeera refers to North Korea firing 10 rounds of artillery into its western waters four days before the Nov 7 launch (the artillery page itself was not read). Date inferred from 'four days before'", None, "No damage", "Medium", "see audit"),
(2060, d(2025,11,4), "US (Treasury)", "Sanction (bankers and IT-worker financing)", "Eight North Korean bankers and representatives, KMCTC, Ryujong Credit Bank", "OFAC sanctions 8 people and 2 entities for laundering cybercrime proceeds and IT-worker money; First Credit Bank's crypto addresses added", None, "n/a", "Medium", "see audit"),
(2061, d(2025,11,5), "US", "Force posture (carrier strike group visits Busan)", "USS George Washington, Busan", "The USS George Washington carrier strike group pulls into Busan for a five-day stay", None, "n/a", "Medium", "see audit"),
(2062, d(2025,11,7), "North Korea (per JCS and Japan MoD)", "Missile launch (short-range ballistic missile)", "From Daegwan, North Pyongan", "One SRBM at 12:35 p.m.; South Korea says 700 km, Japan's MoD about 50 km altitude and 450+ km. The sixth ballistic launch of 2025. The same day North Korea's defense minister CLAIMED the Hegseth DMZ visit fans 'war hysteria'", 2061, "No damage", "Medium", "see audit"),
(2063, d(2026,1,4), "North Korea (per Japan MoD)", "Missile launch (at least two ballistic missiles)", "Sea of Japan", "Japan's defense minister says at least two ballistic missiles launched at about 7:54 and 8:05 a.m., flying about 900 and 950 km (apogee 50 km), landing outside Japan's EEZ; the flight path may have been irregular", None, "No damage", "Medium", "see audit"),
(2064, d(2026,3,9), "US and South Korea", "Joint drills (Freedom Shield begins)", "Korean Peninsula", "The 11-day command-post exercise starts (through Mar 19), with the field training program Warrior Shield", None, "n/a", "Medium", "see audit"),
(2065, d(2026,3,11), "US", "Missile defense (reported move of THAAD parts to the Middle East)", "THAAD in South Korea", "South Korea's president says some US air defenses could be sent abroad because of the Iran war; the Washington Post reported THAAD parts are moving; the Pentagon declined to comment. No confirmed move found", None, "n/a", "Medium", "see audit"),
(2066, d(2026,3,12), "US (Treasury)", "Sanction (IT-worker networks)", "Six people and two entities in the DPRK, Vietnam, Laos and Spain", "OFAC sanctions DPRK government-run IT-worker schemes that Treasury says earned nearly $800 million in 2024", None, "n/a", "Medium", "see audit"),
(2067, d(2026,3,14), "North Korea (per JCS and Japan)", "Missile launch (about 10 ballistic missiles)", "From Sunan toward the East Sea", "About 10 ballistic missiles flew about 220 miles; Japan's defense minister said they landed outside its EEZ. Day 6 of Freedom Shield. Date from the Stripes page date and 'Saturday'", 2064, "No damage", "Medium", "see audit"),
(2068, d(2026,8,17), "US and South Korea", "Joint drills (Ulchi Freedom Shield begins, scaled down)", "Korean Peninsula", "Just before the exercise started on Monday, Trump ordered the Pentagon to 'substantially reduce' it, citing his relationship with Kim; PBS/AP says it was cut roughly in half. (AP via KLTV says it ended Aug 27, six days early; the two sources differ on the end date)", None, "n/a", "Medium", "see audit"),
(2069, d(2026,8,19), "US (Trump)", "Diplomatic talks (says he will meet Kim)", "North Korea", "Asked if he expects to see Kim later this year, Trump says he will; Kim Yo Jong denied any communication between the two. Date from a Wednesday report; PBS/AP carries the statement", None, "n/a", "Medium", "see audit"),
(2070, d(2026,8,20), "North Korea (per JCS)", "Missile launch (about 10 short-range ballistic missiles)", "From the capital region, about 300 km east", "About 10 SRBMs at about 5 p.m. local time, each flying about 300 km, a day before the shortened drill ended. Kim Yo Jong dismissed Trump's gesture", 2068, "No damage", "Medium", "see audit"),
(2071, d(2026,9,7), "US, South Korea, Japan", "Joint drills (Freedom Edge 26 begins)", "Waters near Jeju", "Fourth Freedom Edge since 2024: air defense, medical evacuation and maritime interdiction training with real-time data sharing. On Aug 31 North Korea's foreign ministry CLAIMED nuclear weapons are an 'absolute guarantee' and rejected denuclearization as a precondition", None, "n/a", "Medium", "see audit"),
(2072, d(2026,9,12), "North Korea (per Stars and Stripes)", "Missile launch (multiple ballistic missiles)", "East Sea", "Multiple ballistic missiles fired; North Korea later CLAIMED they were a 'joint firepower attack' drill with drones, cruise missiles, a rocket launcher and tactical ballistic missiles. Start of the Sep 12 - Oct 12, 2026 dense-launch window. Date and type come from a Sep 22 page, not the JCS release", 2071, "No damage", "Medium", "see audit"),
(2073, d(2026,9,20), "North Korea (per JCS and Japan MoD)", "Missile launch (two short-range ballistic missiles)", "East Sea", "Two SRBMs about three hours apart flew about 279 and 373 miles; Japan's Defense Ministry reported a suspected launch outside its territorial waters. North Korea CLAIMS a 'new-type weapon' and a 560+ mile path, which Seoul disputes", None, "No damage", "Medium", "see audit"),
(2074, d(2026,9,21), "North Korea (per UN Command and South Korea)", "Provocation (anti-personnel mine blasts at the DMZ)", "Western DMZ, South Korean side of the line", "Two explosions wound three South Korean soldiers; the UN Command and Seoul find a North Korean anti-personnel mine and an armistice violation. Kim Yo Jong calls the finding a 'conspiratorial farce'. North Korea denies planting the mines", None, "3 South Korean soldiers wounded", "Medium", "see audit"),
(2075, d(2026,10,3), "North Korea (per Reuters)", "Missile launch (hypersonic missile)", "Sea off North Korea's east coast", "Reuters says the last North Korean ballistic launch before Oct 12 was Oct 3; state media (KCNA) CLAIMED a hypersonic missile Kim oversaw. Date comes from the Oct 12 Reuters story, not a JCS release", None, "No damage", "Medium", "see audit"),
(2076, d(2026,10,12), "North Korea (per JCS)", "Missile launch (multiple ballistic missiles)", "From near Pyongyang toward the east coast", "Multiple missiles of different types launched about 9:20 a.m.; one flew more than 900 km; Japan's coast guard reported two projectiles that fell. The JCS called it a show of force responding to South Korea's first hypersonic test. Fourth launch in a month, 10+ tests in 2026", None, "No damage", "Medium", "see audit"),
]

# ---------------------------------------------------------------------------------------------
_ABC13 = _s('North Korea says 6th nuke test was H-bomb, "perfect success"', 'AP (via ABC13)', '2017-09-03', 'https://abc13.com/post/north-korea-says-nuke-test-was-h-bomb-perfect-success/2371055/', 'full text')
_NPR17 = _s('North Korea Apparently Fires Another Missile After 2 1/2 Month Break Between Tests', 'NPR', '2017-11-28', 'https://www.npr.org/sections/thetwo-way/2017/11/28/566994979/north-korea-apparently-fires-another-missile-after-2-1-2-month-break-between-tes', 'full text')
_DEFN17 = _s('DoD detects probable missile launch from North Korea', 'Defense News', '2017-11-28', 'https://www.defensenews.com/flashpoints/2017/11/28/dod-detects-probable-missile-launch-from-north-korea/')
_SLT_MAY4 = _s('North Korea fires several [projectiles]', 'AP (via Salt Lake Tribune)', '2019-05-03', 'https://www.sltrib.com/news/nation-world/2019/05/04/north-korea-fires-several/', 'full text')
_SLT_MAY9 = _s('North Korea fires [two suspected missiles]', 'AP (via Salt Lake Tribune)', '2019-05-09', 'https://www.sltrib.com/news/nation-world/2019/05/09/north-korea-fires/', 'full text')
_PBS_AUG19 = _s('North Korea fires projectiles twice into sea, South Korea says', 'AP (via PBS NewsHour)', '2019-08-05', 'https://www.pbs.org/newshour/amp/world/north-korea-fires-projectiles-twice-into-sea-south-korea-says', 'full text')
_AJ_MAY22 = _s('N Korea fires missiles, "including ICBM", as Biden ends Asia tour', 'Al Jazeera', '2022-05-25', 'https://www.aljazeera.com/news/2022/5/25/north-korea-fires-three-missiles-as-biden-ends-asia-visit', 'full text')
_STRIPES_SEP22 = _s('Korea naval drills, missile launch', 'Stars and Stripes', '2022-09-26', 'https://www.stripes.com/theaters/asia_pacific/2022-09-26/korea-naval-drills-missile-launch-7471043.html', 'full text')
_GPB_SEP22 = _s('North Korea fires missile as US and South Korea get ready for military exercises', 'AP (via NPR / Georgia Public Broadcasting)', '2022-09-25', 'https://www.gpb.org/news/2022/09/25/north-korea-fires-missile-us-and-south-korea-get-ready-for-military-exercises', 'full text')
_NPR_NOV22 = _s('North Korea ratchets up tensions with missile launches', 'NPR (via NPR Illinois)', '2022-11-02', 'https://www.nprillinois.org/2022-11-02/north-korea-ratchets-up-tensions-with-missile-launches', 'full text')
_BG_NOV22 = _s('North Korea launches 23 missiles, triggering air-raid alarm in South', 'Boston Globe (page credits AFP for the photo)', '2022-11-02', 'https://www.bostonglobe.com/2022/11/02/world/north-korea-launches-23-missiles-triggering-air-raid-alarm-south', 'full text')
_AJ_KENT = _s('N Korea fires 2 ballistic missiles as US sub arrives in S Korea', 'Al Jazeera', '2023-07-18', 'https://www.aljazeera.com/news/2023/7/18/n-korea-fires-2-ballistic-missiles-as-us-sub-arrives-in-s-korea', 'full text')
_NPR_AUG23 = _s('North Korea says its 2nd attempt to launch a spy satellite has failed', 'NPR', '2023-08-24', 'https://www.npr.org/2023/08/24/1195576463/north-korea-says-its-2nd-attempt-to-launch-a-spy-satellite-has-failed', 'full text')
_AFT_DEC23 = _s('US flies bombers for joint drills with South Korea, Japan', 'AP (via Air Force Times)', '2023-12-20', 'https://www.airforcetimes.com/news/your-military/2023/12/20/us-flies-bombers-for-joint-drills-with-south-korea-japan/', 'full text')
_USNI_FE24 = _s('U.S., Japan and Korea Begin Freedom Edge Exercise, North Korea Attempts Ballistic Missile Test', 'USNI News', '2024-06-27', 'https://news.usni.org/2024/06/27/u-s-japan-and-korea-begin-freedom-edge-exercise-north-korea-attempts-ballistic-missile-test', 'full text')
_AJ_FEB25 = _s('North Korea warns of retaliation after US nuclear submarine docks in Busan', 'Al Jazeera; reports a KCNA statement', '2025-02-11', 'https://www.aljazeera.com/news/2025/2/11/north-korea-warns-of-retaliation-after-us-nuclear-submarine-docks-in-busan', 'full text')
_NBCNY_MAR25 = _s('North Korea fires several ballistic missiles into sea after US, South Korea began military drills', 'AP (via NBC New York)', '2025-03-10', 'https://www.nbcnewyork.com/news/national-international/north-korea-fires-several-ballistic-missiles-into-sea-after-us-south-korea-began-military-drills/6179351/', 'full text')
_N4J_OCT25 = _s('North Korea has fired ballistic missiles toward the east, Seoul says', 'AP (via News4Jax)', '2025-10-21', 'https://www.news4jax.com/news/world/2025/10/21/north-korea-has-fired-ballistic-missiles-toward-the-east-seoul-says/', 'full text')
_N4J_OCT28 = _s("North Korea says it test fired cruise missiles ahead of Trump's visit to South Korea", 'AP (via News4Jax); reports a KCNA claim', '2025-10-28', 'https://www.news4jax.com/news/world/2025/10/28/north-korea-says-it-test-fired-cruise-missiles-ahead-of-trumps-visit-to-south-korea/', 'full text')
_USNI_NOV25 = _s('North Korea Protests Hegseth, Carrier USS George Washington Visits to South Korea', 'USNI News', '2025-11-11', 'https://news.usni.org/2025/11/11/north-korea-protests-hegseth-carrier-uss-george-washington-visits-to-south-korea', 'full text')
_AJ_NOV25 = _s('North Korea fires ballistic missile days after Hegseth visit, says Seoul', 'Al Jazeera', '2025-11-07', 'https://www.aljazeera.com/news/2025/11/7/north-korea-fires-ballistic-missile-days-after-hegseth-visit-says-seoul', 'full text')
_STRIPES_MAR26 = _s('North Korea missile launch, eastern sea', 'Stars and Stripes', '2026-03-14', 'https://www.stripes.com/theaters/asia_pacific/2026-03-14/north-korea-missile-launch-eastern-sea-21058434.html', 'full text')
_PBS_AUG26 = _s('North Korea fires barrage of missiles toward the sea after dismissing overture from Trump', 'AP (via PBS NewsHour)', '2026-08-20', 'https://www.pbs.org/newshour/world/north-korea-fires-barrage-of-missiles-toward-the-sea-after-dismissing-overture-from-trump', 'full text')
_STRIPES_SEP26B = _s('North Korea "ultra-modern" combat weapon', 'Stars and Stripes; reports a KCNA claim', '2026-09-22', 'https://www.stripes.com/theaters/asia_pacific/2026-09-22/north-korea-ultra-modern-combat-weapon-22926868.html', 'full text')
_STRIPES_SEP26A = _s('North Korea missiles Sept 20', 'Stars and Stripes', '2026-09-20', 'https://www.stripes.com/theaters/asia_pacific/2026-09-20/north-korea-missiles-sept-20-22907123.html', 'full text')
_REUTERS_OCT26 = _s('North Korea fires missiles days after South Korea\'s hypersonic test', 'Reuters (via GV Wire)', '2026-10-12', 'https://gvwire.com/2026/10/12/north-korea-fires-missiles-days-after-south-koreas-hypersonic-test/', 'full text')
_AJ_OCT26 = _s('North Korea fires multiple ballistic missiles towards the sea', 'Al Jazeera', '2026-10-12', 'https://www.aljazeera.com/amp/news/2026/10/12/north-korea-fires-multiple-ballistic-missiles-towards-the-sea')

SOURCES = {
 2001: [_ABC13],
 2002: [_ABC13],
 2003: [_NPR17, _DEFN17],
 2004: [_s('Treasury Announces Largest North Korean Sanctions Package Targeting 56 Shipping and Trading Companies and Vessels', 'Treasury/OFAC (official release)', '2018-02-23', 'https://home.treasury.gov/news/press-releases/sm0297', 'full text')],
 2005: [_s('Joint Statement of President Donald J. Trump and Chairman Kim Jong Un, Singapore Summit', 'White House (official joint statement, archived)', '2018-06-12', 'https://trumpwhitehouse.archives.gov/briefings-statements/joint-statement-president-donald-j-trump-united-states-america-chairman-kim-jong-un-democratic-peoples-republic-korea-singapore-summit', 'full text')],
 2006: [_s("Trump and Kim's second nuclear summit ends with no deal", 'NPR (via WHYY)', '2019-02-28', 'https://whyy.org/npr-story/trump-and-kims-second-nuclear-summit-ends-with-no-deal/', 'full text')],
 2007: [_s('Treasury Designates Two Shipping Companies for Attempted Evasion of North Korea Sanctions', 'Treasury/OFAC (official release)', '2019-03-21', 'https://home.treasury.gov/news/press-releases/sm632', 'full text')],
 2008: [_SLT_MAY4],
 2009: [_SLT_MAY9],
 2010: [_s('US seizes North Korean coal vessel accused of violating sanctions', 'Al Jazeera', '2019-05-09', 'https://www.aljazeera.com/amp/news/2019/5/9/us-seizes-north-korean-coal-vessel-accused-of-violating-sanctions', 'full text'),
        _s("U.S. Takes Control Of North Korean 'Sanctions-Busting' Ship", 'NPR', '2019-05-09', 'https://www.npr.org/2019/05/09/721827706/u-s-takes-control-of-north-korean-sanctions-busting-ship'),
        _s('Department of Justice announces forfeiture of North Korean cargo vessel', 'Justice Department (official release)', '2019-05-09', 'https://www.justice.gov/opa/pr/department-justice-announces-forfeiture-north-korean-cargo-vessel')],
 2011: [_s('Trump meets North Korea\'s Kim at DMZ in landmark visit', 'Al Jazeera', '2019-06-30', 'https://www.aljazeera.com/news/2019/06/30/trump-meets-north-koreas-kim-at-dmz-in-landmark-visit/', 'full text')],
 2012: [_PBS_AUG19],
 2013: [_PBS_AUG19],
 2014: [_s('North Korea tested missiles over the weekend: US, South Korea', 'Al Jazeera', '2021-03-24', 'https://www.aljazeera.com/news/2021/3/24/n-korea-test-fired-missiles-over-the-weekend-reports', 'full text')],
 2015: [_s('US seizes tanker used to evade North Korea sanctions', 'Al Jazeera', '2021-07-31', 'https://www.aljazeera.com/news/2021/7/31/us-seizes-tanker-used-to-evade-north-korea', 'full text')],
 2016: [_s('US sanctions North Koreans, citing "ballistic missile" tests', 'Al Jazeera', '2022-01-12', 'https://www.aljazeera.com/economy/2022/1/12/us-sanctions-north-koreans-citing-ballistic-missile-tests', 'full text'),
        _s('N. Korea fires fresh missiles in response to US sanctions', 'AP (via ClickOnDetroit)', '2022-01-14', 'https://www.clickondetroit.com/news/world/2022/01/14/n-korea-fires-fresh-missiles-in-response-to-us-sanctions/', 'full text')],
 2017: [_s('N. Korea fires fresh missiles in response to US sanctions', 'AP (via ClickOnDetroit)', '2022-01-14', 'https://www.clickondetroit.com/news/world/2022/01/14/n-korea-fires-fresh-missiles-in-response-to-us-sanctions/', 'full text')],
 2018: [_s('N. Korea says it test-fired biggest ICBM, US adds sanctions', 'AP (via Boston Globe)', '2022-03-25', 'https://www.bostonglobe.com/2022/03/25/world/n-korea-says-it-test-fired-biggest-icbm-us-adds-sanctions', 'full text')],
 2019: [_AJ_MAY22],
 2020: [_AJ_MAY22,
        _s('North Korea launches three missiles into the sea, including suspected ICBM', 'AP (via NPR)', '2022-05-25', 'https://www.npr.org/2022/05/25/1101137516/north-korea-launches-three-missiles-into-the-sea-including-suspected-icbm', 'full text')],
 2021: [_STRIPES_SEP22, _GPB_SEP22],
 2022: [_GPB_SEP22, _STRIPES_SEP22],
 2023: [_STRIPES_SEP22],
 2024: [_s('North Korea launches two ballistic missiles on eve of Harris trip', 'Al Jazeera', '2022-09-28', 'https://www.aljazeera.com/news/2022/9/28/south-korea-says-n-korea-launched-missile-on-eve-of-harris-visit', 'full text')],
 2025: [_s('North Korea fires apparent ballistic missile over Japan: Ministry of Defense', 'ABC News (via ABC7 New York)', '2022-10-04', 'https://abc7ny.com/north-korea-japan-ballistic-missile-ministry-of-defense/12292169/', 'full text')],
 2026: [_BG_NOV22],
 2027: [_NPR_NOV22, _BG_NOV22],
 2028: [_s('South Korean military fires warning shots, scrambles jets after North Korean drones enter its airspace', 'AP (via PBS NewsHour)', '2022-12-26', 'https://www.pbs.org/newshour/world/south-korean-military-fires-warning-shots-scrambles-jets-after-north-korean-drones-enter-its-airspace', 'full text')],
 2029: [_s('Biden says nuclear attack by North Korea would mean the end of its regime', 'NPR (via Georgia Public Broadcasting)', '2023-04-26', 'https://www.gpb.org/news/2023/04/26/biden-says-nuclear-attack-north-korea-would-mean-the-end-of-its-regime', 'full text'),
        _s('US, South Korea unveil joint declaration outlining steps to bolster deterrence', 'INDOPACOM (official release)', '2023-04-26', 'https://www.pacom.mil/Media/News/News-Articles/Article/3377077/us-south-korea-unveil-joint-declaration-outlining-steps-to-bolster-deterrence/')],
 2030: [_AJ_KENT,
        _s('Nuclear submarine visit to Busan, South Korea', 'Stars and Stripes', '2023-07-18', 'https://www.stripes.com/branches/navy/2023-07-18/nuclear-submarine-visit-busan-south-korea-10774223.html', 'full text')],
 2031: [_AJ_KENT],
 2032: [_s('US, South Korea, Japan summit starting at Camp David', 'AP (via Washington Times)', '2023-08-18', 'https://www.washingtontimes.com/news/2023/aug/18/us-south-korea-japan-summit-starting-camp-david/')],
 2033: [_NPR_AUG23],
 2034: [_NPR_AUG23],
 2035: [_s('North Korea Lauches Spy Satellite, Violating UN Security Council Resolution', 'USNI News', '2023-11-22', 'https://news.usni.org/2023/11/22/north-korea-lauches-spy-satellite-violating-un-security-council-resolution', 'full text')],
 2036: [_AFT_DEC23],
 2037: [_s('U.S., Japan, South Korea Establish North Korean Missile Warning System, Trilateral Exercises', 'USNI News', '2023-12-19', 'https://news.usni.org/2023/12/19/u-s-japan-south-korea-establish-north-korean-missile-warning-system-trilateral-exercises', 'full text')],
 2038: [_AFT_DEC23],
 2039: [_s('North Korea says it launched hypersonic warhead in latest missile test', 'AP (via NBC Boston)', '2024-01-14', 'https://www.nbcboston.com/news/national-international/north-korea-says-it-launched-hypersonic-warhead-in-latest-missile-test/3246700/', 'full text')],
 2040: [_s('North Korea satellite launch failure', 'Stars and Stripes', '2024-05-28', 'https://stripes.com/theaters/asia_pacific/2024-05-28/north-korea-satellite-launch-failure-14001920.html', 'full text')],
 2041: [_s('US aircraft carrier arrives in South Korea as a show of force against nuclear-armed North Korea', 'AP (via Local 10)', '2024-06-22', 'https://local10.com/news/world/2024/06/22/us-aircraft-carrier-arrives-in-south-korea-as-a-show-of-force-against-nuclear-armed-north-korea', 'full text'), _USNI_FE24],
 2042: [_USNI_FE24],
 2043: [_USNI_FE24],
 2044: [_s('North Korea fires two ballistic missiles, one may have fallen on land', 'Al Jazeera', '2024-07-01', 'https://www.aljazeera.com/amp/news/2024/7/1/north-korea-fires-two-ballistic-missiles-one-may-have-fallen-on-land', 'full text')],
 2045: [_s('North Korea accuses South Korea of sending propaganda drones to Pyongyang', 'Al Jazeera; reports North Korean claims', '2024-10-11', 'https://www.aljazeera.com/news/2024/10/11/north-korea-accuses-south-korea-of-sending-propaganda-drones-to-pyongyang', 'full text')],
 2046: [_s('North Korea boasts of its new long-range missile targeting the US', 'AP (via NBC New York)', '2024-11-01', 'https://www.nbcnewyork.com/news/national-international/north-korea-new-missile-reaching-us/5944098/', 'full text')],
 2047: [_s('North Korea says it tested hypersonic intermediate-range missile aimed at remote Pacific targets', 'AP (via OPB)', '2025-01-07', 'https://opb.org/article/2025/01/06/north-korea-says-it-tested-hypersonic-intermediate-range-missile-aimed-at-remote-pacific-targets', 'full text')],
 2048: [_AJ_FEB25],
 2049: [_AJ_FEB25],
 2050: [_s('USS Carl Vinson Makes South Korea Port Visit', 'USNI News', '2025-03-03', 'https://news.usni.org/2025/03/03/uss-carl-vinson-makes-south-korea-port-visit', 'full text'),
        _s("North Korea won't sit still while US carrier visits South, Kim's sister says", 'Stars and Stripes; reports a KCNA statement', '2025-03-04', 'https://80.stripes.com/stripes-today/north-korea-wont-sit-still-while-us-carrier-visits-south-kims-sister-says', 'full text')],
 2051: [_s("North Korea won't sit still while US carrier visits South, Kim's sister says", 'Stars and Stripes; reports a KCNA statement', '2025-03-04', 'https://80.stripes.com/stripes-today/north-korea-wont-sit-still-while-us-carrier-visits-south-kims-sister-says', 'full text')],
 2052: [_NBCNY_MAR25],
 2053: [_NBCNY_MAR25],
 2054: [_s('US flies long-range bomber for drill with South Korea, as the North marks a key state anniversary', 'AP (via WSLS)', '2025-04-15', 'https://www.wsls.com/news/world/2025/04/15/us-flies-long-range-bomber-for-drill-with-south-korea-as-the-north-marks-a-key-state-anniversary/', 'full text')],
 2055: [_N4J_OCT25],
 2056: [_N4J_OCT28],
 2057: [_N4J_OCT28],
 2058: [_USNI_NOV25],
 2059: [_AJ_NOV25],
 2060: [_s('Treasury Sanctions DPRK Bankers and Institutions Involved in Laundering Cybercrime Proceeds and IT Worker Funds', 'Treasury/OFAC (official release)', '2025-11-04', 'https://home.treasury.gov/news/press-releases/sb0302', 'full text')],
 2061: [_USNI_NOV25],
 2062: [_AJ_NOV25, _USNI_NOV25],
 2063: [_s('Extraordinary Press Conference by Defense Minister Koizumi, January 4, 2026', 'Japan Ministry of Defense (official press conference)', '2026-01-04', 'https://www.mod.go.jp/en/article/2026/01/aa5e30c854760e9da8444434a4ffd1c0ab2c843f.html', 'full text')],
 2064: [_STRIPES_MAR26],
 2065: [_s('Iran war may force US to shift missile defenses from South Korea, Seoul says', 'Army Times', '2026-03-11', 'https://www.armytimes.com/news/your-military/2026/03/11/iran-war-may-force-us-to-shift-missile-defenses-from-south-korea-seoul-says', 'full text')],
 2066: [_s('Treasury Sanctions Facilitators of DPRK IT Worker Fraud Targeting U.S. Businesses', 'Treasury/OFAC (official release)', '2026-03-12', 'https://home.treasury.gov/news/press-releases/sb0416', 'full text')],
 2067: [_STRIPES_MAR26],
 2068: [_PBS_AUG26],
 2069: [_PBS_AUG26],
 2070: [_PBS_AUG26],
 2071: [_s('US, South Korea, Japan hold Freedom Edge military drills this week', 'AP (via KLTV)', '2026-09-07', 'https://www.kltv.com/2026/09/07/us-south-korea-japan-hold-freedom-edge-military-drills-this-week/', 'full text')],
 2072: [_STRIPES_SEP26B],
 2073: [_STRIPES_SEP26A, _STRIPES_SEP26B],
 2074: [_s('S Korea demands apology over DMZ blasts as N Korea denies planting mines', 'Al Jazeera', '2026-09-30', 'https://www.aljazeera.com/news/2026/9/30/south-korea-demands-apology-over-dmz-blasts-as-north-denies-planting-mines', 'full text')],
 2075: [_REUTERS_OCT26],
 2076: [_REUTERS_OCT26, _AJ_OCT26],
}
VERDICT = {k: 'confirmed' for k in SOURCES}
# North Korean claims or reports of a move that an allowed outlet does not confirm.
VERDICT[2057] = 'not_confirmed'   # KCNA-claimed cruise missiles; JCS only said it was analyzing
VERDICT[2065] = 'not_confirmed'   # reported THAAD move; Pentagon declined to confirm
# Rows where an allowed outlet confirms the event but not every detail in the row (date inferred, claim, or no JCS date).
PARTLY = {2002, 2013, 2025, 2026, 2032, 2036, 2042, 2045, 2059, 2067, 2068, 2069, 2072, 2075}

# Which option letter each US move belongs to (B talks, C sanctions, D joint drills, E interdiction,
# F missile defense, G strategic assets, H other posture). A (hold) is not tagged.
US_OPTION = {
 2001: 'G', 2004: 'C', 2005: 'B', 2006: 'B', 2007: 'C', 2010: 'E', 2011: 'B', 2012: 'D',
 2015: 'E', 2016: 'C', 2019: 'H', 2021: 'G', 2023: 'D', 2026: 'D', 2029: 'H', 2030: 'G',
 2032: 'H', 2033: 'D', 2037: 'F', 2038: 'G', 2041: 'G', 2043: 'D', 2048: 'G', 2050: 'G',
 2052: 'D', 2054: 'G', 2056: 'B', 2058: 'H', 2060: 'C', 2061: 'G', 2064: 'D', 2065: 'F',
 2066: 'C', 2068: 'D', 2069: 'B', 2071: 'D',
}

# My own estimate of the engine's credibility score (full-text allowed outlet 0.80, two outlets 0.96,
# claim-only 0.30; under 0.50 is not counted; a single snippet-only source is a guess at 0.60). For the
# organizer's spot check only.
CRED_ESTIMATE = {
 2001: 0.80, 2002: 0.80, 2003: 0.96, 2004: 0.80, 2005: 0.80, 2006: 0.80, 2007: 0.80, 2008: 0.80,
 2009: 0.80, 2010: 0.96, 2011: 0.80, 2012: 0.80, 2013: 0.80, 2014: 0.80, 2015: 0.80, 2016: 0.96,
 2017: 0.80, 2018: 0.80, 2019: 0.80, 2020: 0.96, 2021: 0.96, 2022: 0.96, 2023: 0.80, 2024: 0.80,
 2025: 0.80, 2026: 0.80, 2027: 0.96, 2028: 0.80, 2029: 0.96, 2030: 0.96, 2031: 0.80, 2032: 0.60,
 2033: 0.80, 2034: 0.80, 2035: 0.80, 2036: 0.80, 2037: 0.80, 2038: 0.80, 2039: 0.80, 2040: 0.80,
 2041: 0.96, 2042: 0.80, 2043: 0.80, 2044: 0.80, 2045: 0.80, 2046: 0.80, 2047: 0.80, 2048: 0.80,
 2049: 0.80, 2050: 0.96, 2051: 0.80, 2052: 0.80, 2053: 0.80, 2054: 0.80, 2055: 0.80, 2056: 0.80,
 2057: 0.30, 2058: 0.80, 2059: 0.80, 2060: 0.80, 2061: 0.80, 2062: 0.96, 2063: 0.80, 2064: 0.80,
 2065: 0.30, 2066: 0.80, 2067: 0.80, 2068: 0.80, 2069: 0.80, 2070: 0.80, 2071: 0.80, 2072: 0.80,
 2073: 0.80, 2074: 0.80, 2075: 0.80, 2076: 0.96,
}

# Trigger Census rows: one per US move (reply window: 7 days, DPRK launch / test / provocation / threatening statement).
# Category = what the move was: Economic/Blockade (sanctions, seizures), Military/Property (drills, deployments,
# missile defense, posture), Political/Diplomatic (talks; not in W2's list, flagged for the organizer).
# Status: R-strong (North Korea itself ties the act to the move), R-weak (act within 7 days, link plausible),
# N (no DPRK act found in the 7 days), Unclear (cannot be separated), Unverified (window not searched).
# 2065 (THAAD report) is not_confirmed and has no row. Moves inside a dense-launch window (2023, 2026) are context only.
CENSUS = [
 (2001, "Military/Property", "R-weak", "B-1B and F-35 show of force Aug 31, 2017 -> sixth nuclear test Sep 3 (AP). AP does not say the test was a reply; it only says North Korea strongly protested the flight."),
 (2004, "Economic/Blockade", "Unverified", "Treasury largest shipping sanctions package, Feb 23, 2018. DPRK acts in Feb 24-Mar 2, 2018 were not searched."),
 (2005, "Political/Diplomatic", "N", "Singapore summit, Jun 12, 2018. No DPRK launch or test found in Jun 13-19, 2018; AP (May 2019) and search headlines describe the May 4, 2019 launch as the first in a long gap. No full launch list was pulled."),
 (2006, "Political/Diplomatic", "N", "Hanoi summit ends with no deal, Feb 28, 2019. Next JCS-dated launch found is May 4, 2019 (AP via Salt Lake Tribune), amid talks stalled since Hanoi. No full launch list was pulled."),
 (2007, "Economic/Blockade", "N", "Treasury shipping designations, Mar 21, 2019. Next JCS-dated launch found is May 4, 2019. No full launch list was pulled."),
 (2010, "Economic/Blockade", "N", "Wise Honest seizure announced May 9, 2019, hours after that day's launch (2009). The next launch in the sources read is Jul 25, 2019 (PBS/AP, Aug 2019). Timing of the US announcement was not a reply to the launch, nor the reverse."),
 (2011, "Political/Diplomatic", "N", "DMZ meeting Jun 30, 2019. The next launch in the sources read is Jul 25, 2019, 25 days later (PBS/AP)."),
 (2012, "Military/Property", "R-weak", "Scaled-down drills begin Aug 5, 2019 -> projectiles twice Aug 6 (JCS via AP). North Korea had warned the drills could derail diplomacy; AP does not call the launch a reply."),
 (2015, "Economic/Blockade", "Unverified", "Courageous tanker seizure announced Jul 30, 2021. DPRK acts in Jul 31-Aug 6, 2021 were not searched."),
 (2016, "Economic/Blockade", "R-strong", "US sanctions Jan 12, 2022 -> two SRBMs Jan 14 (JCS). Hours before, North Korea CLAIMED (via state media, as AP reports) the sanctions show a 'confrontational stance' and warned of stronger action."),
 (2019, "Military/Property", "R-weak", "Biden-Yoon summit pledge, May 21, 2022 -> ICBM and two SRBMs May 25, hours after Biden left Asia (JCS, Al Jazeera, AP). Link plausible; North Korea's own statement was not read."),
 (2021, "Military/Property", "R-weak", "USS Ronald Reagan arrives in Busan Sep 23, 2022 -> SRBM Sep 25 (JCS); AP says the launch came as the carrier arrived. A second launch followed Sep 28."),
 (2023, "Military/Property", "Unclear", "Combined naval drills from Sep 26, 2022, inside the Sep 25 - Nov 2, 2022 dense-launch window; two SRBMs on Sep 28 (JCS) cannot be separated from the window's pace. Context only."),
 (2026, "Military/Property", "Unclear", "Large air exercise from Oct 31, 2022, inside the dense-launch window; 23 missiles on Nov 2 (2027) cannot be separated from the window's pace. Context only."),
 (2029, "Military/Property", "Unverified", "Washington Declaration, Apr 26, 2023. NPR/GPB reports no North Korean response as of publication; Apr 27-May 3 was not searched."),
 (2030, "Military/Property", "R-weak", "USS Kentucky arrives Busan Jul 18, 2023 -> two ballistic missiles Jul 19 (JCS, Japan MoD). North Korea had warned against the visit as 'nuclear blackmail' (Stripes). An analyst quoted by Al Jazeera ties the launch to the visit."),
 (2032, "Military/Property", "R-weak", "Camp David summit Aug 18, 2023 -> failed satellite launch Aug 24 (JCS, Japan). Link weak: the launch was also 3 days into Ulchi Freedom Shield."),
 (2033, "Military/Property", "R-weak", "Ulchi Freedom Shield begins Aug 21, 2023 -> failed satellite launch Aug 24 (NPR). North Korea's state media said the drills raise the risk of nuclear war."),
 (2037, "Military/Property", "Unverified", "Missile-warning system announced Dec 19, 2023, a day after the ICBM. DPRK acts in Dec 20-26, 2023 were not searched."),
 (2038, "Military/Property", "Unverified", "B-1B joins trilateral air drill Dec 20, 2023, two days after the ICBM. DPRK acts in Dec 21-27, 2023 were not searched."),
 (2041, "Military/Property", "R-weak", "Roosevelt carrier arrives Busan Jun 22, 2024 -> failed launch Jun 26 (JCS), a day before Freedom Edge began."),
 (2043, "Military/Property", "R-strong", "Freedom Edge begins Jun 27, 2024 -> two ballistic missiles Jul 1 (JCS). A day earlier North Korea CLAIMED it would give an 'offensive and overwhelming' response to the drills (Al Jazeera)."),
 (2048, "Military/Property", "R-weak", "USS Alexandria docks Busan Feb 10, 2025 -> North Korea's defense ministry statement Feb 11 vowing to punish 'provokers' (KCNA via Al Jazeera). The statement names the submarine, but it is the only North Korean act: no launch, test or drill was found inside the 7 days in the sources read. The header rule gives R-strong only when a North Korean act is tied to the move; a statement alone is R-weak (W9 audit; was R-strong)."),
 (2050, "Military/Property", "R-weak", "USS Carl Vinson visits Busan Mar 2, 2025 -> Kim Yo Jong statement Mar 4 threatening options against the 'security of the enemy' (KCNA via Stripes). The reply is a statement and the only North Korean act inside the 7 days; the next launch was Mar 10, 8 days after. A statement alone is R-weak under the header rule (W9 audit; was R-strong)."),
 (2052, "Military/Property", "R-weak", "Freedom Shield begins Mar 10, 2025 -> several close-range ballistic missiles the same day (JCS via AP). North Korea had warned of 'physical conflict'."),
 (2054, "Military/Property", "Unverified", "B-1B drill Apr 15, 2025. AP reports no North Korean response as of publication; Apr 16-22 was not searched."),
 (2056, "Political/Diplomatic", "Unclear", "Trump repeats his wish to meet Kim, Oct 28, 2025. North Korea CLAIMED a cruise-missile test the same day (2057, claim only, not counted); the Oct 22 SRBMs (2055) came before. No counted reply."),
 (2058, "Military/Property", "R-strong", "Hegseth visits the DMZ Nov 3, 2025 -> artillery rounds Nov 3 (2059) and an SRBM Nov 7 (JCS, Japan MoD); on Nov 7 North Korea's defense minister CLAIMED the visit fans 'war hysteria' (USNI)."),
 (2060, "Economic/Blockade", "R-weak", "Treasury sanctions bankers Nov 4, 2025 -> SRBM Nov 7 (3 days). The same launch is also tied to the Hegseth and carrier visits; link to the sanctions is weak."),
 (2061, "Military/Property", "R-strong", "USS George Washington arrives Busan Nov 5, 2025 -> SRBM Nov 7; the defense minister denounced the visits the same day (USNI)."),
 (2064, "Military/Property", "R-weak", "Freedom Shield begins Mar 9, 2026 -> about 10 ballistic missiles Mar 14 (JCS, Japan MoD), day 6 of the drill."),
 (2066, "Economic/Blockade", "R-weak", "Treasury IT-worker sanctions Mar 12, 2026 -> about 10 ballistic missiles Mar 14 (2 days). The launch was also inside Freedom Shield; link to the sanctions is weak."),
 (2068, "Military/Property", "R-weak", "Ulchi Freedom Shield begins scaled down Aug 17, 2026 -> about 10 SRBMs Aug 20 (JCS). Kim Yo Jong dismissed the reduction (AP via PBS)."),
 (2069, "Political/Diplomatic", "R-weak", "Trump says he will meet Kim, Aug 19, 2026 -> about 10 SRBMs Aug 20; AP headline says the barrage came 'after dismissing overture from Trump'."),
 (2071, "Military/Property", "R-weak", "Freedom Edge 26 begins Sep 7, 2026 -> multiple ballistic missiles Sep 12 (Stripes). North Korea described Sep 12 as its own firepower drill; link plausible only."),
]

# Reply pairs (pair id, trigger, reply, category, reply caused casualties Y/N, note)
PAIRS = [
 (2001, 2001, 2002, "Military/Property", "N", "Sixth nuclear test three days after the US B-1B/F-35 flight; AP does not call it a reply"),
 (2002, 2012, 2013, "Military/Property", "N", "Projectiles twice, a day after the scaled-down drills began"),
 (2003, 2016, 2017, "Military/Property", "N", "Two SRBMs two days after US sanctions; North Korea's own statement ties the launch to the sanctions (AP)"),
 (2004, 2019, 2020, "Military/Property", "N", "ICBM and two SRBMs hours after Biden left Asia, four days after the Biden-Yoon summit pledge"),
 (2005, 2021, 2022, "Military/Property", "N", "SRBM as the USS Ronald Reagan arrived in Busan"),
 (2006, 2023, 2024, "Military/Property", "N", "Two SRBMs two days after the naval drills began (inside a dense-launch window, link weak)"),
 (2007, 2026, 2027, "Military/Property", "N", "23 missiles two days after the large air exercise began (inside a dense-launch window, link weak)"),
 (2008, 2030, 2031, "Military/Property", "N", "Two ballistic missiles hours after the USS Kentucky docked in Busan"),
 (2009, 2033, 2034, "Military/Property", "N", "Failed satellite launch three days after Ulchi Freedom Shield began"),
 (2010, 2036, 2038, "Military/Property", "N", "US B-1B joins a trilateral air drill two days after the Hwasong-18 ICBM launch (US reply to North Korea)"),
 (2011, 2041, 2042, "Military/Property", "N", "Failed launch (claimed multiple-warhead test) four days after the Roosevelt reached Busan"),
 (2012, 2043, 2044, "Military/Property", "N", "Two ballistic missiles four days after Freedom Edge began; North Korea CLAIMED an 'overwhelming' response the day before"),
 (2013, 2048, 2049, "Military/Property", "N", "Defense ministry statement threatening to punish 'provokers' the day after the submarine docked (statement, not a launch)"),
 (2014, 2050, 2051, "Military/Property", "N", "Kim Yo Jong statement two days after the Vinson arrived (statement, not a launch)"),
 (2015, 2052, 2053, "Military/Property", "N", "Ballistic missiles the day Freedom Shield began"),
 (2016, 2058, 2062, "Military/Property", "N", "SRBM four days after Hegseth's DMZ visit; defense minister statement the same day"),
 (2017, 2060, 2062, "Military/Property", "N", "SRBM three days after the Treasury bankers sanctions (link weak; same launch as pair 2016 and 2018)"),
 (2018, 2061, 2062, "Military/Property", "N", "SRBM two days after the USS George Washington reached Busan"),
 (2019, 2064, 2067, "Military/Property", "N", "About 10 ballistic missiles on day 6 of Freedom Shield"),
 (2020, 2066, 2067, "Military/Property", "N", "Same launch, two days after Treasury IT-worker sanctions (link weak)"),
 (2021, 2068, 2070, "Military/Property", "N", "About 10 SRBMs three days after the scaled-down Ulchi Freedom Shield began"),
 (2022, 2069, 2070, "Military/Property", "N", "Same launch, a day after Trump said he would meet Kim"),
 (2023, 2071, 2072, "Military/Property", "N", "Ballistic missiles five days after Freedom Edge 26 began; North Korea called it its own drill"),
 (2024, 2032, 2034, "Military/Property", "N", "Failed satellite launch six days after Camp David (link weak; also tied to pair 2009)"),
]

# Dense-launch windows (US moves inside are context only) and the acts that started them.
# North Korea never reached a near-daily pace in the sources read, so these are the two densest stretches found:
#  A: Sep 25 - Nov 2, 2022 (Stripes: 18th round of tests that year on Sep 25, a record; 5 sourced launch days
#     here, and many more on dates not sourced, including Nov 3-9 and the Nov 18 ICBM; the window probably ran to Nov 18).
#  B: Sep 12 - Oct 12, 2026 (Reuters: the Oct 12 launch was the fourth in a month). No US move falls inside B.
WINDOWS = [(d(2022, 9, 25), d(2022, 11, 2)), (d(2026, 9, 12), d(2026, 10, 12))]
START_ACTS = {2022, 2072}

# Phases (oldest first)
PHASES = [
 ("Nuclear and ICBM tests", d(2017, 8, 31), d(2018, 6, 11), "Sixth nuclear test (#2002), Hwasong-15 (#2003), Treasury shipping package (#2004)"),
 ("Summits and stalled talks", d(2018, 6, 12), d(2019, 12, 31), "Singapore (#2005), Hanoi (#2006), DMZ (#2011), 2019 launches (#2008, #2009, #2013), Wise Honest seizure (#2010)"),
 ("Quiet and Biden review", d(2020, 1, 1), d(2021, 12, 31), "Few sourced events: cruise missiles (#2014), tanker seizure (#2015)"),
 ("Record launch pace", d(2022, 1, 1), d(2022, 12, 31), "Sanctions (#2016), ICBM (#2018, #2020), the Sep 25 - Nov 2 dense stretch (#2022-#2027), drones (#2028)"),
 ("Strategic assets and trilateral drills", d(2023, 1, 1), d(2024, 12, 31), "Washington Declaration (#2029), Kentucky (#2030), Camp David (#2032), Freedom Edge (#2043), satellite attempts (#2034, #2035, #2040)"),
 ("Second Trump term", d(2025, 1, 20), d(2026, 10, 24), "Carrier and submarine visits (#2048, #2050, #2061), Freedom Shield, Trump's talk offers (#2056, #2069), 2026 launches (#2063-#2076)"),
]

CHAIN_NAMES = {
 2001: "US bombers over South Korea -> sixth nuclear test",
 2012: "Scaled-down drills -> Aug 2019 projectiles",
 2016: "US sanctions -> two SRBMs Jan 14, 2022",
 2019: "Biden-Yoon pledge -> ICBM and SRBMs May 25, 2022",
 2021: "Reagan in Busan -> SRBM -> naval drills -> SRBMs",
 2026: "Large air exercise -> 23 missiles Nov 2, 2022",
 2030: "USS Kentucky in Busan -> two ballistic missiles",
 2033: "Ulchi Freedom Shield 2023 -> failed satellite launch",
 2036: "Hwasong-18 ICBM -> B-1B trilateral drill",
 2041: "Roosevelt in Busan -> failed launch -> Freedom Edge -> two missiles Jul 1, 2024",
 2048: "Submarine in Busan -> North Korean threat statement",
 2050: "Vinson in Busan -> Kim Yo Jong statement -> Freedom Shield launch",
 2058: "Hegseth DMZ visit, Treasury sanctions and carrier visit -> SRBM Nov 7, 2025",
 2064: "Freedom Shield 2026 and Treasury sanctions -> about 10 missiles Mar 14",
 2068: "Reduced Ulchi Freedom Shield and Trump's offer -> about 10 SRBMs Aug 20, 2026",
 2071: "Freedom Edge 26 -> ballistic missiles Sep 12 and the autumn 2026 launches",
}
