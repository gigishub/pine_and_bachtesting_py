"""Round 3: long/short trend systems on 1h, 4h and 1d Bybit perps, net of costs and funding.

usage: python swing_trend.py train|valid|test    |    python swing_trend.py oracle
"""

from __future__ import annotations

import glob
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

DATA = Path(__file__).resolve().parent.parent / "crypto_data" / "data"
COST = 0.0010
BPD = {"1h": 24, "4h": 6, "1d": 1}
FREQ = {"1h": "1h", "4h": "4h", "1d": "1D"}
DAYS = (5, 20, 60)
SPLITS = {
    "train": (pd.Timestamp("2021-01-01", tz="UTC"), pd.Timestamp("2023-06-30 23:59", tz="UTC")),
    "valid": (pd.Timestamp("2023-07-01", tz="UTC"), pd.Timestamp("2024-09-30 23:59", tz="UTC")),
    "test": (pd.Timestamp("2024-10-01", tz="UTC"), pd.Timestamp("2100-01-01", tz="UTC")),
}
N_SHIFTS = 200


def load(tf: str) -> dict[str, pd.DataFrame]:
    """Per coin: OHLC plus the funding paid to a short over each bar (settlements in (bar start, bar end])."""
    out = {}
    for d in sorted(DATA.iterdir()):
        cf = glob.glob(str(d / f"{d.name}_{tf}_start_*.parquet"))
        ff = glob.glob(str(d / f"{d.name}_funding_start_*.parquet"))
        if not cf or not ff:
            continue
        c = pd.read_parquet(cf[0])
        c.index = c.index.tz_convert("UTC") if c.index.tz else c.index.tz_localize("UTC")
        f = pd.read_parquet(ff[0])["fundingRate"].astype(float)
        f.index = f.index.tz_convert("UTC") if f.index.tz else f.index.tz_localize("UTC")
        f = f.groupby((f.index - pd.Timedelta("1ns")).floor(FREQ[tf])).sum()
        c = c[~c.index.duplicated()].sort_index()
        c["fund"] = f.reindex(c.index).fillna(0.0)
        out[d.name] = c
    return out


def atr(df: pd.DataFrame, n: int) -> pd.Series:
    pc = df["Close"].shift(1)
    tr = pd.concat([df["High"] - df["Low"], (df["High"] - pc).abs(), (df["Low"] - pc).abs()], axis=1).max(axis=1)
    return tr.rolling(n).mean()


def f1(df, n):
    hh, ll = df["High"].rolling(n).max().shift(1), df["Low"].rolling(n).min().shift(1)
    raw = pd.Series(np.nan, index=df.index).mask(df["Close"] > hh, 1.0).mask(df["Close"] < ll, -1.0)
    return raw.ffill().fillna(0.0)


