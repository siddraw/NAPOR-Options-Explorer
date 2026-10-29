"""NAPOR Houthis / Red Sea: the record from Jan 1, 2025 to Oct 24, 2026 (research file).

Same source standard as the rest of NAPOR (docs/SOURCE_STANDARD.md):
- Only allowed outlets and official statements. A wire story read on a syndicated page is labelled
  "AP (via ...)". seen="full text" means the article was read; seen="snippet" means only the
  search-result headline was seen (the credibility score discounts that).
- No Houthi media page (al-Masirah, Saba) was opened in this pass. Everything the Houthis say is
  reached through an allowed outlet and written as "Houthis CLAIM ...". If a Houthi page is added
  later, its outlet string must be "al-Masirah (Houthi claim)" (claim-only, scored 0.30).
- IDs 1301-1599 (events and pairs). This file continues the early file (1001-1299, Oct 2016 - Dec 2024).
- US_OPTION tags every US move with its option letter (B talks, C sanctions/designations, D naval
  defense, E interdict Iranian arms, F strike military sites, G strike risking personnel/leaders,
  H force posture). Statements and threats, and events that are not a US move, have no letter.
- Continuous-fighting rule (as for Iran): while the Houthis attack US ships almost every day, a US
  strike has a "reply" by default, so US strikes in the window are context and not counted.
  Windows here: Jan 1 - Jan 19, 2025 (end of the 2024 campaign) and Mar 15 - May 6, 2025
  (Operation Rough Rider).
"""
import datetime as dt


def d(y, m, day):
    return dt.date(y, m, day)


def _s(headline, outlet, published, url, seen="snippet"):
    return {'headline': headline, 'outlet': outlet, 'published': published, 'seen': seen, 'url': url}


