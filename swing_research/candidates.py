"""New swing strategy candidates on daily/4h data, compared on train and test across all coins."""

from __future__ import annotations

import sys

import numpy as np
import pandas as pd

from common import FEE, TEST_START, available_symbols, load, metrics

PERIODS = [("train", None, TEST_START - pd.Timedelta(seconds=1)), ("test", TEST_START, None)]
BARS_PER_DAY = {"1d": 1, "4h": 6}


def donchian(df: pd.DataFrame, n_entry: int, n_exit: int) -> pd.Series:
    """Long from a close above the prior n_entry-bar high until a close below the prior n_exit-bar low."""
    up = df["close"] > df["high"].rolling(n_entry).max().shift(1)
    down = df["close"] < df["low"].rolling(n_exit).min().shift(1)
    state = pd.Series(np.where(up, 1.0, np.where(down, 0.0, np.nan)), index=df.index).ffill().fillna(0)
    return state.shift(1).fillna(0)  # decided at close, filled at next open


def tsmom(df: pd.DataFrame, lookback: int, rebalance: int) -> pd.Series:
    """Long while the lookback return is positive, re-checked every `rebalance` bars."""
    sig = (df["close"] / df["close"].shift(lookback) - 1 > 0).astype(float)
    checks = np.arange(len(df)) % rebalance == 0
    state = sig.where(checks).ffill().fillna(0)
    return state.shift(1).fillna(0)


OLD_MAJORS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "BNBUSDT", "ADAUSDT", "AVAXUSDT", "LINKUSDT", "DOGEUSDT", "LTCUSDT"]


def rotation(tf: str, lookback_days: int, top_k: int, rebalance_days: int, btc_filter: bool = True,
             symbols: list[str] | None = None) -> tuple[pd.Series, pd.DataFrame]:
    """Equal-weight the top_k coins by lookback return, only while BTC is above its lookback-ago price."""
    bpd = BARS_PER_DAY[tf]
    data = {s: load(s, tf) for s in (symbols or available_symbols(tf))}
    close = pd.DataFrame({s: d["close"] for s, d in data.items()})
    opens = pd.DataFrame({s: d["open"] for s, d in data.items()})
    lb, rb = lookback_days * bpd, rebalance_days * bpd
    mom = close / close.shift(lb) - 1
    rank = mom.rank(axis=1, ascending=False)
    w = (rank <= top_k).astype(float).div(top_k)
    if btc_filter:
        w = w.mul((mom["BTCUSDT"] > 0).astype(float), axis=0)
    checks = np.arange(len(w)) % rb == 0
    w = w.where(pd.Series(checks, index=w.index), np.nan).ffill().fillna(0).shift(1).fillna(0)
    r = (opens.shift(-1) / opens - 1).fillna(0)
    turnover = w.diff().abs().sum(axis=1).fillna(w.abs().sum(axis=1))
    port = (w * r).sum(axis=1) - turnover * FEE
    return (1 + port).cumprod(), w


def equity_stats(eq: pd.Series, w: pd.DataFrame, start, end) -> dict:
    e = eq.loc[start:end]
    e = e / e.iloc[0]
    years = (e.index[-1] - e.index[0]).days / 365.25
    return {"CAGR%": 100 * (e.iloc[-1] ** (1 / years) - 1), "maxDD%": 100 * (e / e.cummax() - 1).min(),
            "expo%": 100 * (w.loc[start:end].sum(axis=1) > 0).mean(),
            "turnover/yr": w.loc[start:end].diff().abs().sum(axis=1).sum() / years}


def per_coin(tf: str, name: str, fn) -> pd.DataFrame:
    rows = []
    for s in available_symbols(tf):
        df = load(s, tf)
        pos = fn(df)
        for p, a, b in PERIODS:
            m = metrics(df, pos, a, b)
            if m:
                rows.append({"strategy": name, "period": p, "symbol": s, **m})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    tf = sys.argv[1] if len(sys.argv) > 1 else "1d"
    k = BARS_PER_DAY[tf]
    specs = {}
    for ne, nx in [(20, 10), (55, 20), (100, 50)]:
        specs[f"donchian_{ne}/{nx}d"] = lambda df, ne=ne, nx=nx: donchian(df, ne * k, nx * k)
    for lb in [30, 60, 90]:
        specs[f"tsmom_{lb}d_weekly"] = lambda df, lb=lb: tsmom(df, lb * k, 7 * k)

    cols = ["trades", "win%", "PF", "CAGR%", "maxDD%", "expo%", "BH%"]
    res = pd.concat([per_coin(tf, n, f) for n, f in specs.items()])
    with pd.option_context("display.float_format", "{:.2f}".format, "display.width", 200):
        print(f"=== {tf}: per-coin strategies, median over {res.symbol.nunique()} coins ===")
        print(res.groupby(["period", "strategy"])[cols].median())
        print("\n=== coins with PF > 1.3 ===")
        print(res.assign(ok=res.PF > 1.3).groupby(["period", "strategy"]).ok.sum().unstack(0))

        for uni_name, uni in [("all coins", None), ("old majors only", OLD_MAJORS)]:
            print(f"\n=== {tf}: rotation portfolio, BTC filter on, {uni_name} ===")
            rows = []
            for lb in [14, 30, 60]:
                for kk in [1, 3, 5]:
                    eq, w = rotation(tf, lb, kk, 7, symbols=uni)
                    for p, a, b in PERIODS:
                        rows.append({"lookback_d": lb, "top_k": kk, "period": p, **equity_stats(eq, w, a, b)})
            print(pd.DataFrame(rows).set_index(["period", "lookback_d", "top_k"]).sort_index())
