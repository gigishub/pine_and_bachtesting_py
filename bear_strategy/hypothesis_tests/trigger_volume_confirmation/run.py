"""CLI entry point for Step 3 — Trigger Volume Confirmation.

Usage:
    source .venv/bin/activate && python -m bear_strategy.hypothesis_tests.trigger_volume_confirmation.run

Timeframe configuration (set in config.py):
    entry_tf = entry candle resolution (default "1h")

    Timeframe guide for bear shorts:
      "15m"  →  intraday scalps,   target hold  15 min – 4 h
      "1h"   →  swing shorts,      target hold  1 – 48 h    ← default
      "4h"   →  position shorts,   target hold  days – weeks

    Smaller entry_tf → more signals, more noise, shorter holds.
    Larger entry_tf → fewer signals, higher quality, longer holds.

Context:
    Step 1 winner regime: ema_below_50.
    Step 2 falsified setup-level proximity — this test runs directly on the
    regime population with no setup gate.

Verdict logic:
    Baseline = not_triggered population.
    Tested   = volume_triggered population.
    A pair passes when:
        - wr_lift  > 2.5 × sqrt(p × (1-p) / n)
        - pf_lift  > noise_floor(n)
        - n_trades > min_trades_per_pair
    Overall pass: clears all thresholds on ≥ 3 of 4 pairs.

Result file is named: step3_results_entry{entry_tf}.csv
"""

from __future__ import annotations

import logging
import math
import sys

import numpy as np
import pandas as pd

from bear_strategy.hypothesis_tests.trigger_volume_confirmation.config import TestConfig
from bear_strategy.hypothesis_tests.trigger_volume_confirmation.runner import run_test
from bear_strategy.hypothesis_tests.experiment_config import ExperimentConfig

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def main() -> None:
    config = TestConfig.from_experiment(ExperimentConfig())

    logger.info("=" * 70)
    logger.info("Bear Strategy — Step 3: Trigger Volume Confirmation")
    logger.info("Entry TF    : %s", config.entry_tf)
    logger.info("Regime      : %s (Step 1 winner)", config.regime_col)
    logger.info("Pairs       : %s", config.pairs)
    logger.info(
        "Volume      : > %.1f× %d-bar rolling average",
        config.volume_mult,
        config.volume_window,
    )
    logger.info(
        "Stop  : %.1f× ATR_%s  |  Target: %.1f× ATR_%s",
        config.stop_atr_mult, config.entry_tf,
        config.target_atr_mult, config.entry_tf,
    )
    logger.info("=" * 70)

    results = run_test(config)

    if results.empty:
        logger.error("No results — check parquet data availability.")
        sys.exit(1)

    _print_summary(results, config)
    _save_results(results, config)
    _print_verdict(results, config)


# ---------------------------------------------------------------------------
# Reporting helpers
# ---------------------------------------------------------------------------


def _print_summary(results: pd.DataFrame, config: TestConfig) -> None:
    print("\n── Per-Pair Results ──\n")
    df = results.reset_index()
    pop_order = ["all_regime", "volume_triggered", "not_triggered"]

    for pair in config.pairs:
        pair_df = df[df["pair"] == pair].set_index("population")
        if pair_df.empty:
            continue
        print(f"  {pair}")
        subset = pair_df.reindex([p for p in pop_order if p in pair_df.index]).copy()
        subset["wr_%"] = (subset["win_rate"] * 100).round(2)
        subset["pf"] = subset["profit_factor"].round(3)
        subset["dur"] = subset["avg_duration"].round(1)
        print(subset[["wr_%", "pf", "dur", "n_trades"]].to_string())
        print()


def _save_results(results: pd.DataFrame, config: TestConfig) -> None:
    config.results_dir.mkdir(parents=True, exist_ok=True)
    filename = f"step3_results_entry{config.entry_tf}.csv"
    out = config.results_dir / filename
    results.reset_index().to_csv(out, index=False)
    logger.info("Results saved → %s", out)


def _min_wr_lift(config: TestConfig, baseline_wr: float, smaller_n: int) -> float:
    if smaller_n <= 0:
        return float("inf")
    variance = max(baseline_wr * (1.0 - baseline_wr), 0.0)
    return config.significance_zscore * math.sqrt(variance / smaller_n)


def _min_pf_diff(config: TestConfig, smaller_n: int) -> float:
    if smaller_n > 50_000:
        return config.min_pf_diff_high_n
    if smaller_n >= 10_000:
        return config.min_pf_diff_mid_n
    return config.min_pf_diff_low_n


