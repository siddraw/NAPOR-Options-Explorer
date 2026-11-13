# Tags most likely to be wrong

For Sidd. 2026-11-12. **No tag was changed.** There are 303 tagged cases across the five theaters; these 32 are the ones most likely to be wrong. They come from rows whose note (`why`) says it was a judgment call, a guess or "kept because", and from rows where the tag does not fit the event's own title (who acts, where, open or covert, move, target). Most doubtful first. Each row ends with a yes or no question: answer it, and I will change the tag or leave it.

How to read a row: the tags are the six settings the page uses (Type of move, Target, Location, Scale, Who acts, Open or covert), in plain words from `napor/action_tags.py`. Tags describe what the US did, never what followed.

## 1. China / Taiwan #3545 (2016-12-02, option F)

- **Title:** NPR reports it as likely the first such call between a US president or president-elect and a Taiwanese leader since 1979. Foreign Minister Wang Yi calls it 'just a small trick by Taiwan'
- **Current tags:** Move: Official visit or high-level contact; Target: No target; Location: No physical place (e.g. sanctions, talks, statements); Scale: One action; Who: The US alone; Open: Announced or claimed by the US
- **Note in the tag file:** Call with Taiwan's president by a president-elect.
- **Why it is uncertain:** The call was made by a president-elect, who was not yet in the US government. The tag treats it as a US action. This is the same kind of doubt as the Israeli-actions rule.
- **Question for Sidd:** Was a president-elect's call a US government action? (tagged: a US contact with Taiwan)

## 2. China / Taiwan #3037 (2023-08-12, option F)

- **Title:** Taiwan Vice President Lai Ching-te stops in New York and San Francisco (Aug 16, per an AP photo caption) on trips to and from Paraguay; US officials greet him. The Aug 12 New York date is inferred: the pages read give no New York arrival date (an AP photo caption shows him in New York on Aug 14)
- **Current tags:** Move: Official visit or high-level contact; Target: No target; Location: No physical place (e.g. sanctions, talks, statements); Scale: One action; Who: The US alone; Open: Announced or claimed by the US
- **Note in the tag file:** Transit stop by Taiwan's vice president in the US.
- **Why it is uncertain:** The one who acts is Taiwan's vice president, passing through the US. The log's only US link is that US officials greet him. It was kept (see napor/non_us_actors.py) but it is a stretch.
- **Question for Sidd:** Is a Taiwan official's stopover, with US officials greeting him, a US move? (tagged: US contact, alone)

## 3. Iran #43 (2026-06-08, option B)

- **Title:** Iran agrees to halt attacks on Israel after the two traded fire on Jun 6-7, the first exchange since the April ceasefire
- **Current tags:** Move: Talks, negotiation, deal or ceasefire; Target: No target; Location: No physical place (e.g. sanctions, talks, statements); Scale: One action; Who: The US alone; Open: Announced or claimed by the US
- **Note in the tag file:** Iran agrees to halt attacks on Israel; US role not detailed
- **Why it is uncertain:** The title is about Iran and Israel. The log does not say the US asked for, mediated or announced this halt, and the tag note says "US role not detailed". Also listed in napor/non_us_actors.py REVIEW.
- **Question for Sidd:** Did the US play a part in this halt (asked for it, mediated it or announced it)? (tagged: talks, US alone)

## 4. China / Taiwan #3031 (2023-04-05, option F)

- **Title:** House Speaker Kevin McCarthy meets President Tsai Ing-wen at the Reagan Library in California; China's foreign ministry had said it would 'take resolute measures'
- **Current tags:** Move: Official visit or high-level contact; Target: No target; Location: No physical place (e.g. sanctions, talks, statements); Scale: One action; Who: The US alone; Open: Announced or claimed by the US
- **Note in the tag file:** Meeting with Taiwan's president held in California.
- **Why it is uncertain:** The actor is the Speaker of the House (Congress), not the executive branch. The tag treats it as a US move.
- **Question for Sidd:** Does a meeting by the House Speaker count as a US move? (tagged: visit, US alone). Same question for Pelosi's trip (#3025).

## 5. Venezuela / Caribbean #4020 (2025-09-05, option E)

