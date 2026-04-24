from __future__ import annotations

from pathlib import Path
from typing import List

DEFAULT_SYMBOLS: List[str] = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT",
    "BNBUSDT",
    "XRPUSDT",
]

# Bybit-compatible timeframe strings used throughout the module
TIMEFRAMES: List[str] = ["1d", "4h", "1h", "15m", "5m", "1m"]

DEFAULT_MARKET_TYPE: str = "linear"

# Parquet files are stored here; the directory is gitignored
OUTPUT_DIR: Path = Path(__file__).parent / "data"