# Columns: ID, Date, Actor, Action Type, Target, Detail, Trigger ID, Severity, Confidence, Source
EVENTS = [
(1301, d(2025,1,17), "US", "Sanctions (designation)", "Yemen Kuwait Bank", "Treasury (OFAC) designates Yemen Kuwait Bank for Trade and Investment for financially supporting the Houthis; the bank's US property is blocked", None, "n/a", "Medium", "see audit"),
(1302, d(2025,1,18), "Houthis (CLAIM)", "Claimed attack (US Navy)", "USS Harry S. Truman strike group", "Houthis CLAIM they attacked the Truman carrier strike group on Jan 18; CENTCOM did not respond to the claim and no outlet confirmed an attack", None, "Unknown", "Low", "see audit"),
(1303, d(2025,1,19), "Houthis", "Pause announcement", "Red Sea shipping", "Houthis say they will stop targeting ships other than Israeli-linked ones while the Gaza ceasefire holds, and will restart if Israel resumes attacks; they do not rule out attacks on US and UK targets", None, "n/a", "Medium", "see audit"),
(1304, d(2025,1,22), "Houthis", "Release (ship crew)", "Galaxy Leader crew", "Houthis release the 25 crew of the Galaxy Leader, held since the Nov 2023 seizure; Oman mediated and Hamas asked for the release", None, "25 crew freed", "Medium", "see audit"),
(1305, d(2025,1,22), "US", "Sanctions (terrorist designation order)", "Houthis (Ansar Allah)", "Trump signs Executive Order 14175 starting the process to designate Ansar Allah (the Houthis) a Foreign Terrorist Organization; State must report in 30 days", None, "n/a", "Medium", "see audit"),
(1306, d(2025,3,4), "US", "Sanctions (terrorist designation)", "Houthis (Ansarallah)", "Secretary of State Rubio announces the designation of Ansarallah as a Foreign Terrorist Organization; it takes effect when published in the Federal Register", 1305, "n/a", "Medium", "see audit"),
(1307, d(2025,3,15), "US", "Strike (Houthi military sites)", "Houthi missile, radar, drone and air-defense sites, Yemen", "Operation Rough Rider opens: US air and naval forces hit dozens of Houthi targets; the Houthi-run health ministry CLAIMS at least 31 killed (another spokesman said 53); first US strikes since the Gaza ceasefire of Jan 19", None, "Houthis CLAIM 31-53 killed, mostly civilians (unverified)", "Medium", "see audit"),
(1308, d(2025,3,16), "Houthis (CLAIM)", "Claimed attack (US Navy)", "USS Harry S. Truman strike group, northern Red Sea", "Houthis CLAIM 18 ballistic and cruise missiles and one drone at the Truman group; a US official said the attack failed; CENTCOM's Grynkewich later said the Houthis missed by over 100 miles; Abdul-Malik al-Houthi says they will target US ships while US strikes continue", 1307, "No US damage reported", "Medium", "see audit"),
(1309, d(2025,3,16), "US", "Air defense (drones shot down)", "Houthi attack drones", "A senior defense official says US warships shot down about a dozen Houthi attack drones headed for the Truman group, which was unaffected", 1308, "Drones destroyed (US claim)", "Medium", "see audit"),
(1310, d(2025,3,20), "US", "Force posture (deployment)", "Middle East (Red Sea)", "Hegseth signs orders keeping the Truman carrier in the Middle East at least a month and sends the Carl Vinson from the Pacific, so two carriers are in the region (AP, from a US official)", None, "n/a", "Medium", "see audit"),
(1311, d(2025,4,2), "US", "Sanctions (designation)", "Houthi Russia procurement network", "Treasury (OFAC) sanctions a Houthi network buying Russian weapons and stolen Ukrainian grain, run by Sa'id al-Jamal, plus a ship, two captains and eight crypto wallets", None, "n/a", "Medium", "see audit"),
(1312, d(2025,4,17), "US", "Sanctions (designation)", "International Bank of Yemen", "Treasury (OFAC) sanctions the International Bank of Yemen and three of its senior officers for supporting the Houthis", None, "n/a", "Medium", "see audit"),
(1313, d(2025,4,17), "US", "Strike (fuel port)", "Ras Isa fuel port, Hodeidah (Yemen)", "US strikes the Ras Isa fuel terminal; CENTCOM says it aimed to cut a fuel source for the Houthis; Houthi-run media CLAIM at least 38 killed and 102 wounded and CENTCOM would not comment on civilian deaths", None, "Houthis CLAIM 38+ killed (unverified)", "Medium", "see audit"),
(1314, d(2025,4,27), "US", "Strike (Houthi leaders and infrastructure)", "Houthi leadership and infrastructure, Yemen", "CENTCOM says Rough Rider has hit 800+ targets and killed hundreds of Houthi fighters and 'numerous Houthi leaders', including senior missile and drone officials, to 'disintegrate' the group; it did not name anyone", None, "Hundreds killed (US claim)", "Medium", "see audit"),
(1315, d(2025,4,28), "US", "Strike (reported migrant center)", "Saada, Yemen", "Houthi media CLAIM a US strike hit a Saada detention center for African migrants (35 dead, later 68 per the BBC); AFP could not confirm it and CENTCOM was asked for comment", None, "Houthis CLAIM 35-68 migrants killed (unverified)", "Low", "see audit"),
(1316, d(2025,4,28), "Unknown (Houthis suspected)", "Shootdown (US drones)", "US MQ-9 Reaper drones", "A US official says seven MQ-9 Reapers have gone down since March 15, about $30 million each; he did not say how they were lost", None, "7 drones lost", "Medium", "see audit"),
(1317, d(2025,4,28), "US (accident)", "Aircraft loss (not Houthi fire)", "USS Harry S. Truman", "An F/A-18E Super Hornet and a tow tractor go overboard from the Truman's hangar bay during towing; one sailor lightly hurt; the Navy says it was lost overboard, not shot down", None, "1 jet lost; 1 sailor injured", "Medium", "see audit"),
(1318, d(2025,5,6), "US (accident)", "Aircraft loss (not Houthi fire)", "USS Harry S. Truman", "A second F/A-18E goes overboard when the arresting gear fails; both pilots eject and are rescued; Pentagon says it was not struck by the Houthis; two officials say the carrier had turned sharply to avoid Houthi fire", None, "1 jet lost; pilots hurt lightly", "Medium", "see audit"),
(1319, d(2025,5,6), "US/Houthis", "Diplomatic talks (ceasefire, Oman)", "Houthis", "Trump says the US will stop bombing the Houthis 'effective immediately'; Oman says neither side will target the other, including US ships, in the Red Sea and Bab al-Mandab; the State Dept says it does not cover the Israel-Houthi conflict; US stand-down ordered May 5", None, "n/a", "Medium", "see audit"),
(1320, d(2025,7,6), "Houthis (claimed)", "Strike (shipping)", "Magic Seas (Greek-operated, Liberian flag), Red Sea", "Small boats, then missiles and drones hit the bulk carrier Magic Seas; the crew abandons ship and is rescued; the ship sinks; the Houthis claimed it", None, "Ship sunk; crew rescued", "Medium", "see audit"),
(1321, d(2025,7,7), "Houthis (claimed)", "Strike (shipping)", "Eternity C (Greek-owned, Liberian flag), Red Sea", "Eternity C is attacked for hours and sinks on Jul 9; Reuters reports at least 4 killed and 15 missing early on, with 6 rescued; USNI later counts at least 9 dead, the Houthis' deadliest attack; the Houthis claimed it", None, "At least 4 killed early; at least 9 per USNI", "Medium", "see audit"),
(1322, d(2025,7,9), "US", "Diplomatic statement", "Houthis", "State Dept spokesperson Tammy Bruce says the attacks show the threat from the Iran-backed Houthis; the US Mission to Yemen accuses the Houthis of holding surviving crew and demands their release", 1321, "n/a", "Medium", "see audit"),
(1323, d(2025,7,16), "Yemeni National Resistance Forces (CENTCOM announcement)", "Seizure (Iranian arms, Yemeni partners)", "Iranian arms bound for the Houthis", "CENTCOM announces Yemen's National Resistance Forces seized 750+ tons of Iranian weapons bound for the Houthis (hundreds of missiles, drone engines, radar); the release describes no direct US military role; also relevant to the Iran log's arms-seizure rows (#264, #265)", None, "Cargo seized", "Medium", "see audit"),
(1324, d(2025,7,22), "US", "Sanctions (designation)", "Houthi petroleum smuggling network", "Treasury (OFAC) sanctions 2 people and 5 companies for Houthi-linked petroleum smuggling and money laundering", None, "n/a", "Medium", "see audit"),
(1325, d(2025,8,31), "Houthis (claimed)", "Strike (shipping, missed)", "Scarlet Ray (Liberian flag), Red Sea", "UKMTO reports an unknown projectile splashing close to the ship on Aug 31; the Houthis announce the attack on Sep 1; the missile missed and all crew are safe", None, "No damage", "Medium", "see audit"),
(1326, d(2025,9,11), "US", "Sanctions (designation)", "Houthi revenue and procurement networks", "Treasury (OFAC) designates 32 people and companies and identifies 4 ships, its largest action against the Houthis so far", None, "n/a", "Medium", "see audit"),
(1327, d(2025,9,29), "Houthis (claimed)", "Strike (shipping)", "Minervagracht (Dutch-flagged), Gulf of Aden", "Houthi cruise missile sets the empty cargo ship on fire; crew airlifted off; two crew hurt and one later dies; the Houthis said the owner broke their ban on calling at Israeli ports", None, "1 crew killed, 1 injured", "Medium", "see audit"),
(1328, d(2025,11,11), "Houthis", "Pause signal", "Israel and Red Sea shipping", "In a letter to Hamas the Houthi chief of staff signals attacks have stopped since the Gaza ceasefire of Oct 10 and warns they will return if Israel resumes the war; last attack was Sep 29", None, "n/a", "Medium", "see audit"),
(1329, d(2026,1,16), "US", "Sanctions (designation)", "Houthi smuggling and revenue networks", "Treasury (OFAC) sanctions 21 people and companies and identifies one ship over Houthi oil sales, weapons buying and finance", None, "n/a", "Medium", "see audit"),
(1330, d(2026,2,28), "Houthis", "Threat (shipping and Israel)", "Red Sea and Israel", "Two senior Houthi officials tell Reuters the group will restart missile and drone attacks on main shipping routes and on Israel in support of Iran, as soon as that night; no formal announcement", None, "n/a", "Medium", "see audit"),
(1331, d(2026,7,20), "Houthis", "Threat (declared Saudi port embargo)", "Saudi Arabia, Red Sea / Bab al-Mandab", "Houthi military spokesman Yahya Saree declares a 'maritime embargo' (naval blockade) of Saudi Arabia, effective immediately, in a televised statement on Monday Jul 20 (Reuters, AAP); a declaration, not an attack on a ship", None, "n/a", "Medium", "see audit"),
(1332, d(2026,7,21), "US", "Diplomatic statement (threat)", "Houthis", "Asked on Tuesday Jul 21 about the blockade threat, Trump says 'If something like that happens, we take care of it' (AFP, Jul 21)", 1331, "n/a", "Medium", "see audit"),
(1333, d(2026,7,22), "Houthis (claimed)", "Strike (shipping)", "Saudi tanker Encelia, Red Sea", "Saudi Arabia confirms the Encelia was hit; the Houthis CLAIM missile and drone strikes on it and the tanker Layla; UKMTO reports another tanker hit by an unknown projectile 70 nm southwest of Al Shuqaiq", 1331, "Fire on a tanker; no deaths reported", "Medium", "see audit"),
(1334, d(2026,7,23), "US", "Diplomatic statement (threat)", "Houthis and Iran", "Trump posts that 'major military punishment will be inflicted upon Iran and, of course, the Houthis themselves' if the attacks go on, and says he is 'very disappointed' in them", 1333, "n/a", "Medium", "see audit"),
(1335, d(2026,9,10), "US", "Force posture (advisers)", "Saudi Arabia", "CNN, from five sources, reports 100+ US military advisers (a US official says about 200 troops) in Saudi Arabia giving intelligence and targeting support against the Houthis; they do not join strikes or refuel jets; DoD does not comment on intelligence", None, "n/a", "Medium", "see audit"),
(1336, d(2026,9,10), "US", "Declined request (no strike)", "Houthis", "Per Axios (relayed by AFP), Saudi Crown Prince Mohammed bin Salman phones Trump twice asking for US strikes on the Houthis and Trump declines; on Sep 12 Trump says 'The Houthis called us and they don't want to fight with us'", None, "n/a", "Medium", "see audit"),
(1337, d(2026,9,13), "US/Houthis", "Diplomatic talks (Muscat)", "Houthi representatives", "Reuters, from sources, says US embassy staff met Houthi officials (incl. Mohammad Abdulsalam) at the US Embassy in Muscat on the weekend of Sep 12-13, helped by Oman; the Houthis said they would not attack US ships and kept to the 2025 ceasefire; State did not confirm; VP Vance said Monday the US is in direct contact", None, "n/a", "Medium", "see audit"),
(1338, d(2026,10,4), "Saudi-backed Yemeni government forces", "Offensive (ground and air)", "Houthi-held areas incl. Mocha and Mayyun island", "The 'Dawn of Yemen' offensive begins; Al Jazeera says US media report US intelligence sharing, target identification and planning help; Saudi-Houthi front, context for the US options", None, "Casualty figures unverified", "Medium", "see audit"),
(1339, d(2026,10,8), "Houthis (Iran-backed)", "Strike (proxy front)", "Riyadh airport (Saudi Arabia)", "Also Iran log #98. Houthi attack on Riyadh's King Khalid airport earlier in the week of Oct 10 kills three Saudis including a pilot (date Oct 8 as in the Iran log; NPR says 'earlier that week')", None, "3 Saudis killed", "Medium", "see audit"),
(1340, d(2026,10,10), "Houthis (Iran-backed)", "Strike (proxy front)", "Riyadh airport (Saudi Arabia)", "Also Iran log #102. A missile hits the domestic terminals; Saudi civil aviation says 12 killed (incl. one American) and 309 wounded; 291+ flights cancelled", 1339, "12 killed, 309 wounded (Saudi GACA via Al Jazeera)", "Medium", "see audit"),
(1341, d(2026,10,10), "US", "Diplomatic statement (threat)", "Houthis", "Asked about joining Saudi strikes, Trump says 'We may. We're going to look at it'; Secretary of State Rubio confirms an American was among the dead", 1340, "n/a", "Medium", "see audit"),
(1342, d(2026,10,12), "Houthis", "Threat (US)", "US forces and interests", "Houthi politburo member Mohammed al-Bukhaiti tells AFP that if the US joins the campaign the Houthis will answer at once, with 'a swift and painful response' on the US and its interests in the region", 1341, "n/a", "Medium", "see audit"),
(1343, d(2026,10,13), "US", "Diplomatic statement", "Houthis", "Trump says the Houthis are 'behaving very badly' and he might ask Turkish President Erdogan to step in on Saudi Arabia's behalf (Reuters via Times of Israel)", None, "n/a", "Medium", "see audit"),
# --- weekly update 2026-10-26 (weekly agent): news Oct 14-26. No US strike on the Houthis and no
# Houthi attack on US forces or on non-Saudi shipping was found. ---
(1344, d(2026,10,18), "US", "Diplomatic statement (security alerts)", "US citizens in the region", "US embassies in Bahrain, Iraq, Israel, Jordan, Kuwait, Lebanon, Oman, Qatar and the UAE issue coordinated alerts that Houthi hostilities 'have the potential to escalate rapidly'; the embassy in Saudi Arabia follows on Oct 19 warning of attacks on airports (ABC calls the wave unprecedented)", None, "n/a", "Medium", "see audit"),
(1345, d(2026,10,20), "Unknown (Houthis suspected)", "Strike (proxy front)", "Shaybah oilfield (Saudi Arabia)", "Saudi air defences stop a drone aimed at Saudi Aramco's Shaybah oilfield; the energy ministry does not say who launched it; Reuters and CBS report it among Houthi attacks on Saudi Arabia", None, "2 killed, 2 injured by falling debris (Saudi energy ministry via CBS, Reuters)", "Medium", "see audit"),
(1346, d(2026,10,21), "Houthis (Iran-backed)", "Strike (proxy front)", "Dammam airport (Saudi Arabia)", "Attack on King Fahd International Airport in Dammam (Reuters, Oct 21); Al Jazeera lists Dammam airport among recent Houthi targets", None, "1 killed, 8 injured (Saudi civil aviation authority via Reuters)", "Medium", "see audit"),
(1347, d(2026,10,21), "US", "Diplomatic precaution (ordered departure)", "US embassy and consulates, Saudi Arabia", "State orders non-emergency US government staff and families to leave Saudi Arabia, saying the 'Iranian-supported Houthis have increasingly engaged in hostilities against Saudi Arabia'; officials say families will also leave other Gulf missions and the military is quietly reducing its footprint (CBS, Reuters)", 1345, "n/a", "Medium", "see audit"),
(1348, d(2026,10,24), "Houthis (CLAIM)", "Strike (proxy front, claimed)", "Saudi Arabia and Aden", "Houthis CLAIM missile and drone attacks on Riyadh airport, Dammam, Najran, Khamis Mushait, oil pipelines and Aden; Saudi Arabia says it intercepted missiles aimed at Taif and Yanbu; Saudi-led jets bomb Marib, Taiz and other provinces", None, "Not stated for the claimed attacks", "Medium", "see audit"),
(1349, d(2026,10,26), "Saudi-led coalition", "Air defense and strike", "Houthi missile launchers, Sanaa", "Saudi-led forces say they intercepted a Houthi ballistic missile aimed at Riyadh and destroyed two launchers in Sanaa; Riyadh airport had reopened two terminals on Oct 25 and the Houthis warned airlines against using it", None, "Not stated", "Medium", "see audit"),
]

