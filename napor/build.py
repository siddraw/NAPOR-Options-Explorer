import datetime as dt
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

FONT_NAME = "Arial"
HEADER_FILL = PatternFill("solid", fgColor="1F3B57")
HEADER_FONT = Font(name=FONT_NAME, bold=True, color="FFFFFF", size=10)
BASE_FONT = Font(name=FONT_NAME, size=10)
BOLD = Font(name=FONT_NAME, bold=True, size=10)
WRAP = Alignment(wrap_text=True, vertical="top")
THIN = Side(style="thin", color="D9D9D9")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

HIGH_FILL = PatternFill("solid", fgColor="E2EFDA")   # confidence High
MED_FILL = PatternFill("solid", fgColor="FFF2CC")    # confidence Medium
LOW_FILL = PatternFill("solid", fgColor="FCE4E4")    # confidence Low

import napor_ids as NAPOR
import napor_threads as THREADS
import napor_intensity as INTENSITY
from data import d, events, pairs, MONTHS, census, census_exclusions, event_audit, census_evidence, pairs_on_hold, event_kind
from audit_sources import SOURCES as AUDIT_SOURCES, CENSUS_SOURCES
# NAPOR credibility rule: events under 0.50 credibility are left out of every statistic.
pairs, _pairs_low_cred = NAPOR.filter_pairs(pairs)
census, _census_low_cred = NAPOR.filter_census(census)
if _census_low_cred:
    census_exclusions.append("Left out by the credibility rule (event credibility under 0.50, or a merged duplicate): " + ", ".join("#%d" % c[0] for c in _census_low_cred) + ".")

n_pending = sum(1 for a in event_audit.values() if a['check'] == 'Pending')
n_unsup = sum(1 for a in event_audit.values() if a['check'] == 'Not supported')
n_verified = sum(1 for a in event_audit.values() if a['check'] in ('Verified', 'Corrected', 'Partly verified'))

wb = Workbook()

# --- Sheet: Read Me -----------------------------------------------------
ws = wb.active
ws.title = "Read Me"
ws.sheet_view.showGridLines = False
lines = [
    ("NAPOR: Options Explorer - Iran-US War", BOLD, 14),
    ("NAPOR is the underlying engine (event log, credibility, chains, phases, forecasts). NAPOR: Options Explorer applies it to lay out the options and the risks and pros of each one. It does not pick an option. Built by Sidd.", BASE_FONT, 11),
    ("", BASE_FONT, 10),
    ("What this is", BOLD, 11),
    ("A structured, dated log of US/Israel-Iran war events from Feb 28, 2026 to Oct 26, 2026, built for computing base rates (how often does X follow Y, and how fast) rather than for narrative reading.", BASE_FONT, 10),
    ("", BASE_FONT, 10),
    ("Sheets", BOLD, 11),
    ("Event Log - every event, one row each, with a Trigger ID column pointing to the row that caused it, where reporting says so. Columns N-O count the reports behind each event and how many different independent or official outlets they come from.", BASE_FONT, 10),
    ("Credibility (0-1) - every report gets a weight = source score x fit score. Source score: credible outlet or official statement 0.80, other outlet 0.60, Iranian state media 0.30 (it can only show what Iran claims). Fit score (how sure we are the story is about this event): read in full 1.00, headline only 0.80, outlet named but story not saved 0.65. Reports under 0.30 do not count. An event combines its reports, each outlet counted once, as 1 - (1-w1)(1-w2)..., the chance that not every outlet got it wrong: one full-text credible story = 0.80, two different outlets = 0.96. Partly verified rows are multiplied by 0.8; Not supported rows are capped at 0.20. RULE: only events at 0.50 or above are used in the statistics; 0.50-0.65 is used but flagged 'use with caution'. The Confidence column (High 0.80+, Medium 0.50-0.80, Low under 0.50) now comes from this score. This is a scoring rule, not a statistical confidence interval.", BASE_FONT, 10),
    ("Chains & Phases - every event is tagged with the war phase it happened in (open war, fragile ceasefire, low-intensity war, holding pattern) and, if it is part of a back-and-forth, a chain ID (T01...). The sheet shows reply rates by phase and how long back-and-forths usually last.", BASE_FONT, 10),
    ("War intensity - a 0-and-up points gauge of how hot the war was in the 14 days before any date (2 per direct strike, 1 per shipping/blockade act, +2 if deadly), banded Quiet/Low/Medium/High. Shown in the Event Log and on Chains & Phases. It did not improve the backtest, so it is a gauge, not an input to the numbers.", BASE_FONT, 10),
    ("Forecast Log - the report card. Predictions are written down before the outcome is known, then resolved and scored (Brier score).", BASE_FONT, 10),
    ("Reports - the ID system. Every news story or official statement gets its own report ID (R0001...) and points to exactly one event ID. Three outlets covering one attack = three reports, one event. Merged duplicates: #76 into #75, #49 into #50, #29 into #28; their reports now point to the surviving event.", BASE_FONT, 10),
    ("Review Queue - pairs of events that might be the same event logged twice, plus new stories waiting for a human to confirm which event they belong to. The matcher is right only about half the time on headlines, so a person makes the call.", BASE_FONT, 10),
    ("Action-Reaction Pairs - the clean trigger->response pairs pulled out of the Event Log, with response time in days and a Trigger Category (what kind of cost the trigger imposed) computed/tagged per row. This is the closest thing to a base-rate dataset.", BASE_FONT, 10),
    ("Factor Analysis - breaks response speed and reliability down by Trigger Category, to show which kind of cost (human casualties vs economic/property loss vs political moves) provokes the fastest, most reliable response, with 95% confidence intervals since some groups are small. All formulas, recalculates automatically.", BASE_FONT, 10),
    ("Trigger Census - the fix for the biggest weakness in Factor Analysis. Factor Analysis only looks at pairs where a reply DID happen, so it says how fast replies are, not whether they come. The census lists every countable hostile act and records whether a reply followed, including the ones where none did, then gives the chance of any reply within 5 days (best estimate plus low/high range).", BASE_FONT, 10),
    ("Options - every option the US has (hold, diplomacy, sanctions, naval pressure, strikes on shipping, strikes on military sites, strikes risking personnel, force posture), side by side, each with its risks and how many past cases back them, organised as a risk profile: every option on the same five risks (harm to people, escalation, military cost, economic harm, political/diplomatic) plus pros, each cell saying what was measured or 'not measured'. Analyst notes are shaded grey. NAPOR does not rank or pick an option. This replaces the old Decision Model and its ranking.", BASE_FONT, 10),
    ("Monthly Summary - strikes by each side, shipping/blockade incidents and diplomatic events per month, counted by formula from the Event Log's 'Kind of act' column (so sanctions, deployments and statements are no longer counted as strikes). It recalculates if you edit or add rows.", BASE_FONT, 10),
    ("", BASE_FONT, 10),
    ("Source standard", BOLD, 11),
    ("Only credible news outlets and official statements count as sources (AP, Reuters, NPR, CBS, ABC, NBC, CNN, Al Jazeera, Axios, USNI News, The War Zone, Stars and Stripes, CENTCOM/DoD/Treasury). Wikipedia is not accepted: the first draft of this log cited it for 62 of 89 events, and every one of those was sent back to credible reporting. Event Log column K shows each row's source check (Verified / Corrected / Partly verified / Not supported / Pending / Date conflict / Not re-checked) and column L says what changed. The Reports sheet lists every news story behind each event, each with its own report ID. Casualty figures from Iranian officials or state media are labelled as claims. Wire stories were often read through syndicated copies on local-news sites: the underlying outlet is cited and the copy's host appears in the Reports sheet.", BASE_FONT, 10),
    ("Dates are as reported. US and Gulf time can differ by a day, so response times carry about +/-1 day of uncertainty; 'within 1 day' is the least fragile measure. Pair 21 is held out of all statistics because the event it points to (#76) looks like a duplicate of #75.", BASE_FONT, 10),
    ("", BASE_FONT, 10),
    ("Confidence column", BOLD, 11),
    ("High = multiple corroborating sources / official confirmation. Medium = single-source or one-sided claim. Low = explicitly disputed or contested by another party. Use this to weight rows, don't drop Medium/Low - contested claims are still informative about intent, even when the damage figure isn't reliable.", BASE_FONT, 10),
    ("", BASE_FONT, 10),
    ("Known gaps / caveats", BOLD, 11),
    ("1. This favors events involving Jordan, since that's the best-documented US-basing target. Bahrain/Kuwait/Qatar strikes are under-represented relative to how often they actually happened.", BASE_FONT, 10),
    ("2. This is a curated log of things that WERE reported, not a full census. The Action-Reaction Pairs and Factor Analysis sheets therefore only show 'how fast, GIVEN a reply happened'. The Trigger Census sheet adds the missing denominator (hostile acts that drew no reply) for strikes, seizures, blockade moves and sanctions; diplomatic moves are not covered, and the rows marked Unverified there have not been checked against outside sources yet.", BASE_FONT, 10),
    ("3. Casualty and damage figures often conflict between US/Israeli, Iranian, and Jordanian sources - where they conflict, that's noted in the Severity column rather than picked between.", BASE_FONT, 10),
    ("4. Individual tanker/shipping attacks (there were 40+) are not all logged here - only the ones that were a clear trigger or response, or were unusually severe. A fuller list would have to be compiled from UKMTO and CENTCOM incident reports.", BASE_FONT, 10),
    ("5. Row 68 (Aug 19) is an analyst's strategic assessment, not an event - kept for context on why the Aug-Sept escalation pattern looks different from June-July.", BASE_FONT, 10),
    ("", BASE_FONT, 10),
    ("Event matcher", BOLD, 11),
    ("matcher.py (same folder) takes a new headline/snippet, checks it's Iran/US-war relevant, guesses which actor acted and which cost-category it falls in (Personnel/Casualty, Military/Property, Economic/Blockade, Political/Diplomatic), finds the closest past events by keyword overlap, and shows what historically followed them plus the base-rate stats for that category - all computed from the same data as the Factor Analysis sheet, so the two can never disagree. It's a keyword-rule matcher, not a trained model - with 86 events that's more honest than a model that would just memorize noise.", BASE_FONT, 10),
    ("", BASE_FONT, 10),
    (f"Compiled: {dt.date.today().isoformat()}. Sources are cited per row; see Event Log column J. Rows 83-86 were added by a live scanner test (Sept 27-29). Rows 90-105 were added on Oct 11 from credible-outlet research covering Oct 2-11 (no US/Israeli strike on Iran and no Iranian strike on a US base was found in that window; the two Houthi rows are context from the separate Saudi-Houthi front). Rows 106-115 were added by the weekly agent on Oct 19 (Oct 12-18 news, plus catch-up rows for Oct 6 and Oct 8); again no US strike on Iranian territory and no Iranian strike on US forces was found, while attacks on shipping hit a record. Rows 87-89 were added by a live matcher test on genuinely new Oct 1 news - the matcher correctly classified the sanctions and diplomatic-statement rows; it fell back to a generic 'Military/Property' guess on the naval force-posture row since that's a troop deployment, not a strike, and the keyword rules don't have a dedicated bucket for that yet. Source audit: {n_pending} events are still Pending credible sourcing and {n_unsup} are Not supported as logged (including #76, a confirmed duplicate of #75); treat those rows, and the Partly verified rows that rest on one side's claims, as leads, not findings.", BASE_FONT, 10),
]
for i, (text, font, size) in enumerate(lines, start=1):
    c = ws.cell(row=i, column=1, value=text)
    c.font = Font(name=FONT_NAME, bold=font.bold, size=size, color=font.color if font.color else "000000")
    c.alignment = Alignment(wrap_text=True, vertical="top")
