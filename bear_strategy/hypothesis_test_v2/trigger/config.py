"""
Trigger phase configuration.

Baseline (PINNED from promoted regime + setup)
-----------------------------------------------
Once both regime and setup indicators are promoted, the trigger baseline
is the population of bars that pass BOTH filters.  The trigger idea is then
tested against that joint baseline.

How to update the baseline
--------------------------
After promoting regime AND setup indicators:
1. Set BASELINE type = "indicators"
2. Add each promoted indicator to BASELINE["list"] in order.
3. Re-run trigger tests — they compare against regime+setup bars.

How to add an idea
------------------
Append a dict to IDEAS.  Set "enabled": False to skip temporarily.
"""

from bear_strategy.hypothesis_test_v2.config import SHARED

# ── Entry timeframes to test ─────────────────────────────────────────────────
ENTRY_TIMEFRAMES: list[str] = ["15m", "1h"]

# ── Baseline ──────────────────────────────────────────────────────────────────
# INITIAL STATE: all candles until regime + setup are promoted.
# After promotion, update to:
#
#   BASELINE = {
#       "type":  "indicators",
#       "label": "ema50_rsi_range",
#       "list": [
#           {
#               "module": "bear_strategy.hypothesis_test_v2.regime.indicators.close_below_ema",
#               "params": {"period": 50},
#           },
#           {
#               "module": "bear_strategy.hypothesis_test_v2.setup.indicators.rsi_range",
#               "params": {"period": 14, "low": 40, "high": 65},
#           },
#       ],
#   }
BASELINE: dict = {
    "type":  "all_candles",
    "label": "all_candles",  # ← update after regime + setup are promoted
}

# ── Ideas ─────────────────────────────────────────────────────────────────────
IDEAS: list[dict] = [
    {
        "name":             "ema_cross_down",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.trigger.indicators.ema_cross_down",
        "params":           {"fast_period": 8, "slow_period": 21},
    },
]