# Who made each US move: option letters (B talks, C sanctions, D naval defense, E arms interdiction,
# F strike military sites, G strike risking personnel/leaders, H force posture)
US_OPTION = {
    1301: "C", 1305: "C", 1306: "C", 1311: "C", 1312: "C", 1324: "C", 1326: "C", 1329: "C",
    1307: "F", 1313: "F", 1315: "F",
    1314: "G",
    1309: "D",
    1310: "H", 1335: "H",
    1319: "B", 1337: "B",
}

# --- sources -------------------------------------------------------------------------------------
_USNI_JAN22 = _s('Houthis Release Galaxy Leader Crew; Trump Designates Group a Foreign Terrorist Organization', 'USNI News', '2025-01-22', 'https://news.usni.org/2025/01/22/houthis-release-galaxy-leader-crew-trump-designates-group-a-foreign-terrorist-organization', 'full text')
_USNI_MAR16 = _s('Houthis Attempt Attack on Carrier Harry S. Truman After U.S. Strikes in Yemen', 'USNI News', '2025-03-16', 'https://news.usni.org/2025/03/16/houthis-claim-to-attack-carrier-harry-s-truman-after-u-s-strikes-in-yemen', 'full text')
_USNI_RR = _s('Operation Rough Rider', 'USNI News', '2025-04-29', 'https://news.usni.org/2025/04/29/operation-rough-rider', 'full text')
_USNI_2025 = _s('Top Stories 2025: Operations in the Middle East, U.S. Southern Command', 'USNI News', '2026-01-02', 'https://news.usni.org/2026/01/02/top-stories-2025-operations-in-the-middle-east-u-s-southern-command', 'full text')
_ABC_MAR15 = _s('Trump orders attacks against Houthis in Yemen', 'ABC News (via 6abc)', '2025-03-17', 'https://6abc.com/amp/post/trump-yemen-today-iran-denies-aiding-houthi-rebels-president-donald-strikes-threats/16031988/', 'full text')
_AJ_MAY6 = _s('Trump says bombing of Yemen to stop as Oman confirms US-Houthi ceasefire', 'Al Jazeera', '2025-05-06', 'https://www.aljazeera.com/news/2025/5/6/trump-says-bombing-of-yemen-to-stop-as-oman-confirms-us-houthi-ceasefire', 'full text')
_AJ_JUL9 = _s('Six rescued, 15 missing after Houthi attack on cargo ship in Red Sea', 'Al Jazeera', '2025-07-09', 'https://www.aljazeera.com/amp/news/2025/7/9/five-rescued-after-suspected-attack-by-yemens-houthis-on-red-sea-vessel', 'full text')
_AFP_AHRAM_0723A = _s('Houthis target Red Sea shipping as US hits Iran', 'AFP (via Ahram Online)', '2026-07-23', 'https://english.ahram.org.eg/News/573354.aspx', 'full text')
_AFP_AHRAM_0723B = _s('Trump threatens Houthis with major military punishment', 'AFP (via Ahram Online)', '2026-07-23', 'https://english.ahram.org.eg/News/573387.aspx', 'full text')
_AJ_OCT11 = _s('Yemen fighting expands as Houthis attack Saudi airport: What to know', 'Al Jazeera', '2026-10-11', 'https://www.aljazeera.com/news/2026/10/11/yemen-fighting-expands-as-houthis-attack-saudi-airport-what-to-know', 'full text')
_NPR_OCT10 = _s('Trump weighs joining the fight against Houthis after Riyadh airport attack', 'NPR (via KUNC)', '2026-10-10', 'https://www.kunc.org/npr-news/2026-10-10/trump-weighs-joining-the-fight-against-houthis-after-riyadh-airport-attack', 'full text')
_TREAS = lambda h, dt_, n: _s(h, 'Treasury (OFAC)', dt_, f'https://home.treasury.gov/news/press-releases/{n}', 'full text')

