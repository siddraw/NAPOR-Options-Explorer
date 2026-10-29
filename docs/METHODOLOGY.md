# NAPOR: Risk Assessment - methodology

Technical reference for how the numbers on the Options Explorer are made. Numbers quoted here come from the
files in this repository as built on 2026-10-29; they change as events are added. For the folder layout see
[ARCHITECTURE.md](ARCHITECTURE.md). For the rules on sources see [SOURCE_STANDARD.md](SOURCE_STANDARD.md).

What the tool is: a count of what followed past US moves, shown as "x of n past cases". It describes the
past. It does not forecast the future and it does not rank or recommend an option. The page lists the
options in fixed letter order (A to H), never sorted by risk.

## 1. The event log and IDs

Each theater has its own event log. A theater is one tab on the page: Iran, Houthis / Red Sea, North Korea,
China / Taiwan, Venezuela / Caribbean (list: `explorer/theaters.json`).

- **Event.** One real-world event, written down once. A row holds an ID, a date, who acted, the action type,
  the target, a detail line and the damage reported. If one event has several news stories, the stories are
  separate **reports** that all point to the same event ID.
- **ID blocks.** Iran 1-128 (the 2026 war), 201-265 (May 2019 to Feb 2026) and 300-376 (Nov 1979 to May 2019);
  Houthis 1001-1599 (Sep 2014 on); North Korea 2001-2999 (2001-2076 from Aug 2017, 2500-2587 for Mar 1993 to Aug 2017);
  China 3001-3999 (3001-3063 from Jan 2019, 3500-3566 for May 1995 to Dec 2018); Venezuela 4001-4999 (4001-4066 from
  Jan 2019, 4500-4568 for Feb 1999 to Jan 2019).
- **Where the rows live.** Iran: `napor/data.py`, `napor/prewar.py` and `napor/prewar_early.py`, sources in `napor/audit_sources.py`.
  Other theaters: `napor/theaters/<id>/events*.py` (the earlier years are in `events_pre2017.py` for North Korea and
  `events_pre2019.py` for China and Venezuela). These files are the record; the code reads them and
  does not change them.