ws.column_dimensions["A"].width = 130

# --- Sheet: Event Log -----------------------------------------------------
ws = wb.create_sheet("Event Log")
headers = ["ID", "Date", "Actor", "Action Type", "Target", "Detail", "Trigger ID", "Severity / Casualties", "Confidence", "Source (credible outlets only)", "Source Check", "Audit note", "Kind of act", "Reports", "Different outlets (independent + official)", "Credibility (0-1)", "Used in stats?", "War phase", "Chain (thread ID)", "War intensity (14 days before)"]
for j, h in enumerate(headers, start=1):
    c = ws.cell(row=1, column=j, value=h)
    c.font = HEADER_FONT
    c.fill = HEADER_FILL
    c.alignment = Alignment(vertical="center")
    c.border = BORDER
ws.freeze_panes = "A2"

for i, row in enumerate(events, start=2):
    (eid, date_, actor, atype, target, detail, trig, sev, conf, src) = row
    conf = NAPOR.credibility_label(NAPOR.event_credibility(eid))
    vals = [eid, date_, actor, atype, target, detail, trig, sev, conf, src, event_audit[eid]['check'], event_audit[eid]['note'], event_kind[eid], (0 if eid in NAPOR.MERGED else NAPOR.corroboration(eid)['reports']), (0 if eid in NAPOR.MERGED else NAPOR.corroboration(eid)['independent'] + NAPOR.corroboration(eid)['official']), NAPOR.event_credibility(eid), NAPOR.used_in_stats(eid), THREADS.event_phase[eid], THREADS.event_thread.get(eid, ''), INTENSITY.band(INTENSITY.event_intensity[eid]) + f' ({INTENSITY.event_intensity[eid]} pts)']
    for j, v in enumerate(vals, start=1):
        c = ws.cell(row=i, column=j, value=v)
        c.font = BASE_FONT
        c.border = BORDER
        c.alignment = WRAP
        if j == 2 and isinstance(v, dt.date):
            c.number_format = "yyyy-mm-dd"
    conf_cell = ws.cell(row=i, column=9)
    if conf_cell.value == "High":
        conf_cell.fill = HIGH_FILL
    elif conf_cell.value == "Medium":
        conf_cell.fill = MED_FILL
    elif conf_cell.value == "Low":
        conf_cell.fill = LOW_FILL

widths = [5, 12, 16, 24, 22, 55, 10, 40, 11, 34, 16, 60, 12, 9, 14, 12, 22, 17, 10, 16]
for j, w in enumerate(widths, start=1):
    ws.column_dimensions[get_column_letter(j)].width = w
CHECK_FILL = {"Verified": HIGH_FILL, "Corrected": HIGH_FILL, "Partly verified": MED_FILL, "Date conflict": MED_FILL,
              "Not re-checked": PatternFill("solid", fgColor="EDEDED"), "Pending": LOW_FILL, "Not supported": LOW_FILL}
for i in range(2, 2 + len(events)):
    ck = ws.cell(row=i, column=11)
    if ck.value in CHECK_FILL:
        ck.fill = CHECK_FILL[ck.value]
ws.auto_filter.ref = f"A1:T{1 + len(events)}"
for i in range(2, 2 + len(events)):
    _u = ws.cell(row=i, column=17)
    _u.fill = HIGH_FILL if _u.value == "Yes" else (MED_FILL if str(_u.value).startswith("Yes") else LOW_FILL)
    ws.cell(row=i, column=16).number_format = "0.00"

