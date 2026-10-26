"""NAPOR Caribbean / Venezuela: the US-Venezuela record, 2019 - Oct 26, 2026 (research file, W10).

Same shape as napor/theaters/houthis/events_early.py. Event IDs 4001-4999 and pair IDs 4001-4999 belong to this file.

Rules used here (docs/SOURCE_STANDARD.md):
- Only allowed outlets and official statements. Wire stories read through a syndicated copy are labelled
  "AP (via ...)", "Reuters (via ...)", "AFP (via ...)". seen="full text" means the article was read through
  WebFetch; seen="snippet" means only the search-result headline was seen.
- Venezuelan state media (TeleSUR, VTV) would be allowed only as a labelled claim. No state-media page was
  opened. Where an allowed outlet reports what state media said, the row says "per TeleSUR" and the verdict
  is not_confirmed.
- A US move has an option letter in US_OPTION:
    B  talks or deals (prisoner swaps, oil licenses, talks and normalization with the interim government)
    C  sanctions, designations, indictments, bounties (including sanctions relief / delistings)
    D  strikes on alleged drug boats
    E  naval or air deployments and posture (carrier group, Southern Spear buildup)
    F  strikes on land targets
    G  raids or operations against leaders (the Jan 2-3, 2026 Maduro capture)
    H  other (recognition, airspace closure declarations, tanker seizures, covert-action authorization,
       FAA advisory)
    A  hold. Not tagged.
- Casualties are recorded as the source states them. No totals of my own. Running boat-strike tolls are quoted
  as the outlet gave them; they come from different outlets on different days and do not always agree
  (for example AP counted 13 strikes on Oct 28, 2025; USNI counted 10 on Oct 24).
- Boat strikes: only 8 of the roughly 70 strikes are logged one by one (the ones read in full). The rest are
  covered by the running tolls and the two exclusion windows below.
- Exclusion windows: two stretches where the strike count rose by about one strike every two days (derived
  from outlet counts, see WINDOWS). Strikes inside them are context only, not separate cases.
- Replies are what Venezuela (or armed groups, or a government that acted) did. Words alone are logged and
  census-marked R-weak; material acts (mobilization, expulsions, suspended contracts) can be R-strong.
  After Jan 3, 2026 the interim government cooperated with Washington; cooperative answers are not replies
  and are census-marked N.
- Dates follow the announcement date when a US move was disclosed later (as in the Houthi file).
"""
import datetime as dt


def d(y, m, day):
    return dt.date(y, m, day)


def _s(headline, outlet, published, url, seen="snippet"):
    return {'headline': headline, 'outlet': outlet, 'published': published, 'seen': seen, 'url': url}


