"""NAPOR: decision log ("what did the US pick?").

For each situation NAPOR writes down, BEFORE knowing what happens:
  - the situation (date, phase, intensity, the event that prompted it)
  - a snapshot of every option's risk profile at that moment
Later, the checker fills in:
  - which option the US actually picked (or "other", with a description)
  - what happened next (did Iran reply, casualties, talks), with credible sources
Over time this shows (a) how the US tends to decide in each phase, and (b) adds one real
case to the chosen option's statistics each time. It records what happened; it does not judge it.

Stored in napor_decisions.json. Entries are never edited after the snapshot, only completed.
"""
import json, os, datetime as dt
import data
import napor_options as OPT
import napor_threads as T
import napor_intensity as INT

HERE = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(HERE, "napor_decisions.json")


def load():
    if os.path.exists(FILE):
        with open(FILE) as f:
            return json.load(f)
    return []


def save(items):
    with open(FILE, "w") as f:
        json.dump(items, f, indent=1)


def open_situation(prompt_event, description, made_on=None, news_through=None):
    """Snapshot the options for a new situation."""
    items = load()
    last = max(e[1] for e in data.events)
    day = last + dt.timedelta(days=1)
    sid = f"S{len(items) + 1:03d}"
    items.append(dict(
        id=sid, opened_on=(made_on or dt.date.today()).isoformat(), news_through=news_through or last.isoformat(),
        situation=description, prompted_by_event=prompt_event,
        phase=T.phase_of(last), intensity=f"{INT.band(INT.intensity_before(day))} ({INT.intensity_before(day)} pts)",
        options_snapshot={o["key"]: dict(name=o["name"], **OPT.risk_profile(o["key"])) for o in OPT.OPTIONS},
        us_choice=None, us_choice_detail=None, choice_event_ids=[], outcome=None, sources=[], closed_on=None))
    save(items)
    return sid


def record_choice(sid, option_key, detail, event_ids=(), outcome=None, sources=(), closed_on=None):
    """option_key: one of A-H, or 'other'. Fills in what the US did and what followed."""
    items = load()
    for it in items:
        if it["id"] == sid:
            if it["us_choice"] is not None:
                raise ValueError(f"{sid} already has a recorded choice")
            it.update(us_choice=option_key, us_choice_detail=detail, choice_event_ids=list(event_ids),
                      outcome=outcome, sources=list(sources), closed_on=(closed_on or dt.date.today()).isoformat())
    save(items)


def choice_patterns():
    """How often the US picked each option, by phase (only closed situations)."""
    from collections import Counter, defaultdict
    by = defaultdict(Counter)
    for it in load():
        if it["us_choice"]:
            by[it["phase"]][it["us_choice"]] += 1
    return {ph: dict(c) for ph, c in by.items()}


def seed():
    if load():
        return
    open_situation(prompt_event=104,
                   description=("Holding pattern, Oct 11: the US has just disabled a blockade runner (#104); attacks on shipping continue; "
                                "Trump says no US strikes before Nov 3; Iran says it will answer the US counter-offer within days. "
                                "What does the US do next (Oct 12-25)?"),
                   made_on=dt.date(2026, 10, 18), news_through="2026-10-11")


if __name__ == "__main__":
    seed()
    for it in load():
        print(it["id"], it["opened_on"], it["phase"], it["intensity"], "| choice:", it["us_choice"], "|", it["situation"][:80])
