"""crypto_data — Bybit OHLCV downloader with date-range filenames.

Usage example::

    from crypto_data import download_market_data, load_market_data

    # Download all default symbols across all timeframes
    download_market_data(
        symbols=["BTCUSDT", "ETHUSDT"],
        start_time="2022-01-01 00:00:00",
        end_time="2024-01-01 00:00:00",
    )

    # Load a specific dataset for backtesting
    df = load_market_data("BTCUSDT", "1h")
"""

from .downloader import download_market_data, load_market_data
from .audit import audit_coin, audit_all, cross_timeframe_check

__all__ = [
    "download_market_data",
    "load_market_data",
    "audit_coin",
    "audit_all",
    "cross_timeframe_check",
]
