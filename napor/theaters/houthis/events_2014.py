"""NAPOR Houthis / Red Sea: the first years of the war, Sep 21, 2014 - Oct 8, 2016 (research file).

Same shape as events_early.py. Event IDs 1050-1099 and pair IDs 1050-1099 belong to this file.
events_early.py continues from Oct 9, 2016 (IDs 1001-1299) and events_late.py from Jan 1, 2025 (IDs 1301-1599).

Rules used here (docs/SOURCE_STANDARD.md):
- Only allowed outlets and official statements (CENTCOM/NAVCENT, Treasury, White House, UN count as official).
  Wire stories read through a syndicated copy are labelled "AP (via ...)". seen="full text" means the article was
  opened and read; seen="snippet" means only the headline and link from a search result were seen.
- Every event below has at least one linked source that was opened. Houthi media would be allowed only as a labelled
  claim; none was opened, and Houthi claims below are reported by AP, Al Jazeera or USNI and say "claimed".
- A US move has an option letter in US_OPTION (B talks, C sanctions/designations, D naval defense/escort,
  E interdict Iranian arms, F strike Houthi military sites, G strike risking personnel/leaders,
  H force posture). The embassy closure (#1055) is a diplomatic withdrawal, not a military posture move,
  so it has no option letter.
- The US did not fight the Houthis in this period. It backed the Saudi-led coalition (from Mar 25, 2015), so the
  Houthi acts logged here are sparse: the big ones (the Sanaa takeover, the palace, the Marib missile, the
  Swift attack). The daily fighting with Saudi and Yemeni forces is NOT logged, so "no Houthi attack logged
  within 7 days" for a 2015-2016 case means "none in this log", not "none happened".
- The Saudi-led air campaign itself is not logged event by event. The one strike logged (#1078, the Oct 8, 2016
  funeral hall) is a context row for the US reaction (#1077) and is not scored (see KIND_OVERRIDE in config.py).
- UN-run talks and ceasefires between Yemeni parties (#1051, #1066, #1069, #1070, #1072) and the UN resolution
  (#1060) are logged as context. They are not US-Houthi talks, so config.py keeps them out of the political-corner talks count.
- Dates follow the announcement date when a move was announced later (as in events_early.py).
- Looked at and left out: the Sep 2015 Arabian Sea arms interdiction (a Combined Maritime Forces member seized
  it, USS Forrest Sherman only assisted, the crew said it was bound for Somalia: AP, VOA); the Feb 27 and Mar 20, 2016
  Australian and French seizures (not US moves).
"""
import datetime as dt


def d(y, m, day):
    return dt.date(y, m, day)


def _s(headline, outlet, published, url, seen="snippet"):
    return {'headline': headline, 'outlet': outlet, 'published': published, 'seen': seen, 'url': url}


