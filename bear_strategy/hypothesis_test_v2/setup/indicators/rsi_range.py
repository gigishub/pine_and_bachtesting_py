"""
rsi_range — Setup indicator.

What it measures
----------------
Checks whether the RSI is inside a specific value band (between *low* and
*high*).  This is a "setup zone" filter rather than a momentum-reversal signal.

The intuition for shorts: entering when RSI is in the 40–65 range avoids
two unfavourable extremes:
  - RSI > 65  →  potentially overbought; could mean reversal UP not down.
  - RSI < 40  →  already oversold; risk of a bounce against the short.

A mid-range RSI suggests the price is in a "distribution zone" — neither
exhausted to the downside nor running away to the upside.

Parameters
----------
period : int
    RSI lookback in bars.  Standard value is 14.
    Higher → smoother, slower; Lower → noisier, faster reaction.

low : float
    Lower bound of the valid RSI band (inclusive).
    Default 40 keeps out deeply oversold conditions.

high : float
    Upper bound of the valid RSI band (inclusive).
    Default 65 keeps out strongly overbought conditions.

Signal contract
---------------
Returns a boolean Series (same index as df).
True  = RSI is in [low, high] → setup zone active.
False = RSI outside the band, or in warm-up (first `period` bars).
"""

from __future__ import annotations

import pandas as pd


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """
    Returns True on bars where RSI(period) is within [low, high].

    Parameters
    ----------
    df:     OHLCV DataFrame with a 'close' column.
    params: {"period": int, "low": float, "high": float}
    """
    period: int   = params["period"]
    low:    float = params["low"]
    high:   float = params["high"]

    delta  = df["close"].diff()
    gain   = delta.clip(lower=0).ewm(alpha=1 / period, adjust=False).mean()
    loss   = (-delta.clip(upper=0)).ewm(alpha=1 / period, adjust=False).mean()

    rs  = gain / loss.replace(0, float("nan"))
    rsi = 100 - (100 / (1 + rs))

    return ((rsi >= low) & (rsi <= high)).fillna(False)
