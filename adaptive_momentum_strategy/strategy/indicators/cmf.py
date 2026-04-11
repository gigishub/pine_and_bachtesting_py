"""CMF (Chaikin Money Flow) volume trigger.

CMF (Chaikin, 1980) measures the volume-weighted average of accumulation vs
distribution.  A value above zero means more volume is occurring on up-closes
than down-closes; a value above +0.05 indicates that aggressive buyers are
actively lifting the ask — confirming that the structural breakout has capital
backing and is not a thin-liquidity 'bull trap'.
"""

from __future__ import annotations

import pandas as pd
import pandas_ta as pta


def compute_cmf(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    volume: pd.Series,
    period: int = 20,
) -> pd.Series:
    """Return CMF oscillator (-1 to +1).

    Args:
        period: Lookback window.  20 bars is the standard; range 14–28.

    Returns:
        Float Series.  NaN for the first `period` bars.
    """
    result = pta.cmf(high, low, close, volume, length=period)
    if result is None:
        return pd.Series(float("nan"), index=close.index, dtype=float)
    return result.astype(float)


def trigger_is_active(cmf: pd.Series, threshold: float = 0.05) -> pd.Series:
    """True when CMF is above threshold (buyers confirmed)."""
    return (cmf > threshold).fillna(False)


def trigger_short_is_active(cmf: pd.Series, threshold: float = 0.05) -> pd.Series:
    """True when CMF is below -threshold (distribution confirmed).

    Args:
        threshold: Absolute value; the condition is cmf < -threshold.
                   Default 0.05 is the long-side threshold mirrored.
    """
    return (cmf < -threshold).fillna(False)
