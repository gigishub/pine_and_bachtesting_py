"""Tests for strategy_evaluation.loader."""

from __future__ import annotations

import textwrap
from pathlib import Path

import pandas as pd
import pytest

from strategy_evaluation.loader import load_run_dir


CSV_CONTENT = textwrap.dedent("""\
    Symbol,Timeframe,Condition,Parameter Signature,use_adx,Return [%],Profit Factor,Win Rate [%],Max Drawdown [%],# Trades,SQN,Sharpe Ratio,Calmar Ratio,Rank
    BTCUSDT,4H,BTCUSDT_4H,use_adx=1,True,30.0,2.5,40.0,8.0,20,1.2,0.9,1.1,1
    BTCUSDT,4H,BTCUSDT_4H,use_adx=0,False,5.0,1.1,30.0,12.0,15,0.3,0.2,0.4,2
""")


@pytest.fixture()
def run_dir(tmp_path: Path) -> Path:
    (tmp_path / "BTCUSDT_4H.csv").write_text(CSV_CONTENT)
    (tmp_path / "run_vbt.log").write_text("INFO some log line")
    trades = tmp_path / "trades"
    trades.mkdir()
    (trades / "BTCUSDT_4H_trade_log.csv").write_text("col1,col2\na,b")
    return tmp_path


def test_load_returns_dataframe(run_dir: Path) -> None:
    df = load_run_dir(run_dir)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2


def test_load_excludes_log_and_trades(run_dir: Path) -> None:
    df = load_run_dir(run_dir)
    # Trade log columns would include "col1" — should not be present
    assert "col1" not in df.columns


def test_load_missing_dir_raises() -> None:
    with pytest.raises(FileNotFoundError):
        load_run_dir("/nonexistent/path")


def test_load_empty_dir_raises(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="No CSV files"):
        load_run_dir(tmp_path)


def test_load_multiple_csvs(tmp_path: Path) -> None:
    for sym in ("ETHUSDT_4H", "SOLUSDT_1H"):
        (tmp_path / f"{sym}.csv").write_text(CSV_CONTENT)
    df = load_run_dir(tmp_path)
    assert len(df) == 4
