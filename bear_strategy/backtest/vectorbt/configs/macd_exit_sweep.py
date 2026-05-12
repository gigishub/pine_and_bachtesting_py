"""MACD histogram cross-zero exit sweep.

Purpose
-------
Test the ``macd_hist_cross_zero`` exit: cover the short when the 1h MACD
histogram crosses from negative to ≥ 0.  Bearish momentum is fading — take
profit early rather than riding out a potential reversal.

MACD params are fixed at the standard (12, 26, 9).  Only SL and TP multiples
are swept here.  Set ``macd_fast_period`` / ``macd_slow_period`` /
``macd_signal_period`` in ``default.py`` (or override in ``base``) to change
them globally.

Fixed TP is disabled for this mode — the SL is the only hard stop.

Lookahead guarantee
-------------------
hist[N] = f(close[0..N]) — computed from 1h bars known at bar N.
Cross: hist.shift(1) < 0 & hist >= 0 — uses bar N-1 and bar N only.
fill_at_next_open +1 → execute at open[N+1].  Zero lookahead.

What to look for
----------------
- Win-rate: MACD cross should exit more winners early vs fixed TP.
- Trade count: expect fewer trades than fixed_tp (some trades exit via SL
  before MACD signal fires).
- Compare avg trade duration — shorter = better capital efficiency.
- If PF < fixed_tp baseline, the MACD is cutting winners too early.

Usage
-----
    python -m bear_strategy.backtest.vectorbt.sweep_run --config macd_exit_sweep
"""

from __future__ import annotations

import dataclasses

from bear_strategy.backtest.vectorbt.configs.default import build_config
from bear_strategy.backtest.vectorbt.configs.sweep import SweepConfig


def build_sweep_config() -> SweepConfig:
    base = build_config()

    base = dataclasses.replace(
        base,
        start_date = "2021-01-01",
        end_date   = "2023-11-01",
        # MACD periods — standard defaults; adjust in default.py to change globally
        macd_fast_period   = 12,
        macd_slow_period   = 26,
        macd_signal_period = 9,
    )

    # Moderate SL grid — very tight stops rarely survive to the MACD signal
    sl_mults = (1.5, 2.0, 2.5, 3.0)
    tp_mults = (2.0, 3.0, 4.0, 5.0, 6.0)

    return SweepConfig(
        base       = base,
        sl_mults   = sl_mults,
        tp_mults   = tp_mults,
        exit_modes = ("macd_hist_cross_zero",),
        min_trades = 10,
    )
