"""One-at-a-time variants of the live bot's exit/entry settings on all coins, train vs test."""
from __future__ import annotations
import sys, warnings
from dataclasses import replace
from pathlib import Path
import numpy as np, pandas as pd
warnings.filterwarnings("ignore")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "btc_sol_hetzner_momentum_bot"))
from bot import signals
from bot.config import StrategyParams
from common import TEST_START, available_symbols, load, metrics

orig = signals.indicators
BTC = load("BTCUSDT", "1d")["close"]
BTC_OK = (BTC / BTC.shift(20) - 1) >= -0.03   # raw, unshifted like the bot's raw_entry_ok

def pos_for(df, p, btc_filter=True):
    def ind(d, pp):
        o = orig(d, pp)
        if btc_filter:
            o["raw_entry_ok"] = BTC_OK.reindex(o.index).fillna(False).to_numpy()
        return o
    signals.indicators = ind
    try:
        s = signals.compute_state(df, p)
    finally:
        signals.indicators = orig
    return s["in_trade"].astype(float)

BASE = StrategyParams()
VARIANTS = {"base": BASE}
for v in (3, 14, 21): VARIANTS[f"trail_lookback={v}"] = replace(BASE, trail_lookback=v)
for v in (14, 20): VARIANTS[f"atr_sl={v}"] = replace(BASE, atr_length_sl=v)
for v in (1.0, 2.0): VARIANTS[f"caution_mult={v}"] = replace(BASE, caution_atr_mult=v)
for v in (3, 5, 20): VARIANTS[f"ema_fast={v}"] = replace(BASE, ema_is_bullish_length=v)
for v in (100, 150): VARIANTS[f"ema_trend={v}"] = replace(BASE, ema_trend_length=v)
for v in (2.5, 99.0): VARIANTS[f"vol_spike_mult={v}"] = replace(BASE, atr_vol_multiplier=v)

PER = {"train": (None, TEST_START - pd.Timedelta(seconds=1)), "test": (TEST_START, None)}
syms = available_symbols("1d")
data = {s: load(s, "1d") for s in syms}
res = {}
for name, p in VARIANTS.items():
    for s, df in data.items():
        pos = pos_for(df, p)
        for per, (a, b) in PER.items():
            m = metrics(df, pos, a, b)
            if m: res[(name, s, per)] = m
R = pd.DataFrame(res).T
R.index.names = ["variant", "sym", "period"]
rows = []
for name in VARIANTS:
    row = {"variant": name}
    for per in PER:
        x = R.xs(name, level="variant").xs(per, level="period")
        b = R.xs("base", level="variant").xs(per, level="period")
        row[f"{per} medCAGR"] = x["CAGR%"].median()
        row[f"{per} medDD"] = x["maxDD%"].median()
        row[f"{per} better/22"] = int((x["CAGR%"] > b["CAGR%"].reindex(x.index)).sum()) if name != "base" else 0
        row[f"{per} BTC"] = x.loc["BTCUSDT", "CAGR%"]; row[f"{per} SOL"] = x.loc["SOLUSDT", "CAGR%"]
    rows.append(row)
with pd.option_context("display.float_format", "{:.1f}".format, "display.width", 250, "display.max_columns", 30):
    print(pd.DataFrame(rows).set_index("variant"))
