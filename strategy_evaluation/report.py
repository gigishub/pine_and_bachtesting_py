"""ASCII CLI report formatting and Markdown file output."""

from __future__ import annotations

import math
from collections import defaultdict
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

# ── Toggle categories (mirrors streamlit_app.py) ──────────────────────────────
_TOGGLE_CATEGORIES: dict[str, list[str]] = {
    "Regime": [
        "adx", "mvrv", "ema", "ribbon", "ma_align", "ma_ribbon", "trend",
        "regime", "htf", "higher_tf", "bull", "bear", "market",
        "rsi_regime", "atr_regime", "vix", "hurst",
        "moving_avg", "moving_average", "sma_align", "dema", "tema",
    ],
    "Setup": [
        "donchian", "channel", "breakout", "squeeze", "bb_squeeze",
        "vah", "val", "vpoc", "volume_profile", "value_area", "lvn",
        "rel_strength", "relative_strength", "ratio", "btc_ratio",
        "structure", "swing", "pattern", "level", "zone",
        "support", "resistance", "consol", "consolidat",
    ],
    "Execution Trigger": [
        "cmf", "chaikin", "cvd", "delta", "order_flow",
        "power_candle", "power_bar", "volume_spike", "vol_spike",
        "trigger", "entry", "signal", "confirm",
        "rsi", "stoch", "macd", "cross", "crossover",
        "engulf", "candle", "bar_pattern", "momentum",
        "diver", "divergen",
    ],
}
_CATEGORY_ORDER = ["Regime", "Setup", "Execution Trigger", "Risk & Exit"]


def _cat(col: str) -> str:
    """Return the strategy phase for a toggle column name."""
    name = col.removeprefix("use_").lower()
    for phase in ("Regime", "Setup", "Execution Trigger"):
        for kw in _TOGGLE_CATEGORIES[phase]:
            if kw in name:
                return phase
    return "Risk & Exit"


def _group_by_category(items: list[str]) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = defaultdict(list)
    for item in items:
        groups[_cat(item)].append(item)
    return dict(groups)


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
        h("Passing Criteria", 2)

        def _tv(x: object) -> object:
            return x[0] if isinstance(x, tuple) else x

        sqn_v = _tv(thresholds.get("Min SQN",            0))
        pf_v  = _tv(thresholds.get("Min Profit Factor",  0))
        tr_v  = _tv(thresholds.get("Min # Trades",       0))
        wr_v  = _tv(thresholds.get("Min Win Rate (%)",   0))
        sh_v  = _tv(thresholds.get("Min Sharpe",         0))
        dd_v  = _tv(thresholds.get("Max Drawdown (%)",   0))
        floor = cfg.min_combo_pass_rate if cfg is not None else 0.20
        lines.append("```")
        lines.append("combo passes if:")
        lines.append(f"  SQN ≥ {sqn_v}  AND  PF ≥ {pf_v}  AND  trades ≥ {tr_v}")
        lines.append(f"  AND  win_rate ≥ {wr_v}%  AND  sharpe ≥ {sh_v}  AND  max_dd ≤ {dd_v}%")
        lines.append("")
        lines.append(f"symbol/TF ✅  if  pass_rate ≥ {floor:.0%}  of its combos")
        lines.append("```")

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
    _freq_groups = _group_by_category(list(result.toggle_frequency.keys()))
    for _phase in _CATEGORY_ORDER:
        _phase_toggles = _freq_groups.get(_phase, [])
        if not _phase_toggles:
            continue
        h(_phase, 3)
        lines.append("| Toggle | Count |")
        lines.append("|--------|-------|")
        for toggle in _phase_toggles:
            lines.append(f"| {toggle} | {result.toggle_frequency[toggle]} |")

    if importance is not None:
        h("Toggle Importance (RandomForest)", 2)
        lines.append(
            f"_Target: `{importance.target_col}` | "
            f"OOB R²: {importance.r2_score:.3f} | "
            f"Trained on {importance.n_combos:,} combos._\n"
        )
        _imp_groups = _group_by_category(list(importance.importances.index))
        for _phase in _CATEGORY_ORDER:
            _phase_ts = _imp_groups.get(_phase, [])
            if not _phase_ts:
                continue
            h(_phase, 3)
            lines.append("| Toggle | Importance |")
            lines.append("|--------|-----------|")
            for toggle in _phase_ts:
                lines.append(f"| {toggle} | {float(importance.importances[toggle]):.4f} |")

    if shap is not None:
        h("Toggle Impact (SHAP)", 2)
        lines.append(
            f"_Target: `{shap.target_col}` | "
            f"n={shap.n_combos:,} combos._\n"
        )
        lines.append(
            "_+ = toggle ON raises SQN.  − = toggle ON lowers SQN._\n"
        )
        _shap_groups = _group_by_category(list(shap.mean_shap.index))
        for _phase in _CATEGORY_ORDER:
            _phase_ts = _shap_groups.get(_phase, [])
            if not _phase_ts:
                continue
            h(_phase, 3)
            lines.append("| Toggle | Mean SHAP | Direction |")
            lines.append("|--------|-----------|-----------|")
            for toggle in _phase_ts:
                val = float(shap.mean_shap[toggle])
                direction = "↑" if val > 0 else "↓"
                lines.append(f"| {toggle} | {val:.4f} | {direction} |")

    if toggle_consensus is not None and not toggle_consensus.empty:
        h("Toggle Consensus", 2)
        lines.append(
            "_Freq = % of top combos this toggle is ON.  "
            "OLS Coeff = avg SQN change when ON.  "
            "SHAP Mean = RF-predicted SQN impact._\n"
        )
        _tc_groups = _group_by_category(toggle_consensus["toggle"].tolist())
        for _phase in _CATEGORY_ORDER:
            _phase_ts = _tc_groups.get(_phase, [])
            if not _phase_ts:
                continue
            h(_phase, 3)
            lines.append("| Toggle | Freq | OLS Coeff | OLS Sig | SHAP Mean | Consensus |")
            lines.append("|--------|------|-----------|---------|-----------|-----------|")
            for _, r in toggle_consensus[toggle_consensus["toggle"].isin(_phase_ts)].iterrows():
                freq_str    = f"{r['freq_pct']:.0%}"
                ols_str     = _fmt(r["ols_coeff"]) if pd.notna(r["ols_coeff"]) else "—"
                ols_sig_str = "✅" if r["ols_sig"] else "⚠️"
                shap_str    = _fmt(r["shap_mean"]) if pd.notna(r["shap_mean"]) else "—"
                lines.append(
                    f"| {r['toggle']} | {freq_str} | {ols_str} | {ols_sig_str} | {shap_str} | {r['consensus']} |"
                )

    if ols is not None:
        h("Toggle Significance (OLS)", 2)
        lines.append(
            f"_Target: `{ols.target_col}` | R²: {ols.r_squared:.3f} | "
            f"n={ols.n_combos:,} combos._\n"
        )
        lines.append("_coeff > 0 → ON raises SQN.  ✅ p < 0.05 = real effect._\n")
        _ols_groups = _group_by_category(ols.table["toggle"].tolist())
        for _phase in _CATEGORY_ORDER:
            _phase_ts = _ols_groups.get(_phase, [])
            if not _phase_ts:
                continue
            h(_phase, 3)
            lines.append("| Toggle | Coefficient | p-value | Significant |")
            lines.append("|--------|-------------|---------|-------------|")
            for _, r in ols.table[ols.table["toggle"].isin(_phase_ts)].iterrows():
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
