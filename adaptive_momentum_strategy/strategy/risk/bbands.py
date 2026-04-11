"""Bollinger Band exit indicator (Exit Option C).

In a strong trend, price 'walks' the outer Bollinger Band.  A close back
inside the upper band suggests the explosive phase is exhausted and a
consolidation or reversal is likely.

Mathematical rule:
    Exit when 1-hour Close < Upper Bollinger Band(period, std_dev)

The upper band serves as the dynamic stop level.  Like PSAR, this exit
should NOT be ratcheted — the runner applies the current upper band value
directly to the open trade each bar, letting the indicator self-manage.

Reference: Bollinger, J. (2001). Bollinger on Bollinger Bands.
"""

from __future__ import annotations

import pandas as pd
import pandas_ta as pta


def compute_bbands_upper(
    close: pd.Series,
    period: int = 20,
    std: float = 2.0,
) -> pd.Series:
    """Return the upper Bollinger Band as the dynamic exit level.

    Args:
        period: Rolling window for mean and standard deviation.
        std:    Number of standard deviations above the mean.
    """
    result = pta.bbands(close, length=period, std=std)
    if result is None or result.empty:
        return pd.Series(float("nan"), index=close.index, dtype=float)

    # pandas_ta names the upper column BBU_<period>_<std>
    upper_col = [c for c in result.columns if c.startswith("BBU")]
    if not upper_col:
        return pd.Series(float("nan"), index=close.index, dtype=float)

    return result[upper_col[0]].astype(float)


def compute_bbands_lower(
    close: pd.Series,
    period: int = 20,
    std: float = 2.0,
) -> pd.Series:
    """Return the lower Bollinger Band as the short exit level.

    For a short trade, a close back above the lower band suggests the
    distribution phase is exhausted — the short-side mirror of compute_bbands_upper().

    Args:
        period: Rolling window for mean and standard deviation.
        std:    Number of standard deviations below the mean.
    """
    result = pta.bbands(close, length=period, std=std)
    if result is None or result.empty:
        return pd.Series(float("nan"), index=close.index, dtype=float)

    lower_col = [c for c in result.columns if c.startswith("BBL")]
    if not lower_col:
        return pd.Series(float("nan"), index=close.index, dtype=float)

    return result[lower_col[0]].astype(float)
