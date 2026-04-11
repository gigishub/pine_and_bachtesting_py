"""Data loading and single-run backtest for the Adaptive Momentum Strategy.

Usage (from project root):
    source .venv/bin/activate
    python -m adaptive_momentum_strategy.backtest.backtesting_py.run
"""

from __future__ import annotations

import logging

import pandas as pd
from backtesting import Backtest

from adaptive_momentum_strategy.backtest.config import BacktestConfig
from adaptive_momentum_strategy.backtest.backtesting_py.strategy import AdaptiveMomentumStrategy

logger = logging.getLogger(__name__)


def load_data(cfg: BacktestConfig) -> pd.DataFrame:
    """Fetch OHLCV data via the UPS_py_v2 unified loader (with disk cache)."""
    import sys
    from pathlib import Path

    _root = Path(__file__).parents[4]
    if str(_root) not in sys.path:
        sys.path.insert(0, str(_root))

    from UPS_py_v2.data.fetch import load_ohlcv

    logger.info(
        "Loading %s %s %s from %s",
        cfg.symbol, cfg.market_type, cfg.timeframe, cfg.start_time,
    )
    df = load_ohlcv(
        source="bybit",
        symbol=cfg.symbol,
        market_type=cfg.market_type,
        timeframe=cfg.timeframe,
        start_time=cfg.start_time,
        end_time=cfg.end_time,
    )
    if df.empty:
        raise ValueError("No data returned -- check symbol/timeframe/date range.")
    logger.info("Loaded %d bars  (%s -> %s)", len(df), df.index[0], df.index[-1])
    return df


def run_backtest(cfg: BacktestConfig | None = None) -> object:
    """Run a single backtest and return the stats object."""
    if cfg is None:
        cfg = BacktestConfig()

    df = load_data(cfg)

    bt = Backtest(
        df,
        AdaptiveMomentumStrategy,
        cash=cfg.initial_cash,
        commission=cfg.commission,
        exclusive_orders=True,
    )

    stats = bt.run()
    logger.info("\n%s", stats)

    if cfg.plot:
        bt.plot()

    return stats
