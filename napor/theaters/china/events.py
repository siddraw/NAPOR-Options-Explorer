"""NAPOR China: Taiwan Strait and South China Sea, Jan 2019 - Oct 24, 2026 (research file, W6 research phase).

Same shape as napor/theaters/houthis/events_early.py (W2). Event IDs 3001-3999 and pair IDs 3001-3999
belong to this file. Config, export and page data are not built yet (that comes after the engine).

Option letters used in US_OPTION (A, hold, is never tagged):
  B  talks, leader calls, summits
  C  sanctions, export controls, entity listings aimed at China's military / bases
  D  Taiwan Strait transits and South China Sea freedom-of-navigation operations (FONOPs)
  E  arms sales to Taiwan (announced dates) and Taiwan military aid
  F  high-level visits or contacts with Taiwan
  G  joint exercises with allies in the region
  H  other deployments / posture
G has one real case (3040) and H has one (3011): both are "very thin evidence".

Rules used here (docs/SOURCE_STANDARD.md):
- Only allowed outlets and official statements. Wire stories read through a syndicated copy are labelled
  "AP (via ...)", "AFP (via ...)", "Reuters (via ...)". seen="full text" means the article was read;
  seen="snippet" means only the search-result headline was seen.
- Xinhua, Global Times, PLA Daily, Chinese MND/MFA were NOT opened. What China says is used only as
  reported by an allowed outlet and written "China says" / "China CLAIMS".
- What counts as a reply (a "reply" is a China action that follows a US move within 7 days):
  * R-strong: China says the action answers the US move, and a dated PLA / coast-guard drill or counter-sanction follows within 7 days.
  * R-weak: a dated PLA, coast-guard or counter-sanction action within 7 days that an allowed outlet ties to the US move, but China does not say so.
  * N: the reaction reported is only a statement, a protest or routine "tracked and monitored" shadowing. This is
    background, not a reply. N means "no reply found in the sources read" (the note says what was read/searched).
  * Unclear / Unverified: see each note.
  Routine PLA activity near Taiwan (daily ADIZ flights, joint combat readiness patrols with no named link) is background,
  not a reply, unless an allowed outlet ties it to a US move or it is a clear step up on a named day.
- The 7-day window is counted from the date of the US move as logged.
- SMALL N: Taiwan-specific US moves are few. Per option: E 7 and F 7 (only 2 of the E moves and 5 of the F moves have a reply inside 7 days), G 1, H 1, C 2.
  Do not read a rate from G, H or C. D (16 moves) is the only option with a usable count, and almost all are N
  because China answers a transit with words and shadowing.
- CENSUS covers US moves of kinds C-H (as in W2). B moves (talks) are logged but not censused.
- Event 3048 is NOT confirmed (only outlets not on the allowed list were found); it is not counted.
- Gaps (searched, no allowed source found, so left out): Oct 30 2025 Trump-Xi Busan meeting; Nov 13 2025 $330M
  arms sale; Sep 24 2026 Xi visit to the White House; the Dec 2024 US entity-list action (date not in any
  allowed article read); 2021 (only 3022 logged); 2022-2023 US SCS FONOPs; Balikatan and other allied drills.
- Dates follow the announcement date for arms sales. Where a date was inferred it is in PARTLY.
"""
import datetime as dt


def d(y, m, day):
    return dt.date(y, m, day)


def _s(headline, outlet, published, url, seen="snippet"):
    return {'headline': headline, 'outlet': outlet, 'published': published, 'seen': seen, 'url': url}


