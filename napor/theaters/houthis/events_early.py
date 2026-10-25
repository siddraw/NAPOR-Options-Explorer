"""NAPOR Houthis / Red Sea: the US-Houthi record, Oct 2016 - Dec 31, 2024 (research file, W2).

Same shape as napor/prewar.py. Event IDs 1001-1299 and pair IDs 1001-1299 belong to this file.
W3 (events_late.py) continues from Jan 1, 2025 with IDs 1301-1599.

Rules used here (docs/SOURCE_STANDARD.md):
- Only allowed outlets and official statements (CENTCOM, Treasury, UN count as official). Wire stories
  read through a syndicated copy are labelled "AP (via ...)". seen="full text" means the article was
  read; seen="snippet" means only the headline was seen.
- Houthi media would be allowed only as a labelled claim, outlet "al-Masirah (Houthi claim)". No
  al-Masirah page was opened; Houthi claims below are reported by AP and say "Houthis CLAIM".
- A US move has an option letter in US_OPTION (B talks, C sanctions/designations, D naval defense/escort,
  E interdict Iranian arms, F strike Houthi military sites, G strike risking personnel/leaders,
  H force posture). No sourced H event was found for this era.
- Continuous-fighting rule: from the first US strikes (Jan 12, 2024) the Houthis attacked ships or
  US forces almost every week, so every US strike in the window has a "reply" by default. US strikes in
  the window are logged as context and are not counted in the census. W3 continues the window.
- Events 1005 and 1009 are also in the Iran log (prewar #264 and #265).
- Dates follow the announcement date when a seizure was announced days later (as in prewar).
"""
import datetime as dt


def d(y, m, day):
    return dt.date(y, m, day)


def _s(headline, outlet, published, url, seen="snippet"):
    return {'headline': headline, 'outlet': outlet, 'published': published, 'seen': seen, 'url': url}


