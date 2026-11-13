"""NAPOR action tags: the six settings a viewer can fill in on the page ("If the US did this...") and the words that
describe every past US-action case, so the page's matcher can find past cases like a viewer's action without AI.

Owner rule (2026-11-06): every counted US-action case (not hold weeks) carries tags. Tags describe WHAT THE US DID
(method, target, place, scale, partners, openness), never what happened after. They come from the event's own title,
kind and linked sources. A case whose tags are a judgment call says so in `why`.

Tag files: napor/tags/<theater>.py, each with TAGS = {event id: dict(move=..., target=[...], where=..., scale=...,
who=..., open=..., why="one short line")}. `target` is a list (an action can hit more than one kind of target);
the other fields are one value each. Use "none" where a field does not apply (talks have no target or place).

The page uses SYNONYMS to read words a viewer types in a setting's text box ("bombing" -> strike). Unknown words are
shown to the viewer as ignored, never guessed.
"""

FIELDS = ["move", "target", "where", "scale", "who", "open"]

LABELS = {
    "move": "Type of move", "target": "Target", "where": "Location", "scale": "Scale", "who": "Who acts", "open": "Open or covert",
}

# field -> {value: plain label shown on the page}
VOCAB = {
    "move": {
        "strike": "Air, missile or drone strike",
        "raid": "Ground raid or special-forces operation",
        "naval": "Naval action (blockade, boarding, seizure, transit, escort, interdiction)",
        "deployment": "Deploy forces or weapons (incl. missile defense, bombers, carriers)",
        "withdrawal": "Withdraw or reduce forces",
        "drill": "Military exercise or drill",
        "sanctions": "Sanctions or export controls",
        "legal": "Legal step (terror listing, indictment, bounty, court case)",
        "arms": "Arms sale or transfer to a partner",
        "talks": "Talks, negotiation, deal or ceasefire",
        "visit": "Official visit or high-level contact",
        "statement": "Statement, warning or ultimatum",
        "cyber": "Cyber operation",
        "other": "Other",
    },
    "target": {
        "equipment": "Military equipment and sites (radars, launchers, bases)",
        "personnel": "Military personnel or fighters",
        "leaders": "Leaders or commanders",
        "economy": "Oil, banks, companies or the economy",
        "shipping": "Commercial shipping or tankers",
        "boats": "Small boats",
        "nuclear": "Nuclear or missile programs",
        "proxy": "A proxy or partner group of the adversary",
        "officials": "Named officials or individuals",
        "none": "No target",
    },
    "where": {
        "adversary": "Inside the adversary's country",
        "proxy": "A proxy's territory",
        "sea": "At sea or in international airspace",
        "third": "A third country (an ally's or neighbor's territory)",
        "none": "No physical place (e.g. sanctions, talks, statements)",
    },
    "scale": {
        "single": "One action",
        "campaign": "A campaign over several days or a series",
    },
    "who": {
        "alone": "The US alone",
        "allies": "With Israel or other allies",
        "partners": "Through partners (local forces, other states acting for the US)",
    },
    "open": {
        "announced": "Announced or claimed by the US",
        "unclaimed": "Unclaimed or covert",
    },
}

