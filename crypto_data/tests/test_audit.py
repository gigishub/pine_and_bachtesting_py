from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from crypto_data.audit import (
    CheckResult,
    TFMismatch,
    _compare_candles,
    _resample_1m_to,
    audit_coin,
    check_completeness,
    check_duplicates,
    check_ohlc_logic,
    check_price_integrity,
    check_price_spikes,
    check_return_profile,
    check_stale_prices,
    check_volume_spikes,
    check_zero_volume,
    compute_trust_score,
    cross_timeframe_check,
    run_audit,
    save_audit_report,
    save_cross_tf_report,
)


# ── Fixture helpers ───────────────────────────────────────────────────────────

def _make_df(n: int = 100, freq: str = "1h") -> pd.DataFrame:
    idx = pd.date_range("2021-01-01", periods=n, freq=freq, tz="UTC")
    base = 50_000.0
    prices = base + np.cumsum(np.random.default_rng(42).normal(0, 100, n))
    df = pd.DataFrame(
        {
            "Open": prices,
            "High": prices + 200,
            "Low": prices - 200,
            "Close": prices + 10,
            "Volume": np.random.default_rng(1).uniform(1000, 5000, n),
        },
        index=idx,
    )
    df.index.name = "Date"
    return df


# ── check_completeness ────────────────────────────────────────────────────────

def test_completeness_full():
    df = _make_df(n=24, freq="1h")
    r = check_completeness(df, "1h")
    assert r.status == "PASS"
    assert r.affected == 0


def test_completeness_missing_rows():
    df = _make_df(n=24, freq="1h")
    df = df.drop(df.index[5:8])  # remove 3 rows
    r = check_completeness(df, "1h")
    assert r.status in ("WARN", "FAIL")
    assert r.affected == 3


def test_completeness_gap_table_populated():
    df = _make_df(n=24, freq="1h")
    df = df.drop(df.index[10])
    r = check_completeness(df, "1h")
    assert not r.flagged.empty
    assert "gap_start" in r.flagged.columns


# ── check_duplicates ──────────────────────────────────────────────────────────

def test_duplicates_clean():
    df = _make_df()
    assert check_duplicates(df).status == "PASS"


def test_duplicates_detected():
    df = _make_df()
    df = pd.concat([df, df.iloc[[0]]])
    r = check_duplicates(df)
    assert r.status == "FAIL"
    assert r.affected >= 1


# ── check_price_integrity ─────────────────────────────────────────────────────

def test_price_integrity_clean():
    df = _make_df()
    assert check_price_integrity(df).status == "PASS"


def test_price_integrity_zero():
    df = _make_df()
    df.iloc[0, df.columns.get_loc("Low")] = 0
    r = check_price_integrity(df)
    assert r.status == "FAIL"
    assert r.affected == 1


def test_price_integrity_negative():
    df = _make_df()
    df.iloc[3, df.columns.get_loc("Open")] = -1.0
    r = check_price_integrity(df)
    assert r.status == "FAIL"


# ── check_ohlc_logic ──────────────────────────────────────────────────────────

def test_ohlc_logic_clean():
    df = _make_df()
    assert check_ohlc_logic(df).status == "PASS"


def test_ohlc_logic_high_below_low():
    df = _make_df()
    df.iloc[0, df.columns.get_loc("High")] = df.iloc[0]["Low"] - 1
    r = check_ohlc_logic(df)
    assert r.status == "FAIL"
    assert r.affected >= 1


def test_ohlc_logic_low_above_close():
    df = _make_df()
    df.iloc[2, df.columns.get_loc("Low")] = df.iloc[2]["Close"] + 1
    r = check_ohlc_logic(df)
    assert r.status == "FAIL"


# ── check_price_spikes ────────────────────────────────────────────────────────

def test_price_spikes_clean():
    df = _make_df()
    r = check_price_spikes(df, "1h")
    assert r.status == "PASS"


def test_price_spikes_detected():
    df = _make_df()
    # Insert a 10× price jump
    df.iloc[10, df.columns.get_loc("Close")] = df.iloc[9]["Close"] * 10
    r = check_price_spikes(df, "1h")
    assert r.status in ("WARN", "FAIL")
    assert r.affected >= 1
    assert "abs_log_return" in r.flagged.columns


def test_price_spikes_short_df():
    df = _make_df(n=1)
    r = check_price_spikes(df, "1h")
    assert r.status == "PASS"


# ── check_stale_prices ────────────────────────────────────────────────────────

def test_stale_prices_clean():
    df = _make_df()
    assert check_stale_prices(df).status == "PASS"


def test_stale_prices_detected():
    df = _make_df(n=20)
    # Force 6 consecutive identical closes
    df.iloc[5:11, df.columns.get_loc("Close")] = 99999.0
    r = check_stale_prices(df)
    assert r.status == "FAIL"
    assert r.affected >= 6