n_events = len(events)
last_event_row = 1 + n_events  # header + rows

# --- Sheet: Action-Reaction Pairs -----------------------------------------
ws2 = wb.create_sheet("Action-Reaction Pairs")
headers2 = ["Pair ID", "Trigger ID", "Trigger Date", "Trigger Actor", "Trigger Action",
            "Response ID", "Response Date", "Response Actor", "Response Action",
            "Response Time (days)", "Trigger Category", "Response Caused Casualties", "Notes"]
for j, h in enumerate(headers2, start=1):
    c = ws2.cell(row=1, column=j, value=h)
    c.font = HEADER_FONT
    c.fill = HEADER_FILL
    c.border = BORDER
ws2.freeze_panes = "A2"

EL = "'Event Log'"
for i, (pid, trig_id, resp_id, category, resp_casualty, note) in enumerate(pairs, start=2):
    ws2.cell(row=i, column=1, value=pid)
    ws2.cell(row=i, column=2, value=trig_id)
    ws2.cell(row=i, column=3, value=f"=INDEX({EL}!$B$2:$B${last_event_row},MATCH(B{i},{EL}!$A$2:$A${last_event_row},0))")
    ws2.cell(row=i, column=3).number_format = "yyyy-mm-dd"
    ws2.cell(row=i, column=4, value=f"=INDEX({EL}!$C$2:$C${last_event_row},MATCH(B{i},{EL}!$A$2:$A${last_event_row},0))")
    ws2.cell(row=i, column=5, value=f"=INDEX({EL}!$F$2:$F${last_event_row},MATCH(B{i},{EL}!$A$2:$A${last_event_row},0))")
    ws2.cell(row=i, column=6, value=resp_id)
    ws2.cell(row=i, column=7, value=f"=INDEX({EL}!$B$2:$B${last_event_row},MATCH(F{i},{EL}!$A$2:$A${last_event_row},0))")
    ws2.cell(row=i, column=7).number_format = "yyyy-mm-dd"
    ws2.cell(row=i, column=8, value=f"=INDEX({EL}!$C$2:$C${last_event_row},MATCH(F{i},{EL}!$A$2:$A${last_event_row},0))")
    ws2.cell(row=i, column=9, value=f"=INDEX({EL}!$F$2:$F${last_event_row},MATCH(F{i},{EL}!$A$2:$A${last_event_row},0))")
    ws2.cell(row=i, column=10, value=f"=G{i}-C{i}")
    ws2.cell(row=i, column=11, value=category)
    ws2.cell(row=i, column=12, value=resp_casualty)
    ws2.cell(row=i, column=13, value=note)
    for j in range(1, 14):
        c = ws2.cell(row=i, column=j)
        c.font = BASE_FONT
        c.border = BORDER
        c.alignment = WRAP

last_pair_row = 1 + len(pairs)
# Summary stat under the table
srow = last_pair_row + 2
ws2.cell(row=srow, column=1, value="Average response time (days):").font = BOLD
ws2.cell(row=srow, column=2, value=f"=AVERAGE(J2:J{last_pair_row})").font = BOLD
ws2.cell(row=srow+1, column=1, value="Median response time (days):").font = BOLD
ws2.cell(row=srow+1, column=2, value=f"=MEDIAN(J2:J{last_pair_row})").font = BOLD
ws2.cell(row=srow+2, column=1, value="Number of pairs (n):").font = BOLD
ws2.cell(row=srow+2, column=2, value=f"=COUNT(J2:J{last_pair_row})").font = BOLD
ws2.cell(row=srow+3, column=1, value="Share responded within 1 day:").font = BOLD
ws2.cell(row=srow+3, column=2, value=f"=COUNTIF(J2:J{last_pair_row},\"<=1\")/COUNT(J2:J{last_pair_row})").font = BOLD
ws2.cell(row=srow+3, column=2).number_format = "0%"

hold_row = srow + 5
ws2.cell(row=hold_row, column=1, value="Pairs on hold (not counted in any statistic):").font = BOLD
for k, hp in enumerate(pairs_on_hold, start=hold_row + 1):
    ws2.cell(row=k, column=1, value=f"Pair {hp[0]}: trigger #{hp[1]} -> response #{hp[2]} ({hp[3]}). {hp[5]} Held because: event #{hp[2]} is likely a duplicate of #{hp[1]}.").font = BASE_FONT

widths2 = [8, 10, 12, 14, 40, 10, 12, 14, 40, 12, 18, 16, 45]
for j, w in enumerate(widths2, start=1):
    ws2.column_dimensions[get_column_letter(j)].width = w
PAIRS_SHEET = "'Action-Reaction Pairs'"

# --- Sheet: Factor Analysis -------------------------------------------
# Breaks response speed/reliability down by what kind of cost the trigger
# imposed - this is what answers "which factor does the country weigh most."
# Every number here is a live formula against Action-Reaction Pairs, so it
# updates automatically as more pairs get added.
ws4 = wb.create_sheet("Factor Analysis")
ws4.sheet_view.showGridLines = False

intro = [
    ("Which factor drives a fast, reliable response?", BOLD, 13),
    ("Each action-reaction pair is tagged by what kind of cost the trigger imposed on the side that responded. Grouping by that tag shows which kind of cost provokes the fastest, most reliable comeback - this is the closest thing this dataset has to 'which factor the country weighs most.'", BASE_FONT, 10),
    ("", BASE_FONT, 10),
]
for i, (text, font, size) in enumerate(intro, start=1):
    c = ws4.cell(row=i, column=1, value=text)
    c.font = Font(name=FONT_NAME, bold=font.bold, size=size)
    c.alignment = Alignment(wrap_text=True, vertical="top")

table_start = len(intro) + 2
headers4 = ["Trigger Category", "n (pairs)", "Mean response time (days)",
            "Share responded within 1 day", "95% CI low", "95% CI high",
            "Share responded within 2 days",
            "Share of responses that cause casualties"]
for j, h in enumerate(headers4, start=1):
    c = ws4.cell(row=table_start, column=j, value=h)
    c.font = HEADER_FONT
    c.fill = HEADER_FILL
    c.border = BORDER
    c.alignment = Alignment(wrap_text=True, vertical="center")

categories = ["Personnel/Casualty", "Military/Property", "Economic/Blockade", "Political/Diplomatic"]
PR = f"{PAIRS_SHEET}!$K$2:$K${last_pair_row}"   # Trigger Category column (K)
TR = f"{PAIRS_SHEET}!$J$2:$J${last_pair_row}"   # Response Time column (J)
CR = f"{PAIRS_SHEET}!$L$2:$L${last_pair_row}"   # Response Caused Casualties column (L)
Z = "1.96"  # 95% confidence z-score

