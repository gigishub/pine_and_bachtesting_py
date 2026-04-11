"""ASCII CLI report formatting and Markdown file output."""

from __future__ import annotations

import math
from datetime import datetime
from pathlib import Path

import pandas as pd

from strategy_evaluation.importance import ImportanceResult, ShapResult
from strategy_evaluation.scorer import RobustnessResult
from strategy_evaluation.significance import OLSResult

_VERDICT_ICONS = {
    "ROBUST": "✅",
    "MARGINAL": "⚠️",
    "WEAK": "❌",
}


def format_report(
    result: RobustnessResult,
    label: str = "Strategy",
    results_path: str | pd.DataFrame = "",
    importance: ImportanceResult | None = None,
    shap: ShapResult | None = None,
    ols: OLSResult | None = None,
    top_combos: pd.DataFrame | None = None,
    thresholds: dict[str, object] | None = None,
    data_period: tuple[str, str] | None = None,
) -> str:
    """Build a full ASCII/Markdown report string from a RobustnessResult."""
    icon = _VERDICT_ICONS.get(result.verdict, "")
    lines: list[str] = []

    def h(text: str, level: int = 2) -> None:
        lines.append(f"\n{'#' * level} {text}")

    def row(k: str, v: str) -> None:
        lines.append(f"- **{k}**: {v}")

    lines.append(f"# {icon} Robustness Report — {label}")
    lines.append(f"\n_Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n")
    if results_path:
        lines.append(f"- Results: `{results_path}`")
    if data_period:
        lines.append(f"- Data period: **{data_period[0]}** → **{data_period[1]}**")

    if thresholds:
        h("Thresholds Used", 2)
        lines.append("| Threshold | Value | What it means |")
        lines.append("|-----------|-------|----------------|")
        for name, val in thresholds.items():
            if isinstance(val, tuple):
                value, comment = val
            else:
                value, comment = val, ""
            lines.append(f"| {name} | **{value}** | {comment} |")

    h("Verdict", 2)
    lines.append(f"\n**{icon} {result.verdict}**\n")
    for note in result.notes:
        lines.append(f"- {note}")

    h("Key Metrics", 2)
    row("Symbol pass rate", f"{result.symbol_rate:.0%} ({sum(1 for v in result.symbol_pass_rates.values() if v > 0)}/{len(result.symbol_pass_rates)} symbols)")
    row("Timeframe pass rate", f"{result.tf_rate:.0%}")
    row("Avg SQN (top-1 per symbol/TF)", _fmt(result.avg_sqn_long))

    h("Symbol Consistency", 2)
    lines.append("| Symbol | Passes |")
    lines.append("|--------|--------|")
    for sym, rate in sorted(result.symbol_pass_rates.items()):
        icon_s = "✅" if rate > 0 else "❌"
        lines.append(f"| {sym} | {icon_s} |")

    h("Timeframe Consistency", 2)
    lines.append("| Timeframe | Pass Rate |")
    lines.append("|-----------|-----------|")
    for tf, rate in sorted(result.tf_pass_rates.items()):
        lines.append(f"| {tf} | {rate:.0%} |")

    h("Top Toggle Frequency (top-5 combos per symbol/TF)", 2)
    lines.append("_Toggles that appear most in top-ranked combos are likely the most impactful filters._\n")
    lines.append("| Toggle | Count |")
    lines.append("|--------|-------|")
    for toggle, count in list(result.toggle_frequency.items())[:15]:
        lines.append(f"| {toggle} | {count} |")

    if importance is not None:
        h("Toggle Importance (RandomForest)", 2)
        lines.append(
            f"_Target: `{importance.target_col}` | "
            f"OOB R²: {importance.r2_score:.3f} | "
            f"Trained on {importance.n_combos:,} combos._\n"
        )
        lines.append("_Higher importance = that toggle explains more variance in the target metric._\n")
        lines.append("| Toggle | Importance |")
        lines.append("|--------|-----------|")
        for toggle, imp in importance.importances.items():
            lines.append(f"| {toggle} | {imp:.4f} |")

    if shap is not None:
        h("Toggle Impact (SHAP)", 2)
        lines.append(
            f"_Target: `{shap.target_col}` | "
            f"n={shap.n_combos:,} combos._\n"
        )
        lines.append(
            "_Mean SHAP = average change in predicted SQN when this toggle is ON. "
            "Positive = enabling hurts, negative = enabling helps (sign is relative to baseline)._\n"
        )
        lines.append("| Toggle | Mean SHAP | Direction |")
        lines.append("|--------|-----------|-----------|")
        for toggle in shap.abs_mean_shap.index:
            val = float(shap.mean_shap[toggle])
            direction = "↑ positive" if val > 0 else "↓ negative"
            lines.append(f"| {toggle} | {val:.4f} | {direction} |")

    if ols is not None:
        h("Toggle Significance (OLS)", 2)
        lines.append(
            f"_Target: `{ols.target_col}` | R²: {ols.r_squared:.3f} | "
            f"n={ols.n_combos:,} combos._\n"
        )
        lines.append(
            "_Coefficient = average change in SQN when toggle is ON. "
            "✅ = p < 0.05 (statistically significant). ⚠️ = p ≥ 0.05 (possible noise)._\n"
        )
        lines.append("| Toggle | Coefficient | p-value | Significant |")
        lines.append("|--------|-------------|---------|-------------|")
        for _, r in ols.table.iterrows():
            sig = "✅" if r["significant"] else "⚠️"
            lines.append(
                f"| {r['toggle']} | {_fmt(r['coefficient'])} "
                f"| {float(r['p_value']):.4f} | {sig} |"
            )

    if top_combos is not None and not top_combos.empty:
        h("Top Passing Combos", 2)
        lines.append(
            "_All combos that passed every threshold, sorted by composite score "
            "(SQN + Profit Factor + Sharpe combined). "
            "These are the setups to carry forward to walk-forward testing._\n"
        )
        display_cols = [
            "Symbol", "Timeframe", "Parameter Signature",
            "_score", "SQN", "Profit Factor", "# Trades",
            "Win Rate [%]", "Sharpe Ratio", "Return [%]",
        ]
        cols = [c for c in display_cols if c in top_combos.columns]
        sorted_df = top_combos[cols].sort_values("_score", ascending=False).reset_index(drop=True)
        # Markdown table header
        lines.append("| " + " | ".join(cols) + " |")
        lines.append("| " + " | ".join(["---"] * len(cols)) + " |")
        for _, row in sorted_df.iterrows():
            cells = []
            for c in cols:
                v = row[c]
                if isinstance(v, float):
                    cells.append(f"{v:.2f}")
                else:
                    cells.append(str(v))
            lines.append("| " + " | ".join(cells) + " |")

    return "\n".join(lines)


def save_report(
    report_str: str,
    label: str = "strategy",
    output_dir: Path | str | None = None,
) -> Path:
    """Save *report_str* to a timestamped Markdown file and return the path.

    Parameters
    ----------
    report_str:
        The full report text.
    label:
        Strategy label used in the filename.
    output_dir:
        Directory to write into.  Defaults to the ``strategy_evaluation/reports/``
        folder inside the package.  Pass the backtest results directory to keep
        the report co-located with the CSV data.
    """
    if output_dir is not None:
        dest = Path(output_dir)
    else:
        dest = Path(__file__).parent / "reports"
    dest.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    filename = f"{timestamp}_{label}_robustness.md"
    path = dest / filename
    path.write_text(report_str, encoding="utf-8")
    return path


def _fmt(value: object) -> str:
    try:
        f = float(value)  # type: ignore[arg-type]
        if math.isnan(f):
            return "—"
        return f"{f:.2f}"
    except (TypeError, ValueError):
        return str(value) if value is not None else "—"
