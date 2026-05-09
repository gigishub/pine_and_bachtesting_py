"""Batch downloader and loader for Bybit open interest history.

Mirrors funding_downloader.py but for open interest. Files are saved as:
    <output_dir>/<symbol>/<symbol>_oi_<interval>_start_<date>_end_<date>.parquet
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import List

import pandas as pd

from .config import DEFAULT_MARKET_TYPE, OUTPUT_DIR
from .fetch_bybit_open_interest import fetch_all_open_interest, normalize_oi_interval
from .storage import build_file_path, load_parquet, save_parquet

logger = logging.getLogger(__name__)


def _oi_tf_token(interval: str) -> str:
    """Return the filename token for a given OI interval, e.g. '1h' → 'oi_1h'."""
    return f"oi_{normalize_oi_interval(interval)}"


def download_open_interest(
    symbols: List[str],
    interval: str = "1h",
    start_time: str = "2021-01-01 00:00:00",
    end_time: str | None = None,
    category: str = DEFAULT_MARKET_TYPE,
    output_dir: Path = OUTPUT_DIR,
    skip_existing: bool = True,
) -> None:
    """Download open interest history for every symbol in *symbols*.

    Args:
        symbols:      List of Bybit symbols, e.g. ['BTCUSDT', 'ETHUSDT'].
        interval:     OI bar interval: '5min','15min','30min','1h','4h','1d'.
        start_time:   UTC datetime string 'YYYY-MM-DD HH:MM:SS'.
        end_time:     UTC datetime string or None (defaults to now).
        category:     Bybit category: 'linear' or 'inverse'.
        output_dir:   Root directory for saved Parquet files.
        skip_existing: If True, skip symbols that already have an OI parquet.
    """
    if end_time is None:
        end_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    tf_token = _oi_tf_token(interval)

    for symbol in symbols:
        coin_dir = output_dir / symbol

        if skip_existing and list(
            coin_dir.glob(f"{symbol}_{tf_token}_start_*_end_*.parquet")
        ):
            logger.info(
                "Skipping %s OI (%s) — file already exists in %s",
                symbol,
                interval,
                coin_dir,
            )
            continue

        logger.info(
            "Downloading %s OI [%s]  %s → %s", symbol, interval, start_time, end_time
        )
        try:
            df = fetch_all_open_interest(
                symbol, interval, category, start_time, end_time
            )
        except Exception as exc:
            logger.error("Failed to fetch %s OI: %s", symbol, exc)
            continue

        if df.empty:
            logger.warning("No OI data returned for %s", symbol)
            continue

        actual_start = df.index.min().strftime("%Y-%m-%d %H:%M:%S")
        actual_end = df.index.max().strftime("%Y-%m-%d %H:%M:%S")
        file_path = build_file_path(output_dir, symbol, tf_token, actual_start, actual_end)

        save_parquet(df, file_path)
        logger.info("Saved %d OI rows → %s", len(df), file_path)


def load_open_interest(
    symbol: str,
    interval: str = "1h",
    output_dir: Path = OUTPUT_DIR,
    start_filter: str | None = None,
    end_filter: str | None = None,
) -> pd.DataFrame:
    """Load open interest data for *symbol* from disk.

    If multiple date-range files exist for the same interval, the
    lexicographically latest one (most recent end date) is returned.

    Args:
        symbol:       Bybit symbol, e.g. 'BTCUSDT'.
        interval:     OI interval used when downloading, e.g. '1h'.
        output_dir:   Root directory where coin subdirectories live.
        start_filter: Optional UTC date string to clip the start of returned data.
        end_filter:   Optional UTC date string to clip the end of returned data.

    Returns:
        DataFrame with DatetimeIndex and an 'openInterest' float column.

    Raises:
        FileNotFoundError: If no matching file is found.
    """
    tf_token = _oi_tf_token(interval)
    coin_dir = output_dir / symbol

    if not coin_dir.exists():
        raise FileNotFoundError(
            f"No data directory found for {symbol}: {coin_dir}"
        )

    matches = sorted(coin_dir.glob(f"{symbol}_{tf_token}_start_*_end_*.parquet"))
    if not matches:
        raise FileNotFoundError(
            f"No OI parquet found for {symbol} [{interval}] in {coin_dir}"
        )

    path = matches[-1]
    logger.info("Loading %s", path)
    df = load_parquet(path)

    if start_filter is not None or end_filter is not None:
        df = df.loc[start_filter:end_filter]
        logger.info(
            "Applied time filter [%s : %s] — %d rows remain",
            start_filter,
            end_filter,
            len(df),
        )

    return df
