"""Deprecated — analysis has moved to bear_strategy/backtest/strategy_evaluation/analyse.py.

Bear Strategy — SL/TP sweep analysis.

Loads a ``sweep_summary.csv`` produced by ``sweep_run.py`` and produces
a ranked analysis of all (sl_mult, tp_mult) combinations using the same
scoring engine as ``strategy_evaluation``.

Usage
-----
    # Analyse the most recent sweep automatically:
    python -m bear_strategy.backtest.vectorbt.analyse_sweep

    # Analyse a specific sweep file:
    python -m bear_strategy.backtest.vectorbt.analyse_sweep \\
        --file bear_strategy/backtest/vectorbt/results/2026-05-10_1032_SWEEP/sweep_summary.csv

    # Relax the minimum trades threshold (fewer trades in OOS window):
    python -m bear_strategy.backtest.vectorbt.analyse_sweep --min-trades 15

Output (printed + saved next to the CSV)
-----------------------------------------
  1. Ranked table — every (SL×, TP×) combo scored across all pairs
  2. Consistency table — how many pairs each combo profits on
  3. Pivot tables — Return / WR / PF / SQN by SL × TP

Scoring formula (0–1 composite)
---------------------------------
  SQN            22 %   (0 → 3)
  Profit Factor  18 %   (1 → 4)
  Expectancy     15 %   (0 → 5 %)
  Sharpe         12 %   (0 → 2)
  Sortino        10 %   (0 → 3)
  Max Drawdown   10 %   (inverted, 0 → 60 %)
  Calmar          5 %   (0 → 5)
  Omega           4 %   (1 → 2)
  R:R Ratio       4 %   (1 → 4)

A combo "passes" when it meets ALL gates on a given pair:
  SQN ≥ min_sqn, PF ≥ min_pf, trades ≥ min_trades, WR ≥ min_wr

Edit the THRESHOLDS block below to tighten or relax the gates.
"""

from __future__ import annotations

import argparse
import logging
import math
import sys
from pathlib import Path

import pandas as pd

_ROOT = Path(__file__).parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

log = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# ★  EDIT THESE THRESHOLDS to tighten or relax pass/fail gates
# ─────────────────────────────────────────────────────────────────────────────

MIN_SQN:        float = 0.0    # 0 = any positive expectancy; 1.0 = strong edge
MIN_PF:         float = 1.0    # Minimum Profit Factor (1.0 = break-even)
MIN_TRADES:     int   = 10     # Minimum trades per pair for the combo to count
MIN_WIN_RATE:   float = 0.0    # Minimum win rate % (0 = don't gate on WR)
MIN_PAIRS_PASS: int   = 1      # Combo must profit on at least this many pairs

# Scoring normalisation ceilings (values above are capped at 1.0)
_SQN_CEIL     = 3.0
_PF_CEIL      = 4.0
_EXP_CEIL     = 5.0    # Expectancy %
_SH_CEIL      = 2.0    # Sharpe Ratio
_SORT_CEIL    = 3.0    # Sortino Ratio
_DD_CEIL      = 60.0   # Max Drawdown % (inverted)
_CAL_CEIL     = 5.0    # Calmar Ratio
_OM_CEIL      = 2.0    # Omega Ratio  (1 = break-even)
_RR_CEIL      = 4.0    # R:R Ratio
_RF_CEIL      = 5.0    # Recovery Factor

# Scoring weights (must sum to 1.0)
_WEIGHTS = {
    "sqn":             0.22,
    "profit_factor":   0.18,
    "expectancy":      0.15,
    "sharpe":          0.12,
    "sortino":         0.10,
    "max_drawdown":    0.10,   # inverted
    "calmar":          0.05,
    "omega":           0.04,
    "rr_ratio":        0.04,
}


# ─────────────────────────────────────────────────────────────────────────────
# Scoring helpers
# ─────────────────────────────────────────────────────────────────────────────

def _norm(v: float, lo: float, hi: float) -> float:
    if math.isnan(v):
        return 0.0
    return max(0.0, min(1.0, (v - lo) / (hi - lo)))