def f2(df, n):
    c = df["Close"]
    return np.sign(c.rolling(max(2, n // 4)).mean() - c.rolling(n).mean()).fillna(0.0)


def f3(df, n):
    c = df["Close"].to_numpy()
    a = atr(df, max(10, n // 4)).to_numpy()
    pos = np.zeros(len(c))
    state, ext = 0, c[0]
    for i in range(len(c)):
        if np.isnan(a[i]):
            continue
        if state == 0:
            state, ext = 1, c[i]
        elif state == 1:
            ext = max(ext, c[i])
            if c[i] < ext - 3 * a[i]:
                state, ext = -1, c[i]
        else:
            ext = min(ext, c[i])
            if c[i] > ext + 3 * a[i]:
                state, ext = 1, c[i]
        pos[i] = state
    return pd.Series(pos, index=df.index)


def f4(df, n):
    return np.sign(df["Close"].pct_change(n)).fillna(0.0)


FAMILIES = {"F1": f1, "F2": f2, "F3": f3, "F4": f4}


def coin_returns(df: pd.DataFrame, pos: pd.Series) -> pd.Series:
    """Net return per bar: position held from the previous close, cost on turnover, funding by side."""
    held = pos.shift(1).fillna(0.0)
    r = df["Close"].pct_change().fillna(0.0)
    turn = held.diff().abs().fillna(held.abs())
    return held * r - COST * turn + held * df["fund"] * -1.0


def portfolio(rets: dict[str, pd.Series]) -> pd.Series:
    return pd.DataFrame(rets).mean(axis=1, skipna=True)


def stats(r: pd.Series, bpy: float) -> dict:
    if len(r) < 50:
        return {}
    eq = (1 + r).cumprod()
    yrs = len(r) / bpy
    cagr = eq.iloc[-1] ** (1 / yrs) - 1 if eq.iloc[-1] > 0 else -1.0
    dd = (eq / eq.cummax() - 1).min()
    return {"CAGR%": 100 * cagr, "maxDD%": 100 * dd, "sharpe": r.mean() / r.std() * np.sqrt(bpy) if r.std() > 0 else np.nan}


def shift_p(dfs, poss, lo, hi, bpy, n=N_SHIFTS, seed=0) -> float:
    """Share of circular shifts of all coins' positions (same shift, inside the split) with Sharpe >= real."""
    names = list(dfs)
    idx = dfs[names[0]].loc[lo:hi].index
    for k in names:
        idx = idx.union(dfs[k].loc[lo:hi].index)
    R = np.full((len(idx), len(names)), np.nan)
    P = np.zeros((len(idx), len(names)))
    Fd = np.zeros((len(idx), len(names)))
    for j, k in enumerate(names):
        d = dfs[k].reindex(idx)
        R[:, j] = d["Close"].pct_change().to_numpy()
        Fd[:, j] = np.nan_to_num(d["fund"].to_numpy())
        P[:, j] = poss[k].reindex(idx).fillna(0.0).to_numpy()
    R = np.nan_to_num(R)

    def sharpe(p):
        held = np.vstack([np.zeros((1, p.shape[1])), p[:-1]])
        turn = np.abs(np.diff(held, axis=0, prepend=held[:1]))
        r = held * R - COST * turn - held * Fd
        avail = (np.abs(held) > 0) | (np.abs(R) > 0)
        cnt = np.maximum(avail.sum(axis=1), 1)
        port = r.sum(axis=1) / cnt
        return port.mean() / port.std() if port.std() > 0 else -np.inf

    real = sharpe(P)
    rng = np.random.default_rng(seed)
    null = [sharpe(np.roll(P, int(s), axis=0)) for s in rng.integers(len(P) // 20, len(P) - len(P) // 20, size=n)]
    return float((np.array(null) >= real).mean())


def run(split: str):
    lo, hi = SPLITS[split]
    rows = []
    for tf in ("1d", "4h", "1h"):
        dfs = load(tf)
        bpy = 365.25 * BPD[tf]
        btc = dfs["BTCUSDT"]["Close"].pct_change().fillna(0.0)
        bh = stats(btc.loc[lo:hi], bpy)
        print(f"[{split}] {tf}: {len(dfs)} coins; BTC buy&hold CAGR {bh['CAGR%']:.1f}% maxDD {bh['maxDD%']:.1f}%", flush=True)
        for fam, fn in FAMILIES.items():
            for days in DAYS:
                n = days * BPD[tf]
                poss = {k: fn(d, n) for k, d in dfs.items()}
                for leg, sel in (("both", lambda p: p), ("long", lambda p: p.clip(lower=0)), ("short", lambda p: p.clip(upper=0))):
                    pp = {k: sel(p) for k, p in poss.items()}
                    port = portfolio({k: coin_returns(dfs[k], pp[k]) for k in dfs})
                    m = stats(port.loc[lo:hi], bpy)
                    p = shift_p(dfs, pp, lo, hi, bpy) if leg == "both" else np.nan
                    flips = np.mean([pp[k].loc[lo:hi].diff().abs().sum() / 2 / max(1, len(pp[k].loc[lo:hi]) / bpy) for k in dfs])
                    rows.append({"tf": tf, "fam": fam, "days": days, "leg": leg, **m, "shift_p": p, "trades/yr": flips})
        print(pd.DataFrame(rows).query("tf == @tf and leg == 'both'").round(2).to_string(index=False), flush=True)
    out = pd.DataFrame(rows)
    out.to_csv(Path(__file__).resolve().parent / "results" / f"round3_{split}.csv", index=False)


def oracle():
    """Hindsight zigzag on daily BTC: total return of riding every >=20% swing both ways (the ceiling)."""
    c = load("1d")["BTCUSDT"]["Close"]
    c = c.loc[SPLITS["train"][0]:SPLITS["train"][1]]
    for thr in (0.10, 0.20, 0.30):
        pivot, direction, log_gain, moves = c.iloc[0], 0, 0.0, 0
        hi_, lo_ = c.iloc[0], c.iloc[0]
        for v in c.iloc[1:]:
            hi_, lo_ = max(hi_, v), min(lo_, v)
            if direction >= 0 and v <= hi_ * (1 - thr):
                log_gain += np.log(hi_ / pivot) if direction == 1 else 0
                pivot, direction, lo_, moves = hi_, -1, v, moves + 1
            elif direction <= 0 and v >= lo_ * (1 + thr):
                log_gain += np.log(pivot / lo_) if direction == -1 else 0
                pivot, direction, hi_, moves = lo_, 1, v, moves + 1
        yrs = len(c) / 365.25
        print(f"zigzag {int(thr * 100)}%: {moves} swings, hindsight long/short ≈ {100 * (np.exp(log_gain / yrs) - 1):.0f}% per year (log-compounded)")
    print(f"BTC buy&hold train: {100 * ((c.iloc[-1] / c.iloc[0]) ** (365.25 / len(c)) - 1):.0f}% per year")


if __name__ == "__main__":
    oracle() if sys.argv[1] == "oracle" else run(sys.argv[1])