for i, cat in enumerate(categories, start=table_start + 1):
    ws4.cell(row=i, column=1, value=cat)
    ws4.cell(row=i, column=2, value=f'=COUNTIF({PR},A{i})')
    ws4.cell(row=i, column=3, value=f'=AVERAGEIF({PR},A{i},{TR})')
    ws4.cell(row=i, column=3).number_format = "0.00"
    ws4.cell(row=i, column=4, value=f'=SUMPRODUCT(({PR}=A{i})*({TR}<=1))/COUNTIF({PR},A{i})')
    ws4.cell(row=i, column=4).number_format = "0%"
    # Wilson score interval on the "within 1 day" share, using n and phat from D and B
    n_ref = f"B{i}"
    p_ref = f"D{i}"
    wilson_center = f"(({p_ref}+({Z}^2)/(2*{n_ref})))/(1+({Z}^2)/{n_ref})"
    wilson_half = f"({Z}*SQRT(({p_ref}*(1-{p_ref})/{n_ref})+(({Z}^2)/(4*{n_ref}^2))))/(1+({Z}^2)/{n_ref})"
    ws4.cell(row=i, column=5, value=f'=MAX(0,{wilson_center}-{wilson_half})')
    ws4.cell(row=i, column=5).number_format = "0%"
    ws4.cell(row=i, column=6, value=f'=MIN(1,{wilson_center}+{wilson_half})')
    ws4.cell(row=i, column=6).number_format = "0%"
    ws4.cell(row=i, column=7, value=f'=SUMPRODUCT(({PR}=A{i})*({TR}<=2))/COUNTIF({PR},A{i})')
    ws4.cell(row=i, column=7).number_format = "0%"
    ws4.cell(row=i, column=8, value=f'=COUNTIFS({PR},A{i},{CR},"Y")/COUNTIF({PR},A{i})')
    ws4.cell(row=i, column=8).number_format = "0%"
    for j in range(1, 9):
        c = ws4.cell(row=i, column=j)
        c.font = BASE_FONT
        c.border = BORDER

last_cat_row = table_start + len(categories)
notes_row = last_cat_row + 2
notes4 = [
    "Reading this table: 'Personnel/Casualty' pairs are triggers that killed or injured someone (an assassination, a strike that hit a school or a wedding, an attack on air-defense crews). 'Economic/Blockade' pairs are triggers about ships, seizures, sanctions, or oil - no one was hurt.",
    "",
    "What it shows, two ways: (1) SPEED/RELIABILITY - triggers that cost human lives get answered faster and more reliably than triggers that only cost money or equipment; economic/blockade moves are the slowest and least certain. (2) COST OF THE COMEBACK - the last column shows how often the response itself produces real casualties, not just a symbolic hit. Personnel/Casualty triggers are answered both fastest AND with the highest chance of a genuinely costly response. Economic/Blockade and Political/Diplomatic triggers have never (in this dataset) drawn a response that killed or injured anyone - the retaliation happens, but it stays contained to property and equipment.",
    "",
    "The 95% CI columns are Wilson score intervals on the 'within 1 day' share - the honest range given how few examples each category has. Notice how wide these are (often 30-40 points wide) for the n=4-5 categories - that's the real uncertainty, not a flaw in the formula. Treat the RANKING across categories as solid; treat any single percentage as a rough midpoint of a wide range.",
    "",
    "Sample-size warning: each group has 4-10 pairs. This is a real, directionally consistent pattern, not a precise coefficient.",
    "",
    "Important limit: every share on this sheet is measured only among pairs where a reply happened. It says how fast and how costly replies are, not whether one comes. For the chance a reply happens at all, see the Trigger Census sheet.",
]
for i, text in enumerate(notes4, start=notes_row):
    c = ws4.cell(row=i, column=1, value=text)
    c.font = BASE_FONT
    c.alignment = Alignment(wrap_text=True, vertical="top")

ws4.merge_cells(start_row=1, start_column=1, end_row=1, end_column=8)
ws4.merge_cells(start_row=2, start_column=1, end_row=2, end_column=8)
for i in range(notes_row, notes_row + len(notes4)):
    ws4.merge_cells(start_row=i, start_column=1, end_row=i, end_column=8)

widths4 = [24, 10, 16, 16, 12, 12, 16, 22]
for j, w in enumerate(widths4, start=1):
    ws4.column_dimensions[get_column_letter(j)].width = w
FACTOR_SHEET = "'Factor Analysis'"
FACTOR_TABLE_START = table_start  # header row of the category table

# --- Sheet: Trigger Census ----------------------------------------------
# Fixes the selection-bias problem in Factor Analysis: that sheet only looks at
# pairs where a reply DID happen. This sheet lists every countable hostile act
# and records whether a reply followed, including the ones where none did.
ws6 = wb.create_sheet("Trigger Census")
ws6.sheet_view.showGridLines = False
GREY_FILL = PatternFill("solid", fgColor="EDEDED")
STATUS_FILL = {"R-strong": HIGH_FILL, "R-weak": MED_FILL, "R-proxy": MED_FILL, "N": LOW_FILL, "Unclear": MED_FILL, "Unverified": GREY_FILL}

census_sorted = sorted(census, key=lambda r: r[0])
n_census = len(census_sorted)
cats3 = ["Personnel/Casualty", "Military/Property", "Economic/Blockade"]

intro6 = [
    ("How often does a hostile act actually get a reply?", BOLD, 13),
    ("Factor Analysis only sees pairs where a reply happened, so it overstates how reliable replies are. This sheet lists every countable hostile act (strikes, seizures, blockade moves, sanctions) and whether the other side hit back within about 5 days - including the ones where nothing followed. Diplomatic moves are not covered.", BASE_FONT, 10),
    ("", BASE_FONT, 10),
]
for i, (text, font, size) in enumerate(intro6, start=1):
    c = ws6.cell(row=i, column=1, value=text)
    c.font = Font(name=FONT_NAME, bold=font.bold, size=size)
    c.alignment = Alignment(wrap_text=True, vertical="top")

SUM_HDR = len(intro6) + 2
notes6 = [
    "PROVISIONAL. These statuses were first assigned from the Wikipedia-based log and a research pass that used some weak outlets. The log has since been re-sourced to credible outlets (see Event Log column K), which found real errors. Most unclear census rows have now been re-checked (see Evidence quality); a few Unverified rows are still left out of the rates. Many 'reply' calls are R-weak, meaning only timing links the reply to the act. Treat every rate on this sheet as a rough draft. Samples are tiny (about 4-12 acts per category), so the ranges matter more than the point estimates.",
    "",
    "Continuous-fighting rule: triggers dated Feb 28-Apr 7 and Jul 7-25 are excluded (except the acts that started those stretches), because while both sides strike each other daily every act is automatically 'answered'. The exclusion list at the bottom names every row moved out.",
    "",
    "Status codes: R-strong = reply is in the log with an explicit link. R-weak = a distinct hostile act followed within 5 days but only timing links it. N = checked against outside sources, no reply found (a pause, talks, or rhetoric only). Unclear = sources conflict or are too thin. Unverified = not checked yet, so left out of every rate below.",
    "",
    "Three estimates because the coding involves judgment. LOW counts only R-strong as replies and treats R-weak, N and Unclear all as no reply. BEST counts R-strong and R-weak as replies and ignores Unclear. HIGH also counts every Unclear as a reply. If a conclusion only holds under one of the three, it is not solid.",
    "",
    "The 95% CI is a Wilson interval around the BEST estimate and shows the sampling uncertainty on top of that judgment range. Samples are small (10-13 acts per category), so treat these as ranges, not points.",
    "",
    "Preliminary: the rows marked Unverified (see the Unverified column) have not been checked against outside sources. They are left out of the rates, not assumed to be replies or non-replies.",
]
notes_start = SUM_HDR + len(cats3) + 2
DET_HDR = notes_start + len(notes6) + 2
det_first = DET_HDR + 1
det_last = DET_HDR + n_census
C_CAT = f"$F${det_first}:$F${det_last}"
C_STAT = f"$G${det_first}:$G${det_last}"

headers6s = ["Trigger Category", "Acts counted", "Got a reply", "No reply found", "Unclear",
             "Unverified (not counted)", "P(any reply) LOW", "P(any reply) BEST", "P(any reply) HIGH",
             "95% CI low (BEST)", "95% CI high (BEST)"]
for j, h in enumerate(headers6s, start=1):
    c = ws6.cell(row=SUM_HDR, column=j, value=h)
    c.font = HEADER_FONT
    c.fill = HEADER_FILL
    c.border = BORDER
    c.alignment = Alignment(wrap_text=True, vertical="center")

