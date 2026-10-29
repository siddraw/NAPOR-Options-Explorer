"""NAPOR China: from the Lee Teng-hui visa to the eve of the McCampbell FONOP, May 22, 1995 - Dec 31, 2018 (research file).

Same shape as events.py. Event IDs 3500-3599 and pair IDs 3500-3599 belong to this file (3500-3566 used).
events.py continues from Jan 7, 2019 (IDs 3001-3063).

Option letters for US moves are the ones in events.py and config.py (B talks, C sanctions, D transits and FONOPs,
E arms sales, F contact with Taiwan, G allied exercises, H other posture). A (hold) is not tagged.
Judgment calls on letters and kinds:
- Summits, leader meetings and the 2001 crew-release agreement are tagged B and use an action type that starts with "Talks".
- The Taiwan Travel Act (#3552) is tagged F: it is a US law that encourages senior visits. It is not a visit.
- Tariff rows (#3554, #3556, #3559) and China's tariff replies (#3555, #3557, #3560): the US rows have no option letter
  (trade is not one of the options). China's replies are logged as "Counter-measure" so the economic category sees them.
- No option letter: the 1999 embassy bombing (#3511), the House vote on the Taiwan Security Enhancement Act (#3514),
  the RIMPAC disinvitation (#3553) and the Asia Reassurance Initiative Act (#3566). They are context rows.
- Chinese diplomatic steps are kept out of the rows and written in the detail of the US move they answer: the Jun 1995
  ambassador recall (#3500), the May 1999 suspension of military ties and the Oct 2008 and Jan 2010 suspensions of
  military contacts (#3512, #3524, #3527). Any row with a China actor counts as a military or coast-guard action in the
  engine, and these were neither.

Source rules (docs/SOURCE_STANDARD.md):
- Only allowed outlets and official releases. Wire stories read on a syndicated page are labelled "NPR (via ...)".
  seen="full text" means the page was opened and read; seen="snippet" means only the search-result line was seen.
- Several 1995-2008 rows rest on a CRS chronology or report (everycrsreport.com mirror) or on the Congressional Record,
  because the search tool found few NYT, AP or Reuters archive pages for those years. The CRS pages were read on the
  everycrsreport.com mirror, not on an official Congress page, so they are labelled "CRS report (via everycrsreport.com)" and the
  engine keeps the 0.60 of an outlet that is not on the news list; a row on one of them alone is flagged "use with caution".
  Rows #3500, #3506-#3510, #3514, #3519, #3521, #3536 and #3537 are in that group. The Congressional Record is an official page and
  scores 0.80 (#3552 now does).
- The "published" date on a CRS page is approximate (the mirror pages show no date), and so is the date on the NBC
  bomber story (#3544), the NBC Impeccable story (#3525) and the NPR anti-satellite page (#3523). Where I did not record
  a page's exact headline, the headline field is a short description of the page.
- No Xinhua, Global Times or Chinese ministry page was opened. What China says is used only as an allowed outlet reports it.

How reply windows were read (CENSUS below):
- A clear link: a dated Chinese action inside 7 days that an allowed outlet ties to the US move, or a clear step up on a
  named day. "Timing only" means a dated action inside 7 days that no page ties to the move.
- N: the source I read reports only words (a protest, a warning, shadowing, a suspension of talks) or nothing. Where I
  also ran a search for a PLA drill or counter-sanction in the 7 days and found none in an allowed outlet, the note says so.
  Where I did not, the note says "words only in the source read". That is weaker evidence.
- Unclear: another Chinese act sits inside the window and no page ties it to the move.
- Unverified: the window was not searched. These are logged but not counted as cases.
- The 7-day window counts from the date of the US move as logged.

Dropped, not logged (no allowed source found, or only mirrors, think tanks or Wikipedia):
- The 1995-96 carrier ship names (no fetched allowed page named them) and the Dec 1995 Nimitz Strait passage (Kitsap Sun only).
- The Jan 2010 sanctions vow and the Mar 2009 USS Chung-Hoon escort (no allowed page); the Jan 2018 USS Hopper FONOP (Military Times only).
- The Aug 23, 2018 tariff round and the Oct 2018 Pence speech (not read); Chinese state media reports of PLA "military pressure"
  after the Taiwan Travel Act (Global Times and Sputnik only).
- Sep 2002, Nov 2002, Sep 2007 and Nov 2007 arms notifications (CRS gives only the month).
- The Oct 2001 Bush-Jiang meeting in Shanghai (page not opened).
"""
import datetime as dt


def d(y, m, day):
    return dt.date(y, m, day)


def _s(headline, outlet, published, url, seen="full text"):
    return {'headline': headline, 'outlet': outlet, 'published': published, 'seen': seen, 'url': url}


