"""Trend ideas. Each returns (long_mask, short_mask) as wide boolean frames known at the daily close."""

from __future__ import annotations

import pandas as pd


def _bcast(s: pd.Series, like: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({col: s for col in like.columns}, index=like.index).fillna(False).astype(bool)


def ema(x, n):
    return x.ewm(span=n, adjust=False, min_periods=n).mean()


# ── regime: BTC or market-wide state, same for every coin ─────────────────────

def btc_above_ema(d, n):
    b = d["close"]["BTCUSDT"]
    e = ema(b, n)
    return _bcast(b > e, d["close"]), _bcast(b < e, d["close"])


def btc_ret(d, n, thr=0.0):
    b = d["close"]["BTCUSDT"]
    r = b / b.shift(n) - 1
    return _bcast(r > thr, d["close"]), _bcast(r < thr, d["close"])


def btc_ema_cross(d, fast, slow):
    b = d["close"]["BTCUSDT"]
    up = ema(b, fast) > ema(b, slow)
    return _bcast(up, d["close"]), _bcast(~up & ema(b, slow).notna(), d["close"])


def btc_bot_filter(d):
    """Live-bot BTC filter for longs; its mirror (below EMA240 and 20d return < 0) for shorts."""
    b = d["close"]["BTCUSDT"]
    e, r = ema(b, 240), b / b.shift(20) - 1
    return _bcast((b > e) & (r >= -0.03), d["close"]), _bcast((b < e) & (r < 0), d["close"])


def breadth(d, n, thr=0.5):
    """Share of today's universe trading above its own EMA(n)."""
    c = d["close"]
    above = (c > ema(c, n)).astype(float).where(d["universe"])
    share = above.sum(axis=1) / d["universe"].sum(axis=1).replace(0, float("nan"))
    return _bcast(share > thr, c), _bcast(share < 1 - thr, c)


# ── setup: the coin's own trend ───────────────────────────────────────────────

def coin_above_ema(d, n):
    c = d["close"]
    e = ema(c, n)
    return c > e, c < e


def coin_ret(d, n):
    c = d["close"]
    r = c / c.shift(n) - 1
    return r > 0, r < 0


def coin_donchian_pos(d, n, thr=0.5):
    """Close in the upper / lower part of its n-day range."""
    c = d["close"]
    hi, lo = c.rolling(n).max(), c.rolling(n).min()
    pos = (c - lo) / (hi - lo)
    return pos > thr, pos < 1 - thr


def coin_ema_cross(d, fast, slow):
    c = d["close"]
    ef, es = ema(c, fast), ema(c, slow)
    return ef > es, (ef < es) & es.notna()


def coin_rel_btc(d, n):
    """Coin beat / lagged BTC over n days."""
    c = d["close"]
    r = c / c.shift(n) - 1
    rb = r["BTCUSDT"]
    return r.sub(rb, axis=0) > 0, r.sub(rb, axis=0) < 0


REGIME = {
    **{f"btc_above_ema{n}": (btc_above_ema, {"n": n}) for n in (50, 100, 200, 240)},
    **{f"btc_ret{n}": (btc_ret, {"n": n}) for n in (20, 60, 120)},
    "btc_ret20_-3%": (btc_ret, {"n": 20, "thr": -0.03}),
    "btc_ema50_200_cross": (btc_ema_cross, {"fast": 50, "slow": 200}),
    "btc_bot_filter": (btc_bot_filter, {}),
    **{f"breadth_ema{n}": (breadth, {"n": n}) for n in (50, 100)},
}

SETUP = {
    **{f"coin_above_ema{n}": (coin_above_ema, {"n": n}) for n in (20, 50, 100, 200)},
    **{f"coin_ret{n}": (coin_ret, {"n": n}) for n in (20, 60, 120)},
    **{f"coin_donchian{n}": (coin_donchian_pos, {"n": n}) for n in (20, 55)},
    "coin_ema20_100_cross": (coin_ema_cross, {"fast": 20, "slow": 100}),
    **{f"coin_rel_btc{n}": (coin_rel_btc, {"n": n}) for n in (30, 90)},
}
