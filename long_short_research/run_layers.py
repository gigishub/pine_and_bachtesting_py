"""Run one layer of the top-down edge check on train.

    python run_layers.py regime
    python run_layers.py setup --long-base btc_above_ema200 --short-base btc_above_ema200
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

import edge_check as ec
import ideas

OUT = Path(__file__).resolve().parent / "results"


def masks(d, name):
    fn, kw = {**ideas.REGIME, **ideas.SETUP}[name]
    return fn(d, **kw)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("layer", choices=["regime", "setup"])
    ap.add_argument("--long-base", default=None)
    ap.add_argument("--short-base", default=None)
    args = ap.parse_args()

    d = ec.build()
    all_bars = d["universe"].copy()
    base = {"long": all_bars, "short": all_bars}
    label = {"long": "all", "short": "all"}
    for side, name in (("long", args.long_base), ("short", args.short_base)):
        if name:
            base[side] = masks(d, name)[0 if side == "long" else 1]
            label[side] = name

    pool = ideas.REGIME if args.layer == "regime" else ideas.SETUP
    res = []
    for name in pool:
        lm, sm = masks(d, name)
        res.append(ec.evaluate(d, name, "long", lm, base["long"]))
        res.append(ec.evaluate(d, name, "short", sm, base["short"]))
    df = ec.table(res).sort_values(["side", "lift"], ascending=[True, False])
    OUT.mkdir(exist_ok=True)
    tag = f"{args.layer}_L-{label['long']}_S-{label['short']}"
    df.to_csv(OUT / f"{tag}.csv", index=False)
    ec.show(df, f"{args.layer} layer, train, baseline long={label['long']} short={label['short']}")


if __name__ == "__main__":
    main()
