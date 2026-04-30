"""CLI entry point for the BB Range Setup Edge Check.

Usage:
    source .venv/bin/activate
    python -m bear_strategy.hypothesis_tests.setup_bb_range_edge_check.run

Timeframe (set entry_tf in config.py):
    "1h"  — swing shorts, 4–48 h holds  ← default
    "15m" — intraday scalps
    "4h"  — position shorts

Result files:
    step2_bb_range_results_entry{entry_tf}.csv
    step2_bb_range_results_entry{entry_tf}.md   ← full analysis report

──────────────────────────────────────────────────────────────────────
What is being tested
──────────────────────────────────────────────────────────────────────
Within EMA-50 confirmed bear regime bars (Step 1 winner), test whether
entries where close is WITHIN the Bollinger Bands produce better edge:

    price_in_bands = close >= BB_lower(bb_period, bb_std_mult)
                     AND close <= BB_upper(bb_period, bb_std_mult)

Hypothesis: when price has already broken below the lower band it is
statistically overextended and prone to mean-reversion bounces, making
it a poor short entry.  Entries within the band envelope still have the
full statistical range available before the market becomes overextended.

This is the complement of setup_bb_edge_check (which tests close <
BB_lower).  Comparing both tests answers: which zone has more edge —
inside-the-bands or broken-below-the-lower-band?

Baseline = regime_only (all eligible regime bars post-warmup).
Decomposition populations to isolate which boundary drives the edge:
    below_upper — only the upper cap (close ≤ BB_upper, no lower floor)
    above_lower — only the lower floor (close ≥ BB_lower, no upper cap)

──────────────────────────────────────────────────────────────────────
Pass/fail criteria
──────────────────────────────────────────────────────────────────────
For each pair:
    wr_lift  > 2.5 × sqrt(p × (1-p) / n)   where p = baseline WR
    pf_lift  > noise_floor(n)               (0.02/0.05/0.10)
    n_trades > min_trades_per_pair
    price_in_bands covers ≥ 40% of eligible regime bars

Overall PASS: ≥ 4 of 5 pairs clear all thresholds.

Regime filter: ema_below_50 (Step 1 winner).
"""

from __future__ import annotations

import logging
import math
import sys

import numpy as np
import pandas as pd

from bear_strategy.hypothesis_tests.report_writer import capture_prints, save_report
from bear_strategy.hypothesis_tests.setup_bb_range_edge_check.config import TestConfig
from bear_strategy.hypothesis_tests.setup_bb_range_edge_check.runner import run_test

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def main() -> None:
    config = TestConfig()

    logger.info("=" * 70)
    logger.info("Bear Strategy — BB Range Setup Edge Check")
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
    logger.info(
        "Coverage guard: price_in_bands must keep ≥ %.0f%% of regime bars",
        config.min_coverage_ratio * 100,
    )
    logger.info("=" * 70)

    results = run_test(config)

    if results.empty:
        logger.error("No results — check parquet data availability.")
        sys.exit(1)

    report_path = config.results_dir / f"step2_bb_range_results_entry{config.entry_tf}.md"

    with capture_prints() as cap:
        _print_summary(results, config)
        _save_results(results, config)
        _print_verdict(results, config)

    save_report(
        cap.text,
        report_path,
        f"Bear Strategy — BB Range Setup Edge Check  (entry_tf={config.entry_tf})",
    )
    logger.info("Analysis report saved → %s", report_path)


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
        ordered = [p for p in ["regime_only", "price_in_bands", "below_upper", "above_lower"] if p in pair_df.index]
        subset = pair_df.reindex(ordered).copy()
        subset["wr_%"] = (subset["win_rate"] * 100).round(2)
        subset["pf"] = subset["profit_factor"].round(3)
        subset["dur"] = subset["avg_duration"].round(1)

        print(subset[["wr_%", "pf", "dur", "n_trades"]].to_string())

        # Coverage: price_in_bands vs regime_only bar count.
        regime_n = pair_df.loc["regime_only", "n_trades"] if "regime_only" in pair_df.index else 0
        inband_n = pair_df.loc["price_in_bands", "n_trades"] if "price_in_bands" in pair_df.index else 0
        if regime_n > 0:
            coverage = inband_n / regime_n
            flag = "⚠️  LOW COVERAGE" if coverage < config.min_coverage_ratio else ""
            print(f"    price_in_bands covers {coverage * 100:.1f}% of regime bars  {flag}")
        print()


