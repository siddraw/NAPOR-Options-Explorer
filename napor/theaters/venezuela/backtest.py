"""venezuela: walk-forward backtest of the page's own numbers (rules in theaters/common.py, same method as backtest_risk.py).

Writes napor/theaters/venezuela/backtest_risk.json. verify.py and export.py read the written weighting decision from it."""
from theaters import common
from theaters.venezuela import cases as K, config as C

_B = common.Backtest(C, K)
JSON_FILE, run, run_and_report, weighting_in_force, context = _B.JSON_FILE, _B.run, _B.run_and_report, _B.weighting_in_force, _B.context
