"""vectorbt portfolio runner for the Bear Strategy.

ARCHITECTURE
------------
Inputs: df_1h, df_1d, funding_df (loaded by the caller)
  1. build_vbt_arrays()  → short_entries, sl_stop, tp_stop, short_size
  2. vbt.Portfolio.from_signals()

SHORT-ONLY MECHANICS
--------------------
Entry fills at the open of the bar AFTER the signal bar (fill_at_next_open=True).
VBT applies sl_stop / tp_stop fractions to the actual fill price (open[N+1]):
  • sl_stop triggers when price RISES by sl_pct above entry → covers the short
  • tp_stop triggers when price FALLS by tp_pct below entry → takes profit

This matches the hypothesis-test outcome engine which checks bar_high ≥ stop_price
and bar_low ≤ target_price on every bar after entry.

WHY fill_at_next_open?
----------------------
The entry signal is computed from bar N's close.  Filling at close of bar N would
require trading the last price of an already-closed bar — look-ahead in real-time.
Shifting +1 and using open[N+1] as fill price eliminates this bias, consistent with
the backtesting.py engine.
"""

from __future__ import annotations

import logging

import pandas as pd

from bear_strategy.strategy.parameters import Parameters
from .signals import build_vbt_arrays

log = logging.getLogger(__name__)


def run(
    df_1h: pd.DataFrame,
    df_1d: pd.DataFrame,
    funding_df: pd.DataFrame,
    params: Parameters | None = None,
    *,
    fees: float = 0.0008,
    init_cash: float = 10_000.0,
    fill_at_next_open: bool = True,
) -> "vbt.Portfolio":  # type: ignore[name-defined]
    """Run the Bear Strategy using vectorbt (short-only).

    Args:
        df_1h:             1h OHLCV DataFrame (entry timeframe), lowercase columns.
        df_1d:             1d OHLCV DataFrame (regime timeframe), lowercase columns.
        funding_df:        Funding rate DataFrame with 'fundingrate' column.
        params:            Strategy parameters. Defaults to Parameters().
        fees:              Round-trip commission fraction (e.g. 0.0008 = 0.08%).
        init_cash:         Starting cash in quote currency.
        fill_at_next_open: When True (default) fills execute at bar N+1 open.

    Returns:
        vbt.Portfolio — call .stats() or use metrics.extract_stats() for results.
    """
    import vectorbt as vbt  # lazy import — avoids numba JIT cost at module load

    p    = params or Parameters()
    arrs = build_vbt_arrays(df_1h, df_1d, funding_df, p, fill_at_next_open)

    fill_price = df_1h["open"].astype(float) if fill_at_next_open else df_1h["close"].astype(float)
    idx        = df_1h.index

    # Dummy long arrays — short-only strategy
    no_entries = pd.Series(False, index=idx, dtype=bool)

    freq = _infer_freq(df_1h)

    return vbt.Portfolio.from_signals(
        close        = fill_price,
        high         = df_1h["high"].astype(float),
        low          = df_1h["low"].astype(float),
        open         = df_1h["open"].astype(float),
        entries      = no_entries,
        exits        = no_entries,
        short_entries = arrs["short_entries"],
        short_exits   = arrs["short_exits"],
        # vbt 0.28.x has no separate short_size — a single `size` array applies
        # to whichever direction is active.  Since entries is all-False, size
        # only ever governs short positions.
        size          = arrs["short_size"],
        size_type     = "percent",
        sl_stop       = arrs["sl_stop"].values,
        tp_stop       = arrs["tp_stop"].values,
        fees          = fees,
        init_cash     = init_cash,
        upon_opposite_entry = "close",
        freq          = freq,
    )


def _infer_freq(df: pd.DataFrame) -> str | None:
    try:
        return pd.infer_freq(df.index)
    except Exception:
        log.debug("Could not infer frequency from DataFrame index.")
        return None
