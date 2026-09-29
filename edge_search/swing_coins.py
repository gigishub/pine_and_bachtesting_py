"""Round 5: the long-only 1h band breakout (Round 4b plateau) on every perp with candles and funding.

usage: python swing_coins.py train|valid|test
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import swing_exit as se
import swing_trend as st

CELLS = [(10, 2.0, 2.0), (10, 2.0, 3.0), (20, 2.0, 2.0), (20, 2.0, 3.0)]  # days, x, m
ORIGINAL = {d.name for d in st.DATA.iterdir() if d.is_dir()}
MIN_BARS = 24 * 90


def run(split: str):
    lo, hi = st.SPLITS[split]
    dfs = {k: d for k, d in st.load("1h").items() if len(d.loc[lo:hi]) >= MIN_BARS}
    bpy = 365.25 * 24
    print(f"[{split}] {len(dfs)} coins with >= 90 days ({sum(k in ORIGINAL for k in dfs)} original)", flush=True)
    ew = {k: d["Close"].pct_change().fillna(0.0) for k, d in dfs.items()}
    liq = st.liquid_mask(dfs, "1h", 20)
    rows, per = [], {}
    for days, x, m in CELLS:
        poss = {k: se.signal(d, days * 24, x, "fixed", m) for k, d in dfs.items()}
        pp = {k: p.clip(lower=0) for k, p in poss.items()}
        rets = {k: st.coin_returns(dfs[k], pp[k]) for k in dfs}
        per[(days, m)] = pd.Series({k: st.stats(r.loc[lo:hi], bpy).get("CAGR%", np.nan) for k, r in rets.items()})
        for label, ks in (("all", list(dfs)), ("original11", [k for k in dfs if k in ORIGINAL]), ("new", [k for k in dfs if k not in ORIGINAL]), ("liquid20", list(dfs))):
            if len(ks) < 3:
                continue
            if label == "liquid20":
                ok = {k: liq[k].shift(1).fillna(False) for k in ks}
                gate = {k: pp[k] * liq[k].fillna(False).astype(float) for k in ks}
                port = st.portfolio({k: st.coin_returns(dfs[k], gate[k]).where(ok[k]) for k in ks})
                bh = st.stats(st.portfolio({k: ew[k].where(ok[k]) for k in ks}).loc[lo:hi], bpy)
                p = st.shift_p({k: dfs[k] for k in ks}, gate, lo, hi, bpy)
            else:
                port = st.portfolio({k: rets[k] for k in ks})
                bh = st.stats(st.portfolio({k: ew[k] for k in ks}).loc[lo:hi], bpy)
                p = st.shift_p({k: dfs[k] for k in ks}, {k: pp[k] for k in ks}, lo, hi, bpy) if label != "original11" else np.nan
            m1 = st.stats(port.loc[lo:hi], bpy)
            share = float((per[(days, m)][ks] > 0).mean())
            rows.append({"days": days, "m": m, "set": label, "coins": len(ks), **m1, "shift_p": p, "coins>0": share,
                         "EWbh_CAGR%": bh["CAGR%"], "EWbh_maxDD%": bh["maxDD%"], "EWbh_sharpe": bh["sharpe"]})
        print(pd.DataFrame(rows[-4:]).round(2).to_string(index=False), flush=True)
    out = pd.DataFrame(rows)
    out.to_csv(Path(__file__).resolve().parent / "results" / f"round5_{split}.csv", index=False)
    pd.DataFrame(per).to_csv(Path(__file__).resolve().parent / "results" / f"round5_{split}_per_coin.csv")


if __name__ == "__main__":
    run(sys.argv[1])
