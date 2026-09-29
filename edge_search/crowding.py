"""Round 2 ideas K-T: crowding overlays (funding, open interest) on the BTC trend baseline (idea A).

An idea is a base weights table, an overlay multiplier (1 = keep, 0.5 = half, 0 = cash) and an optional carry sleeve.
k scales the overlay lookbacks only (7-day windows, 90-day z windows).
"""

from __future__ import annotations

import glob
import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from engine import Market
from ideas import TARGET_VOL, _btc_filter, _n, _weekly

DATA = Path(__file__).resolve().parent.parent / "crypto_data"
ALIAS = json.load(open(Path(__file__).resolve().parent.parent / "long_short_research" / "bybit_map.json"))["alt"]
INV = {v: k for k, v in ALIAS.items()}
CARRY_COST = 0.006  # spot + perp, entry and exit, at 0.15% per side each


def _utc(ix: pd.DatetimeIndex) -> pd.DatetimeIndex:
    return ix.tz_convert("UTC") if ix.tz else ix.tz_localize("UTC")


def load_funding(columns) -> pd.DataFrame:
    """Daily per-8h funding rate per coin: mean of the settlements inside each UTC day (all before that day's close)."""
    out = {}
    for p in glob.glob(str(DATA / "data*" / "*" / "*_funding_start_*.parquet")):
        sym = Path(p).parent.name
        name = INV.get(sym, sym)
        if name not in columns or name in out:
            continue
        f = pd.read_parquet(p)["fundingRate"].astype(float)
        f.index = _utc(f.index)
        out[name] = f.groupby(f.index.floor("D")).mean()
    return pd.DataFrame(out).sort_index()


def load_funding_sum(coin: str) -> pd.Series:
    p = glob.glob(str(DATA / "data" / coin / "*_funding_start_*.parquet"))[0]
    f = pd.read_parquet(p)["fundingRate"].astype(float)
    f.index = _utc(f.index)
    return f.groupby(f.index.floor("D")).sum()


def load_oi(coin: str) -> pd.Series:
    p = glob.glob(str(DATA / "data" / coin / "*_oi_1d_*.parquet"))[0]
    o = pd.read_parquet(p)["openInterest"].astype(float)
    o.index = _utc(o.index)
    return o


def _z(x: pd.Series, n: int) -> pd.Series:
    return (x - x.rolling(n).mean()) / x.rolling(n).std()


@dataclass
class Idea:
    base: pd.DataFrame
    mult: pd.Series
    carry: pd.Series | None = None  # daily carry return on the carry sleeve's notional (blend weight 0.5)


class Data:
    def __init__(self, m: Market):
        self.m = m
        self.idx = m.close.index
        f = load_funding(set(m.close.columns))
        self.fund = f.reindex(self.idx)
        self.btc_fund = self.fund[m.btc]
        self.btc_oi = load_oi(m.btc).reindex(self.idx)
        self.carry_raw = load_funding_sum(m.btc).reindex(self.idx).fillna(0.0)


def _cash(cond: pd.Series) -> pd.Series:
    return 1.0 - cond.fillna(False).astype(float)


def _a_base(m: Market, k: float = 1.0) -> pd.DataFrame:
    w = pd.DataFrame(0.0, index=m.close.index, columns=m.close.columns)
    w[m.btc] = _btc_filter(m, 1.0)
    return w


def _f7(d: Data, k: float) -> pd.Series:
    return d.btc_fund.rolling(_n(7, k), min_periods=_n(7, k)).mean()


def _o7(d: Data, k: float) -> pd.Series:
    n = _n(7, k)
    return d.btc_oi.shift(1) / d.btc_oi.shift(1 + n) - 1


def _c_funding_z(d, k, thr):
    return _z(_f7(d, k), _n(90, k)) > thr


def _c_funding_abs(d, k):
    return _f7(d, k) > 0.0003


def _c_oi_stall(d, k):
    n = _n(7, k)
    return (_o7(d, k) > 0.25) & (d.m.close[d.m.btc].pct_change(n) < 0.02)


def _c_oi_z(d, k):
    return _z(_o7(d, k), _n(90, k)) > 2


def _breadth_funding(d: Data, k: float) -> pd.Series:
    n = _n(7, k)
    f7 = d.fund.rolling(n, min_periods=n).mean().where(d.m.universe)
    return f7.median(axis=1) > 0.0002


def idea_k(d, k=1.0): return Idea(_a_base(d.m), _cash(_c_funding_z(d, k, 2)))
def idea_l(d, k=1.0): return Idea(_a_base(d.m), _cash(_c_funding_abs(d, k)))
def idea_m(d, k=1.0): return Idea(_a_base(d.m), _cash(_c_oi_stall(d, k)))
def idea_n(d, k=1.0): return Idea(_a_base(d.m), _cash(_c_oi_z(d, k)))


def idea_o(d, k=1.0):
    z = _z(_f7(d, k), _n(90, k))
    mult = pd.Series(1.0, index=d.idx).mask(z > 1, 0.5).mask(z > 2, 0.0)
    return Idea(_a_base(d.m), mult)


def idea_p(d, k=1.0): return Idea(_a_base(d.m), _cash(_c_funding_abs(d, k) | _c_oi_stall(d, k)))
def idea_q(d, k=1.0): return Idea(_a_base(d.m), _cash(_breadth_funding(d, k)))


def _r_base(d: Data) -> pd.DataFrame:
    has = d.fund.notna() & d.m.universe
    w = (has.astype(float) / 10).mul(_btc_filter(d.m, 1.0), axis=0)
    return _weekly(w)


def idea_r(d, k=1.0): return Idea(_r_base(d), _cash(_c_funding_z(d, k, 2)))


def _s_base(d: Data, k: float) -> pd.DataFrame:
    vol = d.m.close[d.m.btc].pct_change().rolling(_n(30, 1.0)).std() * np.sqrt(365.25)
    scale = (TARGET_VOL / vol).clip(upper=1.0).fillna(0.0)
    return _a_base(d.m).mul(scale, axis=0)


def idea_s(d, k=1.0): return Idea(_s_base(d, k), _cash(_c_funding_abs(d, k) | _c_oi_stall(d, k)))
def idea_t(d, k=1.0): return Idea(_a_base(d.m), _cash(_c_funding_abs(d, k)), carry=d.carry_raw)


def base_a(d, k=1.0): return Idea(_a_base(d.m), pd.Series(1.0, index=d.idx))


IDEAS = {"K": idea_k, "L": idea_l, "M": idea_m, "N": idea_n, "O": idea_o,
         "P": idea_p, "Q": idea_q, "R": idea_r, "S": idea_s, "T": idea_t}