# words a viewer might type -> (field, value). Lower-case; matched as whole words or short phrases.
SYNONYMS = {
    "move": {   # one-word or short cue words (lowest priority, "tier 3" in CUES below). A word may sit under two moves when it is ambiguous.
        "strike": ["strike", "airstrike", "air strike", "bomb", "bombard", "bombardment", "missile", "rocket", "drone", "attack", "assault", "hit", "shell", "shelling", "tomahawk", "destroy", "blast", "kill", "obliterate"],
        "raid": ["raid", "special forces", "commando", "ground operation", "capture", "snatch", "rescue", "invade", "invasion", "incursion"],
        "naval": ["naval", "navy", "blockade", "boarding", "board", "interdict", "interdiction", "fonop", "freedom of navigation", "escort", "quarantine", "warship", "destroyer", "seizure", "maritime"],
        "deployment": ["deploy", "deployment", "station", "carrier", "bomber", "patriot", "thaad", "reinforce", "buildup", "build-up", "troops", "marines", "advisers", "advisors", "garrison", "battery", "missile defense", "missile defence", "air defense", "air defence", "warship", "surge", "interceptor"],
        "withdrawal": ["withdraw", "withdrawal", "pullout", "pull out", "drawdown", "draw down", "evacuate", "evacuation"],
        "drill": ["drill", "exercise", "war games", "war game", "wargame", "maneuvers", "manoeuvres"],
        "sanctions": ["sanction", "embargo", "export control", "tariff", "freeze", "asset freeze", "blacklist", "penalty", "ofac", "sdn"],
        "legal": ["designate", "designation", "terror listing", "fto", "sdgt", "indict", "indictment", "bounty", "charge", "lawsuit", "court", "prosecute", "warrant", "reward", "extradition"],
        "arms": ["arms sale", "arms", "weapons sale", "arms deal", "military aid", "arms transfer", "security assistance", "arm"],
        "talks": ["talks", "negotiate", "negotiation", "deal", "ceasefire", "truce", "summit", "agreement", "diplomacy", "mediation", "treaty", "dialogue", "call", "phone call", "say", "discussion"],
        "visit": ["visit", "meeting", "meet", "phone call", "call", "phone", "delegation", "contact", "stopover", "layover"],
        "statement": ["statement", "warn", "warning", "threat", "threaten", "ultimatum", "deadline", "speech", "announce", "declare", "say", "tweet", "twitter", "truth social", "pledge", "vow"],
        "cyber": ["cyber", "hack", "hacker", "cyberattack", "cyber attack", "malware", "ransomware"],
    },
    "target": {
        "equipment": ["radar", "radars", "launcher", "launchers", "base", "bases", "air defense", "military site", "military sites", "weapons", "depot", "airfield"],
        "personnel": ["troops", "soldiers", "fighters", "personnel", "irgc", "militia", "forces"],
        "leaders": ["leader", "commander", "general", "president", "regime", "maduro", "kim", "khamenei", "ayatollah", "supreme leader", "dictator", "tsai", "soleimani"],
        "economy": ["oil", "economy", "bank", "banks", "company", "companies", "refinery", "exports", "port", "ports", "energy", "power grid", "infrastructure"],
        "shipping": ["shipping", "ship", "ships", "tanker", "tankers", "cargo", "vessel", "vessels", "freighter"],
        "boats": ["boat", "boats", "speedboat", "speedboats", "drug boat", "fast boats"],
        "nuclear": ["nuclear", "enrichment", "uranium", "fordow", "natanz", "isfahan", "centrifuge", "reactor", "yongbyon", "warhead", "atomic", "missile program", "icbm"],
        "proxy": ["proxy", "proxies", "houthi", "houthis", "hezbollah", "militias"],
        "officials": ["official", "officials", "individuals", "minister", "ministers"],
    },
    "where": {
        "adversary": ["inside", "mainland", "homeland", "in iran", "in venezuela", "in north korea", "in china", "in yemen", "on land", "territory", "soil", "interior", "domestic", "within"],
        "proxy": ["proxy territory", "iraq", "syria", "lebanon", "yemen"],
        "sea": ["sea", "at sea", "strait", "gulf", "red sea", "caribbean", "waters", "international waters", "airspace", "ocean", "coast", "coastal", "offshore", "maritime"],
        "third": ["third country", "ally", "allied", "jordan", "bahrain", "qatar", "japan", "south korea", "taiwan", "philippines", "colombia"],
    },
    "scale": {
        "single": ["one", "single", "once", "one-off", "limited", "one strike", "small", "minor", "brief", "short", "quick", "onetime", "narrow"],
        "campaign": ["campaign", "series", "several days", "weeks", "sustained", "waves", "operation", "big", "large", "major", "massive", "huge", "extended", "prolonged", "long", "ongoing", "broad", "wide", "multi day"],
    },
    "who": {
        "alone": ["alone", "us only", "unilateral", "by itself", "solo", "ourselves", "on our own", "by ourselves"],
        "allies": ["israel", "israeli", "allies", "ally", "uk", "britain", "nato", "coalition", "with allies", "joint", "friends", "friend", "friendly", "buddies"],
        "partners": ["partners", "proxy forces", "local forces", "through partners", "via partners"],
    },
    "open": {
        "announced": ["announced", "open", "public", "claimed", "overt", "declared", "acknowledged", "loud"],
        "unclaimed": ["covert", "secret", "unclaimed", "un claimed", "deniable", "hidden", "quiet", "sneaky", "sneak", "stealth", "stealthy", "undisclosed", "unannounced", "anonymous", "clandestine", "discreet", "in secret"],
    },
}

