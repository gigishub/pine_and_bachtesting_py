"""Regime signal computation for the Bear Strategy.

Two types of regime signal are computed on daily data, then forward-filled
onto the 15-minute timeline via merge_asof (no lookahead):

  ema_{slope_period}_slope_regime  — True when EMA(slope_period) is declining
  ema_below_{p}_regime             — True when daily close < EMA(p)
"""

from __future__ import annotations

import pandas as pd

from bear_strategy.strategy.indicators.regime.ema_200 import compute_ema
from bear_strategy.strategy.indicators.regime.ema_slope import compute_ema_slope_regime
from bear_strategy.strategy.parameters import Parameters


def compute_regime_signals(
    df_15m: pd.DataFrame,
    df_daily: pd.DataFrame,
    params: Parameters,
) -> dict[str, pd.Series]:
    """Compute all regime signals and map them onto the 15-min timeline.

    Signals produced:
      - ``ema_{slope_period}_slope_regime``: EMA slope pointing down.
      - ``ema_below_{p}_regime`` for each p in params.ema_below_periods:
        daily close below that EMA.

    Args:
        df_15m: 15-minute OHLCV DataFrame with a DatetimeIndex or recognised
            timestamp column.
        df_daily: Daily OHLCV DataFrame with the same conventions.
        params: Strategy parameters.

    Returns:
        dict of boolean Series aligned to df_15m's index.
    """
    signal_cols: dict[str, pd.Series] = {}

    # EMA 200 slope signal
    slope_col = f"ema_{params.ema_slope_period}_slope_regime"
    signal_cols[slope_col] = compute_ema_slope_regime(
        df_daily, params.ema_slope_period, params.ema_slope_lookback
    )

    # Close-below-EMA signals
    for period in params.ema_below_periods:
        ema = compute_ema(df_daily, period)
        col = f"ema_below_{period}_regime"
        signal_cols[col] = (df_daily["Close"] < ema).rename(col)

    daily_signals = pd.DataFrame(signal_cols, index=df_daily.index)

    df_15m_ts = _ensure_datetime_index(df_15m)
    daily_ts = _ensure_datetime_index(daily_signals)

    merged = pd.merge_asof(
        df_15m_ts[[]],
        daily_ts,
        left_index=True,
        right_index=True,
        direction="backward",
    )

    return {
        col: merged[col].fillna(False).astype(bool)
        for col in signal_cols
    }


def _ensure_datetime_index(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of df with a sorted DatetimeIndex.

    Handles DataFrames where the datetime is stored in a column named
    'timestamp', 'Open time', or 'date' rather than in the index.
    """
    if isinstance(df.index, pd.DatetimeIndex):
        return df.sort_index()

    for col in ("timestamp", "Open time", "date", "Datetime"):
        if col in df.columns:
            return df.set_index(pd.to_datetime(df[col])).sort_index()

    raise ValueError(
        "DataFrame has no DatetimeIndex and no recognised timestamp column "
        "(expected one of: timestamp, 'Open time', date, Datetime)."
    )
