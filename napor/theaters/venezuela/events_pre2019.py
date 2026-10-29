"""NAPOR Caribbean / Venezuela: from Chavez's inauguration to the eve of the Guaido recognition, Feb 2, 1999 - Jan 10, 2019 (research file).

Same shape as events.py. Event IDs 4500-4599 and pair IDs 4500-4599 belong to this file (4500-4568 used).
events.py continues from Jan 23, 2019 (IDs 4001-4066).

Option letters for US moves are the ones in events.py and config.py (B talks or deals, C sanctions and designations,
E naval and air posture, H other). D, F and G (boat strikes, land strikes, raids on leaders) have no case before 2019.
A (hold) is not tagged, and hold weeks start in Aug 2025 (config.HOLD_START), so nothing in this file makes a hold week.
Judgment calls on letters and kinds:
- Expulsions of diplomats, visa revocations, a statement that blames Chavez for the 2002 ouster, the Aug 2017 "military option" remark,
  Tillerson's coup remark, the NYT-reported officer meetings and the Jan 2019 non-recognition are tagged H (other).
  They are US political moves, not sanctions and not talks. The 2002 and 2018 statements are words, not acts, and are said so in the notes.
- Sanctions, a law that requires sanctions, executive orders, arms-sale bans and the Kingpin and drug-certification designations are tagged C.
- The Obama-Chavez handshake, the Jun 2009 return of ambassadors and the Jun 2016 Shannon visit are tagged B. Their action types start
  with "Talks" or "Diplomatic step" so the political category sees them as talks or deals.
- Venezuelan expulsions of US diplomats start with "Expulsion" and so count as counter-measures in the economic category (14 days).
  The May 2018 EO and the expulsion the next day are the clearest case. Venezuelan statements start with "Statement" and are not replies.
- Venezuelan military drills and orders to prepare for war start with "Mobilization" and count as hostile acts (7 days), as in events.py.
- Russian moves (bombers, ships), the oil strike, the Constituent Assembly vote, the drone incident and the UN seat vote have no option letter.
  Actors that are not the Venezuelan government ("Opposition...", "Unknown group...") are kept off Venezuela's side on purpose.

Source rules (docs/SOURCE_STANDARD.md):
- Only allowed outlets and official releases. Wire stories read on a syndicated page are labelled "AP (via ...)", "Reuters (via ...)", "NPR (via ...)".
  seen="full text" means the page was opened and read; every row here was read that way.
- Several 2002-2009 rows rest on a CRS report (everycrsreport.com mirror), which is an official Congress page that the engine scores 0.60
  (an outlet that is not on the news list), so a row on one of them alone is flagged "use with caution". Rows #4506, #4521 and #4542 are in that group.
  The "published" date of a CRS page is the version date from the page address.
- Some pages carry no date in their text. Where the date comes from the page address, from the day of the week in the text or from the
  publication day, the row is in PARTLY below.
- No Telesur or VTV page was opened. What Venezuelan officials say is used only as an allowed outlet reports it.

How reply windows were read (CENSUS below):
- R-strong / R-weak: a counted Venezuelan hostile act (a military mobilization, drills or an order to prepare for war) inside 7 days of the move.
  This tab's rule (rules.py) keeps these only when such an act is logged; otherwise the row becomes N.
- N: the source read reports only words, a diplomatic step, an expulsion or nothing. The note says "words only in the source read" or similar.
  I ran no separate search for days 2-7 except where a note says so, so these N rows are weak evidence.
- Unclear: another Venezuelan act sits near the window and no page ties it to the move.
- Unverified: the window was not searched. These are logged but not counted as cases.

Dropped, not logged (no allowed source found or no page I could open):
- The May 1999 refusal of US overflights (Inter Press Service only), Chavez turning away two US ships with troops after the Dec 1999 mudslides
  (an NPR page with no date), his Oct 2001 criticism of the Afghan bombing and the recall of the US ambassador (no allowed page), the Jan 2003
  "Friends of Venezuela" group (an AP page that gives no date), the Aug 2004 recall vote reaction (a Knight Ridder page only), the Nov 2015
  arrest of two relatives of Maduro's wife, the Dec 2017 and Jan 2018 Dominican Republic talks (no allowed page), the Apr 2008 Fourth Fleet
  announcement (a Defense Department page that could not be opened), the Mar 2013 US expulsion of two Venezuelan diplomats (a Christian Science
  Monitor page only), the Dec 2018 sanctions by the EU and Canada, and any Telesur or VTV page.
"""
import datetime as dt


def d(y, m, day):
    return dt.date(y, m, day)


def _s(headline, outlet, published, url, seen="full text"):
    return {'headline': headline, 'outlet': outlet, 'published': published, 'seen': seen, 'url': url}


_CRS05 = _s('Venezuela: Political Conditions and U.S. Policy (CRS Report RL32488, 2005 version)', 'CRS (via EveryCRSReport)', '2005-04-01', 'https://www.everycrsreport.com/files/20050401_RL32488_6fe3a6534b668b075a9cfc1654132b699d98692f.html')
_CRS07 = _s('Venezuela: Political Conditions and U.S. Policy (CRS Report RL32488, 2007 version)', 'CRS (via EveryCRSReport)', '2007-06-08', 'https://www.everycrsreport.com/files/20070608_RL32488_62f7562a398c9d5cf8b471380bbe69f652082422.html')
_CRS09 = _s('Venezuela: Political Conditions and U.S. Policy, 2003-2009 (CRS Report RL32488)', 'CRS (via EveryCRSReport)', '2009-07-28', 'https://www.everycrsreport.com/files/20090728_RL32488_21b7532ab19812cfba4244603c93497b71cb067a.html')
_CRS19 = _s('Venezuela: Background and U.S. Relations (CRS Report R44841, Jan 2019 version)', 'CRS (via EveryCRSReport)', '2019-01-21', 'https://www.everycrsreport.com/files/20190121_R44841_01751feeef096c5aeb2bb3d47c1a538d8f492a2f.html')
_CNN_COUP = _s('Chavez back in power after two days (CNN, Apr 14, 2002)', 'CNN', '2002-04-14', 'https://edition.cnn.com/2002/WORLD/americas/04/14/venezuela/index.html')
_AJ_DUDDY = _s('Venezuela, U.S. ambassadors (Al Jazeera, Apr 19, 2009)', 'Al Jazeera', '2009-04-19', 'https://www.aljazeera.com/news/2009/4/19/caracas-will-restore-envoy-to-us')
_NBC_PALMER = _s('U.S., Venezuela evict ambassadors in diplomatic spat', 'NBC News', '2010-12-29', 'https://www.nbcnews.com/id/40851907/ns/politics-more_politics')
_AJ_ROBINSON = _s('Nicolas Maduro expels US envoy amid new sanctions', 'Al Jazeera', '2018-05-22', 'https://www.aljazeera.com/amp/news/2018/5/22/nicolas-maduro-expels-us-envoy-amid-new-sanctions')
_AJ_MIL15 = _s('Venezuela stages military drill to counter US "threat"', 'Al Jazeera', '2015-03-15', 'https://www.aljazeera.com/news/2015/3/15/venezuela-stages-military-drill-to-counter-us-threat')
_AJ_MIL17 = _s('Venezuela: Call for military drills after Trump threat', 'Al Jazeera', '2017-08-15', 'https://www.aljazeera.com/news/2017/8/15/venezuela-call-for-military-drills-after-trump-threat')
_WGBH_MADURO = _s('In wake of sham election, U.S. sanctions Venezuelan president Maduro', 'NPR (via GBH News)', '2017-07-31', 'https://www.wgbh.org/news/2017-07-31/in-wake-of-sham-election-u-s-sanctions-venezuelan-president-maduro')
_NPR_COUP18 = _s('NYT: Trump administration met with Venezuelan coup plotters', 'NPR', '2018-09-09', 'https://www.npr.org/2018/09/09/646018005/nyt-trump-administration-met-with-venezuelan-coup-plotters')
_KNAU_COUP18 = _s('Venezuela decries reported meetings between U.S. officials and coup plotters', 'NPR (via KNAU)', '2018-09-09', 'https://www.knau.org/2018-09-09/venezuela-decries-reported-meetings-between-u-s-officials-and-coup-plotters')
_AJ_COUP18 = _s('Trump officials met Venezuela military coup plotters', 'Al Jazeera', '2018-09-09', 'https://www.aljazeera.com/news/2018/09/trump-officials-met-venezuela-military-coup-plotters-180909061033703.html')
_PBS_MADURO19 = _s('Nicolas Maduro to be sworn in to 2nd term amid Venezuela\'s economic crisis', 'PBS NewsHour', '2019-01-10', 'https://www.pbs.org/newshour/amp/world/nicolas-maduro-to-be-sworn-in-to-2nd-term-amid-venezuelas-economic-crisis')
_AJ_MADURO19 = _s('Peru, Paraguay recall diplomats over Maduro inauguration', 'Al Jazeera', '2019-01-10', 'https://www.aljazeera.com/amp/news/2019/1/10/peru-paraguay-recall-diplomats-over-maduro-inauguration')
_AJ_PNG = _s('Duddy and Alvarez (Al Jazeera, Apr 19, 2009)', 'Al Jazeera', '2009-04-19', 'https://www.aljazeera.com/news/2009/4/19/caracas-will-restore-envoy-to-us')
_BLOOM_PDVSA = _s('Venezuela to study how sanctions will affect oil dispatches', 'Bloomberg', '2011-05-24', 'https://www.bloomberg.com/news/2011-05-24/venezuela-to-study-how-sanctions-will-affect-oil-dispatches-1-.html')
_AJ_COL = _s('Colombia and US sign military pact', 'Al Jazeera', '2009-10-30', 'https://www.aljazeera.com/news/2009/10/30/colombia-and-us-sign-military-pact')
_AJ_ATT = _s('Rumsfeld likens Chavez to Hitler', 'Al Jazeera', '2006-02-03', 'https://www.aljazeera.com/news/2006/2/3/rumsfeld-likens-chavez-to-hitler')
_NBC_ATT = _s('U.S. orders expulsion of Venezuelan diplomat', 'NBC News', '2006-02-03', 'https://www.nbcnews.com/id/wbna11164104')
_TREAS_HP1132 = _s('Treasury designates senior Venezuelan government officials as drug traffickers (Kingpin Act)', 'Treasury/OFAC (official release)', '2008-09-12', 'https://home.treasury.gov/news/press-releases/hp1132')

