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
        "strike": ["strike", "strikes", "airstrike", "airstrikes", "air strike", "air strikes", "bomb", "bombs", "bombing", "bombed", "missile", "missiles", "rocket", "rockets", "drone", "drones", "attack", "attacks", "attacked", "hit", "hits", "shell", "shelling", "tomahawk", "destroy", "destroyed", "blast", "kill", "killing", "killed"],
        "raid": ["raid", "raids", "special forces", "commando", "commandos", "ground operation", "capture", "snatch", "rescue", "invade", "invasion"],
        "naval": ["naval", "navy", "blockade", "boarding", "board", "interdict", "interdiction", "transit", "fonop", "freedom of navigation", "escort", "quarantine", "warship", "warships", "destroyer", "destroyers", "seizure", "maritime"],
        "deployment": ["deploy", "deployed", "deployment", "deployments", "station", "stationed", "carrier", "carriers", "bombers", "patriot", "thaad", "reinforce", "buildup", "build-up", "troops", "marines", "advisers", "advisors", "garrison", "battery", "batteries", "missile defense", "air defense", "warship", "warships", "surge"],
        "withdrawal": ["withdraw", "withdrawal", "withdrawing", "pullout", "pull out", "drawdown", "draw down", "evacuate", "evacuation"],
        "drill": ["drill", "drills", "exercise", "exercises", "war games", "wargame", "wargames", "maneuvers", "manoeuvres"],
        "sanctions": ["sanction", "sanctions", "sanctioned", "embargo", "export control", "export controls", "tariff", "tariffs", "freeze", "asset freeze", "blacklist", "penalty", "penalties"],
        "legal": ["designate", "designation", "terror listing", "fto", "indict", "indictment", "bounty", "charge", "charges", "lawsuit", "court", "prosecute", "warrant", "reward", "extradition"],
        "arms": ["arms sale", "arms sales", "arms", "weapons sale", "weapons sales", "arms deal", "military aid", "arms transfer", "security assistance", "arm"],
        "talks": ["talks", "negotiate", "negotiation", "negotiations", "deal", "ceasefire", "truce", "summit", "agreement", "diplomacy", "mediation", "treaty", "dialogue", "call", "phone call", "say", "says"],
        "visit": ["visit", "visits", "meeting", "meet", "meets", "phone call", "call", "phone", "delegation", "contact"],
        "statement": ["statement", "warn", "warning", "threat", "threaten", "ultimatum", "speech", "announce", "declare", "say", "says"],
        "cyber": ["cyber", "hack", "hacking", "hackers", "cyberattack", "cyber attack", "malware", "ransomware"],
    },
    "target": {
        "equipment": ["radar", "radars", "launcher", "launchers", "base", "bases", "air defense", "military site", "military sites", "weapons", "depot", "airfield"],
        "personnel": ["troops", "soldiers", "fighters", "personnel", "irgc", "militia", "forces"],
        "leaders": ["leader", "leaders", "commander", "commanders", "general", "president", "regime", "maduro", "kim"],
        "economy": ["oil", "economy", "bank", "banks", "company", "companies", "refinery", "exports", "port", "ports", "energy", "power grid", "infrastructure"],
        "shipping": ["shipping", "ship", "ships", "tanker", "tankers", "cargo", "vessel", "vessels", "freighter"],
        "boats": ["boat", "boats", "speedboat", "speedboats", "drug boat", "fast boats"],
        "nuclear": ["nuclear", "enrichment", "uranium", "fordow", "natanz", "missile program", "icbm"],
        "proxy": ["proxy", "proxies", "houthi", "houthis", "hezbollah", "militias"],
        "officials": ["official", "officials", "individuals", "minister", "ministers"],
    },
    "where": {
        "adversary": ["inside", "mainland", "homeland", "in iran", "in venezuela", "in north korea", "in china", "in yemen", "on land", "territory"],
        "proxy": ["proxy territory", "iraq", "syria", "lebanon", "yemen"],
        "sea": ["sea", "at sea", "strait", "gulf", "red sea", "caribbean", "waters", "international waters", "airspace", "ocean"],
        "third": ["third country", "ally", "allied", "jordan", "bahrain", "qatar", "japan", "south korea", "taiwan", "philippines", "colombia"],
    },
    "scale": {
        "single": ["one", "single", "once", "one-off", "limited", "one strike"],
        "campaign": ["campaign", "series", "several days", "weeks", "sustained", "waves", "operation"],
    },
    "who": {
        "alone": ["alone", "us only", "unilateral", "by itself"],
        "allies": ["israel", "israeli", "allies", "ally", "uk", "britain", "nato", "coalition", "with allies", "joint"],
        "partners": ["partners", "proxy forces", "local forces", "through partners", "via partners"],
    },
    "open": {
        "announced": ["announced", "open", "public", "claimed", "overt"],
        "unclaimed": ["covert", "secret", "unclaimed", "deniable", "hidden", "quiet"],
    },
}

