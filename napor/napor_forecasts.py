"""NAPOR: forecast log (the report card).

Rules:
  1. A forecast is written down BEFORE the outcome is known, with the date it was made,
     the exact question, the deadline, the probability, and where the number came from.
  2. A forecast is never edited after it is made. If we change our mind, we add a new one.
  3. After the deadline, it is resolved YES or NO from credible sources, and scored:
     Brier score = (probability - outcome)^2, where outcome is 1 for YES and 0 for NO.
Stored in napor_forecasts.json next to this file.
"""
import json, os, math, datetime as dt
import data
import napor_ids as N
import napor_threads as T
import napor_options as OPT

HERE = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(HERE, "napor_forecasts.json")


def load():
    if os.path.exists(FILE):
        with open(FILE) as f:
            return json.load(f)
    return []


def save(items):
    with open(FILE, "w") as f:
        json.dump(items, f, indent=1)


def add(question, resolves_yes_if, deadline, probability, basis, related_events=(), option=None, made_on=None, news_through=None):
    items = load()
    fid = f"F{len(items) + 1:03d}"
    items.append(dict(id=fid, made_on=(made_on or dt.date.today()).isoformat(), news_through=news_through,
                      question=question, resolves_yes_if=resolves_yes_if, deadline=deadline.isoformat(),
                      probability=round(probability, 2), basis=basis, option=option, related_events=list(related_events),
                      outcome=None, resolved_on=None, resolution_note=None, brier=None))
    save(items)
    return fid


def resolve(fid, outcome_yes, note, sources=(), resolved_on=None):
    items = load()
    for it in items:
        if it["id"] == fid:
            if it["outcome"] is not None:
                raise ValueError(f"{fid} is already resolved")
            y = 1 if outcome_yes else 0
            it.update(outcome="YES" if y else "NO", resolved_on=(resolved_on or dt.date.today()).isoformat(),
                      resolution_note=note, sources=list(sources), brier=round((it["probability"] - y) ** 2, 3))
    save(items)


def scorecard():
    items = load()
    done = [i for i in items if i["brier"] is not None]
    return dict(made=len(items), resolved=len(done), open=len(items) - len(done),
                avg_brier=round(sum(i["brier"] for i in done) / len(done), 3) if done else None)


# ---------------------------------------------------------------------------
# Seeding the first forecasts (run once). Made Oct 14 with news only through Oct 11.
# ---------------------------------------------------------------------------
def seed_first_forecasts():
    if load():
        return
    # F001 - reply to the US strike on a blockade runner (#104)
    census, _ = N.filter_census(data.census)
    ph = [c for c in census if c[2] in ("R-strong", "R-weak", "R-proxy", "N") and T.event_phase[c[0]] == T.phase_of(dt.date(2026, 10, 11))]
    k = sum(1 for c in ph if c[2] != "N")
    p_phase = (k + 1) / (len(ph) + 2)
    d_row = [r for r in OPT.option_rows() if r["key"] == "D"][0]
    add(question="Will Iran hit back for the US strike that disabled a blockade runner in the Gulf of Oman (Oct 10-11, event #104)?",
        resolves_yes_if=("Between Oct 11 and Oct 16 (inclusive), Iran (IRGC or Iranian state forces) carries out, or officially claims, a strike or attack "
                         "on US forces, a US base, or a US-flagged or US-escorted ship, as reported by an allowed outlet or official statement. "
                         "Attacks on other commercial shipping by unknown attackers do not count."),
        deadline=dt.date(2026, 10, 16), probability=p_phase,
        basis=(f"Phase model (best in backtest): in the current holding pattern {k} of {len(ph)} hostile acts drew a reply -> "
               f"({k}+1)/({len(ph)}+2) = {p_phase:.0%}. For comparison, naval-pressure moves in ALL phases drew a reply {d_row['reply']}. "
               "Also: Trump says no US strikes before Nov 3; Iran is reviewing the US counter-offer."),
        related_events=[104], option="D", made_on=dt.date(2026, 10, 14), news_through="2026-10-11")
    # F002 - baseline: shipping attacks keep coming
    bl = OPT.baseline_hold()
    lam = bl["per_week"]
    p_ship = 1 - math.exp(-lam)
    add(question="Will there be at least one new attack on a commercial ship in or near the Strait of Hormuz / Gulf (by Iran or an unidentified attacker) during Oct 12-18?",
        resolves_yes_if=("An allowed outlet, UKMTO or CENTCOM reports at least one new projectile, drone, mine or boarding attack on a commercial vessel in the Gulf, "
                         "Strait of Hormuz or Gulf of Oman dated Oct 12-18, not attributed to the US. Houthi attacks in the Red Sea do not count."),
        deadline=dt.date(2026, 10, 18), probability=p_ship,
        basis=(f"Baseline: {bl['n']} such acts in {bl['weeks']} weeks of the current phase = {lam} per week. "
               f"Chance of at least one in a week (Poisson) = 1 - e^-{lam} = {p_ship:.0%}."),
        related_events=bl["ids"], option="A", made_on=dt.date(2026, 10, 14), news_through="2026-10-11")


if __name__ == "__main__":
    seed_first_forecasts()
    for it in load():
        print(it["id"], it["probability"], it["deadline"], it["question"][:90])
    print(scorecard())
