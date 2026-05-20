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

ENTRY THROTTLE  (regime-aware, always active)
---------------------------------------------
The first trigger in each new regime window is skipped.
A new window begins each time the regime filter (daily RSI bear zone +
funding guard) transitions False→True.  When regime turns False the
counter resets so the next window starts fresh.

  Regime:   F F F T T T T F F T T T T T ...
  Trigger:      .   1 . 2 .   . 1 . 2 3 ...
  Entry:        .   - . ✓ .   . - . ✓ ✓ ...

The first trigger in each window (marked -) is discarded.

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

from bear_strategy.backtest.vectorbt.entry.regime import compute_regime_filter
from bear_strategy.backtest.vectorbt.entry.triggers import TRIGGER_REGISTRY
from bear_strategy.backtest.vectorbt.exits import build_exit_signal


# ─────────────────────────────────────────────────────────────────────────────
# Regime-aware entry throttle
# ─────────────────────────────────────────────────────────────────────────────

def _apply_regime_aware_throttle(
    trigger: pd.Series,
    regime: pd.Series,
    entry_offset: int = 2,
) -> pd.Series:
    """Start from the Nth trigger in each regime window; take all subsequent.

    A new window starts each time regime transitions False→True.
    Triggers before position N in that window are skipped (N=2 by default).
    When regime turns False the counter resets, so the next regime window
    starts fresh from zero.

    Args:
        trigger:      Boolean Series (True = signal fired)
        regime:       Boolean Series (True = regime active)
        entry_offset: Starting position (1=1st, 2=2nd, etc.)
                      Default 2 skips crowded entries.

    Vectorised implementation (no Python loop):
      1. Detect regime-start bars (False→True transitions) and assign
         a monotonically incrementing window-ID to every bar.
      2. Within each window, cumsum the active (regime & trigger) signals.
      3. Keep only bars where cumulative count ≥ entry_offset.
    """
    active = trigger.astype(bool) & regime.astype(bool)
    # Window ID increments each time regime turns ON
    regime_bool  = regime.astype(bool)
    regime_start = (~regime_bool.shift(1, fill_value=False)) & regime_bool
    window_id    = regime_start.cumsum()
    # Cumulative trigger count resets at the start of each new window
    cum_in_window = active.groupby(window_id).cumsum()
    return (active & (cum_in_window >= entry_offset)).astype(bool)



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

    Entry throttle  (configurable via entry_regime_offset parameter)
    ---------------------------------------------------------------
    A new window begins each time the regime filter transitions False→True
    (daily RSI bear zone + funding guard).  Within each window, entries
    start from the Nth trigger (default N=2).  When regime turns False the
    counter resets, so the next active window starts fresh.  N=1 takes all
    triggers; N=2 skips the first (crowded); N=3+ skip more.
    """
    idx   = df_1h.index
    close = df_1h["close"].astype(float)

    # Compute regime and raw trigger signal separately so the throttle
    # can see regime transitions independently of the combined signal.
    regime = compute_regime_filter(df_1h, df_1d, funding_df, params)

    raw_trigger = pd.Series(False, index=idx, dtype=bool)
    for flag, fn in TRIGGER_REGISTRY.items():
        if getattr(params, flag, False):
            raw_trigger = raw_trigger | fn(df_1h, df_1d, funding_df, params)

    short_exits = build_exit_signal(df_1h, df_1d, funding_df, params)
    atr         = compute_atr(df_1h, params.atr_period)

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

    # Regime-aware throttle: configurable starting position in each regime window
    throttled     = _apply_regime_aware_throttle(raw_trigger, regime, params.entry_regime_offset)
    short_entries = (throttled & warmup_mask & min_sl_mask).astype(bool)

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