# Columns: ID, Date, Actor, Action Type, Target, Detail, Trigger ID, Severity, Confidence, Source
EVENTS = [
(3001, d(2019,1,7), "US", "FONOP (destroyer, Paracel Islands)", "Paracel Islands (South China Sea)", "USS McCampbell conducts a freedom of navigation operation near the Paracels. China says it sent military vessels and aircraft to identify the ship and warn it to leave, and lodged 'stern representations'", None, "No damage; verbal protest", "Medium", "see audit"),
(3002, d(2019,1,24), "US", "Taiwan Strait transit (destroyer, oiler)", "Taiwan Strait", "USS McCampbell and USNS Walter Diehl transit the Taiwan Strait (date from USNI's list of transits)", None, "n/a", "Medium", "see audit"),
(3003, d(2019,2,25), "US", "Taiwan Strait transit (destroyer, cargo ship)", "Taiwan Strait", "USS Stethem and USNS Chavez transit the Taiwan Strait, the 4th US warship transit in 5 months", None, "n/a", "Medium", "see audit"),
(3004, d(2019,3,24), "US", "Taiwan Strait transit (destroyer, Coast Guard cutter)", "Taiwan Strait", "USS Curtis Wilbur and USCGC Bertholf transit the Taiwan Strait (date from USNI's list of transits)", None, "n/a", "Medium", "see audit"),
(3005, d(2019,4,28), "US", "Taiwan Strait transit (two destroyers)", "Taiwan Strait", "USS Stethem and USS William P. Lawrence make an overnight transit, the 7th since July 2018. Chinese Foreign Minister spokesman Geng Shuang says Beijing paid 'close attention'; US officials call PLA Navy interactions 'safe and professional'", None, "No damage; verbal reaction only", "Medium", "see audit"),
(3006, d(2019,5,6), "US", "FONOP (two destroyers, Spratly Islands)", "Gaven and Johnson Reefs (Spratlys)", "USS Preble and USS Chung-Hoon pass within 12 nautical miles of Gaven and Johnson Reefs (USNI cites media reports; the 7th Fleet gave no details). China says its navy identified and warned them off and calls it a violation of its sovereignty", None, "No damage; verbal protest", "Medium", "see audit"),
(3007, d(2019,7,8), "US", "Arms sale announced ($2.2 billion)", "Taiwan", "US approves a possible $2.2 billion sale: 108 M1A2T Abrams tanks, 250 Stinger missiles and support. China says it is 'seriously concerned'", None, "n/a", "Medium", "see audit"),
(3008, d(2019,7,13), "China (Foreign Ministry, as reported)", "Counter-sanctions announced (US firms in the sale)", "US companies in the Taiwan sale", "Spokesman Geng Shuang says China 'will impose sanctions on US enterprises participating in this sale'. Al Jazeera names no firm, and no list of firms was found", 3007, "No named firms found", "Medium", "see audit"),
(3009, d(2019,11,20), "US", "FONOP (littoral combat ship, Mischief Reef)", "Mischief Reef (Spratlys)", "USS Gabrielle Giffords sails near Mischief Reef (USNI infers the day from 'Wednesday'). China's Foreign Ministry says it entered waters 'illegally'; Southern Theater Command says the US is stirring up trouble", None, "No damage; verbal protest", "Medium", "see audit"),
(3010, d(2019,11,21), "US", "FONOP (destroyer, Paracel Islands)", "Paracel Islands", "USS Wayne E. Meyer sails near the Paracels, challenging China's baselines (USNI infers the day from 'Thursday'). China says its military vessels tracked both ships and that it made 'stern representations'", None, "No damage; verbal protest", "Medium", "see audit"),
(3011, d(2020,7,4), "US", "Posture (two-carrier operations)", "South China Sea", "USS Nimitz and USS Ronald Reagan carrier groups move into the South China Sea around July 4 and resume dual-carrier operations on July 17. China had held its own drills off the Paracels in early July (before the carriers); China's defense ministry accuses the US of 'flexing its muscles' on July 9", None, "n/a", "Medium", "see audit"),
(3012, d(2020,8,9), "US", "High-level visit (Health Secretary Azar to Taipei)", "Taiwan", "HHS Secretary Alex Azar arrives in Taiwan and meets President Tsai on Aug 10; The War Zone calls it the highest-level US visit in four decades", None, "n/a", "Medium", "see audit"),
(3013, d(2020,8,10), "China (PLA, per Taiwan MND)", "Aircraft cross the median line", "Taiwan Strait median line", "Formations of J-10 and J-11 fighters briefly cross to Taiwan's side shortly before Azar meets Tsai; Taiwan's MND says they were tracked and 'driven out' and calls it deliberate. No aircraft count given", 3012, "No shots; no damage", "Medium", "see audit"),
(3014, d(2020,8,26), "US", "Sanction (24 Chinese firms on the Entity List, visa limits)", "Chinese firms and people tied to South China Sea bases", "Commerce adds 24 Chinese companies to the Entity List and State announces visa limits over the South China Sea buildup; the first US economic sanction for conduct in the South China Sea", None, "n/a", "Medium", "see audit"),
(3015, d(2020,8,26), "China (PLA, per US defense official)", "Missile launch (medium-range ballistic missiles)", "South China Sea between Hainan and the Paracels", "A US defense official tells Reuters China launched four medium-range ballistic missiles into the South China Sea. The timing against the Entity List announcement is unclear and China did not link them. A day earlier China had complained about a US U-2 over a live-fire zone", None, "No damage", "Medium", "see audit"),
(3016, d(2020,8,30), "US", "Taiwan Strait transit (destroyer)", "Taiwan Strait", "USS Halsey transits the Taiwan Strait; USNI reports no Chinese reaction. USS Mustin had transited earlier in August (the Navy's 10th passage of 2020)", None, "n/a", "Medium", "see audit"),
(3017, d(2020,9,17), "US", "High-level visit (Under Secretary Krach to Taipei)", "Taiwan", "Under Secretary of State Keith Krach visits Taiwan (Bloomberg's Sept 18 report says Chinese aircraft crossed 'again' as the envoy visited; start date inferred)", None, "n/a", "Medium", "see audit"),
(3018, d(2020,9,18), "China (PLA)", "Aircraft cross the Taiwan Strait median line", "Taiwan Strait median line", "Chinese aircraft cross the Strait again while the US envoy is in Taiwan (headline only; no count was read)", 3017, "No shots; no damage", "Low", "see audit"),
(3019, d(2020,10,21), "US", "Arms sale announced ($1.8 billion)", "Taiwan", "State Department approves $1.8 billion in new weapons for Taiwan (Al Jazeera says 'last week' on Oct 26; day inferred from a related headline)", None, "n/a", "Medium", "see audit"),
(3020, d(2020,10,26), "China (Foreign Ministry, as reported)", "Counter-sanctions (US defense units)", "Boeing Defense, Lockheed Martin, Raytheon Technologies", "China announces sanctions on the defense units of Boeing, Lockheed Martin and Raytheon over the Taiwan arms sale; spokesman Zhao Lijian says it is to 'uphold national interests'", 3019, "Unspecified sanctions", "Medium", "see audit"),
(3021, d(2020,12,19), "US", "Taiwan Strait transit (destroyer)", "Taiwan Strait", "USS Mustin transits the Taiwan Strait. USNI reports no Chinese response; China's carrier Shandong transits the strait Dec 20, which the PLA Navy calls normal training", None, "n/a", "Medium", "see audit"),
(3022, d(2021,1,9), "US", "High-level contacts (limits on Taiwan contacts lifted)", "Taiwan", "Secretary of State Pompeo lifts the self-imposed limits on US diplomats' contacts with Taiwan ('No more'). AP says the move was expected to upset China; the AP page reports no Chinese response to it (it notes Beijing's earlier criticism of a planned Craft trip to Taiwan)", None, "n/a", "Medium", "see audit"),
(3023, d(2022,2,7), "US", "Arms sale announced ($100 million, missile defense upkeep)", "Taiwan", "US approves a $100 million deal with Lockheed Martin and Raytheon to maintain Taiwan's missile defense systems", None, "n/a", "Medium", "see audit"),
(3024, d(2022,2,21), "China (Foreign Ministry, as reported)", "Counter-sanctions (US defense firms)", "Lockheed Martin, Raytheon Technologies", "China sanctions Lockheed Martin and Raytheon Technologies over the sale (the article is dated Feb 24 and cites a Reuters report dated Feb 21; the day is inferred). This is 14 days after the sale, outside the 7-day window", 3023, "Unspecified sanctions", "Medium", "see audit"),
(3025, d(2022,8,2), "US", "High-level visit (House Speaker Pelosi to Taipei)", "Taiwan", "Speaker Nancy Pelosi arrives in Taiwan, the highest-ranking elected US official to visit in decades, and leaves Aug 3. Beijing had warned against the trip", None, "n/a", "Medium", "see audit"),
(3026, d(2022,8,4), "China (PLA)", "Large-scale drills (live fire in six zones around Taiwan, Aug 4-7, extended)", "Waters around Taiwan", "China says more than 100 warplanes and 10 warships took part in the first two days; Chinese state media say missiles were fired over Taiwan (Japan says five landed in its exclusive economic zone and four others flew over Taiwan). Al Jazeera says the PLA kept drilling on Aug 8, past the planned Aug 7 end", 3025, "No deaths reported; trade and shipping disruption", "Medium", "see audit"),
(3027, d(2022,8,5), "China (Foreign Ministry, as reported)", "Counter-sanctions and suspension of talks", "Pelosi and family; US-China dialogue", "China announces mostly symbolic sanctions on Pelosi and her family and suspends talks with the US on military relations, maritime safety, climate and other areas", 3025, "Talks suspended", "Medium", "see audit"),
(3028, d(2022,8,28), "US", "Taiwan Strait transit (two cruisers)", "Taiwan Strait", "USS Antietam and USS Chancellorsville transit, the first since Pelosi's visit. China's Eastern Theater Command says its forces are 'on high alert'", None, "n/a", "Medium", "see audit"),
(3029, d(2022,9,2), "US", "Arms sale announced ($1.1 billion)", "Taiwan", "US approves a possible $1.1 billion sale: Harpoon anti-ship missiles (about $355M), Sidewinder missiles (about $85.6M) and radar support (about $665M). The Reuters article reports no Chinese statement", None, "n/a", "Medium", "see audit"),
(3030, d(2022,10,7), "US", "Export controls (advanced chips, chip equipment)", "China's advanced computing and chip industry", "Commerce's BIS issues rules limiting China's ability to buy and make high-end chips; phased in from Oct 7. AP (Oct 8): China's foreign ministry criticises it; no counter-measure reported", None, "n/a", "Medium", "see audit"),
(3031, d(2023,4,5), "US", "High-level contact (Speaker McCarthy meets Tsai, California)", "Taiwan", "House Speaker Kevin McCarthy meets President Tsai Ing-wen at the Reagan Library in California; China's foreign ministry had said it would 'take resolute measures'", None, "n/a", "Medium", "see audit"),
(3032, d(2023,4,8), "China (PLA)", "Large-scale drills (three days around Taiwan, ended Apr 10)", "Waters around Taiwan", "China's three-day drills simulate sealing off the island. Taiwan's MND reports 91 Chinese aircraft on Monday Apr 10, 54 crossing the median line (AFP). AFP ties the drills to the Tsai-McCarthy meeting", 3031, "No damage", "Medium", "see audit"),
(3033, d(2023,6,3), "US (with Canada)", "Taiwan Strait transit (destroyer and frigate)", "Taiwan Strait", "USS Chung-Hoon and HMCS Montreal conduct a Taiwan Strait transit", None, "n/a", "Medium", "see audit"),
(3034, d(2023,6,3), "China (PLA Navy)", "Unsafe close pass (destroyer crosses bow)", "USS Chung-Hoon", "A Chinese guided-missile destroyer crosses the Chung-Hoon's bow at about 150 yards (US Indo-Pacific Command); the Chung-Hoon slows to 10 knots. China's defense minister Li Shangfu says the US and allies created the danger", 3033, "No collision", "Medium", "see audit"),
(3035, d(2023,6,19), "US", "Talks (Secretary Blinken meets Xi in Beijing)", "China", "Blinken meets Xi for 35 minutes at the end of a two-day Beijing visit; no breakthroughs on trade, Taiwan or the South China Sea", None, "n/a", "Medium", "see audit"),
(3036, d(2023,7,28), "US", "Military aid announced (up to $345 million, Taiwan)", "Taiwan", "US announces a military aid package for Taiwan worth up to $345 million (headline only)", None, "n/a", "Low", "see audit"),
(3037, d(2023,8,12), "US", "High-level contact (Taiwan VP Lai stops in New York, then San Francisco Aug 16)", "Taiwan", "Taiwan Vice President Lai Ching-te stops in New York and San Francisco (Aug 16, per an AP photo caption) on trips to and from Paraguay; US officials greet him. The Aug 12 New York date is inferred: the pages read give no New York arrival date (an AP photo caption shows him in New York on Aug 14)", None, "n/a", "Medium", "see audit"),
(3038, d(2023,8,19), "China (PLA)", "Large-scale drills (patrols around Taiwan)", "Waters around Taiwan", "China's Eastern Theater Command calls the drills a 'stern warning' to Taiwan separatists colluding with outside forces. Taiwan's MND: 42 aircraft since 9 a.m., 26 crossing the median line, 8 ships (Bloomberg)", 3037, "No damage", "Medium", "see audit"),
(3039, d(2023,11,15), "US", "Talks (Biden-Xi summit, California)", "China", "Biden and Xi agree to restore military contacts China cut after Pelosi's 2022 visit; Xi tells Biden to 'stop arming Taiwan'", None, "n/a", "Medium", "see audit"),
(3040, d(2024,4,7), "US (with Japan, Australia, Philippines)", "Joint exercise (first multilateral maritime cooperative activity)", "Philippine exclusive economic zone", "Naval and air units of the US, Japan, Australia and the Philippines hold their first multilateral maritime cooperative activity in the West Philippine Sea", None, "n/a", "Medium", "see audit"),
(3041, d(2024,4,7), "China (PLA Southern Theater Command)", "Combat patrols (joint naval and air, South China Sea)", "South China Sea", "The command announces 'joint naval and air combat patrols' the same day as the allied drill; AFP calls its line about 'hotspots' an apparent swipe at the allied drills. The Philippine armed forces chief said two Chinese ships came about 7 miles from the allied exercise area (Stars and Stripes)", 3040, "No clash reported", "Medium", "see audit"),
(3042, d(2024,5,23), "China (PLA)", "Large-scale drills (Joint Sword-2024A, two days)", "Waters around Taiwan", "Drills start three days after Lai Ching-te's inauguration, in which he urged Beijing to stop 'intimidation'. No US move is named as the trigger", None, "No clash reported", "Medium", "see audit"),
(3043, d(2024,6,17), "China (Coast Guard)", "Coast guard confrontation (water cannon, ramming, blocking)", "Philippine resupply mission, Second Thomas Shoal", "Chinese vessels block a Philippine resupply run to the BRP Sierra Madre; a Philippine sailor is severely injured and boats damaged. The Pentagon condemns 'escalatory and irresponsible actions'. China's coast guard blames Manila. The US had restated in March that the defense treaty covers Philippine coast guard vessels", None, "1 Philippine sailor severely injured; vessels damaged", "Medium", "see audit"),
(3044, d(2024,10,14), "China (PLA)", "Large-scale drills (Joint Sword-2024B, one day)", "Waters around Taiwan", "China frames the drills as a reply to Lai's Oct 10 National Day speech. Taiwan's MND: 125 sorties, 90 entering the ADIZ, 17 PLA Navy and 17 coast guard ships. The Pentagon calls it 'irresponsible, disproportionate, and destabilizing'", None, "No clash reported", "Medium", "see audit"),
(3045, d(2024,11,29), "US", "Arms sale announced ($385 million)", "Taiwan", "Pentagon announces about $320M for F-16 parts and AESA radars and about $65M for mobile subscriber equipment", None, "n/a", "Medium", "see audit"),
(3046, d(2024,11,30), "US", "High-level contact (President Lai transits Hawaii, then Guam)", "Taiwan", "President Lai makes unofficial stops in Hawaii and Guam on a weeklong Pacific tour that ended Dec 6, his first US stops as president (the Hawaii arrival date is inferred; the Guam date was not read). China calls him a 'separatist'", None, "n/a", "Medium", "see audit"),
(3047, d(2024,12,3), "China (as reported)", "Counter-measure (export ban to the US)", "US buyers of gallium, germanium, antimony and super-hard materials", "AP: China bans exports to the US of gallium, germanium, antimony and other high-tech materials, hitting back at US chip sanctions after Washington added 140 firms to the Entity List. The US listing date is not given in the article read, so no US event is logged", None, "Export ban", "Medium", "see audit"),
(3048, d(2024,12,5), "China (Foreign Ministry, as reported)", "Counter-sanctions (13 US defense firms)", "13 US arms companies", "China sanctions 13 US arms companies after the Nov 29 sale. Only an outlet not on the allowed list was found (agency not named), so this is NOT counted", 3045, "Unspecified sanctions", "Low", "see audit"),
(3049, d(2024,12,10), "China (PLA / coast guard, per Taiwan MND)", "Large maritime deployment (unannounced)", "Waters around Taiwan", "Taiwan's defense ministry reports the largest Chinese maritime movements in decades and 47 PLA aircraft in 24 hours; Beijing announced no drills and did not acknowledge it. This is day 10 after the Lai transit began", None, "No clash reported", "Medium", "see audit"),
(3050, d(2025,2,10), "US", "Taiwan Strait transit (destroyer and survey ship)", "Taiwan Strait", "USS Ralph Johnson and USNS Bowditch transit Feb 10-12, the first of Trump's second term. The Eastern Theater Command says it tracked them and the US 'sent the wrong signals'", None, "n/a", "Medium", "see audit"),
(3051, d(2025,2,26), "China (PLA, per Taiwan MND)", "Live-fire drill (joint combat readiness patrol)", "About 40 nautical miles off Kaohsiung and Pingtung", "Taiwan's MND reports 32 sorties, 22 crossing the median line, plus live fire. USNI names no trigger; China's foreign ministry says it is 'not a question related to foreign affairs'. This is day 16 after the Feb 10 transit", None, "No clash reported", "Medium", "see audit"),
(3052, d(2025,4,1), "China (PLA)", "Large-scale drills (Strait Thunder-2025A, two days)", "Middle and southern Taiwan Strait", "Taiwan's MND counts 76 aircraft, 15 PLA Navy ships and 4 official ships in 24 hours, with 37 sorties crossing the median line into the ADIZ. China's defense ministry blames Lai's 'independence' provocations; USNI names no US trigger", None, "No clash reported", "Medium", "see audit"),
(3053, d(2025,8,11), "China (Coast Guard and PLA Navy)", "Coast guard confrontation (Chinese ships collide)", "Philippine Coast Guard BRP Suluan, Scarborough Shoal", "About 10 nautical miles off Scarborough Shoal, China Coast Guard cutter 3104 collides with PLA Navy destroyer Guilin while both chase the Philippine ship", None, "Collision; Chinese casualties unknown", "Medium", "see audit"),
(3054, d(2025,8,13), "US", "FONOP (destroyer, Scarborough Shoal)", "Scarborough Shoal", "USS Higgins sails within 12 nautical miles of Scarborough Shoal, the second publicly announced FONOP of Trump's term. China's Southern Theater Command CLAIMS it tracked, warned and expelled the ship; the 7th Fleet calls that 'false'", None, "No damage", "Medium", "see audit"),
(3055, d(2025,9,12), "US (with UK)", "Taiwan Strait transit (destroyer and Royal Navy frigate)", "Taiwan Strait", "USS Higgins and HMS Richmond transit. The Eastern Theater Command says it sent forces to 'track and monitor' and that the move 'undermined peace and stability'. Separately China's Southern Theater Command held 'routine patrols' Sept 12-13 that it linked to Philippine patrols with the US and Japan", None, "n/a", "Medium", "see audit"),
(3056, d(2025,12,18), "US", "Arms sale announced ($11.1 billion)", "Taiwan", "US announces a record $11.1 billion arms sale to Taiwan", None, "n/a", "Medium", "see audit"),
(3057, d(2025,12,26), "China (Foreign Ministry, as reported)", "Counter-sanctions (20 US defense firms, 10 executives)", "20 US defense companies and 10 executives", "China sanctions 20 US defense firms, including a Boeing unit and Northrop Grumman, and 10 executives over the sale (announced on the Friday before the drills; day inferred)", 3056, "Sanctions", "Medium", "see audit"),
(3058, d(2025,12,29), "China (PLA and China Coast Guard)", "Large-scale drills (Justice Mission 2025, Dec 29-30)", "Waters around Taiwan", "Eastern Theater Command blockade-style drills with live-fire. Taiwan reports 89 aircraft and drone sorties with 67 in the ADIZ, 14 PLA Navy ships and 14 coast guard ships and a 4-ship amphibious group on day one. USNI says the drills protested the arms sales", 3056, "No clash reported", "Medium", "see audit"),
(3059, d(2026,1,16), "US", "Taiwan Strait transit (destroyer and survey ship)", "Taiwan Strait", "USS John Finn and USNS Mary Sears transit Jan 16-17, the first of 2026. The Eastern Theater Command says it monitored and 'remains on high alert'. Taiwan's MND counted 25 sorties on Jan 16, 6 crossing the median line", None, "n/a", "Medium", "see audit"),
(3060, d(2026,5,14), "US", "Talks (Trump-Xi summit, Beijing)", "China", "Trump and Xi meet in Beijing. Xi says mishandling Taiwan could lead to 'clashes and even conflicts' (as reported from Xinhua); the $11B arms package was approved but not yet delivered. Trump invites Xi to the White House (Sept 24). A Reuters caption dates the Beijing visit May 15", None, "n/a", "Medium", "see audit"),
(3061, d(2026,7,22), "US", "Talks (Secretary Rubio and Foreign Minister Wang Yi)", "China", "Rubio and Wang Yi discuss areas of cooperation to prepare for Xi's Sept 24 visit; Reuters reports no agreement or other outcome and does not mention Taiwan", None, "n/a", "Medium", "see audit"),
(3062, d(2026,7,23), "China (PLA, maritime notice)", "Live-fire drills (two days, near Dongshan Island, Fujian)", "Taiwan Strait near the Fujian coast", "Maritime authorities announce live-fire drills on Jul 23-24 in two areas within about 7 miles of the Chinese coast. Reuters notes they follow the Rubio-Wang talks the day before and gives no stated reason; this is treated as background", None, "No clash reported", "Medium", "see audit"),
(3063, d(2026,7,24), "China (Coast Guard)", "Coast guard confrontation (water cannon, second day)", "Philippine vessels, Scarborough Shoal", "The Philippines accuses China of using water cannon on its vessels on a second day, Fri Jul 24, at Scarborough Shoal (first day Thursday, inferred as Jul 23). Water cannon hit two Philippine ships; China says it used 'control measures'. A separate Second Thomas Shoal confrontation the Monday before left a Filipino sailor hurt by a baton. Rubio, in Manila, calls China's actions 'disturbing' and reaffirms support", None, "Water cannon hit two ships; no Scarborough injuries reported", "Medium", "see audit"),
]

