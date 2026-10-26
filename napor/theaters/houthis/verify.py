"""Houthis: independent recount of every percentage the page shows for this tab (rules in theaters/common.py, class Recount).

It reads the research files and config.py directly and does NOT use cases.py or export.py. Writes explorer/verify-houthis.json."""
from theaters import common
from theaters.houthis import events_early as E, events_late as L, config as C

_R = common.Recount(C, [E, L])
OUT, recount, run, estimates, hold_mondays, weighting_in_force = _R.OUT, _R.recount, _R.run, _R.estimates, _R.hold_mondays, _R.weighting_in_force
