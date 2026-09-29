"""Round 8: historic price-level breaks with volume conviction (see PLAN.md, Round 8).

usage: python levels.py train|valid|test
"""

from __future__ import annotations

import sys
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
import bot_coins as bc  # noqa: E402

COST = 0.0015
N_SHIFTS = 200
LEVELS = ("L90", "L180", "L365", "LP")
CONV = ("none", "V", "VC")


def atr14(h, l, c):
    pc = c.shift(1)
    tr = pd.concat([h - l, (h - pc).abs(), (l - pc).abs()], axis=1).max(axis=1)
    return tr.rolling(14).mean()


def _tested(vals: np.ndarray, tol: float, top: bool) -> float:
    """Most extreme value (highest if top else lowest) that has another value within tol."""
    if len(vals) < 2:
        return np.nan
    v = np.sort(vals)[::-1] if top else np.sort(vals)
    close = np.abs(v[:, None] / v[None, :] - 1) <= tol
    ok = close.sum(axis=1) >= 2
    return v[np.argmax(ok)] if ok.any() else np.nan


def pivot_levels(h: pd.Series, l: pd.Series, k=5, tol=0.015, look=365):
    """Per day: tested resistance (highest pivot high in the last `look` days with another pivot high within tol) and tested support."""
    hv, lv = h.to_numpy(), l.to_numpy()
    n = len(hv)
    res, sup = np.full(n, np.nan), np.full(n, np.nan)
    ph, pl = [], []  # (pivot_index, value), confirmed k days later
    for t in range(2 * k, n):
        c = t - k
        if hv[c] == np.nanmax(hv[c - k:t + 1]):
            ph.append((c, hv[c]))
        if lv[c] == np.nanmin(lv[c - k:t + 1]):
            pl.append((c, lv[c]))
        ph = [x for x in ph if t - x[0] <= look]
        pl = [x for x in pl if t - x[0] <= look]
        res[t] = _tested(np.array([v for _, v in ph]), tol, True)
        sup[t] = _tested(np.array([v for _, v in pl]), tol, False)
    return pd.Series(res, index=h.index), pd.Series(sup, index=h.index)


def machine(c, a, up_lvl, dn_lvl, conv_long, conv_short, mode_long=True, mode_short=True):
    n = len(c)
    pos = np.zeros(n)
    s, lvl, ext = 0, 0.0, 0.0
    armed_l = armed_s = True
    events = []
    for i in range(1, n):
        if np.isnan(a[i]):
            continue
        if not np.isnan(up_lvl[i]) and c[i] <= up_lvl[i]:
            armed_l = True
        if not np.isnan(dn_lvl[i]) and c[i] >= dn_lvl[i]:
            armed_s = True
        if s == 1:
            ext = max(ext, c[i])
            if c[i] < lvl or c[i] < ext - 3 * a[i]:
                s = 0
        elif s == -1:
            ext = min(ext, c[i])
            if c[i] > lvl or c[i] > ext + 3 * a[i]:
                s = 0
        if s == 0:
            if mode_long and armed_l and not np.isnan(up_lvl[i]) and c[i] > up_lvl[i]:
                events.append((i, 1, conv_long[i]))
                if conv_long[i]:
                    s, lvl, ext, armed_l = 1, up_lvl[i], c[i], False
                else:
                    armed_l = False
            elif mode_short and armed_s and not np.isnan(dn_lvl[i]) and c[i] < dn_lvl[i]:
                events.append((i, -1, conv_short[i]))
                if conv_short[i]:
                    s, lvl, ext, armed_s = -1, dn_lvl[i], c[i], False
                else:
                    armed_s = False
        pos[i] = s
    return pos, events


def build(D, level, conv):
    """Positions and (date, side, confirmed) events per coin. Volume conviction gates entries; events without conviction are logged as unconfirmed."""
    close, high, low, dvol = D["close"], D["high"], D["low"], D["dvol"]
    pos, ev = {}, {}
    for k in D["R"].columns:
        c, h, l, v = close[k].dropna(), high[k].reindex(close[k].dropna().index), low[k].reindex(close[k].dropna().index), dvol[k].reindex(close[k].dropna().index)
        if len(c) < 200:
            continue
        a = atr14(h, l, c).to_numpy()
        if level == "LP":
            up, dn = pivot_levels(h, l)
        else:
            n = int(level[1:])
            up, dn = h.rolling(n).max().shift(1), l.rolling(n).min().shift(1)
        volok = (v >= 2 * v.rolling(20).median().shift(1)).to_numpy()
        loc = ((c - l) / (h - l).replace(0, np.nan))
        cl, cs = (volok & (loc >= 0.75).to_numpy()), (volok & (loc <= 0.25).to_numpy())
        ones = np.ones(len(c), dtype=bool)
        cvl, cvs = {"none": (ones, ones), "V": (volok, volok), "VC": (cl, cs)}[conv]
        p, e = machine(c.to_numpy(), a, up.to_numpy(), dn.to_numpy(), cvl, cvs)
        pos[k] = pd.Series(p, index=c.index)
        # event study needs both confirmed and unconfirmed events under the plain (no conviction) rule
        ev[k] = (c, e, volok, cl, cs)
    return pos, ev


def portfolio_arrays(D, pos, btc_filter: bool, side: str):
    idx = D["close"].index
    cols = list(pos)
    P = pd.DataFrame(pos).reindex(index=idx, columns=cols).fillna(0.0)
    if side == "long":
        P = P.clip(lower=0)
    elif side == "short":
        P = P.clip(upper=0)
    if btc_filter:
        ok = (D["close"]["BTCUSDT"].pct_change(20).shift(1) >= -0.03).astype(float)
        P = P.clip(lower=0).mul(ok, axis=0) + P.clip(upper=0).mul(1 - ok, axis=0)
    elig = D["elig"].reindex(columns=cols).fillna(False)
    R = D["close"].reindex(columns=cols).pct_change().fillna(0.0)
    return P, elig, R


