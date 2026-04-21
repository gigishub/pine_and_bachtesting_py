"""Tests for strategy_evaluation.phase2 (trade-log-slicing approach)."""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from strategy_evaluation.config import RobustnessConfig
from strategy_evaluation.phase2 import (
    compute_trade_metrics,
    cross_tf_consensus,
    evaluate_window,
    filter_trades_by_timeframe,
    get_trade_timeframes,
    load_trade_logs,
    passes_trade_thresholds,
    short_sig,
    slice_trades,
    verdict_table,
)

# ── Fixtures ──────────────────────────────────────────────────────────────────


def _make_cfg(**kw) -> RobustnessConfig:
    defaults = dict(
        min_sqn=1.0,
        min_profit_factor=1.2,
        min_win_rate=30.0,
        min_combo_pass_rate=0.0,
    )
    defaults.update(kw)
    return RobustnessConfig(**defaults)


def _make_trades(
    n_trades: int = 20,
    sig: str = "SIG_A",
    symbol: str = "BTCUSDT",
    start: str = "2023-01-01",
    win_pct: float = 0.6,
    avg_win: float = 2.0,
    avg_loss: float = -1.0,
) -> pd.DataFrame:
    """Build a synthetic trade log DataFrame."""
    n_wins   = int(n_trades * win_pct)
    n_losses = n_trades - n_wins
    returns  = [avg_win] * n_wins + [avg_loss] * n_losses

    times = pd.date_range(start, periods=n_trades, freq="6h", tz="UTC")
    return pd.DataFrame({
        "Parameter Signature": sig,
        "Symbol":              symbol,
        "EntryTime":           times,
        "ExitTime":            times + pd.Timedelta("4h"),
        "Return [%]":          returns,
    })


# ── compute_trade_metrics ─────────────────────────────────────────────────────


def test_metrics_basic():
    df = _make_trades(n_trades=20, win_pct=0.6, avg_win=2.0, avg_loss=-1.0)
    m = compute_trade_metrics(df)
    assert m["# Trades"] == 20
    assert m["Win Rate [%]"] == pytest.approx(60.0, abs=0.1)
    assert m["Profit Factor"] > 1.0
    assert not math.isnan(m["SQN"])


def test_metrics_empty():
    m = compute_trade_metrics(pd.DataFrame())
    assert m["# Trades"] == 0
    assert math.isnan(m["SQN"])
    assert math.isnan(m["Win Rate [%]"])


def test_metrics_single_trade():
    df = _make_trades(n_trades=1, win_pct=1.0)
    m = compute_trade_metrics(df)
    assert m["# Trades"] == 1
    assert math.isnan(m["SQN"])  # SQN undefined for N<2


def test_metrics_all_losses():
    df = _make_trades(n_trades=10, win_pct=0.0, avg_loss=-1.5)
    m = compute_trade_metrics(df)
    assert m["Win Rate [%]"] == pytest.approx(0.0)
    assert math.isnan(m["Profit Factor"]) or m["Profit Factor"] == pytest.approx(0.0, abs=0.01)


def test_metrics_profit_factor_cap():
    """PF should be capped at 99.9 when there are no losses."""
    df = _make_trades(n_trades=10, win_pct=1.0, avg_win=2.0)
    m = compute_trade_metrics(df)
    assert m["Profit Factor"] == pytest.approx(99.9)


# ── passes_trade_thresholds ───────────────────────────────────────────────────


def test_passes_threshold_ok():
    df  = _make_trades(n_trades=20, win_pct=0.6, avg_win=2.0, avg_loss=-1.0)
    m   = compute_trade_metrics(df)
    cfg = _make_cfg(min_sqn=0.5, min_profit_factor=1.0, min_win_rate=30.0)
    assert passes_trade_thresholds(m, cfg, min_trades=5) == True