_ABC_OCT20 = _s('Trump admin sees escalating risk from Houthis, prompting unprecedented wave of warnings', 'ABC News', '2026-10-20', 'https://abcnews.com/Politics/trump-admin-sees-escalating-risk-houthis-prompting-unprecedented/story?id=137397953', 'full text')
_CBS_OCT21 = _s('US orders some diplomats to leave Saudi Arabia amid Houthi attacks', 'CBS News', '2026-10-21', 'https://www.cbsnews.com/news/us-saudi-arabia-ordered-departure-houthis/', 'full text')
_RTR_OCT21 = _s('US orders departure of diplomats from Saudi Arabia amid Houthi strikes', 'Reuters (via Internazionale)', '2026-10-21', 'https://www.internazionale.it/ultime-notizie-reuters/2026/10/21/exclusive-us-preparing-to-issue-ordered-departure-of-some-personnel-from-gulf-embassies-us-officials', 'full text')
_AJ_OCT24 = _s("Iran says won't allow US warships to get close as Trump ponders new attacks", 'Al Jazeera', '2026-10-24', 'https://www.aljazeera.com/news/2026/10/24/iran-says-wont-allow-us-warships-to-get-close-as-trump-ponders-new-attacks', 'full text')
_CBS_LIVE_OCT26 = _s('Trump says he\'s weighing deal with Iran against action to "finish them off"', 'CBS News', '2026-10-26', 'https://www.cbsnews.com/live-updates/iran-war-trump-us-oil-gas-prices-strait-of-hormuz-midterms/', 'full text')

