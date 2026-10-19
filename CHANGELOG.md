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
