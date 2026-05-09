"""
Combination regime indicator ideas.

Composite regime filters that combine bearish RSI regimes with bullish funding
conditions. These are managed in the new shared combinations family.
"""

_BASE = "bear_strategy.hypothesis_test_v2.regime.indicators.combinations"

IDEAS: list[dict] = [
    {
        "name":             "rsi_bear_zone_1d_and_funding_bull_positive_raw",
        "enabled":          True,
        "decision":         "REJECTED",
        "indicator_module": f"{_BASE}.rsi_bear_and_funding_bull",
        "params":           {
            "rsi_type": "zone",
            "rsi_period": 14,
            "ma_period": 9,
            "lower": 30,
            "upper": 50,
            "funding_threshold": 0.0,
            "funding_ma_period": 1,
            "funding_direction": "bull",
        },
    },
    {
        "name":             "rsi_bear_zone_1d_and_funding_bull_positive_ma3",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": f"{_BASE}.rsi_bear_and_funding_bull",
        "params":           {
            "rsi_type": "zone",
            "rsi_period": 14,
            "ma_period": 9,
            "lower": 30,
            "upper": 50,
            "funding_threshold": 0.0,
            "funding_ma_period": 3,
            "funding_direction": "bull",
        },
    },
    {
        "name":             "rsi_bear_slope_zone_1d_and_funding_bull_positive_raw",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": f"{_BASE}.rsi_bear_and_funding_bull",
        "params":           {
            "rsi_type": "slope_zone",
            "rsi_period": 14,
            "ma_period": 9,
            "lower": 30,
            "upper": 50,
            "funding_threshold": 0.0,
            "funding_ma_period": 1,
            "funding_direction": "bull",
        },
    },
    {
        "name":             "rsi_bear_slope_zone_1d_and_funding_bull_positive_ma3",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": f"{_BASE}.rsi_bear_and_funding_bull",
        "params":           {
            "rsi_type": "slope_zone",
            "rsi_period": 14,
            "ma_period": 9,
            "lower": 30,
            "upper": 50,
            "funding_threshold": 0.0,
            "funding_ma_period": 3,
            "funding_direction": "bull",
        },
    },
    {
        "name":             "rsi_bear_zone_1d_and_funding_bull_above_floor_raw",
        "enabled":          False,
        "decision":         "REJECTED",
        "indicator_module": f"{_BASE}.rsi_bear_and_funding_bull",
        "params":           {
            "rsi_type": "zone",
            "rsi_period": 14,
            "ma_period": 9,
            "lower": 30,
            "upper": 50,
            "funding_threshold": 0.0001,
            "funding_ma_period": 1,
            "funding_direction": "bull",
        },
    },
    {
        "name":             "rsi_bear_zone_1d_and_funding_bull_above_floor_ma3",
        "enabled":          False,
        "decision":         "REJECTED",
        "indicator_module": f"{_BASE}.rsi_bear_and_funding_bull",
        "params":           {
            "rsi_type": "zone",
            "rsi_period": 14,
            "ma_period": 9,
            "lower": 30,
            "upper": 50,
            "funding_threshold": 0.0001,
            "funding_ma_period": 3,
            "funding_direction": "bull",
        },
    },
    {
        "name":             "rsi_bear_slope_zone_1d_and_funding_bull_above_floor_raw",
        "enabled":          False,
        "decision":         "REJECTED",
        "indicator_module": f"{_BASE}.rsi_bear_and_funding_bull",
        "params":           {
            "rsi_type": "slope_zone",
            "rsi_period": 14,
            "ma_period": 9,
            "lower": 30,
            "upper": 50,
            "funding_threshold": 0.0001,
            "funding_ma_period": 1,
            "funding_direction": "bull",
        },
    },
    {
        "name":             "rsi_bear_slope_zone_1d_and_funding_bull_above_floor_ma3",
        "enabled":          False,
        "decision":         "REJECTED",
        "indicator_module": f"{_BASE}.rsi_bear_and_funding_bull",
        "params":           {
            "rsi_type": "slope_zone",
            "rsi_period": 14,
            "ma_period": 9,
            "lower": 30,
            "upper": 50,
            "funding_threshold": 0.0001,
            "funding_ma_period": 3,
            "funding_direction": "bull",
        },
    },
]
