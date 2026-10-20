"""NAPOR: the US-Iran record BEFORE the 2026 war (May 2019 - Feb 27, 2026).

Why: the 2026 war alone gives only 2-7 past cases per option. Stretching back to the 2019 "maximum
pressure" crisis adds real US moves (deployments, sanctions, strikes, talks) and what followed.

Rules used here (same source standard as the rest of NAPOR: docs/SOURCE_STANDARD.md):
- Only allowed outlets and official statements. Wire stories read through a syndicated copy are
  labelled "AP (via ...)". seen="snippet" means only the search-result headline was seen; the
  credibility score already discounts that.
- Event IDs 201+ are pre-war, so the 2026 IDs (1-115) never change.
- Before 2026 Iran mostly answered the US through groups it arms in Iraq and Syria. A reply by such a
  group is logged with census status "R-proxy" (it counts as a reply, and the page says "Iran or an
  Iran-backed group"). Their actor names do NOT start with "Iran", so they are never counted as a
  direct Iranian strike.
- Continuous-fighting rule (same as for 2026): Oct 17, 2023 - Jan 29, 2024 the militias attacked US
  forces almost daily (until Kataib Hezbollah paused on Jan 30), so every US strike in that stretch has
  a "reply" by default. US strikes in it are logged as context but not counted in the census.
"""
import datetime as dt


def d(y, m, day):
    return dt.date(y, m, day)


def _s(headline, outlet, published, url, seen="snippet"):
    return {'headline': headline, 'outlet': outlet, 'published': published, 'seen': seen, 'url': url}


