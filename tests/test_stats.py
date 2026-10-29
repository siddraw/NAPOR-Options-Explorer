"""The statistics: Wilson ranges, the m=2 estimate, the Brier score and the equal-weight risk index."""
import datetime as dt
import math

import pytest

import backtest_risk as BR
import export_explorer as X
import napor_options as O
from theaters import common


def reference_wilson(k, n, z=1.96):
    """Textbook Wilson score interval, written separately from the project's code."""
    p = k / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z / (1 + z * z / n) * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return max(0.0, centre - half), min(1.0, centre + half)


# (k, n, low, high): well-known 95% Wilson values, to 4 decimals
KNOWN = [
    (5, 10, 0.2366, 0.7634),
    (0, 10, 0.0000, 0.2775),
    (10, 10, 0.7225, 1.0000),
    (1, 10, 0.0179, 0.4042),
    (20, 100, 0.1334, 0.2888),
    (1, 2, 0.0945, 0.9055),
]


@pytest.mark.parametrize("fn", [common.wilson, O.wilson, X.wilson], ids=["common", "napor_options", "export_explorer"])
@pytest.mark.parametrize("k,n,low,high", KNOWN)
def test_wilson_known_values(fn, k, n, low, high):
    lo, hi = fn(k, n)
    assert lo == pytest.approx(low, abs=5e-5)
    assert hi == pytest.approx(high, abs=5e-5)


def test_wilson_empty_sample_has_no_range():
    assert common.wilson(0, 0) is None
    assert O.wilson(0, 0) is None
    assert X.wilson(0, 0) is None


def test_wilson_matches_reference_for_many_samples():
    for n in range(1, 40):
        for k in range(n + 1):
            lo, hi = common.wilson(k, n)
            rlo, rhi = reference_wilson(k, n)
            assert lo == pytest.approx(rlo, abs=1e-12) and hi == pytest.approx(rhi, abs=1e-12)
            assert -1e-12 <= lo <= k / n + 1e-12 and k / n - 1e-12 <= hi <= 1.0 + 1e-12


def test_shrunk_estimate_uses_m_equal_2():
    """NAPOR estimate = (k + 2 x pooled) / (n + 2). Check it through the backtest's own predict()."""
    assert BR.M_MAIN == 2 and common.M == 2
    day = dt.date(2025, 1, 1)
    train = [dict(date=day - dt.timedelta(days=100 + i), closes=day - dt.timedelta(days=90 + i), opt="C", cat="people", y=y, id=i)
             for i, y in enumerate([1, 0, 0, 1])]
    train += [dict(date=day - dt.timedelta(days=100 + i), closes=day - dt.timedelta(days=90 + i), opt="D", cat="people", y=y, id=10 + i)
              for i, y in enumerate([0, 0, 0, 0])]
    row = dict(date=day, closes=day + dt.timedelta(days=7), opt="C", cat="people", y=1, id=99)
    p = BR.predict(train, row)
    k, n, pool = 2, 4, 2 / 8
    assert p["raw"] == pytest.approx(k / n)
    assert p["p_pool"] == pytest.approx(pool)
    assert p["shrunk2"] == pytest.approx((k + 2 * pool) / (n + 2))
    assert p["w_none"] == pytest.approx(p["shrunk2"])


def test_brier_score():
    ps = [dict(raw=0.8, y=1), dict(raw=0.2, y=1), dict(raw=0.5, y=0)]
    assert BR.brier(ps, "raw") == pytest.approx(round((0.04 + 0.64 + 0.25) / 3, 4))
    assert BR.brier([dict(raw=0.5, y=1), dict(raw=0.5, y=0)], "raw") == 0.25      # always saying 50% scores 0.25
    assert BR.brier([], "raw") is None


def test_risk_index_is_equal_weight_average_not_slices_of_100():
    """Index = plain average of the measured category rates; the five rates need not add to 100%."""
    flags = dict(trigger=True, military="reply", is_hold=False)
    case = lambda replied, hurt, kinetic, ship_a, talks14: dict(
        date="2025-01-01", strike7=True, replied=replied, replies=[dict(hurt=hurt, kinetic=kinetic)], civ=None,
        ship_a=ship_a, ship_b=1, talks14=talks14, id=1)
    cases = [case(True, True, True, 3, False), case(False, False, False, 0, True)]
    opt = dict(flags)
    rates = {"people": 0.5, "escalation": 0.5, "military": 0.5, "economic": 0.5, "political": 0.5}
    assert X.risk_index(opt, cases) == pytest.approx(sum(rates.values()) / 5)
    # a category that cannot be measured is left out of the average, not counted as zero
    cases2 = [case(True, True, True, 3, False)]
    assert X.risk_index(opt, cases2) == 1.0
    assert sum(rates.values()) == 2.5            # the corners are separate rates, not shares of 100%
