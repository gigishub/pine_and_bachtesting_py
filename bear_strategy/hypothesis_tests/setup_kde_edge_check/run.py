"""CLI entry point for the KDE Price Cluster Edge Check.

Usage:
    source .venv/bin/activate
    python -m bear_strategy.hypothesis_tests.setup_kde_edge_check.run

Key parameters (set in config.py):
    window         — rolling price sample size for KDE (default: 200 bars)
    bandwidth_mult — multiplier on Scott's rule; < 1.0 = sharper peaks,
                     > 1.0 = smoother/broader clusters (default: 1.0)
    kde_n_points   — evaluation grid resolution (default: 500)
    value_area_pct — fraction of density in Value Area band (default: 0.70)
    lower_duration — bars lower filter stays active after POC breach (default: 5)

Result files (in test_results/):
    csv/kde_results_{stem}.csv
    kde_results_{stem}.md

──────────────────────────────────────────────────────────────────────
What is being tested
──────────────────────────────────────────────────────────────────────
Within the EMA-50 bear regime, test whether the KDE Point of Control
(most-traded price level over a rolling window) creates measurable short
entry edges in two structural setups:

  kde_upper       — open > kde_peak:
      Price opens above the dominant cluster.  In a bear regime this is
      a potential mean-reversion short against cluster resistance.

  kde_lower       — close < kde_peak (unrestricted):
      Price closes below the POC — momentum breakdown signal.

  kde_lower_fresh — close < kde_peak AND counter ≤ lower_duration:
      Fresh momentum window only.  Counter resets when price returns
      above the POC.

Baseline = regime_only (all eligible bars once KDE window is full).

──────────────────────────────────────────────────────────────────────
KDE strength
──────────────────────────────────────────────────────────────────────
The KDE derivative is used to count clusters (n_clusters).  A single
dominant cluster (n_clusters == 1) indicates price has been pinned to
one level — a structurally strong POC.  This is printed in the summary
for context but not used as a hard population filter.

──────────────────────────────────────────────────────────────────────
Pass/fail criteria
──────────────────────────────────────────────────────────────────────
For each pair:
    pf_lift  > noise_floor(n)               (0.02 / 0.05 / 0.10)
    profit_factor > regime_baseline PF

Warnings (do not block pass):
    WR lift below threshold
    Trade count < 30% of regime baseline
    Regime baseline PF < 1.1

Overall PASS: ≥ 4 of 5 pairs clear all thresholds.
"""

from __future__ import annotations

import logging
import math
import sys

import pandas as pd

from bear_strategy.hypothesis_tests.report_writer import (
    _fmt_param,
    capture_prints,
    run_stem,
    save_report,
)
from bear_strategy.hypothesis_tests.setup_kde_edge_check.config import TestConfig
from bear_strategy.hypothesis_tests.setup_kde_edge_check.runner import run_test

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def main() -> None:
    config = TestConfig()

    logger.info("=" * 70)
    logger.info("Bear Strategy — KDE Price Cluster Edge Check")
    logger.info("Entry TF      : %s  |  Regime TF: 1d (daily, fixed)", config.entry_tf)
    logger.info("Regime        : %s (Step 1 winner)", config.regime_col)
    logger.info("Pairs         : %s", config.pairs)
    logger.info(
        "KDE           : window=%d  bw_mult=%s  n_points=%d  va_pct=%.0f%%",
        config.window,
        _fmt_param(config.bandwidth_mult),
        config.kde_n_points,
        config.value_area_pct * 100,
    )
    logger.info(
        "Lower filter  : lower_duration=%d bars",
        config.lower_duration,
    )
    logger.info(
        "Stop : %.1f× ATR(%s,%d)  |  Target: %.1f× ATR(%s,%d)",
        config.stop_atr_mult, config.entry_tf, config.atr_period,
        config.target_atr_mult, config.entry_tf, config.atr_period,
    )
    logger.info("Pass threshold: ≥ %d of %d pairs", config.min_pairs_passing, len(config.pairs))
    logger.info("=" * 70)

    results = run_test(config)

    if results.empty:
        logger.error("No results — check parquet data availability.")
        sys.exit(1)

    bw_str = _fmt_param(config.bandwidth_mult)
    stem = run_stem(
        config.entry_tf, config.stop_atr_mult, config.target_atr_mult, config.atr_period,
        extra=f"kde{config.window}_bw{bw_str}_N{config.lower_duration}",
    )
    _config_params = {
        "entry_tf": config.entry_tf,
        "stop_atr_mult": config.stop_atr_mult,
        "target_atr_mult": config.target_atr_mult,
        "atr_period": config.atr_period,
        "window": config.window,
        "bandwidth_mult": config.bandwidth_mult,
        "kde_n_points": config.kde_n_points,
        "value_area_pct": config.value_area_pct,
        "lower_duration": config.lower_duration,
    }

    with capture_prints() as buf:
        _print_summary(results, config)
        _save_results(results, config, stem)
        _print_verdict(results, config)

    md_path = config.results_dir / f"kde_results_{stem}.md"
    save_report(
        buf.text,
        md_path,
        f"Bear Strategy — KDE Price Cluster Edge Check  (entry_tf={config.entry_tf})",
        config_params=_config_params,
    )


