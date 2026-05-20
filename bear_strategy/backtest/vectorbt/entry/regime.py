"""Always-on regime filter for the Bear Strategy entry signal.

Both conditions below are structural prerequisites — they are never toggled off.
The grid can sweep their numeric parameters but not their on/off state.

Conditions
----------
1. RSI bear zone (1d)
   Daily RSI is below the upper band and ideally cycling in the lower band.
   Implemented in bear_strategy/strategy/indicators/regime/rsi_bear_zone.py.

2. Funding bull guard (1h)
   EMA-smoothed 8h funding rate > funding_threshold.
   Positive funding means longs pay shorts — a tailwind for short positions.
   Guards against shorting when carry is adverse (extreme negative funding).
   Implemented in bear_strategy/strategy/indicators/regime/funding_bull_guard.py.

3. 200d EMA below filter  (optional — activated via params.use_ema_200_regime)
   Daily close must be below the 200-period daily EMA — confirms bearish macro
   structure before any entry is allowed.
"""

from __future__ import annotations

import pandas as pd

from bear_strategy.backtest.vectorbt.indicators import compute_ema
from bear_strategy.hypothesis_test_v2.engine.alignment import align_htf_to_ltf
from bear_strategy.strategy.indicators.regime.funding_bull_guard import compute_funding_bull_guard
from bear_strategy.strategy.indicators.regime.rsi_bear_zone    import compute_rsi_bear_zone
from bear_strategy.strategy.parameters import Parameters


def compute_regime_filter(
    df_1h:      pd.DataFrame,
    df_1d:      pd.DataFrame,
    funding_df: pd.DataFrame,
    params:     Parameters,
) -> pd.Series:
    """Return True on 1h bars where all regime conditions are satisfied.

    Parameters
    ----------
    df_1h       : 1h OHLCV DataFrame (entry timeframe).
    df_1d       : 1d OHLCV DataFrame (regime timeframe).
    funding_df  : 8h funding settlements with a 'fundingrate' column.
    params      : Strategy parameters.
    """
    # --- Condition 1: daily RSI bear zone ---
    rsi_1d = compute_rsi_bear_zone(
        df_1d,
        params.rsi_period,
        params.rsi_ma_period,
        params.rsi_lower,
        params.rsi_upper,
    )
    # align_htf_to_ltf(shift=True) maps the daily signal to the first 1h bar
    # after the daily bar closes — no lookahead.
    regime = align_htf_to_ltf(df_1d, rsi_1d, df_1h, shift=True)

    # --- Condition 2: funding bull guard ---
    funding = compute_funding_bull_guard(
        df_1h, funding_df, params.funding_threshold, params.funding_ma_period
    )

    regime = regime & funding

    # --- Condition 3: price below 200d EMA (optional) ---
    if params.use_ema_200_regime:
        ema_200 = compute_ema(df_1d["close"].astype(float), 200)
        below_ema = (df_1d["close"].astype(float) < ema_200)
        below_ema_1h = align_htf_to_ltf(df_1d, below_ema, df_1h, shift=True)
        regime = regime & below_ema_1h.fillna(False)

    return regime.fillna(False)
