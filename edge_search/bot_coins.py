"""Round 7: what makes the BTC/SOL bot work (traits) and walk-forward coin admission (see PLAN.md, Round 7).

usage: python bot_coins.py prep | traits | admit
"""

from __future__ import annotations

import glob
import logging
import pickle
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "swing_research"))
from bot_baseline import bot_position  # noqa: E402

logging.disable(logging.CRITICAL)

ROOT = Path(__file__).resolve().parent
DATA = ROOT.parent / "crypto_data" / "data_binance" / "1d"
RES = ROOT / "results"
COST = 0.0015
TOP_N, MIN_LISTED, MAX_GAP = 30, 180, 7
SPLITS = {
    "train": (pd.Timestamp("2018-01-01", tz="UTC"), pd.Timestamp("2022-12-31", tz="UTC")),
    "valid": (pd.Timestamp("2023-01-01", tz="UTC"), pd.Timestamp("2024-09-30", tz="UTC")),
    "test": (pd.Timestamp("2024-10-01", tz="UTC"), pd.Timestamp("2100-01-01", tz="UTC")),
}
BTC = "BTCUSDT"
Q = 91


def segments() -> dict[str, pd.DataFrame]:
    out = {}
    now = pd.Timestamp.now(tz="UTC").normalize()
    for path in sorted(glob.glob(str(DATA / "*.parquet"))):
        sym = Path(path).stem
        df = pd.read_parquet(path)
        df = df[df.index < now]
        seg = (df.index.to_series().diff() > pd.Timedelta(days=MAX_GAP)).cumsum()
        for i, part in df.groupby(seg):
            if len(part) >= 60:
                out[sym if i == 0 else f"{sym}~{i + 1}"] = part
    return out


def coin_returns(df: pd.DataFrame, pos: pd.Series) -> pd.Series:
    """Open-to-open return of the position held on each bar, fee on every change, exit at the close on the last bar."""
    nxt = df["open"].shift(-1)
    nxt.iloc[-1] = df["close"].iloc[-1]
    r = nxt / df["open"] - 1
    return pos * r - pos.diff().abs().fillna(pos.iloc[0]) * COST


def prep():
    seg = segments()
    close = pd.DataFrame({k: d["close"] for k, d in seg.items()}).sort_index()
    dvol = pd.DataFrame({k: d["quote_volume"] for k, d in seg.items()}).sort_index()
    listed = close.notna().cumsum()
    liq = dvol.rolling(180, min_periods=120).median().where(close.notna() & (listed >= MIN_LISTED))
    elig = liq.rank(axis=1, ascending=False, method="first") <= TOP_N
    cands = [k for k in elig.columns if elig[k].any()]
    btc = seg[BTC]["close"]
    btc_ok = (btc.pct_change(20).shift(1) >= -0.03)
    rets, pos = {}, {}
    for n, k in enumerate(cands, 1):
        d = seg[k]
        ok = btc_ok.reindex(d.index).fillna(False)
        p = bot_position(d[["open", "high", "low", "close"]], entry_ok=ok).astype(float)
        pos[k], rets[k] = p, coin_returns(d, p)
        if n % 20 == 0:
            print(f"{n}/{len(cands)} coins", flush=True)
    R = pd.DataFrame(rets).reindex(close.index)
    P = pd.DataFrame(pos).reindex(close.index)
    pickle.dump({"R": R, "P": P, "close": close, "dvol": dvol, "liq": liq, "elig": elig, "listed": listed,
                 "high": pd.DataFrame({k: seg[k]["high"] for k in cands}).reindex(close.index),
                 "low": pd.DataFrame({k: seg[k]["low"] for k in cands}).reindex(close.index)}, open(RES / "bot_coins_prep.pkl", "wb"))
    print(f"saved {len(cands)} coins", flush=True)


def load():
    return pickle.load(open(RES / "bot_coins_prep.pkl", "rb"))


