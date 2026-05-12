"""Out-of-sample broad SL/TP sweep.

Purpose
-------
Validate that the (SL × TP) combinations that showed edge in-sample also
hold on completely unseen data.  Use the identical grid as ``is_broad`` so
the results are directly comparable.

Expectation
-----------
OOS performance will be lower.  A combo is considered robust when:
- It still passes all gates (SQN ≥ threshold, PF ≥ 1.0, …).
- The pair pass-rate stays ≥ 50 % of what was seen in-sample.

If *nothing* passes here, the strategy is likely curve-fitted.  Widen the
in-sample SL/TP search or revisit the entry filters.

Usage
-----
    python -m bear_strategy.backtest.vectorbt.sweep_run --config oos_broad
"""

from __future__ import annotations

import dataclasses

from bear_strategy.backtest.vectorbt.configs.default import build_config
from bear_strategy.backtest.vectorbt.configs.sweep import SweepConfig


def build_sweep_config() -> SweepConfig:
    # ── Shared baseline ────────────────────────────────────────────────────
    base = build_config()

    # ── Override: out-of-sample window ────────────────────────────────────
    base = dataclasses.replace(
        base,
        start_date = "2023-11-02",
        end_date   = "2026-04-22",
    )

    # ── Same SL/TP grid as is_broad for a fair comparison ─────────────────
    sl_mults = (1.0, 1.5, 2.0, 2.5, 3.0)
    tp_mults = (1.5, 2.0, 3.0, 4.0, 5.0, 6.0)

    return SweepConfig(
        base       = base,
        sl_mults   = sl_mults,
        tp_mults   = tp_mults,
        exit_modes = ("fixed_tp",),
        min_trades = 10,
    )