# Columns: ID, Date, Actor, Action Type, Target, Detail, Trigger ID, Severity, Confidence, Source
EVENTS = [
(1050, d(2014,9,21), "Houthis", "Offensive operation (capture of Sanaa)", "Sanaa, Yemen's capital (government buildings)", "Houthi fighters take much of Sanaa after days of fighting: the defense ministry, army headquarters, parliament, central bank and state radio are seized with little resistance; on Sep 22 they raid the house of General Ali Mohsen al-Ahmar. The same night they sign a UN-brokered deal with the government (#1051)", None, "At least 200 killed in the fighting since Sep 16 (Yemen health ministry, via Al Jazeera)", "Medium", "see audit"),
(1051, d(2014,9,21), "UN (Yemeni parties)", "Diplomatic agreement (UN-brokered power-sharing deal)", "Houthis and Yemen's government", "President Hadi and the main parties, including the Houthis, sign the Peace and National Partnership deal: an immediate ceasefire and a more inclusive government. The prime minister resigns. The Houthis did not sign the annex asking them to leave Sanaa and other areas within 45 days", None, "n/a", "Medium", "see audit"),
(1052, d(2014,11,10), "US", "Sanctions (Treasury designations)", "Ali Abdullah Saleh and Houthi commanders Abdullah Yahya al-Hakim and Abd al-Khaliq al-Huthi", "Treasury freezes the US assets of the three under E.O. 13611, three days after the UN Security Council sanctioned the same men, for threatening Yemen's stability", None, "n/a", "Medium", "see audit"),
(1053, d(2015,1,20), "Houthis", "Offensive operation (presidential palace seized)", "Presidential palace, Sanaa", "Houthi fighters take the presidential palace after a brief clash, a day after both sides announced ceasefires. President Hadi is surrounded in his home and resigns two days later. The UN Security Council condemns the violence", None, "Nine killed and about 90 wounded in the fighting the day before (Al Jazeera)", "Medium", "see audit"),
(1054, d(2015,2,6), "Houthis", "Declaration (Houthi government announced)", "Yemen's government", "The Houthis dissolve parliament and install a five-member presidential council. The UN says it does not recognise the move; the US says it is deeply concerned and that the move does not meet the standards set by the UN envoy", None, "n/a", "Medium", "see audit"),
(1055, d(2015,2,11), "US", "Posture (embassy closed, staff withdrawn)", "US embassy, Sanaa", "The State Department suspends its Sanaa mission indefinitely, citing the deteriorating security situation; the Marines guarding it are expected to leave (AP). US counterterrorism operations against AQAP are to continue. A diplomatic withdrawal, not a military posture move, so no option letter", None, "n/a", "Medium", "see audit"),
(1056, d(2015,2,11), "Houthis", "Confiscation (US embassy vehicles)", "US embassy vehicles, Sanaa airport", "Houthi fighters take three vehicles the US embassy staff had used at Sanaa airport, shortly after the staff left (AFP). Logged as a reaction to the embassy closure; the link is timing only", 1055, "Three vehicles taken; no injuries reported", "Medium", "see audit"),
(1057, d(2015,3,21), "US", "Posture (withdrawal of last US forces from Al Anad air base)", "Al Anad air base, southern Yemen", "US troops and special forces, about 100 according to reports, leave Al Anad, the last US military presence in Yemen, as Yemeni forces lose ground; the State Department says it removed its remaining personnel. The air base is also near a town just taken by AQAP, so the move is not only about the Houthis", None, "n/a", "Medium", "see audit"),
(1058, d(2015,3,25), "US", "Posture (support for Saudi-led campaign; Joint Planning Cell)", "Saudi-led coalition against the Houthis", "The White House says President Obama authorized logistical and intelligence support for the Gulf-led operation and that the US is setting up a Joint Planning Cell with Saudi Arabia (about a dozen US personnel at the start). US forces take no direct military action", None, "n/a", "Medium", "see audit"),
(1059, d(2015,3,26), "Saudi-led coalition", "Coalition air campaign begins", "Houthi forces in Yemen", "Saudi Arabia and about ten allies begin bombing Houthi targets as the Houthis close in on Aden and President Hadi is reported to have fled. The air campaign itself is not logged strike by strike (see the file note)", None, "n/a", "Medium", "see audit"),
(1060, d(2015,4,14), "UN Security Council (US voted yes)", "Diplomatic resolution (UN arms embargo)", "Houthi leader Abdul Malik al-Houthi, Ahmed Ali Saleh and three others", "Resolution 2216 passes 14-0, Russia abstaining: arms embargo on five named men, asset freeze and travel ban on al-Houthi and Ahmed Ali Saleh, a demand that the Houthis leave Sanaa and other seized areas, and a call for countries to inspect cargo bound for Yemen", None, "n/a", "Medium", "see audit"),
(1061, d(2015,4,14), "US", "Sanctions (Treasury designations)", "Houthi leader Abdul Malik al-Houthi and Ahmed Ali Saleh", "Treasury designates the two under E.O. 13611, the same day as the UN resolution (#1060). The coalition war was already under way", None, "n/a", "Medium", "see audit"),
(1062, d(2015,4,20), "US", "Posture (carrier and cruiser move toward Yemen)", "Arabian Sea, off Yemen", "USS Theodore Roosevelt and USS Normandy leave the Persian Gulf for the Arabian Sea to join other US warships near Yemen. The Pentagon says the Iranian convoy (#1063) is 'one of the factors but not the reason' and that the mission is to keep shipping lanes open", None, "n/a", "Medium", "see audit"),
(1063, d(2015,4,23), "Iran", "Convoy movement (Iranian cargo ships)", "Gulf of Aden", "Nine Iranian cargo ships, joined by Iranian warships, are tracked by the US Navy; press reports link them to arms for the Houthis, but the Pentagon says it does not know what they carry. Iran's Fars agency CLAIMS the warships came to protect the cargo ships. The carrier is about 200 nautical miles away", None, "n/a", "Medium", "see audit"),
(1064, d(2015,4,24), "Iran", "Convoy turns back (Iranian cargo ships)", "Arabian Sea, off Oman", "The Iranian convoy reverses course toward Iran. The Pentagon calls it 'a de-escalation' but says it does not know Iran's future intentions", 1063, "n/a", "Medium", "see audit"),
(1065, d(2015,4,25), "US", "Posture (carrier leaves Yemen area)", "Arabian Sea / Persian Gulf", "USS Theodore Roosevelt and USS Normandy head back toward the Gulf; seven other US warships stay in the Gulf of Aden area (AFP). The carrier never reached the Gulf of Aden", 1064, "n/a", "Medium", "see audit"),
(1066, d(2015,6,15), "UN", "Diplomatic talks (UN, Geneva)", "Yemeni government and Houthis", "UN-sponsored talks open in Geneva with Ban Ki-moon present; the Houthi delegation is delayed a day at Djibouti airport. The US is not mentioned in the report", None, "n/a", "Medium", "see audit"),
(1067, d(2015,9,4), "Houthis (per UAE)", "Strike (Tochka missile)", "Ammunition depot near UAE troops, Marib", "A missile hits a weapons depot in Marib province. The UAE blames the Houthis and Houthi media reportedly confirm a Soviet-era Tochka was fired (anonymous officials, AP). Deadliest day for the UAE military; Bahrain also reports five soldiers killed", None, "45 UAE and 5 Bahraini soldiers killed", "Medium", "see audit"),
(1068, d(2016,4,4), "US", "Seizure (weapons shipment)", "Iranian arms bound for the Houthis (Arabian Sea)", "USS Sirocco seizes 1,500 AK-47s, 200 RPG launchers and 21 heavy machine guns from a stateless dhow, with USS Gravely sent to help (seized Mar 28, announced Apr 4; logged on the announcement date). The Navy says the arms came from Iran and were likely bound for the Houthis. Third allied seizure since late February", None, "n/a", "Medium", "see audit"),
(1069, d(2016,4,10), "UN (Yemeni parties)", "Diplomatic ceasefire (UN-announced truce)", "Yemen: government, coalition and Houthis", "A truce starts at midnight (Apr 10-11). The government and coalition say they will respect it; the Houthis say they are committed but reserve the right to respond. Heavy fighting continues in Taiz and Bayda. The US is not a party", None, "n/a", "Medium", "see audit"),
(1070, d(2016,4,21), "UN", "Diplomatic talks (UN, Kuwait)", "Yemeni government and Houthis", "UN-sponsored talks are due to open in Kuwait on Apr 21 after a delay; the Houthi delegation flew out of Sanaa after UN assurances about the truce. The report is from the day before, so the opening itself was not read", None, "n/a", "Medium", "see audit"),
(1071, d(2016,7,30), "Houthis", "Declaration (Houthi-Saleh governing council)", "Yemen's government", "The Houthis and former president Saleh's party form a 10-member council to run the country; the Hadi government quits the Kuwait talks in response, and the UN calls the move unilateral", None, "n/a", "Medium", "see audit"),
(1072, d(2016,8,6), "UN", "Diplomatic talks (UN, Kuwait) suspended", "Yemeni government and Houthis", "After more than 90 days the Kuwait talks end without a deal: the Houthis and Saleh's party reject a UN plan the government accepted, and the UN envoy announces a month-long suspension while saying the talks are not over", 1071, "n/a", "Medium", "see audit"),
(1073, d(2016,8,20), "US", "Posture (planning cell cut)", "Joint Combined Planning Cell, Saudi Arabia", "Reuters reports that the US pulled staff out of Saudi Arabia in June: fewer than five US service members remain full-time in the planning cell, down from a peak of about 45. Air refuelling (about two sorties a day) and limited intelligence sharing continue. Officials say the cut was not because of criticism over civilian deaths. Logged on the report date", None, "n/a", "Medium", "see audit"),
(1074, d(2016,8,25), "US", "Diplomatic proposal (US peace plan)", "Houthis, Saleh's party, Yemeni government", "Secretary of State Kerry announces a plan from Jeddah, agreed with Gulf states and the UN: a quick national unity government, withdrawal of forces from Sanaa and other areas, and handover of heavy weapons including ballistic missiles to a third party. The UN envoy is to start consultations. Al Jazeera reports no Houthi or government reaction at that time", None, "n/a", "Medium", "see audit"),
(1075, d(2016,10,1), "Houthis (claimed)", "Strike (anti-ship missile)", "HSV-2 Swift, UAE-chartered vessel (near Mokha, Bab el-Mandeb)", "The Houthis CLAIM they destroyed an Emirati warship; the UAE says only that a boat under its command was in an 'incident' and that no one died. Video shows the former US Navy ship burning. USNI: the weapon may have been a C-802 anti-ship missile; a US defense official says the attack is tied to the Yemen conflict, not to shipping in general", None, "Ship burning, not sunk; UAE reports no casualties; damage details unconfirmed", "Medium", "see audit"),
(1076, d(2016,10,4), "US", "Posture (warships move to Bab el-Mandeb)", "Bab el-Mandeb strait", "Officials confirm USS Nitze, USS Mason and the staging ship USS Ponce are near the strait; one official says they moved because of the attack on the Swift. The US says it is committed to the free flow of commerce. Logged on the day officials confirmed it", 1075, "n/a", "Medium", "see audit"),
(1077, d(2016,10,8), "US", "Diplomatic statement (security-support review)", "Saudi-led coalition, Yemen's parties", "NSC spokesman Ned Price says US security cooperation with Saudi Arabia is 'not a blank check', announces an immediate review of its already reduced support for the coalition, and asks all sides, the Houthis included, to commit to a halt in hostilities on the April 10 terms. A statement, not talks", 1078, "n/a", "Medium", "see audit"),
(1078, d(2016,10,8), "Saudi-led coalition (blamed by Yemen health ministry)", "Airstrike (funeral hall, Sanaa)", "Funeral hall, Sanaa", "An airstrike hits a funeral hall where thousands had gathered. The Yemen health ministry blames the coalition; AP could not confirm who carried it out. Victims include Houthi and Saleh-aligned officials. The UN humanitarian coordinator calls for an investigation. Context row for #1077; not scored", None, "More than 140 killed and over 525 wounded (UN humanitarian coordinator, via AP)", "Medium", "see audit"),
]

