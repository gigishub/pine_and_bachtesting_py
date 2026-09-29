"""Round 4: EMA + ATR entries in both directions (see PLAN.md, Round 4).

usage: python swing_band.py train|valid|test
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import swing_trend as st


def _machine(close, ema, long_in, short_in):
    pos = np.zeros(len(close))
    s = 0
    for i in range(len(close)):
        if np.isnan(ema[i]):
            continue
        if s == 1 and close[i] < ema[i]:
            s = 0
        elif s == -1 and close[i] > ema[i]:
            s = 0
        if s == 0:
            if long_in[i]:
                s = 1
            elif short_in[i]:
                s = -1
        pos[i] = s
    return pos


def band(df, n, x):
    c, a = df["Close"], st.atr(df, n)
    ema = c.ewm(span=n, adjust=False).mean()
    pos = _machine(c.to_numpy(), ema.to_numpy(), (c > ema + x * a).to_numpy(), (c < ema - x * a).to_numpy())
    return pd.Series(pos, index=df.index)


def expansion(df, n, x):
    c, a = df["Close"], st.atr(df, n)
    ema = c.ewm(span=n, adjust=False).mean()
    exp = a >= x * a.rolling(n).mean()
    pos = _machine(c.to_numpy(), ema.to_numpy(), ((c > ema) & exp).to_numpy(), ((c < ema) & exp).to_numpy())
    return pd.Series(pos, index=df.index)


CELLS = [("A", band, x) for x in (1.0, 1.5, 2.0)] + [("B", expansion, x) for x in (1.25, 1.5)]


def run(split: str):
    lo, hi = st.SPLITS[split]
    rows = []
    for tf in ("1d", "4h", "1h"):
        dfs = st.load(tf)
        bpd = st.BPD[tf]
        bpy = 365.25 * bpd
        for var, fn, x in CELLS:
            for days in (10, 20):
                n = days * bpd
                poss = {k: fn(d, n, x) for k, d in dfs.items()}
                for leg, sel in (("both", lambda p: p), ("long", lambda p: p.clip(lower=0)), ("short", lambda p: p.clip(upper=0))):
                    pp = {k: sel(p) for k, p in poss.items()}
                    port = st.portfolio({k: st.coin_returns(dfs[k], pp[k]) for k in dfs})
                    m = st.stats(port.loc[lo:hi], bpy)
                    p = st.shift_p(dfs, pp, lo, hi, bpy) if leg == "both" else np.nan
                    tr = np.mean([pp[k].loc[lo:hi].diff().abs().sum() / 2 / max(1, len(pp[k].loc[lo:hi]) / bpy) for k in dfs])
                    exp_ = np.mean([(pp[k].loc[lo:hi] != 0).mean() for k in dfs])
                    rows.append({"tf": tf, "var": var, "x": x, "days": days, "leg": leg, **m, "shift_p": p, "trades/yr": tr, "in_mkt%": 100 * exp_})
        print(pd.DataFrame(rows).query("tf == @tf and leg == 'both'").round(2).to_string(index=False), flush=True)
    pd.DataFrame(rows).to_csv(Path(__file__).resolve().parent / "results" / f"round4_{split}.csv", index=False)


if __name__ == "__main__":
    run(sys.argv[1])