# Columns: ID, Date, Actor, Action Type, Target, Detail, Trigger ID, Severity, Confidence, Source
EVENTS = [
(201, d(2019,5,5), "US", "Force posture (deployment)", "Middle East", "US sends the Abraham Lincoln carrier strike group and a bomber task force to the Middle East as a warning to Iran (Bolton)", None, "n/a", "Medium", "see audit"),
(202, d(2019,5,12), "Iran (suspected; a UAE-led probe blamed a 'state actor')", "Sabotage (shipping)", "UAE (off Fujairah)", "Four commercial ships, including two Saudi tankers, damaged by sabotage off Fujairah", None, "Hull damage; no casualties reported", "Medium", "see audit"),
(203, d(2019,6,13), "Iran (per US; Iran denies)", "Strike (shipping)", "Gulf of Oman", "Tankers Front Altair and Kokuka Courageous attacked in the Gulf of Oman; the US blames Iran, which denies it", None, "Fires on both tankers; crews evacuated, no deaths reported", "Medium", "see audit"),
(204, d(2019,6,17), "US", "Force posture (deployment)", "Middle East", "Pentagon announces about 1,000 more troops for the Middle East, citing hostile Iranian behaviour", 203, "n/a", "Medium", "see audit"),
(205, d(2019,6,20), "Iran", "Shootdown (US drone)", "US Navy drone", "IRGC shoots down a US Navy RQ-4 Global Hawk near the Strait of Hormuz; Trump later says he called off retaliatory strikes", None, "Drone destroyed; no casualties", "Medium", "see audit"),
(206, d(2019,6,24), "US", "Sanctions response", "Iran", "Trump signs an executive order sanctioning Supreme Leader Khamenei and his office", 205, "n/a", "Medium", "see audit"),
(207, d(2019,7,18), "US", "Air defense (drone shot down)", "Iranian drone", "USS Boxer downs an Iranian drone that came close to it in the Strait of Hormuz, Trump says; Iran denies losing one", None, "Drone destroyed (US claim)", "Medium", "see audit"),
(208, d(2019,7,31), "US", "Sanctions response", "Iran", "Treasury sanctions Foreign Minister Javad Zarif", None, "n/a", "Medium", "see audit"),
(209, d(2019,9,14), "Iran (per US; the Houthis claimed it)", "Strike (oil facilities)", "Saudi Arabia (Abqaiq, Khurais)", "Drone and missile attack on Saudi oil facilities knocks out about half of Saudi output; the Houthis claim it, the US blames Iran", None, "No deaths reported; major damage to oil output", "Medium", "see audit"),
(210, d(2019,9,20), "US", "Sanctions response", "Iran", "Treasury sanctions Iran's central bank and national development fund after the Saudi oil attack", 209, "n/a", "Medium", "see audit"),
(211, d(2019,9,20), "US", "Force posture (deployment)", "Saudi Arabia/UAE", "Pentagon announces troops and air-defense equipment for Saudi Arabia and the UAE after the oil attack", 209, "n/a", "Medium", "see audit"),
(212, d(2019,12,27), "Kataib Hezbollah (Iran-backed, per US)", "Strike (rockets)", "K-1 base, Kirkuk (Iraq)", "Rocket attack on the K-1 base near Kirkuk kills a US contractor; the US blames Kataib Hezbollah", None, "1 US contractor killed; US and Iraqi personnel wounded", "Medium", "see audit"),
(213, d(2019,12,29), "US", "Strike (militia sites)", "Kataib Hezbollah, Iraq/Syria", "US strikes five Kataib Hezbollah sites in Iraq and Syria in retaliation for the K-1 attack", 212, "About 25 militia fighters killed", "Medium", "see audit"),
(214, d(2019,12,31), "Kataib Hezbollah supporters (Iran-backed)", "Raid (embassy breach)", "US embassy, Baghdad", "Militia supporters storm the outer compound of the US embassy in Baghdad after the US strikes", 213, "Property damage; no US casualties reported", "Medium", "see audit"),
(215, d(2020,1,3), "US", "Assassination strike", "Iran (IRGC Quds Force)", "US drone strike at Baghdad airport kills IRGC Quds Force commander Qassem Soleimani and militia leader Abu Mahdi al-Muhandis", 214, "Soleimani, al-Muhandis and others killed", "Medium", "see audit"),
(216, d(2020,1,8), "Iran", "Retaliation strike", "Ain al-Asad and Erbil bases (Iraq)", "Iran fires ballistic missiles at bases housing US troops in Iraq in revenge for Soleimani", 215, "No deaths; more than 100 US troops later diagnosed with brain injuries", "Medium", "see audit"),
(217, d(2020,1,10), "US", "Sanctions response", "Iran", "Treasury sanctions Iran's steel and metals sectors and senior officials after the missile attack", 216, "n/a", "Medium", "see audit"),
(218, d(2020,3,11), "Kataib Hezbollah (Iran-backed, per US)", "Strike (rockets)", "Camp Taji (Iraq)", "Rocket attack on Camp Taji kills two US troops and a British soldier", None, "3 killed (2 US, 1 UK)", "Medium", "see audit"),
(219, d(2020,3,12), "US", "Strike (militia weapons sites)", "Kataib Hezbollah, Iraq", "US strikes Kataib Hezbollah weapons storage sites in Iraq after the Taji attack", 218, "Casualty figures not from allowed outlets", "Medium", "see audit"),
(220, d(2020,3,14), "Unknown (Iran-backed militia suspected)", "Strike (rockets)", "Camp Taji (Iraq)", "At least 25 rockets hit Camp Taji a day after the US strikes; no group named", 219, "3 US service members (2 seriously) and 2 Iraqi soldiers wounded (AP)", "Medium", "see audit"),
(221, d(2020,8,14), "US", "Seizure (fuel cargoes)", "Iranian shipping", "US seizes four Iranian fuel cargoes bound for Venezuela", None, "n/a", "Medium", "see audit"),
(222, d(2021,2,25), "US", "Strike (militia facilities)", "Iran-backed militias, eastern Syria", "First strikes under Biden hit facilities used by Iran-backed militias at a Syria-Iraq border crossing, after a rocket attack in Erbil", None, "Casualty figures not from allowed outlets", "Medium", "see audit"),
(223, d(2021,6,27), "US", "Strike (militia facilities)", "Iran-backed militias, Iraq-Syria border", "US strikes facilities used by Iran-backed militias near the Iraq-Syria border", None, "n/a", "Medium", "see audit"),
(224, d(2021,6,28), "Unknown (Iran-backed militia suspected)", "Strike (rockets)", "US forces, eastern Syria", "Rockets fired at US forces in eastern Syria the day after the US strikes", 223, "No US injuries reported", "Medium", "see audit"),
(225, d(2022,8,24), "US", "Strike (militia bunkers)", "IRGC-backed militias, Deir ez-Zor (Syria)", "US strikes bunkers in Deir ez-Zor used by militias backed by the IRGC; the US later says 4 militia members were killed", None, "4 militia members killed (US)", "Medium", "see audit"),
(226, d(2022,8,24), "Militias (Iran-backed, per US)", "Strike (rockets)", "US bases, northeast Syria", "Militia rockets hit Green Village and the Conoco gas field within hours of the US strikes", 225, "3 US service members treated for minor injuries (AP)", "Medium", "see audit"),
(227, d(2023,3,23), "Militia (Iranian-made drone, per US)", "Strike (drone)", "US facility near Hasakah (Syria)", "A drone of Iranian origin hits a US maintenance facility near Hasakah, killing a US contractor", None, "1 US contractor killed; 5 US troops and another contractor wounded", "Medium", "see audit"),
(228, d(2023,3,23), "US", "Strike (IRGC-affiliated facilities)", "IRGC-affiliated groups, eastern Syria", "US F-15s strike facilities in eastern Syria used by groups affiliated with the IRGC", 227, "No deaths reported by allowed outlets", "Medium", "see audit"),
(229, d(2023,3,24), "Militias (Iran-backed, suspected)", "Strike (rockets and drones)", "US bases, northeast Syria", "Rockets and drones target US bases in northeast Syria the day after the US strikes", 228, "1 US service member wounded (ABC)", "Medium", "see audit"),
(230, d(2023,4,27), "Iran", "Seizure (tanker)", "Shipping (Gulf of Oman)", "IRGC Navy seizes the US-bound tanker Advantage Sweet in the Gulf of Oman", None, "Ship and crew held", "Medium", "see audit"),
(231, d(2023,7,17), "US", "Force posture (deployment)", "Gulf region", "Pentagon sends a destroyer, F-35s and F-16s to protect merchant ships after Iranian seizure attempts", None, "n/a", "Medium", "see audit"),
(232, d(2023,8,10), "US/Iran", "Diplomatic proposal (prisoner deal)", "Iran", "US and Iran agree a prisoner swap that releases about $6 billion in frozen Iranian funds (completed Sep 18)", None, "n/a", "Medium", "see audit"),
(233, d(2023,10,26), "US", "Strike (IRGC-linked facilities)", "IRGC and affiliated groups, eastern Syria", "US strikes two facilities in eastern Syria used by the IRGC and affiliated groups after attacks on US forces", None, "n/a", "Medium", "see audit"),
(234, d(2023,11,8), "US", "Strike (IRGC-linked weapons storage)", "IRGC and affiliated groups, eastern Syria", "US strikes an IRGC-linked weapons storage facility in eastern Syria", None, "n/a", "Medium", "see audit"),
(235, d(2023,12,25), "Kataib Hezbollah (Iran-backed, per US)", "Strike (drone)", "Erbil air base (Iraq)", "Drone attack on Erbil air base wounds three US service members", None, "3 US service members wounded, one critically", "Medium", "see audit"),
(236, d(2023,12,26), "US", "Strike (militia sites)", "Kataib Hezbollah, Iraq", "US strikes three sites used by Kataib Hezbollah after the Erbil drone attack", 235, "n/a", "Medium", "see audit"),
(237, d(2024,1,4), "US", "Strike (militia commander)", "Harakat al-Nujaba, Baghdad", "US drone strike in Baghdad kills a Harakat al-Nujaba commander", None, "Commander killed", "Medium", "see audit"),
(238, d(2024,1,28), "Islamic Resistance in Iraq (Iran-backed)", "Strike (drone)", "Tower 22 (Jordan)", "Drone attack on Tower 22 in Jordan kills three US soldiers and wounds dozens", None, "3 US soldiers killed, dozens wounded", "Medium", "see audit"),
(239, d(2024,1,30), "Kataib Hezbollah (Iran-backed)", "Pause announcement", "US forces", "Kataib Hezbollah announces it is suspending attacks on US forces", 238, "n/a", "Medium", "see audit"),
(240, d(2024,2,2), "US", "Strike (IRGC Quds Force and militia sites)", "IRGC Quds Force and affiliated militias, Iraq/Syria", "US strikes more than 85 targets in Iraq and Syria linked to the IRGC Quds Force and affiliated militias, in retaliation for Tower 22", 238, "Deaths reported by Iraq and Syria; figures not from allowed outlets", "Medium", "see audit"),
(241, d(2024,2,4), "Islamic Resistance in Iraq (Iran-backed)", "Strike (drone)", "Al-Omar base (Syria)", "Drone attack on al-Omar base, which houses US troops, kills six US-allied Kurdish fighters", 240, "6 SDF fighters killed; no US troops hurt (AP)", "Medium", "see audit"),
(242, d(2024,2,7), "US", "Assassination strike", "Kataib Hezbollah commander, Baghdad", "US drone strike in Baghdad kills a senior Kataib Hezbollah commander", None, "Commander and others killed", "Medium", "see audit"),
(243, d(2024,4,13), "Iran", "Strike (direct attack on Israel)", "Israel", "Iran launches hundreds of drones and missiles at Israel in its first direct attack; US forces help intercept them", None, "Most intercepted", "Medium", "see audit"),
(244, d(2024,4,18), "US", "Sanctions response", "Iran", "US and UK sanction Iran's drone program after the attack on Israel", 243, "n/a", "Medium", "see audit"),
(245, d(2024,10,1), "Iran", "Strike (missiles at Israel)", "Israel", "Iran fires dozens of ballistic missiles at Israel", None, "Casualty figures not from allowed outlets", "Medium", "see audit"),
(246, d(2024,10,13), "US", "Force posture (deployment)", "Israel", "US sends a THAAD missile-defense battery and troops to operate it to Israel", 245, "n/a", "Medium", "see audit"),
(247, d(2025,2,4), "US", "Sanctions response (maximum pressure)", "Iran", "Trump signs a memorandum restoring 'maximum pressure' on Iran, aiming to drive its oil exports to zero", None, "n/a", "Medium", "see audit"),
(248, d(2025,4,12), "US/Iran", "Diplomatic talks", "-", "First round of US-Iran nuclear talks in Muscat (Witkoff and Araghchi), mediated by Oman", None, "n/a", "Medium", "see audit"),
(249, d(2025,4,19), "US/Iran", "Diplomatic talks", "-", "Second round of talks in Rome; both sides report progress", None, "n/a", "Medium", "see audit"),
(250, d(2025,4,26), "US/Iran", "Diplomatic talks", "-", "Third round of talks in Muscat, with expert-level meetings", None, "n/a", "Medium", "see audit"),
(251, d(2025,5,11), "US/Iran", "Diplomatic talks", "-", "Fourth round of talks in Muscat; Iran calls it 'difficult but useful'", None, "n/a", "Medium", "see audit"),
(252, d(2025,5,23), "US/Iran", "Diplomatic talks", "-", "Fifth round of talks in Rome ends without a breakthrough", None, "n/a", "Medium", "see audit"),
(253, d(2025,6,13), "Israel", "Strike (war start)", "Iran", "Israel launches strikes on Iranian nuclear and military sites, starting a 12-day war", None, "n/a in this log", "Medium", "see audit"),
(254, d(2025,6,13), "Iran", "Retaliation strike", "Israel", "Iran answers with waves of ballistic missiles at Israel, which continue until the Jun 24 ceasefire", 253, "Deaths in Israel (figures not from allowed outlets)", "Medium", "see audit"),
(255, d(2025,6,22), "US", "Strike (nuclear sites)", "Iran (Fordow, Natanz, Isfahan)", "Operation Midnight Hammer: US bombers and missiles strike Iran's Fordow, Natanz and Isfahan nuclear sites", 253, "Heavy damage claimed by the US; no casualty figures", "Medium", "see audit"),
(256, d(2025,6,23), "Iran", "Retaliation strike", "Al Udeid air base (Qatar)", "Iran fires 19 missiles at Al Udeid air base; one hits; Trump thanks Iran for 'early notice'", 255, "No deaths or injuries (Al Jazeera)", "Medium", "see audit"),
(257, d(2025,6,24), "US", "Ceasefire announcement", "Israel/Iran", "Trump announces a ceasefire between Israel and Iran, phased in over 24 hours", 256, "n/a", "Medium", "see audit"),
(258, d(2025,7,30), "US", "Sanctions response", "Iran", "Largest US sanctions on Iran since 2018 target a shipping network linked to the son of senior official Ali Shamkhani", None, "n/a", "Medium", "see audit"),
(259, d(2026,1,27), "US", "Force posture (deployment)", "Middle East", "A US 'armada' led by the Abraham Lincoln carrier group forms in the Middle East as Washington and Tehran trade threats", None, "n/a", "Medium", "see audit"),
(260, d(2026,2,6), "US/Iran", "Diplomatic talks", "-", "US-Iran nuclear talks open in Oman", None, "n/a", "Medium", "see audit"),
(261, d(2026,2,13), "US", "Force posture (deployment)", "Middle East", "Trump orders a second aircraft carrier to the Middle East", None, "n/a", "Medium", "see audit"),
(262, d(2026,2,26), "US/Iran", "Diplomatic talks", "-", "US-Iran nuclear talks resume in Geneva", None, "n/a", "Medium", "see audit"),
(263, d(2021,3,3), "Unknown (Iran-backed militia suspected)", "Strike (rockets)", "Ain al-Asad air base (Iraq)", "Rockets hit Ain al-Asad air base, which hosts US troops; a US civilian contractor dies during the attack", None, "1 US civilian contractor died (NPR)", "Medium", "see audit"),
]

