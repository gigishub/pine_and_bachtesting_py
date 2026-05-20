"""Exit: Bollinger Bands mean reversion.

Mean reversion signal: when price was outside (below) the lower Bollinger Band
in the previous bar and has now closed inside the bands on the current bar,
it signals a return to fair value — exit the short position.

Definition
----------
  middle = SMA(close, bb_period)
  std = std(close, bb_period)
  upper = middle + bb_num_std × std
  lower = middle - bb_num_std × std

  Signal fires when:
    - close[t-1] < lower[t-1]  (previous close outside lower band)
    - lower[t] < close[t] < upper[t]  (current close inside bands)

Parameters used
---------------
  params.bb_period : SMA lookback for Bollinger Bands (default 20)
  params.bb_num_std : number of standard deviations (default 2.0)

Activated by
------------
  params.use_bb_mean_reversion_exit = True
"""

from __future__ import annotations

import pandas as pd

from bear_strategy.backtest.vectorbt.indicators import compute_bollinger_bands
from bear_strategy.strategy.parameters import Parameters

FLAG = "use_bb_mean_reversion_exit"


def compute(
    df_1h:      pd.DataFrame,
    df_1d:      pd.DataFrame,   # unused; kept for uniform signature
    funding_df: pd.DataFrame,   # unused; kept for uniform signature
    params:     Parameters,
) -> pd.Series:
    """Return True on 1h bars where BB mean reversion fires."""
    close = df_1h["close"].astype(float)
    
    # Compute Bollinger Bands
    middle, upper, lower = compute_bollinger_bands(
        close,
        period=params.bb_period,
        num_std=params.bb_num_std,
    )
    
    # Previous close outside lower band
    prev_below = (close.shift(1) < lower.shift(1)).fillna(False)
    
    # Current close inside bands
    curr_inside = ((close > lower) & (close < upper)).fillna(False)
    
    # Both conditions must be true
    return (prev_below & curr_inside).fillna(False)
