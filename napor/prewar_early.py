"""NAPOR: the US-Iran record BEFORE May 2019 (Nov 4, 1979 embassy takeover - May 4, 2019).

Why: the 2019-2026 record gives only a handful of past cases for most options. Going back to the embassy takeover
adds the hostage crisis, the Tanker War, the 1990s embargo, the nuclear file and the 2015 deal.

Rules used here (same source standard as the rest of NAPOR: docs/SOURCE_STANDARD.md):
- Event IDs 300-376 (block 300-999). Pair IDs 300-305. The 2026 IDs (1-115) and the 2019-2026 IDs (201-265) never change.
- Every row has at least one linked https page from an allowed outlet or an official release, and every page was
  opened and read (seen="full text"), except where noted as "snippet" (only the search-result headline was seen, and
  another opened page confirms the facts). Washington Post archive pages rarely print the calendar date ("yesterday"),
  so the date comes from the page's own URL date or from a dated official release.
- Sanctions, talks and statements are US moves. UN and IAEA rows are logged as context: they are not US moves, so they
  are not counted as cases.
- Tanker War rule (same idea as the 2023-24 militia stretch): from the first US convoy (Jul 22, 1987) to the airliner
  shootdown (Jul 3, 1988) Iran and Iraq were hitting ships almost every week, so a US move almost always has a
  "reply" by default. US moves in that stretch are logged and linked, but not counted as cases.
- Iraq 2007: Iran-backed militias were attacking US troops almost daily, so two US sanctions moves (#340, #342) have
  no clean 5-day read and are left "Unclear".
- Covert acts (rescue attempt, arms deliveries), defensive and accidental acts are logged but not counted.
- An N row means no new Iranian attack on US forces, ships or citizens was found in the pages read for the trigger and
  its next five days. It is not a separate full search of those days.

Dropped (no page I could open, or no calendar date from an allowed source):
Khomeini's Sep 1980 terms (WaPo prints only "today"), UN Resolution 457 (Dec 1979), the Apr 1983 embassy bombing in Beirut
(Iran link not in the page), the 1984 terrorism designation, TWA 847 (1985), the July 1988 Iranian acceptance of
Resolution 598, Bush's 1989 inaugural offer, Khatami's Jan 1998 CNN interview (CNN pages blocked), Albright's Mar 2000
speech (page down), the 2002 Natanz disclosure, the 2003 Bam aid, the Jan 2007 Irbil raid (WaPo news page would not
open; only an opinion column), the Jan 2017 USS Mahan warning shots, Iran's Jan 2017 missile test (no dated page),
the 2012 SWIFT cut-off and the EU oil embargo, and the Sep 2018 Basra rockets (no dated page).
"""
import datetime as dt


def d(y, m, day):
    return dt.date(y, m, day)


def _s(headline, outlet, published, url, seen="full text"):
    return {'headline': headline, 'outlet': outlet, 'published': published, 'seen': seen, 'url': url}


_WP = "https://www.washingtonpost.com/archive/politics/"

