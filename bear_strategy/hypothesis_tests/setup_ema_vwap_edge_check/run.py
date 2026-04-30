"""CLI entry point for Step 2 — EMA20 / VWAP Setup Edge Check.

Usage:
    source .venv/bin/activate
    python -m bear_strategy.hypothesis_tests.setup_ema_vwap_edge_check.run

Timeframe (set entry_tf in config.py):
    "1h"  — swing shorts  ← default
    "15m" — intraday scalps
    "4h"  — position shorts

Result files:
    step2_ema_vwap_results_entry{entry_tf}_sl{stop_atr_mult}_tp{target_atr_mult}_atr{atr_period}.csv
    step2_ema_vwap_results_entry{entry_tf}_sl{stop_atr_mult}_tp{target_atr_mult}_atr{atr_period}.md

──────────────────────────────────────────────────────────────────────
What is being tested
──────────────────────────────────────────────────────────────────────
Within EMA-50 confirmed bear regime bars (Step 1 winner), test whether
two common intraday filters — price below EMA(20) and price below
daily-anchored VWAP — add measurable short edge over random regime
entries.

    below_ema20  — close < EMA(20).
    below_vwap   — close < daily VWAP (resets each UTC midnight).
    below_both   — close < EMA(20) AND close < VWAP simultaneously.

Baseline = regime_only (all eligible regime bars post-warmup).

──────────────────────────────────────────────────────────────────────
Pass/fail criteria
──────────────────────────────────────────────────────────────────────
For each pair:
    wr_lift  > 2.5 × sqrt(p × (1-p) / n)   where p = baseline WR
    pf_lift  > noise_floor(n)               (0.02/0.05/0.10)
    n_trades > 500
    primary population covers ≥ 30% of eligible regime bars

Overall PASS: ≥ 4 of 5 pairs clear all thresholds.

Regime filter: ema_below_50 (Step 1 winner).
See: bear_strategy/backtest/hypothesis_tests_raw/results/step1_regime_check/
"""

from __future__ import annotations

import logging
import math
import sys

import pandas as pd

from bear_strategy.hypothesis_tests.report_writer import capture_prints, save_report, run_stem, _fmt_param
from bear_strategy.hypothesis_tests.setup_ema_vwap_edge_check.config import TestConfig
from bear_strategy.hypothesis_tests.setup_ema_vwap_edge_check.runner import run_test

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def main() -> None:
    config = TestConfig()

    logger.info("=" * 70)
    logger.info("Bear Strategy — Step 2: EMA20 / VWAP Setup Edge Check")
    logger.info("Entry TF      : %s  |  Regime TF: 1d (daily, fixed)", config.entry_tf)
    logger.info("Regime        : %s (Step 1 winner)", config.regime_col)
    logger.info("Pairs         : %s", config.pairs)
    logger.info(
        "Indicators    : EMA(%d)  |  VWAP anchor=%s  std_mult=%.1f",
        config.ema_period, config.vwap_anchor, config.vwap_std_mult,
    )
    logger.info(
        "Stop : %.1f× ATR(%s,%d)  |  Target: %.1f× ATR(%s,%d)",
        config.stop_atr_mult, config.entry_tf, config.atr_period,
        config.target_atr_mult, config.entry_tf, config.atr_period,
    )
    logger.info("Pass threshold: ≥ %d of %d pairs", config.min_pairs_passing, len(config.pairs))
    logger.info(
        "Coverage guard: each filter must keep ≥ %.0f%% of regime bars",
        config.min_coverage_ratio * 100,
    )
    logger.info("=" * 70)

    results = run_test(config)

    if results.empty:
        logger.error("No results — check parquet data availability.")
        sys.exit(1)

    stem = run_stem(config.entry_tf, config.stop_atr_mult, config.target_atr_mult, config.atr_period,
                    extra=f"ema{config.ema_period}_vstd{_fmt_param(config.vwap_std_mult)}")
    _config_params = {
        "entry_tf": config.entry_tf,
        "stop_atr_mult": config.stop_atr_mult,
        "target_atr_mult": config.target_atr_mult,
        "atr_period": config.atr_period,
        "ema_period": config.ema_period,
        "vwap_anchor": config.vwap_anchor,
        "vwap_std_mult": config.vwap_std_mult,
    }

    pop_display = {"below_ema20": f"below_ema{config.ema_period}"}

    with capture_prints() as buf:
        _print_summary(results, config, pop_display)
        _save_results(results, config, stem)
        _print_verdict(results, config, pop_display)

    md_path = config.results_dir / f"step2_ema_vwap_results_{stem}.md"
    save_report(
        buf.text,
        md_path,
        f"Bear Strategy — EMA20 / VWAP Setup Edge Check  (entry_tf={config.entry_tf})",
        config_params=_config_params,
    )


# ---------------------------------------------------------------------------
# Reporting helpers
# ---------------------------------------------------------------------------