# ---- Reading the move from a typed description ("Your own option" matcher, v2) ----
# CUES say which Type-of-move values a description clearly points to. They are the matcher's only HARD rule for the
# description: a clear cue keeps only cases whose move is in `moves`; no cue means no move filter (the word-meaning
# model then ranks everything). Cue rows are tried in tiers: tier 1 (specific phrases, e.g. "pull troops out") beats
# tier 2 (a verb plus an object, e.g. "send ... carrier") beats tier 3 (tier 0 is only for acts that no move fits: the filter is then empty) (one cue word, the SYNONYMS["move"] lists above).
# Only the best tier that matched counts; inside that tier every matched row adds its moves (an ambiguous act keeps
# both moves and lets closeness decide). The same list is exported to the page; napor/matcher_ref.py is the Python twin.
# Phrase language (lower-case words; a trailing * means "any ending"): `a|b` = either word, `...` = up to 4 words in between,
# the words must come in this order. Example: "pull ... out|back|down" matches "pull troops out" and "pull back".
# Moves are chosen with the log's own tagging habits in mind: sanctions relief, ceasefires and "restore relations" are
# tagged talks, so those cues keep talks (and sanctions) in.
_OBJ_FORCES = "troop*|force*|soldier*|personnel|presence|footprint|staff|garrison*|deployment*|contingent|marines|advisers|advisors"
_OBJ_ASSETS = "troop*|force*|soldier*|marines|carrier*|warship*|ship*|bomber*|aircraft|jet*|fighter*|destroyer*|submarine*|advisers|advisors|personnel|batter*|defense|defence|patriot|thaad|system*|missile*|radar*|assets|weapons|reinforcements|fleet|navy|capabilit*"
_OBJ_ARMS = "weapon*|arms|missile*|batter*|patriot|thaad|jet*|aircraft|fighter*|tank*|ammunition|munition*|drone*|equipment|system*|artillery|helicopter*|rocket*"
_OBJ_SHIPS = "ship*|tanker*|vessel*|boat*|cargo*|freighter*|shipment*|container*|oil|fuel|crude"
_OBJ_TRADE = "export*|import*|sale*|sell*|purchase*|buy*|trade|oil|chip*|technolog*|invest*|financ*|bank*|crude|gas|energy|supplies|payment*|transaction*|travel|visa*|shipment*|revenue|money|funding|funds"
_RELIEF = "lift*|eas*|relax*|remov*|suspend*|waiv*|roll*|drop*|scrap*|loosen*|repeal*|revok*|rescind*|unfreez*|releas*|end|reduc*|cut*|relief"
_SANC = "sanction*|embargo*|tariff*|restriction*|penalt*|curbs|ban|bans|controls"
_LEADER = "leader*|general*|commander*|chief*|head|scientist*|official*|minister*|president|supreme|ayatollah|khamenei|soleimani|kingpin|boss|dictator|maduro|kim"
_TERROR = "terror*|fto|sdgt|sponsor*"
CUES = [
    # --- tier 1: specific phrases ---
    dict(p=1, moves=["withdrawal"], phrases=["pull ... out|back|down|away|home", "pullout", "draw ... down", "drawdown", "withdraw*", "bring ... home|back", "evacuat*",
        "leave|exit|quit ... iraq|syria|afghanistan|region|base|bases|country|korea|japan|yemen|gulf|bahrain|qatar|kuwait|jordan|saudi|east",
        "reduc*|cut*|scale|scal*|lower|trim|shrink|decreas*|downsiz*|thin ... " + _OBJ_FORCES, "close|shut|abandon ... embass*|consulate*|base|bases|mission"]),
    dict(p=1, moves=["withdrawal", "sanctions"], phrases=["cut|break|sever|end|suspend|downgrad*|expel ... ties|relations|relationship|diplomatic"]),
    dict(p=1, moves=["sanctions", "talks"], phrases=[_RELIEF + " ... " + _SANC, "sanctions relief", "relief ... sanction*", "unfreez*|releas* ... funds|assets|money|oil"]),
    dict(p=1, moves=["legal", "sanctions"], phrases=["delist*", "take|taking|remov*|drop* ... off|from ... list|designation|terror*", "revok*|rescind*|lift*|end ... designation|listing"]),
    dict(p=1, moves=["sanctions"], phrases=["reimpos*|reinstat*|renew*|reapply*|snap* ... sanction*", "restor* ... sanction*|pressure"]),
    dict(p=1, moves=["arms"], phrases=["arms sale*", "arms transfer*", "arms deal*", "arms package*", "weapons sale*", "military aid", "military assistance", "security assistance",
        "sell*|sale*|transfer*|provid*|suppl*|giv*|donat*|deliver*|export*|approv*|authoriz* ... " + _OBJ_ARMS, "send*|ship*|arm|arms|offer* ... weapon*|arms|ammunition|munition*"]),
    dict(p=1, moves=["strike", "raid"], phrases=["kill*|assassinat*|eliminat*|decapitat*|hunt*|murder* ... " + _LEADER, "take|taking|took ... out ... " + _LEADER]),
    dict(p=1, moves=["raid", "legal"], phrases=["captur*|arrest*|abduct*|seiz*|detain*|snatch* ... " + _LEADER]),
    dict(p=1, moves=["legal", "sanctions"], phrases=["designat*|list*|label*|declar*|classif*|brand* ... " + _TERROR]),
    dict(p=1, moves=["sanctions"], phrases=["freez*|froze|frozen|seiz*|block* ... asset*|fund*|money|account*|property|wealth|reserves|deposit*",
        "ban|prohibit*|restrict*|limit*|block*|curb*|cut ... off ... " + _OBJ_TRADE, "ban|prohibit*|restrict*|limit*|curb*|cap|bar|forbid* ... " + _OBJ_TRADE]),
    dict(p=1, moves=["naval"], phrases=["seiz*|captur*|board*|intercept*|detain*|impound*|stop* ... " + _OBJ_SHIPS]),
    dict(p=1, moves=["strike", "naval"], phrases=["destroy*|sink*|sunk ... " + _OBJ_SHIPS.replace("|oil|fuel|crude", "")]),
    dict(p=1, moves=["talks"], phrases=["stop*|halt*|end*|ceas*|suspend*|paus* ... strike*|bomb*|attack*|air*|campaign|war|operation|fighting|hostilit*|raid*", "call ... off ... strike*|bomb*|attack*|campaign|operation",
        "restor*|reopen*|resum*|reestablish*|normaliz*|normalis*|reinstat* ... relations|ties|contact*|embass*|channel*|communication*|dialogue|talks|diplomatic|ambassador*",
        "agree*|reach* ... ceasefire|truce|deal|agreement"]),
    dict(p=1, moves=["drill"], phrases=["cancel*|stop*|halt*|suspend*|end*|postpon*|reduc*|scale|scal*|shrink|cut|curtail* ... drill*|exercise*|war games|wargame*|maneuver*"]),
    dict(p=1, moves=["talks", "statement", "visit"], phrases=["writ*|letter|message|offer*|propos*|invit* ... meet*|talks|negotiat*|dialogue|summit|meeting|engagement"]),
    dict(p=0, moves=[], phrases=["leav*|exit*|quit*|abandon*|withdraw*|pull* ... deal|agreement|accord|treaty|jcpoa|pact"]),   # tier 0, no move: no log row is tagged as leaving an agreement, so no case matches (never talks) and the page says the log has no past cases like it
    # --- tier 2: a verb with its object, or a clear kind of act ---
    dict(p=2, moves=["deployment"], phrases=["send*|deploy*|dispatch*|station*|position*|mov*|bring*|surg*|base*|put|place|install*|increas*|bolster*|reinforc*|boost|add|augment*|fly|flew|stage|forward ... " + _OBJ_ASSETS]),
    dict(p=2, moves=["naval"], phrases=["escort*|convoy*|freedom of navigation|fonop*|transit*|sail*|navigat*|patrol*|boarding|blockad*|quarantin*|interdict*|block* ... port*|strait|coast|shipping|sea|route*|harbor*|harbour*"]),
    dict(p=2, moves=["cyber"], phrases=["cyber*|hack*|malware|ransomware|virus|stuxnet|ddos", "computer network*", "digital attack*"]),
    dict(p=2, moves=["talks", "visit"], phrases=["meet|meeting|meets|visit*|call|phone*|telephone*|speak|summit|invit*|host|welcome|receiv* ... leader*|president|xi|kim|minister*|official*|delegation*|counterpart*"]),
    dict(p=2, moves=["strike", "raid"], phrases=["kill*|assassinat*|eliminat*"]),
    dict(p=2, moves=["drill"], phrases=["hold*|conduct*|launch*|run|start|join*|stage|stag* ... drill*|exercise*|war games|wargame*|maneuver*"]),
]

# Words that name the theater itself. Every case in a theater is already about it, so these words never filter anything,
# never show as "ignored", and are left out of the word-meaning comparison.
NEUTRAL = {
    "iran": ["iran", "iranian", "iranians", "tehran"],
    "houthis": ["houthi", "houthis", "yemen", "yemeni", "yemenis", "ansar", "ansarallah", "sanaa"],
    "northkorea": ["dprk", "north", "korea", "korean", "koreans", "pyongyang"],
    "china": ["china", "chinese", "prc", "beijing"],
    "venezuela": ["venezuela", "venezuelan", "venezuelans", "caracas", "maduro"],
}

# Tuning numbers of the word-meaning matcher (set on the DEV half of tests/matcher_bench.json; docs/METHODOLOGY.md section 13).
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
)

# Widening order when too few cases match: the first field listed is dropped first. Type of move is never dropped.
WIDEN_ORDER = ["open", "who", "scale", "where", "target"]

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
                cues=CUES, neutral=NEUTRAL.get(theater_id, []), params=MATCH)


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
