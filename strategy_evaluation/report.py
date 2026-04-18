"""ASCII CLI report formatting and Markdown file output."""

from __future__ import annotations

import math
from datetime import datetime
from pathlib import Path

import pandas as pd

from strategy_evaluation.config import RobustnessConfig
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
    sweep_results: dict[str, tuple[pd.DataFrame, float]] | None = None,
    toggle_consensus: pd.DataFrame | None = None,
    combo_summary: dict[str, int] | None = None,
    df: pd.DataFrame | None = None,
    cfg: RobustnessConfig | None = None,
) -> str:
    """Build a full ASCII/Markdown report string from a RobustnessResult.

    Parameters
    ----------
    sweep_results:
        Optional dict mapping metric label (e.g. ``"SQN"``) to a tuple of
        ``(sweep_df, current_threshold)`` where *sweep_df* has columns
        ``threshold``, ``symbol_pass_rate``, ``tf_pass_rate``.
    combo_summary:
        Optional dict with keys ``n_total``, ``n_passing``, ``n_symbols``,
        ``n_timeframes``, ``n_param_sets``.  Used to build the Combo Summary
        section explaining how the total combo count is derived.
    df:
        Optional raw results DataFrame (with ``_passes`` column from
        ``annotate_dataframe``).  When provided, Symbol and Timeframe
        Consistency sections show actual combo pass rates instead of the
        binary pass/fail verdict from ``RobustnessResult``.
    """
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

    if combo_summary:
        n_total     = combo_summary.get("n_total", 0)
        n_passing   = combo_summary.get("n_passing", 0)
        n_symbols   = combo_summary.get("n_symbols", 0)
        n_tfs       = combo_summary.get("n_timeframes", 0)
        n_params    = combo_summary.get("n_param_sets", 0)
        pct         = n_passing / n_total if n_total else 0
        h("Combo Summary", 2)
        lines.append(
            f"- **Total combos:** {n_total:,}  "
            f"({n_symbols} symbols × {n_tfs} timeframes × {n_params} parameter sets)"
        )
        lines.append(
            f"- **Passing combos:** {n_passing:,}  ({pct:.1%} of total, with current thresholds)"
        )

    # ── Symbol Consistency ────────────────────────────────────────────────────
    h("Symbol Consistency", 2)
    if df is not None and cfg is not None and "_passes" in df.columns and cfg.col_symbol in df.columns:
        col_sym      = cfg.col_symbol
        n_total_df   = len(df)
        n_syms_df    = df[col_sym].nunique()
        n_per_coin   = n_total_df // n_syms_df if n_syms_df else 0
        combo_rates  = df.groupby(col_sym)["_passes"].mean()
        floor        = cfg.min_combo_pass_rate
        lines.append(
            f"_Combo pass rate per coin (all timeframes combined). "
            f"100% = {n_per_coin} combos. Floor: ≥ {floor:.0%} → ✅_\n"
        )
        lines.append("| Symbol | Pass Rate | Status |")
        lines.append("|--------|-----------|--------|")
        for sym in sorted(combo_rates.index):
            rate = float(combo_rates[sym])
            icon_s = "✅" if rate >= floor else "❌"
            lines.append(f"| {sym} | {rate:.0%} | {icon_s} |")
    else:
        lines.append("| Symbol | Passes |")
        lines.append("|--------|--------|")
        for sym, rate in sorted(result.symbol_pass_rates.items()):
            icon_s = "✅" if rate > 0 else "❌"
            lines.append(f"| {sym} | {icon_s} |")

    # ── Timeframe Consistency ──────────────────────────────────────────────────
    h("Timeframe Consistency", 2)
    if (
        df is not None and cfg is not None
        and "_passes" in df.columns
        and cfg.col_symbol in df.columns
        and cfg.col_timeframe in df.columns
    ):
        col_sym   = cfg.col_symbol
        col_tf    = cfg.col_timeframe
        floor     = cfg.min_combo_pass_rate
        n_syms_df = df[col_sym].nunique()
        n_tfs_df  = df[col_tf].nunique()
        n_per_cpt = len(df) // (n_syms_df * n_tfs_df) if (n_syms_df * n_tfs_df) else 0
        timeframes = sorted(df[col_tf].unique())

        lines.append(
            f"_Per-coin combo pass rate per timeframe. "
            f"100% = {n_per_cpt} combos per coin per TF. Floor: ≥ {floor:.0%} → ✅_\n"
        )

        # Header row
        tf_headers = " | ".join(str(tf) for tf in timeframes)
        tf_sep     = " | ".join("---" for _ in timeframes)
        lines.append(f"| Symbol | {tf_headers} |")
        lines.append(f"|--------|{tf_sep}|")

        all_symbols = sorted(df[col_sym].unique())
        coin_tf_pass: dict[str, list[str]] = {sym: [] for sym in all_symbols}
        tf_rates_map: dict[str, dict[str, float]] = {}
        for tf in timeframes:
            tf_df      = df[df[col_tf] == tf]
            coin_rates = tf_df.groupby(col_sym)["_passes"].mean()
            tf_rates_map[str(tf)] = {sym: float(coin_rates.get(sym, 0)) for sym in all_symbols}
            for sym in all_symbols:
                if coin_rates.get(sym, 0) >= floor:
                    coin_tf_pass[sym].append(str(tf))

        for sym in all_symbols:
            cells = []
            for tf in timeframes:
                rate   = tf_rates_map[str(tf)].get(sym, 0)
                icon_s = "✅" if rate >= floor else "❌"
                cells.append(f"{rate:.0%} {icon_s}")
            lines.append(f"| {sym} | {' | '.join(cells)} |")

        # Coverage summary
        lines.append("")
        lines.append("**TF Coverage per coin:**")
        from collections import defaultdict
        by_count: dict[int, list[str]] = defaultdict(list)
        for sym in all_symbols:
            by_count[len(coin_tf_pass[sym])].append(sym)
        for count in sorted(by_count.keys(), reverse=True):
            group = sorted(by_count[count])
            if count == n_tfs_df:
                lines.append(f"- ✅ All {n_tfs_df} TFs: {', '.join(group)}")
            elif count == 0:
                lines.append(f"- ❌ 0 TFs: {', '.join(group)}")
            else:
                lines.append(f"- ⚠️ {count}/{n_tfs_df} TFs: {', '.join(group)}")
    else:
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
            "Positive = enabling helps (raises SQN). Negative = enabling hurts (lowers SQN)._\n"
        )
        lines.append("| Toggle | Mean SHAP | Direction |")
        lines.append("|--------|-----------|-----------|")
        for toggle in shap.abs_mean_shap.index:
            val = float(shap.mean_shap[toggle])
            direction = "↑ positive" if val > 0 else "↓ negative"
            lines.append(f"| {toggle} | {val:.4f} | {direction} |")

    if toggle_consensus is not None and not toggle_consensus.empty:
        h("Toggle Consensus", 2)
        lines.append(
            "_Cross-check: frequency in passing combos vs OLS coefficient vs SHAP direction. "
            "All three signals must agree for a strong recommendation._\n"
        )
        lines.append("| Toggle | Freq (top combos) | OLS Coeff | OLS Sig | SHAP Mean | Consensus |")
        lines.append("|--------|-------------------|-----------|---------|-----------|-----------|")
        for _, r in toggle_consensus.iterrows():
            freq_str = f"{r['freq_pct']:.0%}"
            ols_str = _fmt(r["ols_coeff"]) if pd.notna(r["ols_coeff"]) else "—"
            ols_sig_str = "✅" if r["ols_sig"] else "⚠️"
            shap_str = _fmt(r["shap_mean"]) if pd.notna(r["shap_mean"]) else "—"
            lines.append(
                f"| {r['toggle']} | {freq_str} | {ols_str} | {ols_sig_str} | {shap_str} | {r['consensus']} |"
            )

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

    if sweep_results:
        h("Threshold Sweep", 2)
        if combo_summary:
            _n_syms  = combo_summary.get("n_symbols", "?")
            _n_tfs   = combo_summary.get("n_timeframes", "?")
            _n_tot   = combo_summary.get("n_total", 0)
            _n_prc   = (_n_tot // _n_syms) if isinstance(_n_syms, int) and _n_syms else "?"
            _floor   = f"{cfg.min_combo_pass_rate:.0%}" if cfg is not None else "20%"
            lines.append(
                f"_Symbol Pass Rate = % of {_n_syms} coins where ≥ {_floor} of the coin's "
                f"{_n_prc} combos (all {_n_tfs} TFs pooled) pass the threshold.  "
                f"◀ current = value active when this report was saved._\n"
            )
        else:
            lines.append(
                "_Symbol pass rate as each threshold is varied.  "
                "◀ current = active threshold._\n"
            )
        for metric_label, (sweep_df, active_val) in sweep_results.items():
            h(f"Sweep — Min {metric_label}", 3)
            lines.append(f"| Min {metric_label} | Symbol pass rate | |")
            lines.append("|---|---|---|")
            _closest = min(sweep_df["threshold"], key=lambda x: abs(float(x) - active_val))
            for _, r in sweep_df.iterrows():
                t      = float(r["threshold"])
                sym    = float(r["symbol_pass_rate"])
                marker = " ◀ current" if abs(t - float(_closest)) < 1e-9 else ""
                lines.append(f"| {t:.3g} | {sym:.0%} |{marker} |")

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
