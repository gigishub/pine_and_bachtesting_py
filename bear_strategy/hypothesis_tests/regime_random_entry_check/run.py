"""CLI entry point for Step 1 — Regime Random Entry Check.

Usage:
    python -m bear_strategy.hypothesis_tests.regime_random_entry_check.run
    python -m bear_strategy.hypothesis_tests.regime_random_entry_check.run --sweep

The script runs the test, prints a summary table, and writes CSV results to
``config.results_dir``.  It also prints a clear verdict against the
falsification thresholds defined in the hypothesis document.

Result files (stem encodes all exit parameters):
    step1_results_entry{entry_tf}_sl{stop_atr_mult}_tp{target_atr_mult}_atr{atr_period}.csv
    step1_results_entry{entry_tf}_sl{stop_atr_mult}_tp{target_atr_mult}_atr{atr_period}.md

--sweep sweeps the EMA slope lookback (1, 2, 3, 5 bars) to find the most
selective lookback for each EMA period.
"""

from __future__ import annotations

import logging
import math
import sys
from pathlib import Path

import pandas as pd

from bear_strategy.hypothesis_tests.report_writer import capture_prints, save_report, run_stem
from bear_strategy.hypothesis_tests.regime_random_entry_check.config import TestConfig
from bear_strategy.hypothesis_tests.regime_random_entry_check.runner import run_test

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def main() -> None:
    config = TestConfig()

    logger.info("=" * 70)
    logger.info("Bear Strategy — Step 1: Regime Random Entry Check")
    logger.info("Entry TF     : %s  |  Regime TF: 1d (daily, fixed)", config.entry_tf)
    logger.info("Pairs        : %s", config.pairs)
    logger.info("EMA slope    : EMA %dd slope down", config.ema_slope_period)
    logger.info("EMA below    : close < EMA %s", config.ema_below_periods)
    logger.info("Slope lookback: %d bar(s)", config.ema_slope_lookback)
    logger.info("Stop  : %.1f× ATR_%s  |  Target: %.1f× ATR_%s", config.stop_atr_mult, config.entry_tf, config.target_atr_mult, config.entry_tf)
    logger.info("=" * 70)

    results = run_test(config)

    if results.empty:
        logger.error("No results produced — check that parquet data is available.")
        sys.exit(1)

    stem = run_stem(config.entry_tf, config.stop_atr_mult, config.target_atr_mult, config.atr_period)
    _config_params = {
        "entry_tf": config.entry_tf,
        "stop_atr_mult": config.stop_atr_mult,
        "target_atr_mult": config.target_atr_mult,
        "atr_period": config.atr_period,
    }

    with capture_prints() as cap:
        _print_summary(results, config)
        _save_results(results, config, stem)
        _print_verdict(results, config)

    md_path = config.results_dir / f"step1_results_{stem}.md"
    actual_path = save_report(
        cap.text,
        md_path,
        f"Bear Strategy — Step 1: Regime Random Entry Check  (entry_tf={config.entry_tf})",
        config_params=_config_params,
    )
    logger.info("Analysis report saved → %s", actual_path)


def _population_names(config: TestConfig) -> list[str]:
    return (
        ["all_candles", f"ema_{config.ema_slope_period}_slope"]
        + [f"ema_below_{p}" for p in config.ema_below_periods]
        + [f"ema_{config.ema_slope_period}_slope_and_below_{p}" for p in config.ema_below_periods]
    )


def _print_summary(results: pd.DataFrame, config: TestConfig) -> None:
    """Print a per-population summary aggregated across all pairs."""
    print("\n── Aggregated Results Across All Pairs ──\n")

    agg = (
        results.reset_index()
        .groupby("population")[["win_rate", "profit_factor", "avg_duration", "n_trades"]]
        .agg(
            win_rate=("win_rate", "mean"),
            profit_factor=("profit_factor", "mean"),
            avg_duration=("avg_duration", "mean"),
            n_trades=("n_trades", "sum"),
        )
    )

    agg = agg.reindex([p for p in _population_names(config) if p in agg.index])
    agg["win_rate_%"] = (agg["win_rate"] * 100).round(1)
    agg["profit_factor"] = agg["profit_factor"].round(3)
    agg["avg_duration"] = agg["avg_duration"].round(1)

    print(agg[["win_rate_%", "profit_factor", "avg_duration", "n_trades"]].to_string())
    print()


def _save_results(results: pd.DataFrame, config: TestConfig, stem: str) -> None:
    csv_dir = config.results_dir / "csv"
    csv_dir.mkdir(parents=True, exist_ok=True)
    filename = f"step1_results_{stem}.csv"
    out = csv_dir / filename
    results.reset_index().to_csv(out, index=False)
    logger.info("Results saved → %s", out)


