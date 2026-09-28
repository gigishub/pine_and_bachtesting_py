"""Chop + mean-reversion edge check, 5-day primary hold.

    python run_chop.py regime                     # chop detectors vs the reversal probe (train)
    python run_chop.py setup --chop btc_er20<0.3  # mean-reversion signals inside chop (train)
    python run_chop.py holdout --chop X --long-signal A --short-signal B   # validation + test, run once
"""

from __future__ import annotations

import argparse
from pathlib import Path

import edge_check as ec
import chop_ideas as ci

OUT = Path(__file__).resolve().parent / "results"
H, HS = 5, (3, 5, 10)


def chop_mask(d, name):
    fn, kw = ci.CHOP[name]
    return fn(d, **kw)


def signal(d, name):
    fn, kw = ci.MEANREV[name]
    return fn(d, **kw)


def ev(d, name, side, cand, base, period=ec.TRAIN):
    return ec.evaluate(d, name, side, cand, base, period=period, h_main=H, horizons=HS)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("layer", choices=["regime", "setup", "holdout"])
    ap.add_argument("--chop")
    ap.add_argument("--long-signal")
    ap.add_argument("--short-signal")
    args = ap.parse_args()
    d = ec.build()
    u = d["universe"]
    OUT.mkdir(exist_ok=True)

    if args.layer == "regime":
        pl, ps = ci.reversal_probe(d)
        res = []
        for name in ci.CHOP:
            m = chop_mask(d, name)
            res += [ev(d, name, "long", m, pl), ev(d, name, "short", m, ps)]
        df = ec.table(res).sort_values(["side", "lift"], ascending=[True, False])
        df.to_csv(OUT / "chop_regime.csv", index=False)
        ec.show(df, "chop regime layer, train, baseline = reversal probe on all days")

    elif args.layer == "setup":
        chop = chop_mask(d, args.chop)
        res = []
        for name in ci.MEANREV:
            lm, sm = signal(d, name)
            res += [ev(d, name, "long", lm, chop), ev(d, name, "short", sm, chop)]
            # same signal on all days, to see whether the chop filter matters
            res += [ev(d, name + " (all days)", "long", lm, u), ev(d, name + " (all days)", "short", sm, u)]
        df = ec.table(res).sort_values(["side", "lift"], ascending=[True, False])
        df.to_csv(OUT / f"chop_setup_{args.chop}.csv", index=False)
        ec.show(df, f"mean-reversion setup layer, train, baseline = {args.chop}")

    else:
        chop = chop_mask(d, args.chop)
        for label, period in (("train", ec.TRAIN), ("validation", ec.VALID), ("test", ec.TEST)):
            res = []
            if args.long_signal:
                res.append(ev(d, f"{args.chop} + {args.long_signal}", "long", signal(d, args.long_signal)[0], chop, period))
            if args.short_signal:
                res.append(ev(d, f"{args.chop} + {args.short_signal}", "short", signal(d, args.short_signal)[1], chop, period))
            ec.show(ec.table(res), label)


if __name__ == "__main__":
    main()
