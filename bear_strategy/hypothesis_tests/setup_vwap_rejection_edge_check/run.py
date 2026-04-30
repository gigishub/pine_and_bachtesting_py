"""CLI entry point for Step 2 — VWAP Rejection Candle Setup Edge Check.

Usage:
    source .venv/bin/activate
    python -m bear_strategy.hypothesis_tests.setup_vwap_rejection_edge_check.run

Timeframe (set entry_tf in config.py):
    "1h"  — swing shorts  ← default
    "15m" — intraday scalps
    "4h"  — position shorts

Key parameters (set in config.py):
    vwap_anchor    "daily" / "weekly" / "monthly"  — VWAP reset period
    max_wick_ratio 0.20  — each wick may be at most this fraction of candle range

Result files:
    step2_vwap_rejection_results_entry{entry_tf}.csv
    step2_vwap_rejection_results_entry{entry_tf}.md

──────────────────────────────────────────────────────────────────────
What is being tested
──────────────────────────────────────────────────────────────────────
Within EMA-50 confirmed bear regime bars (Step 1 winner), test whether
a bearish VWAP rejection candle (open above VWAP, close below VWAP)
creates measurable short edge — and whether filtering for clean bodies
(small wicks at both ends) improves it further.

    vwap_rejection       — any bearish VWAP cross candle.
    vwap_rejection_clean — rejection + both wicks ≤ max_wick_ratio.

Baseline = regime_only (all eligible regime bars post-warmup).

──────────────────────────────────────────────────────────────────────
Candle anatomy (bearish rejection)
──────────────────────────────────────────────────────────────────────

    ─── High
    |                ← top_wick  = High − Open
    ┌───────────┐
    │   OPEN    │  ← above VWAP
    │           │
    │   CLOSE   │  ← below VWAP
    └───────────┘
    |                ← bottom_wick = Close − Low
    ─── Low

    Clean candle: top_wick / range ≤ 0.20  AND  bottom_wick / range ≤ 0.20

──────────────────────────────────────────────────────────────────────
Pass/fail criteria
──────────────────────────────────────────────────────────────────────
For each pair:
    wr_lift  > 2.5 × sqrt(p × (1-p) / n)   where p = baseline WR
    pf_lift  > noise_floor(n)               (0.02/0.05/0.10)
    n_trades > 500
    population covers ≥ 5% of eligible regime bars

Overall PASS: ≥ 4 of 5 pairs clear all thresholds.

Regime filter: ema_below_50 (Step 1 winner).
See: bear_strategy/backtest/hypothesis_tests_raw/results/step1_regime_check/
"""

from __future__ import annotations

import logging
import math
import sys

import pandas as pd

