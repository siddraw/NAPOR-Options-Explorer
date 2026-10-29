"""NAPOR North Korea: the first 24 years, Mar 12, 1993 - Aug 29, 2017 (research file).

Same shape as events.py. Event IDs 2500-2599 and pair IDs 2500-2599 belong to this file (2500-2587 used,
with 2545, 2577 and the numbers after 2587 left free). events.py continues from Aug 31, 2017 (IDs 2001-2076).

Option letters for US moves are the ones in events.py and config.py (B talks, C sanctions, D joint drills,
E interdiction, F missile defense, G strategic assets, H other posture). A (hold) is not tagged.
Judgment calls on letters:
- Talks rows are tagged B, and so are three moves that came out of talks: the Sep 1999 sanctions easing (#2508),
  the Jun 2008 TWEA / terror-list notice (#2530) and the Oct 2008 delisting (#2531).
- #2541 (USS George Washington drills in the Yellow Sea, Nov 28, 2010) is tagged D, not G: the source calls it
  a joint exercise.
- UN Security Council resolutions, KEDO's fuel-oil halt, the Warmbier release and former President Clinton's
  trip (#2535) have no option letter: they are not US moves of kinds B to H, or not a US government act.

Source rules (docs/SOURCE_STANDARD.md):
- Only allowed outlets and official statements. Wire stories read on a syndicated page are labelled "AP (via ...)".
  seen="full text" means the page was opened and read; seen="snippet" means only the search-result line was seen.
- No KCNA or Rodong Sinmun page was opened. What North Korea says is reached through an allowed outlet.
- Pre-2000s archives are thin. Many rows rest on one official page (White House, State Department, UN) or one
  wire story read through a syndicated copy. Where the page I read has no clear date, the headline is taken from
  the page URL and the row is in PARTLY.
- #2502 rests on a State Department (USIA) text read on a GlobalSecurity.org mirror and #2514 on KEDO's own page
  (an international body's official page, which scores 0.80 like an allowed outlet). #2502 is a mirror of a State Department text, so it
  is labelled "via GlobalSecurity.org".
- The 2016 and 2017 launch rows (#2562, #2564, #2567, #2574, #2586) rest on one CBS News launch timeline
  (published Sep 6, 2017, built from NTI and the Joint Chiefs). Its dates are US dates and may be a day
  earlier than the Korea date. Those rows are in PARTLY.

How reply windows were read (Trigger Census in CENSUS below):
- R-weak: a logged North Korean act inside 7 days and a plausible link. No page ties the act to the US move.
- N: the 7 days were checked against a list and nothing was found.
    * 2016-17: the CBS launch timeline lists every launch it knows of. N here means no launch in the window.
      Other provocations (artillery, cyber, statements) were not searched.
    * 1999-2005 (#2508-#2511, #2520, #2522-#2524): NPR's missile chronology has no launch entry in the window.
      The same chronology leaves out the Feb and Mar 2003 cruise-missile tests, so it is not a full list. The
      rows say so.
- Unclear: the move cannot be separated from another act (#2551, same-day as the Kaesong ban).
- Unverified: the window was not searched. This is most of the 1993-2013 rows.

Dropped, not logged (no allowed source found, or only mirrors, think tanks or Wikipedia):
- The May 1993 Nodong test, the 1994 Carter trip, the 1995-97 famine aid talks, the 1999 and 2002 Yellow Sea
  clashes, the 2005 and 2006 Treasury BDA follow-ups, the 2011 US-DPRK talks, the Aug 2017 Guam threat.
- The Sep 2016 engine test (Sep 19-20) was not confirmed in an allowed outlet.

Thin eras (also in config.py under_logged): 1995-1997, 2004, 2007-2008, 2011, 2014-2015. Many Treasury rounds
and almost every pre-2016 short-range launch are missing.
"""
import datetime as dt


def d(y, m, day):
    return dt.date(y, m, day)


def _s(headline, outlet, published, url, seen="snippet"):
    return {'headline': headline, 'outlet': outlet, 'published': published, 'seen': seen, 'url': url}