# ---- Reading the move from a typed description ("Your own option" matcher, v2) ----
# CUES say which Type-of-move values a description clearly points to. They are the matcher's only HARD rule for the
# description: a clear cue keeps only cases whose move is in `moves`; no cue means no move filter (the word-meaning
# model then ranks everything). Cue rows are tried in tiers: tier 1 (specific phrases, e.g. "pull troops out") beats
# tier 2 (a verb plus an object, e.g. "send ... carrier") beats tier 3 (one cue word, the SYNONYMS["move"] lists above);
# tier 0 is only for acts that no move fits (the filter is then empty, so nothing matches).
# Only the best tier that matched counts; inside that tier every matched row adds its moves (an ambiguous act keeps
# both moves and lets closeness decide). The Type-of-move BOX reads every move it names instead (a union, no tiers).
# The same list is exported to the page; napor/matcher_ref.py is the Python twin.
# Phrase language (lower-case words; a trailing * means "any ending"): `a|b` = either word, `...` = up to 4 words in between,
# the words must come in this order. Example: "pull ... out|back|down" matches "pull troops out" and "pull back".
# Words are compared after simple stemming (strikes, striking, struck -> strike), see LANG["irregular"].
# A row with relief=True is a "sanctions relief" act: the cases kept for sanctions or legal moves must be relief cases (LANG relief words).
# Moves are chosen with the log's own tagging habits in mind: sanctions relief, ceasefires and "restore relations" are
# tagged talks, so those cues keep talks (and sanctions) in.
_OBJ_FORCES = "troop*|force*|soldier*|personnel|presence|footprint|staff|garrison*|deployment*|contingent|marines|advisers|advisors"
_OBJ_ASSETS = "troop*|force*|soldier*|marines|carrier*|warship*|ship*|bomber*|aircraft|jet*|fighter*|destroyer*|submarine*|advisers|advisors|personnel|batter*|defense|defence|patriot*|thaad|system*|missile*|radar*|assets|weapons|reinforcements|fleet|navy|capabilit*|interceptor*"
_OBJ_ARMS = "weapon*|arms|missile*|batter*|patriot*|thaad|jet*|aircraft|fighter*|tank*|ammunition|munition*|drone*|equipment|system*|artillery|helicopter*|rocket*|bomb*|interceptor*"
_OBJ_SHIPS = "ship*|tanker*|vessel*|boat*|cargo*|freighter*|shipment*|container*"
_OBJ_TRADE = "export*|import*|sale*|sell*|purchase*|buy*|trade|oil|chip*|technolog*|invest*|financ*|bank*|crude|gas|energy|supplies|payment*|transaction*|travel|visa*|shipment*|revenue|money|funding|funds"
_RELIEF = "lift*|eas*|relax*|remov*|suspend*|waiv*|roll*|drop*|scrap*|loosen*|repeal*|revok*|rescind*|unfreez*|releas*|end|reduc*|cut*|relief"
_SANC = "sanction*|embargo*|tariff*|restriction*|penalt*|curbs|ban|bans|controls"
_LEADER = "leader*|general*|commander*|chief*|head|scientist*|official*|minister*|president|supreme|ayatollah|khamenei|soleimani|kingpin|boss|dictator|maduro|kim"
_TERROR = "terror*|fto|sdgt|sponsor*"
_PLACES_US = "york|california|angeles|francisco|washington|hawaii|texas|houston|boston|chicago|miami|alaska|guam|america|american|united"
_COUNTRY_END = "iraq|syria|afghanistan|region|base|bases|country|korea|japan|yemen|gulf|bahrain|qatar|kuwait|jordan|saudi|east"
CUES = [
    # --- tier 0: acts no log row is tagged as (nothing can match, and the page says so) ---
    dict(p=0, moves=[], phrases=["leav*|exit*|quit*|abandon*|withdraw*|pull* ... deal|agreement|accord|treaty|jcpoa|pact",
        "kill*|scrap*|torpedo*|ruin*|wreck*|sabotag*|void* ... deal|agreement|accord|treaty|jcpoa|pact|ceasefire|truce",
        "nuke|nukes|nuked|nuking", "nuclear|atomic ... bomb|bombs|bombing|strike|strikes|attack|attacks"]),
    # --- tier 1: specific phrases ---
    dict(p=1, moves=["withdrawal"], phrases=["pull ... out|back|down|away|home", "pullout", "draw ... down", "drawdown", "withdraw*", "bring ... home|back", "evacuat*",
        "leave|exit|quit ... " + _COUNTRY_END, "get|getting|got|go|going ... out ... " + _COUNTRY_END,
        "reduc*|cut*|scale|scal*|lower|trim|shrink|decreas*|downsiz*|thin ... " + _OBJ_FORCES, "close|shut|abandon ... embass*|consulate*|base|bases|mission"]),
    dict(p=1, moves=["withdrawal", "sanctions"], phrases=["cut|break|sever|end|suspend|downgrad*|expel ... ties|relations|relationship|diplomatic"]),
    dict(p=1, moves=["sanctions", "talks"], relief=True, phrases=[_RELIEF + " ... " + _SANC, "sanctions relief", "relief ... sanction*", "unfreez*|releas* ... funds|assets|money|oil"]),
    dict(p=1, moves=["legal", "sanctions"], relief=True, phrases=["delist*", "take|taking|remov*|drop* ... off|from ... list|designation|terror*", "revok*|rescind*|lift*|end ... designation|listing"]),
    dict(p=1, moves=["sanctions"], phrases=["reimpos*|reinstat*|renew*|reapply*|snap* ... sanction*", "restor* ... sanction*|pressure"]),
    dict(p=1, moves=["arms"], phrases=["arms sale*", "arms transfer*", "arms deal*", "arms package*", "weapons sale*", "military aid", "military assistance", "security assistance",
        "sell*|sale*|transfer*|provid*|suppl*|giv*|donat*|deliver*|export*|approv*|authoriz* ... " + _OBJ_ARMS, "send*|ship*|arm|arms|offer* ... weapon*|arms|ammunition|munition*"]),
    dict(p=1, moves=["strike", "raid"], phrases=["kill*|assassinat*|eliminat*|decapitat*|hunt*|murder* ... " + _LEADER, "take|taking|took ... out ... " + _LEADER]),
    dict(p=1, moves=["raid", "legal"], phrases=["captur*|arrest*|abduct*|seiz*|detain*|snatch* ... " + _LEADER]),
    dict(p=1, moves=["raid"], phrases=["invad*|invasion*|incursion*", "ground ... invasion|operation|offensive|raid|assault|war|campaign"]),
    dict(p=1, moves=["legal", "sanctions"], phrases=["designat*|list*|label*|declar*|classif*|brand* ... " + _TERROR, "designat*", "ofac|sdn|sdgt|fto|blacklist*", "treasury ... list*|sanction*|designat*|action*"]),
    dict(p=1, moves=["sanctions"], phrases=["freez*|froze|frozen|seiz*|block* ... asset*|fund*|money|account*|property|wealth|reserves|deposit*",
        "ban|prohibit*|restrict*|limit*|block*|curb*|cut ... off ... " + _OBJ_TRADE, "ban|prohibit*|restrict*|limit*|curb*|cap|bar|forbid* ... " + _OBJ_TRADE,
        "stop*|halt*|cease*|end|suspend* ... buy|buying|bought|purchas*|import*",
        "hit|hits|hitting|slap*|impos*|levy|levies|raise|raising|hike ... tariff*|sanction*|duties|duty|penalt*", "tariff*|sanction* ... hit|hits|hitting"]),
    dict(p=1, moves=["naval"], phrases=["seiz*|captur*|board*|intercept*|detain*|impound* ... " + _OBJ_SHIPS + "|oil|fuel|crude", "stop* ... " + _OBJ_SHIPS]),
    dict(p=1, moves=["strike", "naval"], phrases=["destroy*|sink*|sunk ... " + _OBJ_SHIPS]),
    dict(p=1, moves=["talks"], phrases=["stop*|halt*|end*|ceas*|suspend*|paus* ... strike*|bomb*|attack*|air*|campaign|war|operation|fighting|hostilit*|raid*", "call ... off ... strike*|bomb*|attack*|campaign|operation",
        "restor*|reopen*|resum*|reestablish*|normaliz*|normalis*|reinstat* ... relations|ties|contact*|embass*|channel*|communication*|dialogue|talks|diplomatic|ambassador*",
        "agree*|reach* ... ceasefire|truce|deal|agreement", "launch*|start*|begin*|open*|initiat*|resum* ... talks|negotiat*|dialogue|discussion*|summit|diplomacy",
        "strike|struck|striking ... deal|agreement|bargain|accord|compromise|truce"]),
    dict(p=1, moves=["drill"], phrases=["cancel*|stop*|halt*|suspend*|end*|postpon*|reduc*|scale|scal*|shrink|cut|curtail* ... drill*|exercise*|war games|wargame*|maneuver*"]),
    dict(p=1, moves=["talks", "statement", "visit"], phrases=["writ*|letter|message|offer*|propos*|invit* ... meet*|talks|negotiat*|dialogue|summit|meeting|engagement"]),
    dict(p=1, moves=["deployment"], phrases=["strike group*|strike force*", "carrier* ... group*"]),
    dict(p=1, moves=["visit"], phrases=["stopover*|layover*|stop over", "stop|stops|stopping|transit*|transiting ... " + _PLACES_US]),
    dict(p=1, moves=["statement"], phrases=["deadline*|ultimatum*|threat*"]),
    # --- tier 2: a verb with its object, or a clear kind of act ---
    dict(p=2, moves=["deployment"], phrases=["send*|deploy*|dispatch*|station*|position*|mov*|bring*|surg*|base*|put|place|install*|increas*|bolster*|reinforc*|boost|add|augment*|fly|flew|stage|forward ... " + _OBJ_ASSETS,
        "missile|air|aerial|anti ... defen*"]),
    dict(p=2, moves=["naval"], phrases=["freedom of navigation", "fonop*",
        "escort*|convoy*|transit*|sail*|navigat*|patrol*|boarding|blockad*|quarantin*|interdict*|block* ... port*|strait|coast|shipping|sea|route*|harbor*|harbour*|warship*|navy|naval|destroyer*|ship*|vessel*|submarine*|channel|canal|waters",
        "through|across ... strait|canal|channel"]),
    dict(p=2, moves=["cyber"], phrases=["cyber*|hack*|malware|ransomware|virus|stuxnet|ddos", "computer network*", "digital attack*"]),
    dict(p=2, moves=["talks", "visit"], phrases=["meet|meeting|meets|visit*|call|phone*|telephone*|speak|summit|invit*|host|welcome|receiv* ... leader*|president|xi|kim|minister*|official*|delegation*|counterpart*"]),
    dict(p=2, moves=["strike", "raid"], phrases=["kill*|assassinat*|eliminat*"]),
    dict(p=2, moves=["drill"], phrases=["hold*|conduct*|launch*|run|start|join*|stage|stag* ... drill*|exercise*|war games|wargame*|maneuver*"]),
]

