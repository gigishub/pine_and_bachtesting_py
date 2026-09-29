"""Portfolio backtest engine: a weights table in, daily returns and metrics out.

Weights are decided on the daily close of day t and held from the open of day t+1.
Long positive, short negative. Cost is charged on turnover.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "swing_research"))
from rotation_pit import load_panel  # noqa: E402

TRAIN = (pd.Timestamp("2018-01-01", tz="UTC"), pd.Timestamp("2022-12-31", tz="UTC"))
VALID = (pd.Timestamp("2023-01-01", tz="UTC"), pd.Timestamp("2024-09-30", tz="UTC"))
TEST = (pd.Timestamp("2024-10-01", tz="UTC"), pd.Timestamp("2100-01-01", tz="UTC"))
SPLITS = {"train": TRAIN, "valid": VALID, "test": TEST}
COST = 0.0015  # per side of turnover: fee + slippage
UNIVERSE_N = 10
MIN_LISTED = 180
N_SHIFTS = 200


@dataclass
class Market:
    open: pd.DataFrame
    close: pd.DataFrame
    universe: pd.DataFrame  # bool: coin is in the top-N on that day
    ret: pd.DataFrame       # open(t) -> open(t+1) return, exit at last close for a delisted coin
    btc: str = "BTCUSDT"


def build_market(universe_n: int = UNIVERSE_N) -> Market:
    panel = load_panel()
    o, c, v = panel["open"], panel["close"], panel["dvol"]
    listed = c.notna().cumsum()
    liq = v.rolling(180, min_periods=120).median().where(c.notna() & (listed >= MIN_LISTED))
    universe = liq.rank(axis=1, ascending=False, method="first") <= universe_n
    keep = universe.columns[universe.any()]
    o, c, universe = o[keep], c[keep], universe[keep]
    nxt = o.shift(-1)
    last_bar = c.notna() & c.shift(-1).isna()
    nxt = nxt.where(~last_bar, c)
    ret = (nxt / o - 1).fillna(0.0)
    return Market(o, c, universe, ret)


def run(mkt: Market, w: pd.DataFrame, cost: float = COST) -> pd.Series:
    """Daily portfolio return series for target weights w (decided at the close of each day)."""
    w = w.reindex(index=mkt.ret.index, columns=mkt.ret.columns).fillna(0.0)
    held = w.shift(1).fillna(0.0)
    gross = (held * mkt.ret).sum(axis=1)
    turnover = held.diff().abs().sum(axis=1)
    turnover.iloc[0] = held.iloc[0].abs().sum()
    return gross - cost * turnover


def metrics(r: pd.Series, start=None, end=None) -> dict:
    r = r.loc[start:end]
    if len(r) < 30:
        return {}
    eq = (1 + r).cumprod()
    years = len(r) / 365.25
    cagr = eq.iloc[-1] ** (1 / years) - 1 if eq.iloc[-1] > 0 else -1.0
    dd = (eq / eq.cummax() - 1).min()
    return {
        "CAGR%": 100 * cagr,
        "maxDD%": 100 * dd,
        "calmar": cagr / abs(dd) if dd < 0 else np.nan,
        "sharpe": r.mean() / r.std() * np.sqrt(365.25) if r.std() > 0 else np.nan,
        "vol%": 100 * r.std() * np.sqrt(365.25),
    }


def buy_and_hold(mkt: Market, coin: str = "BTCUSDT") -> pd.Series:
    w = pd.DataFrame(0.0, index=mkt.ret.index, columns=mkt.ret.columns)
    w[coin] = 1.0
    return run(mkt, w)


def passes_win_condition(m: dict, bh: dict) -> tuple[bool, bool]:
    """(a) CAGR >= 20% and maxDD <= 20%; (b) beats buy-and-hold on both CAGR and maxDD."""
    if not m:
        return False, False
    a = m["CAGR%"] >= 20 and m["maxDD%"] >= -20
    b = m["CAGR%"] > bh["CAGR%"] and m["maxDD%"] > bh["maxDD%"]
    return a, b


def shift_pvalue(mkt: Market, w: pd.DataFrame, split: tuple, n: int = N_SHIFTS, seed: int = 0) -> float:
    """Share of circular time-shifts of the weights (inside the split) with Calmar >= the real one."""
    lo, hi = split
    w = w.reindex(index=mkt.ret.index, columns=mkt.ret.columns).fillna(0.0)
    idx = w.loc[lo:hi].index
    ret = mkt.ret.loc[idx]
    ww = w.loc[idx].to_numpy()
    rr = ret.to_numpy()

    def calmar(weights: np.ndarray) -> float:
        held = np.vstack([np.zeros((1, weights.shape[1])), weights[:-1]])
        turn = np.abs(np.diff(held, axis=0, prepend=held[:1])).sum(axis=1)
        d = (held * rr).sum(axis=1) - COST * turn
        eq = np.cumprod(1 + d)
        dd = (eq / np.maximum.accumulate(eq) - 1).min()
        cagr = eq[-1] ** (365.25 / len(d)) - 1 if eq[-1] > 0 else -1.0
        return cagr / abs(dd) if dd < 0 else np.inf if cagr > 0 else -np.inf

    real = calmar(ww)
    rng = np.random.default_rng(seed)
    shifts = rng.integers(30, len(ww) - 30, size=n)
    null = np.array([calmar(np.roll(ww, k, axis=0)) for k in shifts])
    return float((null >= real).mean())