# Columns: ID, Date, Actor, Action Type, Target, Detail, Trigger ID, Severity, Confidence, Source
EVENTS = [
# --- 2019-2024: key US moves and the one adversary reply that was sourced ---
(4001, d(2019,1,23), "US", "Diplomatic recognition (Guaido)", "Maduro government", "Trump backs opposition leader Juan Guaido, who declared himself interim president before a rally in Caracas; Trump says the National Assembly declared Maduro illegitimate and the presidency vacant", None, "n/a", "Medium", "see audit"),
(4002, d(2019,1,23), "Venezuela (Maduro)", "Diplomatic break (expulsion order)", "US diplomats in Venezuela", "Maduro announces he is breaking diplomatic relations with the US and gives US diplomatic personnel 72 hours to leave; Pompeo says the US does not recognize his authority to do either", 4001, "n/a", "Medium", "see audit"),
(4003, d(2019,1,28), "US", "Sanction (state oil company)", "PdVSA (Venezuelan state oil company)", "US sanctions PdVSA, effective immediately; US oil purchases go to blocked accounts. CNN reports about $7 billion in assets blocked and more than $11 billion in lost exports expected over a year (Bolton). Stops short of an oil embargo", None, "n/a", "Medium", "see audit"),
(4004, d(2020,3,26), "US", "Indictment and rewards (narco-terrorism)", "Maduro and aides", "Justice Department announces narco-terrorism charges against Maduro and key aides; State Department offers up to $55 million in rewards in total, up to $15 million for Maduro and up to $10 million each for four associates", None, "n/a", "Medium", "see audit"),
(4005, d(2020,3,26), "Venezuela (Foreign Minister Arreaza)", "Statement (denunciation)", "US", "Arreaza says the charges and rewards show the Trump administration's 'desperation' and 'obsession' with Venezuela; Al Jazeera includes no direct response from Maduro", 4004, "n/a", "Medium", "see audit"),
(4006, d(2022,11,26), "US", "Oil license (Chevron)", "Chevron joint ventures with PdVSA", "Treasury lets Chevron resume pumping Venezuelan oil through its PdVSA joint ventures; PdVSA may not receive profits from Chevron's US sales; other sanctions stay. Tied to the Maduro-opposition agreement to resume negotiations", None, "n/a", "Medium", "see audit"),
(4007, d(2023,12,20), "US", "Prisoner swap", "Alex Saab (Maduro ally) and 10 jailed Americans", "US frees Maduro ally Alex Saab; Venezuela frees 10 Americans and the US gets back fugitive contractor Leonard Glenn Francis ('Fat Leonard'); Venezuela also agrees to release 20 political prisoners and suspend arrest warrants for three Venezuelans. Maduro calls it a 'triumph for truth'", None, "n/a", "Medium", "see audit"),
(4008, d(2024,4,17), "US", "Sanction (oil license not renewed)", "Venezuela oil and gas sector", "US lets General License 44 expire (Apr 18) after Maduro's side fell short of election commitments; a replacement license gives companies 45 days to wind down. Petroleum Minister Tellechea says Venezuela stays open to business", None, "n/a", "Medium", "see audit"),
# --- Aug-Oct 2025: bounty, buildup, first boat strikes ---
(4010, d(2025,8,7), "US", "Reward doubled (bounty)", "Maduro", "AG Bondi announces the reward for Maduro's arrest is doubled to $50 million (from $25 million, set in January); accuses him of working with Tren de Aragua, Cartel of the Suns and Sinaloa; says DOJ has seized more than $700 million in assets linked to him", None, "n/a", "Medium", "see audit"),
(4011, d(2025,8,8), "Venezuela (Foreign Minister Gil)", "Statement (denunciation)", "US", "Gil calls the bounty 'crude political propaganda' and 'the most ridiculous smokescreen ever seen', says it is meant to distract from the Epstein controversy, and says 'the dignity of our homeland is not for sale' (reported Aug 8)", 4010, "n/a", "Medium", "see audit"),
(4012, d(2025,8,18), "Venezuela (Maduro)", "Mobilization (militia announced)", "Venezuelan territory (defense)", "Maduro announces a special plan with 'more than 4.5 million militiamen' (his figure) to defend sovereignty, saying 'no empire will touch the sacred soil of Venezuela'; Al Jazeera adds he grounded all aerial drones for 30 days. Came after US naval-movement reports and the bounty", None, "n/a (4.5 million is Maduro's claim)", "Medium", "see audit"),
(4013, d(2025,8,19), "US", "Naval deployment (three destroyers)", "Waters off Venezuela / SOUTHCOM", "US sends three Aegis destroyers (Gravely, Jason Dunham, Sampson) toward waters off Venezuela for counternarcotics; a Defense official says it will run over several months. CNN (Aug 19) says the US confirmed the naval movements to it the prior week; exact day not established, logged on the CNN report date", None, "n/a", "Low", "see audit"),
(4014, d(2025,8,20), "US", "Naval deployment (amphibious group)", "Waters off Venezuela / SOUTHCOM", "Reuters and AFP, from two officials, report the Iwo Jima amphibious group (Iwo Jima, San Antonio, Fort Lauderdale) with about 4,500 personnel including 2,200 Marines could be off Venezuela as early as Sunday Aug 24; Pentagon did not publicly disclose the mission", None, "n/a", "Medium", "see audit"),
(4016, d(2025,8,25), "Venezuela (Interior Minister Cabello)", "Mobilization (troops to Colombian border)", "Venezuela-Colombia border", "Cabello announces 15,000 troops will deploy to the Colombian border against drug trafficking, as three US warships head toward Venezuela's coast (AFP)", 4014, "n/a", "Medium", "see audit"),
(4017, d(2025,9,2), "US", "Strike (alleged drug boat)", "Boat said to be Tren de Aragua, Caribbean", "First strike of the campaign. Trump says it killed '11 terrorists'; a senior defense official confirms a 'precision strike against a drug vessel operated by a designated narco-terrorist organization'; Rubio says the boat departed Venezuela. About 5,000 sailors and Marines in the Caribbean (USNI)", None, "11 killed (Trump); no US forces harmed (Trump)", "Medium", "see audit"),
(4018, d(2025,9,4), "Venezuela (per state media, as reported by Al Jazeera)", "Mobilization (National Militia activated)", "Venezuela (defense)", "Al Jazeera reports Venezuelan state media covered Maduro announcing the first activation of the National Militia, rather than the aircraft incident the same day. State-media claim; no allowed outlet confirms the activation details", 4017, "n/a", "Low", "see audit"),
(4019, d(2025,9,4), "Venezuela (per Pentagon)", "Harassment (military aircraft near US warship)", "USS Jason Dunham (southern Caribbean)", "Pentagon says two Maduro-regime military aircraft (F-16s per a US defense official via the NYT) flew near the destroyer in international waters, a 'highly provocative' attempt to interfere with counter-narcotics operations; warns Venezuela not to obstruct. No official Venezuelan comment in the article", 4017, "No damage or injuries", "Medium", "see audit"),
(4020, d(2025,9,5), "US", "Air deployment (10 F-35s to Puerto Rico)", "Puerto Rico / southern Caribbean", "Reuters, from two sources, reports the US is moving 10 F-35 fighters to a Puerto Rico airfield for operations against designated narco-terrorist groups; expected in the southern Caribbean by late the following week", None, "n/a", "Medium", "see audit"),
(4021, d(2025,9,5), "Venezuela (Maduro)", "Statement (threat perception)", "US", "At a Caracas news conference Maduro says the US is 'seeking a regime change through military threat'", 4020, "n/a", "Medium", "see audit"),
(4022, d(2025,9,15), "US", "Strike (alleged drug boat)", "Boat said to be from Venezuela", "Second boat strike. Trump posts video and says it killed three 'male terrorists' carrying drugs; says the US will stop land-based smuggling the same way. CBS notes the boat in the Sep 2 strike appeared to be turning around when hit", None, "3 killed (Trump)", "Medium", "see audit"),
(4023, d(2025,10,14), "US", "Strike (alleged drug boat)", "Vessel, Caribbean", "Trump says he ordered a lethal strike on a vessel (reported Tuesday Oct 14, Axios Oct 15); says sea trafficking is 'very well under control' and the military will now look at land", None, "6 killed (Trump, per Axios)", "Medium", "see audit"),
(4024, d(2025,10,15), "US", "Covert action (CIA authorized)", "Venezuela", "Trump confirms he authorized the CIA to conduct covert operations inside Venezuela, including possible strikes on cartels; declines to say whether the CIA can act against Maduro; says the administration is 'looking at land'. AP: at least five boats destroyed since early September, 27 killed", None, "n/a", "Medium", "see audit"),
(4025, d(2025,10,15), "Venezuela (Foreign Ministry, Maduro)", "Statement (rejection)", "US", "Foreign Ministry rejects 'the bellicose and extravagant statements by the President of the United States' as a serious violation of international law; Maduro cites the CIA's record of coups and calls for peace", 4024, "n/a", "Medium", "see audit"),
(4026, d(2025,10,15), "US", "Show of force (B-52 attack demonstration)", "Off Venezuela", "Air Forces Southern says B-52H bombers from Barksdale flew an attack demonstration near Venezuela, with F-35Bs alongside; no Venezuelan response in the article", None, "n/a", "Medium", "see audit"),
(4027, d(2025,10,24), "US", "Naval deployment (carrier strike group ordered)", "SOUTHCOM", "Hegseth orders USS Gerald R. Ford, its strike group and air wing to the SOUTHCOM area (Ford was in Split, Croatia). In the region: three destroyers, a cruiser, a littoral combat ship, an attack submarine, the Iwo Jima group with the 22nd MEU, F-35s in Puerto Rico. USNI: ten boat strikes since September, at least 43 killed", None, "n/a", "Medium", "see audit"),
(4028, d(2025,10,26), "US", "Naval visit (USS Gravely in Trinidad)", "Port of Spain, Trinidad and Tobago", "Destroyer USS Gravely arrives with Marines for planned joint exercises with Trinidad and Tobago's defence force; Trinidad says such exercises are regular", None, "n/a", "Medium", "see audit"),
(4029, d(2025,10,27), "Venezuela (VP Rodriguez, Maduro)", "Economic act (energy deals cancelled)", "Trinidad and Tobago", "AP: Rodriguez calls for cancelling energy agreements with Trinidad over its 'hostile' hosting of the Gravely and says she will ask Maduro to withdraw from a 2015 joint gas-exploration agreement. Al Jazeera (Oct 28): Maduro ordered 'immediate suspension' of the gas supply deal, per state broadcaster TeleSUR (state-media claim). Trinidad's PM says the country does not depend on Venezuela", 4028, "n/a", "Medium", "see audit"),
(4030, d(2025,10,27), "US", "Strikes (three alleged drug boats, eastern Pacific)", "Three boats, eastern Pacific", "Hegseth announces (Oct 28) three strikes on Oct 27 in the eastern Pacific. AP count: 13 disclosed strikes since early September, at least 57 killed. A survivor is being sought by Mexican authorities. Opens exclusion window 1", None, "14 killed in total, 1 survivor (Hegseth, per AP)", "Medium", "see audit"),
(4031, d(2025,11,11), "Venezuela (Maduro, Defense Minister Padrino)", "Mobilization (nationwide military exercise)", "Venezuela (defense)", "Venezuela announces a nationwide land-air-sea exercise ('Plan Independencia 200'); Padrino says 200,000 troops are involved (per AFP) and that US boat strikes murder 'defenseless people'. Framed as a response to the US buildup as the Ford entered SOUTHCOM", 4027, "n/a (troop number is Padrino's claim)", "Medium", "see audit"),
(4032, d(2025,11,13), "US", "Operation announced (Southern Spear)", "Latin America counter-narcotics", "Hegseth announces Operation Southern Spear under Joint Task Force Southern Spear, with robotic surface vessels, interceptor boats and robotic aircraft; says it follows Trump's order. Ford had entered SOUTHCOM that Tuesday; CSIS counts more than a dozen US vessels", None, "n/a", "Medium", "see audit"),
(4033, d(2025,11,16), "US", "Naval deployment (carrier enters Caribbean)", "Caribbean Sea", "USS Gerald R. Ford enters the Caribbean via the Anegada Passage. AP: about 12,000 sailors and Marines deployed under Southern Spear. NPR: a US military official says the 'table is being set' for possible action; about 20 boat strikes, 80 killed", None, "n/a", "Medium", "see audit"),
(4034, d(2025,11,16), "Venezuela (Maduro)", "Statement and mobilization claim", "US", "Maduro posts on Facebook that Venezuelans are ready to defend the homeland against 'criminal aggression'; government touts a 'massive' mobilization of troops and civilians and calls the US exercises in Trinidad 'an act of aggression'", 4033, "n/a", "Medium", "see audit"),
(4035, d(2025,11,21), "US", "Diplomatic talks (Trump-Maduro phone call)", "Maduro", "Reuters, from four people briefed: call under 15 minutes; Maduro asks amnesty for himself and family, removal of sanctions on 100+ officials, and Delcy Rodriguez to lead an interim government; Trump rejects most and gives him a week to leave Venezuela. Deadline passed without Maduro leaving", None, "n/a", "Medium", "see audit"),
(4036, d(2025,11,22), "US", "Aviation advisory (FAA warning)", "Venezuelan airspace", "FAA advises operators to exercise caution over Venezuela, citing 'heightened military activity', navigation interference and Venezuelan military exercises (date per Boston Globe); six airlines then cancel flights (Al Jazeera)", None, "n/a", "Low", "see audit"),
(4037, d(2025,11,24), "US", "Terrorist designation (Cartel de los Soles)", "Cartel de los Soles (Venezuelan officials)", "State Department designation of the Cartel of the Suns as a foreign terrorist organization takes effect (Federal Register, Nov 24). Al Jazeera notes the name is a Venezuelan term for corrupt officers; more than 80 killed in boat strikes so far", None, "n/a", "Medium", "see audit"),
(4038, d(2025,11,24), "Venezuela (Foreign Ministry)", "Statement (rejection)", "US", "Calls the designation a 'ridiculous lie' used to justify military intervention", 4037, "n/a", "Medium", "see audit"),
(4039, d(2025,11,29), "US", "Airspace closure declaration", "Venezuelan airspace", "Trump posts on Truth Social: 'please consider THE AIRSPACE ABOVE AND SURROUNDING VENEZUELA TO BE CLOSED IN ITS ENTIRETY', addressed to airlines, pilots, drug dealers and traffickers. Reuters: it came the day after the week he gave Maduro to leave expired", None, "n/a", "Medium", "see audit"),
(4040, d(2025,11,30), "Venezuela (government)", "Statement (condemnation)", "US", "Calls Trump's post a 'colonialist threat' and a 'hostile, unilateral and arbitrary act'; says it effectively suspends US migrant deportation flights (Reuters, Nov 30)", 4039, "n/a", "Medium", "see audit"),
(4041, d(2025,11,30), "Venezuela (government)", "Economic act (airline rights revoked)", "Six international airlines", "Reuters says Venezuela revoked the operating rights of six major international airlines that had suspended flights after the FAA warning. The Reuters text gives no revocation date and names no airline; logged on the Reuters date", 4036, "n/a", "Low", "see audit"),
(4042, d(2025,12,10), "US", "Seizure (oil tanker Skipper)", "Tanker Skipper, off Venezuela", "Coast Guard seizes the Guyana-flagged, US-sanctioned tanker Skipper off Venezuela under a warrant (Bondi: FBI, HSI, Coast Guard, support from the Department of War); Bondi says it carried sanctioned oil from Venezuela and Iran. Trump says more could follow. USNI reports no Venezuelan response", None, "No casualties reported", "Medium", "see audit"),
(4043, d(2025,12,15), "US", "Strikes (three alleged drug boats, eastern Pacific)", "Three boats, eastern Pacific", "US military announces strikes on three boats on Dec 15 (AFP: at least 93 killed in the campaign to date). Opens exclusion window 2", None, "8 killed in total: 3, 2 and 3 on the three boats (AFP)", "Medium", "see audit"),
(4044, d(2025,12,16), "US", "Blockade order (sanctioned tankers)", "Sanctioned oil tankers going into and out of Venezuela", "Trump posts a 'TOTAL AND COMPLETE BLOCKADE OF ALL SANCTIONED OIL TANKERS going into, and out of, Venezuela' and vows to keep building up the military. NPR: unclear how it would be enforced; one tanker seized the week before; at least 95 killed in 25 known boat strikes", None, "n/a", "Medium", "see audit"),
(4045, d(2025,12,16), "Venezuela (government)", "Statement (denunciation, UN complaint)", "US", "Accuses Trump of 'violating international law, free trade, and the principle of free navigation' and trying to steal the nation's wealth; says it will take the matter to the UN", 4044, "n/a", "Medium", "see audit"),
(4046, d(2025,12,20), "US", "Seizure (oil tanker Centuries)", "Tanker Centuries, east of Barbados", "Coast Guard with Pentagon support seizes the Panama-flagged Centuries, said by Reuters to carry about 1.8 million barrels of Venezuelan crude bound for China; the White House calls it a falsely flagged shadow-fleet ship; AP quotes a maritime expert saying it appeared legally registered. Al Jazeera: more than 24 boat strikes, at least 100 killed", None, "No casualties reported", "Medium", "see audit"),
(4047, d(2025,12,20), "Venezuela (VP Rodriguez, government)", "Statement (denunciation, UN complaint)", "US", "Rodriguez denounces the 'theft and hijacking' of the vessel and the 'forced disappearance' of its crew; Caracas calls it a 'serious act of international piracy' that will not go 'unpunished' and says it will complain to the UN Security Council", 4046, "n/a", "Medium", "see audit"),
(4048, d(2025,12,29), "US", "Strike (dock facility, CIA per AP sources)", "Dock area on the Venezuelan coast", "Trump tells WABC radio the US knocked out a 'big facility where ships come from' and later calls it a dock where boats are loaded with drugs; AP, from two sources, says the CIA carried out the strike 'last week' (exact date not given; logged on Trump's disclosure date). Venezuelan officials had not acknowledged it", None, "No casualties stated", "Low", "see audit"),
# --- Jan 2026: capture of Maduro and its aftermath ---
(4049, d(2026,1,3), "US", "Raid (Operation Absolute Resolve, Maduro captured)", "Maduro compound and military sites, Caracas", "Overnight Jan 2-3, more than 150 aircraft (F-18, F-22, F-35, B-1, drones) and helicopters; the raid lasted under 30 minutes; Maduro and Cilia Flores flown to USS Iwo Jima and on to New York; DOJ releases an indictment. Trump says the US will run Venezuela until a transition", None, "US: a few service members injured, Trump believed none killed (AP). Venezuela: Rodriguez says civilians and military were killed; officials say at least 24 security officers (AP via NPR); AG Saab says 'dozens' of officers and civilians. Cuba says 32 officers", "Medium", "see audit"),
(4050, d(2026,1,5), "Venezuela (VP Delcy Rodriguez)", "Statement and swearing-in (interim president)", "US", "Rodriguez is sworn in as interim leader after the Supreme Court names her acting president; says 'history and justice will make them pay' and the US kidnapped Maduro, but invites the US to 'a cooperative agenda'. Trump tells The Atlantic: 'If she doesn't do what's right, she is going to pay a very big price' (NYT via Boston Globe)", 4049, "n/a", "Medium", "see audit"),
(4051, d(2026,1,6), "Cuba (government)", "Casualty statement and mourning", "US (Venezuela operation)", "Cuba publishes the names, ranks and ages (26 to 60) of 32 Cuban military personnel it says were killed, declares two days of mourning; FM Bruno Rodriguez says Cubans are 'prepared to give their lives' against US intervention. US envoy at the OAS calls the operation a 'targeted law enforcement action'. Cuba did not say how they died", 4049, "32 Cuban personnel killed (Cuban government claim)", "Medium", "see audit"),
(4052, d(2026,1,6), "US", "Oil deal announced (30-50 million barrels)", "Venezuelan interim authorities", "Trump says Venezuela will turn over 30 to 50 million barrels of sanctioned oil to be sold at market price, with revenue controlled 'by me'; asks Energy Secretary Wright to carry it out. Rodriguez answers 'My destiny is not determined by them, but by God' (AP via NPR)", None, "n/a", "Medium", "see audit"),
(4053, d(2026,1,7), "US", "Seizure (two Venezuela-linked tankers)", "Marinera (ex-Bella 1, Russian flag), North Atlantic; M Sophia, near the Caribbean", "US special forces take the Russian-flagged Marinera in the North Atlantic under a federal court warrant (EUCOM); Homeland Security Secretary Noem says forces seized the Panama-flagged, US-sanctioned M Sophia. Russia calls the first a breach of maritime law. No Venezuelan reaction in the article", None, "No casualties reported", "Medium", "see audit"),
(4054, d(2026,1,8), "Venezuela (National Assembly head Jorge Rodriguez)", "Concession (prisoner releases)", "US", "Announces Venezuela will release an 'important number' of political prisoners, citizens and foreigners; Foro Penal estimates about 800 remain detained. White House: 'one example of how the President is using maximum leverage'", 4049, "n/a", "Medium", "see audit"),
(4055, d(2026,1,23), "US", "Strike (alleged drug boat, eastern Pacific)", "Boat, eastern Pacific", "First known boat strike since Maduro's capture. AP: 36 known strikes since early September, at least 117 killed, most in the Caribbean. Coast Guard notified to search for a survivor", None, "2 killed, 1 survivor (SOUTHCOM, per AP)", "Medium", "see audit"),
(4056, d(2026,2,19), "Venezuela (interim government)", "Concession (amnesty law)", "Political prisoners", "Rodriguez signs an amnesty law covering politically driven offenses since 1999; Foro Penal tallies 448 releases since Jan 8 and more than 600 still held. AP does not say the US directly pressed for the bill", None, "n/a", "Medium", "see audit"),
(4057, d(2026,3,5), "US", "Diplomatic ties restored", "Venezuela (interim government)", "State Department says the US and Venezuela agree to restore diplomatic relations cut in 2019, with a 'phased process' toward a democratically elected government, at the end of Interior Secretary Burgum's visit. Rodriguez welcomes it on state TV", None, "n/a", "Medium", "see audit"),
(4058, d(2026,3,30), "US", "Embassy reopened (Caracas)", "Venezuela", "Al Jazeera: the US reopens its embassy in Caracas ('We are once again the US Embassy in Caracas'), nearly three months after the Maduro operation", None, "n/a", "Medium", "see audit"),
(4059, d(2026,4,1), "US", "Sanctions relief (Rodriguez delisted)", "Delcy Rodriguez", "Treasury removes Rodriguez from the SDN list (sanctioned in 2018). Rodriguez welcomes it on X and asks for the remaining sanctions to be lifted. Trump has said he will 'run' Venezuela and warned of a second wave if she does not comply", None, "n/a", "Medium", "see audit"),
(4060, d(2026,4,30), "US", "Normalization (first direct commercial flight)", "Venezuela", "Flight AA3599 (Envoy for American Airlines) lands in Caracas, ending a seven-year suspension of direct service that DHS imposed; the State Department and Transportation Secretary Duffy frame it as a milestone", None, "n/a", "Medium", "see audit"),
(4061, d(2026,6,12), "US", "Strike (Tren de Aragua compound in Venezuela)", "Tren de Aragua compound, Venezuela", "Trump announces a 'swift and lethal kinetic' strike killed Tren de Aragua leader Hector Guerrero Flores; Hegseth says it happened earlier in the week and cites a 'shared U.S. and Venezuelan commitment' to fight narco-terrorists. Venezuela's communications ministry did not respond (NPR)", None, "Only Guerrero Flores's death reported", "Medium", "see audit"),
(4062, d(2026,8,24), "US", "Strike (alleged drug boat, eastern Pacific)", "Low-profile vessel, eastern Pacific", "SOUTHCOM announces a strike on a low-profile vessel; AP headline calls it believed to be the first in two months; AP: deaths from the campaign now exceed 210 after more than 60 strikes", None, "2 killed (Pentagon, per AP)", "Medium", "see audit"),
(4063, d(2026,8,28), "US", "Oil deal announced (65 billion barrels)", "Venezuela (interim government)", "Trump posts 'THE BIGGEST OIL DEAL IN WORLD HISTORY!', says Rubio, Hegseth and interim President Rodriguez negotiated it; AP's headline says the US takes control of 65 billion barrels of reserves. No terms given; no Venezuelan response on the page", None, "n/a", "Medium", "see audit"),
(4064, d(2026,10,4), "US", "Strike (alleged drug boat, Caribbean)", "Go-fast boat, Caribbean Sea", "SOUTHCOM says confirmed intelligence showed the vessel's active involvement in narcotrafficking. Stripes: the toll is at least 235 across 70 strikes since September 2025 (no source named for the totals)", None, "4 killed (SOUTHCOM)", "Medium", "see audit"),
(4065, d(2026,10,8), "US", "Indictment (superseding, torture conspiracy)", "Maduro and Cilia Flores", "Prosecutors in the Southern District of New York add conspiracy to commit torture to the narco-terrorism and cocaine-importation charges; the 30-page indictment alleges torture of more than a dozen American citizens in Venezuelan custody", None, "n/a", "Medium", "see audit"),
(4066, d(2026,10,14), "US", "Sanctions relief (Jorge Rodriguez delisted)", "Jorge Rodriguez (National Assembly head)", "OFAC removes Jorge Rodriguez from the SDN list; a source tells Al Jazeera it is part of wider recognition of the interim government and a three-phase transition plan. Rubio says a new round of negotiations on Venezuela's future begins the same day", None, "n/a", "Medium", "see audit"),
]

