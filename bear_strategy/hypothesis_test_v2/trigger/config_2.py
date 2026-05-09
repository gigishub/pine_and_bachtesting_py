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

THRESHOLDS: dict = {
    "min_pf_lift": MIN_PF_LIFT,
    "min_pf_lift_low_n": MIN_PF_LIFT_LOW_N,
    "min_wr_zscore": MIN_WR_ZSCORE,
    "min_coverage": MIN_COVERAGE,
    "min_candidate_pf": MIN_CANDIDATE_PF,
}

# ── Ideas ─────────────────────────────────────────────────────────────────────
# Session VP (approach 1): profile from prior daily session.
#   On 1h: 24 bars/session  |  On 4h: 6 bars/session (sparse)
# Rolling VP (approach 2): profile from prior N bars — richer on 4h.
#   window=168 on 1h ≈ 1 week  |  window=168 on 4h ≈ 28 days
# ─── Session VP (originals — unchanged) ───────────────────────────────────────
IDEAS: list[dict] = [
    {
        "name":             "vp_session_poc_break",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.trigger.indicators.vp_session_poc_break",
        "params":           {"price_bins": 50},
    },
    {
        "name":             "vp_session_hvn_break",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.trigger.indicators.vp_session_hvn_break",
        "params":           {"price_bins": 50},
    },
    {
        "name":             "vp_session_lvn_entry",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.trigger.indicators.vp_session_lvn_entry",
        "params":           {"price_bins": 50},
    },
    # ── 4th trigger: session VP OR combo ──────────────────────────────────────
    {
        "name":             "vp_session_poc_or_hvn_break",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.trigger.indicators.vp_session_poc_or_hvn_break",
        "params":           {"price_bins": 50},
    },

    # ─── Rolling fixed-range VP ────────────────────────────────────────────────
    # Same signal logic as session variants but VP built from a rolling window of
    # prior bars instead of prior daily session.  Gives 168 data points regardless
    # of entry TF — far richer profile on 4h (168 bars ≈ 28 days) vs session (6 bars).
    {
        "name":             "vp_rolling_poc_break_168",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.trigger.indicators.vp_rolling_poc_break",
        "params":           {"window": 168, "price_bins": 50},
    },
    {
        "name":             "vp_rolling_hvn_break_168",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.trigger.indicators.vp_rolling_hvn_break",
        "params":           {"window": 168, "price_bins": 50},
    },
    {
        "name":             "vp_rolling_lvn_entry_168",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.trigger.indicators.vp_rolling_lvn_entry",
        "params":           {"window": 168, "price_bins": 50},
    },
    {
        "name":             "vp_rolling_poc_or_hvn_break_168",
        "enabled":          True,
        "decision":         "PENDING",
        "indicator_module": "bear_strategy.hypothesis_test_v2.trigger.indicators.vp_rolling_poc_or_hvn_break",
        "params":           {"window": 168, "price_bins": 50},
    },
]