for i, cat in enumerate(cats3, start=SUM_HDR + 1):
    ws6.cell(row=i, column=1, value=cat)
    ws6.cell(row=i, column=2, value=f"=C{i}+D{i}")
    ws6.cell(row=i, column=3, value=f'=COUNTIFS({C_CAT},A{i},{C_STAT},"R-strong")+COUNTIFS({C_CAT},A{i},{C_STAT},"R-weak")+COUNTIFS({C_CAT},A{i},{C_STAT},"R-proxy")')
    ws6.cell(row=i, column=4, value=f'=COUNTIFS({C_CAT},A{i},{C_STAT},"N")')
    ws6.cell(row=i, column=5, value=f'=COUNTIFS({C_CAT},A{i},{C_STAT},"Unclear")')
    ws6.cell(row=i, column=6, value=f'=COUNTIFS({C_CAT},A{i},{C_STAT},"Unverified")')
    ws6.cell(row=i, column=7, value=f'=COUNTIFS({C_CAT},A{i},{C_STAT},"R-strong")/(B{i}+E{i})')
    ws6.cell(row=i, column=8, value=f'=C{i}/B{i}')
    ws6.cell(row=i, column=9, value=f'=(C{i}+E{i})/(B{i}+E{i})')
    n_ref, p_ref = f"B{i}", f"H{i}"
    w_center = f"(({p_ref}+({Z}^2)/(2*{n_ref})))/(1+({Z}^2)/{n_ref})"
    w_half = f"({Z}*SQRT(({p_ref}*(1-{p_ref})/{n_ref})+(({Z}^2)/(4*{n_ref}^2))))/(1+({Z}^2)/{n_ref})"
    ws6.cell(row=i, column=10, value=f'=MAX(0,{w_center}-{w_half})')
    ws6.cell(row=i, column=11, value=f'=MIN(1,{w_center}+{w_half})')
    for j in (7, 8, 9, 10, 11):
        ws6.cell(row=i, column=j).number_format = "0%"
    for j in range(1, 12):
        c = ws6.cell(row=i, column=j)
        c.font = BASE_FONT
        c.border = BORDER

for i, text in enumerate(notes6, start=notes_start):
    c = ws6.cell(row=i, column=1, value=text)
    c.font = BASE_FONT
    c.alignment = Alignment(wrap_text=True, vertical="top")
    ws6.merge_cells(start_row=i, start_column=1, end_row=i, end_column=11)
ws6.merge_cells(start_row=1, start_column=1, end_row=1, end_column=11)
ws6.merge_cells(start_row=2, start_column=1, end_row=2, end_column=11)

headers6d = ["Trigger ID", "Date", "Actor", "Action Type", "What happened", "Trigger Category", "Status", "Evidence / note", "Evidence quality"]
for j, h in enumerate(headers6d, start=1):
    c = ws6.cell(row=DET_HDR, column=j, value=h)
    c.font = HEADER_FONT
    c.fill = HEADER_FILL
    c.border = BORDER
ws6.freeze_panes = None

for i, (tid, cat, status, note) in enumerate(census_sorted, start=det_first):
    ws6.cell(row=i, column=1, value=tid)
    ws6.cell(row=i, column=2, value=f"=INDEX({EL}!$B$2:$B${last_event_row},MATCH(A{i},{EL}!$A$2:$A${last_event_row},0))")
    ws6.cell(row=i, column=2).number_format = "yyyy-mm-dd"
    ws6.cell(row=i, column=3, value=f"=INDEX({EL}!$C$2:$C${last_event_row},MATCH(A{i},{EL}!$A$2:$A${last_event_row},0))")
    ws6.cell(row=i, column=4, value=f"=INDEX({EL}!$D$2:$D${last_event_row},MATCH(A{i},{EL}!$A$2:$A${last_event_row},0))")
    ws6.cell(row=i, column=5, value=f"=INDEX({EL}!$F$2:$F${last_event_row},MATCH(A{i},{EL}!$A$2:$A${last_event_row},0))")
    ws6.cell(row=i, column=6, value=cat)
    ws6.cell(row=i, column=7, value=status)
    ws6.cell(row=i, column=8, value=note)
    _ev = census_evidence.get(tid)
    if _ev is None:
        if event_audit[tid]["check"] in ("Pending", "Not supported"):
            _ev = "Trigger event itself is Pending credible sourcing"
        elif status in ("R-strong", "R-proxy"):
            _rids = [p[2] for p in pairs if p[1] == tid] or ([73] if tid == 71 else [])
            _ev = f"Trigger: {event_audit[tid]['check']}. Reply " + ", ".join(f"#{r}: {event_audit[r]['check']}" for r in _rids)
        else:
            _ev = f"Trigger: {event_audit[tid]['check']}. Status itself pending credible re-verification"
    ws6.cell(row=i, column=9, value=_ev)
    for j in range(1, 10):
        c = ws6.cell(row=i, column=j)
        c.font = BASE_FONT
        c.border = BORDER
        c.alignment = WRAP
    ws6.cell(row=i, column=7).fill = STATUS_FILL[status]

ex_row = det_last + 2
ws6.cell(row=ex_row, column=1, value="Not counted, and why").font = BOLD
for k, text in enumerate(census_exclusions, start=ex_row + 1):
    c = ws6.cell(row=k, column=1, value=text)
    c.font = BASE_FONT
    c.alignment = Alignment(wrap_text=True, vertical="top")
    ws6.merge_cells(start_row=k, start_column=1, end_row=k, end_column=11)

for j, w in enumerate([20, 13, 16, 22, 50, 20, 12, 70, 40, 12, 12], start=1):
    ws6.column_dimensions[get_column_letter(j)].width = w

# --- Sheet: Options (NAPOR step 3) --------------------------------------
import napor_options as OPT
ws5 = wb.create_sheet("Options")
ws5.sheet_view.showGridLines = False
_intro = [
    ("Options and their risks - NAPOR does not rank or pick an option", Font(name="Arial", bold=True, size=13)),
    (f"Situation as of {max(e[1] for e in events).isoformat()}: war phase = {OPT.CURRENT_PHASE}. No direct US-Iran strikes since Sep 9; attacks on shipping continue; Trump says no US strikes before the Nov 3 midterms; Iran is expected to answer the US counter-offer.", BASE_FONT),
    ("How to read it: each risk is 'x of n' past cases, so you can see how much evidence is behind it. The range is a 95% Wilson interval: with this few cases, the true chance could be anywhere in it. 'Very thin' means 1-3 past cases.", BASE_FONT),
    ("Important: almost all past cases come from the fragile ceasefire and low-intensity phases, when nearly every hostile act drew a reply. The current quiet phase has only been tested by sanctions (0 of 2 drew a reply). Whether a US strike now would be answered the same way is unknown.", BOLD),
]
for k, (t, f) in enumerate(_intro, start=1):
    c = ws5.cell(row=k, column=1, value=t)
    c.font = f
_ph = 6
ws5.cell(row=_ph - 1, column=1, value="Risk profile: every option on the same five risks, plus pros. Each cell says what was measured (x of n past cases) or 'not measured'.").font = BOLD
_pcols = ["Option", "What it means"] + OPT.RISK_CATEGORIES + ["Pros (analyst notes)", "Other notes on harms (analyst notes)", "Evidence strength"]
for j, h in enumerate(_pcols, start=1):
    c = ws5.cell(row=_ph, column=j, value=h)
    c.font = HEADER_FONT
    c.fill = HEADER_FILL
    c.border = BORDER
    c.alignment = WRAP
