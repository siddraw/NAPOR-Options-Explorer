"""NAPOR step 3: the options sheet.

Lays out every option the US has, side by side, with the risks of each. It does NOT rank
options or pick one: that is the decision-maker's job.

Every number says how many past cases it comes from. The risks come from:
  - the Trigger Census (did Iran reply within ~5 days to past US moves of this kind?)
  - the action-reaction pairs (how fast, and did the reply cause casualties?)
  - the chains (how often a back-and-forth went past one reply)
Only events with credibility 0.50+ are used (napor_ids rule).
"""
import math
from collections import Counter
import data
import napor_ids as N
import napor_threads as T

census, _ = N.filter_census(data.census)
pairs, _ = N.filter_pairs(data.pairs)
EV = {e[0]: e for e in data.events}
KIND = data.event_kind
CURRENT_PHASE = T.phase_of(max(e[1] for e in data.events))
PATRIOTS_PER_SALVO = 30      # Sep 8-9 Jordan strike: 'roughly 30' (US official) / 'more than 30' (CBS)


def wilson(k, n, z=1.96):
    if n == 0:
        return None
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return max(0.0, c - h), min(1.0, c + h)


def us_side(tid):
    return EV[tid][2].lower().startswith(("us", "israel"))


def is_shipping_strike(tid):
    e = EV[tid]
    return KIND[tid] == "Kinetic" and ("shipping" in e[4].lower() or "tanker" in e[5].lower())


# Which past US/Israeli moves count as "this kind of option"
OPTIONS = [
    dict(key="A", name="Hold: no new action",
         what="Keep the current posture: blockade stays, no new strikes or sanctions.",
         match=None),
    dict(key="B", name="Diplomatic move",
         what="Answer Iran's expected reply to the US counter-offer, make a new offer, or ask a mediator to push talks.",
         match=None),
    dict(key="C", name="New sanctions",
         what="More Treasury sanctions on Iranian industries, networks or people.",
         match=lambda t: KIND[t] == "Sanctions"),
    dict(key="D", name="Naval pressure (blockade enforcement, transits, seizures)",
         what="Tighten or enforce the blockade: stop or disable blockade runners, escort or transit warships.",
         match=lambda t: KIND[t] == "Maritime"),
    dict(key="E", name="Strike Iranian shipping (e.g. tankers)",
         what="Destroy IRGC-linked tankers or vessels, as on Sep 5 and Sep 8.",
         match=is_shipping_strike),
    dict(key="F", name="Strike military sites (equipment, not people)",
         what="Hit launchers, radars, missile or drone sites, aiming to avoid casualties.",
         match=lambda t: KIND[t] == "Kinetic" and not is_shipping_strike(t) and data.census and t in {c[0] for c in census if c[1] == "Military/Property"}),
    dict(key="G", name="Strike that risks killing personnel",
         what="Strikes on IRGC units or sites where people are likely to be killed.",
         match=lambda t: t in {c[0] for c in census if c[1] == "Personnel/Casualty"}),
    dict(key="H", name="Change force posture (deploy or withdraw)",
         what="Send more ships, aircraft or troops to the region, or pull some back.",
         match=None),
]


def strength(n):
    if n == 0: return "No data"
    if n <= 3: return "Very thin"
    if n <= 7: return "Thin"
    return "OK"