def _save_results(results: pd.DataFrame, config: TestConfig) -> None:
    config.results_dir.mkdir(parents=True, exist_ok=True)
    filename = f"step2_bb_range_results_entry{config.entry_tf}.csv"
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

    print("── BB Range Setup Edge Verdict ──\n")
    print(
        f"  Baseline (regime_only):  avg WR {avg_base_wr * 100:.1f}%  "
        f"avg PF {avg_base_pf:.3f}"
    )
    print()

    populations_to_test = ["price_in_bands", "below_upper", "above_lower"]
    passing: list[tuple[str, float]] = []

    for pop in populations_to_test:
        pop_df = df[df["population"] == pop].set_index("pair")
        if pop_df.empty:
            print(f"  {pop:<16}  — no data")
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

        # Coverage check only for the primary population.
        if pop == "price_in_bands":
            coverage = joined["n_trades"] / baseline["n_base"]
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
            f"  {pop:<16}  avg WR lift {avg_wr_lift:+.2f}pp  avg PF {avg_pf:.3f}"
            f"  avg PF lift {avg_pf_lift:+.3f}"
            f"  pairs ≥ threshold: {n_passing}/{n_pairs}  {status}"
        )

        for pair, row in joined.iterrows():
            pair_status = "✅" if row["pair_passes"] else "❌"
            cov_note = ""
            if pop == "price_in_bands":
                pair_cov = row["n_trades"] / baseline.loc[pair, "n_base"] if pair in baseline.index else float("nan")
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
        print("  ❌  BB RANGE SETUP EDGE NOT CONFIRMED — no in-band population clears all thresholds.")
        print("      Next steps:")
        print("        • Adjust bb_std_mult (try 1.5× or 2.5×)")
        print("        • Adjust bb_period (try 10 or 30)")
        print("        • Compare with setup_bb_edge_check: edge may lie in the broken-below zone")
        print("        • Try a different entry_tf in config.py")
        print()
        return

    print("  ✅  BB RANGE SETUP EDGE CONFIRMED — in-band entries create a measurable edge.")
    pop_names = {p for p, _ in passing}
    best_pop, best_pf = max(passing, key=lambda x: x[1])
    print(f"      Best performer: {best_pop}  (avg PF {best_pf:.3f})")
    print("      Proceed to Step 3 (volume trigger confirmation).")
    print()

    print("  ── Boundary Attribution ──")
    has_both = "price_in_bands" in pop_names
    has_upper = "below_upper" in pop_names
    has_lower = "above_lower" in pop_names

    if has_both and has_upper and has_lower:
        pf_both = next(pf for p, pf in passing if p == "price_in_bands")
        pf_upper = next(pf for p, pf in passing if p == "below_upper")
        pf_lower = next(pf for p, pf in passing if p == "above_lower")
        if pf_both >= max(pf_upper, pf_lower):
            print("      Full in-band condition is strongest → keep both boundaries.")
        elif pf_lower > pf_upper:
            print(f"      above_lower (PF {pf_lower:.3f}) > below_upper (PF {pf_upper:.3f})")
            print("      → BB_lower floor drives the edge; the BB_upper cap adds little.")
            print("        Consider above_lower for Step 3 to preserve more trade count.")
        else:
            print(f"      below_upper (PF {pf_upper:.3f}) > above_lower (PF {pf_lower:.3f})")
            print("      → BB_upper cap drives the edge; the BB_lower floor adds little.")
            print("        Consider below_upper for Step 3 to preserve more trade count.")
    elif has_both and not has_upper and not has_lower:
        print("      Only the full in-band condition passes — both boundaries required together.")
    elif has_upper and not has_both:
        print("      below_upper passes; price_in_bands does not.")
        print("      → BB_lower floor is over-restrictive; use below_upper for Step 3.")
    elif has_lower and not has_both:
        print("      above_lower passes; price_in_bands does not.")
        print("      → BB_upper cap is over-restrictive; use above_lower for Step 3.")
    print()


if __name__ == "__main__":
    main()
