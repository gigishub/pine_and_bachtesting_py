"""BTC: slow trend filter (EMA length or none) with and without the fast BTC 20-day return filter."""

from __future__ import annotations

import logging

import pandas as pd

from bot_baseline import LIVE_PARAMS, bot_position
from common import TEST_START, available_symbols, load, metrics

logging.disable(logging.CRITICAL)

PERIODS = [("train", None, TEST_START - pd.Timedelta(seconds=1)), ("test", TEST_START, None)]
TRENDS = [240, 150, 100, None]
COLS = ["trades", "win%", "PF", "CAGR%", "maxDD%", "expo%"]


def run(df: pd.DataFrame, btc_close: pd.Series) -> dict[str, pd.Series]:
    ok = ((btc_close / btc_close.shift(20) - 1).shift(1) >= -0.03).reindex(df.index)
    out = {}
    for t in TRENDS:
        p = {**LIVE_PARAMS, "ema_trend_length": t}
        name = f"ema{t}" if t else "no_trend"
        out[f"{name}"] = bot_position(df, p)
        out[f"{name}+ret20"] = bot_position(df, p, entry_ok=ok)
    return out


if __name__ == "__main__":
    btc = load("BTCUSDT", "1d")
    rows = []
    for sym in available_symbols("1d"):
        df = load(sym, "1d")
        for name, pos in run(df, btc["close"]).items():
            for per, a, b in PERIODS:
                m = metrics(df, pos, a, b)
                if m:
                    rows.append({"symbol": sym, "variant": name, "period": per, **m})
    r = pd.DataFrame(rows)
    with pd.option_context("display.float_format", "{:.2f}".format, "display.width", 200):
        print("=== BTC ===")
        print(r[r.symbol == "BTCUSDT"].set_index(["period", "variant"])[COLS].sort_index())
        print(f"\n=== Sanity check: median over all {r.symbol.nunique()} coins ===")
        print(r.groupby(["period", "variant"])[COLS].median())
