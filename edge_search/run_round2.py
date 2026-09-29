"""Round 2 runner: gates, win rule and capture ratios for the crowding overlays.

usage: python run_round2.py train|valid|test [K L ...]   |   python run_round2.py sanity
"""

from __future__ import annotations

import sys
import warnings
from types import SimpleNamespace

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

import engine
from crowding import CARRY_COST, IDEAS, Data, Idea, base_a
from engine import COST, N_SHIFTS, build_market, metrics

SPLITS = {
    "train": (pd.Timestamp("2020-11-15", tz="UTC"), pd.Timestamp("2023-06-30", tz="UTC")),
    "valid": (pd.Timestamp("2023-07-01", tz="UTC"), pd.Timestamp("2024-09-30", tz="UTC")),
    "test": (pd.Timestamp("2024-10-01", tz="UTC"), pd.Timestamp("2100-01-01", tz="UTC")),
}


def returns(mkt, idea: Idea, lo, mult=None) -> pd.Series:
    """Daily return of the idea; mult overrides the overlay (used for shifted nulls)."""
    mult = idea.mult if mult is None else mult
    r = engine.run(mkt, idea.base.mul(mult, axis=0))
    if idea.carry is not None:
        c = idea.carry.copy()
        c.loc[c.index >= lo] = c.loc[c.index >= lo]
        first = c.loc[lo:].index[0]
        c.loc[first] -= CARRY_COST
        r = 0.5 * r + 0.5 * c
    return r


def calmar(r: pd.Series) -> float:
    eq = (1 + r).cumprod()
    dd = (eq / eq.cummax() - 1).min()
    cagr = eq.iloc[-1] ** (365.25 / len(r)) - 1 if eq.iloc[-1] > 0 else -1.0
    return cagr / abs(dd) if dd < 0 else (np.inf if cagr > 0 else -np.inf)


def overlay_shift_p(mkt, idea, lo, hi, n=N_SHIFTS, seed=0) -> float:
    """Share of circular shifts of the overlay (inside the split) whose Calmar >= the real one."""
    real = calmar(returns(mkt, idea, lo).loc[lo:hi])
    win = idea.mult.loc[lo:hi]
    rng = np.random.default_rng(seed)
    null = []
    for s in rng.integers(30, len(win) - 30, size=n):
        m2 = idea.mult.copy()
        m2.loc[lo:hi] = np.roll(win.to_numpy(), int(s))
        null.append(calmar(returns(mkt, idea, lo, m2).loc[lo:hi]))
    return float((np.array(null) >= real).mean())


def blocks(r: pd.Series, lo, hi, n=30) -> pd.Series:
    r = r.loc[lo:hi]
    return (1 + r).groupby(pd.Series(range(len(r)), index=r.index) // n).prod() - 1


def capture(r, btc, lo, hi) -> tuple[float, float, int]:
    b, s = blocks(btc, lo, hi), blocks(r, lo, hi)
    up, dn = b > 0, b <= 0
    upc = 100 * s[up].mean() / b[up].mean()
    dnc = 100 * s[dn].mean() / b[dn].mean() if dn.any() else np.nan
    return upc, dnc, int(dn.sum())


def slim(mkt, lo, hi):
    """Market restricted to the split (plus a day of history) so the null runs fast."""
    sl = slice(lo - pd.Timedelta(days=2), hi)
    return SimpleNamespace(ret=mkt.ret.loc[sl], btc=mkt.btc)


def main():
    split = sys.argv[1]
    lo, hi = SPLITS[split]
    mkt = build_market()
    d = Data(mkt)
    names = sys.argv[2:] or list(IDEAS)
    sm = slim(mkt, lo, hi)

    def sliced(idea):
        s = slice(lo - pd.Timedelta(days=2), hi)
        return Idea(idea.base.loc[s], idea.mult.loc[s], None if idea.carry is None else idea.carry.loc[s])

    btc = engine.buy_and_hold(mkt)
    bh = metrics(btc, lo, hi)
    a = returns(mkt, base_a(d), lo)
    am = metrics(a, lo, hi)
    print(f"[{split}] {lo.date()} -> {min(hi, mkt.ret.index[-1]).date()}")
    print(f"BTC buy&hold  CAGR {bh['CAGR%']:.1f}%  maxDD {bh['maxDD%']:.1f}%   |   A baseline  CAGR {am['CAGR%']:.1f}%  "
          f"maxDD {am['maxDD%']:.1f}%  calmar {am['calmar']:.2f}\n")
    rows = []
    for nm in names:
        idea = IDEAS[nm](d, 1.0)
        r = returns(mkt, idea, lo)
        m = metrics(r, lo, hi)
        vs = [metrics(returns(mkt, IDEAS[nm](d, k), lo), lo, hi).get("CAGR%", np.nan) for k in (0.5, 2.0)]
        p = overlay_shift_p(sm, sliced(idea), lo, hi)
        upc, dnc, ndn = capture(r, btc, lo, hi)
        win_a = m["CAGR%"] >= 20 and m["maxDD%"] >= -20
        win_b_strict = m["CAGR%"] > bh["CAGR%"] and m["maxDD%"] > bh["maxDD%"]
        win_b_cap = upc >= 70 and dnc <= 30
        cut = 100 * (idea.mult.loc[lo:hi] < 1).mean()
        rows.append({"idea": nm, **{k: m[k] for k in ("CAGR%", "maxDD%", "calmar")}, "cut%days": cut,
                     "k0.5": vs[0], "k2": vs[1], "shift_p": p, "up_cap": upc, "dn_cap": dnc, "n_dn": ndn,
                     "g1": m["CAGR%"] > 0, "g2": p <= 0.05, "g3": min(vs) > 0,
                     "g4": m["calmar"] > am["calmar"] and m["maxDD%"] > am["maxDD%"],
                     "win_a": win_a, "win_b": win_b_strict, "win_cap": win_b_cap})
    out = pd.DataFrame(rows).set_index("idea")
    out.to_csv(f"results/round2_{split}.csv")
    with pd.option_context("display.float_format", "{:.2f}".format, "display.width", 300, "display.max_columns", 40):
        print(out)


def sanity():
    """Peeking overlay (cash before down days) must look great; a shuffled overlay must not."""
    lo, hi = SPLITS["train"]
    mkt = build_market()
    d = Data(mkt)
    base = base_a(d)
    peek = 1.0 - (mkt.ret[mkt.btc].shift(-1) < 0).astype(float)
    rng = np.random.default_rng(1)
    shuf = pd.Series(rng.permutation(peek.to_numpy()), index=peek.index)
    sm = slim(mkt, lo, hi)
    s = slice(lo - pd.Timedelta(days=2), hi)
    for label, mult in (("peeking", peek), ("shuffled", shuf)):
        idea = Idea(base.base, mult)
        r = returns(mkt, idea, lo)
        m = metrics(r, lo, hi)
        p = overlay_shift_p(sm, Idea(idea.base.loc[s], idea.mult.loc[s]), lo, hi, n=100)
        print(f"{label:9s} CAGR {m['CAGR%']:.0f}%  maxDD {m['maxDD%']:.0f}%  shift_p {p:.2f}")


if __name__ == "__main__":
    sanity() if sys.argv[1] == "sanity" else main()