# Columns: ID, Date, Actor, Action Type, Target, Detail, Trigger ID, Severity, Confidence, Source
EVENTS = [
(3500, d(1995,5,22), "US", "High-level contact (private visit allowed for Taiwan's President Lee Teng-hui)", "Taiwan", "President Clinton agrees to let Lee Teng-hui visit his alma mater (Cornell) in a private visit. Beijing protests strongly. CRS lists China postponing its defense minister's US visit on May 26 and withdrawing its ambassador on Jun 16", None, "No damage; diplomatic protest", "Medium", "see audit"),
(3501, d(1995,7,21), "China (PLA)", "Missile launch (six ballistic missiles about 80 miles from Taiwan, Jul 21-26)", "Waters north of Taiwan", "Congressional Record statements describe six missiles (four short-range, two intermediate-range). Fishing areas closed and flights diverted; Taiwan's stock market fell 6.8%. A new round was announced for the following week. Members of Congress tie the tests to Lee's Cornell visit; China's reason was not read", 3500, "No damage; Taiwan stocks fell", "Medium", "see audit"),
(3502, d(1995,8,15), "China (PLA)", "Live-fire drills (missile and artillery firing, Aug 15-25)", "East China Sea north of Taiwan", "CRS dates ten days of naval exercises and live missile firings from Aug 15. The Congressional Record describes guided-missile and live artillery firing in the East China Sea north of Taiwan", 3500, "No damage", "Medium", "see audit"),
(3503, d(1995,10,24), "US", "Talks (Clinton-Jiang meeting, New York)", "China", "Clinton and Jiang Zemin meet at the Warwick Hotel. A White House briefing says Clinton did not promise never to grant a visa to Taiwan's president again; visits would be case by case, unofficial and rare. Taiwan took about 10 to 15 minutes of the talks", None, "n/a", "High", "see audit"),
(3504, d(1996,3,8), "China (PLA)", "Live-fire drills (missile launches and live-ammunition tests near Taiwan, from Mar 8)", "Waters off Taiwan", "CRS dates ballistic missile exercises at two impact areas near Taiwan from Mar 8. NPR reports missile and live-ammunition tests off Taiwan's coast, reportedly meant to discourage Taiwan's pro-democracy movement before the Mar 23 presidential vote. Secretary of State Christopher calls them intimidation and coercion", None, "No damage; Taiwanese voters were not deterred (NPR, Mar 13)", "Medium", "see audit"),
(3505, d(1996,3,10), "US", "Posture (two aircraft carrier groups sent toward Taiwan)", "Waters near Taiwan", "Christopher says on NBC that a carrier group will move closer to Taiwan; NPR reports a second carrier is being sent; CRS says the Pentagon disclosed on Mar 10 that two carrier battle groups were ordered to the area. No ship names are given in the pages I read", None, "n/a", "Medium", "see audit"),
(3506, d(1996,8,23), "US", "Arms sale announced ($420 million, Stinger missiles and Humvees)", "Taiwan", "The Pentagon announces the sale despite Chinese objections (CRS)", None, "n/a", "Medium", "see audit"),
(3507, d(1996,11,24), "US", "Talks (Clinton-Jiang meeting, APEC summit, Manila)", "China", "The two leaders agree to exchange state visits within two years (CRS)", None, "n/a", "Medium", "see audit"),
(3508, d(1996,12,9), "US", "Talks (Clinton and Perry meet Chinese Defense Minister Chi Haotian)", "China", "Beijing agrees in principle to US warship visits to Hong Kong after 1997. On Dec 5 Chi had refused to renounce force over Taiwan (CRS)", None, "n/a", "Medium", "see audit"),
(3509, d(1997,10,28), "US", "Talks (Jiang Zemin visit to the US, first summit of Clinton's presidency)", "China", "CRS: the first US-China summit of the Clinton presidency", None, "n/a", "Medium", "see audit"),
(3510, d(1998,6,24), "US", "Talks (Clinton begins nine-day China visit)", "China", "In Shanghai on Jun 30 Clinton says the US does not support Taiwan independence, a remark later seen as a policy shift (CRS)", None, "n/a", "Medium", "see audit"),
(3511, d(1999,5,7), "US (NATO)", "Strike (NATO bombs hit the Chinese Embassy in Belgrade)", "Chinese Embassy, Belgrade", "NATO bombs hit the Chinese Embassy in Belgrade, killing several Chinese nationals; the US calls it a tragic accident (CRS)", None, "Several Chinese nationals killed", "Medium", "see audit"),
(3512, d(1999,5,8), "China (crowds)", "Protests (crowds throw rocks and bricks at the US Embassy, Beijing)", "US Embassy, Beijing", "NPR reports a large crowd marching on May 8, with demonstrators breaking into the US embassy compound and throwing bricks at the British Embassy. By May 11 thousands had thrown rocks at the US embassy, and on May 10 its staff were still barricaded inside. China cut off military ties and other contacts with the US (NPR May 11; CRS dates the suspension May 10)", 3511, "Embassy attacked; staff barricaded inside", "Medium", "see audit"),
(3513, d(1999,11,15), "US", "Talks (US-China bilateral agreement on China's WTO entry)", "China", "A White House fact sheet describes the agreement on tariffs, farm goods and services. CRS dates the agreed terms to Nov 6", None, "n/a", "High", "see audit"),
(3514, d(2000,2,1), "US", "Legislation (House passes the Taiwan Security Enhancement Act, 341-70)", "Taiwan", "CRS reports no Chinese reaction to the vote. China issued a white paper on Feb 21 insisting on its right to use force, but CRS does not link it to the bill", None, "n/a", "Medium", "see audit"),
(3515, d(2001,4,1), "China (PLA)", "Collision (Chinese fighter hits a US Navy EP-3 off Hainan; crew held)", "US EP-3 surveillance aircraft", "A Chinese military jet collides with a US EP-3. The Chinese pilot is killed. The damaged EP-3 lands on Hainan Island without permission and the 24 crew are held for 11 days", None, "Chinese pilot killed; US aircraft kept; 24 crew held 11 days", "High", "see audit"),
(3516, d(2001,4,11), "US", "Talks (US letter of regret; China agrees to release the EP-3 crew)", "China", "The US says it is 'very sorry' for the presumed death of the pilot and that its plane landed without permission, but accepts no blame for the collision. China frees the crew on humanitarian grounds; the plane is left for a meeting on Apr 18", 3515, "n/a", "High", "see audit"),
(3517, d(2001,4,24), "US", "Arms sale announced (submarines, destroyers, P-3C aircraft)", "Taiwan", "President Bush approves the largest package for Taiwan in about a decade: diesel submarines, Kidd-class destroyers and P-3C aircraft. Aegis destroyers are put off. China's Foreign Ministry calls it a violation of the three communiques and Chinese sovereignty", None, "n/a", "High", "see audit"),
(3518, d(2002,2,21), "US", "Talks (Bush-Jiang meeting, Beijing)", "China", "The two presidents hold a meeting and dinner described as fairly friendly. No deal on China's missile exports; Taiwan and human rights are downplayed because of China's help against terrorism (NPR). Date taken from the NPR page address", None, "n/a", "Medium", "see audit"),
(3519, d(2003,9,24), "US", "Arms sale announced (up to $775 million, command and control program)", "Taiwan", "A notification for the Po Sheng command and control program, linked to the JTIDS/Link 16 terminals (CRS)", None, "n/a", "Medium", "see audit"),
(3520, d(2003,12,9), "US", "Talks (Bush and Premier Wen Jiabao, Oval Office)", "China", "Bush says the US opposes Taiwan's plan for a 2004 referendum and backs the status quo while Wen stands beside him. Date taken from the NPR page address", None, "n/a", "Medium", "see audit"),
(3521, d(2004,3,30), "US", "Arms sale announced (up to $1.8 billion, early-warning radars)", "Taiwan", "A notification for two UHF long-range early warning radars (CRS)", None, "n/a", "Medium", "see audit"),
(3522, d(2006,4,20), "US", "Talks (Bush and Hu Jintao, White House)", "China", "Bush says his position on Taiwan has not changed and he does not support Taiwan independence. Hu says China will not allow independence", None, "n/a", "High", "see audit"),
(3523, d(2007,1,11), "China (PLA)", "Missile launch (anti-satellite test, Fengyun-1C weather satellite)", "A Chinese weather satellite in orbit", "A medium-range ballistic missile with a kinetic kill vehicle destroys the satellite about 530 miles up. CRS estimates about 950 pieces of debris 4 inches or larger. The White House says on Jan 18 the test is 'inconsistent with the spirit of cooperation'", None, "No casualties; debris risk to about 700 spacecraft (CRS)", "High", "see audit"),
(3524, d(2008,10,3), "US", "Arms sale announced ($6.5 billion; Patriot missiles, Apache helicopters, Harpoon missiles)", "Taiwan", "The Pentagon notifies Congress. China cancels military exchanges and several arms-control and disaster-relief exchanges, and summons US diplomats for a formal protest; the Pentagon blames China's politicisation of the military relationship", None, "n/a", "High", "see audit"),
(3525, d(2009,3,8), "China (navy and civilian ships)", "Confrontation at sea (five Chinese ships close in on USNS Impeccable)", "USNS Impeccable (South China Sea, about 75 miles south of Hainan)", "Five Chinese ships surround the unarmed survey ship, come within about 25 to 50 feet, drop wood in front of it and block its path, forcing an emergency stop. The Pentagon calls it 'dangerous' and the US protests", None, "No shots; emergency all-stop", "High", "see audit"),
(3526, d(2009,11,17), "US", "Talks (Obama-Hu Jintao joint statement, Beijing)", "China", "The statement covers Taiwan, trade and climate. The US says it follows its one-China policy and the three communiques and welcomes peaceful cross-strait ties", None, "n/a", "High", "see audit"),
(3527, d(2010,1,29), "US", "Arms sale announced (about $6.4 billion; Black Hawk helicopters, Patriot missiles)", "Taiwan", "The Obama administration notifies five programs (CRS). Al Jazeera reports Beijing suspended military cooperation with the US and warned of 'serious repercussions'", None, "n/a", "High", "see audit"),
(3528, d(2011,1,19), "US", "Talks (Hu Jintao state visit to the White House)", "China", "A joint statement covers Taiwan, human rights and military dialogue. The US welcomes the cross-strait trade framework and supports 'peaceful development' across the Strait", None, "n/a", "High", "see audit"),
(3529, d(2011,9,21), "US", "Arms sale announced ($5.9 billion; upgrade of Taiwan's existing F-16A/B fighters)", "Taiwan", "CRS dates the notification Sep 21. Al Jazeera (Oct 3) reports the upgrade, not the new F-16C/D jets Taiwan wanted, and gives no official Chinese reaction", None, "n/a", "Medium", "see audit"),
(3530, d(2011,11,16), "US", "Posture (up to 2,500 US troops for northern Australia)", "Australia (Darwin)", "Al Jazeera says the announcement came a day before Obama spoke in Canberra on Nov 17, so the day is inferred. People's Daily opposed the closer ties; Al Jazeera reports the Chinese sense of encirclement", None, "n/a", "Medium", "see audit"),
(3531, d(2013,6,7), "US", "Talks (Obama-Xi summit, Sunnylands)", "China", "Two days of talks, eight hours in all, on North Korea, cyber attacks and climate change", None, "n/a", "High", "see audit"),
(3532, d(2013,11,25), "US", "Posture (two B-52 bombers fly through China's new East China Sea air defense zone)", "East China Sea", "Two unarmed B-52s from Guam spend under an hour in the zone China declared on Nov 23, with no notice to China. The Pentagon calls it a long-planned training sortie and says China did not react", None, "n/a", "High", "see audit"),
(3533, d(2013,11,29), "China (PLA Air Force)", "Patrol (fighter jets and an early-warning aircraft in the new air defense zone)", "East China Sea air defense zone", "Al Jazeera reports, citing Xinhua, that several fighters and an early-warning aircraft patrolled the zone, which a PLA Air Force spokesman called a defensive measure. Japan and South Korea also sent aircraft through the zone on Nov 28. The date is the date of the report", 3532, "No shots; no damage", "Medium", "see audit"),
(3534, d(2013,12,5), "China (PLA Navy)", "Close pass at sea (Chinese amphibious ship and the cruiser USS Cowpens)", "USS Cowpens (South China Sea)", "The Cowpens takes evasive action to avoid a collision; the Chinese ship came within about 500 yards. The US calls it an attempt to 'impede and harass'; China's defense ministry says the US ship was tailing and harassing its ship during drills", None, "No collision", "Medium", "see audit"),
(3535, d(2014,8,19), "China (PLA)", "Dangerous intercept (Chinese fighter and a US Navy P-8 east of Hainan)", "US P-8 Poseidon patrol aircraft", "A Chinese fighter flies within 20 to 30 feet of the P-8, does a barrel roll and makes passes under and alongside it, about 135 miles east of Hainan. The Pentagon calls it aggressive and unprofessional. The day is taken from 'Tuesday' in the NPR report", None, "No collision", "Medium", "see audit"),
(3536, d(2014,11,10), "US", "Talks (Obama visit to China, Nov 10-12)", "China", "The militaries sign a memorandum on notification of major military activities, and the two sides announce climate targets (CRS)", None, "n/a", "Medium", "see audit"),
(3537, d(2015,9,25), "US", "Talks (Xi Jinping state visit to the White House)", "China", "A cyber agreement and annexes to the 2014 military memoranda. The US criticised China's Spratly building; Xi said China does not intend to militarize it (CRS)", None, "n/a", "Medium", "see audit"),
(3538, d(2015,10,27), "US", "FONOP (destroyer USS Lassen, Subi Reef)", "Subi Reef (Spratlys)", "USS Lassen comes within 12 nautical miles of Subi Reef, the first such mission around the artificial features in years. China's Foreign Ministry calls it provocative and vows a response. The date is the Beijing date; the ship passed on Monday night US time", None, "No damage; verbal protest", "Medium", "see audit"),
(3539, d(2015,12,16), "US", "Arms sale announced ($1.83 billion; frigates, missiles, amphibious vehicles)", "Taiwan", "The first package for Taiwan in four years: two Perry-class frigates, TOW 2B and Javelin missiles, 36 AAV-7 vehicles and Phalanx systems. China's vice foreign minister makes 'solemn representations' to the US charge d'affaires", None, "n/a", "High", "see audit"),
(3540, d(2015,12,17), "China (Foreign Ministry, as reported)", "Counter-sanctions announced (US companies in the sale)", "US firms in the Taiwan sale", "China says it will impose sanctions on companies involved in the sale. No firm was named in the report I read", 3539, "No named firms found", "Medium", "see audit"),
(3541, d(2016,1,30), "US", "FONOP (destroyer USS Curtis Wilbur, Triton Island)", "Triton Island (Paracels)", "USS Curtis Wilbur makes an innocent passage within 12 nautical miles of Triton Island, early Saturday local time (Jan 29 US time). China had not responded when USNI reported it", None, "No damage", "Medium", "see audit"),
(3542, d(2016,5,10), "US", "FONOP (destroyer USS William P. Lawrence, Fiery Cross Reef)", "Fiery Cross Reef (Spratlys)", "USS William P. Lawrence passes within 12 nautical miles of the reef (the morning of May 10 local time). Foreign Ministry spokesman Lu Kang says it threatened China's sovereignty and endangered staff on the reef", None, "No damage; verbal protest", "Medium", "see audit"),
(3543, d(2016,5,17), "China (PLA)", "Dangerous intercept (two J-11 fighters and a US Navy EP-3E east of Hainan)", "US EP-3E surveillance aircraft", "The fighters come within about 50 feet of the EP-3E, which dives about 200 feet to avoid a collision (US account). The Pentagon calls it unsafe. China's Foreign Ministry says the US claim is not true and demands the US stop close reconnaissance. Nothing ties it to the May 10 FONOP", None, "No collision", "Medium", "see audit"),
(3544, d(2016,11,25), "China (PLA)", "Long-range patrol (two H-6K bombers fly around Taiwan)", "Waters around Taiwan", "Taiwan's defense ministry says two H-6K bombers, a TU-154, a Y-8 and two Su-30s loop around the island without entering its air defense zone, the first encirclement on a long-range mission. It says this has 'absolutely no relation' to the Trump-Tsai call a week later. The year is inferred from the Trump-Tsai call", None, "No shots; no damage", "Medium", "see audit"),
(3545, d(2016,12,2), "US", "High-level contact with Taiwan (President-elect Trump takes a call from President Tsai)", "Taiwan", "NPR reports it as likely the first such call between a US president or president-elect and a Taiwanese leader since 1979. Foreign Minister Wang Yi calls it 'just a small trick by Taiwan'", None, "n/a", "High", "see audit"),
(3546, d(2016,12,16), "China (PLA Navy)", "Seizure of a US Navy underwater drone (USNS Bowditch)", "US underwater glider drone (South China Sea)", "A Chinese warship sends a small boat to take the drone while the Bowditch is retrieving another. The Pentagon announced it on Dec 16 and called it inconsistent with international law. China's defense ministry says it examined the drone in a 'professional and responsible manner' and returned it Dec 20. The seizure itself was a day or so earlier", None, "No shots; drone returned Dec 20", "Medium", "see audit"),
(3547, d(2017,4,6), "US", "Talks (Trump-Xi summit, Mar-a-Lago)", "China", "The first face-to-face meeting, on North Korea and the trade deficit", None, "n/a", "High", "see audit"),
(3548, d(2017,6,29), "US", "Arms sale announced ($1.4 billion, first under Trump)", "Taiwan", "Torpedoes, early-warning radar support, anti-radiation missiles and missile parts. Foreign Ministry spokesman Lu Kang demands the deal be cancelled", None, "n/a", "High", "see audit"),
(3549, d(2017,7,2), "US", "FONOP (destroyer USS Stethem, Triton Island)", "Triton Island (Paracels)", "USS Stethem comes within 12 nautical miles. Al Jazeera says Beijing sent military vessels and fighters to warn the ship off and called it a 'serious political and military provocation'", None, "No damage; verbal protest", "High", "see audit"),
(3550, d(2017,8,10), "US", "FONOP (destroyer USS John S. McCain, Mischief Reef)", "Mischief Reef (Spratlys)", "The third South China Sea FONOP of the year. A Chinese frigate radios the ship about 10 times to turn around; a US official calls the contact safe and professional. China's Foreign Ministry says it will lodge a protest", None, "No damage; verbal protest", "High", "see audit"),
(3551, d(2017,11,8), "US", "Talks (Trump visit to Beijing)", "China", "Xi hosts Trump at the Forbidden City in what Chinese officials call a 'state visit plus'. Taiwan watched anxiously", None, "n/a", "Medium", "see audit"),
(3552, d(2018,3,16), "US", "High-level contact with Taiwan (Taiwan Travel Act signed)", "Taiwan", "The act says the US should encourage visits between US and Taiwanese officials at all levels. It is non-binding. I found no allowed outlet's report of China's reaction", None, "n/a", "Medium", "see audit"),
(3553, d(2018,5,23), "US", "Disinvitation (China barred from RIMPAC 2018)", "China", "The Pentagon calls it an 'initial response' to China's militarization of the South China Sea: anti-ship and surface-to-air missiles on the Spratlys and bombers landed on Woody Island", None, "n/a", "High", "see audit"),
(3554, d(2018,6,15), "US", "Tariffs (25% on $50 billion of Chinese goods announced)", "China (about 1,100 products)", "A 25% tariff on goods with 'industrially significant technologies'. Collection starts Jul 6 on the first $34 billion; a second $16 billion is under review", None, "n/a", "High", "see audit"),
(3555, d(2018,6,15), "China (government, as reported)", "Counter-measure (25% tariffs on $50 billion of US goods)", "US exports (meat, soybeans, cars, coal, oil)", "NPR says China 'quickly announced' tariffs of the same size: 25% on about $34 billion from Jul 6 and another $16 billion later. The announcement came hours after the US list, so the day is the US date", 3554, "Trade measure; no damage", "High", "see audit"),
(3556, d(2018,7,6), "US", "Tariffs (25% on $34 billion of Chinese goods take effect)", "China", "Effective 12:01 a.m. Eastern Time. Cars, disk drives, pump and valve parts and other industrial goods; most consumer goods left off", None, "n/a", "High", "see audit"),
(3557, d(2018,7,6), "China (government, as reported)", "Counter-measure (25% tariffs on $34 billion of US goods take effect)", "US exports (lobsters, soybeans, electric cars)", "Foreign Ministry spokesman Lu Kang announces the tariffs hours after the US ones begin; they take effect at the same moment in universal time", 3556, "Trade measure; no damage", "High", "see audit"),
(3558, d(2018,7,7), "US", "Taiwan Strait transit (destroyers USS Mustin and USS Benfold)", "Taiwan Strait", "Two Japan-based destroyers sail through the Strait on Saturday July 7. US officials would not say whether the PLA Navy responded; the Global Times tweeted that the US was aggravating tension and suggested the ships were shadowed", None, "n/a", "Medium", "see audit"),
(3559, d(2018,9,17), "US", "Tariffs (10% on $200 billion of Chinese goods announced)", "China", "Trump announces the tariffs on Monday night after the USTR review and threatens tariffs on about $267 billion more if China retaliates", None, "n/a", "High", "see audit"),
(3560, d(2018,9,18), "China (Finance Ministry, as reported)", "Counter-measure (tariffs of 5% and 10% on $60 billion of US goods)", "5,207 types of US goods", "The Finance Ministry says it is proceeding with plans announced in August and cites 'unilateralism and protectionism'", 3559, "Trade measure; no damage", "High", "see audit"),
(3561, d(2018,9,20), "US", "Sanction (China's Equipment Development Department and its director Li Shangfu)", "Chinese military purchasers of Russian Su-35 jets and S-400 missiles", "State Department sanctions under CAATSA. On Sep 21 spokesman Geng Shuang says China strongly objects and warns of consequences unless the sanctions are withdrawn", None, "n/a", "High", "see audit"),
(3562, d(2018,9,30), "US", "FONOP (destroyer USS Decatur, Gaven Reefs)", "Gaven Reefs (Spratlys)", "USS Decatur keeps 12 nautical miles from the Chinese-held outpost. The Navy releases pictures of the Chinese destroyer Lanzhou crossing in front of it. China's Foreign Ministry says the Decatur violated China's 'indisputable sovereignty'", None, "No damage; verbal protest", "High", "see audit"),
(3563, d(2018,9,30), "China (PLA Navy)", "Close pass at sea (destroyer Lanzhou about 45 yards from USS Decatur)", "USS Decatur (Gaven Reefs)", "The Navy says the Luyang-class destroyer came within 45 yards, less than a third of the Decatur's length; the ships then moved apart. The Navy's first statement named only a 'Luyang-class' ship", 3562, "No collision", "High", "see audit"),
(3564, d(2018,11,28), "US", "Taiwan Strait transit (destroyer USS Stockdale, oiler USNS Pecos)", "Taiwan Strait", "USNI says the Navy reported no significant interactions with Chinese ships. After the October transit Chinese officials said their position had not changed", None, "n/a", "Medium", "see audit"),
(3565, d(2018,12,1), "US", "Talks (Trump-Xi dinner at the G20, Buenos Aires)", "China", "A 90-day tariff truce: the US holds the tariffs on $200 billion at 10% instead of 25% and China agrees to buy US goods, with talks on technology transfer and intellectual property to finish within 90 days", None, "n/a", "High", "see audit"),
(3566, d(2018,12,31), "US", "Legislation (Asia Reassurance Initiative Act signed)", "Taiwan", "The act says it is US policy to support close economic, political and security ties with Taiwan. China's Foreign Ministry says it 'grossly interferes in China's internal affairs' and that the US 'must not implement' the Taiwan provisions (CRS)", None, "n/a", "Medium", "see audit"),
]