_AJ_K1 = _s('US targets pro-Iran militia bases in Iraq, Syria raids', 'Al Jazeera', '2019-12-29', 'https://www.aljazeera.com/news/2019/12/29/us-targets-pro-iran-militia-bases-in-iraq-syria-raids')
_TWZ_K1 = _s('U.S. Strikes Back At Iranian Proxy Forces In Iraq And Syria After Deadly Rocket Attack', 'The War Zone', '2019-12-29', 'https://www.twz.com/31651/u-s-strikes-iranian-proxy-force-bases-in-iraq-and-syria-following-deadly-rocket-attack')
_STR_TAJI = _s('Officials: US strikes Iran-backed militias in response to Iraq base attack', 'Stars and Stripes', '2020-03-12', 'https://stripes.com/news/middle-east/officials-us-strikes-iran-backed-militias-in-response-to-iraq-base-attack-1.622259')
_STR_21 = _s('US forces come under rocket attack in Syria after strikes on Iran-backed militias', 'Stars and Stripes', '2021-06-28', 'https://www.stripes.com/theaters/middle_east/2021-06-28/us-forces-rocket-attack-syria-iraq-iran-1883233.html', 'full text')
_PBS_22 = _s('U.S. says airstrikes killed 4 Iranian-backed militia members in Syria', 'AP (via PBS NewsHour)', '2022-08-25', 'https://www.pbs.org/newshour/politics/u-s-says-airstrikes-killed-4-iranian-backed-militia-members-in-syria', 'full text')
_ABC_23 = _s('Additional attacks on US bases in Syria Friday after retaliatory airstrikes on Iranian-backed groups', 'ABC News (via ABC7)', '2023-03-24', 'https://abc7news.com/syria-airstrike-us-drone-attack-american-contractor-killed-service-members/13007641/', 'full text')
_PBS_24 = _s('Several allied Kurdish fighters killed in drone attack on base housing U.S. troops in Syria', 'AP (via PBS NewsHour)', '2024-02-05', 'https://www.pbs.org/newshour/world/several-allied-kurdish-fighters-killed-in-drone-attack-on-base-housing-u-s-troops-in-syria', 'full text')
_AJ_UDEID = _s('Tehran attacks US base in Qatar, hours later Trump states Israel-Iran truce', 'Al Jazeera', '2025-06-23', 'https://www.aljazeera.com/news/2025/6/23/flares-over-qatars-doha-explosions-heard-amid-us-israel-iran-conflict', 'full text')
_AJ_KH = _s('Kataib Hezbollah announces halt of attacks on US forces', 'Al Jazeera', '2024-01-31', 'https://www.aljazeera.com/news/2024/1/31/kataib-hezbollah-says-it-suspends-attacks-on-us-forces')

