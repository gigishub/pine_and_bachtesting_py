"""Does point-in-time momentum rotation work? Main result, controls, robustness grid, costs, per year."""

from __future__ import annotations

import sys
from dataclasses import replace
from pathlib import Path

import numpy as np
import pandas as pd

from rotation_pit import TEST_START, Params, load_panel, precompute, run, stats

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 30)
pd.set_option("display.float_format", "{:.2f}".format)
TRAIN_END = TEST_START - pd.Timedelta(days=1)


def row(name: str, eq: pd.Series, turn: pd.Series, held: pd.Series) -> dict:
    tr, te, full = stats(eq, None, TRAIN_END), stats(eq, TEST_START, None), stats(eq)
    yrs = (eq.index[-1] - eq.index[0]).days / 365.25
    return {"run": name, "train_CAGR": tr["CAGR%"], "train_DD": tr["maxDD%"], "train_Sh": tr["Sharpe"],
            "test_CAGR": te["CAGR%"], "test_DD": te["maxDD%"], "test_Sh": te["Sharpe"],
            "full_CAGR": full["CAGR%"], "full_DD": full["maxDD%"],
            "turnover/yr": turn.sum() / yrs, "in_mkt%": 100 * (held > 0).mean()}


def per_year(eqs: dict[str, pd.Series]) -> pd.DataFrame:
    return pd.DataFrame({k: 100 * (e.groupby(e.index.year).last() / e.groupby(e.index.year).first() - 1) for k, e in eqs.items()})


if __name__ == "__main__":
    sections = sys.argv[1:] or ["universe", "main", "random", "grid", "offset", "cost"]
    pc = precompute(load_panel())
    base = Params()

    if "universe" in sections:
        c = pc["close"]
        alive = c.notna() & (pc["listed_days"] >= base.min_history)
        top = pc["liq"][base.liq_window].where(alive).rank(axis=1, ascending=False) <= base.universe_n
        now_listed = set(c.columns[c.iloc[-1].notna()])
        ever = top.loc["2018":].any()
        ever = ever[ever].index
        dead = [s for s in ever if s not in now_listed]
        print(f"coins in data: {c.shape[1]}; eligible coins per day (median since 2018): "
              f"{int(alive.loc['2018':].sum(axis=1).median())}")
        print(f"coins ever in the top-{base.universe_n} universe since 2018: {len(ever)}, "
              f"of which no longer trading: {len(dead)}")
        print("  e.g.", ", ".join(sorted(dead)[:40]))

    if "main" in sections:
        runs = {
            "momentum 30d top3 (BTC filter)": base,
            "momentum 30d top3 (no filter)": replace(base, btc_filter=False),
            "CONTROL: BTC only (BTC filter)": replace(base, select="btc"),
            "CONTROL: whole universe EW (BTC filter)": replace(base, select="all"),
            "CONTROL: BTC buy & hold": replace(base, select="btc", btc_filter=False),
            "CONTROL: universe EW buy & hold": replace(base, select="all", btc_filter=False),
        }
        eqs, rows = {}, []
        for name, p in runs.items():
            eq, turn, held = run(pc, p)
            eqs[name] = eq
            rows.append(row(name, eq, turn, held))
        print("\n=== Main result vs controls (train to 2024-09-30, test after) ===")
        print(pd.DataFrame(rows).set_index("run"))
        print("\n=== Return per calendar year, % ===")
        print(per_year(eqs).round(0))

    if "random" in sections:
        n = 100
        mom = row("m", *run(pc, base))
        rnd = pd.DataFrame([row(f"r{i}", *run(pc, replace(base, select="random", seed=i))) for i in range(n)])
        print(f"\n=== Momentum pick vs {n} random picks of 3 from the same universe, same BTC filter ===")
        for k in ["train_CAGR", "test_CAGR", "full_CAGR", "full_DD"]:
            pct = (rnd[k] < mom[k]).mean() * 100
            print(f"{k:11s} momentum {mom[k]:8.1f} | random median {rnd[k].median():8.1f}, "
                  f"5–95% {rnd[k].quantile(.05):8.1f} … {rnd[k].quantile(.95):8.1f} | momentum beats {pct:.0f}% of random")

    if "grid" in sections:
        rows = []
        for lb in [7, 14, 30, 60, 90]:
            for k in [1, 3, 5, 10]:
                for n in [10, 20, 30, 50]:
                    for lw in [30, 180]:
                        if k >= n:
                            continue
                        p = replace(base, lookback=lb, top_k=k, universe_n=n, liq_window=lw)
                        rows.append({"lookback": lb, "top_k": k, "universe_n": n, "liq_window": lw, **row("", *run(pc, p))})
        g = pd.DataFrame(rows)
        ctrl = row("", *run(pc, replace(base, select="all")))
        for n in [10, 30]:
            for lw in [30, 180]:
                sub = g[(g.universe_n == n) & (g.liq_window == lw)]
                for v in ["train_CAGR", "test_CAGR", "full_DD"]:
                    print(f"\n=== Grid {v}: universe top {n} by {lw}d volume (rows lookback, cols top_k) ===")
                    print(sub.pivot(index="lookback", columns="top_k", values=v))
        print("\n=== Grid summary by universe (median over lookback x top_k) ===")
        print(g.groupby(["universe_n", "liq_window"])[["train_CAGR", "test_CAGR", "full_CAGR", "full_DD"]].median())
        for per in ["train_CAGR", "test_CAGR"]:
            beat = (g[per] > ctrl[per]).mean() * 100
            print(f"{per}: {beat:.0f}% of all {len(g)} settings beat the timed equal-weight universe ({ctrl[per]:.1f})")
        btc = row("", *run(pc, replace(base, select="btc")))
        for per in ["train_CAGR", "test_CAGR", "full_CAGR"]:
            beat = (g[per] > btc[per]).mean() * 100
            print(f"{per}: {beat:.0f}% of all {len(g)} settings beat BTC-only with the same filter ({btc[per]:.1f})")
        g.to_csv(Path(__file__).with_name("rotation_grid.csv"), index=False)

    if "offset" in sections:
        rows = [row(f"weekday offset {o}", *run(pc, replace(base, rebalance_offset=o))) for o in range(7)]
        print("\n=== Same strategy, rebalanced on each of the 7 weekdays ===")
        print(pd.DataFrame(rows).set_index("run")[["train_CAGR", "test_CAGR", "full_CAGR", "full_DD"]])

    if "cost" in sections:
        rows = [row(f"cost {c * 100:.2f}% per side", *run(pc, replace(base, cost=c))) for c in [0.001, 0.0015, 0.003, 0.005]]
        print("\n=== Cost sensitivity ===")
        print(pd.DataFrame(rows).set_index("run")[["train_CAGR", "test_CAGR", "full_CAGR", "full_DD", "turnover/yr"]])