# Columns: ID, Date, Actor, Action Type, Target, Detail, Trigger ID, Severity, Confidence, Source
EVENTS = [
(1001, d(2016,10,9), "Houthis (per US)", "Strike (anti-ship missiles)", "USS Mason (Red Sea)", "Two missiles, believed to be Chinese-made C-802s, are fired at the destroyer USS Mason near Bab el-Mandeb; the Mason fires defensive missiles (USNI dates this Oct 9; the Pentagon calls Oct 12 the 'second time in four days')", None, "No damage or injuries", "Medium", "see audit"),
(1002, d(2016,10,12), "Houthis (per US)", "Strike (anti-ship missiles)", "USS Mason (Red Sea)", "Second missile attack on the Mason in four days; the Pentagon says at least one missile came from Houthi-controlled territory near Al Hudaydah and the crew used countermeasures", None, "No damage or injuries", "Medium", "see audit"),
(1003, d(2016,10,13), "US", "Strike (Tomahawk, radar sites)", "Houthi radar sites, Yemen Red Sea coast", "USS Nitze fires Tomahawk missiles at three Houthi-held coastal radar sites; the Pentagon calls them limited self-defense strikes authorized by President Obama. First US shots against the Houthis in Yemen's war", 1002, "Three radar sites destroyed (initial US assessment); no casualty figures", "Medium", "see audit"),
(1004, d(2016,10,15), "Houthis (per US)", "Strike (coastal missiles)", "USS Mason (Red Sea)", "The Mason fires countermeasures at what officials first said were coastal-defense missiles from Yemen, the third reported incident in about a week; US officials later said the first reports were being reassessed", 1003, "No damage or injuries", "Medium", "see audit"),
(1005, d(2020,2,13), "US", "Seizure (weapons shipment)", "Iranian arms bound for the Houthis (Arabian Sea)", "USS Normandy's boarding team seizes 150 Iranian-made Dehlavieh anti-tank missiles and other arms from a dhow (seized Feb 9, announced Feb 13; logged on the announcement date). Also Iran log #264", None, "n/a", "Medium", "see audit"),
(1006, d(2021,1,10), "US", "Sanction (terrorist designation)", "Houthis (Ansarallah)", "Secretary of State Pompeo announces the Houthis will be designated a Foreign Terrorist Organization, plus three leaders; effective Jan 19, 2021", None, "n/a", "Medium", "see audit"),
(1007, d(2021,2,4), "US", "Diplomatic talks (policy change)", "Yemen war", "President Biden ends US support for the Saudi-led offensive, calls for a ceasefire and names Timothy Lenderking special envoy for Yemen", None, "n/a", "Medium", "see audit"),
(1008, d(2021,2,12), "US", "Sanction (designation revoked)", "Houthis (Ansarallah)", "Secretary of State Blinken announces the Houthi terrorist designations will be revoked, effective Feb 16; three leaders stay under sanctions", None, "n/a", "Medium", "see audit"),
(1009, d(2023,1,10), "US", "Seizure (weapons shipment)", "Iranian arms bound for Yemen (Gulf of Oman)", "US Navy intercepts a fishing vessel carrying 2,116 AK-47s on a route from Iran to Yemen (seized Jan 6, announced Jan 10; logged on the announcement date). Also Iran log #265", None, "n/a", "Medium", "see audit"),
(1011, d(2023,11,8), "Houthis (per US defense official)", "Shootdown (US drone)", "US MQ-9 Reaper, off Yemen", "A US defense official confirms Houthi forces shot down an MQ-9 Reaper in international airspace off Yemen", None, "Drone destroyed; no casualties", "Medium", "see audit"),
(1012, d(2023,11,19), "Houthis", "Seizure (ship)", "Galaxy Leader (Red Sea)", "Houthis seize the vehicle carrier Galaxy Leader with 25 crew, citing its Israel link; two US defense officials confirm the Houthis seized it", None, "25 crew held; no deaths reported", "Medium", "see audit"),
(1013, d(2023,11,26), "Houthis (per US)", "Strike (ballistic missiles)", "USS Mason and M/V Central Park (Gulf of Aden)", "While the Mason responds to the hijacking of the Central Park, at least one ballistic missile from Houthi-held Yemen lands about 10 nautical miles away", None, "No damage or injuries", "Medium", "see audit"),
(1014, d(2023,12,3), "Houthis", "Strike (missiles and drones, shipping)", "Unity Explorer, Number 9, Sophie II; USS Carney (Red Sea)", "CENTCOM reports Houthi missiles hit three commercial ships and USS Carney shoots down three drones; CENTCOM says Iran enables the attacks", None, "Minor to moderate damage to ships; no casualties", "Medium", "see audit"),
(1015, d(2023,12,7), "US", "Sanction response (Houthi finance)", "Houthi financing network", "Treasury sanctions 13 people and companies moving money from Iranian commodity sales to the Houthis (Sa'id al-Jamal network)", None, "n/a", "Medium", "see audit"),
(1016, d(2023,12,18), "US", "Force posture (naval defense coalition)", "Red Sea / Gulf of Aden", "Defense Secretary Austin announces Operation Prosperity Guardian, a multinational effort under Combined Task Force 153 to protect shipping from Houthi attacks", None, "n/a", "Medium", "see audit"),
(1017, d(2023,12,30), "Houthis", "Strike (anti-ship ballistic missile)", "Maersk Hangzhou (Red Sea)", "Houthi missile hits the Maersk Hangzhou; USS Gravely shoots down two more missiles. CENTCOM counts it the 23rd attack on merchant ships in the Red Sea", None, "Ship hit; no US damage", "Medium", "see audit"),
(1018, d(2023,12,31), "US", "Strike (helicopters sink boats)", "Houthi small boats, Red Sea", "Helicopters from USS Gravely and USS Eisenhower sink three of four Houthi boats that fired on the Maersk Hangzhou and tried to board; CENTCOM says the crews were killed. Houthis CLAIM ten of their navy members died", 1017, "Ten Houthi fighters killed; no US damage", "Medium", "see audit"),
(1019, d(2024,1,9), "Houthis", "Strike (drones and missiles)", "Red Sea shipping lanes (US, UK warships respond)", "Houthis fire 18 drones, 2 anti-ship cruise missiles and 1 anti-ship ballistic missile toward the southern Red Sea; US and UK ships and jets shoot all 21 down. CENTCOM counts it the 26th launch toward Red Sea shipping", None, "No injuries or damage", "Medium", "see audit"),
(1020, d(2024,1,10), "US (with Japan) at the UN Security Council", "Diplomatic proposal (UN resolution)", "Houthis", "Security Council adopts Resolution 2722, drafted by the US and Japan: demands the Houthis stop attacks on ships and free the Galaxy Leader (11 yes, 4 abstentions)", 1019, "n/a", "Medium", "see audit"),
(1021, d(2024,1,12), "US (with UK)", "Strike (radar, air defense, launch sites)", "Houthi military sites, Yemen", "First US-UK strikes on Houthi radar, air-defense and missile and drone sites; Biden calls them a defensive action after 27 attacks on shipping. A later PBS report puts it at more than 60 targets at 28 locations", 1019, "Houthi casualty figures not from allowed outlets", "Medium", "see audit"),
(1022, d(2024,1,14), "Houthis (per CENTCOM)", "Strike (anti-ship cruise missile)", "USS Laboon (Red Sea)", "An anti-ship cruise missile is fired from Houthi-held Yemen toward USS Laboon and shot down by a US fighter. First US-acknowledged Houthi targeting after the Jan 12 strikes", 1021, "No injuries or damage", "Medium", "see audit"),
(1023, d(2024,1,15), "Houthis", "Strike (anti-ship ballistic missile)", "Gibraltar Eagle (US-owned container ship)", "CENTCOM says a Houthi missile hits the US-owned and operated Gibraltar Eagle in the southern Red Sea", 1021, "No significant damage; no injuries", "Medium", "see audit"),
(1024, d(2024,1,16), "US", "Seizure (weapons shipment)", "Iranian missile parts bound for the Houthis (Arabian Sea)", "CENTCOM announces Navy SEALs seized Iranian-made missile parts from a dhow on Jan 11 (logged on the announcement date); two SEALs were lost at sea. First such seizure since Houthi shipping attacks began", None, "Two US SEALs lost at sea; 14 crew detained", "Medium", "see audit"),
(1025, d(2024,1,17), "US", "Sanction (terrorist designation)", "Houthis (Ansarallah)", "US re-designates the Houthis as a Specially Designated Global Terrorist group; takes effect after 30 days", None, "n/a", "Medium", "see audit"),
(1026, d(2024,1,17), "Houthis", "Strike (drone, shipping)", "Genco Picardy (US-owned bulk carrier, Gulf of Aden)", "A one-way attack drone from Houthi-held Yemen hits the US-owned Genco Picardy", None, "Some damage; no injuries", "Medium", "see audit"),
(1027, d(2024,1,17), "US", "Strike (missiles on launch rails)", "Houthi missiles, Yemen", "CENTCOM says US forces struck 14 Houthi missiles on launch rails that posed an imminent threat to ships (announced Jan 17; local time may be Jan 18)", 1026, "n/a", "Medium", "see audit"),
(1028, d(2024,1,22), "US (with UK)", "Strike (missile, air defense, radar, storage sites)", "Houthi military sites, Yemen", "Second round of joint US-UK strikes: eight targets including missile launchers, air defenses, radars and buried storage; Tomahawks and Navy jets used", None, "n/a", "Medium", "see audit"),
(1029, d(2024,1,26), "Houthis", "Strike (anti-ship ballistic missile)", "Marlin Luanda (tanker, Gulf of Aden)", "A Houthi missile hits the tanker Marlin Luanda; USS Carney and other coalition ships help", 1028, "Damage; no injuries reported", "Medium", "see audit"),
(1030, d(2024,2,3), "US (with UK)", "Strike (36 targets)", "Houthi military sites, Yemen", "CENTCOM says US and UK forces hit 36 targets at 13 locations: underground storage, command sites, missile systems, drone sites, radars and helicopters", None, "n/a", "Medium", "see audit"),
(1031, d(2024,2,20), "Houthis (Houthis CLAIM; US did not confirm)", "Shootdown (US drone)", "US MQ-9 Reaper, near Yemen", "AP reports an apparent Houthi shootdown of a US MQ-9; CENTCOM and the Air Force did not answer AP's questions. Houthis CLAIM it", None, "Not confirmed by the US", "Medium", "see audit"),
(1032, d(2024,3,2), "Houthis", "Strike (shipping, sinking)", "Rubymar (Red Sea)", "The Rubymar, hit by a Houthi anti-ship ballistic missile on Feb 18, sinks; CENTCOM warns of fertilizer and fuel spill risk", None, "Ship lost; no crew deaths reported", "Medium", "see audit"),
(1033, d(2024,3,6), "Houthis", "Strike (anti-ship ballistic missile, shipping)", "True Confidence (Gulf of Aden)", "CENTCOM says a Houthi missile hit the bulk carrier True Confidence, the first fatal Houthi strike on shipping", None, "3 crew killed; at least 4 injured", "Medium", "see audit"),
(1034, d(2024,3,26), "US", "Sanction response (Houthi, IRGC-QF finance)", "Sa'id al-Jamal network", "Treasury sanctions six entities, one person and two tankers in the sixth round on Sa'id al-Jamal's network since Dec 2023", None, "n/a", "Medium", "see audit"),
(1035, d(2024,6,12), "Houthis", "Strike (drone boats, shipping)", "Tutor (bulk carrier, Red Sea)", "Houthi drone boats hit the Greek-owned Tutor (a photo caption dates the hit to Jun 12); it was reported sunk on Jun 19, the second ship the Houthis have sunk", None, "1 crew member killed (White House); ship lost", "Medium", "see audit"),
(1036, d(2024,8,15), "US", "Sanction response (Houthi, Hizballah oil trade)", "Sa'id al-Jamal network", "Treasury sanctions companies, people and vessels moving Iranian oil and LPG for the Houthi financier's network", None, "n/a", "Medium", "see audit"),
(1037, d(2024,8,23), "Houthis", "Strike (tanker)", "Sounion (Greek-flagged tanker, Red Sea)", "After repeated Houthi attacks the tanker Sounion, with about 1 million barrels of crude, is on fire; a French destroyer rescues the 29 aboard. The State Department says the Houthis seem set on sinking it", None, "Fires; crew of 29 rescued, no deaths reported", "Medium", "see audit"),
(1038, d(2024,9,10), "Houthis (per US military)", "Shootdown (US drone)", "US MQ-9 Reaper, Yemen", "The first of two MQ-9 Reapers the US later confirmed lost to Houthi fire in under a week", None, "Drone destroyed", "Medium", "see audit"),
(1039, d(2024,9,16), "Houthis (per US military)", "Shootdown (US drone)", "US MQ-9 Reaper, Yemen", "The second MQ-9 lost within a week; the Pentagon confirms both on Sep 18 and calls the Houthi claim of 10 Reapers 'not accurate'", None, "Drone destroyed", "Medium", "see audit"),
(1040, d(2024,9,30), "Houthis (Houthis CLAIM; US did not confirm)", "Shootdown (US drone)", "US MQ-9 Reaper, Saada province", "Houthis CLAIM they shot down another MQ-9 and show video; the US military did not acknowledge any loss to AP", None, "Not confirmed by the US", "Medium", "see audit"),
(1041, d(2024,10,2), "US", "Sanction response (Houthi arms procurement)", "Houthi networks in Iran and China", "Treasury sanctions one person, three companies, one entity and two vessels tied to Houthi weapons procurement and smuggling", None, "n/a", "Medium", "see audit"),
(1042, d(2024,10,17), "US", "Strike (B-2 bombers, buried weapons sites)", "Houthi underground weapons storage, Yemen", "Austin says B-2 bombers hit five hardened underground weapons storage sites in Houthi-held Yemen; CENTCOM believes no civilians were killed", None, "No damage assessment given", "Medium", "see audit"),
(1043, d(2024,10,17), "US", "Sanction response (Houthi oil shipping)", "Sa'id al-Jamal network", "Treasury sanctions 18 companies, people and vessels shipping Iranian oil for the Houthi financier", None, "n/a", "Medium", "see audit"),
(1044, d(2024,12,19), "US", "Sanction response (Houthi arms and finance)", "Houthi procurement and finance", "Treasury sanctions about a dozen people and entities, including the head of the Houthi-aligned Central Bank of Yemen branch in Sana'a, plus five crypto wallets", None, "n/a", "Medium", "see audit"),
(1045, d(2024,12,21), "US", "Strike (missile storage, command site, Sanaa)", "Houthi sites, Sanaa", "CENTCOM says US warplanes hit a missile storage facility and a command-and-control site in Sanaa on Saturday night and early Sunday (Dec 21-22). During the same hours a US cruiser mistakenly shot down a US F/A-18; both pilots survived. Houthis CLAIM they shot it down", None, "Both F/A-18 pilots recovered alive; no Houthi casualty figures", "Medium", "see audit"),
(1047, d(2024,1,9), "US (with UK)", "Air defense (drones and missiles shot down)", "Houthi drones and missiles, Red Sea", "USS Laboon, Gravely and Mason, Eisenhower jets and HMS Diamond shoot down all 21 Houthi drones and missiles", 1019, "No injuries or damage", "Medium", "see audit"),
]

