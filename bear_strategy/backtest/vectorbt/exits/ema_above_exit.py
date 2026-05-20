"""Exit: 1h close is above EMA(ema_above_period).

For a short position, price trading above the EMA signals the bearish
structure is broken — exit immediately.  Unlike the ema_reclaim_exit
(which requires a cross), this fires on every bar where close > EMA.

Parameters used
---------------
  params.ema_above_period : EMA lookback (default 20)

Activated by
------------
  params.use_ema_above_exit = True
"""

from __future__ import annotations

import pandas as pd

from bear_strategy.strategy.parameters import Parameters
from bear_strategy.backtest.vectorbt.indicators import compute_ema

FLAG = "use_ema_above_exit"


def compute(
    df_1h:      pd.DataFrame,
    df_1d:      pd.DataFrame,   # unused; kept for uniform signature
    funding_df: pd.DataFrame,   # unused; kept for uniform signature
    params:     Parameters,
) -> pd.Series:
    """Return True on 1h bars where close > EMA(ema_above_period)."""
    close = df_1h["close"].astype(float)
    ema   = compute_ema(close, int(params.ema_above_period))
    return (close > ema).fillna(False)
