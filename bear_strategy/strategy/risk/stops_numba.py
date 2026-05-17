"""Numba-compiled SL adjustment callbacks for vectorbt from_signals().

Generic — identical to adaptive_momentum_strategy/strategy/risk/stops_numba.py.
Numba compiles these at first call (~1s JIT warm-up).

ARCHITECTURE
------------
VBT calls adjust_sl_func_nb() on every bar for each open position, BEFORE
checking whether the stop is hit.  Return (new_fraction, is_trailing).

SL FRACTION CONVENTION (VBT)
-----------------------------
  long : sl_fraction = (entry_price - sl_price) / entry_price
  short: sl_fraction = (sl_price   - entry_price) / entry_price

c.init_price is the actual fill price, not an approximation.

RATCHET DIRECTION
-----------------
For SHORTS: SL is above entry.  As price falls, rolling swing_high falls too,
so sl_price = swing_high + buffer decreases → new_frac decreases → SL tightens
(moves DOWN, closer to the falling price).  Only update when new_frac is smaller
(= tighter).
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
    """Ratchet long SL upward to swing_low[i] - n_atr × ATR[i]. Only tightens."""
    swing_low = swing_low_2d[c.i, c.col]
    atr_val   = atr_2d[c.i, c.col]

    sl_price = swing_low - n_atr_trail * atr_val
    if np.isnan(sl_price) or np.isnan(atr_val) or sl_price >= c.init_price:
        return c.curr_stop, c.curr_trail

    new_frac = (c.init_price - sl_price) / c.init_price
    new_frac = max(new_frac, 0.001)

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
    """Ratchet short SL downward to swing_high[i] + n_atr × ATR[i]. Only tightens.

    For shorts: SL is above entry.  As price falls, swing_high falls with it,
    pulling the stop down and locking in profits progressively.
    """
    swing_high = swing_high_2d[c.i, c.col]
    atr_val    = atr_2d[c.i, c.col]

    sl_price = swing_high + n_atr_trail * atr_val
    if np.isnan(sl_price) or np.isnan(atr_val) or sl_price <= c.init_price:
        return c.curr_stop, c.curr_trail

    new_frac = (sl_price - c.init_price) / c.init_price
    new_frac = max(new_frac, 0.001)

    if new_frac < c.curr_stop:
        return new_frac, False
    return c.curr_stop, c.curr_trail