# ---------------------------------------------------------------------------
# Reporting helpers
# ---------------------------------------------------------------------------


def _print_summary(results: pd.DataFrame, config: TestConfig) -> None:
    print("\n── Per-Pair Results ──\n")
    df = results.reset_index()
    ordered_pops = ["regime_only", "kde_upper", "kde_lower", "kde_lower_fresh"]

    for pair in config.pairs:
        pair_df = df[df["pair"] == pair].set_index("population")
        if pair_df.empty:
            continue

        print(f"  {pair}")
        ordered = [p for p in ordered_pops if p in pair_df.index]
        subset = pair_df.reindex(ordered).copy()
        subset["wr_%"] = (subset["win_rate"] * 100).round(2)
        subset["pf"] = subset["profit_factor"].round(3)
        subset["dur"] = subset["avg_duration"].round(1)
        print(subset[["wr_%", "pf", "dur", "n_trades"]].to_string())

        regime_n = pair_df.loc["regime_only", "n_trades"] if "regime_only" in pair_df.index else 0
        if regime_n > 0:
            for pop in ["kde_upper", "kde_lower", "kde_lower_fresh"]:
                if pop in pair_df.index:
                    cov = pair_df.loc[pop, "n_trades"] / regime_n
                    flag = "⚠️  LOW" if cov < config.min_coverage_ratio else ""
                    print(f"    {pop} covers {cov * 100:.1f}% of regime bars  {flag}")
        print()


def _save_results(results: pd.DataFrame, config: TestConfig, stem: str) -> None:
    csv_dir = config.results_dir / "csv"
    csv_dir.mkdir(parents=True, exist_ok=True)
    out = csv_dir / f"kde_results_{stem}.csv"
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

    print("── KDE Price Cluster Edge Verdict ──\n")
    print(
        f"  Baseline (regime_only):  avg WR {avg_base_wr * 100:.1f}%  "
        f"avg PF {avg_base_pf:.3f}"
    )
    print(
        f"  KDE config:  window={config.window}  bw_mult={_fmt_param(config.bandwidth_mult)}"
        f"  lower_duration={config.lower_duration}"
    )
    print()

    populations_to_test = ["kde_upper", "kde_lower", "kde_lower_fresh"]
    passing: list[tuple[str, float]] = []
    all_warnings: list[str] = []

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
        coverage = joined["n_trades"] / baseline["n_base"]

        # Pass criteria: PF only.
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

        # Collect warnings
        wr_fail_pairs = [p for p in joined.index if joined.loc[p, "wr_lift"] <= joined.loc[p, "min_wr_lift"]]
        low_cov_pairs = [p for p in joined.index if coverage.loc[p] < 0.30]
        weak_regime_pairs = [p for p in joined.index if baseline.loc[p, "pf_base"] < 1.1]

        if wr_fail_pairs:
            all_warnings.append(f"⚠️  [{pop}] WR lift below threshold on: {', '.join(wr_fail_pairs)}")
        if low_cov_pairs:
            all_warnings.append(f"⚠️  [{pop}] low trade count (<30% of regime) on: {', '.join(low_cov_pairs)}")
        if weak_regime_pairs:
            all_warnings.append(f"⚠️  [{pop}] weak regime baseline (PF < 1.1) on: {', '.join(weak_regime_pairs)}")

        warn_tags = []
        if wr_fail_pairs:
            warn_tags.append(f"⚠️ WR {len(wr_fail_pairs)}p")
        if low_cov_pairs:
            warn_tags.append(f"⚠️ low count {len(low_cov_pairs)}p")
        if weak_regime_pairs:
            warn_tags.append(f"⚠️ weak regime {len(weak_regime_pairs)}p")
        warn_str = ("  " + "  ".join(warn_tags)) if warn_tags else ""

        print(
            f"  {pop:<18}  avg WR lift {avg_wr_lift:+.2f}pp  avg PF {avg_pf:.3f}"
            f"  avg PF lift {avg_pf_lift:+.3f}"
            f"  pairs ≥ threshold: {n_passing}/{n_pairs}  {status}{warn_str}"
        )

        for pair, row in joined.iterrows():
            pair_status = "✅" if row["pair_passes"] else "❌"
            pair_cov = coverage.loc[pair] if pair in coverage.index else float("nan")
            notes = []
            if row["wr_lift"] <= row["min_wr_lift"]:
                notes.append("⚠️ WR")
            if pair_cov < 0.30:
                notes.append(f"⚠️ cov {pair_cov * 100:.1f}%")
            else:
                notes.append(f"cov {pair_cov * 100:.1f}%")
            if baseline.loc[pair, "pf_base"] < 1.1:
                notes.append(f"⚠️ reg PF {baseline.loc[pair, 'pf_base']:.3f}")
            note_str = "  ".join(notes)
            print(
                f"    {pair:<10}  WR {row['win_rate'] * 100:.2f}%  "
                f"lift {row['wr_lift'] * 100:+.2f}pp / req {row['min_wr_lift'] * 100:.2f}pp  "
                f"PF {row['profit_factor']:.3f}  lift {row['pf_lift']:+.3f} / req {row['min_pf_lift']:.3f}  "
                f"trades {int(row['n_trades']):,}  {note_str}  {pair_status}"
            )
        print()

        if overall:
            passing.append((pop, avg_pf))

    print(
        f"  Thresholds: PF lift > 0.02/0.05/0.10 by n,  "
        f"consistent across ≥ {config.min_pairs_passing} of {len(config.pairs)} pairs"
    )
    print()

    _print_final_verdict(passing, config, all_warnings)


