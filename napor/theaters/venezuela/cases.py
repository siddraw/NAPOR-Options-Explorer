"""venezuela: the event table and the past cases behind every option, in the shape the page uses.

The rules live in theaters/common.py (class Theater); this file only joins the read-only event files (events_pre2019.py and events.py, joined in rules.py) with config.py.
Names are exported at module level (EV, EVENTS, CRED, census, pairs, all_cases(), option_rows(), risk_lines(), ...)."""
from theaters import common
from theaters.venezuela import rules as E        # events_pre2019.py and events.py seen through this tab's escalation rule (see rules.py)
from theaters.venezuela import config as C

_T = common.Theater(C, [E])
globals().update(_T.public())
