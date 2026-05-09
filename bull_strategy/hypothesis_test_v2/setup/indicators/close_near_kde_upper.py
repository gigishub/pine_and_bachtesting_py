"""
close_near_kde_upper — Setup indicator.

What it measures
----------------
Uses a rolling KDE to locate the upper-density peak — the price level where
the most closes have clustered ABOVE the median (the supply / resistance zone).
Returns True when the current close is NEAR that upper peak from below.

When price is near the upper KDE peak, it suggests:
  - Price is at a historically-tested resistance zone.
  - The probability of rejection / downward reversal is elevated.
  - This is a good location to identify exhaustion or resistance levels.

Parameters
----------
bandwidth : float
    KDE bandwidth as a fraction of the price range.  Default 0.15.
lookback_bars : int
    Rolling window of bars used to fit the KDE.  Default 200.

Signal contract
---------------
Returns a boolean Series (same index as df).
True  = close is within bandwidth of the rolling KDE upper peak.
False = close is not near the upper KDE peak, or warm-up bars.
"""

from __future__ import annotations

import pandas as pd

from bull_strategy.hypothesis_test_v2.setup.indicators.kde_upper import compute_kde_upper


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """
    Returns True on bars where close is within *bandwidth* of the rolling
    KDE upper peak (price at resistance zone).

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

    peak = compute_kde_upper(df["close"], bandwidth=bandwidth, lookback_bars=lookback_bars)

    # True when close is within bandwidth-fraction of the upper KDE peak.
    proximity_threshold = bandwidth * df["close"]
    near_peak = (df["close"] - peak).abs() <= proximity_threshold

    return near_peak.fillna(False)
