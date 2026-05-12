"""Bear Strategy — sweep analysis CLI.

Loads sweep_summary.csv, applies pass/fail gates, and prints:
  1. Ranked table — only combos where MIN_PAIRS_PASS pairs clear ALL gates.
     Aggregate metrics are computed exclusively from the passing pairs.
  2. Per-combo detail — which pairs pass/fail and their key metrics.
  3. Pivot heatmaps — Return / SQN / PF by SL × TP.

Usage
-----
    python -m bear_strategy.backtest.strategy_evaluation.analyse
    python -m bear_strategy.backtest.strategy_evaluation.analyse \\
        --file bear_strategy/backtest/vectorbt/results/.../sweep_summary.csv \\
        --min-sqn 0.5 --min-pf 1.2 --min-trades 15
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import pandas as pd

_ROOT = Path(__file__).parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from bear_strategy.backtest.strategy_evaluation.scoring import (
    score_row, passes_gates, combo_label,
    DEFAULT_MIN_SQN, DEFAULT_MIN_PF, DEFAULT_MIN_TRADES, DEFAULT_MIN_WR,
)

log = logging.getLogger(__name__)

_RESULTS_ROOT = Path("bear_strategy/backtest/vectorbt/results")

_DETAIL_COLS = [
    "Return [%]", "SQN", "Profit Factor", "Expectancy [%]",
    "Win Rate [%]", "Max. Drawdown [%]", "Sharpe Ratio", "# Trades",
]


# ─────────────────────────────────────────────────────────────────────────────
# Data loading
# ─────────────────────────────────────────────────────────────────────────────

def load_sweep(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    if "symbol" in df.columns and "Symbol" not in df.columns:
        df = df.rename(columns={"symbol": "Symbol"})
    df["Symbol"] = df["Symbol"].str.strip()
    return df


def find_latest_sweep() -> Path | None:
    sweeps = sorted(_RESULTS_ROOT.glob("*_SWEEP/sweep_summary.csv"), reverse=True)
    return sweeps[0] if sweeps else None


# ─────────────────────────────────────────────────────────────────────────────
# Analysis
# ─────────────────────────────────────────────────────────────────────────────

def analyse(
    df: pd.DataFrame,
    min_sqn:       float = DEFAULT_MIN_SQN,
    min_pf:        float = DEFAULT_MIN_PF,
    min_trades:    int   = DEFAULT_MIN_TRADES,
    min_wr:        float = DEFAULT_MIN_WR,
    min_pairs_pass: int  = 1,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Run full analysis.

    Returns
    -------
    ranked_all : pd.DataFrame
        Every combo that has >= min_pairs_pass pairs passing, aggregated over
        all pairs (same behaviour as the original sweep analyser).
    ranked_passing : pd.DataFrame
        Same combos aggregated over passing pairs only. Metrics reflect what
        you would see if you traded only those pairs.
    per_pair : pd.DataFrame
        One row per (combo x pair) with PASS/FAIL and all key metrics.
    """
    df = df.copy()

    def _make_label(r: pd.Series) -> str:
        mode      = r["exit_mode"]          if "exit_mode"          in r.index else "fixed_tp"
        rsi_lvl   = r["exit_rsi_level"]     if "exit_rsi_level"     in r.index else None
        os_lvl    = r["rsi_oversold_level"] if "rsi_oversold_level" in r.index else None
        ema_per   = r["exit_ema_period"]    if "exit_ema_period"    in r.index else None
        # Coerce pandas NA/NaN to None
        rsi_lvl = None if rsi_lvl is not None and pd.isna(rsi_lvl) else rsi_lvl
        os_lvl  = None if os_lvl  is not None and pd.isna(os_lvl)  else os_lvl
        ema_per = None if ema_per is not None and pd.isna(ema_per)  else ema_per
        return combo_label(
            r["sl_mult"], r["tp_mult"], mode,
            exit_rsi_level=rsi_lvl,
            rsi_oversold_level=os_lvl,
            exit_ema_period=int(ema_per) if ema_per is not None else None,
        )

    df["_label"]  = df.apply(_make_label, axis=1)
    df["_passes"] = df.apply(
        lambda r: passes_gates(r, min_sqn, min_pf, min_trades, min_wr), axis=1
    )
    df["_score"] = df.apply(score_row, axis=1)

    symbols = sorted(df["Symbol"].unique())
    n_pairs = len(symbols)

    rows_all:     list[dict] = []
    rows_passing: list[dict] = []

    for label, grp in df.groupby("_label"):
        passing_grp = grp[grp["_passes"]]
        n_pass      = len(passing_grp)

        if n_pass < min_pairs_pass:
            continue

        passing_pairs = sorted(passing_grp["Symbol"].tolist())
        sl = grp["sl_mult"].iloc[0]
        tp = grp["tp_mult"].iloc[0]
        mode    = grp["exit_mode"].iloc[0]          if "exit_mode"          in grp.columns else "fixed_tp"
        rsi_lvl = grp["exit_rsi_level"].iloc[0]     if "exit_rsi_level"     in grp.columns else None
        os_lvl  = grp["rsi_oversold_level"].iloc[0] if "rsi_oversold_level" in grp.columns else None
        ema_per = grp["exit_ema_period"].iloc[0]    if "exit_ema_period"    in grp.columns else None
        rsi_lvl = None if rsi_lvl is not None and pd.isna(rsi_lvl) else rsi_lvl
        os_lvl  = None if os_lvl  is not None and pd.isna(os_lvl)  else os_lvl
        ema_per = None if ema_per is not None and pd.isna(ema_per)  else ema_per
        pairs_label = f"{n_pass} \u2192 {', '.join(passing_pairs)}"

        # ── All-pairs aggregate ───────────────────────────────────────────
        avg_score_all     = grp["_score"].mean()
        breadth_score_all = avg_score_all * (n_pass / n_pairs)
        row_all: dict = {
            "Signature":               label,
            "SL\u00d7":               sl,
            "TP\u00d7":               tp,
            f"Pairs ({n_pairs} total)": pairs_label,
            "Breadth Score":           round(breadth_score_all, 4),
            "Avg Score (all pairs)":   round(avg_score_all, 4),
        }
        for col in _DETAIL_COLS:
            if col in grp.columns:
                row_all[f"Avg {col}"] = round(grp[col].mean(), 3)
        rows_all.append(row_all)

        # ── Passing-pairs-only aggregate ──────────────────────────────────
        avg_score_pass     = passing_grp["_score"].mean()
        breadth_score_pass = avg_score_pass * (n_pass / n_pairs)
        row_pass: dict = {
            "Signature":               label,
            "SL\u00d7":               sl,
            "TP\u00d7":               tp,
            f"Pairs ({n_pairs} total)": pairs_label,
            "Breadth Score":           round(breadth_score_pass, 4),
            "Avg Score (passing)":     round(avg_score_pass, 4),
        }
        for col in _DETAIL_COLS:
            if col in passing_grp.columns:
                row_pass[f"Avg {col}"] = round(passing_grp[col].mean(), 3)
        rows_passing.append(row_pass)

    def _sort(rows: list[dict]) -> pd.DataFrame:
        df_ = (
            pd.DataFrame(rows)
            .sort_values("Breadth Score", ascending=False)
            .reset_index(drop=True)
        )
        df_.index += 1
        return df_

    ranked_all     = _sort(rows_all)
    ranked_passing = _sort(rows_passing)

    # Build per-pair detail for every combo (all pairs, not just passing)
    detail_rows: list[dict] = []
    for label, grp in df.groupby("_label"):
        for _, r in grp.iterrows():
            row = {
                "Signature": label,
                "Symbol":    r["Symbol"],
                "Pass":      "✅" if r["_passes"] else "❌",
                "Score":     round(r["_score"], 4),
            }
            for col in _DETAIL_COLS:
                if col in r.index:
                    row[col] = round(float(r[col]), 3) if pd.notna(r[col]) else float("nan")
            detail_rows.append(row)

    per_pair = pd.DataFrame(detail_rows)

    return ranked_all, ranked_passing, per_pair