# Columns: ID, Date, Actor, Action Type, Target, Detail, Trigger ID, Severity, Confidence, Source
EVENTS = [
(2500, d(1993,3,12), "North Korea", "Diplomatic declaration (notice to withdraw from the NPT)", "Treaty on the Non-Proliferation of Nuclear Weapons", "North Korea's government decides to withdraw from the NPT under Article X and tells the UN Security Council in a letter dated Mar 12 (S/25407). The notice takes effect after three months; a French statement in the Council cites the Jun 12 deadline", None, "n/a", "Medium", "see audit"),
(2501, d(1993,6,11), "US and North Korea", "Diplomatic talks (New York talks; North Korea suspends its NPT withdrawal)", "North Korea", "President Clinton issues a statement on the US-North Korea talks in New York. North Korea suspends its withdrawal from the NPT, a day before the notice was due to take effect (Jun 12). Date is the White House statement date", None, "n/a", "Medium", "see audit"),
(2502, d(1994,3,3), "US", "Diplomatic talks (Geneva round set; Team Spirit '94 suspended)", "North Korea", "State Department spokesman Michael McCurry announces that the US and North Korea will meet in Geneva on Mar 21 for a third round, and that South Korea and the US have decided to suspend the Team Spirit exercise in 1994", None, "n/a", "Medium", "see audit"),
(2503, d(1994,6,22), "US", "Diplomatic talks (North Korea freeze; Geneva talks; sanctions push paused)", "North Korea", "In remarks to reporters, President Clinton says North Korea has agreed to freeze its nuclear program while talks go on. The US will hold talks in Geneva and pause its push for UN sanctions", None, "n/a", "Medium", "see audit"),
(2504, d(1994,10,18), "US", "Diplomatic talks (Agreed Framework text settled)", "North Korea", "White House statement: the US and North Korea have agreed the text of an agreement on North Korea's nuclear program. Robert Gallucci is to sign it in Geneva on Friday, Oct 21. Logged on the announcement date", None, "n/a", "Medium", "see audit"),
(2505, d(1994,12,17), "North Korea", "Provocation (US Army helicopter shot down)", "US Army OH-58 helicopter near the DMZ", "An unarmed OH-58 strays into North Korea near the DMZ and is shot down. North Korea says it shot down an 'enemy helicopter'. Chief Warrant Officer David Hilemon is killed and Bobby Hall is held; Hall is released on Dec 29. Dated Dec 17: the Dec 18 report says only 'Saturday'", None, "1 US pilot killed; 1 held 12 days", "Medium", "see audit"),
(2506, d(1996,4,16), "US", "Diplomatic proposal (four-party talks)", "North Korea", "Presidents Clinton and Kim Young-sam, meeting on Cheju island, propose four-party talks among the two Koreas, the US and China on a peace agreement", None, "n/a", "Medium", "see audit"),
(2507, d(1998,8,31), "North Korea", "Missile launch (multistage Taepodong-1, over Japan)", "Pacific Ocean, over Japan", "North Korea fires a multistage Taepodong-1 missile over Japan and into the Pacific Ocean (NPR chronology)", None, "No damage reported", "Medium", "see audit"),
(2508, d(1999,9,17), "US", "Diplomatic talks (Berlin talks; sanctions eased; missile test freeze)", "North Korea", "After talks in Berlin on Sep 7-12, the White House says the US is easing sanctions on North Korea. On Sep 13 North Korea pledged to freeze long-range missile tests while talks go on. Logged on the briefing date", None, "n/a", "Medium", "see audit"),
(2509, d(2000,10,12), "US and North Korea", "Diplomatic talks (joint communique, Washington)", "North Korea", "After a visit by North Korea's Vice Marshal Jo Myong Rok (Oct 9-12) the two countries issue a joint communique: they will take steps to fundamentally improve relations, and Secretary Albright will visit North Korea soon", None, "n/a", "Medium", "see audit"),
(2510, d(2000,10,24), "US", "Diplomatic talks (Albright visit, Pyongyang)", "North Korea", "Secretary of State Madeleine Albright ends a visit to North Korea that ABC News calls historic. Dated the day ABC says the visit ended", None, "n/a", "Medium", "see audit"),
(2511, d(2001,6,6), "US", "Diplomatic proposal (policy review done; offer to talk)", "North Korea", "President Bush announces that his North Korea policy review is complete and that the US will seek talks with North Korea. A second White House page for this statement shows Jun 13", None, "n/a", "Medium", "see audit"),
(2512, d(2002,1,29), "US", "Diplomatic statement (State of the Union: 'axis of evil')", "North Korea, Iran and Iraq", "In his State of the Union address President Bush names North Korea, with Iran and Iraq, as an 'axis of evil'", None, "n/a", "Medium", "see audit"),
(2513, d(2002,10,16), "North Korea (per US officials)", "Diplomatic declaration (acknowledges a uranium enrichment program)", "US envoy James Kelly, Pyongyang", "US officials say North Korea told Assistant Secretary of State James Kelly in Pyongyang that it has a uranium enrichment program, which breaks the 1994 Agreed Framework. The US ends its drive for better relations. Dated by the US announcement reported on Oct 17", None, "n/a", "Medium", "see audit"),
(2514, d(2002,11,14), "KEDO board (US, South Korea, Japan, EU)", "Sanction (KEDO halts heavy fuel oil shipments)", "North Korea", "The KEDO executive board suspends heavy fuel oil deliveries starting with the December shipment; later shipments depend on North Korea taking concrete and credible steps to end its uranium enrichment program", None, "n/a", "Medium", "see audit"),
(2515, d(2002,12,27), "North Korea", "Provocation (IAEA seals and cameras removed; inspectors ordered out)", "IAEA monitoring at Yongbyon", "That week North Korea removes IAEA seals and cameras at its nuclear facilities and orders the inspectors out of the country (CBS, CNN)", None, "No injuries reported", "Medium", "see audit"),
(2516, d(2003,1,10), "North Korea", "Diplomatic declaration (announces NPT withdrawal)", "Treaty on the Non-Proliferation of Nuclear Weapons", "North Korea announces it is pulling out of the NPT (NPR). The page has no time stamp; dated by its URL", None, "n/a", "Medium", "see audit"),
(2517, d(2003,3,2), "North Korea", "Provocation (four MiGs intercept US RC-135S)", "US Air Force RC-135S reconnaissance aircraft", "Four North Korean MiG fighters intercept a US Air Force RC-135S reconnaissance aircraft. CBS (Mar 4) says 'Sunday', which is Mar 2; NPR dates the intercept Mar 1", None, "No injuries; plane landed safely", "Medium", "see audit"),
(2518, d(2003,3,5), "US", "Force posture (24 bombers to Guam)", "Guam", "The US sends 24 bombers (12 B-1B and 12 B-52) to Guam as a deterrent against North Korea. The Pentagon says the move was planned long before", None, "n/a", "Medium", "see audit"),
(2519, d(2003,3,10), "North Korea", "Missile launch (short-range anti-ship cruise missile)", "Sea of Japan", "North Korea fires a short-range anti-ship cruise missile on Monday, Mar 10 (PBS, Mar 11); an earlier one was fired on Feb 24. Day set from the weekday in the PBS report", 2518, "No damage reported", "Medium", "see audit"),
(2520, d(2003,8,27), "US", "Diplomatic talks (first six-party round, Beijing)", "North Korea", "The first round of six-party talks opens: the US, North Korea, China, South Korea, Japan and Russia", None, "n/a", "Medium", "see audit"),
(2521, d(2005,2,10), "North Korea", "Diplomatic declaration (says it has nuclear weapons)", "Six-party talks", "North Korea's foreign ministry says it has built nuclear weapons (Al Jazeera). North Korea CLAIMS this; no test had been held", None, "n/a", "Medium", "see audit"),
(2522, d(2005,9,15), "US (Treasury)", "Sanction (Banco Delta Asia named a money-laundering concern, Section 311)", "Banco Delta Asia, Macau", "Treasury names Banco Delta Asia a primary money-laundering concern under Section 311 of the USA PATRIOT Act, citing its dealings with North Korea", None, "n/a", "Medium", "see audit"),
(2523, d(2005,9,19), "US", "Diplomatic talks (six-party joint statement)", "North Korea", "The six-party talks end with a joint statement in which North Korea pledges to give up its nuclear weapons and programs (Al Jazeera, NPR)", None, "n/a", "Medium", "see audit"),
(2524, d(2005,10,21), "US (Treasury)", "Sanction (eight entities, E.O. 13382)", "Eight North Korean entities", "Treasury freezes the assets of eight North Korean entities as WMD proliferators under E.O. 13382", None, "n/a", "Medium", "see audit"),
(2525, d(2006,7,5), "North Korea", "Missile launch (seven missiles, Taepodong-2 failed)", "Sea of Japan", "North Korea launches seven missiles, including a long-range Taepodong-2 that fails (CNN). NPR's chronology lists the launch for July 5", None, "No damage reported", "Medium", "see audit"),
(2526, d(2006,7,15), "UN Security Council (US voted yes)", "Diplomatic resolution (UN Resolution 1695)", "North Korea", "The Security Council adopts Resolution 1695, which condemns the July launches and calls on North Korea to suspend its ballistic missile program (UN press release)", 2525, "n/a", "Medium", "see audit"),
(2527, d(2006,10,9), "North Korea", "Nuclear test (first)", "Punggye-ri test site", "North Korea announces and carries out its first nuclear test. President Bush calls it a provocative act and says the world will respond", None, "No injuries reported", "Medium", "see audit"),
(2528, d(2006,10,14), "UN Security Council (US voted yes)", "Diplomatic resolution (UN Resolution 1718)", "North Korea", "The Security Council adopts Resolution 1718 after the nuclear test: sanctions on arms and luxury goods and an asset freeze and travel ban on named persons", 2527, "n/a", "Medium", "see audit"),
(2529, d(2007,2,13), "US", "Diplomatic talks (six-party draft accord)", "North Korea", "The six-party talks end with a draft accord on North Korea's nuclear program (NPR). The page has no time stamp; dated by its URL", None, "n/a", "Medium", "see audit"),
(2530, d(2008,6,26), "US", "Diplomatic step (Trading with the Enemy Act lifted; terror-list rescission notified)", "North Korea", "President Bush ends the application of the Trading with the Enemy Act to North Korea and tells Congress he will rescind North Korea's state sponsor of terrorism designation", None, "n/a", "Medium", "see audit"),
(2531, d(2008,10,11), "US", "Diplomatic step (removed from the terror list)", "North Korea", "The US removes North Korea from its list of state sponsors of terrorism on Saturday, Oct 11 (CNN)", None, "n/a", "Medium", "see audit"),
(2532, d(2009,4,5), "North Korea", "Missile launch (long-range rocket; North Korea says satellite)", "Pacific Ocean, over Japan", "North Korea launches a long-range rocket. The White House statement and CNN report the launch; North Korea says it was a satellite launch", None, "No damage reported", "Medium", "see audit"),
(2533, d(2009,5,25), "North Korea", "Nuclear test (second)", "Punggye-ri test site", "North Korea carries out a second nuclear test; world leaders condemn it (PBS NewsHour)", None, "No injuries reported", "Medium", "see audit"),
(2534, d(2009,6,12), "UN Security Council (US voted yes)", "Diplomatic resolution (UN Resolution 1874)", "North Korea", "The Security Council adopts Resolution 1874 after the second test: a wider arms embargo and cargo inspections", 2533, "n/a", "Medium", "see audit"),
(2535, d(2009,8,4), "US (former President Clinton)", "Diplomatic visit (Clinton in Pyongyang; two journalists freed)", "North Korea", "Former President Bill Clinton flies to Pyongyang and brings home two American journalists held there (PBS NewsHour). A private trip, not a US government move", None, "n/a", "Medium", "see audit"),
(2536, d(2009,12,8), "US", "Diplomatic talks (envoy Stephen Bosworth in Pyongyang)", "North Korea", "US envoy Stephen Bosworth holds talks in Pyongyang as the US tries to restart the nuclear talks (NPR)", None, "n/a", "Medium", "see audit"),
(2537, d(2010,3,26), "North Korea (blamed by Seoul's investigation)", "Provocation (South Korean corvette Cheonan sunk)", "ROKS Cheonan, Yellow Sea", "The South Korean warship Cheonan is sunk near Baengnyeong Island. A South Korean-led investigation, announced May 20, says a North Korean torpedo did it. Logged on the date of the sinking", None, "46 South Korean sailors killed", "Medium", "see audit"),
(2538, d(2010,7,25), "US (with South Korea)", "Joint drills (Invincible Spirit)", "Korean Peninsula", "US and South Korean forces start the Invincible Spirit exercise; Stars and Stripes says both sides are trying to strike the right tone after the Cheonan sinking", None, "n/a", "Medium", "see audit"),
(2539, d(2010,8,30), "US (White House)", "Sanction (E.O. 13551)", "North Korean officials and entities", "President Obama signs E.O. 13551 blocking the property of certain persons with respect to North Korea", None, "n/a", "Medium", "see audit"),
(2540, d(2010,11,23), "North Korea", "Provocation (artillery attack on Yeonpyeong island)", "Yeonpyeong island, South Korea", "North Korea shells Yeonpyeong island; the island's residents recount the attack and two more bodies are found (AP)", None, "4 killed and 18 wounded", "Medium", "see audit"),
(2541, d(2010,11,28), "US (with South Korea)", "Joint drills (USS George Washington, Yellow Sea)", "Yellow Sea", "The carrier USS George Washington joins South Korean ships for drills in the Yellow Sea, five days after the Yeonpyeong shelling (NBC)", 2540, "n/a", "Medium", "see audit"),
(2542, d(2012,2,29), "US and North Korea", "Diplomatic talks (Leap Day deal: test halt, food aid)", "North Korea", "After talks, North Korea agrees to halt nuclear tests and the US agrees to provide food aid (NPR)", None, "n/a", "Medium", "see audit"),
(2543, d(2012,4,13), "North Korea", "Missile launch (long-range rocket, failed)", "Yellow Sea", "North Korea's long-range rocket launch fails. The White House says the US will not give food aid after the launch (CBS, AP)", None, "No damage reported", "Medium", "see audit"),
(2544, d(2012,12,12), "North Korea", "Missile launch (long-range rocket)", "Pacific Ocean", "North Korea launches a long-range rocket; the UN and many governments condemn it (NPR, CNN)", None, "No damage reported", "Medium", "see audit"),
(2546, d(2013,2,12), "North Korea", "Nuclear test (third)", "Punggye-ri test site", "North Korea carries out a third nuclear test; the White House calls it highly provocative (NBC)", None, "No injuries reported", "Medium", "see audit"),
(2547, d(2013,3,7), "UN Security Council (US voted yes)", "Diplomatic resolution (UN Resolution 2094)", "North Korea", "The Security Council adopts Resolution 2094 after the third nuclear test, adding new sanctions", 2546, "n/a", "Medium", "see audit"),
(2548, d(2013,3,15), "US", "Missile defense (14 more interceptors)", "Alaska and California", "The Pentagon says it will add 14 more ground-based missile interceptors to meet the North Korean threat (CBS, AP)", None, "n/a", "Medium", "see audit"),
(2549, d(2013,3,28), "US", "Force posture (B-2 stealth bomber flights)", "Korean Peninsula", "US B-2 stealth bombers fly practice missions over South Korea (NPR, Air Force Global Strike Command)", None, "n/a", "Medium", "see audit"),
(2550, d(2013,4,3), "North Korea", "Provocation (Kaesong industrial zone closed to South Korean workers)", "Kaesong industrial zone", "North Korea bars South Korean workers from the Kaesong industrial zone (NPR)", 2549, "Work stopped at the joint zone; no injuries reported", "Medium", "see audit"),
(2551, d(2013,4,3), "US", "Missile defense (THAAD to Guam)", "Guam", "The US sends a THAAD missile defense battery to Guam. NPR frames it as a response to North Korean threats and reports it on the same day as the Kaesong ban", 2550, "n/a", "Medium", "see audit"),
(2552, d(2014,12,19), "North Korea (per FBI)", "Provocation (cyber attack on Sony Pictures)", "Sony Pictures Entertainment", "The FBI says North Korea is behind the Sony Pictures cyber attack; President Obama vows a response (Al Jazeera, NPR)", None, "Company systems and data hit; no physical harm reported", "Medium", "see audit"),
(2553, d(2015,1,2), "US (Treasury)", "Sanction (Sony-linked designations)", "North Korean officials and entities", "Treasury sanctions North Korean officials and entities after the Sony attack", 2552, "n/a", "Medium", "see audit"),
(2554, d(2015,8,17), "US (with South Korea)", "Joint drills (Ulchi Freedom Guardian)", "Korean Peninsula", "The annual US-South Korea Ulchi Freedom Guardian exercise starts despite North Korean protests (Stars and Stripes)", None, "n/a", "Medium", "see audit"),
(2555, d(2015,8,20), "North Korea", "Provocation (artillery exchange across the border)", "Border with South Korea", "North and South Korea trade fire across the border (NPR). On Aug 4, two South Korean soldiers were wounded by mines", 2554, "Aug 4 mines wounded 2 ROK soldiers; no casualties reported for Aug 20", "Medium", "see audit"),
(2556, d(2016,1,6), "North Korea", "Nuclear test (fourth)", "Punggye-ri test site", "North Korea claims a successful hydrogen bomb test (ABC)", None, "No injuries reported", "Medium", "see audit"),
(2557, d(2016,1,10), "US", "Force posture (B-52 flies over South Korea)", "Osan air base, South Korea", "A US B-52 bomber flies over South Korea in a show of force after the nuclear test (NPR)", 2556, "n/a", "Medium", "see audit"),
(2558, d(2016,2,7), "North Korea", "Missile launch (long-range rocket; North Korea says satellite)", "Pacific Ocean", "North Korea launches a long-range rocket from Dongchang-ri (AP, CBS). North Korea says it was a satellite launch", None, "No damage reported", "Medium", "see audit"),
(2559, d(2016,2,18), "US", "Sanction (North Korea Sanctions and Policy Enhancement Act)", "North Korea", "The US enacts the North Korea Sanctions and Policy Enhancement Act (AP)", 2558, "n/a", "Medium", "see audit"),
(2560, d(2016,3,2), "UN Security Council (US voted yes)", "Diplomatic resolution (UN Resolution 2270)", "North Korea", "The Security Council adopts Resolution 2270; President Obama welcomes it in a White House statement", 2558, "n/a", "Medium", "see audit"),
(2561, d(2016,3,7), "US (with South Korea)", "Joint drills (Key Resolve and Foal Eagle)", "Korean Peninsula", "Key Resolve (Mar 7-18) and Foal Eagle start; about 17,000 US troops take part (US Forces Korea)", None, "n/a", "Medium", "see audit"),
(2562, d(2016,3,10), "North Korea", "Missile launch (two Scud ballistic missiles)", "Sea of Japan", "Two Scud missiles are fired and fly about 300 miles (CBS timeline, citing the BBC). US date in the timeline", 2561, "No damage reported", "Medium", "see audit"),
(2563, d(2016,3,16), "US (White House)", "Sanction (E.O. 13722)", "North Korean government and Workers' Party of Korea", "President Obama signs E.O. 13722 blocking the property of the North Korean government and the Workers' Party (message to Congress dated Mar 15)", None, "n/a", "Medium", "see audit"),
(2564, d(2016,3,18), "North Korea", "Missile launch (two Nodong ballistic missiles)", "Sea of Japan", "Two mid-range Nodong ballistic missiles are fired and fly about 500 miles (CBS timeline, citing South Korea's Joint Chiefs)", 2563, "No damage reported", "Medium", "see audit"),
(2565, d(2016,7,6), "US (Treasury)", "Sanction (Kim Jong Un named)", "Kim Jong Un and other officials", "The US sanctions Kim Jong Un for the first time, over human rights abuses (AP)", None, "n/a", "Medium", "see audit"),
(2566, d(2016,7,8), "US (with South Korea)", "Missile defense (agreement to deploy THAAD)", "South Korea", "The US and South Korea agree to deploy a THAAD missile defense battery in South Korea (Defense News, US Forces Korea)", None, "n/a", "Medium", "see audit"),
(2567, d(2016,7,9), "North Korea", "Missile launch (submarine-launched ballistic missile)", "East Sea", "A submarine-launched ballistic missile is fired off the east coast; Seoul says it appeared to explode at about 10 km (CBS timeline). US date in the timeline", 2565, "No damage reported", "Medium", "see audit"),
(2568, d(2016,9,9), "North Korea", "Nuclear test (fifth)", "Punggye-ri test site", "North Korea carries out its fifth and biggest nuclear test; it draws global outrage (PBS NewsHour)", None, "No injuries reported", "Medium", "see audit"),
(2569, d(2016,9,13), "US (with South Korea)", "Force posture (B-1B flyover)", "South Korea", "Two US B-1B bombers fly over South Korea in a show of force against North Korea (ABC)", 2568, "n/a", "Medium", "see audit"),
(2570, d(2016,11,30), "UN Security Council (US voted yes)", "Diplomatic resolution (UN Resolution 2321)", "North Korea", "The Security Council adopts Resolution 2321 after the September test, tightening sanctions including on coal exports (UN News)", 2568, "n/a", "Medium", "see audit"),
(2571, d(2017,2,12), "North Korea", "Missile launch (Pukguksong-2 ballistic missile)", "East Sea (Sea of Japan)", "North Korea fires an intermediate-range Polaris-2 (KN-15) ballistic missile into the East Sea, its first launch of 2017", None, "No damage reported", "Medium", "see audit"),
(2572, d(2017,3,6), "North Korea", "Missile launch (four Scud-ER ballistic missiles)", "Sea of Japan", "North Korea fires four extended-range Scud ballistic missiles toward Japan. US THAAD parts reach Osan the same evening (The War Zone); that move is not logged on its own", None, "No damage reported", "Medium", "see audit"),
(2573, d(2017,4,8), "US", "Force posture (carrier strike group ordered toward Korea)", "Korean Peninsula", "Admiral Harris orders the USS Carl Vinson strike group toward Korea; on Apr 15 it was still about 3,500 miles away (USNI, Defense News)", None, "n/a", "Medium", "see audit"),
(2574, d(2017,4,16), "North Korea", "Missile launch (Hwasong-12 ballistic missile, failed)", "Sinpo", "A Hwasong-12 ballistic missile launch fails very early (CBS timeline)", None, "No damage reported", "Medium", "see audit"),
(2575, d(2017,5,14), "North Korea", "Missile launch (Hwasong-12 ballistic missile)", "Sea of Japan", "North Korea launches a Hwasong-12 ballistic missile that flies about 400 miles; it CLAIMS it could carry a nuclear warhead (NPR, CBS timeline)", None, "No damage reported", "Medium", "see audit"),
(2576, d(2017,5,21), "North Korea", "Missile launch (medium-range ballistic missile)", "East Sea", "North Korea fires a medium-range ballistic missile in what AFP calls a fresh test (AFP, CBS timeline)", None, "No damage reported", "Medium", "see audit"),
(2578, d(2017,6,13), "US (State Department)", "Diplomatic release (Otto Warmbier freed)", "Otto Warmbier", "Secretary of State Tillerson announces that North Korea has freed American student Otto Warmbier, held since January 2016 and sentenced to 15 years of hard labor. His father says he is in a coma", None, "Warmbier in a coma, per his father", "Medium", "see audit"),
(2579, d(2017,6,29), "US (Treasury)", "Sanction (Bank of Dandong, Section 311; shipping and individuals)", "Bank of Dandong, Dalian Global Unity Shipping", "Treasury proposes to cut the Bank of Dandong off from the US financial system under Section 311 and designates Dalian Global Unity Shipping and two Chinese individuals", None, "n/a", "Medium", "see audit"),
(2580, d(2017,7,4), "North Korea (claimed)", "Missile launch (ICBM, Hwasong-14)", "East Sea", "North Korea CLAIMS its first successful ICBM test, the Hwasong-14 (Al Jazeera, CBS timeline)", 2579, "No damage reported", "Medium", "see audit"),
(2581, d(2017,7,28), "North Korea", "Missile launch (second ICBM)", "Sea of Japan", "North Korea fires a second ICBM that flies longer and higher than the first; it says the whole US is in range (AP, CBS timeline)", None, "No damage reported", "Medium", "see audit"),
(2582, d(2017,7,30), "US (with South Korea)", "Force posture (B-1B flyover)", "Korean Peninsula", "US B-1B bombers fly over South Korea two days after the second ICBM test (AP)", 2581, "n/a", "Medium", "see audit"),
(2583, d(2017,8,5), "UN Security Council (US voted yes)", "Diplomatic resolution (UN Resolution 2371)", "North Korea", "The Security Council adopts Resolution 2371 after the two ICBM tests, banning more North Korean exports", 2581, "n/a", "Medium", "see audit"),
(2584, d(2017,8,21), "US (with South Korea)", "Joint drills (Ulchi Freedom Guardian)", "Korean Peninsula", "The annual US-South Korea drills start and run 11 days (Al Jazeera)", None, "n/a", "Medium", "see audit"),
(2585, d(2017,8,22), "US (Treasury)", "Sanction (Chinese and Russian firms and individuals)", "Chinese and Russian entities", "Treasury sanctions Chinese and Russian companies and individuals over North Korea (Al Jazeera)", None, "n/a", "Medium", "see audit"),
(2586, d(2017,8,25), "North Korea", "Missile launch (three short-range missiles)", "East Sea", "North Korea launches three unidentified short-range missiles within 30 minutes; one likely exploded soon after take-off (CBS timeline)", 2584, "No damage reported", "Medium", "see audit"),
(2587, d(2017,8,29), "North Korea", "Missile launch (Hwasong-12 ballistic missile over Japan)", "Pacific Ocean, over Hokkaido", "A Hwasong-12 ballistic missile flies over Hokkaido, Japan; South Korea says it flew 1,677 miles to a height of 341 miles. Dated Aug 29 by Japan and Seoul; the CBS timeline lists it as Aug 28 (US date)", None, "No damage reported", "Medium", "see audit"),
]

