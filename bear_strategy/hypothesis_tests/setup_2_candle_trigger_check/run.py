"""CLI entry point for Setup 2 Candle Trigger: KDE Upper (4h) + 15m bar-quality signals.

Usage:
    source .venv/bin/activate
    python -m bear_strategy.hypothesis_tests.setup_2_candle_trigger_check.run

Key parameters (set in config.py):
    kde_window           -- rolling 4h-bar sample size for KDE (default: 200)
    kde_bandwidth_mult   -- Scott's rule multiplier (default: 1.0)
    rvol_window          -- rolling volume baseline in 15m bars (default: 96 = 24h)
    rvol_threshold       -- RVOL ratio to beat (default: 1.0 = above average)
    wick_ratio_threshold -- upper wick / bar range threshold (default: 0.5)
    breakdown_close_pct  -- close must be in bottom N% of range (default: 0.25)
    roc_period           -- N bars back for rate-of-change (default: 3)

----------------------------------------------------------------------
What is being tested
----------------------------------------------------------------------
Baseline (promoted from Setup 1): regime AND kde_upper (4h KDE open > peak).

All entry signals are evaluated on 15m bars.

  Bar-quality signals:
    bearish_rvol         -- bearish bar AND volume > 24h rolling mean
    upper_wick_rejection -- upper wick > 50% of bar range
    breakdown_bar        -- bearish close in bottom 25% of bar range
    roc_negative         -- N-bar rate of change is negative
    bearish_engulf       -- bearish engulfing pattern

----------------------------------------------------------------------
Pass/fail criteria
----------------------------------------------------------------------
  Baseline for lift: kde_upper_baseline PF (on 15m bars).
  profit_factor > baseline PF AND PF lift > noise_floor(n).

Warnings (do not block pass):
    WR lift below statistical threshold
    Trade count < 30% of baseline
    Baseline PF < 1.1 on a pair

Overall PASS: >= 3 of 5 pairs clear all PF thresholds.
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
from bear_strategy.hypothesis_tests.setup_2_candle_trigger_check.config import TestConfig
from bear_strategy.hypothesis_tests.setup_2_candle_trigger_check.runner import run_test

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

_DISPLAY_ORDER = [
    "kde_upper_baseline",
    "bearish_rvol",
    "upper_wick_rejection",
    "breakdown_bar",
    "roc_negative",
    "bearish_engulf",
]

_TEST_POPULATIONS = [p for p in _DISPLAY_ORDER if p != "kde_upper_baseline"]

_GROUP_BREAKS_BEFORE: set[str] = set()

_GROUP = {
    "bearish_rvol":        "Bar quality  ",
    "upper_wick_rejection":"Bar quality  ",
    "breakdown_bar":       "Bar quality  ",
    "roc_negative":        "Momentum     ",
    "bearish_engulf":      "Pattern      ",
}


def main() -> None:
    config = TestConfig()
    bw_str = _fmt_param(config.kde_bandwidth_mult)
    rvol_str = _fmt_param(config.rvol_threshold)
    wick_str = _fmt_param(config.wick_ratio_threshold)
    bkdn_str = _fmt_param(config.breakdown_close_pct)
    roc_str = str(config.roc_period)

    logger.info("=" * 70)
    logger.info("Bear Strategy -- Setup 2 Candle Trigger: KDE Upper (4h) + 15m bar quality")
    logger.info(
        "Entry TF : %s  |  KDE TF: %s",
        config.entry_tf, config.kde_tf,
    )
    logger.info("Baseline : regime AND kde_upper (4h, promoted from Setup 1)")
    logger.info("Pairs    : %s", config.pairs)
    logger.info(
        "KDE      : tf=%s  window=%d  bw_mult=%s",
        config.kde_tf, config.kde_window, bw_str,
    )
    logger.info(
        "bearish_rvol     : rvol_window=%d bars (%gh)  threshold=%s",
        config.rvol_window, config.rvol_window * 15 / 60, rvol_str,
    )
    logger.info("wick_rejection   : upper_wick/range > %s", wick_str)
    logger.info("breakdown_bar    : close in bottom %s of range", bkdn_str)
    logger.info("roc_negative     : lookback=%s bars", roc_str)
    logger.info("bearish_engulf   : classic engulfing pattern (no extra params)")
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
        extra=(
            f"candle_kde{config.kde_window}_bw{bw_str}"
            f"_rvol{config.rvol_window}x{rvol_str}"
            f"_wick{wick_str}_bkdn{bkdn_str}_roc{roc_str}"
        ),
    )
    _config_params = {
        "entry_tf": config.entry_tf,
        "kde_tf": config.kde_tf,
        "stop_atr_mult": config.stop_atr_mult,
        "target_atr_mult": config.target_atr_mult,
        "atr_period": config.atr_period,
        "kde_window": config.kde_window,
        "kde_bandwidth_mult": config.kde_bandwidth_mult,
        "rvol_window": config.rvol_window,
        "rvol_threshold": config.rvol_threshold,
        "wick_ratio_threshold": config.wick_ratio_threshold,
        "breakdown_close_pct": config.breakdown_close_pct,
        "roc_period": config.roc_period,
    }

    with capture_prints() as buf:
        _print_summary(results, config)
        _save_results(results, config, stem)
        _print_verdict(results, config)

    md_path = config.results_dir / f"setup2_candle_results_{stem}.md"
    save_report(
        buf.text,
        md_path,
        (
            f"Bear Strategy -- Setup 2 Candle Trigger: KDE Upper (4h) + {config.entry_tf} bar quality  "
            f"(entry_tf={config.entry_tf}  kde_tf={config.kde_tf})"
        ),
        config_params=_config_params,
    )


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------


def _print_summary(results: pd.DataFrame, config: TestConfig) -> None:
    print(f"\n-- Per-Pair Results (baseline = kde_upper_baseline on {config.entry_tf}) --\n")
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

        baseline_n = (
            pair_df.loc["kde_upper_baseline", "n_trades"]
            if "kde_upper_baseline" in pair_df.index else 0
        )
        if baseline_n > 0:
            print()
            for pop in _TEST_POPULATIONS:
                if pop in pair_df.index:
                    cov = pair_df.loc[pop, "n_trades"] / baseline_n
                    flag = "  !! LOW" if cov < 0.30 else ""
                    print(f"    {pop:<22}  covers {cov * 100:.1f}% of baseline bars{flag}")
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

    baseline_df = df[df["population"] == "kde_upper_baseline"].set_index("pair")
    if baseline_df.empty:
        logger.error("No kde_upper_baseline rows -- cannot compute verdict.")
        return

    baseline = baseline_df[["win_rate", "profit_factor", "n_trades"]].rename(
        columns={"win_rate": "wr_base", "profit_factor": "pf_base", "n_trades": "n_base"}
    )
    avg_base_wr = baseline["wr_base"].mean()
    avg_base_pf = baseline["pf_base"].mean()

    bw_str = _fmt_param(config.kde_bandwidth_mult)
    rvol_str = _fmt_param(config.rvol_threshold)
    wick_str = _fmt_param(config.wick_ratio_threshold)
    bkdn_str = _fmt_param(config.breakdown_close_pct)

    print(f"\n-- Setup 2 Candle Trigger ({config.entry_tf}) -- Verdict --\n")
    print(
        f"  Baseline (kde_upper_baseline on {config.entry_tf}):  "
        f"avg WR {avg_base_wr * 100:.1f}%  avg PF {avg_base_pf:.3f}"
    )
    print(
        f"  KDE ({config.kde_tf}): window={config.kde_window}  bw={bw_str}  "
        f"|  RVOL: {config.rvol_window} bars ({config.rvol_window * 15 / 60:.0f}h) threshold={rvol_str}  "
        f"|  wick={wick_str}  breakdown={bkdn_str}  roc={config.roc_period}bars"
    )
    print()

    passing: list[tuple[str, float]] = []
    all_warnings: list[str] = []

    for pop in _TEST_POPULATIONS:
        pop_df = df[df["population"] == pop].set_index("pair")
        if pop_df.empty:
            print(f"  [{_GROUP[pop]}]  {pop:<22}  -- no data")
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
        weak_pairs = [p for p in joined.index if baseline.loc[p, "pf_base"] < 1.1]

        if wr_fail_pairs:
            all_warnings.append(f"!! [{pop}] WR lift below threshold on: {', '.join(wr_fail_pairs)}")
        if low_cov_pairs:
            all_warnings.append(f"!! [{pop}] low trade count (<30% baseline) on: {', '.join(low_cov_pairs)}")
        if weak_pairs:
            all_warnings.append(f"!! [{pop}] weak baseline PF (<1.1) on: {', '.join(weak_pairs)}")

        warn_tags = []
        if wr_fail_pairs:
            warn_tags.append(f"WR {len(wr_fail_pairs)}p")
        if low_cov_pairs:
            warn_tags.append(f"low# {len(low_cov_pairs)}p")
        warn_str = ("  warn: " + ", ".join(warn_tags)) if warn_tags else ""

        print(
            f"  [{_GROUP[pop]}]  {pop:<22}  "
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
            cov_pct = pair_cov * 100
            notes.append(f"cov {cov_pct:.0f}%{'!' if pair_cov < 0.30 else ''}")
            print(
                f"    {pair:<10}  WR {row['win_rate'] * 100:.1f}%  "
                f"PF {row['profit_factor']:.3f}  lift {row['pf_lift']:+.3f} / req {row['min_pf_lift']:.2f}  "
                f"n={int(row['n_trades']):,}  {'  '.join(notes)}  [{pair_status}]"
            )

        if overall:
            passing.append((pop, avg_pf))

    print()
    print(
        f"  Thresholds: PF lift > 0.02/0.05/0.10 by n,  "
        f">= {config.min_pairs_passing} of {len(config.pairs)} pairs"
    )
    print()

    _print_final_verdict(passing, config, all_warnings, avg_base_pf)


def _save_results(results: pd.DataFrame, config: TestConfig, stem: str) -> None:
    csv_dir = config.results_dir / "csv"
    csv_dir.mkdir(parents=True, exist_ok=True)
    out = csv_dir / f"setup2_candle_results_{stem}.csv"
    results.reset_index().to_csv(out, index=False)
    logger.info("Results saved --> %s", out)


def _print_final_verdict(
    passing: list[tuple[str, float]],
    config: TestConfig,
    warnings: list[str],
    base_pf: float,
) -> None:
    rvol_str = _fmt_param(config.rvol_threshold)
    wick_str = _fmt_param(config.wick_ratio_threshold)

    if not passing:
        print(
            f"  [XX]  SETUP 2 CANDLE TRIGGER ({config.entry_tf}) -- "
            "no population improves on kde_upper_baseline."
        )
        print(f"        Baseline avg PF was {base_pf:.3f}  -- bar-quality signals add no measurable edge.")
        print("      Next steps:")
        print(f"        * Loosen wick threshold (currently {wick_str} of bar range)")
        print(f"        * Raise RVOL threshold (currently {rvol_str}x, window={config.rvol_window} bars)")
        print(f"        * Try longer ROC period (currently {config.roc_period} bars)")
        print()
        return

    passing_pops = {p for p, _ in passing}
    best_pop, best_pf = max(passing, key=lambda x: x[1])

    print(
        f"  [OK]  SETUP 2 CANDLE TRIGGER ({config.entry_tf}) CONFIRMED -- "
        "populations below improve on kde_upper_baseline."
    )
    print(f"        Base: avg PF {base_pf:.3f}  |  Best: {best_pop}  (avg PF {best_pf:.3f})")
    print()

    if warnings:
        print("  Warnings (results valid -- interpret with care):")
        for w in warnings:
            print(f"    {w}")
        print()

    print("  -- Confirmed populations --")
    groups = {
        "Bar quality": {"bearish_rvol", "upper_wick_rejection", "breakdown_bar"},
        "Momentum":    {"roc_negative"},
        "Pattern":     {"bearish_engulf"},
    }
    for group_label, members in groups.items():
        confirmed = members & passing_pops
        failed = members - passing_pops
        if confirmed or failed:
            print(f"    [{group_label}]")
            for p in sorted(confirmed):
                pf_val = next(pf for name, pf in passing if name == p)
                print(f"      [OK] {p:<24}  avg PF {pf_val:.3f}")
            for p in sorted(failed):
                print(f"      [--] {p}")

    print()
    print("  Proceed using confirmed 15m candle trigger(s) for setup 3 construction.")
    print()


if __name__ == "__main__":
    main()