# ---------------------------------------------------------------------------------------------
_USNI16 = _s('Pentagon Pledges to Respond in "Appropriate Manner" After New Yemen Missile Attack on USS Mason', 'USNI News', '2016-10-12', 'https://news.usni.org/2016/10/12/pentagon-respond-appropriate-manner-new-missile-attack-uss-mason-yemen', 'full text')
_DOD16 = _s('Statement by Pentagon Press Secretary Peter Cook on USS Mason', 'DoD (Pentagon statement, via CENTCOM)', '2016-10-13', 'https://www.centcom.mil/MEDIA/PUBLIC-RELEASES/Article/972273/statement-by-pentagon-press-secretary-peter-cook-on-uss-mason/', 'full text')
_USNI_UNITY = _s('Destroyer USS Carney Downs 3 Drones in Red Sea; Commercial Ships Attacked', 'USNI News', '2023-12-03', 'https://news.usni.org/2023/12/03/carney-shoots-down-two-drones-in-red-sea', 'full text')
_USNI_HELO = _s('U.S. Navy Helo Crews Kill Houthi Assault Boat Teams After Red Sea Attack', 'USNI News', '2023-12-31', 'https://news.usni.org/2023/12/31/u-s-navy-helo-crews-kill-houthi-assault-boat-teams-after-red-sea-attack', 'full text')
_USNI_JAN9 = _s('US Destroyers, Ike Aircraft Shoot Down Houthi-Launched Missiles, Drones Over Red Sea', 'USNI News', '2024-01-10', 'https://news.usni.org/2024/01/10/us-destroyers-ike-aircraft-shoot-down-houthi-launched-missiles-drones-over-red-sea', 'full text')
_ABC_MQ9 = _s('US military acknowledges Yemen\'s Houthi rebels shot down 2 MQ-9 Reaper drones', 'AP (via ABC News)', '2024-09-18', 'https://abcnews.go.com/Business/wireStory/us-military-acknowledges-yemens-houthi-rebels-shot-2-113796212', 'full text')

