"""
Out-of-sample (OOS) test configuration.

Date window is COMPLETELY SEPARATE from the development window in config.py.
Never move start earlier than the dev window's end date (2023-11-01).

STRATEGIES lists the FULL filter stack (regime + setup + trigger) to evaluate.
Each strategy's filters are AND-ed to produce a compound signal.
The baseline is always random (all warmed candles in the OOS window).

How to add a new strategy combination
--------------------------------------
Append a new dict to STRATEGIES with a descriptive name and the ordered
list of filters.  Set "enabled": False to skip it without deleting it.
"""

# ── OOS date window (unseen data) ────────────────────────────────────────────
# Dev window closed 2023-11-01.  OOS starts the next day.
OOS_SHARED: dict = {
    "start": "2023-11-02",
    "end":   "2026-04-22",
    "stop_atr_mult":   2.0,
    "target_atr_mult": 3,
    "atr_period":      7,
    "data_dir": "crypto_data/data",
}

# ── Pairs under test ──────────────────────────────────────────────────────────
# Narrowed to the 6 pairs that reached the trigger phase.
PAIRS: list[str] = [
    "ADAUSDT",
    "BATUSDT",
    "DOTUSDT",
    "ETHUSDT",
    "LTCUSDT",
    "XRPUSDT",
]

# ── Entry timeframes ──────────────────────────────────────────────────────────
ENTRY_TIMEFRAMES: list[str] = ["4h"]

# ── Pass/fail thresholds ──────────────────────────────────────────────────────
THRESHOLDS: dict = {
    "min_pf_lift":       0.05,
    "min_wr_zscore":     2.5,
    "min_coverage":      0.02,   # OOS — highly selective triggers are acceptable
    "min_candidate_pf":  1.0,
}

# ── Strategies ────────────────────────────────────────────────────────────────
# Each entry is the FULL promoted stack (regime + setup + trigger).
# Filters are evaluated in order and AND-ed together.
# "context_tf" causes the signal to be computed on that timeframe then
# shift(1)+merge_asof-aligned to the entry TF — no lookahead.
STRATEGIES: list[dict] = [
    {
        # Promoted stack: rsi_bear_zone_1d + kde_upper + macd_downward
        "name":    "bear_rsi_kde_macd_downward",
        "enabled": True,
        "filters": [
            # ── Regime: RSI bear zone on daily ───────────────────────────
            {
                "module": "bear_strategy.hypothesis_test_v2.regime.indicators.rsi.rsi_bear_zone",
                "params": {"rsi_period": 14, "ma_period": 9, "lower": 30, "upper": 50},
                "context_tf": "1d",
            },
            # ── Setup: KDE price near upper of range ─────────────────────
            {
                "module": "bear_strategy.hypothesis_test_v2.setup.indicators.kde_upper",
                "params": {"bandwidth": 0.15, "lookback_bars": 200},
            },
            # ── Trigger: MACD histogram turning downward ─────────────────
            {
                "module": "bear_strategy.hypothesis_test_v2.setup.indicators.macd_downward",
                "params": {"fast_period": 12, "slow_period": 26, "signal_period": 9},
            },
        ],
    },
]
