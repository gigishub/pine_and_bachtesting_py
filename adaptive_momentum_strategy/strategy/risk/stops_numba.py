"""Numba-compiled SL adjustment callbacks for vectorbt from_signals().

These functions are compiled by Numba at first use (JIT warm-up ~1s).
They are separate from stops.py (pandas) because Numba cannot call pandas.

ARCHITECTURE
------------
VBT calls adjust_sl_func_nb() on every bar per open position, BEFORE checking
whether the stop is hit.  The function returns a new (stop_fraction, is_trailing)
tuple.  The ratchet logic (only tighten, never loosen) is enforced here.

SL FRACTION CONVENTION
-----------------------
VBT stores `sl_stop` as a fraction of the initial (acquisition) price:
    long:  sl_fraction = (entry_price - sl_price) / entry_price
    short: sl_fraction = (sl_price   - entry_price) / entry_price

c.init_price is the ACTUAL fill price — not close-approximated.

USAGE IN runner.py
------------------
    pf = vbt.Portfolio.from_signals(
        ...
        sl_stop=sl_frac_long.values,         # initial fraction at entry bar
        adjust_sl_func_nb=adjust_swing_sl_long_nb,
        adjust_sl_args=(swing_low_2d, atr_2d, n_atr_trail),
    )

PARAMETERS PASSED VIA adjust_sl_args
--------------------------------------
    swing_low_2d  : np.ndarray, shape (n_bars, n_cols)  — rolling swing low prices
    atr_2d        : np.ndarray, shape (n_bars, n_cols)  — ATR values
    n_atr_trail   : float                               — ATR buffer multiplier
"""

from __future__ import annotations

import numpy as np
from numba import njit


@njit
def adjust_swing_sl_long_nb(
    c,
    swing_low_2d: np.ndarray,
    atr_2d: np.ndarray,
    n_atr_trail: float,
) -> tuple:
    """Ratchet the long SL upward to swing_low[i] - n_atr * ATR[i].

    Called by VBT on every bar for each open long position.
    SL can only tighten (move closer to price) — never loosen.

    Args:
        c:              AdjustSLContext with .i, .col, .init_price,
                        .curr_stop, .curr_trail, .position_now
        swing_low_2d:   Rolling swing lows, shape (n_bars, n_cols)
        atr_2d:         ATR values, shape (n_bars, n_cols)
        n_atr_trail:    Multiplier for ATR buffer below swing low

    Returns:
        (new_sl_fraction, is_trailing) — VBT uses these to update the stop.
    """
    swing_low = swing_low_2d[c.i, c.col]
    atr_val = atr_2d[c.i, c.col]

    # Proposed SL price: last swing low minus ATR buffer
    sl_price = swing_low - n_atr_trail * atr_val

    # Guard: SL must be below entry price; NaN means not enough history yet
    if np.isnan(sl_price) or np.isnan(atr_val) or sl_price >= c.init_price:
        return c.curr_stop, c.curr_trail

    # Convert absolute SL price to fraction of entry price
    new_frac = (c.init_price - sl_price) / c.init_price
    new_frac = max(new_frac, 0.001)   # floor: 0.1% minimum SL distance

    # Ratchet: smaller fraction = tighter SL; only update if tightening
    if new_frac < c.curr_stop:
        return new_frac, False
    return c.curr_stop, c.curr_trail


@njit
def adjust_swing_sl_short_nb(
    c,
    swing_high_2d: np.ndarray,
    atr_2d: np.ndarray,
    n_atr_trail: float,
) -> tuple:
    """Ratchet the short SL downward to swing_high[i] + n_atr * ATR[i].

    Called by VBT on every bar for each open short position.
    SL can only tighten (move closer to price) — never loosen.

    Args:
        c:               AdjustSLContext with .i, .col, .init_price,
                         .curr_stop, .curr_trail, .position_now
        swing_high_2d:   Rolling swing highs, shape (n_bars, n_cols)
        atr_2d:          ATR values, shape (n_bars, n_cols)
        n_atr_trail:     Multiplier for ATR buffer above swing high

    Returns:
        (new_sl_fraction, is_trailing)
    """
    swing_high = swing_high_2d[c.i, c.col]
    atr_val = atr_2d[c.i, c.col]

    # Proposed SL price: last swing high plus ATR buffer
    sl_price = swing_high + n_atr_trail * atr_val

    # Guard: SL must be above entry price for shorts
    if np.isnan(sl_price) or np.isnan(atr_val) or sl_price <= c.init_price:
        return c.curr_stop, c.curr_trail

    # For shorts: SL is above entry; fraction = (sl_price - entry) / entry
    new_frac = (sl_price - c.init_price) / c.init_price
    new_frac = max(new_frac, 0.001)

    # Ratchet: smaller fraction = tighter SL (SL moves down toward price)
    if new_frac < c.curr_stop:
        return new_frac, False
    return c.curr_stop, c.curr_trail
