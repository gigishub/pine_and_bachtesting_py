"""Phase 2 — Top-10 Targeted Validation.

Runs a focused backtest over the 10 best-ranked signatures from the Phase 1
broad sweep (2026-04-10_2329_AMS_long_only).  Constants across all 10 combos
are pinned; only the 5 varying toggles are swept, producing 32 total combos
(= 2^5) that include all 10 targets as a subset.

Top-10 signatures (by weighted final_score):
  1. adx + volume_profile + cmf + trailing_stop                         → 0.5266
  2. adx + volume_profile + cmf + psar + trailing_stop                  → 0.4721
  3. adx + volume_profile + cmf + chandelier + psar                     → 0.2794
  4. adx + volume_profile + cmf + chandelier                            → 0.2733
  5. adx + volume_profile + cmf + chandelier + psar + trailing_stop     → 0.2683
  6. ema_ribbon + volume_profile + cmf + psar + trailing_stop           → 0.2320
  7. adx + volume_profile + cmf + chandelier + trailing_stop            → 0.2235
  8. ema_ribbon + volume_profile + cmf + trailing_stop                  → 0.2180
  9. ema_ribbon + volume_profile + cmf + chandelier + psar              → 0.2159
 10. ema_ribbon + volume_profile + cmf + chandelier + psar + ts         → 0.2153

Pinned OFF (always 0 in every top-10 signature):
    use_donchian, use_power_candle, use_bbands

Pinned ON (always 1 in every top-10 signature):
    use_volume_profile, use_cmf

Swept (vary between 0 and 1 across the top-10):
    use_adx, use_ema_ribbon, use_chandelier, use_psar, use_trailing_stop

No exclusive mode — full combination grid so all 32 combos run together.
trade_logs_top_n=15 ensures all 10 target signatures have trade logs saved
for Phase 2 date-range sensitivity analysis.

Usage:
    python -m adaptive_momentum_strategy.backtest.vectorbt.run \
        --config phase2_top10_targeted
"""

from __future__ import annotations

from pathlib import Path

from adaptive_momentum_strategy.backtest.config import MomentumGridConfig


def build_config(output_dir: Path | None = None) -> MomentumGridConfig:
    symbols = [
        "BTCUSDT", "ETHUSDT", "XRPUSDT", "BNBUSDT", "SOLUSDT",
        "TRXUSDT", "DOGEUSDT", "ADAUSDT", "AVAXUSDT", "LINKUSDT",
    ]
    timeframes = ["1h", "4H"]

    return MomentumGridConfig(
        source="bybit",
        market_type="linear",
        symbols=symbols,
        timeframes=timeframes,
        start_time="2020-09-01 00:00:00",
        end_time=None,
        boolean_filter_ranges={
            # ── Regime (sweep: both appear in top-10) ──────────────────────
            "use_adx":            (False, True),
            "use_ema_ribbon":     (False, True),
            # ── Setup (pinned: donchian always off, volume_profile always on)
            "use_donchian":       (False,),
            "use_volume_profile": (True,),
            # ── Execution trigger (pinned: cmf always on, power_candle off) ─
            "use_cmf":            (True,),
            "use_power_candle":   (False,),
            # ── Risk & Exit (sweep: vary across top-10) ────────────────────
            "use_chandelier":     (False, True),
            "use_psar":           (False, True),
            "use_bbands":         (False,),          # always off in top-10
            "use_trailing_stop":  (False, True),
            # ── Short flags (all pinned off — long-only run) ───────────────
            "use_vbt_sl":               (False,),
            "use_ema_ribbon_short":     (False,),
            "use_donchian_short":       (False,),
            "use_volume_profile_short": (False,),
            "use_cmf_short":            (False,),
            "use_power_candle_short":   (False,),
            "use_chandelier_short":     (False,),
            "use_psar_short":           (False,),
            "use_bbands_short":         (False,),
            "use_trailing_stop_short":  (False,),
        },
        enable_long=True,
        enable_short=False,
        # No exclusive mode — all combinations are valid here
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
        trade_logs_top_n=15,   # 15 > 10 targets → all 10 sigs captured per condition
    )