- **Title:** Reuters, from two sources, reports the US is moving 10 F-35 fighters to a Puerto Rico airfield for operations against designated narco-terrorist groups; expected in the southern Caribbean by late the following week
- **Current tags:** Move: Deploy forces or weapons (incl. missile defense, bombers, carriers); Target: No target; Location: A third country (an ally's or neighbor's territory); Scale: One action; Who: The US alone; Open: Unclaimed or covert
- **Note in the tag file:** F-35s to Puerto Rico known from sources; Puerto Rico counted as third
- **Why it is uncertain:** Puerto Rico is US territory, but the tag says "third country (an ally's or neighbor's territory)". Known only from two Reuters sources.
- **Question for Sidd:** Should Puerto Rico count as a third country? (tagged: a third country)

## 6. Houthis / Red Sea #1058 (2015-03-25, option H)

- **Title:** The White House says President Obama authorized logistical and intelligence support for the Gulf-led operation and that the US is setting up a Joint Planning Cell with Saudi Arabia (about a dozen US personnel at the start). US forces take no direct military action
- **Current tags:** Move: Deploy forces or weapons (incl. missile defense, bombers, carriers); Target: No target; Location: A third country (an ally's or neighbor's territory); Scale: One action; Who: Through partners (local forces, other states acting for the US); Open: Announced or claimed by the US
- **Note in the tag file:** Planning cell and support for the Saudi-led campaign; no direct US action, so tagged as acting through a partner
- **Why it is uncertain:** The US gave support and set up a planning cell but "takes no direct military action". It is tagged as deploying forces, acting through a partner. A planning cell and intelligence is not clearly a deployment.
- **Question for Sidd:** Is setting up a planning cell and giving support a deployment of forces? (tagged: deploy forces, through partners)

## 7. Venezuela / Caribbean #4061 (2026-06-12, option F)

- **Title:** Trump announces a 'swift and lethal kinetic' strike killed Tren de Aragua leader Hector Guerrero Flores; Hegseth says it happened earlier in the week and cites a 'shared U.S. and Venezuelan commitment' to fight narco-terrorists. Venezuela's communications ministry did not respond (NPR)
- **Current tags:** Move: Air, missile or drone strike; Target: Leaders or commanders, Military equipment and sites (radars, launchers, bases); Location: Inside the adversary's country; Scale: One action; Who: The US alone; Open: Announced or claimed by the US
- **Note in the tag file:** Hegseth cited a shared US-Venezuelan commitment; tagged US alone because the US struck
- **Why it is uncertain:** Hegseth cited a "shared US and Venezuelan commitment" and Venezuela did not respond. The tag says the US struck alone.
- **Question for Sidd:** Was this strike joint with Venezuela? (tagged: the US alone)

## 8. Iran #104 (2026-10-11, option D)

- **Title:** CENTCOM releases footage of a fighter jet bombing the stern of a cargo ship it says was running the blockade of Iranian ports, disabling it (strike Oct 10 or 11)
- **Current tags:** Move: Air, missile or drone strike; Target: Commercial shipping or tankers; Location: At sea or in international airspace; Scale: One action; Who: The US alone; Open: Announced or claimed by the US
- **Note in the tag file:** jet disables cargo ship running the blockade; listed under naval but a strike
- **Why it is uncertain:** The case sits in the naval option (D) but is tagged as a strike, because a jet bombed a ship. The same note is on #152. The choice decides which "strike" and "naval" requests find it.
- **Question for Sidd:** Is a jet bombing a ship's stern a strike rather than a naval action? (tagged: strike). Same question for #152.

## 9. Iran #40 (2026-05-04, option F)

- **Title:** Operation Project Freedom: announced May 3, began May 4; Navy escort mission for stranded ships; US says six boats sunk (Trump said seven); pause announced May 5 US time (May 6 Gulf time)
- **Current tags:** Move: Naval action (blockade, boarding, seizure, transit, escort, interdiction); Target: Small boats, Commercial shipping or tankers; Location: At sea or in international airspace; Scale: A campaign over several days or a series; Who: The US alone; Open: Announced or claimed by the US
- **Note in the tag file:** escort operation (listed option says strike) with boats sunk; kept as naval
- **Why it is uncertain:** Project Freedom is an escort mission in which boats were sunk. It sits in the strike option (F) but is tagged as a naval action. Its target tag has both small boats and shipping.
- **Question for Sidd:** Is this escort mission a naval action rather than a strike? (tagged: naval action, a campaign)

## 10. Iran #221 (2020-08-14, option D)