_CRS_9500 = _s('CRS Report 97-484: dated entries, 1995-2000 (entries to Jul 18, 2000)', 'CRS report (via everycrsreport.com)', '2000-07-18', 'https://www.everycrsreport.com/reports/97-484.html')
_CRS_ARMS = _s('Taiwan: Major U.S. Arms Sales Since 1990 (CRS Report RL30957)', 'CRS report (via everycrsreport.com)', '2015-01-05', 'https://www.everycrsreport.com/reports/RL30957.html')
_CR_E1871 = _s('Congressional Record, Extensions of Remarks, Sep 28, 1995 (pp. E1871-E1872)', 'Congressional Record (House)', '1995-09-28', 'https://www.govinfo.gov/link/crec/141/E/1871')
_NPR_TT = _s('Taiwan Troubles', 'NPR (via WYPR)', '1996-03-10', 'https://www.wypr.org/1996-03-10/taiwan-troubles')
_NPR_BG = _s('Bush In China', 'NPR', '2002-02-21', 'https://www.npr.org/2002/02/21/1138444/bush-in-china')
_AJ_ADIZ = _s('China fighter jets fly through disputed zone', 'Al Jazeera', '2013-11-29', 'https://www.aljazeera.com/news/2013/11/29/china-fighter-jets-fly-through-disputed-zone')
_USNI_P1 = _s('U.S. Destroyer Comes Within 12 Nautical Miles of Chinese South China Sea Artificial Island, Beijing Threatens Response', 'USNI News', '2015-10-27', 'https://news.usni.org/2015/10/27/u-s-destroyer-comes-within-12-nautical-miles-of-chinese-south-china-sea-artificial-island-beijing-threatens-response')
_NPR_TARIFF = _s('Trump levies $50 billion in tariffs as China says it will retaliate', 'NPR', '2018-06-15', 'https://www.npr.org/2018/06/15/620259820/trump-levies-50-billion-in-tariffs-as-china-says-it-will-retaliate')
_AJ_TARIFF = _s('Trade war begins as China strikes back against US over tariffs', 'Al Jazeera', '2018-07-06', 'https://www.aljazeera.com/economy/2018/7/6/trade-war-begins-as-china-strikes-back-against-us-over-tariffs')
_CBS_TARIFF = _s('China retaliates with $60 billion in tariffs as trade spat with U.S. intensifies', 'CBS News', '2018-09-18', 'https://www.cbsnews.com/amp/news/china-retaliates-with-60-billion-in-tariffs-as-trade-spat-with-u-s-intensifies')
_TWZ_DEC = _s('U.S. Navy releases images of Chinese warship\'s dangerous maneuvers near its destroyer', 'The War Zone', '2018-09-30', 'https://www.twz.com/23986/u-s-navy-releases-images-of-chinese-warships-dangerous-maneuvers-near-its-destroyer')
_STRIPES_BMB = _s('US: 2 bombers over China\'s new airspace were on long-planned training', 'Stars and Stripes', '2013-11-26', 'https://www.stripes.com/news/2013-11-26/us-2-bombers-over-chinas-new-airspace-were-on-long-planned-training-1843726.html')

