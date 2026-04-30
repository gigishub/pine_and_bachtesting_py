"""CLI entry point for Step 2b — Caution Exclusion Filter.

Usage:
    source .venv/bin/activate
    python -m bear_strategy.hypothesis_tests.caution_exclusion_check.run

Timeframe (set entry_tf in config.py):
    "1h"  — swing shorts, 4–48 h holds  ← default
    "15m" — intraday scalps
    "4h"  — position shorts

Result files (stem encodes all exit parameters):
    step2b_caution_results_entry{entry_tf}_sl{stop_atr_mult}_tp{target_atr_mult}_atr{atr_period}.csv
    step2b_caution_results_entry{entry_tf}_sl{stop_atr_mult}_tp{target_atr_mult}_atr{atr_period}.md

──────────────────────────────────────────────────────────────────────
What is being tested
──────────────────────────────────────────────────────────────────────
Within EMA-50 confirmed bear regime bars (Step 1 winner), test whether
excluding "caution" bars improves short-entry quality.

    is_caution = (close > EMA(close, 20))      ← reclaiming local EMA
                 OR (range7 > ATR(7) × 1.5)    ← choppy, not trending

    range7 = High − min(Low, last 7 bars)      ← recent swing magnitude

Populations compared against the regime_only baseline:
    ema20_filter — removes only EMA-reclaim bars
    range_filter — removes only wide-range (choppy) bars
    no_caution   — removes both types (full exclusion)

──────────────────────────────────────────────────────────────────────
Pass/fail criteria (from spec)
──────────────────────────────────────────────────────────────────────
For each pair:
    wr_lift  > 2.5 × sqrt(p × (1-p) / n)   where p = baseline WR
    pf_lift  > noise_floor(n)               (0.02/0.05/0.10 by n tier)
    n_trades > min_trades_per_pair
    no_caution keeps ≥ 40% of eligible regime bars (by mask count, not n_trades)

Overall PASS: no_caution clears all thresholds on ≥ 4 of 5 pairs.

Regime filter: ema_below_50 (Step 1 winner).
See: bear_strategy/backtest/hypothesis_tests_raw/results/step1_regime_check/
"""

from __future__ import annotations

import logging
import math
import sys

import numpy as np
import pandas as pd

from bear_strategy.hypothesis_tests.caution_exclusion_check.config import TestConfig
from bear_strategy.hypothesis_tests.caution_exclusion_check.runner import run_test
from bear_strategy.hypothesis_tests.report_writer import capture_prints, save_report, run_stem, _fmt_param

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def main() -> None:
    config = TestConfig()

    logger.info("=" * 70)
    logger.info("Bear Strategy — Step 2b: Caution Exclusion Filter")
    logger.info("Entry TF     : %s  |  Regime TF: 1d (daily, fixed)", config.entry_tf)
    logger.info("Regime       : %s (Step 1 winner)", config.regime_col)
    logger.info("Pairs        : %s", config.pairs)
    logger.info(
        "EMA20 period : %d  |  Range period: %d  |  Range mult: %.1f×",
        config.ema20_period, config.range_period, config.range_atr_mult,
    )
    logger.info(
        "Stop : %.1f× ATR(%s,%d)  |  Target: %.1f× ATR(%s,%d)",
        config.stop_atr_mult, config.entry_tf, config.atr_period,
        config.target_atr_mult, config.entry_tf, config.atr_period,
    )
    logger.info("Pass threshold: ≥ %d of %d pairs", config.min_pairs_passing, len(config.pairs))
    logger.info(
        "Coverage guard: no_caution must keep ≥ %.0f%% of regime bars",
        config.min_coverage_ratio * 100,
    )
    logger.info("=" * 70)

    results = run_test(config)

    if results.empty:
        logger.error("No results — check parquet data availability.")
        sys.exit(1)

    stem = run_stem(config.entry_tf, config.stop_atr_mult, config.target_atr_mult, config.atr_period,
                    extra=f"ema{config.ema20_period}")
    _config_params = {
        "entry_tf": config.entry_tf,
        "stop_atr_mult": config.stop_atr_mult,
        "target_atr_mult": config.target_atr_mult,
        "atr_period": config.atr_period,
        "ema20_period": config.ema20_period,
        "range_period": config.range_period,
        "range_atr_mult": config.range_atr_mult,
    }

    pop_display = {"ema20_filter": f"ema{config.ema20_period}_filter"}

    with capture_prints() as cap:
        _print_summary(results, config, pop_display)
        _save_results(results, config, stem)
        _print_verdict(results, config, pop_display)

    md_path = config.results_dir / f"step2b_caution_results_{stem}.md"
    actual_path = save_report(
        cap.text,
        md_path,
        f"Bear Strategy — Step 2b: Caution Exclusion Filter  (entry_tf={config.entry_tf})",
        config_params=_config_params,
    )
    logger.info("Analysis report saved → %s", actual_path)


