"""CLI entry point for Trigger Search 1: event triggers on rsi_ma_below_50 baseline.

Usage:
    source .venv/bin/activate
    python -m bear_strategy.hypothesis_tests.trigger_search_1.run

Key parameters (all in config.py):
    entry_tf             -- entry timeframe (default: 1h)
    rsi_period           -- RSI period for baseline MA (default: 14)
    rsi_ma_period        -- MA period applied to RSI for baseline (default: 5)
    rsi_ma_type          -- "ema" or "sma" (default: ema)
    rsi_ma_threshold     -- baseline gate level (default: 50)
    atr_expansion_mult   -- bar range multiple for atr_expansion trigger (default: 1.5)
    macd_fast/slow/signal-- MACD params for macd_cross trigger (default: 12/26/9)
    rsi_cross_threshold  -- RSI level for rsi_cross_50 trigger (default: 50)
    ema_fast / ema_slow  -- EMA periods for ema_cross trigger (default: 9/20)
    bb_period / bb_std   -- Bollinger Band params for close_below_bb (default: 20/2.0)

----------------------------------------------------------------------
Design: event triggers vs held-state filters
----------------------------------------------------------------------
T8 showed held-state filters (RSI<50, EMA order, etc.) are 80-97% correlated
with rsi_ma_baseline and cannot add meaningful lift.

This test asks: "Which specific entry bar gives the best outcomes?"
Each trigger fires on ONE bar — the moment something happens.
Coverage will be sparse (2-20%) — that is expected and desired.

Reference:  kde_upper_baseline — regime AND kde_upper (Setup 1)
New base:   rsi_ma_baseline    — kde_upper_baseline AND rsi_ma < threshold

Seven event triggers tested on rsi_ma_baseline:

  bearish_engulfing     body fully engulfs prior bar (open>prev_close, close<prev_open)
  break_prior_low       close strictly below prior candle's low
  atr_expansion         bar range > atr_mult×ATR AND close < open
  macd_cross            MACD line crosses below signal line (event)
  rsi_cross_50          RSI crosses from above to below threshold (event)
  ema_cross             EMA(fast) crosses below EMA(slow) (event)
  close_below_bb        close < lower Bollinger Band

----------------------------------------------------------------------
Pass/fail criteria
----------------------------------------------------------------------
  Baseline for lift: rsi_ma_baseline PF.
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
from bear_strategy.hypothesis_tests.trigger_search_1.config import TestConfig
from bear_strategy.hypothesis_tests.trigger_search_1.runner import run_test

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

_DISPLAY_ORDER = [
    "kde_upper_baseline",
    "rsi_ma_baseline",
    "close_below_bb",
    "bearish_candle_size",
    "ema_cross_price",
]

_TEST_POPULATIONS = [p for p in _DISPLAY_ORDER if p not in ("kde_upper_baseline", "rsi_ma_baseline")]

_GROUP = {
    "close_below_bb":     "Volatility ",
    "bearish_candle_size": "Price Action",
    "ema_cross_price":    "Momentum   ",
}


def main() -> None:
    config = TestConfig()
    bw_str = _fmt_param(config.kde_bandwidth_mult)
    bb_str = _fmt_param(config.bb_std)

    logger.info("=" * 70)
    logger.info("Bear Strategy -- Trigger Search 1: event triggers on rsi_ma baseline")
    logger.info("Entry TF : %s  |  KDE TF: %s", config.entry_tf, config.kde_tf)
    logger.info(
        "Baseline : regime AND kde_upper AND RSI_MA(%s,%d) < %.0f",
        config.rsi_ma_type, config.rsi_ma_period, config.rsi_ma_threshold,
    )
    logger.info("Pairs    : %s", config.pairs)
    logger.info("KDE      : tf=%s  window=%d  bw_mult=%s", config.kde_tf, config.kde_window, bw_str)
    logger.info(
        "close_below_bb     : close < lower BB(%d, %.1fstd) [BASE CONFIRMED]",
        config.bb_period, config.bb_std,
    )
    logger.info(
        "bearish_candle_size: bar_range in [%.1f–%.1f]×ATR AND close < open",
        config.atr_candle_min, config.atr_candle_max,
    )
    logger.info(
        "ema_cross_price    : price crosses below EMA(%d) (event)",
        config.ema_cross_period,
    )
    logger.info(
        "Stop: %.1f × ATR  Target: %.1f × ATR  (period=%d)",
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
            f"ts1_kde{config.kde_window}_bw{bw_str}"
            f"_rsiMA{config.rsi_ma_type}{config.rsi_ma_period}h{int(config.rsi_ma_threshold)}"
            f"_bb{config.bb_period}s{bb_str}"
            f"_atrCandle{_fmt_param(config.atr_candle_min)}_{_fmt_param(config.atr_candle_max)}"
            f"_emaXPrice{config.ema_cross_period}"
        ),
    )

    _config_params = {
        "entry_tf":            config.entry_tf,
        "kde_tf":              config.kde_tf,
        "stop_atr_mult":       config.stop_atr_mult,
        "target_atr_mult":     config.target_atr_mult,
        "atr_period":          config.atr_period,
        "kde_window":          config.kde_window,
        "kde_bandwidth_mult":  config.kde_bandwidth_mult,
        "rsi_period":          config.rsi_period,
        "rsi_ma_period":       config.rsi_ma_period,
        "rsi_ma_type":         config.rsi_ma_type,
        "rsi_ma_threshold":    config.rsi_ma_threshold,
        "bb_period":           config.bb_period,
        "bb_std":              config.bb_std,
        "atr_candle_min":      config.atr_candle_min,
        "atr_candle_max":      config.atr_candle_max,
        "ema_cross_period":    config.ema_cross_period,
    }

    with capture_prints() as buf:
        _print_summary(results, config)
        _save_results(results, config, stem)
        _print_verdict(results, config)

    md_path = config.results_dir / f"trigger_search_1_{stem}.md"
    save_report(
        buf.text,
        md_path,
        (
            f"Trigger Search 1  "
            f"(entry_tf={config.entry_tf}  kde_tf={config.kde_tf}  "
            f"baseline=rsi_ma_{config.rsi_ma_type}{config.rsi_ma_period}<{config.rsi_ma_threshold:.0f})"
        ),
        config_params=_config_params,
    )


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

def _print_summary(results: pd.DataFrame, config: TestConfig) -> None:
    print(
        f"\n-- Per-Pair Results  "
        f"(baseline = rsi_ma_{config.rsi_ma_type}{config.rsi_ma_period}<{config.rsi_ma_threshold:.0f}"
        f"  entry_tf={config.entry_tf}) --\n"
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
                    flag = "  !! LOW" if cov < 0.05 else ""
                    print(f"    {pop:<22}  covers {cov * 100:.1f}% of rsi_ma_baseline{flag}")
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

    kde_df = df[df["population"] == "kde_upper_baseline"].set_index("pair")
    avg_kde_pf = kde_df["profit_factor"].mean() if not kde_df.empty else float("nan")
    avg_kde_wr = kde_df["win_rate"].mean()       if not kde_df.empty else float("nan")

    print(f"\n-- Trigger Search 2 ({config.entry_tf}) -- Verdict --\n")
    print(
        f"  [ref]  kde_upper_baseline:   avg WR {avg_kde_wr * 100:.1f}%  avg PF {avg_kde_pf:.3f}"
    )
    print(
        f"  [base] rsi_ma_{config.rsi_ma_type}{config.rsi_ma_period}<{config.rsi_ma_threshold:.0f}:   "
        f"avg WR {avg_base_wr * 100:.1f}%  avg PF {avg_base_pf:.3f}  "
        f"[+{avg_base_pf - avg_kde_pf:.3f} vs ref]"
    )
    print(
        f"  Close Below BB({config.bb_period},{config.bb_std}std)  +  "
        f"Bearish Candle [{config.atr_candle_min}–{config.atr_candle_max}]×ATR  +  "
        f"EMA({config.ema_cross_period}) Cross"
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

        wr_fail_pairs  = [p for p in joined.index if joined.loc[p, "wr_lift"] <= joined.loc[p, "min_wr_lift"]]
        sparse_pairs   = [p for p in joined.index if coverage.loc[p] < 0.05]
        low_cov_pairs  = [p for p in joined.index if 0.05 <= coverage.loc[p] < 0.15]

        if wr_fail_pairs:
            all_warnings.append(f"!! [{pop}] WR lift below threshold on: {', '.join(wr_fail_pairs)}")
        if sparse_pairs:
            all_warnings.append(f"!! [{pop}] very sparse (<5% baseline) on: {', '.join(sparse_pairs)}")

        warn_tags = []
        if wr_fail_pairs:
            warn_tags.append(f"WR {len(wr_fail_pairs)}p")
        if sparse_pairs:
            warn_tags.append(f"sparse {len(sparse_pairs)}p")
        elif low_cov_pairs:
            warn_tags.append(f"low# {len(low_cov_pairs)}p")
        warn_str = ("  warn: " + ", ".join(warn_tags)) if warn_tags else ""

        avg_cov = coverage.mean() * 100
        print(
            f"  [{_GROUP[pop]}]  {pop:<22}  "
            f"WR lift {avg_wr_lift:+.1f}pp  avg PF {avg_pf:.3f}  "
            f"PF lift {avg_pf_lift:+.3f}  cov {avg_cov:.1f}%  "
            f"{n_passing}/{n_pairs} pairs  [{status}]{warn_str}"
        )

        for pair, row in joined.iterrows():
            pair_status = "OK" if row["pair_passes"] else "--"
            pair_cov    = coverage.loc[pair] if pair in coverage.index else float("nan")
            notes = []
            if row["wr_lift"] <= row["min_wr_lift"]:
                notes.append("WR!")
            notes.append(f"cov {pair_cov * 100:.1f}%{'!' if pair_cov < 0.05 else ''}")
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
    out = csv_dir / f"trigger_search_1_{stem}.csv"
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
            f"  [XX]  TRIGGER SEARCH 1 ({config.entry_tf}) -- "
            "no event trigger improves on rsi_ma_baseline."
        )
        print(f"        rsi_ma_baseline avg PF was {base_pf:.3f}.")
        print("      Tuning ideas:")
        print(f"        * Loosen atr_expansion_mult (currently {config.atr_expansion_mult})")
        print(f"        * Try rsi_cross_threshold=45 (currently {config.rsi_cross_threshold})")
        print(f"        * Adjust bb_std (currently {config.bb_std})")
    else:
        confirmed = sorted(passing, key=lambda x: x[1], reverse=True)
        best_name, best_pf = confirmed[0]
        print(
            f"  [OK]  TRIGGER SEARCH 1 ({config.entry_tf}) CONFIRMED -- "
            f"{len(confirmed)} event trigger(s) improve on rsi_ma_baseline."
        )
        print(f"        rsi_ma_baseline avg PF {base_pf:.3f}  |  Best: {best_name}  (avg PF {best_pf:.3f})")
        print()

        groups: dict[str, list[tuple[str, float, str]]] = {}
        confirmed_names = {n for n, _ in confirmed}
        for name, pf in confirmed:
            g = _GROUP[name].strip()
            groups.setdefault(g, []).append((name, pf, "OK"))
        for non_name in _TEST_POPULATIONS:
            if non_name not in confirmed_names:
                g = _GROUP[non_name].strip()
                groups.setdefault(g, []).append((non_name, 0.0, "--"))

        print("  -- Confirmed triggers --")
        for group_name, items in groups.items():
            print(f"    [{group_name}]")
            for name, pf, status in items:
                pf_str = f"avg PF {pf:.3f}" if status == "OK" else ""
                print(f"      [{status}] {name:<22} {pf_str}")

        print()
        print("  These event triggers can be used as entry timing signals in Setup 3.")

    if warnings:
        print()
        print("  Warnings (results valid -- interpret with care):")
        for w in warnings:
            print(f"    {w}")


if __name__ == "__main__":
    main()