# ---------------------------------------------------------------------------------------------
_CBS_TL = _s('North Korea missile tests: a timeline', 'CBS News', '2017-09-06', 'https://www.cbsnews.com/amp/news/north-korea-missile-tests-a-timeline', 'full text')
_NPR_CHRON = _s("Chronology of North Korea's Missile Program", 'NPR', '2006-07-05', 'https://www.npr.org/2006/07/05/5534639/chronology-of-north-koreas-missile-program', 'full text')
_UCSB = 'https://www.presidency.ucsb.edu/'

SOURCES = {
 2500: [_s('Letter dated 12 March 1993 from the Permanent Representative of the DPRK to the UN (S/25407)', 'UN (Digital Library record)', '1993-03-12', 'https://digitallibrary.un.org/record/164463', 'full text'),
        _s('Letters dated 12 and 19 March 1993 (Security Council Repertoire)', 'UN (Security Council Repertoire)', '1993-03-12', 'https://www.un.org/french/docs/cs/repertoire/93-95/CHAPTER 8/ASIA/15 - Letters dated 12 and 19 March 93.pdf', 'full text')],
 2501: [_s('Statement on the Nuclear Nonproliferation Talks With North Korea', 'White House (via American Presidency Project)', '1993-06-11', _UCSB + 'documents/statement-nuclear-nonproliferation-talks-with-north-korea', 'full text')],
 2502: [_s('State Department statement: Geneva talks Mar 21; Team Spirit suspended (USIA text)', 'State Department (via GlobalSecurity.org; USIA text)', '1994-03-03', 'https://www.globalsecurity.org/wmd/library/news/dprk/1994/940303-dprk-usia.htm', 'full text')],
 2503: [_s('Remarks and an Exchange With Reporters on North Korea', 'White House (via American Presidency Project)', '1994-06-22', _UCSB + 'documents/remarks-and-exchange-with-reporters-north-korea', 'full text')],
 2504: [_s("President's Statement on North Korea", 'White House (archived)', '1994-10-18', 'https://clintonwhitehouse6.archives.gov/1994/10/1994-10-18-presidents-statement-on-north-korea.html', 'full text')],
 2505: [_s('President statement on helicopter downing in Korea', 'White House (archived)', '1994-12-19', 'https://clintonwhitehouse6.archives.gov/1994/12/1994-12-19-president-statement-on-helicopter-downing-in-korea.html', 'full text'),
        _s('U.S. demands return of 2 helicopter pilots', 'The New York Times (News Service, via Deseret News)', '1994-12-18', 'https://www.deseret.com/1994/12/18/19148441/u-s-demands-return-of-2-helicopter-pilots/', 'full text')],
 2506: [_s("The President's News Conference With President Kim Yong-sam of South Korea in Cheju", 'White House (via American Presidency Project)', '1996-04-16', _UCSB + 'documents/the-presidents-news-conference-with-president-kim-yong-sam-south-korea-cheju', 'full text')],
 2507: [_NPR_CHRON],
 2508: [_s('Press briefing on easing sanctions on North Korea', 'White House (via American Presidency Project)', '1999-09-17', _UCSB + 'node/271181', 'full text'), _NPR_CHRON],
 2509: [_s('US-DPRK Joint Communique (Washington File EPF407)', 'State Department (via usinfo.org; Washington File)', '2000-10-12', 'https://usinfo.org/wf-archive/2000/001012/epf407.htm', 'full text')],
 2510: [_s('Albright Ends Historic N. Korea Visit', 'ABC News', '2000-10-24', 'https://abcnews.go.com/International/story?id=82290', 'full text')],
 2511: [_s('Statement on the Completion of the North Korea Policy Review', 'White House (via American Presidency Project)', '2001-06-06', _UCSB + 'documents/statement-completion-the-north-korea-policy-review', 'full text')],
 2512: [_s('Address Before a Joint Session of the Congress on the State of the Union', 'White House (via American Presidency Project)', '2002-01-29', _UCSB + 'documents/address-before-joint-session-the-congress-the-state-the-union-22', 'full text')],
 2513: [_s('North Korea acknowledges nuclear program (NewsHour)', 'PBS NewsHour', '2002-10-17', 'https://www.pbs.org/newshour/politics/asia-july-dec02-north-korea_10-17', 'full text'),
        _s('CNN transcript, Oct 17, 2002', 'CNN', '2002-10-17', 'https://www.cnn.com/TRANSCRIPTS/0210/17/lt.08.html', 'full text')],
 2514: [_s('KEDO Executive Board statement, November 14, 2002', 'KEDO (official press release)', '2002-11-14', 'https://kedo.org/news_detail.asp?NewsID=23', 'full text')],
 2515: [_s('N. Korea to expel U.N. inspectors', 'CBS News', '2002-12-27', 'https://www.cbsnews.com/news/n-korea-to-expel-un-inspectors', 'full text'),
        _s('CNN transcript, Dec 27, 2002', 'CNN', '2002-12-27', 'https://www.cnn.com/TRANSCRIPTS/0212/27/ltm.01.html', 'full text')],
 2516: [_s('N. Korea pulls out of global nuclear treaty', 'NPR', '2003-01-10', 'https://www.npr.org/2003/01/10/912158/n-korea-pulls-out-of-global-nuclear-treaty', 'full text')],
 2517: [_s('N. Korean MiGs intercepted U.S. plane', 'CBS News', '2003-03-04', 'https://www.cbsnews.com/news/n-korean-migs-intercepted-us-plane/', 'full text'),
        _s('North Korea intercepts Air Force aircraft', 'DoD (US Air Force article)', '2003-03-04', 'https://www.af.mil/News/Article-Display/Article/139911/north-korea-intercepts-air-force-aircraft/', 'full text')],
 2518: [_s('U.S. deploys bombers to deter N. Korea', 'NPR', '2003-03-05', 'https://www.npr.org/2003/03/05/1183341/u-s-deploys-bombers-to-deter-n-korea', 'full text'),
        _s('CNN transcript, Mar 5, 2003', 'CNN', '2003-03-05', 'https://www.cnn.com/TRANSCRIPTS/0303/05/ltm.07.html', 'full text')],
 2519: [_s('North Korea (NewsHour)', 'PBS NewsHour', '2003-03-11', 'https://www.pbs.org/newshour/politics/asia-jan-june03-north-korea_03-11', 'full text')],
 2520: [_s('North Korea (NewsHour), six-party talks', 'PBS NewsHour', '2003-08-27', 'https://www.pbs.org/newshour/world/asia-july-dec03-north-korea_08-27', 'full text')],
 2521: [_s('North Korea claims nuclear weapons', 'Al Jazeera', '2005-02-10', 'https://www.aljazeera.com/news/2005/2/10/north-korea-claims-nuclear-weapons', 'full text')],
 2522: [_s('Treasury Designates Banco Delta Asia as Primary Money Laundering Concern under USA PATRIOT Act', 'Treasury/OFAC (official release)', '2005-09-15', 'https://home.treasury.gov/news/press-releases/js2720', 'full text')],
 2523: [_s('Deal struck in North Korean talks', 'Al Jazeera', '2005-09-19', 'https://www.aljazeera.com/news/2005/9/19/deal-struck-in-north-korean-talks', 'full text'),
        _s('North Korea pledges to abandon nuclear arms work', 'NPR', '2005-09-19', 'https://www.npr.org/2005/09/19/4854535/north-korea-pledges-to-abandon-nuclear-arms-work', 'full text')],
 2524: [_s('Treasury Targets North Korean Entities for Supporting WMD Proliferation', 'Treasury/OFAC (official release)', '2005-10-21', 'https://home.treasury.gov/news/press-releases/js2984', 'full text')],
 2525: [_s('CNN transcript, Jul 5, 2006', 'CNN', '2006-07-05', 'https://www.cnn.com/TRANSCRIPTS/0607/05/ltm.08.html', 'full text'), _NPR_CHRON],
 2526: [_s('Security Council condemns Democratic People\'s Republic of Korea\'s missile launches (Resolution 1695)', 'UN (Security Council press release)', '2006-07-15', 'https://press.un.org/en/2006/sc8778.doc.htm', 'full text'),
        _s('Resolution 1695 (2006), UN Digital Library record', 'UN (Digital Library record)', '2006-07-15', 'https://digitallibrary.un.org/record/578923', 'full text')],
 2527: [_s('President Bush Statement on North Korea Nuclear Test', 'White House (archived)', '2006-10-09', 'https://georgewbush-whitehouse.archives.gov/news/releases/2006/10/20061009.html', 'full text'),
        _s('Bush denounces N. Korea test as provocative act', 'NPR (via KAXE)', '2006-10-09', 'https://www.kaxe.org/news/2006-10-09/bush-denounces-n-korea-test-as-provocative-act', 'full text')],
 2528: [_s('Security Council imposes sanctions on DPRK (Resolution 1718)', 'UN (Security Council press release)', '2006-10-14', 'https://press.un.org/en/2006/sc8853.doc.htm', 'full text'),
        _s('Resolution 1718 (2006), UN Digital Library record', 'UN (Digital Library record)', '2006-10-14', 'https://digitallibrary.un.org/record/584729', 'full text')],
 2529: [_s('North Korea nuclear talks yield draft accord', 'NPR', '2007-02-13', 'https://www.npr.org/2007/02/13/7379431/north-korea-nuclear-talks-yield-draft-accord', 'full text')],
 2530: [_s('Fact sheet / message on North Korea: Trading with the Enemy Act and state sponsor of terrorism (June 26, 2008)', 'White House (archived)', '2008-06-26', 'https://georgewbush-whitehouse.archives.gov/news/releases/2008/06/20080626-9.html', 'full text')],
 2531: [_s('U.S. removes North Korea from terror list', 'CNN', '2008-10-11', 'https://edition.cnn.com/2008/WORLD/asiapcf/10/11/us.north.korea/other2.html', 'full text')],
 2532: [_s('Statement by the President on North Korea launch', 'White House (archived)', '2009-04-05', 'https://obamawhitehouse.archives.gov/the-press-office/statement-president-north-korea-launch', 'full text'),
        _s('CNN transcript, Apr 5, 2009', 'CNN', '2009-04-05', 'https://www.cnn.com/TRANSCRIPTS/0904/05/sm.01.html', 'full text')],
 2533: [_s("News of North Korea's nuclear test stuns world leaders", 'PBS NewsHour', '2009-05-25', 'https://www.pbs.org/newshour/show/news-of-north-koreas-nuclear-test-stuns-world-leaders', 'full text')],
 2534: [_s('Security Council condemns DPRK nuclear test, adopts Resolution 1874', 'UN (Security Council press release)', '2009-06-12', 'https://press.un.org/en/2009/sc9679.doc.htm', 'full text')],
 2535: [_s('Clinton frees two journalists in North Korea (NewsHour)', 'PBS NewsHour', '2009-08-04', 'https://www.pbs.org/newshour/politics/asia-july-dec09-clintonkorea_08-04', 'full text')],
 2536: [_s('U.S. attempts to restart North Korean nuclear talks', 'NPR', '2009-12-09', 'https://www.npr.org/2009/12/09/121255806/u-s-attempts-to-restart-north-korean-nuclear-talks', 'full text')],
 2537: [_s('Seoul: N Korean torpedo sank ship', 'Al Jazeera', '2010-05-20', 'https://www.aljazeera.com/news/2010/5/20/seoul-n-korean-torpedo-sank-ship', 'full text'),
        _s('Thursday: South Korea accuses North of sinking ship', 'PBS NewsHour', '2010-05-20', 'https://www.pbs.org/newshour/nation/thursday-south-korea-accuses-north-of-sinking-ship-oil-reaches-marshlands', 'snippet')],
 2538: [_s('U.S., S. Korea aim to strike the right tone as exercise kicks off', 'Stars and Stripes', '2010-07-25', 'https://www.stripes.com/theaters/asia_pacific/2010-07-25/u.s.,-s.-korea-aim-to-strike-the-right-tone-as-exercise-kicks-off-1902739.html', 'full text')],
 2539: [_s('Executive Order: Blocking Property of Certain Persons with Respect to North Korea', 'White House (archived)', '2010-08-30', 'https://obamawhitehouse.archives.gov/the-press-office/2010/08/30/executive-order-president-blocking-property-certain-persons-with-respect', 'full text')],
 2540: [_s('S. Koreans recount attack, 2 more bodies found', 'AP (via CBS News)', '2010-11-24', 'https://www.cbsnews.com/news/s-koreans-recount-attack-2-more-bodies-found', 'full text')],
 2541: [_s('US, South Korea drills in the Yellow Sea (NBC News)', 'NBC News', '2010-11-28', 'https://www.nbcnews.com/id/wbna40390864', 'full text')],
 2542: [_s('N. Korea to halt nuclear tests; U.S. to provide aid', 'NPR', '2012-02-29', 'https://www.npr.org/2012/02/29/147654942/n-korea-to-halt-nuclear-tests-u-s-to-provide-aid', 'full text')],
 2543: [_s('White House: No food aid for North Korea', 'AP (via CBS News)', '2012-04-13', 'https://www.cbsnews.com/news/white-house-no-food-aid-for-north-korea', 'full text')],
 2544: [_s('North Korea rocket launch', 'CNN', '2012-12-12', 'https://edition.cnn.com/2012/12/11/world/asia/north-korea-rocket-launch', 'full text'),
        _s("Global chorus of condemnation after North Korea's rocket launch", 'NPR (via KUNC)', '2012-12-12', 'https://www.kunc.org/npr-news/2012-12-12/global-chorus-of-condemnation-after-north-koreas-rocket-launch', 'full text')],
 2546: [_s('White House: North Korea nuclear test highly provocative', 'NBC News', '2013-02-12', 'https://www.nbcnews.com/news/world/white-house-north-korea-nuclear-test-highly-provocative-flna1c8335073', 'full text')],
 2547: [_s('Resolution 2094 (2013), UN Digital Library record', 'UN (Digital Library record)', '2013-03-07', 'https://digitallibrary.un.org/record/745263', 'full text')],
 2548: [_s('US ramping up missile defense to meet North Korea threat', 'AP (via CBS News)', '2013-03-15', 'https://www.cbsnews.com/news/us-ramping-up-missile-defense-to-meet-north-korea-threat', 'full text')],
 2549: [_s('U.S. flies B-2 stealth bombers over South Korea amid escalating tensions with the North', 'NPR (via Public Radio East)', '2013-03-28', 'https://www.publicradioeast.org/world/2013-03-28/u-s-flies-b-2-stealth-bombers-over-south-korea-amid-escalating-tensions-with-the-north', 'snippet'),
        _s('U.S. B-2 bombers conduct extended deterrence mission to the Republic of Korea', 'DoD (Air Force Global Strike Command)', '2013-03-28', 'https://www.afgsc.af.mil/News/Article-Display/Article/454647/us-b-2-bombers-conduct-extended-deterrence-mission-to-the-republic-of-korea/', 'snippet')],
 2550: [_s('Responding to North Korea, U.S. sends missile defenses to Guam', 'NPR', '2013-04-03', 'https://www.npr.org/sections/thetwo-way/2013/04/03/176160859/responding-to-north-korea-u-s-sends-missile-defenses-to-guam', 'full text')],
 2551: [_s('Responding to North Korea, U.S. sends missile defenses to Guam', 'NPR', '2013-04-03', 'https://www.npr.org/sections/thetwo-way/2013/04/03/176160859/responding-to-north-korea-u-s-sends-missile-defenses-to-guam', 'full text')],
 2552: [_s('Obama vows response to N Korea cyber-attack', 'Al Jazeera', '2014-12-19', 'https://www.aljazeera.com/amp/news/2014/12/19/obama-vows-response-to-n-korea-cyber-attack', 'full text'),
        _s('FBI officially pins Sony cyberattack on North Korea', 'NPR (via Public Radio East)', '2014-12-19', 'https://www.publicradioeast.org/us/2014-12-19/fbi-officially-pins-sony-cyberattack-on-north-korea', 'full text')],
 2553: [_s('Treasury Imposes Sanctions Against the Government of North Korea (Sony)', 'Treasury/OFAC (official release)', '2015-01-02', 'https://home.treasury.gov/news/press-releases/jl9733', 'full text')],
 2554: [_s('US, South Korea ignore North Korea\'s protests, launch war games', 'Stars and Stripes', '2015-08-17', 'https://www.stripes.com/news/2015-08-17/us-south-korea-ignore-north-koreas-protests-launch-war-games-1804473.html', 'full text')],
 2555: [_s('North and South Korea trade shots', 'NPR (via NHPR)', '2015-08-20', 'https://www.nhpr.org/2015-08-20/north-and-south-korea-trade-shots', 'full text')],
 2556: [_s('N. Korea claims successful hydrogen bomb test', 'ABC News (via ABC13)', '2016-01-06', 'https://abc13.com/post/n-korea-claims-successful-hydrogen-bomb-test/1147964/', 'full text')],
 2557: [_s('US flies bomber over South Korea in show of force', 'NPR (via KPBS)', '2016-01-10', 'https://www.kpbs.org/news/2016/01/10/us-flies-bomber-over-south-korea-in-show-of', 'full text')],
 2558: [_s('North Korea rocket launch, United Nations', 'AP (via ABC7)', '2016-02-07', 'https://abc7.com/north-korea-missile-rocket-launch-united-nations/1189986/', 'full text')],
 2559: [_s('North Korea sanctions act', 'AP (via ABC11)', '2016-02-18', 'https://abc11.com/news/1206064', 'full text')],
 2560: [_s('Statement by the President on United Nations Security Council Resolution 2270', 'White House (archived)', '2016-03-02', 'https://obamawhitehouse.archives.gov/the-press-office/2016/03/02/statement-president-united-nations-security-council-resolution-2270', 'full text')],
 2561: [_s('CFC announces start of Key Resolve and Foal Eagle 2016', 'DoD (US Forces Korea press release)', '2016-03-06', 'https://www.usfk.mil/Media/Press-Products/Press-Releases/Article/686836/cfc-announces-start-of-key-resolve-and-foal-eagle-2016/', 'full text')],
 2562: [_CBS_TL],
 2563: [_s('Message to Congress: Blocking Property of the Government of North Korea and the Workers\' Party of Korea', 'White House (archived)', '2016-03-16', 'https://obamawhitehouse.archives.gov/the-press-office/2016/03/16/message-blocking-property-government-north-korea-and-workers-party-korea', 'full text')],
 2564: [_CBS_TL],
 2565: [_s('U.S. imposes sanctions on North Korean leader Kim Jong Un for the first time', 'AP (via PBS NewsHour)', '2016-07-06', 'https://www.pbs.org/newshour/world/u-s-imposes-sanctions-on-north-korean-leader-kim-jong-un-for-the-first-time', 'full text')],
 2566: [_s('THAAD to officially deploy to South Korea', 'Defense News', '2016-07-08', 'https://www.defensenews.com/home/2016/07/08/thaad-to-officially-deploy-to-south-korea/', 'full text'),
        _s('ROK-US Alliance agrees to deploy THAAD', 'DoD (US Forces Korea press release)', '2016-07-08', 'https://www.usfk.mil/Media/Press-Products/Press-Releases/Article/831166/rok-us-alliance-agrees-to-deploy-thaad/', 'full text')],
 2567: [_CBS_TL],
 2568: [_s("North Korea's fifth and biggest nuclear test draws global outrage", 'PBS NewsHour', '2016-09-09', 'https://www.pbs.org/newshour/world/north-koreas-fifth-and-biggest-nuclear-test-draws-global-outrage', 'full text')],
 2569: [_s('US flies bombers in show of force against North Korea', 'ABC News (via ABC30)', '2016-09-13', 'https://abc30.com/news/us-flies-bombers-in-show-of-force-against-north-korea/1509603/', 'full text')],
 2570: [_s('Security Council tightens sanctions on North Korea (Resolution 2321)', 'UN (UN News)', '2016-11-30', 'https://news.un.org/en/story/2016/11/546622', 'full text')],
 2571: [_s('North Korea missile launch', 'CNN', '2017-02-12', 'https://edition.cnn.com/2017/02/11/asia/north-korea-missile', 'full text'), _CBS_TL],
 2572: [_s('After North Korean missiles fly, THAAD missile defense suddenly arrives', 'The War Zone', '2017-03-06', 'https://www.twz.com/8134/after-north-korean-missiles-fly-thaad-missile-defense-suddenly-arrives', 'full text'), _CBS_TL],
 2573: [_s('SECDEF Mattis: No specific demand signal prompted Vinson carrier strike group move', 'USNI News', '2017-04-11', 'https://news.usni.org/2017/04/11/secdef-mattis-no-specific-demand-signal-prompted-vinson-carrier-strike-group-move', 'full text'),
        _s('Nothing to see here: US carrier still thousands of miles from Korea', 'Defense News', '2017-04-17', 'https://www.defensenews.com/naval/2017/04/17/nothing-to-see-here-us-carrier-still-thousands-of-miles-from-korea/', 'full text')],
 2574: [_CBS_TL],
 2575: [_s('North Korea celebrates test of new long-range missile', 'NPR (via WGBH)', '2017-05-15', 'https://www.wgbh.org/news/2017-05-15/north-korea-celebrates-test-of-new-long-range-missile', 'full text'), _CBS_TL],
 2576: [_s('North Korea fires medium-range ballistic missile in fresh test', 'AFP (via Times of Israel)', '2017-05-21', 'https://www.timesofisrael.com/north-korea-fires-medium-range-ballistic-missile-in-fresh-test/', 'full text'), _CBS_TL],
 2578: [_s('Otto Warmbier has been released from a North Korean prison', 'NPR', '2017-06-13', 'https://www.npr.org/sections/thetwo-way/2017/06/13/532755522/otto-warmbier-has-been-released-from-a-north-korean-prison', 'full text')],
 2579: [_s('Treasury Acts to Increase Pressure on North Korea (Bank of Dandong)', 'Treasury/OFAC (official release)', '2017-06-29', 'https://home.treasury.gov/news/press-releases/sm0118', 'full text')],
 2580: [_s('North Korea claims test of intercontinental missile', 'Al Jazeera', '2017-07-05', 'https://www.aljazeera.com/amp/news/2017/7/5/north-korea-claims-test-of-intercontinental-missile', 'full text'), _CBS_TL],
 2581: [_s('North Korea says 2nd ICBM test puts entire US in range', 'AP (via KTVU)', '2017-07-29', 'https://www.ktvu.com/news/north-korea-says-2nd-icbm-test-puts-entire-us-in-range', 'full text'), _CBS_TL],
 2582: [_s("US bombers fly over South Korea after North's 2nd ICBM test", 'AP (via KTVU)', '2017-07-30', 'https://www.ktvu.com/news/us-bombers-fly-over-south-korea-after-norths-2nd-icbm-test', 'full text')],
 2583: [_s('Security Council strengthens sanctions on DPRK (Resolution 2371)', 'UN (Security Council press release)', '2017-08-05', 'https://press.un.org/en/2017/sc12945.doc.htm', 'full text')],
 2584: [_s("US, S Korea drills begin amid tensions with N Korea", 'Al Jazeera', '2017-08-21', 'https://www.aljazeera.com/news/2017/8/21/us-s-korea-drills-begin-amid-tensions-with-n-korea', 'full text')],
 2585: [_s('US sanctions target Chinese, Russians over North Korea', 'Al Jazeera', '2017-08-22', 'https://www.aljazeera.com/news/2017/8/22/us-sanctions-target-chinese-russians-over-north-korea', 'full text')],
 2586: [_CBS_TL],
 2587: [_s('North Korea missile launch over Japan (live updates)', 'AP (via CBS News)', '2017-08-29', 'https://www.cbsnews.com/amp/news/north-korea-missile-launch-over-japan-live-updating', 'full text'),
        _s('Japan is on high alert after North Korea missile launch', 'NPR (via WFAE)', '2017-08-29', 'https://www.wfae.org/world/2017-08-29/japan-is-on-high-alert-after-north-korea-missile-launch', 'full text')],
}
VERDICT = {k: 'confirmed' for k in SOURCES}
# Rows where an allowed outlet confirms the event but not every detail in the row (date inferred, mirror, US-date timeline).
#   2502: text read on a GlobalSecurity.org mirror of the USIA release.   2505: date set from "Saturday" in a Dec 18 report.
#   2510: dated by the day the report says the visit ended.             2513: dated by the US announcement.
#   2519: day set from the weekday in the PBS report.                   2537: the blame rests on Seoul's own investigation.
#   2549: both pages seen only as search results.                        2562, 2564, 2567, 2574, 2586: one US-date timeline.
PARTLY = {2502, 2505, 2510, 2513, 2519, 2537, 2549, 2562, 2564, 2567, 2574, 2586}

