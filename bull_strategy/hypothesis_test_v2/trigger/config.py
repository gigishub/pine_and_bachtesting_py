"""
Trigger phase configuration.

Baseline (PINNED from promoted regime + setup)
-----------------------------------------------
Once both regime and setup indicators are promoted, the trigger baseline
is the population of bars that pass BOTH filters.

After promoting regime AND setup indicators:
1. Set BASELINE type = "indicators"
2. Add each promoted indicator to BASELINE["list"] in order.
3. Re-run trigger tests — they compare against regime+setup bars.

Example:
    BASELINE = {
        "type":  "indicators",
        "label": "ema_slope_up_50_1d__rsi_range_35_60",
        "list": [
            {
                "module":     "bull_strategy.hypothesis_test_v2.regime.indicators.ema_slope_up",
                "params":     {"period": 50},
                "context_tf": "1d",
            },
            {
                "module": "bull_strategy.hypothesis_test_v2.setup.indicators.rsi_range",
                "params": {"period": 14, "low": 35, "high": 60},
            },
        ],
    }
"""

from bull_strategy.hypothesis_test_v2.config import SHARED  # noqa: F401 (kept for IDE navigation)

# ── Pairs under test for this phase ─────────────────────────────────────────
# Edit this list to narrow or expand the universe for the trigger phase.
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
    "min_pf_lift":       0.05,
    "min_pf_lift_low_n": 0.10,
    "min_wr_zscore":     2.5,
    "min_coverage":      0.10,
    "min_candidate_pf":  1.0,
}

# ── Entry timeframes to test ─────────────────────────────────────────────────
ENTRY_TIMEFRAMES: list[str] = ["15m", "1h"]

# ── Baseline ──────────────────────────────────────────────────────────────────
BASELINE: dict = {
    "type":  "all_candles",
    "label": "all_candles",
}

# ── Ideas ─────────────────────────────────────────────────────────────────────
IDEAS: list[dict] = [
    {
        "name":             "ema_cross_up",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bull_strategy.hypothesis_test_v2.trigger.indicators.ema_cross_up",
        "params":           {"fast_period": 8, "slow_period": 21},
    },
]