# Columns: ID, Date, Actor, Action Type, Target, Detail, Trigger ID, Severity, Confidence, Source
EVENTS = [
# --- 1999-2004: Chavez's first term, the 2002 coup attempt and strike ---
(4500, d(1999,2,2), "Venezuela (Chavez)", "Inauguration (Hugo Chavez takes office)", "Venezuela", "CNN's 2024 profile says Chavez took power on Feb 2, 1999. This is where the log starts. Later rows trace how Washington and Chavez's government fell into conflict", None, "n/a", "Medium", "see audit"),
(4501, d(2000,8,10), "Venezuela (Chavez)", "Visit (Chavez meets Saddam Hussein in Baghdad)", "Iraq", "Chavez is the first head of state to visit Iraq since the 1991 Gulf War and goes in by car from Iran to avoid the UN flight ban. State Department spokesman Richard Boucher asks why he would raise the prestige of a dictator; US officials say Iraq is using the visit for propaganda. Chavez: 'What can I do if they (Americans) get upset?'", None, "n/a", "Medium", "see audit"),
(4502, d(2002,4,12), "Venezuela (military leaders)", "Coup attempt (military removes Chavez; Pedro Carmona takes over)", "Venezuelan presidency", "Military leaders remove Chavez after a protest in which 12 people died, according to the State Department (CNN). Business leader Pedro Carmona takes over on Apr 12 (CRS dates the removal Apr 11). He resigns the next day under military pressure", None, "n/a", "Medium", "see audit"),
(4503, d(2002,4,12), "US", "Statement (Bush administration blames Chavez and calls it a change of government)", "Chavez government", "Officials call Chavez's exit a 'change of government', say he brought it on himself and show open satisfaction (Washington Post, Apr 13). The State Department says the US 'expressed solidarity with the Venezuelan people' (CRS). They hope for elections by year's end. These are words, not an act", 4502, "n/a", "Medium", "see audit"),
(4504, d(2002,4,14), "Venezuela (Chavez)", "Return to power (Chavez back in the presidential palace)", "Venezuelan presidency", "Chavez returns before dawn on Sunday. National Security Adviser Rice says he 'needs to respect constitutional processes'. On Apr 16 White House spokesman Fleischer says US officials had told opposition leaders the US would not support a coup and that the US voted at the OAS to condemn the 'alteration of constitutional order'", 4502, "n/a", "Medium", "see audit"),
(4505, d(2002,12,2), "Opposition and PDVSA strikers", "Work stoppage (general strike that cuts oil exports)", "Venezuelan oil industry", "A strike to force Chavez out begins on Dec 2 and cuts Venezuela's oil output by more than two-thirds (AP, Jan 23, 2003). NPR (Dec 9) reports panic at refineries and worry about exports to the US. The strike runs to early Feb 2003", None, "n/a", "Medium", "see audit"),
(4506, d(2004,8,15), "Venezuela (Chavez)", "Recall referendum (Chavez wins)", "Venezuelan presidency", "Chavez wins the recall vote, 59.3% 'no' to 40.7% 'yes' (CRS). The OAS passes a resolution on Aug 26 saying it is satisfied with the holding of the referendum. CRS notes Chavez said in April 2004 he would stop selling oil to the US if it kept 'intervening' and in June that Bush would be his greatest rival", None, "n/a", "Medium", "see audit"),
# --- 2005-2008: oil threats, DEA, arms ban, expulsions, Russia ---
(4507, d(2005,3,4), "Venezuela (Chavez)", "Statement (threat to cut oil to the US if attacked)", "US", "Speaking in New Delhi, Chavez renews his threat: 'If there is any aggression, there will be no oil.' The State Department calls his claim that Washington plots to kill him 'ridiculous and untrue'", None, "n/a", "Medium", "see audit"),
(4508, d(2005,4,22), "Venezuela (Chavez)", "Expulsion (US military instructors)", "US military instructors and one student", "Venezuela orders four US military instructors and one student to leave its bases and schools under a bilateral exchange programme. The US embassy says it 'regrets this unexpected action'", None, "n/a", "Medium", "see audit"),
(4509, d(2005,8,8), "Venezuela (Chavez)", "Counter-measure (ends anti-drug cooperation with the DEA)", "US Drug Enforcement Administration", "Chavez says he has suspended cooperation with the DEA, which he says was used as a cover to spy on his government, while voting in local elections. The US rejects the charge", None, "n/a", "Medium", "see audit"),
(4510, d(2005,9,15), "US", "Designation (Venezuela 'failed demonstrably' on drug cooperation)", "Venezuela", "Bush lists Venezuela as a major drug-transit country that 'failed demonstrably' to meet its counternarcotics obligations over the past 12 months, but keeps US funds for democracy and community programs (White House press statement; CRS)", None, "n/a", "High", "see audit"),
(4511, d(2006,2,2), "US", "Statement (Rumsfeld compares Chavez to Hitler)", "Chavez", "Defense Secretary Rumsfeld says Chavez was 'elected legally just as Adolf Hitler was elected legally'. A State Department spokesman later says the comparison misses the mark. Words, not an act", None, "n/a", "Medium", "see audit"),
(4512, d(2006,2,2), "Venezuela (Chavez)", "Expulsion (US naval attache John Correa)", "US Navy attache in Caracas", "Chavez expels the attache, saying he passed secret information from Venezuelan officers to the Pentagon. The State Department denies any spying", 4511, "n/a", "Medium", "see audit"),
(4513, d(2006,2,3), "US", "Expulsion (Venezuelan ambassador's chief of staff)", "Jeny Figueredo Frias, Venezuelan embassy", "The State Department declares her persona non grata and gives her 72 hours to leave. Spokesman Sean McCormack: 'we were forced to respond' to the expulsion of the attache", 4512, "n/a", "Medium", "see audit"),
(4514, d(2006,2,4), "Venezuela (Chavez)", "Statement (says Bush is worse than Hitler and the US weighs an invasion)", "US", "At a rally marking his 1992 coup attempt Chavez says 'Hitler would be like a suckling baby next to George Bush', calls the US attitude 'imperialist, genocidal, fascist', says Washington is considering an invasion and calls for more weapons. US officials call it inflammatory rhetoric and say they plan no break in relations", 4511, "n/a", "Medium", "see audit"),
(4515, d(2006,2,18), "Venezuela (Chavez)", "Statement (oil warning: no oil if the US 'crosses the line')", "US", "Chavez says that if the US government crosses the line it will get none of Venezuela's oil, and that he has started taking measures toward that end without saying which", None, "n/a", "Medium", "see audit"),
(4516, d(2006,5,15), "US", "Sanction (ban on arms sales to Venezuela)", "Venezuela (arms trade)", "The State Department bans all US commercial weapons sales and bars other countries from re-selling US arms and technology, and names Venezuela as not cooperating fully on terrorism. It cites Chavez's ties with Cuba and Iran and his failure to act against Colombian guerrillas", None, "n/a", "Medium", "see audit"),
(4517, d(2006,5,15), "Venezuela (Chavez)", "Statement (dismisses the arms ban, says oil will not be used as a weapon)", "US", "Speaking in London, Chavez says 'this doesn't matter to us at all', calls the US 'the empire' and says Venezuela will not retaliate and will never use oil as a political weapon against a people", 4516, "n/a", "Medium", "see audit"),
(4518, d(2006,9,20), "Venezuela (Chavez)", "Statement (calls Bush 'the devil' at the UN)", "US", "The day after Bush speaks, Chavez makes the sign of the cross and calls him 'the devil' at the UN General Assembly. US Ambassador John Bolton says the remarks do not deserve a reply", None, "n/a", "Medium", "see audit"),
(4519, d(2006,10,17), "US", "Diplomatic contest (backs Guatemala against Venezuela for a UN Security Council seat)", "Venezuela", "Guatemala beats Venezuela 110 to 77 in the tenth round but neither reaches two thirds. Venezuela's UN ambassador accuses Washington of 'brutal pressure'. A Tanzanian ambassador says Guatemala might have won outright without the US lobbying. A compromise later picks Panama", None, "n/a", "Medium", "see audit"),
(4520, d(2008,9,8), "Russia", "Announcement (navy to join exercises with Venezuela in November)", "Venezuela", "Russia says its nuclear-powered cruiser Peter the Great and the destroyer Admiral Chabanenko will take part in naval exercises with Venezuela, the first near the US since the Cold War. White House spokesman Gordon Johndroe says the US will 'watch how the exercise went'", None, "n/a", "Medium", "see audit"),
(4521, d(2008,9,10), "Russia", "Deployment (two Tu-160 bombers arrive in Venezuela)", "Venezuela", "Two Russian long-range bombers arrive for training exercises with the Venezuelan military (CRS)", None, "n/a", "Medium", "see audit"),
(4522, d(2008,9,11), "Venezuela (Chavez)", "Expulsion (US ambassador Patrick Duddy, 72 hours to leave)", "US ambassador to Venezuela", "In support of Bolivia, which expelled the US ambassador a day earlier, Chavez gives Duddy 72 hours to leave and recalls Venezuela's ambassador Bernardo Alvarez, who he says will return 'when there's a new government in the United States'. He accuses the US of backing a plot to kill him and offers no evidence", None, "n/a", "Medium", "see audit"),
(4523, d(2008,9,12), "US", "Expulsion (Venezuelan ambassador Bernardo Alvarez declared persona non grata)", "Venezuelan ambassador to the US", "CRS dates it Sep 12. Al Jazeera (Apr 2009) says the Bush administration then expelled both countries' ambassadors", 4522, "n/a", "Medium", "see audit"),
(4524, d(2008,9,12), "US", "Sanction (Kingpin Act: two senior intelligence officials and a former interior minister)", "Hugo Carvajal, Henry Rangel Silva, Ramon Rodriguez Chacin", "OFAC freezes the US assets of the heads of Venezuela's military intelligence and its police intelligence service and a former interior minister for helping the FARC's drug trafficking", None, "n/a", "High", "see audit"),
(4525, d(2008,11,25), "Russia", "Deployment (Russian warships enter Venezuelan waters for joint exercises)", "Venezuela", "Russian ships arrive for exercises on Dec 1, Moscow's first deployment to the region since the Cold War. Chavez says it is not a provocation. State Department spokesman Sean McCormack: 'that's fine', but the US will be 'watching it very closely'", None, "n/a", "Medium", "see audit"),
# --- 2009-2012: thaw, Colombia bases, ambassadors ---
(4526, d(2009,4,17), "US", "Talks (Obama shakes hands with Chavez at the Summit of the Americas)", "Venezuela (Chavez)", "Obama and Chavez exchange handshakes and Chavez gives him Galeano's 'Open Veins of Latin America'. The White House says the two sides did not discuss restoring ambassadors. Chavez calls it 'a good moment'", None, "n/a", "Medium", "see audit"),
(4527, d(2009,4,19), "Venezuela (Chavez)", "Diplomatic step (will send an ambassador back to Washington)", "US", "Chavez says he will restore Venezuela's envoy to the US, hours after saying he has no doubt relations will improve with Obama in the White House. No immediate US response", 4526, "n/a", "Medium", "see audit"),
(4528, d(2009,6,25), "US", "Talks (US and Venezuela agree to return their ambassadors)", "Venezuela", "The State Department says the two countries agree to send ambassadors back after the tit-for-tat expulsions of Sep 2008. Duddy is to return to Caracas and Alvarez to Washington", None, "n/a", "High", "see audit"),
(4529, d(2009,10,30), "US", "Posture (agreement for greater US access to seven Colombian bases)", "Colombia (military bases)", "Colombia and the US sign a pact giving US forces greater access to seven Colombian bases, with $46 million to refurbish the Palanquero air base. Washington and Bogota say the deal will not exceed 800 troops and 600 civilian contractors", None, "n/a", "Medium", "see audit"),
(4530, d(2009,11,9), "Venezuela (Chavez)", "Mobilization (army told to prepare for war; 15,000 troops sent to the Colombian border the week before)", "Colombia border", "On his weekly show Chavez says US access to Colombian bases threatens Venezuela and 'the best way to avoid war is preparing for it'. Al Jazeera says he ordered 15,000 soldiers to the border the week before, without a day", 4529, "n/a", "Medium", "see audit"),
(4531, d(2010,7,25), "Venezuela (Chavez)", "Statement (threat to cut oil to the US if Colombia attacks)", "US", "After Colombia presents evidence of FARC camps in Venezuela at the OAS, Chavez calls it a 'bogus show', says he will break relations with Colombia and put border troops on alert, and threatens to cut oil to the US if US-allied Colombia attacks. The US backs Colombia and calls his response 'petulant'", None, "n/a", "Medium", "see audit"),
(4532, d(2010,12,28), "Venezuela (Chavez)", "Statement (dares the US to expel his ambassador; rejects Larry Palmer)", "US", "Chavez has refused to accept Larry Palmer, Obama's pick as ambassador, since August over remarks on low military morale and rebels in Venezuela. He says 'If the government is going to expel our ambassador there, let them do it'", None, "n/a", "Medium", "see audit"),
(4533, d(2010,12,29), "US", "Visa revocation (Venezuelan ambassador Bernardo Alvarez)", "Venezuelan ambassador to the US", "The State Department revokes his visa; spokesman P.J. Crowley calls it 'appropriate, proportional and reciprocal action'. Alvarez was not in the US at the time", 4532, "n/a", "Medium", "see audit"),
(4534, d(2011,5,24), "US", "Sanction (PDVSA over gasoline additive deliveries to Iran)", "PDVSA (Venezuelan state oil company)", "The State Department sanctions PDVSA and six other foreign companies for working with Iran's energy sector. It says PDVSA delivered at least two cargoes of a gasoline additive worth $50 million to Iran between December and March", None, "n/a", "Medium", "see audit"),
(4535, d(2011,5,24), "Venezuela (government)", "Statement (may not be able to guarantee all oil shipments to the US)", "US", "Venezuela says it may not be able to guarantee all future oil shipments to the US after the sanctions", 4534, "n/a", "Medium", "see audit"),
(4536, d(2012,1,8), "US", "Expulsion (Venezuelan consul general in Miami, Livia Acosta Noguera)", "Venezuelan consul general in Miami", "The State Department declares her persona non grata and orders her out by Jan 10 under Article 23 of the Vienna Convention. It had said it was looking into 'very disturbing' allegations, from a Univision documentary, that she took part in an alleged Iranian plot to launch cyber-attacks on US facilities. It gives no further reason", None, "n/a", "Medium", "see audit"),
# --- 2013-2016: Maduro, expulsions, the first sanctions ---
(4537, d(2013,3,5), "Venezuela (Maduro)", "Expulsion (two US Air Force attaches)", "US embassy in Caracas", "As Chavez's health worsens, Vice President Maduro gives one attache 24 hours to leave and Foreign Minister Jaua expels a second, accusing them of spying on the military and plotting to destabilize Venezuela. A Pentagon spokesperson rejects the claims", None, "n/a", "Medium", "see audit"),
(4538, d(2013,9,30), "Venezuela (Maduro)", "Expulsion (US charge d'affaires Kelly Keiderling and two diplomats)", "US embassy in Caracas", "Maduro gives Keiderling, Elizabeth Hunderland and David Mutt 48 hours to leave, accusing them of meeting the 'far right' and financing 'acts of sabotage against the electrical system'. The State Department rejects the claims", None, "n/a", "Medium", "see audit"),
(4539, d(2013,10,2), "US", "Expulsion (three Venezuelan diplomats, 48 hours)", "Venezuelan embassy in Washington", "The State Department calls the Venezuelan expulsions 'regrettable' and based on 'groundless allegations', and says they require reciprocal action. Al Jazeera's page gives the day as a Tuesday, which was Oct 1; the date here is set from the page address", 4538, "n/a", "Medium", "see audit"),
(4540, d(2014,2,17), "Venezuela (Maduro)", "Expulsion (three US consular officials)", "US embassy in Caracas", "Maduro expels three US diplomats, saying they supported opposition plots to overthrow him", None, "n/a", "Medium", "see audit"),
(4541, d(2014,2,25), "US", "Expulsion (three Venezuelan diplomats, 48 hours)", "Venezuelan embassy in Washington", "The State Department answers the Feb 17 expulsions. Spokeswoman Jen Psaki says the US stays open to relations but 'Venezuela also needs to show seriousness'. Foreign Minister Jaua calls it retaliation, not reciprocity", 4540, "n/a", "Medium", "see audit"),
(4542, d(2014,12,18), "US", "Sanction (law requires sanctions on officials who abuse protesters)", "Venezuelan officials", "President Obama approves the Venezuela Defense of Human Rights and Civil Society Act (Public Law 113-278). It requires sanctions on those responsible for violence and abuses against the 2014 protesters, with a presidential waiver. The requirement was first set to end on Dec 31, 2016", None, "n/a", "High", "see audit"),
(4543, d(2015,3,9), "US", "Sanction (executive order declares a national emergency; seven officials)", "Venezuelan intelligence, police and prosecution officials", "Obama signs an order declaring an 'unusual and extraordinary threat' to US national security, freezing the assets of seven officials including the head of the national intelligence service. The White House calls for release of political prisoners and says the US stays open to better relations. Maduro had accused the US of plotting a coup (NPR)", None, "n/a", "High", "see audit"),
(4544, d(2015,3,14), "Venezuela (Maduro)", "Mobilization (nationwide 10-day military exercises, about 100,000 troops)", "Venezuela (defense)", "Defense Minister Padrino opens the drills in Caracas and calls US sanctions 'an imminent danger'. About 20,000 civilians also take part. AFP: the drills came amid tension over the sanctions", 4543, "n/a", "Medium", "see audit"),
(4545, d(2016,6,20), "US", "Talks (State Department's Thomas Shannon visits Caracas to foster dialogue)", "Venezuela (Maduro)", "AP, Jun 21: Shannon visits during food riots and looting; spokesman John Kirby says he hopes to foster dialogue and will try to meet Maduro, who calls it 'very good that we're taking these steps with the US'. The page does not confirm a meeting took place", None, "n/a", "Medium", "see audit"),
# --- 2017: the Constituent Assembly, sanctions on Maduro, the military option ---
(4546, d(2017,2,13), "US", "Sanction (Vice President Tareck El Aissami named a drug kingpin)", "Tareck El Aissami and Samark Lopez", "Treasury freezes the assets of the vice president and a businessman under the Kingpin Act. Officials say the action is not a political message. Treasury's FAQ: designating an official does not block the government itself. The article reports no Venezuelan response", None, "n/a", "Medium", "see audit"),
(4547, d(2017,4,26), "Venezuela (Maduro)", "Diplomatic step (starts a 24-month process to leave the OAS)", "Organization of American States", "Foreign Minister Delcy Rodriguez announces it on TV and calls the OAS an 'interventionist coalition' led by Washington, shortly after OAS envoys vote to call a meeting of foreign ministers on Venezuela. The 24-month process means it is not an immediate break", None, "n/a", "Medium", "see audit"),
(4548, d(2017,5,18), "US", "Sanction (eight Supreme Court justices)", "Venezuela's Supreme Court president and seven Constitutional Chamber judges", "OFAC freezes their US assets under Executive Order 13692 over rulings that undermined the opposition-led National Assembly", None, "n/a", "High", "see audit"),
(4549, d(2017,7,26), "US", "Sanction (13 current and former senior officials)", "Venezuelan officials tied to the Constituent Assembly vote", "OFAC freezes assets of 13 officials, including the election council chief and police and National Guard leaders, ahead of the July 30 vote. NPR: about 100 people had died in four months of protests", None, "n/a", "High", "see audit"),
(4550, d(2017,7,30), "Venezuela (Maduro)", "Election (National Constituent Assembly vote)", "Venezuela", "The vote to elect an assembly that can rewrite the constitution is boycotted by the opposition. The US does not recognize it (CRS). At least 10 people die on election day (NPR via GBH)", None, "n/a", "Medium", "see audit"),
(4551, d(2017,7,31), "US", "Sanction (President Maduro personally)", "Nicolas Maduro", "Treasury freezes all of Maduro's US-jurisdiction assets a day after the vote; it is only the fourth time the US has sanctioned a sitting head of state. National Security Adviser McMaster calls him 'a dictator'. Mnuchin says 'all options are on the table'", 4550, "n/a", "High", "see audit"),
(4552, d(2017,8,11), "US", "Statement (Trump: a military option for Venezuela is not ruled out)", "Venezuela (Maduro)", "Trump tells reporters at his New Jersey golf course he is 'not going to rule out' a military option, 'certainly something that we could pursue'. Words, not an act", None, "n/a", "Medium", "see audit"),
(4553, d(2017,8,14), "Venezuela (Maduro)", "Mobilization (orders national military exercises for Aug 26-27)", "Venezuela (defense)", "Speaking to supporters in Caracas, Maduro tells them to prepare for an 'imperialist' invasion and orders a two-day defense operation with soldiers and civilians. He says he still wants talks with the US", 4552, "n/a", "Medium", "see audit"),
(4554, d(2017,8,24), "US", "Sanction (executive order on financial markets: PDVSA and government debt)", "Venezuelan government and PDVSA", "Trump signs it on Aug 24 (issued and effective Aug 25). It bars new debt over 90 days from PDVSA and over 30 days from the government, new equity, and purchases of government bonds issued before the order", None, "n/a", "High", "see audit"),
(4555, d(2017,8,26), "Venezuela (Maduro)", "Mobilization (nationwide armed forces exercises; civilians called to reserves)", "Venezuela (defense)", "Reuters: state TV says 'all Venezuelans between the ages of 18 and 60' must help in the 'integral defense of the nation'. The drills follow Trump's Aug 11 remark and the Aug 24 order. They were already announced on Aug 14", 4554, "n/a", "Medium", "see audit"),
# --- 2018 to the eve of the Guaido recognition ---
(4556, d(2018,2,1), "US", "Statement (Secretary of State Tillerson raises a military coup in Venezuela)", "Venezuela (Maduro)", "At the University of Texas Tillerson says Latin American militaries often 'handled' transitions from bad governments, denies advocating 'regime change', and jokes that Maduro could retire to a beach hacienda in Cuba. Words, not an act", None, "n/a", "Medium", "see audit"),
(4557, d(2018,2,2), "Venezuela (Defense Minister Padrino)", "Statement (armed forces 'radically reject' the remarks)", "US", "Padrino condemns the remarks as interference and reads a statement backing Maduro", 4556, "n/a", "Medium", "see audit"),
(4558, d(2018,3,19), "US", "Sanction (executive order bans US dealings in Venezuela's digital currency, the petro)", "Venezuela (petro cryptocurrency)", "Trump calls the petro an 'attempt to circumvent U.S. sanctions'. Maduro said he created the currency to get around the sanctions. Venezuela launched it in February 2018 and said it had $5 billion in investment commitments", None, "n/a", "Medium", "see audit"),
(4559, d(2018,5,21), "US", "Sanction (executive order bars purchases of Venezuelan government debt and certain assets), day after Maduro's re-election", "Venezuelan government", "OFAC posts the order 'Prohibiting Certain Additional Transactions with Respect to Venezuela' on May 21. The White House calls the May 20 vote a 'sham'", None, "n/a", "High", "see audit"),
(4560, d(2018,5,22), "Venezuela (Maduro)", "Expulsion (top US diplomat Todd Robinson and deputy Brian Naranjo, 48 hours)", "US embassy in Caracas", "In a TV speech Maduro says 'the empire doesn't dominate us here' and accuses the two of trying to sabotage the election. The Foreign Ministry calls the sanctions 'a crime against humanity'", 4559, "n/a", "Medium", "see audit"),
(4561, d(2018,8,4), "Unknown group (drone explosions)", "Incident (explosions from drones at a National Guard parade, Caracas)", "Maduro and the military parade", "Maduro survives an apparent assassination attempt while speaking; seven National Guard members are hurt. He blames the far right with Colombia's former president Santos and says planners live in Florida. A senior State Department official says the US 'had heard the reports'. A Colombian source calls the accusation baseless. Who carried out the attack is not established in the source", None, "7 hurt (CNN)", "Medium", "see audit"),
(4562, d(2018,9,8), "US", "Contact (reported meetings with Venezuelan officers who wanted to oust Maduro)", "Venezuelan military officers", "The New York Times reports at least three secret meetings abroad with officers who approached a US embassy; the officers asked for encrypted radios and the US declined. US officials neither confirm nor deny. A National Security Council spokesperson says US policy favors a peaceful return to democracy. The meetings happened earlier (plans in summer 2017 and in March and May 2018); the date is the report's", None, "n/a", "Medium", "see audit"),
(4563, d(2018,9,9), "Venezuela (Foreign Minister Arreaza)", "Statement (condemns 'intervention plans and support of military plots')", "US", "Arreaza says 'blatant evidence has come to light' in US media", 4562, "n/a", "Medium", "see audit"),
(4564, d(2018,9,25), "US", "Sanction (Maduro's wife Cilia Flores, Delcy Rodriguez, Jorge Rodriguez, Defense Minister Padrino)", "Maduro's inner circle", "Treasury sanctions four members of Maduro's inner circle. Mnuchin says they target officials who help Maduro keep control of the military and government. The article reports no Venezuelan response", None, "n/a", "Medium", "see audit"),
(4565, d(2018,11,1), "US", "Sanction (executive order on Venezuela's gold sector and corrupt transactions)", "Venezuelan gold sector", "Trump signs the order and National Security Adviser Bolton announces it, calling Venezuela, Cuba and Nicaragua the 'Troika of Tyranny'. Officials believe gold trade with Turkey weakens pressure on Maduro", None, "n/a", "Medium", "see audit"),
(4566, d(2018,12,10), "Russia", "Deployment (two Tu-160 nuclear-capable bombers land near Caracas)", "Venezuela", "Pompeo tweets that the Russian and Venezuelan governments are 'two corrupt governments squandering public funds'. Kremlin spokesman Peskov calls that 'undiplomatic'. A Pentagon spokesman has no specific information on the bombers", None, "n/a", "Medium", "see audit"),
(4567, d(2019,1,10), "Venezuela (Maduro)", "Inauguration (Maduro sworn in for a second term)", "Venezuela", "Sworn in at the Supreme Court in Caracas after a 2018 election the opposition largely boycotted. Most European and Latin American countries send no representatives. Peru and Paraguay recall their diplomats and Paraguay cuts ties", None, "n/a", "Medium", "see audit"),
(4568, d(2019,1,10), "US", "Statement (rejects Maduro's new term as illegitimate; joins OAS vote)", "Venezuela (Maduro)", "Bolton says the US will not recognize 'the Maduro dictatorship's illegitimate inauguration' and Pompeo calls it a 'usurpation of power'. The OAS votes not to recognize the term, on a resolution the US co-presented. Words and a vote, not an act against Venezuela", 4567, "n/a", "Medium", "see audit"),
]

