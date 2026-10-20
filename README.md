# NAPOR: Risk Assessment

**NAPOR** is the underlying engine: a clean, credible event log with IDs, credibility scores,
cause-and-reply chains, war phases, a forecast log and a decision log.

**NAPOR: Risk Assessment** is the project built on top of it. It lays out the options the US has
in the Iran–US war, and the risks and pros of each one.
**It does not pick an option.** That is the decision-maker's job.

Scope: the 2026 Iran–US war only, until the method is proven.

## How it works

1. **Event log** – every event, once, with an ID, from credible outlets only (`napor/data.py`,
   `docs/SOURCE_STANDARD.md`). Every news story gets its own report ID and points to one event.
2. **Credibility (0–1)** – each event is scored from its reports; only events at 0.50+ count in
   the statistics (`napor/napor_ids.py`).
3. **Chains and phases** – cause→reply chains get thread IDs; every event is tagged with the war
   phase (open war, fragile ceasefire, low-intensity war, holding pattern) and a war-intensity
   gauge (`napor_threads.py`, `napor_intensity.py`).
4. **Options** – every US option, on the same five risks (harm to people, escalation, military
   cost, economic harm, political/diplomatic) plus pros. Every number is "x of n past cases" or
   "not measured" (`napor_options.py`).
5. **Forecast log** – predictions written down before the outcome, never edited, then graded
   with the Brier score (`napor_forecasts.py`, `napor_forecasts.json`).
6. **Decision log** – for each situation, a snapshot of the options; later, what the US actually
   picked and what followed (`napor_decisions.py`, `napor_decisions.json`).
7. **Backtest** – replays the past without peeking ahead (`backtest.py`).

Options Explorer (interactive page): `explorer/index.html` reads `explorer/data.json`, which
`napor/export_explorer.py` regenerates every week. Percentages come with 95% (Wilson) ranges.

Build the workbook: `cd napor && python3 build.py` → `NAPOR_iran_war.xlsx`.

## Known limits

- Small samples: options rest on 3–16 past cases (2019 onward; pre-war record in `napor/prewar.py`).
- Before 2026 most replies came from Iran-backed militias; they count as replies and are labelled "proxy".
- Pre-war years are logged less densely than 2026, so war intensity before 2026 is understated.
- The phase boundaries were drawn with hindsight.
- July's nightly US strikes and pre-September shipping attacks are under-logged.
- "After" is not "because of".

See `AGENT.md` for the rules the weekly maintenance agent follows.
