"""EMA reclaim exit sweep (1h EMA).

Purpose
-------
Test the ``ema_reclaim`` exit: cover the short when the 1h close crosses
back ABOVE EMA(exit_ema_period).  The bearish price structure is broken —
exit now rather than holding against the trend.

Both the SL/TP grid and the EMA period are swept.  Shorter periods react
faster; longer periods filter out noise.

Fixed TP is disabled for this mode — the SL is the only hard stop.

Lookahead guarantee
-------------------
ema[N] = f(close[0..N]) — computed from 1h bars known at bar N.
Cross: close.shift(1) < ema.shift(1) & close >= ema — uses bar N-1 and bar N.
fill_at_next_open +1 → execute at open[N+1].  Zero lookahead.

What to look for
----------------
- Short EMA (e.g. 14): fires often, may cut winners early.
- Long EMA (e.g. 50): fires rarely, may hold too long vs fixed TP.
- Sweet spot is usually EMA(21) or EMA(34) for 1h crypto.
- Compare win-rate and avg winner vs ``is_broad`` (fixed_tp) baseline.

Usage
-----
    python -m bear_strategy.backtest.vectorbt.sweep_run --config ema_exit_sweep
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
    )

    sl_mults = (1.5, 2.0, 2.5, 3.0)
    tp_mults = (2.0, 3.0, 4.0, 5.0)

    # EMA periods: fast (14), standard (21), medium (34), slow (50)
    exit_ema_periods = (14, 21, 34, 50)

    return SweepConfig(
        base             = base,
        sl_mults         = sl_mults,
        tp_mults         = tp_mults,
        exit_modes       = ("ema_reclaim",),
        exit_ema_periods = exit_ema_periods,
        min_trades       = 10,
    )
