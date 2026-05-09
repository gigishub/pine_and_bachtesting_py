"""
Trigger phase hypothesis testing — CONFIG 2.

Alternative configuration with improved volume profile using session-based approach
instead of rolling 168-bar window. Session VP resets daily, giving cleaner zones.

Baseline: rsi_bear_zone_1d_and_funding_bull_positive_ma3 (regime-only, no setup layer)
Entry TFs: 1h, 4h
Thresholds: min_coverage=0.01, min_wr_zscore=1.0, min_pf_lift=0.05, min_candidate_pf=1.0
"""
from __future__ import annotations

# ── Baseline ──────────────────────────────────────────────────────────────────
BASELINE: dict = {
    "type": "indicator",
    "label": "rsi_bear_zone_1d_and_funding_bull_positive_ma3",
    "module": "bear_strategy.hypothesis_test_v2.regime.indicators.combinations.rsi_bear_and_funding_bull",
    "params": {
        "rsi_type": "zone",
        "rsi_period": 14,
        "ma_period": 9,
        "lower": 30,
        "upper": 50,
        "funding_threshold": 0.0,
        "funding_ma_period": 3,
        "funding_direction": "bull",
    },
    "context_tf": "1d",
}

# ── Pairs ─────────────────────────────────────────────────────────────────────
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

# ── Entry Timeframes ──────────────────────────────────────────────────────────
ENTRY_TIMEFRAMES: list[str] = ["1h", "4h"]

# ── Thresholds ────────────────────────────────────────────────────────────────
MIN_PF_LIFT: float = 0.05          # Minimum PF improvement over baseline
MIN_WR_ZSCORE: float = 1.0         # Relaxed for rare trigger signals
MIN_COVERAGE: float = 0.01         # Allow very rare triggers (1%)
MIN_CANDIDATE_PF: float = 1.0      # Absolute floor: must not lose money

MIN_PF_LIFT_LOW_N: float = 0.10    # Stricter for very low sample size (<100 trades)

# ── Ideas ─────────────────────────────────────────────────────────────────────
# Session-based volume profile triggers ONLY (testing alternative approach)
IDEAS: list[dict] = [
    {
        "name":             "vp_session_poc_break",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.trigger.indicators.vp_session_poc_break",
        "params":           {"price_bins": 100},
    },
    {
        "name":             "vp_session_hvn_break",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.trigger.indicators.vp_session_hvn_break",
        "params":           {"price_bins": 100},
    },
    {
        "name":             "vp_session_lvn_entry",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.trigger.indicators.vp_session_lvn_entry",
        "params":           {"price_bins": 100},
    },
]
