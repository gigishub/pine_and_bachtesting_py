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
    )


def _infer_freq(df: pd.DataFrame) -> str | None:
    try:
        return pd.infer_freq(df.index)
    except Exception:
        logger.debug("Could not infer frequency from DataFrame index.")
        return None
