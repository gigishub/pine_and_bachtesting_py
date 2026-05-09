"""
close_above_kde_upper — Setup indicator.

What it measures
----------------
Uses a rolling Kernel Density Estimate of recent closes to locate the
upper-density peak — the price cluster where most supply is concentrated
above the median.  Fires when the current close is AT or ABOVE that level.

Why this is bearish
-------------------
When price rises into an overhead supply cluster it faces the highest
probability of rejection.  A close above the KDE upper peak means price
has reached the densest resistance zone in the recent lookback window —
a high-probability reversal point for short setups.

Parameters
----------
bandwidth : float
    KDE bandwidth as a fraction of the price range.  Default 0.15 (15%).
lookback_bars : int
    Rolling window of bars used to fit the KDE.  Default 200.

Signal contract
---------------
Returns a boolean Series (same index as df).
True  = close >= rolling KDE upper peak (price inside/above supply cluster).
False = close is below the KDE peak, or warm-up bars.
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

log = logging.getLogger(__name__)


def _compute_kde_upper_peak(
    closes: pd.Series,
    bandwidth: float,
    lookback_bars: int,
) -> pd.Series:
    """Return rolling KDE upper-peak price level (NaN during warm-up)."""
    try:
        from scipy.stats import gaussian_kde
    except ImportError as exc:
        raise ImportError(
            "scipy is required for close_above_kde_upper; install with: pip install scipy"
        ) from exc

    peaks = pd.Series(index=closes.index, dtype=float)

    for i in range(lookback_bars, len(closes)):
        window = closes.iloc[i - lookback_bars : i].dropna().values
        if len(window) < 10:
            continue

        price_range = window.max() - window.min()
        if price_range == 0:
            continue

        bw = bandwidth * price_range
        try:
            kde = gaussian_kde(window, bw_method=bw / window.std())
        except Exception:
            log.debug("KDE failed at bar %d — skipping", i)
            continue

        xs = np.linspace(window.min(), window.max(), 200)
        dens = kde(xs)
        median_price = float(np.median(window))

        upper_mask = xs >= median_price
        if not upper_mask.any():
            continue

        peak_price = xs[upper_mask][np.argmax(dens[upper_mask])]
        peaks.iloc[i] = peak_price

    return peaks


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """
    Return True when close >= rolling KDE upper peak.

    Parameters
    ----------
    df:     OHLCV DataFrame with a 'close' column.
    params: {
        "bandwidth":     float (default 0.15),
        "lookback_bars": int   (default 200),
    }
    """
    bandwidth: float = float(params.get("bandwidth", 0.15))
    lookback_bars: int = int(params.get("lookback_bars", 200))

    peak = _compute_kde_upper_peak(df["close"], bandwidth=bandwidth, lookback_bars=lookback_bars)

    # Bearish setup: price at or above the supply cluster peak.
    return (df["close"] >= peak).fillna(False)