SOURCES = {
 263: [_s('U.S. Civilian Contractor Dies During Rocket Strike On Iraq Air Base', 'NPR (via WGCU)', '2021-03-03', 'https://www.wgcu.org/2021-03-03/u-s-civilian-contractor-dies-during-rocket-strike-on-iraq-air-base'),
       _s('Iraq military base used by U.S. hit by rockets year after similar attack brought U.S. and Iran close to war', 'CBS News', '2021-03-03', 'https://www.cbsnews.com/news/rockets-strike-al-asad-airbase-iraq-hosting-us-troops')],
 201: [_s('Bolton: US deploying bombers to Middle East in warning to Iran', 'Al Jazeera', '2019-05-06', 'https://www.aljazeera.com/news/2019/5/6/bolton-us-deploying-bombers-to-middle-east-in-warning-to-iran')],
 202: [_s("UAE says four ships subjected to 'sabotage' off east coast", 'Al Jazeera', '2019-05-13', 'https://www.aljazeera.com/news/2019/5/13/uae-says-four-ships-subjected-to-sabotage-off-east-coast'),
       _s('US issues new warning to ships after sabotage off UAE', 'AP (via Washington Times)', '2019-05-12', 'https://www.washingtontimes.com/news/2019/may/12/us-issues-new-warning-to-ships-after-sabotage-off-/')],
 203: [_s("'Ridiculous, dangerous': Iran denies US claims over Gulf tankers", 'Al Jazeera', '2019-06-14', 'https://www.aljazeera.com/news/2019/6/14/ridiculous-dangerous-iran-denies-us-claims-over-gulf-tankers'),
       _s('Tankers on fire in Gulf of Oman after suspected attack', 'NPR (via WAMC)', '2019-06-13', 'https://www.wamc.org/2019-06-13/tankers-on-fire-in-gulf-of-oman-after-suspected-attack')],
 204: [_s('U.S. sending 1,000 more troops to Middle East amid tensions with Iran', 'CBS News', '2019-06-17', 'https://www.cbsnews.com/amp/news/us-sending-1000-more-troops-to-middle-east-amid-tensions-with-iran-announced-today-2019-06-17'),
       _s('U.S. to send more troops to Middle East', 'PBS NewsHour', '2019-06-17', 'https://www.pbs.org/newshour/world/u-s-to-send-more-troops-to-middle-east')],
 205: [_s("Iran's Revolutionary Guard shoots down US drone", 'Al Jazeera', '2019-06-20', 'https://www.aljazeera.com/news/2019/06/iran-revolutionary-guard-shoots-spy-drone-report-190620035802427.html'),
       _s("US: Iran shot down drone in international airspace in 'unprovoked attack'", 'Times of Israel', '2019-06-20', 'https://www.timesofisrael.com/us-iran-shot-down-drone-in-international-airspace-in-unprovoked-attack/')],
 206: [_s('Trump announces new sanctions on Iran, including on supreme leader', 'ABC News (via ABC7)', '2019-06-24', 'https://abc7news.com/trump-announces-new-sanctions-on-iran-including-on-supreme-leader-/5361919/')],
 207: [_s("Trump says US warship 'destroyed' Iranian drone in Gulf", 'Al Jazeera', '2019-07-18', 'https://www.aljazeera.com/news/2019/07/warship-destroys-iranian-drone-strait-hormuz-190718192635252.html'),
       _s("USS Boxer Downs Iranian Drone in 'Defensive Action'", 'USNI News', '2019-07-18', 'https://news.usni.org/?p=68160')],
 208: [_s('US imposes sanctions on Iranian Foreign Minister Zarif', 'Al Jazeera', '2019-08-01', 'https://www.aljazeera.com/amp/economy/2019/8/1/us-imposes-sanctions-on-iranian-foreign-minister-zarif'),
       _s('US sanctions Iranian Foreign Minister Zarif', 'CNN (via KPAX)', '2019-07-31', 'https://www.kpax.com/cnn-us-politics/2019/07/31/us-sanctions-iranian-foreign-minister-zarif/')],
 209: [_s('Pompeo blames Iran for strike on Saudi oil facilities', 'CBS News', '2019-09-14', 'https://www.cbsnews.com/news/yemen-drones-hit-saudi-oil-sites-including-key-chokepoint-abqaiq-aramco-2019-09-14/'),
       _s('US blames Iran after attacks on Saudi oil facilities cripple production', 'Times of Israel', '2019-09-14', 'https://www.timesofisrael.com/us-blames-iran-after-attacks-on-saudi-oil-facilities-cripple-production/')],
 210: [_s("US sanctions Iran's central bank in wake of Aramco attacks", 'Al Jazeera', '2019-09-20', 'https://www.aljazeera.com/economy/2019/9/20/us-sanctions-irans-central-bank-in-wake-of-aramco-attacks')],
 211: [_s('Trump sends troops to Middle East after attack on Saudi oil facilities', 'NPR', '2019-09-20', 'https://www.npr.org/2019/09/20/762935873/trump-sends-troops-to-middle-east-after-attack-on-saudi-oil-facilities'),
       _s('U.S. to send troops to Saudi Arabia', 'Axios', '2019-09-20', 'https://www.axios.com/2019/09/20/us-troops-deploying-saudi-arabia')],
 212: [_AJ_K1, _TWZ_K1],
 213: [_AJ_K1, _TWZ_K1],
 214: [_s('Iraqi mourners try to storm US embassy after airstrikes', 'AP (via NBC Washington)', '2019-12-31', 'https://www.nbcwashington.com/news/national-international/iraqi-mourners-try-to-storm-us-embassy-after-airstrikes')],
 215: [_s("Iran's Qassem Soleimani killed in US air raid at Baghdad airport", 'Al Jazeera', '2020-01-03', 'https://www.aljazeera.com/news/2020/1/3/irans-qassem-soleimani-killed-in-us-air-raid-at-baghdad-airport'),
       _s('US drone strike kills top Iranian general', 'AP (Best of the Week page)', '2020-01-03', 'https://leads.svcs.associatedpress.com/best-of-the-week/us-drone-strike-kills-top-iranian-general')],
 216: [_s('Iran launches missile attacks on US facilities in Iraq', 'Al Jazeera', '2020-01-08', 'https://www.aljazeera.com/amp/news/2020/1/8/iran-launches-missile-attacks-on-us-facilities-in-iraq'),
       _s('U.S. awards 29 Purple Hearts for brain injuries in Iran attack', 'PBS NewsHour', '2020', 'https://www.pbs.org/newshour/amp/nation/u-s-awards-29-purple-hearts-for-brain-injuries-in-iran-attack')],
 217: [_s("U.S. Set to Impose Sanctions on Iran's Metal Exports and Leaders", 'Bloomberg', '2020-01-10', 'https://www.bloomberg.com/news/articles/2020-01-10/u-s-set-to-impose-sanctions-on-iran-s-metal-exports-and-leaders')],
 218: [_STR_TAJI],
 219: [_STR_TAJI],
 220: [_s('Iraq officials: Rocket attack hits base housing US troops', 'AP (via News4Jax)', '2020-03-14', 'https://www.news4jax.com/news/2020/03/14/iraq-officials-rocket-attack-hits-base-housing-us-troops/', 'full text')],
 221: [_s('US says it seized 4 Iranian fuel shipments headed for Venezuela', 'Al Jazeera', '2020-08-15', 'https://www.aljazeera.com/news/2020/8/15/us-says-it-seized-4-iranian-fuel-shipments-headed-for-venezuela'),
       _s('U.S. Seizes Four Tankers Carrying Iranian Oil to Venezuela', 'Bloomberg', '2020-08-14', 'https://www.bloomberg.com/news/articles/2020-08-14/u-s-seizes-four-tankers-carrying-iranian-oil-to-venezuela')],
 222: [_s('U.S. bombs facilities in Syria used by Iran-backed militia', 'AP (via Las Vegas Sun)', '2021-02-25', 'https://lasvegassun.com/news/2021/feb/25/us-bombs-facilities-in-syria-used-by-iran-backed-m/')],
 223: [_STR_21],
 224: [_STR_21, _s('US troops in Syria attacked after airstrikes on militias', 'AP (via News4Jax)', '2021-06-28', 'https://www.news4jax.com/news/politics/2021/06/28/us-troops-in-syria-attacked-after-airstrikes-on-militias/')],
 225: [_PBS_22, _s("US carries out raids in Syria on 'Iran-linked' targets", 'Al Jazeera', '2022-08-24', 'https://www.aljazeera.com/news/2022/8/24/us-military-carries-out-raids-in-syria-on-iran-linked-targets')],
 226: [_PBS_22],
 227: [_ABC_23, _s('US military carries out airstrikes in Syria after drone attack kills American contractor', 'ABC News (via ABC11)', '2023-03-23', 'https://abc11.com/syria-airstrike-us-drone-attack-american-contractor-killed-service-members/13001155/')],
 228: [_ABC_23],
 229: [_ABC_23],
 230: [_s("Iran seizes oil tanker 'trying to flee' in Gulf waters", 'Al Jazeera', '2023-04-27', 'https://www.aljazeera.com/news/2023/4/27/iran-seizes-oil-tanker-trying-to-flee-in-gulf-waters'),
       _s('Why did Iran seize a US-bound oil tanker in the Gulf of Oman?', 'Al Jazeera', '2023-04-29', 'https://www.aljazeera.com/news/2023/4/29/why-did-iran-seize-a-us-bound-oil-tanker-in-the-gulf-of-oman')],
 231: [_s('U.S. Sending Destroyer, F-35s, F-16s to Protect Merchant Ships in Middle East', 'USNI News', '2023-07-17', 'https://news.usni.org/2023/07/17/u-s-sending-destroyer-f-35s-f-16s-to-protect-merchant-ships-in-middle-east'),
       _s('US to send F-16 fighter jets to Gulf amid Iran shipping tensions', 'Al Jazeera', '2023-07-15', 'https://www.aljazeera.com/news/2023/7/15/us-to-send-f-16-fighter-jets-to-gulf-amid-iran-shipping-tensions')],
 232: [_s('US makes deal with Iran to swap prisoners and release $6 billion in frozen Iranian funds', 'AP (via NBC Miami)', '2023-09-11', 'https://www.nbcmiami.com/news/national-international/us-makes-deal-with-iran-to-swap-prisoners-and-release-6-billion-in-frozen-iranian-funds/3109532/?amp=1'),
       _s("What's happening with the Iran-US prisoner swap deal?", 'Al Jazeera', '2023-09-12', 'https://www.aljazeera.com/news/2023/9/12/whats-happening-with-the-iran-us-prisoner-swap-deal')],
 233: [_s('U.S. strikes Iran-linked sites in Syria after attacks on American troops', 'Axios', '2023-10-27', 'https://www.axios.com/2023/10/27/us-strikes-syria-iran-linked-groups')],
 234: [_s("US hits alleged Iran-linked 'weapons storage' facility in Syria", 'Al Jazeera', '2023-11-09', 'https://www.aljazeera.com/amp/news/2023/11/9/us-hits-alleged-iran-linked-weapons-storage-facility-in-syria')],
 235: [_s('U.S. launches retaliatory strikes after drone attack on Iraq military base wounds 3 U.S. service members', 'CBS News', '2023-12-25', 'https://www.cbsnews.com/amp/texas/news/drone-attack-iraq-military-base-3-u-s-service-members-wounded-kataib-hezbollah-retaliatory-strikes')],
 236: [_s('US launches strikes on Iraq over drone attack blamed on Iran-aligned forces', 'Al Jazeera', '2023-12-26', 'https://www.aljazeera.com/amp/news/2023/12/26/us-strikes-iraq-after-blaming-iran-backed-groups-for-drone-attack'),
       _s('U.S. launches retaliatory strikes after drone attack on Iraq military base wounds 3 U.S. service members', 'CBS News', '2023-12-25', 'https://www.cbsnews.com/amp/texas/news/drone-attack-iraq-military-base-3-u-s-service-members-wounded-kataib-hezbollah-retaliatory-strikes')],
 237: [_s('U.S. drone strike kills Iran-backed commander in Iraq amid escalating regional violence', 'NPR (via KGOU)', '2024-01-04', 'https://www.kgou.org/2024-01-04/u-s-drone-strike-kills-iran-backed-commander-in-iraq-amid-escalating-regional-violence')],
 238: [_s('What we know about drone attack that killed US troops in Jordan', 'Al Jazeera', '2024-01-29', 'https://www.aljazeera.com/amp/video/newsfeed/2024/1/29/what-we-know-about-drone-attack-that-killed-us-troops-in-jordan')],
 239: [_AJ_KH, _s("Iraq's Kataeb Hezbollah faction suspends attacks on US forces", 'Times of Israel', '2024-01-30', 'https://www.timesofisrael.com/iraqs-kataib-hezbollah-faction-suspends-attacks-on-us-forces/')],
 240: [_s('AP Report: U.S. begins retaliatory strikes on militias in Iraq and Syria, officials say', 'AP (via PBS NewsHour)', '2024-02-02', 'https://www.pbs.org/newshour/world/ap-report-u-s-begins-retaliatory-strikes-on-militias-in-iraq-and-syria-officials-say'),
       _s('US Strikes More Than 85 Targets in Iraq and Syria, Centcom Says', 'Bloomberg', '2024-02-02', 'https://www.bloomberg.com/news/articles/2024-02-02/us-strikes-more-than-85-targets-in-iraq-and-syria-centcom-says')],
 241: [_PBS_24],
 242: [_s('Paramilitary commander killed in Baghdad drone strike: Reports', 'Al Jazeera', '2024-02-07', 'https://www.aljazeera.com/news/2024/2/7/paramilitary-commander-killed-in-baghdad-drone-strike-reports')],
 243: [_s('Iran launches hundreds of missiles, drones in first direct attack on Israel', 'Al Jazeera', '2024-04-13', 'https://www.aljazeera.com/news/2024/4/13/israeli-army-says-iran-has-launched-drones-at-israel')],
 244: [_s("U.S. and UK sanction Iranian firms involved in drone production in response to Tehran's attack on Israel", 'AP (via ABC News)', '2024-04-18', 'https://abcnews.go.com/US/wireStory/us-uk-sanction-iranian-firms-involved-drone-production-109380429')],
 245: [_s('Iran fires dozens of missiles at Israel', 'Al Jazeera', '2024-10-01', 'https://www.aljazeera.com/video/newsfeed/2024/10/1/iran-fires-dozens-of-missiles-at-israel')],
 246: [_s('US deploying THAAD missile defence system, troops to Israel', 'Al Jazeera', '2024-10-13', 'https://www.aljazeera.com/news/2024/10/13/us-deploying-thaad-missile-defence-system-troops-to-israel'),
       _s('U.S. sending THAAD missile system and troops to operate it to Israel', 'Axios', '2024-10-13', 'https://www.axios.com/2024/10/13/us-send-thaad-missile-israel')],
 247: [_s("Where does Trump's renewed 'maximum pressure' leave any Iran-US deal?", 'Al Jazeera', '2025-02-06', 'https://www.aljazeera.com/news/2025/2/6/where-does-trumps-renewed-maximum-pressure-leave-any-iran-us-deal')],
 248: [_s('Trump envoy, Iranian foreign minister meet in first round of nuclear talks', 'Axios', '2025-04-12', 'https://www.axios.com/2025/04/12/us-iran-begin-nucearl-talks-begin-oman?stream=top'),
       _s('Iran-US talks in Oman live: Delegations to hold nuclear discussions', 'Al Jazeera', '2025-04-12', 'https://www.aljazeera.com/amp/news/liveblog/2025/4/12/iran-us-talks-in-oman-live-delegations-to-hold-nuclear-discussions')],
 249: [_s('Iran, US report progress in nuclear talks, confirm third round next week', 'Al Jazeera', '2025-04-19', 'https://www.aljazeera.com/news/2025/4/19/iran-says-progress-in-nuclear-talks-with-us-confirms-third-round-next-week')],
 250: [_s('Iran, US report progress in nuclear talks, confirm third round next week', 'Al Jazeera', '2025-04-19', 'https://www.aljazeera.com/news/2025/4/19/iran-says-progress-in-nuclear-talks-with-us-confirms-third-round-next-week')],
 251: [_s("Iran and US conclude a fourth round of negotiations over Tehran's nuclear program in Oman", 'AP (via AOL)', '2025-05-11', 'https://www.aol.com/iran-us-begin-4th-round-094046088.html')],
 252: [_s('Iran sees hope for progress after fifth round of nuclear talks with US', 'Al Jazeera', '2025-05-23', 'https://www.aljazeera.com/news/2025/5/23/red-lines-stalk-fifth-round-of-iran-us-nuclear-talks')],
 253: [_s("Live: Israel warns 'Tehran will burn' after deadly missile barrage by Iran", 'Al Jazeera', '2025-06-14', 'https://www.aljazeera.com/news/liveblog/2025/6/14/live-israel-warns-tehran-will-burn-after-deadly-missile-barrage-by-iran')],
 254: [_s("Live: Israel warns 'Tehran will burn' after deadly missile barrage by Iran", 'Al Jazeera', '2025-06-14', 'https://www.aljazeera.com/news/liveblog/2025/6/14/live-israel-warns-tehran-will-burn-after-deadly-missile-barrage-by-iran')],
 255: [_s("US bombs Iran's nuclear sites: What we know so far", 'Al Jazeera', '2025-06-22', 'https://www.aljazeera.com/news/2025/6/22/us-bombs-irans-nuclear-sites-what-we-know-so-far'),
       _s("Live: US joins Israel's attacks on Iran, bombs three nuclear sites", 'Al Jazeera', '2025-06-22', 'https://www.aljazeera.com/news/liveblog/2025/6/22/live-us-joins-israels-attacks-on-iran-bombs-three-nuclear-sites')],
 256: [_AJ_UDEID],
 257: [_AJ_UDEID, _s('Trump claims ceasefire reached between Israel and Iran', 'Al Jazeera', '2025-06-23', 'https://aljazeera.com/news/2025/6/23/trump-claims-ceasefire-reached-between-israel-and-iran')],
 258: [_s("US says sanctions hit Iran 'shipping empire' linked to top Tehran official", 'Al Jazeera', '2025-07-31', 'https://www.aljazeera.com/amp/news/2025/7/31/us-says-sanctions-hit-iran-shipping-empire-linked-to-top-tehran-official')],
 259: [_s("Live: US, Iran ratchet up rhetoric as 'big armada' forms in the Middle East", 'Al Jazeera', '2026-01-27', 'https://www.aljazeera.com/amp/news/liveblog/2026/1/27/live-us-iran-ratchet-up-rhetoric-as-big-armada-forms-in-the-middle-east')],
 260: [_s('US-Iran talks live: Critical negotiations set to begin in Oman', 'Al Jazeera', '2026-02-06', 'https://www.aljazeera.com/amp/news/liveblog/2026/2/6/us-iran-talks-live-critical-negotiations-set-to-begin-in-oman')],
 261: [_s('Trump orders second aircraft carrier to Middle East', 'Al Jazeera', '2026-02-13', 'https://www.aljazeera.com/video/newsfeed/2026/2/13/trump-orders-second-aircraft-carrier-to-middle-east')],
 262: [_s('Iran-US Nuclear Talks Set to Resume in Geneva on Feb. 26', 'Bloomberg Government', '2026-02', 'https://news.bgov.com/states-of-play/iran-us-nuclear-talks-set-to-resume-in-geneva-on-feb-26-1')],
}
VERDICT = {k: 'confirmed' for k in SOURCES}
# Rows where an allowed outlet confirms the event but not every detail in the row.
PARTLY = set()