def _print_final_verdict(
    passing: list[tuple[str, float]],
    config: TestConfig,
    warnings: list[str],
) -> None:
    if not passing:
        print("  ❌  KDE CLUSTER EDGE NOT CONFIRMED — no population clears all thresholds.")
        print("      Next steps:")
        print(f"        • Adjust window (currently {config.window}) — try 100 or 300")
        print(f"        • Adjust bandwidth_mult (currently {_fmt_param(config.bandwidth_mult)}) — try 0.5 or 2.0")
        print(f"        • Adjust lower_duration (currently {config.lower_duration}) — try 3 or 10")
        print("        • Try a different entry_tf in config.py")
        print("        • KDE clusters may need volume weighting for consistent edge")
        print()
        return

    pop_names = {p for p, _ in passing}
    best_pop, best_pf = max(passing, key=lambda x: x[1])
    print("  ✅  KDE CLUSTER EDGE CONFIRMED — at least one population creates predictive edge.")
    print(f"      Best performer: {best_pop}  (avg PF {best_pf:.3f})")

    if warnings:
        print("      Warnings (results valid but interpret with care):")
        for w in warnings:
            print(f"        {w}")

    print("      Proceed to the next setup step.")
    print()

    print("  ── Population Interpretation ──")
    if "kde_upper" in pop_names:
        print(
            "      kde_upper       ✅ — opening above the POC (cluster resistance reclaim) adds "
            "mean-reversion short edge within the bear regime."
        )
    if "kde_lower" in pop_names:
        print("      kde_lower       ✅ — any close below POC adds breakdown edge; duration limit not needed.")
    if "kde_lower_fresh" in pop_names:
        print(
            f"      kde_lower_fresh ✅ — fresh POC breach (≤{config.lower_duration} bars) concentrates "
            "the edge. Staleness filtering is valuable."
        )
        if "kde_lower" not in pop_names:
            print(
                "                          Note: unrestricted breakdown failed — the duration "
                "counter is doing essential filtering work."
            )

    not_passing = [p for p in ["kde_upper", "kde_lower", "kde_lower_fresh"] if p not in pop_names]
    for p in not_passing:
        label = {
            "kde_upper": "kde_upper       ❌ — open above POC does not add reliable edge.",
            "kde_lower": "kde_lower       ❌ — unrestricted POC breakdown does not add reliable edge.",
            "kde_lower_fresh": (
                f"kde_lower_fresh ❌ — lower_duration={config.lower_duration} qualifier does not help."
            ),
        }[p]
        print(f"      {label}")
    print()


if __name__ == "__main__":
    main()
