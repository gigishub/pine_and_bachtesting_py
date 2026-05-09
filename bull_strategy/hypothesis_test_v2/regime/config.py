"""
Regime phase configuration.

Baseline
--------
type = "all_candles"
Every warmed bar is a random entry — no prior filter applied.
This is the CORRECT baseline for regime testing.

Multi-TF support (context_tf)
------------------------------
Add "context_tf" to any idea to compute the signal on a different timeframe
and have it automatically shift(1)+aligned to the entry bars with no lookahead.

Example — EMA computed on 1d, entries on 15m / 1h:
    {
        "name":             "close_above_ema_50_1d",
        "indicator_module": "bull_strategy.hypothesis_test_v2.regime.indicators.close_above_ema",
        "params":           {"period": 50},
        "context_tf":       "1d",   # ← signal computed on 1d, aligned to entry_tf
    }

Without context_tf, the signal is computed directly on the entry_tf bars.

How to promote to setup phase
------------------------------
1. Change "decision" to "PROMOTED" in the winning idea.
2. Copy the indicator_module + params + context_tf (if any) to setup/config.py BASELINE.
3. The setup phase will compare new ideas against regime-filtered bars.
"""

from bull_strategy.hypothesis_test_v2.config import SHARED  # noqa: F401 (kept for IDE navigation)

# ── Pairs under test for this phase ─────────────────────────────────────────
# Edit this list to narrow or expand the universe for the regime phase.
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
    "min_coverage":     0.10,
    "min_candidate_pf": 1.0,
}

# ── Entry timeframes for trade entries ───────────────────────────────────────
ENTRY_TIMEFRAMES: list[str] = [ "1h", "4h", "1d"]

# ── Baseline: all bars (unrestricted random-entry population) ─────────────────
BASELINE: dict = {
    "type":  "all_candles",
    "label": "all_candles",
}

