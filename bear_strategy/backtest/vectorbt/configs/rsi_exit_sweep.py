"""RSI exit mode sweep.

Purpose
-------
Test whether adding an RSI-based exit improves performance vs a pure
fixed-TP exit on the SL/TP combinations that already showed edge in-sample.

Run this *after* ``is_broad`` — use the winning (sl, tp) cluster in
``sl_mults`` / ``tp_mults`` below rather than the full broad grid.

Exit modes tested
-----------------
  fixed_tp
      Close when price falls ``target_atr_mult × ATR`` below entry.
      Baseline — no RSI involved.

  rsi_cross_up
      Close when the 1h RSI crosses UP above ``exit_rsi_level``.
      TP is disabled; SL always stays active.
      Use when you want to ride the trade until momentum shifts up.

  fixed_tp_or_rsi_cross_up
      Close at whichever fires first: the TP level or the RSI cross.
      SL always stays active.
      Use when you want the TP as a hard floor but want to exit early
      when RSI shows momentum reversal.

How to read the results
-----------------------
- Compare the "rsi_cross_up" rows against "fixed_tp" baseline:
  higher SQN / PF with comparable trades → RSI exit adds value.
- If "fixed_tp_or_rsi_cross_up" beats both → early exits help but TP is
  still needed as protection.
- Check Win Rate — RSI exits often reduce WR but increase avg win size.

Usage
-----
    python -m bear_strategy.backtest.vectorbt.sweep_run --config rsi_exit_sweep

Then adjust the (sl_mults, tp_mults) cluster below to focus on the combos
that already passed the is_broad gates.
"""

from __future__ import annotations

import dataclasses

from bear_strategy.backtest.vectorbt.configs.default import build_config
from bear_strategy.backtest.vectorbt.configs.sweep import SweepConfig


def build_sweep_config() -> SweepConfig:
    # ── Shared baseline ────────────────────────────────────────────────────
    base = build_config()

    # ── Override: in-sample window ─────────────────────────────────────────
    # Run on the same IS window used in is_broad for a fair comparison.
    base = dataclasses.replace(
        base,
        start_date     = "2021-01-01",
        end_date       = "2023-11-01",
        exit_rsi_period = 14,   # RSI period used for all RSI-based exit modes
    )

    # ── Narrow SL/TP grid ─────────────────────────────────────────────────
    # Edit this to focus on the winning cluster from is_broad.
    # Running the full 5×6 grid here triples run time without adding signal.
    sl_mults = (1.5, 2.0, 2.5)
    tp_mults = (2.0, 3.0, 4.0)

    # ── Exit modes to compare ─────────────────────────────────────────────
    exit_modes = (
        "fixed_tp",                   # baseline
        "rsi_cross_up",               # RSI-only exit
        "fixed_tp_or_rsi_cross_up",   # TP floor + RSI early exit
    )

    # ── RSI levels to test for the RSI exit modes ──────────────────────────
    # 40 → exit very early (momentum just turned)
    # 55 → exit later (momentum clearly reversed)
    exit_rsi_levels = (40.0, 45.0, 50.0, 55.0)

    return SweepConfig(
        base            = base,
        sl_mults        = sl_mults,
        tp_mults        = tp_mults,
        exit_modes      = exit_modes,
        exit_rsi_levels = exit_rsi_levels,
        min_trades      = 10,
    )
