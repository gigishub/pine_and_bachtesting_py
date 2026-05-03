"""CLI entry point for Setup 2 – Trigger 8: rsi_ma_below_50 reinforced baseline.

Usage:
    source .venv/bin/activate
    python -m bear_strategy.hypothesis_tests.setup_2_trigger_8_check.run

Change entry_tf in config.py to test 15m / 1h / 4h.

Key parameters (all in config.py):
    entry_tf           -- entry timeframe (default: 1h)
    rsi_period         -- RSI period for baseline MA and positional filters (default: 14)
    rsi_ma_period      -- MA period applied to RSI (default: 5)
    rsi_ma_type        -- "ema" or "sma" for RSI MA (default: ema)
    rsi_ma_threshold   -- gate for the reinforced baseline (default: 50)
    rsi_threshold      -- RSI level for rsi_below_50 (default: 50)
    mfi_period         -- MFI lookback (default: 14)
    mfi_threshold      -- MFI level for mfi_below_50 (default: 50)
    ema_fast           -- fast EMA period (default: 9)
    ema_slow           -- slow EMA period (default: 20)
    macd_fast/slow/signal -- MACD parameters (default: 12/26/9)
    bb_period          -- Bollinger Band period (default: 20)
    bb_std             -- BB std multiplier (default: 2.0)

----------------------------------------------------------------------
What is being tested
----------------------------------------------------------------------
Reference:  kde_upper_baseline — regime AND kde_upper (Setup 1 gate).
New base:   rsi_ma_baseline    — kde_upper_baseline AND rsi_ma < threshold.
            rsi_ma_below_50 was confirmed in Trigger 4 (avg PF 1.969, 3/5 pairs).

Seven held-state conditions tested on top of rsi_ma_baseline:

  rsi_below_50         RSI(14) < 50 — price momentum bearish
  mfi_below_50         MFI(14) < 50 — volume momentum bearish
  rsi_and_mfi          RSI < 50 AND MFI < 50 — dual confluence
  close_below_ema      Close < EMA(slow) — price below macro trend average
  ema_bearish_order    EMA(fast) < EMA(slow) — MA stack in bearish order
  macd_signal_wall     MACD < 0 AND MACD < signal — positional MACD regime
  lower_bb_declining   lower_bb < lower_bb[1] — floor actively falling

----------------------------------------------------------------------
Pass/fail criteria
----------------------------------------------------------------------
  Baseline for lift: rsi_ma_baseline PF (not kde_upper_baseline).
  profit_factor > rsi_ma_baseline PF AND PF lift > noise_floor(n).
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
from bear_strategy.hypothesis_tests.setup_2_trigger_8_check.config import TestConfig
from bear_strategy.hypothesis_tests.setup_2_trigger_8_check.runner import run_test

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Populations shown in summary table (both baselines + 7 conditions)
_DISPLAY_ORDER = [
    "kde_upper_baseline",
    "rsi_ma_baseline",
    "rsi_below_50",
    "mfi_below_50",
    "rsi_and_mfi",
    "close_below_ema",
    "ema_bearish_order",
    "macd_signal_wall",
    "lower_bb_declining",
]

# Populations that the verdict evaluates (excludes both baselines)
_TEST_POPULATIONS = [p for p in _DISPLAY_ORDER if p not in ("kde_upper_baseline", "rsi_ma_baseline")]

_GROUP = {
    "rsi_below_50":       "Momentum   ",
    "mfi_below_50":       "Momentum   ",
    "rsi_and_mfi":        "Confluence ",
    "close_below_ema":    "Trend      ",
    "ema_bearish_order":  "Trend      ",
    "macd_signal_wall":   "MACD       ",
    "lower_bb_declining": "Volatility ",
}


def main() -> None:
    config = TestConfig()
    bw_str = _fmt_param(config.kde_bandwidth_mult)
    bb_str = _fmt_param(config.bb_std)

    logger.info("=" * 70)
    logger.info("Bear Strategy -- Setup 2 Trigger 8: rsi_ma_below_50 reinforced baseline")
    logger.info("Entry TF : %s  |  KDE TF: %s", config.entry_tf, config.kde_tf)
    logger.info(
        "Baseline : regime AND kde_upper AND RSI_MA(%s,%d) < %.0f",
        config.rsi_ma_type, config.rsi_ma_period, config.rsi_ma_threshold,
    )
    logger.info("Pairs    : %s", config.pairs)
    logger.info("KDE      : tf=%s  window=%d  bw_mult=%s", config.kde_tf, config.kde_window, bw_str)
    logger.info(
        "rsi_below_50      : RSI(%d) < %.0f", config.rsi_period, config.rsi_threshold,
    )
    logger.info(
        "mfi_below_50      : MFI(%d) < %.0f", config.mfi_period, config.mfi_threshold,
    )
    logger.info(
        "rsi_and_mfi       : RSI(%d) < %.0f AND MFI(%d) < %.0f",
        config.rsi_period, config.rsi_threshold, config.mfi_period, config.mfi_threshold,
    )
    logger.info(
        "close_below_ema   : Close < EMA(%d)", config.ema_slow,
    )
    logger.info(
        "ema_bearish_order : EMA(%d) < EMA(%d)", config.ema_fast, config.ema_slow,
    )
    logger.info(
        "macd_signal_wall  : MACD(%d,%d,%d) < 0 AND MACD < signal",
        config.macd_fast, config.macd_slow, config.macd_signal,
    )
    logger.info(
        "lower_bb_declining: BB(%d, %.1fstd) lower band falling",
        config.bb_period, config.bb_std,
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
            f"trigger8_kde{config.kde_window}_bw{bw_str}"
            f"_rsiMA{config.rsi_ma_type}{config.rsi_ma_period}h{int(config.rsi_ma_threshold)}"
            f"_rsi{config.rsi_period}h{int(config.rsi_threshold)}"
            f"_mfi{config.mfi_period}h{int(config.mfi_threshold)}"
            f"_ema{config.ema_fast}_{config.ema_slow}"
            f"_macd{config.macd_fast}_{config.macd_slow}_{config.macd_signal}"
            f"_bb{config.bb_period}s{bb_str}"
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
        "rsi_ma_period":      config.rsi_ma_period,
        "rsi_ma_type":        config.rsi_ma_type,
        "rsi_ma_threshold":   config.rsi_ma_threshold,
        "rsi_threshold":      config.rsi_threshold,
        "mfi_period":         config.mfi_period,
        "mfi_threshold":      config.mfi_threshold,
        "ema_fast":           config.ema_fast,
        "ema_slow":           config.ema_slow,
        "macd_fast":          config.macd_fast,
        "macd_slow":          config.macd_slow,
        "macd_signal":        config.macd_signal,
        "bb_period":          config.bb_period,
        "bb_std":             config.bb_std,
    }

    with capture_prints() as buf:
        _print_summary(results, config)
        _save_results(results, config, stem)
        _print_verdict(results, config)

    md_path = config.results_dir / f"trigger8_results_{stem}.md"
    save_report(
        buf.text,
        md_path,
        (
            f"Bear Strategy -- Setup 2 Trigger 8  "
            f"(entry_tf={config.entry_tf}  kde_tf={config.kde_tf}  "
            f"rsi_ma_baseline={config.rsi_ma_type}{config.rsi_ma_period}<{config.rsi_ma_threshold})"
        ),
        config_params=_config_params,
    )


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

def _print_summary(results: pd.DataFrame, config: TestConfig) -> None:
    print(
        f"\n-- Per-Pair Results (new base = rsi_ma_baseline on {config.entry_tf}) --\n"
    )
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
            pair_df.loc["rsi_ma_baseline", "n_trades"]
            if "rsi_ma_baseline" in pair_df.index else 0
        )
        if baseline_n > 0:
            print()
            for pop in _TEST_POPULATIONS:
                if pop in pair_df.index:
                    cov  = pair_df.loc[pop, "n_trades"] / baseline_n
                    flag = "  !! LOW" if cov < 0.30 else ""
                    print(f"    {pop:<26}  covers {cov * 100:.1f}% of rsi_ma_baseline bars{flag}")
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

    # Use rsi_ma_baseline as the reference for all lifts
    baseline_df = df[df["population"] == "rsi_ma_baseline"].set_index("pair")
    if baseline_df.empty:
        logger.error("No rsi_ma_baseline rows -- cannot compute verdict.")
        return

    baseline = baseline_df[["win_rate", "profit_factor", "n_trades"]].rename(
        columns={"win_rate": "wr_base", "profit_factor": "pf_base", "n_trades": "n_base"}
    )
    avg_base_wr = baseline["wr_base"].mean()
    avg_base_pf = baseline["pf_base"].mean()
    bw_str      = _fmt_param(config.kde_bandwidth_mult)

    # Also show kde_upper_baseline for reference
    kde_df = df[df["population"] == "kde_upper_baseline"].set_index("pair")
    if not kde_df.empty:
        avg_kde_pf = kde_df["profit_factor"].mean()
        avg_kde_wr = kde_df["win_rate"].mean()
        print(
            f"\n-- Setup 2 Trigger 8 ({config.entry_tf}) -- Verdict --\n"
            f"\n  [ref]  kde_upper_baseline ({config.entry_tf}):        "
            f"avg WR {avg_kde_wr * 100:.1f}%  avg PF {avg_kde_pf:.3f}"
        )
    else:
        print(f"\n-- Setup 2 Trigger 8 ({config.entry_tf}) -- Verdict --\n")

    print(
        f"  [base] rsi_ma_baseline ({config.rsi_ma_type}{config.rsi_ma_period}<{config.rsi_ma_threshold:.0f}):  "
        f"avg WR {avg_base_wr * 100:.1f}%  avg PF {avg_base_pf:.3f}  "
        f"[lift vs kde ref: {avg_base_pf - (avg_kde_pf if not kde_df.empty else 0):+.3f}]"
    )
    print(
        f"  KDE ({config.kde_tf}): window={config.kde_window}  bw={bw_str}  |  "
        f"RSI({config.rsi_period})  MFI({config.mfi_period})  "
        f"EMA({config.ema_fast},{config.ema_slow})  BB({config.bb_period})"
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
        f">= {config.min_pairs_passing} of {len(config.pairs)} pairs  "
        f"(vs rsi_ma_baseline)"
    )
    print()
    _print_final_verdict(passing, config, all_warnings, avg_base_pf)


def _save_results(results: pd.DataFrame, config: TestConfig, stem: str) -> None:
    csv_dir = config.results_dir / "csv"
    csv_dir.mkdir(parents=True, exist_ok=True)
    out = csv_dir / f"trigger8_results_{stem}.csv"
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
            f"  [XX]  SETUP 2 TRIGGER 8 ({config.entry_tf}) -- "
            "no condition improves on rsi_ma_baseline."
        )
        print(f"        rsi_ma_baseline avg PF was {base_pf:.3f}.")
        print("      Tuning ideas:")
        print(f"        * Lower rsi_ma_threshold (currently {config.rsi_ma_threshold})")
        print(f"        * Try rsi_ma_type='sma' (currently {config.rsi_ma_type})")
        print(f"        * Adjust ema_slow (currently {config.ema_slow})")
    else:
        confirmed = sorted(passing, key=lambda x: x[1], reverse=True)
        best_name, best_pf = confirmed[0]
        print(
            f"  [OK]  SETUP 2 TRIGGER 8 ({config.entry_tf}) CONFIRMED -- "
            f"{len(confirmed)} condition(s) improve on rsi_ma_baseline."
        )
        print(f"        rsi_ma_baseline avg PF {base_pf:.3f}  |  Best: {best_name}  (avg PF {best_pf:.3f})")
        print()

        groups: dict[str, list[tuple[str, float, str]]] = {}
        for name, pf in confirmed:
            g = _GROUP[name].strip()
            groups.setdefault(g, []).append((name, pf, "OK"))
        for non_name in _TEST_POPULATIONS:
            if not any(non_name == n for n, _ in confirmed):
                g = _GROUP[non_name].strip()
                groups.setdefault(g, []).append((non_name, 0.0, "--"))

        print("  -- Confirmed populations --")
        for group_name, items in groups.items():
            print(f"    [{group_name}]")
            for name, pf, status in items:
                pf_str = f"avg PF {pf:.3f}" if status == "OK" else ""
                print(f"      [{status}] {name:<26} {pf_str}")

        print()
        print("  Proceed using confirmed condition(s) for setup 3 construction.")

    if warnings:
        print()
        print("  Warnings (results valid -- interpret with care):")
        for w in warnings:
            print(f"    {w}")


if __name__ == "__main__":
    main()
