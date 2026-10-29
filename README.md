# NAPOR: Risk Assessment

NAPOR was inspired by how the Maven Smart System organizes information: it pulls reports from many
sources into one picture so a decision-maker can see what is happening and what their options are.
NAPOR follows the same idea on a smaller scale, using only public news. NAPOR is simply an acronym for
the mechanism itself: **Notebook, Arrows, Patterns, Organization, and Report.**

- **Notebook** – every event written down once, with an ID, credible sources and a 0–1 credibility score.
- **Arrows** – links from a US move to the replies that followed it.
- **Patterns** – what usually follows what, counted as "x of n past cases".
- **Organization** – war phases, intensity, duplicate checks and a change log.
- **Report** – predictions locked before the outcome, then graded.

Originally I set out to build a model that predicts the future. I switched it to an **Options
Explorer**, because the more useful question is "what happened the last times the US did this?"
The underlying problem was quantifying risk. Risk is perspective based and can be too broad, so
quantifying it requires a specific definition, and any definition is controversial. Looking at past
conflicts, NAPOR found the same five kinds of risk across many previous cases:

1. **People** – someone was hurt, by the US action or by the reply.
2. **Escalation** – the other side struck back within days.
3. **Military** – the reply used missiles, rockets or drones.
4. **Economic** – attacks on shipping or other economic damage went up afterward.
5. **Political** – no talks, meetings or deals followed within 14 days.

The page lays out each option and its risks. **It does not pick the "best" option.** That is the
decision-maker's job.

![NAPOR Options Explorer](docs/screenshot.png)

## Why Iran first

The US–Iran conflict was first because it is ongoing and has a long record of past cases. In terms of
US conflicts, Iran is one of the most trending headlines, so it made a good prototype: a current
conflict that has gone on long enough to have a significant number of past cases. Once the model
worked for Iran, it was easy to copy it and apply it to other theaters: the Houthis / Red Sea, North
Korea, China / Taiwan, and Venezuela / Caribbean.

## How I built this

This was my first project where I used AI to build a system for me. I wanted to learn how well AI
follows instructions and learns from failures. The process took a lot of failure (wrong news sources,
wrong ways of defining risk, numbers that did not hold up in testing), and I wanted to see how well AI
could learn from those failures and keep improving the model.

**What I designed:**
- The source rules: which outlets count as credible and which only count as labelled claims.
- The core rule that the page presents options and their risk, and never ranks them or picks one.
- What counts as risk: the five categories (AI helped me spot patterns in the past cases), and the idea
  that risk is defined by what happened in past cases.
- The NAPOR structure itself, modeled on how the Maven Smart System organizes information.
- Connecting the weekly news scan to the live page, so it updates on its own every Monday.
- The approval rule: the AI can suggest changes to the model, but no rule changes without my OK.
- The multi-AI workflow described below.

**What Claude did:** Claude helped heavily with researching the past cases, since AI is, in my opinion,
the fastest and best information processor. It looked into each past case, pulled out the relevant
information, and sorted it into the five categories. It also wrote most of the code, built the
interactive page, ran the backtests that check whether the numbers hold up, and runs the weekly news scan.

## Next steps

- **Better news sources.** Public news can be incomplete, so access to better-quality sources would mean
  more accurate data and more past cases to find patterns in.
- **More theaters.** Apply the model to more US interactions, so every one has its own tab.
- **More frequent scans.** Move the weekly scan to twice a week or daily (currently limited by usage).
- **AI improving the model.** Keep using a team of AI models to find ways to improve it. Opus (max effort)
  is the "mastermind" that comes up with ideas and does the final review, Opus (medium effort) is the
  "organizer" that turns them into instructions and checks the work, and Sonnet models are the "workers"
  that do the research and coding.

## View the page

The Options Explorer is `explorer/index.html`.

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
- **Venezuela / Caribbean**: US moves toward Venezuela and the boat-strike campaign, and Venezuelan or armed-group replies. Caveat: only 8 of about 70 boat strikes are logged one by one, most Venezuelan replies are statements (not counted as escalation), option G has 1 case, and hold weeks may hide unlogged strikes.

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
