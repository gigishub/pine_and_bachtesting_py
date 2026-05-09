"""OSS-validated backtest configuration.

Parameters match exactly what was promoted in hypothesis_test_v2/oss_test/config.py
as ``bear_rsi_vp_session_poc_or_hvn_break``.

Strategy:
  - Regime: RSI bear zone (RSI 14 + EMA9, zone 30–50) on 1d bars
  - Regime gate: Funding bull guard (EMA3 of 8h funding > 0.0) on 1h
  - Trigger: Session VP POC-failed-reclaim OR HVN cross-below on 1h
  - Risk: ATR(7), SL = entry + 2×ATR, TP = entry − 3×ATR
  - OOS date range: 2023-11-02 → 2026-04-22
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
    start_date:   str       = "2023-11-02"
    end_date:     str       = "2026-04-22"
    initial_cash: float     = 10_000.0
    commission:   float     = 0.0008   # 0.08% taker fee — Bybit standard
    # margin=0.1 → 10x leverage, matching a conservative perpetual futures account.
    # Required so short orders aren't canceled by insufficient margin on high-priced assets.
    margin:       float     = 0.1
    # Trade sizing: fraction of available margin capacity used per trade.
    # At margin=0.1 (10x), trade_size=0.5 → 5x effective leverage per trade.
    trade_size:   float     = 0.5


OSS_RUN_CONFIG = RunConfig()

OSS_PARAMS = Parameters(
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
    data_dir        = "crypto_data/data",
)