# Columns: ID, Date, Actor, Action Type, Target, Detail, Trigger ID, Severity, Confidence, Source
EVENTS = [
# --- Hostage crisis, 1979-81 ---
(300, d(1979,11,4), "Iran (students with state backing)", "Raid (US embassy takeover)", "US embassy, Tehran", "Students seize the US embassy in Tehran and hold about 60 Americans, first demanding the Shah's return; Revolutionary Guards loyal to Khomeini keep the compound", None, "More than 50 Americans held for 444 days", "Medium", "see audit"),
(301, d(1979,11,12), "US", "Sanctions (ban on Iranian oil imports)", "Iran", "Carter halts all US purchases of Iranian oil, about 700,000 barrels a day or nearly 10 percent of US imports", 300, "n/a", "Medium", "see audit"),
(302, d(1979,11,14), "US", "Sanctions (freeze of Iranian government assets)", "Iran", "Carter signs an order freezing Iranian government assets in the US; transfers now need Treasury approval", 300, "n/a", "Medium", "see audit"),
(303, d(1980,4,7), "US", "Sanctions (export ban and break in relations)", "Iran", "Carter announces the US is breaking diplomatic relations with Iran and orders a ban on US exports to Iran", 300, "n/a", "Medium", "see audit"),
(304, d(1980,4,24), "US", "Operation (hostage rescue attempt, Eagle Claw)", "Iran", "A US mission to free the hostages is called off after helicopter failures in the desert", 300, "8 US servicemen killed", "Medium", "see audit"),
(305, d(1980,11,2), "Iran", "Diplomatic demand (parliament sets terms for release)", "US", "Iran's parliament sets conditions for freeing the hostages (a pledge not to interfere in Iran, unfreezing assets) and passes them to the US through Algeria", None, "n/a", "Medium", "see audit"),
(306, d(1981,1,19), "US and Iran (Algerian mediation)", "Diplomatic talks (Algiers Accords, hostage deal)", "Iran", "The US announces an agreement with Iran to free the 52 hostages, worked out through Algerian mediators", 305, "n/a", "Medium", "see audit"),
(307, d(1981,1,20), "Iran", "Release (52 hostages freed)", "US", "The 52 Americans leave Tehran on the morning Reagan is sworn in, after 444 days", 306, "n/a", "Medium", "see audit"),
# --- Beirut and Iran-Contra, 1983-86 ---
(308, d(1983,10,23), "Hezbollah (Iran-backed; a US court found Iran directed it)", "Strike (truck bombing, Marine barracks)", "US Marines, Beirut", "Truck bomb hits the US Marine barracks in Beirut; in 2003 a US judge ruled Hezbollah carried it out at Iran's direction", None, "241 US servicemen killed", "Medium", "see audit"),
(309, d(1985,11,25), "US and Israel (covert)", "Arms transfer (covert, Hawk missiles)", "Iran", "Eighteen Hawk anti-aircraft missiles are flown from Israel to Iran as part of the secret arms-for-hostages channel", None, "n/a", "Medium", "see audit"),
(310, d(1986,2,17), "US (covert, via Israel)", "Arms transfer (covert, TOW missiles)", "Iran", "The first 500 TOW anti-tank missiles are delivered to Iran via Israel; a second 500 follow on Feb 27", None, "n/a", "Medium", "see audit"),
(311, d(1986,5,25), "US (covert)", "Diplomatic mission (secret trip to Tehran)", "Iran", "Former national security adviser McFarlane flies to Tehran with Hawk spare parts; the mission fails", None, "n/a", "Medium", "see audit"),
(312, d(1986,11,13), "US", "Diplomatic statement (Reagan address on arms to Iran)", "Iran", "After the secret channel is exposed, Reagan tells the nation the US sent arms to Iran for 'access and influence' and denies it was a trade for hostages", None, "n/a", "Medium", "see audit"),
# --- Tanker War, 1987-88 ---
(313, d(1987,7,20), "UN Security Council", "Diplomatic demand (Resolution 598)", "Iran and Iraq", "The Council unanimously demands an immediate ceasefire and a pull-back to the borders in the Iran-Iraq war", None, "n/a", "Medium", "see audit"),
(314, d(1987,7,22), "US", "Force posture (Operation Earnest Will convoys begin)", "Persian Gulf", "The first US Navy escort convoy of reflagged Kuwaiti tankers leaves the UAE for Kuwait", None, "n/a", "Medium", "see audit"),
(315, d(1987,7,24), "Iran (mine, per US)", "Mine strike (reflagged tanker Bridgeton)", "Persian Gulf, near Farsi Island", "The US-flagged tanker Bridgeton hits an Iranian mine on the first Earnest Will convoy; the hull is holed but it reaches Kuwait", 314, "Hull damage; the ship kept going", "Medium", "see audit"),
(316, d(1987,9,21), "US", "Seizure (Iran Ajr, Iranian minelaying ship)", "Iranian navy ship", "US Army helicopters fire on the Iranian ship Iran Ajr as its crew drops mines, and Navy SEALs board it", None, "Ship set on fire and later scuttled", "Medium", "see audit"),
(317, d(1987,10,8), "US", "Strike (Army helicopters sink an Iranian gunboat)", "Iranian speedboats", "Army helicopters answering a call from an observation helicopter sink one Iranian boat and badly damage two (the Washington Post reported three sunk)", None, "Iranian crew casualties not reported by allowed outlets", "Medium", "see audit"),
(318, d(1987,10,15), "Iran", "Strike (Silkworm missile, tanker Sungari)", "Tanker off Mina al-Ahmadi, Kuwait", "A Silkworm missile fired from the Faw peninsula hits the tanker Sungari and sets it on fire", None, "Tanker on fire", "Medium", "see audit"),
(319, d(1987,10,16), "Iran", "Strike (Silkworm missile, US-flagged Sea Isle City)", "Kuwaiti offshore terminal", "A second Silkworm hits the US-flagged tanker Sea Isle City at the Kuwaiti terminal", None, "18 wounded; the US master permanently blinded", "Medium", "see audit"),
(320, d(1987,10,19), "US", "Strike (destroyers shell an Iranian oil platform, Nimble Archer)", "Iranian platform, Rashadat field", "Four US destroyers shell and set ablaze an Iranian military platform; Reagan calls it a reprisal for the Silkworm attacks", 319, "Platform destroyed; no casualties reported", "Medium", "see audit"),
(321, d(1987,10,22), "Iran", "Strike (Silkworm missile, Sea Island terminal)", "Kuwait oil terminal", "A Silkworm hits Kuwait's Sea Island loading terminal and sets tanks on fire; the Washington Post ties it to the US reprisal", 320, "3 workers hurt", "Medium", "see audit"),
(322, d(1988,4,14), "Iran (mine, per US)", "Mine strike (USS Samuel B. Roberts)", "Persian Gulf", "The frigate USS Samuel B. Roberts hits an Iranian mine and is badly damaged", None, "10 sailors injured, 4 badly burned", "Medium", "see audit"),
(323, d(1988,4,18), "US", "Strike (Operation Praying Mantis, platforms and ships)", "Iranian platforms and warships", "The Navy destroys two Iranian oil platforms and sinks or cripples Iranian warships, the largest US surface action since World War II", 322, "Iranian sailors killed (15 on one missile boat); 2 US Marines died in a helicopter crash that night", "Medium", "see audit"),
(324, d(1988,4,18), "Iran", "Strike (boats and missile boat attack ships)", "Merchant ships and USS Wainwright", "The same day Iranian gunboats damage three merchant ships and the missile boat Joshan fires a Harpoon at USS Wainwright", 323, "3 merchant ships damaged", "Medium", "see audit"),
(325, d(1988,7,3), "US", "Air defense (Vincennes shoots down Iran Air 655)", "Iranian airliner", "The cruiser USS Vincennes, in a clash with Iranian boats, shoots down an Iranian airliner; Reagan calls it a defensive action and expresses sympathy", None, "All 290 aboard killed (Navy history)", "Medium", "see audit"),
# --- 1995-2001 ---
(326, d(1995,3,15), "US", "Sanctions (Executive Order 12957, oil development)", "Iran", "Clinton bars US firms from financing or managing Iranian oil development", None, "n/a", "Medium", "see audit"),
(327, d(1995,5,6), "US", "Sanctions (Executive Order 12959, trade and investment ban)", "Iran", "Clinton bans most trade and new US investment with Iran", None, "n/a", "Medium", "see audit"),
(328, d(1996,6,25), "Saudi Hezbollah (Iran-backed, per a US indictment)", "Strike (truck bombing, Khobar Towers)", "US airmen, Saudi Arabia", "Truck bomb hits the Khobar Towers housing complex; a 2001 US indictment says elements of the Iranian government inspired, supported and supervised the group", None, "19 US airmen killed, 372 Americans wounded", "Medium", "see audit"),
(329, d(1996,8,5), "US", "Sanctions (Iran and Libya Sanctions Act signed)", "Iran and Libya", "Clinton signs the act to cut off funds Iran and Libya use for terrorism and weapons of mass destruction", None, "n/a", "Medium", "see audit"),
(330, d(1998,6,17), "US", "Diplomatic proposal (Albright offers a road map)", "Iran", "Secretary of State Albright says the US could work with Iran 'when it is ready' on a road map to normal relations, while naming terrorism, human rights and weapons as concerns", None, "n/a", "Medium", "see audit"),
(331, d(2001,6,21), "US", "Indictment (Khobar Towers bombing)", "Saudi Hezbollah members", "The Justice Department charges 14 people over the Khobar bombing and says elements of the Iranian government inspired, supported and supervised the group", None, "n/a", "Medium", "see audit"),
# --- Nuclear file, 2002-2009 ---
(332, d(2002,1,29), "US", "Diplomatic statement (Bush names Iran in an 'axis of evil')", "Iran", "In the State of the Union Bush says Iran 'aggressively pursues these weapons and exports terror' and names it, with Iraq and North Korea, an axis of evil", None, "n/a", "Medium", "see audit"),
(333, d(2003,10,21), "US", "Diplomatic statement (White House on Iran's deal with Europe)", "Iran", "The White House welcomes Iran's agreement with Britain, France and Germany but says the test is follow-through and that Iran must end enrichment and reprocessing", None, "n/a", "Medium", "see audit"),
(334, d(2005,9,24), "IAEA", "Diplomatic resolution (Board finds Iran in non-compliance)", "Iran", "The IAEA Board of Governors finds Iran's failures and breaches amount to non-compliance", None, "n/a", "Medium", "see audit"),
(335, d(2006,2,4), "IAEA", "Diplomatic resolution (Iran file to go to the UN Security Council)", "Iran", "The IAEA Board asks that its reports and resolutions on Iran be sent to the UN Security Council", None, "n/a", "Medium", "see audit"),
(336, d(2006,5,31), "US", "Diplomatic proposal (Rice offers to join talks)", "Iran", "Secretary of State Rice says the US will join Britain, France and Germany at the table if Iran fully and verifiably suspends enrichment, and warns of stronger sanctions if it does not", None, "n/a", "Medium", "see audit"),
(337, d(2006,7,31), "UN Security Council", "Diplomatic demand (Resolution 1696)", "Iran", "The Council demands that Iran halt uranium enrichment", None, "n/a", "Medium", "see audit"),
(338, d(2006,12,23), "UN Security Council", "Sanctions (Resolution 1737, first UN sanctions)", "Iran", "The Council bans nuclear-related trade with Iran and freezes assets of key people and companies", None, "n/a", "Medium", "see audit"),
(339, d(2007,2,14), "US", "Diplomatic statement (Bush blames the Quds Force for weapons in Iraq)", "Iran", "Bush says he is certain Iranian-supplied weapons have been used against US forces in Iraq and blames the Quds Force; he says he does not know whether Iran's leaders ordered it", None, "n/a", "Medium", "see audit"),
(340, d(2007,2,16), "US", "Sanctions (Treasury targets three nuclear companies)", "Iran", "Treasury designates Kalaye Electric, Kavoshyar and Pioneer Energy Industries as owned or controlled by Iran's Atomic Energy Organization", None, "n/a", "Medium", "see audit"),
(341, d(2007,3,24), "UN Security Council", "Sanctions (Resolution 1747, arms embargo)", "Iran", "The Council adds a two-way arms embargo and widens the asset freeze", None, "n/a", "Medium", "see audit"),
(342, d(2007,10,25), "US", "Sanctions (IRGC, Quds Force and two banks)", "Iran", "State and Treasury designate the Revolutionary Guard, the Quds Force and Banks Melli and Mellat", None, "n/a", "Medium", "see audit"),
(343, d(2007,12,3), "US", "Diplomatic statement (intelligence estimate released)", "Iran", "National security adviser Hadley releases the intelligence estimate on Iran's nuclear program and says pressure must continue while the US stays open to talks", None, "n/a", "Medium", "see audit"),
(344, d(2008,1,6), "Iran (IRGC Navy, per the Navy)", "Naval confrontation (speedboats close on three US warships)", "Strait of Hormuz", "Five fast boats close on the cruiser Port Royal, the destroyer Hopper and the frigate Ingraham; the US ships prepare to fire before the boats turn away", None, "No shots fired", "Medium", "see audit"),
(345, d(2008,3,3), "UN Security Council", "Sanctions (Resolution 1803)", "Iran", "The Council again requires Iran to stop all enrichment and adds measures on people and companies", None, "n/a", "Medium", "see audit"),
(346, d(2009,3,20), "US", "Diplomatic proposal (Obama offers engagement)", "Iran", "In a Nowruz video message Obama offers 'engagement that is honest and grounded in mutual respect' and a new beginning", None, "n/a", "Medium", "see audit"),
(347, d(2009,9,25), "US, UK and France", "Diplomatic statement (secret enrichment site near Qom)", "Iran", "The three leaders say Iran has been building a covert enrichment plant near Qom and tell the IAEA the day before", None, "n/a", "Medium", "see audit"),
# --- Sanctions build-up, 2010-2013 ---
(348, d(2010,6,9), "UN Security Council", "Sanctions (Resolution 1929)", "Iran", "The Council passes tighter sanctions on nuclear and missile activity; Obama calls them the toughest Iran has faced", None, "n/a", "Medium", "see audit"),
(349, d(2010,7,1), "US", "Sanctions (CISADA signed)", "Iran", "Obama signs the Comprehensive Iran Sanctions, Accountability and Divestment Act; Treasury gains power to cut off foreign banks that serve Iran's nuclear program or the Guard", None, "n/a", "Medium", "see audit"),
(350, d(2011,10,11), "Iran (Quds Force, per US)", "Plot (to kill the Saudi ambassador in Washington)", "Saudi ambassador to the US", "The US says it has foiled an Iranian plot to assassinate the Saudi ambassador", None, "Foiled; no casualties", "Medium", "see audit"),
(351, d(2011,10,11), "US", "Sanctions (five people tied to the plot)", "Iran (Quds Force)", "Treasury designates five individuals over the plot", 350, "n/a", "Medium", "see audit"),
(352, d(2011,11,21), "US", "Sanctions (energy order and money-laundering finding)", "Iran", "Executive Order 13590 targets help to Iran's oil and petrochemical sectors, and Iran's whole financial sector, including its central bank, is named a primary money-laundering concern", None, "n/a", "Medium", "see audit"),
(353, d(2011,12,4), "Iran", "Drone capture (US RQ-170, Iran claims electronic ambush)", "US drone", "Iran says it brought down a US stealth drone and shows it on TV; US officials do not dispute it has the aircraft and think a malfunction is more likely", None, "Drone lost", "Medium", "see audit"),
(354, d(2012,2,6), "US", "Sanctions (Executive Order 13599 freezes Iranian assets)", "Iran", "Obama's order freezes the property of the Iranian government, its central bank and Iranian banks under US jurisdiction", None, "n/a", "Medium", "see audit"),
# --- Nuclear deal years, 2013-2017 ---
(355, d(2013,9,27), "US", "Diplomatic talks (Obama and Rouhani speak by phone)", "Iran", "The first call between US and Iranian presidents since 1979; Obama says a comprehensive nuclear solution is possible", None, "n/a", "Medium", "see audit"),
(356, d(2013,11,23), "US", "Diplomatic talks (Geneva first-step deal reached)", "Iran", "Iran halts some enrichment and gets limited relief; a six-month window opens for a full deal (the IAEA dates the deal Nov 24)", None, "n/a", "Medium", "see audit"),
(357, d(2014,1,20), "US", "Economic relief (first-step deal takes effect)", "Iran", "Treasury pauses efforts to cut Iran's oil exports further, suspends sanctions on petrochemicals, gold and autos, and lets Iran reach a limited amount of frozen funds", 356, "n/a", "Medium", "see audit"),
(358, d(2015,4,2), "US", "Diplomatic talks (Lausanne framework announced)", "Iran", "The key parameters of a final nuclear deal are announced in Lausanne", None, "n/a", "Medium", "see audit"),
(359, d(2015,4,28), "Iran", "Seizure (container ship Maersk Tigris)", "Strait of Hormuz", "Iranian forces fire on and board the Marshall Islands-flagged container ship Maersk Tigris", None, "Ship seized", "Medium", "see audit"),
(360, d(2015,4,28), "US", "Force posture (destroyer sent toward the Tigris)", "Strait of Hormuz", "The Pentagon sends surveillance aircraft and orders the destroyer USS Farragut toward the Tigris", 359, "n/a", "Medium", "see audit"),
(361, d(2015,7,14), "US", "Diplomatic talks (nuclear deal reached)", "Iran", "Obama announces a comprehensive long-term nuclear deal with Iran and the world powers", None, "n/a", "Medium", "see audit"),
(362, d(2015,7,20), "UN Security Council", "Diplomatic resolution (Resolution 2231 endorses the deal)", "Iran", "The Council unanimously endorses the nuclear deal and sets a timetable to end its earlier sanctions resolutions", None, "n/a", "Medium", "see audit"),
(363, d(2016,1,12), "Iran", "Seizure (US Navy boats and sailors)", "Farsi Island", "Iran holds US sailors who strayed into Iranian waters between Kuwait and Bahrain; they are freed within 24 hours", None, "No injuries reported; videos of the sailors released", "Medium", "see audit"),
(364, d(2016,1,16), "US", "Economic relief (Implementation Day)", "Iran", "After the IAEA verifies Iran's steps, the US and EU lift nuclear-related sanctions", None, "n/a", "Medium", "see audit"),
(365, d(2016,1,17), "US", "Diplomatic exchange (prisoners swapped)", "Iran", "Iran frees several Americans, including Jason Rezaian, and the US grants clemency to seven Iranians", None, "n/a", "Medium", "see audit"),
(366, d(2017,2,3), "US", "Sanctions (missile program and Quds Force supporters)", "Iran", "Treasury sanctions 25 people and companies; National Security Adviser Flynn says Iran's provocations will no longer be tolerated", None, "n/a", "Medium", "see audit"),
(367, d(2017,8,2), "US", "Sanctions (CAATSA signed)", "Iran, Russia and North Korea", "Trump signs the act with new sanctions on Iran, Russia and North Korea, calling it 'seriously flawed'", None, "n/a", "Medium", "see audit"),
(368, d(2017,10,13), "US", "Diplomatic statement (Trump will not certify the nuclear deal)", "Iran", "Trump announces a new Iran strategy and says he cannot certify that the deal's sanctions relief is proportionate", None, "n/a", "Medium", "see audit"),
# --- Maximum pressure begins, 2018-19 ---
(369, d(2018,5,8), "US", "Diplomatic decision (Trump leaves the nuclear deal)", "Iran", "Trump says the US will withdraw from the nuclear deal and signs a memorandum to start restoring nuclear sanctions", None, "n/a", "Medium", "see audit"),
(370, d(2018,5,21), "US", "Diplomatic demand (Pompeo's twelve demands)", "Iran", "Pompeo lists twelve demands, including an end to enrichment and to missile and proxy support, before any new deal", 369, "n/a", "Medium", "see audit"),
(371, d(2018,8,6), "US", "Sanctions (first set of nuclear-deal sanctions reimposed)", "Iran", "Trump's order restores sanctions on dollar purchases, metals, autos and Iran's currency, taking effect Aug 7", 369, "n/a", "Medium", "see audit"),
(372, d(2018,9,28), "US", "Force posture (Basra consulate on ordered departure)", "Basra, Iraq", "Pompeo puts the US consulate in Basra on ordered departure; services move to the Baghdad embassy", None, "n/a", "Medium", "see audit"),
(373, d(2018,10,3), "US", "Diplomatic statement (Pompeo blames Iran for attacks on US missions in Iraq)", "Iran", "Pompeo says Iran is to blame for the attacks on the Basra consulate and the Baghdad embassy, orders staff out of Basra and warns Tehran it will be held accountable, including for proxies", 372, "n/a", "Medium", "see audit"),
(374, d(2018,11,5), "US", "Sanctions (all nuclear-deal sanctions reimposed)", "Iran", "Treasury restores the remaining sanctions that had been lifted or waived and lists more than 700 people, companies, ships and aircraft", 369, "n/a", "Medium", "see audit"),
(375, d(2019,4,8), "US", "Sanctions (Revolutionary Guard named a terrorist organization)", "Iran (IRGC, including the Quds Force)", "State announces it will list the Guard as a Foreign Terrorist Organization, effective Apr 15", None, "n/a", "Medium", "see audit"),
(376, d(2019,4,22), "US", "Sanctions (oil purchase waivers to end)", "Iran", "State says it will not renew the exceptions that let eight countries buy Iranian oil; they expire May 2", None, "n/a", "Medium", "see audit"),
]