SOURCES = {
 1001: [_USNI16, _DOD16],
 1002: [_USNI16, _DOD16],
 1003: [_s('Updated: USS Nitze Destroys 3 Houthi Controlled Radar Sites in Retaliatory Strike', 'USNI News', '2016-10-13', 'https://news.usni.org/2016/10/13/video-uss-nitze-destroys-3-houthi-controlled-radar-sites-retaliatory-strike', 'full text'),
        _s('Officials say US missiles destroy radar sites on Yemen coast', 'AP (via ABC30 Fresno)', '2016-10-13', 'https://abc30.com/yemen-airstrike-coast/1552839', 'full text')],
 1004: [_s('Missiles fired at ship off Yemen', 'AP (via PBS NewsHour)', '2016-10-16', 'https://www.pbs.org/newshour/world/missiles-fired-ship-yemen', 'full text'),
        _s('CNO Richardson: USS Mason "Appears to Have Come Under Attack"', 'USNI News', '2016-10-15', 'https://news.usni.org/2016/10/15/cno-richardson-uss-mason-attacked-cruise-missiles-off-yemen', 'full text'),
        _s('USS Mason Fires Missiles at Possible Missile Attack', 'ABC News (via 6abc)', '2016-10-17', 'https://6abc.com/post/uss-mason-fires-missiles-at-possible-missile-attack/1557046/', 'full text')],
 1005: [_s('VIDEO: USS Normandy Seizes Cache Of Iranian-Made Weapons in Arabian Sea', 'USNI News', '2020-02-13', 'https://news.usni.org/2020/02/13/video-uss-normandy-seizes-cache-of-iranian-made-weapons-in-arabian-sea', 'full text')],
 1006: [_s("Pompeo to designate Yemen's Houthi rebels as terrorist group", 'AP (via News4JAX)', '2021-01-11', 'https://www.news4jax.com/news/politics/2021/01/11/pompeo-to-designate-yemens-houthi-rebels-as-terrorist-group/', 'full text'),
        _s("Biden administration to lift blacklisting of Yemen's Houthis", 'Al Jazeera', '2021-02-12', 'https://www.aljazeera.com/news/2021/2/12/biden-administration-to-lift-blacklisting-of-yemens-houthis', 'full text')],
 1007: [_s('Biden ending US support for Saudi-led offensive in Yemen', 'AP (via NewsChannel 9)', '2021-02-04', 'https://newschannel9.com/news/nation-world/biden-to-end-us-support-for-saudi-led-offensive-in-yemen', 'full text')],
 1008: [_s("Biden administration to lift blacklisting of Yemen's Houthis", 'Al Jazeera', '2021-02-12', 'https://www.aljazeera.com/news/2021/2/12/biden-administration-to-lift-blacklisting-of-yemens-houthis', 'full text')],
 1009: [_s('U.S. Navy Intercepts More Than 2,000 Assault Rifles Shipped from Iran', 'NAVCENT (official release)', '2023-01-10', 'https://www.cusnc.navy.mil/Media/News/Display/Article/3263172/us-navy-intercepts-more-than-2000-assault-rifles-shipped-from-iran/', 'full text'),
        _s('U.S. Navy seizes more than 2,000 AK-47s likely bound for Iranian-backed rebels in Yemen', 'NBC News', '2023-01', 'https://www.nbcnews.com/news/world/us-navy-seizes-ak-47-assault-rifles-iran-houthis-yemen-rcna65027', 'full text')],
 1011: [_s('US Reaper drone shot down near Yemen by Iranian-backed Houthi militants, defense official says', 'ABC News (via ABC7 New York)', '2023-11-08', 'https://abc7ny.com/houthis-yemen-us-drone-reaper/14028878/', 'full text')],
 1012: [_s("Yemen's Houthi rebels hijack an Israeli-linked ship in the Red Sea and take 25 crew members hostage", 'AP (via WLOS)', '2023-11-19', 'https://wlos.com/news/nation-world/yemens-houthi-rebels-hijack-an-israeli-linked-ship-in-the-red-sea-and-take-25-crew-members-hostage', 'full text')],
 1013: [_s('U.S., Coalition Reacts to Distress Call', 'CENTCOM (official release)', '2023-11-26', 'https://www.centcom.mil/MEDIA/PUBLIC-RELEASES/Article/3600004/us-coalition-reacts-to-distress-call/', 'full text')],
 1014: [_USNI_UNITY],
 1015: [_s('Treasury Targets Network Financing Houthi Regional Aggression', 'Treasury/OFAC (official release)', '2023-12-07', 'https://home.treasury.gov/news/press-releases/jy1961', 'full text')],
 1016: [_s("'Operation Prosperity Guardian' Set to Protect Ships in the Red Sea, Carrier IKE in Gulf of Aden", 'USNI News', '2023-12-18', 'https://news.usni.org/?p=107728', 'full text'),
        _s('Austin announces US-led security operation focusing on Red Sea, Gulf of Aden after Houthi attacks on commercial shipping', 'CNN (via KTVZ)', '2023-12-18', 'https://ktvz.com/politics/cnn-us-politics/2023/12/18/austin-announces-us-led-security-operation-focusing-on-red-sea-gulf-of-aden-after-houthi-attacks-on-commercial-shipping/', 'full text')],
 1017: [_USNI_HELO],
 1018: [_USNI_HELO],
 1019: [_USNI_JAN9],
 1020: [_s('Security Council adopts Resolution 2722 (2024) on Red Sea attacks', 'UN (official press release)', '2024-01-10', 'https://press.un.org/en/2024/sc15561.doc.htm', 'full text')],
 1021: [_s('Biden, White House defends strikes on Houthis amid mixed reaction', 'ABC News (via Good Morning America)', '2024-01-12', 'https://www.goodmorningamerica.com/news/story/biden-white-house-defends-strikes-houthis-amid-mixed-106322306', 'full text'),
        _s('Watch live: Pentagon holds briefing after U.S., U.K. launch new strike against Houthis in Yemen', 'PBS NewsHour', '2024-01-23', 'https://www.pbs.org/newshour/politics/watch-live-pentagon-holds-briefing-after-u-s-u-k-launch-new-strike-against-houthis-in-yemen', 'full text'),
        _s('What to Know in Washington: US, Allies Launch Houthi Airstrikes', 'Bloomberg Government', '2024-01-12', 'https://news.bgov.com/bloomberg-government-news/what-to-know-in-washington-us-allies-launch-houthi-airstrikes')],
 1022: [_s("Yemen's Houthi rebels fire missile at US warship in Red Sea in first attack after American-led strikes", 'AP (via NBC Washington)', '2024-01-14', 'https://www.nbcwashington.com/news/national-international/yemens-houthi-rebels-fire-missile-at-us-warship-in-red-sea-in-first-attack-after-american-led-strikes/3516123/?amp=1', 'full text')],
 1023: [_s('Houthis Strike Commercial Vessel in Southern Red Sea', 'CENTCOM (official release)', '2024-01-15', 'https://www.centcom.mil/MEDIA/PRESS-RELEASES/Press-Release-View/Article/3645588/houthis-strike-commercial-vessel-in-southern-red-sea/', 'full text')],
 1024: [_s('Two Missing Navy SEALs Helped Interdict Ship Transporting Weapons to Houthis', 'USNI News', '2024-01-16', 'https://news.usni.org/2024/01/16/two-missing-navy-seals-helped-interdict-ship-transporting-weapons-to-houthis', 'full text')],
 1025: [_s("US designates Yemen's Houthis as 'global terrorists'", 'Al Jazeera', '2024-01-17', 'https://www.aljazeera.com/amp/news/2024/1/17/us-redesignates-yemens-houthis-a-global-terrorist-group', 'full text')],
 1026: [_s('Houthis Attack U.S.-Owned and Operated Bulk Carrier', 'CENTCOM (official release)', '2024-01-17', 'https://www.centcom.mil/MEDIA/PRESS-RELEASES/Press-Release-View/Article/3648157/houthis-attack-us-owned-and-operated-bulk-carrier/', 'full text')],
 1027: [_s('U.S. Forces Strike Missile Sites in Yemen Following Houthi Attack on U.S. Commercial Ship', 'USNI News', '2024-01-17', 'https://news.usni.org/2024/01/17/u-s-forces-strike-missile-sites-in-yemen-following-houthi-attack-on-u-s-commercial-ship', 'full text')],
 1028: [_s('U.S. Forces, Allies Conduct Joint Strikes in Yemen', 'CENTCOM (official release)', '2024-01-23', 'https://www.centcom.mil/MEDIA/PUBLIC-RELEASES/Article/3652569/us-forces-allies-conduct-joint-strikes-in-yemen/', 'full text'),
        _s('UPDATED: U.S., U.K. Launch Major Strike Mission on Houthi Missile, Drone Infrastructure', 'USNI News', '2024-01-22', 'https://news.usni.org/?p=108429', 'full text'),
        _s('Watch live: Pentagon holds briefing after U.S., U.K. launch new strike against Houthis in Yemen', 'PBS NewsHour', '2024-01-23', 'https://www.pbs.org/newshour/politics/watch-live-pentagon-holds-briefing-after-u-s-u-k-launch-new-strike-against-houthis-in-yemen', 'full text')],
 1029: [_s('Houthis Strike M/V Marlin Luanda Operating in the Gulf of Aden', 'CENTCOM (official release)', '2024-01-26', 'https://www.centcom.mil/MEDIA/PUBLIC-RELEASES/Article/3658422/houthis-strike-mv-marlin-luanda-operating-in-the-gulf-of-aden/', 'full text')],
 1030: [_s('U.S. Forces, Allies Conduct Joint Strikes in Yemen', 'CENTCOM (official release)', '2024-02-04', 'https://www.centcom.mil/MEDIA/PUBLIC-RELEASES/Article/3665878/us-forces-allies-conduct-joint-strikes-in-yemen/', 'full text')],
 1031: [_s('Houthis shoot down US drone flying near Yemen', 'AP (via KOMO)', '2024-02-20', 'https://komonews.com/news/nation-world/houthis-shoot-down-us-drone-flying-near-yemen-report-war-weapons-mq-9-missile-airstrikes-debris-video-footage', 'full text')],
 1032: [_s('Cargo ship sinks in Red Sea nearly 2 weeks after being hit by Yemen\'s Houthi rebels', 'AP (via NPR)', '2024-03-02', 'https://npr.org/2024/03/02/1235521730/red-sea-cargo-ship-sinks-houthis-rubymar', 'full text')],
 1033: [_s("Houthi missile attack kills 3 crew members in rebels' first fatal assault on shipping", 'AP (via Michigan Public / NPR)', '2024-03-06', 'https://www.michiganpublic.org/2024-03-06/houthi-missile-attack-kills-3-crew-members-in-rebels-first-fatal-assault-on-shipping', 'full text')],
 1034: [_s('Treasury Targets Qods Force, Houthi, and Hizballah Finance and Trade Facilitators', 'Treasury/OFAC (official release)', '2024-03-26', 'https://home.treasury.gov/news/press-releases/jy2209', 'full text')],
 1035: [_s("Ship attacked by Yemen's Houthi rebels in fatal assault sinks in Red Sea, in second such sinking", 'AP (via ClickOnDetroit)', '2024-06-19', 'https://www.clickondetroit.com/news/world/2024/06/19/ship-attacked-by-yemens-houthi-rebels-in-fatal-assault-sinks-in-red-sea-in-second-such-sinking/', 'full text')],
 1036: [_s('Treasury Adds Further Sanctions Targeting Houthi and Hizballah Trade Networks', 'Treasury/OFAC (official release)', '2024-08-15', 'https://home.treasury.gov/news/press-releases/jy2538', 'full text')],
 1037: [_s('Greek-flagged tanker is burning after Houthi attacks but no sign of oil spill', 'AP (via KSAT)', '2024-08-26', 'https://www.ksat.com/news/world/2024/08/26/greek-flagged-tanker-is-burning-after-houthi-attacks-but-no-sign-of-oil-spill/', 'full text'),
        _s('Greek-flagged tanker in Red Sea still ablaze three days after Houthi attack', 'Times of Israel', '2024-08-26', 'https://www.timesofisrael.com/greek-flagged-tanker-in-red-sea-still-ablaze-three-days-after-houthi-attack/', 'full text')],
 1038: [_ABC_MQ9],
 1039: [_ABC_MQ9],
 1040: [_s("Yemen's Houthi rebels claim shooting down another US-made drone", 'AP (via ABC News); reports a Houthi claim', '2024-09-30', 'https://abcnews.go.com/International/wireStory/yemens-houthi-rebels-claim-shooting-us-made-drone-114342857', 'full text')],
 1041: [_s('Treasury Sanctions Houthi Weapons Smuggling and Procurement Networks', 'Treasury/OFAC (official release)', '2024-10-02', 'https://home.treasury.gov/news/press-releases/jy2627', 'full text')],
 1042: [_s("US long-range B-2 stealth bombers target underground bunkers of Yemen's Houthi rebels", 'AP (via News4JAX)', '2024-10-17', 'https://www.news4jax.com/news/world/2024/10/17/us-long-range-b-2-stealth-bombers-target-underground-bunkers-of-yemens-houthi-rebels/', 'full text')],
 1043: [_s('Treasury Sanctions Network for Shipping Oil on Behalf of Iran-Backed Houthi Financier', 'Treasury/OFAC (official release)', '2024-10-17', 'https://home.treasury.gov/news/press-releases/jy2652', 'full text')],
 1044: [_s('Treasury Maintains Pressure on Houthi Procurement and Financing Schemes', 'Treasury/OFAC (official release)', '2024-12-19', 'https://home.treasury.gov/news/press-releases/jy2757', 'full text')],
 1045: [_s('2 U.S. Navy pilots shot down over Red Sea in apparent friendly fire incident, CENTCOM says', 'AP (via PBS NewsHour)', '2024-12-22', 'https://www.pbs.org/newshour/world/2-u-s-navy-pilots-shot-down-over-red-sea-in-apparent-friendly-fire-incident-centcom-says', 'full text')],
 1047: [_USNI_JAN9],
}
VERDICT = {k: 'confirmed' for k in SOURCES}
# Houthi claims the US did not confirm (AP only reports what the Houthis say).
VERDICT[1031] = 'not_confirmed'
VERDICT[1040] = 'not_confirmed'
# Rows where an allowed outlet confirms the event but not every detail in the row.
PARTLY = {1001, 1027, 1035, 1037, 1045}