SOURCES = {
 3500: [_CRS_9500],
 3501: [_CR_E1871, _s('Congressional Record, Senate, Aug 11, 1995 (pp. S12417-S12419)', 'Congressional Record (Senate)', '1995-08-11', 'https://www.govinfo.gov/link/crec/141/S/12418'), _CRS_9500],
 3502: [_CR_E1871, _CRS_9500],
 3503: [_s('Briefing by Winston Lord and Bob Suettinger, New York, Oct 24, 1995', 'White House (Clinton archive)', '1995-10-24', 'https://clintonwhitehouse6.archives.gov/1995/10/1995-10-24-briefing-by-winston-lord-and-bob-suettinger-nyc.html'), _CRS_9500],
 3504: [_NPR_TT, _s('Defiance', 'NPR (via KAXE)', '1996-03-13', 'https://www.kaxe.org/1996-03-13/defiance'), _CRS_9500],
 3505: [_NPR_TT, _s('China', 'NPR (via KAXE)', '1996-03-10', 'https://www.kaxe.org/1996-03-10/china'), _CRS_9500],
 3506: [_CRS_9500],
 3507: [_CRS_9500],
 3508: [_CRS_9500],
 3509: [_CRS_9500],
 3510: [_CRS_9500],
 3511: [_CRS_9500, _s('China Reacts', 'NPR', '1999-05-08', 'https://www.npr.org/1999/05/08/1049822/china-reacts')],
 3512: [_s('China Reacts', 'NPR', '1999-05-08', 'https://www.npr.org/1999/05/08/1049822/china-reacts'), _s('China Latest', 'NPR', '1999-05-10', 'https://www.npr.org/1999/05/10/1049853/china-latest'), _s('Chinese Embassy Incident', 'NPR', '1999-05-11', 'https://www.npr.org/1999/05/11/1049909/chinese-embassy-incident'), _CRS_9500],
 3513: [_s('U.S.-China Bilateral WTO Agreement (fact sheet)', 'White House (Clinton archive)', '1999-11-15', 'https://clintonwhitehouse5.archives.gov/textonly/WH/new/WTO-Conf-1999/factsheets/fs-004.html'), _CRS_9500],
 3514: [_s('Taiwan Security Enhancement Act (CRS Report RS20370)', 'CRS report (via everycrsreport.com)', '2000-02-01', 'https://www.everycrsreport.com/reports/RS20370.html')],
 3515: [_s('China Agrees to Release U.S. Crew', 'PBS NewsHour', '2001-04-11', 'https://www.pbs.org/newshour/nation/military-jan-june01-plane_04-11'), _s('A US surveillance plane collided with a Chinese jet 25 years ago today, setting off an 11-day standoff', 'NPR (via KPCW)', '2026-04-01', 'https://www.kpcw.org/npr-news/2026-04-01/a-us-surveillance-plane-collided-with-a-chinese-jet-25-years-ago-today-setting-off-an-11-day-standoff')],
 3516: [_s('China Agrees to Release U.S. Crew', 'PBS NewsHour', '2001-04-11', 'https://www.pbs.org/newshour/nation/military-jan-june01-plane_04-11')],
 3517: [_s('CNN transcript, Apr 29, 2001: Taiwan arms sales', 'CNN', '2001-04-29', 'https://www.cnn.com/TRANSCRIPTS/0104/29/wr.01.html'), _CRS_ARMS],
 3518: [_NPR_BG],
 3519: [_CRS_ARMS],
 3520: [_s('Bush Urges Taiwan Status Quo', 'NPR', '2003-12-09', 'https://www.npr.org/2003/12/09/1539586/bush-warns-taiwan-against-independence-movement')],
 3521: [_CRS_ARMS],
 3522: [_s('President Bush Meets with President Hu of the People\'s Republic of China', 'White House (Bush archive)', '2006-04-20', 'https://georgewbush-whitehouse.archives.gov/news/releases/2006/04/20060420-1.html')],
 3523: [_s('NPR report on China\'s Jan 11, 2007 anti-satellite test (page shows no date)', 'NPR', '2007-01-01', 'https://www.npr.org/transcripts/6915533'), _s('China\'s January 2007 anti-satellite test (CRS Report RS22652)', 'CRS report (via everycrsreport.com)', '2007-01-01', 'https://www.everycrsreport.com/reports/RS22652.html')],
 3524: [_s('China backlash at Taiwan arms sale', 'Al Jazeera', '2008-10-07', 'https://www.aljazeera.com/news/2008/10/7/china-backlash-at-taiwan-arms-sale'), _CRS_ARMS],
 3525: [_s('Pentagon: Five Chinese vessels harass US ship', 'Stars and Stripes', '2009-03-10', 'https://www.stripes.com/news/2009-03-10/pentagon-five-chinese-vessels-harass-us-ship-1988887.html'), _s('Chinese ships harass US Navy vessel (Impeccable)', 'NBC News', '2009-03-09', 'https://www.nbcnews.com/news/amp/wbna29596179')],
 3526: [_s('In full: U.S.-China joint statement', 'CBS News', '2009-11-17', 'https://www.cbsnews.com/news/in-full-us-china-joint-statement/')],
 3527: [_s('China envoy on Taiwan arms deal', 'Al Jazeera', '2010-01-30', 'https://www.aljazeera.com/news/2010/1/30/china-envoy-on-taiwan-arms-deal'), _CRS_ARMS],
 3528: [_s('U.S.-China Joint Statement, Jan 19, 2011', 'White House (Obama archive)', '2011-01-19', 'https://obamawhitehouse.archives.gov/the-press-office/2011/01/19/US-China-joint-statement')],
 3529: [_CRS_ARMS, _s('US-Taiwan fighter jet deal remains grounded', 'Al Jazeera', '2011-10-03', 'https://www.aljazeera.com/features/2011/10/3/us-taiwan-fighter-jet-deal-remains-grounded')],
 3530: [_s('Closer US-Australia defence ties irk China', 'Al Jazeera', '2011-11-18', 'https://www.aljazeera.com/news/2011/11/18/closer-us-australia-defence-ties-irk-china')],
 3531: [_s('Obama-Xi summit at Sunnylands', 'CNN', '2013-06-09', 'https://edition.cnn.com/2013/06/09/politics/obama-xi-summit')],
 3532: [_STRIPES_BMB, _s('U.S. flies bombers through East China Sea air space China claims', 'NPR', '2013-11-26', 'https://www.npr.org/2013/11/26/247392824/u-s-flies-bombers-through-east-china-sea-air-space-china-claims')],
 3533: [_AJ_ADIZ],
 3534: [_s('Beijing near-miss: U.S. warship harassed Chinese vessel', 'NPR (via APR)', '2013-12-18', 'https://www.apr.org/2013-12-18/beijing-near-miss-as-u-s-warship-harassed-chinese-vessel?_amp=true')],
 3535: [_s('Chinese fighter buzzed U.S. Navy plane in dangerous intercept', 'NPR', '2014-08-22', 'https://www.npr.org/sections/thetwo-way/2014/08/22/342465620/chinese-fighter-buzzed-u-s-navy-plane-in-dangerous-intercept')],
 3536: [_s('CRS Insight IN10181: President Obama\'s November 2014 visit to China', 'CRS report (via everycrsreport.com)', '2014-11-01', 'https://www.everycrsreport.com/reports/IN10181.html')],
 3537: [_s('Chinese President Xi\'s September 2015 State Visit (CRS In Focus IF10291)', 'CRS report (via everycrsreport.com)', '2015-10-01', 'https://www.everycrsreport.com/reports/IF10291.html')],
 3538: [_USNI_P1],
 3539: [_s('U.S. Plans Modest $1.83B Taiwan Arms Deal', 'USNI News', '2015-12-16', 'https://news.usni.org/2015/12/16/breaking-u-s-plans-modest-1-83b-taiwan-arms-deal-little-offensive-power-in-proposed-package'), _s('China summons US envoy over sale of warships to Taiwan', 'Al Jazeera', '2015-12-17', 'https://www.aljazeera.com/news/2015/12/17/china-summons-us-envoy-over-sale-of-warships-to-taiwan')],
 3540: [_s('China summons US envoy over sale of warships to Taiwan', 'Al Jazeera', '2015-12-17', 'https://www.aljazeera.com/news/2015/12/17/china-summons-us-envoy-over-sale-of-warships-to-taiwan')],
 3541: [_s('Destroyer USS Curtis Wilbur conducts freedom of navigation operation near Triton Island', 'USNI News', '2016-01-30', 'https://news.usni.org/?p=16738')],
 3542: [_s('U.S. Destroyer Passes Near Chinese Artificial Island in South China Sea Freedom of Navigation Operation', 'USNI News', '2016-05-10', 'https://news.usni.org/2016/05/10/u-s-destroyer-passes-near-chinese-artificial-island-in-south-china-sea-freedom-of-navigation-operation')],
 3543: [_s('Chinese fighters intercept U.S. Navy EP-3 near Hainan', 'USNI News', '2016-05-17', 'https://news.usni.org/?p=19720')],
 3544: [_s('China flew nuclear-capable bombers near Taiwan before Trump call', 'NBC News', '2016-12-05', 'https://www.nbcnews.com/news/world/china-flew-nuclear-capable-bombers-near-taiwan-trump-call-n692421')],
 3545: [_s('Trump speaks to Taiwan\'s president, in move likely to anger Beijing', 'NPR (via APR)', '2016-12-02', 'https://www.apr.org/politics-government/2016-12-02/trump-speaks-to-taiwans-president-in-move-likely-to-anger-beijing')],
 3546: [_s('China says it will return seized U.S. underwater drone in appropriate way', 'NPR', '2016-12-17', 'https://www.npr.org/sections/thetwo-way/2016/12/17/505982198/china-says-it-will-return-seized-u-s-underwater-drone-in-appropriate-way'), _s('China returns U.S. Navy drone seized in South China Sea', 'NPR', '2016-12-20', 'https://www.npr.org/sections/thetwo-way/2016/12/20/506256081/china-returns-u-s-navy-drone-seized-in-south-china-sea')],
 3547: [_s('Trump welcomes Chinese President Xi Jinping at Mar-a-Lago', 'NPR', '2017-04-06', 'https://www.npr.org/2017/04/06/522903377/trump-welcomes-chinese-president-xi-jinping-at-mar-a-lago')],
 3548: [_s('China demands US nix Taiwan arms deal', 'CBS News', '2017-06-30', 'https://cbsnews.com/news/china-demands-us-nix-taiwan-arms-weapons-deal-one-china-policy')],
 3549: [_s('U.S. destroyer conducts freedom of navigation operation in South China Sea past Chinese island', 'USNI News', '2017-07-02', 'https://news.usni.org/2017/07/02/u-s-destroyer-conducts-freedom-navigation-operation-south-china-sea-past-chinese-island'), _s('China: US warship near island a serious provocation', 'Al Jazeera', '2017-07-03', 'https://www.aljazeera.com/news/2017/7/3/china-us-warship-near-island-a-serious-provocation')],
 3550: [_s('USS John S. McCain conducts South China Sea freedom of navigation operation past Mischief Reef', 'USNI News', '2017-08-10', 'https://news.usni.org/2017/08/10/uss-john-s-mccain-conducts-south-china-sea-freedom-navigation-operation-past-mischief-reef-3rd-south-china-sea-fonop-year'), _s('China protests US ship near South China Sea island', 'Al Jazeera', '2017-08-11', 'https://www.aljazeera.com/amp/news/2017/8/11/china-protests-us-ship-near-south-china-sea-island')],
 3551: [_s('China lavishes red carpet treatment on Trump as he arrives for talks with Xi Jinping', 'NPR (via WBUR)', '2017-11-08', 'https://wbur.org/npr/562819640/china-lavishes-red-carpet-treatment-on-trump-as-he-arrives-for-talks-with-xi-jin')],
 3552: [_s('Taiwan Travel Act (Public Law 115-135)', 'Congress (govinfo.gov)', '2018-03-16', 'https://www.govinfo.gov/content/pkg/PLAW-115publ135/html/PLAW-115publ135.htm')],
 3553: [_s('China disinvited from RIMPAC 2018', 'USNI News', '2018-05-23', 'https://news.usni.org/?p=33801')],
 3554: [_NPR_TARIFF],
 3555: [_NPR_TARIFF],
 3556: [_AJ_TARIFF],
 3557: [_AJ_TARIFF],
 3558: [_s('Two U.S. destroyers sail through the Taiwan Strait', 'USNI News', '2018-07-07', 'https://news.usni.org/2018/07/07/two-u-s-destroyers-sail-taiwan-strait')],
 3559: [_CBS_TARIFF],
 3560: [_CBS_TARIFF],
 3561: [_s('China urges US to withdraw sanctions or face consequences', 'Al Jazeera', '2018-09-21', 'https://www.aljazeera.com/news/2018/09/china-urges-withdraw-sanctions-face-consequences-180921064337322.html')],
 3562: [_TWZ_DEC],
 3563: [_TWZ_DEC],
 3564: [_s('USS Stockdale and USNS Pecos transit the Taiwan Strait', 'USNI News', '2018-11-28', 'https://news.usni.org/2018/11/28/39064')],
 3565: [_s('Trump, Xi agree to a temporary trade truce', 'CNN', '2018-12-01', 'https://edition.cnn.com/2018/12/01/politics/trump-china-tariffs/index.html')],
 3566: [_s('Asia Reassurance Initiative Act (CRS In Focus IF11148)', 'CRS report (via everycrsreport.com)', '2019-03-20', 'https://www.everycrsreport.com/files/2019-03-20_IF11148_bd48f7c8b4fc29fb9b4356802351649f037897a5.html')],
}
VERDICT = {k: 'confirmed' for k in SOURCES}
# Rows where an allowed outlet or official page confirms the event but not every detail in the row (day inferred, year inferred, date set from a page address).
#   3518, 3520: date set from the NPR page address.     3530: day inferred from "a day before" Obama's Nov 17 speech.
#   3533: dated by the report, not the flights.         3535: day set from "Tuesday".
#   3544: year inferred from the Trump-Tsai call.       3546: dated by the Pentagon announcement, not the seizure.
PARTLY = {3518, 3520, 3530, 3533, 3535, 3544, 3546}

