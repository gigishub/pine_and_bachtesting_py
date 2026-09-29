"""Does extreme funding say anything about forward returns? Top-40 point-in-time universe, daily.

Funding signal at the close of day t uses only settlements strictly before that close.
Three fixed questions (all decided before looking at results):
  1. Longs: does dropping days with crowded-long funding (hot) improve a long book?
  2. Shorts: does dropping days with crowded-short funding (very negative) improve a short book?
  3. Contrarian: is hot funding a short signal, and very negative funding a long signal, on its own?
Baselines are the btc_ret20 regime for each side (the trend book) and all universe days.
"""

from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

import edge_check as ec
import ideas

ROOT = Path(__file__).resolve().parent.parent / "crypto_data"
H, HS = 10, (5, 10, 20)


def load_funding_daily(columns) -> pd.DataFrame:
    """Daily mean funding rate per 8h settlement, for settlements before each daily close. Bybit 1000x names mapped back."""
    alias = json.load(open(Path(__file__).resolve().parent / "bybit_map.json"))["alt"]
    inv = {v: k for k, v in alias.items()}
    out = {}
    for p in glob.glob(str(ROOT / "data*" / "*" / "*_funding_start_*.parquet")):
        sym = Path(p).parent.name
        name = inv.get(sym, sym)
        if name not in columns:
            continue
        f = pd.read_parquet(p)["fundingRate"].astype(float)
        f.index = f.index.tz_convert("UTC") if f.index.tz else f.index.tz_localize("UTC")
        # a settlement at 00:00 belongs to the day it closes, but is excluded (equal to the close instant)
        day = (f.index - pd.Timedelta(seconds=1)).normalize()
        out[name] = f.groupby(day).mean()
    df = pd.DataFrame(out).sort_index()
    return df.reindex(pd.date_range(df.index.min(), df.index.max(), freq="D", tz="UTC"))


def build_masks(d: dict, fd: pd.DataFrame) -> dict[str, tuple[pd.DataFrame, pd.DataFrame]]:
    """Name -> (hot, cold) masks. Funding smoothed over 3 days."""
    f = fd.reindex(index=d["close"].index, columns=d["close"].columns).rolling(3, min_periods=2).mean()
    z = (f - f.rolling(90, min_periods=60).mean()) / f.rolling(90, min_periods=60).std()
    rank = f.where(d["universe"]).rank(axis=1, pct=True)
    return {
        "abs 3d > 0.03% / < 0": (f > 0.0003, f < 0.0),
        "abs 3d > 0.05% / < -0.01%": (f > 0.0005, f < -0.0001),
        "z90 > 2 / < -2": (z > 2, z < -2),
        "z90 > 1 / < -1": (z > 1, z < -1),
        "cross-section top20% / bottom20%": (rank > 0.8, rank < 0.2),
    }


def main() -> None:
    d = ec.build(40)
    u = d["universe"]
    fd = load_funding_daily(set(u.columns))
    have = fd.reindex(d["close"].index).notna().reindex(columns=u.columns, fill_value=False)
    covered = u & have
    print(f"universe coin-days {int(u.values.sum())}, with funding {int(covered.values.sum())} "
          f"({100 * covered.values.sum() / u.values.sum():.0f}%); coins with funding: {fd.shape[1]}")
    by_year = pd.DataFrame({"universe": u.sum(axis=1), "with_funding": covered.sum(axis=1)}).groupby(lambda t: t.year).mean()
    print("avg coins/day by year:\n", by_year.round(1).T.to_string())

    rl, rs = ideas.btc_ret(d, 20)  # regime books
    books = {"all days": (u & have, u & have), "btc_ret20 regime": (u & have & rl, u & have & rs)}
    masks = build_masks(d, fd)
    periods = (("train", (pd.Timestamp("2021-01-01", tz="UTC"), ec.TRAIN[1])), ("validation", ec.VALID), ("test", ec.TEST))

    for label, period in periods:
        res = []
        for bname, (bl, bs) in books.items():
            for mname, (hot, cold) in masks.items():
                # 1 & 2: keep the book, drop crowded days (candidate = not crowded on that side)
                res.append(ec.evaluate(d, f"[{bname}] no hot | {mname}", "long", ~hot.fillna(True), bl, period, h_main=H, horizons=HS))
                res.append(ec.evaluate(d, f"[{bname}] no cold | {mname}", "short", ~cold.fillna(True), bs, period, h_main=H, horizons=HS))
                # 3: contrarian on its own, against the same book population
                res.append(ec.evaluate(d, f"[{bname}] hot=short | {mname}", "short", hot.fillna(False), u & have, period, h_main=H, horizons=HS))
                res.append(ec.evaluate(d, f"[{bname}] cold=long | {mname}", "long", cold.fillna(False), u & have, period, h_main=H, horizons=HS))
        df = ec.table(res)
        df.to_csv(Path(__file__).resolve().parent / "results" / f"funding_filter_{label}.csv", index=False)
        cols = ["idea", "side", "n", "cov%", "PF", "basePF", "lift", "mean%", "base%", "p_shift", "coins", "years", "pass"]
        ec.show(df[cols], f"funding filter, {label}, hold {H}d, top-40 universe")


if __name__ == "__main__":
    (Path(__file__).resolve().parent / "results").mkdir(exist_ok=True)
    main()