SOURCES = {
 4500: [_s('Hugo Chavez: 10 key moments (CNN en Espanol)', 'CNN (CNN en Espanol)', '2024-02-01', 'https://cnnespanol.cnn.com/2024/02/01/hugo-chavez-10-momentos-clave-orix')],
 4501: [_s('Chavez goes his own way, to Iraq', 'CBS News (AP)', '2000-08-09', 'https://www.cbsnews.com/news/chavez-goes-his-own-way-151-to-iraq'),
        _s('Chavez In Baghdad', 'NPR (via KAXE)', '2000-08-08', 'https://www.kaxe.org/2000-08-08/chavez-in-baghdad')],
 4502: [_CNN_COUP, _CRS05],
 4503: [_s('U.S. supports new Venezuela government', 'Washington Post (via Lawrence Journal-World)', '2002-04-13', 'https://www2.ljworld.com/news/2002/apr/13/us_supports_new/'), _CRS05, _CNN_COUP],
 4504: [_CNN_COUP, _s('Press briefing by Ari Fleischer, Apr 16, 2002', 'White House (Bush archive)', '2002-04-16', 'https://georgewbush-whitehouse.archives.gov/news/releases/2002/04/20020416-5.html')],
 4505: [_s('Venezuela strike drives oil prices up', 'CBS News (AP)', '2003-01-23', 'https://www.cbsnews.com/news/venezuela-strike-drives-oil-prices-up'),
        _s('Venezuela general strike could hurt oil exports', 'NPR', '2002-12-09', 'https://www.npr.org/2002/12/09/871361/venezuela-general-strike-could-hurt-oil-exports')],
 4506: [_CRS05],
 4507: [_s('Chavez renews threat to cut oil to US', 'Al Jazeera (AFP)', '2005-03-04', 'https://www.aljazeera.com/amp/news/2005/3/4/chavez-renews-threat-to-cut-oil-to-us')],
 4508: [_s('Venezuela bans US military instructors', 'Al Jazeera', '2005-04-23', 'https://www.aljazeera.com/news/2005/4/23/venezuela-bans-us-military-instructors')],
 4509: [_s('Venezuela snaps drug ties with US', 'Al Jazeera (Reuters)', '2005-08-08', 'https://www.aljazeera.com/news/2005/8/8/venezuela-snaps-drug-ties-with-us'), _CRS07],
 4510: [_s('Statement on the annual list of major drug-producing and drug-transit countries, Sep 15, 2005', 'White House (Bush archive)', '2005-09-15', 'https://georgewbush-whitehouse.archives.gov/news/releases/2005/09/20050915-1.html'), _CRS07],
 4511: [_AJ_ATT, _CRS07],
 4512: [_AJ_ATT, _NBC_ATT, _CRS07],
 4513: [_NBC_ATT, _AJ_ATT],
 4514: [_s('Chavez: Bush worse than Hitler', 'Al Jazeera', '2006-02-05', 'https://www.aljazeera.com/news/2006/2/5/chavez-bush-worse-than-hitler')],
 4515: [_s('Chavez warns US over Venezuelan oil', 'Al Jazeera', '2006-02-18', 'https://www.aljazeera.com/archive/2006/02/2008410115652521187.html')],
 4516: [_s('US bans arms sales to Venezuela', 'Al Jazeera', '2006-05-15', 'https://www.aljazeera.com/news/2006/5/15/us-bans-arms-sales-to-venezuela'), _CRS07],
 4517: [_s('US bans arms sales to Venezuela', 'Al Jazeera', '2006-05-15', 'https://www.aljazeera.com/news/2006/5/15/us-bans-arms-sales-to-venezuela')],
 4518: [_s('Chavez calls Bush devil, assails U.S. policies', 'NPR', '2006-09-20', 'https://www.npr.org/2006/09/20/6111992/chavez-calls-bush-devil-assails-u-s-policies'), _CRS07],
 4519: [_s('Stalemate in UN ballot', 'Al Jazeera', '2006-10-17', 'https://www.aljazeera.com/news/2006/10/17/stalemate-in-un-ballot')],
 4520: [_s('Russia sending navy to Venezuela', 'Al Jazeera', '2008-09-08', 'https://www.aljazeera.com/news/2008/9/8/russia-sending-navy-to-venezuela')],
 4521: [_CRS09],
 4522: [_s('Diplomats ousted as U.S.-Latin row deepens', 'CBS News (AP)', '2008-09-11', 'https://www.cbsnews.com/news/diplomats-ousted-as-us-latin-row-deepens-11-09-2008/'),
        _s('Venezuelan leader orders U.S. ambassador out', 'NBC News', '2008-09-11', 'https://www.nbcnews.com/news/amp/wbna26665875'),
        _s('Chavez expels U.S. ambassador (CNN, Sep 11, 2008)', 'CNN', '2008-09-11', 'https://us.cnn.com/2008/WORLD/americas/09/11/venezuela.us/index.html'), _CRS09],
 4523: [_CRS09, _AJ_PNG],
 4524: [_TREAS_HP1132, _CRS09],
 4525: [_s('Russian warships enter Venezuela', 'Al Jazeera', '2008-11-25', 'https://www.aljazeera.com/news/2008/11/25/russian-warships-enter-venezuela')],
 4526: [_s('Obama offers cooperation during South American summit', 'AP (via MPR News)', '2009-04-18', 'https://www.mprnews.org/story/2009/04/18/obama_south_america_summit'), _AJ_DUDDY],
 4527: [_AJ_DUDDY],
 4528: [_s('US and Venezuela to restore ties', 'Al Jazeera (Reuters)', '2009-06-25', 'https://www.aljazeera.com/news/2009/6/25/us-and-venezuela-to-restore-ties'), _CRS09],
 4529: [_AJ_COL],
 4530: [_s('Prepare for war, Chavez tells army', 'Al Jazeera', '2009-11-09', 'https://www.aljazeera.com/news/2009/11/9/prepare-for-war-chavez-tells-army')],
 4531: [_s('Venezuela threatens oil cut to US', 'Al Jazeera', '2010-07-25', 'https://www.aljazeera.com/news/2010/7/25/venezuela-threatens-oil-cut-to-us')],
 4532: [_NBC_PALMER, _s('U.S. revokes Venezuelan ambassador\'s visa', 'NBC News', '2010-12-29', 'https://www.nbcnews.com/id/wbna40846053')],
 4533: [_NBC_PALMER, _s('U.S. revokes Venezuelan ambassador\'s visa', 'NBC News', '2010-12-29', 'https://www.nbcnews.com/id/wbna40846053')],
 4534: [_BLOOM_PDVSA],
 4535: [_BLOOM_PDVSA],
 4536: [_s('US expels Venezuelan consul general', 'Al Jazeera', '2012-01-08', 'https://www.aljazeera.com/news/2012/1/8/us-expels-venezuelan-consul-general')],
 4537: [_s('Venezuela expels 2 U.S. officials amid spy accusation', 'CBS News (AP)', '2013-03-05', 'https://cbsnews.com/news/venezuela-expels-2-us-officials-amid-spy-accusation')],
 4538: [_s('Venezuela expels US diplomats for "sabotage"', 'Al Jazeera', '2013-10-01', 'https://www.aljazeera.com/amp/news/2013/10/1/venezuela-expels-us-diplomats-for-sabotage')],
 4539: [_s('US expels Venezuelan diplomats in retaliation', 'Al Jazeera', '2013-10-02', 'https://www.aljazeera.com/amp/news/2013/10/2/us-expels-venezuelan-diplomats-in-retaliation')],
 4540: [_s('US expels three Venezuelan diplomats', 'Al Jazeera', '2014-02-26', 'https://www.aljazeera.com/amp/news/2014/2/26/us-expels-three-venezuelan-diplomats')],
 4541: [_s('US expels three Venezuelan diplomats', 'Al Jazeera', '2014-02-26', 'https://www.aljazeera.com/amp/news/2014/2/26/us-expels-three-venezuelan-diplomats')],
 4542: [_s('Venezuela Defense of Human Rights and Civil Society Act of 2014 (Public Law 113-278)', 'Congress (govinfo.gov)', '2014-12-18', 'https://www.govinfo.gov/content/pkg/PLAW-113publ278/html/PLAW-113publ278.htm')],
 4543: [_s('Obama imposes sanctions on Venezuela, invoking emergency powers', 'NPR (via MPR News)', '2015-03-09', 'https://mprnews.org/story/2015/03/09/npr-sanctions-venezuela'),
        _s('Statement by the Press Secretary on Venezuela, Mar 9, 2015', 'White House (Obama archive)', '2015-03-09', 'https://obamawhitehouse.archives.gov/the-press-office/2015/03/09/statement-press-secretary-venezuela')],
 4544: [_AJ_MIL15, _s('Venezuela gears up military machine amid economic crunch', 'Defense News (AFP)', '2015-03-15', 'https://www.defensenews.com/global/the-americas/2015/03/15/venezuela-gears-up-military-machine-amid-economic-crunch/')],
 4545: [_s('Top US diplomat meets officials amid crisis', 'AP (via Jamaica Gleaner)', '2016-06-21', 'https://jamaica-gleaner.com/article/world-news/20160622/top-us-diplomat-meets-officials-amid-crisis')],
 4546: [_s('U.S. Treasury sanctions Venezuelan vice president over drug trade allegations', 'NPR', '2017-02-13', 'https://www.npr.org/sections/thetwo-way/2017/02/13/515074498/u-s-treasury-sanctions-venezuelan-vice-president-over-drug-trade-allegations')],
 4547: [_s('Venezuela to quit Organization of American States', 'Al Jazeera', '2017-04-26', 'https://www.aljazeera.com/news/2017/4/26/venezuela-to-quit-organization-of-american-states')],
 4548: [_s('Treasury sanctions eight members of the Venezuelan Supreme Court (May 18, 2017)', 'Treasury/OFAC (official release)', '2017-05-18', 'https://home.treasury.gov/news/press-releases/sm0090')],
 4549: [_s('Treasury sanctions 13 current and former Venezuelan officials (Jul 26, 2017)', 'Treasury/OFAC (official release)', '2017-07-26', 'https://home.treasury.gov/news/press-releases/sm0132'),
        _s('Trump places sanctions on 13 Venezuelan officials', 'NPR (via KAXE)', '2017-07-26', 'https://www.kaxe.org/2017-07-26/trump-places-sanctions-on-13-venezuelan-officials')],
 4550: [_WGBH_MADURO, _CRS19],
 4551: [_WGBH_MADURO, _CRS19],
 4552: [_s('Trump says he is considering a military response to Venezuela', 'CBS News', '2017-08-11', 'https://www.cbsnews.com/pittsburgh/news/trump-considers-military-response-venezuela')],
 4553: [_AJ_MIL17],
 4554: [_s('Presidential Executive Order on Imposing Sanctions with Respect to the Situation in Venezuela', 'White House (Trump archive)', '2017-08-25', 'https://trumpwhitehouse.archives.gov/the-press-office/2017/08/25/presidential-executive-order-imposing-sanctions-respect-situation'), _CRS19],
 4555: [_s('Venezuelan military holds exercises after Trump threat', 'Reuters (via Global News)', '2017-08-26', 'https://globalnews.ca/news/3698777/veneuelan-military-trump')],
 4556: [_s('US remarks on Maduro ouster angers Caracas', 'Reuters (via Gulf Times)', '2018-02-02', 'https://www.gulf-times.com/story/580314/us-remarks-on-maduro-ouster-angers-caracas')],
 4557: [_s('US remarks on Maduro ouster angers Caracas', 'Reuters (via Gulf Times)', '2018-02-02', 'https://www.gulf-times.com/story/580314/us-remarks-on-maduro-ouster-angers-caracas')],
 4558: [_s('Trump bans use of Venezuelan cryptocurrency', 'PBS NewsHour (AP)', '2018-03-19', 'https://www.pbs.org/newshour/nation/trump-bans-use-of-venezuelan-cryptocurrency')],
 4559: [_s('Recent actions, May 21, 2018: new Executive Order "Prohibiting Certain Additional Transactions with Respect to Venezuela"', 'Treasury/OFAC (official release)', '2018-05-21', 'https://ofac.treasury.gov/recent-actions/20180521'), _AJ_ROBINSON],
 4560: [_AJ_ROBINSON],
 4561: [_s('Venezuelan President Maduro survives apparent assassination attempt', 'CNN', '2018-08-04', 'https://amp.cnn.com/cnn/2018/08/04/americas/venezuela-maduro')],
 4562: [_NPR_COUP18, _AJ_COUP18, _KNAU_COUP18],
 4563: [_KNAU_COUP18, _AJ_COUP18],
 4564: [_s('US sanctions Venezuela president\'s wife and inner circle', 'CNN', '2018-09-25', 'https://amp.cnn.com/cnn/2018/09/25/politics/us-venezuela-sanctions-maduro-wife')],
 4565: [_s('Trump orders sanctions on Venezuela gold to pressure Maduro', 'Bloomberg', '2018-11-01', 'https://www.bloomberg.com/news/articles/2018-11-01/trump-orders-sanctions-on-venezuela-gold-to-pressure-maduro'), _CRS19],
 4566: [_s('Russia scoffs at US criticism of bomber deployment to Venezuela', 'Al Jazeera', '2018-12-11', 'https://www.aljazeera.com/news/2018/12/11/russia-scoffs-at-us-criticism-of-bomber-deployment-to-venezuela')],
 4567: [_PBS_MADURO19, _AJ_MADURO19],
 4568: [_PBS_MADURO19, _AJ_MADURO19],
}
VERDICT = {k: 'confirmed' for k in SOURCES}
# Rows where an allowed outlet or official page confirms the event but not every detail in the row (day set from the page address, the day of the week or
# the publication day; the date of a report, not of the act; a figure or detail from one source only).
#   4501: AP page is dated Aug 9 but says "Thursday", so Aug 10 is used.   4502: ousted Apr 11 per CRS; Carmona's takeover is Apr 12.
#   4509: Aug 8 is the day Al Jazeera published; CRS says "early August".   4523: US expulsion dated by CRS, which is the only dated source.
#   4526: Apr 17 is the opening day of the summit; the AP page is dated Apr 18.   4529: pact signed in Bogota, reported Oct 30.
#   4530: the troop move to the border is "the week before", with no day.   4539: day set from the page address (the page says Tuesday).
#   4545: AP says Shannon "would try to meet Maduro"; no meeting is confirmed.   4562: dated by the Times report, not the meetings.
#   4565: Bloomberg gives only "Thursday"; Nov 1 is from CRS.
PARTLY = {4501, 4502, 4509, 4523, 4526, 4529, 4530, 4539, 4545, 4562, 4565}