def test_passes_threshold_too_few_trades():
    df  = _make_trades(n_trades=3, win_pct=0.6, avg_win=2.0, avg_loss=-1.0)
    m   = compute_trade_metrics(df)
    cfg = _make_cfg()
    assert passes_trade_thresholds(m, cfg, min_trades=5) == False


def test_passes_threshold_low_sqn():
    m   = {"# Trades": 20, "SQN": 0.3, "Profit Factor": 2.0, "Win Rate [%]": 60.0}
    cfg = _make_cfg(min_sqn=1.0)
    assert passes_trade_thresholds(m, cfg, min_trades=5) == False


def test_passes_threshold_nan_sqn():
    m   = {"# Trades": 20, "SQN": float("nan"), "Profit Factor": 2.0, "Win Rate [%]": 60.0}
    cfg = _make_cfg()
    assert passes_trade_thresholds(m, cfg, min_trades=5) == False


# ── slice_trades ──────────────────────────────────────────────────────────────


def test_slice_middle():
    trades = _make_trades(n_trades=30, start="2022-01-01")  # 6h steps → ~7 days
    sliced = slice_trades(trades, "2022-01-02", "2022-01-04")
    assert not sliced.empty
    assert (sliced["EntryTime"] >= pd.Timestamp("2022-01-02", tz="UTC")).all()
    assert (sliced["EntryTime"] < pd.Timestamp("2022-01-04",  tz="UTC")).all()


def test_slice_no_bound():
    trades = _make_trades(n_trades=10)
    assert len(slice_trades(trades, None, None)) == 10


def test_slice_empty_returns_empty():
    assert slice_trades(pd.DataFrame(), "2023-01-01", "2024-01-01").empty


def test_slice_out_of_range():
    trades = _make_trades(n_trades=5, start="2022-01-01")
    sliced = slice_trades(trades, "2025-01-01", "2026-01-01")
    assert sliced.empty


# ── evaluate_window ───────────────────────────────────────────────────────────


def _multi_sig_df() -> pd.DataFrame:
    """Two signatures, two coins, each with 20 trades in 2023."""
    parts = [
        _make_trades(20, "SIG_A", "BTCUSDT", "2023-01-01", 0.65, 2.0, -1.0),
        _make_trades(20, "SIG_A", "ETHUSDT", "2023-01-01", 0.60, 2.0, -1.2),
        _make_trades(20, "SIG_B", "BTCUSDT", "2023-01-01", 0.40, 1.0, -2.0),
        _make_trades(20, "SIG_B", "ETHUSDT", "2023-01-01", 0.40, 1.0, -2.0),
    ]
    return pd.concat(parts, ignore_index=True)


def test_evaluate_window_sig_a_passes():
    trades = _multi_sig_df()
    cfg = _make_cfg(min_sqn=0.5, min_profit_factor=1.0, min_win_rate=30.0)
    result = evaluate_window(trades, ["SIG_A", "SIG_B"], "2023-01-01", "2024-01-01", cfg, min_trades_per_coin=5)
    row_a = result[result["Parameter Signature"] == "SIG_A"].iloc[0]
    assert row_a["coins_passing"] == 2
    assert row_a["sig_present"] == True


def test_evaluate_window_sig_b_fails():
    trades = _multi_sig_df()
    cfg = _make_cfg(min_sqn=1.5, min_profit_factor=1.5, min_win_rate=50.0)
    result = evaluate_window(trades, ["SIG_B"], "2023-01-01", "2024-01-01", cfg, min_trades_per_coin=5)
    row_b = result.iloc[0]
    assert row_b["coins_passing"] == 0


def test_evaluate_window_sig_not_present():
    trades = _multi_sig_df()
    cfg = _make_cfg()
    result = evaluate_window(trades, ["SIG_MISSING"], "2023-01-01", "2024-01-01", cfg)
    assert result.iloc[0]["sig_present"] == False
    assert result.iloc[0]["coins_passing"] == 0