# ---------------------------------------------------------------------------------------------
_AJ_SANAA = _s('Houthis tighten grip on Yemen capital', 'Al Jazeera', '2014-09-22', 'https://www.aljazeera.com/amp/news/2014/9/22/houthis-tighten-grip-on-yemen-capital', 'full text')
_AJ_DEAL = _s('Yemen rivals sign peace agreement', 'Al Jazeera', '2014-09-22', 'https://www.aljazeera.com/amp/news/2014/9/22/yemen-rivals-sign-peace-agreement', 'full text')
_NBC_DEAL = _s('Yemeni Parties, Rebels Sign Deal to End Fighting, Form Government', 'NBC News', '2014-09-21', 'https://www.nbcnews.com/news/world/yemeni-parties-rebels-sign-deal-end-fighting-form-government-n208426', 'full text')
_TREAS_APR15 = _s('Treasury Designates Houthi leader and Ahmed Ali Saleh (E.O. 13611)', 'Treasury/OFAC (official release)', '2015-04-14', 'https://home.treasury.gov/news/press-releases/jl10021', 'full text')
_AFP_EMBASSY = _s('Shiite militiamen seize US diplomatic cars in Yemen', 'AFP (via Ahram Online)', '2015-02-11', 'https://english.ahram.org.eg/News/122812.aspx', 'full text')
_AFP_US_SUPPORT = _s('US to give "logistical, intelligence" support to Saudi-led coalition in Yemen', 'AFP (via Ahram Online)', '2015-03-26', 'https://english.ahram.org.eg/News/126126.aspx', 'full text')
_DN_ROOSEVELT_OUT = _s('Officials: US aircraft carrier heading away from Yemen', 'AFP (via Defense News)', '2015-04-25', 'https://www.defensenews.com/home/2015/04/25/officials-us-aircraft-carrier-heading-away-from-yemen/', 'full text')
_CBS_CONVOY = _s('U.S.: Iranian turnaround makes confrontation less likely', 'AP (via CBS News)', '2015-04-24', 'https://www.cbsnews.com/amp/news/us-iranian-turnaround-makes-confrontation-less-likely', 'full text')
_USNI_SWIFT = _s('Officials: 3 U.S. Warships Off Yemen Following Attack on UAE Ship', 'USNI News', '2016-10-04', 'https://news.usni.org/2016/10/04/official-3-u-s-warships-off-yemen-following-attack-uae-ship', 'full text')
_TWZ_SHIPS = _s('Report: Navy Sending Ships To Mandeb Strait Following HSV-2 Swift Attack', 'The War Zone', '2016-10-04', 'https://www.twz.com/5422/report-navy-sending-ships-to-mandeb-strait-following-hsv-2-swift-attack', 'full text')
_SPOK_FUNERAL = _s('UN, Yemeni officials indicate more than 140 killed in airstrike on funeral', 'AP (via The Spokesman-Review)', '2016-10-08', 'https://www.spokesman.com/stories/2016/oct/08/un-yemeni-officials-indicate-more-than-140-killed-/', 'full text')

