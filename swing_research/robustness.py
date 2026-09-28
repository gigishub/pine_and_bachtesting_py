"""Check whether the BTC-trend entry filter works across nearby settings, not just one."""

from __future__ import annotations

import logging

import pandas as pd

from bot_baseline import bot_position
from common import TEST_START, available_symbols, load, metrics

logging.disable(logging.CRITICAL)

LOOKBACKS = [10, 20, 30, 60]
THRESHOLDS = [-0.06, -0.03, 0.0, 0.03]
PERIODS = [("train", None, TEST_START - pd.Timedelta(seconds=1)), ("test", TEST_START, None)]


if __name__ == "__main__":
    btc = load("BTCUSDT", "1d")["close"]
    syms = available_symbols("1d")
    data = {s: load(s, "1d") for s in syms}
    live = {s: bot_position(df) for s, df in data.items()}
    base = {(s, p): metrics(df, live[s], a, b).get("CAGR%") for s, df in data.items() for p, a, b in PERIODS}

    rows = []
    for lb in LOOKBACKS:
        btc_ret = (btc / btc.shift(lb) - 1).shift(1)
        for th in THRESHOLDS:
            for s, df in data.items():
                pos = bot_position(df, entry_ok=btc_ret.reindex(df.index) >= th)
                for p, a, b in PERIODS:
                    m = metrics(df, pos, a, b)
                    if not m or base[(s, p)] is None:
                        continue
                    rows.append({"lookback": lb, "threshold": th, "period": p, "symbol": s,
                                 "dCAGR": m["CAGR%"] - base[(s, p)], "maxDD%": m["maxDD%"]})
    r = pd.DataFrame(rows)
    print(f"{len(syms)} coins. dCAGR = change in yearly return vs live bot, in % points.\n")
    for p in ["train", "test"]:
        g = r[r.period == p].groupby(["lookback", "threshold"])
        print(f"=== {p}: median dCAGR over coins ===")
        print(g["dCAGR"].median().unstack().round(1))
        print(f"=== {p}: coins improved (of {len(syms)}) ===")
        print(g["dCAGR"].apply(lambda x: (x > 0).sum()).unstack())
        print()
