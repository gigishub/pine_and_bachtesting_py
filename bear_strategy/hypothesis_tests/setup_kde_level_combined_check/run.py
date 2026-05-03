"""CLI entry point for the KDE + Level Proximity Combined Check.

Usage:
    source .venv/bin/activate
    python -m bear_strategy.hypothesis_tests.setup_kde_level_combined_check.run

Key parameters (set in config.py):
    kde_window         -- rolling 4h-bar sample size for KDE (default: 200)
    kde_bandwidth_mult -- Scott's rule multiplier (default: 1.0)
    kde_lower_duration -- max bars for kde_lower_fresh to stay active (default: 5)
    vwap_anchor        -- VWAP reset period: "daily" (default)
    vpvr_window        -- trailing 1d bars for volume profile (default: 50)
    setup_distance_atr -- proximity threshold in 1h ATR units (default: 1.0)

----------------------------------------------------------------------
What is being tested
----------------------------------------------------------------------
Within the EMA-50 bear regime on the 1h TF, test each KDE direction
independently against daily-reference level proximity signals.

  KDE signals (4h):
    kde_upper       -- open > kde_peak (mean-reversion from above POC)
    kde_lower_fresh -- close < kde_peak AND counter <= lower_duration

  Level signals (1d reference):
    vwap_only   -- price near daily VWAP
    vpvr_only   -- price near VPVR HVN (1d)
    near_setup  -- near VWAP OR near VPVR

  Intersections:
    kde_upper x {vwap, vpvr, near}
    kde_lower_fresh x {vwap, vpvr, near}

Keeping the two KDE directions separate lets you see which structural
context (above-POC vs fresh-breakdown) each level signal benefits.

----------------------------------------------------------------------
Pass/fail criteria
----------------------------------------------------------------------
  profit_factor > regime_baseline PF
  PF lift > noise_floor(n)  (0.02 / 0.05 / 0.10 by n)

Warnings (do not block pass):
    WR lift below threshold
    Trade count < 30% of regime baseline
    Regime baseline PF < 1.1

Overall PASS: >= 3 of 5 pairs clear all thresholds.
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
from bear_strategy.hypothesis_tests.setup_kde_level_combined_check.config import TestConfig
from bear_strategy.hypothesis_tests.setup_kde_level_combined_check.runner import run_test

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

_DISPLAY_ORDER = [
    "regime_only",
    "kde_gate",
    "kde_upper",
    "kde_lower_fresh",
    "vwap_only",
    "vpvr_only",
    "near_setup",
    "kde_gate_and_vwap",
    "kde_gate_and_vpvr",
    "kde_gate_and_near",
    "kde_upper_and_vwap",
    "kde_upper_and_vpvr",
    "kde_upper_and_near",
    "kde_lower_and_vwap",
    "kde_lower_and_vpvr",
    "kde_lower_and_near",
]

_TEST_POPULATIONS = [p for p in _DISPLAY_ORDER if p != "regime_only"]

# Group label for each population (for verdict display)
_GROUP = {
    "kde_gate":            "KDE gate     ",
    "kde_upper":           "KDE upper    ",
    "kde_lower_fresh":     "KDE lower    ",
    "vwap_only":           "Level        ",
    "vpvr_only":           "Level        ",
    "near_setup":          "Level        ",
    "kde_gate_and_vwap":   "Gate x VWAP  ",
    "kde_gate_and_vpvr":   "Gate x VPVR  ",
    "kde_gate_and_near":   "Gate x Near  ",
    "kde_upper_and_vwap":  "Upper x VWAP ",
    "kde_upper_and_vpvr":  "Upper x VPVR ",
    "kde_upper_and_near":  "Upper x Near ",
    "kde_lower_and_vwap":  "Lower x VWAP ",
    "kde_lower_and_vpvr":  "Lower x VPVR ",
    "kde_lower_and_near":  "Lower x Near ",
}


def main() -> None:
    config = TestConfig()
    bw_str = _fmt_param(config.kde_bandwidth_mult)
    dist_str = _fmt_param(config.setup_distance_atr)

    logger.info("=" * 70)
    logger.info("Bear Strategy -- KDE + Level Proximity Combined Check")
    logger.info(
        "Entry TF : %s  |  KDE TF: %s  |  Level reference: %s",
        config.entry_tf, config.kde_tf, config.context_tf,
    )
    logger.info("Regime   : %s", config.regime_col)
    logger.info("Pairs    : %s", config.pairs)
    logger.info(
        "KDE      : tf=%s  window=%d  bw_mult=%s  lower_duration=%d",
        config.kde_tf, config.kde_window, bw_str, config.kde_lower_duration,
    )
    logger.info("VWAP     : %s-anchored on %s bars", config.vwap_anchor, config.entry_tf)
    logger.info("VPVR     : window=%d 1d bars  bins=%d", config.vpvr_window, config.vpvr_n_bins)
    logger.info("Proximity: %s x ATR(%s,%d)", dist_str, config.entry_tf, config.atr_period)
    logger.info(
        "Stop: %.1f x ATR  Target: %.1f x ATR  (period=%d)",
        config.stop_atr_mult, config.target_atr_mult, config.atr_period,
    )
    logger.info("Pass threshold: >= %d of %d pairs", config.min_pairs_passing, len(config.pairs))
    logger.info("=" * 70)

    results = run_test(config)

    if results.empty:
        logger.error("No results -- check parquet data availability.")
        sys.exit(1)

    stem = run_stem(
        config.entry_tf, config.stop_atr_mult, config.target_atr_mult, config.atr_period,
        extra=f"kdelevel_kde{config.kde_window}_bw{bw_str}_N{config.kde_lower_duration}_dist{dist_str}",
    )
    _config_params = {
        "entry_tf": config.entry_tf,
        "kde_tf": config.kde_tf,
        "context_tf": config.context_tf,
        "stop_atr_mult": config.stop_atr_mult,
        "target_atr_mult": config.target_atr_mult,
        "atr_period": config.atr_period,
        "kde_window": config.kde_window,
        "kde_bandwidth_mult": config.kde_bandwidth_mult,
        "kde_lower_duration": config.kde_lower_duration,
        "vwap_anchor": config.vwap_anchor,
        "vpvr_window": config.vpvr_window,
        "vpvr_n_bins": config.vpvr_n_bins,
        "setup_distance_atr": config.setup_distance_atr,
    }

    with capture_prints() as buf:
        _print_summary(results, config)
        _save_results(results, config, stem)
        _print_verdict(results, config)

    md_path = config.results_dir / f"kde_level_results_{stem}.md"
    save_report(
        buf.text,
        md_path,
        f"Bear Strategy -- KDE + Level Proximity Combined Check  (entry_tf={config.entry_tf}  kde_tf={config.kde_tf})",
        config_params=_config_params,
    )


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------


def _print_summary(results: pd.DataFrame, config: TestConfig) -> None:
    print("\n-- Per-Pair Results --\n")
    df = results.reset_index()

    for pair in config.pairs:
        pair_df = df[df["pair"] == pair].set_index("population")
        if pair_df.empty:
            continue

        print(f"  {pair}")
        ordered = [p for p in _DISPLAY_ORDER if p in pair_df.index]
        subset = pair_df.reindex(ordered).copy()
        subset["wr_%"] = (subset["win_rate"] * 100).round(2)
        subset["pf"] = subset["profit_factor"].round(3)
        subset["dur"] = subset["avg_duration"].round(1)
        print(subset[["wr_%", "pf", "dur", "n_trades"]].to_string())

        regime_n = pair_df.loc["regime_only", "n_trades"] if "regime_only" in pair_df.index else 0
        if regime_n > 0:
            print()
            for pop in _TEST_POPULATIONS:
                if pop in pair_df.index:
                    cov = pair_df.loc[pop, "n_trades"] / regime_n
                    flag = "  !! LOW" if cov < 0.30 else ""
                    print(f"    {pop:<24}  covers {cov * 100:.1f}% of regime bars{flag}")
        print()


# ---------------------------------------------------------------------------
# Verdict helpers
# ---------------------------------------------------------------------------


def _min_pf_diff(smaller_n: int) -> float:
    if smaller_n > 50_000:
        return 0.02
    if smaller_n >= 10_000:
        return 0.05
    return 0.10


def _min_wr_lift(baseline_wr: float, smaller_n: int, zscore: float = 2.5) -> float:
    if smaller_n <= 0:
        return float("inf")
    return zscore * math.sqrt(max(baseline_wr * (1.0 - baseline_wr), 0.0) / smaller_n)


def _print_verdict(results: pd.DataFrame, config: TestConfig) -> None:
    df = results.reset_index()

    baseline_df = df[df["population"] == "regime_only"].set_index("pair")
    if baseline_df.empty:
        logger.error("No regime_only rows -- cannot compute verdict.")
        return

    baseline = baseline_df[["win_rate", "profit_factor", "n_trades"]].rename(
        columns={"win_rate": "wr_base", "profit_factor": "pf_base", "n_trades": "n_base"}
    )
    avg_base_wr = baseline["wr_base"].mean()
    avg_base_pf = baseline["pf_base"].mean()

    bw_str = _fmt_param(config.kde_bandwidth_mult)
    dist_str = _fmt_param(config.setup_distance_atr)

    print("\n-- KDE + Level Combined -- Verdict --\n")
    print(
        f"  Baseline (regime_only):  avg WR {avg_base_wr * 100:.1f}%  avg PF {avg_base_pf:.3f}"
    )
    print(
        f"  KDE ({config.kde_tf}): window={config.kde_window}  bw={bw_str}  lower_dur={config.kde_lower_duration}"
        f"  |  VWAP: {config.vwap_anchor}  VPVR: {config.vpvr_window}d  |  dist={dist_str}xATR"
    )
    print()

    # Separator line positions for grouping
    _group_breaks_before = {
        "kde_gate", "kde_upper", "vwap_only",
        "kde_gate_and_vwap", "kde_upper_and_vwap", "kde_lower_and_vwap",
    }

    passing: list[tuple[str, float]] = []
    all_warnings: list[str] = []

    for pop in _TEST_POPULATIONS:
        if pop in _group_breaks_before:
            print()

        pop_df = df[df["population"] == pop].set_index("pair")
        if pop_df.empty:
            print(f"  [{_GROUP[pop]}]  {pop:<24}  -- no data")
            continue

        joined = pop_df.join(baseline)
        joined["smaller_n"] = joined[["n_trades", "n_base"]].min(axis=1).astype(int)
        joined["wr_lift"] = joined["win_rate"] - joined["wr_base"]
        joined["pf_lift"] = joined["profit_factor"] - joined["pf_base"]
        joined["min_wr_lift"] = joined.apply(
            lambda row: _min_wr_lift(float(row["wr_base"]), int(row["smaller_n"])), axis=1
        )
        joined["min_pf_lift"] = joined["smaller_n"].apply(_min_pf_diff)
        coverage = joined["n_trades"] / baseline["n_base"]

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
        status = "OK" if overall else "XX"

        wr_fail_pairs = [p for p in joined.index if joined.loc[p, "wr_lift"] <= joined.loc[p, "min_wr_lift"]]
        low_cov_pairs = [p for p in joined.index if coverage.loc[p] < 0.30]
        weak_regime_pairs = [p for p in joined.index if baseline.loc[p, "pf_base"] < 1.1]

        if wr_fail_pairs:
            all_warnings.append(f"!! [{pop}] WR lift below threshold on: {', '.join(wr_fail_pairs)}")
        if low_cov_pairs:
            all_warnings.append(f"!! [{pop}] low trade count (<30% regime) on: {', '.join(low_cov_pairs)}")
        if weak_regime_pairs:
            all_warnings.append(f"!! [{pop}] weak regime baseline (PF < 1.1) on: {', '.join(weak_regime_pairs)}")

        warn_tags = []
        if wr_fail_pairs:
            warn_tags.append(f"WR {len(wr_fail_pairs)}p")
        if low_cov_pairs:
            warn_tags.append(f"low# {len(low_cov_pairs)}p")
        warn_str = ("  warn: " + ", ".join(warn_tags)) if warn_tags else ""

        print(
            f"  [{_GROUP[pop]}]  {pop:<24}  "
            f"WR lift {avg_wr_lift:+.1f}pp  avg PF {avg_pf:.3f}  "
            f"PF lift {avg_pf_lift:+.3f}  "
            f"{n_passing}/{n_pairs} pairs  [{status}]{warn_str}"
        )

        for pair, row in joined.iterrows():
            pair_status = "OK" if row["pair_passes"] else "--"
            pair_cov = coverage.loc[pair] if pair in coverage.index else float("nan")
            notes = []
            if row["wr_lift"] <= row["min_wr_lift"]:
                notes.append("WR!")
            if pair_cov < 0.30:
                notes.append(f"cov {pair_cov * 100:.0f}%!")
            else:
                notes.append(f"cov {pair_cov * 100:.0f}%")
            note_str = "  ".join(notes)
            print(
                f"    {pair:<10}  WR {row['win_rate'] * 100:.1f}%  "
                f"PF {row['profit_factor']:.3f}  lift {row['pf_lift']:+.3f} / req {row['min_pf_lift']:.2f}  "
                f"n={int(row['n_trades']):,}  {note_str}  [{pair_status}]"
            )

        if overall:
            passing.append((pop, avg_pf))

    print()
    print(
        f"  Thresholds: PF lift > 0.02/0.05/0.10 by n,  "
        f">= {config.min_pairs_passing} of {len(config.pairs)} pairs"
    )
    print()

    _print_final_verdict(passing, config, all_warnings)


def _save_results(results: pd.DataFrame, config: TestConfig, stem: str) -> None:
    csv_dir = config.results_dir / "csv"
    csv_dir.mkdir(parents=True, exist_ok=True)
    out = csv_dir / f"kde_level_results_{stem}.csv"
    results.reset_index().to_csv(out, index=False)
    logger.info("Results saved --> %s", out)


def _print_final_verdict(
    passing: list[tuple[str, float]],
    config: TestConfig,
    warnings: list[str],
) -> None:
    bw_str = _fmt_param(config.kde_bandwidth_mult)
    dist_str = _fmt_param(config.setup_distance_atr)

    if not passing:
        print("  [XX]  KDE + LEVEL COMBINATION NOT CONFIRMED -- no population clears thresholds.")
        print("      Next steps:")
        print(f"        * Adjust KDE window (currently {config.kde_window} {config.kde_tf} bars)")
        print(f"        * Adjust proximity threshold (currently {dist_str} x ATR_1h)")
        print(f"        * Adjust VPVR window (currently {config.vpvr_window} daily bars)")
        print()
        return

    passing_pops = {p for p, _ in passing}
    best_pop, best_pf = max(passing, key=lambda x: x[1])

    print("  [OK]  KDE + LEVEL EDGE CONFIRMED -- confirmed populations below.")
    print(f"        Best performer: {best_pop}  (avg PF {best_pf:.3f})")
    print()

    if warnings:
        print("  Warnings (results valid -- interpret with care):")
        for w in warnings:
            print(f"    {w}")
        print()

    print("  -- Confirmed populations --")
    groups = {
        "KDE gate (combined OR)": {"kde_gate"},
        "KDE signal (standalone)": {"kde_upper", "kde_lower_fresh"},
        "Level signal (standalone)": {"vwap_only", "vpvr_only", "near_setup"},
        "kde_gate x level": {"kde_gate_and_vwap", "kde_gate_and_vpvr", "kde_gate_and_near"},
        "kde_upper x level": {"kde_upper_and_vwap", "kde_upper_and_vpvr", "kde_upper_and_near"},
        "kde_lower_fresh x level": {"kde_lower_and_vwap", "kde_lower_and_vpvr", "kde_lower_and_near"},
    }
    for group_label, members in groups.items():
        confirmed = members & passing_pops
        failed = members - passing_pops
        if confirmed or failed:
            print(f"    [{group_label}]")
            for p in sorted(confirmed):
                pf_for = next(pf for name, pf in passing if name == p)
                print(f"      [OK] {p:<26}  avg PF {pf_for:.3f}")
            for p in sorted(failed):
                print(f"      [--] {p}")

    print()
    print("  Proceed to next setup step using confirmed populations.")
    print()


if __name__ == "__main__":
    main()
