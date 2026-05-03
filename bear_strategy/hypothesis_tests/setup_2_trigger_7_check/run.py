"""CLI entry point for Setup 2 – Trigger 7: exhaustion / momentum-fade signals.

Usage:
    source .venv/bin/activate
    python -m bear_strategy.hypothesis_tests.setup_2_trigger_7_check.run

Change entry_tf in config.py to test 15m / 1h / 4h.

Key parameters (all in config.py):
    entry_tf           -- entry timeframe (default: 1h)
    divergence_lookback-- bars back for swing-high comparison (default: 20)
    rsi_period         -- RSI period for divergence (default: 14)
    impulse_lookback   -- bars back for high-to-high gain comparison (default: 20)
    wick_ratio         -- upper wick / bar range threshold (default: 0.5)
    bb_period          -- Bollinger Band SMA period (default: 20)
    bb_std             -- BB standard deviation multiplier (default: 2.0)
    bb_proximity_pct   -- closeness to upper band for "walking" (default: 0.01)
    bb_lookback        -- bars ago price was walking upper band (default: 10)
    ema_fast           -- fast EMA period (default: 9)
    ema_slow           -- slow EMA period (default: 20)

----------------------------------------------------------------------
What is being tested
----------------------------------------------------------------------
Baseline (promoted from Setup 1): regime AND kde_upper (4h KDE open > peak).

Five exhaustion signals tested on top:

  price_rsi_divergence   Price HH but RSI LH — hollow upmove
  shrinking_impulse      High-to-high gain shrinking + long upper wick
  bb_rounding            Was walking upper BB, now pulling to midline
  ema_tightening         |fast EMA - slow EMA| narrowing while fast < slow
  ema_cross_down         Fast EMA crosses below slow EMA (bearish crossover)

----------------------------------------------------------------------
Pass/fail criteria
----------------------------------------------------------------------
  Baseline for lift: kde_upper_baseline PF.
  profit_factor > baseline PF AND PF lift > noise_floor(n).
  Overall PASS: >= 3 of 5 pairs clear threshold.
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
from bear_strategy.hypothesis_tests.setup_2_trigger_7_check.config import TestConfig
from bear_strategy.hypothesis_tests.setup_2_trigger_7_check.runner import run_test

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

_DISPLAY_ORDER = [
    "kde_upper_baseline",
    "price_rsi_divergence",
    "shrinking_impulse",
    "bb_rounding",
    "ema_tightening",
    "ema_cross_down",
]

_TEST_POPULATIONS = [p for p in _DISPLAY_ORDER if p != "kde_upper_baseline"]

_GROUP = {
    "price_rsi_divergence": "Divergence ",
    "shrinking_impulse":    "Price Act  ",
    "bb_rounding":          "Volatility ",
    "ema_tightening":       "Momentum   ",
    "ema_cross_down":       "EMA Cross  ",
}


def main() -> None:
    config  = TestConfig()
    bw_str  = _fmt_param(config.kde_bandwidth_mult)
    bb_str  = _fmt_param(config.bb_std)

    logger.info("=" * 70)
    logger.info("Bear Strategy -- Setup 2 Trigger 7: exhaustion / momentum-fade signals")
    logger.info("Entry TF : %s  |  KDE TF: %s", config.entry_tf, config.kde_tf)
    logger.info("Baseline : regime AND kde_upper (4h, promoted from Setup 1)")
    logger.info("Pairs    : %s", config.pairs)
    logger.info("KDE      : tf=%s  window=%d  bw_mult=%s", config.kde_tf, config.kde_window, bw_str)
    logger.info(
        "price_rsi_divergence: RSI(%d) LH while Price HH over %d bars",
        config.rsi_period, config.divergence_lookback,
    )
    logger.info(
        "shrinking_impulse   : high-to-high gain shrinking over %d bars + wick>%.0f%% range",
        config.impulse_lookback, config.wick_ratio * 100,
    )
    logger.info(
        "bb_rounding         : was near upper BB(%d,%.1fstd) %d bars ago, now pulling to midline",
        config.bb_period, config.bb_std, config.bb_lookback,
    )
    logger.info(
        "ema_tightening      : |EMA(%d)-EMA(%d)| narrowing while fast < slow",
        config.ema_fast, config.ema_slow,
    )
    logger.info(
        "ema_cross_down       : EMA(%d) crosses below EMA(%d) (event signal)",
        config.ema_fast, config.ema_slow,
    )
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
            f"trigger7_kde{config.kde_window}_bw{bw_str}"
            f"_rsi{config.rsi_period}_divlb{config.divergence_lookback}"
            f"_implb{config.impulse_lookback}_wick{_fmt_param(config.wick_ratio)}"
            f"_bb{config.bb_period}s{bb_str}lb{config.bb_lookback}"
            f"_ema{config.ema_fast}_{config.ema_slow}"
        ),
    )
    _config_params = {
        "entry_tf":           config.entry_tf,
        "kde_tf":             config.kde_tf,
        "stop_atr_mult":      config.stop_atr_mult,
        "target_atr_mult":    config.target_atr_mult,
        "atr_period":         config.atr_period,
        "kde_window":         config.kde_window,
        "kde_bandwidth_mult": config.kde_bandwidth_mult,
        "rsi_period":         config.rsi_period,
        "divergence_lookback":config.divergence_lookback,
        "impulse_lookback":   config.impulse_lookback,
        "wick_ratio":         config.wick_ratio,
        "bb_period":          config.bb_period,
        "bb_std":             config.bb_std,
        "bb_proximity_pct":   config.bb_proximity_pct,
        "bb_lookback":        config.bb_lookback,
        "ema_fast":           config.ema_fast,
        "ema_slow":           config.ema_slow,
    }

    with capture_prints() as buf:
        _print_summary(results, config)
        _save_results(results, config, stem)
        _print_verdict(results, config)

    md_path = config.results_dir / f"trigger7_results_{stem}.md"
    save_report(
        buf.text,
        md_path,
        (
            f"Bear Strategy -- Setup 2 Trigger 7  "
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
        subset  = pair_df.reindex(ordered).copy()
        subset["wr_%"] = (subset["win_rate"] * 100).round(2)
        subset["pf"]   = subset["profit_factor"].round(3)
        subset["dur"]  = subset["avg_duration"].round(1)
        print(subset[["wr_%", "pf", "dur", "n_trades"]].to_string())

        baseline_n = (
            pair_df.loc["kde_upper_baseline", "n_trades"]
            if "kde_upper_baseline" in pair_df.index else 0
        )
        if baseline_n > 0:
            print()
            for pop in _TEST_POPULATIONS:
                if pop in pair_df.index:
                    cov  = pair_df.loc[pop, "n_trades"] / baseline_n
                    flag = "  !! LOW" if cov < 0.30 else ""
                    print(f"    {pop:<26}  covers {cov * 100:.1f}% of baseline bars{flag}")
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
    bw_str      = _fmt_param(config.kde_bandwidth_mult)

    print(f"\n-- Setup 2 Trigger 7 ({config.entry_tf}) -- Verdict --\n")
    print(
        f"  Baseline (kde_upper_baseline on {config.entry_tf}):  "
        f"avg WR {avg_base_wr * 100:.1f}%  avg PF {avg_base_pf:.3f}"
    )
    print(
        f"  KDE ({config.kde_tf}): window={config.kde_window}  bw={bw_str}  |  "
        f"RSI({config.rsi_period})  BB({config.bb_period})  EMA({config.ema_fast},{config.ema_slow})"
    )
    print()

    passing: list[tuple[str, float]] = []
    all_warnings: list[str] = []

    for pop in _TEST_POPULATIONS:
        pop_df = df[df["population"] == pop].set_index("pair")
        if pop_df.empty:
            print(f"  [{_GROUP[pop]}]  {pop:<26}  -- no data")
            continue

        joined = pop_df.join(baseline)
        joined["smaller_n"]   = joined[["n_trades", "n_base"]].min(axis=1).astype(int)
        joined["wr_lift"]     = joined["win_rate"] - joined["wr_base"]
        joined["pf_lift"]     = joined["profit_factor"] - joined["pf_base"]
        joined["min_wr_lift"] = joined.apply(
            lambda row: _min_wr_lift(float(row["wr_base"]), int(row["smaller_n"])), axis=1
        )
        joined["min_pf_lift"] = joined["smaller_n"].apply(_min_pf_diff)
        coverage = joined["n_trades"] / baseline["n_base"]

        joined["pair_passes"] = (
            (joined["pf_lift"] > joined["min_pf_lift"])
            & (joined["profit_factor"] > joined["pf_base"])
        )

        n_pairs     = len(joined)
        n_passing   = int(joined["pair_passes"].sum())
        avg_pf      = joined["profit_factor"].mean()
        avg_wr_lift = joined["wr_lift"].mean() * 100
        avg_pf_lift = joined["pf_lift"].mean()
        overall     = n_passing >= config.min_pairs_passing
        status      = "OK" if overall else "XX"

        wr_fail_pairs = [p for p in joined.index if joined.loc[p, "wr_lift"] <= joined.loc[p, "min_wr_lift"]]
        low_cov_pairs = [p for p in joined.index if coverage.loc[p] < 0.30]

        if wr_fail_pairs:
            all_warnings.append(f"!! [{pop}] WR lift below threshold on: {', '.join(wr_fail_pairs)}")
        if low_cov_pairs:
            all_warnings.append(f"!! [{pop}] low trade count (<30% baseline) on: {', '.join(low_cov_pairs)}")

        warn_tags = []
        if wr_fail_pairs:
            warn_tags.append(f"WR {len(wr_fail_pairs)}p")
        if low_cov_pairs:
            warn_tags.append(f"low# {len(low_cov_pairs)}p")
        warn_str = ("  warn: " + ", ".join(warn_tags)) if warn_tags else ""

        print(
            f"  [{_GROUP[pop]}]  {pop:<26}  "
            f"WR lift {avg_wr_lift:+.1f}pp  avg PF {avg_pf:.3f}  "
            f"PF lift {avg_pf_lift:+.3f}  "
            f"{n_passing}/{n_pairs} pairs  [{status}]{warn_str}"
        )

        for pair, row in joined.iterrows():
            pair_status = "OK" if row["pair_passes"] else "--"
            pair_cov    = coverage.loc[pair] if pair in coverage.index else float("nan")
            notes = []
            if row["wr_lift"] <= row["min_wr_lift"]:
                notes.append("WR!")
            notes.append(f"cov {pair_cov * 100:.0f}%{'!' if pair_cov < 0.30 else ''}")
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
    out = csv_dir / f"trigger7_results_{stem}.csv"
    results.reset_index().to_csv(out, index=False)
    logger.info("Results saved --> %s", out)


def _print_final_verdict(
    passing: list[tuple[str, float]],
    config: TestConfig,
    warnings: list[str],
    base_pf: float,
) -> None:
    if not passing:
        print(
            f"  [XX]  SETUP 2 TRIGGER 7 ({config.entry_tf}) -- "
            "no exhaustion signal improves on kde_upper_baseline."
        )
        print(f"        Baseline avg PF was {base_pf:.3f}.")
        print("      Tuning ideas:")
        print(f"        * Adjust divergence_lookback (currently {config.divergence_lookback})")
        print(f"        * Adjust wick_ratio (currently {config.wick_ratio})")
        print(f"        * Adjust bb_lookback (currently {config.bb_lookback})")
        print(f"        * Adjust ema_fast/slow (currently {config.ema_fast}/{config.ema_slow})")
        print(f"        * Try a different entry TF (currently {config.entry_tf})")
        print()
        return

    best_pop, best_pf = max(passing, key=lambda x: x[1])
    passing_pops = {p for p, _ in passing}

    print(
        f"  [OK]  SETUP 2 TRIGGER 7 ({config.entry_tf}) CONFIRMED -- "
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
    for group_label, members in {
        "Divergence":  ["price_rsi_divergence"],
        "Price Action": ["shrinking_impulse"],
        "Volatility":  ["bb_rounding"],
        "Momentum":    ["ema_tightening"],
    }.items():
        any_relevant = any(m in passing_pops or m in _TEST_POPULATIONS for m in members)
        if any_relevant:
            print(f"    [{group_label}]")
            for p in members:
                if p in passing_pops:
                    pf_val = next(pf for name, pf in passing if name == p)
                    print(f"      [OK] {p:<26}  avg PF {pf_val:.3f}")
                elif p in _TEST_POPULATIONS:
                    print(f"      [--] {p}")

    print()
    print("  Proceed using confirmed exhaustion signal(s) for setup 3 construction.")
    print()


if __name__ == "__main__":
    main()