# ── check_zero_volume ─────────────────────────────────────────────────────────

def test_zero_volume_clean():
    df = _make_df()
    assert check_zero_volume(df).status == "PASS"


def test_zero_volume_warn():
    df = _make_df(n=100)
    df.iloc[0, df.columns.get_loc("Volume")] = 0
    r = check_zero_volume(df)
    # 1 out of 100 = 1% → exactly at the boundary
    assert r.status in ("WARN", "FAIL")


def test_zero_volume_fail():
    df = _make_df(n=100)
    df.iloc[:5, df.columns.get_loc("Volume")] = 0  # 5% zero volume
    r = check_zero_volume(df)
    assert r.status == "FAIL"


# ── check_volume_spikes ───────────────────────────────────────────────────────

def test_volume_spikes_clean():
    df = _make_df()
    assert check_volume_spikes(df).status == "PASS"


def test_volume_spikes_detected():
    df = _make_df(n=100)
    df.iloc[50, df.columns.get_loc("Volume")] = 1_000_000_000  # extreme outlier
    r = check_volume_spikes(df)
    assert r.status == "WARN"
    assert r.affected >= 1
    assert "volume_ratio" in r.flagged.columns


def test_volume_spikes_insufficient_data():
    df = _make_df(n=5)
    r = check_volume_spikes(df)
    assert r.status == "PASS"


# ── check_return_profile ──────────────────────────────────────────────────────

def test_return_profile_normal():
    df = _make_df(n=200)
    r = check_return_profile(df)
    assert r.status in ("PASS", "WARN")
    assert "mean=" in r.detail


# ── run_audit ─────────────────────────────────────────────────────────────────

def test_run_audit_returns_all_checks():
    df = _make_df()
    results = run_audit(df, "BTCUSDT", "1h")
    names = [r.name for r in results]
    assert any("Completeness" in n for n in names)
    assert any("OHLC" in n for n in names)
    assert any("spike" in n.lower() for n in names)
    assert any("volume" in n.lower() for n in names)


# ── compute_trust_score ───────────────────────────────────────────────────────

def test_trust_score_perfect_data():
    df = _make_df(n=200)
    results = run_audit(df, "BTCUSDT", "1h")
    score = compute_trust_score(results)
    assert score >= 85.0  # clean synthetic data should score high


def test_trust_score_decreases_with_violations():
    df_clean = _make_df(n=100)
    df_bad = df_clean.copy()
    df_bad.iloc[:10, df_bad.columns.get_loc("High")] = df_bad.iloc[:10]["Low"] - 1

    clean_score = compute_trust_score(run_audit(df_clean, "BTCUSDT", "1h"))
    bad_score = compute_trust_score(run_audit(df_bad, "BTCUSDT", "1h"))
    assert bad_score < clean_score


def test_trust_score_range():
    df = _make_df()
    score = compute_trust_score(run_audit(df, "BTCUSDT", "1h"))
    assert 0.0 <= score <= 100.0


# ── save_audit_report ─────────────────────────────────────────────────────────

def test_save_audit_report_creates_file(tmp_path: Path):
    df = _make_df()
    results = run_audit(df, "BTCUSDT", "1h")
    score = compute_trust_score(results)
    path = save_audit_report(tmp_path / "BTCUSDT", "BTCUSDT", "1h", results, score)
    assert path.exists()
    assert path.name == "BTCUSDT_1h_audit_report.md"


def test_save_audit_report_content(tmp_path: Path):
    df = _make_df()
    results = run_audit(df, "BTCUSDT", "1h")
    score = compute_trust_score(results)
    path = save_audit_report(tmp_path / "BTCUSDT", "BTCUSDT", "1h", results, score)
    content = path.read_text()
    assert "Trust Score" in content
    assert "OHLC" in content
    assert "Completeness" in content


def test_save_audit_report_overwrites(tmp_path: Path):
    df = _make_df()
    results = run_audit(df, "BTCUSDT", "1h")
    score = compute_trust_score(results)
    coin_dir = tmp_path / "BTCUSDT"
    save_audit_report(coin_dir, "BTCUSDT", "1h", results, score)
    save_audit_report(coin_dir, "BTCUSDT", "1h", results, score)
    content = (coin_dir / "BTCUSDT_1h_audit_report.md").read_text()
    assert content.count("# Audit Report") == 1


# ── audit_coin ────────────────────────────────────────────────────────────────

def test_audit_coin(tmp_path: Path):
    from crypto_data.storage import build_file_path, save_parquet
    df = _make_df(n=200)
    path = build_file_path(tmp_path, "BTCUSDT", "1h", "2021-01-01", "2021-12-31")
    save_parquet(df, path)
    score = audit_coin("BTCUSDT", "1h", output_dir=tmp_path)
    assert 0.0 <= score <= 100.0
    assert (tmp_path / "BTCUSDT" / "BTCUSDT_1h_audit_report.md").exists()


