"""Phase 1 — Broad Sweep.

Purpose
-------
First pass over the full indicator space.  Every toggle is swept (on/off),
all three timeframes are tested, and exclusive mode isolates each indicator
so you can see individual contribution.

What to look for in the robustness report
------------------------------------------
- Symbol pass rate >= 60% and timeframe pass rate >= 60% → ROBUST.
- OLS table: toggles with significant negative coefficient → candidates to
  pin OFF in Phase 2.
- OLS table: toggles with significant positive coefficient → candidates to
  pin ON in Phase 2.
- Timeframe Consistency table: identify the best-performing timeframe(s).
- Top Toggle Frequency: confirms which toggles appear in winning combos.

Next step
---------
If pass rates are below threshold (MARGINAL/WEAK), proceed to Phase 2:
    python -m adaptive_momentum_strategy.backtest.vectorbt.run --config phase2_4h_cleanup
"""

from __future__ import annotations

from pathlib import Path

from adaptive_momentum_strategy.backtest.config import MomentumGridConfig


def build_config(output_dir: Path | None = None) -> MomentumGridConfig:
    symbols = [
        "BTCUSDT", "ETHUSDT", "XRPUSDT", "BNBUSDT", "SOLUSDT",
        "TRXUSDT", "DOGEUSDT", "ADAUSDT", "AVAXUSDT", "LINKUSDT",
    ]
    timeframes = ["1h", "4H", "1D"]

    start_time = "2022-09-01 00:00:00"
    end_time = "2025-09-01 00:00:00"

    enable_long = True
    enable_short = False

    def _flag_range(enabled: bool) -> tuple[bool, ...]:
        return (False, True) if enabled else (False,)

    boolean_filter_ranges = {
        "use_adx":            _flag_range(enable_long),
        "use_ema_ribbon":     _flag_range(enable_long),
        "use_donchian":       _flag_range(enable_long),
        "use_volume_profile": _flag_range(enable_long),
        "use_cmf":            _flag_range(enable_long),
        "use_power_candle":   _flag_range(enable_long),
        "use_chandelier":     _flag_range(enable_long),
        "use_psar":           _flag_range(enable_long),
        "use_bbands":         _flag_range(enable_long),
        "use_trailing_stop":  _flag_range(enable_long),
        # Short flags pinned off
        "use_vbt_sl":               (False,),
        "use_vbt_sl_trail":         (False,),
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
        regime_exclusive=True,   # isolate each indicator: one per layer
        setup_exclusive=True,
        trigger_exclusive=True,
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
