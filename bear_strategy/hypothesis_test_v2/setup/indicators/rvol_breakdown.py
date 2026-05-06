"""
rvol_breakdown — Setup indicator (currently REJECTED / disabled).

What it measures
----------------
Relative volume (RVOL) breakdown: flags bars where the current volume is
significantly above the rolling average — indicating a surge of selling
activity that could accelerate a breakdown.

Why it was rejected
-------------------
On crypto data the volume spikes are highly noisy and occur in both
directions.  The RVOL threshold did not produce statistically meaningful lift
in PF over the regime-only baseline on BTCUSDT/ETHUSDT 15m–1h.

It remains here as a reference and can be re-enabled by changing
"decision": "REJECTED" → "PENDING" and "enabled": False → True in
setup/config.py IDEAS.

Parameters
----------
period : int
    Rolling average lookback for volume.  Default 20 bars.
    A larger period gives a more stable average; a smaller one reacts faster
    to recent volume shifts.

threshold : float
    Multiplier above average.  E.g. 2.0 means "volume is 2× the average".
    Higher → fewer but more extreme signals; lower → noisier.

Signal contract
---------------
Returns a boolean Series (same index as df).
True  = current volume > threshold × rolling_avg_volume.
False = volume is normal, or warm-up bars.
"""

from __future__ import annotations

import pandas as pd


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """
    Returns True on bars where volume exceeds threshold × rolling average.

    Parameters
    ----------
    df:     OHLCV DataFrame with a 'volume' column.
    params: {"period": int, "threshold": float}
    """
    period:    int   = params.get("period",    20)
    threshold: float = params.get("threshold", 2.0)

    avg_vol = df["volume"].rolling(period, min_periods=period).mean()
    return (df["volume"] > threshold * avg_vol).fillna(False)
