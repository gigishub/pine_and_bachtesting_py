"""
Supertrend regime indicator ideas.

Set "enabled": False to skip an idea without deleting it.
"""

_BASE = "bear_strategy.hypothesis_test_v2.regime.indicators.supertrend"

IDEAS: list[dict] = [
    {
        "name":             "supertrend_bear",
        "enabled":          False,
        "decision":         "PENDING",
        "indicator_module": f"{_BASE}.supertrend",
        "params":           {"atr_period": 10, "multiplier": 3.0},
    },
]
