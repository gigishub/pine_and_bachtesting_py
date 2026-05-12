"""Bear Strategy — markdown report generator.

Produces a self-contained analysis report from the output of ``analyse()``.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd


_DETAIL_COLS = [
    "Return [%]", "SQN", "Profit Factor", "Expectancy [%]",
    "Win Rate [%]", "Max. Drawdown [%]", "Sharpe Ratio", "# Trades",
]

_VERDICT_THRESHOLDS = {
    "SQN":           (1.6, 1.0, 0.0),   # strong / ok / weak
    "Profit Factor": (1.5, 1.2, 1.0),
    "Sharpe Ratio":  (1.0, 0.5, 0.0),
}


def _verdict(val: float, col: str) -> str:
    """Return a short verdict string based on value and column."""
    thresholds = _VERDICT_THRESHOLDS.get(col)
    if thresholds is None or pd.isna(val):
        return ""
    strong, ok, _ = thresholds
    if val >= strong:
        return "🟢 strong"
    if val >= ok:
        return "🟡 ok"
    return "🔴 weak"


def _df_to_md(df: pd.DataFrame) -> str:
    """Render a DataFrame as a GitHub-flavoured markdown table."""
    return df.to_markdown(index=True)


def _gate_bottleneck(per_pair: pd.DataFrame, all_symbols: list[str]) -> str:
    """Identify which gate is blocking the most pairs."""
    lines: list[str] = []
    for gate_col in ("SQN", "Profit Factor", "# Trades", "Win Rate [%]"):
        if gate_col not in per_pair.columns:
            continue
        failing = per_pair[per_pair["Pass"] == "❌"]
        # How many distinct symbols are blocked uniquely by this column being low?
        n_fail = len(failing["Symbol"].unique())
        lines.append(f"- **{gate_col}**: {n_fail} pair(s) failing")
    return "\n".join(lines) if lines else "_No breakdown available._"


def build_report(
    csv_path: Path,
    ranked_all: pd.DataFrame,
    ranked_passing: pd.DataFrame,
    per_pair: pd.DataFrame,
    df_raw: pd.DataFrame,
    gates: dict,
    chosen_pairs: list[str],
) -> str:
    """Return the full markdown report as a string."""
    now        = datetime.now().strftime("%Y-%m-%d %H:%M")
    sweep_name = csv_path.parent.name
    all_symbols = sorted(df_raw["Symbol"].str.strip().unique())
    n_combos   = len(df_raw["_label"].unique()) if "_label" in df_raw.columns else "?"
    n_passing  = len(ranked_all)

    lines: list[str] = []

    # ── Header ────────────────────────────────────────────────────────────────
    lines += [
        f"# Bear Strategy — Sweep Analysis Report",
        f"",
        f"**Generated:** {now}  ",
        f"**Sweep run:** `{sweep_name}`  ",
        f"**File:** `{csv_path}`  ",
        f"",
        f"---",
        f"",
    ]

    # ── Gates used ────────────────────────────────────────────────────────────
    lines += [
        f"## Pass / Fail Gates",
        f"",
        f"| Gate | Value |",
        f"|------|-------|",
        f"| Min SQN | {gates['min_sqn']} |",
        f"| Min Profit Factor | {gates['min_pf']} |",
        f"| Min Trades | {gates['min_trades']} |",
        f"| Min Win Rate % | {gates['min_wr']} |",
        f"| Min Pairs Passing | {gates['min_pairs']} |",
        f"",
        f"**Universe tested:** {', '.join(all_symbols)} ({len(all_symbols)} pairs)  ",
        f"**Pairs included in this run:** {', '.join(chosen_pairs)}  ",
        f"**Total combos in sweep:** {n_combos}  ",
        f"",
        f"---",
        f"",
    ]

    # ── Executive summary ─────────────────────────────────────────────────────
    lines += [
        f"## Executive Summary",
        f"",
    ]

    if ranked_all.empty:
        lines += [
            f"> ⚠️  **No combo cleared all gates.**  Consider relaxing the thresholds.",
            f"",
        ]
    else:
        best = ranked_passing.iloc[0]
        pairs_col = next(c for c in best.index if c.startswith("Pairs"))
        sqn_val   = best.get("Avg SQN", float("nan"))
        pf_val    = best.get("Avg Profit Factor", float("nan"))
        sh_val    = best.get("Avg Sharpe Ratio", float("nan"))
        ret_val   = best.get("Avg Return [%]", float("nan"))

        lines += [
            f"- **{n_passing}** combo(s) cleared the gates out of {n_combos} tested.",
            f"- **Top combo (passing-pairs avg):** {best['Signature']}",
            f"  - Breadth Score: `{best['Breadth Score']}`",
            f"  - Pairs: {best[pairs_col]}",
            f"  - Avg Return: `{ret_val:.2f}%`  |  SQN: `{sqn_val:.3f}` {_verdict(sqn_val, 'SQN')}",
            f"  - Profit Factor: `{pf_val:.3f}` {_verdict(pf_val, 'Profit Factor')}  |  Sharpe: `{sh_val:.3f}` {_verdict(sh_val, 'Sharpe Ratio')}",
            f"",
        ]

    lines += [f"---", f""]

    # ── Ranked tables ─────────────────────────────────────────────────────────
    if not ranked_all.empty:
        lines += [
            f"## Ranked Combos",
            f"",
            f"### All pairs averaged",
            f"",
            _df_to_md(ranked_all),
            f"",
            f"### Passing pairs averaged",
            f"",
            _df_to_md(ranked_passing),
            f"",
            f"---",
            f"",
        ]

        # ── Per-combo pair breakdown (top 3) ──────────────────────────────────
        lines += [
            f"## Per-Pair Breakdown (Top 3 Combos)",
            f"",
        ]

        for sig in ranked_passing["Signature"].head(3).tolist():
            detail = per_pair[per_pair["Signature"] == sig].copy()
            detail = detail.sort_values("Pass", ascending=False).reset_index(drop=True)
            passing = detail[detail["Pass"] == "✅"]["Symbol"].tolist()
            failing = detail[detail["Pass"] == "❌"]["Symbol"].tolist()

            display_cols = ["Symbol", "Pass", "Score"] + [
                c for c in _DETAIL_COLS if c in detail.columns
            ]
            tbl = detail[[c for c in display_cols if c in detail.columns]]

            lines += [
                f"### {sig}",
                f"",
                f"- ✅ **Passing:** {', '.join(passing) if passing else '—'}",
                f"- ❌ **Failing:** {', '.join(failing) if failing else '—'}",
                f"",
                _df_to_md(tbl),
                f"",
            ]

        lines += [f"---", f""]

    # ── Gate bottleneck analysis ───────────────────────────────────────────────
    lines += [
        f"## Gate Bottleneck Analysis",
        f"",
        f"_Pairs failing across all combos by gate (rough count — a pair can fail multiple gates):_",
        f"",
        _gate_bottleneck(per_pair, all_symbols),
        f"",
        f"---",
        f"",
    ]

    # ── SL / TP pivot (Return and SQN) ────────────────────────────────────────
    if "_label" in df_raw.columns:
        lines += [f"## SL × TP Pivot Tables (all pairs, all combos)", f""]
        for metric in ("Return [%]", "SQN", "Profit Factor"):
            if metric not in df_raw.columns:
                continue
            piv = df_raw.pivot_table(
                index="sl_mult", columns="tp_mult", values=metric, aggfunc="mean"
            ).round(3)
            piv.index.name = f"SL \\ {metric}"
            lines += [
                f"### Avg {metric}",
                f"",
                piv.to_markdown(),
                f"",
            ]
        lines += [f"---", f""]

    # ── Footer ────────────────────────────────────────────────────────────────
    lines += [
        f"## Notes",
        f"",
        f"- This report is generated from in-sample or out-of-sample sweep data.",
        f"  Always validate top combos on the **opposite window** before trading.",
        f"- Breadth Score = avg\\_score × (passing\\_pairs / total\\_pairs).",
        f"  A combo that profits on 8/9 pairs with moderate edge outscores one",
        f"  that dominates on 2 pairs.",
        f"- See `TRANSLATION_GUIDE.md` for the full hypothesis-test → backtest pipeline.",
        f"",
        f"_Report end._",
    ]

    return "\n".join(lines)


def save_report(report_md: str, csv_path: Path) -> Path:
    """Write the report to the same directory as the sweep CSV."""
    out = csv_path.parent / "analysis_report.md"
    out.write_text(report_md, encoding="utf-8")
    return out