# Which option letter each US move belongs to (B talks, C sanctions/designations, D naval defense/escort,
# E interdict Iranian arms, F strike Houthi military sites, G strike risking personnel/leaders, H posture).
US_OPTION = {
 1003: 'F', 1005: 'E', 1006: 'C', 1007: 'B', 1008: 'C', 1009: 'E', 1015: 'C', 1016: 'D',
 1018: 'G', 1020: 'B', 1021: 'F', 1024: 'E', 1025: 'C', 1027: 'F', 1028: 'F', 1030: 'F',
 1034: 'C', 1036: 'C', 1041: 'C', 1042: 'F', 1043: 'C', 1044: 'C', 1045: 'F', 1047: 'D',
}

# My own estimate of the engine's credibility score (full-text allowed outlet 0.80, two outlets 0.96,
# claim-only 0.30; under 0.50 is not counted). For the organizer's spot check only.
CRED_ESTIMATE = {
 1001: 0.96, 1002: 0.96, 1003: 0.96, 1004: 0.96, 1005: 0.80, 1006: 0.96, 1007: 0.80, 1008: 0.80,
 1009: 0.96, 1011: 0.80, 1012: 0.80, 1013: 0.80, 1014: 0.80, 1015: 0.80, 1016: 0.96, 1017: 0.80,
 1018: 0.80, 1019: 0.80, 1020: 0.80, 1021: 0.96, 1022: 0.80, 1023: 0.80, 1024: 0.80, 1025: 0.80,
 1026: 0.80, 1027: 0.80, 1028: 0.96, 1029: 0.80, 1030: 0.80, 1031: 0.30, 1032: 0.80, 1033: 0.80,
 1034: 0.80, 1035: 0.80, 1036: 0.80, 1037: 0.96, 1038: 0.80, 1039: 0.80, 1040: 0.30, 1041: 0.80,
 1042: 0.80, 1043: 0.80, 1044: 0.80, 1045: 0.80, 1047: 0.80,
}

