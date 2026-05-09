"""Entry signal composition for the Bear Strategy.

Combines three layers into a single boolean entry signal:
  1. RSI bear zone on 1d bars (regime) → aligned to entry TF via merge_asof.
  2. Funding rate bull guard on entry TF (regime gate).
  3. Session VP POC / HVN break on entry TF (trigger).

All indicators are anti-lookahead by design (shift(1) on HTF before alignment;
shift(1) on funding settled rate).
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from bear_strategy.hypothesis_test_v2.engine.alignment import align_htf_to_ltf
from bear_strategy.strategy.indicators.regime.funding_bull_guard import compute_funding_bull_guard
from bear_strategy.strategy.indicators.regime.rsi_bear_zone import compute_rsi_bear_zone
from bear_strategy.strategy.indicators.trigger.vp_session_poc_or_hvn_break import compute_vp_signal
from bear_strategy.strategy.parameters import Parameters


def compute_entry_signal(
    df_1h: pd.DataFrame,
    df_1d: pd.DataFrame,
    funding_df: pd.DataFrame,
    params: Parameters,
) -> pd.Series:
    """Compute the full bear-strategy entry signal on the 1h timeline.

    Args:
        df_1h:       1h OHLCV DataFrame (entry timeframe). Must have a
                     DatetimeIndex and lowercase column names.
        df_1d:       1d OHLCV DataFrame (regime timeframe). Same conventions.
        funding_df:  Funding rate DataFrame with a 'fundingrate' column.
        params:      Strategy parameters.

    Returns:
        Boolean Series on df_1h.index — True = all filters pass → enter short.
    """
    # Layer 1: RSI bear zone on daily bars, aligned backward to 1h
    rsi_1d   = compute_rsi_bear_zone(df_1d, params.rsi_period, params.rsi_ma_period,
                                     params.rsi_lower, params.rsi_upper)
    regime   = align_htf_to_ltf(df_1d, rsi_1d, df_1h, shift=True)

    # Layer 2: Funding bull guard on entry TF
    funding  = compute_funding_bull_guard(df_1h, funding_df,
                                          params.funding_threshold, params.funding_ma_period)

    # Layer 3: Session VP POC/HVN break trigger on entry TF
    trigger  = compute_vp_signal(df_1h, params.vp_price_bins)

    return (regime & funding & trigger).fillna(False)


def compute_atr(df: pd.DataFrame, period: int) -> pd.Series:
    """Compute Average True Range on entry-TF OHLCV data.

    Uses exponential moving average (Wilder's method) consistent with the
    hypothesis test engine.

    Args:
        df:     OHLCV DataFrame with 'high', 'low', 'close' columns.
        period: ATR lookback period.

    Returns:
        Float Series on df.index (first ``period`` bars are NaN).
    """
    high, low, prev_close = df["high"], df["low"], df["close"].shift(1)
    tr = pd.concat(
        [high - low, (high - prev_close).abs(), (low - prev_close).abs()],
        axis=1,
    ).max(axis=1)
    return tr.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()


# ── Legacy backward-compat function for hypothesis_tests/ infrastructure ──────

def compute_regime_signals(
    df_entry: pd.DataFrame,
    df_daily: pd.DataFrame,
    params: "Parameters",
) -> "dict[str, pd.Series]":
    """Compute EMA-based regime signals and map them onto the entry timeline.

    Preserved for backward compatibility with hypothesis_tests/ runners.
    New code should use compute_entry_signal() instead.
    """
    from bear_strategy.strategy.indicators.regime.ema_200 import compute_ema
    from bear_strategy.strategy.indicators.regime.ema_slope import compute_ema_slope_regime
    from bear_strategy.hypothesis_test_v2.engine.alignment import align_htf_to_ltf

    signal_cols: dict[str, pd.Series] = {}

    slope_col = f"ema_{params.ema_slope_period}_slope_regime"
    slope_raw = compute_ema_slope_regime(df_daily, params.ema_slope_period, params.ema_slope_lookback)
    signal_cols[slope_col] = align_htf_to_ltf(df_daily, slope_raw, df_entry, shift=True)

    for period in params.ema_below_periods:
        ema = compute_ema(df_daily, period)
        raw = (df_daily["close"] < ema).rename(f"ema_below_{period}_regime")
        signal_cols[f"ema_below_{period}_regime"] = align_htf_to_ltf(df_daily, raw, df_entry, shift=True)

    return signal_cols
