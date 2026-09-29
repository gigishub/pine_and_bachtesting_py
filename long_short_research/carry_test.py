"""Funding carry: long spot + short perp on Bybit. Return per year of notional, net of entry/exit costs.

Price moves cancel; what is left is funding (received when the rate is positive, paid when negative) minus the
cost of opening and closing both legs. Basis moves and liquidation risk are not modelled.
"""

from __future__ import annotations

import glob
from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "crypto_data" / "data"
LEG_COST = 0.00205          # per leg-pair side: spot taker 0.1% + perp taker 0.055% + 0.05% slippage
SWITCH_COST = 2 * LEG_COST  # open + close = 0.41% of notional
PERIODS = {"train 2020-21 → 2022": ("2019-01-01", "2022-12-31"),
           "validation 2023 → 2024-09": ("2023-01-01", "2024-09-30"),
           "test 2024-10 → now": ("2024-10-01", "2100-01-01")}


def load_funding() -> pd.DataFrame:
    cols = {}
    for p in sorted(glob.glob(str(DATA / "*" / "*_funding_start_*.parquet"))):
        cols[Path(p).parent.name] = pd.read_parquet(p)["fundingRate"].astype(float)
    return pd.DataFrame(cols).sort_index()


def always_on(f: pd.Series) -> pd.Series:
    """Per-funding-period return of a permanent carry position; pays the cost once at start and end."""
    r = f.dropna().copy()
    r.iloc[0] -= SWITCH_COST / 2
    r.iloc[-1] -= SWITCH_COST / 2
    return r


def smart(f: pd.Series, window: int = 21, thr: float = 0.00005) -> pd.Series:
    """Hold only after the trailing mean funding (7 days) is above thr; decided before the period is paid."""
    f = f.dropna()
    on = (f.rolling(window).mean().shift(1) > thr).astype(float)
    switches = on.diff().abs().fillna(on.iloc[0])
    return f * on - switches * SWITCH_COST / 2


def stats(r: pd.Series, a: str, z: str) -> dict:
    r = r.loc[a:z]
    if len(r) < 90:
        return {}
    yrs = len(r) / (3 * 365)
    eq = (1 + r).cumprod()
    daily = r.groupby(r.index.date).sum()
    return {"APR% notional": 100 * (eq.iloc[-1] ** (1 / yrs) - 1), "maxDD%": 100 * (eq / eq.cummax() - 1).min(),
            "worst30d%": 100 * daily.rolling(30).sum().min(), "neg 30d%": 100 * (daily.rolling(30).sum() < 0).mean(),
            "years": yrs}


def main() -> None:
    f = load_funding()
    basket = f.drop(columns=["HYPEUSDT", "TONUSDT"])  # short history / 4h funding
    series = {
        "BTC always-on": always_on(f["BTCUSDT"]),
        "ETH always-on": always_on(f["ETHUSDT"]),
        "BTC smart (7d>0.005%)": smart(f["BTCUSDT"]),
        "ETH smart (7d>0.005%)": smart(f["ETHUSDT"]),
        "BTC+ETH always-on": (always_on(f["BTCUSDT"]).add(always_on(f["ETHUSDT"]), fill_value=0) / 2),
    }
    ew = basket.apply(lambda c: c.fillna(0))
    series["alts EW always-on (no costs, survivors)"] = ew.mean(axis=1).loc["2021-10-01":]
    rows = []
    for name, r in series.items():
        for label, (a, z) in PERIODS.items():
            s = stats(r, a, z)
            if s:
                rows.append({"strategy": name, "period": label, **s})
    df = pd.DataFrame(rows)
    with pd.option_context("display.float_format", "{:.2f}".format, "display.width", 200):
        print(df.to_string(index=False))
    yr = pd.DataFrame({k: r.groupby(r.index.year).sum() * 100 for k, r in series.items() if "alts" not in k})
    print("\nFunding earned per calendar year, % of notional (costs included in the first/last period):")
    with pd.option_context("display.float_format", "{:.2f}".format, "display.width", 200):
        print(yr)


if __name__ == "__main__":
    main()
