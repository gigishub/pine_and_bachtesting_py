"""Test simple entry filters and volatility sizing on top of the live bot. Thresholds come from train quartiles."""

from __future__ import annotations

import logging

import pandas as pd

from bot_baseline import bot_position
from common import TEST_START, available_symbols, load, metrics
from trade_features import indicator_frame

logging.disable(logging.CRITICAL)

ATR_MAX = 0.08        # skip entries when daily ATR is above 8% of price
BTC_RET20_MIN = -0.03  # skip entries when BTC fell more than 3% over 20 days
TARGET_ATR = 0.045    # vol sizing: full size at 4.5% ATR, smaller above


def size_at_entry(pos: pd.Series, size: pd.Series) -> pd.Series:
    """Hold the size chosen on the entry bar for the whole trade."""
    entry = (pos > 0) & (pos.shift(fill_value=0) == 0)
    return pos * size.where(entry).ffill().fillna(0)


def variants(sym: str, btc_feats: pd.DataFrame) -> dict[str, pd.Series]:
    df = load(sym, "1d")
    f = indicator_frame(df).shift(1)
    btc_ret20 = btc_feats["ret_20"].shift(1).reindex(df.index)
    low_vol = f["atr_pct"] <= ATR_MAX
    btc_ok = btc_ret20 >= BTC_RET20_MIN
    base = bot_position(df)
    return {
        "0_live": base,
        "1_skip_high_vol": bot_position(df, entry_ok=low_vol),
        "2_skip_btc_down": bot_position(df, entry_ok=btc_ok),
        "3_both_filters": bot_position(df, entry_ok=low_vol & btc_ok),
        "4_vol_sizing": size_at_entry(base, (TARGET_ATR / f["atr_pct"]).clip(upper=1)),
        "5_both+sizing": size_at_entry(bot_position(df, entry_ok=low_vol & btc_ok), (TARGET_ATR / f["atr_pct"]).clip(upper=1)),
    }


if __name__ == "__main__":
    btc_feats = indicator_frame(load("BTCUSDT", "1d"))
    rows = []
    for sym in available_symbols("1d"):
        df = load(sym, "1d")
        for name, pos in variants(sym, btc_feats).items():
            for period, s, e in [("train", None, TEST_START - pd.Timedelta(seconds=1)), ("test", TEST_START, None)]:
                m = metrics(df, pos, s, e)
                if m:
                    rows.append({"variant": name, "period": period, "symbol": sym, **m})
    r = pd.DataFrame(rows)
    cols = ["trades", "win%", "PF", "avg%", "CAGR%", "maxDD%", "expo%"]
    with pd.option_context("display.float_format", "{:.2f}".format, "display.width", 200):
        print(f"{r.symbol.nunique()} coins\n\n=== Median over all coins ===")
        print(r.groupby(["period", "variant"])[cols].median())
        r["beats_live"] = r.groupby(["period", "symbol"])["CAGR%"].transform(lambda x: x > x[r.loc[x.index, "variant"] == "0_live"].iloc[0])
        print("\n=== Coins where CAGR beats the live bot ===")
        print(r.groupby(["period", "variant"])["beats_live"].sum().unstack(0))
        for sym in ["BTCUSDT", "SOLUSDT"]:
            print(f"\n=== {sym} ===")
            print(r[r.symbol == sym].set_index(["period", "variant"])[cols])
