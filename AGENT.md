# NAPOR: Risk Assessment – weekly agent instructions and rules

You maintain NAPOR: Risk Assessment (NAPOR is the underlying engine; this project applies it to risk assessment). Read `README.md` and `docs/SOURCE_STANDARD.md` first. Sidd (the owner) wants
reports in simple, plain language.

## Every week

Five theaters are live (`explorer/theaters.json`): `iran`, `houthis`, `northkorea`, `china`, `venezuela`. Steps 1-2 and 6-7
are done once per theater. Steps 3-5 are Iran only.

1. **Scan, per theater.** Find the past week's events using only allowed credible outlets and official
   statements (`docs/SOURCE_STANDARD.md`). No Wikipedia, blogs or tabloids as sources. Never invent URLs.
   Each theater has its own claim-only media, shown only as labelled claims (score 0.30): Iran: Iranian state
   media; Houthis: al-Masirah and Houthi statements; North Korea: KCNA and Rodong Sinmun; China: Xinhua,
   Global Times, CGTN, PLA Daily, Chinese MND/MFA; Venezuela: Telesur and VTV (Venezuelan state media). The list is in each theater's `config.py`.
2. **File events, per theater.** Add confirmed new events in that theater's file and ID block, in the same
   record format as the rows already there, with sources:
   - Iran: `data.py` (+ `audit_sources.py`); run each story through `napor_ids.intake()`. Pre-war: `prewar.py` (201+).
   - Houthis: `napor/theaters/houthis/events_early.py` / `events_late.py`, IDs 1001-1599.
   - North Korea: `napor/theaters/northkorea/events.py`, IDs 2001-2999.
   - China: `napor/theaters/china/events.py`, IDs 3001-3999.
   - Venezuela / Caribbean: `napor/theaters/venezuela/events.py`, IDs 4001-4999 (event and pair IDs). Venezuela's escalation rule is stricter than the census: `rules.py` keeps a census reply only if a hostile act (attack, harassment, mobilization) is logged within 7 days; statements do not count.
   **Link rule (approved 2026-10-28): only add events that have a link.** Every new event needs at least one source with
   a working https URL from an allowed outlet or an official release. A name-only report gets zero credit, and an event
   with no linked source is excluded from every count (credibility 0). Treat any existing link-less event as excluded;
   find a link for it or leave it out.
   Uncertain matches go to the Review Queue for Sidd; do not guess.
3. **Grade forecasts (Iran only).** For every forecast in `napor_forecasts.json` whose deadline has passed,
   resolve it with `napor_forecasts.resolve()` from credible sources, citing them.
4. **Record US choices (Iran only).** For every open situation in `napor_decisions.json`, find which option
   the US actually picked (A-H, or "other" with a description) and what followed, and record it
   with `napor_decisions.record_choice()`, citing sources.
5. **Open new situations and forecasts (Iran only).** When something important happens, open a situation
   (`napor_decisions.open_situation()`) and add forecasts (`napor_forecasts.add()`) BEFORE the
   outcome is known.
6. **Hold weeks, where they apply.** Iran: if a new week of the war passed with no logged US sanctions, naval,
   strike or posture move, `python3 hold_weeks.py` lists it with "Missing people-hurt flags". Read the damage
   text of the hostile events in the 7 days after that Monday and add an entry to `PEOPLE_HURT` in
   `napor/hold_weeks.py` (True/False, the evidence event IDs, a one-line note). Do not guess: if the damage is
   not reported, say so in the note and use False only when the logged text says no one was hurt or gives no
   casualties. If an allowed outlet reports a US move that is missing from the log, add the event (preferred)
   or list the week in `UNCERTAIN` with the source. For the other theaters, do the same only if their
   `config.py` defines hold weeks; if it does not, Option A has no cases there and the page says so.
7. **Update "right now", per theater.** Edit `napor/napor_now.json` (Iran) or
   `napor/theaters/<id>/now.json` (others) from the week's news: `as_of`, `headline` (3-5 plain-language
   bullets), `key_dates`, `pending`, and for every option a `status` (`active` = the US is doing it now,
   `open` = available, `constrained` = ruled out or limited, for example by a pledge) with a one-sentence
   `reason` and the event IDs it rests on. This is an analyst reading of the news, not data: only use logged
   events, say "not confirmed" where it is uncertain, and never rank or recommend an option.
