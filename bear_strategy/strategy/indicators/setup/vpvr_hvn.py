"""VPVR high-volume node indicator for the Bear Strategy.

Computes the nearest High Volume Node (HVN) ABOVE each bar's close price
using a trailing window volume profile.  No lookahead: bar t uses bars
[t - window, t - 1] only.

Note: The HVN level is selected relative to bar t's own close.  When the
result is forward-filled onto the 15-minute grid (after a 1-bar shift in
the runner's alignment step), the actual 15-minute close is used for the
proximity check in entries.py — see entries.build_population_masks().
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def compute_vpvr_hvn(
    df_4h: pd.DataFrame,
    window: int = 200,
    n_bins: int = 50,
) -> pd.Series:
    """Return the nearest HVN above each 4H bar's close price.

    Uses a trailing window of ``window`` completed bars ending one bar before
    the current bar (i.e. bars [t - window, t - 1]).  Returns NaN for bars
    where the window is not yet full or where all volume sits at or below the
    current close.

    The shift-by-1 before 15m alignment is applied in the runner, not here,
    so that all 4H signals are shifted consistently in one place.

    Args:
        df_4h: 4H OHLCV DataFrame with a DatetimeIndex.
        window: Number of completed 4H bars in the trailing profile.
        n_bins: Price grid resolution for the histogram.

    Returns:
        pd.Series indexed like df_4h, named ``vpvr_hvn``.
    """
    high = df_4h["High"].to_numpy(dtype=float)
    low = df_4h["Low"].to_numpy(dtype=float)
    close = df_4h["Close"].to_numpy(dtype=float)
    volume = df_4h["Volume"].to_numpy(dtype=float)
    typical = (high + low + close) / 3.0
    n = len(df_4h)
    hvn = np.full(n, np.nan)

    for t in range(window, n):
        w_high = high[t - window : t]
        w_low = low[t - window : t]
        w_typical = typical[t - window : t]
        w_vol = volume[t - window : t]

        price_min = w_low.min()
        price_max = w_high.max()
        if (
            not np.isfinite(price_min)
            or not np.isfinite(price_max)
            or price_max <= price_min
        ):
            continue

        edges = np.linspace(price_min, price_max, n_bins + 1)
        vol_profile, _ = np.histogram(w_typical, bins=edges, weights=w_vol)
        mids = (edges[:-1] + edges[1:]) / 2.0

        ref_price = close[t]
        above = mids > ref_price
        if not above.any():
            continue

        above_idx = np.where(above)[0]
        best = above_idx[np.argmax(vol_profile[above_idx])]
        hvn[t] = mids[best]

    return pd.Series(hvn, index=df_4h.index, name="vpvr_hvn")