# Trigger Census rows for pre-war US moves (window: ~5 days for a reply).
# Category = what the move cost the other side; Status as in data.py, plus "R-proxy".
CENSUS = [
 (206, "Economic/Blockade", "N", "Khamenei sanctions, Jun 24, 2019. No Iranian attack on US forces or ships found Jun 25-29."),
 (208, "Economic/Blockade", "N", "Zarif sanctions, Jul 31, 2019. No Iranian attack on US forces or ships found Aug 1-5. Iran seized a small Iraqi fuel-smuggling tanker on Aug 4 (Al Jazeera, https://www.aljazeera.com/news/2019/08/iranian-forces-capture-foreign-tanker-smuggling-fuel-state-tv-190804090043971.html), not aimed at the US."),
 (210, "Economic/Blockade", "N", "Central-bank sanctions, Sep 20, 2019. No Iranian attack found Sep 21-25."),
 (213, "Personnel/Casualty", "R-proxy", "Strikes on Kataib Hezbollah (about 25 killed), Dec 29, 2019 -> militia supporters storm the US embassy compound Dec 31 (AP). Reply by an Iran-backed group."),
 (215, "Personnel/Casualty", "R-strong", "Soleimani killed, Jan 3, 2020 -> Iran fires ballistic missiles at Ain al-Asad and Erbil, Jan 8, and calls it revenge for Soleimani."),
 (217, "Economic/Blockade", "N", "Metals sanctions, Jan 10, 2020. Iran stood down after Jan 8; no attack found Jan 11-15."),
 (219, "Military/Property", "R-proxy", "Strikes on Kataib Hezbollah weapons sites, Mar 12, 2020 -> 25+ rockets hit Camp Taji Mar 14, wounding 3 US troops (AP). No group named; timing only."),
 (221, "Economic/Blockade", "N", "Seizure of four Iranian fuel cargoes, Aug 14, 2020. Iran denied owning them; no Iranian action found Aug 15-19."),
 (222, "Military/Property", "N", "Strikes in Syria, Feb 25, 2021. The next attack on US forces was the Mar 3 rocket attack on Ain al-Asad (#263, CBS, NPR), 6 days later: outside the 5-day window."),
 (223, "Military/Property", "R-proxy", "Strikes near the Iraq-Syria border, Jun 27, 2021 -> rockets at US forces in eastern Syria Jun 28, no injuries (Stars and Stripes). Timing only."),
 (225, "Military/Property", "R-proxy", "Strikes on militia bunkers in Deir ez-Zor, Aug 24, 2022 -> militia rockets hit two US bases within hours, 3 troops treated for minor injuries (AP)."),
 (228, "Military/Property", "R-proxy", "Strikes on IRGC-affiliated facilities, Mar 23, 2023 -> rockets and drones at US bases Mar 24, 1 US service member wounded (ABC)."),
 (240, "Military/Property", "R-proxy", "85+ targets struck in Iraq and Syria, Feb 2, 2024 -> Islamic Resistance in Iraq drone kills 6 US-allied Kurdish fighters at al-Omar base Feb 4 (AP)."),
 (242, "Personnel/Casualty", "N", "Kataib Hezbollah commander killed, Feb 7, 2024. The group had paused attacks on Jan 30 and no attack on US forces is logged Feb 8-12."),
 (244, "Economic/Blockade", "N", "Drone-program sanctions, Apr 18, 2024. No Iranian attack on US forces found Apr 19-23."),
 (247, "Economic/Blockade", "N", "'Maximum pressure' restored, Feb 4, 2025. No Iranian attack found Feb 5-9."),
 (255, "Military/Property", "R-strong", "Operation Midnight Hammer, Jun 22, 2025 -> Iran fires 19 missiles at Al Udeid, Jun 23; one hit, no casualties; Trump said Iran gave 'early notice' (Al Jazeera)."),
 (258, "Economic/Blockade", "N", "Shipping-network sanctions, Jul 30, 2025. No Iranian attack found Jul 31-Aug 4."),
]