# Trigger Census rows for US moves of kinds C-H (window: ~5 days for a reply).
# Category = what the move cost the other side; Status as in data.py, plus "R-proxy" (not used here).
# US strikes inside the Jan 12 - Dec 31, 2024 window (1027, 1028, 1030, 1042, 1045) are context only.
CENSUS = [
 (1003, "Military/Property", "R-weak", "Tomahawk strikes on three radar sites, Oct 13, 2016 -> a third reported missile incident at USS Mason on Oct 15 (AP, USNI). US officials later said the first reports of that incident were being reassessed, so the link is plausible, not firm."),
 (1005, "Economic/Blockade", "N", "Seizure of Iranian-made missiles bound for the Houthis, announced Feb 13, 2020. A web search found no Houthi attack on US forces or shipping on Feb 14-18, 2020."),
 (1006, "Economic/Blockade", "N", "Terrorist designation announced Jan 10, 2021 (effective Jan 19). A web search found no Houthi attack on US forces or shipping on Jan 11-15, 2021; Al Jazeera (Feb 8, 2021) reports Houthi attacks on Saudi Arabia, none on US forces or ships."),
 (1008, "Economic/Blockade", "N", "Designation revoked Feb 12, 2021. Coverage read (Al Jazeera, Feb 8, 2021) shows Houthi attacks on Saudi Arabia only; no attack on US forces or shipping found."),
 (1009, "Economic/Blockade", "N", "Seizure of 2,116 rifles from Iran, announced Jan 10, 2023. A web search found no Houthi attack on US forces or shipping on Jan 11-15, 2023."),
 (1015, "Economic/Blockade", "Unclear", "Treasury network sanctions, Dec 7, 2023. Houthi attacks on shipping were already frequent (CENTCOM Dec 3), and no source was read for Dec 8-12, so a reply cannot be separated."),
 (1016, "Military/Property", "Unclear", "Operation Prosperity Guardian announced Dec 18, 2023. Houthi attacks on shipping were already frequent; no source was read for Dec 19-23, so a reply cannot be separated."),
 (1018, "Personnel/Casualty", "Unclear", "Helicopters sink three Houthi boats, Dec 31, 2023; Houthis CLAIM ten died. No Houthi attack on US forces or shipping was read for Jan 1-5, 2024; the next one sourced here is the Jan 9 barrage (9 days later)."),
 (1021, "Military/Property", "R-weak", "First US-UK strikes, Jan 12, 2024 (opens the window) -> Houthi missile at USS Laboon Jan 14 (AP) and a missile hit on the US-owned Gibraltar Eagle Jan 15 (CENTCOM). Houthis vowed revenge; link plausible."),
 (1024, "Economic/Blockade", "Unclear", "Seizure of Iranian missile parts announced Jan 16, 2024, inside the continuous-fighting window; Houthi attacks on ships followed (1026 on Jan 17) but cannot be tied to the seizure."),
 (1025, "Economic/Blockade", "Unclear", "Terrorist re-designation, Jan 17, 2024, inside the continuous-fighting window; Houthi attacks the same week (1026, 1029) cannot be tied to it."),
 (1034, "Economic/Blockade", "Unclear", "Treasury sanctions, Mar 26, 2024, inside the continuous-fighting window; a reply cannot be separated from routine attacks."),
 (1036, "Economic/Blockade", "Unclear", "Treasury sanctions, Aug 15, 2024, inside the continuous-fighting window; a reply cannot be separated from routine attacks."),
 (1041, "Economic/Blockade", "Unclear", "Treasury sanctions, Oct 2, 2024, inside the continuous-fighting window; a reply cannot be separated from routine attacks."),
 (1043, "Economic/Blockade", "Unclear", "Treasury sanctions, Oct 17, 2024, inside the continuous-fighting window; a reply cannot be separated from routine attacks."),
 (1044, "Economic/Blockade", "Unclear", "Treasury sanctions, Dec 19, 2024, inside the continuous-fighting window; a reply cannot be separated from routine attacks."),
 (1047, "Military/Property", "Unclear", "US and UK ships and jets shoot down 21 Houthi drones and missiles, Jan 9, 2024. A defensive act; Houthi attacks continued, but no reply to this act alone can be separated."),
]

