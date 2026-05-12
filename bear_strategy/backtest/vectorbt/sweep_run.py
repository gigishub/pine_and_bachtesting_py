"""Bear Strategy — SL/TP grid sweep entry point.

Runs the bear strategy across every combination defined in a named sweep
config and prints pivot tables so you can identify which parameter settings
perform best.

Usage
-----
    source .venv/bin/activate
    python -m bear_strategy.backtest.vectorbt.sweep_run

    # Named config (see backtest/vectorbt/configs/ for options):
    python -m bear_strategy.backtest.vectorbt.sweep_run --config is_broad
    python -m bear_strategy.backtest.vectorbt.sweep_run --config oos_broad
    python -m bear_strategy.backtest.vectorbt.sweep_run --config rsi_exit_sweep

    # Quick overrides (applied on top of whatever config is loaded):
    python -m bear_strategy.backtest.vectorbt.sweep_run --config is_broad \\
        --pairs BTCUSDT ETHUSDT \\
        --window dev

Output
------
One results directory per run:
    bear_strategy/backtest/vectorbt/results/<YYYY-MM-DD_HHMM>_SWEEP/

  sweep_summary.csv  — one row per (combo × symbol)
  pivot_return.csv   — Return [%] pivot:  rows=SL, cols=TP
  pivot_winrate.csv  — Win Rate [%] pivot
  pivot_pf.csv       — Profit Factor pivot
  pivot_trades.csv   — Trade count pivot
  pivot_sqn.csv      — SQN pivot
  base_config.csv    — snapshot of the base VbtRunConfig used
"""

from __future__ import annotations

import argparse
import dataclasses
import logging
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

_ROOT = Path(__file__).parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from bear_strategy.backtest.vectorbt.configs import load_sweep_config
from bear_strategy.backtest.vectorbt.configs.sweep import SweepConfig, SweepCombo
from bear_strategy.backtest.vectorbt.metrics import extract_stats
from bear_strategy.backtest.vectorbt.runner import run
from bear_strategy.hypothesis_test_v2.engine.data_loader import load_funding, load_ohlcv

log = logging.getLogger(__name__)

_WINDOWS = {
    "dev": {"start": "2021-01-01", "end": "2023-11-01"},
    "oos": {"start": "2023-11-02", "end": "2026-04-22"},
}

# All metrics saved to sweep_summary.csv — everything extract_stats() returns
# except the non-numeric "Max. Drawdown Duration" field.
_PIVOT_METRICS = [
    "Return [%]",
    "Expectancy [%]",
    "Profit Factor",
    "Win Rate [%]",
    "# Trades",
    "Max. Drawdown [%]",
    "Recovery Factor",
    "SQN",
    "Sharpe Ratio",
    "Sortino Ratio",
    "Calmar Ratio",
    "Omega Ratio",
    "R:R Ratio",
    "Avg. Win Trade [%]",
    "Avg. Loss Trade [%]",
    "Best Trade [%]",
    "Worst Trade [%]",
]


# ── Core sweep logic ──────────────────────────────────────────────────────────

