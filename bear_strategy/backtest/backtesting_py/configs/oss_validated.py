"""Bear backtest configuration — in-sample (development) window.

Matches the exact strategy parameters promoted through hypothesis_test_v2
(``bear_rsi_vp_session_poc_or_hvn_break``).

Date range: 2021-01-01 → 2023-11-01  ← same window used in hypothesis testing.
Do NOT extend to OOS dates here; use oss_test/ for that.

Strategy
--------
- Regime:  RSI bear zone (RSI 14 + EMA9, zone 30–50) on 1d bars
- Guard:   Funding bull guard (EMA3 of 8h funding > 0) on 1h
- Trigger: Session VP POC-failed-reclaim OR HVN cross-below on 1h
- Risk:    ATR(7), SL = entry + 2×ATR, TP = entry − 3×ATR
- Sizing:  Risk 1% of equity per trade (size = equity×0.01 / stop_distance)
"""

from __future__ import annotations

from dataclasses import dataclass, field

from bear_strategy.strategy.parameters import Parameters

PAIRS: list[str] = [
    "ADAUSDT",
    "BNBUSDT",
    "BTCUSDT",
    "DOTUSDT",
    "ETHUSDT",
    "LTCUSDT",
    "SOLUSDT",
    "XLMUSDT",
    "XRPUSDT",
]


@dataclass
class RunConfig:
    """Top-level config for a multi-pair backtest run."""

    pairs:        list[str] = field(default_factory=lambda: list(PAIRS))
    # Development window — same as hypothesis_test_v2/config.py SHARED dates.
    start_date:   str       = "2021-01-01"
    end_date:     str       = "2023-11-01"
    initial_cash: float     = 10_000.0
    commission:   float     = 0.0008   # 0.08% taker — Bybit standard
    # margin=1.0: no leverage multiplier (standard futures margin accounting).
    # Risk-based sizing keeps individual position notional well within equity.
    margin:       float     = 1.0
    # Fraction of equity to risk per trade (1% → max loss per trade = 1% equity).
    risk_pct:     float     = 0.01
    plot_trades:  bool      = False
    plot_pair:    str       = "BTCUSDT"


DEFAULT_RUN_CONFIG = RunConfig()

DEFAULT_PARAMS = Parameters(
    rsi_period      = 14,
    rsi_ma_period   = 9,
    rsi_lower       = 30.0,
    rsi_upper       = 50.0,
    funding_threshold  = 0.0,
    funding_ma_period  = 3,
    vp_price_bins   = 50,
    atr_period      = 7,
    stop_atr_mult   = 2.0,
    target_atr_mult = 3.0,
    min_sl_pct      = 0.005,
    risk_pct        = 0.01,
    data_dir        = "crypto_data/data",
)