# Which option letter each US move belongs to (see header). A (hold) is not tagged.
US_OPTION = {
 4503: 'H', 4510: 'C', 4513: 'H', 4516: 'C', 4523: 'H', 4524: 'C', 4526: 'B', 4528: 'B', 4529: 'E', 4533: 'H',
 4534: 'C', 4536: 'H', 4539: 'H', 4541: 'H', 4542: 'C', 4543: 'C', 4545: 'B', 4546: 'C', 4548: 'C', 4549: 'C',
 4551: 'C', 4552: 'H', 4554: 'C', 4556: 'H', 4558: 'C', 4559: 'C', 4562: 'H', 4564: 'C', 4565: 'C', 4568: 'H',
}


def _cred(k):
    """My own estimate of the engine's credibility score (full-text allowed outlet or official release 0.80, CRS 0.60, two different
    outlets combine, 'Partly' x0.8). For spot checks only."""
    best = {}
    for s in SOURCES[k]:
        outlet = s['outlet'].split(' (')[0].strip()
        w = 0.60 if outlet.startswith(('CRS', 'Congress')) else 0.80
        best[outlet] = max(best.get(outlet, 0), w)
    p = 1.0
    for w in best.values():
        p *= (1 - w)
    c = min(0.99, 1 - p)
    if k in PARTLY:
        c *= 0.8
    return round(c, 2)


