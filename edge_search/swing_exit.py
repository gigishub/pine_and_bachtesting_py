"""Round 4b: band breakout (variant A) with trailing or fixed stops (see PLAN.md).

usage: python swing_exit.py train|valid|test
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import swing_trend as st


def machine(close, ema, a, x, mode, m):
    n = len(close)
    up = close > ema + x * a
    dn = close < ema - x * a
    pos = np.zeros(n)
    s, ext, stop, armed = 0, 0.0, 0.0, True
    for i in range(n):
        if np.isnan(a[i]):
            continue
        if not (up[i] or dn[i]):
            armed = True
        if s == 1:
            ext = max(ext, close[i])
            hit = close[i] < ext - m * a[i] if mode == "trail" else (close[i] < stop or close[i] < ema[i])
            if hit:
                s, armed = 0, False
        elif s == -1:
            ext = min(ext, close[i])
            hit = close[i] > ext + m * a[i] if mode == "trail" else (close[i] > stop or close[i] > ema[i])
            if hit:
                s, armed = 0, False
        if s == 0 and armed:
            if up[i]:
                s, ext, stop, armed = 1, close[i], close[i] - m * a[i], True
            elif dn[i]:
                s, ext, stop, armed = -1, close[i], close[i] + m * a[i], True
        pos[i] = s
    return pos


def signal(df, n, x, mode, m):
    c, a = df["Close"], st.atr(df, n)
    ema = c.ewm(span=n, adjust=False).mean()
    return pd.Series(machine(c.to_numpy(), ema.to_numpy(), a.to_numpy(), x, mode, m), index=df.index)


def run(split: str, only_tf: str | None = None, only_x: float | None = None, only_exit: str | None = None):
    lo, hi = st.SPLITS[split]
    rows = []
    for tf in (only_tf,) if only_tf else ("1d", "4h", "1h"):
        dfs = st.load(tf)
        bpd = st.BPD[tf]
        bpy = 365.25 * bpd
        for days in (10, 20):
            for x in (only_x,) if only_x else (1.0, 2.0):
                for mode in (only_exit,) if only_exit else ("trail", "fixed"):
                    for m in (2.0, 3.0):
                        poss = {k: signal(d, days * bpd, x, mode, m) for k, d in dfs.items()}
                        for leg, sel in (("both", lambda p: p), ("long", lambda p: p.clip(lower=0)), ("short", lambda p: p.clip(upper=0))):
                            pp = {k: sel(p) for k, p in poss.items()}
                            port = st.portfolio({k: st.coin_returns(dfs[k], pp[k]) for k in dfs})
                            r = port.loc[lo:hi]
                            mm = st.stats(r, bpy)
                            p = st.shift_p(dfs, pp, lo, hi, bpy) if leg != "short" else np.nan
                            tr = np.mean([pp[k].loc[lo:hi].diff().abs().sum() / 2 / max(1, len(pp[k].loc[lo:hi]) / bpy) for k in dfs])
                            rows.append({"tf": tf, "days": days, "x": x, "exit": mode, "m": m, "leg": leg, **mm, "shift_p": p, "trades/yr": tr})
        print(tf, "done", flush=True)
    pd.DataFrame(rows).to_csv(Path(__file__).resolve().parent / "results" / f"round4b_{split}{'_plateau' if only_tf else ''}.csv", index=False)


if __name__ == "__main__":
    a = sys.argv
    run(a[1], *(a[2:3]), *([float(a[3])] if len(a) > 3 else []), *(a[4:5]))
