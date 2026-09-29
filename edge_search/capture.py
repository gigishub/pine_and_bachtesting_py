"""Up/down capture vs BTC buy-and-hold in non-overlapping 30-day blocks (train and validation only)."""

from __future__ import annotations

import warnings

import pandas as pd

from engine import SPLITS, build_market, buy_and_hold, run
from ideas import IDEAS

warnings.filterwarnings("ignore", category=FutureWarning)
BLOCK = 30

mkt = build_market()
btc = buy_and_hold(mkt)
rets = {n: run(mkt, f(mkt, 1.0)) for n, f in IDEAS.items()}


def blocks(r: pd.Series, lo, hi) -> pd.Series:
    r = r.loc[lo:hi]
    return (1 + r).groupby(pd.Series(range(len(r)), index=r.index) // BLOCK).prod() - 1


for split in ("train", "valid"):
    lo, hi = SPLITS[split]
    b = blocks(btc, lo, hi)
    up, down = b > 0, b <= 0
    print(f"\n[{split}] {len(b)} blocks: {up.sum()} BTC-up (avg {100 * b[up].mean():.1f}%), "
          f"{down.sum()} BTC-down (avg {100 * b[down].mean():.1f}%)")
    rows = []
    for n, r in rets.items():
        s = blocks(r, lo, hi)
        rows.append({"idea": n,
                     "up_capture%": 100 * s[up].mean() / b[up].mean(),
                     "down_capture%": 100 * s[down].mean() / b[down].mean(),
                     "avg_down_block%": 100 * s[down].mean(),
                     "worst_block%": 100 * s.min(),
                     "btc_worst_block%": 100 * b.min(),
                     "down_blocks_positive%": 100 * (s[down] > 0).mean()})
    with pd.option_context("display.float_format", "{:.1f}".format, "display.width", 200):
        print(pd.DataFrame(rows).set_index("idea"))