_r = _ph + 1
_STRF = {"OK": HIGH_FILL, "Thin": MED_FILL, "Very thin": LOW_FILL, "No data": PatternFill("solid", fgColor="EDEDED")}
for _o in OPT.OPTIONS:
    _p = OPT.risk_profile(_o["key"])
    vals = [f"{_o['key']}. {_o['name']}", _o["what"]] + [_p[k] for k in OPT.RISK_CATEGORIES] + [_p["Pros (analyst notes)"], _p["Other notes on harms (analyst notes)"], _p["Evidence strength"]]
    for j, v in enumerate(vals, start=1):
        c = ws5.cell(row=_r, column=j, value=v)
        c.font = BASE_FONT
        c.border = BORDER
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for j in (8, 9):
        ws5.cell(row=_r, column=j).fill = PatternFill("solid", fgColor="F2F2F2")
    ws5.cell(row=_r, column=10).fill = _STRF.get(_p["Evidence strength"], PatternFill("solid", fgColor="FFF2CC"))
    ws5.row_dimensions[_r].height = 150
    _r += 1
for j, w in enumerate([24, 28, 40, 40, 34, 28, 30, 40, 40, 14, 11, 22, 50], start=1):
    ws5.column_dimensions[get_column_letter(j)].width = w
ws5.freeze_panes = ws5.cell(row=_ph + 1, column=2)
_hdr = ["Option", "What it means", "Chance of an Iranian hostile reply within ~5 days (past cases)", "Plausible range (95%)",
        "In the current phase", "Reply within 2 days (of replies)", "Reply caused casualties (of replies)",
        "Chance a back-and-forth goes past one reply", "Patriot interceptors likely used", "Evidence strength",
        "Avg credibility of cases", "Past cases used", "What we don't know"]
_h = ws5.max_row + 4
ws5.cell(row=_h - 2, column=1, value="Details behind the numbers").font = Font(name="Arial", bold=True, size=12)
for j, h in enumerate(_hdr, start=1):
    c = ws5.cell(row=_h, column=j, value=h)
    c.font = HEADER_FONT
    c.fill = HEADER_FILL
    c.border = BORDER
    c.alignment = WRAP
ws5.row_dimensions[_h].height = 60
_STR_FILL = {"OK": HIGH_FILL, "Thin": MED_FILL, "Very thin": LOW_FILL, "No data": PatternFill("solid", fgColor="EDEDED")}
_r = _h + 1
for row in OPT.option_rows():
    _s = OPT.strength(row["n"])
    vals = [f"{row['key']}. {row['name']}", row["what"], row["reply"], row["reply_range"], row["phase_note"], row["fast"],
            row["casualties"], row["longer"], row["patriots"], _s, row["credibility"], row["cases"], OPT.UNKNOWNS[row["key"]]]
    for j, v in enumerate(vals, start=1):
        c = ws5.cell(row=_r, column=j, value=v)
        c.font = BASE_FONT
        c.border = BORDER
        c.alignment = WRAP
    ws5.cell(row=_r, column=10).fill = _STR_FILL[_s]
    _r += 1
_r += 1
_bl = OPT.baseline_hold()
ws5.cell(row=_r, column=1, value=(f"Baseline (what happens with no new US move): in the current phase, {_bl['n']} hostile acts by Iran or unknown attackers were logged over {_bl['weeks']} weeks "
                                   f"(about {_bl['per_week']} per week), almost all attacks on shipping: " + ", ".join(f"#{i}" for i in _bl["ids"]) +
                                   ". Houthi strikes on Saudi Arabia are a separate front and not counted.")).font = BASE_FONT
_r += 1
ws5.cell(row=_r, column=1, value=(f"Back-and-forth column: across all {OPT.T.chain_stats()['chains']} logged chains with a hostile act, about a third went past one reply (longest: 3 rounds). "
                                   "It is not broken down by option because each option has too few chains.")).font = BASE_FONT
_r += 1
ws5.cell(row=_r, column=1, value=(f"Interceptors: one measured salvo (Sep 8-9, Jordan) used about {OPT.PATRIOTS_PER_SALVO} Patriots ('roughly 30' per a US official; 'more than 30' per CBS). "
                                   "The column multiplies that by the reply chance. CSIS estimated fewer than 850 Patriots left theater-wide (Sep). Not independently re-checked.")).font = BASE_FONT
_r += 1
ws5.cell(row=_r, column=1, value="Only events with credibility 0.50+ are used. Every number here is recomputed from the Event Log by napor_options.py when the workbook is rebuilt.").font = BASE_FONT


# --- Sheet: Monthly Summary -------------------------------------------
ws3 = wb.create_sheet("Monthly Summary")
headers3 = ["Month", "US/Israel strikes (on territory/forces)", "Iran strikes (on territory/forces)",
            "Shipping/blockade incidents (any side)", "Diplomatic events (talks, proposals, ceasefires)", "Ceasefire status", "Notes"]
for j, h in enumerate(headers3, start=1):
    c = ws3.cell(row=1, column=j, value=h)
    c.font = HEADER_FONT
    c.fill = HEADER_FILL
    c.border = BORDER
ws3.freeze_panes = "A2"

ceasefire_status = {
    "Feb 2026": "No ceasefire - war start",
    "Mar 2026": "No ceasefire",
    "Apr 2026": "Two-week ceasefire announced Apr 7-8 (no signed text found), violated same day, collapsing through month",
    "May 2026": "Nominal ceasefire, blockade/counter-blockade ongoing",
    "Jun 2026": "New ceasefire Jun 8, MOU signed Jun 17",
    "Jul 2026": "MOU collapses Jul 7-8; heaviest fighting month",
    "Aug 2026": "No ceasefire, lower-intensity than July",
    "Sep 2026": "No ceasefire; new Iranian proposal Sep 23, rejected Sep 26",
    "Oct 2026 (to Oct 26)": "No ceasefire; Trump says no US strikes on Iran before the Nov 3 midterms (Oct 8); strike plans reported (Oct 16); Trump weighs 'a deal' or renewed strikes (Oct 23-25)",
}
notes_map = {
    "Feb 2026": "War start (Feb 28)",
    "Mar 2026": "Highest-intensity month of the initial campaign",
    "Apr 2026": "Ceasefire signed and broken within hours",
    "May 2026": "Blockade/counter-blockade tit-for-tat, lower kinetic tempo",
    "Jun 2026": "Two ceasefires reached; MOU by month end",
    "Jul 2026": "MOU collapse; deadliest month for US troops",
    "Aug 2026": "Relative lull; Larak Island strike late month",
    "Sep 2026": "Partial month - renewed escalation, then a new peace proposal",
    "Oct 2026 (to Oct 26)": "Partial month. Record attacks on shipping (GFS Pride sunk Oct 13); US bombers leave RAF Fairford; more US sanctions; US staff drawdown from Gulf posts (Oct 21-23); no US-Iran strikes",
}

