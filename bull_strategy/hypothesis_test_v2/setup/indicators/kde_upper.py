"""
kde_upper — Setup indicator helper.

Computes a rolling Kernel Density Estimate of recent closing prices and
returns the upper-density peak price level — the price where the most closes
have clustered ABOVE the current median (the supply / resistance zone).

This module exposes compute_kde_upper() as a shared utility, and signal()
as the standard indicator interface.

signal() returns True when price is at or above the rolling KDE
upper peak — i.e., price is in a historically strong resistance zone, useful
for identifying rally exhaustion or resistance levels.

Parameters
----------
bandwidth : float
    KDE bandwidth as a fraction of the price range.  Default 0.15.
lookback_bars : int
    Rolling window of bars used to fit the KDE.  Default 200.

Signal contract
---------------
Returns a boolean Series (same index as df).
True  = current close is at or above the rolling KDE upper peak.
False = close is not at the upper KDE peak, or warm-up bars.
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

log = logging.getLogger(__name__)


def compute_kde_upper(
    closes: pd.Series,
    bandwidth: float = 0.15,
    lookback_bars: int = 200,
) -> pd.Series:
    """
    Rolling KDE upper-peak price level (supply/resistance zone).

    For each bar, fits a KDE on the previous *lookback_bars* closes, evaluates
    the density at 200 evenly-spaced price points, and returns the price where
    density is maximum ABOVE the median.

    Parameters
    ----------
    closes:        Series of closing prices.
    bandwidth:     Bandwidth as a fraction of [min, max] range in the window.
    lookback_bars: Rolling lookback length.

    Returns
    -------
    pd.Series of upper-peak prices (NaN during warm-up).
    """
    try:
        from scipy.stats import gaussian_kde
    except ImportError as exc:
        raise ImportError("scipy is required for kde_upper; install with: pip install scipy") from exc

    peaks = pd.Series(index=closes.index, dtype=float)

    for i in range(lookback_bars, len(closes)):
        window = closes.iloc[i - lookback_bars: i].dropna().values
        if len(window) < 10:
            continue

        price_range = window.max() - window.min()
        if price_range == 0:
            continue

        bw = bandwidth * price_range
        try:
            kde = gaussian_kde(window, bw_method=bw / window.std())
        except Exception:
            continue

        xs    = np.linspace(window.min(), window.max(), 200)
        dens  = kde(xs)
        median_price = np.median(window)

        # Upper peak: highest density point ABOVE the median.
        upper_mask = xs >= median_price
        if not upper_mask.any():
            continue
        peak_price = xs[upper_mask][np.argmax(dens[upper_mask])]
        peaks.iloc[i] = peak_price

    return peaks


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """
    Returns True when close is at or above the rolling KDE upper peak
    (price is at or above the resistance zone).

    Parameters
    ----------
    df:     OHLCV DataFrame with a 'close' column.
    params: {
        "bandwidth":     float (default 0.15),
        "lookback_bars": int   (default 200),
    }
    """
    bandwidth:     float = params.get("bandwidth",     0.15)
    lookback_bars: int   = params.get("lookback_bars", 200)

    upper_peak = compute_kde_upper(df["close"], bandwidth=bandwidth, lookback_bars=lookback_bars)

    # True when price is at or above the rolling KDE upper-peak (supply/resistance zone).
    return (df["close"] >= upper_peak).fillna(False)
