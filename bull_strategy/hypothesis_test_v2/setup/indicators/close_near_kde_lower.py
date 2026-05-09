"""
close_near_kde_lower — Setup indicator.

What it measures
----------------
Uses a rolling KDE to locate the lower-density peak — the price level where
the most closes have clustered BELOW the median (the demand / support zone).
Returns True when the current close is NEAR that lower peak from above.

This is the bull-strategy equivalent of the bear-strategy's
close_above_kde_upper: instead of looking for price near overhead supply
(for shorts), we look for price near underlying demand (for longs).

When price is near the lower KDE peak, it suggests:
  - Price is at a historically-tested demand zone.
  - The probability of a bounce / upward continuation is elevated.
  - This is a good location to start looking for a long entry trigger.

Parameters
----------
bandwidth : float
    KDE bandwidth as a fraction of the price range.  Default 0.15.
lookback_bars : int
    Rolling window of bars used to fit the KDE.  Default 200.

Signal contract
---------------
Returns a boolean Series (same index as df).
True  = close is within bandwidth of the rolling KDE lower peak.
False = close is not near the lower KDE peak, or warm-up bars.
"""

from __future__ import annotations

import pandas as pd

from bull_strategy.hypothesis_test_v2.setup.indicators.kde_lower import compute_kde_lower


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """
    Returns True on bars where close is within *bandwidth* of the rolling
    KDE lower peak (price at demand zone).

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

    peak = compute_kde_lower(df["close"], bandwidth=bandwidth, lookback_bars=lookback_bars)

    # True when close is within bandwidth-fraction of the lower KDE peak.
    proximity_threshold = bandwidth * df["close"]
    near_peak = (df["close"] - peak).abs() <= proximity_threshold

    return near_peak.fillna(False)