# Which option letter each US move belongs to (B talks, C sanctions, D joint drills, E interdiction,
# F missile defense, G strategic assets, H other posture). A (hold) is not tagged.
US_OPTION = {
 2501: 'B', 2502: 'B', 2503: 'B', 2504: 'B', 2506: 'B', 2508: 'B', 2509: 'B', 2510: 'B', 2511: 'B',
 2518: 'G', 2520: 'B', 2522: 'C', 2523: 'B', 2524: 'C', 2529: 'B', 2530: 'B', 2531: 'B', 2536: 'B',
 2538: 'D', 2539: 'C', 2541: 'D', 2542: 'B', 2548: 'F', 2549: 'G', 2551: 'F', 2553: 'C', 2554: 'D',
 2557: 'G', 2559: 'C', 2561: 'D', 2563: 'C', 2565: 'C', 2566: 'F', 2569: 'G', 2573: 'G', 2579: 'C',
 2582: 'G', 2584: 'D', 2585: 'C',
}

# CRED_ESTIMATE: filled in below by cred_estimate(); see the function.
def cred_estimate():
    """My own estimate of the engine's credibility score (full-text allowed outlet 0.80, two outlets 0.96, 'Partly' x0.8,
    independent outlet not on the list 0.60; KEDO and other official pages 0.80). For spot checks only."""
    out = {}
    for eid, srcs in SOURCES.items():
        best = {}
        for s in srcs:
            outlet = s['outlet'].split(' (')[0].strip()
            w = 0.60 if outlet.startswith('Los Angeles') else 0.80
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

