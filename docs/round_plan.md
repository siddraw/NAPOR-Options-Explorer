# NAPOR: Risk Assessment - Round 2 plan (organizer, 2026-10-24)

Repo: `/home/claude/napor-risk-assessment`, branch `round2`. Workers in one wave run in parallel on
files that do not overlap. Waves run in order; the organizer reviews (checklist at the end) before
starting the next wave. **No worker commits. No worker edits a file it does not own.** If a worker
needs a change in a file it does not own, it writes the exact change in its final report instead.

Rules every worker obeys (read them in the files named):
- `docs/SOURCE_STANDARD.md` (allowed outlets; never invent a URL or quote; seen="full text"/"snippet").
- `AGENT.md` "Rules (do not break)": NAPOR **never ranks, sorts by risk, recommends or picks** an
  option. No wording like "best option", "safest", "should", "we recommend". Options stay in letter order.
- Plain language in anything a reader sees (Sidd prefers simple words).
- Final report to the organizer: files changed, commands run with their PASS/FAIL lines, open
  questions, and any change you need in a file you do not own.

---------------------------------------------------------------------------------------------------
## WAVE 1 (W1, W2, W3 in parallel)

### W1 - Recency weighting (Stage 1) and political-category proposal (Stage 2)

You are a Python + vanilla-JS engineer on NAPOR, a tool that shows US options A-H in the Iran-US war
and, for each, five risk rates (people, escalation, military, economic, political) as "x of n past
cases" with 95% Wilson ranges and a "NAPOR estimate" = (k + m*pooled)/(n + m), m=2, where pooled is the
same category's rate across all options. Read first: `README.md`, `AGENT.md`, `napor/napor_cases.py`
(case shape, `outcome()`, `window_days()`), `napor/backtest_risk.py` (walk-forward Brier, `decide()`),
`napor/export_explorer.py` (`risk_index`, `pooled_rates`, `update_history`, `recount_diff`),
`napor/verify_explorer.py`, and in `explorer/index.html` the functions `asofCase`, `catScores`,
`pooled`, `estOf`, `riskIndex`, the case pop-ups, `How this works` (~line 1153) and the Report card (~1112).

**You own (only these):** `napor/backtest_risk.py`, `napor/napor_cases.py`, `napor/export_explorer.py`,
`napor/verify_explorer.py`, `explorer/index.html`, and the files they generate: `napor/backtest_risk.json`,
`explorer/data/iran.json`, `explorer/data/iran-history.json`, `explorer/data.json`, `explorer/theaters.json`,
`explorer/verify.json`. Do not run `build.py` or `weekly_build.py` (they rewrite the workbook, not yours).
Do not edit CHANGELOG.md/AGENT.md/README.md; put the CHANGELOG text you want in your report.

**Naming:** call it the "recency weight" or "case weight" everywhere. The page already has user
"category weights" sliders (`S.w`); do not mix the two.

**Stage 1 - definitions (exact).** For a prediction or display made on as-of date T, case i (date d_i,
outcome y_i in {0,1}) gets weight w_i. Candidates:
- `none`: w=1 (current behaviour).
- `era25`, `era50`: w=0.25 / 0.5 if d_i < 2026-01-01, else 1.
- `hl180`, `hl365`, `hl730`: w = 0.5 ** ((T - d_i).days / H), H = 180/365/730.
Weighted rate p_w = sum(w*y)/sum(w). Effective n: n_eff = sum(w). Pooled prior p_pool = the same weighted
formula over all options' counted cases in that category (same w). Estimate = (sum(w*y) + 2*p_pool)/(n_eff + 2).
"Assumed 0" military corners stay 0. Raw k/n and the Wilson range stay on the **unweighted** k, n.
In the backtest T = the predicted case's date and only rows with `closes < T` are used (unchanged rule);
hold weeks use their Monday as d_i. Keep `raw`, `shrunk1/2/4`, `pooled`, `half` rows as now; add
`w_<cand>` methods (weighted + shrunk m=2) for the 6 candidates (`w_none` must equal `shrunk2`).
Report Brier overall, per category, and 2026-only (rows dated >= 2026-01-01) for every candidate.