# ---------------------------------------------------------------------------
# Sources (every URL below was opened and read unless seen="snippet")
# ---------------------------------------------------------------------------
_WH_R = "White House (Reagan Library)"
_HG = "DoD (Naval History and Heritage Command)"
_H18 = "https://www.history.navy.mil/content/history/nhhc/about-us/leadership/director/directors-corner/h-grams/h-gram-018/h-018-1.html"
_H18_TANKER = _s('H-018-1: Tanker War timeline, 1987-1988', _HG, '2018-04-13', _H18)

SOURCES = {
 300: [_s('Iranian Crises (short history): students seize the US embassy, Nov 4, 1979', 'State Department (Office of the Historian)', '', 'https://history.state.gov/departmenthistory/short-history/iraniancrises'),
       _s('Americans Still Captive in Tehran Embassy', 'Washington Post', '1979-11-06', _WP + '1979/11/06/americans-still-captive-in-tehran-embassy/0bc9b845-a014-4942-8deb-24cc29cf157d/')],
 301: [_s('U.S., Iran Declare Halt to Oil Trade', 'Washington Post', '1979-11-13', _WP + '1979/11/13/us-iran-declare-halt-to-oil-trade/0141298a-fe50-4fae-bc59-b71eb2614765/')],
 302: [_s('The Freeze', 'Washington Post', '1979-11-15', _WP + '1979/11/15/the-freeze/a2fbd1b3-d4ae-4931-838f-33dd75a0fe09/')],
 303: [_s('Foreign Relations of the United States 1977-80, vol. XI, doc 246: Carter breaks relations, Apr 7, 1980', 'State Department (Office of the Historian)', '1980-04-07', 'https://history.state.gov/historicaldocuments/frus1977-80v11p1/d246')],
 304: [_s('Series of Mishaps Defeated Rescue in Iran', 'Washington Post', '1980-04-26', _WP + '1980/04/26/series-of-mishaps-defeated-rescue-in-iran/db6b11b9-a1b7-4617-b311-b1846726faa6/')],
 305: [_s('Iranians Demand Fast Response to Hostage Terms', 'Washington Post', '1980-11-05', _WP + '1980/11/05/iranians-demand-fast-response-to-hostage-terms/7acddba7-2421-4c90-8ac1-77561c937fe1/')],
 306: [_s('U.S. Announces Resolution of Dispute Blocking Return of Hostages from Iran', 'Washington Post', '1981-01-20', _WP + '1981/01/20/us-announces-resolution-of-dispute-blocking-return-of-hostages-from-iran/145ddcfc-06d0-4564-a4ee-a8dff50fe152/')],
 307: [_s('The Hostages Are Free', 'Washington Post', '1981-01-20', _WP + '1981/01/20/the-hostages-are-free/6558b490-ec3a-4c74-8c5c-75f063bab687/')],
 308: [_s('Judge: Iran Behind 83 Beirut Bombing', 'Washington Post', '2003-05-31', _WP + '2003/05/31/judge-iran-behind-83-beirut-bombing/b4e3c60e-2921-45fa-a9fd-a1c48ce81e44/')],
 309: [_s('The Iran-Contra Chronology', 'Washington Post', '1987-09-06', _WP + '1987/09/06/the-irancontra-chronology/40b810a1-7482-410c-93f5-31c38f153272/')],
 310: [_s('The Iran-Contra Chronology', 'Washington Post', '1987-09-06', _WP + '1987/09/06/the-irancontra-chronology/40b810a1-7482-410c-93f5-31c38f153272/')],
 311: [_s('The Iran-Contra Chronology', 'Washington Post', '1987-09-06', _WP + '1987/09/06/the-irancontra-chronology/40b810a1-7482-410c-93f5-31c38f153272/')],
 312: [_s('Reagan Denies Ransom Was Paid for Hostages', 'Washington Post', '1986-11-14', _WP + '1986/11/14/reagan-denies-ransom-was-paid-for-hostages/fd5ea2c0-028c-44a1-9fdb-6419e65d97cf/')],
 313: [_s('Resolution 598 (1987)', 'UN (Digital Library)', '1987-07-20', 'https://digitallibrary.un.org/record/137345?ln=en')],
 314: [_H18_TANKER],
 315: [_s('Reflagged Tanker Hits Gulf Mine', 'Washington Post', '1987-07-25', _WP + '1987/07/25/reflagged-tanker-hits-gulf-mine/43ce4376-1ac5-4919-92f9-e4109abdf554/'), _H18_TANKER],
 316: [_s('U.S. Navy Seizes Iranian Mine Ship', 'Washington Post', '1987-09-23', _WP + '1987/09/23/us-navy-seizes-iranian-mine-ship/d68e7508-f335-4e56-ab8a-7a06b39f6607/'), _H18_TANKER],
 317: [_s('U.S. Helicopters Sink 3 Iranian Gunboats in Persian Gulf', 'Washington Post', '1987-10-09', _WP + '1987/10/09/us-helicopters-sink-3-iranian-gunboats-in-persian-gulf/cfe5e927-97bf-4080-8e57-d8add44c38d2/'), _H18_TANKER],
 318: [_s('Iran Hits U.S.-Owned Tanker', 'Washington Post', '1987-10-16', _WP + '1987/10/16/iran-hits-us-owned-tanker/bf2e5e5c-21c4-4ae3-9da3-b68002bfc58e/'), _H18_TANKER],
 319: [_H18_TANKER,
       _s('Statement on the United States Reprisal Against Iran (Silkworm strikes on US-flagged vessels)', _WH_R, '1987-10-19', 'https://www.reaganlibrary.gov/archives/speech/statement-united-states-reprisal-against-iran'),
       _s('Iranian Missile Hits U.S.-Flagged Ship at Kuwaiti Port', 'Washington Post', '1987-10-17', _WP + '1987/10/17/iranian-missile-hits-us-flagged-ship-at-kuwaiti-port/4677b1a4-180e-46ef-99bd-21590c927448/', 'snippet')],
 320: [_s('Statement on the United States Reprisal Against Iran', _WH_R, '1987-10-19', 'https://www.reaganlibrary.gov/archives/speech/statement-united-states-reprisal-against-iran'),
       _s('U.S. Destroyers Shell Iranian Military Platform in Gulf', 'Washington Post', '1987-10-20', _WP + '1987/10/20/us-destroyers-shell-iranian-military-platform-in-gulf/297e0868-effb-4ac4-952b-75a5982082a7/')],
 321: [_s('Silkworm Hits Kuwaiti Oil Terminal', 'Washington Post', '1987-10-23', _WP + '1987/10/23/silkworm-hits-kuwaiti-oil-terminal/38039a67-6e04-45dc-81d0-208198de6b04/')],
 322: [_s('Operation Praying Mantis (USS Samuel B. Roberts mined, Apr 14, 1988)', _HG, '', 'https://www.history.navy.mil/browse-by-topic/wars-conflicts-and-operations/middle-east/praying-mantis.html'), _H18_TANKER],
 323: [_s('Operation Praying Mantis', _HG, '', 'https://www.history.navy.mil/browse-by-topic/wars-conflicts-and-operations/middle-east/praying-mantis.html'),
       _s('U.S. Sinks or Cripples 6 Iranian Ships in Gulf Battles', 'Washington Post', '1988-04-19', _WP + '1988/04/19/us-sinks-or-cripples-6-iranian-ships-in-gulf-battles/f5a66fc6-589a-4b4f-ab5c-876bb6b451df/')],
 324: [_H18_TANKER],
 325: [_s('Statement on the Destruction of an Iranian Jetliner by the United States Navy Over the Persian Gulf', _WH_R, '1988-07-03', 'https://www.reaganlibrary.gov/archives/speech/statement-destruction-iranian-jetliner-united-states-navy-over-persian-gulf'), _H18_TANKER],
 326: [_s('Executive Order 12957: barring Iranian petroleum development', 'White House (Clinton archive)', '1995-03-15', 'https://clintonwhitehouse6.archives.gov/1995/03/1995-03-15-executive-order-12957-barring-iranian-petroleum-development.html')],
 327: [_s('Executive Order 12959: Iran trade ban', 'White House (Clinton archive)', '1995-05-06', 'https://clintonwhitehouse6.archives.gov/1995/05/1995-05-06-executive-order-12959-on-iran-trade-ban.html')],
 328: [_s('Attorney General statement on the Khobar Towers indictment', 'Justice Department', '2001-06-21', 'https://www.justice.gov/archive/opa/pr/2001/June/275ag.htm')],
 329: [_s('Remarks by the President at Sanctions Act signing', 'White House (Clinton archive)', '1996-08-05', 'https://clintonwhitehouse6.archives.gov/1996/08/1996-08-05-remarks-by-president-at-sanctions-act-signing.html')],
 330: [_s('Albright to the Asia Society, Jun 17, 1998', 'State Department', '1998-06-18', 'https://1997-2001.state.gov/statements/1998/980617a.html')],
 331: [_s('Attorney General statement on the Khobar Towers indictment', 'Justice Department', '2001-06-21', 'https://www.justice.gov/archive/opa/pr/2001/June/275ag.htm')],
 332: [_s('President Delivers State of the Union Address', 'White House (Bush archive)', '2002-01-29', 'https://georgewbush-whitehouse.archives.gov/news/releases/2002/01/20020129-11.html')],
 333: [_s('Remarks by the Press Secretary on Iran', 'White House (Bush archive)', '2003-10-21', 'https://georgewbush-whitehouse.archives.gov/news/releases/2003/10/20031021-15.html')],
 334: [_s('IAEA and Iran: Chronology of Key Events (24 Sep 2005)', 'IAEA', '', 'https://www.iaea.org/newscenter/focus/iran/chronology-of-key-events')],
 335: [_s('IAEA and Iran: Chronology of Key Events (4 Feb 2006)', 'IAEA', '', 'https://www.iaea.org/newscenter/focus/iran/chronology-of-key-events')],
 336: [_s('Statement by Secretary of State Condoleezza Rice, May 31, 2006', 'State Department', '2006-05-31', 'https://2001-2009.state.gov/secretary/rm/2006/67088.htm')],
 337: [_s('S/RES/1696 (2006)', 'UN Security Council', '2006-07-31', 'https://main.un.org/securitycouncil/en/s/res/1696-(2006)')],
 338: [_s('S/RES/1737 (2006)', 'UN Security Council', '2006-12-23', 'https://main.un.org/securitycouncil/en/s/res/1737-(2006)')],
 339: [_s('Bush Says Iran Is Supplying Weapons in Iraq', 'Washington Post', '2007-02-14', 'https://www.washingtonpost.com/archive/business/technology/2007/02/14/bush-says-iran-is-supplying-weapons-in-iraq/da5011a5-975c-4074-87cf-4bb309b19624/')],
 340: [_s('Treasury Targets Iranian Companies for Supporting WMD Proliferation', 'Treasury', '2007-02-16', 'https://home.treasury.gov/news/press-releases/hp267')],
 341: [_s('S/RES/1747 (2007)', 'UN Security Council', '2007-03-24', 'https://main.un.org/securitycouncil/en/s/res/1747-(2007)')],
 342: [_s('Fact Sheet: Designation of Iranian Entities and Individuals for Proliferation Activities and Support for Terrorism', 'Treasury', '2007-10-25', 'https://home.treasury.gov/news/press-releases/hp644')],
 343: [_s('Statement by National Security Advisor Stephen Hadley', 'White House (Bush archive)', '2007-12-03', 'https://georgewbush-whitehouse.archives.gov/news/releases/2007/12/20071203-5.html')],
 344: [_s('Port Royal II (CG-73): five Iranian speedboats close on three US ships, Jan 6, 2008', _HG, '', 'https://www.history.navy.mil/research/histories/ship-histories/danfs/p/port-royal-ii--cg-73-.html')],
 345: [_s('S/RES/1803 (2008)', 'UN Security Council', '2008-03-03', 'https://main.un.org/securitycouncil/en/s/res/1803-(2008)')],
 346: [_s('Videotaped Remarks by The President in Celebration of Nowruz', 'White House (Obama archive)', '2009-03-20', 'https://obamawhitehouse.archives.gov/the-press-office/videotaped-remarks-president-celebration-nowruz')],
 347: [_s('Statements by President Obama, President Sarkozy and Prime Minister Brown on Iranian Nuclear Facility', 'White House (Obama archive)', '2009-09-25', 'https://obamawhitehouse.archives.gov/the-press-office/2009/09/25/statements-president-obama-french-president-sarkozy-and-british-prime-mi')],
 348: [_s('S/RES/1929 (2010)', 'UN Security Council', '2010-06-09', 'https://main.un.org/securitycouncil/en/s/res/1929-(2010)'),
       _s('Remarks by the President on United Nations Security Council Resolution on Iran Sanctions', 'White House (Obama archive)', '2010-06-09', 'https://obamawhitehouse.archives.gov/the-press-office/remarks-president-united-nations-security-council-resolution-iran-sanctions')],
 349: [_s('Statement of Secretary Geithner on the Signing of the Iran Sanctions Act', 'Treasury', '2010-07-01', 'https://home.treasury.gov/news/press-releases/tg767')],
 350: [_s('Treasury Sanctions Five Individuals Tied to Iranian Plot to Assassinate the Saudi Arabian Ambassador', 'Treasury', '2011-10-11', 'https://home.treasury.gov/news/press-releases/tg1320')],
 351: [_s('Treasury Sanctions Five Individuals Tied to Iranian Plot to Assassinate the Saudi Arabian Ambassador', 'Treasury', '2011-10-11', 'https://home.treasury.gov/news/press-releases/tg1320')],
 352: [_s('Fact Sheet: New Sanctions on Iran', 'Treasury', '2011-11-21', 'https://home.treasury.gov/news/press-releases/tg1367')],
 353: [_s('Iran Displays Plane Identified as Downed U.S. Drone', 'Washington Post', '2011-12-08', 'https://www.washingtonpost.com/world/middle_east/iran-displays-plane-identified-as-downed-us-drone/2011/12/08/gIQA7xvGgO_story.html'),
       _s('Iran says it downed U.S. stealth drone; Pentagon acknowledges aircraft downing', 'Washington Post', '2011-12-04', 'https://www.washingtonpost.com/world/national-security/iran-says-it-downed-us-stealth-drone-pentagon-acknowledges-aircraft-downing/2011/12/04/gIQAyxa8TO_story.html', 'snippet')],
 354: [_s('Fact Sheet: Implementation of National Defense Authorization Act Sanctions on Iran (EO 13599)', 'Treasury', '2012-02-06', 'https://home.treasury.gov/news/press-releases/tg1409')],
 355: [_s('Statement by the President (call with President Rouhani)', 'White House (Obama archive)', '2013-09-27', 'https://obamawhitehouse.archives.gov/the-press-office/2013/09/27/statement-president')],
 356: [_s("Statement by the President on First Step Agreement on Iran's Nuclear Program", 'White House (Obama archive)', '2013-11-23', 'https://obamawhitehouse.archives.gov/the-press-office/2013/11/23/statement-president-first-step-agreement-irans-nuclear-program'),
       _s('IAEA and Iran: Chronology of Key Events (24 Nov 2013)', 'IAEA', '', 'https://www.iaea.org/newscenter/focus/iran/chronology-of-key-events')],
 357: [_s('Treasury: how the US is implementing the Joint Plan of Action', 'Treasury', '2014-01-20', 'https://home.treasury.gov/news/press-releases/jl2260')],
 358: [_s('Parameters for a Joint Comprehensive Plan of Action Regarding the Islamic Republic of Iran', 'State Department', '2015-04-02', 'https://2009-2017.state.gov/r/pa/prs/ps/2015/04/240170.htm')],
 359: [_s('U.S. dispatches destroyer after Iran boards commercial ship', 'Washington Post', '2015-04-28', 'https://www.washingtonpost.com/world/national-security/us-dispatches-destroyer-after-iran-boards-commercial-ship/2015/04/28/56ef48c2-edc6-11e4-a55f-38924fca94f9_story.html')],
 360: [_s('U.S. dispatches destroyer after Iran boards commercial ship', 'Washington Post', '2015-04-28', 'https://www.washingtonpost.com/world/national-security/us-dispatches-destroyer-after-iran-boards-commercial-ship/2015/04/28/56ef48c2-edc6-11e4-a55f-38924fca94f9_story.html')],
 361: [_s('Statement by the President on Iran', 'White House (Obama archive)', '2015-07-14', 'https://obamawhitehouse.archives.gov/the-press-office/2015/07/14/statement-president-iran')],
 362: [_s('Resolution 2231 (2015) on Iran Nuclear Issue', 'UN Security Council', '2015-07-20', 'https://main.un.org/securitycouncil/en/content/2231/background')],
 363: [_s('Briefing on the Release of United States Sailors by Iran', 'State Department', '2016-01-13', 'https://2009-2017.state.gov/r/pa/prs/ps/2016/01/251188.htm'),
       _s('Statement by the President on Iran', 'White House (Obama archive)', '2016-01-17', 'https://obamawhitehouse.archives.gov/the-press-office/2016/01/17/statement-president-iran')],
 364: [_s('Remarks on Implementation Day', 'State Department', '2016-01-16', 'https://2009-2017.state.gov/secretary/remarks/2016/01/251336.htm')],
 365: [_s('Statement by the President on Iran', 'White House (Obama archive)', '2016-01-17', 'https://obamawhitehouse.archives.gov/the-press-office/2016/01/17/statement-president-iran')],
 366: [_s('Treasury Sanctions Supporters of Iran\'s Ballistic Missile Program and IRGC Qods Force', 'Treasury', '2017-02-03', 'https://home.treasury.gov/news/press-releases/as0004'),
       _s('Statement by National Security Advisor Michael T. Flynn on Iran', 'White House (Trump archive)', '2017-02-03', 'https://trumpwhitehouse.archives.gov/briefings-statements/statement-national-security-advisor-michael-t-flynn-iran/')],
 367: [_s('Statement by President Trump on Signing the Countering America\'s Adversaries Through Sanctions Act', 'White House (Trump archive)', '2017-08-02', 'https://trumpwhitehouse.archives.gov/briefings-statements/statement-president-donald-j-trump-signing-countering-americas-adversaries-sanctions-act/')],
 368: [_s('Remarks by President Trump on Iran Strategy', 'White House (Trump archive)', '2017-10-13', 'https://trumpwhitehouse.archives.gov/briefings-statements/remarks-president-trump-iran-strategy/')],
 369: [_s('Remarks by President Trump on the Joint Comprehensive Plan of Action', 'White House (Trump archive)', '2018-05-08', 'https://trumpwhitehouse.archives.gov/briefings-statements/remarks-president-trump-joint-comprehensive-plan-action/')],
 370: [_s('After the Deal: A New Iran Strategy (Pompeo, Heritage Foundation)', 'State Department', '2018-05-21', 'https://2017-2021.state.gov/after-the-deal-a-new-iran-strategy/')],
 371: [_s('Executive Order Reimposing Certain Sanctions with Respect to Iran', 'White House (Trump archive)', '2018-08-06', 'https://trumpwhitehouse.archives.gov/presidential-actions/executive-order-reimposing-certain-sanctions-respect-iran/')],
 372: [_s('On Ordered Departure at Consulate Basrah', 'State Department', '2018-09-28', 'https://2017-2021.state.gov/on-ordered-departure-at-consulate-basrah')],
 373: [_s('Remarks to the Media (Pompeo, Oct 3, 2018)', 'State Department', '2018-10-03', 'https://2017-2021.state.gov/remarks-to-the-media-3')],
 374: [_s('Re-imposition of the sanctions on Iran that had been lifted or waived under the JCPOA', 'Treasury (OFAC)', '2018-11-05', 'https://ofac.treasury.gov/sanctions-programs-and-country-information/iran-sanctions/re-imposition-of-the-sanctions-on-iran-that-had-been-lifted-or-waived-under-the-jcpoa')],
 375: [_s('Designation of the Islamic Revolutionary Guard Corps', 'State Department', '2019-04-08', 'https://2017-2021-translations.state.gov/2019/04/08/designation-of-the-islamic-revolutionary-guard-corps/index.html')],
 376: [_s('Iran Sanctions: oil waivers will not be renewed (CRS In Focus IN11108)', 'CRS (via EveryCRSReport)', '2019-04-22', 'https://www.everycrsreport.com/reports/IN11108.html')],
}
VERDICT = {k: 'confirmed' for k in SOURCES}
PARTLY = set()