SOURCES = {
 1050: [_AJ_SANAA, _NBC_DEAL],
 1051: [_AJ_DEAL, _NBC_DEAL],
 1052: [_s('Treasury Sanctions Ali Abdullah Saleh and Houthi commanders (E.O. 13611)', 'Treasury/OFAC (official release)', '2014-11-10', 'https://home.treasury.gov/news/press-releases/jl2693', 'full text'),
        _s('US blacklists Yemen ex-president Saleh, Huthi commanders', 'AFP (via Ahram Online)', '2014-11-10', 'https://english.ahram.org.eg/News/115209.aspx', 'full text')],
 1053: [_s('Houthis take over Yemen presidential palace', 'Al Jazeera', '2015-01-21', 'https://www.aljazeera.com/amp/news/2015/1/21/houthis-take-over-yemen-presidential-palace', 'full text')],
 1054: [_s("Yemen's Houthis form own government in Sanaa", 'Al Jazeera', '2015-02-06', 'https://www.aljazeera.com/news/2015/2/6/yemens-houthis-form-own-government-in-sanaa', 'full text')],
 1055: [_s('Officials: US closing embassy in Yemen amid continued unrest', 'AP (via Military Times)', '2015-02-10', 'https://www.militarytimes.com/news/your-military/2015/02/10/officials-u-s-closing-embassy-in-yemen-amid-continued-unrest/', 'full text'),
        _AFP_EMBASSY,
        _s('U.S. Said to Close Embassy in Yemen Over Security Concerns', 'Bloomberg', '2015-02-10', 'https://www.bloomberg.com/news/articles/2015-02-10/u-s-said-to-close-embassy-in-yemen-over-security-concerns', 'snippet')],
 1056: [_AFP_EMBASSY],
 1057: [_s('Reports: US forces evacuating Yemen air base', 'Defense News', '2015-03-21', 'https://www.defensenews.com/home/2015/03/21/reports-us-forces-evacuating-yemen-air-base/', 'full text'),
        _s('US withdraws remaining personnel from Yemen', 'AP (via PBS NewsHour)', '2015-03-22', 'https://www.pbs.org/newshour/politics/us-withdraws-remaining-personnel-yemen', 'full text')],
 1058: [_AFP_US_SUPPORT,
        _s('US weighs tanker, radar planes for Saudi Yemen op', 'AFP (via Defense News)', '2015-03-26', 'https://www.defensenews.com/global/mideast-africa/2015/03/26/us-weighs-tanker-radar-planes-for-saudi-yemen-op/', 'full text'),
        _s('U.S. Confirms It Is Supporting Saudi Military Operations In Yemen', 'NPR (via GBH)', '2015-03-26', 'https://www.wgbh.org/news/2015-03-26/u-s-confirms-it-is-supporting-saudi-military-operations-in-yemen', 'full text')],
 1059: [_s('U.S. Confirms It Is Supporting Saudi Military Operations In Yemen', 'NPR (via GBH)', '2015-03-26', 'https://www.wgbh.org/news/2015-03-26/u-s-confirms-it-is-supporting-saudi-military-operations-in-yemen', 'full text'),
        _s('US weighs tanker, radar planes for Saudi Yemen op', 'AFP (via Defense News)', '2015-03-26', 'https://www.defensenews.com/global/mideast-africa/2015/03/26/us-weighs-tanker-radar-planes-for-saudi-yemen-op/', 'full text')],
 1060: [_s('UN approves arms embargo against Yemen\'s Houthis', 'AP (via Ahram Online)', '2015-04-14', 'https://english.ahram.org.eg/News/127661.aspx', 'full text')],
 1061: [_TREAS_APR15,
        _s('US places sanctions on leader, backer of Yemen\'s Houthis', 'AFP (via Ahram Online)', '2015-04-14', 'https://english.ahram.org.eg/News/127689.aspx', 'full text')],
 1062: [_s('Pentagon: Iranian Convoy \'One of the Factors\' in Moving U.S. Carrier Roosevelt Closer to Yemen', 'USNI News', '2015-04-21', 'https://news.usni.org/2015/04/21/pentagon-iranian-convoy-one-of-the-factors-in-moving-u-s-carrier-roosevelt-closer-to-yemen', 'full text'),
        _s('U.S. warship reportedly sent to Yemen', 'PBS NewsHour', '2015-04-20', 'https://www.pbs.org/newshour/nation/u-s-warship-reportedly-sent-to-yemen', 'snippet')],
 1063: [_s('Iranian warships join cargo flotilla near Yemen; questions raised over its direction', 'Stars and Stripes', '2015-04-23', 'https://www.stripes.com/news/2015-04-23/iranian-warships-join-cargo-flotilla-near-yemen-questions-raised-over-its-direction-1812891.html1', 'full text'),
        _s('Pentagon: Iranian Convoy \'One of the Factors\' in Moving U.S. Carrier Roosevelt Closer to Yemen', 'USNI News', '2015-04-21', 'https://news.usni.org/2015/04/21/pentagon-iranian-convoy-one-of-the-factors-in-moving-u-s-carrier-roosevelt-closer-to-yemen', 'full text')],
 1064: [_CBS_CONVOY, _DN_ROOSEVELT_OUT],
 1065: [_DN_ROOSEVELT_OUT, _CBS_CONVOY],
 1066: [_s('Yemen peace talks open in Geneva without Houthis', 'Al Jazeera', '2015-06-16', 'https://www.aljazeera.com/amp/news/2015/6/16/yemen-peace-talks-open-in-geneva-without-houthis', 'full text')],
 1067: [_s('UAE says 45 of its troops killed in Yemen', 'AP (via Military Times)', '2015-09-04', 'https://www.militarytimes.com/news/your-military/2015/09/04/united-arab-emirates-says-45-of-its-troops-killed-in-yemen/', 'full text'),
        _s('Scores of Gulf troops killed in Yemen conflict', 'Al Jazeera', '2015-09-05', 'https://www.aljazeera.com/news/2015/9/5/scores-of-gulf-troops-killed-in-yemen-conflict', 'full text')],
 1068: [_s('U.S. Navy Seizes Suspected Iranian Arms Shipment Bound for Yemen', 'USNI News', '2016-04-04', 'https://news.usni.org/2016/04/04/u-s-navy-seizes-suspected-iranian-arms-shipment-bound-for-yemen', 'full text'),
        _s('Third Illicit Arms Shipment in Recent Weeks Seized in Arabian Sea', 'NAVCENT (official release)', '2016-04-04', 'https://www.cusnc.navy.mil/Media/News/Display/Article/713256/third-illicit-arms-shipment-in-recent-weeks-seized-in-arabian-sea/', 'full text'),
        _s('Navy: Over 1,000 Weapons From Iran Likely Bound for Yemen Seized', 'NBC News', '2016-04-04', 'https://www.nbcnews.com/news/us-news/navy-over-1-000-weapons-iran-likely-bound-yemen-seized-n550406', 'full text')],
 1069: [_s('Yemeni truce begins amid reports of clashes', 'Al Jazeera', '2016-04-11', 'https://www.aljazeera.com/amp/news/2016/4/11/yemeni-truce-begins-amid-reports-of-clashes', 'full text')],
 1070: [_s('Yemen peace talks set to begin in Kuwait after delay', 'Al Jazeera', '2016-04-20', 'https://www.aljazeera.com/amp/news/2016/4/20/yemen-peace-talks-set-to-begin-in-kuwait-after-delay', 'full text')],
 1071: [_s("Yemen: Hadi's government withdraws from UN talks", 'Al Jazeera', '2016-07-30', 'https://www.aljazeera.com/amp/news/2016/7/30/yemen-hadis-government-withdraws-from-un-talks', 'full text')],
 1072: [_s('Yemen peace talks in Kuwait end amid fighting', 'Al Jazeera', '2016-08-07', 'https://www.aljazeera.com/amp/news/2016/8/7/yemen-peace-talks-in-kuwait-end-amid-fighting', 'full text')],
 1073: [_s('Exclusive: U.S. withdraws staff from Saudi Arabia dedicated to Yemen planning', "Reuters (via Rep. Ted Lieu's website)", '2016-08-22', 'https://lieu.house.gov/media-center/in-the-news/exclusive-us-withdraws-staff-saudi-arabia-dedicated-yemen-planning', 'full text')],
 1074: [_s('US pushes for new Yemen peace initiative', 'Al Jazeera', '2016-08-25', 'https://www.aljazeera.com/amp/news/2016/8/25/us-pushes-for-new-yemen-peace-initiative', 'full text')],
 1075: [_s('Yemen: Houthis claim attack on UAE military vessel', 'Al Jazeera', '2016-10-02', 'https://www.aljazeera.com/amp/news/2016/10/2/yemen-houthis-claim-attack-on-uae-military-vessel', 'full text'),
        _s('HSV-2 Swift Destroyed Off Yemeni Coast By Anti-Ship Missile', 'The War Zone', '2016-10-02', 'https://twz.com/5404/hsv-2-swift-destroyed-off-yemeni-coast-by-anti-ship-missile', 'full text'),
        _USNI_SWIFT],
 1076: [_USNI_SWIFT, _TWZ_SHIPS],
 1077: [_s('Statement by NSC Spokesperson Ned Price on Yemen', 'White House (official statement)', '2016-10-08', 'https://obamawhitehouse.archives.gov/the-press-office/2016/10/08/statement-nsc-spokesperson-ned-price-yemen', 'full text'),
        _SPOK_FUNERAL],
 1078: [_SPOK_FUNERAL],
}
VERDICT = {k: 'confirmed' for k in SOURCES}
# Rows where an allowed outlet confirms the event but not every detail in the row.
#   1067: the Houthi role rests on UAE statements and anonymous Houthi officials (AP, Al Jazeera).
#   1070: the report is from the day before the talks opened.
#   1075: the Houthi claim and the weapon type are not confirmed by the UAE; the damage is not assessed.
PARTLY = {1067, 1070, 1075}

