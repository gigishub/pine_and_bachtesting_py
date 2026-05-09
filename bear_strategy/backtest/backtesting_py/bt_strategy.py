"""Bear strategy class for the backtesting.py engine.

Precomputed signals (entry mask and ATR series) are injected as class
attributes before calling Backtest.run() so the framework never touches
raw multi-TF data or disk I/O directly.

Short trade mechanics:
  - Entry:  self.sell() → executes at the next bar's open.
  - Stop:   entry_close + stop_mult × ATR (price level).
  - Target: entry_close − target_mult × ATR (price level).
  - One trade at a time; new signal while in position is ignored.
"""

from __future__ import annotations

import numpy as np
from backtesting import Strategy


class BearStrategy(Strategy):
    # Injected by the runner before bt.run().  Arrays match df length exactly.
    _entry_signal: np.ndarray = None   # bool dtype
    _atr:          np.ndarray = None   # float64

    # Injected from Parameters; overridden per pair via type(...) subclass.
    stop_mult:   float = 2.0
    target_mult: float = 3.0
    trade_size:  float = 0.5   # fraction of margin capacity per trade

    def init(self) -> None:
        # Wrap precomputed arrays so backtesting.py tracks them correctly.
        self.entry = self.I(lambda: self.__class__._entry_signal, name="entry", plot=False)
        self.atr   = self.I(lambda: self.__class__._atr, name="ATR", plot=False)

    def next(self) -> None:
        if self.position:
            # Existing SL/TP orders managed automatically by the framework.
            return

        if not self.entry[-1]:
            return

        atr = self.atr[-1]
        if np.isnan(atr) or atr <= 0:
            return

        # SL/TP are computed from the signal-bar close so they scale with
        # volatility at signal time; actual entry fills at next bar open.
        ref = self.data.Close[-1]
        self.sell(
            size = self.__class__.trade_size,
            sl   = ref + self.stop_mult * atr,
            tp   = ref - self.target_mult * atr,
        )
