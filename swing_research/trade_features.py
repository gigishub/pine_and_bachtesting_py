"""Per-trade table for the live bot with features known at entry, pooled over all coins."""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

from bot_baseline import bot_position
from common import TEST_START, available_symbols, load, trades_from_position

logging.disable(logging.CRITICAL)


def indicator_frame(df: pd.DataFrame) -> pd.DataFrame:
    """Features computed on closed bars; row t uses data up to the close of t."""
    c = df["close"]
    tr = pd.concat([df["high"] - df["low"], (df["high"] - c.shift()).abs(), (df["low"] - c.shift()).abs()], axis=1).max(axis=1)
    atr14 = tr.rolling(14).mean()
    ema240 = c.ewm(span=240, adjust=False).mean()
    above = c > ema240
    streak = above.groupby((above != above.shift()).cumsum()).cumcount() + 1
    stop = df["low"].rolling(7).max() - tr.rolling(5).mean()
    return pd.DataFrame({
        "dist_ema240": c / ema240 - 1,
        "ema240_slope20": ema240 / ema240.shift(20) - 1,
        "trend_age": streak.where(above, 0),
        "atr_pct": atr14 / c,
        "ret_5": c / c.shift(5) - 1,
        "ret_20": c / c.shift(20) - 1,
        "ret_60": c / c.shift(60) - 1,
        "vol_ratio": df["volume"] / df["volume"].rolling(20).mean(),
        "stop_dist": (c - stop) / c,
        "range_pos20": (c - df["low"].rolling(20).min()) / (df["high"].rolling(20).max() - df["low"].rolling(20).min()),
    })


def build_trades(tf: str = "1d") -> pd.DataFrame:
    btc = indicator_frame(load("BTCUSDT", tf))
    rows = []
    for sym in available_symbols(tf):
        df = load(sym, tf)
        feats = indicator_frame(df).shift(1)  # known at the close before the entry bar
        feats["btc_dist_ema240"] = btc["dist_ema240"].shift(1).reindex(df.index)
        feats["btc_ret_20"] = btc["ret_20"].shift(1).reindex(df.index)
        tr = trades_from_position(df, bot_position(df))
        tr = tr.join(feats, on="entry")
        tr["symbol"] = sym
        rows.append(tr)
    out = pd.concat(rows, ignore_index=True)
    out["period"] = np.where(out["entry"] >= TEST_START, "test", "train")
    return out


def bucket_table(trades: pd.DataFrame, feature: str, q: int = 4) -> pd.DataFrame:
    """Win rate, mean and total return per quantile of a feature (edges from train only)."""
    train = trades[trades.period == "train"]
    edges = np.unique(np.nanquantile(train[feature], np.linspace(0, 1, q + 1)))
    edges[0], edges[-1] = -np.inf, np.inf
    b = pd.cut(trades[feature], edges)
    g = trades.groupby([trades.period, b], observed=True)["ret"]
    return pd.DataFrame({"n": g.size(), "win%": 100 * g.apply(lambda r: (r > 0).mean()),
                         "avg%": 100 * g.mean(), "sum%": 100 * g.sum()})


if __name__ == "__main__":
    t = build_trades()
    print(f"{len(t)} trades, {t.symbol.nunique()} coins; train {sum(t.period == 'train')}, test {sum(t.period == 'test')}")
    feats = [c for c in t.columns if c not in ("entry", "exit", "ret", "bars", "symbol", "period")]
    with pd.option_context("display.float_format", "{:.2f}".format, "display.width", 200):
        for f in feats:
            print(f"\n--- {f} ---")
            print(bucket_table(t, f).unstack(0).swaplevel(axis=1).sort_index(axis=1)[["train", "test"]])
