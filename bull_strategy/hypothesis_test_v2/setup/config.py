"""
Setup phase configuration.

Baseline (PINNED from promoted regime)
---------------------------------------
Once a regime indicator is promoted, it becomes the BASELINE here.
Update the BASELINE dict below to point to the promoted regime indicator,
including context_tf if the regime was computed on a higher timeframe.

Example after promoting "ema_slope_up_50_1d":
    BASELINE = {
        "type":       "indicator",
        "label":      "ema_slope_up_50_1d",
        "module":     "bull_strategy.hypothesis_test_v2.regime.indicators.ema_slope_up",
        "params":     {"period": 50},
        "context_tf": "1d",
    }

How to promote to trigger phase
--------------------------------
1. Change "decision" to "PROMOTED" in the winning idea.
2. Add both regime and setup entries to trigger/config.py BASELINE["list"].
"""

from bull_strategy.hypothesis_test_v2.config import SHARED  # noqa: F401 (kept for IDE navigation)

# ── Pairs under test for this phase ─────────────────────────────────────────
# Edit this list to narrow or expand the universe for the setup phase.
PAIRS: list[str] = [
    "ADAUSDT",
    "BATUSDT",
    "BNBUSDT",
    "BTCUSDT",
    "DOTUSDT",
    "ETHUSDT",
    "LTCUSDT",
    "SOLUSDT",
    "TRXUSDT",
    "XLMUSDT",
    "XRPUSDT",
]

# ── Verdict thresholds for this phase ────────────────────────────────────────
THRESHOLDS: dict = {
    "min_pf_lift":      0.05,
    "min_wr_zscore":    2.5,
    "min_coverage":     0.20,
    "min_candidate_pf": 1.0,
}

# ── Entry timeframes for trade entries ───────────────────────────────────────
ENTRY_TIMEFRAMES: list[str] = ["15m", "1h", "4h", "1d"]

# ── Baseline ──────────────────────────────────────────────────────────────────
# INITIAL: all candles until a regime is promoted.
# After regime promotion update to the winning regime indicator.
BASELINE: dict = {
    "type":  "all_candles",
    "label": "all_candles",
}

# ── Ideas ─────────────────────────────────────────────────────────────────────
IDEAS: list[dict] = [
    {
        "name":             "rsi_range_35_60",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bull_strategy.hypothesis_test_v2.setup.indicators.rsi_range",
        "params":           {"period": 14, "low": 35, "high": 60},
    },
    {
        "name":             "kde_lower_entry_tf",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bull_strategy.hypothesis_test_v2.setup.indicators.kde_lower",
        "params":           {"bandwidth": 0.15, "lookback_bars": 200},
    },
    {
        "name":             "kde_lower_4h",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bull_strategy.hypothesis_test_v2.setup.indicators.kde_lower",
        "params":           {"bandwidth": 0.15, "lookback_bars": 200},
        "context_tf":       "4h",
    },
    {
        "name":             "close_near_kde_lower",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bull_strategy.hypothesis_test_v2.setup.indicators.close_near_kde_lower",
        "params":           {"bandwidth": 0.15, "lookback_bars": 200},
    },
    {
        "name":             "close_near_kde_lower_4h",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bull_strategy.hypothesis_test_v2.setup.indicators.close_near_kde_lower",
        "params":           {"bandwidth": 0.15, "lookback_bars": 200},
        "context_tf":       "4h",
    },
]