# Which option letter each US move belongs to (B talks, C sanctions/designations, D naval defense/escort,
# E interdict Iranian arms, F strike Houthi military sites, G strike risking personnel/leaders, H posture).
US_OPTION = {
 1052: 'C', 1057: 'H', 1058: 'H', 1061: 'C', 1062: 'H', 1065: 'H', 1068: 'E', 1073: 'H', 1074: 'B', 1076: 'H',
}

# My own estimate of the engine's credibility score (full-text allowed outlet 0.80, two outlets 0.96,
# claim-only 0.30; under 0.50 is not counted). For spot checks only.
CRED_ESTIMATE = {
 1050: 0.96, 1051: 0.96, 1052: 0.96, 1053: 0.80, 1054: 0.80, 1055: 0.99, 1056: 0.80, 1057: 0.96,
 1058: 0.96, 1059: 0.96, 1060: 0.80, 1061: 0.96, 1062: 0.93, 1063: 0.96, 1064: 0.96, 1065: 0.96,
 1066: 0.80, 1067: 0.77, 1068: 0.99, 1069: 0.80, 1070: 0.64, 1071: 0.80, 1072: 0.80, 1073: 0.80,
 1074: 0.80, 1075: 0.79, 1076: 0.96, 1077: 0.96, 1078: 0.80,
}