# ---------------------------------------------------------------------------
# Reporting helpers
# ---------------------------------------------------------------------------


def _print_summary(results: pd.DataFrame, config: TestConfig, pop_display: dict[str, str]) -> None:
    print("\n── Per-Pair Results ──\n")
    df = results.reset_index()

    for pair in config.pairs:
        pair_df = df[df["pair"] == pair].set_index("population")
        if pair_df.empty:
            continue

        print(f"  {pair}")
        ordered = [p for p in _POPULATION_ORDER if p in pair_df.index]
        subset = pair_df.reindex(ordered).copy()
        subset.index = [pop_display.get(p, p) for p in subset.index]
        subset["wr_%"] = (subset["win_rate"] * 100).round(2)
        subset["pf"] = subset["profit_factor"].round(3)
        subset["dur"] = subset["avg_duration"].round(1)

        print(subset[["wr_%", "pf", "dur", "n_trades", "mask_count"]].to_string())

        # Coverage uses raw mask_count (not n_trades) per rubber-duck advice.
        regime_bars = pair_df.loc["regime_only", "mask_count"] if "regime_only" in pair_df.index else 0
        nc_bars = pair_df.loc["no_caution", "mask_count"] if "no_caution" in pair_df.index else 0
        if regime_bars > 0:
            coverage = nc_bars / regime_bars
            flag = "⚠️  LOW COVERAGE" if coverage < config.min_coverage_ratio else ""
            print(f"    no_caution keeps {coverage * 100:.1f}% of regime bars  {flag}")
        print()


_POPULATION_ORDER = ["regime_only", "ema20_filter", "range_filter", "no_caution"]


def _save_results(results: pd.DataFrame, config: TestConfig, stem: str) -> None:
    csv_dir = config.results_dir / "csv"
    csv_dir.mkdir(parents=True, exist_ok=True)
    filename = f"step2b_caution_results_{stem}.csv"
    out = csv_dir / filename
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


def _print_verdict(results: pd.DataFrame, config: TestConfig, pop_display: dict[str, str]) -> None:
    df = results.reset_index()

    baseline_df = df[df["population"] == "regime_only"].set_index("pair")
    if baseline_df.empty:
        logger.error("No regime_only rows — cannot compute verdict.")
        return

    baseline = baseline_df[["win_rate", "profit_factor", "n_trades", "mask_count"]].rename(
        columns={
            "win_rate": "wr_base",
            "profit_factor": "pf_base",
            "n_trades": "n_base",
            "mask_count": "mask_base",
        }
    )

    avg_base_wr = baseline["wr_base"].mean()
    avg_base_pf = baseline["pf_base"].mean()

    print("── Caution Exclusion Verdict ──\n")
    print(
        f"  Baseline (regime_only):  avg WR {avg_base_wr * 100:.1f}%  "
        f"avg PF {avg_base_pf:.3f}"
    )
    print()

    populations_to_test = ["ema20_filter", "range_filter", "no_caution"]
    passing: list[str] = []
    all_warnings: list[str] = []

    for pop in populations_to_test:
        pop_df = df[df["population"] == pop].set_index("pair")
        lbl = pop_display.get(pop, pop)
        if pop_df.empty:
            print(f"  {lbl:<14}  — no data")
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

        # Coverage check for no_caution only (uses raw mask counts, not n_trades)
        if pop == "no_caution":
            coverage = joined["mask_count"] / baseline["mask_base"]
            joined["coverage_ok"] = coverage >= config.min_coverage_ratio
        else:
            joined["coverage_ok"] = True

        joined["pair_passes"] = (
            (joined["pf_lift"] > joined["min_pf_lift"])
            & (joined["profit_factor"] > joined["pf_base"])
        )

        n_pairs = len(joined)
        n_passing = int(joined["pair_passes"].sum())
        avg_pf = joined["profit_factor"].mean()
        avg_wr_lift = joined["wr_lift"].mean() * 100
        avg_pf_lift = joined["pf_lift"].mean()
        overall = n_passing >= config.min_pairs_passing
        status = "✅" if overall else "❌"

        # Population-level warnings
        wr_lift_pairs = [p for p in joined.index if joined.loc[p, "wr_lift"] <= joined.loc[p, "min_wr_lift"]]
        low_count_pairs = [p for p in joined.index if joined.loc[p, "n_trades"] / baseline.loc[p, "n_base"] < 0.30]
        weak_regime_pairs = [p for p in joined.index if baseline.loc[p, "pf_base"] < 1.1]
        if wr_lift_pairs:
            all_warnings.append(f"⚠️  [{pop}] WR lift below threshold on: {', '.join(str(p) for p in wr_lift_pairs)}")
        if low_count_pairs:
            all_warnings.append(f"⚠️  [{pop}] low trade count (<30% of regime) on: {', '.join(str(p) for p in low_count_pairs)}")
        if weak_regime_pairs:
            all_warnings.append(f"⚠️  [{pop}] weak regime baseline (PF < 1.1) on: {', '.join(str(p) for p in weak_regime_pairs)}")

        warn_tags = []
        if wr_lift_pairs:
            warn_tags.append(f"⚠️ WR {len(wr_lift_pairs)}p")
        if low_count_pairs:
            warn_tags.append(f"⚠️ low count {len(low_count_pairs)}p")
        if weak_regime_pairs:
            warn_tags.append(f"⚠️ weak regime {len(weak_regime_pairs)}p")
        warn_str = ("  " + "  ".join(warn_tags)) if warn_tags else ""

        print(
            f"  {lbl:<14}  avg WR lift {avg_wr_lift:+.2f}pp  avg PF {avg_pf:.3f}"
            f"  avg PF lift {avg_pf_lift:+.3f}"
            f"  pairs ≥ threshold: {n_passing}/{n_pairs}  {status}{warn_str}"
        )

        for pair, row in joined.iterrows():
            pair_status = "✅" if row["pair_passes"] else "❌"
            cov_note = ""
            if pop == "no_caution":
                pair_cov = row["mask_count"] / baseline.loc[pair, "mask_base"] if pair in baseline.index else float("nan")
                cov_note = f"  cov {pair_cov * 100:.1f}%" + (" ⚠️" if not row["coverage_ok"] else "")
            wr_note = "  ⚠️ WR" if row["wr_lift"] <= row["min_wr_lift"] else ""
            print(
                f"    {pair:<10}  WR {row['win_rate'] * 100:.2f}%  "
                f"lift {row['wr_lift'] * 100:+.2f}pp / req {row['min_wr_lift'] * 100:.2f}pp  "
                f"PF {row['profit_factor']:.3f}  lift {row['pf_lift']:+.3f} / req {row['min_pf_lift']:.3f}  "
                f"trades {int(row['n_trades']):,}{cov_note}{wr_note}  {pair_status}"
            )
        print()

        if overall:
            passing.append(pop)

    print(
        f"  Thresholds: WR lift > 2.5×sqrt(p(1-p)/n),  "
        f"PF lift > 0.02/0.05/0.10 by n,  "
        f"consistent across ≥ {config.min_pairs_passing} of {len(config.pairs)} pairs"
    )
    print()

    _print_final_verdict(passing, config, pop_display, all_warnings)