def test_evaluate_window_out_of_range():
    """Window outside trade date range → 0 coins pass, but sig is present."""
    trades = _multi_sig_df()
    cfg = _make_cfg(min_sqn=0.5, min_profit_factor=1.0, min_win_rate=30.0)
    result = evaluate_window(trades, ["SIG_A"], "2025-01-01", "2026-01-01", cfg)
    assert result.iloc[0]["coins_passing"] == 0
    assert result.iloc[0]["sig_present"] == True  # sig exists in full log


def test_evaluate_window_min_trades_filter():
    """If min_trades_per_coin is higher than total, nothing passes."""
    trades = _multi_sig_df()
    cfg = _make_cfg(min_sqn=0.5, min_profit_factor=1.0, min_win_rate=30.0)
    result = evaluate_window(trades, ["SIG_A"], "2023-01-01", "2024-01-01", cfg, min_trades_per_coin=999)
    assert result.iloc[0]["coins_passing"] == 0


def test_evaluate_window_empty_trades():
    cfg = _make_cfg()
    result = evaluate_window(pd.DataFrame(), ["SIG_A"], "2023-01-01", "2024-01-01", cfg)
    assert result.iloc[0]["sig_present"] == False


# ── verdict_table ─────────────────────────────────────────────────────────────


def _eval_dfs() -> dict[str, pd.DataFrame]:
    trades = _multi_sig_df()
    cfg = _make_cfg(min_sqn=0.5, min_profit_factor=1.0, min_win_rate=30.0)
    return {
        "Bear":     evaluate_window(trades, ["SIG_A", "SIG_B"], "2023-01-01", "2023-06-01", cfg),
        "Recovery": evaluate_window(trades, ["SIG_A", "SIG_B"], "2023-01-01", "2024-01-01", cfg),
        "Bull":     evaluate_window(trades, ["SIG_A", "SIG_B"], "2025-01-01", "2026-01-01", cfg),
    }


def test_verdict_table_shape():
    vt = verdict_table(_eval_dfs(), min_coins_pass=1, min_windows_pass=2)
    assert set(["Parameter Signature", "verdict", "windows_passing"]).issubset(vt.columns)
    assert len(vt) == 2


def test_verdict_table_sig_a_passes():
    vt = verdict_table(_eval_dfs(), min_coins_pass=1, min_windows_pass=2)
    row = vt[vt["Parameter Signature"] == "SIG_A"].iloc[0]
    assert "PASS" in row["verdict"]


def test_verdict_table_sorted_desc():
    vt = verdict_table(_eval_dfs(), min_coins_pass=1, min_windows_pass=2)
    assert vt["windows_passing"].iloc[0] >= vt["windows_passing"].iloc[-1]


def test_verdict_table_empty():
    assert verdict_table({}, 1, 2).empty


def test_verdict_table_all_fail():
    trades = _multi_sig_df()
    cfg = _make_cfg(min_sqn=99.0)  # impossibly high
    evals = {
        "Bear": evaluate_window(trades, ["SIG_A"], "2023-01-01", "2024-01-01", cfg),
    }
    vt = verdict_table(evals, min_coins_pass=10, min_windows_pass=1)
    assert "FAIL" in vt.iloc[0]["verdict"]


# ── load_trade_logs ───────────────────────────────────────────────────────────


def test_load_trade_logs_missing_dir(tmp_path):
    result = load_trade_logs(tmp_path / "nonexistent")
    assert result.empty


def test_load_trade_logs_empty_trades_dir(tmp_path):
    (tmp_path / "trades").mkdir()
    result = load_trade_logs(tmp_path)
    assert result.empty


def test_load_trade_logs_valid_file(tmp_path):
    trades_dir = tmp_path / "trades"
    trades_dir.mkdir()
    df = _make_trades(10)
    df.to_csv(trades_dir / "BTC_1H_trade_log.csv", index=False)
    result = load_trade_logs(tmp_path)
    assert len(result) == 10
    assert pd.api.types.is_datetime64_any_dtype(result["EntryTime"])


