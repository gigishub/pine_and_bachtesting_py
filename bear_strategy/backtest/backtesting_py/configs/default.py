"""Default single-run config for the backtesting.py engine."""

from __future__ import annotations

from bear_strategy.backtest.config import BacktestConfig

DEFAULT_CONFIG = BacktestConfig(
    symbol="BTCUSDT",
    timeframe="15m",
    start_time="2021-01-01 00:00:00",
    commission=0.0008,
    plot=False,
)