# ---------------------------------------------------------------------------------------------
_USNI_TBL = _s('Two U.S. Warships Pass Through Taiwan Strait in 7th Transit Since 2018', 'USNI News', '2019-04-29', 'https://news.usni.org/2019/04/29/two-u-s-warships-pass-through-taiwan-strait-in-7th-transit-since-2018', 'full text')
_USNI_MUSTIN = _s('Destroyer USS Mustin Transited Taiwan Strait, Chinese Aircraft Carrier Followed', 'USNI News', '2020-12-21', 'https://news.usni.org/2020/12/21/destroyer-uss-mustin-transited-taiwan-strait-chinese-aircraft-carrier-followed', 'full text')
_AJ_PELOSI = _s('Pelosi to meet President Tsai Ing-wen, China drills underway (live blog)', 'Al Jazeera', '2022-08-03', 'https://www.aljazeera.com/amp/news/liveblog/2022/8/3/pelosi-to-meet-president-tsai-ing-wen-china-drills-underway', 'full text')
_WYPR = _s('China halts climate and military dialogue with the U.S. over Pelosi\'s Taiwan visit', 'NPR (via WYPR)', '2022-08-05', 'https://www.wypr.org/2022-08-05/china-halts-climate-and-military-dialogue-with-the-u-s-over-pelosis-taiwan-visit', 'full text')
_KVIA = _s("China's maritime movements around Taiwan are largest in decades, Taipei says", 'CNN (via KVIA)', '2024-12-10', 'https://kvia.com/news/us-world/cnn-world/2024/12/10/chinas-maritime-movements-around-taiwan-are-largest-in-decades-taipei-says/', 'full text')
_USNI_JM = _s('China Launches Blockade Drills Around Taiwan in Protest of U.S. Arms Sales', 'USNI News', '2025-12-29', 'https://news.usni.org/2025/12/29/china-launches-blockade-drills-around-taiwan-in-protest-of-u-s-arms-sales', 'full text')
_REUT_RUBIO = _s('Trump says Xi will visit US on September 24', 'Reuters (via internazionale.it)', '2026-07-23', 'https://www.internazionale.it/ultime-notizie-reuters/2026/07/23/trump-says-xi-will-visit-us-on-september-24', 'full text')
_AFP_APR23 = _s('China ends Taiwan war games aimed at sealing off island', 'AFP (via Borneo Post)', '2023-04-11', 'https://www.theborneopost.com/2023/04/11/china-ends-taiwan-war-games-aimed-at-sealing-off-island/', 'full text')
_AJ_ENTITY = _s('US hits Chinese companies, individuals over South China Sea spat', 'Al Jazeera', '2020-08-27', 'https://www.aljazeera.com/amp/economy/2020/8/27/us-hits-chinese-companies-individuals-over-south-china-sea-spat', 'full text')
_AJ_SANC20 = _s('China to sanction Boeing, other US firms over Taiwan arms sales', 'Al Jazeera', '2020-10-26', 'https://www.aljazeera.com/economy/2020/10/26/china-to-sanction-boeing-and-raytheon-over-taiwan-arms-sales', 'full text')
_AJ_JS24A = _s("'Strong punishment': China starts two days of military drills around Taiwan", 'Al Jazeera', '2024-05-23', 'https://www.aljazeera.com/news/2024/5/23/china-starts-military-drills-around-the-self-governed-island-of-taiwan', 'full text')