# ---------------------------------------------------------------------------------------------
_AJ_BOUNTY = _s('US doubles reward for arrest of Venezuela\'s President Maduro to $50m', 'Al Jazeera', '2025-08-08', 'https://www.aljazeera.com/news/2025/8/8/us-doubles-reward-for-arrest-of-venezuelas-president-maduro-to-50m', 'full text')
_AJ_AUG21 = _s('US warships may reach Venezuela coast by weekend in drug cartel operation', 'Al Jazeera', '2025-08-21', 'https://www.aljazeera.com/news/2025/8/21/us-warships-may-reach-venezuela-coast-by-weekend-in-drug-cartel-operation', 'full text')
_AJ_SEP5 = _s('Pentagon warns Venezuela as 2 military aircraft fly near US warship', 'Al Jazeera', '2025-09-05', 'https://www.aljazeera.com/news/2025/9/5/pentagon-warns-venezuela-as-2-military-aircraft-fly-near-us-navy-ship', 'full text')
_AP_CIA = _s('Trump confirms the CIA is conducting covert operations inside Venezuela', 'AP (via News4JAX)', '2025-10-15', 'https://www.news4jax.com/news/politics/2025/10/15/trump-confirms-the-cia-is-conducting-covert-operations-inside-venezuela/', 'full text')
_AXIOS_CIA = _s('Oct 15, 2025 - Politics & Policy (Trump, Venezuela, CIA, covert action)', 'Axios', '2025-10-15', 'https://www.axios.com/2025/10/15/trump-venezuela-cia-maduro-covert-action', 'full text')
_AP_TT = _s('Venezuela moves to cancel energy agreements with Trinidad after U.S. warship arrives at island nation', 'AP (via PBS NewsHour)', '2025-10-27', 'https://www.pbs.org/newshour/world/venezuela-moves-to-cancel-energy-agreements-with-trinidad-after-u-s-warship-arrives-at-island-nation', 'full text')
_AP_FORD = _s('US aircraft carrier arrives in the Caribbean in major buildup near Venezuela', 'AP (via Messenger-Inquirer)', '2025-11-16', 'https://www.messenger-inquirer.com/ap/elections/us-aircraft-carrier-arrives-in-the-caribbean-in-major-buildup-near-venezuela/article_68c3d9e5-4345-5705-8240-f1fd3e6c14f4.html', 'full text')
_BG_AIRSPACE = _s('Trump says Venezuelan airspace should be considered closed (Truth Social post, Nov 29)', 'Boston Globe', '2025-11-29', 'https://www.bostonglobe.com/2025/11/29/business/trump-venezuelan-airspace-closed/', 'full text')
_RTR_AIRSPACE = _s('Venezuela condemns Trump\'s \'colonialist threat\' on airspace', 'Reuters (via BusinessDay)', '2025-11-30', 'https://www.businessday.co.za/world/2025-11-30-venezuela-condemns-trumps-colonialist-threat-on-airspace/', 'full text')
_AJ_FTO = _s('US adds Venezuelan \'cartel\' to terror list as military threat rises', 'Al Jazeera', '2025-11-24', 'https://aljazeera.com/news/2025/11/24/us-adds-venezuelan-cartel-to-terror-list-as-military-threat-rises', 'full text')
_NPR_BLOCKADE = _s('Trump orders blockade of \'sanctioned oil tankers\' into Venezuela', 'NPR', '2025-12-16', 'https://www.npr.org/2025/12/16/nx-s1-5646721/trump-orders-blockade-of-sanctioned-oil-tankers-into-venezuela', 'full text')
_AJ_CENTURIES = _s('US seizes second oil tanker off Venezuela\'s coast', 'Al Jazeera', '2025-12-20', 'https://www.aljazeera.com/news/2025/12/20/us-seizes-second-oil-vessel-off-venezuela-coast-officials-say', 'full text')
_AP_CENTURIES = _s('US forces stop a second merchant vessel off the coast of Venezuela, American officials say', 'AP (via News4JAX)', '2025-12-20', 'https://www.news4jax.com/news/politics/2025/12/20/us-forces-stop-a-second-merchant-vessel-off-the-coast-of-venezuela-american-officials-say/', 'full text')
_AP_CAPTURE = _s('How U.S. forces captured Venezuelan leader Nicolás Maduro in Caracas', 'AP (via PBS NewsHour)', '2026-01-03', 'https://www.pbs.org/newshour/world/how-u-s-forces-captured-venezuelan-leader-nicolas-maduro-in-caracas', 'full text')
_AP_CUBA = _s('Cuba releases details of 32 officers killed in US strike on Venezuela as US defends attack', 'AP (via ABC News)', '2026-01-07', 'https://abcnews.go.com/International/wireStory/cuba-releases-details-32-officers-killed-us-strike-128955026', 'full text')
_NPR_OIL = _s('Trump says US to get 30 million to 50 million barrels of oil from Venezuela at market price', 'AP (via NPR / KJZZ)', '2026-01-07', 'https://www.kjzz.org/npr-top-stories/2026-01-07/trump-says-us-to-get-30-million-to-50-million-barrels-of-oil-from-venezuela-at-market-price', 'full text')