# Reply pairs (pair id, trigger, reply, category, reply caused casualties Y/N, note)
PAIRS = [
 (26, 212, 213, "Personnel/Casualty", "Y", "US answers the deadly K-1 rocket attack with strikes on Kataib Hezbollah two days later"),
 (27, 213, 214, "Personnel/Casualty", "N", "Militia supporters storm the US embassy compound two days after the strikes"),
 (28, 215, 216, "Personnel/Casualty", "Y", "Iran's missile revenge for Soleimani: no deaths, but more than 100 US troops with brain injuries"),
 (29, 218, 219, "Personnel/Casualty", "N", "US strikes Kataib Hezbollah the day after two US troops are killed at Taji"),
 (30, 219, 220, "Military/Property", "Y", "Rockets hit Taji again two days after the US strikes (no group named)"),
 (31, 223, 224, "Military/Property", "N", "Rockets at US forces in Syria the day after strikes on militia facilities"),
 (32, 225, 226, "Military/Property", "Y", "Militia rockets hit two US bases within hours of the US strikes"),
 (33, 227, 228, "Personnel/Casualty", "N", "US strikes IRGC-affiliated facilities hours after a drone kills a US contractor"),
 (34, 228, 229, "Military/Property", "Y", "Rockets and drones at US bases the day after the US strikes"),
 (35, 238, 240, "Personnel/Casualty", "N", "US strikes 85+ targets five days after three US soldiers are killed at Tower 22"),
 (36, 240, 241, "Military/Property", "Y", "Iran-backed group's drone kills 6 US-allied fighters two days after the US strikes"),
 (37, 255, 256, "Military/Property", "N", "Iran answers the strikes on its nuclear sites with a telegraphed missile attack on Al Udeid"),
]