**Adoption rule (write it into a `decide_weighting()` next to `decide()`):** adopt the candidate with the
lowest overall Brier only if it beats `w_none` by >= 0.003 overall AND is not worse than `w_none` by more
than 0.01 in any category; otherwise keep `none` and print "KEEP no recency weighting". Ties: pick the
milder weight (none < era50 < hl730 < hl365 < era25 < hl180). Store the result in `backtest_risk.json` and
in the page data as `estimate.weighting = {scheme, param, adopt, gain, worse_by_cat, rule}`.
`no_hindsight_check` must still PASS with weights (extend it to compare the `w_*` methods too).

**Everywhere the estimate appears, use the adopted weighting:** `export_explorer.risk_index` /
`pooled_rates` / history `estimate`, the page (`pooled`, `estOf`, `riskIndex`; T = `S.asof` or `D.asof`
when not looking back - look-back must never use a case dated after T), and `verify_explorer.py`, which
must compute the weights itself (no import of napor_cases/export_explorer) and write, per option and
category, `[k, n, sum_wy, sum_w]` plus the estimate at `D.asof` into `explorer/verify.json`.
`recount_diff` compares all four numbers (tolerance 1e-9). If `none` wins, numbers must be unchanged.

**Page:** in each case pop-up show "Recency weight 0.42 (case is 400 days old)" (or "weight 1" when none);
keep "x of n" visible; add 2-4 plain sentences in "How this works" and one Report card card "Older cases
count less?" with a small table of the 6 candidates (overall / 2026-only Brier) and the decision text.
No new ranking or sorting of options.

**Stage 2 - political proposal (do NOT change the live rule).** Current rule: risk = no event of kind
Diplomatic (any side, incl. statements) within 14 days (`O._talks`). Backtest with the same walk-forward:
(P1) no talks/proposal/ceasefire/deal event (words as `_CONC` in export_explorer) within 30 days;
(P2) no talks/proposal/ceasefire/deal event within 14 days; (P3) political left out of the index (report
the index-level Brier effect: average of the other four). Report Brier vs the current rule and vs 0.25.
Page: Report card table titled exactly "Proposal - needs Sidd's approval", plus `report_card.political_proposal`
in the data. The live political numbers must stay exactly as today.

**Acceptance checks:** `cd napor && python3 backtest_risk.py` prints the candidate table, a weighting
decision line and "No-hindsight check ... PASS"; `python3 export_explorer.py` prints "page counts match
workbook counts" and "risk rates match the independent recount" and exits 0; `python3 verify_explorer.py`
runs; a Node check (`node` is at /opt/node22/bin/node; keep the script in your scratch dir, not the repo)
evaluates the page's `catScores/pooled/estOf/riskIndex` on `explorer/data/iran.json` and matches
`verify.json` for every option/category to 4 decimals, both at D.asof and at one look-back date;
if `none` is kept, `git diff --stat explorer/data/iran.json` changes only generated dates/new keys
(prove with a small diff of option numbers). Open the page in a browser if you can; it must load with
no console errors. Report the full candidate table and the decision in your report.

### W2 - Houthi event log, Oct 2016 - Dec 2024 (research)

You are a careful researcher building a sourced event log for a new NAPOR "Houthis / Red Sea" tab.
Read first: `docs/SOURCE_STANDARD.md`, `docs/THEATERS.md` (section 1), and `napor/prewar.py` -
**copy its file structure exactly**: `d()`, `_s()`, `EVENTS` (10-column tuples: ID, date, actor, action
type, target, detail, trigger ID, severity/damage, confidence, "see audit"), `SOURCES`, `VERDICT`,
`PARTLY`, `CENSUS`, `PAIRS`, `WINDOWS`, `START_ACTS`, `PHASES`, `CHAIN_NAMES`.
**You own only:** `napor/theaters/houthis/events_early.py` (create the folders; no `__init__.py`, W4 adds it).

**IDs (integers - the engine uses int IDs):** events 1001-1299, pairs 1001-1299. Never use another range.

