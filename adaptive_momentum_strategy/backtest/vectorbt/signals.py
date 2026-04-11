"""vectorbt signal adapter for the Adaptive Momentum Strategy.

ARCHITECTURE
------------
backtesting.py runs bar-by-bar in Python (Strategy.next()).
vectorbt avoids that loop: you hand it numpy arrays and it simulates the whole
portfolio in a single compiled (numba) pass.

This module is the adapter between our strategy logic and vectorbt's API:
  1. Calls compute_signals() / compute_short_signals() — same functions as backtesting.py.
  2. Derives entry/exit bool arrays and per-bar position-size arrays.
  3. Supports long-only (use_long=True), short-only (use_short=True), or both.

KEY DIFFERENCE FROM backtesting.py
------------------------------------
In backtesting.py:
  - The chandelier/trailing_stop are *ratcheted* bar-by-bar inside next():
    the stop can only move UP for longs (DOWN for shorts) — never gives back gains.

In vectorbt:
  - We use `exits = close < stop_series` as a pre-computed exit signal.
  - The raw stop_series is generally monotone during trends but can fluctuate
    when ATR spikes — this is a known approximation.
  - The backtesting.py engine is the precise reference; vbt trades precision for
    speed (grid-search).

POSITION SIZING
---------------
  size_frac = risk_pct / 100 / stop_dist_pct
  where stop_dist_pct = |close - stop_series| / close

  Clipped to [0, 0.9999] to stay within available cash.
  size_type="percent" in from_signals() means fraction of available cash.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from ...strategy.parameters import Parameters
from ...strategy.signals import compute_signals
from ...strategy.short_signals import compute_short_signals


def build_vbt_arrays(
    df: pd.DataFrame,
    params: Parameters | None = None,
) -> dict[str, pd.Series]:
    """Build all arrays needed for vbt.Portfolio.from_signals().

    Returns a dict with keys:
      long_entries   - bool Series (long entry bars)
      long_exits     - bool Series (long exit bars)
      long_size      - float Series (long position size as fraction of cash)
      short_entries  - bool Series (short entry bars)   — all False if use_short=False
      short_exits    - bool Series (short cover bars)   — all False if use_short=False
      short_size     - float Series (short size)        — all 0.0 if use_short=False

    Args:
        df:     OHLCV DataFrame with DatetimeIndex and columns Open/High/Low/Close/Volume.
        params: Strategy parameters. Defaults to Parameters().
    """
    p = params or Parameters()
    idx = df.index
    close = df["Close"].astype(float)

    # ---- Long signals ---------------------------------------------------
    if p.use_long:
        sig = compute_signals(df, p)

        entries_raw = (
            sig["is_ready"].astype(bool)
            & sig["regime_filter"].astype(bool)
            & sig["setup_signal"].astype(bool)
            & sig["trigger_signal"].astype(bool)
        )
        long_entries = entries_raw.fillna(False).astype(bool)

        stop = sig["stop_series"]
        long_exits = (close < stop).fillna(False).astype(bool)

        long_size = _compute_size(close, stop, p.risk_pct)
    else:
        long_entries = pd.Series(False, index=idx, dtype=bool)
        long_exits   = pd.Series(False, index=idx, dtype=bool)
        long_size    = pd.Series(0.0,   index=idx, dtype=float)

    # ---- Short signals --------------------------------------------------
    if p.use_short:
        short_sig = compute_short_signals(df, p)

        short_entries_raw = (
            short_sig["short_is_ready"].astype(bool)
            & short_sig["short_regime_filter"].astype(bool)
            & short_sig["short_setup_signal"].astype(bool)
            & short_sig["short_trigger_signal"].astype(bool)
        )
        short_entries = short_entries_raw.fillna(False).astype(bool)

        short_stop = short_sig["short_stop_series"]
        # For shorts: exit (cover) when price RISES above the stop
        short_exits = (close > short_stop).fillna(False).astype(bool)

        short_size = _compute_size(close, short_stop, p.risk_pct)
    else:
        short_entries = pd.Series(False, index=idx, dtype=bool)
        short_exits   = pd.Series(False, index=idx, dtype=bool)
        short_size    = pd.Series(0.0,   index=idx, dtype=float)

    return {
        "long_entries":  pd.Series(long_entries.values,  index=idx, dtype=bool),
        "long_exits":    pd.Series(long_exits.values,    index=idx, dtype=bool),
        "long_size":     pd.Series(long_size.values,     index=idx, dtype=float),
        "short_entries": pd.Series(short_entries.values, index=idx, dtype=bool),
        "short_exits":   pd.Series(short_exits.values,   index=idx, dtype=bool),
        "short_size":    pd.Series(short_size.values,    index=idx, dtype=float),
        # Legacy keys — long arrays for backward compatibility with any existing callers
        "entries": pd.Series(long_entries.values, index=idx, dtype=bool),
        "exits":   pd.Series(long_exits.values,   index=idx, dtype=bool),
        "size":    pd.Series(long_size.values,     index=idx, dtype=float),
    }


def _compute_size(
    close: pd.Series,
    stop: pd.Series,
    risk_pct: float,
) -> pd.Series:
    """Compute position size as fraction of available cash based on stop distance."""
    safe_close = close.where(close > 0, np.nan)
    stop_dist_pct = (safe_close - stop).abs() / safe_close
    risk_frac = risk_pct / 100.0
    raw_size = risk_frac / stop_dist_pct.replace(0, np.nan)
    return raw_size.clip(lower=0.0, upper=0.9999).fillna(0.0)