# ---------------------------------------------------------------------------
# Trigger census rows for US moves (window: ~5 days for a reply). Rows for #316, #317, #320 and #323 are
# inside the Tanker War stretch below, so the engine moves them out of the counts.
# ---------------------------------------------------------------------------
CENSUS = [
 (301, "Economic/Blockade", "N", "Oil import ban, Nov 12, 1979. The hostages stayed in captivity, but no new Iranian attack on US forces or ships was found Nov 13-17."),
 (302, "Economic/Blockade", "N", "Asset freeze, Nov 14, 1979. No new Iranian attack found Nov 15-19."),
 (303, "Economic/Blockade", "N", "Export ban and break in relations, Apr 7, 1980. No new Iranian attack found Apr 8-12."),
 (316, "Military/Property", "Unclear", "Iran Ajr seized, Sep 21, 1987. Iran was hitting ships nearly every week in the Tanker War, so a quiet five days proves nothing. The Navy timeline shows no Iranian act against US forces until Oct 8."),
 (317, "Military/Property", "Unclear", "Gunboat clash, Oct 8, 1987. The next Iranian strikes were the Silkworm hits on Oct 15 and 16 (7-8 days later, outside the window), but Tanker War ship attacks make a five-day read unreliable."),
 (320, "Military/Property", "R-weak", "Strike on the Rashadat platform, Oct 19, 1987 -> Silkworm hits Kuwait's Sea Island terminal Oct 22, 3 workers hurt (Washington Post ties it to the reprisal). Timing and a press link only."),
 (323, "Military/Property", "R-strong", "Operation Praying Mantis, Apr 18, 1988 -> same day Iranian gunboats damage three merchant ships and the missile boat Joshan fires a Harpoon at USS Wainwright (Navy history)."),
 (326, "Economic/Blockade", "N", "Oil-development ban, Mar 15, 1995. No Iranian attack on US forces, ships or citizens found Mar 16-20."),
 (327, "Economic/Blockade", "N", "Trade and investment ban, May 6, 1995. No Iranian attack found May 7-11."),
 (329, "Economic/Blockade", "N", "Iran and Libya Sanctions Act, Aug 5, 1996. No Iranian attack found Aug 6-10."),
 (340, "Economic/Blockade", "Unclear", "Nuclear-company sanctions, Feb 16, 2007. Iran-backed militias were attacking US troops in Iraq almost daily, so a five-day gap shows nothing."),
 (342, "Economic/Blockade", "Unclear", "Guard, Quds Force and bank sanctions, Oct 25, 2007. Same reason as #340: militia attacks in Iraq were near-daily."),
 (349, "Economic/Blockade", "N", "CISADA signed, Jul 1, 2010. No Iranian attack found Jul 2-6."),
 (351, "Economic/Blockade", "N", "Sanctions on five people over the Saudi-ambassador plot, Oct 11, 2011. No Iranian attack found Oct 12-16."),
 (352, "Economic/Blockade", "N", "Energy order and money-laundering finding, Nov 21, 2011. No Iranian attack on US targets found Nov 22-26 (the mob attack on the British embassy came Nov 29 and hit the UK)."),
 (354, "Economic/Blockade", "N", "Order freezing Iranian assets, Feb 6, 2012. No Iranian attack found Feb 7-11."),
 (366, "Economic/Blockade", "N", "Missile-program sanctions, Feb 3, 2017. No Iranian attack found Feb 4-8."),
 (367, "Economic/Blockade", "N", "CAATSA signed, Aug 2, 2017. No Iranian attack found Aug 3-7."),
 (371, "Economic/Blockade", "N", "First set of deal sanctions reimposed, Aug 6, 2018. No Iranian attack found Aug 7-11."),
 (374, "Economic/Blockade", "N", "All remaining deal sanctions reimposed, Nov 5, 2018. No Iranian attack found Nov 6-10."),
 (375, "Economic/Blockade", "N", "Guard named a terrorist organization, Apr 8, 2019. No Iranian attack on US forces or ships found Apr 9-13."),
 (376, "Economic/Blockade", "N", "Oil waivers to end, Apr 22, 2019. No Iranian attack found Apr 23-27 (the next logged act was the Fujairah sabotage on May 12, #202)."),
]

