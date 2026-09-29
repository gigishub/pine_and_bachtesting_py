"""The 10 pre-declared ideas. Each returns target weights (decided on the day's close).

k scales every lookback (1 = declared value; 0.5 and 2 are the robustness variants).
B, E, H, J rebalance weekly (Monday); the rest follow their signal daily.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from engine import Market

TARGET_VOL = 0.30
SLOTS = 10


def _n(x: int, k: float) -> int:
    return max(2, int(round(x * k)))


def _btc_filter(m: Market, k: float) -> pd.Series:
    b = m.close[m.btc]
    return ((b > b.rolling(_n(200, k)).mean()) & (b.pct_change(_n(20, k)) > -0.03)).astype(float)


def _weekly(w: pd.DataFrame) -> pd.DataFrame:
    monday = pd.Series(w.index.dayofweek == 0, index=w.index)
    return w.where(monday, axis=0).ffill().fillna(0.0)


def _top(score: pd.DataFrame, m: Market, n: int, ascending: bool = False) -> pd.DataFrame:
    s = score.where(m.universe)
    rank = s.rank(axis=1, ascending=ascending, method="first")
    return ((rank <= n) & s.notna()).astype(float)


def _vol_target(w: pd.DataFrame, m: Market, k: float) -> pd.DataFrame:
    """Scale weights down (never up) so trailing 30d realised portfolio vol stays at the target."""
    rc = m.close.pct_change()
    port = (w.shift(1).reindex_like(rc).fillna(0) * rc).sum(axis=1)
    vol = port.rolling(_n(30, k)).std() * np.sqrt(365.25)
    scale = (TARGET_VOL / vol).clip(upper=1.0).fillna(0.0)
    return w.mul(scale, axis=0)


def idea_a(m: Market, k: float = 1.0) -> pd.DataFrame:
    w = pd.DataFrame(0.0, index=m.close.index, columns=m.close.columns)
    w[m.btc] = _btc_filter(m, k)
    return w


def idea_b(m: Market, k: float = 1.0) -> pd.DataFrame:
    top = _top(m.close.pct_change(_n(60, k)), m, 3) / 3
    return _weekly(top.mul(_btc_filter(m, k), axis=0))


def idea_c(m: Market, k: float = 1.0) -> pd.DataFrame:
    c = m.close
    mask = m.universe & (c.pct_change(_n(60, k)) > 0) & (c > c.rolling(_n(100, k)).mean())
    return mask.astype(float) / SLOTS


def idea_d(m: Market, k: float = 1.0) -> pd.DataFrame:
    c = m.close
    mask = m.universe & (c.pct_change(_n(60, k)) > 0) & (c > c.rolling(_n(100, k)).mean())
    inv = (1 / c.pct_change().rolling(_n(30, k)).std()).where(mask)
    raw = inv.div(inv.sum(axis=1), axis=0).fillna(0.0)
    return _vol_target(raw, m, k)


def idea_e(m: Market, k: float = 1.0) -> pd.DataFrame:
    vol = m.close.pct_change().rolling(_n(60, k)).std()
    low = _top(vol, m, 3, ascending=True) / 3
    return _weekly(low.mul(_btc_filter(m, k), axis=0))


def _rsi(c: pd.DataFrame, n: int) -> pd.DataFrame:
    d = c.diff()
    up = d.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    return 100 - 100 / (1 + up / dn)


def idea_f(m: Market, k: float = 1.0) -> pd.DataFrame:
    c = m.close
    sig = m.universe & (c > c.rolling(_n(100, k)).mean()) & (_rsi(c, 2) < 10)
    hold = sig.astype(float).rolling(_n(5, k)).max().fillna(0.0)
    return hold / SLOTS


def idea_g(m: Market, k: float = 1.0) -> pd.DataFrame:
    c = m.close
    sma = c.rolling(_n(20, k)).mean()
    sd = c.rolling(_n(20, k)).std()
    upper = sma + 2 * sd
    width = (4 * sd) / sma
    squeeze = width.rolling(_n(120, k)).rank(pct=True) < 0.2
    recent = squeeze.astype(float).rolling(10).max() > 0
    entry = (recent & (c > upper) & m.universe).to_numpy()
    exit_ = (c < sma).to_numpy()
    pos = np.full(entry.shape, np.nan)
    pos[entry] = 1.0
    pos[exit_ & ~entry] = 0.0
    pos = pd.DataFrame(pos, index=c.index, columns=c.columns).ffill().fillna(0.0)
    return pos.div(pos.sum(axis=1).clip(lower=SLOTS), axis=0)


def idea_h(m: Market, k: float = 1.0) -> pd.DataFrame:
    score = m.close.pct_change(_n(60, k))
    long_ = _top(score, m, 3) / 3 * 0.5
    short = _top(score, m, 3, ascending=True) / 3 * 0.5
    return _weekly(long_ - short)


def idea_i(m: Market, k: float = 1.0) -> pd.DataFrame:
    c = m.close
    above = ((c > c.rolling(_n(50, k)).mean()) & m.universe).sum(axis=1)
    breadth_on = (above / m.universe.sum(axis=1).clip(lower=1) > 0.5).astype(float)
    return (m.universe.astype(float) / SLOTS).mul(breadth_on, axis=0)


def idea_j(m: Market, k: float = 1.0) -> pd.DataFrame:
    ew = _weekly(m.universe.astype(float) / SLOTS)
    ew = ew.mul(_btc_filter(m, k), axis=0)
    return _vol_target(ew, m, k)


IDEAS = {"A": idea_a, "B": idea_b, "C": idea_c, "D": idea_d, "E": idea_e,
         "F": idea_f, "G": idea_g, "H": idea_h, "I": idea_i, "J": idea_j}
