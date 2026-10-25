# NAPOR: Risk Assessment

**NAPOR** is the underlying engine: a clean, credible event log with IDs, credibility scores,
cause-and-reply chains, war phases, a forecast log and a decision log.

**NAPOR: Risk Assessment** is the project built on top of it. It lays out the options the US has
in the Iran–US war, and the risks and pros of each one.
**It does not pick an option.** That is the decision-maker's job.

Scope: four theaters: the 2026 Iran–US war, the Houthis / Red Sea, North Korea, and China / Taiwan. Iran is the main one.

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

Options Explorer (interactive page): `explorer/index.html` loads `explorer/theaters.json` (one tab per
conflict; four today) and the theater's data file `explorer/data/iran.json` (fallback: `explorer/data.json`),
which `napor/export_explorer.py` regenerates every week. Percentages come with 95% (Wilson) ranges; each corner
is shown as a NAPOR estimate (the x of n pulled toward the all-options rate, chosen by `napor/backtest_risk.py`)
with the raw x of n beside it. Option A (Hold) uses hold weeks (`napor/hold_weeks.py`). The Report card view
shows locked forecasts and the backtest of the page's own numbers.

Weekly check, one command: `cd napor && python3 weekly_build.py` (PASS/FAIL checklist; publish only on PASS).

Build the workbook: `cd napor && python3 build.py` → `NAPOR_iran_war.xlsx`.

## Theaters

- **Iran** (2019 on, mostly the 2026 war): the main tab, with forecasts and a decision log.
- **Houthis / Red Sea**: US moves and Houthi replies. Caveat: 2024 was continuous fighting, so few cases count, and the 2025–26 log is thin.
- **North Korea**: US/South Korea moves and DPRK launches. Caveat: the launch log is a sample; economic harm is not measured.
- **China / Taiwan**: Taiwan Strait and South China Sea. Caveat: small n; Option A has no cases.

Each non-Iran theater is a package in `napor/theaters/<id>/`; data goes to `explorer/data/<id>.json`.

## Known limits

The limits below are for Iran unless a theater is named.


- Small samples: options rest on 3–16 past cases (2019 onward; pre-war record in `napor/prewar.py`).
- Hold weeks (option A) are mostly quiet weeks with few logged events; they show what the log records, and an unlogged event would change them.
- Fitted on 2019-2025 only, every method does worse on 2026 cases than always saying 50% (Report card): the pre-war record alone does not predict this war well.
- Before 2026 most replies came from Iran-backed militias; they count as replies and are labelled "proxy".
- Pre-war years are logged less densely than 2026, so war intensity before 2026 is understated.
- The phase boundaries were drawn with hindsight.
- July's nightly US strikes and pre-September shipping attacks are under-logged.
- "After" is not "because of".

See `AGENT.md` for the rules the weekly maintenance agent follows.
