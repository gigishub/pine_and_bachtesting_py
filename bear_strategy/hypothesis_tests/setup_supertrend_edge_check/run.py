"""CLI entry point for Step 2 — SuperTrend Setup Edge Check.

Usage:
    source .venv/bin/activate
    python -m bear_strategy.hypothesis_tests.setup_supertrend_edge_check.run

Timeframe (set entry_tf in config.py):
    "1h"  — swing shorts, 4–48 h holds  ← default
    "15m" — intraday scalps
    "4h"  — position shorts

Result files:
    step2_supertrend_results_entry{entry_tf}.csv
    step2_supertrend_results_entry{entry_tf}.md

──────────────────────────────────────────────────────────────────────
What is being tested
──────────────────────────────────────────────────────────────────────
Within EMA-50 confirmed bear regime bars (Step 1 winner), test whether
SuperTrend direction = −1 creates a measurable edge:

    st_bear = SuperTrend(10, 3.0) direction == −1
              (close is below the ST line → ST line acts as overhead resistance)

Sub-populations decompose where the edge lives:

    st_near_resistance — close within 0.5×ATR of the ST resistance line
    st_extended        — close >0.5×ATR below the ST line

Baseline = regime_only (all eligible regime bars post ST/ATR warmup).

──────────────────────────────────────────────────────────────────────
Pass/fail criteria (from spec)
──────────────────────────────────────────────────────────────────────
For each pair:
    wr_lift  > 2.5 × sqrt(p × (1-p) / n)   where p = baseline WR
    pf_lift  > noise_floor(n)               (0.02/0.05/0.10)
    n_trades > 1 000
    st_bear covers ≥ 30% of eligible regime bars

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

from bear_strategy.hypothesis_tests.report_writer import capture_prints, save_report
from bear_strategy.hypothesis_tests.setup_supertrend_edge_check.config import TestConfig
from bear_strategy.hypothesis_tests.setup_supertrend_edge_check.runner import run_test

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def main() -> None:
    config = TestConfig()

    logger.info("=" * 70)
    logger.info("Bear Strategy — Step 2: SuperTrend Setup Edge Check")
    logger.info("Entry TF     : %s  |  Regime TF: 1d (daily, fixed)", config.entry_tf)
    logger.info("Regime       : %s (Step 1 winner)", config.regime_col)
    logger.info("Pairs        : %s", config.pairs)
    logger.info(
        "SuperTrend   : length=%d  multiplier=%.1f  proximity=%.2f×ATR",
        config.st_length,
        config.st_multiplier,
        config.proximity_atr_mult,
    )
    logger.info(
        "Stop : %.1f× ATR(%s,%d)  |  Target: %.1f× ATR(%s,%d)",
        config.stop_atr_mult, config.entry_tf, config.atr_period,
        config.target_atr_mult, config.entry_tf, config.atr_period,
    )
    logger.info("Pass threshold: ≥ %d of %d pairs", config.min_pairs_passing, len(config.pairs))
    logger.info(
        "Coverage guard: st_bear must keep ≥ %.0f%% of regime bars",
        config.min_coverage_ratio * 100,
    )
    logger.info("=" * 70)

    results = run_test(config)

    if results.empty:
        logger.error("No results — check parquet data availability.")
        sys.exit(1)

    with capture_prints() as buf:
        _print_summary(results, config)
        _save_results(results, config)
        _print_verdict(results, config)

    md_path = config.results_dir / f"step2_supertrend_results_entry{config.entry_tf}.md"
    save_report(buf.text, md_path, title="SuperTrend Setup Edge Check")


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
        ordered = [
            p for p in ["regime_only", "st_bear", "st_near_resistance", "st_extended"]
            if p in pair_df.index
        ]
        subset = pair_df.reindex(ordered).copy()
        subset["wr_%"] = (subset["win_rate"] * 100).round(2)
        subset["pf"] = subset["profit_factor"].round(3)
        subset["dur"] = subset["avg_duration"].round(1)

        print(subset[["wr_%", "pf", "dur", "n_trades"]].to_string())

        # Coverage check inline.
        regime_n = pair_df.loc["regime_only", "n_trades"] if "regime_only" in pair_df.index else 0
        st_n = pair_df.loc["st_bear", "n_trades"] if "st_bear" in pair_df.index else 0
        if regime_n > 0:
            coverage = st_n / regime_n
            coverage_flag = "⚠️  LOW COVERAGE" if coverage < config.min_coverage_ratio else ""
            print(f"    st_bear covers {coverage * 100:.1f}% of regime bars  {coverage_flag}")
        print()


def _save_results(results: pd.DataFrame, config: TestConfig) -> None:
    config.results_dir.mkdir(parents=True, exist_ok=True)
    filename = f"step2_supertrend_results_entry{config.entry_tf}.csv"
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

    print("── SuperTrend Setup Edge Verdict ──\n")
    print(
        f"  Baseline (regime_only):  avg WR {avg_base_wr * 100:.1f}%  "
        f"avg PF {avg_base_pf:.3f}"
    )
    print()

    populations_to_test = ["st_bear", "st_near_resistance", "st_extended"]
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

        # Coverage guard applies only to the primary st_bear filter.
        if pop == "st_bear":
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
            f"  {pop:<20}  avg WR lift {avg_wr_lift:+.2f}pp  avg PF {avg_pf:.3f}"
            f"  avg PF lift {avg_pf_lift:+.3f}"
            f"  pairs ≥ threshold: {n_passing}/{n_pairs}  {status}"
        )

        for pair, row in joined.iterrows():
            pair_status = "✅" if row["pair_passes"] else "❌"
            cov_note = ""
            if pop == "st_bear" and pair in baseline.index:
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
        print("  ❌  SUPERTREND SETUP EDGE NOT CONFIRMED — no population clears all thresholds.")
        print("      Next steps:")
        print("        • Adjust st_length (try 7 or 14)")
        print("        • Adjust st_multiplier (try 2.0 or 4.0)")
        print("        • Adjust proximity_atr_mult (try 1.0 or 0.25)")
        print("        • Try a different entry_tf in config.py")
        print("        • Re-examine whether setup layer is needed before trigger layer")
        print()
        return

    print("  ✅  SUPERTREND SETUP EDGE CONFIRMED — ST direction adds predictive edge.")
    pop_names = {p for p, _ in passing}
    best_pop, best_pf = max(passing, key=lambda x: x[1])
    print(f"      Best performer: {best_pop}  (avg PF {best_pf:.3f})")
    print("      Proceed to Step 3 (volume trigger confirmation).")
    print()

    # Component attribution guidance.
    has_bear = "st_bear" in pop_names
    has_near = "st_near_resistance" in pop_names
    has_ext = "st_extended" in pop_names

    print("  ── Component Decision ──")
    if has_near and has_ext:
        pf_near = next(pf for p, pf in passing if p == "st_near_resistance")
        pf_ext = next(pf for p, pf in passing if p == "st_extended")
        if pf_near > pf_ext:
            print(f"      st_near_resistance (PF {pf_near:.3f}) > st_extended (PF {pf_ext:.3f})")
            print("      → Edge concentrates at/near the ST resistance line (overhead supply).")
            print("        Carry st_near_resistance forward; require close within 0.5×ATR of ST.")
        else:
            print(f"      st_extended (PF {pf_ext:.3f}) > st_near_resistance (PF {pf_near:.3f})")
            print("      → Edge concentrates in momentum continuation, not near the resistance.")
            print("        Carry st_extended (or full st_bear) forward to Step 3.")
    elif has_near and not has_ext:
        print("      Only st_near_resistance passes; st_extended does not.")
        print("      → Require close within 0.5×ATR of ST line for Step 3.")
    elif has_ext and not has_near:
        print("      Only st_extended passes; st_near_resistance does not.")
        print("      → Proximity to resistance doesn't help; carry st_extended to Step 3.")
    elif has_bear and not has_near and not has_ext:
        print("      Only st_bear (full directional filter) passes.")
        print("      → Carry st_bear as-is; proximity decomposition is not informative here.")
    print()


if __name__ == "__main__":
    main()
