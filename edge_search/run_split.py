"""Run the ideas on one split and print metrics, gates and the win condition.

usage: python run_split.py train [A B ...]      (valid/test only for ideas that passed the earlier split)
"""

from __future__ import annotations

import sys
import warnings

import pandas as pd

warnings.filterwarnings("ignore", category=FutureWarning)

from engine import SPLITS, build_market, buy_and_hold, metrics, passes_win_condition, run, shift_pvalue
from ideas import IDEAS

split = sys.argv[1]
names = sys.argv[2:] or list(IDEAS)
lo, hi = SPLITS[split]
mkt = build_market()

bh = metrics(buy_and_hold(mkt), lo, hi)
ew = metrics(run(mkt, mkt.universe.astype(float) / 10), lo, hi)
print(f"[{split}] BTC buy&hold: CAGR {bh['CAGR%']:.1f}%  maxDD {bh['maxDD%']:.1f}%   "
      f"| EW top-10 buy&hold: CAGR {ew['CAGR%']:.1f}%  maxDD {ew['maxDD%']:.1f}%\n")

rows = []
for name in names:
    w = IDEAS[name](mkt, 1.0)
    m = metrics(run(mkt, w), lo, hi)
    variants = [metrics(run(mkt, IDEAS[name](mkt, k)), lo, hi).get("CAGR%", float("nan")) for k in (0.5, 2.0)]
    p = shift_pvalue(mkt, w, (lo, hi))
    a, b = passes_win_condition(m, bh)
    rows.append({"idea": name, **m, "k0.5 CAGR%": variants[0], "k2 CAGR%": variants[1], "shift_p": p,
                 "gate1": m["CAGR%"] > 0, "gate2": p <= 0.05, "gate3": min(variants) > 0,
                 "win_a": a, "win_b": b})
out = pd.DataFrame(rows).set_index("idea")
with pd.option_context("display.float_format", "{:.2f}".format, "display.width", 250, "display.max_columns", 30):
    print(out)
