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
6. **Re-run checks.** `python3 build.py`, recalculate the workbook (0 formula errors),
   `python3 backtest.py`, `python3 test_resolver.py`.
7. **Update "right now".** Edit `napor/napor_now.json` from the week's news: `as_of`, `headline`
   (3-5 plain-language bullets), `key_dates`, `pending`, and for every option A-H a `status`
   (`active` = the US is doing it now, `open` = available, `constrained` = ruled out or limited,
   for example by a pledge) with a one-sentence `reason` and the event IDs it rests on. This is
   an analyst reading of the news, not data: only use logged events, say "not confirmed" where it
   is uncertain, and never rank or recommend an option.
   **Refresh the Options Explorer page.** Run `cd napor && python3 export_explorer.py` (it writes
   `explorer/data.json` and prints whether its counts match the workbook; investigate any
   mismatch) and whether every risk rate matches the independent recount in
   `verify_explorer.py` (it must say "match"; if not, find the cause before publishing). Then publish with the Artifact tool: first `read` the artifact
   https://claude.ai/artifact/8YQyFjEyHHNv4RA5qqopow, then publish `explorer/index.html` to that
   same `url` with `files` = {"data.json": "explorer/data.json"}. Do not change `index.html`
   unless Sidd asked for a design change. If the Artifact tool is not available, commit the
   new `explorer/data.json` and `explorer/history.json` anyway and say in the report that the page was not republished.
8. **Look for what is not working.** Repeated misses, a phase that seems to have changed, numbers
   that drift from what is happening, a US choice the options did not cover.
9. **Report to Sidd** in plain language: what happened, how the forecasts did, what the US
   picked, any suggested fixes and the evidence for them, and that the Options Explorer was
   refreshed (or why not).

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
- **Be honest about uncertainty.** Say "not measured" or "too few cases" rather than guess.