def _min_win_rate_lift(config: TestConfig, baseline_wr: float, smaller_n: int) -> float:
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
    """Evaluate each filter population against sample-size-aware thresholds."""
    df = results.reset_index()
    baseline = (
        df[df["population"] == "all_candles"]
        .set_index("pair")[["win_rate", "profit_factor", "n_trades"]]
        .rename(
            columns={
                "win_rate": "wr_base",
                "profit_factor": "pf_base",
                "n_trades": "n_base",
            }
        )
    )
    avg_base_pf = baseline["pf_base"].mean()
    avg_base_wr = baseline["wr_base"].mean()

    print("── Falsification Verdict ──\n")
    print(f"  Baseline (all_candles):  avg WR {avg_base_wr * 100:.1f}%  avg PF {avg_base_pf:.3f}")
    print()

    populations = (
        [f"ema_{config.ema_slope_period}_slope"]
        + [f"ema_below_{p}" for p in config.ema_below_periods]
        + [f"ema_{config.ema_slope_period}_slope_and_below_{p}" for p in config.ema_below_periods]
    )

    passing: list[tuple[str, float]] = []
    all_warnings: list[str] = []

    for pop in populations:
        pop_df = df[df["population"] == pop].set_index("pair")
        if pop_df.empty:
            continue

        joined = pop_df.join(baseline)
        joined["smaller_n"] = joined[["n_trades", "n_base"]].min(axis=1).astype(int)
        joined["wr_lift"] = joined["win_rate"] - joined["wr_base"]
        joined["pf_lift"] = joined["profit_factor"] - joined["pf_base"]
        joined["min_wr_lift"] = joined.apply(
            lambda row: _min_win_rate_lift(
                config,
                float(row["wr_base"]),
                int(row["smaller_n"]),
            ),
            axis=1,
        )
        joined["min_pf_lift"] = joined["smaller_n"].apply(lambda n: _min_pf_diff(config, int(n)))
        joined["pair_passes"] = (
            (joined["pf_lift"] > joined["min_pf_lift"])
            & (joined["profit_factor"] > joined["pf_base"])
        )

        n_pairs = len(joined)
        n_passing_pairs = int(joined["pair_passes"].sum())
        avg_pf = joined["profit_factor"].mean()
        avg_wr_lift = joined["wr_lift"].mean() * 100
        avg_lift = joined["pf_lift"].mean()
        overall_passes = n_passing_pairs >= config.min_pairs_passing
        status = "✅" if overall_passes else "❌"

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
            f"  {pop:<22}  avg WR lift {avg_wr_lift:+.2f}pp  avg PF {avg_pf:.3f}"
            f"  avg PF lift {avg_lift:+.3f}"
            f"  pairs ≥ threshold: {n_passing_pairs}/{n_pairs}  {status}{warn_str}"
        )
        for pair, row in joined.iterrows():
            pair_status = "✅" if row["pair_passes"] else "❌"
            wr_note = "  ⚠️ WR" if row["wr_lift"] <= row["min_wr_lift"] else ""
            print(
                f"    {pair:<10}  WR {row['win_rate'] * 100:.2f}%  "
                f"lift {row['wr_lift'] * 100:+.2f}pp / req {row['min_wr_lift'] * 100:.2f}pp  "
                f"PF {row['profit_factor']:.3f}  lift {row['pf_lift']:+.3f} / req {row['min_pf_lift']:.3f}  "
                f"trades {int(row['n_trades']):,}{wr_note}  {pair_status}"
            )
        print()

        if overall_passes:
            passing.append((pop, avg_pf))

    print(
        f"  Thresholds: WR lift > 2.5 * sqrt(p * (1-p) / n),  "
        f"PF lift > 0.02 when n > 50k / 0.05 when n >= 10k / 0.10 when n < 10k,  "
        f"consistent across ≥ {config.min_pairs_passing} pairs"
    )
    print()

    if passing:
        best_pop, best_pf = max(passing, key=lambda x: x[1])
        print("  ✅  HYPOTHESIS SURVIVES — at least one filter creates directional skew.")
        print(f"      Best performer: {best_pop}  (avg PF {best_pf:.3f})")
        if all_warnings:
            print("      Warnings (results valid but interpret with care):")
            for w in all_warnings:
                print(f"        {w}")
        print("      Proceed to Step 2 (setup level edge check).")
    else:
        print("  ❌  HYPOTHESIS FAILS — no filter creates sufficient directional skew.")
        print("      Do NOT proceed to Step 2. Revisit Layer 1 regime definition.")

    print()