# Trigger Census rows: one per US move (reply window: 7 days, a North Korean launch / test / provocation).
# Category = what the move was: Economic/Blockade (sanctions), Military/Property (drills, deployments, missile defense,
# posture), Political/Diplomatic (talks). Status: R-strong (North Korea itself ties the act to the move), R-weak (act within
# 7 days, link plausible), N (no North Korean act found in the 7 days), Unclear, Unverified (window not searched).
# No row here is R-strong: no North Korean statement tying an act to a US move was read for these years.
_NPR_NOTE = "NPR's missile chronology has no launch entry in the window; it is not a full list (it omits the Feb-Mar 2003 cruise missiles) and other provocations were not searched."
_CBS_NOTE = "The CBS launch timeline lists no launch in the window; artillery, cyber acts and statements were not searched."
CENSUS = [
 (2501, "Political/Diplomatic", "Unverified", "New York talks, Jun 11, 1993. Jun 12-18, 1993 was not searched."),
 (2502, "Political/Diplomatic", "Unverified", "Geneva round set and Team Spirit suspended, Mar 3, 1994. Mar 4-10, 1994 was not searched."),
 (2503, "Political/Diplomatic", "Unverified", "Clinton on the freeze and Geneva talks, Jun 22, 1994. Jun 23-29, 1994 was not searched."),
 (2504, "Political/Diplomatic", "Unverified", "Agreed Framework text settled, Oct 18, 1994. Oct 19-25, 1994 was not searched."),
 (2506, "Political/Diplomatic", "Unverified", "Four-party talks proposal, Apr 16, 1996. Apr 17-23, 1996 was not searched."),
 (2508, "Political/Diplomatic", "N", "Sanctions eased after the Berlin talks, Sep 17, 1999. " + _NPR_NOTE + " North Korea had pledged on Sep 13 to freeze long-range tests."),
 (2509, "Political/Diplomatic", "N", "Joint communique, Oct 12, 2000. " + _NPR_NOTE),
 (2510, "Political/Diplomatic", "N", "Albright visit ends, Oct 24, 2000. " + _NPR_NOTE),
 (2511, "Political/Diplomatic", "N", "Bush policy review and offer to talk, Jun 6, 2001. " + _NPR_NOTE),
 (2518, "Military/Property", "R-weak", "24 bombers sent to Guam Mar 5, 2003 -> short-range anti-ship cruise missile Mar 10, day 5 (PBS). The Pentagon said the move was planned long before and the intercept of Mar 2 came first, so the link is plausible only."),
 (2520, "Political/Diplomatic", "N", "First six-party round, Aug 27, 2003. " + _NPR_NOTE),
 (2522, "Economic/Blockade", "N", "Banco Delta Asia named a Section 311 concern, Sep 15, 2005. " + _NPR_NOTE + " The May 2005 short-range launch is outside the window."),
 (2523, "Political/Diplomatic", "N", "Six-party joint statement, Sep 19, 2005. " + _NPR_NOTE),
 (2524, "Economic/Blockade", "N", "Treasury freezes eight entities, Oct 21, 2005. " + _NPR_NOTE),
 (2529, "Political/Diplomatic", "Unverified", "Six-party draft accord, Feb 13, 2007. Feb 14-20, 2007 was not searched."),
 (2530, "Political/Diplomatic", "Unverified", "Trading with the Enemy Act lifted, Jun 26, 2008. Jun 27-Jul 3, 2008 was not searched."),
 (2531, "Political/Diplomatic", "Unverified", "Removed from the terror list, Oct 11, 2008. Oct 12-18, 2008 was not searched."),
 (2536, "Political/Diplomatic", "Unverified", "Bosworth in Pyongyang, Dec 8, 2009. Dec 9-15, 2009 was not searched."),
 (2538, "Military/Property", "Unverified", "Invincible Spirit starts Jul 25, 2010. Jul 26-Aug 1, 2010 was not searched."),
 (2539, "Economic/Blockade", "Unverified", "E.O. 13551, Aug 30, 2010. Aug 31-Sep 6, 2010 was not searched."),
 (2541, "Military/Property", "Unverified", "George Washington drills, Nov 28, 2010, five days after the Yeonpyeong shelling (a US reply to North Korea). Nov 29-Dec 5, 2010 was not searched."),
 (2542, "Political/Diplomatic", "Unverified", "Leap Day deal, Feb 29, 2012. Mar 1-7, 2012 was not searched."),
 (2548, "Military/Property", "Unverified", "14 more interceptors announced Mar 15, 2013. Mar 16-22, 2013 was not searched."),
 (2549, "Military/Property", "R-weak", "B-2 flights Mar 28, 2013 -> North Korea closes Kaesong to South Korean workers Apr 3, day 6 (NPR). NPR does not call the closing a reply."),
 (2551, "Military/Property", "Unclear", "THAAD to Guam, Apr 3, 2013, the same day as the Kaesong ban (#2550). NPR frames the US move as a response to North Korean threats, so the order cannot be separated. Context only."),
 (2553, "Economic/Blockade", "Unverified", "Sony-linked sanctions, Jan 2, 2015, a reply to the Dec 19 attribution. Jan 3-9, 2015 was not searched."),
 (2554, "Military/Property", "R-weak", "Ulchi Freedom Guardian starts Aug 17, 2015 -> artillery exchange across the border Aug 20, day 3 (NPR). Stars and Stripes says North Korea protested the drills; the Aug 4 mines came earlier."),
 (2557, "Military/Property", "N", "B-52 flyover, Jan 10, 2016. The next launch in the CBS timeline is Feb 7, day 28; the Jan 6 test came before. " + _CBS_NOTE),
 (2559, "Economic/Blockade", "N", "North Korea sanctions act, Feb 18, 2016. The next launch in the CBS timeline is Mar 10, day 21. " + _CBS_NOTE),
 (2561, "Military/Property", "R-weak", "Key Resolve and Foal Eagle start Mar 7, 2016 -> two Scud missiles Mar 10, day 3 (CBS timeline, US date). The timeline does not link the launch to the drills."),
 (2563, "Economic/Blockade", "R-weak", "E.O. 13722 signed Mar 15-16, 2016 -> two Nodong missiles Mar 18, day 2 (CBS timeline). The launch fell inside Key Resolve; link to the order is weak."),
 (2565, "Economic/Blockade", "R-weak", "Kim Jong Un sanctioned Jul 6, 2016 -> submarine-launched ballistic missile Jul 9, day 3 (CBS timeline, US date). The launch is also close to the THAAD decision (#2566)."),
 (2566, "Military/Property", "R-weak", "THAAD deployment agreed Jul 8, 2016 -> submarine-launched ballistic missile Jul 9, day 1 (CBS timeline, US date). Link plausible only; the same launch follows the Jul 6 sanctions."),
 (2569, "Military/Property", "Unverified", "B-1B flyover, Sep 13, 2016, four days after the fifth test. Sep 14-20, 2016 was not searched beyond the launch timeline, which lists no launch in the window; an engine test around Sep 19-20 could not be confirmed in an allowed outlet."),
 (2573, "Military/Property", "N", "Carrier group ordered toward Korea Apr 8, 2017. The next launch in the CBS timeline is Apr 16, day 8. " + _CBS_NOTE),
 (2579, "Economic/Blockade", "R-weak", "Bank of Dandong action Jun 29, 2017 -> ICBM Jul 4, day 5 (Al Jazeera, CBS timeline). North Korea had been preparing the launch; no page ties it to the sanctions."),
 (2582, "Military/Property", "N", "B-1B flyover Jul 30, 2017, after the second ICBM. The next launch in the CBS timeline is Aug 25, day 26. " + _CBS_NOTE),
 (2584, "Military/Property", "R-weak", "Ulchi Freedom Guardian starts Aug 21, 2017 -> three short-range missiles Aug 25, day 4 (CBS timeline)."),
 (2585, "Economic/Blockade", "R-weak", "Treasury sanctions on Chinese and Russian firms Aug 22, 2017 -> three short-range missiles Aug 25, day 3 (CBS timeline)."),
]