SOURCES = {
 1301: [_TREAS('Treasury Increases Financial Pressure on the Houthis', '2025-01-17', 'jy2794')],
 1302: [_USNI_JAN22],
 1303: [_s("Yemen's Houthis say they'll limit their attacks in the Red Sea corridor", 'AP (via ClickOnDetroit)', '2025-01-20', 'https://www.clickondetroit.com/news/world/2025/01/20/yemens-houthis-say-theyll-limit-their-attacks-in-the-red-sea-corridor/', 'full text'),
        _s("With Gaza ceasefire, Yemen's Houthi rebels halt attacks on ships in the Red Sea", 'NPR (via KUNC)', '2025-01-29', 'https://www.kunc.org/2025-01-29/with-gaza-ceasefire-yemens-houthi-rebels-halt-attacks-on-ships-in-the-red-sea')],
 1304: [_USNI_JAN22],
 1305: [_s('Executive Order 14175: Designation of Ansar Allah as a Foreign Terrorist Organization', 'White House (via The American Presidency Project)', '2025-01-22', 'https://www.presidency.ucsb.edu/documents/executive-order-14175-designation-ansar-allah-foreign-terrorist-organization', 'full text'),
        _USNI_JAN22],
 1306: [_s('Designation of Ansarallah as a Foreign Terrorist Organization', 'State Department (via GlobalSecurity)', '2025-03-04', 'https://www.globalsecurity.org/security/library/news/2025/03/sec-250304-state01.htm', 'full text'),
        _s('Trump administration again labels the Houthis a foreign terrorist organization', 'AP (via GPB)', '2025-03-04', 'https://www.gpb.org/news/2025/03/04/trump-administration-again-labels-the-houthis-foreign-terrorist-organization')],
 1307: [_ABC_MAR15, _USNI_MAR16],
 1308: [_USNI_MAR16, _ABC_MAR15, _USNI_RR],
 1309: [_USNI_MAR16],
 1310: [_s('Hegseth beefs up warship presence in the Middle East and will have 2 aircraft carriers in the region', 'AP (via WSLS)', '2025-03-21', 'https://www.wsls.com/news/politics/2025/03/21/hegseth-beefs-up-warship-presence-in-the-middle-east-and-will-have-2-aircraft-carriers-in-the-region/', 'full text')],
 1311: [_TREAS('Treasury Sanctions Houthi Network Procuring Weapons and Commodities from Russia', '2025-04-02', 'sb0068')],
 1312: [_TREAS('Treasury sanctions International Bank of Yemen', '2025-04-17', 'sb0092')],
 1313: [_s('Houthis report at least 38 killed in US airstrikes on Yemen oil port', 'Times of Israel', '2025-04-18', 'https://www.timesofisrael.com/houthis-report-at-least-38-killed-in-us-airstrikes-on-yemen-oil-port/', 'full text'), _USNI_RR],
 1314: [_USNI_RR, _s('Houthis say U.S. strike in Yemen hits migrant detention center in Saada, killing at least 35', 'CBS News (AFP report)', '2025-04-28', 'https://www.cbsnews.com/amp/news/houthis-us-strikes-yemen-saada-migrant-detention-center-deaths', 'full text')],
 1315: [_s('Houthis say U.S. strike in Yemen hits migrant detention center in Saada, killing at least 35', 'CBS News (AFP report)', '2025-04-28', 'https://www.cbsnews.com/amp/news/houthis-us-strikes-yemen-saada-migrant-detention-center-deaths', 'full text'), _USNI_RR],
 1316: [_s('US loses 7 multimillion dollar drones in Yemen area since mid-March', 'AFP (via Arab News)', '2025-04-28', 'https://www.arabnews.com/node/2598827/middle-east', 'full text')],
 1317: [_s('For second time in 8 days, U.S. fighter jet assigned to USS Truman is lost in Red Sea', 'CBS News', '2025-05-07', 'https://www.cbsnews.com/amp/philadelphia/news/u-s-fighter-jet-assigned-to-uss-truman-lost-red-sea-second-time', 'full text'),
        _s('US loses 7 multimillion dollar drones in Yemen area since mid-March', 'AFP (via Arab News)', '2025-04-28', 'https://www.arabnews.com/node/2598827/middle-east', 'full text')],
 1318: [_s('For second time in 8 days, U.S. fighter jet assigned to USS Truman is lost in Red Sea', 'CBS News', '2025-05-07', 'https://www.cbsnews.com/amp/philadelphia/news/u-s-fighter-jet-assigned-to-uss-truman-lost-red-sea-second-time', 'full text')],
 1319: [_AJ_MAY6, _s('U.S. Stops Houthi Bombing Campaign on Presidential Orders', 'USNI News', '2025-05-06', 'https://news.usni.org/?p=115832', 'full text')],
 1320: [_AJ_JUL9, _USNI_2025],
 1321: [_AJ_JUL9, _USNI_2025],
 1322: [_AJ_JUL9],
 1323: [_s('Yemeni partners successfully interdict massive Iranian weapons shipment bound for Houthis', 'CENTCOM', '2025-07-16', 'https://www.centcom.mil/MEDIA/PRESS-RELEASES/Press-Release-View/Article/4246960/yemeni-partners-successfully-interdict-massive-iranian-weapons-shipment-bound-f/', 'full text')],
 1324: [_TREAS('Treasury Sanctions Houthi-Linked Petroleum Smuggling and Sanctions Evasion Network', '2025-07-22', 'sb0203')],
 1325: [_s('Houthis say they shot at Israeli ship in Red Sea; maritime agency says missile missed', 'Times of Israel', '2025-09-01', 'https://www.timesofisrael.com/houthis-say-they-shot-at-israeli-ship-in-red-sea-maritime-agency-says-missile-missed/', 'full text')],
 1326: [_TREAS('Treasury Sanctions Houthi Illicit Revenue and Procurement Networks', '2025-09-11', 'sb0243')],
 1327: [_s('Houthis Attack Dutch Ship in the Red Sea', 'USNI News', '2025-10-02', 'https://news.usni.org/2025/10/02/houthis-attack-dutch-ship-in-the-red-sea', 'full text'),
        _s("Yemen's Houthi rebels signal that they've stopped attacks on Israel and ships in the Red Sea", 'AP (via ClickOnDetroit)', '2025-11-11', 'https://www.clickondetroit.com/news/world/2025/11/11/yemens-houthi-rebels-signal-that-theyve-stopped-attacks-on-israel-and-ships-in-the-red-sea/', 'full text')],
 1328: [_s("Yemen's Houthi rebels signal that they've stopped attacks on Israel and ships in the Red Sea", 'AP (via ClickOnDetroit)', '2025-11-11', 'https://www.clickondetroit.com/news/world/2025/11/11/yemens-houthi-rebels-signal-that-theyve-stopped-attacks-on-israel-and-ships-in-the-red-sea/', 'full text'), _USNI_2025],
 1329: [_TREAS('Treasury Increases Pressure on Houthi Smuggling and Illicit Revenue Generation Networks', '2026-01-16', 'sb0366')],
 1330: [_s('US-Israel strike on Iran: Houthis warn of imminent missile and drone attacks in Red Sea corridor', 'Reuters (via Business Today)', '2026-02-28', 'https://www.businesstoday.in/amp/world/middle-east/story/us-israel-strike-on-iran-houthis-warn-of-imminent-missile-and-drone-attacks-in-red-sea-corridor-518464-2026-02-28', 'full text')],
 1331: [_s("Yemen's Houthis say they will impose naval blockade against Saudi Arabia", 'Reuters (via The Star)', '2026-07-20', 'https://www.thestar.com.my/news/world/2026/07/20/yemen039s-houthis-declare-naval-blockade-against-saudi-arabia---statement', 'full text'),
        _s('Houthis declare naval blockade against Saudi Arabia', 'AAP (via Newcastle Herald)', '2026-07-20', 'https://www.newcastleherald.com.au/story/9314342/houthis-declare-naval-blockade-against-saudi-arabia/', 'full text'),
        _AFP_AHRAM_0723A],
 1332: [_s("Trump says will 'take care of' Houthis if they blockade Saudi ports", 'AFP (via Ahram Online)', '2026-07-21', 'https://english.ahram.org.eg/News/573280.aspx', 'full text')],
 1333: [_AFP_AHRAM_0723A, _AFP_AHRAM_0723B],
 1334: [_AFP_AHRAM_0723B],
 1335: [_s('Exclusive: US expands intel, targeting support for Saudi campaign against Iranian ally', 'CNN (via KEYT)', '2026-09-10', 'https://keyt.com/politics/cnn-us-politics/2026/09/10/exclusive-us-expands-intel-targeting-support-for-saudi-campaign-against-iranian-ally/', 'full text')],
 1336: [_s('Houthis tell US to stay out as Red Sea corridor grip tightens, Trump says', 'AFP (via Malay Mail)', '2026-09-12', 'https://www.malaymail.com/news/world/2026/09/12/houthis-tell-us-to-stay-out-as-red-sea-corridor-grip-tightens-trump-says/234980', 'full text')],
 1337: [_s('U.S. officials met Iran-backed Houthis in Oman over the weekend, sources say', 'Reuters (via Internazionale)', '2026-09-16', 'https://www.internazionale.it/ultime-notizie-reuters/2026/09/16/u-s-officials-met-iran-backed-houthis-in-oman-over-the-weekend-sources-say', 'full text'),
        _s('Yemeni forces target Houthis and a Saudi base as US rules out direct role', 'Al Jazeera', '2026-09-17', 'https://www.aljazeera.com/amp/news/2026/9/17/yemeni-forces-target-houthis-and-a-saudi-base-as-us-rules-out-direct-role', 'full text')],
 1338: [_AJ_OCT11],
 1339: [_NPR_OCT10, _AJ_OCT11],
 1340: [_AJ_OCT11, _NPR_OCT10],
 1341: [_NPR_OCT10, _AJ_OCT11],
 1342: [_s("Houthi official warns of 'swift, painful response' if US enters Yemen war", 'AFP (via Times of Israel)', '2026-10-12', 'https://www.timesofisrael.com/liveblog_entry/houthi-official-warns-of-swift-painful-response-if-us-enters-yemen-war/', 'full text')],
 1343: [_s("Trump says Yemen's Houthis are 'behaving very badly,' may ask Erdogan to intervene", 'Reuters (via Times of Israel)', '2026-10-13', 'https://www.timesofisrael.com/liveblog_entry/trump-says-yemens-houthis-are-behaving-very-badly-may-ask-erdogan-to-intervene/', 'full text')],
 # weekly update 2026-10-26: every URL came from a search result or fetch in that session
 1344: [_ABC_OCT20],
 1345: [_CBS_OCT21, _RTR_OCT21],
 1346: [_RTR_OCT21, _AJ_OCT24],
 1347: [_CBS_OCT21, _RTR_OCT21],
 1348: [_CBS_LIVE_OCT26, _AJ_OCT24],
 1349: [_CBS_LIVE_OCT26],
}
VERDICT = {k: 'confirmed' for k in SOURCES}
VERDICT[1302] = 'not_confirmed'   # only a Houthi claim, relayed by USNI; CENTCOM did not respond
# Rows where an allowed outlet confirms the event but not every detail in the row.
PARTLY = {1315, 1316, 1345}   # 1331/1332 re-sourced 2026-10-25 (Reuters, AAP, AFP give the dates)

