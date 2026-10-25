"""Houthis / Red Sea: the event table and the past cases behind every option, in the shape the page uses.

The rules live in theaters/common.py (class Theater); this file only joins the read-only research files
(events_early.py, events_late.py) with config.py. Everything here is a function of those inputs, so a fix to the
research files flows through on the next run. Names are exported at module level (EV, EVENTS, CRED, census, pairs,
all_cases(), option_rows(), risk_lines(), ...) because export.py, verify.py and backtest.py read them from here.
"""
from theaters import common
from theaters.houthis import events_early as E, events_late as L
from theaters.houthis import config as C

_T = common.Theater(C, [E, L])
globals().update(_T.public())
