# Changelog

## 2026-10-28 - Tests, docs, license and three consistency fixes
- I added a pytest suite (`tests/`) and a CI workflow that runs it, plus methodology and architecture docs in `docs/` and a license file.
- **Venezuela now follows the same continuous-fighting rule as the other theaters.** A US move dated inside an exclusion window is no longer a case, except the move that starts the window. Before, Venezuela used its windows only to skip hold weeks, so #4032, #4044, #4046 and #4048 still counted. They are now "Unclear" in the census (context only). The windows are unchanged. The shared helper is `exclude_in_windows` in `theaters/common.py`, called from `theaters/venezuela/rules.py`. Cases per option: E 8 to 7, F 2 to 1, H 8 to 6; the rest are the same. I rewrote the Venezuelan notes for E, F and H to match, and added a test that no Venezuelan case sits inside a window.
- **Iran `n_events` now counts only events at credibility 0.50 or more**, as the other theaters do (it used to include the 4 events under the cut). The page's "new events" line in the history strip now says "counted (credibility 0.50+)".
- I corrected the Houthi event count below (88 to 94) and the 2026-10-26 backtest numbers (Iran 0.1806 vs raw 0.1902).
- Re-sourced 9 Iran events with links; corrected dates for #44/#45 and wording for #83/#87; 4 events still rely on outlet names only (#84, #86, #88, #89) and #67 has no source.