# Reply pairs (pair id, trigger, reply, category, reply caused casualties Y/N, note)
PAIRS = [
 (1001, 1002, 1003, "Military/Property", "N", "US fires Tomahawks at three Houthi radar sites the day after the second missile attack on USS Mason"),
 (1002, 1003, 1004, "Military/Property", "N", "A third missile incident at USS Mason two days after the US strikes (later reassessed by US officials)"),
 (1003, 1017, 1018, "Personnel/Casualty", "Y", "US helicopters sink three Houthi boats the day after the Maersk Hangzhou missile hit; ten Houthi fighters died"),
 (1004, 1019, 1021, "Military/Property", "N", "First US-UK strikes three days after the Houthi barrage that US and UK ships shot down"),
 (1005, 1021, 1022, "Military/Property", "N", "Missile fired at USS Laboon two days after the first strikes; shot down"),
 (1006, 1021, 1023, "Military/Property", "N", "Missile hits the US-owned Gibraltar Eagle three days after the first strikes; no injuries"),
 (1007, 1026, 1027, "Military/Property", "N", "US strikes 14 Houthi missiles on launch rails right after a drone hits the US-owned Genco Picardy"),
 (1008, 1028, 1029, "Military/Property", "N", "Missile hits the tanker Marlin Luanda four days after the second round of strikes; Houthi attacks were near-constant, so the link is weak"),
]

