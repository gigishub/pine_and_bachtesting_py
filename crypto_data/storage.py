from __future__ import annotations

from pathlib import Path

import pandas as pd


def build_file_path(
    output_dir: Path,
    symbol: str,
    tf: str,
    start_time: str,
    end_time: str,
) -> Path:
    """Return <output_dir>/<symbol>/<symbol>_<tf>_start_<date>_end_<date>.parquet.

    start_time / end_time may be full datetime strings or bare dates —
    only the YYYY-MM-DD portion is used in the filename.
    """
    start_date = start_time[:10]
    end_date = end_time[:10]
    filename = f"{symbol}_{tf}_start_{start_date}_end_{end_date}.parquet"
    return output_dir / symbol / filename


def save_parquet(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path)


def load_parquet(path: Path) -> pd.DataFrame:
    return pd.read_parquet(path)
