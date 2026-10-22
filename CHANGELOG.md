# Changelog

## 2026-10-19 (Sidd)
- Project renamed to NAPOR: Risk Assessment. NAPOR is the underlying engine; this project applies it to risk
  assessment. Updated README, AGENT.md and the workbook title. Repository renamed on GitHub to `siddraw/NAPOR-risk-assessment`.

## 2026-10-19 (weekly agent)
Data updates only; no model rules changed.
- New events #106-#115 (Oct 12-18 news, plus catch-up rows #106 Oct 6 dhow strike, announced Oct 14, and
  #107 Oct 8 shadow-fleet sanctions, missed last week). Sources added to audit_sources.py (allowed outlets and
  official Treasury releases only). #113 is an IRGC claim (Partly verified). Reason: weekly scan.
- Review queue: 10 stories confirmed as new events; 2 left for Sidd (R0222: IRGC claims of Oct 11-12 tanker
  strikes may duplicate #103/#105; R0252: Iranian army claim of two tanker fires in the Gulf of Oman Oct 15-16 -
  the matcher said SAME EVENT as #113, which looks wrong). Reason: uncertain matches are not guessed.
- Trigger Census: added #104, #106, #107 as 'Unclear' and #110 as 'Unverified' so they do not move any rate until
  Sidd decides how to score them (see the weekly report suggestion). Reason: their 5-day windows closed (or are
  still open for #110) and scoring them is a judgement call.
- Data labels: #106 target set to 'IRGC-linked shipping' so it is grouped with option E (strikes on Iranian
  vessels); #111 typed as a statement (reported war plans), not a strike. Month label now 'Oct 2026 (to Oct 18)'.
  Option notes for B and D updated to say what happened (text only).
- Forecasts graded: F001 NO (Brier 0.063), F002 YES (Brier 0.029). Reason: deadlines passed.
- New situation S002 (US choice in the two weeks after the Nov 3 midterms) and new forecasts F003-F005, made
  Oct 19 with news through Oct 18, before the outcomes are known. S001 stays open (window runs to Oct 25).
- Rebuilt workbook (115 events), recalculated (410 formulas, 0 errors); backtest unchanged (28 predictions;
  phase model Brier 0.159); resolver test 52% top-1.

## 2026-10-18
- Packaged NAPOR as a repository. Added the decision log (napor_decisions.py) and the first open
  situation, S001 (what the US does after the Oct 10-11 blockade-runner strike).

## 2026-10-11 to 2026-10-18 (built in chat with Sidd)
- Credible-source audit of every event (Wikipedia removed); duplicates merged (#76->#75, #49->#50, #29->#28).
- Report IDs and 0-1 credibility scores; events under 0.50 left out of statistics.
- Chains (thread IDs), war phases, war-intensity gauge.
- Options sheet with no ranking: five-category risk profile plus pros.
- Forecast log with F001 and F002 (made Oct 14, news through Oct 11).

## 2026-10-20 - Options Explorer v2 (Sidd's request)
- Added `napor/export_explorer.py` and `explorer/` (index.html + data.json). Page shows percentages
  with Wilson 95% ranges, a war-intensity scale and timeline, filters by phase and intensity, and a
  compare view. The weekly agent now refreshes it (AGENT.md step 7).
- Explorer counts "talks within 14 days" as still open (not "no") when fewer than 14 days have
  passed; the workbook's Options sheet still counts a partly-open window as "no". This only changes
  recent cases. Suggestion for Sidd: align the workbook with the page.
- README now states what NAPOR stands for.

## 2026-10-20 (later) - Explorer: risk index, conditions lens, "right now" (Sidd's request)
- Each option now shows a NAPOR risk index (0-100%): the average of five measured rates (people hurt,
  Iranian reply, missile/drone replies, shipping attacks rising, no talks followed), equal weights by
  default and adjustable on the page. It summarizes past cases only and is not a ranking.
- The phase/intensity filter is now a click-to-select lens that shows how much each condition mattered.
- Added `napor/napor_now.json` (which options are open now and why) and `explorer/history.json`
  (weekly snapshots, shown as "since last update").

## 2026-10-20 (evening) - Explorer: per-option tabs
- Removed the top "right now" panel; each option tab now carries its availability, key dates, what we are
  waiting on, and the situation summary. Added likely-outcome bars, a risk gauge, a five-axis radar and
  shipping before/after bars to every option, and a weekly shipping chart plus open forecasts for Hold.

## 2026-10-20 - Explorer layout tidy-up
- War intensity and conditions moved into pop-up windows opened from two summary buttons; option list stays in view while scrolling; pros, harms and unknowns side by side; past-case table folds away.

## 2026-10-20 - Pre-war record, 2019-2026 (Sidd's request)
- Added `napor/prewar.py`: 63 events from May 2019 to Feb 27, 2026 (IDs 201-263), each sourced to
  allowed outlets (AP, Al Jazeera, Stars and Stripes, ABC, CBS, NPR, PBS, The War Zone, official statements).
  New phases: Maximum-pressure crisis, Shadow conflict, Twelve-day war, Pre-war standoff.
- New census status "R-proxy": a reply by an Iran-backed militia counts as a reply. "Iran struck within
  7 days" now also counts Iran-backed militias (not the Houthis, a separate front).
- Continuous-fighting rule applied to Oct 17, 2023 - Jan 29, 2024 and the twelve-day war (Jun 13-24, 2025).
- Past cases per option now: B 16, C 11, D 5, E 3, F 12, G 7, H 10 (A has none).
- Backtest after the change (Test 1, 46 predictions): type-of-act model 0.197, phase model 0.211,
  overall rate 0.238, always-50% 0.250. Before, the phase model was best; this is a finding, not a rule change.
- Explorer: scrollable timeline with year buttons, radar labels moved in, formula under the index,
  "corners don't add to 100%" note, proxy labels. `verify_explorer.py` recounts every rate independently
  and the weekly export checks it.

## 2026-10-21 - Click-through risk breakdowns
- Every risk percentage (category rows, pentagon corners, stacked-bar segments) opens a pop-up with the rule for what counts as risk and every past case marked Counts / Doesn't count / Not counted yet, with the harm, replies, strikes, talks or shipping counts behind it. The exporter now includes that evidence per case. Pop-up counts are checked to equal the index.

## 2026-10-22 - Look back to a past date
- New "Viewing" button: pick any date since May 2019 (or a preset). Every option's risk index, outcome bars and breakdowns are recomputed using only the cases and outcomes known on that day (outcome windows still open then are left out). Shows each option's risk over time and the logged US moves of each kind in the following 14 days. Weekly availability statuses are now archived in history.json so past weeks can show them.