# Continuous-fighting windows (US strikes inside are context only) and the acts that started them.
# W3 continues this window to its real end (Jan 19, 2025 pause, if confirmed).
WINDOWS = [(d(2024, 1, 12), d(2024, 12, 31))]
START_ACTS = {1021}

# Phases (oldest first)
PHASES = [
 ("First missile attacks", d(2016, 10, 9), d(2016, 10, 15), "#1001-#1002 missiles at USS Mason; #1003 the first US strikes; #1004 a third incident"),
 ("Quiet years: designations and arms seizures", d(2016, 10, 16), d(2023, 10, 18), "Arms seizures (#1005, #1009), the terrorist designation and its reversal (#1006, #1008), Biden's Yemen policy change (#1007)"),
 ("Red Sea shipping attacks begin", d(2023, 10, 19), d(2024, 1, 11), "Galaxy Leader seized (#1012), missiles near US ships, Operation Prosperity Guardian (#1016), helicopters sink boats (#1018)"),
 ("US-UK strikes and the shipping war", d(2024, 1, 12), d(2024, 12, 31), "Strikes from #1021 on, ship sinkings (#1032, #1035), lost drones, sanctions rounds and the B-2 strike (#1042); W3 continues from Jan 2025"),
]

CHAIN_NAMES = {
 1002: "Mason attacks -> Tomahawk strikes -> third Mason incident",
 1017: "Maersk Hangzhou hit -> helicopters sink Houthi boats",
 1019: "Jan 9 barrage -> first US-UK strikes -> missiles at Laboon and Gibraltar Eagle",
 1026: "Genco Picardy hit -> US strikes on 14 missiles",
 1028: "Second strikes -> Marlin Luanda hit",
}
