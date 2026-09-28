"""Shared data loading, trade simulation, and metrics for swing research."""

from __future__ import annotations

import glob
from pathlib import Path

import numpy as np
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "crypto_data" / "data"
FEE = 0.001  # per side
TEST_START = pd.Timestamp("2024-10-01", tz="UTC")
TF_DELTA = {"1d": pd.Timedelta(days=1), "4h": pd.Timedelta(hours=4), "1h": pd.Timedelta(hours=1)}


def available_symbols(tf: str) -> list[str]:
    return sorted(Path(p).parent.name for p in glob.glob(str(DATA_DIR / "*" / f"*_{tf}_start_*.parquet")))


def load(symbol: str, tf: str) -> pd.DataFrame:
    """Load closed candles only, with lowercase OHLCV columns."""
    path = sorted(glob.glob(str(DATA_DIR / symbol / f"{symbol}_{tf}_start_*.parquet")))[-1]
    df = pd.read_parquet(path)
    df.columns = [c.lower() for c in df.columns]
    now = pd.Timestamp.now(tz="UTC")
    return df[df.index + TF_DELTA[tf] <= now]


def trades_from_position(df: pd.DataFrame, pos: pd.Series) -> pd.DataFrame:
    """Turn a 0/1 position series (already aligned to the bar it is held on) into trades.

    Entering at bar i means buying at open[i]; leaving at bar i means selling at open[i].
    """
    pos = (pos.fillna(0) > 0).astype(int)
    change = pos.diff().fillna(pos.iloc[0])
    entries = df.index[change == 1]
    exits = df.index[change == -1]
    rows = []
    for t_in in entries:
        later = exits[exits > t_in]
        t_out = later[0] if len(later) else None
        p_in = df.at[t_in, "open"]
        p_out = df.at[t_out, "open"] if t_out is not None else df["close"].iloc[-1]
        ret = (p_out * (1 - FEE)) / (p_in * (1 + FEE)) - 1
        rows.append({"entry": t_in, "exit": t_out, "ret": ret,
                     "bars": (df.index.get_loc(t_out) if t_out is not None else len(df)) - df.index.get_loc(t_in)})
    return pd.DataFrame(rows, columns=["entry", "exit", "ret", "bars"])


def equity_from_position(df: pd.DataFrame, pos: pd.Series) -> pd.Series:
    """Open-to-open equity curve with fees charged on each position change."""
    pos = pos.fillna(0)
    r = df["open"].shift(-1) / df["open"] - 1
    fees = pos.diff().abs().fillna(pos.iloc[0]) * FEE
    return (1 + pos * r.fillna(0) - fees).cumprod()


def metrics(df: pd.DataFrame, pos: pd.Series, start=None, end=None) -> dict:
    sel = slice(start, end)
    d, p = df.loc[sel], pos.loc[sel]
    if len(d) < 2:
        return {}
    eq = equity_from_position(d, p)
    tr = trades_from_position(d, p)
    years = (d.index[-1] - d.index[0]).days / 365.25
    wins, losses = tr.ret[tr.ret > 0].sum(), -tr.ret[tr.ret <= 0].sum()
    bh = d["close"].iloc[-1] / d["open"].iloc[0]
    return {
        "trades": len(tr),
        "win%": 100 * (tr.ret > 0).mean() if len(tr) else np.nan,
        "PF": wins / losses if losses > 0 else np.nan,
        "avg%": 100 * tr.ret.mean() if len(tr) else np.nan,
        "ret%": 100 * (eq.iloc[-1] - 1),
        "CAGR%": 100 * (eq.iloc[-1] ** (1 / years) - 1) if years > 0 else np.nan,
        "maxDD%": 100 * (eq / eq.cummax() - 1).min(),
        "expo%": 100 * (p > 0).mean(),
        "BH%": 100 * (bh - 1),
        "BH_DD%": 100 * (d["close"] / d["close"].cummax() - 1).min(),
    }


def report(results: dict[str, pd.Series], tf: str, title: str) -> pd.DataFrame:
    """Train/test metrics table for a dict of symbol -> position series."""
    rows = []
    for sym, pos in results.items():
        df = load(sym, tf)
        for name, s, e in [("train", None, TEST_START - pd.Timedelta(seconds=1)), ("test", TEST_START, None)]:
            m = metrics(df, pos, s, e)
            if m:
                rows.append({"symbol": sym, "period": name, **m})
    out = pd.DataFrame(rows).set_index(["period", "symbol"]).sort_index()
    print(f"\n=== {title} ===")
    with pd.option_context("display.float_format", "{:.2f}".format, "display.width", 200):
        print(out)
        print("\nMedian by period:")
        print(out.groupby(level=0).median())
    return out
