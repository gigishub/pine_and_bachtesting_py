"""Bear Strategy — vectorbt backtest entry point.

Edit ``bear_strategy/backtest/vectorbt/configs/default.py`` to set
pairs, date window, SL/TP multiples, and execution costs, then run:

    source .venv/bin/activate
    python -m bear_strategy.backtest.vectorbt.run

CLI flags always override the file-based config:

    python -m bear_strategy.backtest.vectorbt.run \\
        --pairs BTCUSDT ETHUSDT \\
        --start 2021-01-01 --end 2023-11-01 \\
        --sl-mult 1.5 --tp-mult 2.5 \\
        --min-sl-pct 0.008 \\
        --fees 0.001 --cash 20000

Results are saved to:
    bear_strategy/backtest/vectorbt/results/<YYYY-MM-DD_HHMM>/

One CSV per pair with per-trade records, plus a summary CSV across all pairs.

DESIGN NOTES
------------
• Short-only: entry on regime + funding guard + VP trigger; exit via sl_stop / tp_stop.
• fill_at_next_open=True: signal fires at close[N], fills at open[N+1].
• Fees: configurable; default 0.08% round-trip taker (Bybit standard).
• Min SL filter: entries with sl_pct < min_sl_pct are skipped.
"""

from __future__ import annotations

import argparse
import dataclasses
import logging
import math
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd

# Allow running from project root without `pip install -e .`
_ROOT = Path(__file__).parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from bear_strategy.backtest.vectorbt.configs.default import VbtRunConfig, build_config
from bear_strategy.backtest.vectorbt.metrics import extract_stats
from bear_strategy.backtest.vectorbt.runner import run
from bear_strategy.hypothesis_test_v2.engine.data_loader import (
    load_funding,
    load_ohlcv,
)

log = logging.getLogger(__name__)

# Convenience date-window shortcuts (override start/end in the config or via CLI)
_WINDOWS: dict[str, dict[str, str]] = {
    "dev": {"start": "2021-01-01", "end": "2023-11-01"},
    "oos": {"start": "2023-11-02", "end": "2026-04-22"},
}


# ── Core run helpers ──────────────────────────────────────────────────────────

def run_pair(
    symbol: str,
    *,
    cfg: VbtRunConfig,
) -> pd.Series:
    """Load data and run the vectorbt backtest for one symbol.

    Args:
        symbol: Ticker, e.g. "BTCUSDT".
        cfg:    Full run configuration.

    Returns:
        Standardised stats pd.Series.
    """
    params = cfg.to_parameters()
    log.info("Loading %s …", symbol)
    df_1h      = load_ohlcv(symbol, "1h", cfg.start_date, cfg.end_date, params.data_dir)
    df_1d      = load_ohlcv(symbol, "1d", cfg.start_date, cfg.end_date, params.data_dir)
    funding_df = load_funding(symbol, cfg.start_date, cfg.end_date, params.data_dir)

    log.info("Running VBT backtest for %s …", symbol)
    pf = run(df_1h, df_1d, funding_df, params, fees=cfg.fees, init_cash=cfg.init_cash)
    return extract_stats(pf)


def run_all(
    cfg: VbtRunConfig,
    *,
    results_dir: Path | None = None,
) -> dict[str, pd.Series]:
    """Run the backtest for every pair in cfg.pairs.

    Args:
        cfg:         Full run configuration.
        results_dir: If provided, saves a summary CSV and per-pair stat CSVs there.

    Returns:
        Dict mapping symbol → stats Series.
    """
    all_stats: dict[str, pd.Series] = {}

    for symbol in cfg.pairs:
        try:
            stats = run_pair(symbol, cfg=cfg)
            all_stats[symbol] = stats
            _print_pair(symbol, stats)
        except Exception:
            log.exception("Backtest failed for %s", symbol)

    _print_aggregate(all_stats)

    if results_dir is not None:
        _save_results(all_stats, results_dir, cfg)

    return all_stats


# ── Output helpers ────────────────────────────────────────────────────────────

def _print_pair(symbol: str, stats: pd.Series) -> None:
    n   = int(stats.get("# Trades", 0))
    ret = _f(stats, "Return [%]")
    wr  = _f(stats, "Win Rate [%]")
    pf  = _f(stats, "Profit Factor")
    dd  = _f(stats, "Max. Drawdown [%]")
    exp = _f(stats, "Expectancy [%]")
    sqn = _f(stats, "SQN")
    print(
        f"  {symbol:10s}  trades={n:4d}  ret={ret:+7.2f}%  "
        f"WR={wr:.1f}%  PF={pf:.3f}  MaxDD={dd:.1f}%  "
        f"Exp={exp:+.2f}%  SQN={sqn:.2f}"
    )


def _f(stats: pd.Series, key: str) -> float:
    try:
        v = float(stats.get(key, math.nan))
        return v if not math.isnan(v) else 0.0
    except (TypeError, ValueError):
        return 0.0


def _print_aggregate(all_stats: dict[str, pd.Series]) -> None:
    if not all_stats:
        return
    rets = [_f(s, "Return [%]")    for s in all_stats.values()]
    wrs  = [_f(s, "Win Rate [%]")  for s in all_stats.values()]
    pfs  = [_f(s, "Profit Factor") for s in all_stats.values()]
    print(
        f"\n{'─'*70}\n"
        f"  {len(all_stats)} pairs │ avg return {pd.Series(rets).mean():+.2f}% │ "
        f"avg WR {pd.Series(wrs).mean():.1f}% │ avg PF {pd.Series(pfs).mean():.3f}"
    )