**Scope:** US moves toward the Houthis and Houthi actions toward US forces, US-linked or commercial
shipping, Oct 2016 - Dec 31, 2024. Must include, if confirmed: Oct 2016 Mason missile attacks and the
Oct 13 2016 US Tomahawk strikes on radar sites; Iranian-arms seizures bound for the Houthis (prewar #264
and #265 are already in the Iran log - log them here too with a note "also Iran log #264"); the Jan 2021
FTO designation and Feb 2021 revocation; Nov 19 2023 Galaxy Leader seizure; Dec 2023 Operation Prosperity
Guardian; the Jan 12 2024 first US/UK strikes; Jan 17 2024 SDGT re-designation; key 2024 strikes, ship
sinkings (Rubymar, True Confidence deaths, Tutor), and US drone (MQ-9) losses. Target 30-45 events.

**Option tag (required, because the keyword classifier would mis-sort them):** add
`US_OPTION = {event_id: letter}` for every US move, letters: B Diplomacy/talks, C Sanctions/designations,
D Naval defense/escort (incl. shooting down Houthi missiles/drones aimed at ships), E Interdict Iranian
arms shipments, F Strike Houthi military sites, G Strike risking personnel/leaders, H Force posture.
Action-type strings should still contain the usual words (sanction, deploy/posture, seizure, strike, talks).

**Sources:** only outlets in SOURCE_STANDARD (CENTCOM, DoD, Treasury/OFAC, State, UKMTO, UN count as
official). Houthi media (al-Masirah, Saba) **only as labelled claims**: outlet string
`"al-Masirah (Houthi claim)"`, and say "Houthis CLAIM" in the detail. Every URL must have come back from
WebSearch/WebFetch in this session. Wikipedia only as a map to the cited outlet. If not confirmed, leave
the event out (or VERDICT "not_confirmed"). Credibility is computed by the engine from your sources
(`napor/napor_ids.py`: full-text allowed outlet 0.80, two outlets 0.96, claim-only 0.30; under 0.50 is not
counted) - so aim for 2 outlets per counted event, full text where possible. Add `CRED_ESTIMATE = {id: x}`
with your own 0-1 estimate by that formula so the organizer can spot-check.

**Census and pairs:** a `CENSUS` row for each US move of kinds C-H: (id, "Economic/Blockade" |
"Military/Property" | "Personnel/Casualty", status, note). Status: R-strong (Houthis say it is a reply and
attack within ~5 days), R-weak (attack within ~5 days, link plausible), R-proxy (not used here unless an
attack comes from another Iran-backed group), N (no Houthi attack on US forces/shipping found in the 5
days - say what you searched), Unclear, Unverified. `PAIRS` for every trigger -> reply (pair id, trigger,
reply, category, casualties Y/N, note). `WINDOWS`: continuous-fighting stretches whose US strikes are
context only - at least Jan 12 2024 -> Dec 31 2024 (end of your era; W3 continues it) unless you find a
real lull; `START_ACTS` = the act that opens each window (counted).

**Acceptance:** `python3 -c "import sys; sys.path.insert(0,'napor/theaters/houthis'); import events_early as E; print(len(E.EVENTS))"`
works; every EVENTS id has SOURCES and VERDICT; every CENSUS/PAIRS/US_OPTION id exists in EVENTS; all ids
in range; no URL from memory. Report: event count, counted vs context, list of not-confirmed items.

### W3 - Houthi event log, Jan 2025 - Oct 24 2026 (research)

Same brief as W2 (read it above: structure, sources, claims labelling, US_OPTION letters, census, pairs,
CRED_ESTIMATE, acceptance checks) with these differences.
**You own only:** `napor/theaters/houthis/events_late.py`. **IDs:** events 1301-1599, pairs 1301-1599.
**Scope:** Jan 1 2025 - Oct 24 2026: Jan 2025 Houthi pause after the Gaza ceasefire; Jan 22 2025 executive
order and Mar 2025 FTO re-designation; Operation Rough Rider (from Mar 15 2025: opening strikes, notable
strikes incl. Ras Isa port and Saada migrant-centre deaths, MQ-9 and F/A-18 losses); May 6 2025 Oman-brokered
US-Houthi ceasefire; any 2025-2026 Houthi attacks on shipping (e.g. Jul 2025 Magic Seas / Eternity C) and
US responses; Treasury/OFAC Houthi sanctions; 2026 events, including the Oct 2026 Saudi-Houthi fighting and
US threats/statements (the Iran log has #98 and #102 - log them here with a note "also Iran log #98").
Target 20-40 events. **WINDOWS:** the continuation of W2's window until its real end (Jan 19 2025 pause, if
confirmed) and Mar 15 - May 6 2025; START_ACTS includes the Mar 15 2025 opening strike.
Add `CONSTRAINTS = [(start, end, "text", [event ids])]` for periods an option was limited (e.g. May 6 2025
ceasefire -> F/G constrained). Coordinate nothing with W2 except the ID ranges; overlap at Jan 2025 is fine.

---------------------------------------------------------------------------------------------------
## WAVE 2 (after wave 1 is reviewed and committed)

### W4 - Per-theater engine and the Houthi tab

You are a Python engineer generalizing NAPOR from one conflict (Iran) to several. Read: `README.md`,
`AGENT.md`, `docs/THEATERS.md`, all of `napor/` (start with `data.py`, `napor_ids.py`, `napor_options.py`,
`napor_cases.py`, `hold_weeks.py`, `napor_threads.py`, `export_explorer.py`, `verify_explorer.py`,
`backtest_risk.py`, `weekly_build.py`), `napor/theaters/houthis/events_early.py` and `events_late.py`
(research files - **read only**), `explorer/index.html` (theater code ~lines 412, 1163-1199).
**You own:** everything under `napor/` except `napor/theaters/houthis/events_*.py`; `explorer/theaters.json`,
`explorer/data/houthis.json`, `explorer/data/houthis-history.json`, the Iran generated files, and
`explorer/index.html` (fix only what breaks for the Houthi tab - no redesign).

**Target layout:** `napor/theaters/<id>/` packages with `config.py` (wording dict now in
`export_explorer.THEATER`; option set; per-option flags as `napor_cases.FLAGS`; category wording;
claim-media outlets; actor test for "adversary side"; hold-week rules; constraint periods), `cases.py`,
and thin `export/verify/backtest` entry points that the top-level `export_explorer.py`, `verify_explorer.py`,
`backtest_risk.py` and `weekly_build.py` loop over for every theater in `explorer/theaters.json`.
`iran` wraps the existing modules. **Iran output must be numerically identical** to the committed wave-1
`explorer/data/iran.json` (prove: a script comparing every option's cases and k/n/estimate; only
`generated` may differ). Keep `explorer/data.json` = Iran fallback.

**Things the current code hard-wires that you must make per theater:** `napor_ids.STATE_MEDIA` is Iranian
only - claim-only outlets per theater (Houthis: al-Masirah, Saba; scored 0.30); `napor_options._usable`
drops actors starting "houthi" and `_iran_side` defines the adversary - per theater; option membership -
Houthis use the research files' `US_OPTION` map, not `act_kind` keywords (seizures would otherwise land in D);
continuous-war `WINDOWS`/`START_ACTS` and `CONSTRAINTS` from the research files; `napor_threads` imports
`prewar` directly; `hold_weeks` is 2026-Iran only.

**Houthi config:** adversary "the Houthis", actor "the Houthis or another Iran-backed group", proxy note
(Iran arms the Houthis; Iranian-arms seizures are option E); options A Hold, B Diplomacy, C Sanctions/
designations, D Naval defense/escort, E Interdict Iranian arms shipments, F Strike Houthi military sites,
G Strike risking personnel/leaders, H Force posture; flags: trigger C-G, military "reply" D-G, "none" B/C/H;
economic = Houthi attacks on shipping 7 days after > 7 days before; political as the live Iran rule (and
wave-1 weighting if adopted). Hold weeks (A): only weeks inside a densely logged stretch (propose
Nov 19 2023 - present minus WINDOWS); if fewer than 3, show A as "too few cases", do not invent weeks.
Mark n <= 3 as "very thin evidence" (page already does).

**Acceptance:** `cd napor && python3 weekly_build.py` prints PASS for every step and every theater;
backtest no-hindsight PASS per theater; the Houthi recount matches; page loads both tabs (`#iran`,
`#houthis`) with no console errors, look-back works, pop-ups show sources, Report card shows the Houthi
backtest; Iran identity proof attached. AGENT.md/README/CHANGELOG edits go in your report (W7 applies them).

---------------------------------------------------------------------------------------------------
## WAVE 3 (after the Houthi tab is reviewed)

### W5 - North Korea theater

You build the NAPOR North Korea tab on the per-theater engine (read `napor/theaters/houthis/` as the
model, plus `docs/SOURCE_STANDARD.md`, `docs/THEATERS.md` section 2, W2's brief above for record rules).
**You own only:** `napor/theaters/northkorea/` and `explorer/data/northkorea*.json`. Do not edit
`explorer/theaters.json` (W7 registers the tab); to test, pass the theater id to the export entry point.
**IDs:** events/pairs 2001-2999.
**Research 2017 - Oct 24 2026:** US/ROK(/Japan) drills, strategic-asset deployments (bombers, carriers,
SSBN visits), sanctions, talks/summits (Singapore, Hanoi, DMZ), and DPRK missile launches/nuclear tests/
provocations as replies, dated by South Korea's JCS or Japan's MoD as reported by allowed outlets.
KCNA/Rodong Sinmun only as labelled claims (claim-only outlets in config). Target 40-70 events.
**Config (write each definition into `config.py`, plain words):** options A Hold, B Talks/summit offer,
C Sanctions, D Joint drills, E Strategic-asset deployment, F Missile-defense moves, G Interdiction/
ship-to-ship enforcement, H Force posture (adjust only with reason). Categories: escalation = DPRK missile
launch, nuclear test or military provocation within 7 days; people = anyone hurt; military = launch over/near
Japan or a live-fire provocation; economic = say "not measured" unless a clear measure exists (do not force
a shipping measure); political = no talks/contact within 14 days. Mark routine launch seasons honestly.
**Acceptance:** export, verify recount and backtest (no-hindsight PASS) run for `northkorea`; every counted
event has allowed sources; report n per option.

### W6 - China: Taiwan Strait and South China Sea theater

Same rules as W5 (read its brief). **You own only:** `napor/theaters/china/` and `explorer/data/china*.json`.
**IDs:** 3001-3999. **Research 2019 - Oct 24 2026:** Taiwan Strait transits and SCS FONOPs, arms sales to
Taiwan, high-level visits (Pelosi Aug 2022, Tsai-McCarthy Apr 2023, etc.), sanctions/export controls, talks;
replies = PLA drills (Joint Sword etc.), ADIZ surges as reported, coast-guard actions, sanctions on US firms.
Xinhua, Global Times, CGTN, PLA Daily, Chinese MND/MFA only as labelled claims of what China says.
Separate "background" PLA activity from replies: a reply needs a dated PLA/coast-guard action that China or an
allowed outlet links to the US move, or a clear step up within 7 days (R-weak). Options adapted (B talks,
C sanctions/export controls, D transit/FONOP, E arms sale, F high-level visit, H posture; G only if real cases
exist, else "not measured"). **Say clearly in the config and page wording where n is small.**
**Acceptance:** as W5.

### W7 - Register, document, weekly build PASS (after W5/W6 reviewed)

**You own:** `explorer/theaters.json`, `AGENT.md`, `README.md`, `CHANGELOG.md`, `docs/THEATERS.md`,
`napor/weekly_build.py`. Register `northkorea` and `china` (status, data path) next to `iran`, `houthis`;
update AGENT.md weekly steps to scan every theater with its own claim-media rule and to publish all data files
(`files` map in step 9); README scope and known limits per theater; CHANGELOG entries for waves 1-3 (use the
texts the workers put in their reports, dated); THEATERS.md status. Run `cd napor && python3 weekly_build.py`
until PASS for all four theaters. Do not change engine or theater files; report any failure you cannot fix.

---------------------------------------------------------------------------------------------------
## REVIEW CHECKLIST (organizer, every worker)

1. Only owned files changed (`git status`, `git diff --stat`); nothing committed.
2. Sources: every counted event has an allowed outlet; spot-check 5 URLs per research file with WebFetch
   (real, says what the row says); claims (IRNA/Tasnim/al-Masirah/KCNA/Xinhua...) labelled and scored 0.30.
3. Credibility < 0.50 events are not counted anywhere (census, pairs, windows of other cases).
4. No hindsight: no-hindsight check PASS; look-back on the page uses only cases/outcomes known by that date;
   recency weights measured from the as-of date.
5. Iran numbers unchanged, except the approved recency weighting (diff of option k/n/estimate).
6. Python, independent recount and page JS agree (export self-checks, verify.json, Node check).
7. No ranking/recommending: grep new text for best|safest|recommend|should|rank|top; options in A-H order.
8. Weighting/political decisions follow the written rules; political change shown only as "Proposal - needs
   Sidd's approval".
9. Page loads every tab with no console errors; pop-ups, look-back, Report card work; phone width OK.
10. `cd napor && python3 weekly_build.py` -> RESULT: PASS (from wave 2 on).