SOURCES = {
 4001: [_s("Venezuela's Maduro cuts off U.S. relations after Trump backs opposition leader Juan Guaido", 'NBC News (NBC Latino)', '2019-01-23', 'https://www.nbcnews.com/news/latino/trump-recognizes-venezuela-opposition-leader-juan-guaido-interim-president-n961771', 'full text'),
        _s('In Venezuela, opposition leader Juan Guaido declares himself interim president', 'NPR', '2019-01-23', 'https://www.npr.org/2019/01/23/687951060/in-venezuela-opposition-leader-juan-guaid-declares-himself-interim-president', 'full text')],
 4002: [_s("Venezuela's Maduro cuts off U.S. relations after Trump backs opposition leader Juan Guaido", 'NBC News (NBC Latino)', '2019-01-23', 'https://www.nbcnews.com/news/latino/trump-recognizes-venezuela-opposition-leader-juan-guaido-interim-president-n961771', 'full text'),
        _s('In Venezuela, opposition leader Juan Guaido declares himself interim president', 'NPR', '2019-01-23', 'https://www.npr.org/2019/01/23/687951060/in-venezuela-opposition-leader-juan-guaid-declares-himself-interim-president', 'full text')],
 4003: [_s('US sanctions Venezuelan oil company', 'CNN', '2019-01-28', 'https://amp.cnn.com/cnn/2019/01/28/politics/us-sanctions-venezuelan-oil-company', 'full text')],
 4004: [_s("US indicts Venezuela's Maduro on narco-terrorism charges", 'Al Jazeera', '2020-03-26', 'https://www.aljazeera.com/news/2020/3/26/us-indicts-venezuelas-maduro-on-narco-terrorism-charges', 'full text')],
 4005: [_s("US indicts Venezuela's Maduro on narco-terrorism charges", 'Al Jazeera', '2020-03-26', 'https://www.aljazeera.com/news/2020/3/26/us-indicts-venezuelas-maduro-on-narco-terrorism-charges', 'full text')],
 4006: [_s('U.S. gives Chevron go ahead to pump oil in Venezuela again', 'Axios', '2022-11-26', 'https://www.axios.com/2022/11/26/us-chevron-venezula-oil', 'full text')],
 4007: [_s("The US has released an ally of Venezuela's president in a swap for jailed Americans, the AP learns", 'AP (via WSLS)', '2023-12-20', 'https://www.wsls.com/news/politics/2023/12/20/the-us-has-released-an-ally-of-venezuelas-president-in-a-swap-for-jailed-americans-the-ap-learns/', 'full text')],
 4008: [_s('US reimposes oil sanctions against Venezuela over election concerns', 'Al Jazeera', '2024-04-18', 'https://www.aljazeera.com/amp/news/2024/4/18/us-reimposes-oil-sanctions-against-venezuela-over-election-concerns', 'full text')],
 4010: [_AJ_BOUNTY],
 4011: [_AJ_BOUNTY],
 4012: [_s("Venezuela mobilizes its militia after US says it's deploying military forces to waters around Latin America", 'CNN (via KRDO)', '2025-08-19', 'https://krdo.com/news/2025/08/19/venezuela-mobilizes-its-militia-after-us-says-its-deploying-military-forces-to-waters-around-latin-america/', 'full text'),
        _AJ_AUG21],
 4013: [_s("Venezuela mobilizes its militia after US says it's deploying military forces to waters around Latin America", 'CNN (via KRDO)', '2025-08-19', 'https://krdo.com/news/2025/08/19/venezuela-mobilizes-its-militia-after-us-says-its-deploying-military-forces-to-waters-around-latin-america/', 'full text'),
        _s('3 U.S. warships to sail off Venezuela as Trump pushes cartel crackdown', 'CBS News / Reuters / AP (via Yahoo)', '', 'https://www.yahoo.com/news/articles/3-u-warships-sail-off-121040669.html', 'full text')],
 4014: [_AJ_AUG21,
        _s('destroyers near venezuela joined amphibious warship cartels', 'Stars and Stripes (Reuters report)', '2025-08-21', 'https://www.stripes.com/theaters/americas/2025-08-21/destroyers-near-venezuela-joined-amphibious-warship-cartels-18837034.html', 'full text')],
 4016: [_s('Caracas, Aug 25, 2025 (AFP) - Venezuela builds up border security over US warships', 'AFP (via NAMPA)', '2025-08-25', 'https://www.nampa.org/text/22717930', 'full text')],
 4017: [_s('VIDEO: U.S. Military Strikes Suspected Drug Vessel as Warships Gather in the Caribbean', 'USNI News', '2025-09-02', 'https://news.usni.org/2025/09/02/u-s-military-makes-precision-strike-against-suspected-drug-vessel-as-warships-gather-in-the-caribbean', 'full text')],
 4018: [_AJ_SEP5],
 4019: [_AJ_SEP5],
 4020: [_s('US moving 10 fighter jets to Puerto Rico to fight cartels, sources say', 'Reuters (via Yahoo)', '2025-09-05', 'https://www.yahoo.com/news/articles/us-moving-10-fighter-jets-134133146.html', 'full text')],
 4021: [_s('US moving 10 fighter jets to Puerto Rico to fight cartels, sources say', 'Reuters (via Yahoo)', '2025-09-05', 'https://www.yahoo.com/news/articles/us-moving-10-fighter-jets-134133146.html', 'full text')],
 4022: [_s('Trump announces second U.S. strike against alleged drug boat from Venezuela', 'CBS News', '2025-09-15', 'https://www.cbsnews.com/news/trump-strike-second-alleged-venezuela-drug-boat', 'full text')],
 4023: [_AXIOS_CIA],
 4024: [_AP_CIA, _AXIOS_CIA],
 4025: [_AP_CIA],
 4026: [_s('B-52 bomber demonstration near Venezuela', 'Stars and Stripes', '2025-10-21', 'https://www.stripes.com/branches/air_force/2025-10-21/b52-bomber-demonstration-near-venezuela-19499687.html', 'full text')],
 4027: [_s('Hegseth Orders USS Gerald R. Ford to U.S. Southern Command', 'USNI News', '2025-10-24', 'https://news.usni.org/2025/10/24/hegseth-orders-uss-gerald-r-ford-to-u-s-southern-command', 'full text')],
 4028: [_AP_TT,
        _s('Venezuela suspends Trinidad and Tobago gas accord over US warship visit', 'Al Jazeera', '2025-10-28', 'https://www.aljazeera.com/news/2025/10/28/venezuela-suspends-trinidad-and-tobago-gas-accord-over-us-warship-visit', 'full text')],
 4029: [_AP_TT,
        _s('Venezuela suspends Trinidad and Tobago gas accord over US warship visit (reports a TeleSUR state-media claim)', 'Al Jazeera; reports a TeleSUR (state media) claim', '2025-10-28', 'https://www.aljazeera.com/news/2025/10/28/venezuela-suspends-trinidad-and-tobago-gas-accord-over-us-warship-visit', 'full text')],
 4030: [_s('Hegseth says US carried out 3 strikes on alleged drug-running boats in eastern Pacific, killing 14', 'AP (via NY1 / Spectrum News)', '2025-10-28', 'https://ny1.com/nyc/all-boroughs/ap-top-news/2025/10/28/hegseth-says-us-carried-out-3-strikes-on-alleged-drug-running-boats-in-eastern-pacific-killing-14', 'full text')],
 4031: [_s('Venezuela launches huge military exercise as U.S. Navy flotilla nears Caribbean waters', 'CBS News (reports AFP)', '2025-11-12', 'https://www.cbsnews.com/amp/texas/news/venezuela-military-mobilization-us-navy-flotilla-nears-caribbean-uss-ford', 'full text')],
 4032: [_s('us southern spear robotic fleet cartels', 'Stars and Stripes', '2025-11-14', 'https://www.stripes.com/theaters/us/2025-11-13/us-southern-spear-robotic-fleet-cartels-19759479.html', 'full text'),
        _s('Hegseth Unveils Operation Southern Spear With Venezuela Tensions High', 'Bloomberg', '2025-11-13', 'https://www.bloomberg.com/news/articles/2025-11-13/operation-southern-spear-unveiled-after-us-boat-strikes-in-caribbean', 'snippet')],
 4033: [_AP_FORD,
        _s('USS Gerald Ford enters Caribbean Sea as threat of U.S. action against Venezuela rises', 'NPR (via KUNC)', '2025-11-15', 'https://www.kunc.org/npr-news/2025-11-15/uss-gerald-ford-enters-caribbean-sea-as-threat-of-u-s-action-against-venezuela-rises', 'full text')],
 4034: [_AP_FORD],
 4035: [_s('Trump rejected Maduro requests on call. Options narrow for Venezuela leader', 'Reuters (via Baird Maritime)', '', 'https://www.bairdmaritime.com/security/trump-rejected-maduro-requests-on-call-options-narrow-for-venezuela-leader', 'full text')],
 4036: [_BG_AIRSPACE, _AJ_FTO],
 4037: [_AJ_FTO],
 4038: [_AJ_FTO],
 4039: [_BG_AIRSPACE, _RTR_AIRSPACE],
 4040: [_RTR_AIRSPACE],
 4041: [_RTR_AIRSPACE],
 4042: [_s('UPDATED: U.S. Seizes Tanker Off Coast of Venezuela', 'USNI News', '2025-12-10', 'https://news.usni.org/2025/12/10/u-s-seizes-tanker-off-coast-of-venezuela-trump-says', 'full text')],
 4043: [_s('8 killed as 3 drug boats blown up in Pacific: US military', 'AFP (via Gulf News)', '2025-12-16', 'https://gulfnews.com/world/americas/8-killed-as-3-drug-boats-blown-up-in-pacific-us-military-1.500381218', 'full text')],
 4044: [_NPR_BLOCKADE],
 4045: [_NPR_BLOCKADE],
 4046: [_AJ_CENTURIES, _AP_CENTURIES],
 4047: [_AJ_CENTURIES, _AP_CENTURIES],
 4048: [_s('CIA behind strike at Venezuelan dock that Trump claims was used by drug smugglers, AP sources say', 'AP (via News4JAX)', '2025-12-30', 'https://www.news4jax.com/news/politics/2025/12/31/cia-behind-strike-at-venezuelan-dock-that-trump-claims-was-used-by-drug-smugglers-ap-sources-say/', 'full text')],
 4049: [_AP_CAPTURE, _NPR_OIL, _AP_CUBA],
 4050: [_s('venezuela delcy rodriguez (swearing-in as interim leader)', 'New York Times (via Boston Globe)', '2026-01-05', 'https://www.bostonglobe.com/2026/01/05/world/venezuela-delcy-rodriguez/', 'full text')],
 4051: [_AP_CUBA],
 4052: [_NPR_OIL,
        _s('US oil, Trump, Venezuela, Maduro (oil announcement)', 'Axios', '2026-01-07', 'https://www.axios.com/2026/01/07/us-oil-trump-venezuela-maduro', 'full text')],
 4053: [_s('US seizes Venezuela-linked Russian oil tanker', 'Al Jazeera', '2026-01-07', 'https://www.aljazeera.com/amp/news/2026/1/7/us-attempting-to-seize-venezuela-linked-russian-oil-tanker-reports', 'full text')],
 4054: [_s('Venezuela to release "important number" of political prisoners, lawmaker says', 'Axios', '2026-01-08', 'https://www.axios.com/2026/01/08/venezuela-maduro-political-prisoners-release', 'full text')],
 4055: [_s("US carries out first known strike on alleged drug boat since Maduro's capture", 'AP (via News4JAX)', '2026-01-23', 'https://www.news4jax.com/news/politics/2026/01/23/us-carries-out-first-known-strike-on-alleged-drug-boat-since-maduros-capture/', 'full text')],
 4056: [_s('Venezuela approves amnesty bill that could see release of hundreds detained for political reasons', 'AP (via KSAT)', '2026-02-19', 'https://www.ksat.com/news/world/2026/02/19/venezuela-approves-amnesty-bill-that-could-see-release-of-hundreds-detained-for-political-reasons/', 'full text')],
 4057: [_s("U.S. and Venezuela agree to reestablish diplomatic ties in major shift after Maduro's ouster", 'AP (via PBS NewsHour)', '2026-03-05', 'https://www.pbs.org/newshour/world/u-s-and-venezuela-agree-to-reestablish-diplomatic-ties-in-major-shift-after-maduros-ouster', 'full text')],
 4058: [_s('US embassy reopens in Venezuela months after Maduro abduction', 'Al Jazeera', '2026-03-30', 'https://www.aljazeera.com/video/newsfeed/2026/3/30/us-embassy-reopens-in-venezuela-months-after-maduro-abduction', 'full text')],
 4059: [_s("US removes sanctions on Venezuela's interim President Delcy Rodriguez", 'Al Jazeera', '2026-04-01', 'https://www.aljazeera.com/news/2026/4/1/us-removes-sanctions-on-venezuelas-interim-president-delcy-rodriguez', 'full text')],
 4060: [_s('First US-Venezuela flight lands in Caracas after seven-year suspension', 'Al Jazeera', '2026-04-30', 'https://aljazeera.com/economy/2026/4/30/first-us-venezuela-flight-lands-in-caracas-after-seven-year-suspension', 'full text')],
 4061: [_s('Trump says U.S. military strike killed leader of Tren de Aragua gang', 'NPR', '2026-06-12', 'https://www.npr.org/2026/06/12/nx-s1-5856611/u-s-military-kill-leader-tren-de-aragua', 'full text')],
 4062: [_s('US launches deadly strike on alleged drug boat, believed to be 1st in 2 months', 'AP (via WAFF)', '2026-08-24', 'https://www.waff.com/2026/08/24/us-launches-deadly-strike-alleged-drug-boat-believed-be-1st-2-months/', 'full text')],
 4063: [_s('Trump says US has entered deal with Venezuela to take control of 65 billion barrels of oil reserves', 'AP (via 6abc)', '2026-08-28', 'https://6abc.com/story/trump-says-us-has-entered-deal-venezuela-take-control-65-billion-barrels-oil-reserves/19754218/', 'full text')],
 4064: [_s('us strike caribbean kills 4', 'Stars and Stripes', '2026-10-05', 'https://www.stripes.com/theaters/americas/2026-10-05/us-strike-caribbean-kills-4-23061506.html', 'full text')],
 4065: [_s('Nicolas Maduro, Cilia Flores new torture charge', 'CBS News', '2026-10-08', 'https://cbsnews.com/news/nicolas-maduro-cilia-flores-new-torture-charge', 'full text')],
 4066: [_s("US lifts sanctions on Venezuela's top legislator", 'Al Jazeera', '2026-10-14', 'https://www.aljazeera.com/news/2026/10/14/us-lifts-sanctions-on-venezuelas-top-legislator', 'full text')],
}
VERDICT = {k: 'confirmed' for k in SOURCES}
# Venezuelan state-media claim relayed by an allowed outlet; no allowed outlet confirms the details.
VERDICT[4018] = 'not_confirmed'
# Rows where an allowed outlet confirms the event but not every detail in the row
# (figures are a government's own claim, a date is inferred, or one part rests on state media).
PARTLY = {4012, 4013, 4029, 4031, 4036, 4041, 4048, 4051}

