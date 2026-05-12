"""RSI oversold exit sweep (1h RSI).

Purpose
-------
Test the ``rsi_oversold`` exit: cover the short when the 1h RSI drops BELOW
``rsi_oversold_level``.  The short-side move is exhausted — take profit
before the bounce.

Both the SL/TP grid and the oversold threshold are swept.  RSI period is
fixed at ``exit_rsi_period`` (default 14 in default.py).

Fixed TP is disabled for this mode — the SL is the only hard stop.

Lookahead guarantee
-------------------
rsi_1h[N] = f(close[0..N]) — computed from 1h bars known at bar N.
Cross: rsi.shift(1) >= level & rsi < level — uses bar N-1 and bar N only.
fill_at_next_open +1 → execute at open[N+1].  Zero lookahead.

What to look for
----------------
- Lower oversold levels (e.g. 25) = fewer exits, higher avg winner.
- Higher oversold levels (e.g. 40) = more exits, potentially more losers cut.
- Compare avg trade duration across levels — the exit should be timelier than
  fixed TP when the market is genuinely oversold.
- If exits fire too rarely (< 20 % of trades), the level may be too tight.

Usage
-----
    python -m bear_strategy.backtest.vectorbt.sweep_run --config rsi_oversold_sweep
"""

from __future__ import annotations

import dataclasses

from bear_strategy.backtest.vectorbt.configs.default import build_config
from bear_strategy.backtest.vectorbt.configs.sweep import SweepConfig


def build_sweep_config() -> SweepConfig:
    base = build_config()

    base = dataclasses.replace(
        base,
        start_date      = "2021-01-01",
        end_date        = "2023-11-01",
        exit_rsi_period = 14,   # RSI period for 1h oversold calculation
    )

    sl_mults = (1.5, 2.0, 2.5, 3.0)
    tp_mults = (2.0, 3.0, 4.0, 5.0)

    # Oversold levels: 25 = deep oversold (rare), 40 = early warning
    rsi_oversold_levels = (25.0, 30.0, 35.0, 40.0)

    return SweepConfig(
        base                = base,
        sl_mults            = sl_mults,
        tp_mults            = tp_mults,
        exit_modes          = ("rsi_oversold",),
        rsi_oversold_levels = rsi_oversold_levels,
        min_trades          = 10,
    )