def sweep_ema_slope_lookback(lookbacks: list[int] | None = None) -> None:
    """Sweep EMA slope lookback values and compare each EMA period.

    Useful for finding whether a smoother slope (longer lookback) filters
    the regime more selectively than a 1-bar diff.

    Args:
        lookbacks: Lookback values to test. Defaults to [1, 2, 3, 5].
    """
    if lookbacks is None:
        lookbacks = [1, 2, 3, 5]

    base_config = TestConfig()
    sweep_records: list[dict] = []

    logger.info("=" * 70)
    logger.info("Bear Strategy — Step 1b: EMA Slope Lookback Sweep")
    logger.info("Pairs        : %s", base_config.pairs)
    logger.info("EMA slope pd : %d", base_config.ema_slope_period)
    logger.info("Below periods: %s", base_config.ema_below_periods)
    logger.info("Lookbacks    : %s", lookbacks)
    logger.info("=" * 70)

    for lookback in lookbacks:
        config = TestConfig(ema_slope_lookback=lookback)
        logger.info("Running slope_lookback = %d", lookback)
        results = run_test(config)
        if results.empty:
            logger.warning("No results for lookback %d", lookback)
            continue

        agg = (
            results.reset_index()
            .groupby("population")[["profit_factor", "n_trades"]]
            .agg(
                profit_factor=("profit_factor", "mean"),
                n_trades=("n_trades", "sum"),
            )
        )

        all_pf: float = agg.at["all_candles", "profit_factor"] if "all_candles" in agg.index else float("nan")  # type: ignore[assignment]
        all_wr: float = agg.at["all_candles", "win_rate"] if "all_candles" in agg.index else float("nan")  # type: ignore[assignment]
        all_n: int = agg.at["all_candles", "n_trades"] if "all_candles" in agg.index else 0  # type: ignore[assignment]

        # Only the slope population varies with the lookback; iterate all pops
        all_pops = [f"ema_{config.ema_slope_period}_slope"] + [
            f"ema_below_{p}" for p in config.ema_below_periods
        ]
        for pop in all_pops:
            if pop not in agg.index:
                continue
            wr: float = agg.at[pop, "win_rate"]  # type: ignore[assignment]
            pf: float = agg.at[pop, "profit_factor"]  # type: ignore[assignment]
            wr_lift = wr - all_wr
            pf_lift = pf - all_pf
            n_val: int = agg.at[pop, "n_trades"]  # type: ignore[assignment]
            smaller_n = min(n_val, all_n)
            min_wr_lift = _min_win_rate_lift(config, all_wr, smaller_n)
            min_pf_lift = _min_pf_diff(config, smaller_n)
            passes = (
                wr_lift > min_wr_lift
                and pf_lift > min_pf_lift
                and n_val > config.min_trades_per_pair
                and pf > all_pf
            )
            sweep_records.append(
                {
                    "slope_lookback": lookback,
                    "population": pop,
                    "win_rate": round(wr, 4),
                    "win_rate_lift_pp": round(wr_lift * 100, 2),
                    "min_wr_lift_pp": round(min_wr_lift * 100, 2),
                    "profit_factor": round(pf, 3),
                    "pf_lift": round(pf_lift, 3),
                    "min_pf_lift": round(min_pf_lift, 3),
                    "baseline_pf": round(all_pf, 3),
                    "n_trades": n_val,
                    "passes": "✅" if passes else "❌",
                }
            )

        # Save per-lookback CSV
        config.results_dir.mkdir(parents=True, exist_ok=True)
        out = config.results_dir / f"step1_slope_lookback_{lookback}.csv"
        results.reset_index().to_csv(out, index=False)

    if not sweep_records:
        logger.error("Sweep produced no results.")
        return

    sweep_df = pd.DataFrame(sweep_records).set_index(["slope_lookback", "population"])
    print("\n── EMA Slope Lookback Sweep Results ──\n")
    print(sweep_df.to_string())
    print()

    passing = sweep_df[sweep_df["passes"] == "✅"]
    if passing.empty:
        print("  ❌  No combination passes all criteria.")
        print("      Consider: longer lookback, different EMA periods, or alternative regime logic.")
    else:
        best_idx = passing["profit_factor"].idxmax()
        lookback_val, pop_val = best_idx  # type: ignore[misc]
        print(f"  ✅  Best combination: slope_lookback={lookback_val}, population={pop_val}")
        print("      Update config.py ema_slope_lookback to match.")
    print()


if __name__ == "__main__":
    if "--sweep" in sys.argv:
        sweep_ema_slope_lookback()
    else:
        main()
