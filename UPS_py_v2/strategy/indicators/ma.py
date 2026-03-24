"""MA primitives and MA-context series for the UPS strategy.

Pure pandas/numpy functions — no side effects.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .atr import ind_atr


def ind_ema(close: pd.Series, length: int) -> pd.Series:
    """EMA with Pine-like warmup behaviour via min_periods."""
    return close.ewm(span=length, adjust=False, min_periods=length).mean()


def zen_bars_below_ma(close: pd.Series, ma: pd.Series, lookback: int) -> pd.Series:
    """Pine-equivalent of Zen barsBelowMA(lookback, ma)."""
    out = pd.Series(0, index=close.index, dtype=int)
    c_arr = close.to_numpy(dtype=float)
    m_arr = ma.to_numpy(dtype=float)
    for t in range(len(c_arr)):
        c = 0
        for i in range(1, lookback + 1):
            j = t - i
            if j < 0:
                continue
            if not np.isnan(c_arr[j]) and not np.isnan(m_arr[j]) and c_arr[j] < m_arr[j]:
                c += 1
        out.iat[t] = c
    return out


def zen_bars_above_ma(close: pd.Series, ma: pd.Series, lookback: int) -> pd.Series:
    """Pine-equivalent of Zen barsAboveMA(lookback, ma)."""
    out = pd.Series(0, index=close.index, dtype=int)
    c_arr = close.to_numpy(dtype=float)
    m_arr = ma.to_numpy(dtype=float)
    for t in range(len(c_arr)):
        c = 0
        for i in range(1, lookback + 1):
            j = t - i
            if j < 0:
                continue
            if not np.isnan(c_arr[j]) and not np.isnan(m_arr[j]) and c_arr[j] > m_arr[j]:
                c += 1
        out.iat[t] = c
    return out


def zen_bars_crossed_ma(open_: pd.Series, close: pd.Series, ma: pd.Series, lookback: int) -> pd.Series:
    """Pine-equivalent of Zen barsCrossedMA(lookback, ma)."""
    out = pd.Series(0, index=close.index, dtype=int)
    o_arr = open_.to_numpy(dtype=float)
    c_arr = close.to_numpy(dtype=float)
    m_arr = ma.to_numpy(dtype=float)
    for t in range(len(c_arr)):
        c = 0
        for i in range(1, lookback + 1):
            j = t - i
            if j < 0:
                continue
            o_j, c_j, m_j = o_arr[j], c_arr[j], m_arr[j]
            if np.isnan(o_j) or np.isnan(c_j) or np.isnan(m_j):
                continue
            crossed = (o_j > m_j and c_j < m_j) or (o_j < m_j and c_j > m_j)
            if crossed:
                c += 1
        out.iat[t] = c
    return out


def compute_base_and_ma_context(
    df: pd.DataFrame,
    ma_length: int,
    ma_breach_lookback: int,
    ma_consolidation_lookback: int,
    ma_consolidation_count: int,
    atr_length: int,
    atr_max_size: float,
) -> dict[str, pd.Series]:
    """Compute EMA, ATR, and all MA-context counter series for one DataFrame."""
    close = df["Close"].astype(float)
    open_ = df["Open"].astype(float)
    high = df["High"].astype(float)
    low = df["Low"].astype(float)

    ma1 = ind_ema(close, ma_length)
    atr_value = ind_atr(high, low, close, atr_length)
    price_above_ma = (close > ma1).fillna(False)
    atr_max_size_check = (atr_max_size == 0.0) | ((high - low).abs() <= (atr_value * atr_max_size))

    candles_below_ma = zen_bars_below_ma(close, ma1, ma_breach_lookback)
    candles_above_ma = zen_bars_above_ma(close, ma1, ma_breach_lookback)
    ma_cross_count = zen_bars_crossed_ma(open_, close, ma1, ma_consolidation_lookback)
    ma_cross_filter = ma_cross_count < ma_consolidation_count

    is_ready = ma1.notna() & atr_value.notna()

    return {
        "ma1": ma1,
        "atr_value": atr_value,
        "price_above_ma": price_above_ma,
        "atr_max_size_check": atr_max_size_check.fillna(False),
        "candles_below_ma": candles_below_ma,
        "candles_above_ma": candles_above_ma,
        "ma_cross_count": ma_cross_count,
        "ma_cross_filter": ma_cross_filter.fillna(False),
        "is_ready": is_ready.fillna(False),
    }
