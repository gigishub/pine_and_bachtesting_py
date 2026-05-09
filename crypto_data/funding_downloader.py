"""Batch downloader and loader for Bybit funding rate history.

Mirrors downloader.py but for funding rates. Files are saved as:
    <output_dir>/<symbol>/<symbol>_funding_start_<date>_end_<date>.parquet
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import List

import pandas as pd

from .config import DEFAULT_MARKET_TYPE, OUTPUT_DIR
from .fetch_bybit_funding_rates import fetch_all_funding_rates
from .storage import build_file_path, load_parquet, save_parquet

logger = logging.getLogger(__name__)

_FUNDING_TF = "funding"  # used as the "timeframe" token in the filename


def download_funding_rates(
    symbols: List[str],
    start_time: str = "2021-01-01 00:00:00",
    end_time: str | None = None,
    category: str = DEFAULT_MARKET_TYPE,
    output_dir: Path = OUTPUT_DIR,
    skip_existing: bool = True,
) -> None:
    """Download funding rate history for every symbol in *symbols*.

    Args:
        symbols:      List of Bybit symbols, e.g. ['BTCUSDT', 'ETHUSDT'].
        start_time:   UTC datetime string 'YYYY-MM-DD HH:MM:SS'.
        end_time:     UTC datetime string or None (defaults to now).
        category:     Bybit category: 'linear' or 'inverse'.
        output_dir:   Root directory for saved Parquet files.
        skip_existing: If True, skip symbols that already have a funding parquet.
    """
    if end_time is None:
        end_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    for symbol in symbols:
        coin_dir = output_dir / symbol

        if skip_existing and list(
            coin_dir.glob(f"{symbol}_{_FUNDING_TF}_start_*_end_*.parquet")
        ):
            logger.info(
                "Skipping %s funding — file already exists in %s", symbol, coin_dir
            )
            continue

        logger.info("Downloading %s funding  %s → %s", symbol, start_time, end_time)
        try:
            df = fetch_all_funding_rates(symbol, category, start_time, end_time)
        except Exception as exc:
            logger.error("Failed to fetch %s funding: %s", symbol, exc)
            continue

        if df.empty:
            logger.warning("No funding data returned for %s", symbol)
            continue

        actual_start = df.index.min().strftime("%Y-%m-%d %H:%M:%S")
        actual_end = df.index.max().strftime("%Y-%m-%d %H:%M:%S")
        file_path = build_file_path(output_dir, symbol, _FUNDING_TF, actual_start, actual_end)

        save_parquet(df, file_path)
        logger.info("Saved %d funding rows → %s", len(df), file_path)


def load_funding_rates(
    symbol: str,
    output_dir: Path = OUTPUT_DIR,
    start_filter: str | None = None,
    end_filter: str | None = None,
) -> pd.DataFrame:
    """Load funding rate data for *symbol* from disk.

    If multiple date-range files exist, the lexicographically latest one
    (most recent end date) is returned.

    Args:
        symbol:       Bybit symbol, e.g. 'BTCUSDT'.
        output_dir:   Root directory where coin subdirectories live.
        start_filter: Optional UTC date string to clip the start of returned data.
        end_filter:   Optional UTC date string to clip the end of returned data.

    Returns:
        DataFrame with DatetimeIndex and a 'fundingRate' column.

    Raises:
        FileNotFoundError: If no matching file is found.
    """
    coin_dir = output_dir / symbol

    if not coin_dir.exists():
        raise FileNotFoundError(
            f"No data directory found for {symbol}: {coin_dir}"
        )

    matches = sorted(
        coin_dir.glob(f"{symbol}_{_FUNDING_TF}_start_*_end_*.parquet")
    )
    if not matches:
        raise FileNotFoundError(
            f"No funding parquet found for {symbol} in {coin_dir}"
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