def _print_final_verdict(passing: list[str], config: TestConfig, pop_display: dict[str, str], warnings: list[str]) -> None:
    no_caution_passes = "no_caution" in passing
    ema20_passes = "ema20_filter" in passing
    range_passes = "range_filter" in passing
    ema_lbl = pop_display.get("ema20_filter", "ema20_filter")

    if no_caution_passes:
        print("  ✅  CAUTION EXCLUSION CONFIRMED — filtering out high-caution bars improves edge.")
        print()

        if warnings:
            print("      Warnings (results valid but interpret with care):")
            for w in warnings:
                print(f"        {w}")

        print("  ── Component Attribution ──")
        if ema20_passes and range_passes:
            print("      Both conditions pass individually → both contribute.")
            print("      Carry full no_caution filter to Step 3.")
        elif ema20_passes and not range_passes:
            print(f"      {ema_lbl} passes; range_filter does not.")
            print("      → EMA reclaim bars are the primary noise source.")
            print("        Range condition adds modest marginal value.")
            print(f"        Consider {ema_lbl} alone for more trade count in Step 3.")
        elif range_passes and not ema20_passes:
            print(f"      range_filter passes; {ema_lbl} does not.")
            print("      → Wide-range/chop bars are the primary noise source.")
            print("        EMA-20 condition adds modest marginal value.")
            print("        Consider range_filter alone for more trade count in Step 3.")
        else:
            # Both components fail individually but no_caution passes — synergy
            print("      Neither component passes alone — combined exclusion is synergistic.")
            print("      Carry full no_caution filter to Step 3.")
        print()
        print("  Proceed to Step 3 (volume trigger confirmation).")
        print()
        return

    print("  ❌  CAUTION EXCLUSION NOT CONFIRMED — no improvement over regime baseline.")
    print()

    # Individual components passing is informative even if no_caution fails
    if ema20_passes:
        print(f"      {ema_lbl} passes individually → try {ema_lbl} as setup layer.")
    if range_passes:
        print("      range_filter passes individually → try range_filter as setup layer.")
    if not ema20_passes and not range_passes:
        print("      No component shows edge — caution exclusion hypothesis rejected.")

    print()
    print("  Next steps:")
    print("    • Adjust range_atr_mult (try 1.2× or 2.0×)")
    print("    • Adjust ema20_period (try 10 or 30)")
    print("    • Try a different entry_tf in config.py")
    print("    • Re-examine whether a setup layer is needed before the trigger layer")
    print()


if __name__ == "__main__":
    main()
