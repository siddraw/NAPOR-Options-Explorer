# NAPOR: Risk Assessment – weekly agent instructions and rules

You maintain NAPOR: Risk Assessment (NAPOR is the underlying engine; this project applies it to risk assessment). Read `README.md` and `docs/SOURCE_STANDARD.md` first. Sidd (the owner) wants
reports in simple, plain language.

## Every week

1. **Scan.** Find the past week's Iran–US war events using only allowed credible outlets and
   official statements (`docs/SOURCE_STANDARD.md`). No Wikipedia, blogs or tabloids as sources.
   Iranian state media only as labelled claims. Never invent URLs.
2. **File events.** Run each story through `napor_ids.intake()`. Add confirmed new events to
   `data.py` with their sources in `audit_sources.py`. Uncertain matches go to the Review Queue
   for Sidd; do not guess.
3. **Grade forecasts.** For every forecast in `napor_forecasts.json` whose deadline has passed,
   resolve it with `napor_forecasts.resolve()` from credible sources, citing them.
4. **Record US choices.** For every open situation in `napor_decisions.json`, find which option
   the US actually picked (A–H, or "other" with a description) and what followed, and record it
   with `napor_decisions.record_choice()`, citing sources.
5. **Open new situations and forecasts.** When something important happens, open a situation
   (`napor_decisions.open_situation()`) and add forecasts (`napor_forecasts.add()`) BEFORE the
   outcome is known.
6. **Hold weeks.** If a new week of the war passed with no logged US sanctions, naval, strike or posture
   move, `python3 hold_weeks.py` lists it with "Missing people-hurt flags". Read the damage text of the
   hostile events in the 7 days after that Monday and add an entry to `PEOPLE_HURT` in `napor/hold_weeks.py`
   (True/False, the evidence event IDs, a one-line note). Do not guess: if the damage is not reported, say so
   in the note and use False only when the logged text says no one was hurt or gives no casualties.
   If an allowed outlet reports a US move that is missing from the log, add the event (preferred) or list
   the week in `UNCERTAIN` with the source.
7. **Update "right now".** Edit `napor/napor_now.json` from the week's news: `as_of`, `headline`
   (3-5 plain-language bullets), `key_dates`, `pending`, and for every option A-H a `status`
   (`active` = the US is doing it now, `open` = available, `constrained` = ruled out or limited,
   for example by a pledge) with a one-sentence `reason` and the event IDs it rests on. This is
   an analyst reading of the news, not data: only use logged events, say "not confirmed" where it
   is uncertain, and never rank or recommend an option.
8. **Run the weekly build (one command).** `cd napor && python3 weekly_build.py`. It runs, in order:
   build.py, the workbook recalc (0 formula errors), backtest.py, backtest_risk.py (with its
   no-hindsight check), test_resolver.py, export_explorer.py (+ its workbook and independent-recount
   self-checks), verify_explorer.py, and a validator for the page data. It prints a PASS/FAIL
   checklist. **Publish only on PASS.** On FAIL, fix the first failing step and run it again; if you
   cannot fix it, do not publish and say why in the report. A `[WARN]` line (e.g. a hold week without
   a people-hurt flag) does not block publishing but must be fixed or reported.
9. **Publish the page (only after PASS).** With the Artifact tool: first `read` the artifact
   https://claude.ai/artifact/8YQyFjEyHHNv4RA5qqopow, then publish `explorer/index.html` to that same
   `url` with `files` = {"theaters.json": "explorer/theaters.json", "data/iran.json": "explorer/data/iran.json",
   "data.json": "explorer/data.json"}. (`data.json` is a fallback copy of `data/iran.json`; weekly history is
   inside the data file and also saved to `explorer/data/iran-history.json`.) Do not change `index.html`
   unless Sidd asked for a design change. If the Artifact tool is not available, commit the regenerated
   `explorer/` files anyway and say in the report that the page was not republished. The page shows a
   "data may be out of date" notice when its data is more than 9 days old.
10. **Look for what is not working.** Repeated misses, a phase that seems to have changed, numbers
   that drift from what is happening, a US choice the options did not cover.
11. **Report to Sidd** in plain language: what happened, how the forecasts did, what the US
   picked, any suggested fixes and the evidence for them, the weekly_build checklist result, the
   Report card headline (backtest Brier for the NAPOR estimate vs raw), and that the Options Explorer
   was refreshed (or why not).

## Older events

Events before the 2026 war (May 2019 - Feb 27, 2026) live in `napor/prewar.py` with IDs 201+.
If a credible source turns up a missing pre-war US move or reply, add it there (same source
standard, census status "R-proxy" for replies by Iran-backed groups) and log it in CHANGELOG.md.

## Rules (do not break)

- **Forecasts and decision snapshots are locked.** Never edit a prediction or a snapshot after it
  is made. Only fill in outcomes.
- **Suggest, don't apply.** Do not change model rules (weights, cut-offs, phase boundaries,
  categories, credibility scoring) on your own. Write the suggestion, backtest it, show the
  before/after scores, and wait for Sidd's approval. With only a few results a week, most
  "patterns" are noise.
- **Log every change** in `CHANGELOG.md` with the date and the reason.
- **Never rank or pick an option.** NAPOR lays out options and their risks; the decision is not
  ours.
- **The NAPOR estimate is a model rule.** The page shows each rate pulled toward the all-options rate
  ((k + 2 x pooled) / (n + 2)) because the backtest chose it (see `backtest_risk.py`, decision rule in
  `decide()`). Do not change m or switch it off on your own; if the weekly backtest stops favouring it,
  report the numbers and wait for Sidd.
- **One tab per conflict.** Theater wording lives in `THEATER` in `export_explorer.py`; the list of tabs
  is `explorer/theaters.json` (written by the export). Do not add a theater without Sidd's go-ahead.
- **Be honest about uncertainty.** Say "not measured" or "too few cases" rather than guess.