def option_rows():
    out = []
    chain = T.chain_stats()
    longer = 1 - chain["share_stopped_after_one_reply"] if chain else None
    for o in OPTIONS:
        row = dict(key=o["key"], name=o["name"], what=o["what"])
        if o["match"] is None:
            row.update(n=0, reply="Not measured", reply_range="", phase_note="", fast="Not measured", casualties="Not measured",
                       longer="", patriots="", cases="", credibility="")
        else:
            rows = [c for c in census if us_side(c[0]) and o["match"](c[0])]
            counted = [c for c in rows if c[2] in ("R-strong", "R-weak", "R-proxy", "N")]
            unclear = [c for c in rows if c[2] == "Unclear"]
            k = sum(1 for c in counted if c[2] != "N")
            n = len(counted)
            ci = wilson(k, n)
            row["n"] = n
            row["reply"] = f"{k} of {n} ({k / n:.0%})" if n else "No past cases"
            row["reply_range"] = f"{ci[0]:.0%}-{ci[1]:.0%}" if ci else ""
            ph = [c for c in counted if T.event_phase[c[0]] == CURRENT_PHASE]
            kp = sum(1 for c in ph if c[2] != "N")
            row["phase_note"] = f"{kp} of {len(ph)}" if ph else "Not tested in this phase yet"
            trig = {c[0] for c in rows}
            pr = [p for p in pairs if p[1] in trig]
            if pr:
                fast = sum(1 for p in pr if (EV[p[2]][1] - EV[p[1]][1]).days <= 2)
                cas = sum(1 for p in pr if p[4] == "Y")
                row["fast"] = f"{fast} of {len(pr)}"
                row["casualties"] = f"{cas} of {len(pr)}"
            else:
                row["fast"] = row["casualties"] = "No past replies to measure"
            row["longer"] = (f"~{longer:.0%} (all chains, n={chain['chains']})" if longer is not None and k else "No past replies")
            kinetic_reply = o["key"] in ("D", "E", "F", "G")
            row["patriots"] = f"~{round(k / n * PATRIOTS_PER_SALVO)} if the reply is a missile salvo like Sep 8-9" if (n and kinetic_reply) else ("Unlikely to need any" if o["key"] == "C" else "")
            row["cases"] = ", ".join(f"#{c[0]}" for c in counted) + (f" (+ unclear: {', '.join('#%d' % c[0] for c in unclear)})" if unclear else "")
            creds = [N.event_credibility(c[0]) for c in counted]
            row["credibility"] = f"{sum(creds) / len(creds):.2f}" if creds else ""
        out.append(row)
    return out


def baseline_hold():
    """What has been happening WITHOUT new US moves: hostile acts by Iran/unknown in the current phase."""
    start = [p for p in T.PHASES if p[0] == CURRENT_PHASE][-1][1]
    last = max(e[1] for e in data.events)
    acts = [e for e in data.events if e[1] >= start and e[0] not in data.MERGED
            and KIND[e[0]] in ("Kinetic", "Maritime") and not us_side(e[0]) and not e[2].startswith("Houthi")]
    weeks = max(1, ((last - start).days + 1) / 7)
    return dict(n=len(acts), weeks=round(weeks, 1), per_week=round(len(acts) / weeks, 1), ids=[e[0] for e in acts])


UNKNOWNS = {
    "A": "Shipping attacks have kept coming without any new US move (see the baseline line). Trump has said there will be no US strikes before Nov 3; what Iran does if that holds is not in the data.",
    "B": "Diplomatic moves are not in the census, so there is no reply rate. The last rounds (Sep 23 - Oct 9) drew rejections and counter-offers, not attacks. Iran called the US answer 'insufficient' (Oct 11) and on Oct 18 said it was still reviewing US 'comments'.",
    "C": "Both past cases are from the current quiet phase, and neither drew a linked attack. Tanker attacks continued that week, but no outlet tied them to the sanctions.",
    "D": "Small sample. Iran answered the blockade start and a ship seizure, but not a warship transit. The Oct 10-11 strike on a blockade runner drew no Iranian attack on US forces within 5 days (F001: NO), but attacks on commercial shipping surged; how to score it is waiting for Sidd (census row #104 is 'Unclear').",
    "E": "Only 2 cases, both in early September; both drew Iranian missile fire (at a US warship, then at a Jordan base).",
    "F": "Every past case drew a reply, but all were before the current quiet phase. One logged reply caused casualties (Qatar, Jul 12: 3 wounded, including a child).",
    "G": "Every past case drew a fast reply, mostly the same day. One logged reply caused casualties (Tel Aviv, Feb 28: 1 killed, 27 injured). None in the current quiet phase.",
    "H": "No data: deployments and withdrawals are logged but not tested as triggers. The US recently pulled bombers from RAF Fairford and one carrier left the region.",
}


if __name__ == "__main__":
    print("Current phase:", CURRENT_PHASE)
    for r in option_rows():
        print(r["key"], r["name"], "|", r["reply"], r["reply_range"], "| phase:", r["phase_note"], "| fast:", r["fast"], "| cas:", r["casualties"], "|", r["patriots"], "|", r["cases"], r["credibility"])
    print("Baseline:", baseline_hold())


