from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from crypto_data.storage import build_file_path, load_parquet, save_parquet


def _make_df() -> pd.DataFrame:
    idx = pd.to_datetime(["2021-01-01 00:00:00+00:00"])
    df = pd.DataFrame(
        {"Open": [1.0], "High": [2.0], "Low": [0.5], "Close": [1.5], "Volume": [100.0]},
        index=idx,
    )
    df.index.name = "Date"
    return df


def test_build_file_path_full_datetime():
    path = build_file_path(
        Path("/data"), "BTCUSDT", "1h",
        "2021-01-01 00:00:00", "2024-01-01 00:00:00",
    )
    assert path == Path("/data/BTCUSDT/BTCUSDT_1h_start_2021-01-01_end_2024-01-01.parquet")


def test_build_file_path_bare_date():
    path = build_file_path(Path("/data"), "ETHUSDT", "4h", "2022-06-15", "2023-12-31")
    assert path.name == "ETHUSDT_4h_start_2022-06-15_end_2023-12-31.parquet"
    assert path.parent.name == "ETHUSDT"


def test_build_file_path_coin_subdir():
    path = build_file_path(Path("/out"), "SOLUSDT", "1d", "2023-01-01", "2023-12-31")
    assert path.parent == Path("/out/SOLUSDT")


def test_save_creates_parent_dirs(tmp_path: Path):
    df = _make_df()
    path = build_file_path(tmp_path, "BTCUSDT", "1d", "2021-01-01", "2021-01-01")
    save_parquet(df, path)
    assert path.exists()


def test_save_load_roundtrip(tmp_path: Path):
    df = _make_df()
    path = build_file_path(tmp_path, "BTCUSDT", "1d", "2021-01-01", "2021-01-01")
    save_parquet(df, path)
    loaded = load_parquet(path)
    pd.testing.assert_frame_equal(df, loaded)