# Which option letter each US move belongs to (see header). A (hold) is not tagged.
US_OPTION = {
 3500: 'F', 3503: 'B', 3505: 'H', 3506: 'E', 3507: 'B', 3508: 'B', 3509: 'B', 3510: 'B', 3513: 'B', 3516: 'B',
 3517: 'E', 3518: 'B', 3519: 'E', 3520: 'B', 3521: 'E', 3522: 'B', 3524: 'E', 3526: 'B', 3527: 'E', 3528: 'B',
 3529: 'E', 3530: 'H', 3531: 'B', 3532: 'H', 3536: 'B', 3537: 'B', 3538: 'D', 3539: 'E', 3541: 'D', 3542: 'D',
 3545: 'F', 3547: 'B', 3548: 'E', 3549: 'D', 3550: 'D', 3551: 'B', 3552: 'F', 3558: 'D', 3561: 'C', 3562: 'D',
 3564: 'D', 3565: 'B',
}


def cred_estimate():
    """My own estimate of the engine's credibility score (official release or allowed outlet, full text 0.80;
    a CRS mirror 0.60; two different outlets combine; 'Partly' x0.8). For spot checks only."""
    out = {}
    for eid, srcs in SOURCES.items():
        best = {}
        for s in srcs:
            outlet = s['outlet'].split(' (')[0].strip()
            w = 0.60 if outlet.startswith('CRS') else 0.80
            w *= 1.0 if s['seen'].startswith('full') else 0.8
            best[outlet] = max(best.get(outlet, 0), w)
        p = 1.0
        for w in best.values():
            p *= (1 - w)
        c = min(0.99, 1 - p)
        if eid in PARTLY:
            c *= 0.8
        out[eid] = round(c, 2)
    return out