CRED_ESTIMATE = {e[0]: _cred(e[0]) for e in EVENTS}

_W = "words only in the source read; days 2-7 not searched further"

# Trigger Census rows for US moves of kinds B-H (window: 7 days for a reply).
# Category = what the move cost the other side; Status: R-strong / R-weak (a Venezuelan military mobilization within 7 days),
# N (nothing but words, a diplomatic step or an expulsion in the source read), Unclear, Unverified (see the header).
CENSUS = [
 (4503, "Political/Diplomatic", "N", "Statement blaming Chavez for the Apr 2002 ouster, Apr 12. Chavez returned to power on Apr 14 (#4504); CNN and the White House briefing report no Venezuelan military act in the window (" + _W + "). A statement, not an act: weak as a case."),
 (4510, "Economic/Blockade", "N", "'Failed demonstrably' drug designation, Sep 15, 2005. The White House statement and CRS report no Venezuelan act in the window (" + _W + ")."),
 (4513, "Political/Diplomatic", "N", "Expulsion of a Venezuelan embassy official, Feb 3, 2006, in answer to #4512. Chavez's rally speech on Feb 4 (#4514) was words and a call for more weapons; AJ reports no mobilization (" + _W + ")."),
 (4516, "Economic/Blockade", "N", "Ban on arms sales, May 15, 2006. Chavez dismissed it the same day and said Venezuela would not retaliate (Al Jazeera; #4517). Words only."),
 (4523, "Political/Diplomatic", "N", "Expulsion of Ambassador Alvarez, Sep 12, 2008, a day after Chavez expelled Duddy (#4522). No Venezuelan hostile act reported (" + _W + ")."),
 (4524, "Economic/Blockade", "N", "Kingpin Act designations, Sep 12, 2008. Treasury's release and CRS report no Venezuelan reply (" + _W + ")."),
 (4526, "Political/Diplomatic", "N", "Obama-Chavez handshake, Apr 17, 2009. Chavez said on Apr 19 he would restore his ambassador (#4527): a cooperative step, not a hostile act."),
 (4528, "Political/Diplomatic", "N", "Agreement to return ambassadors, Jun 25, 2009. No hostile reply in Al Jazeera or CRS (" + _W + ")."),
 (4529, "Military/Property", "Unclear", "US-Colombia bases pact, Oct 30, 2009. Chavez sent 15,000 troops to the Colombian border 'the week before' Nov 9 (no day given) and told his army to prepare for war on Nov 9 (#4530), day 10, outside the window. Whether a dated troop move fell inside the 7 days cannot be told from the page."),
 (4533, "Political/Diplomatic", "N", "Visa revoked for Ambassador Alvarez, Dec 29, 2010, a day after Chavez dared the US to expel him (#4532). NBC reports no hostile act in the window (" + _W + ")."),
 (4534, "Economic/Blockade", "N", "PDVSA sanctions over Iran, May 24, 2011. Venezuela said it may not be able to guarantee all oil shipments to the US (#4535, Bloomberg): words, not a cut-off."),
 (4536, "Political/Diplomatic", "Unverified", "Expulsion of the Venezuelan consul in Miami, Jan 8, 2012. Al Jazeera reports no Venezuelan response and the window was not searched."),
 (4539, "Political/Diplomatic", "Unverified", "US expulsion of three Venezuelan diplomats, Oct 2, 2013, in answer to #4538. Al Jazeera reports no Venezuelan response and the window was not searched."),
 (4541, "Political/Diplomatic", "N", "US expulsion of three Venezuelan diplomats, Feb 25, 2014, in answer to #4540. Foreign Minister Jaua called it retaliation, not reciprocity (Al Jazeera). Words only."),
 (4542, "Economic/Blockade", "Unverified", "Law requiring sanctions, Dec 18, 2014. The Public Law page has no Venezuelan response and the window was not searched."),
 (4543, "Economic/Blockade", "R-strong", "Executive order and national emergency, Mar 9, 2015 -> Venezuela begins 10 days of nationwide military exercises with about 100,000 troops on Mar 14, and Defense Minister Padrino calls the sanctions 'an imminent danger' (Al Jazeera, AFP via Defense News)."),
 (4545, "Political/Diplomatic", "N", "Shannon's Caracas visit, Jun 20, 2016. Maduro welcomed it; no hostile act reported (" + _W + ")."),
 (4546, "Economic/Blockade", "N", "El Aissami named a kingpin, Feb 13, 2017. The NPR article reports no Venezuelan response (" + _W + ")."),
 (4548, "Economic/Blockade", "Unverified", "Sanctions on eight Supreme Court justices, May 18, 2017. Only Treasury's release was read and the window was not searched."),
 (4549, "Economic/Blockade", "N", "Sanctions on 13 officials, Jul 26, 2017. NPR (Jul 31) says Maduro publicly honored each of the 13 and called the measures 'imperialist sanctions': words only."),
 (4551, "Economic/Blockade", "N", "Sanctions on Maduro, Jul 31, 2017. The NPR article reports no Venezuelan act in the window (" + _W + ")."),
 (4552, "Military/Property", "R-strong", "Trump's 'military option' remark, Aug 11, 2017 -> Maduro orders national military exercises for Aug 26-27 and tells supporters to prepare for an 'imperialist' invasion, Aug 14 (Al Jazeera). The remark is words, not an act."),
 (4554, "Economic/Blockade", "R-weak", "Executive order on financial markets, Aug 24, 2017 -> Venezuela holds nationwide exercises on Aug 26 (Reuters). They had been announced on Aug 14 (#4553), so the link to the order is timing only."),
 (4556, "Political/Diplomatic", "N", "Tillerson's coup remark, Feb 1, 2018. Defense Minister Padrino said the armed forces 'radically reject' it (Reuters): words only."),
 (4558, "Economic/Blockade", "N", "Petro ban, Mar 19, 2018. The AP article reports no Venezuelan response (" + _W + ")."),
 (4559, "Economic/Blockade", "N", "Debt executive order, May 21, 2018. Maduro expelled the top US diplomats the next day (#4560, an expulsion, which is counted as a counter-measure in the economic category) and the Foreign Ministry called the sanctions 'a crime against humanity'. No hostile act."),
 (4562, "Political/Diplomatic", "N", "Report of US meetings with Venezuelan officers, Sep 8, 2018. Foreign Minister Arreaza condemned it on Sep 9 (#4563): words only."),
 (4564, "Economic/Blockade", "N", "Sanctions on Maduro's wife and inner circle, Sep 25, 2018. The CNN article reports no Venezuelan response (" + _W + ")."),
 (4565, "Economic/Blockade", "Unverified", "Gold-sector executive order, Nov 1, 2018. The Venezuelan reaction was not read and the window was not searched."),
 (4568, "Political/Diplomatic", "Unverified", "US rejection of Maduro's new term, Jan 10, 2019. Venezuela's reaction was not read; the Jan 23 events (#4001, #4002) are 13 days later, outside the window."),
]