def run_sweep(cfg: SweepConfig) -> pd.DataFrame:
    """Run all combos defined by ``cfg.combinations()`` and return a tidy DataFrame.

    Args:
        cfg: Sweep configuration (pairs, date window, SL/TP grid, exit dims).

    Returns:
        DataFrame with columns: sl_mult, tp_mult, exit_mode, exit_rsi_level,
        symbol + all metric columns.
    """
    combos = cfg.combinations()
    base   = cfg.base
    params = base.to_parameters()

    # Pre-load all data once so we don't hit disk on every combo
    log.info("Pre-loading OHLCV and funding data for %d pairs …", len(base.pairs))
    data: dict[str, dict] = {}
    for symbol in base.pairs:
        try:
            data[symbol] = {
                "1h":      load_ohlcv(symbol, "1h", base.start_date, base.end_date, params.data_dir),
                "1d":      load_ohlcv(symbol, "1d", base.start_date, base.end_date, params.data_dir),
                "funding": load_funding(symbol, base.start_date, base.end_date, params.data_dir),
            }
        except Exception:
            log.exception("Failed to load data for %s — skipping.", symbol)

    rows: list[dict] = []
    total = len(combos) * len(data)
    done  = 0

    for combo in combos:
        # Apply all swept dimensions on top of the base params
        combo_params = dataclasses.replace(
            params,
            stop_atr_mult      = combo.sl_mult,
            target_atr_mult    = combo.tp_mult,
            exit_mode          = combo.exit_mode,
            use_exit_rsi       = "rsi_cross_up" in combo.exit_mode,
            exit_rsi_level     = (
                combo.exit_rsi_level
                if combo.exit_rsi_level is not None
                else params.exit_rsi_level
            ),
            rsi_oversold_level = (
                combo.rsi_oversold_level
                if combo.rsi_oversold_level is not None
                else params.rsi_oversold_level
            ),
            exit_ema_period    = (
                combo.exit_ema_period
                if combo.exit_ema_period is not None
                else params.exit_ema_period
            ),
        )

        # Build a short human-readable label for the mode-specific param
        mode_param_str = "—"
        if combo.exit_rsi_level is not None:
            mode_param_str = f"rsi_lvl={combo.exit_rsi_level:.0f}"
        elif combo.rsi_oversold_level is not None:
            mode_param_str = f"os_lvl={combo.rsi_oversold_level:.0f}"
        elif combo.exit_ema_period is not None:
            mode_param_str = f"ema={combo.exit_ema_period}"

        for symbol, dfs in data.items():
            done += 1
            log.info(
                "[%d/%d] SL=%.1f× TP=%.1f× exit=%s %s %s",
                done, total, combo.sl_mult, combo.tp_mult,
                combo.exit_mode, mode_param_str, symbol,
            )
            try:
                pf    = run(dfs["1h"], dfs["1d"], dfs["funding"], combo_params,
                            fees=base.fees, init_cash=base.init_cash)
                stats = extract_stats(pf)
                row   = {
                    "sl_mult":            combo.sl_mult,
                    "tp_mult":            combo.tp_mult,
                    "exit_mode":          combo.exit_mode,
                    "exit_rsi_level":     combo.exit_rsi_level,
                    "rsi_oversold_level": combo.rsi_oversold_level,
                    "exit_ema_period":    combo.exit_ema_period,
                    "symbol":             symbol,
                }
                row.update({k: stats.get(k) for k in _PIVOT_METRICS})
                rows.append(row)
            except Exception:
                log.exception("Failed: SL=%.1f TP=%.1f %s", combo.sl_mult, combo.tp_mult, symbol)

    return pd.DataFrame(rows)


# ── Reporting helpers ─────────────────────────────────────────────────────────

def _pivot(
    df: pd.DataFrame,
    metric: str,
    min_trades: int,
    exit_mode: str | None = None,
) -> pd.DataFrame:
    """Build a SL×TP pivot table averaged across all pairs.

    Args:
        exit_mode: When set, only rows with this exit_mode are included.
                   Pass ``None`` to include all rows (single-mode sweeps).

    Cells where total trades < min_trades are replaced with NaN.
    """
    d = df
    if exit_mode is not None and "exit_mode" in df.columns:
        d = df[df["exit_mode"] == exit_mode]
    trades_mean = (
        d.groupby(["sl_mult", "tp_mult"])["# Trades"]
        .sum()
        .rename("total_trades")
        .reset_index()
    )
    mean_vals = (
        d.groupby(["sl_mult", "tp_mult"])[metric]
        .mean()
        .reset_index()
    )
    merged = mean_vals.merge(trades_mean, on=["sl_mult", "tp_mult"])
    merged.loc[merged["total_trades"] < min_trades, metric] = float("nan")

    pivot = merged.pivot(index="sl_mult", columns="tp_mult", values=metric)
    pivot.index.name   = f"SL mult \\ {metric}"
    pivot.columns.name = "TP mult"
    return pivot


def _print_pivot(pivot: pd.DataFrame, title: str) -> None:
    """Pretty-print a pivot table to stdout."""
    print(f"\n{'─'*60}")
    print(f"  {title}")
    print(f"{'─'*60}")
    print(pivot.to_string(float_format=lambda x: f"{x:+.2f}" if x == x else "  n/a"))


def _print_best(df: pd.DataFrame, metric: str, top_n: int = 5) -> None:
    """Print the top N (sl_mult, tp_mult) combinations by metric."""
    agg = df.groupby(["sl_mult", "tp_mult"]).agg(
        mean_metric=(metric, "mean"),
        total_trades=("# Trades", "sum"),
    ).reset_index()
    agg = agg[agg["total_trades"] >= 5].sort_values("mean_metric", ascending=False)
    print(f"\n  Top {top_n} by avg {metric}:")
    for _, row in agg.head(top_n).iterrows():
        print(f"    SL={row['sl_mult']:.1f}×  TP={row['tp_mult']:.1f}×  "
              f"avg {metric}={row['mean_metric']:+.2f}  trades={int(row['total_trades'])}")