# ---- the language rules both implementations share (the page reads them from the exported data; napor/matcher_ref.py is the Python twin) ----
# Words are lower-case letters only (digits, hyphens, apostrophes and other characters are separators: "don't" is `don` `t`, "at-sea" is `at` `sea`).
# Negation rows `p` use the same phrase language as CUES (| = either word, * = any ending, words in a row must follow each other with no gap).
#   kind "neg": the words after it (to the next comma/clause break or 8 words) are what the US would NOT do.
#   kind "rev": a reversing verb (lift, stop, cancel...). With a move after it, it names the OPPOSITE of that move (REVMAP); with no move it does nothing.
#   can: it may cancel a "not" right before it ("won't refuse", "don't stop"). adj: it cancels a "not" only when directly next to it ("don't not").
#   solo: it means "hold back" by itself ("stay out", "refrain", "wait and see").
SILENT = ("the a an of to for by with if did does do would from then than is it that this these those some all as be into u s us on in at near onto over off against up "
          "t m d ll re ve").split()
FLUFF = ("take takes took taking make makes made making keep keeps kept keeping go goes going get gets have has had be been being are was were am will shall should "
         "could can may might must we i you they he she our their its his her my your america american americans washington administration government president trump "
         "united states also just only please now and or but any anything more further new additional another other again ever even still simply really actually so too very much "
         "many there here what which who when while such yet gonna gotta wanna lets let".split())
