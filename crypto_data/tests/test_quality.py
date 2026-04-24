from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from crypto_data.quality import check_quality, save_quality_report


def _make_df(n: int = 24, freq: str = "1h") -> pd.DataFrame:
    idx = pd.date_range("2021-01-01", periods=n, freq=freq, tz="UTC")
    df = pd.DataFrame(
        {
            "Open": [100.0] * n,
            "High": [105.0] * n,
            "Low": [95.0] * n,
            "Close": [102.0] * n,
            "Volume": [1000.0] * n,
        },
        index=idx,
    )
    df.index.name = "Date"
    return df


def test_clean_data_no_issues():
    df = _make_df()
    r = check_quality(df, "BTCUSDT", "1h")
    assert r["nan_count"] == 0
    assert r["duplicate_timestamps"] == 0
    assert r["ohlc_violations"] == 0
    assert r["completeness_pct"] > 0


def test_nan_detection():
    df = _make_df()
    df.iloc[2, df.columns.get_loc("Close")] = float("nan")
    r = check_quality(df, "BTCUSDT", "1h")
    assert r["nan_count"] == 1


def test_duplicate_timestamps():
    df = _make_df()
    df = pd.concat([df, df.iloc[[0]]])
    r = check_quality(df, "BTCUSDT", "1h")
    assert r["duplicate_timestamps"] >= 1


def test_ohlc_violation_high_below_low():
    df = _make_df()
    # Force High < Low on the first row
    df.iloc[0, df.columns.get_loc("High")] = 50.0
    r = check_quality(df, "BTCUSDT", "1h")
    assert r["ohlc_violations"] >= 1


def test_ohlc_violation_high_below_close():
    df = _make_df()
    df.iloc[0, df.columns.get_loc("High")] = df.iloc[0]["Close"] - 1
    r = check_quality(df, "BTCUSDT", "1h")
    assert r["ohlc_violations"] >= 1


def test_completeness_full():
    df = _make_df(n=25)  # 25 hourly rows = start + 24 hours
    r = check_quality(df, "BTCUSDT", "1h")
    assert r["completeness_pct"] >= 95.0


def test_save_quality_report_creates_md(tmp_path: Path):
    df = _make_df()
    r = check_quality(df, "BTCUSDT", "1h")
    save_quality_report(tmp_path / "BTCUSDT", "BTCUSDT", {"1h": r})

    report = (tmp_path / "BTCUSDT" / "BTCUSDT_quality_report.md")
    assert report.exists()
    content = report.read_text()
    assert "BTCUSDT" in content
    assert "1h" in content
    assert "Completeness" in content


def test_save_quality_report_overwrites(tmp_path: Path):
    """Second call should replace the report, not append."""
    df = _make_df()
    r = check_quality(df, "BTCUSDT", "1h")
    coin_dir = tmp_path / "BTCUSDT"
    save_quality_report(coin_dir, "BTCUSDT", {"1h": r})
    save_quality_report(coin_dir, "BTCUSDT", {"1h": r})
    content = (coin_dir / "BTCUSDT_quality_report.md").read_text()
    # The header line should appear exactly once
    assert content.count("# Quality Report") == 1
