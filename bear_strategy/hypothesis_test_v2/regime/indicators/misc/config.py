"""
Miscellaneous price-structure regime indicator ideas (Bollinger Bands, SAR).

Set "enabled": False to skip an idea without deleting it.
"""

_BASE = "bear_strategy.hypothesis_test_v2.regime.indicators.misc"

IDEAS: list[dict] = [
    {
        "name":             "close_below_bbands_lower_20_2",
        "enabled":          False,
        "decision":         "PENDING",
        "indicator_module": f"{_BASE}.close_below_bbands_lower",
        "params":           {"period": 20, "std_dev": 2.0},
    },
    {
        "name":             "close_below_sar_1d",
        "enabled":          False,
        "decision":         "PENDING",
        "indicator_module": f"{_BASE}.close_below_sar",
        "params":           {"af_initial": 0.02, "af_step": 0.02, "af_max": 0.20},
        "context_tf":       "1w",
    },
]