def _print_verdict(results: pd.DataFrame, config: TestConfig) -> None:
    df = results.reset_index()

    baseline_df = df[df["population"] == "not_triggered"].set_index("pair")
    if baseline_df.empty:
        logger.error("No not_triggered rows — cannot compute verdict.")
        return

    baseline = baseline_df[["win_rate", "profit_factor", "n_trades"]].rename(
        columns={"win_rate": "wr_base", "profit_factor": "pf_base", "n_trades": "n_base"}
    )

    avg_base_wr = baseline["wr_base"].mean()
    avg_base_pf = baseline["pf_base"].mean()

    print("── Trigger Volume Confirmation Verdict ──\n")
    print(
        f"  Baseline (not_triggered):  avg WR {avg_base_wr * 100:.1f}%  "
        f"avg PF {avg_base_pf:.3f}"
    )
    print()

    passing: list[tuple[str, float]] = []

    for pop in ["volume_triggered"]:
        pop_df = df[df["population"] == pop].set_index("pair")
        if pop_df.empty:
            print(f"  {pop:<22}  — no data")
            continue

        joined = pop_df.join(baseline)
        joined["smaller_n"] = joined[["n_trades", "n_base"]].min(axis=1).astype(int)
        joined["wr_lift"] = joined["win_rate"] - joined["wr_base"]
        joined["pf_lift"] = joined["profit_factor"] - joined["pf_base"]
        joined["min_wr_lift"] = joined.apply(
            lambda row: _min_wr_lift(config, float(row["wr_base"]), int(row["smaller_n"])),
            axis=1,
        )
        joined["min_pf_lift"] = joined["smaller_n"].apply(
            lambda n: _min_pf_diff(config, int(n))
        )
        joined["pair_passes"] = (
            (joined["wr_lift"] > joined["min_wr_lift"])
            & (joined["pf_lift"] > joined["min_pf_lift"])
            & (joined["n_trades"] > config.min_trades_per_pair)
            & (joined["profit_factor"] > joined["pf_base"])
        )

        n_pairs = len(joined)
        n_passing = int(joined["pair_passes"].sum())
        avg_pf = joined["profit_factor"].mean()
        avg_wr_lift = joined["wr_lift"].mean() * 100
        avg_pf_lift = joined["pf_lift"].mean()
        overall = n_passing >= config.min_pairs_passing
        status = "✅" if overall else "❌"

        print(
            f"  {pop:<22}  avg WR lift {avg_wr_lift:+.2f}pp  avg PF {avg_pf:.3f}"
            f"  avg PF lift {avg_pf_lift:+.3f}"
            f"  pairs ≥ threshold: {n_passing}/{n_pairs}  {status}"
        )
        for pair, row in joined.iterrows():
            pair_status = "✅" if row["pair_passes"] else "❌"
            print(
                f"    {pair:<10}  WR {row['win_rate'] * 100:.2f}%  "
                f"lift {row['wr_lift'] * 100:+.2f}pp / req {row['min_wr_lift'] * 100:.2f}pp  "
                f"PF {row['profit_factor']:.3f}  lift {row['pf_lift']:+.3f} / req {row['min_pf_lift']:.3f}  "
                f"trades {int(row['n_trades']):,}  {pair_status}"
            )
        print()

        if overall:
            passing.append((pop, avg_pf))

    print(
        f"  Thresholds: WR lift > 2.5×sqrt(p(1-p)/n),  "
        f"PF lift > 0.02 if n>50k / 0.05 if n≥10k / 0.10 if n<10k,  "
        f"trades > {config.min_trades_per_pair:,},  "
        f"consistent across ≥ {config.min_pairs_passing} pairs"
    )
    print()

    if passing:
        _, best_pf = max(passing, key=lambda x: x[1])
        print("  ✅  VOLUME TRIGGER CONFIRMED — volume_triggered adds edge beyond regime.")
        print(f"      avg PF {best_pf:.3f}")
        print("      Proceed to Step 4 (exit calibration).")
        print(
            "      Promote volume trigger logic to "
            "bear_strategy/strategy/indicators/trigger/volume_spike.py"
        )
    else:
        print("  ❌  VOLUME TRIGGER NOT CONFIRMED — does not clear all thresholds.")
        print("      Consider:")
        print("        • Adjusting volume_mult (try 1.2×, 1.5×, 2.0×)")
        print("        • Adjusting volume_window (try 10 or 50 bars)")
        print("        • Proceeding to Step 4 on raw all_regime population")
    print()


if __name__ == "__main__":
    main()