- **Title:** US seizes four Iranian fuel cargoes bound for Venezuela
- **Current tags:** Move: Naval action (blockade, boarding, seizure, transit, escort, interdiction); Target: Oil, banks, companies or the economy, Commercial shipping or tankers; Location: At sea or in international airspace; Scale: One action; Who: The US alone; Open: Announced or claimed by the US
- **Note in the tag file:** seized fuel cargoes; location not stated, tagged sea
- **Why it is uncertain:** The title does not say where the seizure happened, and the tag says "sea". A seizure of cargoes may have been a legal step, not a boarding at sea.
- **Question for Sidd:** Were the fuel cargoes seized at sea? (tagged: naval action, at sea)

## 11. North Korea #2068 (2026-08-17, option D)

- **Title:** Just before the exercise started on Monday, Trump ordered the Pentagon to 'substantially reduce' it, citing his relationship with Kim; PBS/AP says it was cut roughly in half. (AP via KLTV says it ended Aug 27, six days early; the two sources differ on the end date)
- **Current tags:** Move: Military exercise or drill; Target: No target; Location: A third country (an ally's or neighbor's territory); Scale: A campaign over several days or a series; Who: With Israel or other allies; Open: Announced or claimed by the US
- **Note in the tag file:** Scaled-down drill.
- **Why it is uncertain:** Trump ordered the exercise to be cut about in half. It is tagged as a military drill, but the US action was to reduce one.
- **Question for Sidd:** Is cutting a drill in half a drill (rather than a reduction of forces)? (tagged: military exercise or drill)

## 12. Venezuela / Caribbean #4024 (2025-10-15, option H)

- **Title:** Trump confirms he authorized the CIA to conduct covert operations inside Venezuela, including possible strikes on cartels; declines to say whether the CIA can act against Maduro; says the administration is 'looking at land'. AP: at least five boats destroyed since early September, 27 killed
- **Current tags:** Move: Other; Target: No target; Location: Inside the adversary's country; Scale: One action; Who: The US alone; Open: Announced or claimed by the US
- **Note in the tag file:** CIA covert action authorization, confirmed by Trump; aimed inside Venezuela
- **Why it is uncertain:** Trump confirmed a CIA covert-action order in public. The tag says announced, but the action itself is covert. The move is tagged "other".
- **Question for Sidd:** Was this move announced rather than covert? (tagged: announced or claimed by the US)

## 13. Iran #28 (2026-04-07, option B)