SOURCES = {
 3001: [_s('USS McCampbell FONOP Past Paracel Islands Irks China', 'USNI News', '2019-01-07', 'https://news.usni.org/2019/01/07/40202', 'full text')],
 3002: [_USNI_TBL],
 3003: [_s('U.S. Destroyer, Cargo Ship Pass Through Taiwan Strait in 4th Warship Transit in 5 Months', 'USNI News', '2019-02-25', 'https://news.usni.org/2019/02/25/u-s-destroyer-cargo-ship-conduct-taiwan-strait-transit-4th-time-5-months'), _USNI_TBL],
 3004: [_USNI_TBL],
 3005: [_USNI_TBL],
 3006: [_s('U.S. Destroyers Active in 2 Separate South China Sea Operations', 'USNI News', '2019-05-09', 'https://news.usni.org/2019/05/09/u-s-destroyers-active-in-2-seperate-south-china-sea-operations', 'full text')],
 3007: [_s('US approves possible $2.2bn arms sale to Taiwan', 'Al Jazeera', '2019-07-09', 'https://www.aljazeera.com/news/2019/07/approves-22bn-arms-sale-taiwan-190708233858400.html', 'full text')],
 3008: [_s('China vows sanctions on US firms over Taiwan arms sale', 'Al Jazeera', '2019-07-13', 'https://www.aljazeera.com/amp/news/2019/7/13/china-vows-sanctions-on-us-firms-over-taiwan-arms-sale', 'full text')],
 3009: [_s('Beijing Irked at Twin U.S. South China Sea FONOPS', 'USNI News', '2019-11-22', 'https://news.usni.org/2019/11/22/beijing-irked-at-twin-u-s-south-china-sea-fonops', 'full text')],
 3010: [_s('Beijing Irked at Twin U.S. South China Sea FONOPS', 'USNI News', '2019-11-22', 'https://news.usni.org/2019/11/22/beijing-irked-at-twin-u-s-south-china-sea-fonops', 'full text')],
 3011: [_s('Two U.S. Carriers Return to South China Sea After State Dept. Formally Rejects Chinese Claims', 'USNI News', '2020-07-17', 'https://news.usni.org/?p=78457', 'full text')],
 3012: [_s('China sends fighters into Taiwan\'s side of the Strait as high-level U.S. visit begins', 'The War Zone', '2020-08-10', 'https://www.twz.com/35537/china-sends-fighters-into-taiwans-side-of-the-strait-as-high-level-u-s-visit-begins.md', 'full text')],
 3013: [_s('China sends fighters into Taiwan\'s side of the Strait as high-level U.S. visit begins', 'The War Zone', '2020-08-10', 'https://www.twz.com/35537/china-sends-fighters-into-taiwans-side-of-the-strait-as-high-level-u-s-visit-begins.md', 'full text')],
 3014: [_AJ_ENTITY, _s('U.S. targets Chinese individuals, companies over escalation in South China Sea', 'Axios', '2020-08-26', 'https://www.axios.com/2020/08/26/south-china-sea-us-commerce-blacklist-companies')],
 3015: [_AJ_ENTITY],
 3016: [_s('U.S. Destroyer Transits Taiwan Strait for Second Time in August', 'USNI News', '2020-08-31', 'https://news.usni.org/2020/08/31/u-s-destroyer-transits-taiwan-strait-for-second-time-in-august', 'full text')],
 3017: [_s('China Aircraft Cross Taiwan Strait Again as U.S. Envoy Visits', 'Bloomberg', '2020-09-18', 'https://www.bloomberg.com/news/articles/2020-09-18/china-holds-exercises-in-taiwan-strait-amid-u-s-envoy-visit')],
 3018: [_s('China Aircraft Cross Taiwan Strait Again as U.S. Envoy Visits', 'Bloomberg', '2020-09-18', 'https://www.bloomberg.com/news/articles/2020-09-18/china-holds-exercises-in-taiwan-strait-amid-u-s-envoy-visit')],
 3019: [_AJ_SANC20],
 3020: [_AJ_SANC20],
 3021: [_USNI_MUSTIN],
 3022: [_s('Pompeo voids restrictions on diplomatic contacts with Taiwan', 'AP (via WSLS)', '2021-01-09', 'https://www.wsls.com/news/politics/2021/01/09/pompeo-voids-restrictions-on-diplomatic-contacts-with-taiwan/', 'full text')],
 3023: [_s('China sanctions Lockheed, Raytheon over Taiwan arms sales', 'Reuters (via The Defense Post)', '2022-02-24', 'https://www.thedefensepost.com/2022/02/24/china-sanctions-taiwan-arms-sales/', 'full text')],
 3024: [_s('China sanctions Lockheed, Raytheon over Taiwan arms sales', 'Reuters (via The Defense Post)', '2022-02-24', 'https://www.thedefensepost.com/2022/02/24/china-sanctions-taiwan-arms-sales/', 'full text')],
 3025: [_AJ_PELOSI, _WYPR],
 3026: [_WYPR, _AJ_PELOSI],
 3027: [_WYPR],
 3028: [_s('The U.S. sails warships through the Taiwan Strait for first time since Pelosi\'s visit', 'NPR (via KAXE)', '2022-08-28', 'https://www.kaxe.org/news/2022-08-28/the-u-s-sails-warships-through-the-taiwan-strait-for-first-time-since-pelosis-visit', 'full text')],
 3029: [_s('US approves potential $1.1 billion arms sale to Taiwan, Pentagon says', 'Reuters (via Inquirer)', '2022-09-03', 'https://newsinfo.inquirer.net/1657858/us-approves-potential-1-1-billion-arms-sale-to-taiwan-pentagon-says', 'full text')],
 3030: [_s('Commerce Department rolls out export controls on China (BIS announcement)', 'Commerce / BIS (official release)', '2022-10-07', 'https://www.bis.gov/node/20292', 'full text'),
        _s('China lashes out at latest US export controls on chips', 'AP (via News4JAX)', '2022-10-08', 'https://www.news4jax.com/business/2022/10/08/china-lashes-out-at-latest-us-export-controls-on-chips/', 'full text')],
 3031: [_AFP_APR23],
 3032: [_AFP_APR23],
 3033: [_s('Navy releases video of U.S. destroyer\'s close call with Chinese warship in Taiwan Strait', 'CBS News', '2023-06-05', 'https://www.cbsnews.com/amp/news/china-us-taiwan-navy-video-warships-close-call', 'full text')],
 3034: [_s('Navy releases video of U.S. destroyer\'s close call with Chinese warship in Taiwan Strait', 'CBS News', '2023-06-05', 'https://www.cbsnews.com/amp/news/china-us-taiwan-navy-video-warships-close-call', 'full text')],
 3035: [_s('Antony Blinken meets China\'s Xi in a bid to ease soaring U.S.-China tensions', 'AP (via NPR)', '2023-06-19', 'https://www.npr.org/2023/06/19/1183045131/antony-blinken-meets-chinas-xi-in-a-bid-to-ease-soaring-u-s-china-tensions', 'full text')],
 3036: [_s('US announces $345 mln military aid package for Taiwan', 'ABC17 News (wire copy, agency not named)', '2023-07-28', 'https://abc17news.com/?p=1195707')],
 3037: [_s('Taiwan condemns China responding to vice president trip with military exercises', 'Bloomberg (via Fortune)', '2023-08-19', 'https://www.fortune.com/2023/08/19/taiwan-condemns-china-responding-to-vice-president-trip-with-military-exercises/', 'full text')],
 3038: [_s('Taiwan condemns China responding to vice president trip with military exercises', 'Bloomberg (via Fortune)', '2023-08-19', 'https://www.fortune.com/2023/08/19/taiwan-condemns-china-responding-to-vice-president-trip-with-military-exercises/', 'full text')],
 3039: [_s('Five takeaways from the Biden-Xi summit at California\'s Filoli estate', 'Al Jazeera', '2023-11-16', 'https://www.aljazeera.com/amp/news/2023/11/16/five-takeaways-from-the-biden-xi-summit-at-californias-filoli-estate', 'full text')],
 3040: [_s('China conducts combat patrols as US holds drills with allies in disputed waters', 'AFP (via Borneo Post)', '2024-04-08', 'https://www.theborneopost.com/2024/04/08/china-conducts-combat-patrols-as-us-holds-drills-with-allies-in-disputed-waters/', 'full text')],
 3041: [_s('China conducts combat patrols as US holds drills with allies in disputed waters', 'AFP (via Borneo Post)', '2024-04-08', 'https://www.theborneopost.com/2024/04/08/china-conducts-combat-patrols-as-us-holds-drills-with-allies-in-disputed-waters/', 'full text'),
        _s('Historic South China Sea naval drills', 'Stars and Stripes', '2024-04-08', 'https://www.stripes.com/branches/navy/2024-04-08/historic-south-china-sea-naval-drills-13509902.html', 'full text')],
 3042: [_AJ_JS24A],
 3043: [_s('Philippine Sailor Severely Injured, Vessels Damaged as Chinese Block South China Sea Mission', 'USNI News', '2024-06-17', 'https://news.usni.org/2024/06/17/philippine-sailor-severely-injured-vessels-damaged-as-chinese-block-south-china-sea-mission', 'full text')],
 3044: [_s('China Targets Taiwan in Major Military Exercise, Pentagon Condemns \'Irresponsible\' Action', 'USNI News', '2024-10-14', 'https://news.usni.org/2024/10/14/china-targets-taiwan-in-major-military-exercise-pentagon-condemns-irresponsible-action', 'full text')],
 3045: [_s('US approves $385 mln arms sale to Taiwan', 'Reuters (via Kathmandu Post)', '2024-11-30', 'https://kathmandupost.com/world/2024/11/30/us-approves-385-mln-arms-sale-to-taiwan', 'full text')],
 3046: [_KVIA],
 3047: [_s('China bans exports to U.S. of key high-tech materials in response to chip sanctions', 'AP (via PBS NewsHour)', '2024-12-03', 'https://www.pbs.org/newshour/world/china-bans-exports-to-u-s-of-key-high-tech-materials-in-response-to-chip-sanctions', 'full text')],
 3048: [_s('China punishes 13 US arms companies for Taiwan arms deliveries', 'bluewin.ch (agency not named; not an allowed outlet)', '2024-12-05', 'https://www.bluewin.ch/en/news/international/china-punishes-13-us-arms-companies-for-taiwan-arms-deliveries-2474794.html', 'full text')],
 3049: [_KVIA],
 3050: [_s('Chinese Navy Tracks First U.S. Taiwan Strait Transit under Trump Administration', 'USNI News', '2025-02-12', 'https://news.usni.org/2025/02/12/chinese-navy-tracks-first-u-s-taiwan-strait-transit-under-trump-administration', 'full text')],
 3051: [_s('Chinese Warships, Fighters Hold Snap Live Fire Drills 40 Miles Off Taiwan, Say Officials', 'USNI News', '2025-02-26', 'https://news.usni.org/?p=114853', 'full text')],
 3052: [_s('Chinese Military Wraps Intimidation Drills Off Taiwan', 'USNI News', '2025-04-02', 'https://news.usni.org/2025/04/02/chinese-military-wraps-intimidation-drills-off-taiwan', 'full text')],
 3053: [_s('Navy Denies China Chased off U.S. Warship from Scarborough Shoal', 'USNI News', '2025-08-13', 'https://news.usni.org/2025/08/13/navy-denies-china-chased-off-u-s-warship-from-scarborough-shoal', 'full text')],
 3054: [_s('Navy Denies China Chased off U.S. Warship from Scarborough Shoal', 'USNI News', '2025-08-13', 'https://news.usni.org/2025/08/13/navy-denies-china-chased-off-u-s-warship-from-scarborough-shoal', 'full text')],
 3055: [_s('U.S., U.K. Warships Transit Taiwan Strait, Pentagon Confirms', 'USNI News', '2025-09-16', 'https://news.usni.org/2025/09/16/u-s-u-k-warships-transit-taiwan-strait-pentagon-confirms', 'full text'),
        _s('US, UK warships transit Taiwan Strait', 'Stars and Stripes', '2025-09-15', 'https://www.stripes.com/branches/navy/2025-09-15/taiwan-strait-transit-navy-uk-19095815.html', 'full text')],
 3056: [_USNI_JM],
 3057: [_USNI_JM, _s('China sanctions 20 US firms over Taiwan arms sales', 'AFP (via Free Malaysia Today)', '2025-12-27', 'https://www.freemalaysiatoday.com/category/world/2025/12/27/china-sanctions-20-us-firms-over-taiwan-arms-sales', 'full text')],
 3058: [_USNI_JM],
 3059: [_s('UPDATED: U.S. Destroyer, Survey Vessel Conduct First Taiwan Strait Transit of 2026', 'USNI News', '2026-01-17', 'https://news.usni.org/2026/01/17/u-s-destroyer-survey-vessel-conduct-first-taiwan-strait-transit-of-2026-say-chinese-officials', 'full text')],
 3060: [_s('Latest: presidents Xi and Trump (Beijing summit, Xi\'s Taiwan warning)', 'AP (via WOKV)', '2026-05-14', 'https://www.wokv.com/news/world/latest-presidents-xi/YAA7GRURHU2RLD4IFXRISO7RGM/', 'full text'), _REUT_RUBIO],
 3061: [_REUT_RUBIO],
 3062: [_s('China begins two days of live-fire drills in Taiwan Strait', 'Reuters (via internazionale.it)', '2026-07-23', 'https://www.internazionale.it/ultime-notizie-reuters/2026/07/23/china-announces-live-fire-drills-in-taiwan-strait', 'full text')],
 3063: [_s('Philippines accuses China of using water cannon on vessels for second day', 'Al Jazeera', '2026-07-24', 'https://aljazeera.com/news/2026/7/24/philippines-accuses-china-of-using-water-cannon-on-vessels-for-second-day', 'full text')],
}
VERDICT = {k: 'confirmed' for k in SOURCES}
VERDICT[3048] = 'not_confirmed'   # only a non-allowed outlet found; not counted
# Rows where an allowed outlet confirms the event but not every detail in the row (date inferred, number from one side, etc.)
PARTLY = {3037, 3007, 3011, 3014, 3015, 3017, 3019, 3024, 3026, 3030, 3032, 3046, 3054, 3057, 3060, 3012}