def _save_results(
    all_stats: dict[str, pd.Series],
    results_dir: Path,
    cfg: VbtRunConfig,
) -> None:
    results_dir.mkdir(parents=True, exist_ok=True)

    if not all_stats:
        log.warning("No successful pair results — nothing to save.")
        return

    rows = [{"Symbol": sym, **stats.to_dict()} for sym, stats in all_stats.items()]
    summary = pd.DataFrame(rows).set_index("Symbol")
    summary_path = results_dir / "summary.csv"
    summary.to_csv(summary_path)
    log.info("Summary saved → %s", summary_path)

    for symbol, stats in all_stats.items():
        stats.to_csv(results_dir / f"{symbol}_stats.csv")

    # Save the full config so results are self-documenting
    pd.Series(dataclasses.asdict(cfg)).to_csv(results_dir / "config.csv")
    log.info("Config saved → %s", results_dir / "config.csv")


# ── CLI entry point ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Bear Strategy — vectorbt multi-pair backtest.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--window",
        choices=["dev", "oos"],
        default=None,
        help="Shortcut date window: dev=in-sample, oos=out-of-sample. "
             "Overrides --start / --end and the config file dates.",
    )
    parser.add_argument(
        "--start",
        default=None,
        metavar="YYYY-MM-DD",
        help="Override start date from config.",
    )
    parser.add_argument(
        "--end",
        default=None,
        metavar="YYYY-MM-DD",
        help="Override end date from config.",
    )
    parser.add_argument(
        "--pairs",
        nargs="+",
        default=None,
        help="Override pairs from config (e.g. BTCUSDT ETHUSDT).",
    )
    parser.add_argument(
        "--sl-mult",
        type=float,
        default=None,
        metavar="FLOAT",
        help="Override stop_atr_mult (e.g. 1.5).",
    )
    parser.add_argument(
        "--tp-mult",
        type=float,
        default=None,
        metavar="FLOAT",
        help="Override target_atr_mult (e.g. 2.5).",
    )
    parser.add_argument(
        "--min-sl-pct",
        type=float,
        default=None,
        metavar="FLOAT",
        help="Override min SL distance filter (fraction, e.g. 0.005 for 0.5%%).",
    )
    parser.add_argument(
        "--entry-every-n",
        type=int,
        default=None,
        metavar="INT",
        help="Keep every Nth trigger (e.g. 2 keeps every second trigger).",
    )
    parser.add_argument(
        "--entry-phase",
        type=int,
        default=None,
        metavar="INT",
        help="Which hit to keep in each N-trigger cycle (1..N).",
    )
    parser.add_argument(
        "--use-exit-rsi",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Toggle daily RSI exit on/off.",
    )
    parser.add_argument(
        "--exit-mode",
        choices=["fixed_tp", "rsi_cross_up", "fixed_tp_or_rsi_cross_up"],
        default=None,
        help="Exit rule while always keeping SL active.",
    )
    parser.add_argument(
        "--exit-rsi-period",
        type=int,
        default=None,
        metavar="INT",
        help="Daily RSI period for RSI-based exits.",
    )
    parser.add_argument(
        "--exit-rsi-level",
        type=float,
        default=None,
        metavar="FLOAT",
        help="Exit short when daily RSI crosses above this level.",
    )
    parser.add_argument(
        "--fees",
        type=float,
        default=None,
        metavar="FLOAT",
        help="Override round-trip taker fee fraction (e.g. 0.0008).",
    )
    parser.add_argument(
        "--cash",
        type=float,
        default=None,
        metavar="FLOAT",
        help="Override starting cash.",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )

    # Load base config from configs/default.py
    cfg = build_config()

    # Apply --window shortcut first (overrides config dates)
    if args.window is not None:
        w = _WINDOWS[args.window]
        cfg = dataclasses.replace(cfg, start_date=w["start"], end_date=w["end"])

    # Apply individual CLI overrides
    overrides: dict[str, Any] = {}
    if args.start       is not None: overrides["start_date"]      = args.start
    if args.end         is not None: overrides["end_date"]         = args.end
    if args.pairs       is not None: overrides["pairs"]            = args.pairs
    if args.sl_mult     is not None: overrides["stop_atr_mult"]    = args.sl_mult
    if args.tp_mult     is not None: overrides["target_atr_mult"]  = args.tp_mult
    if args.min_sl_pct  is not None: overrides["min_sl_pct"]       = args.min_sl_pct
    if args.entry_every_n is not None: overrides["entry_every_n"]  = args.entry_every_n
    if args.entry_phase is not None: overrides["entry_phase"]      = args.entry_phase
    if args.use_exit_rsi is not None: overrides["use_exit_rsi"]    = args.use_exit_rsi
    if args.exit_mode is not None: overrides["exit_mode"]          = args.exit_mode
    if args.exit_rsi_period is not None: overrides["exit_rsi_period"] = args.exit_rsi_period
    if args.exit_rsi_level is not None: overrides["exit_rsi_level"] = args.exit_rsi_level
    if args.fees        is not None: overrides["fees"]              = args.fees
    if args.cash        is not None: overrides["init_cash"]         = args.cash
    if overrides:
        cfg = dataclasses.replace(cfg, **overrides)

    ts          = datetime.now().strftime("%Y-%m-%d_%H%M")
    tag         = args.window.upper() if args.window else "CUSTOM"
    results_dir = cfg.results_root / f"{ts}_{tag}"

    print(f"\n{'═'*70}")
    print("  Bear Strategy — vectorbt Backtest")
    for line in cfg.summary_lines():
        print(line)
    print(f"  Results  : {results_dir}")
    print(f"{'═'*70}\n")

    run_all(cfg=cfg, results_dir=results_dir)