# ---------------------------------------------------------------------------
# PROS and OTHER HARMS
#
# Two kinds of evidence, kept apart:
#   Measured signals - what the log shows in the days after past US moves of this kind.
#                      Small samples, and "after" is not "because of": other things were
#                      happening too. Shipping attacks before September are under-logged.
#   Analyst notes    - reasoning about likely pros and harms, checked against the log where
#                      possible. These are judgement, not data, and are labelled as such.
# ---------------------------------------------------------------------------
import datetime as _dt

_LAST = max(e[1] for e in data.events)


def _usable(e):
    return e[0] not in data.MERGED and N.counts(e[0]) and not e[2].lower().startswith("houthi")


def _ship(e): return _usable(e) and KIND[e[0]] == "Maritime" and not us_side(e[0])
def _iran_side(actor):
    """Iran itself, or a group it arms (Iraqi/Syrian militias). Houthis are a separate front and are left out by _usable."""
    a = actor.lower()
    return a.startswith("iran") or any(w in a for w in ("iran-backed", "iranian-made", "islamic resistance in iraq", "kataib"))


def _irstrike(e): return _usable(e) and KIND[e[0]] == "Kinetic" and _iran_side(e[2])
def _talks(e): return _usable(e) and KIND[e[0]] == "Diplomatic"


def _window(f, day, a, b):
    return [e[0] for e in data.events if f(e) and day + _dt.timedelta(days=a) <= e[1] <= day + _dt.timedelta(days=b)]


# Civilian harm reported in the US/Israeli act itself (from the Event Log's credible-outlet wording)
CIVILIAN_HARM = {
    2: "Minab girls' school: Iranian authorities say 168-175 killed; no country has claimed the strike (AP, NBC)",
    74: "Kuhestak wedding: Iranian figures 4-5 killed incl. children, 50+ wounded; the US said it was investigating",
    60: "Two bridges among the 90 targets (civilian infrastructure); no casualty figure in the log",
}


def option_cases(key):
    """Past US/Israeli moves of this kind with a full 7-day 'after' window."""
    if key == "A":
        return []
    if key == "B":
        # conciliatory moves only: offers, talks, ceasefires, deals (not ultimatums, rejections or rhetoric)
        _CONC = ("proposal", "talks", "ceasefire announcement", "ceasefire (", "ceasefire statement")
        ids = [e[0] for e in data.events if _usable(e) and us_side(e[0]) and KIND[e[0]] == "Diplomatic"
               and any(w in e[3].lower() for w in _CONC)]
    elif key == "H":
        ids = [e[0] for e in data.events if _usable(e) and us_side(e[0]) and KIND[e[0]] == "Posture"]
    else:
        o = [x for x in OPTIONS if x["key"] == key][0]
        ids = [c[0] for c in census if us_side(c[0]) and o["match"](c[0])]
    return [i for i in ids if (_LAST - EV[i][1]).days >= 7]


def measured_signals(key):
    ids = option_cases(key)
    if not ids:
        return dict(n=0)
    st_after = sum(1 for i in ids if _window(_irstrike, EV[i][1], 1, 7))
    sh_b = sum(len(_window(_ship, EV[i][1], -7, -1)) for i in ids)
    sh_a = sum(len(_window(_ship, EV[i][1], 1, 7)) for i in ids)
    talks = sum(1 for i in ids if _window(_talks, EV[i][1], 1, 14))
    civ = [i for i in ids if i in CIVILIAN_HARM]
    return dict(n=len(ids), ids=ids,
                strikes_after=f"{st_after} of {len(ids)}",
                shipping=f"{sh_b} -> {sh_a}",
                talks=f"{talks} of {len(ids)}",
                civilian=(f"{len(civ)} of {len(ids)}: " + "; ".join(f"#{i} {CIVILIAN_HARM[i]}" for i in civ)) if civ else f"0 of {len(ids)} reported")