LANG = dict(
    silent=SILENT, fluff=FLUFF,
    leader_words="leader leaders commander commanders general generals regime maduro kim khamenei ayatollah supreme dictator tsai soleimani chief chiefs minister ministers kingpin boss".split(),
    say="say says said declare declares state states announce announces pledge pledges promise promises reaffirm affirm tell tells warn warns reiterate clarify commit vow publicly".split(),
    neg_rows=[
        dict(p="no longer", kind="rev", can=True),
        dict(p="stop|stops|stopping|stopped short of", kind="neg", can=True),
        dict(p="rule|rules|ruled|ruling out", kind="neg", can=True),
        dict(p="hold|holds|holding|held off|back", kind="neg", can=True, solo=True),
        dict(p="stay|stays|staying|stayed|keep|keeps|keeping|kept out|away", kind="neg", can=True, solo=True),
        dict(p="steer|steers|steering clear", kind="neg", can=True, solo=True),
        dict(p="back|backs|backing|backed off", kind="neg", can=True, solo=True),
        dict(p="wait|waits|waiting and see", kind="neg", solo=True),
        dict(p="status quo", kind="neg", solo=True),
        dict(p="stand|stands|standing down", kind="neg", solo=True),
        dict(p="remain|remains|stay|stays|be neutral", kind="neg", solo=True),
        dict(p="exercise|exercises|exercising restraint|caution|patience", kind="neg", solo=True),
        dict(p="restraint", kind="neg", solo=True),
        dict(p="instead of", kind="neg"), dict(p="rather than", kind="neg"), dict(p="in place of", kind="neg"), dict(p="as opposed to", kind="neg"),
        dict(p="other than", kind="neg"), dict(p="apart|aside from", kind="neg"),
        dict(p="than", kind="neg", before="better|prefer|prefers|preferred|preferable|rather|sooner"),
        dict(p="let|lets|letting|leave|leaves|leaving israel|israeli|israelis|netanyahu|idf|others|allies|europe|europeans|saudi|saudis|them|him|her|nato|partners|ukraine|kurds|kurdish", kind="neg"),
        dict(p="refrain*|abstain*|forgo*|forego*|eschew*|forswear*|renounc*", kind="neg", can=True, solo=True),
        dict(p="refus*|avoid*|declin*|shun*|skip*|without", kind="neg", can=True),
        dict(p="lift|lifts|lifted|lifting|ease|eases|eased|easing|relax|relaxes|relaxed|relaxing|remove|removes|removed|removing|suspend|suspends|suspended|suspending", kind="rev", can=True),
        dict(p="withhold|withholds|withheld|withholding|cancel|cancels|canceled|cancelled|canceling|cancelling|halt|halts|halted|halting", kind="rev", can=True),
        dict(p="stop|stops|stopped|stopping|end|ends|ended|ending|curtail*|revok*|rescind*|waive|waives|waived|waiving|repeal*|terminat*|discontinu*|scrap|scraps|scrapped", kind="rev", can=True),
        dict(p="don|doesn|didn|won|can|shouldn|wouldn|couldn|mustn|isn|aren|wasn|weren|hasn|haven|hadn|ain t", kind="neg"),
        dict(p="not|never|no", kind="neg", adj=True),
        dict(p="nothing|neither|nor|dont|doesnt|didnt|wont|cant|cannot|shouldnt|wouldnt|couldnt|mustnt|aint|isnt|arent|wasnt|werent|hasnt|havent|hadnt|unless|except|excluding", kind="neg"),
    ],
    # phrases that LOOK like a negation but are not one (anchored at the cue; back=1: the phrase starts one word before it; start=True: only at the start of a clause)
    not_neg=[
        dict(p="not only|just|merely|simply|to|least|even|bad"), dict(p="no doubt|question|wonder|problem|matter|way|surprise|worries"),
        dict(p="no more|fewer|less|later|sooner|earlier|greater|higher|lower|better|worse than"), dict(p="without delay|warning|notice|hesitation|hesitating|hesitate|waiting|pause|question|doubt|fail|further|exception"),
        dict(p="nothing short of"), dict(p="can|couldn t hurt|harm"), dict(p="cant|couldnt|cannot hurt|harm"),
        dict(p="not|dont|doesnt|didnt|cant|couldnt|shouldnt|wouldnt|wont", pre="why"), dict(p="don|doesn|didn|can|couldn|shouldn|wouldn|won t", pre="why"),
        dict(p="cant|couldnt|shouldnt|wouldnt|wont|dont|didnt|isnt we|us|they|you|i", start=True), dict(p="can|couldn|shouldn|wouldn|won|don|didn|isn t we|us|they|you|i", start=True),
    ],
    # words that are not a move even though a cue word is in them ("labor strike", "oil drilling", "fire the general", "seize the moment")
    nocue=[
        "labor|labour|worker*|union*|hunger|general|rent|dock*|teacher*|nurse*|miner*|trucker*|farmer*|pilot*|rail* ... strike|strikes|striking|struck",
        "oil|gas|water|well|wells|deep|offshore|arctic ... drill|drills|drilling|drilled", "fire|fires|fired|firing|sack*|dismiss*|resign* ... general|official*|adviser*|advisor*|secretary|chief|director|minister|commander|envoy|ambassador|staff",
        "seize|seizes|seized|grab|grabs|miss|missed ... moment|opportunity|day|initiative|chance|lead",
    ],
    # the opposite of a move (what "stop X" or "lift X" asks for): the log's matching kind, or [] = no matching kind (the US holds back)
    revmap=dict(strike=["talks"], raid=["talks"], sanctions=["talks", "sanctions"], legal=["legal", "sanctions"], deployment=["withdrawal"], drill=["drill"]),
    relief_words="lift eas relax waiv relief licens revok rescind delist unfreez suspend remov repeal resum".split(),     # word starts of a sanctions-relief case
    anti_relief_words="restor reimpos reinstat snapback impos".split(),                                                    # ... that mark an imposition instead
    # irregular word forms -> base word (regular endings -s -es -ies -ed -ing -ly are stripped by the matcher itself)
    irregular=dict(struck="strike", sent="send", sold="sell", took="take", taken="take", froze="freeze", frozen="freeze", bought="buy", brought="bring", held="hold", fought="fight",
                   sank="sink", sunk="sink", shot="shoot", led="lead", met="meet", paid="pay", gave="give", given="give", made="make", ran="run", flew="fly", flown="fly", hid="hide",
                   hidden="hide", went="go", left="leave", lost="lose", built="build", kept="keep", knew="know", said="say", told="tell", wrote="write", written="write", spoke="speak",
                   stood="stand", withdrew="withdraw", withdrawn="withdraw", overthrew="overthrow", slain="slay", slew="slay", fled="flee"),
    # small lexicon: a rare word, acronym or operation name -> plain words the matcher and the word model understand (the word itself is kept too)
    lexicon={
        "fordow": "nuclear enrichment site underground", "fordo": "fordow nuclear enrichment site underground", "natanz": "nuclear enrichment site", "isfahan": "nuclear site",
        "bunker buster": "bomb strike underground nuclear site", "bunker busters": "bomb strike underground nuclear site", "bunkerbuster": "bomb strike underground nuclear site",
        "massive ordnance penetrator": "bomb strike underground nuclear site", "mop": "bomb underground", "gbu": "bomb", "jdam": "bomb",
        "midnight hammer": "strike nuclear sites bombers fordow natanz isfahan", "epic fury": "strikes war iran", "rough rider": "strikes houthi campaign",
        "southern spear": "strikes boats caribbean operation", "prosperity guardian": "coalition escort ships red sea",
        "kharg": "kharg island oil terminal", "hormuz": "strait of hormuz", "bab el mandeb": "strait red sea shipping", "bab al mandab": "strait red sea shipping", "mandeb": "strait red sea shipping", "mandab": "strait red sea shipping",
        "thaad": "air missile defense battery deployment", "sm 3": "interceptor missile defense", "sm3": "interceptor missile defense", "patriot": "air missile defense battery", "iron dome": "air missile defense",
        "aegis": "destroyer missile defense", "interceptor": "missile defense",
        "fto": "foreign terrorist organization designation", "sdgt": "terrorist designation", "ofac": "treasury sanctions designation", "sdn": "treasury sanctions designation list",
        "dmz": "demilitarized zone border korea", "rok": "south korea", "dprk": "north korea", "irgc": "revolutionary guard", "pla": "chinese military", "plan": "chinese navy",
        "jcpoa": "nuclear deal agreement talks", "snapback": "sanctions reimposed", "maximum pressure": "sanctions pressure",
        "tsai": "taiwan president", "lai": "taiwan president", "tsai ing wen": "taiwan president", "lai ching te": "taiwan president",
        "key resolve": "joint exercise drill", "foal eagle": "joint exercise drill", "ulchi": "joint exercise drill south korea", "freedom edge": "trilateral exercise drill japan south korea",
        "freedom shield": "joint exercise drill south korea", "balikatan": "exercise drill philippines", "talisman sabre": "exercise drill australia",
        "hodeidah": "hodeidah port", "hudaydah": "hodeidah port", "hudeida": "hodeidah port", "guaido": "venezuela opposition leader recognize", "scarborough": "shoal south china sea philippines",
        "tanf": "base syria", "fujairah": "port uae oil", "kataib": "militia iraq", "pezeshkian": "iranian president", "araghchi": "iranian foreign minister", "witkoff": "envoy talks",
        "matsu": "taiwan island", "penghu": "taiwan island", "kinmen": "taiwan island", "huawei": "chinese technology company export controls", "tiktok": "app ban", "shahed": "drone",
    },
)

