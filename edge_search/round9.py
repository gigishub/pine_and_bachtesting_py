"""Round 9: literature ideas U-Y. usage: python round9.py train|valid|test [U V ...]"""
from __future__ import annotations
import sys, warnings
import numpy as np, pandas as pd
warnings.filterwarnings("ignore")
from engine import SPLITS, build_market, buy_and_hold, metrics, passes_win_condition, run, shift_pvalue, Market
from ideas import _weekly, _top, _n


def idea_u(m: Market, k=1.0):
    b = m.close[m.btc]
    frac = 0
    lbs = [5, 10, 20, 30, 60, 90, 150, 250, 360]
    sig = pd.DataFrame(index=b.index)
    for n in lbs:
        n = _n(n, k)
        up = b > b.shift(1).rolling(n).max()
        dn = b < b.shift(1).rolling(n).min()
        s = pd.Series(np.nan, index=b.index)
        s[up] = 1.0; s[dn] = 0.0
        sig[n] = s.ffill().fillna(0.0)
    f = sig.mean(axis=1)
    rv = b.pct_change().rolling(30).std() * np.sqrt(365)
    w = (f * (0.25 / rv)).clip(upper=1.0).fillna(0.0)
    out = pd.DataFrame(0.0, index=m.close.index, columns=m.close.columns)
    out[m.btc] = w
    return out


def _ls(score: pd.DataFrame, m: Market, n=3):
    long = _top(score, m, n, ascending=False)
    short = _top(score, m, n, ascending=True)
    return (long - short) / n


def idea_v(m: Market, k=1.0):
    mx = m.close.pct_change().rolling(_n(30, k)).max()
    return _weekly(_ls(-mx, m))


def idea_w(m: Market, k=1.0):
    r = m.close.pct_change(_n(7, k))
    return _weekly(_ls(-r, m))


def idea_x(m: Market, k=1.0):
    r = m.close.pct_change()
    dow = pd.Series(r.index.dayofweek, index=r.index)
    n = _n(8, k)
    score = pd.DataFrame(np.nan, index=r.index, columns=r.columns)
    for d in range(7):
        rd = r[dow == d]
        hist = rd.shift(1).rolling(n).mean()  # past same weekdays, known before that day
        # score decided on close of day t-1 for day t (weekday d): use hist at the next occurrence
        score.loc[rd.index] = hist
    nxt = score.shift(-1)  # row t holds score for day t+1
    return _ls(nxt.where(m.universe), m)


def idea_y(m: Market, k=1.0):
    e, b = "ETHUSDT", m.btc
    lr = np.log(m.close[e] / m.close[b])
    n = _n(60, k)
    z = (lr - lr.rolling(n).mean()) / lr.rolling(n).std()
    pos = np.zeros(len(z)); cur = 0
    for i, v in enumerate(z.to_numpy()):
        if np.isnan(v): pos[i] = 0; continue
        if cur == 0:
            cur = -1 if v > 2 else (1 if v < -2 else 0)
        elif (cur == -1 and v <= 0) or (cur == 1 and v >= 0):
            cur = 0
        pos[i] = cur
    out = pd.DataFrame(0.0, index=m.close.index, columns=m.close.columns)
    out[e] = 0.5 * pos; out[b] = -0.5 * pos
    return out


IDEAS = {"U": idea_u, "V": idea_v, "W": idea_w, "X": idea_x, "Y": idea_y}
if __name__ == "__main__":
    split = sys.argv[1]; names = sys.argv[2:] or list(IDEAS)
    lo, hi = SPLITS[split]; mkt = build_market()
    bh = metrics(buy_and_hold(mkt), lo, hi)
    print(f"[{split}] BTC B&H CAGR {bh['CAGR%']:.1f} maxDD {bh['maxDD%']:.1f}")
    rows = []
    for nm in names:
        w = IDEAS[nm](mkt, 1.0); m = metrics(run(mkt, w), lo, hi)
        var = [metrics(run(mkt, IDEAS[nm](mkt, k)), lo, hi).get("CAGR%", np.nan) for k in (0.5, 2.0)]
        p = shift_pvalue(mkt, w, (lo, hi)); a, b = passes_win_condition(m, bh)
        rows.append({"idea": nm, **m, "k.5": var[0], "k2": var[1], "shift_p": p, "win_a": a, "win_b": b})
    with pd.option_context("display.float_format", "{:.2f}".format, "display.width", 200):
        print(pd.DataFrame(rows).set_index("idea"))
