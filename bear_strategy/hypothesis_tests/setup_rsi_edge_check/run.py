"""CLI entry point for the RSI Setup Edge Check.

Usage:
    source .venv/bin/activate
    python -m bear_strategy.hypothesis_tests.setup_rsi_edge_check.run

Timeframe (set entry_tf in config.py):
    "1h"  — swing shorts, 4–48 h holds  ← default
    "15m" — intraday scalps
    "4h"  — position shorts

Result files:
    step2_rsi_results_entry{entry_tf}_sl{stop_atr_mult}_tp{target_atr_mult}_atr{atr_period}.csv
    step2_rsi_results_entry{entry_tf}_sl{stop_atr_mult}_tp{target_atr_mult}_atr{atr_period}.md   ← full analysis report

──────────────────────────────────────────────────────────────────────
What is being tested
──────────────────────────────────────────────────────────────────────
Within EMA-50 confirmed bear regime bars (Step 1 winner), test whether
requiring RSI to be in the bearish-but-not-oversold zone creates edge:

    rsi_30_50 = RSI(rsi_period) > rsi_lower   ← exclude oversold bars
                AND RSI(rsi_period) < rsi_upper ← exclude neutral/overbought

Hypothesis: oversold bars (RSI < 30) are likely to bounce and make poor
short entries; bars above RSI 50 are not yet in a confirmed bearish
momentum phase.  The [30, 50] window targets the "falling knife" zone
where downward momentum is active but not exhausted.

Baseline = regime_only (all eligible regime bars post-warmup).
Decomposition populations to isolate which boundary drives the edge:
    rsi_below_50 — only the upper cap (no oversold exclusion)
    rsi_above_30 — only the oversold exclusion (no upper cap)

──────────────────────────────────────────────────────────────────────
Pass/fail criteria
──────────────────────────────────────────────────────────────────────
For each pair:
    wr_lift  > 2.5 × sqrt(p × (1-p) / n)   where p = baseline WR
    pf_lift  > noise_floor(n)               (0.02/0.05/0.10)
    n_trades > min_trades_per_pair
    rsi_30_50 covers ≥ 20% of eligible regime bars

Overall PASS: ≥ 4 of 5 pairs clear all thresholds.

Regime filter: ema_below_50 (Step 1 winner).
"""

from __future__ import annotations

import logging
import math
import sys

import numpy as np
import pandas as pd

