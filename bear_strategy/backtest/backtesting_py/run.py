"""Multi-pair backtesting.py runner for the Bear Strategy.

Usage
-----
    cd /path/to/pine_script
    source .venv/bin/activate
    python -m bear_strategy.backtest.backtesting_py.run

Or pass a custom config / params programmatically via run_all_pairs().

Exit-condition sweep
--------------------
    python -m bear_strategy.backtest.backtesting_py.run --sweep

Tests all 4 combinations of:
  use_fixed_tp   × use_vbt_sl_trail  (True/False each)
SL is always active — every combination produces trades.
"""

from __future__ import annotations

import logging
from dataclasses import replace
from itertools import product
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from backtesting import Backtest

from bear_strategy.backtest.backtesting_py.bt_strategy import BearStrategy
from bear_strategy.backtest.backtesting_py.configs.oss_validated import (
    DEFAULT_PARAMS,
    DEFAULT_RUN_CONFIG,
    RunConfig,
)
from bear_strategy.hypothesis_test_v2.engine.data_loader import load_funding, load_ohlcv
from bear_strategy.strategy.parameters import Parameters
from bear_strategy.strategy.signals import compute_atr, compute_entry_signal

log = logging.getLogger(__name__)


def _to_bt_df(df: pd.DataFrame) -> pd.DataFrame:
    """Rename lowercase OHLCV columns to the capitalised form backtesting.py expects."""
    return df[["open", "high", "low", "close", "volume"]].rename(
        columns={"open": "Open", "high": "High", "low": "Low",
                 "close": "Close", "volume": "Volume"}
    )


def run_pair(
    symbol: str,
    config: RunConfig,
    params: Parameters,
    results_dir: Path | None = None,
) -> dict[str, Any]:
    """Load data, compute signals, run backtesting.py for one symbol.

    Args:
        symbol:      Ticker, e.g. "BTCUSDT".
        config:      Run config (dates, cash, commission).
        params:      Strategy parameters.
        results_dir: If provided, save the stats CSV there.

    Returns:
        backtesting.py stats dict for the pair.
    """
    log.info("Loading data for %s …", symbol)
    df_1h = load_ohlcv(symbol, "1h",  config.start_date, config.end_date, params.data_dir)
    df_1d = load_ohlcv(symbol, "1d",  config.start_date, config.end_date, params.data_dir)
    funding_df = load_funding(symbol, config.start_date, config.end_date, params.data_dir)

    log.info("Computing entry signal for %s …", symbol)
    entry_signal = compute_entry_signal(df_1h, df_1d, funding_df, params)
    atr          = compute_atr(df_1h, params.atr_period)

    bt_df = _to_bt_df(df_1h)

    # Inject precomputed arrays into a *per-pair subclass* so parallel runs
    # (if ever used) don't overwrite each other's class attributes.
    attrs: dict[str, Any] = {
        "_entry_signal":  entry_signal.values,
        "_atr":           atr.values,
        "stop_mult":      params.stop_atr_mult,
        "target_mult":    params.target_atr_mult,
        "risk_pct":       config.risk_pct,
        "min_sl_pct":     params.min_sl_pct,
        # ── exit flags ────────────────────────────────────────────────────────
        "use_fixed_tp":     params.use_fixed_tp,
        "use_vbt_sl_trail": params.use_vbt_sl_trail,
        "sl_n_atr_trail":   params.sl_n_atr_trail,
    }

    # Precompute rolling swing-high only when trailing SL is requested.
    if params.use_vbt_sl_trail:
        swing_high = (
            df_1h["high"]
            .rolling(params.sl_swing_lookback, min_periods=1)
            .max()
        )
        attrs["_swing_high"] = swing_high.values

    strategy_cls = type(f"BearStrategy_{symbol}", (BearStrategy,), attrs)

    # FractionalBacktest handles assets priced above initial_cash (e.g. BTC at $50k+)
    bt = Backtest(
        bt_df,
        strategy_cls,
        cash             = config.initial_cash,
        commission       = config.commission,
        margin           = config.margin,
        exclusive_orders = True,   # one trade at a time (matches hypothesis test)
    )
    stats = bt.run()

    # Save interactive chart with trade markers for a selected pair.
    if config.plot_trades and symbol == config.plot_pair:
        chart_dir = (results_dir or Path("bear_strategy/backtest/backtesting_py/results"))
        chart_dir.mkdir(parents=True, exist_ok=True)
        chart_path = chart_dir / f"{symbol}_trades_chart.html"
        bt.plot(filename=str(chart_path), open_browser=False)
        log.info("Trade chart saved to %s", chart_path)

    if results_dir is not None:
        results_dir.mkdir(parents=True, exist_ok=True)
        out_path = results_dir / f"{symbol}_stats.csv"
        pd.Series(stats).to_csv(out_path)
        log.info("Stats saved to %s", out_path)

    return stats