def _score_row(row: pd.Series) -> float:
    def _g(col: str) -> float:
        v = row.get(col, float("nan"))
        return float("nan") if pd.isna(v) else float(v)

    sqn    = _g("SQN")
    pf     = _g("Profit Factor")
    exp    = _g("Expectancy [%]")
    sh     = _g("Sharpe Ratio")
    sortino = _g("Sortino Ratio")
    dd     = _g("Max. Drawdown [%]")
    cal    = _g("Calmar Ratio")
    omega  = _g("Omega Ratio")
    rr     = _g("R:R Ratio")

    return (
        _WEIGHTS["sqn"]           * _norm(sqn,     0.0, _SQN_CEIL)
        + _WEIGHTS["profit_factor"] * _norm(pf,    1.0, _PF_CEIL)
        + _WEIGHTS["expectancy"]    * _norm(exp,   0.0, _EXP_CEIL)
        + _WEIGHTS["sharpe"]        * _norm(sh,    0.0, _SH_CEIL)
        + _WEIGHTS["sortino"]       * _norm(sortino, 0.0, _SORT_CEIL)
        + _WEIGHTS["max_drawdown"]  * (1.0 - _norm(dd, 0.0, _DD_CEIL))
        + _WEIGHTS["calmar"]        * _norm(cal,   0.0, _CAL_CEIL)
        + _WEIGHTS["omega"]         * _norm(omega, 1.0, _OM_CEIL)
        + _WEIGHTS["rr_ratio"]      * _norm(rr,    1.0, _RR_CEIL)
    )


def _passes(row: pd.Series) -> bool:
    def _g(col: str) -> float:
        v = row.get(col, float("nan"))
        return float("nan") if pd.isna(v) else float(v)

    sqn     = _g("SQN")
    pf      = _g("Profit Factor")
    trades  = _g("# Trades")
    wr      = _g("Win Rate [%]")

    if any(math.isnan(x) for x in [sqn, pf, trades, wr]):
        return False
    return (
        sqn    >= MIN_SQN
        and pf >= MIN_PF
        and trades >= MIN_TRADES
        and wr >= MIN_WIN_RATE
    )


def _sig(sl: float, tp: float) -> str:
    return f"SL={sl:.1f}× TP={tp:.1f}×"


# ─────────────────────────────────────────────────────────────────────────────
# Analysis
# ─────────────────────────────────────────────────────────────────────────────

def analyse(df: pd.DataFrame) -> None:
    """Run full analysis and print results."""
    df = df.copy()
    df.columns = df.columns.str.strip()

    # Normalise column names from older CSVs
    if "symbol" in df.columns and "Symbol" not in df.columns:
        df = df.rename(columns={"symbol": "Symbol"})

    df["_sig"]     = df.apply(lambda r: _sig(r["sl_mult"], r["tp_mult"]), axis=1)
    df["_passes"]  = df.apply(_passes, axis=1)
    df["_score"]   = df.apply(_score_row, axis=1)

    symbols = sorted(df["Symbol"].unique())
    sigs    = sorted(df["_sig"].unique())
    n_pairs = len(symbols)

    # ── 1. Per-combo aggregate across all pairs ───────────────────────────────
    agg_rows = []
    for sig, grp in df.groupby("_sig"):
        sl = grp["sl_mult"].iloc[0]
        tp = grp["tp_mult"].iloc[0]

        pairs_passing  = int(grp["_passes"].sum())
        total_trades   = int(grp["# Trades"].sum())
        avg_ret        = grp["Return [%]"].mean()
        avg_pf         = grp["Profit Factor"].mean()
        avg_wr         = grp["Win Rate [%]"].mean()
        avg_sqn        = grp["SQN"].mean()
        avg_score      = grp["_score"].mean()
        # Breadth bonus: avg_score × (pairs_passing / n_pairs)
        breadth_score  = avg_score * (pairs_passing / n_pairs) if n_pairs else 0.0

        agg_rows.append({
            "SL×":            sl,
            "TP×":            tp,
            "Signature":      sig,
            "Pairs Passing":  pairs_passing,
            "Total Trades":   total_trades,
            "Avg Return [%]": round(avg_ret, 2),
            "Avg WR [%]":     round(avg_wr,  1),
            "Avg PF":         round(avg_pf,  3),
            "Avg SQN":        round(avg_sqn, 3),
            "Avg Score":      round(avg_score, 4),
            "Breadth Score":  round(breadth_score, 4),
        })

    ranked = (
        pd.DataFrame(agg_rows)
        .sort_values("Breadth Score", ascending=False)
        .reset_index(drop=True)
    )
    ranked.index += 1  # rank from 1

    # ── 2. Consistency table: pairs_passing breakdown per combo ───────────────
    consistency_rows = []
    for _, row in ranked.iterrows():
        sig  = row["Signature"]
        grp  = df[df["_sig"] == sig]
        pair_cols = {
            sym: ("✅" if grp[grp["Symbol"] == sym]["_passes"].any() else "❌")
            for sym in symbols
        }
        consistency_rows.append({"Signature": sig, **pair_cols,
                                   "Pairs ✅": row["Pairs Passing"]})
    consistency = pd.DataFrame(consistency_rows).set_index("Signature")

    # ── 3. Pivots ──────────────────────────────────────────────────────────────
    def _pivot(metric: str) -> pd.DataFrame:
        piv = df.pivot_table(
            index="sl_mult", columns="tp_mult", values=metric, aggfunc="mean"
        )
        piv.index.name   = f"SL \\ {metric}"
        piv.columns.name = "TP mult"
        return piv

    # ── Print ──────────────────────────────────────────────────────────────────
    print(f"\n{'═'*72}")
    print("  SL/TP SWEEP ANALYSIS")
    print(f"  Thresholds: SQN≥{MIN_SQN}  PF≥{MIN_PF}  trades≥{MIN_TRADES}  WR≥{MIN_WIN_RATE}%")
    print(f"  Pairs: {', '.join(symbols)}  ({n_pairs} total)")
    print(f"{'═'*72}")

    print("\n── Ranked Table (sorted by Breadth Score = avg_score × pairs_passing/N) ──")
    print(ranked.to_string(index=True))

    print(f"\n── Consistency (✅ = passes gates on that pair, ❌ = fails) ──")
    print(consistency.to_string())

    for metric, fmt in [
        ("Return [%]",    "+.2f"),
        ("Profit Factor", ".3f"),
        ("SQN",           ".2f"),
        ("Win Rate [%]",  ".1f"),
    ]:
        if metric in df.columns:
            piv = _pivot(metric)
            print(f"\n── Avg {metric} (rows=SL, cols=TP) ──")
            print(piv.to_string(float_format=lambda x: f"{x:{fmt}}" if x == x else "  n/a"))

    return ranked, consistency


