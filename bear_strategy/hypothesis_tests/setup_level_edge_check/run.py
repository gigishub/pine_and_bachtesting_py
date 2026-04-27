"""CLI entry point for Step 2 — Setup Level Edge Check.

Usage:
    python -m bear_strategy.hypothesis_tests.setup_level_edge_check.run

Timeframe configuration (set in config.py):
    entry_tf   = entry candle resolution (default "1h")
    context_tf = higher-TF for VPVR, AVWAP, and ATR signals (default "4h")

    Timeframe guide for bear shorts:
      "15m" + "4h"  →  intraday scalps,   target hold  1–8 h
      "1h"  + "4h"  →  swing shorts,      target hold  4–48 h  ← default
      "4h"  + "1d"  →  position shorts,   target hold  days–weeks

    Larger entry_tf → fewer trades, higher per-trade quality, longer holds.
    Smaller entry_tf → more trades, more noise, tighter stops needed.

Regime filter: ema_below_50 (Step 1 winner).
See: bear_strategy/backtest/results/backtesting_py/step1_regime_check/step1_results.csv

Result file is named: step2_results_entry{entry_tf}_context{context_tf}.csv

Verdict logic:
    Baseline for comparison = away_from_setup population.
    Populations tested: near_setup, vpvr_only, vwap_only.
    A population passes a pair when:
        - wr_lift  > 2.5 × sqrt(p × (1-p) / n)
        - pf_lift  > noise_floor(n)   (0.02 if n>50k, 0.05 if 10k-50k, 0.10 if <10k)
        - n_trades > min_trades_per_pair
    Overall pass: clears all thresholds on ≥ 3 of 4 pairs.
"""

from __future__ import annotations

import logging
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from bear_strategy.hypothesis_tests.setup_level_edge_check.config import TestConfig
from bear_strategy.hypothesis_tests.setup_level_edge_check.runner import run_test

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def main() -> None:
    config = TestConfig()

    logger.info("=" * 70)
    logger.info("Bear Strategy — Step 2: Setup Level Edge Check")
    logger.info("Entry TF    : %s  |  Context TF: %s", config.entry_tf, config.context_tf)
    logger.info("Regime      : %s (Step 1 winner)", config.regime_col)
    logger.info("Pairs       : %s", config.pairs)
    logger.info("Distance    : %.1f× ATR_%s from VPVR HVN or Anchored VWAP", config.setup_distance_atr, config.context_tf)
    logger.info("VPVR window : %d %s bars", config.vpvr_window, config.context_tf)
    logger.info("Swing SH    : lookback=%d  confirm=%d bars", config.swing_lookback, config.swing_confirmation_bars)
    logger.info("Stop  : %.1f× ATR_%s  |  Target: %.1f× ATR_%s", config.stop_atr_mult, config.entry_tf, config.target_atr_mult, config.entry_tf)
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

    for pair in config.pairs:
        pair_df = df[df["pair"] == pair].set_index("population")
        if pair_df.empty:
            continue
        print(f"  {pair}")
        subset = pair_df.reindex(
            [p for p in ["all_regime", "near_setup", "away_from_setup", "vpvr_only", "vwap_only"] if p in pair_df.index]
        )
        subset = subset.copy()
        subset["wr_%"] = (subset["win_rate"] * 100).round(2)
        subset["pf"] = subset["profit_factor"].round(3)
        subset["dur"] = subset["avg_duration"].round(1)
        print(
            subset[["wr_%", "pf", "dur", "n_trades"]].to_string()
        )
        print()


def _save_results(results: pd.DataFrame, config: TestConfig) -> None:
    config.results_dir.mkdir(parents=True, exist_ok=True)
    filename = f"step2_results_entry{config.entry_tf}_context{config.context_tf}.csv"
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

    away_df = df[df["population"] == "away_from_setup"].set_index("pair")
    if away_df.empty:
        logger.error("No away_from_setup rows — cannot compute verdict.")
        return

    baseline = away_df[["win_rate", "profit_factor", "n_trades"]].rename(
        columns={"win_rate": "wr_base", "profit_factor": "pf_base", "n_trades": "n_base"}
    )

    avg_base_wr = baseline["wr_base"].mean()
    avg_base_pf = baseline["pf_base"].mean()

    print("── Setup Level Edge Verdict ──\n")
    print(
        f"  Baseline (away_from_setup):  avg WR {avg_base_wr * 100:.1f}%  "
        f"avg PF {avg_base_pf:.3f}"
    )
    print()

    populations_to_test = ["near_setup", "vpvr_only", "vwap_only"]
    passing: list[tuple[str, float]] = []

    for pop in populations_to_test:
        pop_df = df[df["population"] == pop].set_index("pair")
        if pop_df.empty:
            print(f"  {pop:<20}  — no data")
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
            f"  {pop:<20}  avg WR lift {avg_wr_lift:+.2f}pp  avg PF {avg_pf:.3f}"
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
        best_pop, best_pf = max(passing, key=lambda x: x[1])
        print("  ✅  SETUP EDGE CONFIRMED — at least one setup level creates predictive resistance.")
        print(f"      Best performer: {best_pop}  (avg PF {best_pf:.3f})")
        print("      Proceed to Step 3 (trigger confirmation).")
        print()
        _print_component_verdict(passing)
    else:
        print("  ❌  SETUP EDGE NOT CONFIRMED — no setup level clears all thresholds.")
        print("      Consider:")
        print("        • Adjusting setup_distance_atr (try 0.3× or 0.7×)")
        print("        • Redefining VPVR or AVWAP computation")
        print("        • Revisiting regime filter or data range")
    print()


def _print_component_verdict(passing: list[tuple[str, float]]) -> None:
    """Print which components to keep based on individual vs combined."""
    pop_names = {p for p, _ in passing}
    has_combined = "near_setup" in pop_names
    has_vpvr = "vpvr_only" in pop_names
    has_vwap = "vwap_only" in pop_names

    print("  ── Component Decision ──")
    if has_combined and has_vpvr and has_vwap:
        pf_combined = next(pf for p, pf in passing if p == "near_setup")
        pf_vpvr = next(pf for p, pf in passing if p == "vpvr_only")
        pf_vwap = next(pf for p, pf in passing if p == "vwap_only")
        if pf_combined >= max(pf_vpvr, pf_vwap):
            print("      Combined (near_setup) ≥ both components → keep both VPVR and AVWAP.")
        elif pf_vwap > pf_vpvr:
            print("      AVWAP outperforms combined → consider cutting VPVR.")
        else:
            print("      VPVR outperforms combined → consider cutting AVWAP.")
    elif has_vpvr and not has_vwap:
        print("      Only vpvr_only passes → AVWAP adds no edge, cut it.")
    elif has_vwap and not has_vpvr:
        print("      Only vwap_only passes → VPVR adds no edge, cut it.")
    elif has_combined and not has_vpvr and not has_vwap:
        print("      Only combined passes → both components needed together.")
    print()


if __name__ == "__main__":
    main()