# ── Ideas ─────────────────────────────────────────────────────────────────────
IDEAS: list[dict] = [
    # ── ACTIVE TEST — single Supertrend bullish filter ─────────────────────────
    {
        "name":             "supertrend_bull",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bull_strategy.hypothesis_test_v2.regime.indicators.supertrend",
        "params":           {"atr_period": 10, "multiplier": 3.0},
    },

    # ── DEACTIVATED — previous regime candidates ───────────────────────────────
    {
        "name":             "rsi_bull_zone_1d_and_close_above_ema_200",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bull_strategy.hypothesis_test_v2.regime.indicators.rsi_bull_zone_1d_and_close_above_ema_200",
        "params":           {"rsi_period": 14, "ma_period": 9, "lower": 50, "upper": 70, "ema_period": 200},
    },
    {
        "name":             "ema_slope_up_50",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bull_strategy.hypothesis_test_v2.regime.indicators.ema_slope_up",
        "params":           {"period": 50},
    },
    {
        "name":             "ema_slope_up_200",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bull_strategy.hypothesis_test_v2.regime.indicators.ema_slope_up",
        "params":           {"period": 200},
    },
    {
        "name":             "ema_slope_up_50_1d",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bull_strategy.hypothesis_test_v2.regime.indicators.ema_slope_up",
        "params":           {"period": 50},
        "context_tf":       "1d",
    },
    {
        "name":             "ema_slope_up_200_1d",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bull_strategy.hypothesis_test_v2.regime.indicators.ema_slope_up",
        "params":           {"period": 200},
        "context_tf":       "1d",
    },
    {
        "name":             "ema_dual_slope_up_50_200",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bull_strategy.hypothesis_test_v2.regime.indicators.ema_dual_slope_up",
        "params":           {"fast_period": 50, "slow_period": 200},
    },
    {
        "name":             "ema_dual_slope_up_50_200_1d",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bull_strategy.hypothesis_test_v2.regime.indicators.ema_dual_slope_up",
        "params":           {"fast_period": 50, "slow_period": 200},
        "context_tf":       "1d",
    },
    {
        "name":             "close_above_ema_200",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bull_strategy.hypothesis_test_v2.regime.indicators.close_above_ema",
        "params":           {"period": 200},
    },
    {
        "name":             "close_above_ema_200_1d",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bull_strategy.hypothesis_test_v2.regime.indicators.close_above_ema",
        "params":           {"period": 200},
        "context_tf":       "1d",
    },
    {
        "name":             "close_above_bbands_upper_20_2",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bull_strategy.hypothesis_test_v2.regime.indicators.close_above_bbands_upper",
        "params":           {"period": 20, "std_dev": 2.0},
    },
    {
        "name":             "close_above_sar_1d",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bull_strategy.hypothesis_test_v2.regime.indicators.close_above_sar",
        "params":           {"af_initial": 0.02, "af_step": 0.02, "af_max": 0.20},
        "context_tf":       "1d",
    },
    {
        "name":             "rsi_bull_zone",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bull_strategy.hypothesis_test_v2.regime.indicators.rsi_bull_zone",
        "params":           {"rsi_period": 14, "ma_period": 9, "lower": 50, "upper": 70},
    },
    {
        "name":             "rsi_bull_zone_1d",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bull_strategy.hypothesis_test_v2.regime.indicators.rsi_bull_zone",
        "params":           {"rsi_period": 14, "ma_period": 9, "lower": 50, "upper": 70},
        "context_tf":       "1d",
    },
    {
        "name":             "rsi_bull_slope_zone",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bull_strategy.hypothesis_test_v2.regime.indicators.rsi_bull_slope_zone",
        "params":           {"rsi_period": 14, "ma_period": 9, "lower": 50, "upper": 70},
    },
    {
        "name":             "rsi_bull_slope_zone_1d",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bull_strategy.hypothesis_test_v2.regime.indicators.rsi_bull_slope_zone",
        "params":           {"rsi_period": 14, "ma_period": 9, "lower": 50, "upper": 70},
        "context_tf":       "1d",
    },
    {
        "name":             "rsi_bull_momentum_zone",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bull_strategy.hypothesis_test_v2.regime.indicators.rsi_bull_momentum_zone",
        "params":           {"rsi_period": 14, "lower": 50, "upper": 70},
    },
    {
        "name":             "rsi_bull_momentum_zone_1d",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bull_strategy.hypothesis_test_v2.regime.indicators.rsi_bull_momentum_zone",
        "params":           {"rsi_period": 14, "lower": 50, "upper": 70},
        "context_tf":       "1d",
    },

    # ── ACTIVE — Funding rate bullish regime ──────────────────────────────────
    # funding > threshold → longs dominate OI, bullish funding environment.
    # threshold=0.0     : any positive funding (longs pay shorts)
    # threshold=0.0001  : above the Bybit floor rate (clearly bullish OI pressure)
    # ma_period=1       : raw 8h funding rate (responsive)
    # ma_period=3       : 3-observation EMA (~24h smoothing, filters spikes)
    {
        "name":             "funding_bull_positive_raw",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bull_strategy.hypothesis_test_v2.regime.indicators.funding_rate",
        "params":           {"threshold": 0.0, "ma_period": 1},
    },
    {
        "name":             "funding_bull_above_floor_raw",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bull_strategy.hypothesis_test_v2.regime.indicators.funding_rate",
        "params":           {"threshold": 0.0001, "ma_period": 1},
    },
    {
        "name":             "funding_bull_positive_ma3",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bull_strategy.hypothesis_test_v2.regime.indicators.funding_rate",
        "params":           {"threshold": 0.0, "ma_period": 3},
    },
    {
        "name":             "funding_bull_above_floor_ma3",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bull_strategy.hypothesis_test_v2.regime.indicators.funding_rate",
        "params":           {"threshold": 0.0001, "ma_period": 3},
    },
]
