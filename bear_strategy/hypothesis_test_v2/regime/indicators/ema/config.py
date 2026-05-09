"""
EMA regime indicator ideas.

Tests whether price or EMA slope conditions identify a bearish regime.
Set "enabled": False to skip an idea without deleting it.
"""

_BASE = "bear_strategy.hypothesis_test_v2.regime.indicators.ema"

IDEAS: list[dict] = [
    {
        "name":             "close_below_ema_200",
        "enabled":          False,
        "decision":         "PENDING",
        "indicator_module": f"{_BASE}.close_below_ema",
        "params":           {"period": 200},
    },
    {
        "name":             "close_below_ema_200_1d",
        "enabled":          False,
        "decision":         "PENDING",
        "indicator_module": f"{_BASE}.close_below_ema",
        "params":           {"period": 300},
        "context_tf":       "1d",
    },
    {
        "name":             "close_below_ema_200_and_ema_dual_slope_down_50_200",
        "enabled":          False,
        "decision":         "PENDING",
        "indicator_module": f"{_BASE}.close_below_ema_200_and_ema_dual_slope_down_50_200",
        "params":           {"ema_period": 200, "fast_period": 50, "slow_period": 200},
    },
    {
        "name":             "ema_slope_down_50",
        "enabled":          False,
        "decision":         "PENDING",
        "indicator_module": f"{_BASE}.ema_slope_down",
        "params":           {"period": 50},
    },
    {
        "name":             "ema_slope_down_200",
        "enabled":          False,
        "decision":         "PENDING",
        "indicator_module": f"{_BASE}.ema_slope_down",
        "params":           {"period": 200},
    },
    {
        "name":             "ema_slope_down_50_1d",
        "enabled":          False,
        "decision":         "PENDING",
        "indicator_module": f"{_BASE}.ema_slope_down",
        "params":           {"period": 50},
        "context_tf":       "1d",
    },
    {
        "name":             "ema_slope_down_200_1d",
        "enabled":          False,
        "decision":         "PENDING",
        "indicator_module": f"{_BASE}.ema_slope_down",
        "params":           {"period": 200},
        "context_tf":       "1d",
    },
    {
        "name":             "ema_dual_slope_down_50_200",
        "enabled":          False,
        "decision":         "PENDING",
        "indicator_module": f"{_BASE}.ema_dual_slope_down",
        "params":           {"fast_period": 50, "slow_period": 200},
    },
    {
        "name":             "ema_dual_slope_down_50_200_1d",
        "enabled":          False,
        "decision":         "PENDING",
        "indicator_module": f"{_BASE}.ema_dual_slope_down",
        "params":           {"fast_period": 50, "slow_period": 200},
        "context_tf":       "1d",
    },
]