def split_of(d: pd.Timestamp) -> str:
    for k, (lo, hi) in SPLITS.items():
        if lo <= d <= hi:
            return k
    return "none"


def qdates(close: pd.DataFrame) -> list[pd.Timestamp]:
    d = pd.Timestamp("2019-01-01", tz="UTC")
    last = close.index[-1] - pd.Timedelta(days=Q)
    out = []
    while d <= last:
        out.append(d)
        d += pd.Timedelta(days=Q)
    return out


def traits(D: dict) -> dict[str, pd.DataFrame]:
    c, cands = D["close"][D["R"].columns], D["R"].columns
    ret = c.pct_change()
    er = ((c - c.shift(20)).abs() / c.diff().abs().rolling(20).sum()).rolling(365, min_periods=300).mean()
    r5 = c.pct_change(5)
    t = {
        "liquidity": np.log(D["liq"][cands]),
        "volatility": ret.rolling(365, min_periods=300).std(),
        "trend_eff": er,
        "persistence": r5.rolling(365, min_periods=300).corr(r5.shift(5)),
        "btc_corr": ret.rolling(365, min_periods=300).corr(ret[BTC]),
        "age": D["listed"][cands].astype(float),
    }
    return {k: v.shift(1) for k, v in t.items()}


def fwd(R: pd.DataFrame, d: pd.Timestamp) -> pd.Series:
    w = R.loc[d:d + pd.Timedelta(days=Q - 1)]
    return np.log1p(w.fillna(0.0)).sum().where(w.notna().any())


def run_traits():
    D = load()
    T = traits(D)
    rows, spread_rows = [], []
    for d in qdates(D["close"]):
        elig = D["elig"].loc[d] & (D["listed"].loc[d] >= 365)
        names = [k for k in D["R"].columns if elig.get(k, False)]
        if len(names) < 12:
            continue
        y = fwd(D["R"], d)[names]
        for tn, tv in T.items():
            x = tv.loc[d, names]
            ok = x.notna() & y.notna()
            if ok.sum() < 12:
                continue
            rho = x[ok].rank().corr(y[ok].rank())
            hi, lo = x[ok] >= x[ok].quantile(2 / 3), x[ok] <= x[ok].quantile(1 / 3)
            rows.append({"date": d, "split": split_of(d), "trait": tn, "rho": rho, "top_minus_bottom": y[ok][hi].mean() - y[ok][lo].mean(), "n": int(ok.sum())})
    df = pd.DataFrame(rows)
    df.to_csv(RES / "round7_traits_quarters.csv", index=False)
    g = df.groupby(["trait", "split"]).agg(mean_rho=("rho", "mean"), t=("rho", lambda s: s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 1 else np.nan),
                                           spread=("top_minus_bottom", "mean"), quarters=("rho", "size")).round(3)
    print(g.to_string())
    g.to_csv(RES / "round7_traits_summary.csv")
    # where BTC and SOL sit (percentile among eligible coins at the last full quarter date)
    d = qdates(D["close"])[-1]
    elig = D["elig"].loc[d] & (D["listed"].loc[d] >= 365)
    names = [k for k in D["R"].columns if elig.get(k, False)]
    print(f"\nPercentiles among {len(names)} eligible coins on {d.date()}:")
    for tn, tv in T.items():
        x = tv.loc[d, names].dropna()
        print(tn, {c: round(100 * (x < x[c]).mean(), 0) for c in ("BTCUSDT", "SOLUSDT") if c in x.index})


def pf(r: pd.Series) -> float:
    g, l = r[r > 0].sum(), -r[r < 0].sum()
    return g / l if l > 0 else np.inf if g > 0 else 0.0


def trades_stats(P: pd.Series, R: pd.Series) -> tuple[int, float]:
    """Trades and profit factor of the daily returns split at trade boundaries."""
    ent = (P > 0) & (P.shift(fill_value=0) == 0)
    tid = ent.cumsum().where(P > 0)
    tr = R.groupby(tid).apply(lambda s: (1 + s).prod() - 1)
    return len(tr), pf(tr)