# Words that name the theater itself. Every case in a theater is already about it, so these words never filter anything,
# never show as "ignored", and are left out of the word-meaning comparison.
NEUTRAL = {
    "iran": ["iran", "iranian", "iranians", "tehran"],
    "houthis": ["houthi", "houthis", "yemen", "yemeni", "yemenis", "ansar", "ansarallah", "sanaa"],
    "northkorea": ["dprk", "north", "korea", "korean", "koreans", "pyongyang"],
    "china": ["china", "chinese", "prc", "beijing"],
    "venezuela": ["venezuela", "venezuelan", "venezuelans", "caracas"],
}

# Words that name the adversary itself (not its adjective): "bomb Venezuela", "strike Iran" ask for force on its own ground.
ADVERSARY = {
    "iran": ["iran", "tehran"],
    "houthis": ["houthi", "houthis", "yemen", "sanaa"],
    "northkorea": ["dprk", "pyongyang"],
    "china": ["china", "beijing", "prc"],
    "venezuela": ["venezuela", "caracas"],
}

# Place words: a place a past case happened at is weak evidence of what kind of action it was, so these count for less in the word-meaning
# comparison (a viewer's "in the Strait of Hormuz" must not push a clear match under the "nothing" cut-off).
PLACES = {
    "iran": ["hormuz", "gulf", "persian", "bushehr", "bandar", "abbas", "qeshm", "caspian", "oman", "strait", "iraq", "syria", "baghdad", "lebanon"],
    "houthis": ["red", "sea", "bab", "mandeb", "mandab", "aden", "marib", "saada", "hodeidah", "strait", "saudi", "arabia", "oman", "djibouti"],
    "northkorea": ["dmz", "busan", "guam", "seoul", "japan", "pacific", "peninsula", "kunsan", "okinawa", "south"],
    "china": ["strait", "scarborough", "spratly", "spratlys", "paracel", "paracels", "matsu", "kinmen", "penghu", "philippines", "pacific", "sea", "south", "east", "japan", "guam"],
    "venezuela": ["caribbean", "maracaibo", "orinoco", "guyana", "trinidad", "tobago", "curacao", "aruba", "colombia", "puerto", "rico", "sea", "atlantic"],
}