- **Title:** Trump announces a two-week ceasefire on Truth Social after Pakistan's PM Sharif asks him to extend his deadline; Iran's Supreme National Security Council accepts (Reuters, AP). Apr 7 US time / Apr 8 Gulf time
- **Current tags:** Move: Talks, negotiation, deal or ceasefire; Target: No target; Location: No physical place (e.g. sanctions, talks, statements); Scale: One action; Who: The US alone; Open: Announced or claimed by the US
- **Note in the tag file:** ceasefire announced on Truth Social after Pakistani request
- **Why it is uncertain:** Pakistan asked Trump to extend his deadline and Pakistani channels were used, but the tag says the US alone. Similar cases (#19, #86, #129) are tagged "through partners".
- **Question for Sidd:** Did Pakistan act for the US here, so it counts as through partners? (tagged: the US alone)

## 14. Iran #232 (2023-08-10, option B)

- **Title:** US and Iran agree a prisoner swap that releases about $6 billion in frozen Iranian funds (completed Sep 18)
- **Current tags:** Move: Talks, negotiation, deal or ceasefire; Target: No target; Location: No physical place (e.g. sanctions, talks, statements); Scale: One action; Who: The US alone; Open: Announced or claimed by the US
- **Note in the tag file:** prisoner swap with frozen funds; Qatar helped
- **Why it is uncertain:** Qatar helped with the prisoner swap. The tag says the US alone, but other cases with a mediator (#86, #129) are tagged through partners.
- **Question for Sidd:** Did Qatar act for the US here, so it counts as through partners? (tagged: the US alone)

## 15. Houthis / Red Sea #1007 (2021-02-04, option B)

- **Title:** President Biden ends US support for the Saudi-led offensive, calls for a ceasefire and names Timothy Lenderking special envoy for Yemen
- **Current tags:** Move: Talks, negotiation, deal or ceasefire; Target: No target; Location: No physical place (e.g. sanctions, talks, statements); Scale: One action; Who: The US alone; Open: Announced or claimed by the US
- **Note in the tag file:** Policy change plus an envoy; no target
- **Why it is uncertain:** Biden ended support for a Saudi offensive, called for a ceasefire and named an envoy. The tag says talks, but ending support is also a policy or arms step.
- **Question for Sidd:** Is ending support for an offensive plus an envoy "talks"? (tagged: talks, negotiation, deal or ceasefire)

## 16. Iran #244 (2024-04-18, option C)

- **Title:** US and UK sanction Iran's drone program after the attack on Israel
- **Current tags:** Move: Sanctions or export controls; Target: Nuclear or missile programs; Location: No physical place (e.g. sanctions, talks, statements); Scale: One action; Who: With Israel or other allies; Open: Announced or claimed by the US
- **Note in the tag file:** joint with UK per source; drone program
- **Why it is uncertain:** The title says "drone program". The target list has only "nuclear or missile programs", so drones were put there.
- **Question for Sidd:** Is a drone program a "nuclear or missile program"? (tagged: nuclear or missile programs)

## 17. Iran #225 (2022-08-24, option F)

- **Title:** US strikes bunkers in Deir ez-Zor used by militias backed by the IRGC; the US later says 4 militia members were killed
- **Current tags:** Move: Air, missile or drone strike; Target: Military equipment and sites (radars, launchers, bases), Military personnel or fighters, A proxy or partner group of the adversary; Location: A proxy's territory; Scale: One action; Who: The US alone; Open: Announced or claimed by the US
- **Note in the tag file:** bunkers; listed as equipment strike but personnel risk
- **Why it is uncertain:** The title says bunkers used by militias. The tag adds fighters as a target, and the later note that four fighters were killed may have influenced it. Tags are meant to describe what the US did, not what followed.
- **Question for Sidd:** Was the strike aimed at fighters as well as bunkers? (tagged: equipment, fighters, proxy)

## 18. Iran #74 (2026-09-01, option G)

- **Title:** Kuhestak/Sirik wedding strike, part of the same wave as #73
- **Current tags:** Move: Air, missile or drone strike; Target: Military equipment and sites (radars, launchers, bases), Military personnel or fighters; Location: Inside the adversary's country; Scale: One action; Who: The US alone; Open: Announced or claimed by the US
- **Note in the tag file:** wedding strike, part of a wave; tagged single
- **Why it is uncertain:** The title is only "wedding strike, part of the same wave as #73" and does not say what was hit. The tag says military equipment and fighters, which is not in the title.
- **Question for Sidd:** Was this strike aimed at military equipment and fighters? (tagged: equipment, personnel)

## 19. China / Taiwan #3532 (2013-11-25, option H)

- **Title:** Two unarmed B-52s from Guam spend under an hour in the zone China declared on Nov 23, with no notice to China. The Pentagon calls it a long-planned training sortie and says China did not react
- **Current tags:** Move: Deploy forces or weapons (incl. missile defense, bombers, carriers); Target: No target; Location: At sea or in international airspace; Scale: One action; Who: The US alone; Open: Announced or claimed by the US
- **Note in the tag file:** Bomber flight through an air defense zone, counted as deployment.
- **Why it is uncertain:** Two B-52s flew through China's declared air defense zone. The tag says deploy forces, but it was a one-hour flight, not a deployment. It could be read as a show of force.
- **Question for Sidd:** Is a one-hour bomber flight a deployment? (tagged: deploy forces or weapons)

## 20. Iran #120 (2026-10-21, option H)

- **Title:** State orders non-emergency staff and families out of Saudi Arabia (Oct 21), citing Houthi attacks, and on Oct 23 cuts staff at embassies in Jordan, Lebanon, Qatar and the UAE; US officials say the military is quietly reducing its footprint at Middle East posts, partly over direct threats from Iran
- **Current tags:** Move: Withdraw or reduce forces; Target: No target; Location: A third country (an ally's or neighbor's territory); Scale: One action; Who: The US alone; Open: Announced or claimed by the US
- **Note in the tag file:** State order was public, military cuts described as quiet; tagged announced
- **Why it is uncertain:** The State order to staff was public, but the military cuts were "quiet". The tag says announced.
- **Question for Sidd:** Was this reduction announced rather than quiet? (tagged: announced or claimed by the US)

## 21. Venezuela / Caribbean #4028 (2025-10-26, option E)

- **Title:** Destroyer USS Gravely arrives with Marines for planned joint exercises with Trinidad and Tobago's defence force; Trinidad says such exercises are regular
- **Current tags:** Move: Military exercise or drill; Target: No target; Location: A third country (an ally's or neighbor's territory); Scale: One action; Who: With Israel or other allies; Open: Announced or claimed by the US
- **Note in the tag file:** Port visit with joint exercises with Trinidad and Tobago
- **Why it is uncertain:** A destroyer arrived with Marines for joint exercises. It is in the deployment option (E) but tagged as a military exercise, with a third country as the place.
- **Question for Sidd:** Is this a drill rather than a deployment? (tagged: military exercise or drill, a third country)

## 22. China / Taiwan #3516 (2001-04-11, option B)

- **Title:** The US says it is 'very sorry' for the presumed death of the pilot and that its plane landed without permission, but accepts no blame for the collision. China frees the crew on humanitarian grounds; the plane is left for a meeting on Apr 18
- **Current tags:** Move: Talks, negotiation, deal or ceasefire; Target: No target; Location: No physical place (e.g. sanctions, talks, statements); Scale: One action; Who: The US alone; Open: Announced or claimed by the US
- **Note in the tag file:** Letter of regret to secure release of the EP-3 crew.
- **Why it is uncertain:** A "very sorry" letter to win the crew's release. Tagged as talks. It could also be a statement.
- **Question for Sidd:** Is a letter of regret to free a crew "talks" rather than a statement? (tagged: talks, negotiation, deal or ceasefire)

## 23. China / Taiwan #3500 (1995-05-22, option F)

- **Title:** President Clinton agrees to let Lee Teng-hui visit his alma mater (Cornell) in a private visit. Beijing protests strongly. CRS lists China postponing its defense minister's US visit on May 26 and withdrawing its ambassador on Jun 16
- **Current tags:** Move: Official visit or high-level contact; Target: No target; Location: No physical place (e.g. sanctions, talks, statements); Scale: One action; Who: The US alone; Open: Announced or claimed by the US
- **Note in the tag file:** Visa for Taiwan's president to visit the US.
- **Why it is uncertain:** The US agreed to let Taiwan's president visit (a visa). It is tagged as a visit, but the US did not visit anyone.
- **Question for Sidd:** Is allowing a visit a "visit" move? (tagged: visit or call)

## 24. North Korea #2508 (1999-09-17, option B)

- **Title:** After talks in Berlin on Sep 7-12, the White House says the US is easing sanctions on North Korea. On Sep 13 North Korea pledged to freeze long-range missile tests while talks go on. Logged on the briefing date
- **Current tags:** Move: Talks, negotiation, deal or ceasefire; Target: No target; Location: No physical place (e.g. sanctions, talks, statements); Scale: One action; Who: The US alone; Open: Announced or claimed by the US
- **Note in the tag file:** Sanctions easing is part of the talks outcome; tagged as talks.
- **Why it is uncertain:** Easing sanctions is part of talks, but the tag says talks. In other cases easing sanctions is tagged sanctions.
- **Question for Sidd:** Should easing sanctions be tagged sanctions rather than talks? (tagged: talks)

## 25. North Korea #2010 (2019-05-09, option E)

- **Title:** The Justice Department announces the US has seized the Wise Honest for illegally shipping North Korean coal and delivering heavy machinery to the North. The announcement came hours after the DPRK launch (2009); the ship itself had been held since 2018, so the timing is not a US reply
- **Current tags:** Move: Naval action (blockade, boarding, seizure, transit, escort, interdiction); Target: Commercial shipping or tankers; Location: No physical place (e.g. sanctions, talks, statements); Scale: One action; Who: The US alone; Open: Announced or claimed by the US
- **Note in the tag file:** Announcement of a ship seizure held since 2018; place not stated, so none.
- **Why it is uncertain:** A ship seizure announced by the Justice Department. It is tagged naval action with no place, but the seizure was a legal step and the ship had been held since 2018.
- **Question for Sidd:** Is this a naval action rather than a legal step? (tagged: naval action, no place)

## 26. Iran #336 (2006-05-31, option B)

- **Title:** Secretary of State Rice says the US will join Britain, France and Germany at the table if Iran fully and verifiably suspends enrichment, and warns of stronger sanctions if it does not
- **Current tags:** Move: Talks, negotiation, deal or ceasefire; Target: No target; Location: No physical place (e.g. sanctions, talks, statements); Scale: One action; Who: With Israel or other allies; Open: Announced or claimed by the US
- **Note in the tag file:** offer to join talks plus a warning; tagged talks; joint with UK, France, Germany
- **Why it is uncertain:** Rice made an offer to join talks plus a warning. It is tagged talks, and "with allies" because Britain, France and Germany are named.
- **Question for Sidd:** Is an offer to join talks, with a warning, "talks" rather than a statement? (tagged: talks, with allies)

## 27. Houthis / Red Sea #1319 (2025-05-06, option B)

- **Title:** Trump says the US will stop bombing the Houthis 'effective immediately'; Oman says neither side will target the other, including US ships, in the Red Sea and Bab al-Mandab; the State Dept says it does not cover the Israel-Houthi conflict; US stand-down ordered May 5
- **Current tags:** Move: Talks, negotiation, deal or ceasefire; Target: No target; Location: No physical place (e.g. sanctions, talks, statements); Scale: One action; Who: The US alone; Open: Announced or claimed by the US
- **Why it is uncertain:** Trump said the US would stop bombing; Oman said the deal covered both sides. The tag says the US alone and has no note.
- **Question for Sidd:** Did Oman act for the US here, so it counts as through partners? (tagged: the US alone)

## 28. Venezuela / Caribbean #4513 (2006-02-03, option H)

- **Title:** The State Department declares her persona non grata and gives her 72 hours to leave. Spokesman Sean McCormack: 'we were forced to respond' to the expulsion of the attache
- **Current tags:** Move: Other; Target: Named officials or individuals; Location: No physical place (e.g. sanctions, talks, statements); Scale: One action; Who: The US alone; Open: Announced or claimed by the US
- **Note in the tag file:** Expulsion or visa step against diplomats; fits no listed move, so other
- **Why it is uncertain:** Expelling diplomats or taking away a visa fits no move on the list, so it is tagged "other". The same question applies to #4523, #4533 and #4541.
- **Question for Sidd:** Should expelling a diplomat be tagged "other" (not a legal step)? (tagged: other)

## 29. China / Taiwan #3040 (2024-04-07, option G)

- **Title:** Naval and air units of the US, Japan, Australia and the Philippines hold their first multilateral maritime cooperative activity in the West Philippine Sea
- **Current tags:** Move: Military exercise or drill; Target: No target; Location: At sea or in international airspace; Scale: One action; Who: With Israel or other allies; Open: Announced or claimed by the US
- **Note in the tag file:** Multilateral maritime activity in the Philippine zone.
- **Why it is uncertain:** A multilateral maritime activity with Japan, Australia and the Philippines. It is tagged as a drill, but could be a naval action.
- **Question for Sidd:** Is this activity a drill rather than a naval action? (tagged: military exercise or drill)

## 30. Iran #375 (2019-04-08, option C)

- **Title:** State announces it will list the Guard as a Foreign Terrorist Organization, effective Apr 15
- **Current tags:** Move: Legal step (terror listing, indictment, bounty, court case); Target: Military personnel or fighters; Location: No physical place (e.g. sanctions, talks, statements); Scale: One action; Who: The US alone; Open: Announced or claimed by the US
- **Note in the tag file:** FTO listing of the IRGC; target tagged personnel (a military force)
- **Why it is uncertain:** Listing the Guard as a terror organization is tagged legal, with the target "military personnel or fighters". It could be "officials" or "a proxy or partner group".
- **Question for Sidd:** Is the Guard a target of the "personnel" kind? (tagged: military personnel or fighters)

## 31. Iran #255 (2025-06-22, option F)

- **Title:** Operation Midnight Hammer: US bombers and missiles strike Iran's Fordow, Natanz and Isfahan nuclear sites
- **Current tags:** Move: Air, missile or drone strike; Target: Nuclear or missile programs; Location: Inside the adversary's country; Scale: One action; Who: The US alone; Open: Announced or claimed by the US
- **Note in the tag file:** US alone; Israel struck separately
- **Why it is uncertain:** The note says the US struck alone and Israel struck separately. Israel's war on Iran was going on at the same time.
- **Question for Sidd:** Was the US strike on the nuclear sites separate from Israel's strikes? (tagged: the US alone)

## 32. Iran #70 (2026-08-30, option G)

- **Title:** Strikes 2 IRGC rocket launchers on Larak Island, said to be preparing sea mines
- **Current tags:** Move: Air, missile or drone strike; Target: Military equipment and sites (radars, launchers, bases), Military personnel or fighters; Location: Inside the adversary's country; Scale: One action; Who: The US alone; Open: Announced or claimed by the US
- **Why it is uncertain:** Two rocket launchers on an island. The tag adds fighters as a target, which the title does not say. It sits in the option for strikes that risk killing personnel.
- **Question for Sidd:** Was this strike aimed at fighters as well as launchers? (tagged: equipment, personnel)