- **Duplicates.** A duplicate keeps its row as a record, but its reports move to the surviving event (Iran: #76 into
  #75, #49 into #50, #29 into #28). Uncertain matches go to `napor/napor_review_queue.json` for a person to decide.
- **Kind of act.** Each row is a Kinetic, Maritime, Diplomatic, Sanctions, Posture or Other act. Iran and Houthis use
  the shared word list (`data.act_kind`); the other theaters sort by the first words of the action type (`KIND_OF`).
- **Links.** A row can name the event that triggered it, and `PAIRS` link a US move to a logged reply. Back-and-forth
  links form a **chain** with its own ID (for example `H01`); a "round" is each switch of the acting side.
- **Phases and intensity.** Each date is tagged with a phase (for example open war, ceasefire, quiet), drawn with
  hindsight, and a 14-day intensity band that is not: 2 points per hostile Kinetic act, 1 per Maritime act, +2 if
  someone died; 0 Quiet, 1-5 Low, 6-11 Medium, 12 or more High. Only events at 0.50 or more count.

## 2. Source rules

The full list is in [SOURCE_STANDARD.md](SOURCE_STANDARD.md). In short:

- Allowed: major wire services and newspapers, named defense trade press, and official statements (CENTCOM, DoD, White
  House, Treasury/OFAC, UKMTO, UN, IAEA). Not allowed: Wikipedia, blogs, aggregators, tabloids, think-tank opinion, social media.
- **Official or primary sources (approved 2026-10-29).** An official or primary source can be the citation and scores like an
  allowed outlet: government and military sites (.gov, .mil), legislative records (Congressional Record, govinfo.gov,
  congress.gov, CRS reports), courts and the Justice Department, the UN and other international bodies (IAEA, KEDO, OAS, NATO),
  a foreign government's own ministry for what it did or said, and official archives such as presidential libraries. A mirror
  that only hosts a copy (everycrsreport.com, GlobalSecurity.org) is not the official source and keeps the lower score.
- **Label what was read.** The outlet label names the site the URL points to. A copy of a wire or outlet story read on another
  site is labelled "AP (via kpax.com)", never with the original outlet's bare name. `tests/test_sources.py` checks every label
  in every theater against its URL domain.
- **Claim-only media.** The adversary's state media is allowed only to show what that side claims, and is
  labelled as a claim: Iran (IRNA, Tasnim, Press TV), Houthis (al-Masirah, Saba), North Korea (KCNA,
  Rodong Sinmun), China (Xinhua, Global Times, CGTN, PLA Daily and others), Venezuela (Telesur, VTV).
  The lists are in each theater's `config.py`.
- Every source records the outlet, headline, publish date, URL and whether the article was read in full
  (`full text`) or only the search snippet was seen (`snippet`). A URL is never made up. Test
  `tests/test_theaters.py` checks that every URL starts with `https://` and none is a Wikipedia page. A claim that no
  allowed outlet confirms is marked `not_confirmed`.

## 3. Credibility and the 0.50 cut

Defined in `napor/napor_ids.py` (`credibility_of`) and shared by every theater.

1. Each **report** gets a weight: source score x fit score.
   - Source score: allowed outlet or official/primary source read on its own page 0.80; other outlet, or a mirror of an official page, 0.60; claim-only outlet 0.30.
   - Fit score (how sure the report is about this event): read in full 1.00; snippet only 0.80; outlet
     named but story not saved 0.65.
   - **Link rule (approved 2026-10-28).** A report counts only if it has a working `https://` link to an allowed
     outlet or an official or primary source. A report that only names an outlet gets weight 0 (`napor_ids.has_link`).
   - A report with weight under 0.30 is dropped.
2. An **event** combines its reports, counting each outlet once (its best report):
   `credibility = 1 - (1 - w1) x (1 - w2) x ...`, capped at 0.99. One full-text allowed outlet gives 0.80;
   two different outlets give 0.96; a claim-only outlet alone gives 0.30.
3. The source check adjusts it: "Partly verified" x 0.8; "Date conflict" x 0.9; "Not supported" capped at 0.20.
4. **The cut.** An event with no linked source has credibility 0, so it is always under the cut and is left out of
   every count, rate, backtest and recount, in all five theaters. Otherwise an event is used in the statistics only if credibility is **0.50 or more**
   (`napor_ids.INCLUDE_AT`). Events from 0.50 to 0.65 are used but flagged "use with caution". Below 0.50
   the event stays in the log but is dropped from cases, replies, chains, the intensity scale and every
   count. Census rows and pairs that touch such an event are dropped too.
Today the cut removes 8 of 267 Iran events (#22, #64, #67, #101 and the 4 newly under the link rule, #84, #86, #88 and #89), 3 of 123 Houthi, 3 of 162 North Korea, 2 of 130 China and 1 of 133 Venezuela events. That leaves 798 counted events (Iran 259, Houthis 120, North Korea 159, China 128, Venezuela 132).

## 4. How a US move becomes a case

A **case** is one past US move (or one quiet week) with its outcomes measured the same way for every option. Letters are
fixed in every theater: A hold, B diplomacy or talks, C to H other kinds of move (names differ; see `OPTIONS` in `config.py`).

- **Trigger options** (C to G in Iran and Houthis; C to H in China; B to H in North Korea and Venezuela). The cases are
  the theater's **Trigger Census**: every countable US move of that kind, with a status:
  `R-strong` (a reply is logged with an explicit link), `R-weak` (a distinct hostile act followed inside
  the reply window and only timing links it), `R-proxy` (a reply by a group the adversary arms), `N`
  (checked; no reply found) or `Unclear` / `Unverified` (not counted). Only R-strong, R-weak, R-proxy and N are counted.
- **Other options** (B, H and similar). Every counted US move with that letter is a case, once it has at
  least 7 days of news after it.
- **Option A (hold).** A case is a Monday-to-Monday week with no logged US sanctions, naval, strike or posture
  move, and not inside a fighting window. Weeks where an allowed outlet reports a US move missing from the log
  are left out (`UNCERTAIN`). Fewer than 3 hold weeks (`MIN_HOLD_WEEKS`, all theaters except Iran): the page says "too few cases". Start dates: Iran
  Feb 28, 2026; Houthis Nov 20, 2023; North Korea Jan 20, 2025; Venezuela Aug 11, 2025; China has none.
- **Reply window.** Iran and Houthis: about 5 days. North Korea, China and Venezuela: 7 days (`REPLY_DAYS`).
- **Fewer than 3 counted cases** (`MIN_CASES`, Houthis, North Korea, China, Venezuela): the page shows "too few cases" instead of a risk index.

## 5. Continuous-fighting exclusion windows

While both sides strike every day, every act has a "reply" by default, which would inflate the reply rate.
Moves inside these windows are context only, not cases. The act that started each stretch still counts.

| Theater | Windows | Acts that started them (kept) |
|---|---|---|
| Iran | Jul 22, 1987 - Jul 3, 1988 (Tanker War); Oct 17, 2023 - Jan 29, 2024; Jun 13-24, 2025; Feb 28 - Apr 7, 2026; Jul 7-25, 2026 | none for 1987-88; #255, #2, #57, #60 |
| Houthis | Jan 12, 2024 - Jan 19, 2025; Mar 15 - May 6, 2025 | #1021, #1307 |
| North Korea | Sep 25 - Nov 2, 2022; Sep 12 - Oct 12, 2026 | #2022, #2072 |
| China | Aug 4-31, 2022 | #3026 |
| Venezuela | Oct 27 - Nov 15, 2025; Dec 15, 2025 - Jan 2, 2026 | #4030, #4043 |

How the windows are applied differs by theater. Iran: the code removes census rows inside a window. Houthis, North Korea
and China: the research files mark such rows `Unclear`, so they are not counted. Venezuela: `theaters/common.exclude_in_windows`
(called from `rules.py`) marks census rows inside a window `Unclear`, except the start acts, so #4032, #4044, #4046 and #4048
are context only. In every theater a window also keeps hold weeks out, because a quiet week there is "a logging gap, not a hold".

## 6. The five risk categories

Every option is described with the same five categories. Each is a share: cases where the outcome happened,
out of cases where it could be judged. A case whose window is still open is not judged yet (it counts only once
the answer is already "yes"). Window lengths are in section 9.

| Category | What counts as risk |
|---|---|
| People | Anyone hurt in a reply, or civilian harm reported in the US act itself |
| Escalation | The other side acted within the window (trigger options: a reply; others: a hostile act within 7 days) |
| Military | The reply was armed in the theater's sense (below). Options that cannot draw a military reply count as 0% and that 0% is shown as assumed |
| Economic | The theater's economic measure got worse after the move (below) |
| Political | No actual talks within 14 days (section 6.2) |

### 6.1 Exact rules by theater (from each `config.py`)

**Iran** (`napor_options.py`, `napor_cases.py`, `hold_weeks.py`)
- People: a linked reply hurt someone, or the US act has civilian harm reported (#2, #74). Hold weeks: set by hand.
- Escalation: Iran or an Iran-backed group replied within about 5 days (D to G, C). Other options: Iran or a proxy struck within 7 days (Houthis are a separate front and excluded).
- Military: the reply was a kinetic strike (D to G). Hold weeks: any Iran/proxy kinetic strike in the 7 days after. B, C, H: 0% assumed.
- Economic: attacks on shipping in the 7 days after the move are more than in the 7 days before.
- Political: see 6.2. Rows added by hand: #99, #127.

**Houthis** (same structure as Iran)
- Attack kinds: Kinetic and Maritime. Economic: attacks on shipping 7 days after > 7 days before; five missile or drone hits on ships filed as Kinetic are added by ID (`SHIP_ATTACK_EXTRA`).
- Military reply: a missile, drone or boat attack. Reply window about 5 days. UN Security Council resolution 2722 (#1020) is excluded from talks.

**North Korea**
- People: anyone hurt in a North Korean reply within 7 days.
- Escalation: a missile launch, nuclear test or provocation within 7 days. A threatening statement filed as a provocation (#2045, #2049, #2051) counts because the log files it so.
- Military: the reply was a ballistic missile or ICBM (action type or cited headline says ballistic, ICBM, IRBM or SRBM). Satellite rockets, cruise missiles, drones, nuclear tests and statements do not.
- Economic: **not measured** (`ECON mode "none"`); the corner is left out of the index.

**China**
- People: anyone hurt in a Chinese reply (window 11 days, see section 9).
- Escalation: a PLA named drill, a spike of aircraft in Taiwan's air defense zone, a coast-guard confrontation or a counter-sanction within 7 days, tied to the US move by China or an allowed outlet. Routine flights and shadowing are background (status N).
- Military: the reply was a live-fire or named large-scale drill.
- Economic: a Chinese counter-sanction or trade measure within **14 days**.

**Venezuela**
- People: anyone killed or hurt in the US action itself or in a Venezuelan reply, as the source reports it. Boat-strike deaths count.
- Escalation: a hostile act by Venezuela or an armed group within 7 days: an attack, harassment of US assets, or a mobilization. Words, diplomatic steps and economic steps do not (`rules.py` re-labels census replies that were only words as `N`).
- Military: armed action only (an attack on, or armed harassment of, US forces or assets). A mobilization or exercise does not.
- Economic: a Venezuelan counter-measure within 14 days (oil or gas cut-off, airline ban, expelling firms or diplomats). Timing only; eleven such acts are logged (eight before 2019).

### 6.2 Political: "talks only" (all theaters)
Risk = no actual talks, meeting, negotiation, formal proposal, ceasefire or deal between the US and the adversary
(directly or through a mediator) logged within 14 days. Statements, threats and appeals do not count, and neither
does a multilateral act such as a UN resolution. The test is `TALK_WORDS` in `napor_options.py` ("proposal",
"talks", "ceasefire announcement", "ceasefire (", "ceasefire statement") applied to the action type of a
Diplomatic row, plus every US option-B row, plus listed exceptions (`TALK_EXTRA`, `TALK_EXCLUDE`). See section 11.

## 7. Wilson ranges and the m=2 estimate

- **Raw rate and range.** k of n, with n always shown, plus the Wilson 95% range. `wilson(k, n)` in `common.py`: with p = k/n and z = 1.96,
  centre = (p + z^2 / 2n) / (1 + z^2 / n); half-width = z x sqrt(p(1-p)/n + z^2/4n^2) / (1 + z^2 / n).
  Examples: 5 of 10 gives 24% to 76%; 0 of 10 gives 0% to 28%. Small samples give wide ranges. Tested in `tests/test_stats.py`.
- **NAPOR estimate (shrinkage, m = 2).** The option's rate is pulled toward the pooled rate for the same
  category across all options: `(k + 2 x pooled) / (n + 2)`. It steadies rates built on a handful of cases.
  It is a model rule: it is shown only for a theater where the backtest chose it, by this written rule
  (`decide()` in `backtest_risk.py`): the shrunk value must beat raw by at least 0.005 overall and be no worse
  than raw by more than 0.01 in any category. **Today only Iran passes** (gain 0.0082). Houthis, North Korea and
  China fail on overall gain; Venezuela gains 0.0093 overall but fails because the people category is worse by 0.0115.
  The page always shows the raw x of n first, as the big number, and the NAPOR estimate (where adopted) as a small second number: "NAPOR estimate: z%".
  Where it fails the page shows only the raw k of n. Raw k/n and the Wilson range are never shrunk.

## 8. The risk index

For each option, the **NAPOR risk index** is the plain average of its measured categories, with equal weights
(`risk_index()` in `export_explorer.py`). Notes:
- The page shows the raw index (the plain average of the raw category rates) as the big number, with its range; where the estimate is adopted it is shown small beside it. The formula line uses the raw rates.
- The five categories are separate rates, not slices of 100%. They do not add up to 100% and they overlap.
- A category that cannot be measured at all (North Korea economic) is left out. A category that is
  assumed 0% because the move cannot draw that kind of reply (military for options B, C, H in Iran) is
  included as 0.
- The viewer can change the weights on the page; the stored history uses equal weights. The index summarizes past
  cases. It is not a ranking and not a recommendation.

## 9. The look-back with no hindsight and the closing windows

The page can show any past date. It then uses only cases and events that were logged by that date, and a case
counts for a category only if that category's window had closed (or the answer was already "yes").
`CLOSE` gives days after the case when each category's outcome is final:

| Theater | People | Escalation | Military | Economic | Political |
|---|---|---|---|---|---|
| Iran | 7 | 5 (trigger) / 7 | 5 (reply) / 7 | 7 | 14 |
| Houthis | 7 | 5 (trigger) / 7 | 5 (reply) / 7 | 7 | 14 |
| North Korea | 7 | 7 | 7 | not measured | 14 |
| China | 11 | 7 | 11 | 14 | 14 |
| Venezuela | 18 | 7 | 18 | 14 | 14 |

Iran and Houthis use the defaults in `napor_cases.window_days`. For the others, linked replies count at any lag, so
the window must reach the longest logged lag: 11 days for China (#3056), 18 days for Venezuela (#4027 to #4031).
`window_covers_lags()` fails the build if a window is too short. Look-back dates tested per theater are in `LOOKBACKS`.

## 10. Walk-forward backtest and Brier score

`napor/backtest_risk.py` checks the method against its own history.

1. Each case and category with a final outcome becomes one row (date, closes-on date, option, category, yes/no).
2. Rows are taken in date order. For each row the method sees **only rows that closed before that row's date**
   and produces a probability: the raw rate, the shrunk estimate (m = 1, 2, 4), the pooled rate or 50%.
3. A row is skipped if its option has no closed past case for that category yet.
4. **Brier score** = average of (probability - outcome)^2. 0 is perfect; 0.25 is what "always 50%" scores. Lower is better.
5. **No-hindsight check.** A fake future case is appended; no earlier probability may change. The same check requires every
   window to cover the longest reply lag. It runs for every theater in the weekly build and in the tests.

Current results (`napor/backtest_risk.json`, `napor/theaters/<id>/backtest_risk.json`; retrospective scores, not forecasts):

| Theater | Rows | Scored | Raw | Shrunk (m=2) | Pooled | 50% | Page shows |
|---|---|---|---|---|---|---|---|
| Iran | 449 | 398 | 0.1393 | 0.1311 | 0.1554 | 0.25 | estimate |
| Houthis | 503 | 472 | 0.0567 | 0.0586 | 0.0647 | 0.25 | raw |
| North Korea | 468 | 432 | 0.0642 | 0.0621 | 0.0979 | 0.25 | raw |
| China | 264 | 230 | 0.0623 | 0.0653 | 0.0796 | 0.25 | raw |
| Venezuela | 368 | 313 | 0.0688 | 0.0595 | 0.0702 | 0.25 | raw |

Out of sample (fit through Dec 31, 2025, score 2026): Iran 0.2818 (shrunk) and 0.2775 (raw, 126 rows scored), both worse than 50%,
so the pre-war record alone did not describe the 2026 war; Houthis 0.0495; North Korea 0.0332; China 0.0027
(9 rows); Venezuela 0.0305.

## 11. Decisions taken

**Recency weighting: tested, rejected (2026-10-24, CHANGELOG).** Six versions were backtested on Iran: no weight; pre-2026
cases weighted 0.25 or 0.5; half-life 180, 365 or 730 days. The best overall was pre-2026 weight 0.25 (0.1763 vs 0.1806 with no
weight), but it made military worse by 0.022 and escalation by 0.015, which fails the written rule (adopt only if the gain is
at least 0.003 and no category is worse by more than 0.01). No change was made. On today's data (the log now starts in 1979) the best
version is a 730-day half-life, 0.1255 vs 0.1311 with no weight, with military worse by 0.0297, so the answer holds. Houthis, North Korea,
China and Venezuela also keep no weighting. The weighting code stays in place, switched off.

**Political "talks only": adopted 2026-10-26 (CHANGELOG).** Old rule: no diplomatic event of any kind in 14 days
(statements and threats included). Problem: one public threat cancelled a political risk, so the corner mostly
measured how often officials talk. Round-2 test on Iran: "talks only, 14 days" scored 0.268 against 0.304 for the live rule.
Adopted by the project owner, with the same rule in every theater. Brier of the political corner, old to new (today's data, 1979 on): Iran 0.2460 to
0.2262; Houthis 0.1219 to 0.0295; North Korea 0.0545 to 0.0362; China 0.0000 to 0.0000; Venezuela 0.0320 to 0.0320. Index Brier, old to
new: Iran 0.1409 to 0.1369; Houthis 0.0777 to 0.0593; North Korea 0.0667 to 0.0621; China and Venezuela unchanged (0.0687, 0.0592). No option's risk index moved more than 5
points. A lower score here means the new definition is easier to forecast, not that it measures political risk better.
The old rule is still computed so the Report card can show both.

## 12. Limits

- **Small n.** Many options have 1 to 7 cases, so ranges are wide and one case can move a rate by many points. The page
  shows n everywhere and "too few cases" below 3.
- **After is not because of.** A reply is a logged act inside a window. Timing links it to the US move; it does not prove cause.
- **The log is not the world.** Only events that allowed outlets reported are logged, and later years are logged more thinly
  (Houthis 2025-2026; North Korea launches; Venezuela boat strikes, about 8 of about 70 logged one by one). "None logged" is not
  proof nothing happened. Hold weeks are the most exposed.
- **Older years are thinner.** The record keeps the older years, but they are logged more thinly than recent ones, so older cases
  may be missing and numbers that rest on them are softer. Each theater's `thin_before` date (Iran May 2019, Houthis Oct 2016,
  North Korea Aug 31 2017, China and Venezuela Jan 2019) is where the denser record starts. The page says so under the header of each
  tab, in "Known limits", and tags cases before that date "older, thinner data".
- **Judgment calls.** Census statuses, `TALK_EXTRA` rows, civilian-harm entries and hold-week "people hurt" flags are set by hand
  from the logged text (Iran #115 and the Oct 2026 `Unclear` rows are examples).
- **Lopsided outcomes.** Where nearly every case has the same outcome (Houthis political: 102 of 105 had no talks; North Korea
  people: none hurt), a low Brier mostly reflects that, not skill.
- **Backtest scope.** Scores are retrospective and use definitions tuned on this same data; the shrinkage and weighting choices
  were made after earlier backtests. Iran's out-of-sample score is worse than 50%.
- **Not measured.** Oil and freight prices, harm to ordinary people in the adversary country, strain with allies, and North Korea's
  economic harm. Sources are public news only; state-media claims are labelled and scored 0.30.
- **Known gaps.** Iran #67 has no source. About 20 Iran reports are names without a link (flagged not re-checked); they get zero credit under the link rule, and four events (#84, #86, #88, #89) relied on them alone and are now excluded. The exported `n_events` counts only events at credibility 0.50 or more in every theater, Iran included (Iran logs 267, so its `n_events`, 259, is lower by the 8 under the cut).