# Trigger Census rows for US moves of kinds C-G (window: ~5 days for a reply). "Reply" means a Houthi attack on US forces or shipping.
CENSUS = [
 (1052, "Economic/Blockade", "N", "Treasury designations of Saleh and two Houthi commanders, Nov 10, 2014. A web search found no Houthi attack on US forces or shipping on Nov 11-15, 2014; the coverage found is about Saleh's party leaving the cabinet."),
 (1061, "Economic/Blockade", "Unclear", "Treasury designations, Apr 14, 2015. The Saudi-led war had started 19 days earlier and the Houthis were fighting coalition and Yemeni forces every day, so a reply to this act cannot be separated. No Houthi attack on US forces or shipping was found for Apr 15-19."),
 (1068, "Economic/Blockade", "N", "Seizure of 1,500 AK-47s and other arms, announced Apr 4, 2016. A web search found no Houthi attack on US forces or shipping on Apr 5-9, 2016; the UN-announced truce began on Apr 10-11 (Al Jazeera)."),
]

# Reply pairs (pair id, trigger, reply, category, reply caused casualties Y/N, note)
PAIRS = [
 (1050, 1075, 1076, "Military/Property", "N", "US moves USS Nitze, USS Mason and USS Ponce to the Bab el-Mandeb three days after the Swift attack; an official said they moved because of it (USNI)"),
]