# Which option letter each US move belongs to (B talks/deals, C sanctions/designations/indictments/bounties and
# their relief, D boat strikes, E naval/air deployments and posture, F land strikes, G raids on leaders,
# H other). A (hold) is not tagged.
US_OPTION = {
 4001: 'H', 4003: 'C', 4004: 'C', 4006: 'B', 4007: 'B', 4008: 'C', 4010: 'C',
 4013: 'E', 4014: 'E', 4017: 'D', 4020: 'E', 4022: 'D', 4023: 'D', 4024: 'H', 4026: 'E',
 4027: 'E', 4028: 'E', 4030: 'D', 4032: 'E', 4033: 'E', 4035: 'B', 4036: 'H', 4037: 'C',
 4039: 'H', 4042: 'H', 4043: 'D', 4044: 'H', 4046: 'H', 4048: 'F', 4049: 'G', 4052: 'B',
 4053: 'H', 4055: 'D', 4057: 'B', 4058: 'B', 4059: 'C', 4060: 'B', 4061: 'F', 4062: 'D',
 4063: 'B', 4064: 'D', 4065: 'C', 4066: 'C',
}


def _cred(k):
    if VERDICT.get(k) != 'confirmed':
        return 0.30
    outlets = {s['outlet'].split(' (')[0].split(';')[0].split(' / ')[0] for s in SOURCES[k] if s['seen'] == 'full text'}
    return 0.96 if len(outlets) >= 2 else 0.80