def test_audit_coin_missing_data(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        audit_coin("UNKNOWN", "1h", output_dir=tmp_path)


# ── _resample_1m_to ───────────────────────────────────────────────────────────

def _make_1m(n: int = 300) -> pd.DataFrame:
    """Clean 1m OHLCV DataFrame starting at a round UTC hour."""
    idx = pd.date_range("2021-01-01 00:00", periods=n, freq="1min", tz="UTC")
    rng = np.random.default_rng(7)
    prices = 50_000.0 + np.cumsum(rng.normal(0, 10, n))
    return pd.DataFrame(
        {
            "Open": prices,
            "High": prices + 20,
            "Low": prices - 20,
            "Close": prices + 1,
            "Volume": rng.uniform(10, 100, n),
        },
        index=idx,
    )


def test_resample_1m_to_5m():
    df_1m = _make_1m(n=60)
    df_5m = _resample_1m_to(df_1m, "5m")
    # 60 1m candles → 12 5m candles
    assert len(df_5m) == 12
    # First candle Open should equal first 1m Open
    assert df_5m["Open"].iloc[0] == pytest.approx(df_1m["Open"].iloc[0])
    # High of first 5m candle == max High of first 5 1m candles
    assert df_5m["High"].iloc[0] == pytest.approx(df_1m["High"].iloc[:5].max())
    # Volume of first 5m candle == sum of first 5 1m volumes
    assert df_5m["Volume"].iloc[0] == pytest.approx(df_1m["Volume"].iloc[:5].sum())


def test_resample_1m_to_1h():
    df_1m = _make_1m(n=120)
    df_1h = _resample_1m_to(df_1m, "1h")
    # 120 1m candles → 2 1h candles
    assert len(df_1h) == 2
    assert df_1h["Close"].iloc[0] == pytest.approx(df_1m["Close"].iloc[59])


def test_resample_1m_to_4h():
    df_1m = _make_1m(n=240)
    df_4h = _resample_1m_to(df_1m, "4h")
    assert len(df_4h) == 1
    assert df_4h["Low"].iloc[0] == pytest.approx(df_1m["Low"].min())


def test_resample_1m_unknown_tf_raises():
    df_1m = _make_1m(n=10)
    with pytest.raises(ValueError, match="No resample rule"):
        _resample_1m_to(df_1m, "99x")


# ── _compare_candles ──────────────────────────────────────────────────────────

def test_compare_candles_clean():
    df_1m = _make_1m(n=300)
    df_5m = _resample_1m_to(df_1m, "5m")
    result = _compare_candles(df_5m, df_5m.copy(), "5m", ohlc_rtol=1e-6, vol_rtol=1e-4)
    assert result.status == "PASS"
    assert result.mismatches == 0


def test_compare_candles_corrupted_high():
    df_1m = _make_1m(n=300)
    df_5m = _resample_1m_to(df_1m, "5m")
    df_corrupted = df_5m.copy()
    # Inflate High on 3 candles well beyond any tolerance
    df_corrupted.iloc[0, df_corrupted.columns.get_loc("High")] += 5_000
    df_corrupted.iloc[5, df_corrupted.columns.get_loc("High")] += 5_000
    df_corrupted.iloc[10, df_corrupted.columns.get_loc("High")] += 5_000
    result = _compare_candles(df_5m, df_corrupted, "5m", ohlc_rtol=1e-6, vol_rtol=1e-4)
    assert result.status == "FAIL"
    assert result.by_column["High"] == 3
    assert not result.flagged.empty
    assert "rel_diff_pct" in result.flagged.columns


def test_compare_candles_no_overlap():
    idx_a = pd.date_range("2021-01-01", periods=12, freq="5min", tz="UTC")
    idx_b = pd.date_range("2022-01-01", periods=12, freq="5min", tz="UTC")
    cols = ["Open", "High", "Low", "Close", "Volume"]
    rng = np.random.default_rng(0)
    df_a = pd.DataFrame(rng.uniform(100, 200, (12, 5)), index=idx_a, columns=cols)
    df_b = pd.DataFrame(rng.uniform(100, 200, (12, 5)), index=idx_b, columns=cols)
    result = _compare_candles(df_a, df_b, "5m", ohlc_rtol=1e-6, vol_rtol=1e-4)
    assert result.common_candles == 0
    assert result.mismatches == 0


def test_compare_candles_volume_tolerance():
    df_1m = _make_1m(n=300)
    df_5m = _resample_1m_to(df_1m, "5m")
    df_nearly = df_5m.copy()
    # Nudge Volume by 0.001% (< 0.01% vol_rtol=1e-4 tolerance) → should still PASS
    df_nearly["Volume"] *= 1.000001
    result = _compare_candles(df_5m, df_nearly, "5m", ohlc_rtol=1e-6, vol_rtol=1e-4)
    assert result.by_column["Volume"] == 0


# ── cross_timeframe_check integration ────────────────────────────────────────

def _write_parquet(df: pd.DataFrame, coin_dir: Path, symbol: str, tf: str) -> Path:
    from crypto_data.storage import save_parquet
    start = df.index.min().strftime("%Y-%m-%d")
    end = df.index.max().strftime("%Y-%m-%d")
    p = coin_dir / f"{symbol}_{tf}_start_{start}_end_{end}.parquet"
    save_parquet(df, p)
    return p


def test_cross_tf_check_all_pass(tmp_path: Path):
    symbol = "TESTUSDT"
    coin_dir = tmp_path / symbol
    coin_dir.mkdir()

    df_1m = _make_1m(n=300)
    _write_parquet(df_1m, coin_dir, symbol, "1m")

    # Derive 5m and 15m directly from the same 1m data (ground truth)
    df_5m = _resample_1m_to(df_1m, "5m")
    _write_parquet(df_5m, coin_dir, symbol, "5m")

    df_15m = _resample_1m_to(df_1m, "15m")
    _write_parquet(df_15m, coin_dir, symbol, "15m")

    results = cross_timeframe_check(symbol, output_dir=tmp_path)

    tfs_checked = {r.tf for r in results}
    assert "5m" in tfs_checked
    assert "15m" in tfs_checked

    for r in results:
        assert r.status == "PASS", f"Expected PASS for {r.tf}, got {r.status} ({r.mismatches} mismatches)"

    # Report written
    assert (coin_dir / f"{symbol}_cross_tf_audit_report.md").exists()


def test_cross_tf_check_detects_corrupted_candle(tmp_path: Path):
    symbol = "TESTUSDT"
    coin_dir = tmp_path / symbol
    coin_dir.mkdir()

    df_1m = _make_1m(n=300)
    _write_parquet(df_1m, coin_dir, symbol, "1m")

    # Create 5m file with one deliberately wrong High value
    df_5m = _resample_1m_to(df_1m, "5m")
    df_bad = df_5m.copy()
    df_bad.iloc[3, df_bad.columns.get_loc("High")] += 10_000  # impossible spike
    _write_parquet(df_bad, coin_dir, symbol, "5m")

    results = cross_timeframe_check(symbol, output_dir=tmp_path)
    r5m = next(r for r in results if r.tf == "5m")
    assert r5m.status == "FAIL"
    assert r5m.by_column["High"] >= 1


def test_cross_tf_check_no_1m_raises(tmp_path: Path):
    symbol = "GHOSTUSDT"
    (tmp_path / symbol).mkdir()
    with pytest.raises(FileNotFoundError, match="No 1m data"):
        cross_timeframe_check(symbol, output_dir=tmp_path)


def test_cross_tf_check_no_higher_tf_files(tmp_path: Path):
    """If only 1m data exists, the check runs but returns an empty list."""
    symbol = "ALONECOIN"
    coin_dir = tmp_path / symbol
    coin_dir.mkdir()

    df_1m = _make_1m(n=120)
    _write_parquet(df_1m, coin_dir, symbol, "1m")

    results = cross_timeframe_check(symbol, output_dir=tmp_path)
    assert results == []


def test_save_cross_tf_report_pass(tmp_path: Path):
    symbol = "BTCUSDT"
    coin_dir = tmp_path / symbol
    coin_dir.mkdir()

    df_1m = _make_1m(n=120)
    result = TFMismatch("5m", 24, 0, {c: 0 for c in ["Open", "High", "Low", "Close", "Volume"]})
    path = save_cross_tf_report(coin_dir, symbol, [result], df_1m)

    assert path.exists()
    content = path.read_text()
    assert "ALL PASS" in content
    assert "No mismatches found" in content


def test_save_cross_tf_report_fail(tmp_path: Path):
    symbol = "BTCUSDT"
    coin_dir = tmp_path / symbol
    coin_dir.mkdir()

    df_1m = _make_1m(n=120)
    flagged = pd.DataFrame(
        [{"timestamp": pd.Timestamp("2021-01-01", tz="UTC"), "column": "High", "from_1m": 100.0, "actual": 200.0, "rel_diff_pct": 100.0}]
    )
    result = TFMismatch("5m", 24, 1, {"Open": 0, "High": 1, "Low": 0, "Close": 0, "Volume": 0}, flagged)
    path = save_cross_tf_report(coin_dir, symbol, [result], df_1m)

    content = path.read_text()
    assert "ISSUES FOUND" in content
    assert "FAIL" in content

