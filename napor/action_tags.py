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
    "move": {
        "strike": ["strike", "strikes", "airstrike", "air strike", "bomb", "bombing", "bombed", "missile", "missiles", "drone", "drones", "attack", "hit", "shell", "tomahawk"],
        "raid": ["raid", "special forces", "commando", "ground operation", "capture", "seize leader", "snatch"],
        "naval": ["naval", "navy", "blockade", "boarding", "board", "seize", "seizure", "interdict", "interdiction", "transit", "fonop", "freedom of navigation", "escort", "quarantine", "warship"],
        "deployment": ["deploy", "deployment", "send", "station", "carrier", "bombers", "patriot", "thaad", "reinforce", "buildup", "build-up", "troops"],
        "withdrawal": ["withdraw", "withdrawal", "pull out", "pullout", "reduce", "drawdown", "leave"],
        "drill": ["drill", "drills", "exercise", "exercises", "war games", "wargame"],
        "sanctions": ["sanction", "sanctions", "embargo", "export control", "export controls", "tariff", "tariffs", "freeze", "asset freeze", "ban"],
        "legal": ["designate", "designation", "terror listing", "fto", "indict", "indictment", "bounty", "charge", "lawsuit", "court"],
        "arms": ["arms sale", "arms", "weapons sale", "sell weapons", "arm", "military aid", "arms transfer"],
        "talks": ["talks", "negotiate", "negotiation", "deal", "ceasefire", "truce", "summit", "agreement", "diplomacy", "mediation"],
        "visit": ["visit", "meeting", "meet", "call", "phone call", "delegation", "contact"],
        "statement": ["statement", "warn", "warning", "threat", "threaten", "ultimatum", "speech", "announce"],
        "cyber": ["cyber", "hack", "hacking", "cyberattack", "cyber attack", "malware"],
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


def page_vocab():
    """What the exporter writes to the page data: labels, values, synonyms and widening order."""
    return dict(fields=FIELDS, labels=LABELS, vocab=VOCAB, synonyms=SYNONYMS, widen=WIDEN_ORDER)