# My own estimate of the engine's credibility score (full-text allowed outlet 0.80, two distinct outlets 0.96,
# claim-only 0.30; under 0.50 is not counted). For the organizer's spot check only.
CRED_ESTIMATE = {e[0]: _cred(e[0]) for e in EVENTS}

# Trigger Census rows for US moves of kinds B-H (window: 7 days for a reply).
# Category = what the move cost the other side; Status: R-strong (material act, clearly linked), R-weak (words
# only or a plausible link), N (no reply reported in the source read), as in data.py.
# After Jan 3, 2026 the interim government cooperated; its welcomes are not replies and are marked N.
# Boat strikes inside the exclusion windows (WINDOWS) are context only; the two start acts are 4030 and 4043.
CENSUS = [
 (4001, "Political/Diplomatic", "R-strong", "Recognition of Guaido, Jan 23, 2019 -> Maduro breaks relations and gives US diplomats 72 hours to leave, same day (NBC, NPR)."),
 (4003, "Economic/Blockade", "N", "PdVSA sanctions, Jan 28, 2019. The CNN article reports no Venezuelan government response; no further search made for Jan 29 - Feb 4."),
 (4004, "Political/Diplomatic", "R-weak", "Maduro indictment and rewards, Mar 26, 2020 -> Arreaza denounces them the same day (Al Jazeera). Words only."),
 (4006, "Political/Diplomatic", "N", "Chevron license, Nov 26, 2022. A deal, tied to the Maduro-opposition agreement; no hostile reply reported."),
 (4007, "Political/Diplomatic", "N", "Saab-for-Americans swap, Dec 20, 2023. A deal; Maduro called it a 'triumph for truth' (AP). No hostile reply."),
 (4008, "Economic/Blockade", "N", "GL44 not renewed, Apr 17-18, 2024. Tellechea said Venezuela stays open to business; no retaliatory act reported (Al Jazeera)."),
 (4010, "Political/Diplomatic", "R-weak", "$50 million bounty, Aug 7, 2025 -> Foreign Minister Gil calls it propaganda (Al Jazeera, Aug 8). Maduro's militia call came Aug 18, 11 days later."),
 (4013, "Military/Property", "R-weak", "Three destroyers confirmed (CNN Aug 19). Within 7 days: 15,000 troops to the Colombian border, Aug 25 (AFP), framed as anti-drug. Maduro's militia call (Aug 18) came before the CNN report date."),
 (4014, "Military/Property", "R-weak", "Amphibious group reported Aug 20 -> Cabello announces 15,000 troops to the Colombian border Aug 25 (AFP); Maduro's drone grounding and militia plan were announced Aug 18."),
 (4017, "Personnel/Casualty", "R-weak", "First boat strike, Sep 2, 2025 (11 killed per Trump) -> two Venezuelan aircraft fly near USS Jason Dunham Sep 4 (Pentagon) and state media show a militia activation. Venezuela gave no official reason; link plausible."),
 (4020, "Military/Property", "R-weak", "10 F-35s to Puerto Rico, Sep 5, 2025 -> Maduro says the US is seeking regime change through military threat (Reuters), same day. Words only."),
 (4022, "Personnel/Casualty", "N", "Second boat strike, Sep 15, 2025 (3 killed). No Venezuelan act found for Sep 16-22 in the sources read."),
 (4023, "Personnel/Casualty", "N", "Strike of Oct 14, 2025 (6 killed per Trump). The Oct 15 Venezuelan statement answered Trump's CIA remarks (4024), not the strike."),
 (4024, "Military/Property", "R-weak", "CIA covert-action disclosure, Oct 15, 2025 -> Foreign Ministry rejects Trump's 'bellicose' statements the same day (AP). Words only."),
 (4026, "Military/Property", "N", "B-52 demonstration, Oct 15, 2025. No Venezuelan response reported (Stripes)."),
 (4027, "Military/Property", "N", "Ford ordered to SOUTHCOM, Oct 24, 2025. Venezuela's Oct 27 energy cutoff answered the Gravely visit (4028); its next reply to the carrier was the Nov 11 exercise, 18 days later."),
 (4028, "Military/Property", "R-strong", "USS Gravely in Port of Spain, Oct 26, 2025 -> Venezuela moves to cancel energy deals with Trinidad Oct 27 (AP; TeleSUR claim of immediate suspension)."),
 (4030, "Personnel/Casualty", "N", "Three boat strikes, Oct 27, 2025 (14 killed per Hegseth). Starts exclusion window 1. No Venezuelan act found for Oct 28 - Nov 3; the next, the Nov 11 exercise, was 15 days later."),
 (4032, "Military/Property", "R-weak", "Southern Spear announced Nov 13, 2025 -> Maduro says Venezuelans are ready to defend the homeland and the government touts a 'massive' mobilization (AP, Nov 16). Words and claimed mobilization."),
 (4033, "Military/Property", "R-weak", "Ford enters the Caribbean, Nov 16, 2025 -> Maduro's Facebook post and claimed mobilization the same day (AP)."),
 (4035, "Political/Diplomatic", "N", "Trump-Maduro call, Nov 21, 2025. Maduro did not leave by the deadline; no hostile act found Nov 22-28. The next reply logged is to the FAA warning (4041)."),
 (4036, "Economic/Blockade", "R-weak", "FAA advisory, Nov 22, 2025 -> Venezuela revokes six airlines' rights (Reuters, Nov 30). Reuters gives no revocation date, so within 7 days is likely but not proven."),
 (4037, "Political/Diplomatic", "R-weak", "Cartel de los Soles designation, Nov 24, 2025 -> Foreign Ministry calls it a 'ridiculous lie' the same day (Al Jazeera). Words only."),
 (4039, "Economic/Blockade", "R-weak", "Airspace closure post, Nov 29, 2025 -> Venezuela calls it a 'colonialist threat' and says it effectively suspends deportation flights (Reuters, Nov 30). Words, plus the airline revocation (4041)."),
 (4042, "Economic/Blockade", "N", "Skipper seizure, Dec 10, 2025. USNI reports no Venezuelan response; the Dec 16 statement answered the blockade order (4044)."),
 (4043, "Personnel/Casualty", "N", "Three boat strikes, Dec 15, 2025 (8 killed per AFP). Starts exclusion window 2. No Venezuelan act tied to the strikes found."),
 (4044, "Economic/Blockade", "R-weak", "Blockade order, Dec 16, 2025 -> Venezuela calls it a violation of international law and says it will go to the UN (NPR), same day. Words only."),
 (4046, "Economic/Blockade", "R-weak", "Centuries seized, Dec 20, 2025 -> Rodriguez denounces 'theft and hijacking' and Caracas says it will complain to the UN Security Council (Al Jazeera, AP), same day. Words only."),
 (4048, "Military/Property", "N", "Dock strike disclosed Dec 29, 2025. Venezuelan officials had not acknowledged it (AP); Maduro did not mention it in a Tuesday speech."),
 (4049, "Personnel/Casualty", "R-strong", "Maduro captured, Jan 2-3, 2026 -> within 5 days: casualty claims and a war-crime investigation announced (AP), Rodriguez's swearing-in speech (Jan 5, NYT), and political-prisoner releases announced Jan 8 (Axios). No military retaliation reported. The reply is political, not violent."),
 (4052, "Political/Diplomatic", "R-weak", "Oil announcement, Jan 6, 2026 -> Rodriguez says her destiny is not set by the US (AP via NPR); the Jan 8 prisoner release (4054) followed. Words plus a concession."),
 (4053, "Economic/Blockade", "N", "Tanker seizures, Jan 7, 2026. Russia objected to the Marinera seizure; no Venezuelan reaction in the Al Jazeera article."),
 (4055, "Personnel/Casualty", "N", "First boat strike since the capture, Jan 23, 2026 (2 killed). No Venezuelan act reported."),
 (4057, "Political/Diplomatic", "N", "Ties restored, Mar 5, 2026. Rodriguez welcomed it on state TV (AP); a cooperative answer, not a reply."),
 (4058, "Political/Diplomatic", "N", "Embassy reopened, Mar 30, 2026. No hostile reply reported."),
 (4059, "Economic/Blockade", "N", "Rodriguez delisted, Apr 1, 2026. She welcomed it on X and asked for more relief; cooperative."),
 (4060, "Political/Diplomatic", "N", "First direct flight, Apr 30, 2026. No hostile reply reported."),
 (4061, "Personnel/Casualty", "N", "Strike on Tren de Aragua compound in Venezuela, announced Jun 12, 2026. Hegseth cited a shared US-Venezuelan commitment; Venezuela's communications ministry did not respond (NPR)."),
 (4062, "Personnel/Casualty", "N", "Boat strike, Aug 24, 2026 (2 killed). No Venezuelan act reported."),
 (4063, "Political/Diplomatic", "N", "Oil deal announced, Aug 28, 2026. AP page includes no Venezuelan response; the interim government negotiated it."),
 (4064, "Personnel/Casualty", "N", "Boat strike, Oct 4, 2026 (4 killed). Stripes mentions no Venezuelan connection or response."),
 (4065, "Political/Diplomatic", "N", "Superseding torture indictment, Oct 8, 2026. No Venezuelan reply found in the CBS article."),
 (4066, "Economic/Blockade", "N", "Jorge Rodriguez delisted, Oct 14, 2026. Sanctions relief within a cooperative phase; no hostile reply."),
]