# Reply pairs (pair id, trigger, reply, category, reply caused casualties Y/N, note)
PAIRS = [
 (4500, 4502, 4503, "Political/Diplomatic", "N", "The Bush administration blames Chavez the same day he is removed and calls it a change of government (words)"),
 (4501, 4511, 4512, "Political/Diplomatic", "N", "Chavez expels the US naval attache the day Rumsfeld compares him to Hitler (timing only)"),
 (4502, 4512, 4513, "Political/Diplomatic", "N", "The US expels a Venezuelan embassy official the next day"),
 (4503, 4522, 4523, "Political/Diplomatic", "N", "The US expels Venezuela's ambassador a day after Chavez expels the US ambassador"),
 (4504, 4532, 4533, "Political/Diplomatic", "N", "The US revokes the Venezuelan ambassador's visa a day after Chavez dares it to expel him"),
 (4505, 4534, 4535, "Economic/Blockade", "N", "Venezuela says it may not guarantee all oil shipments to the US the day PDVSA is sanctioned (words)"),
 (4506, 4538, 4539, "Political/Diplomatic", "N", "The US expels three Venezuelan diplomats two days after Maduro expels three US diplomats"),
 (4507, 4540, 4541, "Political/Diplomatic", "N", "The US expels three Venezuelan diplomats eight days after Maduro expels three US consular officials"),
 (4508, 4543, 4544, "Military/Property", "N", "Nationwide military exercises with about 100,000 troops five days after the national emergency order"),
 (4509, 4552, 4553, "Military/Property", "N", "Maduro orders national military exercises three days after Trump's 'military option' remark"),
 (4510, 4554, 4555, "Military/Property", "N", "Nationwide exercises two days after the financial-markets order (they were announced earlier, on Aug 14)"),
 (4511, 4556, 4557, "Political/Diplomatic", "N", "Defense Minister Padrino says the armed forces reject Tillerson's remarks the next day (words)"),
 (4512, 4559, 4560, "Political/Diplomatic", "N", "Maduro expels the top US diplomats a day after the debt executive order"),
 (4513, 4562, 4563, "Political/Diplomatic", "N", "Foreign Minister Arreaza condemns the reported coup meetings the next day (words)"),
]