## 2026-10-26 - Model rule change: "political" corner is now "talks only" (I approved on 2026-10-26)
- **Rule, every theater.** Old: risk = no diplomatic event of any kind (statements and threats by any side included) logged within 14 days. New: risk = no actual talks, meeting, negotiation, formal proposal, ceasefire or deal between the US and the adversary (directly or through a mediator) logged within 14 days. Statements, threats and appeals do not count. This is the "P2: talks only, 14 days" rule tested in round 2 (same words as the "Diplomacy" option's past moves: `napor_options.TALK_WORDS`).
- **Reason.** The old rule let a single public threat or warning cancel a political risk, so the corner mostly measured how often officials talk, not whether talks were happening. I approved the talks-only rule after the round-2 backtest.
- **Follow-up fixes (same day, coordinator).** (1) Every US option-B (talks/deals) row counts, so Venezuela's oil deals and license, prisoner swap, restored ties, embassy reopening and normalization flight now count as deals; an adversary row that is a negotiation counts too: Iran #99 (Oct 9, "talks continue through mediators") and #127 (Oct 25, messages still passed to the US through intermediaries) were added (`TALK_EXTRA`); #115 (Iran reviewing US comments) and rejections were left out. (2) Houthis: UN Security Council Resolution 2722 (#1020) is a multilateral act, not talks or a proposal to or by the Houthis, so it no longer counts (`TALK_EXCLUDE`); "proposal" counts only when made to or by the adversary.
- **Political Brier (old to new, walk-forward, NAPOR estimate):** Iran 0.3084 to 0.2989; Houthis 0.1100 to 0.0225; North Korea 0.0233 to 0.0233 (no change); China 0.0000 to 0.0000 (no change); Venezuela 0.0730 to 0.0730 (no change: every logged Venezuelan diplomatic row is an option-B row, so the new rule equals the old one there).
- **Index Brier (old to new):** Iran 0.1816 to 0.1797 (new Iran index Brier 0.1797); Houthis 0.0770 to 0.0595; North Korea 0.0495 to 0.0495; China 0.0813 to 0.0813; Venezuela 0.0829 to 0.0829. A lower score means the new rule is easier to predict, not that it measures political risk better.
- **Effect on the page.** No option's risk index moved by more than 5 points (largest: Houthis A 22.6 to 24.9; Iran A 19.2 to 20.8; Iran F 53.5 to 55.1; Iran B 19.5 to 20.7). Venezuela, North Korea and China are unchanged.
- **Code.** `napor_options.py` (`_talks` now needs the talk words; `_diplo` keeps the old any-diplomatic test), `backtest_risk.py` (`political_change` replaces `political_proposal`; the old rule is still computed so the Report Card can show old vs new), `theaters/common.py` (`_talks`, `is_talk`, `Recount` talk test, `talk_dates`), each theater `config.py` (plain rule text; the Houthi text no longer says threats count), `export_explorer.py`, `hold_weeks.py` docstring, `explorer/index.html` (pop-up and "How this works" text; the "Proposal - needs Sidd's approval" block is replaced by a short note with the old and new Brier). Python (export, recount, backtest) and the page JS give the same political k of n for every option in all five theaters (checked in headless Chromium). `weekly_build.py`: PASS.
- **Known edge cases.** Iran #115 is a judgment call left out. Option-B rows count even when they are only normalization steps (Venezuela #4058, #4060).

## 2026-10-26 — Venezuela / Caribbean tab (fifth theater)
- **Venezuela tab** (64 events, IDs 4001–4066 in block 4001–4999; `napor/theaters/venezuela/`): US moves toward Venezuela and the boat-strike campaign, and Venezuelan or armed-group replies. Registered in `explorer/theaters.json`; `weekly_build.py` PASS. Telesur and VTV are claim-only. Escalation counts only a hostile act within 7 days (attack, harassment, mobilization); `rules.py` demotes census replies that were words, diplomatic or economic steps. Military = armed action (only #4019). Economic = Venezuelan counter-measures within 14 days (events mode; only 3 logged). Political = no US talks or deal within 14 days.
- Weak spots: only 8 of about 70 boat strikes are logged one by one; most replies are statements, so escalation is 0 of 6 to 8 for most options; F (2 cases) and G (1 case) show "too few cases"; E's 4 replies are 2 Venezuelan acts; hold weeks (14) may hide unlogged strikes (weeks with outlet-count evidence are excluded); the economic corner rests on 3 acts, one dated by report; the 2 newest sanctions moves wait for 7 days of news.
- Shared code: `common.py` Recount now counts `CIVILIAN_HARM` in the people corner (as the page and verify_explorer.py already did); no effect on other theaters (empty there). `index.html`: the "harm in the US action" labels read `theater.us_hurt` when set (Venezuela: "Anyone killed or hurt in the US action"); defaults unchanged.

## 2026-10-24 — Round 2, stages 3–5
- **Per-theater engine** (`napor/theaters/common.py`): shared code for cases, export, verify and backtest. Each theater is a package `napor/theaters/<id>/` (config, events, now.json, wrappers). `weekly_build.py` now loops over every theater in `explorer/theaters.json`. Page data goes to `explorer/data/<id>.json`, `<id>-history.json` and `explorer/verify-<id>.json`. Iran has a wrapper package too; its numbers are unchanged.
- **Houthi tab** (94 events, IDs 1001–1599): Red Sea crisis, US strikes and Houthi replies. Problems found in review were fixed. Weak spots: 2024 was continuous fighting, so few cases count as separate cases; the 2025–26 log is thin.
- **North Korea tab** (76 events, IDs 2001–2999): US/South Korea drills, deployments, sanctions and talks, and DPRK launches and tests as replies. Weak spots: the launch log is a sample, not every launch; economic harm is not measured; routine launch seasons are hard to tell from replies.
- **China tab** (63 events, IDs 3001–3999): Taiwan Strait transits, arms sales, visits, sanctions, and PLA drills as replies. Weak spots: small n, so wide ranges; Option A (Hold) has no cases; background PLA activity vs a real reply is a judgment call.
- Chinese, Houthi and DPRK state media are used only as labelled claims.
## 2026-10-26 (weekly agent)
Data updates only; no model rules changed.
- **Iran**: new events #117-#128 (news Oct 19-26), sources in audit_sources.py (allowed outlets, Treasury/OFAC; every URL from
  this session's searches/fetches). #121 and #123 are IRGC claims (partly confirmed). Reason: weekly scan.
- Review queue: 9 stories confirmed as new events (R0352-R0360). 1 left for Sidd (R0361: the IRGC's "seven tankers" claim, #121,
  may include the UKMTO-confirmed Bukha tanker hit, #118; duplicate_watch 0.64). Reason: uncertain matches are not guessed.
- Trigger Census: #110 moved from 'Unverified' to 'Unclear' (window closed; proposed N, waiting on Sidd as for #104/#106/#107);
  #119 (Oct 21 sanctions) added as 'Unverified' (window still open). These do not move any rate.
- Forecast graded: F004 YES (Brier 0.012). S001 closed: US choice C (sanctions), with the blockade continuing and no strikes.
  New situation S003 (US choice Oct 26-Nov 3) and forecast F006 (shipping attacks Oct 26-Nov 1, 91%), made Oct 26 before the outcome.
- napor_now.json rewritten for Oct 26 (H now "in use": staff drawdown #120). Month label 'Oct 2026 (to Oct 26)' in data.py and
  build.py text. Hold weeks: none new (week of Oct 19 has #119 sanctions).
- **Houthis / Red Sea**: new events #1344-#1349 (news Oct 14-26) in theaters/houthis/events_late.py with sources; none is
  tagged as a US option move (#1347, the Saudi ordered departure, is a diplomatic precaution). The open-ended end date of the
  current phase and of the two constraints moved from Oct 24 to Oct 26 (no boundary moved; they run "to the latest news").
  Hold week of Oct 19: people-hurt flag True (#1345, #1346). now.json rewritten for Oct 26.
- Weekly build: PASS. Backtest of the page's numbers: Iran NAPOR estimate 0.1806 vs raw 0.1902; Houthis 0.077 vs 0.082.

## 2026-10-24 — Round 2, stages 1–2
- Recency weighting (approved to test): backtested six versions (none; pre-2026 weight 0.25/0.5; half-life 180/365/730 days). Best overall was era 0.25 (0.1763 vs 0.1806), but it made military worse by 0.022 and escalation by 0.015, failing the written rule (no category worse by >0.01). **No change**: Iran numbers unchanged. Weighting code, page support and weighted recount are in place for later.
- Political category: three alternative definitions backtested and shown on the Report Card as a proposal only (live rule unchanged). "Talks only, within 14 days" scored 0.268 vs 0.304 live; dropping political from the index scored 0.149 vs 0.180.

## 2026-10-22 - Improvement round 1: Hold data, backtest of the risk numbers, Report card, one-command weekly build, theater-ready page
- **Option A (Hold) now has real cases** (`napor/hold_weeks.py`): weeks of the 2026 war (Mondays) with no logged US
  sanctions, naval, strike or posture move in the Monday-to-Monday window. Left out: Feb 28-Apr 7 and Jul 7-25 (US
  activity continuous but logged as a few rows), pre-war weeks (too sparsely logged) and the week of Aug 17 (AP reports
  an "economic D-Day" sanctions push that is not in the log). 11 hold weeks. "People hurt" is set by hand per week with
  evidence event IDs. A's numbers (raw): people 0 of 11, escalation 1 of 11, military 1 of 11, economic 1 of 11,
  political 6 of 11. Caveat on the page: most hold weeks have few or no logged events.
- New catch-up event #116 (Jun 6-7: Iran and Israel trade fire, the first exchange since the April ceasefire; NPR),
  found while building the hold weeks. No other option's rates changed.
- **Backtest of the risk assessment itself** (`napor/backtest_risk.py`): walk-forward over every past case and category,
  using only cases whose outcome window had closed before the case's date. Brier (lower is better, 0.25 = always 50%),
  293 predictions (47 skipped, no history): raw x of n 0.191; shrunk toward the all-options rate m=1 0.181, m=2 0.181,
  m=4 0.182; pooled 0.212; 50% 0.250. Shrinkage (m=2) beats raw in every category, so by the pre-agreed rule the page
  now shows a "NAPOR estimate" ((k + 2 x pooled rate) / (n + 2)) with the raw x of n beside it. Out of sample (fit
  2019-2025, score 2026) every method is worse than 50% (best 0.275): the pre-war record alone does not predict this war.
  Also calibration bins, a learning curve and a robustness table for reply rules. A test proves no hindsight.
- `napor/napor_cases.py`: one shared definition of the cases and the five categories (export + backtest). Options now
  carry flags (trigger, military = reply/strike/none, us_move, is_hold, salvo); the page no longer hard-codes letters.
- **One-command weekly build** (`napor/weekly_build.py`): build, recalc, both backtests, resolver test, export with its
  self-checks, independent recount, and a page-data validator; PASS/FAIL checklist, non-zero exit on failure. AGENT.md
  now says to publish only on PASS and lists the files to publish.
- **Page**: tab bar from `explorer/theaters.json` (Iran only; `#iran` deep link), data moved to `explorer/data/iran.json`
  (fallback `explorer/data.json`; history now `explorer/data/iran-history.json`), theater wording in the data file,
  new Report card view (locked forecasts, backtest charts with plain takeaways, robustness table), "How this works"
  pop-up with a live worked example, outlet links and credibility scores in the why-pop-ups and the past-case table,
  and a "data may be out of date" notice when the data is over 9 days old.
- `docs/THEATERS.md`: research memo on the next tabs (Houthis/Red Sea, North Korea, China, Caribbean/Venezuela,
  Mexico, Russia-Ukraine, Gaza, Iraq/Syria militias) with dated allowed-outlet sources and a suggested build order.

## 2026-10-22 - Re-sourcing and two pre-war naval cases (improvement round 1)
- Re-sourced 8 low-credibility 2026 rows with allowed outlets read in full (URLs from search/fetch results only):
  #43 (NPR), #46 (NPR, CENTCOM), #54 (Al Jazeera), #57 (Axios, Reuters), #58 (Reuters), #59 (NPR), #60 (CENTCOM, Bloomberg),
  #85 (Al Jazeera, AP). Credibility rose from 0.52 to 0.80-0.96 each.
- Corrections found while checking: #43 Iran and Israel traded fire Jun 6-7 before Iran agreed to stop (the old text said
  they had not); #46 targets were air-defense, ground-control and radar sites (the named towns were not in the Jun 9 reports);
  #57 the "49 to 25 vessels a day" figure was dropped (not found in an allowed outlet); #60 bridges were NOT among the Jul 8
  targets (the bridge strikes were Jul 16-17, AFP), so #60 was removed from the "civilian harm in the US act" list
  (option F's people-hurt rate is unchanged at 5 of 12 because #60's replies hurt people); #85 date is Sep 29, not Sep 28.
- Not re-confirmed this round (no allowed outlet found in the time available; rows unchanged): #22, #62, #63, #64, #67,
  #77, #81, #84, #87, #89, #101. #64, #67 and #101 remain IRGC claims.
- Pre-war naval pressure (option D): added #264 (USS Normandy seizes Iranian-made missiles bound for the Houthis, announced
  Feb 13, 2020) and #265 (2,116 rifles shipped from Iran seized in the Gulf of Oman, announced Jan 10, 2023). Both are
  logged on the announcement date (when a reply became possible) and scored N with evidence notes. Option D now has 7 cases
  (escalation 2 of 6). The Suez Rajan cargo seizure was left out: no allowed outlet gives its date. No US strike on Iranian
  vessels (option E) was found outside the Oct 2023 - Jan 2024 continuous-fighting window.
- NAVCENT added to the list of official sources in `napor_ids.py`.

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

## 2026-10-22 - Availability changes with the date
- Added `napor/napor_context.py`: ceasefires and the no-strike pledge, each bounded by logged events. On past dates each option is "In use" (US did it in the 14 days before), "Constrained" (a ceasefire or pledge in force ruled it out, including when it began after the last use) or "Open". Hold shows "Current course" when no US strike, sanctions or naval move is logged in the 14 days before. Only the US's own moves count (not Israel alone). The weekly hand-written status still applies to its own week.

## 2026-10-22 - Review of round 1
- Reviewed round 1 (weekly build PASS, page test 73/73, numbers and sources spot-checked). Corrected #59 to Jul 7 (NPR dates the remark to Tuesday). Merged to main.