# Which option letter each US move belongs to (see header).
US_OPTION = {
 3001: 'D', 3002: 'D', 3003: 'D', 3004: 'D', 3005: 'D', 3006: 'D', 3007: 'E', 3009: 'D', 3010: 'D',
 3011: 'H', 3012: 'F', 3014: 'C', 3016: 'D', 3017: 'F', 3019: 'E', 3021: 'D', 3022: 'F', 3023: 'E',
 3025: 'F', 3028: 'D', 3029: 'E', 3030: 'C', 3031: 'F', 3033: 'D', 3035: 'B', 3036: 'E', 3037: 'F',
 3039: 'B', 3040: 'G', 3045: 'E', 3046: 'F', 3050: 'D', 3054: 'D', 3055: 'D', 3056: 'E', 3059: 'D',
 3060: 'B', 3061: 'B',
}

# My own estimate of the engine's credibility score (full-text allowed outlet 0.80, two outlets 0.96, claim-only 0.30;
# under 0.50 is not counted). Snippet-only rows are estimated at 0.60 (the engine's treatment of snippets was not checked).
CRED_ESTIMATE = {
 3001: 0.80, 3002: 0.80, 3003: 0.96, 3004: 0.80, 3005: 0.80, 3006: 0.80, 3007: 0.80, 3008: 0.80, 3009: 0.80,
 3010: 0.80, 3011: 0.80, 3012: 0.80, 3013: 0.80, 3014: 0.96, 3015: 0.80, 3016: 0.80, 3017: 0.60, 3018: 0.60,
 3019: 0.80, 3020: 0.80, 3021: 0.80, 3022: 0.80, 3023: 0.80, 3024: 0.80, 3025: 0.96, 3026: 0.96, 3027: 0.80,
 3028: 0.80, 3029: 0.80, 3030: 0.96, 3031: 0.80, 3032: 0.80, 3033: 0.80, 3034: 0.80, 3035: 0.80, 3036: 0.60,
 3037: 0.80, 3038: 0.80, 3039: 0.80, 3040: 0.80, 3041: 0.80, 3042: 0.80, 3043: 0.80, 3044: 0.80, 3045: 0.80,
 3046: 0.80, 3047: 0.80, 3048: 0.30, 3049: 0.80, 3050: 0.80, 3051: 0.80, 3052: 0.80, 3053: 0.80, 3054: 0.80,
 3055: 0.96, 3056: 0.80, 3057: 0.96, 3058: 0.80, 3059: 0.80, 3060: 0.96, 3061: 0.80, 3062: 0.80, 3063: 0.80,
}

