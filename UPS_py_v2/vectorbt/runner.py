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

from ..strategy.strategy_parameters import StrategySettings
from .signals import build_vbt_arrays

logger = logging.getLogger(__name__)


def run(
    df: pd.DataFrame,
    settings: StrategySettings | None = None,
    *,
    fees: float = 0.001,
    init_cash: float = 10_000.0,
) -> vbt.Portfolio:
    """Run the UPS strategy using vectorbt and return a Portfolio object.

    Args:
        df:        OHLCV DataFrame with DatetimeIndex and Open/High/Low/Close/Volume columns.
        settings:  Strategy parameters. Defaults to StrategySettings().
        fees:      Round-trip commission rate (e.g. 0.001 = 0.1 %).
        init_cash: Starting cash.

    Returns:
        vbt.Portfolio — call .stats() for metrics or .plot() for the chart.

    Note:
        trail_stop is silently ignored. Use UPS_py_v2.backtest for trailing stop support.
    """
    s = settings or StrategySettings()
    arrs = build_vbt_arrays(df, s)

    freq = _infer_freq(df)

    return vbt.Portfolio.from_signals(
        # Price data — vbt uses OHLC to check whether a stop is hit WITHIN a bar
        # (e.g. if high >= TP level the trade closes at TP even if close < TP).
        # This is more accurate than backtesting.py which only checks on close.
        close=df["Close"].astype(float),
        high=df["High"].astype(float),
        low=df["Low"].astype(float),
        open=df["Open"].astype(float),
        # Entry signals
        entries=arrs["entries"],               # long entry at True bars
        short_entries=arrs["short_entries"],   # short entry at True bars
        # Stop and target — fractions from entry price, set at the time of entry.
        # vbt anchors these to the actual fill price, not our pre-computed close.
        sl_stop=arrs["sl_stop"],
        tp_stop=arrs["tp_stop"],
        # Position sizing — fraction of available cash per trade.
        # Derived from risk_per_trade and the ATR stop distance (see signals.py).
        size=arrs["size"],
        size_type="percent",    # treat size as % of available cash (not $ amount)
        fees=fees,
        init_cash=init_cash,
        # When the opposite signal fires while a position is open, close it first.
        # Mirrors exclusive_orders=True in backtesting.py (no simultaneous long+short).
        upon_opposite_entry="close",
        freq=freq,              # needed for annualised metrics (Sharpe, Calmar, etc.)
    )


def _infer_freq(df: pd.DataFrame) -> str | None:
    """Attempt to infer the bar frequency from a DatetimeIndex."""
    try:
        return pd.infer_freq(df.index)
    except Exception:
        logger.debug("Could not infer frequency from DataFrame index.")
        return None
