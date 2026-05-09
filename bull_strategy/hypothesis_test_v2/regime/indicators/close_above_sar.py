"""
close_above_sar — Regime indicator.

What it measures
----------------
True when the closing price is above the Parabolic SAR.  When price is above
SAR, the indicator is in bullish (uptrend) mode — the SAR dot is below price
and acts as a trailing stop for longs.

Parameters
----------
af_initial : float
    Initial acceleration factor.  Default 0.02.
af_step : float
    Increment applied each bar the extreme point advances.  Default 0.02.
af_max : float
    Maximum acceleration factor cap.  Default 0.20.

Signal contract
---------------
Returns a boolean Series (same index as df).
True  = close > SAR (bullish regime).
False = close <= SAR (bearish regime), or warm-up bars.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def _compute_sar(
    high: pd.Series,
    low: pd.Series,
    af_initial: float = 0.02,
    af_step: float = 0.02,
    af_max: float = 0.20,
) -> pd.Series:
    """
    Wilder Parabolic SAR.

    Returns a Series of SAR values.  Values on warm-up bars (first 2) are NaN.
    """
    highs = high.values
    lows  = low.values
    n     = len(highs)
    sar   = np.full(n, np.nan)

    # Initialise: assume bullish start
    bullish = True
    af      = af_initial
    ep      = highs[0]          # extreme point (highest high in uptrend)
    sar[0]  = lows[0]           # initial SAR below first bar

    for i in range(1, n):
        prev_sar = sar[i - 1]

        if bullish:
            sar[i] = prev_sar + af * (ep - prev_sar)
            # SAR must be below the two preceding lows
            sar[i] = min(sar[i], lows[i - 1])
            if i >= 2:
                sar[i] = min(sar[i], lows[i - 2])

            if lows[i] < sar[i]:
                # Flip to bearish
                bullish = False
                sar[i]  = ep          # SAR jumps to the highest high
                ep      = lows[i]
                af      = af_initial
            else:
                if highs[i] > ep:
                    ep = highs[i]
                    af = min(af + af_step, af_max)
        else:
            sar[i] = prev_sar - af * (prev_sar - ep)
            # SAR must be above the two preceding highs
            sar[i] = max(sar[i], highs[i - 1])
            if i >= 2:
                sar[i] = max(sar[i], highs[i - 2])

            if highs[i] > sar[i]:
                # Flip to bullish
                bullish = True
                sar[i]  = ep          # SAR jumps to the lowest low
                ep      = highs[i]
                af      = af_initial
            else:
                if lows[i] < ep:
                    ep = lows[i]
                    af = min(af + af_step, af_max)

    return pd.Series(sar, index=high.index)


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """Return True when close > Parabolic SAR (bullish regime)."""
    af_initial: float = float(params.get("af_initial", 0.02))
    af_step:    float = float(params.get("af_step",    0.02))
    af_max:     float = float(params.get("af_max",     0.20))

    sar = _compute_sar(df["high"], df["low"], af_initial, af_step, af_max)
    return (df["close"] > sar).fillna(False)