# Reply pairs (pair id, trigger, reply, category, reply caused casualties Y/N, note)
PAIRS = [
 (4001, 4001, 4002, "Political/Diplomatic", "N", "Maduro breaks relations and orders US diplomats out within 72 hours, the same day the US backs Guaido"),
 (4002, 4004, 4005, "Political/Diplomatic", "N", "Venezuela's foreign minister denounces the indictment and rewards the same day"),
 (4003, 4010, 4011, "Political/Diplomatic", "N", "Foreign Minister Gil dismisses the $50 million bounty as propaganda"),
 (4004, 4014, 4016, "Military/Property", "N", "15,000 troops to the Colombian border five days after reports of the amphibious group"),
 (4005, 4017, 4019, "Military/Property", "N", "Venezuelan aircraft fly near USS Jason Dunham two days after the first boat strike; no shots or damage"),
 (4006, 4017, 4018, "Military/Property", "N", "State media show the first activation of the National Militia two days after the first boat strike (claim)"),
 (4007, 4020, 4021, "Political/Diplomatic", "N", "Maduro says the US seeks regime change by military threat, the day the F-35 move is reported"),
 (4008, 4024, 4025, "Political/Diplomatic", "N", "Foreign Ministry rejects Trump's 'bellicose' statements the day he confirms CIA action"),
 (4009, 4028, 4029, "Economic/Blockade", "N", "Venezuela moves to cancel Trinidad energy deals the day after USS Gravely arrives in Port of Spain"),
 (4010, 4027, 4031, "Military/Property", "N", "Nationwide exercise (Padrino: 200,000 troops) 18 days after the Ford order, as the carrier entered SOUTHCOM"),
 (4011, 4033, 4034, "Military/Property", "N", "Maduro says Venezuelans are ready to defend the homeland the day the Ford enters the Caribbean"),
 (4012, 4036, 4041, "Economic/Blockade", "N", "Venezuela revokes six airlines' rights after the FAA warning led them to suspend flights (date not given by Reuters)"),
 (4013, 4037, 4038, "Political/Diplomatic", "N", "Foreign Ministry calls the Cartel de los Soles designation a 'ridiculous lie' the same day"),
 (4014, 4039, 4040, "Political/Diplomatic", "N", "Venezuela calls the airspace post a 'colonialist threat' the next day"),
 (4015, 4044, 4045, "Political/Diplomatic", "N", "Venezuela says the blockade breaks international law and goes to the UN, the same day"),
 (4016, 4046, 4047, "Political/Diplomatic", "N", "Rodriguez calls the Centuries seizure piracy and promises a UN Security Council complaint, the same day"),
 (4017, 4049, 4050, "Political/Diplomatic", "N", "Rodriguez swears in as interim leader two days after the raid: threatens 'justice will make them pay' but offers cooperation"),
 (4018, 4049, 4054, "Political/Diplomatic", "N", "Venezuela announces political-prisoner releases five days after the raid; White House calls it 'maximum leverage'"),
]