# Reply pairs (pair id, trigger, reply, category, reply caused casualties Y/N, note)
PAIRS = [
 (300, 300, 304, "Personnel/Casualty", "Y", "The US answers the hostage-taking with a rescue attempt five months later; eight US servicemen die in the failed mission"),
 (301, 319, 320, "Military/Property", "N", "The US shells an Iranian platform three days after Silkworm missiles hit a US-flagged tanker; no casualties reported"),
 (302, 320, 321, "Military/Property", "Y", "A Silkworm hits Kuwait's Sea Island terminal three days after the US reprisal; three workers hurt"),
 (303, 322, 323, "Military/Property", "Y", "Operation Praying Mantis four days after the Roberts hit a mine; Iranian sailors killed"),
 (304, 323, 324, "Military/Property", "N", "Iranian boats and a missile boat attack ships the same day as Praying Mantis; damage but no deaths reported"),
 (305, 359, 360, "Military/Property", "N", "The Pentagon sends a destroyer the day Iran seizes the Maersk Tigris; no casualties"),
]

# Continuous-fighting window (US moves inside are context only) and the acts that started it
WINDOWS = [(d(1987, 7, 22), d(1988, 7, 3))]
START_ACTS = set()

# Phases, oldest first
PHASES = [
 ("Hostage crisis", d(1979, 11, 4), d(1981, 1, 20), "#300 the embassy is seized; oil ban, asset freeze, break in relations and the failed rescue (#301-#304) until the hostages are freed (#307)"),
 ("Proxy war and Iran-Contra", d(1981, 1, 21), d(1987, 7, 21), "Beirut barracks bombing (#308) and the secret arms channel to Iran (#309-#312)"),
 ("Tanker War", d(1987, 7, 22), d(1988, 8, 20), "#314 US convoys begin; mines, Silkworm strikes and the two US reprisals (#320, #323); the Iran Air 655 shootdown (#325)"),
 ("Quiet years", d(1988, 8, 21), d(1995, 3, 14), "No logged Iran events: the record is thin here"),
 ("Embargo and containment", d(1995, 3, 15), d(2001, 12, 31), "Executive orders (#326, #327), the sanctions act (#329), Khobar (#328) and the 1998 offer (#330)"),
 ("Nuclear file opens", d(2002, 1, 1), d(2009, 12, 31), "'Axis of evil' (#332), IAEA findings, UN resolutions (#337, #338, #341, #345), Quds Force designations (#342) and Obama's offer (#346)"),
 ("Sanctions build-up", d(2010, 1, 1), d(2013, 9, 26), "UN 1929 and CISADA (#348, #349), the 2011 plot (#350) and the oil and bank sanctions (#352, #354)"),
 ("Nuclear deal years", d(2013, 9, 27), d(2018, 5, 7), "Rouhani call (#355), interim deal (#356), final deal (#361), sailors (#363), Implementation Day (#364)"),
 ("Maximum pressure begins", d(2018, 5, 8), d(2019, 5, 4), "#369 the US leaves the deal; sanctions return (#371, #374), the Guard is listed (#375) and oil waivers end (#376)"),
]