8. **Run the weekly build (one command).** `cd napor && python3 weekly_build.py`. It loops over every
   theater in `theaters.json` and runs, in order: build.py, the workbook recalc (0 formula errors),
   backtest.py, backtest_risk.py (with its no-hindsight check), test_resolver.py, then for each theater the
   export (+ its workbook and independent-recount self-checks), verify and a validator for the page data. It
   prints a PASS/FAIL checklist. **Publish only on PASS.** On FAIL, fix the first failing step and run it
   again; if you cannot fix it, do not publish and say why in the report. A `[WARN]` line (e.g. a hold week
   without a people-hurt flag) does not block publishing but must be fixed or reported.
9. **Publish the page (only after PASS).** With the Artifact tool: first `read` the artifact
   https://claude.ai/artifact/8YQyFjEyHHNv4RA5qqopow, then publish `explorer/index.html` to that same
   `url` with `files` = {"theaters.json": "explorer/theaters.json", "data.json": "explorer/data.json",
   and for every theater id in `theaters.json`: "data/<id>.json": "explorer/data/<id>.json" and
   "data/<id>-history.json": "explorer/data/<id>-history.json"}. (Today: iran, houthis, northkorea, china, venezuela.
   `data.json` is a fallback copy of `data/iran.json`. The verify files `explorer/verify-<id>.json` are
   checks, not page files.) Do not change `index.html` unless Sidd asked for a design change. If the Artifact
   tool is not available, commit the regenerated `explorer/` files anyway and say in the report that the page
   was not republished. The page shows a "data may be out of date" notice when its data is more than 9 days old.
10. **Look for what is not working.** Repeated misses, a phase that seems to have changed, numbers
   that drift from what is happening, a US choice the options did not cover. Check each theater.
11. **Report to Sidd** in plain language: what happened in each theater, how the Iran forecasts did, what the
   US picked, any suggested fixes and the evidence for them, the weekly_build checklist result, the
   Report card headline (backtest Brier for the NAPOR estimate vs raw, per theater), and that the Options
   Explorer was refreshed (or why not).

## Adding a new theater (only with Sidd's go-ahead)

1. Copy a finished package, for example `napor/theaters/northkorea/`, to `napor/theaters/<id>/`.
2. Write `config.py` in plain words: options, the five risk categories, claim-only outlets, the Option A
   rule, and where n is small.
3. Write `events*.py` in a new ID block (next free thousand: 4001-4999 and so on), same record format, allowed
   sources only. Write `now.json`.
4. Check the cases/export/verify/backtest wrappers point to the new id. Shared code is
   `napor/theaters/common.py`; do not edit it for one theater.
5. Register the theater in `explorer/theaters.json` (id, name, status, data path, as-of).
6. Run `weekly_build.py` until PASS, add the new files to the step 9 `files` map, log it in CHANGELOG.md.

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
- **The "political" corner counts talks only (changed 2026-10-26, approved by Sidd).** A past case counts as political risk when no
  actual talks, meeting, negotiation, formal proposal, ceasefire or deal between the US and the adversary (directly or through a
  mediator) was logged within 14 days. Statements, threats and appeals do NOT count as talks, and neither does a multilateral act
  such as a UN resolution. Every US option-B row counts (so Venezuela's deals and swaps do), and so does an adversary row that is a
  negotiation. The rule is the same in every theater (`napor_options.TALK_WORDS`, `TALK_EXTRA`, `TALK_EXCLUDE`, config `TALK_EXTRA` /
  `TALK_EXCLUDE`, `_talks` in `napor_options.py` and `theaters/common.py`); do not change it without Sidd. When you file a
  diplomatic event, put the right words in its action type: "talks", "proposal" or "ceasefire (...)" only for real talks, offers or
  ceasefires; "statement", "threat", "demand" or "rejection" for words alone.
- **One tab per conflict.** Theater wording lives in each theater's `config.py` (Iran: `THEATER` in
  `export_explorer.py`); the list of tabs is `explorer/theaters.json`. Do not add a theater without Sidd's go-ahead.
- **Be honest about uncertainty.** Say "not measured" or "too few cases" rather than guess.

## Commits
- No AI attribution: never add Co-Authored-By, Claude-Session or similar lines to commit messages, and commit as the repo owner.
