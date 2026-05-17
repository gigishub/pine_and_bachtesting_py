"""VBT signal adapter for the Bear Strategy.

ARCHITECTURE
------------
                 ┌──────────────────────────────────────┐
                 │  strategy/signals.py                 │
                 │  compute_atr()                       │  ← shared with backtesting.py
                 └──────────────┬───────────────────────┘
                                │
                    ┌───────────┼───────────┐
                    ▼           ▼           ▼
            entry/regime.py  entry/      exits/
            entry/triggers.py __init__.py __init__.py
             (always-on)     (build)     (registry)
                    └───────────┼───────────┘
                                │
                                ▼
                 ┌──────────────────────────────────────┐
                 │  vectorbt/signals.py  ← YOU ARE HERE │
                 │  build_vbt_arrays()                  │  converts to VBT format
                 └──────────────┬───────────────────────┘
                                │
                                ▼
                 ┌──────────────────────────────────────┐
                 │  vectorbt/runner.py                  │
                 │  run() → vbt.Portfolio               │
                 └──────────────────────────────────────┘

MODIFYING ENTRY / EXIT LOGIC
-----------------------------
  Add / change entry trigger  →  entry/triggers.py   (add function + register)
  Add / change exit            →  exits/<name>_exit.py (new file + register in exits/__init__.py)
  Change regime conditions     →  entry/regime.py
  Change indicator math        →  indicators.py

FILL MODEL
----------
entry_signal fires at bar N (computed from close[N]).
fill_at_next_open=True shifts arrays +1 so VBT fills at open[N+1].
sl_stop / tp_stop are also shifted so the ATR from signal bar N
governs the exit levels (consistent with the backtesting.py engine).

EXIT MODEL  (flag-driven OR logic)
----------
VBT sl_stop / tp_stop are fractions relative to the actual fill price:
  sl_stop[i] = stop_atr_mult  × ATR[i] / close[i]   → SHORT exits when price RISES by this fraction
  tp_stop[i] = target_atr_mult × ATR[i] / close[i]  → SHORT exits when price FALLS by this fraction

Each use_*_exit flag activates an indicator exit. Multiple active flags use OR logic —
the trade closes on whichever signal fires first. use_fixed_tp=False zeros tp_pct
(indicator-only exits, no hard TP stop).

MIN SL DISTANCE FILTER
-----------------------
Signals where sl_pct < params.min_sl_pct are masked out before shifting.

SIZING
------
  size_frac = risk_pct / sl_pct     (both dimensionless fractions)
Clipped to [0, 0.9999] so the position never exceeds available equity.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from bear_strategy.strategy.parameters import Parameters
from bear_strategy.strategy.signals import compute_atr

from bear_strategy.backtest.vectorbt.entry import build_entry_signal
from bear_strategy.backtest.vectorbt.exits import build_exit_signal


# ─────────────────────────────────────────────────────────────────────────────
# VBT-specific helper (not an indicator — throttling is a sampling concern)
# ─────────────────────────────────────────────────────────────────────────────

def _apply_entry_throttle(signal: pd.Series, every_n: int, phase: int) -> pd.Series:
    if every_n <= 1:
        return signal.fillna(False).astype(bool)
    if phase < 1 or phase > every_n:
        phase = 1
    sig = signal.fillna(False).astype(bool)
    hit_count = sig.cumsum()
    keep = sig & (((hit_count - phase) % every_n) == 0)
    return keep.astype(bool)


# ─────────────────────────────────────────────────────────────────────────────
# Main signal builder
# ─────────────────────────────────────────────────────────────────────────────

def build_vbt_arrays(
    df_1h: pd.DataFrame,
    df_1d: pd.DataFrame,
    funding_df: pd.DataFrame,
    params: Parameters,
    fill_at_next_open: bool = True,
) -> dict[str, pd.Series]:
    """Compute all arrays needed for vbt.Portfolio.from_signals().

    Args:
        df_1h:             1h OHLCV DataFrame (entry timeframe), lowercase columns.
        df_1d:             1d OHLCV DataFrame (regime timeframe), lowercase columns.
        funding_df:        Funding rate DataFrame with 'fundingrate' column.
        params:            Strategy parameters.
        fill_at_next_open: When True (default) shift arrays +1 bar so VBT fills
                           at the open of the bar after the signal.

    Returns:
        Dict with keys:
          short_entries — bool Series (entry bars)
          short_exits   — bool Series (indicator-based exits)
          sl_stop       — float Series (SL fraction relative to fill price)
          tp_stop       — float Series (TP fraction relative to fill price)
          short_size    — float Series (position size fraction of equity)
    """
    idx   = df_1h.index
    close = df_1h["close"].astype(float)

    entry_signal = build_entry_signal(df_1h, df_1d, funding_df, params)
    short_exits  = build_exit_signal(df_1h, df_1d, funding_df, params)
    atr          = compute_atr(df_1h, params.atr_period)

    # SL / TP as fractions of current close price
    safe_close = close.where(close > 0, np.nan)
    sl_pct = (params.stop_atr_mult  * atr / safe_close).fillna(0.0)
    tp_pct = (params.target_atr_mult * atr / safe_close).fillna(0.0)

    # When use_fixed_tp is False, disable the VBT TP stop so only indicator
    # exits and the SL govern exit timing.
    if not params.use_fixed_tp:
        tp_pct = pd.Series(0.0, index=idx, dtype=float)

    # Min-SL filter: skip when stop distance is too small vs price
    # (prevents trades dominated by taker fees)
    min_sl_mask = sl_pct >= params.min_sl_pct
    warmup_mask = atr.notna()

    short_entries = (entry_signal & warmup_mask & min_sl_mask).astype(bool)
    short_entries = _apply_entry_throttle(
        short_entries,
        every_n=max(int(params.entry_every_n), 1),
        phase=max(int(params.entry_phase), 1),
    )

    # ── Risk-based sizing: fraction of equity = risk_pct / sl_pct ─────────────
    raw_size = (
        params.risk_pct / sl_pct.replace(0.0, np.nan)
    ).clip(lower=0.0, upper=0.9999).fillna(0.0)

    # ── Shift everything +1 bar so VBT fills at the next open ─────────────────
    if fill_at_next_open:
        short_entries = short_entries.shift(1, fill_value=False)
        short_exits   = short_exits.shift(1, fill_value=False)
        sl_pct        = sl_pct.shift(1).fillna(0.0)
        tp_pct        = tp_pct.shift(1).fillna(0.0)
        raw_size      = raw_size.shift(1).fillna(0.0)

    return {
        "short_entries": pd.Series(short_entries.values, index=idx, dtype=bool),
        "short_exits":   pd.Series(short_exits.values,   index=idx, dtype=bool),
        "sl_stop":       pd.Series(sl_pct.values,        index=idx, dtype=float),
        "tp_stop":       pd.Series(tp_pct.values,        index=idx, dtype=float),
        "short_size":    pd.Series(raw_size.values,      index=idx, dtype=float),
    }
