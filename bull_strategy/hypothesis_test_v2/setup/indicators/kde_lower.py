"""
kde_lower — Setup indicator helper.

Computes a rolling Kernel Density Estimate of recent closing prices and
returns the lower-density peak price level — the price where the most closes
have clustered BELOW the current median (the demand / support zone).

This module exposes compute_kde_lower() as a shared utility, and signal()
as the standard indicator interface.

signal() returns True when price is within *bandwidth* of the rolling KDE
lower peak — i.e., price is near a historically strong demand zone, a good
location for a long setup.

Parameters
----------
bandwidth : float
    KDE bandwidth as a fraction of the price range.  Default 0.15.
lookback_bars : int
    Rolling window of bars used to fit the KDE.  Default 200.

Signal contract
---------------
Returns a boolean Series (same index as df).
True  = current close is within bandwidth of the rolling KDE lower peak.
False = close is not near the lower KDE peak, or warm-up bars.
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

log = logging.getLogger(__name__)


def compute_kde_lower(
    closes: pd.Series,
    bandwidth: float = 0.15,
    lookback_bars: int = 200,
) -> pd.Series:
    """
    Rolling KDE lower-peak price level (demand zone).

    For each bar, fits a KDE on the previous *lookback_bars* closes, evaluates
    the density at 200 evenly-spaced price points, and returns the price where
    density is maximum BELOW the median.

    Parameters
    ----------
    closes:        Series of closing prices.
    bandwidth:     Bandwidth as a fraction of [min, max] range in the window.
    lookback_bars: Rolling lookback length.

    Returns
    -------
    pd.Series of lower-peak prices (NaN during warm-up).
    """
    try:
        from scipy.stats import gaussian_kde
    except ImportError as exc:
        raise ImportError("scipy is required for kde_lower; install with: pip install scipy") from exc

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

        # Lower peak: highest density point BELOW the median.
        lower_mask = xs <= median_price
        if not lower_mask.any():
            continue
        peak_price = xs[lower_mask][np.argmax(dens[lower_mask])]
        peaks.iloc[i] = peak_price

    return peaks


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """
    Returns True for the first *max_bars* bars where close is at or below
    the rolling KDE lower peak (price is entering the demand zone).

    Parameters
    ----------
    df:     OHLCV DataFrame with a 'close' column.
    params: {
        "bandwidth":     float (default 0.15),
        "lookback_bars": int   (default 200),
        "max_bars":      int   (default 5),
    }
    """
    bandwidth:     float = params.get("bandwidth",     0.15)
    lookback_bars: int   = params.get("lookback_bars", 200)
    max_bars:      int   = int(params.get("max_bars",  5))

    lower_peak = compute_kde_lower(df["close"], bandwidth=bandwidth, lookback_bars=lookback_bars)

    # True when price is at or below the rolling KDE lower-peak (demand zone).
    below_lower = (df["close"] < lower_peak).fillna(False)

    # Limit signal to the first max_bars consecutive bars in each run.
    run_id    = below_lower.ne(below_lower.shift()).cumsum()
    run_index = below_lower.groupby(run_id).cumcount()

    return (below_lower & (run_index < max_bars)).fillna(False)
