"""
RSI regime indicator ideas.

All variants test whether RSI (and RSI-MA) identify a bearish regime zone.
Set "enabled": False to skip an idea without deleting it.
"""

_BASE = "bear_strategy.hypothesis_test_v2.regime.indicators.rsi"

IDEAS: list[dict] = [
    {
        "name":             "rsi_bear_zone",
        "enabled":          False,
        "decision":         "PENDING",
        "indicator_module": f"{_BASE}.rsi_bear_zone",
        "params":           {"rsi_period": 14, "ma_period": 9, "lower": 30, "upper": 50},
    },
    {
        "name":             "rsi_bear_zone_1d",
        "enabled":          True,
        "decision":         "PROMOTED",
        "indicator_module": f"{_BASE}.rsi_bear_zone",
        "params":           {"rsi_period": 14, "ma_period": 9, "lower": 30, "upper": 50},
        "context_tf":       "1d",
    },
    {
        "name":             "rsi_bear_slope_zone",
        "enabled":          False,
        "decision":         "PENDING",
        "indicator_module": f"{_BASE}.rsi_bear_slope_zone",
        "params":           {"rsi_period": 14, "ma_period": 9, "lower": 30, "upper": 50},
    },
    {
        "name":             "rsi_bear_slope_zone_1d",
        "enabled":          True,
        "decision":         "PROMOTED",
        "indicator_module": f"{_BASE}.rsi_bear_slope_zone",
        "params":           {"rsi_period": 14, "ma_period": 9, "lower": 30, "upper": 50},
        "context_tf":       "1d",
    },
    {
        "name":             "rsi_bear_momentum_zone",
        "enabled":          False,
        "decision":         "PENDING",
        "indicator_module": f"{_BASE}.rsi_bear_momentum_zone",
        "params":           {"rsi_period": 14, "lower": 30, "upper": 50},
    },
    {
        "name":             "rsi_bear_momentum_zone_1d",
        "enabled":          False,
        "decision":         "PENDING",
        "indicator_module": f"{_BASE}.rsi_bear_momentum_zone",
        "params":           {"rsi_period": 14, "lower": 30, "upper": 50},
        "context_tf":       "1d",
    },
    {
        "name":             "rsi_bear_1d_any_zone",
        "enabled":          False,
        "decision":         "PENDING",
        "indicator_module": f"{_BASE}.rsi_bear_1d_any_zone",
        "params":           {"rsi_period": 14, "ma_period": 9, "lower": 30, "upper": 50},
        "context_tf":       "1d",
    },
    {
        "name":             "rsi_bear_zone_1d_and_close_below_ema_100",
        "enabled":          False,
        "decision":         "PENDING",
        "indicator_module": f"{_BASE}.rsi_bear_signal_and_close_below_ema",
        "params":           {"rsi_type": "zone", "rsi_period": 14, "ma_period": 9, "lower": 30, "upper": 50, "ema_period": 100},
        "context_tf":       "1d",
    },
    {
        "name":             "rsi_bear_zone_1d_and_close_below_ema_200",
        "enabled":          False,
        "decision":         "PENDING",
        "indicator_module": f"{_BASE}.rsi_bear_signal_and_close_below_ema",
        "params":           {"rsi_type": "zone", "rsi_period": 14, "ma_period": 9, "lower": 30, "upper": 50, "ema_period": 200},
        "context_tf":       "1d",
    },
    {
        "name":             "rsi_bear_slope_zone_1d_and_close_below_ema_100",
        "enabled":          False,
        "decision":         "PENDING",
        "indicator_module": f"{_BASE}.rsi_bear_signal_and_close_below_ema",
        "params":           {"rsi_type": "slope_zone", "rsi_period": 14, "ma_period": 9, "lower": 30, "upper": 50, "ema_period": 100},
        "context_tf":       "1d",
    },
    {
        "name":             "rsi_bear_slope_zone_1d_and_close_below_ema_200",
        "enabled":          False,
        "decision":         "PENDING",
        "indicator_module": f"{_BASE}.rsi_bear_signal_and_close_below_ema",
        "params":           {"rsi_type": "slope_zone", "rsi_period": 14, "ma_period": 9, "lower": 30, "upper": 50, "ema_period": 200},
        "context_tf":       "1d",
    },
    {
        "name":             "rsi_bear_zone_or_slope_1d_and_close_below_ema_100_200",
        "enabled":          False,
        "decision":         "PENDING",
        "indicator_module": f"{_BASE}.rsi_bear_zone_or_slope_1d_and_close_below_ema_100_200",
        "params":           {"rsi_period": 14, "ma_period": 9, "lower": 30, "upper": 50, "ema_period_100": 100, "ema_period_200": 200},
        "context_tf":       "1d",
    },
    {
        "name":             "rsi_bear_slope_zone_and_close_below_ema_200",
        "enabled":          False,
        "decision":         "PENDING",
        "indicator_module": f"{_BASE}.rsi_bear_slope_zone_and_close_below_ema",
        "params":           {"rsi_period": 14, "ma_period": 9, "lower": 30, "upper": 50, "ema_period": 200},
    },
    {
        "name":             "rsi_bear_slope_zone_and_ema_slope_down_50",
        "enabled":          False,
        "decision":         "PENDING",
        "indicator_module": f"{_BASE}.rsi_bear_slope_zone_and_ema_slope_down_50",
        "params":           {"rsi_period": 14, "ma_period": 9, "lower": 30, "upper": 50, "ema_period": 50},
    },
]