# Exclusion windows (boat strikes inside are context only, not separate cases) and the acts that start them.
# Derived from outlet counts of strikes, which are not fully reconciled between outlets:
#  Window 1, Oct 27 - Nov 15, 2025: USNI (Oct 24) 10 strikes -> AP (Oct 28) 13, including the three of Oct 27 (4030)
#    -> NPR (Nov 15) 20: ten strikes in about 20 days, roughly one every two days.
#  Window 2, Dec 15, 2025 - Jan 2, 2026: NPR (Dec 16) 25 strikes -> AP (Jan 23) 36 including that day's; AP says
#    strikes largely paused after Jan 3 and Jan 23 was the first known since the capture, so about ten strikes
#    fell in the 18 days to Jan 2 (4043 is the three-boat day that opens it).
# Other stretches ran slower: 10 strikes in the 52 days from Sep 2 to Oct 24; about 24 strikes from Jan 23 to
# Aug 24, 2026 (36 -> more than 60), with "first in two months" on Aug 24 (AP).
WINDOWS = [(d(2025, 10, 27), d(2025, 11, 15)), (d(2025, 12, 15), d(2026, 1, 2))]
START_ACTS = {4030, 4043}

# Phases (oldest first)
PHASES = [
 ("Sanctions and deals before the buildup", d(2019, 1, 23), d(2025, 8, 6), "Guaido recognition and Maduro's break (#4001-#4002), PdVSA sanctions (#4003), indictment (#4004), Chevron license (#4006), prisoner swap (#4007), license lapse (#4008)"),
 ("Bounty, naval buildup and first boat strikes", d(2025, 8, 7), d(2025, 10, 23), "Bounty (#4010), destroyers and amphibious group (#4013-#4014), militia and border troops (#4012, #4016), first strike (#4017), F-35s (#4020), CIA authorization (#4024)"),
 ("Carrier and Southern Spear", d(2025, 10, 24), d(2025, 11, 30), "Ford ordered and arrives (#4027, #4033), Trinidad energy cutoff (#4029), Venezuelan exercise (#4031), Southern Spear (#4032), Maduro call (#4035), FTO designation (#4037), airspace post (#4039)"),
 ("Blockade and tanker seizures", d(2025, 12, 1), d(2026, 1, 2), "Skipper and Centuries seizures (#4042, #4046), blockade order (#4044), dock strike (#4048); second boat-strike cluster"),
 ("Maduro captured; interim government cooperates", d(2026, 1, 3), d(2026, 10, 26), "Capture (#4049), oil deals (#4052, #4063), ties and embassy (#4057, #4058), delistings (#4059, #4066), Tren de Aragua strike (#4061); boat strikes continue at a slower pace"),
]

CHAIN_NAMES = {
 4001: "Guaido recognition -> Maduro breaks relations",
 4017: "First boat strike -> Venezuelan aircraft near USS Jason Dunham and militia activation",
 4028: "USS Gravely in Trinidad -> Venezuela cancels Trinidad energy deals",
 4036: "FAA warning -> airlines suspend -> Venezuela revokes six airlines' rights",
 4049: "Maduro captured -> Rodriguez threat and offer -> prisoner releases",
}
