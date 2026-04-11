"""Phase 3 — Numeric Parameter Sweep.

Purpose
-------
After Phase 2 confirms avg SQN >= 1.5 with the clean toggle config, this
phase sweeps the key numeric parameters of the surviving indicators to find
optimal values without blowing up the grid.

Gating condition
----------------
Only run this phase if Phase 2 robustness report shows:
  - Avg SQN >= 1.5
  - Symbol pass rate >= 70%

What to look for
----------------
- Which numeric values consistently appear in the top combos?
- Does tuning numeric params further lift SQN or is the gain minimal?
- Beware overfitting: if the best combo is a single extreme value (e.g.
  cmf_threshold=0.00), treat it with suspicion.

Next step
---------
Take the best numeric params and run a walk-forward test (out-of-sample).
"""

from __future__ import annotations

from pathlib import Path

from adaptive_momentum_strategy.backtest.config import MomentumGridConfig


def build_config(output_dir: Path | None = None) -> MomentumGridConfig:
    symbols = [
        "BTCUSDT", "ETHUSDT", "XRPUSDT", "BNBUSDT", "SOLUSDT",
        "TRXUSDT", "DOGEUSDT", "ADAUSDT",
    ]
    timeframes = ["4H"]

    start_time = "2022-09-01 00:00:00"
    end_time = "2025-09-01 00:00:00"

    enable_long = True
    enable_short = False

    # Toggle config carried over from Phase 2 (pinned / grid)
    boolean_filter_ranges = {
        "use_adx":            (False, True),
        "use_ema_ribbon":     (False, True),
        "use_donchian":       (False, True),  # keep in grid — splitter
        "use_volume_profile": (False, True),
        "use_cmf":            (True,),         # pinned ON
        "use_power_candle":   (False,),        # pinned OFF
        "use_chandelier":     (False, True),
        "use_psar":           (False, True),
        "use_bbands":         (False,),        # pinned OFF (consistently hurt)
        "use_trailing_stop":  (False, True),
        "use_ema_ribbon_short":     (False,),
        "use_donchian_short":       (False,),
        "use_volume_profile_short": (False,),
        "use_cmf_short":            (False,),
        "use_power_candle_short":   (False,),
        "use_chandelier_short":     (False,),
        "use_psar_short":           (False,),
        "use_bbands_short":         (False,),
        "use_trailing_stop_short":  (False,),
    }

    config = MomentumGridConfig(
        source="bybit",
        market_type="linear",
        symbols=symbols,
        timeframes=timeframes,
        start_time=start_time,
        end_time=end_time,
        boolean_filter_ranges=boolean_filter_ranges,
        enable_long=enable_long,
        enable_short=enable_short,
        regime_exclusive=False,
        setup_exclusive=False,
        trigger_exclusive=False,
        exit_exclusive=False,
        initial_cash=10_000.0,
        fees=0.001,
        n_jobs=-1,
        min_bars=500,
        output_dir=output_dir or Path("adaptive_momentum_strategy/backtest/results/results_vbt"),
        consistency_top_n=10,
        save_trade_logs=True,
        trade_logs_top_n=5,
    )

    # Numeric sweeps — conservative choices to avoid overfitting
    config.cmf_threshold_range = (0.03, 0.05, 0.08)
    config.chandelier_atr_mult_range = (2.0, 3.0)
    config.adx_threshold_range = (20.0, 25.0, 30.0)

    return config