def metrics(r: pd.Series) -> dict:
    r = r.dropna()
    if len(r) < 60:
        return {}
    eq = (1 + r).cumprod()
    yrs = len(r) / 365.25
    cagr = eq.iloc[-1] ** (1 / yrs) - 1 if eq.iloc[-1] > 0 else -1.0
    dd = (eq / eq.cummax() - 1).min()
    return {"CAGR%": 100 * cagr, "maxDD%": 100 * dd, "calmar": cagr / abs(dd) if dd < 0 else np.nan,
            "sharpe": r.mean() / r.std() * np.sqrt(365.25) if r.std() > 0 else np.nan}


def run_admit():
    D = load()
    R, P = D["R"], D["P"]
    strat = {"admit": [], "btc": [], "btc_sol": [], "all": [], "traits_top": []}
    series = {k: pd.Series(0.0, index=R.index) for k in strat}
    counts = []
    for d in qdates(D["close"]):
        end = d + pd.Timedelta(days=Q - 1)
        elig = D["elig"].loc[d] & (D["listed"].loc[d] >= 365)
        names = [k for k in R.columns if elig.get(k, False)]
        adm = []
        for k in names:
            lo1, lo2 = d - pd.Timedelta(days=730), d - pd.Timedelta(days=365)
            rr, pp = R[k].loc[lo1:d - pd.Timedelta(days=1)], P[k].loc[lo1:d - pd.Timedelta(days=1)]
            if rr.notna().sum() < 700:
                continue
            n, p = trades_stats(pp, rr)
            h1 = (1 + rr.loc[:lo2 - pd.Timedelta(days=1)].fillna(0)).prod() - 1
            h2 = (1 + rr.loc[lo2:].fillna(0)).prod() - 1
            if n >= 8 and p >= 1.5 and h1 > 0 and h2 > 0:
                adm.append(k)
        counts.append({"date": d, "split": split_of(d), "eligible": len(names), "admitted": len(adm), "coins": ",".join(adm)})
        win = slice(d, end)
        series["admit"].loc[win] = R.loc[win, adm].mean(axis=1).fillna(0.0) if adm else 0.0
        series["btc"].loc[win] = R.loc[win, BTC].fillna(0.0)
        bs = [k for k in (BTC, "SOLUSDT") if k in R.columns and R[k].loc[win].notna().any()]
        series["btc_sol"].loc[win] = R.loc[win, bs].mean(axis=1).fillna(0.0)
        series["all"].loc[win] = R.loc[win, names].mean(axis=1).fillna(0.0)
    pd.DataFrame(counts).to_csv(RES / "round7_admission.csv", index=False)
    close = D["close"]
    bh = close[BTC].pct_change().shift(-1).fillna(0.0)
    rows = []
    for sp in ("train", "valid", "test"):
        lo, hi = SPLITS[sp]
        lo = max(lo, pd.Timestamp("2019-01-01", tz="UTC"))
        for name, s in list(series.items()) + [("btc_buy_hold", bh)]:
            if name == "traits_top":
                continue
            m = metrics(s.loc[lo:hi][s.loc[lo:hi].index >= lo])
            if m:
                rows.append({"split": sp, "strategy": name, **m})
    out = pd.DataFrame(rows)
    print(out.round(2).to_string(index=False))
    out.to_csv(RES / "round7_admit_results.csv", index=False)
    c = pd.DataFrame(counts)
    print(c.groupby("split")[["eligible", "admitted"]].mean().round(1))
    print(c.tail(6)[["date", "admitted", "coins"]].to_string(index=False))


if __name__ == "__main__":
    {"prep": prep, "traits": run_traits, "admit": run_admit}[sys.argv[1]]()
