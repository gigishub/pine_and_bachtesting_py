"""vectorbt portfolio runner for the Bear Strategy.

ARCHITECTURE
------------
Inputs: df_1h, df_1d, funding_df (loaded by the caller)
  1. build_vbt_arrays()  → short_entries, sl_stop, tp_stop, short_size
  2. Conditionally build entry-candle SL + optional trailing callback
  3. vbt.Portfolio.from_signals()

SHORT-ONLY MECHANICS
--------------------
Entry fills at the open of the bar AFTER the signal bar (fill_at_next_open=True).
VBT applies sl_stop / tp_stop fractions to the actual fill price (open[N+1]):
  • sl_stop triggers when price RISES by sl_pct above entry → covers the short
  • tp_stop triggers when price FALLS by tp_pct below entry → takes profit

SL MODES
--------
  use_vbt_sl=False  (default)
    ATR-fraction SL: stop_atr_mult × ATR / close — the original behaviour.

  use_vbt_sl=True, use_vbt_sl_trail=False
    Entry-candle SL: placed at candle_high + sl_n_atr_init × ATR(sl_atr_period).
    Hard stop for the life of the trade, tighter than the ATR-fraction SL.

  use_vbt_sl_trail=True  (works on top of EITHER SL mode above)
    Swing-high trailing ratchet via adjust_swing_sl_short_nb.
    Stop moves DOWN as price falls, locking in profits progressively.
    ATR reference: sl_atr_period when use_vbt_sl=True, atr_period otherwise.

⚠  VBT rejects adjust_sl_func_nb=None — never pass None directly.
   Always use the **sl_kwargs pattern to include the key only when set.
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

from bear_strategy.strategy.parameters import Parameters
from bear_strategy.strategy.signals import compute_atr
from bear_strategy.strategy.risk.stops import compute_entry_candle_sl_short
from bear_strategy.strategy.risk.stops_numba import adjust_swing_sl_short_nb
from .signals import build_vbt_arrays

log = logging.getLogger(__name__)


def run(
    df_1h: pd.DataFrame,
    df_1d: pd.DataFrame,
    funding_df: pd.DataFrame,
    params: Parameters | None = None,
    *,
    fees: float = 0.0011,
    init_cash: float = 10_000.0,
    fill_at_next_open: bool = True,
) -> "vbt.Portfolio":  # type: ignore[name-defined]
    """Run the Bear Strategy using vectorbt (short-only).

    Args:
        df_1h:             1h OHLCV DataFrame (entry timeframe), lowercase columns.
        df_1d:             1d OHLCV DataFrame (regime timeframe), lowercase columns.
        funding_df:        Funding rate DataFrame with 'fundingrate' column.
        params:            Strategy parameters. Defaults to Parameters().
        fees:              Round-trip commission fraction (e.g. 0.0011 = 0.11%).
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

    # ── SL stop array + optional trailing callback ────────────────────────────
    sl_kwargs = _build_sl_kwargs(df_1h, p, arrs, fill_at_next_open)

    return vbt.Portfolio.from_signals(
        close        = fill_price,
        high         = df_1h["high"].astype(float),
        low          = df_1h["low"].astype(float),
        open         = df_1h["open"].astype(float),
        entries      = no_entries,
        exits        = no_entries,
        short_entries = arrs["short_entries"],
        short_exits   = arrs["short_exits"],
        size          = arrs["short_size"],
        size_type     = "percent",
        tp_stop       = arrs["tp_stop"].values,
        fees          = fees,
        init_cash     = init_cash,
        upon_opposite_entry = "close",
        freq          = freq,
        **sl_kwargs,
    )


def _build_sl_kwargs(
    df_1h: pd.DataFrame,
    p: Parameters,
    arrs: dict,
    fill_at_next_open: bool,
) -> dict:
    """Build the sl_stop (and optional trailing) kwargs for from_signals().

    Returns a dict that is always non-empty — sl_stop is always present.
    adjust_sl_func_nb / adjust_sl_args are only added when use_vbt_sl_trail=True,
    because VBT raises an error if adjust_sl_func_nb=None is passed explicitly.

    use_vbt_sl_trail is independent of use_vbt_sl: trailing can be layered on top
    of either the classic ATR-fraction SL or the entry-candle SL.
    """
    high = df_1h["high"].astype(float)

    if p.use_vbt_sl:
        # Entry-candle SL: high[entry_bar] + sl_n_atr_init × ATR
        close  = df_1h["close"].astype(float)
        atr_sl = compute_atr(df_1h, p.sl_atr_period)
        sl_frac = compute_entry_candle_sl_short(high, close, atr_sl, p.sl_n_atr_init)
        if fill_at_next_open:
            sl_frac = sl_frac.shift(1).bfill()
        kwargs: dict = {"sl_stop": sl_frac.values}
    else:
        # Classic ATR-fraction SL from build_vbt_arrays
        kwargs = {"sl_stop": arrs["sl_stop"].values}
        # Use entry ATR as the ATR reference for trailing (same period as SL/TP)
        atr_sl = compute_atr(df_1h, p.atr_period)

    if p.use_vbt_sl_trail:
        # Rolling swing high (lookback bars) + ATR buffer — ratchets SL down.
        # Works on top of whichever initial SL mode is active.
        swing_high = high.rolling(p.sl_swing_lookback).max()
        # Fill leading NaN with the bar high so Numba sees a valid value
        swing_high = swing_high.fillna(high)
        atr_filled = atr_sl.fillna(0.0)

        # VBT Numba callbacks require 2D C-contiguous float64 arrays
        swing_high_2d = np.ascontiguousarray(swing_high.values.reshape(-1, 1))
        atr_2d        = np.ascontiguousarray(atr_filled.values.reshape(-1, 1))

        kwargs["adjust_sl_func_nb"] = adjust_swing_sl_short_nb
        kwargs["adjust_sl_args"]    = (swing_high_2d, atr_2d, float(p.sl_n_atr_trail))
        log.debug(
            "Trailing SL enabled: lookback=%d n_atr_trail=%.2f",
            p.sl_swing_lookback, p.sl_n_atr_trail,
        )

    return kwargs


def _infer_freq(df: pd.DataFrame) -> str | None:
    try:
        return pd.infer_freq(df.index)
    except Exception:
        log.debug("Could not infer frequency from DataFrame index.")
        return None
