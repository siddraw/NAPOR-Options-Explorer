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
7. **Look for what is not working.** Repeated misses, a phase that seems to have changed, numbers
   that drift from what is happening, a US choice the options did not cover.
8. **Report to Sidd** in plain language: what happened, how the forecasts did, what the US
   picked, any suggested fixes and the evidence for them.

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