CRED_ESTIMATE = cred_estimate()

_ONLY_WORDS = "words only in the source read; days 2-7 not searched further"

# Rows for US moves of kinds C-H (window: 7 days for a reply, counted from the logged date).
# Category = what the move targeted. C = Economic/Blockade; D, E, F, G, H = Military/Property (placeholder wording).
CENSUS = [
 (3500, "Military/Property", "N", "Visa for Lee Teng-hui, May 22, 1995. CRS lists, inside the window, only a postponed defense minister visit (May 26, day 4); the ambassador recall was Jun 16 (day 25) and the first missile tests Jul 21 (day 60). No drill, launch or counter-sanction in the 7 days, but the only source is a CRS chronology. The later tests (#3501, #3502) were tied to the visit by members of Congress and not by any page I read as a reply."),
 (3505, "Military/Property", "Unclear", "Carrier groups sent toward Taiwan, Mar 10, 1996. China's missile tests began Mar 8, before the move, and ran on through the window, so a reply cannot be separated from the tests that prompted the move. Context only. No ship names were found in an allowed page."),
 (3506, "Military/Property", "Unverified", "$420M sale, Aug 23, 1996 (CRS). The window was not searched."),
 (3517, "Military/Property", "N", "Sale of submarines, destroyers and P-3Cs, Apr 24, 2001. CNN: the Foreign Ministry protested and warned of serious effects on relations. CRS: no sanctions tied to the 2001 notifications. Words only in the source read; days 2-7 not searched further. The EP-3 standoff (#3515) had ended two weeks earlier."),
 (3519, "Military/Property", "Unverified", "Po Sheng notification, Sep 24, 2003 (CRS). The window was not searched."),
 (3521, "Military/Property", "Unverified", "Early-warning radar notification, Mar 30, 2004 (CRS). The window was not searched."),
 (3524, "Military/Property", "N", "$6.5B sale, Oct 3, 2008. Al Jazeera: China cancelled military exchanges and protested to US diplomats. No drill, patrol or counter-sanction in the report read. A search for a PLA drill or counter-sanction in Oct 4-10, 2008 found nothing in an allowed outlet. The cancelled exchanges are a diplomatic step and are not counted as a reply."),
 (3527, "Military/Property", "N", "$6.4B package, Jan 29, 2010. Al Jazeera: China suspended military cooperation and warned of 'serious repercussions'. No sanction on named firms or drill in that report; the sanctions vow some outlets reported was not found in an allowed one (dropped). Words and a suspended dialogue only."),
 (3529, "Military/Property", "Unverified", "F-16A/B upgrade, Sep 21, 2011. Al Jazeera (Oct 3) reports no official Chinese response. The window was not searched."),
 (3530, "Military/Property", "N", "US troops to Australia, Nov 16, 2011. Al Jazeera: People's Daily opposed it and Chinese commentators spoke of encirclement. No PLA action reported (" + _ONLY_WORDS + "). n = 1 or 2 for posture (H): very thin evidence."),
 (3532, "Military/Property", "R-weak", "B-52 flight through the new air defense zone, Nov 25, 2013 -> Chinese fighters and an early-warning aircraft patrol the zone, reported Nov 29 (day 4, Al Jazeera). China called the patrol a defensive measure and did not say it answered the flight. Link plausible only; the zone was China's own new line. n = 2 for posture (H): very thin evidence."),
 (3538, "Military/Property", "N", "Lassen FONOP at Subi Reef, Oct 27, 2015. USNI: the Foreign Ministry called it provocative and vowed a response; the Chinese Navy shadowed the destroyer (background). A search for a PLA drill or counter-sanction in Oct 28-Nov 3, 2015 found nothing in an allowed outlet."),
 (3539, "Military/Property", "R-weak", "$1.83B sale, Dec 16, 2015 -> China says on Dec 17 it will impose sanctions on companies in the sale (#3540). No firm was named in the report read, so the link is a stated plan, not a confirmed sanction."),
 (3541, "Military/Property", "Unverified", "Curtis Wilbur at Triton Island, Jan 30, 2016. China had not responded when USNI wrote. The window was not searched."),
 (3542, "Military/Property", "Unclear", "Lawrence FONOP at Fiery Cross Reef, May 10, 2016. A Chinese fighter made an unsafe intercept of a US EP-3E on May 17 (#3543, day 7). The Pentagon and USNI do not tie it to the FONOP, and China demanded an end to close reconnaissance. Not counted."),
 (3545, "Military/Property", "N", "Trump-Tsai call, Dec 2, 2016. NPR: Foreign Minister Wang Yi called it 'a small trick by Taiwan'. A search for PLA drills after the call found nothing in an allowed outlet. The bomber loop around Taiwan (#3544) was a week before the call and the drone seizure (#3546) 14 days after, so neither is a reply inside 7 days."),
 (3548, "Military/Property", "N", "$1.4B sale, Jun 29, 2017. CBS (AP): Lu Kang demanded the deal be cancelled. A search for a PLA drill in Jun 30-Jul 6, 2017 found nothing in an allowed outlet."),
 (3549, "Military/Property", "N", "Stethem FONOP at Triton Island, Jul 2, 2017. Al Jazeera: China sent vessels and fighters to warn the ship off, which is the routine response (background), and called it a serious provocation. Same search window as #3548; none found."),
 (3550, "Military/Property", "N", "McCain FONOP at Mischief Reef, Aug 10, 2017. A Chinese frigate radioed the ship and China said it would protest. Routine shadowing plus words (" + _ONLY_WORDS + ")."),
 (3552, "Military/Property", "Unverified", "Taiwan Travel Act, Mar 16, 2018. The reaction that Chinese officials were reported to give was found only on outlets that are not allowed, and PLA activity in Mar 17-23 was not searched."),
 (3558, "Military/Property", "N", "Mustin and Benfold Strait transit, Jul 7, 2018. USNI: US officials would not say whether the PLA Navy responded; the Global Times said the ships were at least shadowed. Words and shadowing only (" + _ONLY_WORDS + ")."),
 (3561, "Economic/Blockade", "N", "Sanctions on the Equipment Development Department, Sep 20, 2018. Al Jazeera: Geng Shuang warned of consequences unless the sanctions were withdrawn. No counter-sanction or drill in that report. The Decatur close pass (#3563) came on day 10, outside the window. China's tariffs of Sep 18 (#3560) came before the sanctions."),
 (3562, "Military/Property", "R-weak", "Decatur FONOP at Gaven Reefs, Sep 30, 2018 -> the destroyer Lanzhou crosses in front of it at about 45 yards the same day (#3563, The War Zone). China did not say it answered the FONOP; the link is the encounter itself."),
 (3564, "Military/Property", "Unverified", "Stockdale and Pecos Strait transit, Nov 28, 2018. USNI: the Navy reported no significant interactions with Chinese ships. The window was not searched."),
]