# Reply pairs (pair id, trigger, reply, category, reply caused casualties Y/N, note). Each reply is within 7 days of its trigger.
PAIRS = [
 (2500, 2518, 2519, "Military/Property", "N", "Short-range anti-ship cruise missile five days after the US sent 24 bombers to Guam; the Pentagon said the move was planned long before"),
 (2501, 2549, 2550, "Military/Property", "N", "Kaesong closed to South Korean workers six days after the B-2 flights"),
 (2502, 2554, 2555, "Military/Property", "N", "Artillery exchange across the border three days after Ulchi Freedom Guardian started"),
 (2503, 2561, 2562, "Military/Property", "N", "Two Scud missiles three days after Key Resolve and Foal Eagle started (US date in the source)"),
 (2504, 2563, 2564, "Military/Property", "N", "Two Nodong missiles two days after E.O. 13722 (link weak)"),
 (2505, 2565, 2567, "Military/Property", "N", "Submarine-launched ballistic missile three days after Kim Jong Un was sanctioned (US date in the source)"),
 (2506, 2566, 2567, "Military/Property", "N", "Same launch, a day after the THAAD deployment was agreed (link plausible only)"),
 (2507, 2579, 2580, "Military/Property", "N", "First ICBM test five days after the Bank of Dandong action (no page ties them)"),
 (2508, 2584, 2586, "Military/Property", "N", "Three short-range missiles four days after Ulchi Freedom Guardian started"),
 (2509, 2585, 2586, "Military/Property", "N", "Same launch, three days after the sanctions on Chinese and Russian firms"),
]