PROS = {
    "A": "No new US act for Iran to answer, so no added risk of retaliation from it. Keeps Trump's stated no-strike pledge before Nov 3. Leaves room for Iran's expected reply to the US counter-offer. Uses no interceptors.",
    "B": "No direct casualties. In the log, US diplomatic moves were usually followed by more diplomacy within two weeks (see measured column). A deal is the only option that addresses all the goals at once: the June memorandum included phased Hormuz reopening and an end to the blockade.",
    "C": "Economic pressure without casualties or interceptor use. Neither past case drew an Iranian military reply.",
    "D": "Aims directly at the blockade and Hormuz goals. In the April cases, no direct Iranian strike followed within 7 days, and the replies that came caused no casualties (0 of 2).",
    "E": "In both past cases, logged attacks on shipping dropped to zero the following week. Hits IRGC oil revenue (US claim). Crews were told to abandon ship before the Sep 8 strike, and no deaths were reported.",
    "F": "Aims to reduce Iran's ability to launch missiles, drones and mines (military effect is claimed by CENTCOM, not independently measured). In 1 of 4 logged replies did anyone get hurt.",
    "G": "Can remove commanders or units preparing attacks (e.g. the Aug 30 Larak strike hit launchers said to be preparing sea mines). Military effect is claimed, not independently measured.",
    "H": "No direct harm. Adding forces strengthens defence; pulling back reduces exposure (bombers left RAF Fairford after a suspected Iranian drone plot).",
}
HARMS = {
    "A": "Attacks on shipping continue at about 1-2 a week (baseline), injuring crews (On Peace: 12 hurt) and raising shipping risk. Whether holding back weakens deterrence cannot be measured from this log.",
    "B": "Past deals did not hold: the April ceasefire was violated the same day, and the June deal collapsed on Jul 7 (Iran later said it never took effect). Shipping attacks continued during talks. Political costs of concessions are not measured here.",
    "C": "No measured effect on shipping attacks (they rose in the following week, during the record week, so this may be coincidence). Possible economic harm to ordinary Iranians is not measured. Iran's president called talks 'futile' days later (no causal link shown).",
    "D": "Iran answered 2 of 3 past cases at sea (re-closing the Strait, seizing ships), so pressure at sea can spread at sea. Risk to the crews of disabled ships. The Oct 10-11 case drew no attack on US forces (forecast F001: NO), but shipping attacks surged the same week; whether that counts as a reply is not settled.",
    "E": "Both cases drew Iranian missile fire within days (at a US warship, then at a Jordan base, where an A-10 was badly damaged, ~8 F-15s were lightly damaged and ~30 Patriots were used). Possible environmental damage from destroyed laden tankers is not measured.",
    "F": "Every past case drew a reply; Iranian strikes followed within 7 days in most. One logged reply wounded civilians in Qatar. One past wave hit bridges (civilian infrastructure). Untested in the current quiet phase: it could restart the cycle.",
    "G": "Every past case drew a fast reply, mostly the same day. Civilians were reported killed in 2 of 4 past cases (Iranian figures). One logged reply killed a civilian in Tel Aviv. Highest risk of a longer back-and-forth.",
    "H": "Deployments in early October were followed by more shipping attacks, but that was the record week anyway. No data on how Iran reads deployments or withdrawals.",
}


# ---------------------------------------------------------------------------
# FIVE-CATEGORY RISK PROFILE
# Every option is described with the same five risk categories, so they can be compared
# side by side. Each line says what was measured (x of n past cases) or "not measured".
#   1 Harm to people   2 Escalation   3 Military cost   4 Economic harm   5 Political / diplomatic
# ---------------------------------------------------------------------------
# Equipment losses in Iranian replies that the US or credible outlets confirmed (claims excluded)
REPLY_EQUIPMENT_LOSS = {
    80: "Sep 8-9 Jordan: 1 A-10 lost a wing, ~8 F-15s lightly damaged (CBS, anonymous US sources)",
    45: "Jun 9: a US Apache helicopter downed over the Strait (crew rescued)",
}
RISK_CATEGORIES = ["1. Harm to people", "2. Escalation", "3. Military cost", "4. Economic harm", "5. Political / diplomatic"]


def _replies(key):
    o = [x for x in OPTIONS if x["key"] == key][0]
    if not o["match"]:
        return []
    trig = {c[0] for c in census if us_side(c[0]) and o["match"](c[0])}
    return [p for p in pairs if p[1] in trig]


