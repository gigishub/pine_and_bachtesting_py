"""Bear strategy class for the backtesting.py engine.

Precomputed signals (entry mask, ATR, and optional swing-high series) are
injected as class attributes before Backtest.run() so the framework never
touches raw multi-TF data or disk I/O directly.

Short trade mechanics
---------------------
- Entry:    self.sell() → fills at the next bar's open (standard bt.py).
- SL:       always set — entry close + stop_mult × ATR.  No trade without it.
- TP:       optional.  Active when use_fixed_tp=True (entry − target_mult × ATR).
            When False the trade runs until SL (possibly trailing) fires.
- Trail SL: optional.  When use_vbt_sl_trail=True the SL ratchets down each bar
            to rolling_swing_high + sl_n_atr_trail × ATR (only ever tightens).
- Sizing:   risk-based — risk ``risk_pct`` of current equity per trade.
            size = (equity × risk_pct) / (stop_mult × ATR)
- One trade at a time; new signals while in position are skipped.
"""

from __future__ import annotations

import numpy as np
from backtesting import Strategy


class BearStrategy(Strategy):
    # ── Injected by the runner (arrays match df length exactly) ──────────────
    _entry_signal: np.ndarray = None   # bool
    _atr:          np.ndarray = None   # float64
    # Precomputed rolling max of High over sl_swing_lookback bars.
    # Required when use_vbt_sl_trail=True; None otherwise.
    _swing_high:   np.ndarray = None   # float64 | None

    # ── Entry / sizing parameters ─────────────────────────────────────────────
    stop_mult:   float = 2.0
    target_mult: float = 3.0
    risk_pct:    float = 0.01
    min_sl_pct:  float = 0.005   # skip if SL distance / price < this

    # ── Exit flags ────────────────────────────────────────────────────────────
    # SL is always active.  At least one of these may be True in addition.
    use_fixed_tp:     bool  = True   # ATR-based fixed take-profit
    use_vbt_sl_trail: bool  = False  # swing-high trailing-SL ratchet

    # ── Trailing-SL parameters (used when use_vbt_sl_trail=True) ─────────────
    sl_n_atr_trail: float = 0.5   # ATR buffer above trailing swing high

    def init(self) -> None:
        self.entry = self.I(lambda: self.__class__._entry_signal, name="entry", plot=False)
        self.atr   = self.I(lambda: self.__class__._atr,          name="ATR",   plot=False)
        if self.__class__._swing_high is not None:
            self.swing_high = self.I(
                lambda: self.__class__._swing_high, name="SwingHigh", plot=False
            )

    def next(self) -> None:
        # Ratchet trailing SL before checking for new entries.
        if self.position and self.__class__.use_vbt_sl_trail:
            self._ratchet_trail_sl()

        if self.position:
            return  # remaining SL/TP orders managed automatically

        if not self.entry[-1]:
            return

        atr = float(self.atr[-1])
        if np.isnan(atr) or atr <= 0:
            return

        ref       = self.data.Close[-1]
        stop_dist = self.__class__.stop_mult * atr
        sl_price  = ref + stop_dist

        # Skip if stop distance is too small relative to price (fees dominate).
        if stop_dist / ref < self.__class__.min_sl_pct:
            return

        # Express size as a fraction of equity (backtesting.py fractional API).
        size = self.__class__.risk_pct * ref / stop_dist
        size = min(size, 0.99)
        if size <= 0:
            return

        if self.__class__.use_fixed_tp:
            tp_price = ref - self.__class__.target_mult * atr
            if tp_price <= 0:
                # Target below zero — price too low vs ATR, skip.
                return
            self.sell(size=size, sl=sl_price, tp=tp_price)
        else:
            # SL-only entry: trade runs until the hard SL (or trailing SL) fires.
            self.sell(size=size, sl=sl_price)

    def _ratchet_trail_sl(self) -> None:
        """Tighten the open short trade's SL toward the trailing swing high.

        The SL only ever moves down (toward price) — it never widens.
        """
        if not self.trades:
            return
        atr = float(self.atr[-1])
        if np.isnan(atr) or atr <= 0:
            return
        swing_high = float(self.swing_high[-1])
        if np.isnan(swing_high):
            return
        new_sl = swing_high + self.__class__.sl_n_atr_trail * atr
        trade = self.trades[-1]
        # Ratchet: only lower SL (never widen it back up).
        if new_sl < trade.sl:
            trade.sl = new_sl