# Trigger Census rows for US moves of kinds C-H.
# Category = what the move cost the other side; status as in data.py (R-strong, R-weak, R-proxy, N, Unclear, Unverified).
# Moves inside a continuous-fighting window (Mar 15 - May 6, 2025) are "Unclear": the Houthis were
# already firing at US ships, so a reply cannot be told apart from the fighting.
CENSUS = [
 (1301, "Economic/Blockade", "Unverified", "Yemen Kuwait Bank designation, Jan 17, 2025. The Houthis CLAIM they attacked the Truman group on Jan 18 (USNI); CENTCOM did not respond and no outlet confirmed it. They announced their pause on Jan 19 (AP)."),
 (1305, "Economic/Blockade", "N", "EO 14175, Jan 22, 2025. No Houthi attack on US forces or shipping found Jan 23-27: the Houthis were in their Gaza-ceasefire pause (AP Jan 20; USNI Jan 22). UKMTO had logged no Houthi attacks on shipping since the ceasefire as of Mar 16 (USNI)."),
 (1306, "Economic/Blockade", "N", "FTO designation announced Mar 4, 2025. No Houthi attack found Mar 5-9; USNI (Mar 16) says UKMTO had logged no attacks on shipping since the ceasefire and that Mar 15 were the first US strikes since Jan 19."),
 (1307, "Military/Property", "R-strong", "Operation Rough Rider opening strikes, Mar 15, 2025 -> Houthis CLAIM 18 missiles and a drone at the Truman group on Mar 16; the US official said it failed. Abdul-Malik al-Houthi said they will target US ships while the US strikes (USNI)."),
 (1309, "Military/Property", "Unclear", "US warships shoot down about a dozen drones, Mar 16, 2025. Inside the Mar 15 - May 6 window; this is the defence against the Houthi attack, not a separate trigger."),
 (1310, "Military/Property", "Unclear", "Second carrier ordered, Mar 20, 2025. Inside the Mar 15 - May 6 window: the Houthis were already attacking, so a reply cannot be separated."),
 (1311, "Economic/Blockade", "Unclear", "Russia-procurement network sanctions, Apr 2, 2025. Inside the Mar 15 - May 6 window (continuous fighting), so a reply cannot be separated."),
 (1312, "Economic/Blockade", "Unclear", "International Bank of Yemen sanctions, Apr 17, 2025. Inside the window (continuous fighting)."),
 (1313, "Military/Property", "Unclear", "Ras Isa strike, Apr 17, 2025. Inside the window: a US strike there is context, not counted."),
 (1314, "Personnel/Casualty", "Unclear", "CENTCOM statement on hitting Houthi leaders, Apr 27, 2025. Inside the window; context only."),
 (1315, "Personnel/Casualty", "Unclear", "Reported Saada strike, Apr 28, 2025. Inside the window; the strike itself is a Houthi claim that AFP could not confirm."),
 (1324, "Economic/Blockade", "N", "Petroleum-network sanctions, Jul 22, 2025. No Houthi attack found Jul 23-27; next found Aug 31 (Scarlet Ray)."),
 (1326, "Economic/Blockade", "N", "32-target sanctions, Sep 11, 2025. No Houthi attack found Sep 12-16; the next found was Minervagracht on Sep 29 (AP, USNI), 18 days later."),
 (1329, "Economic/Blockade", "N", "21-target sanctions, Jan 16, 2026. No Houthi attack on US forces or shipping found Jan 17-21; AFP says the Houthis were relatively restrained until the Iran war began."),
 (1335, "Military/Property", "N", "US advisers in Saudi Arabia, reported by CNN on Sep 10, 2026 (anonymous sources; DoD would not comment). No Houthi attack on US forces or US-linked shipping found Sep 11-15; Houthi fire in that period was on Saudi targets."),
]