def risk_profile(key):
    rows = {r["key"]: r for r in option_rows()}
    r = rows[key]
    m = measured_signals(key)
    rp = _replies(key)
    bl = baseline_hold()
    prof = {}
    # 1. People
    if key in ("D", "E", "F", "G"):
        hurt = [p for p in rp if p[4] == "Y"]
        det = "; ".join(f"#{p[2]} {EV[p[2]][7][:70]}" for p in hurt)
        prof[RISK_CATEGORIES[0]] = (f"Iranian replies that hurt people: {len(hurt)} of {len(rp)}" + (f" ({det})" if hurt else "") + ". "
                                    f"US personnel hurt in these logged replies: 0 of {len(rp)} (US troops were killed on Jul 17, #65, during the July campaign, which is outside these counts). "
                                    f"Civilian harm reported in the US act itself: {m.get('civilian', 'not measured')}.")
    elif key == "A":
        prof[RISK_CATEGORIES[0]] = f"Ship crews: attacks on shipping continue at ~{bl['per_week']} a week (e.g. On Peace, Oct 6: 12 crew injured). No new US act to answer."
    elif key == "C":
        prof[RISK_CATEGORIES[0]] = "No direct casualties. Harm to ordinary Iranians from sanctions: not measured."
    else:
        prof[RISK_CATEGORIES[0]] = "No direct casualties from the move itself."
    # 2. Escalation
    if key in ("C", "D", "E", "F", "G"):
        prof[RISK_CATEGORIES[1]] = (f"Iran replied within ~5 days: {r['reply']} (range {r['reply_range'] or '-'}). Fast (within 2 days): {r['fast']}. "
                                    f"Back-and-forth past one reply: {r['longer']}. In the current quiet phase: {r['phase_note']}.")
    elif key == "A":
        prof[RISK_CATEGORIES[1]] = "No new US trigger. Iranian or unidentified attacks on shipping keep happening anyway (baseline). Whether holding back changes Iran's behaviour: not measured."
    elif key == "B":
        prof[RISK_CATEGORIES[1]] = f"Iran struck within 7 days after {m['strikes_after']} past conciliatory US moves (timing only, not shown to be replies). Reply rate to diplomacy: not measured (not in the census)."
    else:
        prof[RISK_CATEGORIES[1]] = f"Iran struck within 7 days after {m['strikes_after']} past posture changes (all early October). Not tested as triggers."
    # 3. Military cost
    if key in ("D", "E", "F", "G"):
        losses = [REPLY_EQUIPMENT_LOSS[p[2]] for p in rp if p[2] in REPLY_EQUIPMENT_LOSS]
        prof[RISK_CATEGORIES[2]] = (f"Patriot interceptors: {r['patriots']}. Confirmed US equipment losses in past replies: "
                                    + ("; ".join(losses) if losses else "none logged") + ".")
    elif key == "A":
        prof[RISK_CATEGORIES[2]] = "No added interceptor use from a US act; the blockade and patrols continue to cost what they cost now (not measured)."
    else:
        prof[RISK_CATEGORIES[2]] = "No interceptor use expected from the move itself."
    # 4. Economic
    if m.get("n"):
        prof[RISK_CATEGORIES[3]] = f"Attacks on shipping, 7 days before -> after past cases: {m['shipping']} (total). Oil prices and shipping costs: not measured."
    else:
        prof[RISK_CATEGORIES[3]] = f"Baseline: ~{bl['per_week']} attacks on shipping a week in the current phase. Oil prices and shipping costs: not measured."
    # 5. Political / diplomatic
    if m.get("n"):
        prof[RISK_CATEGORIES[4]] = f"Talks or diplomatic moves within 14 days after: {m['talks']}. Strain with allies (Jordan, Gulf states, UK): not measured."
    else:
        prof[RISK_CATEGORIES[4]] = "Iran is expected to answer the US counter-offer; Trump's no-strike pledge stands until Nov 3. Strain with allies: not measured."
    prof["Pros (analyst notes)"] = PROS[key]
    prof["Other notes on harms (analyst notes)"] = HARMS[key]
    prof["Evidence strength"] = strength(r["n"]) if key in ("C", "D", "E", "F", "G") else (f"{m['n']} past cases (timing only)" if m.get("n") else "No data")
    return prof
