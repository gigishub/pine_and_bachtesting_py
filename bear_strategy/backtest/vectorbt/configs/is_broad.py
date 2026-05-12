"""In-sample broad SL/TP sweep.  (default config)

Purpose
-------
First look at which (SL × TP) combinations show edge across the full
in-sample window.  Exit is fixed TP only — the RSI exit dimension is added
later in ``rsi_exit_sweep``.

What to look for
----------------
- Cluster of combos where SQN > 0, PF > 1.0 and the same pairs keep passing.
- Diagonal pattern in the Return heatmap → the R:R ratio matters more than
  the absolute SL or TP level.
- Any combo where fewer than 3 pairs pass is fragile — ignore it.

Next step
---------
- Run ``oos_broad`` with the same grid to check robustness on unseen data.
- Run ``rsi_exit_sweep`` on the best (sl, tp) cluster to test exit variants.

Usage
-----
    python -m bear_strategy.backtest.vectorbt.sweep_run --config is_broad
    python -m bear_strategy.backtest.vectorbt.sweep_run               # (same — this is the default)
"""

from __future__ import annotations

import dataclasses

from bear_strategy.backtest.vectorbt.configs.default import build_config
from bear_strategy.backtest.vectorbt.configs.sweep import SweepConfig


def build_sweep_config() -> SweepConfig:
    # ── Shared baseline ────────────────────────────────────────────────────
    # Everything not listed here comes from default.py unchanged.
    base = build_config()

    # ── Override: in-sample window ─────────────────────────────────────────
    base = dataclasses.replace(
        base,
        start_date = "2021-01-01",
        end_date   = "2023-11-01",
    )

    # ── SL grid ────────────────────────────────────────────────────────────
    # 1.0× = very tight stops (many stop-outs, small individual losses)
    # 3.0× = wide stops (fewer stop-outs, larger per-trade loss)
    sl_mults = (1.0, 1.5, 2.0, 2.5, 3.0)

    # ── TP grid ────────────────────────────────────────────────────────────
    # Only pairs where tp_mult > sl_mult are run (inverted R:R is excluded).
    tp_mults = (1.5, 2.0, 3.0, 4.0, 5.0, 6.0)

    return SweepConfig(
        base       = base,
        sl_mults   = sl_mults,
        tp_mults   = tp_mults,
        exit_modes = ("fixed_tp",),   # RSI exit not tested here
        min_trades = 10,
    )
