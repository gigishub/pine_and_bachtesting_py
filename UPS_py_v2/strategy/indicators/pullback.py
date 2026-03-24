"""Pullback state-machine series for the UPS strategy.

Pure numpy loop — stateful bar-by-bar transitions.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def _pullback_bar_count(open_arr: np.ndarray, close_arr: np.ndarray, t: int, lookback: float, direction: int) -> int:
    if np.isnan(lookback) or lookback <= 0:
        return 0
    lb = int(lookback)
    c = 0
    for i in range(1, lb + 1):
        j = t - i
        if j < 0:
            continue
        if direction == 1 and close_arr[j] > open_arr[j]:
            c += 1
        if direction == -1 and close_arr[j] < open_arr[j]:
            c += 1
    return c


def compute_pullback_state_series(
    close: pd.Series,
    open_: pd.Series,
    high: pd.Series,
    low: pd.Series,
    ma1: pd.Series,
    lookback: int,
) -> dict[str, pd.Series]:
    n = len(close)
    close_arr = close.to_numpy(dtype=float)
    open_arr = open_.to_numpy(dtype=float)
    high_arr = high.to_numpy(dtype=float)
    low_arr = low.to_numpy(dtype=float)
    ma_arr = ma1.to_numpy(dtype=float)

    bullish_close_pb = np.full(n, np.nan, dtype=float)
    bullish_high_pb = np.full(n, np.nan, dtype=float)
    bullish_low_pb = np.full(n, np.nan, dtype=float)
    bearish_close_pb = np.full(n, np.nan, dtype=float)
    bearish_high_pb = np.full(n, np.nan, dtype=float)
    bearish_low_pb = np.full(n, np.nan, dtype=float)
    pb_lookback_bullish = np.full(n, np.nan, dtype=float)
    pb_lookback_bearish = np.full(n, np.nan, dtype=float)
    bullish_pb = np.zeros(n, dtype=bool)
    bearish_pb = np.zeros(n, dtype=bool)
    dbg_bullish_reset = np.zeros(n, dtype=bool)
    dbg_bullish_reinit = np.zeros(n, dtype=bool)
    dbg_bullish_high_set = np.zeros(n, dtype=bool)
    dbg_bullish_low_set = np.zeros(n, dtype=bool)

    b_close = np.nan
    b_high = np.nan
    b_low = np.nan
    s_close = np.nan
    s_high = np.nan
    s_low = np.nan
    last_low_eq_bearish_low = None
    last_high_eq_bullish_high = None

    for t in range(n):
        c = close_arr[t]
        o = open_arr[t]
        h = high_arr[t]
        l = low_arr[t]
        m = ma_arr[t]

        c1 = close_arr[t - 1] if t >= 1 else np.nan
        c2 = close_arr[t - 2] if t >= 2 else np.nan
        h1 = high_arr[t - 1] if t >= 1 else np.nan
        l1 = low_arr[t - 1] if t >= 1 else np.nan
        m1 = ma_arr[t - 1] if t >= 1 else np.nan
        m2 = ma_arr[t - 2] if t >= 2 else np.nan

        fixed_bullish_pb = _pullback_bar_count(open_arr, close_arr, t, lookback, 1) >= 2
        fixed_bearish_pb = _pullback_bar_count(open_arr, close_arr, t, lookback, -1) >= 2

        prev_b_high = b_high
        prev_s_low = s_low

        if not np.isnan(m) and c > m:
            if np.isnan(b_high) or h > b_high:
                b_high = h
                dbg_bullish_high_set[t] = True
            if c > b_close:
                b_close = c
            cond_low_reset = np.isnan(b_low) or l < b_low
            cond_pb = fixed_bearish_pb or (not np.isnan(l1) and l < l1 and c < o)
            if c > m and cond_low_reset and cond_pb:
                b_low = l
                dbg_bullish_low_set[t] = True
            if not np.isnan(prev_b_high) and c > prev_b_high:
                b_low = np.nan

        if (
            not np.isnan(m) and not np.isnan(m1) and not np.isnan(m2)
            and c < m and c1 < m1 and c2 > m2
        ):
            b_close = np.nan
            b_high = np.nan
            b_low = np.nan
            dbg_bullish_reset[t] = True

        if (
            not np.isnan(m) and not np.isnan(m1) and not np.isnan(m2)
            and c > m and c1 > m1 and c2 < m2
        ):
            b_close = c
            b_low = np.nan
            b_high = np.nan
            dbg_bullish_reinit[t] = True

        if not np.isnan(m) and c < m:
            if np.isnan(s_low) or l < s_low:
                s_low = l
            if c < s_close:
                s_close = c
            cond_high_reset = np.isnan(s_high) or h > s_high
            cond_pb = fixed_bullish_pb or (not np.isnan(h1) and h > h1 and c > o)
            if c < m and cond_high_reset and cond_pb:
                s_high = h
            if not np.isnan(prev_s_low) and c < prev_s_low:
                s_high = np.nan

        if (
            not np.isnan(m) and not np.isnan(m1) and not np.isnan(m2)
            and c > m and c1 > m1 and c2 < m2
        ):
            s_close = np.nan
            s_high = np.nan
            s_low = np.nan

        if (
            not np.isnan(m) and not np.isnan(m1) and not np.isnan(m2)
            and c < m and c1 < m1 and c2 > m2
        ):
            s_close = c
            s_high = np.nan
            s_low = np.nan

        bullish_close_pb[t] = b_close
        bullish_high_pb[t] = b_high
        bullish_low_pb[t] = b_low
        bearish_close_pb[t] = s_close
        bearish_high_pb[t] = s_high
        bearish_low_pb[t] = s_low

        if not np.isnan(s_low) and l == s_low:
            last_low_eq_bearish_low = t
        if not np.isnan(b_high) and h == b_high:
            last_high_eq_bullish_high = t

        lb_bull = (t - last_low_eq_bearish_low) if last_low_eq_bearish_low is not None else np.nan
        lb_bear = (t - last_high_eq_bullish_high) if last_high_eq_bullish_high is not None else np.nan
        pb_lookback_bullish[t] = lb_bull
        pb_lookback_bearish[t] = lb_bear

        bullish_pb[t] = _pullback_bar_count(open_arr, close_arr, t, lb_bull, 1) >= 2
        bearish_pb[t] = _pullback_bar_count(open_arr, close_arr, t, lb_bear, -1) >= 2

    idx = close.index
    return {
        "bullish_close_pb": pd.Series(bullish_close_pb, index=idx, dtype=float),
        "bullish_high_pb": pd.Series(bullish_high_pb, index=idx, dtype=float),
        "bullish_low_pb": pd.Series(bullish_low_pb, index=idx, dtype=float),
        "bearish_close_pb": pd.Series(bearish_close_pb, index=idx, dtype=float),
        "bearish_high_pb": pd.Series(bearish_high_pb, index=idx, dtype=float),
        "bearish_low_pb": pd.Series(bearish_low_pb, index=idx, dtype=float),
        "pb_lookback_bullish": pd.Series(pb_lookback_bullish, index=idx, dtype=float),
        "pb_lookback_bearish": pd.Series(pb_lookback_bearish, index=idx, dtype=float),
        "bullish_pb": pd.Series(bullish_pb, index=idx, dtype=bool),
        "bearish_pb": pd.Series(bearish_pb, index=idx, dtype=bool),
        "dbg_bullish_reset": pd.Series(dbg_bullish_reset, index=idx, dtype=bool),
        "dbg_bullish_reinit": pd.Series(dbg_bullish_reinit, index=idx, dtype=bool),
        "dbg_bullish_high_set": pd.Series(dbg_bullish_high_set, index=idx, dtype=bool),
        "dbg_bullish_low_set": pd.Series(dbg_bullish_low_set, index=idx, dtype=bool),
    }