def test_load_trade_logs_multiple_files(tmp_path):
    trades_dir = tmp_path / "trades"
    trades_dir.mkdir()
    for sym in ["BTC_1H", "ETH_4H"]:
        _make_trades(5, symbol=sym).to_csv(trades_dir / f"{sym}_trade_log.csv", index=False)
    result = load_trade_logs(tmp_path)
    assert len(result) == 10


# ── short_sig ─────────────────────────────────────────────────────────────────


def test_short_sig_short():
    assert short_sig("abc", 50) == "abc"


def test_short_sig_truncated():
    sig = "x" * 60
    assert short_sig(sig, 50).endswith("…")
    assert len(short_sig(sig, 50)) == 51  # 50 chars + ellipsis


def test_short_sig_exact_length():
    sig = "x" * 50
    assert short_sig(sig, 50) == sig


# ── get_trade_timeframes ──────────────────────────────────────────────────────


def _make_trades_with_condition(
    n: int = 10,
    sig: str = "SIG_A",
    symbol: str = "BTCUSDT",
    condition: str = "BTCUSDT_1H",
    start: str = "2023-01-01",
) -> pd.DataFrame:
    times = pd.date_range(start, periods=n, freq="6h", tz="UTC")
    returns = [1.0] * (n // 2) + [-0.5] * (n - n // 2)
    return pd.DataFrame({
        "Parameter Signature": sig,
        "Symbol": symbol,
        "Condition": condition,
        "EntryTime": times,
        "ExitTime": times + pd.Timedelta("4h"),
        "Return [%]": returns,
    })


def test_get_trade_timeframes_basic():
    df = pd.concat([
        _make_trades_with_condition(condition="BTCUSDT_1H"),
        _make_trades_with_condition(condition="ETHUSDT_4H"),
        _make_trades_with_condition(condition="XRPUSDT_1H"),
    ], ignore_index=True)
    tfs = get_trade_timeframes(df)
    assert tfs == ["1H", "4H"]


def test_get_trade_timeframes_single():
    df = _make_trades_with_condition(condition="BTCUSDT_4H")
    assert get_trade_timeframes(df) == ["4H"]


def test_get_trade_timeframes_missing_col():
    df = pd.DataFrame({"Symbol": ["BTC"], "Return [%]": [1.0]})
    assert get_trade_timeframes(df) == []


def test_get_trade_timeframes_empty():
    assert get_trade_timeframes(pd.DataFrame()) == []


# ── filter_trades_by_timeframe ────────────────────────────────────────────────


def test_filter_by_timeframe_basic():
    df = pd.concat([
        _make_trades_with_condition(n=5, condition="BTCUSDT_1H"),
        _make_trades_with_condition(n=8, condition="ETHUSDT_4H"),
    ], ignore_index=True)
    filtered = filter_trades_by_timeframe(df, "1H")
    assert len(filtered) == 5
    assert (filtered["Condition"] == "BTCUSDT_1H").all()


def test_filter_by_timeframe_unknown_tf():
    df = _make_trades_with_condition(condition="BTCUSDT_1H")
    result = filter_trades_by_timeframe(df, "1D")
    assert result.empty


def test_filter_by_timeframe_empty_input():
    result = filter_trades_by_timeframe(pd.DataFrame(), "1H")
    assert result.empty


# ── cross_tf_consensus ────────────────────────────────────────────────────────


def _make_verdict(sigs_pass: list[str], sigs_fail: list[str]) -> pd.DataFrame:
    rows = (
        [{"Parameter Signature": s, "verdict": "✅ PASS"} for s in sigs_pass]
        + [{"Parameter Signature": s, "verdict": "❌ FAIL"} for s in sigs_fail]
    )
    return pd.DataFrame(rows)


def test_cross_tf_consensus_all_pass():
    tf_verdicts = {
        "1H": _make_verdict(["SIG_A", "SIG_B"], []),
        "4H": _make_verdict(["SIG_A", "SIG_B"], []),
    }
    df = cross_tf_consensus(tf_verdicts)
    assert len(df) == 2
    assert (df["tfs_passing"] == 2).all()
    assert (df["cross_verdict"] == "✅ ALL").all()


def test_cross_tf_consensus_partial():
    tf_verdicts = {
        "1H": _make_verdict(["SIG_A"], ["SIG_B"]),
        "4H": _make_verdict(["SIG_A", "SIG_B"], []),
    }
    df = cross_tf_consensus(tf_verdicts)
    row_a = df[df["Parameter Signature"] == "SIG_A"].iloc[0]
    row_b = df[df["Parameter Signature"] == "SIG_B"].iloc[0]
    assert row_a["tfs_passing"] == 2
    assert row_a["cross_verdict"] == "✅ ALL"
    assert row_b["tfs_passing"] == 1
    assert row_b["cross_verdict"] == "⚠️ SOME"


def test_cross_tf_consensus_none_pass():
    tf_verdicts = {
        "1H": _make_verdict([], ["SIG_A"]),
        "4H": _make_verdict([], ["SIG_A"]),
    }
    df = cross_tf_consensus(tf_verdicts)
    assert df.iloc[0]["cross_verdict"] == "❌ NONE"


def test_cross_tf_consensus_empty():
    assert cross_tf_consensus({}).empty
    assert cross_tf_consensus({"1H": pd.DataFrame()}).empty


# ── coin_window_breakdown ──────────────────────────────────────────────────────

from strategy_evaluation.phase2 import coin_window_breakdown  # noqa: E402


def test_coin_window_breakdown_basic():
    """Two coins, one passing per window — correct sigs_passing and pass_rate."""
    cfg = _make_cfg(min_sqn=1.0, min_win_rate=30.0, min_profit_factor=1.2)
    sig = "SIG_A"
    # BTC passes (20 good trades), ETH only has 2 trades → fails min_trades
    btc = _make_trades(n_trades=20, sig=sig, symbol="BTCUSDT", start="2023-01-01")
    eth = _make_trades(n_trades=2, sig=sig, symbol="ETHUSDT", start="2023-01-01")
    trades = pd.concat([btc, eth], ignore_index=True)

    windows_cfg: dict = {"Full Period": (None, None)}
    df = coin_window_breakdown(trades, [sig], windows_cfg, cfg, min_trades_per_coin=5)

    assert not df.empty
    btc_row = df[df["Symbol"] == "BTCUSDT"].iloc[0]
    eth_row = df[df["Symbol"] == "ETHUSDT"].iloc[0]
    assert btc_row["sigs_passing"] == 1
    assert btc_row["pass_rate"] == pytest.approx(1.0)
    assert eth_row["sigs_passing"] == 0
    assert eth_row["pass_rate"] == pytest.approx(0.0)


def test_coin_window_breakdown_empty_input():
    """Empty trades → empty DataFrame."""
    cfg = _make_cfg()
    df = coin_window_breakdown(pd.DataFrame(), ["SIG_A"], {"Full Period": (None, None)}, cfg)
    assert df.empty


def test_coin_window_breakdown_all_pass():
    """All sigs pass for the single coin → pass_rate == 1.0 for every window row."""
    cfg = _make_cfg(min_sqn=0.0, min_win_rate=0.0, min_profit_factor=0.0)
    sigs = ["SIG_A", "SIG_B"]
    rows = [
        _make_trades(n_trades=20, sig=s, symbol="BTCUSDT", start="2023-01-01")
        for s in sigs
    ]
    trades = pd.concat(rows, ignore_index=True)

    windows_cfg = {"Bear": ("2023-01-01", "2023-06-30"), "Full Period": (None, None)}
    df = coin_window_breakdown(trades, sigs, windows_cfg, cfg, min_trades_per_coin=1)

    assert not df.empty
    assert (df["pass_rate"] == 1.0).all()