# Tuning numbers of the word-meaning matcher (set on the DEV half of tests/matcher_bench.json and the tester inputs; docs/METHODOLOGY.md section 13).
MATCH = dict(
    kind_weight=1.0,     # how much the case's short "kind" line counts next to its title
    tag_weight=0.0,      # how much the plain labels of the move and target tags count (tested on dev: no gain, so 0)
    soft=0.5,            # share of the "every description word has a close word in the case" score (the rest is whole-sentence closeness)
    rel_gap=0.09,        # keep cases within this much of the best one
    max_cases=12,        # never return more than this
    min_sim=0.70,        # a case must be at least this close (no clear move in the words)
    min_sim_move=0.65,   # the same, when the words clearly name a move (the move filter already removed unlike cases)
    none_below=0.70,     # if even the best case is below this, say the log has nothing like it (no clear move)
    none_below_move=0.60,
    very_close=0.85,     # closeness for the label "Very close" (also needs every box setting met)
    close=0.75,          # closeness for the label "Close"
    min_pool=3,          # fewer cases than this: relax box settings one by one (never the move)
    small_pool=3,        # a precise phrase naming a move the log has this few cases of: show them all, as Loose
    cue_w=1.5,           # extra weight of the words that named the move (the rest of the description counts 1)
    lex_w=1.0,           # weight of the plain words a lexicon term stands for
    lam=0.2,             # share of the "literal words" score (rare words of the description found in the case title) in the closeness
    place_w=0.35,        # how much a place word counts next to other words
    lex_min=0.30,        # without the word model: closeness cut-offs on the literal-words score alone
    lex_none=0.30,
    lex_close=0.60,
    lex_very_close=0.85,
    adv_bonus=0.10,      # ranking bonus for cases on the adversary's own ground or against its leaders when the words ask for force against the adversary's leader or the country itself
    anchor_df=6,         # a word is "rare" when it is in 1 to this many case titles: such a literal word keeps a case of the read move above the closeness lines
    anchor_min=0.40,     # ... but never one this far from the words
    fix_top=6000,        # typo repair looks at this many of the most common model words (plus the cue, lexicon and case-title words)
)

