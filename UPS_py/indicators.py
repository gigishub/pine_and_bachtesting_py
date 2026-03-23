"""Indicator and Zen-equivalent counter helpers for UPS translation.

This module contains reusable, side-effect-free primitives.
Strategy orchestration stays in strategy_logic.py.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def ind_rma(series: pd.Series, length: int) -> pd.Series:
    """Pine-compatible RMA smoothing (used by ta.atr)."""
    return series.ewm(alpha=1.0 / float(length), adjust=False, min_periods=length).mean()


def ind_atr(high: pd.Series, low: pd.Series, close: pd.Series, length: int) -> pd.Series:
    """Pine-compatible ATR using True Range + RMA."""
    prev_close = close.shift(1)
    tr = pd.concat(
        [
            (high - low),
            (high - prev_close).abs(),
            (low - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)
    return ind_rma(tr, length)


def ind_ema(close: pd.Series, length: int) -> pd.Series:
    """EMA with Pine-like warmup behavior via min_periods."""
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
            c_j = c_arr[j]
            m_j = m_arr[j]
            if not np.isnan(c_j) and not np.isnan(m_j) and c_j < m_j:
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
            c_j = c_arr[j]
            m_j = m_arr[j]
            if not np.isnan(c_j) and not np.isnan(m_j) and c_j > m_j:
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
            o_j = o_arr[j]
            c_j = c_arr[j]
            m_j = m_arr[j]
            if np.isnan(o_j) or np.isnan(c_j) or np.isnan(m_j):
                continue
            crossed = (o_j > m_j and c_j < m_j) or (o_j < m_j and c_j > m_j)
            if crossed:
                c += 1
        out.iat[t] = c
    return out
