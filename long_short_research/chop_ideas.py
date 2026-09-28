"""Chop detectors (regime) and mean-reversion signals (setup). All known at the daily close."""

from __future__ import annotations

import numpy as np
import pandas as pd

from ideas import _bcast, ema


def efficiency(x: pd.DataFrame | pd.Series, n: int):
    """Kaufman efficiency ratio: net move / path length over n days. Near 0 = chop, near 1 = clean trend."""
    return (x - x.shift(n)).abs() / x.diff().abs().rolling(n).sum()


def rsi(c: pd.DataFrame, n: int) -> pd.DataFrame:
    delta = c.diff()
    up = delta.clip(lower=0).ewm(alpha=1 / n, min_periods=n, adjust=False).mean()
    dn = (-delta.clip(upper=0)).ewm(alpha=1 / n, min_periods=n, adjust=False).mean()
    return 100 - 100 / (1 + up / dn)


# ── regime: chop detectors, return one mask (chop = True) ─────────────────────

def btc_er(d, n, thr):
    return _bcast(efficiency(d["close"]["BTCUSDT"], n) < thr, d["close"])


def btc_flat(d, n, thr):
    b = d["close"]["BTCUSDT"]
    return _bcast((b / b.shift(n) - 1).abs() < thr, d["close"])


def btc_flips(d, lookback, min_flips):
    """BTC 20-day trend sign changed at least min_flips times in the last lookback days."""
    b = d["close"]["BTCUSDT"]
    sign = np.sign(b / b.shift(20) - 1)
    flips = (sign.diff().abs() > 0).astype(int).rolling(lookback).sum()
    return _bcast(flips >= min_flips, d["close"])


def btc_near_ema(d, n, thr):
    b = d["close"]["BTCUSDT"]
    return _bcast((b / ema(b, n) - 1).abs() < thr, d["close"])


def coin_er(d, n, thr):
    return efficiency(d["close"], n) < thr


def coin_flat(d, n, thr):
    c = d["close"]
    return (c / c.shift(n) - 1).abs() < thr


CHOP = {
    "btc_er20<0.2": (btc_er, {"n": 20, "thr": 0.2}),
    "btc_er20<0.3": (btc_er, {"n": 20, "thr": 0.3}),
    "btc_er40<0.2": (btc_er, {"n": 40, "thr": 0.2}),
    "btc_flat30<10%": (btc_flat, {"n": 30, "thr": 0.10}),
    "btc_flat60<15%": (btc_flat, {"n": 60, "thr": 0.15}),
    "btc_flips60>=3": (btc_flips, {"lookback": 60, "min_flips": 3}),
    "btc_flips90>=4": (btc_flips, {"lookback": 90, "min_flips": 4}),
    "btc_near_ema100<5%": (btc_near_ema, {"n": 100, "thr": 0.05}),
    "coin_er20<0.2": (coin_er, {"n": 20, "thr": 0.2}),
    "coin_er20<0.3": (coin_er, {"n": 20, "thr": 0.3}),
    "coin_flat30<15%": (coin_flat, {"n": 30, "thr": 0.15}),
}


def reversal_probe(d):
    """Generic mean reversion: long after a 5-day drop, short after a 5-day rise."""
    c = d["close"]
    r = c / c.shift(5) - 1
    return r < 0, r > 0


# ── setup: mean-reversion entries, (long_mask, short_mask) ────────────────────

def rsi_extreme(d, n, lo, hi):
    r = rsi(d["close"], n)
    return r < lo, r > hi


def band_z(d, n, z):
    """Close vs n-day mean in n-day standard deviations (Bollinger position)."""
    c = d["close"]
    zz = (c - c.rolling(n).mean()) / c.rolling(n).std()
    return zz < -z, zz > z


def range_pos(d, n, edge):
    c = d["close"]
    hi, lo = c.rolling(n).max(), c.rolling(n).min()
    pos = (c - lo) / (hi - lo)
    return pos < edge, pos > 1 - edge


def ret_z(d, n, z):
    """n-day return in units of its typical size (60-day daily vol * sqrt(n))."""
    c = d["close"]
    vol = c.pct_change().rolling(60).std() * np.sqrt(n)
    zz = (c / c.shift(n) - 1) / vol
    return zz < -z, zz > z


MEANREV = {
    "rsi2<10|>90": (rsi_extreme, {"n": 2, "lo": 10, "hi": 90}),
    "rsi14<35|>65": (rsi_extreme, {"n": 14, "lo": 35, "hi": 65}),
    "rsi14<30|>70": (rsi_extreme, {"n": 14, "lo": 30, "hi": 70}),
    "band20_z1.5": (band_z, {"n": 20, "z": 1.5}),
    "band20_z2": (band_z, {"n": 20, "z": 2.0}),
    "range20_edge0.2": (range_pos, {"n": 20, "edge": 0.2}),
    "range40_edge0.15": (range_pos, {"n": 40, "edge": 0.15}),
    "ret3_z1": (ret_z, {"n": 3, "z": 1.0}),
    "ret5_z1.5": (ret_z, {"n": 5, "z": 1.5}),
}
