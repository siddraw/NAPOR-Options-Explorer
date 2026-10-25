"""china: independent recount of every percentage the page shows for this tab (rules in theaters/common.py, class Recount).

It reads events.py and config.py directly and does NOT use cases.py or export.py. Writes explorer/verify-china.json."""
from theaters import common
from theaters.china import events as E, config as C

_R = common.Recount(C, [E])
OUT, recount, run, estimates, hold_mondays, weighting_in_force = _R.OUT, _R.recount, _R.run, _R.estimates, _R.hold_mondays, _R.weighting_in_force
