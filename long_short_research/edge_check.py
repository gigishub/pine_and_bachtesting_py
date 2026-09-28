"""Top-down edge check for long/short trend signals on the point-in-time large-cap universe.

Each (coin, day) in the universe where a signal fires is one sample: enter at the next open, hold H days.
A layer's edge = profit factor of those samples minus the profit factor of its baseline population,
checked against random time-shifts of the same signal, per coin and per year.
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
HORIZONS = (3, 5, 10, 20)
PRIMARY_H = 20
ROUND_TRIP = 0.002
UNIVERSE_N = 10
MIN_LISTED = 180
N_SHIFTS = 200
MIN_SAMPLES_COIN = 60
MIN_SAMPLES_YEAR = 30


def build(universe_n: int = UNIVERSE_N) -> dict:
    """Wide price frames, universe mask, and forward returns per horizon."""
    panel = load_panel()
    o, c, v = panel["open"], panel["close"], panel["dvol"]
    listed = c.notna().cumsum()
    liq = v.rolling(180, min_periods=120).median().where(c.notna() & (listed >= MIN_LISTED))
    universe = liq.rank(axis=1, ascending=False, method="first") <= universe_n
    keep = universe.columns[universe.any()]
    o, c, v, universe = o[keep], c[keep], v[keep], universe[keep]
    last_close = c.ffill()
    entry = o.shift(-1)
    last_day = c.index[-1]
    fwd = {}
    for h in HORIZONS:
        # exit at the open h days after entry; a coin that stops trading exits at its last close
        exit_ = o.shift(-1 - h).fillna(last_close.shift(-h))
        r = exit_ / entry - 1
        r[c.index + pd.Timedelta(days=1 + h) > last_day] = np.nan
        fwd[h] = r.where(entry.notna())
    return {"open": o, "close": c, "dvol": v, "universe": universe, "fwd": fwd}


def pf(r: np.ndarray) -> float:
    gains, losses = r[r > 0].sum(), -r[r < 0].sum()
    if losses > 0:
        return gains / losses
    return np.inf if gains > 0 else np.nan


def side_returns(fwd: pd.DataFrame, side: str) -> pd.DataFrame:
    return (fwd if side == "long" else -fwd) - ROUND_TRIP


def samples(ret: pd.DataFrame, mask: pd.DataFrame, period: tuple, h: int) -> pd.Series:
    """Stacked returns where mask is true, with signal date inside the period and exit before its end."""
    idx = ret.index
    ok = (idx >= period[0]) & (idx + pd.Timedelta(days=1 + h) <= period[1] + pd.Timedelta(days=1))
    s = ret[ok].where(mask[ok].fillna(False).astype(bool)).stack()
    return s.dropna()


@dataclass
class Result:
    name: str
    side: str
    n: int
    base_n: int
    pf: float
    base_pf: float
    lift: float
    mean: float
    base_mean: float
    p_shift: float
    coins_ok: str
    years_ok: str
    lift_h: dict
    passed: bool


def evaluate(d: dict, name: str, side: str, cand: pd.DataFrame, base: pd.DataFrame,
             period: tuple = TRAIN, shifts: int = N_SHIFTS, seed: int = 0,
             h_main: int = PRIMARY_H, horizons: tuple = (5, 10, 20)) -> Result:
    """Candidate = base AND cand. Everything is restricted to the universe."""
    u = d["universe"]
    base = base & u
    both = base & cand
    ret = side_returns(d["fwd"][h_main], side)
    s_c, s_b = samples(ret, both, period, h_main), samples(ret, base, period, h_main)
    pf_c, pf_b = pf(s_c.values), pf(s_b.values)
    lift = pf_c - pf_b

    # null: shift the candidate signal in time (same shift for all coins), keep the baseline fixed
    rng = np.random.default_rng(seed)
    cv = cand.fillna(False).to_numpy()
    null = []
    for k in rng.integers(60, len(cand) - 60, size=shifts):
        shifted = pd.DataFrame(np.roll(cv, k, axis=0), index=cand.index, columns=cand.columns)
        null.append(pf(samples(ret, base & shifted, period, h_main).values) - pf_b)
    p_shift = float(np.mean(np.array(null) >= lift)) if shifts else np.nan

    def grouped_ok(key_c, key_b, min_n):
        ok = tot = 0
        for g, rc in s_c.groupby(key_c):
            rb = s_b[key_b == g]
            if len(rc) >= min_n and len(rb) >= min_n:
                tot += 1
                ok += pf(rc.values) > pf(rb.values)
        return ok, tot

    co, ct = grouped_ok(s_c.index.get_level_values(1), s_b.index.get_level_values(1), MIN_SAMPLES_COIN)
    yo, yt = grouped_ok(s_c.index.get_level_values(0).year, s_b.index.get_level_values(0).year, MIN_SAMPLES_YEAR)

    lift_h = {}
    for h in horizons:
        rh = side_returns(d["fwd"][h], side)
        lift_h[h] = pf(samples(rh, both, period, h).values) - pf(samples(rh, base, period, h).values)

    passed = (lift >= 0.05 and p_shift <= 0.05 and ct > 0 and co / ct >= 0.6 and yt > 0 and yo / yt >= 0.6)
    return Result(name, side, len(s_c), len(s_b), pf_c, pf_b, lift, s_c.mean(), s_b.mean(), p_shift,
                  f"{co}/{ct}", f"{yo}/{yt}", lift_h, passed)


def table(results: list[Result]) -> pd.DataFrame:
    rows = []
    for r in results:
        rows.append({"idea": r.name, "side": r.side, "n": r.n, "cov%": 100 * r.n / max(r.base_n, 1),
                     "PF": r.pf, "basePF": r.base_pf, "lift": r.lift,
                     "mean%": 100 * r.mean, "base%": 100 * r.base_mean, "p_shift": r.p_shift,
                     "coins": r.coins_ok, "years": r.years_ok,
                     **{f"lift{h}": v for h, v in r.lift_h.items()}, "pass": "PASS" if r.passed else "fail"})
    return pd.DataFrame(rows)


def show(df: pd.DataFrame, title: str) -> None:
    print(f"\n=== {title} ===")
    with pd.option_context("display.float_format", "{:.3f}".format, "display.width", 250,
                           "display.max_columns", 30):
        print(df.to_string(index=False))