def _save(results_dir: Path, df: pd.DataFrame, cfg: SweepConfig) -> None:
    results_dir.mkdir(parents=True, exist_ok=True)

    df.to_csv(results_dir / "sweep_summary.csv", index=False)
    log.info("Sweep summary → %s", results_dir / "sweep_summary.csv")

    # Pivots use the primary (first) exit mode so SL×TP tables are clean
    primary_mode = cfg.exit_modes[0] if cfg.exit_modes else None
    for metric, fname in [
        ("Return [%]",    "pivot_return.csv"),
        ("Win Rate [%]",  "pivot_winrate.csv"),
        ("Profit Factor", "pivot_pf.csv"),
        ("# Trades",      "pivot_trades.csv"),
        ("SQN",           "pivot_sqn.csv"),
    ]:
        pivot = _pivot(df, metric, cfg.min_trades, exit_mode=primary_mode)
        pivot.to_csv(results_dir / fname)

    pd.Series(dataclasses.asdict(cfg.base)).to_csv(results_dir / "base_config.csv")
    log.info("Results saved → %s", results_dir)


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Bear Strategy — parameter sweep runner.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--config", default="is_broad",
        help=(
            "Named sweep config to load from configs/  (filename without .py).  "
            "Available: is_broad, oos_broad, rsi_exit_sweep — or any file you add."
        ),
    )
    # ── Quick overrides (applied on top of the loaded config) ────────────────
    parser.add_argument(
        "--window", choices=["dev", "oos"], default=None,
        help="Date window shortcut: dev=2021-01-01→2023-11-01, oos=2023-11-02→2026-04-22.",
    )
    parser.add_argument(
        "--pairs", nargs="+", default=None,
        help="Override pairs (e.g. --pairs BTCUSDT ETHUSDT).",
    )
    parser.add_argument(
        "--entry-every-n", type=int, default=None,
        help="Keep every Nth trigger.",
    )
    parser.add_argument(
        "--entry-phase", type=int, default=None,
        help="Which hit to keep in each N-trigger cycle (1..N).",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

    cfg = load_sweep_config(args.config)

    # Apply CLI overrides
    if args.window:
        w    = _WINDOWS[args.window]
        base = dataclasses.replace(cfg.base, start_date=w["start"], end_date=w["end"])
        cfg  = dataclasses.replace(cfg, base=base)
    if args.pairs:
        base = dataclasses.replace(cfg.base, pairs=args.pairs)
        cfg  = dataclasses.replace(cfg, base=base)
    if args.entry_every_n is not None:
        base = dataclasses.replace(cfg.base, entry_every_n=args.entry_every_n)
        cfg  = dataclasses.replace(cfg, base=base)
    if args.entry_phase is not None:
        base = dataclasses.replace(cfg.base, entry_phase=args.entry_phase)
        cfg  = dataclasses.replace(cfg, base=base)

    combos = cfg.combinations()

    print(f"\n{'═'*60}")
    print(f"  Bear Strategy — Sweep  (config: {args.config})")
    for line in cfg.base.summary_lines():
        print(line)
    print(f"  SL range    : {cfg.sl_mults}")
    print(f"  TP range    : {cfg.tp_mults}")
    print(f"  Exit modes  : {cfg.exit_modes}")
    if any("rsi" in m for m in cfg.exit_modes):
        print(f"  RSI levels  : {cfg.exit_rsi_levels}")
    print(f"  Combos      : {len(combos)} valid  (tp > sl)")
    print(f"  Total runs  : {len(combos) * len(cfg.base.pairs)}")
    print(f"{'═'*60}\n")

    df = run_sweep(cfg)

    if df.empty:
        print("No results — check data availability.")
        sys.exit(1)

    # Pivot tables are shown for the primary (first) exit mode only
    pm = cfg.exit_modes[0] if cfg.exit_modes else None
    _print_pivot(_pivot(df, "Return [%]",    cfg.min_trades, pm), "Avg Return [%]    (rows=SL mult, cols=TP mult)")
    _print_pivot(_pivot(df, "Win Rate [%]",  cfg.min_trades, pm), "Avg Win Rate [%]")
    _print_pivot(_pivot(df, "Profit Factor", cfg.min_trades, pm), "Avg Profit Factor")
    _print_pivot(_pivot(df, "SQN",           cfg.min_trades, pm), "Avg SQN")
    _print_pivot(_pivot(df, "# Trades",      0,              pm), "Total Trades")

    # Print top combos by key metrics
    _print_best(df, "Return [%]")
    _print_best(df, "Profit Factor")
    _print_best(df, "SQN")

    ts          = datetime.now().strftime("%Y-%m-%d_%H%M")
    results_dir = cfg.base.results_root / f"{ts}_SWEEP_{args.config.upper()}"
    _save(results_dir, df, cfg)

    print(f"\n  Results saved → {results_dir}\n")
