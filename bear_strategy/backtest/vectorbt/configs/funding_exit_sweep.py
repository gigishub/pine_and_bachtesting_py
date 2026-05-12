"""Funding regime-shift exit sweep.

Purpose
-------
Test the ``funding_regime_shift`` exit across a range of SL multiples.
The exit fires when the EMA-smoothed 8h funding rate drops at or below
``funding_threshold`` — i.e. the carry tailwind (longs paying shorts)
has disappeared.  A fixed ATR TP remains active as a safety net.

The idea: we entered because funding was positive (longs paying us to hold
the short).  When that funding regime flips, the strategic reason for the
trade is gone — exit regardless of price.

Lookahead guarantee
-------------------
The exit uses ``settled = smoothed.shift(1)`` (matching the entry guard)
then detects ``(settled.shift(1) > thr) & (settled <= thr)``, so it only
reads ``smoothed[N-2]`` and ``smoothed[N-1]`` at bar N — both past values.
``fill_at_next_open`` adds +1 → execution at open[N+1].  Zero lookahead.

What to look for
----------------
- Win-rate boost vs ``fixed_tp``: the regime-shift exit should let winners
  run while cutting short any trade where the carry edge has evaporated.
- Compare average trade duration to ``fixed_tp``.  Shorter + same return
  = better capital efficiency.
- Pairs where PF drops vs ``fixed_tp`` may have funding that flips
  frequently even within healthy downtrends — apply a pair-level filter.

Next step
---------
- Compare passing pairs against ``is_broad`` results.
- If the same pairs pass, consider combining funding exit with a tight TP
  (``fixed_tp_or_funding``) — not yet implemented but easy to add.

Usage
-----
    python -m bear_strategy.backtest.vectorbt.sweep_run --config funding_exit_sweep
"""

from __future__ import annotations

import dataclasses

from bear_strategy.backtest.vectorbt.configs.default import build_config
from bear_strategy.backtest.vectorbt.configs.sweep import SweepConfig


def build_sweep_config() -> SweepConfig:
    base = build_config()

    # In-sample window — same as is_broad for apples-to-apples comparison
    base = dataclasses.replace(
        base,
        start_date = "2021-01-01",
        end_date   = "2023-11-01",
        # funding_threshold stays at default (0.0): exit when rate ≤ 0
        # Increase to e.g. 0.0001 for an earlier / tighter funding exit
    )

    # Narrow SL grid — funding exit works best with moderate stops
    sl_mults = (1.5, 2.0, 2.5, 3.0)

    # TP still active as a safety net — test both conservative and wide TP
    tp_mults = (2.0, 3.0, 4.0, 5.0)

    return SweepConfig(
        base       = base,
        sl_mults   = sl_mults,
        tp_mults   = tp_mults,
        exit_modes = ("funding_regime_shift",),
        min_trades = 10,
    )