# Reply pairs (pair id, trigger, reply, category, reply caused casualties Y/N, note)
PAIRS = [
 (1301, 1307, 1308, "Military/Property", "N", "Houthis CLAIM a missile and drone attack on the Truman group the day after the opening strikes; the US said it failed"),
 (1302, 1308, 1309, "Military/Property", "N", "US warships shoot down about a dozen Houthi drones headed for the Truman group the same day"),
 (1303, 1339, 1340, "Personnel/Casualty", "Y", "Second, deadlier Houthi attack on Riyadh airport two days later (Iran log #98 -> #102)"),
 (1304, 1340, 1341, "Personnel/Casualty", "N", "Trump says the US may join Saudi strikes after the Oct 10 attack; Rubio confirms an American died"),
 (1305, 1341, 1342, "Personnel/Casualty", "N", "Houthi official warns of a swift response on the US if it joins; a threat, no attack on US forces found"),
]

# Continuous-fighting windows (US strikes inside are context only) and the acts that started them.
# Continues the early file's window (Jan 12 - Dec 31, 2024): the Houthis paused on Jan 19, 2025.
WINDOWS = [(d(2025, 1, 1), d(2025, 1, 19)), (d(2025, 3, 15), d(2025, 5, 6))]
START_ACTS = {1307}

