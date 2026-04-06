"""vectorbt portfolio runner for the UPS strategy.

HOW IT FITS INTO THE ARCHITECTURE
----------------------------------
                 ┌─────────────────────────────────┐
                 │  strategy/signals.py             │
                 │  build_strategy_series()         │  ← shared with backtesting.py engine
                 └──────────────┬──────────────────┘
                                │  (entry signals as bool Series)
                                ▼
                 ┌─────────────────────────────────┐
                 │  vectorbt/signals.py             │
                 │  build_vbt_arrays()              │  ← converts to vbt format
                 └──────────────┬──────────────────┘
                                │  (entries, sl_stop, tp_stop, size)
                                ▼
                 ┌─────────────────────────────────┐
                 │  vectorbt/runner.py  ← YOU ARE HERE
                 │  run() → vbt.Portfolio           │
                 └──────────────┬──────────────────┘
                                │
                                ▼
                 ┌─────────────────────────────────┐
                 │  vectorbt/metrics.py             │
                 │  extract_stats() → pd.Series     │  ← pipeline-compatible output
                 └─────────────────────────────────┘

WHY vbt.Portfolio.from_signals()?
----------------------------------
from_signals() is the simplest vbt simulation mode:
  - You supply entry/exit boolean arrays + stop parameters.
  - vbt handles the simulation loop internally in compiled (numba) code.
  - The result is identical to from_order_func() for fixed SL/TP strategies,
    but requires far less boilerplate.

from_order_func() would be needed only for dynamic per-bar logic such as trailing
stops — which are explicitly out of scope for this engine path.
"""

from __future__ import annotations

import logging

import pandas as pd
import vectorbt as vbt

from ...strategy.strategy_parameters import StrategySettings
from .signals import build_vbt_arrays

logger = logging.getLogger(__name__)


def run(
    df: pd.DataFrame,
    settings: StrategySettings | None = None,
    *,
    fees: float = 0.001,
    init_cash: float = 10_000.0,
    fill_at_next_open: bool = True,
) -> vbt.Portfolio:
    """Run the UPS strategy using vectorbt and return a Portfolio object.

    Args:
        df:                OHLCV DataFrame with DatetimeIndex and columns Open/High/Low/Close/Volume.
        settings:          Strategy parameters. Defaults to StrategySettings().
        fees:              Round-trip commission rate (e.g. 0.001 = 0.1 %).
        init_cash:         Starting cash.
        fill_at_next_open: When True (default), entries are filled at the **open of the bar
                           after the signal fires** — matching backtesting.py behaviour and
                           avoiding look-ahead bias.  When False, entries fill at the close
                           of the signal bar (vectorbt's default).

    Returns:
        vbt.Portfolio — call .stats() for metrics or .plot() for the chart.

    Note:
        trail_stop is silently ignored. Use the backtesting_py engine for trailing stop support.
    """
    s = settings or StrategySettings()
    arrs = build_vbt_arrays(df, s)

    freq = _infer_freq(df)

    if fill_at_next_open:
        # Shift all per-signal arrays forward by 1 bar so that vbt "sees" the
        # signal on bar N+1 (the fill bar) rather than bar N (the signal bar).
        # We also replace the close price fed to vbt with Open so that the fill
        # price becomes the open of the fill bar — exactly what backtesting.py does.
        #
        # sl_stop / tp_stop / size are computed from bar N's ATR; shifting them
        # forwards applies those same values on bar N+1 where the fill happens.
        # vbt anchors sl/tp percentages to the actual fill price automatically.
        entries       = arrs["entries"].shift(1, fill_value=False).astype(bool)
        short_entries = arrs["short_entries"].shift(1, fill_value=False).astype(bool)
        sl_stop       = arrs["sl_stop"].shift(1, fill_value=0.0)
        tp_stop       = arrs["tp_stop"].shift(1, fill_value=0.0)
        size          = arrs["size"].shift(1, fill_value=0.0)
        fill_price    = df["Open"].astype(float)   # fill at open of the fill bar
    else:
        entries       = arrs["entries"]
        short_entries = arrs["short_entries"]
        sl_stop       = arrs["sl_stop"]
        tp_stop       = arrs["tp_stop"]
        size          = arrs["size"]
        fill_price    = df["Close"].astype(float)  # fill at close of signal bar

    return vbt.Portfolio.from_signals(
        # Price data.  vbt uses OHLC to check whether a stop is hit WITHIN a bar
        # (if high >= TP level the trade closes at TP even when close < TP).
        # close is also the fill price, so we swap it for Open when fill_at_next_open.
        close=fill_price,
        high=df["High"].astype(float),
        low=df["Low"].astype(float),
        open=df["Open"].astype(float),
        entries=entries,
        short_entries=short_entries,
        sl_stop=sl_stop,
        tp_stop=tp_stop,
        # Fraction of available cash per trade (derived from risk_per_trade + ATR stop).
        size=size,
        size_type="percent",
        fees=fees,
        init_cash=init_cash,
        # Close any open position before entering the opposite direction —
        # mirrors exclusive_orders=True in backtesting.py.
        upon_opposite_entry="close",
        freq=freq,
    )


def _infer_freq(df: pd.DataFrame) -> str | None:
    """Attempt to infer the bar frequency from a DatetimeIndex."""
    try:
        return pd.infer_freq(df.index)
    except Exception:
        logger.debug("Could not infer frequency from DataFrame index.")
        return None
