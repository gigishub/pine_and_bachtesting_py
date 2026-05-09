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
        "module":     "bear_strategy.hypothesis_test_v2.regime.indicators.ema.close_below_ema",
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
# Setup: raise coverage floor — a setup that fires < 20 % of regime-confirmed
# time is too sparse to be useful as a structural condition.
THRESHOLDS: dict = {
    "min_pf_lift":   0.05,   # absolute PF lift required
    "min_wr_zscore": 2.5,    # WR z-score (> 2.5 → 99 % confidence)
    "min_coverage":  0.20,   # stricter than regime — setup must fire often enough
    "min_candidate_pf": 1.0, # absolute PF floor
}

# ── Entry timeframes for trade entries ───────────────────────────────────────
ENTRY_TIMEFRAMES: list[str] = ["1h", "4h"]

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
        "type":             "indicator",
        "label":            "rsi_bear_zone_1d_and_funding_bull_positive_ma3",
        "module":           "bear_strategy.hypothesis_test_v2.regime.indicators.combinations.rsi_bear_and_funding_bull",
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
        "context_tf":       "1d",
}

# ── Ideas ─────────────────────────────────────────────────────────────────────
IDEAS: list[dict] = [

    {
        "name":             "kde_upper",
        "enabled":          False,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.setup.indicators.kde_upper",
        "params":           {"bandwidth": 0.15, "lookback_bars": 200},
    },
    {
        "name":             "kde_lower_first_5",
        "enabled":          False,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.setup.indicators.kde_lower",
        "params":           {"bandwidth": 0.15, "lookback_bars": 200, "max_bars": 5},
    },
    {
        "name":             "close_above_kde_upper",
        "enabled":          False,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.setup.indicators.close_above_kde_upper",
        "params":           {"bandwidth": 0.15, "lookback_bars": 200},
        # no context_tf: KDE level computed on entry_tf bars
    },

    {
        "name":             "rvol_breakdown_1.5x",
        "enabled":          False,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.setup.indicators.rvol_breakdown",
        "params":           {"period": 20, "threshold": 1.5},
    },
    {
        "name":             "macd_downward",
        "enabled":          False,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.setup.indicators.macd_downward",
        "params":           {"fast_period": 12, "slow_period": 26, "signal_period": 9},

    },

    {
        "name":             "macd_red_acceleration",
        "enabled":          False,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.setup.indicators.macd_red_acceleration",
        "params":           {"fast_period": 12, "slow_period": 26, "signal_period": 9, "drop_pct": 0.50},

    },
    {
        "name":             "rsi_30_50",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.setup.indicators.rsi_range",
        "params":           {"period": 14, "low": 30, "high": 50},
    },
    {
        "name":             "macd_above_zero_converging",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.setup.indicators.macd_above_zero_converging",
        "params":           {"fast_period": 12, "slow_period": 26, "signal_period": 9},
    },
    {
        "name":             "macd_above_threshold_converging",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.setup.indicators.macd_above_threshold_converging",
        "params":           {"fast_period": 12, "slow_period": 26, "signal_period": 9, "threshold": 0.0005},
    },
    {
        "name":             "rsi_ma_dynamic_band",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.setup.indicators.rsi_ma_dynamic_band",
        "params":           {"rsi_period": 14, "ma_period": 9, "ma_lower": 65, "ma_upper": 75, "distance_at_lower": 0.10, "distance_at_upper": 0.05},
    },
]