def _print_summary(results: pd.DataFrame, config: TestConfig, pop_display: dict[str, str]) -> None:
    print("\n── Per-Pair Results ──\n")
    df = results.reset_index()

    ordered_pops = ["regime_only", "below_ema20", "below_vwap", "below_both", "below_vwap_1std"]

    for pair in config.pairs:
        pair_df = df[df["pair"] == pair].set_index("population")
        if pair_df.empty:
            continue

        print(f"  {pair}")
        ordered = [p for p in ordered_pops if p in pair_df.index]
        subset = pair_df.reindex(ordered).copy()
        subset.index = [pop_display.get(p, p) for p in subset.index]
        subset["wr_%"] = (subset["win_rate"] * 100).round(2)
        subset["pf"] = subset["profit_factor"].round(3)
        subset["dur"] = subset["avg_duration"].round(1)
        print(subset[["wr_%", "pf", "dur", "n_trades"]].to_string())

        regime_n = pair_df.loc["regime_only", "n_trades"] if "regime_only" in pair_df.index else 0
        if regime_n > 0:
            for pop in ["below_ema20", "below_vwap", "below_both", "below_vwap_1std"]:
                if pop in pair_df.index:
                    cov = pair_df.loc[pop, "n_trades"] / regime_n
                    flag = "⚠️  LOW" if cov < config.min_coverage_ratio else ""
                    print(f"    {pop_display.get(pop, pop)} covers {cov * 100:.1f}% of regime bars  {flag}")
        print()


def _save_results(results: pd.DataFrame, config: TestConfig, stem: str) -> None:
    csv_dir = config.results_dir / "csv"
    csv_dir.mkdir(parents=True, exist_ok=True)
    out = csv_dir / f"step2_ema_vwap_results_{stem}.csv"
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

    print("── EMA20 / VWAP Setup Edge Verdict ──\n")
    print(
        f"  Baseline (regime_only):  avg WR {avg_base_wr * 100:.1f}%  "
        f"avg PF {avg_base_pf:.3f}"
    )
    print()

    populations_to_test = ["below_ema20", "below_vwap", "below_both", "below_vwap_1std"]
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
        regime_n = baseline["n_base"]
        coverage = joined["n_trades"] / regime_n
        joined["coverage_ok"] = coverage >= config.min_coverage_ratio

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
            pair_cov = (
                row["n_trades"] / baseline.loc[pair, "n_base"]
                if pair in baseline.index else float("nan")
            )
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
        print("  ❌  EMA20/VWAP EDGE NOT CONFIRMED — no filter clears all thresholds.")
        print("      Next steps:")
        print("        • Try ema_period = 10 or 50")
        print("        • Try a different entry_tf in config.py")
        print("        • Note: in a strong bear regime most bars are already below EMA20")
        print("          — high coverage may dilute the signal vs the baseline")
        print()
        return

    print("  ✅  EMA/VWAP EDGE CONFIRMED — at least one filter creates predictive edge.")
    pop_names = {p for p, _ in passing}
    best_pop, best_pf = max(passing, key=lambda x: x[1])
    print(f"      Best performer: {pop_display.get(best_pop, best_pop)}  (avg PF {best_pf:.3f})")
    if warnings:
        print("      Warnings (results valid but interpret with care):")
        for w in warnings:
            print(f"        {w}")
    print("      Proceed to Step 3 (volume trigger confirmation).")
    print()

    ema_lbl = pop_display.get("below_ema20", "below_ema20")
    print("  ── Filter Interpretation ──")
    if "below_ema20" in pop_names:
        print(f"      {ema_lbl:<17} ✅ — price below EMA adds edge within bear regime.")
        print("                             Use as setup condition before trigger entry.")
    if "below_vwap" in pop_names:
        print("      below_vwap        ✅ — price below VWAP adds edge within bear regime.")
        print("                             Strong intraday short signal in bear context.")
    if "below_both" in pop_names:
        print("      below_both        ✅ — EMA + VWAP combination is the strongest filter.")
        print("                             Require both for highest-quality setups.")
    if "below_vwap_1std" in pop_names:
        print(f"      below_vwap_1std   ✅ — price > {config.vwap_std_mult:.1f}σ below VWAP adds extra edge.")
        print("                             Deep bearish positioning; narrower but higher quality.")

    not_passing = [p for p in ["below_ema20", "below_vwap", "below_both", "below_vwap_1std"] if p not in pop_names]
    for p in not_passing:
        p_lbl = pop_display.get(p, p)
        label = {
            "below_ema20":       f"{p_lbl:<17} ❌ — EMA filter does not add edge beyond regime alone.",
            "below_vwap":        "below_vwap        ❌ — VWAP filter does not add edge beyond regime alone.",
            "below_both":        "below_both        ❌ — combined EMA+VWAP does not improve over single filters.",
            "below_vwap_1std":   "below_vwap_1std   ❌ — deep below VWAP band does not add extra edge.",
        }[p]
        print(f"      {label}")
    print()


if __name__ == "__main__":
    main()
