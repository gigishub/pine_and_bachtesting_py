"""Phase 2 — 4H Combination Mode.

Purpose
-------
Phase 1 showed 4H timeframe pass rate of 80% (only TF worth pursuing).
Phase 1 used exclusive=True — each indicator was tested in isolation, one
per layer at a time.

This phase keeps ALL indicators in the grid but narrows to 4H only and
switches to combination mode (exclusive=False).  This tests whether
indicators that performed well individually also stack well together.

Why NOT to pin indicators off based on Phase 1 OLS alone
---------------------------------------------------------
The Phase 1 OLS showed donchian with coefficient −1.19, but donchian also
appeared in 53 top-ranking combos and had the highest RF importance (0.2886).
High importance + negative average coefficient = the toggle creates a large
split: great in some combinations, terrible in others.  Forcing it off removes
both the bad AND the good half.  Let the combination grid find the right context.

What to look for in the robustness report
------------------------------------------
- Avg SQN vs Phase 1 (1.07): should be >= 1.2 to confirm combinations help.
- Symbol pass rate: should stay near 80%.
- Top Toggle Frequency: which combos consistently appear in passing results?
- OLS: now with combinations, does donchian coefficient stay negative?
  If yes in all combinations → reconsider pinning it off in Phase 3.

Next step
---------
If avg SQN >= 1.5 and pass rates hold → proceed to numeric sweep:
    python -m adaptive_momentum_strategy.backtest.vectorbt.run --config phase3_numeric_sweep

If donchian still shows negative OLS in combination results → pin it off
then and only then in a targeted Phase 3 run.
"""

from __future__ import annotations

from pathlib import Path

from adaptive_momentum_strategy.backtest.config import MomentumGridConfig


def build_config(output_dir: Path | None = None) -> MomentumGridConfig:
    symbols = [
        "BTCUSDT", "ETHUSDT", "XRPUSDT", "BNBUSDT", "SOLUSDT",
        "TRXUSDT", "DOGEUSDT", "ADAUSDT", "AVAXUSDT", "LINKUSDT",
    ]
    timeframes = ["4H"]  # best TF from Phase 1

    start_time = "2022-09-01 00:00:00"
    end_time = "2025-09-01 00:00:00"

    enable_long = True
    enable_short = False

    # All long toggles in the grid — let combinations reveal the real signal.
    # Nothing forced off based on average OLS alone.
    boolean_filter_ranges = {
        "use_adx":            (False, True),
        "use_ema_ribbon":     (False, True),
        "use_donchian":       (False, True),  # kept in grid — OLS average ≠ always bad
        "use_volume_profile": (False, True),
        "use_cmf":            (False, True),
        "use_power_candle":   (False, True),
        "use_chandelier":     (False, True),
        "use_psar":           (False, True),
        "use_bbands":         (False, True),
        "use_trailing_stop":  (False, True),
        # Short flags pinned off
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

    return MomentumGridConfig(
        source="bybit",
        market_type="linear",
        symbols=symbols,
        timeframes=timeframes,
        start_time=start_time,
        end_time=end_time,
        boolean_filter_ranges=boolean_filter_ranges,
        enable_long=enable_long,
        enable_short=enable_short,
        regime_exclusive=False,   # combination mode: test synergies between indicators
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
    # Numeric params pinned to baseline.
    # Unlock in Phase 3 only after SQN improves and donchian story is clearer.