def sim(P: np.ndarray, E: np.ndarray, R: np.ndarray, cost=COST):
    P = P * E
    held = np.vstack([np.zeros((1, P.shape[1])), P[:-1]])
    turn = np.abs(np.diff(held, axis=0, prepend=held[:1]))
    n = np.maximum(E.sum(axis=1), 1)
    return ((held * R - cost * turn).sum(axis=1)) / n


def stats(r: pd.Series) -> dict:
    return bc.metrics(r)


def shift_p(P, E, R, lo_i, hi_i, n=N_SHIFTS, seed=0):
    Pw, Ew, Rw = P[lo_i:hi_i], E[lo_i:hi_i], R[lo_i:hi_i]

    def sharpe(p):
        r = sim(p, Ew, Rw)
        return r.mean() / r.std() if r.std() > 0 else -np.inf

    real = sharpe(Pw)
    rng = np.random.default_rng(seed)
    null = [sharpe(np.roll(Pw, int(s), axis=0)) for s in rng.integers(len(Pw) // 20, len(Pw) - len(Pw) // 20, size=n)]
    return float((np.array(null) >= real).mean())


def event_study(ev, D, lo, hi, h=10):
    """Mean net forward return per event (long: +, short: -), volume-confirmed vs plain, monthly-clustered."""
    rows = []
    for k, (c, events, volok, cl, cs) in ev.items():
        fwd = c.shift(-h) / c - 1
        for i, side, _ in events:
            d = c.index[i]
            if not (lo <= d <= hi) or np.isnan(fwd.iloc[i]) or not D["elig"].loc[d].get(k, False):
                continue
            r = side * fwd.iloc[i] - 0.003
            rows.append({"date": d, "coin": k, "side": side, "vol": bool(volok[i]), "vc": bool(cl[i] if side == 1 else cs[i]), "ret": r})
    df = pd.DataFrame(rows)
    out = {}
    if df.empty:
        return out
    for name, sel in (("plain", df), ("V", df[df.vol]), ("VC", df[df.vc]), ("noV", df[~df.vol])):
        for sd, ss in (("long", sel[sel.side == 1]), ("short", sel[sel.side == -1])):
            if len(ss) < 5:
                continue
            m = ss.groupby(ss.date.dt.to_period("M")).ret.mean()
            t = m.mean() / (m.std() / np.sqrt(len(m))) if len(m) > 2 and m.std() > 0 else np.nan
            out[(name, sd)] = (len(ss), 100 * ss.ret.mean(), t)
    return out


PROMOTED = {("L180", "V"), ("L180", "VC"), ("L365", "V"), ("L365", "VC")}


def run(split: str, promoted_only: bool = False):
    D = bc.load()
    lo, hi = bc.SPLITS[split]
    idx = D["close"].index
    lo_i, hi_i = idx.searchsorted(lo), idx.searchsorted(min(hi, idx[-1]), side="right")
    btc = D["close"]["BTCUSDT"].pct_change().fillna(0.0)
    ewbh = (D["close"].pct_change().where(D["elig"].shift(1).fillna(False))).mean(axis=1).fillna(0.0)
    print(f"[{split}] BTC buy&hold {({k: round(v, 1) for k, v in stats(btc.iloc[lo_i:hi_i]).items()})}\n"
          f"        EW top30 buy&hold {({k: round(v, 1) for k, v in stats(ewbh.iloc[lo_i:hi_i]).items()})}", flush=True)
    rows, evrows = [], []
    for level in LEVELS:
        for conv in CONV:
            if promoted_only and (level, conv) not in PROMOTED and conv != "none":
                continue
            if promoted_only and level not in ("L180", "L365"):
                continue
            pos, ev = build(D, level, conv)
            if conv == "none":
                es = event_study(ev, D, lo, hi)
                for (grp, sd), (n, m, t) in es.items():
                    evrows.append({"level": level, "group": grp, "side": sd, "events": n, "mean10d%_net": m, "t_monthly": t})
            for filt in (False, True):
                for side in (("long",) if promoted_only else ("both", "long", "short")):
                    P, E, R = portfolio_arrays(D, pos, filt, side)
                    r = pd.Series(sim(P.to_numpy(), E.to_numpy().astype(float), R.to_numpy()), index=idx)
                    m = stats(r.iloc[lo_i:hi_i])
                    p = shift_p(P.to_numpy(), E.to_numpy().astype(float), R.to_numpy(), lo_i, hi_i) if side != "short" and m else np.nan
                    tr = float(np.mean([(P[k].iloc[lo_i:hi_i].diff().abs().sum() / 2) / max(1, (hi_i - lo_i) / 365.25) for k in P.columns]))
                    rows.append({"level": level, "conv": conv, "btc_filter": filt, "side": side, **m, "shift_p": p, "trades/yr/coin": tr})
        print(f"{level} done", flush=True)
    out = pd.DataFrame(rows)
    tag = "_promoted" if promoted_only else ""
    out.to_csv(bc.RES / f"round8_{split}{tag}.csv", index=False)
    pd.DataFrame(evrows).to_csv(bc.RES / f"round8_{split}{tag}_events.csv", index=False)
    print(pd.DataFrame(evrows).round(2).to_string(index=False))
    print(out[out.side == ("long" if promoted_only else "both")].round(2).to_string(index=False))


if __name__ == "__main__":
    run(sys.argv[1], len(sys.argv) > 2 and sys.argv[2] == "promoted")
