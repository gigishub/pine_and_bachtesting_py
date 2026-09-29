"""Round 6: BTC as the leader for other coins (see PLAN.md, Round 6).

usage: python swing_lead.py train|valid|test
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import swing_exit as se
import swing_trend as st

BTC = "BTCUSDT"


def btc_filter_bars(btc_daily: pd.DataFrame, index: pd.DatetimeIndex) -> pd.Series:
    """BTC trend filter from daily closes (close > SMA200 and 20d return > -3%), known from the previous closed day."""
    c = btc_daily["Close"]
    f = ((c > c.rolling(200).mean()) & (c.pct_change(20) > -0.03)).astype(float).shift(1)
    return f.reindex(index.floor("D")).set_axis(index).fillna(0.0)


def follow_machine(close, a, trigger_long, trigger_short, btc_state, m):
    """R3: enter when BTC state flips to +/-1, exit when BTC state changes or at the ATR stop."""
    pos = np.zeros(len(close))
    s, stop = 0, 0.0
    for i in range(1, len(close)):
        if np.isnan(a[i]):
            continue
        if s == 1 and (btc_state[i] != 1 or close[i] < stop):
            s = 0
        elif s == -1 and (btc_state[i] != -1 or close[i] > stop):
            s = 0
        if s == 0:
            if trigger_long[i]:
                s, stop = 1, close[i] - m * a[i]
            elif trigger_short[i]:
                s, stop = -1, close[i] + m * a[i]
        pos[i] = s
    return pos


def build_positions(rule, dfs, tf, n_days, liquid):
    bpd = st.BPD[tf]
    btc = dfs[BTC]
    btc_daily = st.load("1d")[BTC]
    out = {}
    if rule in ("R1", "R2", "R3"):
        bstate = se.signal(btc, n_days * bpd, 2.0, "fixed", 3.0).reindex(next(iter(dfs.values())).index.union(btc.index)).ffill()
    for k, d in dfs.items():
        if k == BTC:
            continue
        if rule == "R0":
            p = se.signal(d, 20 * bpd, 2.0, "fixed", 3.0).clip(lower=0)
        elif rule == "R1":
            p = se.signal(d, 20 * bpd, 2.0, "fixed", 3.0).clip(lower=0) * btc_filter_bars(btc_daily, d.index)
        elif rule == "R2":
            b = bstate.reindex(d.index).ffill().fillna(0.0)
            p = se.signal(d, n_days * bpd, 2.0, "fixed", 3.0).clip(lower=0) * (b == 1)
        elif rule == "R3":
            b = bstate.reindex(d.index).ffill().fillna(0.0)
            flip_l = ((b == 1) & (b.shift(1) != 1)).to_numpy()
            flip_s = ((b == -1) & (b.shift(1) != -1)).to_numpy()
            a = st.atr(d, n_days * bpd).to_numpy()
            p = pd.Series(follow_machine(d["Close"].to_numpy(), a, flip_l, flip_s, b.to_numpy(), 3.0), index=d.index)
        elif rule == "R4":
            r5 = btc["Close"].pct_change(5 * bpd).reindex(d.index).ffill()
            p = pd.Series(np.where(r5 > 0.08, 1.0, np.where(r5 < -0.08, -1.0, 0.0)), index=d.index)
        out[k] = p * liquid[k].reindex(d.index).fillna(False).astype(float)
    return out


def lead_lag(dfs, tf, w_bars, lo, hi, n=200, seed=0):
    """Pooled OLS coefficient of BTC's past-w return on the alt's next-w return (controlling for the alt's own past-w), and its shift p-value."""
    btc = dfs[BTC]["Close"]
    bp = btc.pct_change(w_bars)
    cols = {}
    for k, d in dfs.items():
        if k == BTC:
            continue
        c = d["Close"]
        cols[k] = pd.DataFrame({"fut": c.shift(-w_bars) / c - 1, "own": c.pct_change(w_bars)})
    idx = bp.loc[lo:hi].index[::w_bars]  # non-overlapping
    X_own, Y, Bp = [], [], []
    for k, df in cols.items():
        j = df.reindex(idx).dropna()
        X_own.append(j["own"].to_numpy()); Y.append(j["fut"].to_numpy()); Bp.append(bp.reindex(j.index).to_numpy())
    if not Y:
        return np.nan, np.nan, 0

    def coef(bser):
        x1 = np.concatenate(X_own); y = np.concatenate(Y); x2 = np.concatenate(bser)
        ok = ~np.isnan(x1 + y + x2)
        A = np.column_stack([np.ones(ok.sum()), x1[ok], x2[ok]])
        return np.linalg.lstsq(A, y[ok], rcond=None)[0][2]

    real = coef(Bp)
    rng = np.random.default_rng(seed)
    null = []
    for s in rng.integers(5, max(6, len(idx) - 5), size=n):
        null.append(coef([np.roll(b, int(s)) for b in Bp]))
    null = np.array(null)
    p = float((np.abs(null) >= abs(real)).mean())
    return float(real), p, int(sum(len(y) for y in Y))


def run(split: str):
    lo, hi = st.SPLITS[split]
    root = Path(__file__).resolve().parent / "results"
    rows, ll = [], []
    for tf in ("1d", "4h", "1h"):
        dfs = st.load(tf)
        bpd, bpy = st.BPD[tf], 365.25 * st.BPD[tf]
        liquid = st.liquid_mask(dfs, tf, 20)
        alts = [k for k in dfs if k != BTC]
        ew = st.portfolio({k: dfs[k]["Close"].pct_change().where(liquid[k].shift(1).fillna(False)) for k in alts})
        bh = st.stats(ew.loc[lo:hi], bpy)
        print(f"[{split}] {tf}: {len(alts)} alts; liquid-set buy&hold CAGR {bh['CAGR%']:.1f}% maxDD {bh['maxDD%']:.1f}%", flush=True)
        for w in {"1d": (1, 5), "4h": (1, 6), "1h": (4, 24)}[tf]:
            coef, p, nobs = lead_lag(dfs, tf, w, lo, hi)
            ll.append({"tf": tf, "w_bars": w, "coef_btc": coef, "shift_p": p, "n": nobs})
            print(f"   lead-lag {tf} w={w} bars: BTC coef {coef:.3f}  p {p:.2f}  n {nobs}", flush=True)
        for rule, ns in (("R0", (20,)), ("R1", (20,)), ("R2", (10, 20)), ("R3", (10, 20)), ("R4", (5,))):
            for n_days in ns:
                poss = build_positions(rule, dfs, tf, n_days, liquid)
                for leg, sel in (("both", lambda p: p), ("long", lambda p: p.clip(lower=0)), ("short", lambda p: p.clip(upper=0))):
                    pp = {k: sel(p) for k, p in poss.items()}
                    rets = {k: st.coin_returns(dfs[k], pp[k]).where(liquid[k].shift(1).fillna(False)) for k in pp}
                    port = st.portfolio(rets)
                    m = st.stats(port.loc[lo:hi], bpy)
                    p = st.shift_p({k: dfs[k] for k in pp}, pp, lo, hi, bpy) if leg != "short" and rule != "R0" or (rule == "R0" and leg == "long") else np.nan
                    tr = np.mean([pp[k].loc[lo:hi].diff().abs().sum() / 2 / max(1, len(pp[k].loc[lo:hi]) / bpy) for k in pp])
                    rows.append({"tf": tf, "rule": rule, "n": n_days, "leg": leg, **m, "shift_p": p, "trades/yr": tr,
                                 "EWbh_CAGR%": bh["CAGR%"], "EWbh_maxDD%": bh["maxDD%"]})
        print(pd.DataFrame(rows).query("tf == @tf and leg != 'short'").round(2).to_string(index=False), flush=True)
    pd.DataFrame(rows).to_csv(root / f"round6_{split}.csv", index=False)
    pd.DataFrame(ll).to_csv(root / f"round6_{split}_leadlag.csv", index=False)


if __name__ == "__main__":
    run(sys.argv[1])