CHAIN_NAMES = {
 300: "Embassy seized -> oil ban, asset freeze, break in relations, failed rescue (hostage crisis)",
 305: "Parliament sets terms -> Algiers deal -> hostages freed",
 314: "Convoys begin -> Bridgeton mine (Tanker War, context)",
 319: "Sea Isle City hit -> Nimble Archer -> Silkworm on Kuwait terminal (Tanker War, context)",
 322: "Roberts mine -> Praying Mantis -> Iranian attacks the same day (Tanker War, context)",
 350: "Saudi-ambassador plot -> Treasury sanctions",
 356: "Geneva first-step deal -> sanctions relief",
 359: "Maersk Tigris seized -> destroyer sent",
 369: "Deal exit -> twelve demands -> sanctions return",
 372: "Basra consulate drawdown -> Pompeo blames Iran",
}

# Lines added to the page's list of rows left out of the counts
NOTES = [
 "Tanker War, Jul 22, 1987 - Jul 3, 1988: Iran and Iraq were hitting ships almost every week, so every US move has a 'reply' by default. US moves in that stretch (#316, #317, #320, #323) are logged and linked but not counted. "
 "Nimble Archer (#320) had a press-linked Silkworm reply three days later and Praying Mantis (#323) drew Iranian attacks the same day; both would count if the stretch were not left out.",
 "Early rows not counted: #304 (covert rescue attempt), #309-#311 (covert arms deliveries and the secret trip), #314 and #360 (deployments, measured separately), #325 (accidental airliner shootdown), "
 "#340 and #342 (Iran-backed militia attacks in Iraq were near-daily in 2007, so no clean 5-day read), and all talks, statements and UN or IAEA rows.",
 "Before 2019 the record is a sample of the big moments, not every day. An N row means no new Iranian attack was found in the pages read, not that the days were searched one by one.",
]