def _find_latest_sweep() -> Path | None:
    results_root = Path("bear_strategy/backtest/vectorbt/results")
    sweeps = sorted(results_root.glob("*_SWEEP/sweep_summary.csv"), reverse=True)
    return sweeps[0] if sweeps else None


def _save_analysis(ranked: pd.DataFrame, consistency: pd.DataFrame, csv_path: Path) -> None:
    out_dir = csv_path.parent
    ranked.to_csv(out_dir / "analysis_ranked.csv")
    consistency.to_csv(out_dir / "analysis_consistency.csv")
    log.info("Analysis saved → %s", out_dir)


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analyse a sweep_summary.csv produced by sweep_run.py.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--file", default=None, metavar="PATH",
        help="Path to sweep_summary.csv.  Defaults to the most recent *_SWEEP/ folder.",
    )
    parser.add_argument("--min-sqn",    type=float, default=None, help="Override MIN_SQN gate.")
    parser.add_argument("--min-pf",     type=float, default=None, help="Override MIN_PF gate.")
    parser.add_argument("--min-trades", type=int,   default=None, help="Override MIN_TRADES gate.")
    parser.add_argument("--min-wr",     type=float, default=None, help="Override MIN_WIN_RATE gate.")
    args = parser.parse_args()

    logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")

    # Apply CLI threshold overrides
    if args.min_sqn    is not None: MIN_SQN        = args.min_sqn
    if args.min_pf     is not None: MIN_PF         = args.min_pf
    if args.min_trades is not None: MIN_TRADES      = args.min_trades
    if args.min_wr     is not None: MIN_WIN_RATE    = args.min_wr

    # Locate CSV
    if args.file:
        csv_path = Path(args.file)
    else:
        csv_path = _find_latest_sweep()
        if csv_path is None:
            print("No sweep results found.  Run sweep_run.py first, or pass --file.")
            sys.exit(1)
        print(f"  Loading: {csv_path}")

    df = pd.read_csv(csv_path)
    result = analyse(df)

    if result is not None:
        ranked, consistency = result
        _save_analysis(ranked, consistency, csv_path)
        print(f"\n  Analysis saved alongside {csv_path.name}\n")
