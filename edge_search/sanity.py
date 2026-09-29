"""M1 sanity checks: the engine must find nothing in noise and something when it peeks."""

from __future__ import annotations

import numpy as np
import pandas as pd

from engine import TRAIN, build_market, buy_and_hold, metrics, run, shift_pvalue

mkt = build_market()
idx = mkt.ret.index

# 1. buy-and-hold BTC matches the raw price move (before the one-off entry cost)
bh = buy_and_hold(mkt)
lo, hi = TRAIN
raw = mkt.open.loc[hi + pd.Timedelta(days=1), "BTCUSDT"] / mkt.open.loc[lo, "BTCUSDT"]
eng = (1 + bh.loc[lo:hi]).prod()
print(f"BTC train: raw price ratio {raw:.3f}, engine {eng:.3f} (engine slightly lower = entry cost)")

# 2. peeking (weights = sign of tomorrow's return, long only) must look great
nxt = mkt.ret.shift(-1)
peek = (nxt > 0).astype(float).where(mkt.universe).fillna(0) / 10
print("peek train:", {k: round(v, 1) for k, v in metrics(run(mkt, peek), *TRAIN).items()})

# 3. random weights: fraction that beat 95% of their own time-shifts should be about 5%
rng = np.random.default_rng(1)
passed = 0
trials = 40
for s in range(trials):
    flags = pd.DataFrame(rng.random(mkt.ret.shape) < 0.3, index=idx, columns=mkt.ret.columns)
    flags = flags.rolling(20).max().fillna(0)  # sticky random positions, like a real signal
    w = (flags.where(mkt.universe).fillna(0) > 0).astype(float)
    w = w.div(w.sum(axis=1).clip(lower=1), axis=0)
    p = shift_pvalue(mkt, w, TRAIN, n=100, seed=s)
    passed += p <= 0.05
print(f"random weights passing p<=0.05: {passed}/{trials} (expect ~2)")
