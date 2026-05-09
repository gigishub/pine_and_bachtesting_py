"""
Funding rate regime indicator ideas.

Tests whether the funding rate environment is bearish.
threshold=0.0    : strictly negative funding (shorts pay longs)
threshold=0.0001 : below the Bybit floor rate (neutral-to-bearish)
ma_period=1      : raw 8h rate (responsive)
ma_period=3      : 3-observation EMA (~24h smoothing, filters spikes)

Set "enabled": False to skip an idea without deleting it.
"""

_BASE = "bear_strategy.hypothesis_test_v2.regime.indicators.funding_rate"

IDEAS: list[dict] = [
    {
        "name":             "funding_bear_negative_raw",
        "enabled":          False,
        "decision":         "PENDING",
        "indicator_module": f"{_BASE}.funding_rate",
        "params":           {"threshold": 0.0, "ma_period": 1},
    },
    {
        "name":             "funding_bear_below_floor_raw",
        "enabled":          False,
        "decision":         "PENDING",
        "indicator_module": f"{_BASE}.funding_rate",
        "params":           {"threshold": 0.0001, "ma_period": 1},
    },
    {
        "name":             "funding_bear_negative_ma3",
        "enabled":          False,
        "decision":         "PENDING",
        "indicator_module": f"{_BASE}.funding_rate",
        "params":           {"threshold": 0.0, "ma_period": 3},
    },
    {
        "name":             "funding_bear_below_floor_ma3",
        "enabled":          False,
        "decision":         "PENDING",
        "indicator_module": f"{_BASE}.funding_rate",
        "params":           {"threshold": 0.0001, "ma_period": 3},
    },
    {
        "name":             "funding_bull_positive_raw",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": f"{_BASE}.funding_rate",
        "params":           {"threshold": 0.0, "ma_period": 1, "direction": "bull"},
    },
    {
        "name":             "funding_bull_above_floor_raw",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": f"{_BASE}.funding_rate",
        "params":           {"threshold": 0.0001, "ma_period": 1, "direction": "bull"},
    },
    {
        "name":             "funding_bull_positive_ma3",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": f"{_BASE}.funding_rate",
        "params":           {"threshold": 0.0, "ma_period": 3, "direction": "bull"},
    },
]
