"""
Setup phase configuration.

Baseline (PINNED from promoted regime)
---------------------------------------
Once a regime indicator is promoted, it becomes the BASELINE here.
Update the BASELINE dict below to point to the promoted regime indicator,
including context_tf if the regime was computed on a higher timeframe.

Example after promoting "close_below_ema_50_1d":
    BASELINE = {
        "type":       "indicator",
        "label":      "close_below_ema_50_1d",
        "module":     "bear_strategy.hypothesis_test_v2.regime.indicators.close_below_ema",
        "params":     {"period": 50},
        "context_tf": "1d",   # same context_tf as how regime was computed
    }

Multi-TF ideas (context_tf)
-----------------------------
Setup ideas can also compute on a different TF:
    {
        "name":             "kde_upper_4h",
        "indicator_module": "...kde_upper",
        "params":           {"bandwidth": 0.15, "lookback_bars": 200},
        "context_tf":       "4h",   # KDE computed on 4h, aligned to entry_tf
    }

How to promote to trigger phase
--------------------------------
1. Change "decision" to "PROMOTED" in the winning idea.
2. Add both regime and setup entries to trigger/config.py BASELINE["list"].
"""

from bear_strategy.hypothesis_test_v2.config import SHARED

# ── Entry timeframes for trade entries ───────────────────────────────────────
ENTRY_TIMEFRAMES: list[str] = ["15m", "1h"]

# ── Baseline ──────────────────────────────────────────────────────────────────
# INITIAL: all candles until a regime is promoted.
# After regime promotion update to the winning regime indicator, e.g.:
#   BASELINE = {
#       "type":       "indicator",
#       "label":      "close_below_ema_50_1d",
#       "module":     "bear_strategy.hypothesis_test_v2.regime.indicators.close_below_ema",
#       "params":     {"period": 50},
#       "context_tf": "1d",
#   }
BASELINE: dict = {
    "type":  "all_candles",
    "label": "all_candles",
}

# ── Ideas ─────────────────────────────────────────────────────────────────────
IDEAS: list[dict] = [
    {
        "name":             "rsi_range_40_65",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.setup.indicators.rsi_range",
        "params":           {"period": 14, "low": 40, "high": 65},
        # no context_tf: RSI computed on entry_tf bars
    },
    {
        "name":             "kde_upper_entry_tf",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.setup.indicators.kde_upper",
        "params":           {"bandwidth": 0.15, "lookback_bars": 200},
        # no context_tf: KDE computed on entry_tf closes
    },
    {
        "name":             "rvol_breakdown_2x",
        "enabled":          False,
        "decision":         "REJECTED",
        "indicator_module": "bear_strategy.hypothesis_test_v2.setup.indicators.rvol_breakdown",
        "params":           {"period": 20, "threshold": 2.0},
    },
]