for i, (label, start, end) in enumerate(MONTHS, start=2):
    ws3.cell(row=i, column=1, value=label)
    start_s = start.isoformat()
    end_s = end.isoformat()
    _rng = (f'{EL}!$B$2:$B${last_event_row},">="&DATE({start.year},{start.month},{start.day}),'
            f'{EL}!$B$2:$B${last_event_row},"<="&DATE({end.year},{end.month},{end.day})')
    _C = f"{EL}!$C$2:$C${last_event_row}"; _M = f"{EL}!$M$2:$M${last_event_row}"
    us_formula = (f'=COUNTIFS({_C},"US*",{_M},"Kinetic",{_rng})+COUNTIFS({_C},"Israel*",{_M},"Kinetic",{_rng})')
    iran_formula = f'=COUNTIFS({_C},"Iran*",{_M},"Kinetic",{_rng})'
    ship_formula = f'=COUNTIFS({_M},"Maritime",{_rng})'
    dip_formula = f'=COUNTIFS({_M},"Diplomatic",{_rng})'
    ws3.cell(row=i, column=2, value=us_formula)
    ws3.cell(row=i, column=3, value=iran_formula)
    ws3.cell(row=i, column=4, value=ship_formula)
    ws3.cell(row=i, column=5, value=dip_formula)
    ws3.cell(row=i, column=6, value=ceasefire_status[label])
    ws3.cell(row=i, column=7, value=notes_map[label])
    for j in range(1, 8):
        c = ws3.cell(row=i, column=j)
        c.font = BASE_FONT
        c.border = BORDER
        c.alignment = WRAP

widths3 = [14, 20, 20, 20, 22, 45, 40]
for j, w in enumerate(widths3, start=1):
    ws3.column_dimensions[get_column_letter(j)].width = w

# --- Sheet: Reports (NAPOR ID system) -------------------------------------
ws7 = wb.create_sheet("Reports")
_hdr = ["Report ID", "Event ID", "Outlet", "Kind of source", "Headline", "Published", "URL", "Read as", "Logged under", "Source score", "Fit score", "Weight (counts if 0.30+)"]
for j, h in enumerate(_hdr, start=1):
    c = ws7.cell(row=1, column=j, value=h)
    c.font = HEADER_FONT
    c.fill = HEADER_FILL
    c.border = BORDER
ws7.freeze_panes = "A2"
_r = 2
for rp in NAPOR.REPORTS:
    vals = [rp["report_id"], rp["event_id"], rp["outlet_raw"], rp["kind"], rp["headline"], rp["published"], rp["url"], rp["seen"],
            rp["logged_under"] if rp["logged_under"] != rp["event_id"] else "",
            NAPOR.source_score(rp), NAPOR.fit_score(rp), NAPOR.report_weight(rp)]
    for j, v in enumerate(vals, start=1):
        c = ws7.cell(row=_r, column=j, value=v)
        c.font = BASE_FONT
        c.alignment = WRAP
        c.border = BORDER
    if rp["kind"].startswith("Iranian state media"):
        ws7.cell(row=_r, column=4).fill = LOW_FILL
    elif rp["seen"].startswith("name only"):
        ws7.cell(row=_r, column=8).fill = PatternFill("solid", fgColor="EDEDED")
    _r += 1
_rep_last = _r - 1
_r += 1
ws7.cell(row=_r, column=1, value="Evidence behind Trigger Census re-checks (not event reports)").font = BOLD
_r += 1
for _tid in sorted(CENSUS_SOURCES):
    for sc in CENSUS_SOURCES[_tid]:
        for j, v in enumerate(["", f"Census #{_tid}", sc["outlet"], NAPOR.source_kind(sc["outlet"]), sc["headline"], sc["published"], sc["url"], sc["seen"], ""], start=1):
            c = ws7.cell(row=_r, column=j, value=v)
            c.font = BASE_FONT
            c.alignment = WRAP
            c.border = BORDER
        _r += 1
for j, w in enumerate([10, 9, 34, 22, 60, 11, 60, 16, 10, 10, 9, 12], start=1):
    ws7.column_dimensions[get_column_letter(j)].width = w
ws7.auto_filter.ref = f"A1:L{_rep_last}"

# --- Sheet: Chains & Phases ---------------------------------------------
ws9 = wb.create_sheet("Chains & Phases")
ws9.cell(row=1, column=1, value="War phases").font = Font(name="Arial", bold=True, size=12)
ws9.cell(row=2, column=1, value="People act differently in open war than in a ceasefire or a quiet spell, so NAPOR counts risk numbers within the right phase. Boundaries are judgement calls; each names the event that marks it.").font = BASE_FONT
for j, h in enumerate(["Phase", "From", "To", "What marks it", "Events in log"], start=1):
    c = ws9.cell(row=4, column=j, value=h); c.font = HEADER_FONT; c.fill = HEADER_FILL; c.border = BORDER
_r = 5
from collections import Counter as _C
_cen_ph = {}
for _tid, _cat, _st, _nt in census:
    if _st in ("R-strong", "R-weak", "R-proxy", "N"):
        _p = THREADS.event_phase[_tid]; a, n = _cen_ph.get(_p, (0, 0))
        _cen_ph[_p] = (a + (_st != "N"), n + 1)
for name, a, bnd, why in THREADS.PHASES:
    n_ev = sum(1 for e in events if a <= e[1] <= bnd and e[0] not in NAPOR.MERGED)
    for j, v in enumerate([name, a, min(bnd, max(e[1] for e in events)), why, n_ev], start=1):
        c = ws9.cell(row=_r, column=j, value=v); c.font = BASE_FONT; c.border = BORDER; c.alignment = WRAP
        if isinstance(v, dt.date): c.number_format = "yyyy-mm-dd"
    _r += 1
_r += 1
ws9.cell(row=_r, column=1, value="Chance of any reply within ~5 days, by phase (census, best estimate; Open war rows are mostly excluded by the continuous-fighting rule)").font = BOLD
_r += 1
for j, h in enumerate(["Phase", "Got a reply", "Counted", "Share"], start=1):
    c = ws9.cell(row=_r, column=j, value=h); c.font = HEADER_FONT; c.fill = HEADER_FILL; c.border = BORDER
_r += 1
for _p in ["Open war", "Fragile ceasefire", "Low-intensity war", "Holding pattern"]:
    a, n = _cen_ph.get(_p, (0, 0))
    for j, v in enumerate([_p, a, n, f"=IF(C{_r}>0,B{_r}/C{_r},\"-\")"], start=1):
        c = ws9.cell(row=_r, column=j, value=v); c.font = BASE_FONT; c.border = BORDER
    ws9.cell(row=_r, column=4).number_format = "0%"
    _r += 1
ws9.cell(row=_r, column=1, value="Backtest (backtest.py): predicting with the reply rate in the same phase scored a Brier score of 0.159, better than the overall rate (0.170) and the rate by type of act (0.183); on the last 6 cases 0.20 vs 0.38. Caveat: the phase boundaries were drawn with hindsight, and in real time you only know a quiet spell has started after some days.").font = BASE_FONT
_r += 3
ws9.cell(row=_r, column=1, value="Chains (back-and-forths)").font = Font(name="Arial", bold=True, size=12)
_r += 1
_cs = THREADS.chain_stats()
ws9.cell(row=_r, column=1, value=(f"Each chain links events where one is a reply to another. Across {_cs['chains']} chains with a hostile act: on average {_cs['avg_rounds']} side-switches, "
                                   f"longest {_cs['max_rounds']}; {_cs['share_stopped_after_one_reply']:.0%} stopped after one reply; average length {_cs['avg_days']} days. "
                                   "Caveat: July's nightly US strikes are under-logged, so chain T13 looks shorter than it was.")).font = BASE_FONT
_r += 2
for j, h in enumerate(["Thread ID", "Chain", "Start", "End", "Days", "Events", "Side-switches", "Hostile acts", "Phase", "Event IDs"], start=1):
    c = ws9.cell(row=_r, column=j, value=h); c.font = HEADER_FONT; c.fill = HEADER_FILL; c.border = BORDER