def run_all_pairs(
    config: RunConfig = DEFAULT_RUN_CONFIG,
    params: Parameters = DEFAULT_PARAMS,
    results_dir: Path | None = None,
) -> dict[str, Any]:
    """Run the backtest for every pair in config.pairs.

    Args:
        config:      Run configuration (pairs, dates, cash, commission).
        params:      Strategy parameters.
        results_dir: Directory to write per-pair stat CSVs.

    Returns:
        Dict mapping symbol → backtesting.py stats object.
    """
    all_stats: dict[str, Any] = {}
    for symbol in config.pairs:
        try:
            stats = run_pair(symbol, config, params, results_dir)
            all_stats[symbol] = stats
            _print_summary(symbol, stats)
        except Exception:
            log.exception("Backtest failed for %s", symbol)

    _print_aggregate(all_stats)
    return all_stats


def _print_summary(symbol: str, stats: Any) -> None:
    n_trades = int(stats.get("# Trades", 0))
    ret      = stats.get("Return [%]", float("nan"))
    bnh      = stats.get("Buy & Hold Return [%]", float("nan"))
    wr       = stats.get("Win Rate [%]", float("nan"))
    dd       = stats.get("Max. Drawdown [%]", float("nan"))
    pf       = stats.get("Profit Factor", float("nan"))
    sqn      = stats.get("SQN", float("nan"))
    print(
        f"  {symbol:10s}  trades={n_trades:4d}  ret={ret:+7.2f}%  B&H={bnh:+7.2f}%  "
        f"WR={wr:.1f}%  PF={pf:.3f}  MaxDD={dd:.1f}%  SQN={sqn:.2f}"
    )


def _print_aggregate(all_stats: dict[str, Any]) -> None:
    if not all_stats:
        return
    rets = [s.get("Return [%]", float("nan")) for s in all_stats.values()]
    wrs  = [s.get("Win Rate [%]", float("nan")) for s in all_stats.values()]
    import numpy as np
    print(
        f"\n{'─'*65}\n"
        f"  {len(all_stats)} pairs │ avg return {float(pd.Series(rets).mean()):+.2f}% │ "
        f"avg WR {float(pd.Series(wrs).mean()):.1f}%"
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    _results = Path("bear_strategy/backtest/backtesting_py/results")
    print(f"\n{'═'*65}")
    print("  Bear Strategy — In-Sample Backtest (development window)")
    print(f"  Pairs: {DEFAULT_RUN_CONFIG.pairs}")
    print(f"  Range: {DEFAULT_RUN_CONFIG.start_date} → {DEFAULT_RUN_CONFIG.end_date}")
    print(f"  Cash: ${DEFAULT_RUN_CONFIG.initial_cash:,.0f}  Commission: {DEFAULT_RUN_CONFIG.commission*100:.2f}%")
    print(f"  Risk per trade: {DEFAULT_RUN_CONFIG.risk_pct*100:.1f}% of equity")
    print(f"{'═'*65}\n")

    run_all_pairs(results_dir=_results)