# Periods when an option was limited: (start, end, text, [event ids])
# (The Jan 19 - Mar 14, 2025 Houthi pause is a phase, not a US constraint: strikes stayed available.)
CONSTRAINTS = [
 (d(2025, 5, 6), d(2026, 10, 26), "Oman-brokered US-Houthi ceasefire: the US stopped striking the Houthis and the Houthis said they would not target US ships, so strikes (F/G) were limited. No US strike on the Houthis was found after May 6, 2025 in the searches for this file; the Houthis told US officials in Sep 2026 they still keep the ceasefire (Reuters).", [1319, 1337]),
 (d(2026, 9, 10), d(2026, 10, 26), "Saudi-Houthi war: Trump declined Saudi requests for US strikes (Axios via AFP, Sep 10) and US help was limited to intelligence and targeting advice, with no US strikes or refuelling (CNN). CNN also says US forces are stretched by the Iran conflict. Trump said on Oct 10 'We may' join; no decision found by Oct 26, and ABC (Oct 20) says the administration is wary of opening a second front.", [1335, 1336, 1341, 1344]),
]

# Phases (oldest first)
PHASES = [
 ("End of the 2024 campaign", d(2025, 1, 1), d(2025, 1, 18), "Last weeks of the Red Sea campaign; the Houthis CLAIM a Jan 18 attack on the Truman group (#1302)"),
 ("Gaza-ceasefire pause", d(2025, 1, 19), d(2025, 3, 14), "Houthis pause (#1303), free the Galaxy Leader crew (#1304); Trump's order and the FTO designation (#1305, #1306)"),
 ("Operation Rough Rider", d(2025, 3, 15), d(2025, 5, 6), "Daily US strikes from #1307; Houthi attacks on US warships; ends with the Oman-brokered ceasefire (#1319)"),
 ("US-Houthi ceasefire, attacks on other ships", d(2025, 5, 7), d(2025, 10, 9), "Magic Seas and Eternity C sunk (#1320, #1321); sanctions rounds; Minervagracht (#1327)"),
 ("Gaza-ceasefire lull", d(2025, 10, 10), d(2026, 2, 27), "No Houthi attacks logged after Sep 29; Houthis signal the pause (#1328); Treasury round (#1329)"),
 ("Iran war and Saudi-Houthi front", d(2026, 2, 28), d(2026, 10, 26), "Houthis threaten a restart (#1330), blockade Saudi ports (#1331), Riyadh airport attacks (#1339, #1340); US threats, advisers and Muscat talks (#1334, #1335, #1337)"),
]

CHAIN_NAMES = {
 1307: "Rough Rider opening -> Houthi attack on Truman -> drones shot down",
 1339: "Riyadh airport attacks -> Trump weighs joining -> Houthi warning",
 1331: "Saudi blockade -> tanker hit -> Trump threat",
}


# --- credibility estimate (same formula as napor/napor_ids.py, for spot-checks) --------------------
def _estimate(eid):
    best = {}
    for s in SOURCES[eid]:
        outlet = s['outlet'].split(' (')[0].strip()
        fit = 1.0 if s['seen'].startswith('full') else 0.8
        best[outlet] = max(best.get(outlet, 0), 0.8 * fit)
    p = 1.0
    for w in best.values():
        p *= 1 - w
    c = min(0.99, 1 - p)
    if eid in PARTLY:
        c *= 0.8
    return round(c, 2)


CRED_ESTIMATE = {eid: _estimate(eid) for eid in SOURCES}
CRED_ESTIMATE[1302] = 0.30   # a claim relayed by one outlet; nothing confirms an attack
