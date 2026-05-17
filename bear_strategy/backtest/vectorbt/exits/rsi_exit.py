"""Exit: daily RSI crosses above exit_rsi_level.

When daily RSI crosses above the exit level the bearish momentum is ending
— close the short before it reverses.

Parameters used
---------------
  params.exit_rsi_period   : RSI lookback period (default 14)
  params.exit_rsi_level    : cross-up threshold (default 50.0)

Activated by
------------
  params.use_rsi_exit = True
"""

from __future__ import annotations

import pandas as pd

from bear_strategy.hypothesis_test_v2.engine.alignment import align_htf_to_ltf
from bear_strategy.strategy.parameters import Parameters

from bear_strategy.backtest.vectorbt.indicators import compute_rsi

FLAG = "use_rsi_exit"


def compute(
    df_1h:      pd.DataFrame,
    df_1d:      pd.DataFrame,
    funding_df: pd.DataFrame,   # not used; kept for uniform signature
    params:     Parameters,
) -> pd.Series:
    """Return True on 1h bars where the daily RSI cross-up exit fires."""
    period = max(int(params.exit_rsi_period), 2)
    level  = float(params.exit_rsi_level)

    rsi_1d = compute_rsi(df_1d["close"].astype(float), period)
    # cross up: was ≤ level, now > level
    cross_1d = (rsi_1d.shift(1) <= level) & (rsi_1d > level)

    # Align the daily cross to the first 1h bar after the daily close (shift=True).
    return align_htf_to_ltf(df_1d, cross_1d.fillna(False), df_1h, shift=True).fillna(False)