from bear_strategy.hypothesis_tests.report_writer import capture_prints, save_report
from bear_strategy.hypothesis_tests.setup_vwap_rejection_edge_check.config import TestConfig
from bear_strategy.hypothesis_tests.setup_vwap_rejection_edge_check.runner import run_test

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def main() -> None:
    config = TestConfig()

    logger.info("=" * 70)
    logger.info("Bear Strategy — Step 2: VWAP Rejection Candle Setup Edge Check")
    logger.info("Entry TF      : %s  |  Regime TF: 1d (daily, fixed)", config.entry_tf)
    logger.info("Regime        : %s (Step 1 winner)", config.regime_col)
    logger.info("Pairs         : %s", config.pairs)
    logger.info(
        "VWAP          : anchor=%s  |  Clean filter: max_wick_ratio=%.2f",
        config.vwap_anchor, config.max_wick_ratio,
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

    stem = f"step2_vwap_rejection_results_entry{config.entry_tf}"

    with capture_prints() as buf:
        _print_summary(results, config)
        _save_results(results, config, stem)
        _print_verdict(results, config)

    md_path = config.results_dir / f"{stem}.md"
    save_report(buf.text, md_path, title="VWAP Rejection Candle Setup Edge Check")


# ---------------------------------------------------------------------------
# Reporting helpers
# ---------------------------------------------------------------------------


def _print_summary(results: pd.DataFrame, config: TestConfig) -> None:
    print("\n── Per-Pair Results ──\n")
    df = results.reset_index()
    ordered_pops = ["regime_only", "vwap_rejection", "vwap_rejection_clean"]

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
            for pop in ["vwap_rejection", "vwap_rejection_clean"]:
                if pop in pair_df.index:
                    cov = pair_df.loc[pop, "n_trades"] / regime_n
                    flag = "⚠️  LOW" if cov < config.min_coverage_ratio else ""
                    print(f"    {pop} covers {cov * 100:.1f}% of regime bars  {flag}")
        print()


def _save_results(results: pd.DataFrame, config: TestConfig, stem: str) -> None:
    config.results_dir.mkdir(parents=True, exist_ok=True)
    out = config.results_dir / f"{stem}.csv"
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

    print("── VWAP Rejection Candle Edge Verdict ──\n")
    print(
        f"  Baseline (regime_only):  avg WR {avg_base_wr * 100:.1f}%  "
        f"avg PF {avg_base_pf:.3f}"
    )
    print(
        f"  Config: vwap_anchor={config.vwap_anchor}  "
        f"max_wick_ratio={config.max_wick_ratio:.2f}"
    )
    print()

    populations_to_test = ["vwap_rejection", "vwap_rejection_clean"]
    passing: list[tuple[str, float]] = []

    for pop in populations_to_test:
        pop_df = df[df["population"] == pop].set_index("pair")
        if pop_df.empty:
            print(f"  {pop:<24}  — no data")
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
            f"  {pop:<24}  avg WR lift {avg_wr_lift:+.2f}pp  avg PF {avg_pf:.3f}"
            f"  avg PF lift {avg_pf_lift:+.3f}"
            f"  pairs ≥ threshold: {n_passing}/{n_pairs}  {status}"
        )

        for pair, row in joined.iterrows():
            pair_status = "✅" if row["pair_passes"] else "❌"
            pair_cov = (
                row["n_trades"] / baseline.loc[pair, "n_base"]
                if pair in baseline.index else float("nan")
            )
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
        print("  ❌  VWAP REJECTION EDGE NOT CONFIRMED — no pattern clears all thresholds.")
        print("      Next steps:")
        print("        • Try vwap_anchor = 'weekly' (VWAP as swing resistance)")
        print(f"        • Loosen max_wick_ratio (currently {config.max_wick_ratio:.2f}) → try 0.30")
        print("        • Try a different entry_tf in config.py")
        print("        • VWAP rejections may need a trigger filter (e.g. volume spike)")
        print("          before they produce consistent edge")
        print()
        return

    print("  ✅  VWAP REJECTION EDGE CONFIRMED — at least one pattern creates predictive edge.")
    pop_names = {p for p, _ in passing}
    best_pop, best_pf = max(passing, key=lambda x: x[1])
    print(f"      Best performer: {best_pop}  (avg PF {best_pf:.3f})")
    print("      Proceed to Step 3 (volume trigger confirmation).")
    print()

    print("  ── Pattern Interpretation ──")
    if "vwap_rejection" in pop_names:
        print("      vwap_rejection        ✅ — any bearish VWAP cross adds edge in bear regime.")
        print("                                 VWAP is acting as resistance consistently.")
    if "vwap_rejection_clean" in pop_names:
        print("      vwap_rejection_clean  ✅ — clean-body rejections are higher-quality entries.")
        print(
            f"                                 Small wicks (≤{config.max_wick_ratio:.0%} each) "
            "mean decisive selling with no recovery."
        )
        if "vwap_rejection" not in pop_names:
            print("                                 Note: raw rejections failed — only clean ones work.")
            print("                                 The wick filter is doing meaningful work here.")

    not_passing = [
        p for p in ["vwap_rejection", "vwap_rejection_clean"] if p not in pop_names
    ]
    for p in not_passing:
        label = {
            "vwap_rejection":       "vwap_rejection        ❌ — raw VWAP cross does not add edge alone.",
            "vwap_rejection_clean": "vwap_rejection_clean  ❌ — clean body filter does not improve further.",
        }[p]
        print(f"      {label}")
    print()


if __name__ == "__main__":
    main()
