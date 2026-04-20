"""Phase 2 — Free Combination Sweep.

Purpose
-------
Follows Phase 1 (exclusive sweep across all 10 coins / 3 TFs).

Phase 1 findings applied here:
  Symbols:  AVAXUSDT, LINKUSDT only — remaining 8 showed 0% pass rate
  TFs:      1h, 4H only — 1D showed 0% pass rate
  Pinned OFF (0 frequency in Phase 1 top combos):
    use_donchian      → 0 / 36 top combos
    use_power_candle  → 0 / 36 top combos
    use_bbands        → 0 / 36 top combos
  Freely swept (exclusive pairs broken apart):
    use_adx, use_ema_ribbon, use_volume_profile, use_cmf,
    use_chandelier, use_psar, use_trailing_stop

All exclusive_mode flags are False — toggles vary independently so
RF/SHAP/OLS/Toggle Consensus in the Phase 2 Streamlit app are valid.

What to look for
----------------
- Sections 1–9 are all valid — no exclusive-mode correlation.
- OLS/SHAP: does use_cmf stay positive? Does use_adx stay negative?
- Toggle Consensus: which toggles reach ✅ Keep ON or ❌ Remove?
- Top combos: identify the 2–3 parameter sets to carry forward.

Estimated combos
----------------
  2 symbols × 2 TFs × 2^7 toggle combos = 512 combos
  (invalid combos filtered before run — actual count will be lower)
"""

from __future__ import annotations

from pathlib import Path

from adaptive_momentum_strategy.backtest.config import MomentumGridConfig


def build_config(output_dir: Path | None = None) -> MomentumGridConfig:
    symbols = ["ADAUSDT", "BNBUSDT", "BTCUSDT", "DOGEUSDT", "ETHUSDT", "SOLUSDT", "TRXUSDT", "XRPUSDT"]
    timeframes = ["1h", "4H"]

    start_time = "2022-09-01 00:00:00"
    end_time = "2025-09-01 00:00:00"

    boolean_filter_ranges = {
        # Freely swept — exclusive mode OFF, all vary independently
        "use_adx":            (False, True),
        "use_ema_ribbon":     (False, True),
        "use_volume_profile": (True,),
        "use_cmf":            (True,),
        "use_chandelier":     (False, True),
        "use_psar":           (False, True),
        "use_trailing_stop":  (False, True),
        # Pinned OFF — 0 frequency in Phase 1 top combos
        "use_donchian":       (False,),
        "use_power_candle":   (False,),
        "use_bbands":         (False,),
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
        enable_long=True,
        enable_short=False,
        # All exclusive flags OFF — required for valid RF/SHAP/OLS analysis
        regime_exclusive=False,
        setup_exclusive=False,
        trigger_exclusive=False,
        exit_exclusive=False,
        initial_cash=10_000.0,
        fees=0.001,
        n_jobs=-1,
        min_bars=500,
        output_dir=output_dir or Path(
            "adaptive_momentum_strategy/backtest/results/results_vbt"
        ),
        consistency_top_n=10,
        save_trade_logs=True,
        trade_logs_top_n=5,
    )