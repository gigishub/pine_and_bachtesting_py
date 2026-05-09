"""
Data loader for hypothesis testing.

Guarantees:
  - Returned DataFrame is always sliced to [start_date, end_date] (fixes
    the silent "use all data" bug in the legacy loader).
  - DateRangeMismatchError is raised when existing CSVs in results_dir were
    produced with a different date window, preventing mixed-range comparisons.
"""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

log = logging.getLogger(__name__)


class DateRangeMismatchError(Exception):
    """Raised when an existing result CSV uses a different date range."""


def load_ohlcv(
    symbol: str,
    timeframe: str,
    start_date: str,
    end_date: str,
    data_dir: str = "crypto_data/data",
) -> pd.DataFrame:
    """
    Load OHLCV parquet for *symbol* / *timeframe* and slice to [start_date, end_date].

    Parameters
    ----------
    symbol:     Ticker, e.g. "BTCUSDT".
    timeframe:  Bar size, e.g. "15m", "4h", "1d".
    start_date: Inclusive start as ISO date string ("YYYY-MM-DD").
    end_date:   Inclusive end   as ISO date string ("YYYY-MM-DD").
    data_dir:   Root directory containing per-symbol subdirectories.

    Returns
    -------
    pd.DataFrame with DatetimeIndex, columns: open, high, low, close, volume.
    Raises FileNotFoundError if no matching parquet is found.
    """
    base = Path(data_dir) / symbol
    candidates = sorted(base.glob(f"{symbol}_{timeframe}_*.parquet"))
    if not candidates:
        raise FileNotFoundError(
            f"No parquet file found for {symbol}/{timeframe} in {base}"
        )

    # Prefer an exact date-range match in the filename; fall back to first.
    exact = [
        p for p in candidates
        if start_date.replace("-", "-") in p.name and end_date.replace("-", "-") in p.name
    ]
    path = exact[0] if exact else candidates[0]
    if not exact:
        log.debug("No exact-match parquet for %s/%s; using %s", symbol, timeframe, path.name)

    df = pd.read_parquet(path)
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    # Normalise column names to lowercase so downstream code always uses 'close' etc.
    df.columns = [c.lower() for c in df.columns]

    # Always slice — this is the critical fix over the legacy loader.
    df = df.loc[start_date:end_date]

    if df.empty:
        raise ValueError(
            f"No data for {symbol}/{timeframe} in [{start_date}, {end_date}]"
        )
    return df


def load_funding(
    symbol: str,
    start_date: str,
    end_date: str,
    data_dir: str = "crypto_data/data",
) -> pd.DataFrame:
    """
    Load the funding-rate parquet for *symbol* and slice to [start_date, end_date].

    Returns a single-column DataFrame with column ``fundingrate`` and a
    timezone-naive UTC DatetimeIndex (8-hour intervals: 00:00, 08:00, 16:00).

    Raises FileNotFoundError if no funding parquet is found for the symbol.
    """
    base = Path(data_dir) / symbol
    candidates = sorted(base.glob(f"{symbol}_funding_*.parquet"))
    if not candidates:
        raise FileNotFoundError(
            f"No funding parquet found for {symbol} in {base}"
        )
    path = candidates[0]
    df = pd.read_parquet(path)
    df.index = pd.to_datetime(df.index, utc=True).tz_localize(None)
    df = df.sort_index()
    df.columns = [c.lower() for c in df.columns]
    return df.loc[start_date:end_date]


def assert_date_range_consistent(
    results_dir: Path,
    start_date: str,
    end_date: str,
) -> None:
    """
    Scan every CSV in *results_dir* and assert every file's start_date / end_date
    columns match *start_date* / *end_date*.

    Raises DateRangeMismatchError on first mismatch.
    Should be called at the beginning of each batch run so stale results
    from a different date window are caught immediately.
    """
    for csv_path in results_dir.glob("*.csv"):
        try:
            df = pd.read_csv(csv_path, nrows=1)
        except Exception:
            continue

        if "start_date" not in df.columns or "end_date" not in df.columns:
            continue

        existing_start = str(df["start_date"].iloc[0])
        existing_end   = str(df["end_date"].iloc[0])

        if existing_start != start_date or existing_end != end_date:
            raise DateRangeMismatchError(
                f"{csv_path.name} was computed on [{existing_start}, {existing_end}] "
                f"but the current config uses [{start_date}, {end_date}]. "
                "Delete or archive the old results before running with a new date range."
            )