# Continuous-fighting windows (US strikes inside are context only) and the acts that started them
WINDOWS = [(d(2023, 10, 17), d(2024, 1, 29)), (d(2025, 6, 13), d(2025, 6, 24))]
START_ACTS = {255}

# Pre-war phases (oldest first)
PHASES = [
 ("Maximum-pressure crisis", d(2019, 5, 5), d(2020, 3, 31), "#201 carrier and bombers sent; tanker attacks, drone shootdown, Abqaiq, Soleimani (#215) and Iran's missile revenge (#216)"),
 ("Shadow conflict", d(2020, 4, 1), d(2025, 6, 12), "Sanctions, tanker seizures and tit-for-tat strikes with Iran-backed militias in Iraq and Syria; talks in 2023 and 2025"),
 ("Twelve-day war", d(2025, 6, 13), d(2025, 6, 24), "#253 Israel strikes Iran; #255 US bombs nuclear sites; #256 Iran hits Al Udeid; #257 ceasefire"),
 ("Pre-war standoff", d(2025, 6, 25), d(2026, 2, 27), "Sanctions, a US buildup (#259, #261) and talks (#260, #262) before the 2026 war"),
]

CHAIN_NAMES = {
 203: "Tanker attacks -> more US troops",
 205: "Drone shootdown -> Khamenei sanctions",
 209: "Abqaiq attack -> sanctions and troops for Saudi Arabia",
 212: "K-1 attack -> strikes -> embassy -> Soleimani -> Iran's missile revenge -> sanctions",
 218: "Taji attack -> US strikes -> Taji hit again",
 223: "Border strikes -> rockets in Syria",
 225: "Deir ez-Zor strikes -> rockets at US bases",
 227: "Contractor killed -> US strikes -> more rockets",
 235: "Erbil drone attack -> US strikes (militia campaign, context)",
 238: "Tower 22 -> pause announced -> 85 targets -> al-Omar drone",
 243: "Iran's first direct attack on Israel -> drone-program sanctions",
 245: "Iran's missiles at Israel -> THAAD to Israel",
 253: "Twelve-day war -> Midnight Hammer -> Al Udeid -> ceasefire",
}