# No continuous-fighting windows here: the log shows no pace of acts dense enough to need one before Jan 2019.
WINDOWS = []
START_ACTS = set()

# Phases (oldest first)
PHASES = [
 ("Chavez's first term", d(1999, 2, 2), d(2002, 4, 10), "Inauguration (#4500) and the Baghdad visit (#4501)"),
 ("Coup attempt, strike and recall", d(2002, 4, 11), d(2005, 2, 28), "Apr 2002 ouster and return (#4502-#4504), the oil strike (#4505), the 2004 recall vote (#4506)"),
 ("Bush years: oil threats, expulsions and arms ban", d(2005, 3, 1), d(2009, 1, 19), "Oil threats (#4507, #4515), the DEA and instructors (#4508-#4509), Feb 2006 expulsions (#4512-#4513), arms ban (#4516), Sep 2008 expulsions and Kingpin sanctions (#4522-#4524), Russian bombers and ships (#4521, #4525)"),
 ("Obama years: thaw, Colombia bases and new frictions", d(2009, 1, 20), d(2012, 12, 31), "Handshake and ambassadors (#4526-#4528), Colombia bases and war talk (#4529-#4530), the Palmer dispute (#4532-#4533), PDVSA sanctions (#4534), consul expelled (#4536)"),
 ("Maduro: expulsions and the first sanctions", d(2013, 1, 1), d(2016, 12, 31), "Expulsions (#4537-#4541), the 2014 sanctions law and the 2015 emergency order (#4542-#4543), the March 2015 drills (#4544), Shannon in Caracas (#4545)"),
 ("Trump: sanctions and the military option", d(2017, 1, 1), d(2019, 1, 22), "Sanctions on officials and Maduro (#4546-#4551), military option and drills (#4552-#4555), Tillerson (#4556), EOs (#4558-#4559), expulsions (#4560), drone incident (#4561), coup-meeting report (#4562), Nov 2018 gold order (#4565), Maduro's second term (#4567-#4568)"),
]