# ─────────────────────────────────────────────────────────────────────────────
# Printing
# ─────────────────────────────────────────────────────────────────────────────

def _print_analysis(
    ranked: pd.DataFrame,
    per_pair: pd.DataFrame,
    df: pd.DataFrame,
    min_sqn: float,
    min_pf: float,
    min_trades: int,
    min_wr: float,
) -> None:
    symbols = sorted(df["Symbol"].unique())
    print(f"\n{'═'*72}")
    print("  SWEEP ANALYSIS — passing combos only")
    print(f"  Gates: SQN≥{min_sqn}  PF≥{min_pf}  trades≥{min_trades}  WR≥{min_wr}%")
    print(f"  Pairs in sweep: {', '.join(symbols)}")
    print(f"{'═'*72}")

    if ranked.empty:
        print("\n  ⚠  No combo cleared the gates.  Relax thresholds with --min-* flags.\n")
        return

    print(f"\n── {len(ranked)} combo(s) passed ─────────────────────────────────────────────")
    print(ranked.to_string(index=True))

    print("\n── Per-pair detail (top 3 combos) ───────────────────────────────────────")
    top_sigs = ranked["Signature"].head(3).tolist()
    for sig in top_sigs:
        sub = per_pair[per_pair["Signature"] == sig].drop(columns=["Signature"])
        print(f"\n  {sig}")
        print(sub.to_string(index=False))

    # SQN pivot across all combos
    _df = df.copy()
    _df["_label"] = _df.apply(lambda r: combo_label(r["sl_mult"], r["tp_mult"]), axis=1)
    for metric in ("Return [%]", "SQN", "Profit Factor"):
        if metric in _df.columns:
            piv = _df.pivot_table(index="sl_mult", columns="tp_mult", values=metric, aggfunc="mean")
            piv.index.name = f"SL \\ {metric}"
            print(f"\n── Avg {metric} (all combos / all pairs) ──")
            print(piv.round(3).to_string())


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analyse sweep_summary.csv — only passing combos shown.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--file",        default=None,              metavar="PATH")
    parser.add_argument("--min-sqn",     type=float, default=DEFAULT_MIN_SQN)
    parser.add_argument("--min-pf",      type=float, default=DEFAULT_MIN_PF)
    parser.add_argument("--min-trades",  type=int,   default=DEFAULT_MIN_TRADES)
    parser.add_argument("--min-wr",      type=float, default=DEFAULT_MIN_WR)
    parser.add_argument("--min-pairs",   type=int,   default=1,
                        help="Minimum number of pairs that must pass for a combo to be listed.")
    args = parser.parse_args()

    logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")

    csv_path = Path(args.file) if args.file else find_latest_sweep()
    if csv_path is None:
        print("No sweep results found.  Run sweep_run.py first, or pass --file.")
        sys.exit(1)
    print(f"  Loading: {csv_path}")

    df = load_sweep(csv_path)
    ranked_all, ranked_passing, per_pair = analyse(
        df,
        min_sqn        = args.min_sqn,
        min_pf         = args.min_pf,
        min_trades     = args.min_trades,
        min_wr         = args.min_wr,
        min_pairs_pass = args.min_pairs,
    )

    _print_analysis(ranked_all, per_pair, df, args.min_sqn, args.min_pf, args.min_trades, args.min_wr)

    if not ranked_all.empty:
        out_dir = csv_path.parent
        ranked_all.to_csv(out_dir / "analysis_ranked_all.csv")
        ranked_passing.to_csv(out_dir / "analysis_ranked_passing.csv")
        per_pair.to_csv(out_dir / "analysis_per_pair.csv", index=False)
        print(f"\n  Saved → {out_dir}/analysis_ranked_all.csv")
        print(f"  Saved → {out_dir}/analysis_ranked_passing.csv")
        print(f"  Saved → {out_dir}/analysis_per_pair.csv\n")