from bear_strategy.hypothesis_tests.report_writer import capture_prints, save_report, run_stem, _fmt_param
from bear_strategy.hypothesis_tests.setup_rsi_edge_check.config import TestConfig
from bear_strategy.hypothesis_tests.setup_rsi_edge_check.runner import run_test

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def main() -> None:
    config = TestConfig()

    rsi_zone_lbl = f"rsi_{_fmt_param(config.rsi_lower)}_{_fmt_param(config.rsi_upper)}"
    rsi_below_lbl = f"rsi_below_{_fmt_param(config.rsi_upper)}"
    rsi_above_lbl = f"rsi_above_{_fmt_param(config.rsi_lower)}"
    pop_display = {
        "rsi_30_50": rsi_zone_lbl,
        "rsi_below_50": rsi_below_lbl,
        "rsi_above_30": rsi_above_lbl,
    }

    logger.info("=" * 70)
    logger.info("Bear Strategy — RSI Setup Edge Check")
    logger.info("Entry TF     : %s  |  Regime TF: 1d (daily, fixed)", config.entry_tf)
    logger.info("Regime       : %s (Step 1 winner)", config.regime_col)
    logger.info("Pairs        : %s", config.pairs)
    logger.info(
        "RSI          : period=%d  zone=(%.0f, %.0f)",
        config.rsi_period, config.rsi_lower, config.rsi_upper,
    )
    logger.info(
        "Stop : %.1f× ATR(%s,%d)  |  Target: %.1f× ATR(%s,%d)",
        config.stop_atr_mult, config.entry_tf, config.atr_period,
        config.target_atr_mult, config.entry_tf, config.atr_period,
    )
    logger.info("Pass threshold: ≥ %d of %d pairs", config.min_pairs_passing, len(config.pairs))
    logger.info(
        "Coverage guard: %s must keep ≥ %.0f%% of regime bars",
        rsi_zone_lbl, config.min_coverage_ratio * 100,
    )
    logger.info("=" * 70)

    results = run_test(config)

    if results.empty:
        logger.error("No results — check parquet data availability.")
        sys.exit(1)

    stem = run_stem(config.entry_tf, config.stop_atr_mult, config.target_atr_mult, config.atr_period,
                    extra=f"rsi{config.rsi_period}_{_fmt_param(config.rsi_lower)}_{_fmt_param(config.rsi_upper)}")
    _config_params = {
        "entry_tf": config.entry_tf,
        "stop_atr_mult": config.stop_atr_mult,
        "target_atr_mult": config.target_atr_mult,
        "atr_period": config.atr_period,
        "rsi_period": config.rsi_period,
        "rsi_lower": config.rsi_lower,
        "rsi_upper": config.rsi_upper,
    }

    report_path = config.results_dir / f"step2_rsi_results_{stem}.md"

    with capture_prints() as cap:
        _print_summary(results, config, pop_display)
        _save_results(results, config, stem)
        _print_verdict(results, config, pop_display)

    actual_path = save_report(
        cap.text,
        report_path,
        f"Bear Strategy — RSI Setup Edge Check  (entry_tf={config.entry_tf})",
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
        ordered = [p for p in ["regime_only", "rsi_30_50", "rsi_below_50", "rsi_above_30"] if p in pair_df.index]
        subset = pair_df.reindex(ordered).copy()
        subset.index = [pop_display.get(p, p) for p in subset.index]
        subset["wr_%"] = (subset["win_rate"] * 100).round(2)
        subset["pf"] = subset["profit_factor"].round(3)
        subset["dur"] = subset["avg_duration"].round(1)

        print(subset[["wr_%", "pf", "dur", "n_trades"]].to_string())

        # Coverage: primary zone vs regime_only bar count.
        regime_n = pair_df.loc["regime_only", "n_trades"] if "regime_only" in pair_df.index else 0
        rsi_n = pair_df.loc["rsi_30_50", "n_trades"] if "rsi_30_50" in pair_df.index else 0
        if regime_n > 0:
            coverage = rsi_n / regime_n
            flag = "⚠️  LOW COVERAGE" if coverage < config.min_coverage_ratio else ""
            print(f"    {pop_display.get('rsi_30_50', 'rsi_30_50')} covers {coverage * 100:.1f}% of regime bars  {flag}")
        print()


def _save_results(results: pd.DataFrame, config: TestConfig, stem: str) -> None:
    csv_dir = config.results_dir / "csv"
    csv_dir.mkdir(parents=True, exist_ok=True)
    filename = f"step2_rsi_results_{stem}.csv"
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

    baseline = baseline_df[["win_rate", "profit_factor", "n_trades"]].rename(
        columns={"win_rate": "wr_base", "profit_factor": "pf_base", "n_trades": "n_base"}
    )

    avg_base_wr = baseline["wr_base"].mean()
    avg_base_pf = baseline["pf_base"].mean()

    print("── RSI Setup Edge Verdict ──\n")
    print(
        f"  Baseline (regime_only):  avg WR {avg_base_wr * 100:.1f}%  "
        f"avg PF {avg_base_pf:.3f}"
    )
    print()

    populations_to_test = ["rsi_30_50", "rsi_below_50", "rsi_above_30"]
    passing: list[tuple[str, float]] = []
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

        # Coverage check only for the primary population.
        if pop == "rsi_30_50":
            coverage = joined["n_trades"] / baseline["n_base"]
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
            if pop == "rsi_30_50":
                pair_cov = row["n_trades"] / baseline.loc[pair, "n_base"] if pair in baseline.index else float("nan")
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
            passing.append((pop, avg_pf))

    print(
        f"  Thresholds: WR lift > 2.5×sqrt(p(1-p)/n),  "
        f"PF lift > 0.02/0.05/0.10 by n,  "
        f"consistent across ≥ {config.min_pairs_passing} of {len(config.pairs)} pairs"
    )
    print()

    _print_final_verdict(passing, config, pop_display, all_warnings)


def _print_final_verdict(passing: list[tuple[str, float]], config: TestConfig, pop_display: dict[str, str], warnings: list[str]) -> None:
    if not passing:
        print("  ❌  RSI SETUP EDGE NOT CONFIRMED — no RSI population clears all thresholds.")
        print("      Next steps:")
        print("        • Adjust rsi_upper (try 45 or 55)")
        print("        • Adjust rsi_lower (try 20 or 35)")
        print("        • Adjust rsi_period (try 7 or 21)")
        print("        • Try a different entry_tf in config.py")
        print()
        return

    print("  ✅  RSI SETUP EDGE CONFIRMED — RSI zone creates a measurable edge.")
    pop_names = {p for p, _ in passing}
    best_pop, best_pf = max(passing, key=lambda x: x[1])
    print(f"      Best performer: {pop_display.get(best_pop, best_pop)}  (avg PF {best_pf:.3f})")
    if warnings:
        print("      Warnings (results valid but interpret with care):")
        for w in warnings:
            print(f"        {w}")
    print("      Proceed to Step 3 (volume trigger confirmation).")
    print()

    zone_lbl = pop_display.get("rsi_30_50", "rsi_30_50")
    upper_lbl = pop_display.get("rsi_below_50", "rsi_below_50")
    lower_lbl = pop_display.get("rsi_above_30", "rsi_above_30")

    print("  ── Boundary Attribution ──")
    has_both = "rsi_30_50" in pop_names
    has_upper = "rsi_below_50" in pop_names
    has_lower = "rsi_above_30" in pop_names

    if has_both and has_upper and has_lower:
        pf_both = next(pf for p, pf in passing if p == "rsi_30_50")
        pf_upper = next(pf for p, pf in passing if p == "rsi_below_50")
        pf_lower = next(pf for p, pf in passing if p == "rsi_above_30")
        if pf_both >= max(pf_upper, pf_lower):
            print(f"      Combined zone [{zone_lbl}] is strongest → keep both boundaries.")
        elif pf_upper > pf_lower:
            print(f"      {upper_lbl} (PF {pf_upper:.3f}) > {lower_lbl} (PF {pf_lower:.3f})")
            print("      → RSI < cap drives the edge; the RSI > floor adds little.")
            print(f"        Consider {upper_lbl} for Step 3 to preserve more trade count.")
        else:
            print(f"      {lower_lbl} (PF {pf_lower:.3f}) > {upper_lbl} (PF {pf_upper:.3f})")
            print("      → Oversold exclusion (RSI > floor) drives the edge; upper cap adds little.")
            print(f"        Consider {lower_lbl} for Step 3 to preserve more trade count.")
    elif has_both and not has_upper and not has_lower:
        print(f"      Only the combined zone [{zone_lbl}] passes — both boundaries required together.")
    elif has_upper and not has_both:
        print(f"      {upper_lbl} passes; {zone_lbl} does not.")
        print(f"      → RSI > floor is over-restrictive; use {upper_lbl} for Step 3.")
    elif has_lower and not has_both:
        print(f"      {lower_lbl} passes; {zone_lbl} does not.")
        print(f"      → RSI < cap is over-restrictive; use {lower_lbl} for Step 3.")
    print()


if __name__ == "__main__":
    main()