CHAIN_NAMES = {
 4502: "Apr 2002 ouster -> US statement blaming Chavez -> Chavez returns",
 4511: "Feb 2006 Rumsfeld remark -> naval attache expelled -> US expels a Venezuelan official",
 4522: "Sep 2008 Duddy expelled -> US expels Venezuela's ambassador",
 4529: "Oct 2009 US-Colombia bases -> Chavez tells army to prepare for war",
 4532: "Dec 2010 Palmer dispute -> US revokes Venezuela's ambassador's visa",
 4534: "May 2011 PDVSA sanctions -> Venezuela warns of oil shipments",
 4538: "Sep 2013 US diplomats expelled -> US expels three Venezuelan diplomats",
 4540: "Feb 2014 consular officials expelled -> US expels three Venezuelan diplomats",
 4543: "Mar 2015 emergency order -> Venezuelan military exercises",
 4550: "Jul 2017 Constituent Assembly vote -> sanctions on Maduro",
 4516: "May 2006 arms-sales ban -> Chavez dismisses it",
 4526: "Apr 2009 Obama-Chavez handshake -> Chavez to restore his envoy",
 4552: "Aug 2017 'military option' remark -> Maduro orders exercises",
 4554: "Aug 2017 financial-markets order -> exercises held",
 4556: "Feb 2018 Tillerson remark -> armed forces reject it",
 4559: "May 2018 debt order -> US diplomats expelled",
 4562: "Sep 2018 coup-meeting report -> Arreaza condemns it",
 4567: "Jan 2019 Maduro's second term -> US and OAS reject it",
}
