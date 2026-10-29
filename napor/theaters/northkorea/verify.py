"""northkorea: independent recount of every percentage the page shows for this tab (rules in theaters/common.py, class Recount).

It reads events_pre2017.py, events.py and config.py directly and does NOT use cases.py or export.py. Writes explorer/verify-northkorea.json."""
from theaters import common
from theaters.northkorea import events_pre2017 as E0, events as E, config as C

_R = common.Recount(C, [E0, E])
OUT, recount, run, estimates, hold_mondays, weighting_in_force = _R.OUT, _R.recount, _R.run, _R.estimates, _R.hold_mondays, _R.weighting_in_force