# Continuous-fighting windows (US strikes inside are context only) and the acts that started them.
# The US did not strike in this period, so there are none here.
WINDOWS = []
START_ACTS = set()

# Phases (oldest first)
PHASES = [
 ("Houthi takeover and US pullout", d(2014, 9, 21), d(2015, 3, 24), "#1050-#1051 Sanaa taken and the UN-brokered deal, #1052 the first Treasury designations, #1053-#1054 palace and Houthi government, #1055 embassy closed, #1057 last US forces leave"),
 ("Saudi-led war; US backs it from the side", d(2015, 3, 25), d(2016, 4, 10), "#1058-#1059 US support and the coalition campaign, #1060-#1061 UN embargo and Treasury designations, #1062-#1065 carrier and Iranian convoy, #1067 Marib missile, #1068 arms seizure"),
 ("Kuwait talks and the road to the Red Sea attacks", d(2016, 4, 11), d(2016, 10, 8), "Truce and Kuwait talks (#1069-#1072), US planning cell cut (#1073), Kerry plan (#1074), Swift attack and US ships (#1075-#1076), NSC review (#1077); events_early.py starts Oct 9"),
]

CHAIN_NAMES = {
 1055: "US embassy closes -> Houthis take US vehicles",
 1063: "Iranian convoy -> convoy turns back -> US carrier leaves",
 1071: "Houthi-Saleh council -> Kuwait talks suspended",
 1075: "Swift attack -> US warships to Bab el-Mandeb",
 1077: "Funeral hall airstrike -> NSC reviews US support",
}
