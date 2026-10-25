"""Houthis: build and write everything the page needs for the Houthis / Red Sea tab (rules in theaters/common.py).

Writes explorer/data/houthis.json, explorer/data/houthis-history.json and this theater's entry in explorer/theaters.json.
Run by export_explorer.py (python3 export_explorer.py houthis)."""
from theaters import common
from theaters.houthis import backtest as BT, cases as K, config as C, verify

_X = common.Export(C, K, BT)
build, write, run_checks = _X.build, _X.write, _X.run
DATA_FILE, HISTORY_FILE = _X.DATA_FILE, _X.HISTORY_FILE


def recount_diff(out):
    return _X.recount_diff(out, verify.recount)


def run():
    return _X.run(verify.recount)
