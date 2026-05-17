"""Exit: 1h RSI drops below rsi_oversold_level.

When the 1h RSI crosses below the oversold level the short-side move is
exhausted — take profit before a bounce reverses the trade.

Parameters used
---------------
  params.exit_rsi_period      : RSI lookback period (default 14)
  params.rsi_oversold_level   : cross-down threshold (default 30.0)

Activated by
------------
  params.use_rsi_oversold_exit = True
"""

from __future__ import annotations

import pandas as pd

from bear_strategy.strategy.parameters import Parameters

from bear_strategy.backtest.vectorbt.indicators import compute_rsi

FLAG = "use_rsi_oversold_exit"


def compute(
    df_1h:      pd.DataFrame,
    df_1d:      pd.DataFrame,   # not used; kept for uniform signature
    funding_df: pd.DataFrame,   # not used; kept for uniform signature
    params:     Parameters,
) -> pd.Series:
    """Return True on 1h bars where the 1h RSI crosses below rsi_oversold_level."""
    period   = max(int(params.exit_rsi_period), 2)
    oversold = float(params.rsi_oversold_level)

    rsi_1h = compute_rsi(df_1h["close"].astype(float), period)
    # cross down: was ≥ oversold, now < oversold
    return ((rsi_1h.shift(1) >= oversold) & (rsi_1h < oversold)).fillna(False)
