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
        "name":             "close_below_ema_50_1d",
        "indicator_module": "bear_strategy.hypothesis_test_v2.regime.indicators.close_below_ema",
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

from bear_strategy.hypothesis_test_v2.config import SHARED

# ── Entry timeframes for trade entries ───────────────────────────────────────
# These are the timeframes where trades are entered.
# The signal can be computed on a different (context) TF — see context_tf below.
ENTRY_TIMEFRAMES: list[str] = ["15m", "1h"]

# ── Baseline: all bars (unrestricted random-entry population) ─────────────────
BASELINE: dict = {
    "type":  "all_candles",
    "label": "all_candles",
}

# ── Ideas ─────────────────────────────────────────────────────────────────────
IDEAS: list[dict] = [
    # Signal on entry TF (no context_tf) — classic same-TF regime gate
    {
        "name":             "close_below_ema_50",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.regime.indicators.close_below_ema",
        "params":           {"period": 50},
        # no context_tf → signal computed on entry_tf bars directly
    },
    {
        "name":             "close_below_ema_200",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.regime.indicators.close_below_ema",
        "params":           {"period": 200},
    },
    # Signal on 1d context TF — EMA is smoother, avoids noise on entry_tf
    {
        "name":             "close_below_ema_50_1d",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.regime.indicators.close_below_ema",
        "params":           {"period": 50},
        "context_tf":       "1d",  # compute EMA on daily bars, align to entry_tf
    },
    {
        "name":             "close_below_ema_100_1d",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.regime.indicators.close_below_ema",
        "params":           {"period": 100},
        "context_tf":       "1d",  # compute EMA on daily bars, align to entry_tf
    },
    {
        "name":             "close_below_ema_200_1d",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.regime.indicators.close_below_ema",
        "params":           {"period": 300},
        "context_tf":       "1d", 
    }
]
