"""Exit signal package for the Bear Strategy vectorbt backtest.

Each exit is a separate module with a compute() function and a FLAG constant.
The EXIT_REGISTRY maps the Parameters flag name to its compute function.

Available exits
---------------
  use_rsi_exit            rsi_exit.py            Daily RSI crosses above exit level
  use_macd_exit           macd_exit.py           1h MACD histogram negative → ≥ 0
  use_rsi_oversold_exit   rsi_oversold_exit.py   1h RSI drops below oversold level
  use_ema_reclaim_exit    ema_reclaim_exit.py    1h close reclaims EMA (cross up)
  use_funding_exit        funding_exit.py        Smoothed funding drops ≤ threshold
  use_ema_above_exit      ema_above_exit.py      1h close above EMA(ema_above_period)
  use_vwap_exit           vwap_exit.py           1h close above anchor-period VWAP
  use_vwma_exit           vwma_exit.py           1h close above VWMA(vwma_period)
  use_engulfing_exit      engulfing_exit.py      Bullish engulfing candle on 1h
  use_hammer_exit         hammer_exit.py         Hammer candle on 1h
  use_bb_mean_reversion_exit  bb_mean_reversion_exit.py  BB mean reversion (price return)
  use_atr_reversal_exit   atr_reversal_exit.py   ATR reversal (vol compression)

Adding a new exit
-----------------
1.  Create exits/<name>_exit.py with:
      FLAG = "use_<name>_exit"
      def compute(df_1h, df_1d, funding_df, params) -> pd.Series[bool]: ...
2.  Add  use_<name>_exit: bool = False  to Parameters
    in bear_strategy/strategy/parameters.py.
3.  Register it in EXIT_REGISTRY below.
4.  Add the flag to BearGridConfig.boolean_filter_ranges
    in bear_strategy/backtest/vectorbt/bear_grid_config.py.
5.  Add the flag to _AUDITABLE_BEAR_FLAGS in bear_grid_config.py.
6.  Add the flag to _EXIT_FLAGS in pipeline.py.

Removing / disabling an exit
------------------------------
  - Temporary: set boolean_filter_ranges["use_<name>_exit"] = (False,) in the
    grid config — it is pinned off and never enters the grid.
  - Permanent: delete the exit file and remove it from EXIT_REGISTRY.
"""

from __future__ import annotations

from typing import Callable

import pandas as pd

from bear_strategy.strategy.parameters import Parameters

from . import (
    atr_reversal_exit,
    bb_mean_reversion_exit,
    ema_above_exit,
    ema_reclaim_exit,
    engulfing_exit,
    funding_exit,
    hammer_exit,
    macd_exit,
    rsi_exit,
    rsi_oversold_exit,
    vwap_exit,
    vwma_exit,
)

# ── Type alias ────────────────────────────────────────────────────────────────

ExitFn = Callable[
    [pd.DataFrame, pd.DataFrame, pd.DataFrame, Parameters],
    pd.Series,
]

# ── Registry — maps Parameters flag → exit compute function ──────────────────

EXIT_REGISTRY: dict[str, ExitFn] = {
    rsi_exit.FLAG:              rsi_exit.compute,
    macd_exit.FLAG:             macd_exit.compute,
    rsi_oversold_exit.FLAG:     rsi_oversold_exit.compute,
    ema_reclaim_exit.FLAG:      ema_reclaim_exit.compute,
    funding_exit.FLAG:          funding_exit.compute,
    ema_above_exit.FLAG:        ema_above_exit.compute,
    vwap_exit.FLAG:             vwap_exit.compute,
    vwma_exit.FLAG:             vwma_exit.compute,
    engulfing_exit.FLAG:        engulfing_exit.compute,
    hammer_exit.FLAG:           hammer_exit.compute,
    bb_mean_reversion_exit.FLAG: bb_mean_reversion_exit.compute,
    atr_reversal_exit.FLAG:     atr_reversal_exit.compute,
}


def build_exit_signal(
    df_1h:      pd.DataFrame,
    df_1d:      pd.DataFrame,
    funding_df: pd.DataFrame,
    params:     Parameters,
) -> pd.Series:
    """OR-compose all active indicator exits into a single bool Series.

    Returns a bool Series on df_1h.index.
    The trade exits on whichever active exit fires first.
    use_fixed_tp is NOT handled here — it controls tp_stop in build_vbt_arrays().
    """
    exits = pd.Series(False, index=df_1h.index, dtype=bool)
    for flag, fn in EXIT_REGISTRY.items():
        if getattr(params, flag, False):
            exits = exits | fn(df_1h, df_1d, funding_df, params)
    return exits.astype(bool)