# No continuous-fighting windows here: the log shows no North Korean pace dense enough to need one before Aug 2017.
WINDOWS = []
START_ACTS = set()

# Phases (oldest first)
PHASES = [
 ("NPT crisis and the Agreed Framework", d(1993, 3, 1), d(1995, 12, 31), "NPT notice (#2500), New York talks (#2501), Geneva talks and the Agreed Framework (#2502-#2504), helicopter shot down (#2505)"),
 ("Framework years, Taepodong and Albright", d(1996, 1, 1), d(2001, 12, 31), "Four-party proposal (#2506), Taepodong-1 (#2507), sanctions eased (#2508), joint communique and Albright visit (#2509-#2510), Bush review (#2511)"),
 ("Axis of evil and the uranium crisis", d(2002, 1, 1), d(2004, 12, 31), "Axis of evil (#2512), uranium admission (#2513), KEDO halt (#2514), inspectors out and NPT exit (#2515-#2516), bombers to Guam (#2518), six-party talks (#2520)"),
 ("Six-party talks and first tests", d(2005, 1, 1), d(2009, 12, 31), "Weapons claim (#2521), Banco Delta Asia (#2522), joint statement (#2523), 2006 missiles and first test (#2525-#2528), delisting (#2531), second test (#2533-#2534)"),
 ("Cheonan, Yeonpyeong and the Kim Jong Un years", d(2010, 1, 1), d(2015, 12, 31), "Cheonan (#2537), Yeonpyeong (#2540), rocket launches (#2543-#2544), third test (#2546), Kaesong (#2550), Sony (#2552), 2015 border clash (#2555)"),
 ("Fourth to sixth test run-up", d(2016, 1, 1), d(2017, 8, 30), "Fourth and fifth tests (#2556, #2568), 2016 launches (#2562-#2567), THAAD (#2566), 2017 missiles (#2571-#2587), Warmbier (#2578)"),
]

CHAIN_NAMES = {
 2518: "Bombers to Guam -> cruise missile Mar 10, 2003",
 2540: "Yeonpyeong shelling -> USS George Washington drills",
 2549: "B-2 flights -> Kaesong closed -> THAAD to Guam",
 2552: "Sony attack -> Treasury sanctions",
 2554: "Ulchi Freedom Guardian 2015 -> border artillery exchange",
 2556: "Fourth nuclear test -> B-52 flyover",
 2561: "Key Resolve 2016 -> Scud launch Mar 10",
 2563: "E.O. 13722 -> Nodong launch Mar 18, 2016",
 2565: "Kim Jong Un sanctions and THAAD decision -> SLBM Jul 9, 2016",
 2568: "Fifth nuclear test -> B-1B flyover",
 2579: "Bank of Dandong action -> first ICBM test",
 2581: "Second ICBM -> B-1B flyover",
 2584: "Ulchi Freedom Guardian 2017 and Treasury sanctions -> missiles Aug 25",
}
