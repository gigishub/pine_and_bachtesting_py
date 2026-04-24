from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import List

import pandas as pd

from .config import DEFAULT_MARKET_TYPE, DEFAULT_SYMBOLS, OUTPUT_DIR, TIMEFRAMES
from .fetcher import fetch_ohlcv, normalize_timeframe
from .quality import check_quality, save_quality_report
from .storage import build_file_path, load_parquet, save_parquet

logger = logging.getLogger(__name__)


def download_market_data(
    symbols: List[str] = DEFAULT_SYMBOLS,
    timeframes: List[str] = TIMEFRAMES,
    start_time: str = "2021-01-01 00:00:00",
    end_time: str | None = None,
    market_type: str = DEFAULT_MARKET_TYPE,
    output_dir: Path = OUTPUT_DIR,
    skip_existing: bool = True,
) -> None:
    """Batch-download OHLCV data for every symbol × timeframe combination.

    For each coin, a Markdown quality report is saved to the coin's directory
    after all timeframes have been fetched.

    Args:
        symbols:       List of Bybit symbols, e.g. ['BTCUSDT', 'ETHUSDT'].
        timeframes:    List of timeframes, e.g. ['1d', '4h', '1h', '15m', '5m', '1m'].
        start_time:    UTC datetime string 'YYYY-MM-DD HH:MM:SS'.
        end_time:      UTC datetime string or None (defaults to now).
        market_type:   Bybit market type: 'linear', 'spot', or 'inverse'.
        output_dir:    Root directory for saved Parquet files.
        skip_existing: If True, skip any symbol+tf whose parquet file already exists.
    """
    if end_time is None:
        end_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    for symbol in symbols:
        tf_results: dict[str, dict] = {}

        for tf in timeframes:
            tf_norm = normalize_timeframe(tf)
            coin_dir = output_dir / symbol

            # skip_existing check: glob for any already-downloaded file for this
            # symbol+tf — we don't know the actual date range until after the fetch.
            if skip_existing and list(coin_dir.glob(f"{symbol}_{tf_norm}_start_*_end_*.parquet")):
                logger.info("Skipping %s %s — file already exists in %s", symbol, tf_norm, coin_dir)
                continue

            logger.info(
                "Downloading %s %s  %s → %s", symbol, tf_norm, start_time, end_time
            )
            try:
                df = fetch_ohlcv(symbol, tf_norm, start_time, end_time, market_type)
            except Exception as exc:
                logger.error("Failed to fetch %s %s: %s", symbol, tf_norm, exc)
                continue

            if df.empty:
                logger.warning("No data returned for %s %s", symbol, tf_norm)
                continue

            # Use the actual first/last candle dates — not the requested range —
            # so the filename accurately reflects what the file contains.
            actual_start = df.index.min().strftime("%Y-%m-%d %H:%M:%S")
            actual_end = df.index.max().strftime("%Y-%m-%d %H:%M:%S")
            file_path = build_file_path(output_dir, symbol, tf_norm, actual_start, actual_end)

            save_parquet(df, file_path)
            logger.info("Saved %d rows → %s", len(df), file_path)

            tf_results[tf_norm] = check_quality(df, symbol, tf_norm)

        if tf_results:
            save_quality_report(output_dir / symbol, symbol, tf_results)


def load_market_data(
    symbol: str,
    tf: str,
    output_dir: Path = OUTPUT_DIR,
    start_filter: str | None = None,
    end_filter: str | None = None,
) -> pd.DataFrame:
    """Load OHLCV data for a symbol + timeframe from disk.

    If multiple date-range files exist for the same symbol+tf, the
    lexicographically latest one (most recent end date) is returned.

    Args:
        symbol:       Bybit symbol, e.g. 'BTCUSDT'.
        tf:           Timeframe string, e.g. '1h' or '1hour'.
        output_dir:   Root directory where coin subdirectories live.
        start_filter: Optional UTC date/datetime string to clip the start of the
                      returned data, e.g. '2023-01-01' or '2023-01-01 00:00:00'.
        end_filter:   Optional UTC date/datetime string to clip the end of the
                      returned data.

    Returns:
        DataFrame with DatetimeIndex and OHLCV columns, optionally filtered.

    Raises:
        FileNotFoundError: If no matching file is found.
    """
    tf_norm = normalize_timeframe(tf)
    coin_dir = output_dir / symbol

    if not coin_dir.exists():
        raise FileNotFoundError(f"No data directory found for {symbol}: {coin_dir}")

    matches = sorted(coin_dir.glob(f"{symbol}_{tf_norm}_start_*_end_*.parquet"))
    if not matches:
        raise FileNotFoundError(
            f"No parquet file found for {symbol} {tf_norm} in {coin_dir}"
        )

    # Use the last entry — filenames sort chronologically by end date
    path = matches[-1]
    logger.info("Loading %s", path)
    df = load_parquet(path)

    if start_filter is not None or end_filter is not None:
        df = df.loc[start_filter:end_filter]
        logger.info(
            "Applied time filter [%s : %s] — %d rows remain",
            start_filter, end_filter, len(df),
        )

    return df
