"""Bear strategy class for the backtesting.py engine.

Precomputed signals (entry mask and ATR series) are injected as class
attributes before Backtest.run() so the framework never touches raw
multi-TF data or disk I/O directly.

Short trade mechanics
---------------------
- Entry:    self.sell() → fills at the next bar's open (standard bt.py).
- SL/TP:    computed from signal-bar close + ATR so they scale with volatility.
- Sizing:   risk-based — risk ``risk_pct`` of current equity per trade.
            size = (equity × risk_pct) / (stop_mult × ATR)
- One trade at a time; new signals while in position are skipped.
"""

from __future__ import annotations

import numpy as np
from backtesting import Strategy


class BearStrategy(Strategy):
    # Injected by the runner (arrays match df length exactly).
    _entry_signal: np.ndarray = None  # bool
    _atr:          np.ndarray = None  # float64

    # Strategy parameters — overridden per pair via type() subclass.
    stop_mult:   float = 2.0
    target_mult: float = 3.0
    # Risk per trade as a fraction of current equity (e.g. 0.01 = 1 %).
    risk_pct:    float = 0.01

    def init(self) -> None:
        self.entry = self.I(lambda: self.__class__._entry_signal, name="entry", plot=False)
        self.atr   = self.I(lambda: self.__class__._atr,          name="ATR",   plot=False)

    def next(self) -> None:
        if self.position:
            return  # SL/TP orders are managed automatically by the framework

        if not self.entry[-1]:
            return

        atr = float(self.atr[-1])
        if np.isnan(atr) or atr <= 0:
            return

        ref          = self.data.Close[-1]
        stop_dist    = self.__class__.stop_mult * atr   # price distance to SL
        sl_price     = ref + stop_dist
        tp_price     = ref - self.__class__.target_mult * atr
        if tp_price <= 0:
            # Target would go below zero — skip this signal (price too low vs ATR).
            return

        # Express size as a fraction of equity (backtesting.py fractional API).
        # Fraction = risk_pct × price / stop_distance
        #   → fills (fraction × equity / price) units, which risks exactly risk_pct × equity.
        size = self.__class__.risk_pct * ref / stop_dist
        size = min(size, 0.99)  # cap at 99 % so we never exceed available equity
        if size <= 0:
            return

        self.sell(size=size, sl=sl_price, tp=tp_price)
