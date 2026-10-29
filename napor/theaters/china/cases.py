"""china: the event table and the past cases behind every option, in the shape the page uses.

The rules live in theaters/common.py (class Theater); this file only joins the read-only research files (events_pre2019.py, then events.py) with config.py.
Names are exported at module level (EV, EVENTS, CRED, census, pairs, all_cases(), option_rows(), risk_lines(), ...)."""
from theaters import common
from theaters.china import events_pre2019 as E0, events as E
from theaters.china import config as C

_T = common.Theater(C, [E0, E])
globals().update(_T.public())