# Trigger Census rows for US moves of kinds C-H (window: 7 days for a reply, counted from the logged date).
# Category = what the move targeted. C = Economic/Blockade; D, E, F, G, H = Military/Property (placeholder wording).
CENSUS = [
 (3001, "Military/Property", "N", "FONOP at the Paracels, Jan 7, 2019. USNI: China sent ships and aircraft to warn the destroyer off and protested. Routine shadowing plus a protest, not a reply. Re-checked in the W9 audit: USNI's report shows only the warning-off and protest; searched Jan 8-14, none found in allowed outlets."),
 (3002, "Military/Property", "Unverified", "Strait transit Jan 24, 2019, known only from USNI's list of transits. No Chinese reaction was read."),
 (3003, "Military/Property", "Unverified", "Strait transit Feb 25, 2019 (headline and list only). No Chinese reaction was read."),
 (3004, "Military/Property", "Unverified", "Strait transit Mar 24, 2019, known only from USNI's list. No Chinese reaction was read."),
 (3005, "Military/Property", "N", "Strait transit Apr 28, 2019. USNI: Beijing paid 'close attention'; PLA Navy interactions 'safe and professional'. A web search for PLA flights near Taiwan in early May 2019 returned no matching headline. Words only. W9 audit: searched PLA drill / ADIZ / coast-guard action Apr 29-May 5, 2019 again; none found in allowed outlets."),
 (3006, "Military/Property", "N", "FONOP at Gaven and Johnson Reefs, May 6, 2019. USNI: China warned the ships off and protested. Routine shadowing plus a protest. W9 audit: searched PLA drill / ADIZ / coast-guard action May 7-13, 2019; none found in allowed outlets."),
 (3007, "Military/Property", "R-weak", "$2.2B arms sale Jul 8, 2019 -> China's foreign ministry says Jul 13 it 'will impose sanctions on US enterprises' in the sale (event 3008). No firm was named in the report read, so the link is a stated plan, not a confirmed sanction."),
 (3009, "Military/Property", "N", "FONOP at Mischief Reef, Nov 20, 2019. USNI: China's foreign ministry and Southern Theater Command protested; China says its vessels tracked the ships. Words and shadowing. W9 audit: USNI (Nov 22) shows only protests and tracking; searched Nov 21-27, 2019 for a PLA drill, ADIZ spike or coast-guard action; none found in allowed outlets."),
 (3010, "Military/Property", "N", "FONOP at the Paracels, Nov 21, 2019. Same USNI report: protest and tracking only. W9 audit: searched Nov 22-28, 2019; none found in allowed outlets."),
 (3011, "Military/Property", "Unclear", "Two-carrier operations from about Jul 4, 2020. China held drills off the Paracels in early July (before the carriers) and its defense ministry criticised the US on Jul 9. No allowed source ties a PLA action to the carriers. n = 1 for posture (H): very thin evidence."),
 (3012, "Military/Property", "R-weak", "Azar visit Aug 9-10, 2020 -> PLA J-10/J-11 fighters cross the median line on Aug 10 (The War Zone; Taiwan MND). No count and China gave no reason; link plausible."),
 (3014, "Economic/Blockade", "Unclear", "Entity List and visa limits, Aug 26, 2020. A US official told Reuters China fired four medium-range missiles into the South China Sea, but the timing against the listing is unclear and China did not link them (event 3015). The Chinese embassy called the sanctions 'completely unreasonable'. n = 2 for sanctions (C): very thin evidence."),
 (3016, "Military/Property", "Unverified", "Strait transit Aug 30, 2020. USNI reports no Chinese reaction. Not searched further."),
 (3017, "Military/Property", "R-weak", "Krach visit Sept 17-19, 2020 -> Chinese aircraft cross the Strait median line again on Sept 18 (Bloomberg headline only; no count read, visit start date inferred)."),
 (3019, "Military/Property", "R-strong", "$1.8B arms sale (about Oct 21, 2020) -> China announces sanctions on Boeing Defense, Lockheed Martin and Raytheon units on Oct 26 and says it is to uphold national interests (Al Jazeera)."),
 (3021, "Military/Property", "N", "Strait transit Dec 19, 2020. USNI reports no Chinese response; the Shandong carrier transited Dec 20 and the PLA Navy called it normal training. A web search for median-line activity in late Dec 2020 found nothing tied to the transit. W9 audit: USNI says the PLA Navy called the Shandong transit 'normal arrangements' and does not tie it to the transit; searched Dec 20-26, 2020 for a PLA drill, ADIZ spike or coast-guard action; none found in allowed outlets (only routine small ADIZ flights, on non-allowed pages)."),
 (3022, "Military/Property", "Unverified", "Pompeo lifts limits on Taiwan contacts, Jan 9, 2021. AP says only that the move was expected to upset China and reports no Chinese response; no PLA action was searched for Jan 10-16."),
 (3023, "Military/Property", "N", "$100M missile defense upkeep sale Feb 7, 2022 -> China sanctions Lockheed and Raytheon on about Feb 21, which is day 14, outside the 7-day window. Counted N for the window; note the later reply."),
 (3025, "Military/Property", "R-strong", "Pelosi visit Aug 2, 2022 -> large-scale drills in six zones from Aug 4 (3026) and counter-sanctions plus suspended talks on Aug 5 (3027). China ties the response to the visit (NPR, Al Jazeera)."),
 (3028, "Military/Property", "Unclear", "Strait transit Aug 28, 2022 sits inside the post-Pelosi elevated period (WINDOWS), so a reply cannot be separated; the Eastern Theater Command said it was 'on high alert'. Context only."),
 (3029, "Military/Property", "Unclear", "$1.1B arms sale Sept 2, 2022. The Reuters article read reports no Chinese statement; no search of Sept 3-9 was done."),
 (3030, "Economic/Blockade", "N", "Chip export controls Oct 7, 2022. AP (Oct 8): China's foreign ministry criticised them; no counter-measure reported. Days 2-7 not searched."),
 (3031, "Military/Property", "R-strong", "Tsai-McCarthy meeting Apr 5, 2023 -> three-day drills around Taiwan from about Apr 8, with 91 aircraft and 54 crossing the median line on Apr 10 (AFP, which ties the drills to the meeting)."),
 (3033, "Military/Property", "R-weak", "Chung-Hoon/Montreal transit Jun 3, 2023 -> a Chinese destroyer crossed the Chung-Hoon's bow at about 150 yards the same day. China's defense minister blamed US patrols; the link is the transit itself."),
 (3036, "Military/Property", "Unverified", "$345M aid package Jul 28, 2023 (headline only). No Chinese reaction was read."),
 (3037, "Military/Property", "R-strong", "Lai stops in New York (Aug 12) and San Francisco (Aug 16), 2023 -> drills around Taiwan on Aug 19, called a 'stern warning' to separatists colluding with outside forces (Bloomberg). Day 7 from the first stop."),
 (3040, "Military/Property", "R-weak", "First multilateral maritime cooperative activity Apr 7, 2024 -> same-day PLA Southern Theater Command 'joint naval and air combat patrols' (AFP). China did not say it was a reply. n = 1 for allied exercises (G): very thin evidence."),
 (3045, "Military/Property", "Unclear", "$385M arms sale Nov 29, 2024. A 13-firm sanctions round on Dec 5 (day 6) is reported only by an outlet not on the allowed list, so it is not counted. China's counter-sanctions are a known pattern but are not confirmed here."),
 (3046, "Military/Property", "Unclear", "Lai transits Hawaii and Guam (about Nov 30 - Dec 5, 2024). Taiwan's MND reported the largest Chinese maritime movements in decades on Dec 10 (day 10 from Nov 30, after the tour ended Dec 6); Beijing did not acknowledge it. No link and outside the 7-day window as logged."),
 (3050, "Military/Property", "N", "Strait transit Feb 10, 2025. USNI: the Eastern Theater Command tracked it and said it 'sent the wrong signals'. The next PLA live-fire drill (3051) was Feb 26, day 16. Words only inside the window. W9 audit: PLA 'combat alert patrol' training Jan 28-Feb 12, 2025 and a Feb 12 frigate live-fire are reported only by RFA and Chinese state outlets (not allowed), and the training began before the transit, so they are not counted; searched Feb 11-17 for an allowed-outlet report of a PLA drill, ADIZ spike or coast-guard action, none found."),
 (3054, "Military/Property", "Unclear", "FONOP at Scarborough Shoal Aug 13, 2025. China CLAIMS it expelled the ship; the 7th Fleet calls that false. A Chinese coast guard ship and a PLA Navy destroyer collided Aug 11, two days before (3053), so there is no clean separation."),
 (3055, "Military/Property", "N", "US-UK transit Sept 12, 2025. USNI and Stars and Stripes: the Eastern Theater Command tracked it and said it undermined peace. Southern Theater Command patrols Sept 12-13 were linked by China to Philippine patrols, not to this transit. W9 audit: USNI (Sep 16) mentions the carrier Fujian passing through the Strait on Sep 12 during sea trials, with no link to the transit; searched Sep 13-19, 2025 for a PLA drill, ADIZ spike or coast-guard action, none found in allowed outlets."),
 (3056, "Military/Property", "N", "$11.1B arms sale Dec 18, 2025. China's replies came late: sanctions on 20 US defense firms and 10 executives on Dec 26 (day 8, 3057) and 'Justice Mission 2025' drills on Dec 29-30 (day 11, 3058). USNI says the drills protested the sale. Counted N for the strict 7-day window; both later replies are linked in PAIRS."),
 (3059, "Military/Property", "N", "Strait transit Jan 16-17, 2026. USNI: the Eastern Theater Command said it monitored the ships. Taiwan's MND counted 25 sorties on Jan 16 (6 over the median line), a normal level. A web search for late Jan 2026 found no named PLA drill. W9 audit: USNI (Jan 17) reports the Eastern Theater Command only tracked the ships; no drill or coast-guard action tied to the transit; searched Jan 17-23, none found."),
]