# Reply pairs (pair id, trigger, reply, category, reply caused casualties Y/N, note)
PAIRS = [
 (3500, 3532, 3533, "Military/Property", "N", "Chinese fighters and an early-warning aircraft patrol the new air defense zone four days after the B-52 flight (link plausible only)"),
 (3501, 3539, 3540, "Economic/Blockade", "N", "China says it will sanction US firms the day after the $1.83B Taiwan arms sale (no firm named)"),
 (3502, 3562, 3563, "Military/Property", "N", "A Chinese destroyer crosses the Decatur's bow at about 45 yards the same day as the FONOP"),
]

# No continuous-fighting windows here: the log shows no Chinese pace dense enough to need one before Jan 2019.
WINDOWS = []
START_ACTS = set()

# Phases (oldest first)
PHASES = [
 ("Third Taiwan Strait Crisis", d(1995, 5, 22), d(1996, 12, 31), "Lee visa (#3500), missile tests and drills (#3501-#3502, #3504), carriers sent (#3505), Clinton-Jiang meetings (#3503, #3507-#3508)"),
 ("Engagement and the embassy bombing", d(1997, 1, 1), d(2001, 3, 31), "Jiang visit and Clinton trip (#3509-#3510), the Belgrade bombing and protests (#3511-#3512), WTO deal (#3513), the House Taiwan bill (#3514)"),
 ("EP-3 collision and the Bush years", d(2001, 4, 1), d(2008, 12, 31), "EP-3 collision and crew release (#3515-#3516), the April 2001 sale (#3517), summits (#3518, #3520, #3522), anti-satellite test (#3523), Oct 2008 sale (#3524)"),
 ("Obama: sales, summits and incidents at sea", d(2009, 1, 1), d(2015, 9, 30), "Impeccable (#3525), Jan 2010 and Sep 2011 sales (#3527, #3529), Australia deployment (#3530), air defense zone (#3532-#3533), Cowpens and P-8 incidents (#3534-#3535), summits (#3526, #3528, #3531, #3536)"),
 ("FONOPs begin and the Trump transition", d(2015, 10, 1), d(2017, 12, 31), "Xi visit (#3537), Lassen and later FONOPs (#3538, #3541-#3542, #3549-#3550), Dec 2015 sale (#3539-#3540), Trump-Tsai call (#3545), drone seizure (#3546), Mar-a-Lago and Beijing summits (#3547, #3551)"),
 ("Trade war and the Decatur incident", d(2018, 1, 1), d(2019, 1, 6), "Taiwan Travel Act (#3552), tariffs and counter-tariffs (#3554-#3560), Sep 2018 sanctions (#3561), Decatur and Lanzhou (#3562-#3563), Buenos Aires truce (#3565), Asia Reassurance Initiative Act (#3566)"),
]

CHAIN_NAMES = {
 3532: "Nov 2013 B-52 flight -> PLA patrol of the air defense zone",
 3539: "Dec 2015 sale -> China vows sanctions on US firms",
 3562: "Sep 2018 Decatur FONOP -> Lanzhou close pass",
}
