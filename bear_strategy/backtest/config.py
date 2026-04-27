"""Backtest configuration — data source, fees, and execution assumptions."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class DatasetConfig:
    """Immutable descriptor for one pair / timeframe fetch request."""

    source: str = "bybit"
    symbol: str = "BTCUSDT"
    market_type: str = "linear"
    timeframe: str = "15m"
    start_time: str = "2021-01-01 00:00:00"
    end_time: str | None = None

    @property
    def condition_key(self) -> str:
        """Filesystem-safe key, e.g. 'BTCUSDT_15M'."""
        return f"{self.symbol}_{self.timeframe.upper()}"


@dataclass
class BacktestConfig:
    """Single-run configuration for the backtesting.py engine."""

    symbol: str = "BTCUSDT"
    market_type: str = "linear"
    timeframe: str = "15m"
    start_time: str = "2021-01-01 00:00:00"
    end_time: str | None = None

    initial_cash: float = 10_000.0
    # 0.08% taker fee — Bybit standard for mid-tier pairs
    commission: float = 0.0008
    plot: bool = False

    data_dir: Path = Path("crypto_data/data")
