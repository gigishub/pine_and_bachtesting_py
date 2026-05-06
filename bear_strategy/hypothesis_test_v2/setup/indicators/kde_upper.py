"""
kde_upper — Setup indicator.

What it measures
----------------
Uses a Kernel Density Estimate (KDE) of recent closing prices to locate the
upper-density peak — the price level where the most closes have clustered above
the current price.  When price is near this "supply ceiling", the probability
of resistance and a downward rejection is elevated.

Why KDE instead of a fixed level
---------------------------------
Support/resistance levels shift as the market evolves.  A rolling KDE adapts
to the recent distribution of closes, detecting where price has spent the most
time *above* current price — a proxy for overhead supply / resistance.

Important: this indicator uses the entry-timeframe close for the density
estimate by default (no HTF alignment required).  If you pass htf="4h", the
density peak is estimated on 4h closes and the result is compared against the
current LTF close — this requires the caller to align using alignment.py.

Parameters
----------
htf : str or None
    Higher timeframe to compute the density on, e.g. "4h".
    None → use the same timeframe as the input DataFrame.
    When htf is set, the runner must pass the HTF DataFrame separately and
    call compute_kde_peak() directly; the signal() function below assumes the
    DataFrame is already the target timeframe.

bandwidth : float
    KDE bandwidth as a fraction of the price range.  Default 0.15 (15%).
    Lower → tighter, more sensitive to local peaks.
    Higher → smoother, fewer but more robust peaks.

lookback_bars : int
    Rolling window of bars used to fit the KDE.  Default 200.
    More bars → more stable estimate; fewer → faster adaptation.

Signal contract
---------------
Returns a boolean Series (same index as df).
True  = current close is within *bandwidth* of the rolling KDE upper peak.
False = close is not near the KDE peak, or warm-up bars.
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

log = logging.getLogger(__name__)


def compute_kde_peak(
    closes: pd.Series,
    bandwidth: float = 0.15,
    lookback_bars: int = 200,
) -> pd.Series:
    """
    Rolling KDE upper-peak price level.

    For each bar, fits a KDE on the previous *lookback_bars* closes, evaluates
    the density at 200 evenly-spaced price points, and returns the price where
    density is maximum above the median.

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
    Returns True on bars where close is within *bandwidth* fraction of the
    rolling KDE upper peak (i.e., price is near overhead supply).

    Parameters
    ----------
    df:     OHLCV DataFrame with a 'close' column.
    params: {
        "htf":           str or None,
        "bandwidth":     float (default 0.15),
        "lookback_bars": int   (default 200),
    }

    Note: When htf is not None, this function expects df to already be
    the correct timeframe (i.e., the caller has handled HTF alignment externally).
    """
    bandwidth:     float = params.get("bandwidth",     0.15)
    lookback_bars: int   = params.get("lookback_bars", 200)

    peak = compute_kde_peak(df["close"], bandwidth=bandwidth, lookback_bars=lookback_bars)

    # True when price is within bandwidth-fraction of the KDE peak level.
    proximity_threshold = bandwidth * df["close"]
    near_peak = (peak - df["close"]).abs() <= proximity_threshold

    return near_peak.fillna(False)
