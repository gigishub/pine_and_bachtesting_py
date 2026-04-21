"""vectorbt portfolio runner for the Adaptive Momentum Strategy.

ARCHITECTURE
------------
                 ┌─────────────────────────────────┐
                 │  strategy/signals.py             │
                 │  compute_signals()               │  ← shared with backtesting.py engine
                 └──────────────┬──────────────────┘
                                │
                                ▼
                 ┌─────────────────────────────────┐
                 │  vectorbt/signals.py             │
                 │  build_vbt_arrays()              │  ← converts to vbt format
                 └──────────────┬──────────────────┘
                                │  (entries, exits, size)
                                ▼
                 ┌─────────────────────────────────┐
                 │  vectorbt/runner.py  ← YOU ARE HERE
                 │  run() → vbt.Portfolio           │
                 └──────────────┬──────────────────┘
                                │
                                ▼
                 ┌─────────────────────────────────┐
                 │  vectorbt/metrics.py             │
                 │  extract_stats() → pd.Series     │
                 └─────────────────────────────────┘

WHY fill_at_next_open?
-----------------------
Signals are computed from bar N's close.  Entering at close of bar N would be
look-ahead (the close is the last price of the bar — you cannot trade it in
real-time while the bar is still forming).  Shifting arrays forward by 1 bar
and using Open as the fill price matches backtesting.py's default behaviour
and eliminates the look-ahead bias.
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd
import pandas_ta as pta

from ...strategy.parameters import Parameters
from .signals import build_vbt_arrays

logger = logging.getLogger(__name__)


def run(
    df: pd.DataFrame,
    params: Parameters | None = None,
    *,
    fees: float = 0.001,
    init_cash: float = 10_000.0,
    fill_at_next_open: bool = True,
) -> "vbt.Portfolio":  # type: ignore[name-defined]
    """Run the Adaptive Momentum Strategy using vectorbt.

    Args:
        df:                OHLCV DataFrame with DatetimeIndex.
        params:            Strategy parameters. Defaults to Parameters().
        fees:              Round-trip commission (e.g. 0.001 = 0.1%).
        init_cash:         Starting cash.
        fill_at_next_open: When True (default), fills execute at the open of the
                           bar after the signal fires — matching backtesting.py.

    Returns:
        vbt.Portfolio
    """
    p = params or Parameters()
    arrs = build_vbt_arrays(df, p)
    freq = _infer_freq(df)

    import vectorbt as vbt  # lazy import — avoids numba JIT cost at module load

    # Build VBT-native SL arrays if enabled.
    # When use_vbt_sl=True, the entry-candle SL is registered with VBT
    # (sl_stop), and adjust_swing_sl_long/short_nb ratchets it inward each bar.
    # The precomputed long_exits / short_exits still fire for explicit strategy
    # exits (regime change, etc.) — VBT exits on whichever comes first.
    sl_stop_long = sl_stop_short = None
    adjust_sl_func_long = adjust_sl_func_short = None
    adjust_sl_args_long = adjust_sl_args_short = None

    if p.use_vbt_sl:
        from ...strategy.risk.stops import compute_entry_candle_sl
        from ...strategy.risk.stops_numba import (
            adjust_swing_sl_long_nb,
            adjust_swing_sl_short_nb,
        )

        raw_high  = df["High"].astype(float)
        raw_low   = df["Low"].astype(float)
        raw_close = df["Close"].astype(float)

        atr = pta.atr(raw_high, raw_low, raw_close, length=p.sl_atr_period)
        if atr is None:
            logger.warning("ATR returned None — skipping VBT SL (insufficient data).")
        else:
            sl_frac_long, sl_frac_short = compute_entry_candle_sl(
                raw_high, raw_low, raw_close, atr,
                n_atr_init=p.sl_n_atr_init,
            )

            # Shift fracs by 1 to align with the shifted entry signal
            if fill_at_next_open:
                sl_frac_long  = sl_frac_long.shift(1).bfill()
                sl_frac_short = sl_frac_short.shift(1).bfill()

            swing_low  = raw_low.rolling(p.sl_swing_lookback).min()
            swing_high = raw_high.rolling(p.sl_swing_lookback).max()

            # Numba requires 2D C-contiguous float64 arrays (bars × 1 for single symbol)
            swing_low_2d  = np.ascontiguousarray(swing_low.values.reshape(-1, 1))
            swing_high_2d = np.ascontiguousarray(swing_high.values.reshape(-1, 1))
            atr_2d        = np.ascontiguousarray(atr.values.reshape(-1, 1))

            sl_stop_long  = sl_frac_long.values
            sl_stop_short = sl_frac_short.values
            adjust_sl_func_long  = adjust_swing_sl_long_nb
            adjust_sl_func_short = adjust_swing_sl_short_nb
            adjust_sl_args_long  = (swing_low_2d,  atr_2d, p.sl_n_atr_trail)
            adjust_sl_args_short = (swing_high_2d, atr_2d, p.sl_n_atr_trail)

    if fill_at_next_open:
        long_entries  = arrs["long_entries"].shift(1, fill_value=False).astype(bool)
        long_exits    = arrs["long_exits"].shift(1, fill_value=False).astype(bool)
        long_size     = arrs["long_size"].shift(1, fill_value=0.0)
        short_entries = arrs["short_entries"].shift(1, fill_value=False).astype(bool)
        short_exits   = arrs["short_exits"].shift(1, fill_value=False).astype(bool)
        short_size    = arrs["short_size"].shift(1, fill_value=0.0)
        fill_price    = df["Open"].astype(float)
    else:
        long_entries  = arrs["long_entries"]
        long_exits    = arrs["long_exits"]
        long_size     = arrs["long_size"]
        short_entries = arrs["short_entries"]
        short_exits   = arrs["short_exits"]
        short_size    = arrs["short_size"]
        fill_price    = df["Close"].astype(float)

    # vbt from_signals() has a single `size` param for both directions.
    # Build a combined array: long_size at long entry bars, short_size at
    # short entry bars, 0 elsewhere.  Long takes precedence if somehow both
    # fire on the same bar (shouldn't happen due to mutual exclusion logic).
    combined_size = pd.Series(
        np.where(long_entries, long_size,
                 np.where(short_entries, short_size, 0.0)),
        index=long_entries.index,
    )

    # Only pass SL kwargs when the SL was successfully built — VBT rejects None.
    active_sl_stop  = sl_stop_long  if p.use_long else sl_stop_short
    active_sl_func  = adjust_sl_func_long  if p.use_long else adjust_sl_func_short
    active_sl_args  = adjust_sl_args_long  if p.use_long else adjust_sl_args_short

    sl_kwargs: dict = {}
    if active_sl_stop is not None and active_sl_func is not None:
        sl_kwargs = {
            "sl_stop":           active_sl_stop,
            "adjust_sl_func_nb": active_sl_func,
            "adjust_sl_args":    active_sl_args,
        }

    return vbt.Portfolio.from_signals(
        close=fill_price,
        high=df["High"].astype(float),
        low=df["Low"].astype(float),
        open=df["Open"].astype(float),
        entries=long_entries,
        exits=long_exits,
        short_entries=short_entries,
        short_exits=short_exits,
        size=combined_size,
        size_type="percent",
        fees=fees,
        init_cash=init_cash,
        upon_opposite_entry="close",
        freq=freq,
        **sl_kwargs,
    )


def _infer_freq(df: pd.DataFrame) -> str | None:
    try:
        return pd.infer_freq(df.index)
    except Exception:
        logger.debug("Could not infer frequency from DataFrame index.")
        return None
