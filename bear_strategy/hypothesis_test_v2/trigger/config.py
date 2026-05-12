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

# ── Verdict thresholds for this phase ────────────────────────────────────────
# Trigger: n drops sharply once inside regime + setup, so PF lift floor is
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

# tiered by sample size (0.10 when n < 10k, 0.05 when 10k-50k).
# Coverage floor is relaxed — a trigger that fires 10 % of setup-confirmed
# time is still operationally valid.
THRESHOLDS: dict = {
    "min_pf_lift":      0.05,   # mid-n tier; batch_runner uses tiered logic
    "min_pf_lift_low_n": 0.10,  # used when candidate_n < 10 000
    "min_wr_zscore":   1,    # WR z-score
    "min_coverage":     0.01,   # looser — trigger fires selectively by design
    "min_candidate_pf": 1.0,    # absolute PF floor
}

# ── Entry timeframes to test ─────────────────────────────────────────────────
ENTRY_TIMEFRAMES: list[str] = ["1h","4h"]

# ── Baseline ──────────────────────────────────────────────────────────────────
# Uses regime baseline: rsi_bear_zone_1d_and_funding_bull_positive_ma3 (same as setup)
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
        "name":             "lower_high_formation",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.trigger.indicators.lower_high_formation",
        "params":           {},
    },
    {
        "name":             "inside_bar_break",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.trigger.indicators.inside_bar_break",
        "params":           {},
    },
    {
        "name":             "candle_body_momentum",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.trigger.indicators.candle_body_momentum",
        "params":           {},
    },
    {
        "name":             "n_bar_low_break",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.trigger.indicators.n_bar_low_break",
        "params":           {"n": 5},
    },
    {
        "name":             "pivot_low_break",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.trigger.indicators.pivot_low_break",
        "params":           {"lookback": 5},
    },
    {
        "name":             "rsi_slope",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.trigger.indicators.rsi_slope",
        "params":           {"rsi_period": 14},
    },
    {
        "name":             "stoch_double_cross",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.trigger.indicators.stoch_double_cross",
        "params":           {"k_period": 14, "d_period": 3, "smooth_k": 3},
    },
    {
        "name":             "cci_cross_below_zero",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.trigger.indicators.cci_cross_below_zero",
        "params":           {"length": 20},
    },
    {
        "name":             "roc_cross_below_zero",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.trigger.indicators.roc_cross_below_zero",
        "params":           {"length": 12},
    },
    {
        "name":             "trix_cross",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.trigger.indicators.trix_cross",
        "params":           {"length": 15, "signal_length": 9},
    },
    {
        "name":             "cmf_cross_below_zero",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.trigger.indicators.cmf_cross_below_zero",
        "params":           {"length": 20},
    },
    {
        "name":             "histogram_peak_roll",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.trigger.indicators.histogram_peak_roll",
        "params":           {"fast_period": 12, "slow_period": 26, "signal_period": 9},
    },
    {
        "name":             "falling_tunnel",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.trigger.indicators.falling_tunnel",
        "params":           {"length": 20, "std": 2.0},
    },
    {
        "name":             "atr_expansion_bearish",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.trigger.indicators.atr_expansion_bearish",
        "params":           {"atr_length": 14, "expansion_factor": 1.2},
    },
    {
        "name":             "vwap_cross_below",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.trigger.indicators.vwap_cross_below",
        "params":           {},
    },
    {
        "name":             "vp_below_hvn",
        "enabled":          False,
        "decision":         "SKIP_COMPLEX",
        "indicator_module": "bear_strategy.hypothesis_test_v2.trigger.indicators.vp_below_hvn",
        "params":           {"window": 168, "price_bins": 100},
    },
    {
        "name":             "vp_enters_lvn",
        "enabled":          False,
        "decision":         "SKIP_COMPLEX",
        "indicator_module": "bear_strategy.hypothesis_test_v2.trigger.indicators.vp_enters_lvn",
        "params":           {"window": 168, "price_bins": 100},
    },
    {
        "name":             "vp_poc_retest_fail",
        "enabled":          False,
        "decision":         "SKIP_COMPLEX",
        "indicator_module": "bear_strategy.hypothesis_test_v2.trigger.indicators.vp_poc_retest_fail",
        "params":           {"window": 168, "price_bins": 100, "retest_threshold": 0.02},
    },
]