# Widening order when too few cases match: the first field listed is dropped first. Type of move is never dropped.
WIDEN_ORDER = ["open", "who", "scale", "where", "target"]

# A move read from the words may also admit the other move's cases that happened on land (a "bomb the country" can be a raid in the log).
SIBLINGS = {"strike": ["raid"]}
# a kind of move the log of a theater has no case of is read as this kind there (China logs what the US says as talks)
ALIKE = {"statement": ["talks"]}

ROW_FIELDS = set(FIELDS) | {"why"}


def check(theater, tags, case_ids):
    """Problems with one theater's tags (empty list = fine). case_ids = ids of counted US-action cases."""
    out = []
    for i in sorted(set(case_ids) - set(tags)):
        out.append(f"{theater} #{i}: counted case has no tags (add it to napor/tags/{theater}.py)")
    for i, t in tags.items():
        if set(t) - ROW_FIELDS or set(FIELDS) - set(t):
            out.append(f"{theater} #{i}: tag fields must be exactly {FIELDS} + why")
            continue
        for f in FIELDS:
            vals = t[f] if f == "target" else [t[f]]
            if f == "target" and not isinstance(t[f], list):
                out.append(f"{theater} #{i}: target must be a list"); continue
            for v in vals:
                if v not in VOCAB[f]:
                    out.append(f"{theater} #{i}: {f}={v!r} is not in VOCAB")
    return out


def page_vocab(theater_id=None):
    """What the exporter writes to the page data: labels, values, synonyms, cue rows, the theater's neutral words,
    the matcher's tuning numbers and the widening order."""
    return dict(fields=FIELDS, labels=LABELS, vocab=VOCAB, synonyms=SYNONYMS, widen=WIDEN_ORDER,
                cues=CUES, neutral=NEUTRAL.get(theater_id, []), params=MATCH, lang=LANG, places=PLACES.get(theater_id, []), adversary=ADVERSARY.get(theater_id, []), siblings=SIBLINGS, alike=ALIKE)


def load_tags(theater_id):
    """The TAGS dict of napor/tags/<theater_id>.py, or None when the theater has no tag file yet."""
    import importlib, importlib.util
    try:
        if importlib.util.find_spec(f"tags.{theater_id}") is None:
            return None
    except ModuleNotFoundError:
        return None
    return importlib.import_module(f"tags.{theater_id}").TAGS


def counted_case_ids(out):
    """Ids of every counted (non-hold-week) case in one theater's page data."""
    return sorted({c["id"] for o in out["options"] for c in o["cases"] if not c.get("week")})


def annotate(out, theater_id):
    """Write each non-week case's tags (the TAGS row without `why`, plus `why` only if non-empty) and the top-level
    `matcher` into the page data. A theater with no tag file gets neither (the page then hides the matcher)."""
    tags = load_tags(theater_id)
    if tags is None:
        return out
    for o in out["options"]:
        for c in o["cases"]:
            if c.get("week") or c["id"] not in tags:
                continue
            row = tags[c["id"]]
            t = {f: (list(row[f]) if f == "target" else row[f]) for f in FIELDS}
            if row.get("why"):
                t["why"] = row["why"]
            c["tags"] = t
    out["matcher"] = page_vocab(theater_id)
    return out
