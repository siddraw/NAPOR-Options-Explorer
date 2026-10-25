"""northkorea: build and write everything the page needs for this tab (rules in theaters/common.py).

Writes explorer/data/northkorea.json, explorer/data/northkorea-history.json and this theater's entry in explorer/theaters.json.
Run by export_explorer.py (python3 export_explorer.py northkorea)."""
from theaters import common
from theaters.northkorea import backtest as BT, cases as K, config as C, verify

_X = common.Export(C, K, BT)
build, write = _X.build, _X.write
DATA_FILE, HISTORY_FILE = _X.DATA_FILE, _X.HISTORY_FILE


def recount_diff(out):
    return _X.recount_diff(out, verify.recount)


def run():
    return _X.run(verify.recount)