# Reply pairs (pair id, trigger, reply, category, reply caused casualties Y/N, note)
PAIRS = [
 (3001, 3007, 3008, "Economic/Blockade", "N", "China says it will sanction US firms five days after the $2.2B Taiwan arms sale (no firm named)"),
 (3002, 3012, 3013, "Military/Property", "N", "PLA fighters cross the median line the day after Azar arrives in Taiwan"),
 (3003, 3017, 3018, "Military/Property", "N", "Chinese aircraft cross the median line again while Krach is in Taiwan (headline only)"),
 (3004, 3019, 3020, "Economic/Blockade", "N", "China sanctions Boeing Defense, Lockheed Martin and Raytheon five days after the $1.8B arms sale"),
 (3005, 3025, 3026, "Military/Property", "N", "Six-zone live-fire drills begin two days after Pelosi arrives"),
 (3006, 3025, 3027, "Economic/Blockade", "N", "Sanctions on Pelosi and suspended talks three days after her visit"),
 (3007, 3031, 3032, "Military/Property", "N", "Three-day drills around Taiwan about three days after the Tsai-McCarthy meeting"),
 (3008, 3033, 3034, "Military/Property", "N", "A Chinese destroyer crosses the Chung-Hoon's bow the same day as the Taiwan Strait transit"),
 (3009, 3037, 3038, "Military/Property", "N", "Drills around Taiwan seven days after Lai's New York stop and the day after his return"),
 (3010, 3040, 3041, "Military/Property", "N", "PLA announces combat patrols the same day as the first allied maritime activity"),
 (3011, 3056, 3057, "Economic/Blockade", "N", "China sanctions 20 US defense firms eight days after the $11.1B arms sale (outside 7 days; the drills are inside)"),
 (3012, 3056, 3058, "Military/Property", "N", "Justice Mission 2025 drills 11 days after the sale announcement; USNI says they protested the sale"),
]

