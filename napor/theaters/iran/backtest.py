"""Iran: thin entry point to the walk-forward backtest (backtest_risk.py writes napor/backtest_risk.json)."""
def run_and_report(report):
    import json, os
    import backtest_risk as BR
    cb = BR.all_cases()
    res = BR.run(cb)
    json.dump(res, open(os.path.join(BR.HERE, "backtest_risk.json"), "w"), indent=1, default=str)
    report(res, cb)
    return res
