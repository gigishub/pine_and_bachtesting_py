"""Exit: ATR reversal.

Volatility mean reversion signal: when ATR has been elevated (above N× moving
average) but then drops below that threshold, it signals volatility compression
and reduced downside pressure — exit the short position.

Definition
----------
  atr = Average True Range (Wilder smoothing)
  atr_ma = SMA(atr, atr_reversal_period)
  threshold = atr_ma × atr_reversal_mult

  Signal fires when:
    - atr[t-1] > threshold[t-1]  (previous ATR elevated)
    - atr[t] <= threshold[t]      (current ATR normalized)

Higher atr_reversal_mult (e.g. 2.0) requires ATR to be well above average
before it qualifies for reversal. Lower mult (e.g. 1.2) reacts to smaller
deviations.

Parameters used
---------------
  params.atr_reversal_mult : ATR threshold as multiple of SMA (default 1.5)
  params.atr_reversal_period : ATR and MA period (default 14)

Activated by
------------
  params.use_atr_reversal_exit = True
"""

from __future__ import annotations

import pandas as pd

from bear_strategy.backtest.vectorbt.indicators import compute_atr
from bear_strategy.strategy.parameters import Parameters

FLAG = "use_atr_reversal_exit"


def compute(
    df_1h:      pd.DataFrame,
    df_1d:      pd.DataFrame,   # unused; kept for uniform signature
    funding_df: pd.DataFrame,   # unused; kept for uniform signature
    params:     Parameters,
) -> pd.Series:
    """Return True on 1h bars where ATR reversal fires."""
    high = df_1h["high"].astype(float)
    low = df_1h["low"].astype(float)
    close = df_1h["close"].astype(float)
    
    # Compute ATR
    atr = compute_atr(high, low, close, period=params.atr_reversal_period)
    
    # ATR moving average (SMA)
    atr_ma = atr.rolling(params.atr_reversal_period).mean()
    
    # Threshold = ATR MA × multiplier
    threshold = atr_ma * params.atr_reversal_mult
    
    # Previous ATR was elevated
    prev_elevated = (atr.shift(1) > threshold.shift(1)).fillna(False)
    
    # Current ATR normalized
    curr_normalized = (atr <= threshold).fillna(False)
    
    # Both conditions must be true
    return (prev_elevated & curr_normalized).fillna(False)