# Elevated-activity stretches whose US moves are context only (approximate end), and the acts that opened them.
WINDOWS = [(d(2022, 8, 4), d(2022, 8, 31))]
START_ACTS = {3026}

# Phases (oldest first)
PHASES = [
 ("Routine transits and FONOPs", d(2019, 1, 7), d(2020, 7, 3), "Strait transits and South China Sea FONOPs answered with protests and shadowing (#3001-#3010); the $2.2B sale and China's sanctions vow (#3007-#3008)"),
 ("Visits, sales and sanctions on arms makers", d(2020, 7, 4), d(2022, 7, 31), "Carriers (#3011), Azar and Krach visits (#3012, #3017), Oct 2020 sale and sanctions (#3019-#3020), Feb 2022 sanctions (#3024)"),
 ("Pelosi crisis", d(2022, 8, 1), d(2022, 8, 31), "Pelosi visit (#3025), six-zone drills (#3026), sanctions and suspended talks (#3027), transit (#3028)"),
 ("Named drills after leader visits", d(2022, 9, 1), d(2024, 12, 31), "Tsai-McCarthy and the April 2023 drills (#3031-#3032), Lai's August 2023 stops (#3037-#3038), Joint Sword 2024A/B (#3042, #3044), talks with Biden (#3035, #3039)"),
 ("Trump second term", d(2025, 1, 1), d(2026, 10, 24), "Transits (#3050, #3055, #3059), Strait Thunder 2025A (#3052), the $11.1B sale, sanctions and Justice Mission 2025 (#3056-#3058), Beijing summit (#3060), July 2026 talks and drills (#3061-#3062)"),
]

CHAIN_NAMES = {
 3007: "Jul 2019 sale -> China vows sanctions on US firms",
 3019: "Oct 2020 sale -> sanctions on Boeing Defense, Lockheed, Raytheon",
 3025: "Pelosi visit -> six-zone drills and sanctions/suspended talks",
 3031: "Tsai-McCarthy meeting -> three-day drills",
 3037: "Lai stopovers -> August 2023 drills",
 3056: "Dec 2025 $11.1B sale -> sanctions -> Justice Mission 2025",
}
