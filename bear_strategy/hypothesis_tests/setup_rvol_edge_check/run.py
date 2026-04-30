"""CLI entry point for Step 2 — RVOL Setup Edge Check.

Usage:
    source .venv/bin/activate
    python -m bear_strategy.hypothesis_tests.setup_rvol_edge_check.run

Timeframe (set entry_tf in config.py):
    "1h"  — swing shorts  ← default
    "15m" — intraday scalps (increase min_bars_active to 2–3)
    "4h"  — position shorts

Key parameter — min_bars_active (set in config.py):
    1  → single spike bar qualifies             (default, suitable for 4h/1h)
    2  → two consecutive spike bars required    (recommended for 1h/15m)
    3  → three consecutive spike bars required  (recommended for 15m/5m)

Result files:
    step2_rvol_results_entry{entry_tf}_bars{min_bars_active}_sl{stop_atr_mult}_tp{target_atr_mult}_atr{atr_period}.csv
    step2_rvol_results_entry{entry_tf}_bars{min_bars_active}_sl{stop_atr_mult}_tp{target_atr_mult}_atr{atr_period}.md

──────────────────────────────────────────────────────────────────────
What is being tested
──────────────────────────────────────────────────────────────────────
Within EMA-50 confirmed bear regime bars (Step 1 winner), test whether
a Relative Volume spike (volume ≥ 1.5× its 20-bar rolling average)
creates measurable short edge over random regime entries.

    rvol_spike         — volume spike alone (any direction).
    rvol_spike_bearish — spike + bearish candle (close < open).
    rvol_spike_down    — spike + price declined (close < prev close).

Baseline = regime_only (all eligible regime bars post-warmup).

──────────────────────────────────────────────────────────────────────
Pass/fail criteria
──────────────────────────────────────────────────────────────────────
For each pair:
    wr_lift  > 2.5 × sqrt(p × (1-p) / n)   where p = baseline WR
    pf_lift  > noise_floor(n)               (0.02/0.05/0.10)
    n_trades > 500
    primary population covers ≥ 20% of eligible regime bars

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
from bear_strategy.hypothesis_tests.setup_rvol_edge_check.config import TestConfig
from bear_strategy.hypothesis_tests.setup_rvol_edge_check.runner import run_test

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def main() -> None:
    config = TestConfig()

    logger.info("=" * 70)
    logger.info("Bear Strategy — Step 2: RVOL Setup Edge Check")
    logger.info("Entry TF      : %s  |  Regime TF: 1d (daily, fixed)", config.entry_tf)
    logger.info("Regime        : %s (Step 1 winner)", config.regime_col)
    logger.info("Pairs         : %s", config.pairs)
    logger.info(
        "RVOL          : threshold=%.1fx  vol_ma_len=%d  min_bars_active=%d",
        config.rvol_threshold, config.vol_ma_len, config.min_bars_active,
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

    stem = run_stem(
        config.entry_tf, config.stop_atr_mult, config.target_atr_mult, config.atr_period,
        extra=f"rvol{_fmt_param(config.rvol_threshold)}_bars{config.min_bars_active}",
    )
    _config_params = {
        "entry_tf": config.entry_tf,
        "stop_atr_mult": config.stop_atr_mult,
        "target_atr_mult": config.target_atr_mult,
        "atr_period": config.atr_period,
        "rvol_threshold": config.rvol_threshold,
        "vol_ma_len": config.vol_ma_len,
        "min_bars_active": config.min_bars_active,
    }

    with capture_prints() as buf:
        _print_summary(results, config)
        _save_results(results, config, stem)
        _print_verdict(results, config)

    md_path = config.results_dir / f"step2_rvol_results_{stem}.md"
    save_report(
        buf.text,
        md_path,
        f"Bear Strategy — RVOL Setup Edge Check  (entry_tf={config.entry_tf})",
        config_params=_config_params,
    )


# ---------------------------------------------------------------------------
# Reporting helpers
# ---------------------------------------------------------------------------


def _print_summary(results: pd.DataFrame, config: TestConfig) -> None:
    print("\n── Per-Pair Results ──\n")
    df = results.reset_index()

    ordered_pops = ["regime_only", "rvol_spike", "rvol_spike_bearish", "rvol_spike_down"]

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
            for pop in ["rvol_spike", "rvol_spike_bearish", "rvol_spike_down"]:
                if pop in pair_df.index:
                    cov = pair_df.loc[pop, "n_trades"] / regime_n
                    flag = "⚠️  LOW" if cov < config.min_coverage_ratio else ""
                    print(f"    {pop} covers {cov * 100:.1f}% of regime bars  {flag}")
        print()


def _save_results(results: pd.DataFrame, config: TestConfig, stem: str) -> None:
    csv_dir = config.results_dir / "csv"
    csv_dir.mkdir(parents=True, exist_ok=True)
    out = csv_dir / f"step2_rvol_results_{stem}.csv"
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

    print("── RVOL Setup Edge Verdict ──\n")
    print(
        f"  Baseline (regime_only):  avg WR {avg_base_wr * 100:.1f}%  "
        f"avg PF {avg_base_pf:.3f}"
    )
    print(
        f"  RVOL config: threshold={config.rvol_threshold:.1f}×  "
        f"vol_ma_len={config.vol_ma_len}  min_bars_active={config.min_bars_active}"
    )
    print()

    populations_to_test = ["rvol_spike", "rvol_spike_bearish", "rvol_spike_down"]
    passing: list[tuple[str, float]] = []

    for pop in populations_to_test:
        pop_df = df[df["population"] == pop].set_index("pair")
        if pop_df.empty:
            print(f"  {pop:<22}  — no data")
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
            f"  {pop:<22}  avg WR lift {avg_wr_lift:+.2f}pp  avg PF {avg_pf:.3f}"
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
        print("  ❌  RVOL EDGE NOT CONFIRMED — no population clears all thresholds.")
        print("      Next steps:")
        print("        • Increase min_bars_active (reduces noise on lower TF)")
        print("        • Try rvol_threshold = 2.0 (stricter spike definition)")
        print("        • Try vol_ma_len = 10 or 50")
        print("        • Try a different entry_tf in config.py")
        print("        • Re-examine whether setup layer is needed before trigger layer")
        print()
        return

    print("  ✅  RVOL EDGE CONFIRMED — at least one population creates predictive edge.")
    pop_names = {p for p, _ in passing}
    best_pop, best_pf = max(passing, key=lambda x: x[1])
    print(f"      Best performer: {best_pop}  (avg PF {best_pf:.3f})")
    print("      Proceed to Step 3 (volume trigger confirmation).")
    print()

    print("  ── Population Interpretation ──")
    if "rvol_spike" in pop_names:
        print("      rvol_spike           ✅ — raw volume spikes add edge regardless of direction.")
        print("                               Volume alone is informative in this bear regime.")
    if "rvol_spike_bearish" in pop_names:
        print("      rvol_spike_bearish   ✅ — high-volume bearish candles are the strongest signal.")
        print("                               Combine with trigger for entries.")
    if "rvol_spike_down" in pop_names:
        print("      rvol_spike_down      ✅ — high-volume price declines confirm short momentum.")

    not_passing = [
        p for p in ["rvol_spike", "rvol_spike_bearish", "rvol_spike_down"]
        if p not in pop_names
    ]
    for p in not_passing:
        label = {
            "rvol_spike":          "rvol_spike           ❌ — volume spikes alone do not add edge.",
            "rvol_spike_bearish":  "rvol_spike_bearish   ❌ — bearish candle filter does not help.",
            "rvol_spike_down":     "rvol_spike_down      ❌ — down-move filter does not help.",
        }[p]
        print(f"      {label}")

    if config.min_bars_active == 1:
        print()
        print(
            f"      ℹ️  min_bars_active=1 (single-bar spike).  "
            "If running on 15m or lower, try min_bars_active=2 to reduce noise."
        )
    print()


if __name__ == "__main__":
    main()
