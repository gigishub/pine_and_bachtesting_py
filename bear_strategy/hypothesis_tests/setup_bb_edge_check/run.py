"""CLI entry point for Step 2 — BB Widening Setup Edge Check.

Usage:
    source .venv/bin/activate
    python -m bear_strategy.hypothesis_tests.setup_bb_edge_check.run

Timeframe (set entry_tf in config.py):
    "1h"  — swing shorts, 4–48 h holds  ← default
    "15m" — intraday scalps
    "4h"  — position shorts

Result files:
    step2_bb_results_entry{entry_tf}.csv
    step2_bb_results_entry{entry_tf}.md

──────────────────────────────────────────────────────────────────────
What is being tested
──────────────────────────────────────────────────────────────────────
Within EMA-50 confirmed bear regime bars (Step 1 winner), test whether
BB bands widening (volatility picking up) creates a measurable edge:

    bb_widening = BB_width(20) > BB_width(20)[1]
                  (bands are expanding bar over bar)

Sub-populations decompose where the edge concentrates:
    bb_widening_bearish  — widening AND close < BB_basis (lower half of channel)
    bb_widening_breakout — widening AND close < BB_lower (full lower-band break)

Baseline = regime_only (all eligible regime bars post-warmup).

──────────────────────────────────────────────────────────────────────
Pass/fail criteria (from spec)
──────────────────────────────────────────────────────────────────────
For each pair:
    wr_lift  > 2.5 × sqrt(p × (1-p) / n)   where p = baseline WR
    pf_lift  > noise_floor(n)               (0.02/0.05/0.10)
    n_trades > min_trades_per_pair
    bb_widening covers ≥ 30% of eligible regime bars

Overall PASS: ≥ 4 of 5 pairs clear all thresholds.

Regime filter: ema_below_50 (Step 1 winner).
See: bear_strategy/backtest/hypothesis_tests_raw/results/step1_regime_check/
"""

from __future__ import annotations

import logging
import math
import sys

import numpy as np
import pandas as pd

from bear_strategy.hypothesis_tests.setup_bb_edge_check.config import TestConfig
from bear_strategy.hypothesis_tests.setup_bb_edge_check.runner import run_test

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def main() -> None:
    config = TestConfig()

    logger.info("=" * 70)
    logger.info("Bear Strategy — Step 2: BB Widening Setup Edge Check")
    logger.info("Entry TF     : %s  |  Regime TF: 1d (daily, fixed)", config.entry_tf)
    logger.info("Regime       : %s (Step 1 winner)", config.regime_col)
    logger.info("Pairs        : %s", config.pairs)
    logger.info("BB           : period=%d  std_mult=%.1f", config.bb_period, config.bb_std_mult)
    logger.info(
        "Stop : %.1f× ATR(%s,%d)  |  Target: %.1f× ATR(%s,%d)",
        config.stop_atr_mult, config.entry_tf, config.atr_period,
        config.target_atr_mult, config.entry_tf, config.atr_period,
    )
    logger.info("Pass threshold: ≥ %d of %d pairs", config.min_pairs_passing, len(config.pairs))
    logger.info("Coverage guard: bb_widening must keep ≥ %.0f%% of regime bars", config.min_coverage_ratio * 100)
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
        ordered = [p for p in ["regime_only", "bb_widening", "bb_widening_bearish", "bb_widening_breakout"] if p in pair_df.index]
        subset = pair_df.reindex(ordered).copy()
        subset["wr_%"] = (subset["win_rate"] * 100).round(2)
        subset["pf"] = subset["profit_factor"].round(3)
        subset["dur"] = subset["avg_duration"].round(1)

        print(subset[["wr_%", "pf", "dur", "n_trades"]].to_string())

        # Coverage check inline
        regime_n = pair_df.loc["regime_only", "n_trades"] if "regime_only" in pair_df.index else 0
        bb_n = pair_df.loc["bb_widening", "n_trades"] if "bb_widening" in pair_df.index else 0
        if regime_n > 0:
            coverage = bb_n / regime_n
            coverage_flag = "⚠️  LOW COVERAGE" if coverage < config.min_coverage_ratio else ""
            print(f"    bb_widening covers {coverage * 100:.1f}% of regime bars  {coverage_flag}")
        print()


