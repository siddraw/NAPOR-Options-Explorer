"""Venezuela / Caribbean: the word tests shared by config.py (what each logged row is) and rules.py (which census rows count as replies).

Kept in one small file with no imports from the rest of the package, so the page rules and the independent recount cannot drift apart."""


def adversary_side(actor):
    """Venezuela itself (the Maduro government, the interim government, its ministers and forces, including 'per Pentagon' and
    'per state media' labels) or an armed group (Tren de Aragua, ELN, FARC dissidents, 'armed group'). Cuba, Russia and Trinidad are not."""
    a = actor.lower()
    return a.startswith(("venezuela", "tren de aragua", "eln", "farc", "armed group", "cartel"))


def is_hostile(action):
    """A hostile act by the other side: an attack, harassment of US assets, or a military mobilization (troops, militia, a national exercise).
    Words alone (a statement, a denunciation), a diplomatic step and an economic step are not."""
    a = action.lower()
    return a.startswith(("attack", "harassment", "strike")) or "mobilization" in a


def is_armed(action):
    """Armed action: an attack on, or armed harassment of, US forces or assets (for example military aircraft close to a US warship).
    A mobilization announcement or an exercise is not."""
    return action.lower().startswith(("attack", "harassment", "strike"))


def is_countermeasure(action):
    """A Venezuelan counter-measure: oil, gas or shipping cut-offs, airline bans, expelling firms or diplomats."""
    return action.lower().startswith(("economic act", "diplomatic break", "expulsion", "counter-measure"))
