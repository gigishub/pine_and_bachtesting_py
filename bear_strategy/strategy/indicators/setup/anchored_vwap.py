"""Anchored VWAP indicator from confirmed swing highs.

Computes a cumulative VWAP anchored from the most recently confirmed
4H swing high.  Confirmation lag prevents lookahead: a bar at position i
is only declared a swing high once ``confirmation_bars`` subsequent bars
with strictly lower highs have been observed.

The shift-by-1 before 15m alignment is applied in the runner.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def compute_anchored_vwap(
    df_4h: pd.DataFrame,
    swing_lookback: int = 5,
    confirmation_bars: int = 3,
) -> pd.Series:
    """Return the Anchored VWAP from the most recently confirmed swing high.

    A swing high at bar ``i`` requires:
    - ``high[i]`` is strictly greater than all bars in
      ``high[i - swing_lookback : i]`` (left side)
    - ``high[i]`` is strictly greater than all bars in
      ``high[i + 1 : i + confirmation_bars + 1]`` (right side)

    Confirmation is available at bar ``i + confirmation_bars``.  The
    cumulative VWAP resets its anchor to ``i`` whenever a more recent
    swing high is confirmed.

    Returns NaN until the first swing high is confirmed.

    Args:
        df_4h: 4H OHLCV DataFrame with a DatetimeIndex.
        swing_lookback: Number of bars to the left for swing-high detection.
        confirmation_bars: Number of lower bars required on the right to
            confirm.

    Returns:
        pd.Series indexed like df_4h, named ``anchored_vwap``.
    """
    high = df_4h["High"].to_numpy(dtype=float)
    low = df_4h["Low"].to_numpy(dtype=float)
    close = df_4h["Close"].to_numpy(dtype=float)
    volume = df_4h["Volume"].to_numpy(dtype=float)
    n = len(df_4h)

    typical = (high + low + close) / 3.0
    cum_tp_vol = np.cumsum(typical * volume)
    cum_vol = np.cumsum(volume)

    # Pre-compute confirmed swing-high positions (True at the swing bar itself).
    # Only positions with enough left and right history qualify.
    swing_high_at = np.zeros(n, dtype=bool)
    for i in range(swing_lookback, n - confirmation_bars):
        left = high[i - swing_lookback : i]
        right = high[i + 1 : i + confirmation_bars + 1]
        if len(left) < swing_lookback or len(right) < confirmation_bars:
            continue
        if high[i] > left.max() and high[i] > right.max():
            swing_high_at[i] = True

    avwap = np.full(n, np.nan)
    anchor: int = -1

    for t in range(n):
        # A swing high at position (t - confirmation_bars) becomes known at bar t.
        swing_pos = t - confirmation_bars
        if 0 <= swing_pos < n and swing_high_at[swing_pos]:
            if anchor < swing_pos:
                anchor = swing_pos

        if anchor < 0:
            continue

        prev_tp_vol = cum_tp_vol[anchor - 1] if anchor > 0 else 0.0
        prev_vol = cum_vol[anchor - 1] if anchor > 0 else 0.0
        denom = cum_vol[t] - prev_vol
        if denom > 0:
            avwap[t] = (cum_tp_vol[t] - prev_tp_vol) / denom

    return pd.Series(avwap, index=df_4h.index, name="anchored_vwap")