def _save_results(results: pd.DataFrame, config: TestConfig) -> None:
    config.results_dir.mkdir(parents=True, exist_ok=True)
    filename = f"step2_bb_results_entry{config.entry_tf}.csv"
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

    baseline_df = df[df["population"] == "regime_only"].set_index("pair")
    if baseline_df.empty:
        logger.error("No regime_only rows — cannot compute verdict.")
        return

    baseline = baseline_df[["win_rate", "profit_factor", "n_trades"]].rename(
        columns={"win_rate": "wr_base", "profit_factor": "pf_base", "n_trades": "n_base"}
    )

    avg_base_wr = baseline["wr_base"].mean()
    avg_base_pf = baseline["pf_base"].mean()

    print("── BB Widening Setup Edge Verdict ──\n")
    print(
        f"  Baseline (regime_only):  avg WR {avg_base_wr * 100:.1f}%  "
        f"avg PF {avg_base_pf:.3f}"
    )
    print()

    populations_to_test = ["bb_widening", "bb_widening_bearish", "bb_widening_breakout"]
    passing: list[tuple[str, float]] = []

    for pop in populations_to_test:
        pop_df = df[df["population"] == pop].set_index("pair")
        if pop_df.empty:
            print(f"  {pop:<18}  — no data")
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

        # Coverage guard applies only to the primary bb_widening filter.
        if pop == "bb_widening":
            regime_n = baseline["n_base"]
            coverage = joined["n_trades"] / regime_n
            joined["coverage_ok"] = coverage >= config.min_coverage_ratio
        else:
            joined["coverage_ok"] = True

        joined["pair_passes"] = (
            (joined["wr_lift"] > joined["min_wr_lift"])
            & (joined["pf_lift"] > joined["min_pf_lift"])
            & (joined["n_trades"] > config.min_trades_per_pair)
            & (joined["profit_factor"] > joined["pf_base"])
            & joined["coverage_ok"]
        )

        n_pairs = len(joined)
        n_passing = int(joined["pair_passes"].sum())
        avg_pf = joined["profit_factor"].mean()
        avg_wr_lift = joined["wr_lift"].mean() * 100
        avg_pf_lift = joined["pf_lift"].mean()
        overall = n_passing >= config.min_pairs_passing
        status = "✅" if overall else "❌"

        print(
            f"  {pop:<18}  avg WR lift {avg_wr_lift:+.2f}pp  avg PF {avg_pf:.3f}"
            f"  avg PF lift {avg_pf_lift:+.3f}"
            f"  pairs ≥ threshold: {n_passing}/{n_pairs}  {status}"
        )

        for pair, row in joined.iterrows():
            pair_status = "✅" if row["pair_passes"] else "❌"
            cov_note = ""
            if pop == "bb_widening" and pair in baseline.index:
                pair_cov = row["n_trades"] / baseline.loc[pair, "n_base"]
                cov_note = f"  cov {pair_cov * 100:.1f}%" + (" ⚠️" if not row["coverage_ok"] else "")
            print(
                f"    {pair:<10}  WR {row['win_rate'] * 100:.2f}%  "
                f"lift {row['wr_lift'] * 100:+.2f}pp / req {row['min_wr_lift'] * 100:.2f}pp  "
                f"PF {row['profit_factor']:.3f}  lift {row['pf_lift']:+.3f} / req {row['min_pf_lift']:.3f}  "
                f"trades {int(row['n_trades']):,}{cov_note}  {pair_status}"
            )
        print()

        if overall:
            passing.append((pop, avg_pf))

    print(
        f"  Thresholds: WR lift > 2.5×sqrt(p(1-p)/n),  "
        f"PF lift > 0.02/0.05/0.10 by n,  "
        f"trades > {config.min_trades_per_pair:,},  "
        f"consistent across ≥ {config.min_pairs_passing} of {len(config.pairs)} pairs"
    )
    print()

    _print_final_verdict(passing, config)


def _print_final_verdict(passing: list[tuple[str, float]], config: TestConfig) -> None:
    if not passing:
        print("  ❌  BB WIDENING SETUP EDGE NOT CONFIRMED — no population clears all thresholds.")
        print("      Next steps:")
        print("        • Adjust bb_period (try 10 or 30)")
        print("        • Adjust bb_std_mult (try 1.5× or 2.5×)")
        print("        • Try a different entry_tf in config.py")
        print("        • Re-examine whether setup layer is needed before trigger layer")
        print()
        return

    print("  ✅  BB WIDENING SETUP EDGE CONFIRMED — expanding bands create predictive edge.")
    pop_names = {p for p, _ in passing}
    best_pop, best_pf = max(passing, key=lambda x: x[1])
    print(f"      Best performer: {best_pop}  (avg PF {best_pf:.3f})")
    print("      Proceed to Step 3 (volume trigger confirmation).")
    print()

    has_widening = "bb_widening" in pop_names
    has_bearish = "bb_widening_bearish" in pop_names
    has_breakout = "bb_widening_breakout" in pop_names

    print("  ── Component Decision ──")
    if has_bearish and has_breakout:
        pf_bearish = next(pf for p, pf in passing if p == "bb_widening_bearish")
        pf_breakout = next(pf for p, pf in passing if p == "bb_widening_breakout")
        if pf_breakout >= pf_bearish:
            print(f"      bb_widening_breakout (PF {pf_breakout:.3f}) ≥ bb_widening_bearish (PF {pf_bearish:.3f})")
            print("      → Edge concentrated in full lower-band breaks during volatility expansion.")
            print("        Carry bb_widening_breakout to Step 3.")
        else:
            print(f"      bb_widening_bearish (PF {pf_bearish:.3f}) > bb_widening_breakout (PF {pf_breakout:.3f})")
            print("      → Lower-band break over-filters; price below basis is sufficient.")
            print("        Carry bb_widening_bearish to Step 3 for larger trade count.")
    elif has_breakout and not has_bearish:
        print("      Only bb_widening_breakout passes.")
        print("      → Full lower-band break required during widening; carry to Step 3.")
    elif has_bearish and not has_breakout:
        print("      Only bb_widening_bearish passes; bb_widening_breakout does not.")
        print("      → Lower-band break is over-restrictive; carry bb_widening_bearish to Step 3.")
    elif has_widening and not has_bearish and not has_breakout:
        print("      Only bb_widening (no price-position filter) passes.")
        print("      → Widening alone is sufficient; carry bb_widening to Step 3.")
    print()


if __name__ == "__main__":
    main()
