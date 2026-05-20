"""Shared low-level indicator helpers for the bear_strategy vectorbt backtest.

Pure functions: no I/O, no side-effects, no lookahead at bar N.
Used by both the entry/ and exits/ packages so they don't duplicate math.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def compute_rsi(close: pd.Series, period: int) -> pd.Series:
    """Wilder-smoothed RSI using EWM (alpha = 1/period)."""
    delta = close.diff()
    gain = delta.clip(lower=0).ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    loss = (-delta.clip(upper=0)).ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    rs = gain / loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def compute_macd_histogram(
    close: pd.Series,
    fast: int,
    slow: int,
    signal: int,
) -> pd.Series:
    """MACD histogram = (fast EMA − slow EMA) − signal EMA of that difference.

    All EMAs are causal (adjust=False) — no lookahead at bar N.
    """
    ema_fast    = close.ewm(span=fast,   adjust=False).mean()
    ema_slow    = close.ewm(span=slow,   adjust=False).mean()
    macd_line   = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    return macd_line - signal_line


def compute_ema(close: pd.Series, period: int) -> pd.Series:
    """Exponential Moving Average, causal (adjust=False)."""
    return close.ewm(span=period, adjust=False).mean()


def compute_vwap(df_1h: pd.DataFrame, anchor_hours: int = 24) -> pd.Series:
    """Anchor-period VWAP for 1h bars.

    Resets every ``anchor_hours`` hours.  Returns NaN on bars where cumulative
    volume is zero (first bar of a new window with no trades reported).

    Args:
        df_1h:        1h OHLCV DataFrame with a DatetimeIndex.
        anchor_hours: Window size in hours for VWAP reset.
                      24 = daily (default), 48 = 2-day, 168 = weekly.
    """
    typical = (df_1h["high"].astype(float) + df_1h["low"].astype(float) + df_1h["close"].astype(float)) / 3
    vol = df_1h["volume"].astype(float)
    # Assign each bar to an anchor window: floor-divide the hour-of-epoch
    hour_epoch = typical.index.view("int64") // (10 ** 9 * 3600)  # ns → hours
    window_id  = pd.Series(hour_epoch // anchor_hours, index=typical.index)
    tpv = typical * vol
    cum_tpv = tpv.groupby(window_id).cumsum()
    cum_vol = vol.groupby(window_id).cumsum()
    return (cum_tpv / cum_vol.replace(0, float("nan"))).rename("vwap")


def compute_vwma(df_1h: pd.DataFrame, period: int = 20) -> pd.Series:
    """Rolling Volume Weighted Moving Average (VWMA) for 1h bars.

    VWMA(n) = sum(close[i] × volume[i], n) / sum(volume[i], n)

    Bars with zero cumulative volume in the window return NaN.

    Args:
        df_1h:  1h OHLCV DataFrame.
        period: Rolling lookback in bars (default: 20).
    """
    close = df_1h["close"].astype(float)
    vol   = df_1h["volume"].astype(float)
    cum_cv  = (close * vol).rolling(period).sum()
    cum_vol = vol.rolling(period).sum()
    return (cum_cv / cum_vol.replace(0, float("nan"))).rename("vwma")


def compute_bollinger_bands(close: pd.Series, period: int = 20, num_std: float = 2.0) -> tuple[pd.Series, pd.Series, pd.Series]:
    """Bollinger Bands: middle (SMA), upper, lower.
    
    Args:
        close: Price series.
        period: SMA lookback (default 20).
        num_std: Number of standard deviations (default 2.0).
    
    Returns:
        (middle, upper, lower) tuple of Series.
    """
    middle = close.rolling(period).mean()
    std = close.rolling(period).std()
    upper = middle + (num_std * std)
    lower = middle - (num_std * std)
    return middle, upper, lower


def compute_atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
    """Average True Range using Wilder smoothing.
    
    Args:
        high, low, close: OHLC price series.
        period: ATR lookback (default 14).
    
    Returns:
        ATR series.
    """
    tr1 = high - low
    tr2 = (high - close.shift()).abs()
    tr3 = (low - close.shift()).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()


def get_smoothed_funding(
    funding_df: pd.DataFrame,
    target_index: pd.DatetimeIndex,
    ma_period: int,
) -> pd.Series:
    """Align 8h funding settlements to target_index and apply EMA smoothing.

    Returns the smoothed series WITHOUT any shift — the caller must apply
    whichever shift is appropriate for their use-case (entry guard vs exit).
    """
    rate = funding_df["fundingrate"].copy()
    fund_idx = pd.to_datetime(rate.index)
    fund_idx = (
        fund_idx.tz_localize("UTC") if fund_idx.tz is None else fund_idx.tz_convert("UTC")
    )
    rate.index = fund_idx

    tgt_utc = (
        target_index.tz_localize("UTC")
        if target_index.tz is None
        else target_index.tz_convert("UTC")
    )
    combined = rate.reindex(rate.index.union(tgt_utc)).ffill()
    result = combined.reindex(tgt_utc)
    result.index = target_index

    if ma_period > 1:
        result = result.ewm(span=ma_period, adjust=False).mean()
    return result