_r += 1
for t in THREADS.THREADS:
    for j, v in enumerate([t["thread_id"], t["name"], t["start"], t["end"], t["days"], t["n"], t["rounds"], t["hostile_acts"], t["phase"], ", ".join(f"#{i}" for i in t["events"])], start=1):
        c = ws9.cell(row=_r, column=j, value=v); c.font = BASE_FONT; c.border = BORDER; c.alignment = WRAP
        if isinstance(v, dt.date): c.number_format = "yyyy-mm-dd"
    _r += 1
for j, w in enumerate([18, 44, 12, 12, 7, 8, 12, 11, 17, 30], start=1):
    ws9.column_dimensions[get_column_letter(j)].width = w

# --- Sheet: Forecast Log (report card) -----------------------------------
import napor_forecasts as FC
wsF = wb.create_sheet("Forecast Log")
wsF.cell(row=1, column=1, value="Forecast Log - the report card").font = Font(name="Arial", bold=True, size=13)
wsF.cell(row=2, column=1, value=("Each forecast is written down BEFORE the outcome is known and never edited afterwards. After the deadline it is resolved YES/NO from credible sources "
                                 "and scored with the Brier score: (probability - outcome)^2, 0 = perfect, 0.25 = coin flip. Over time this shows whether NAPOR's risk numbers can be trusted.")).font = BASE_FONT
_sc = FC.scorecard()
wsF.cell(row=3, column=1, value=f"Made: {_sc['made']}   Resolved: {_sc['resolved']}   Open: {_sc['open']}   Average Brier score so far: {_sc['avg_brier'] if _sc['avg_brier'] is not None else '-'}").font = BOLD
_fh = ["ID", "Made on", "News known up to", "Question", "Counts as YES if", "Deadline", "Probability", "Where the number came from", "Option", "Outcome", "Resolved on", "Brier score", "Resolution note"]
for j, h in enumerate(_fh, start=1):
    c = wsF.cell(row=5, column=j, value=h)
    c.font = HEADER_FONT
    c.fill = HEADER_FILL
    c.border = BORDER
    c.alignment = WRAP
_r = 6
for it in FC.load():
    vals = [it["id"], it["made_on"], it.get("news_through") or "", it["question"], it["resolves_yes_if"], it["deadline"], it["probability"], it["basis"],
            it.get("option") or "", it["outcome"] or "OPEN", it["resolved_on"] or "", it["brier"] if it["brier"] is not None else "", it["resolution_note"] or ""]
    for j, v in enumerate(vals, start=1):
        c = wsF.cell(row=_r, column=j, value=v)
        c.font = BASE_FONT
        c.border = BORDER
        c.alignment = WRAP
    wsF.cell(row=_r, column=7).number_format = "0%"
    wsF.cell(row=_r, column=10).fill = MED_FILL if (it["outcome"] is None) else HIGH_FILL
    _r += 1
for j, w in enumerate([6, 11, 12, 40, 50, 11, 11, 50, 7, 9, 11, 9, 40], start=1):
    wsF.column_dimensions[get_column_letter(j)].width = w
wsF.freeze_panes = "B6"

# --- Intensity section on the Chains & Phases sheet ------------------------
import napor_intensity as INT
_r = ws9.max_row + 3
ws9.cell(row=_r, column=1, value="War intensity, week by week").font = Font(name="Arial", bold=True, size=12)
_r += 1
ws9.cell(row=_r, column=1, value=("Points per week: 2 for each direct strike between the US/Israel and Iran, 1 for each attack on shipping / seizure / blockade move, +2 if it killed someone. "
                                  "The 14-day band (Quiet 0, Low 1-5, Medium 6-11, High 12+) uses only earlier events, so it works in real time. "
                                  "Backtest: using this band to predict replies did NOT help (Brier 0.197 vs 0.170 for the plain overall rate): replies came even after quiet weeks, as on Jun 9. "
                                  "So it is shown as a gauge, not used in the numbers. Caveat: it counts logged rows, so big campaigns logged as one row look smaller than they were.")).font = BASE_FONT
_r += 2
for j, h in enumerate(["Week starting", "Week ending", "Direct strikes", "Shipping/blockade acts", "Deadly events", "Points this week", "14-day band at week end"], start=1):
    c = ws9.cell(row=_r, column=j, value=h)
    c.font = HEADER_FONT
    c.fill = HEADER_FILL
    c.border = BORDER
_r += 1
_BAND_FILL = {"Quiet": PatternFill("solid", fgColor="EDEDED"), "Low": HIGH_FILL, "Medium": MED_FILL, "High": LOW_FILL}
for w in INT.weekly_table():
    for j, v in enumerate([w["week_start"], w["week_end"], w["kinetic"], w["shipping"], w["deadly"], w["points"], w["band_14d"]], start=1):
        c = ws9.cell(row=_r, column=j, value=v)
        c.font = BASE_FONT
        c.border = BORDER
        if isinstance(v, dt.date):
            c.number_format = "yyyy-mm-dd"
    ws9.cell(row=_r, column=7).fill = _BAND_FILL[w["band_14d"]]
    _r += 1

# --- Sheet: Review Queue --------------------------------------------------
ws8 = wb.create_sheet("Review Queue")
ws8.cell(row=1, column=1, value="Review Queue - a person decides these").font = Font(name="Arial", bold=True, size=12)
ws8.cell(row=2, column=1, value="Part 1: event pairs that look alike (same few days, same place, same side). Many are two parts of one attack wave, or a claim and the real event, rather than true duplicates. Check each and either merge it or mark it 'different events'.").font = BASE_FONT
_h = ["Similarity (0-1)", "Event A", "Date A", "Event A detail", "Event B", "Date B", "Event B detail", "Decision"]
for j, h in enumerate(_h, start=1):
    c = ws8.cell(row=4, column=j, value=h)
    c.font = HEADER_FONT
    c.fill = HEADER_FILL
    c.border = BORDER
_r = 5
for dw in NAPOR.duplicate_watch():
    for j, v in enumerate([dw["score"], dw["event_a"], dw["date_a"], dw["detail_a"], dw["event_b"], dw["date_b"], dw["detail_b"], NAPOR.SUGGEST.get((dw["event_a"], dw["event_b"]), "to check")], start=1):
        c = ws8.cell(row=_r, column=j, value=v)
        c.font = BASE_FONT
        c.alignment = WRAP
        c.border = BORDER
    _r += 1
ws8.cell(row=_r, column=1, value="Already resolved: #76 merged into #75 (one attack reported over two days); #49 merged into #50 (same Jun 17 deal signing); #29 merged into #28 (same Apr 7-8 ceasefire).").font = BASE_FONT
_r += 2
ws8.cell(row=_r, column=1, value="Part 2: new stories waiting to be filed (from napor_ids.intake). Empty means nothing is waiting.").font = BOLD
_r += 1
_h2 = ["Report ID", "Published", "Outlet", "Headline", "Matcher's call", "Best match (event)", "Status"]
for j, h in enumerate(_h2, start=1):
    c = ws8.cell(row=_r, column=j, value=h)
    c.font = HEADER_FONT
    c.fill = HEADER_FILL
    c.border = BORDER
_r += 1
for q in NAPOR._load_queue():
    for j, v in enumerate([q["report_id"], q["published"], q["outlet"], q["headline"], q["decision"], q["matched_event"] or q.get("proposed_new_event_id"), q["status"]], start=1):
        c = ws8.cell(row=_r, column=j, value=v)
        c.font = BASE_FONT
        c.alignment = WRAP
        c.border = BORDER
    _r += 1
for j, w in enumerate([12, 9, 12, 50, 9, 12, 50, 40], start=1):
    ws8.column_dimensions[get_column_letter(j)].width = w

import os as _os
wb.save(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "NAPOR_iran_war.xlsx"))
print(f"Saved. {n_events} events, {len(pairs)} action-reaction pairs.")
