from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pandas as pd
import pytest

from crypto_data.downloader import download_market_data, load_market_data
from crypto_data.storage import build_file_path, save_parquet


def _make_df() -> pd.DataFrame:
    idx = pd.date_range("2021-01-01", periods=3, freq="1h", tz="UTC")
    df = pd.DataFrame(
        {
            "Open": [100.0, 101.0, 102.0],
            "High": [105.0, 106.0, 107.0],
            "Low": [95.0, 96.0, 97.0],
            "Close": [102.0, 103.0, 104.0],
            "Volume": [1000.0, 1100.0, 1200.0],
        },
        index=idx,
    )
    df.index.name = "Date"
    return df


def test_download_creates_parquet(tmp_path: Path):
    df = _make_df()  # first candle 2021-01-01 00:00, last 2021-01-01 02:00
    with patch("crypto_data.downloader.fetch_ohlcv", return_value=df):
        download_market_data(
            symbols=["BTCUSDT"],
            timeframes=["1h"],
            start_time="2021-01-01 00:00:00",
            end_time="2021-01-02 00:00:00",
            output_dir=tmp_path,
        )
    files = list((tmp_path / "BTCUSDT").glob("*.parquet"))
    assert len(files) == 1
    # Filename reflects actual candle dates, not the requested range
    assert "BTCUSDT_1h_start_2021-01-01_end_2021-01-01" in files[0].name


def test_download_creates_quality_report(tmp_path: Path):
    with patch("crypto_data.downloader.fetch_ohlcv", return_value=_make_df()):
        download_market_data(
            symbols=["BTCUSDT"],
            timeframes=["1h"],
            start_time="2021-01-01 00:00:00",
            end_time="2021-01-02 00:00:00",
            output_dir=tmp_path,
        )
    report = tmp_path / "BTCUSDT" / "BTCUSDT_quality_report.md"
    assert report.exists()
    assert "BTCUSDT" in report.read_text()


def test_skip_existing_skips_fetch(tmp_path: Path):
    df = _make_df()
    # Pre-create a file with the glob-matching pattern; exact dates don't matter
    path = build_file_path(tmp_path, "BTCUSDT", "1h", "2021-01-01", "2021-01-01")
    save_parquet(df, path)

    call_count = 0

    def fake_fetch(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        return df

    with patch("crypto_data.downloader.fetch_ohlcv", side_effect=fake_fetch):
        download_market_data(
            symbols=["BTCUSDT"],
            timeframes=["1h"],
            start_time="2021-01-01 00:00:00",
            end_time="2021-01-02 00:00:00",
            output_dir=tmp_path,
            skip_existing=True,
        )

    assert call_count == 0


def test_skip_existing_false_refetches(tmp_path: Path):
    df = _make_df()
    path = build_file_path(tmp_path, "BTCUSDT", "1h", "2021-01-01", "2021-01-01")
    save_parquet(df, path)

    call_count = 0

    def fake_fetch(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        return df

    with patch("crypto_data.downloader.fetch_ohlcv", side_effect=fake_fetch):
        download_market_data(
            symbols=["BTCUSDT"],
            timeframes=["1h"],
            start_time="2021-01-01 00:00:00",
            end_time="2021-01-02 00:00:00",
            output_dir=tmp_path,
            skip_existing=False,
        )

    assert call_count == 1


def test_empty_df_not_saved(tmp_path: Path):
    empty = pd.DataFrame(columns=["Open", "High", "Low", "Close", "Volume"])
    with patch("crypto_data.downloader.fetch_ohlcv", return_value=empty):
        download_market_data(
            symbols=["BTCUSDT"],
            timeframes=["1h"],
            start_time="2021-01-01 00:00:00",
            end_time="2021-01-02 00:00:00",
            output_dir=tmp_path,
        )
    files = list(tmp_path.rglob("*.parquet"))
    assert len(files) == 0


def test_load_market_data(tmp_path: Path):
    df = _make_df()
    path = build_file_path(tmp_path, "ETHUSDT", "4h", "2021-01-01", "2021-01-31")
    save_parquet(df, path)
    loaded = load_market_data("ETHUSDT", "4h", output_dir=tmp_path)
    # Parquet does not preserve DatetimeIndex frequency metadata; compare values only
    pd.testing.assert_frame_equal(df, loaded, check_freq=False)


def test_load_market_data_returns_latest_when_multiple(tmp_path: Path):
    """When multiple date-range files exist, the latest end-date is returned."""
    df1 = _make_df()
    df2 = _make_df()
    df2["Close"] = 999.0  # sentinel to distinguish

    save_parquet(df1, build_file_path(tmp_path, "BTCUSDT", "1h", "2021-01-01", "2021-06-01"))
    save_parquet(df2, build_file_path(tmp_path, "BTCUSDT", "1h", "2021-01-01", "2021-12-31"))

    loaded = load_market_data("BTCUSDT", "1h", output_dir=tmp_path)
    assert (loaded["Close"] == 999.0).all()


def test_load_market_data_missing_symbol(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        load_market_data("UNKNOWN", "1h", output_dir=tmp_path)


def test_load_market_data_missing_tf(tmp_path: Path):
    df = _make_df()
    save_parquet(df, build_file_path(tmp_path, "BTCUSDT", "1d", "2021-01-01", "2021-12-31"))
    with pytest.raises(FileNotFoundError):
        load_market_data("BTCUSDT", "1h", output_dir=tmp_path)


def test_load_market_data_start_filter(tmp_path: Path):
    df = _make_df()  # 3 rows: 00:00, 01:00, 02:00 on 2021-01-01
    save_parquet(df, build_file_path(tmp_path, "BTCUSDT", "1h", "2021-01-01", "2021-01-31"))
    loaded = load_market_data("BTCUSDT", "1h", output_dir=tmp_path, start_filter="2021-01-01 01:00:00")
    assert len(loaded) == 2
    assert loaded.index[0] == pd.Timestamp("2021-01-01 01:00:00+00:00")


def test_load_market_data_end_filter(tmp_path: Path):
    df = _make_df()
    save_parquet(df, build_file_path(tmp_path, "BTCUSDT", "1h", "2021-01-01", "2021-01-31"))
    loaded = load_market_data("BTCUSDT", "1h", output_dir=tmp_path, end_filter="2021-01-01 01:00:00")
    assert len(loaded) == 2
    assert loaded.index[-1] == pd.Timestamp("2021-01-01 01:00:00+00:00")


def test_load_market_data_start_and_end_filter(tmp_path: Path):
    df = _make_df()
    save_parquet(df, build_file_path(tmp_path, "BTCUSDT", "1h", "2021-01-01", "2021-01-31"))
    loaded = load_market_data(
        "BTCUSDT", "1h", output_dir=tmp_path,
        start_filter="2021-01-01 01:00:00",
        end_filter="2021-01-01 01:00:00",
    )
    assert len(loaded) == 1
