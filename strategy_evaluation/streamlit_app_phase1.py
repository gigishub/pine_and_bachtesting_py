"""Streamlit Phase 1 dashboard — exclusive-mode sweep analysis.

Covers sections 1–5 (mapped from original §1, 2, 3, 8, 9).
Zero dependency on sklearn, shap, statsmodels, importance.py, significance.py,
scorer.py, or report.py.

Run with:
    streamlit run strategy_evaluation/streamlit_app_phase1.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure the project root is on sys.path so `strategy_evaluation` is importable
# regardless of the working directory when `streamlit run` is invoked.
sys.path.insert(0, str(Path(__file__).parent.parent))

from collections import defaultdict
from datetime import datetime

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from strategy_evaluation.config import RobustnessConfig
from strategy_evaluation.consistency import (
    sweep_threshold,
    symbol_pass_rate,
    timeframe_pass_rate,
    toggle_frequency,
)
from strategy_evaluation.loader import load_data_period, load_run_dir, validate_columns
from strategy_evaluation.metrics import annotate_dataframe

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Strategy Robustness — Phase 1",
    page_icon="📊",
    layout="wide",
)


# ── Helpers ──────────────────────────────────────────────────────────────────

def _info(text: str, label: str = "ℹ️ How to read this") -> None:
    with st.expander(label):
        st.markdown(text)


# ── Toggle categorisation ────────────────────────────────────────────────────
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
    "Risk & Exit": [
        "sl", "tp", "trail", "trailing", "exit", "risk",
        "stoploss", "stop_loss", "stop", "takeprofit", "take_profit",
        "chandelier", "atr_exit", "atr_trail", "atr_stop",
        "psar", "sar", "parabolic",
        "bb_exit", "bollinger_exit", "bb_close",
        "drawdown", "position", "size", "sizing",
        "breakeven", "break_even", "be_stop",
    ],
}
_CATEGORY_ORDER = ["Regime", "Setup", "Execution Trigger", "Risk & Exit"]
_CATEGORY_COLOURS = {
    "Regime":             "#3498db",
    "Setup":              "#f39c12",
    "Execution Trigger":  "#2ecc71",
    "Risk & Exit":        "#e74c3c",
}


def _categorize_toggle(col: str) -> str:
    """Map a ``use_*`` column name to its strategy phase."""
    name = col.removeprefix("use_").lower()
    for cat in ("Regime", "Setup", "Execution Trigger"):
        for kw in _TOGGLE_CATEGORIES[cat]:
            if kw in name:
                return cat
    return "Risk & Exit"


def _add_category_col(df: pd.DataFrame, toggle_col: str = "Toggle") -> pd.DataFrame:
    """Insert a 'Category' column in *df* based on the *toggle_col* values."""
    df = df.copy()
    df.insert(0, "Category", df[toggle_col].apply(_categorize_toggle))
    return df


# ── Section renderers ─────────────────────────────────────────────────────────

def _section_overall_symbol(cfg: RobustnessConfig, df: pd.DataFrame) -> None:
    """Section 1 — overall combo pass rate per coin across ALL timeframes combined."""
    n_total    = len(df)
    n_symbols  = df[cfg.col_symbol].nunique()
    n_tfs      = df[cfg.col_timeframe].nunique()
    n_params   = n_total // (n_symbols * n_tfs) if (n_symbols * n_tfs) else 0
    n_per_coin = n_total // n_symbols if n_symbols else 0
    floor      = cfg.min_combo_pass_rate

    _info(
        f"```\n"
        f"data: {n_symbols} coins × {n_tfs} TFs × {n_params} params = {n_total:,} combos\n"
        f"bar:  n_pass / {n_per_coin} combos per coin  (all TFs pooled)\n"
        f"floor ≥ {floor:.0%}  →  coin ✅  |  below → coin ❌\n"
        f"```\n"
        f"⚙️ `SQN≥{cfg.min_sqn}  PF≥{cfg.min_profit_factor}  trades≥{cfg.min_trades}  "
        f"win%≥{cfg.min_win_rate:.0f}  sharpe≥{cfg.min_sharpe}  max_dd≤{cfg.max_max_drawdown:.0f}%`"
    )

    combo_rates = (
        df.groupby(cfg.col_symbol)["_passes"].mean()
        if "_passes" in df.columns
        else pd.Series(dtype=float)
    )
    rows = []
    for sym in sorted(combo_rates.index):
        n_sym_total = int((df[cfg.col_symbol] == sym).sum())
        n_sym_pass  = int(df[df[cfg.col_symbol] == sym]["_passes"].sum()) if "_passes" in df.columns else 0
        rows.append({
            "Symbol": sym,
            "Combo pass rate": float(combo_rates.get(sym, 0)),
            "n_total": n_sym_total,
            "n_pass":  n_sym_pass,
        })
    df_plot = pd.DataFrame(rows)
    df_plot["Status"] = df_plot["Combo pass rate"].apply(
        lambda r: "✅ Pass" if r >= floor else "❌ Fail"
    )

    fig = px.bar(
        df_plot, x="Symbol", y="Combo pass rate",
        color="Status",
        color_discrete_map={"✅ Pass": "#2ecc71", "❌ Fail": "#e74c3c"},
        title=f"Overall combo pass rate per coin  (all {n_tfs} TFs combined)",
        labels={"Combo pass rate": f"Pass rate  (100% = {n_per_coin} combos)"},
        custom_data=["n_total", "n_pass"],
    )
    fig.update_traces(
        hovertemplate="%{x}: %{customdata[1]} / %{customdata[0]} pass  (%{y:.0%})<extra></extra>"
    )
    fig.add_hline(
        y=floor, line_dash="dash", line_color="white",
        annotation_text=f"Floor ({floor:.0%})", annotation_position="top right",
    )
    fig.update_layout(yaxis_range=[0, 1.05], yaxis_tickformat=".0%", showlegend=True)
    st.plotly_chart(fig, use_container_width=True)


def _section_per_tf_charts(cfg: RobustnessConfig, df: pd.DataFrame) -> None:
    """Section 2 — one bar chart per tested timeframe + coverage summary."""
    n_total           = len(df)
    n_symbols         = df[cfg.col_symbol].nunique()
    n_tfs             = df[cfg.col_timeframe].nunique()
    n_params          = n_total // (n_symbols * n_tfs) if (n_symbols * n_tfs) else 0
    n_per_tf          = n_total // n_tfs if n_tfs else 0
    n_per_coin_per_tf = n_per_tf // n_symbols if n_symbols else 0
    floor             = cfg.min_combo_pass_rate
    col_sym           = cfg.col_symbol
    col_tf            = cfg.col_timeframe

    _info(
        f"```\n"
        f"same {n_total:,} combos — split by TF\n"
        f"each TF: {n_symbols} coins × {n_params} params = {n_per_tf:,} combos per TF\n"
        f"bar: n_pass / {n_per_coin_per_tf} combos per (coin, TF)\n"
        f"floor ≥ {floor:.0%}  →  coin/TF ✅  |  below → ❌\n"
        f"```\n"
        f"⚙️ `SQN≥{cfg.min_sqn}  PF≥{cfg.min_profit_factor}  trades≥{cfg.min_trades}  "
        f"win%≥{cfg.min_win_rate:.0f}  sharpe≥{cfg.min_sharpe}  max_dd≤{cfg.max_max_drawdown:.0f}%`"
    )

    timeframes  = sorted(df[col_tf].unique())
    all_symbols = sorted(df[col_sym].unique())
    coin_tf_pass: dict[str, list[str]] = {sym: [] for sym in all_symbols}

    for tf in timeframes:
        tf_df      = df[df[col_tf] == tf]
        coin_rates = (
            tf_df.groupby(col_sym)["_passes"].mean()
            if "_passes" in tf_df.columns
            else pd.Series(dtype=float)
        )
        rows = []
        for sym in all_symbols:
            n_sym_total = int((tf_df[col_sym] == sym).sum())
            n_sym_pass  = int(tf_df[tf_df[col_sym] == sym]["_passes"].sum()) if "_passes" in tf_df.columns else 0
            rate        = float(coin_rates.get(sym, 0))
            passed      = rate >= floor
            if passed:
                coin_tf_pass[sym].append(str(tf))
            rows.append({
                "Symbol": sym,
                "Combo pass rate": rate,
                "n_total": n_sym_total,
                "n_pass":  n_sym_pass,
                "Status":  "✅ Pass" if passed else "❌ Fail",
            })

        df_tf = pd.DataFrame(rows)
        fig = px.bar(
            df_tf, x="Symbol", y="Combo pass rate",
            color="Status",
            color_discrete_map={"✅ Pass": "#2ecc71", "❌ Fail": "#e74c3c"},
            title=f"TF {tf} — combo pass rate per coin  ({n_per_coin_per_tf} combos / coin)",
            labels={"Combo pass rate": f"Pass rate  (100% = {n_per_coin_per_tf} combos)"},
            custom_data=["n_total", "n_pass"],
        )
        fig.update_traces(
            hovertemplate="%{x}: %{customdata[1]} / %{customdata[0]} pass  (%{y:.0%})<extra></extra>"
        )
        fig.add_hline(
            y=floor, line_dash="dash", line_color="white",
            annotation_text=f"Floor ({floor:.0%})", annotation_position="top right",
        )
        fig.update_layout(yaxis_range=[0, 1.05], yaxis_tickformat=".0%", showlegend=True)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Coverage summary")
    coverage_rows = []
    for sym in all_symbols:
        passing_tfs = coin_tf_pass[sym]
        n = len(passing_tfs)
        if n == n_tfs:
            verdict = f"✅ All {n_tfs} TFs"
        elif n == 0:
            verdict = "❌ None"
        else:
            verdict = f"⚠️ {n}/{n_tfs}"
        coverage_rows.append({
            "Coin":        sym,
            "Passing TFs": ", ".join(passing_tfs) if passing_tfs else "—",
            "Count":       f"{n}/{n_tfs}",
            "Verdict":     verdict,
        })
    st.dataframe(pd.DataFrame(coverage_rows), use_container_width=True, hide_index=True)

    by_count: dict[int, list[str]] = defaultdict(list)
    for sym in all_symbols:
        by_count[len(coin_tf_pass[sym])].append(sym)

    for count in sorted(by_count.keys(), reverse=True):
        group = sorted(by_count[count])
        if count == n_tfs:
            st.caption(f"✅ {len(group)} coin(s) pass all {n_tfs} TFs — strongest candidates: {', '.join(group)}")
        elif count == 0:
            st.caption(f"❌ {len(group)} coin(s) pass 0 TFs — skip entirely: {', '.join(group)}")
        else:
            st.caption(f"⚠️ {len(group)} coin(s) pass {count}/{n_tfs} TFs — timeframe-specific: {', '.join(group)}")


def _section_combo_overlap(cfg: RobustnessConfig, df: pd.DataFrame) -> None:
    """Section 2b — for each timeframe, which exact parameter signatures pass on multiple coins?

    Answers: "Does this combo on ETHUSDT 4H also pass on ADAUSDT 4H and SOLUSDT 4H?"
    """
    if "_passes" not in df.columns or not df["_passes"].any():
        st.info("No combos pass the current thresholds — relax the sliders.")
        return

    col_sym = cfg.col_symbol
    col_tf  = cfg.col_timeframe
    col_sig = cfg.col_param_sig

    if col_sig not in df.columns:
        st.warning(f"Column '{col_sig}' not found in CSV — cannot compute combo overlap.")
        return

    all_symbols = sorted(df[col_sym].unique())
    n_coins     = len(all_symbols)

    _info(
        "```\n"
        "rows  = unique parameter signatures (exact toggle combinations)\n"
        "cols  = coins tested on this timeframe\n"
        "cell  = ✅  if that exact combo passes all thresholds on that coin\n"
        "# Coins = total coins where this combo passes simultaneously\n\n"
        "top rows  →  most universal combos  →  strategy holds across multiple markets\n"
        "single ✅  →  coin-specific result  →  may be curve-fitted or asset-specific\n"
        "```"
    )

    min_coins = st.slider(
        "Show combos passing on at least N coins",
        min_value=1,
        max_value=n_coins,
        value=1,
        step=1,
        key="combo_overlap_min_coins",
        help="Set to 2+ to see only combos that are truly cross-coin.",
    )

    passing_df = df[df["_passes"]]
    timeframes = sorted(df[col_tf].unique())

    for tf in timeframes:
        st.markdown(f"#### ⏱ {tf}")
        tf_pass = passing_df[passing_df[col_tf] == tf]

        if tf_pass.empty:
            st.caption(f"No passing combos on {tf} with current thresholds.")
            continue

        # Pivot: rows = signature, cols = symbol → 1 if passes, 0 if not
        pivot = (
            tf_pass.groupby([col_sig, col_sym])
            .size()
            .unstack(fill_value=0)
            .clip(upper=1)
            .astype(int)
        )
        # Ensure every tested coin appears even if none of its combos passed
        for sym in all_symbols:
            if sym not in pivot.columns:
                pivot[sym] = 0
        coin_cols = sorted(all_symbols)
        pivot     = pivot[coin_cols]
        pivot["# Coins"] = pivot[coin_cols].sum(axis=1)
        pivot     = pivot[pivot["# Coins"] >= min_coins].sort_values("# Coins", ascending=False)

        if pivot.empty:
            st.caption(f"No combos pass on ≥ {min_coins} coin(s) on {tf}.")
            continue

        n_multi_coin = int((pivot["# Coins"] > 1).sum())
        n_all_coins  = int((pivot["# Coins"] == n_coins).sum())
        st.caption(
            f"**{len(pivot)}** combos shown  |  "
            f"**{n_multi_coin}** pass on ≥ 2 coins  |  "
            f"**{n_all_coins}** pass on all {n_coins} coins"
        )

        # Heatmap
        heat = pivot[coin_cols]
        fig = px.imshow(
            heat,
            color_continuous_scale=[[0, "#1a1a2e"], [1, "#2ecc71"]],
            aspect="auto",
            title=f"{tf} — combo × coin pass matrix ({len(pivot)} combos)",
            labels={"x": "Coin", "y": "Parameter Signature", "color": "Passes"},
            zmin=0,
            zmax=1,
        )
        fig.update_coloraxes(showscale=False)
        fig.update_xaxes(side="top")
        fig.update_yaxes(tickfont_size=10)
        st.plotly_chart(fig, use_container_width=True)

        # Detailed table: ✅/blank per coin + # Coins
        disp = pd.DataFrame(index=pivot.index)
        for sym in coin_cols:
            disp[sym] = pivot[sym].map({1: "✅", 0: ""})
        disp["# Coins"] = pivot["# Coins"]
        disp.index.name = col_sig
        st.dataframe(disp.reset_index(), use_container_width=True, hide_index=True)


def _section_toggle_frequency(tog_freq: dict[str, int]) -> None:
    """Section 3 — toggle frequency in top-5 combos per symbol/timeframe."""
    _info(
        "```\n"
        "# top-5 combos per (coin, TF) — from passing combos only  ⚙️ threshold-sensitive\n"
        "count = how often toggle is ON in those selections\n\n"
        "count → high  →  toggle in most passing combos  →  likely key ingredient\n"
        "count → low   →  toggle barely appears  →  probably not helping → consider removing\n\n"
        "no clear winner?  →  performance requires very specific combination  →  fragile signal\n"
        "```"
    )
    if not tog_freq:
        st.info("No toggle data available.")
        return
    df_tog = pd.DataFrame(
        [{"Toggle": k, "Count": v} for k, v in tog_freq.items()]
    )
    df_tog = _add_category_col(df_tog)
    df_tog = df_tog.sort_values("Count")
    fig = px.bar(
        df_tog, x="Count", y="Toggle", orientation="h",
        title="Toggle frequency in top-5 combos per symbol/timeframe",
        color="Category",
        color_discrete_map=_CATEGORY_COLOURS,
        category_orders={"Category": _CATEGORY_ORDER},
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)


def _section_top_combos(df: pd.DataFrame, cfg: RobustnessConfig) -> None:
    """Section 4 — all combos that pass current thresholds."""
    _n_pass = int(df["_passes"].sum()) if "_passes" in df.columns else 0
    _n_all  = len(df)
    _info(
        f"```\n"
        f"# combos that pass all thresholds  ({_n_pass} / {_n_all})\n"
        f"SQN ≥ {cfg.min_sqn}  AND  PF ≥ {cfg.min_profit_factor}  AND  trades ≥ {cfg.min_trades}\n"
        f"AND  win_rate ≥ {cfg.min_win_rate:.0f}%  AND  sharpe ≥ {cfg.min_sharpe}  AND  max_dd ≤ {cfg.max_max_drawdown:.0f}%\n\n"
        f"sorted by _score  (composite SQN + PF + Sharpe)\n\n"
        f"< 5 combos  →  relax thresholds\n"
        f"> 50 combos →  tighten thresholds\n"
        f"```"
    )
    view = df[df["_passes"]].copy() if "_passes" in df.columns else df.copy()
    if view.empty:
        st.warning("No combos pass the current thresholds. Try relaxing the sliders.")
        return

    col_a, col_b = st.columns(2)
    sym_options = ["All"] + sorted(view[cfg.col_symbol].unique().tolist())
    tf_options  = ["All"] + sorted(view[cfg.col_timeframe].unique().tolist())
    sel_sym = col_a.selectbox("Filter by Symbol", sym_options)
    sel_tf  = col_b.selectbox("Filter by Timeframe", tf_options)
    if sel_sym != "All":
        view = view[view[cfg.col_symbol] == sel_sym]
    if sel_tf != "All":
        view = view[view[cfg.col_timeframe] == sel_tf]

    show_cols = [
        cfg.col_symbol, cfg.col_timeframe, cfg.col_param_sig, "_score",
        cfg.col_sqn, cfg.col_pf, cfg.col_expectancy,
        cfg.col_trades, cfg.col_win_rate, cfg.col_sharpe,
        cfg.col_max_drawdown, cfg.col_calmar, cfg.col_return,
    ]
    available = [c for c in show_cols if c in view.columns]
    sort_col  = "_score" if "_score" in view.columns else available[0]
    st.dataframe(
        view[available].sort_values(sort_col, ascending=False).reset_index(drop=True),
        use_container_width=True,
    )
    st.caption(f"{len(view)} passing combos shown.")


def _fmt_cell(value: object) -> str:
    """Format a table cell value for Markdown output."""
    if isinstance(value, float):
        return f"{value:.4g}"
    return str(value)


def _format_phase1_report(
    label: str,
    results_dir: str,
    run_ts: str,
    cfg: RobustnessConfig,
    sym_rates: dict[str, float],
    tf_rates: dict[str, float],
    tog_freq: dict[str, int],
    n_total: int,
    n_passing: int,
    n_symbols: int,
    n_timeframes: int,
    n_param_sets: int,
    df: pd.DataFrame | None = None,
    sweep_data: dict[str, tuple[pd.DataFrame, float]] | None = None,
) -> str:
    """Generate a comprehensive Markdown Phase 1 report matching everything visible in the app.

    Sections:
        Header / Passing Criteria / Overview
        §1  Overall Strategy Effectiveness  (per-coin combo pass rates)
        §2  Performance per Timeframe       (per-coin per-TF tables + coverage summary)
        §2b Universal Combos per Timeframe  (cross-coin combo overlap pivot)
        §3  Parameter Stability             (toggle frequency by category)
        §4  Top Passing Combos              (full table sorted by _score)
        §5  Threshold Sweep                 (two-line sweep tables for SQN, PF, # Trades)
    """
    floor      = cfg.min_combo_pass_rate
    pct_pass   = f"{n_passing / n_total:.1%}" if n_total else "—"
    n_per_coin = n_total // n_symbols if n_symbols else 0
    n_per_cpt  = n_total // (n_symbols * n_timeframes) if (n_symbols * n_timeframes) else 0

    lines: list[str] = []

    def h(text: str, level: int = 2) -> None:
        lines.append(f"\n{'#' * level} {text}\n")

    # ── Header ─────────────────────────────────────────────────────────────────
    lines.append(f"# Phase 1 Robustness Report — {label}")
    lines.append(f"\n**Generated:** {run_ts}  \n**Results dir:** `{results_dir}`\n")

    # ── Passing Criteria ───────────────────────────────────────────────────────
    h("Passing Criteria")
    lines.append(
        "> A **combo passes** if ALL thresholds below are met simultaneously.  \n"
        "> A **symbol or timeframe ✅** if ≥ the combo pass rate floor of its combos pass.\n"
    )
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")
    lines.append(f"| Min SQN | {cfg.min_sqn} |")
    lines.append(f"| Min Profit Factor | {cfg.min_profit_factor} |")
    lines.append(f"| Min # Trades | {cfg.min_trades} |")
    lines.append(f"| Min Win Rate | {cfg.min_win_rate:.0f}% |")
    lines.append(f"| Min Sharpe | {cfg.min_sharpe} |")
    lines.append(f"| Max Drawdown | {cfg.max_max_drawdown:.0f}% |")
    lines.append(f"| Min Combo Pass Rate Floor | {floor:.0%} |")
    lines.append("")
    lines.append("```")
    lines.append("combo passes if:")
    lines.append(f"  SQN ≥ {cfg.min_sqn}  AND  PF ≥ {cfg.min_profit_factor}  AND  trades ≥ {cfg.min_trades}")
    lines.append(f"  AND  win_rate ≥ {cfg.min_win_rate:.0f}%  AND  sharpe ≥ {cfg.min_sharpe}  AND  max_dd ≤ {cfg.max_max_drawdown:.0f}%")
    lines.append("")
    lines.append(f"symbol/TF ✅  if  pass_rate ≥ {floor:.0%}  of its combos")
    lines.append("```")

    # ── Overview ───────────────────────────────────────────────────────────────
    h("Overview")
    lines.append(
        f"**{n_total:,} total combos** — "
        f"{n_symbols} symbols × {n_timeframes} timeframes × {n_param_sets} parameter sets  \n"
        f"**{n_passing:,} pass ({pct_pass})** with current thresholds"
    )

    # ── §1 Overall Strategy Effectiveness ─────────────────────────────────────
    h("§1. Overall Strategy Effectiveness")
    lines.append(
        "_How to read:_\n"
        "```\n"
        f"data: {n_symbols} coins × {n_timeframes} TFs × {n_param_sets} params = {n_total:,} combos\n"
        f"bar:  n_pass / {n_per_coin} combos per coin  (all TFs pooled)\n"
        f"floor ≥ {floor:.0%}  →  coin ✅  |  below → coin ❌\n"
        f"SQN≥{cfg.min_sqn}  PF≥{cfg.min_profit_factor}  trades≥{cfg.min_trades}  "
        f"win%≥{cfg.min_win_rate:.0f}  sharpe≥{cfg.min_sharpe}  max_dd≤{cfg.max_max_drawdown:.0f}%\n"
        "```\n"
    )
    lines.append("| Symbol | Pass Rate | Passes | Total | Status |")
    lines.append("|--------|-----------|--------|-------|--------|")
    if df is not None and "_passes" in df.columns:
        col_sym = cfg.col_symbol
        for sym in sorted(df[col_sym].unique()):
            sym_df      = df[df[col_sym] == sym]
            n_sym_total = len(sym_df)
            n_sym_pass  = int(sym_df["_passes"].sum())
            rate        = n_sym_pass / n_sym_total if n_sym_total else 0.0
            status      = "✅" if rate >= floor else "❌"
            lines.append(f"| {sym} | {rate:.0%} | {n_sym_pass} | {n_sym_total} | {status} |")
    else:
        for sym, rate in sorted(sym_rates.items()):
            status = "✅" if rate >= floor else "❌"
            lines.append(f"| {sym} | {rate:.0%} | — | — | {status} |")

    # ── §2 Performance per Timeframe ──────────────────────────────────────────
    h("§2. Performance per Timeframe")
    lines.append(
        "_How to read:_\n"
        "```\n"
        f"same {n_total:,} combos — split by TF\n"
        f"each TF: {n_symbols} coins × {n_param_sets} params = {n_per_cpt * n_symbols:,} combos per TF\n"
        f"bar: n_pass / {n_per_cpt} combos per (coin, TF)\n"
        f"floor ≥ {floor:.0%}  →  coin/TF ✅  |  below → ❌\n"
        "```\n"
    )
    if df is not None and "_passes" in df.columns:
        col_sym    = cfg.col_symbol
        col_tf     = cfg.col_timeframe
        timeframes = sorted(df[col_tf].unique())
        all_symbols = sorted(df[col_sym].unique())
        coin_tf_pass: dict[str, list[str]] = {sym: [] for sym in all_symbols}

        for tf in timeframes:
            tf_df = df[df[col_tf] == tf]
            lines.append(f"### TF {tf}\n")
            lines.append("| Symbol | Pass Rate | Passes | Total | Status |")
            lines.append("|--------|-----------|--------|-------|--------|")
            for sym in all_symbols:
                sym_tf = tf_df[tf_df[col_sym] == sym]
                n_st   = len(sym_tf)
                n_sp   = int(sym_tf["_passes"].sum()) if n_st else 0
                rate   = n_sp / n_st if n_st else 0.0
                status = "✅" if rate >= floor else "❌"
                if rate >= floor:
                    coin_tf_pass[sym].append(str(tf))
                lines.append(f"| {sym} | {rate:.0%} | {n_sp} | {n_st} | {status} |")
            lines.append("")

        lines.append("### Coverage Summary\n")
        lines.append("| Coin | Passing TFs | Count | Verdict |")
        lines.append("|------|------------|-------|---------|")
        n_tfs_total = len(timeframes)
        for sym in all_symbols:
            passing_tfs = coin_tf_pass[sym]
            n_ptfs      = len(passing_tfs)
            if n_ptfs == n_tfs_total:
                verdict = f"✅ All {n_tfs_total} TFs"
            elif n_ptfs == 0:
                verdict = "❌ None"
            else:
                verdict = f"⚠️ {n_ptfs}/{n_tfs_total}"
            lines.append(
                f"| {sym} | {', '.join(passing_tfs) if passing_tfs else '—'} "
                f"| {n_ptfs}/{n_tfs_total} | {verdict} |"
            )
        lines.append("")

        by_count: dict[int, list[str]] = defaultdict(list)
        for sym in all_symbols:
            by_count[len(coin_tf_pass[sym])].append(sym)
        lines.append("**TF Coverage summary:**\n")
        for count in sorted(by_count.keys(), reverse=True):
            group = sorted(by_count[count])
            if count == n_tfs_total:
                lines.append(f"- ✅ {len(group)} coin(s) pass all {n_tfs_total} TFs: {', '.join(group)}")
            elif count == 0:
                lines.append(f"- ❌ {len(group)} coin(s) pass 0 TFs: {', '.join(group)}")
            else:
                lines.append(f"- ⚠️ {len(group)} coin(s) pass {count}/{n_tfs_total} TFs: {', '.join(group)}")
    else:
        lines.append("| Timeframe | Pass Rate | Status |")
        lines.append("|-----------|-----------|--------|")
        for tf, rate in sorted(tf_rates.items()):
            status = "✅" if rate >= floor else "❌"
            lines.append(f"| {tf} | {rate:.0%} | {status} |")

    # ── §2b Universal Combos per Timeframe ─────────────────────────────────────
    h("§2b. Universal Combos per Timeframe")
    lines.append(
        "_How to read:_\n"
        "```\n"
        "rows  = unique parameter signatures (exact toggle combinations)\n"
        "cols  = coins tested on this timeframe\n"
        "cell  = ✅  if that exact combo passes all thresholds on that coin\n"
        "# Coins = total coins where this combo passes simultaneously\n\n"
        "top rows  →  most universal combos  →  strategy holds across multiple markets\n"
        "single ✅  →  coin-specific result  →  may be curve-fitted or asset-specific\n"
        "```\n"
    )
    if df is not None and "_passes" in df.columns and df["_passes"].any():
        col_sym = cfg.col_symbol
        col_tf  = cfg.col_timeframe
        col_sig = cfg.col_param_sig
        if col_sig in df.columns:
            passing_df  = df[df["_passes"]]
            all_symbols = sorted(df[col_sym].unique())
            n_coins     = len(all_symbols)
            timeframes  = sorted(df[col_tf].unique())
            for tf in timeframes:
                tf_pass = passing_df[passing_df[col_tf] == tf]
                lines.append(f"### TF {tf}\n")
                if tf_pass.empty:
                    lines.append(f"_No passing combos on {tf} with current thresholds._\n")
                    continue
                pivot = (
                    tf_pass.groupby([col_sig, col_sym])
                    .size()
                    .unstack(fill_value=0)
                    .clip(upper=1)
                    .astype(int)
                )
                for sym in all_symbols:
                    if sym not in pivot.columns:
                        pivot[sym] = 0
                coin_cols    = sorted(all_symbols)
                pivot        = pivot[coin_cols]
                pivot["# Coins"] = pivot[coin_cols].sum(axis=1)
                pivot        = pivot.sort_values("# Coins", ascending=False)
                n_multi_coin = int((pivot["# Coins"] > 1).sum())
                n_all_coins  = int((pivot["# Coins"] == n_coins).sum())
                lines.append(
                    f"**{len(pivot)}** combos  |  "
                    f"**{n_multi_coin}** pass on ≥ 2 coins  |  "
                    f"**{n_all_coins}** pass on all {n_coins} coins\n"
                )
                coin_header = " | ".join(coin_cols)
                coin_sep    = " | ".join("---" for _ in coin_cols)
                lines.append(f"| Parameter Signature | {coin_header} | # Coins |")
                lines.append(f"|---------------------|{coin_sep}|---------|")
                for sig, row_data in pivot.iterrows():
                    cells = " | ".join("✅" if row_data[sym] else "  " for sym in coin_cols)
                    lines.append(f"| `{sig}` | {cells} | {int(row_data['# Coins'])} |")
                lines.append("")
        else:
            lines.append(f"_Column '{cfg.col_param_sig}' not found in data._\n")
    else:
        lines.append("_No passing combos with current thresholds._\n")

    # ── §3 Toggle Frequency ────────────────────────────────────────────────────
    h("§3. Parameter Stability (Toggle Frequency)")
    lines.append(
        "_How to read:_\n"
        "```\n"
        "top-5 combos per (coin, TF) — from passing combos only  (threshold-sensitive)\n"
        "count = how often toggle is ON in those selections\n\n"
        "count → high  →  toggle in most passing combos  →  likely key ingredient\n"
        "count → low   →  toggle barely appears  →  probably not helping → consider removing\n\n"
        "no clear winner?  →  performance requires very specific combination  →  fragile signal\n"
        "```\n"
    )
    if tog_freq:
        cat_groups: dict[str, list[str]] = defaultdict(list)
        for tog in tog_freq:
            cat_groups[_categorize_toggle(tog)].append(tog)
        for cat in _CATEGORY_ORDER:
            if cat not in cat_groups:
                continue
            lines.append(f"### {cat}\n")
            lines.append("| Toggle | Count |")
            lines.append("|--------|-------|")
            for tog in sorted(cat_groups[cat], key=lambda x: -tog_freq[x]):
                lines.append(f"| `{tog}` | {tog_freq[tog]} |")
            lines.append("")
    else:
        lines.append("_No toggle data available._\n")

    # ── §4 Top Passing Combos ──────────────────────────────────────────────────
    h("§4. Top Passing Combos")
    lines.append(
        "_How to read:_\n"
        f"```\n"
        f"combos that pass ALL thresholds  ({n_passing} / {n_total})\n"
        f"SQN ≥ {cfg.min_sqn}  AND  PF ≥ {cfg.min_profit_factor}  AND  trades ≥ {cfg.min_trades}\n"
        f"AND  win_rate ≥ {cfg.min_win_rate:.0f}%  AND  sharpe ≥ {cfg.min_sharpe}  AND  max_dd ≤ {cfg.max_max_drawdown:.0f}%\n\n"
        f"sorted by _score  (composite SQN + PF + Sharpe)\n\n"
        f"< 5 combos  →  relax thresholds\n"
        f"> 50 combos →  tighten thresholds\n"
        f"```\n"
    )
    if df is not None and "_passes" in df.columns:
        view = df[df["_passes"]].copy()
        if view.empty:
            lines.append("_No combos pass the current thresholds._\n")
        else:
            show_cols = [
                cfg.col_symbol, cfg.col_timeframe, cfg.col_param_sig, "_score",
                cfg.col_sqn, cfg.col_pf, cfg.col_expectancy,
                cfg.col_trades, cfg.col_win_rate, cfg.col_sharpe,
                cfg.col_max_drawdown, cfg.col_calmar, cfg.col_return,
            ]
            available = [c for c in show_cols if c in view.columns]
            sort_col  = "_score" if "_score" in view.columns else available[0]
            view      = view[available].sort_values(sort_col, ascending=False).reset_index(drop=True)
            header = " | ".join(available)
            sep    = " | ".join("---" for _ in available)
            lines.append(f"| {header} |")
            lines.append(f"|{sep}|")
            for _, r in view.iterrows():
                cells = [_fmt_cell(r[c]) for c in available]
                lines.append(f"| {' | '.join(cells)} |")
            lines.append(f"\n_{len(view)} passing combos._\n")
    else:
        lines.append("_DataFrame not available._\n")

    # ── §5 Threshold Sweep ─────────────────────────────────────────────────────
    h("§5. Threshold Sweep")
    lines.append(
        "_How to read:_\n"
        "```\n"
        f"'Robust (≥{floor:.0%})' line  : coin ✅ if ≥ {floor:.0%} of its combos pass — robustness floor\n"
        f"'Any combo passes' line       : coin ✅ if ≥ 1 combo passes — matches Top Combos table\n\n"
        f"Gap between lines = coins with passing combos below the robustness floor\n"
        f"  (they appear in Top Combos but NOT counted as robust in the symbol pass rate)\n\n"
        f"steep drop  →  threshold sensitive  →  small change excludes many coins\n"
        f"flat line   →  stable zone  →  safe to move threshold here\n"
        "```\n"
    )
    _sweep_explanations: dict[str, str] = {
        "SQN": (
            f"**SQN sweep** — consistency of returns.  "
            f"`< 1.0` = not viable  |  `1–2` = acceptable  |  `≥ 2` = strong.  "
            f"Active threshold: `SQN ≥ {cfg.min_sqn}`"
        ),
        "Profit Factor": (
            f"**PF sweep** — gross profit ÷ gross loss.  "
            f"`1.5` = earn $1.50 per $1 lost.  "
            f"Active threshold: `PF ≥ {cfg.min_profit_factor}`"
        ),
        "# Trades": (
            f"**Trades sweep** — minimum trade count filter.  "
            f"Too few trades → can't distinguish skill from luck.  "
            f"Active threshold: `trades ≥ {cfg.min_trades}`"
        ),
    }
    if sweep_data:
        for metric_label, (sweep_df, active_val) in sweep_data.items():
            h(f"Sweep — {metric_label}", 3)
            if metric_label in _sweep_explanations:
                lines.append(_sweep_explanations[metric_label] + "\n")
            _closest = min(sweep_df["threshold"], key=lambda x: abs(float(x) - float(active_val)))
            lines.append(f"| Min {metric_label} | Robust (≥{floor:.0%}) | Any combo passes | |")
            lines.append("|---|---|---|---|")
            for _, r in sweep_df.iterrows():
                t       = float(r["threshold"])
                robust  = float(r["symbol_pass_rate"])
                any_p   = r.get("symbol_any_pass_rate", float("nan"))
                try:
                    any_str = f"{float(any_p):.0%}"
                except (TypeError, ValueError):
                    any_str = "—"
                marker = " ◀ **current**" if abs(t - float(_closest)) < 1e-9 else ""
                lines.append(f"| {t:.3g} | {robust:.0%} | {any_str} |{marker} |")
            lines.append("")
    else:
        lines.append("_Sweep data not available._\n")

    lines.append("")
    return "\n".join(lines)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("⚙️ Configuration")

    results_dir = st.text_input(
        "Results directory",
        placeholder="/path/to/2026-04-10_2329_AMS",
        help="Path to the VBT backtest results folder containing per-symbol CSVs.",
    )
    label = st.text_input("Strategy label", value="AMS")

    st.markdown("---")

    with st.expander("📊 Thresholds"):
        min_sqn      = st.slider("Min SQN",           0.0,  3.0,  1.0,  0.1,
            help="System Quality Number — how consistently the strategy makes money. "
                 "1.0 = minimum viable; ≥2.0 = excellent.")
        min_pf       = st.slider("Min Profit Factor",  1.0,  5.0,  1.5,  0.1,
            help="Gross profit ÷ gross loss. 1.5 means you earn $1.50 for every $1 lost. "
                 "Below 1.0 = net loser.")
        min_trades   = st.slider("Min # Trades",       1,    150,   30,   1,
            help="Minimum number of trades a combo must have to count — filters out "
                 "combos with so few trades that stats are meaningless.")
        min_win_rate = st.slider("Min Win Rate (%)",   0.0,  70.0, 30.0, 1.0,
            help="Percentage of trades that close in profit. Low win rate is acceptable "
                 "if average winner is much larger than average loser.")
        min_sharpe   = st.slider("Min Sharpe",         0.0,  2.0,  0.5,  0.05,
            help="Risk-adjusted return (return ÷ volatility). 0.5 = acceptable; "
                 "≥1.0 = good; ≥2.0 = exceptional.")
        max_max_dd   = st.slider("Max Drawdown (%)",   10.0, 50.0, 20.0, 1.0,
            help="Maximum allowed peak-to-trough equity drawdown. "
                 "Combos that exceed this are excluded regardless of other metrics.")
        min_combo_pass_rate = st.slider(
            "Min combo pass rate (%)", 0, 50, 20, 1,
            help="Minimum percentage of combos for a symbol/timeframe that must pass "
                 "all thresholds before it counts as 'passing'. 0 = any single combo "
                 "is enough; 100 = every combo must pass.",
        ) / 100.0

    with st.expander("⚙️ Sweep settings"):
        sqn_sweep_range    = st.slider("SQN sweep range",    0.0, 3.0, (0.5, 2.0), 0.1,
            help="Range of Min SQN values to sweep over in Section 5.")
        pf_sweep_range     = st.slider("PF sweep range",     1.0, 5.0, (1.2, 3.0), 0.1,
            help="Range of Min Profit Factor values to sweep over in Section 5.")
        trades_sweep_range = st.slider("Trades sweep range", 1,   150,  (5, 40),    1,
            help="Range of Min # Trades values to sweep over in Section 5.")
        sweep_steps        = st.slider("Sweep steps",        5,   30,  15,         1,
            help="Number of evenly-spaced threshold values to evaluate per metric.")

    _prev_raw = st.session_state.get("_raw_df")

    with st.expander("🕐 Timeframe Filter", expanded=_prev_raw is not None):
        if _prev_raw is not None:
            _tf_col  = RobustnessConfig().col_timeframe
            _all_tfs = sorted(_prev_raw[_tf_col].unique().tolist())
            active_timeframes: list | None = [
                tf for tf in _all_tfs
                if st.checkbox(str(tf), value=True, key=f"tf_{tf}")
            ]
        else:
            active_timeframes = None
            st.caption("📎 Timeframe filter available after the first run.")

    with st.expander("🔧 Toggle Pre-filter", expanded=_prev_raw is not None):
        if _prev_raw is not None:
            _all_toggle_cols = sorted(c for c in _prev_raw.columns if c.startswith("use_"))
            _cat_groups: dict[str, list[str]] = defaultdict(list)
            for _tc in _all_toggle_cols:
                _cat_groups[_categorize_toggle(_tc)].append(_tc)

            _toggle_states: dict[str, str] = {}
            for _cat in _CATEGORY_ORDER:
                if _cat not in _cat_groups:
                    continue
                st.markdown(f"**{_cat}**")
                for col in _cat_groups[_cat]:
                    _toggle_states[col] = st.selectbox(
                        col,
                        ["Neutral", "Force ON", "Force OFF"],
                        key=f"toggle_{col}",
                        help=(
                            "Neutral = include all combos for this toggle.  "
                            "Force ON = keep only combos where this toggle is enabled.  "
                            "Force OFF = exclude combos where this toggle is enabled."
                        ),
                    )
            forced_on_toggles  = [c for c, s in _toggle_states.items() if s == "Force ON"]
            forced_off_toggles = [c for c, s in _toggle_states.items() if s == "Force OFF"]
        else:
            forced_on_toggles:  list[str] = []
            forced_off_toggles: list[str] = []
            st.caption("📎 Toggle filter available after the first run.")

    with st.expander("🪙 Symbol Filter", expanded=_prev_raw is not None):
        if _prev_raw is not None:
            _sym_col_raw  = RobustnessConfig().col_symbol
            _all_syms_raw = sorted(_prev_raw[_sym_col_raw].unique().tolist())
            _sym_mode = st.radio(
                "Mode", ["All", "1 pair", "Custom"],
                horizontal=True, key="sym_mode",
            )
            if _sym_mode == "All":
                selected_symbols = None
            elif _sym_mode == "1 pair":
                _one_sym = st.selectbox("Select pair", _all_syms_raw, key="sym_one")
                selected_symbols = [_one_sym]
            else:
                selected_symbols = st.multiselect(
                    "Select pairs", options=_all_syms_raw, default=_all_syms_raw, key="sym_custom",
                )
        else:
            selected_symbols = None
            st.caption("📎 Symbol filter available after the first run.")

    run_btn = st.button("▶ Run analysis", type="primary", use_container_width=True)

    # ── Save report (appears after first successful run) ──────────────────────
    if st.session_state.get("_report_str"):
        st.markdown("---")
        _save_btn = st.button("💾 Save Report", use_container_width=True)
        _fname_default = st.session_state.get("_report_filename_default", f"{label}_phase1.md")
        if st.session_state.pop("_reset_report_filename", False):
            if "p1_report_filename_input" in st.session_state:
                del st.session_state["p1_report_filename_input"]
        _save_fname = st.text_input("Filename", key="p1_report_filename_input", value=_fname_default)
        if _save_btn:
            try:
                _rd = st.session_state.get("committed", {}).get("results_dir", "")
                _dest = Path(_rd).expanduser().resolve() if _rd else Path(".")
                _dest.mkdir(parents=True, exist_ok=True)
                _fpath = _dest / (_save_fname.strip() or _fname_default)
                _fpath.write_text(st.session_state["_report_str"], encoding="utf-8")
                st.success(f"Saved → `{_fpath}`")
            except Exception as _e:
                st.error(f"Save failed: {_e}")


# ── Commit all sidebar values on Run click ────────────────────────────────────
if run_btn:
    st.session_state["committed"] = dict(
        results_dir=results_dir,
        label=label,
        min_sqn=min_sqn,
        min_pf=min_pf,
        min_trades=min_trades,
        min_win_rate=min_win_rate,
        min_sharpe=min_sharpe,
        max_max_dd=max_max_dd,
        min_combo_pass_rate=min_combo_pass_rate,
        sqn_sweep_range=sqn_sweep_range,
        pf_sweep_range=pf_sweep_range,
        trades_sweep_range=trades_sweep_range,
        sweep_steps=sweep_steps,
        forced_on_toggles=forced_on_toggles,
        forced_off_toggles=forced_off_toggles,
        active_timeframes=active_timeframes,
        selected_symbols=selected_symbols,
    )
    st.session_state["_reset_report_filename"] = True


# ── Main ──────────────────────────────────────────────────────────────────────
st.title("📊 Strategy Robustness — Phase 1")
st.markdown(
    "Sweep analysis across symbols and timeframes. "
    "Sections 1–3: effectiveness, per-TF coverage, toggle frequency. "
    "Sections 4–5: top passing combos and threshold sweep."
)

committed = st.session_state.get("committed")
if committed is None:
    st.info("Enter a results directory in the sidebar and click **▶ Run analysis**.")
    st.stop()

c = committed

results_dir        = c["results_dir"]
label              = c["label"]
min_sqn            = c["min_sqn"]
min_pf             = c["min_pf"]
min_trades         = c["min_trades"]
min_win_rate       = c["min_win_rate"]
min_sharpe         = c["min_sharpe"]
max_max_dd         = c["max_max_dd"]
sqn_sweep_range    = c["sqn_sweep_range"]
pf_sweep_range     = c["pf_sweep_range"]
trades_sweep_range = c["trades_sweep_range"]
sweep_steps        = c["sweep_steps"]
c_forced_on        = c["forced_on_toggles"]
c_forced_off       = c["forced_off_toggles"]
c_active_tfs       = c["active_timeframes"]
c_selected_symbols = c.get("selected_symbols")

if not results_dir:
    st.error("Please provide a results directory.")
    st.stop()

if isinstance(c_active_tfs, list) and len(c_active_tfs) == 0:
    st.warning(
        "No timeframes selected — tick at least one in **🕐 Timeframe Filter** and re-run."
    )
    st.stop()

if isinstance(c_selected_symbols, list) and len(c_selected_symbols) == 0:
    st.warning(
        "No symbols selected — pick at least one in **🪙 Symbol Filter** and re-run."
    )
    st.stop()

cfg = RobustnessConfig(
    min_sqn=min_sqn,
    min_profit_factor=min_pf,
    min_trades=int(min_trades),
    min_win_rate=min_win_rate,
    min_sharpe=min_sharpe,
    max_max_drawdown=max_max_dd,
    min_combo_pass_rate=c["min_combo_pass_rate"],
)

# ── Load raw CSV (cached by directory path) ───────────────────────────────────
if st.session_state.get("_cached_dir") != results_dir:
    with st.spinner("Loading backtest results…"):
        try:
            _raw_df = load_run_dir(results_dir)
        except Exception as exc:
            st.error(f"Failed to load results directory: {exc}")
            st.stop()
        st.session_state["_raw_df"]     = _raw_df
        st.session_state["_cached_dir"] = results_dir
        # Force re-render so sidebar TF/toggle expanders see _raw_df immediately.
        st.rerun()

raw_df = st.session_state["_raw_df"]

# ── Apply filters and annotate ────────────────────────────────────────────────
_analysis_raw = raw_df
if c_active_tfs:
    _analysis_raw = _analysis_raw[_analysis_raw[cfg.col_timeframe].isin(c_active_tfs)]
for _t in c_forced_off:
    if _t in _analysis_raw.columns:
        _analysis_raw = _analysis_raw[_analysis_raw[_t] == 0]
for _t in c_forced_on:
    if _t in _analysis_raw.columns:
        _analysis_raw = _analysis_raw[_analysis_raw[_t] == 1]
if c_selected_symbols is not None and cfg.col_symbol in _analysis_raw.columns:
    _analysis_raw = _analysis_raw[_analysis_raw[cfg.col_symbol].isin(c_selected_symbols)]

_n_raw_total = len(raw_df)

df = annotate_dataframe(_analysis_raw, cfg)

col_status = validate_columns(df, cfg)
missing_required = [c for c, ok in col_status.items() if not ok and c in {
    cfg.col_sqn, cfg.col_pf, cfg.col_trades, cfg.col_win_rate,
    cfg.col_sharpe, cfg.col_return,
}]
missing_optional = [c for c, ok in col_status.items() if not ok and c in {
    cfg.col_max_drawdown, cfg.col_expectancy, cfg.col_calmar,
}]
if missing_required:
    st.error(f"Required columns missing from CSV — analysis may be incorrect: {missing_required}")
if missing_optional:
    st.info(
        f"Optional columns not found in CSV (scoring will fall back to 0 for those components): "
        f"{missing_optional}"
    )

tog_freq  = toggle_frequency(df, cfg)
sym_rates = symbol_pass_rate(df, cfg)
tf_rates  = timeframe_pass_rate(df, cfg)

_n_total      = len(df)
_n_symbols    = df[cfg.col_symbol].nunique()
_n_timeframes = df[cfg.col_timeframe].nunique()
_n_param_sets = _n_total // (_n_symbols * _n_timeframes) if (_n_symbols * _n_timeframes) else 0
_n_passing    = int(df["_passes"].sum()) if "_passes" in df.columns else 0
_pct_passing  = _n_passing / _n_total if _n_total else 0

_all_raw_symbols = set(raw_df[cfg.col_symbol].unique())
_is_sym_filtered = c_selected_symbols is not None and set(c_selected_symbols) != _all_raw_symbols
_filter_active   = bool(c_forced_off or c_forced_on or c_active_tfs or _is_sym_filtered)

if _filter_active:
    _n_excluded = _n_raw_total - _n_total
    _parts: list[str] = []
    if _is_sym_filtered:
        _parts.append(f"Symbols: {', '.join(sorted(c_selected_symbols))}")
    if c_active_tfs:
        _parts.append(f"TFs: {', '.join(str(t) for t in c_active_tfs)}")
    if c_forced_off:
        _parts.append(", ".join(f"`{t}=OFF`" for t in c_forced_off))
    if c_forced_on:
        _parts.append(", ".join(f"`{t}=ON`" for t in c_forced_on))
    st.info(
        f"📊 **{_n_total:,} combos after filter** "
        f"({_n_excluded:,} excluded — {' | '.join(_parts)}).  "
        f"With current thresholds: **{_n_passing:,} pass ({_pct_passing:.1%})**."
    )
else:
    st.info(
        f"📊 **{_n_total:,} total combos** — {_n_symbols} symbols × {_n_timeframes} timeframes × "
        f"{_n_param_sets} parameter sets.  "
        f"With current thresholds: **{_n_passing:,} pass ({_pct_passing:.1%})**."
    )

with st.expander("ℹ️ Passing criteria (thresholds)"):
    st.code(
        f"combo passes if:\n"
        f"  SQN ≥ {min_sqn}  AND  PF ≥ {min_pf}  AND  trades ≥ {min_trades}\n"
        f"  AND  win_rate ≥ {min_win_rate:.0f}%  AND  sharpe ≥ {min_sharpe}  AND  max_dd ≤ {max_max_dd:.0f}%\n\n"
        f"symbol/TF ✅  if  pass_rate ≥ {cfg.min_combo_pass_rate:.0%}  of its combos",
        language=None,
    )

st.divider()
st.subheader("1. Overall Strategy Effectiveness")
_section_overall_symbol(cfg, df)

st.divider()
st.subheader("2. Performance per Timeframe")
_section_per_tf_charts(cfg, df)

st.divider()
st.subheader("2b. Universal Combos per Timeframe")
_section_combo_overlap(cfg, df)

st.divider()
st.subheader("3. Parameter Stability (Toggle Frequency)")
_section_toggle_frequency(tog_freq)

st.divider()
st.subheader("4. Top Passing Combos")
_section_top_combos(df, cfg)

st.divider()
st.subheader("5. Threshold Sweep")

_n_per_coin = _n_total // _n_symbols if _n_symbols else 0
_n_per_cpt  = _n_total // (_n_symbols * _n_timeframes) if (_n_symbols * _n_timeframes) else 0
_tfs_sorted = sorted(df[cfg.col_timeframe].unique())
_tf_lines   = "\n".join(f"  All {_n_per_cpt} combos on {tf}" for tf in _tfs_sorted)
_floor_pct  = cfg.min_combo_pass_rate

_info(
    f"```\n"
    f"# data: {_n_total:,} combos — {_n_symbols} coins × {_n_timeframes} TFs × {_n_param_sets} params\n"
    f"# 'robust' line  : coin ✅ if ≥ {_floor_pct:.0%} of its {_n_per_coin} combos pass\n"
    f"# 'any pass' line: coin ✅ if ≥ 1 combo passes  (matches the Top Combos table)\n"
    f"# y = passing coins ÷ {_n_symbols}\n\n"
    f"Gap between the two lines = coins that have 1–{int(_floor_pct * _n_per_coin) - 1} passing combos\n"
    f"but fall below the {_floor_pct:.0%} robustness floor — they appear in Top Combos\n"
    f"but are NOT counted as robust in the symbol pass rate.\n\n"
    f"steep drop  →  threshold sensitive  →  small change excludes many coins\n"
    f"flat line   →  stable zone  →  safe to move threshold here\n"
    f"```"
)

_SWEEP_EXPLANATIONS = {
    "SQN": (
        f"**SQN sweep** — consistency of returns.  "
        f"`< 1.0` = not viable  |  `1–2` = acceptable  |  `≥ 2` = strong.  "
        f"Active: `SQN ≥ {min_sqn}`"
    ),
    "Profit Factor": (
        f"**PF sweep** — gross profit ÷ gross loss.  "
        f"`1.5` = earn $1.50 per $1 lost.  "
        f"Active: `PF ≥ {min_pf}`"
    ),
    "# Trades": (
        f"**Trades sweep** — cutoff filter (combos below excluded entirely, not penalised).  "
        f"Too few trades → can't distinguish skill from luck.  "
        f"Active: `trades ≥ {min_trades}`"
    ),
}

_sweep_specs = [
    ("SQN",           "SQN",           sqn_sweep_range,    min_sqn,    ">="),
    ("Profit Factor", "Profit Factor",  pf_sweep_range,     min_pf,     ">="),
    ("# Trades",      "# Trades",       trades_sweep_range, min_trades, ">="),
]
_sweep_results_for_report: dict[str, tuple[pd.DataFrame, float]] = {}
for _metric_label, _metric_col, _sweep_range, _active_val, _cmp in _sweep_specs:
    st.markdown(_SWEEP_EXPLANATIONS[_metric_label])
    _lo, _hi = float(_sweep_range[0]), float(_sweep_range[1])
    _values = [float(v) for v in np.linspace(_lo, _hi, sweep_steps)]
    with st.spinner(f"Sweeping {_metric_label}…"):
        _sweep_df = sweep_threshold(df, _metric_col, _values, cfg, comparison=_cmp)
    _sweep_results_for_report[_metric_label] = (_sweep_df, float(_active_val))
    # Build tidy (long) dataframe for two-line chart
    _tidy = pd.concat([
        _sweep_df[["threshold", "symbol_pass_rate"]].rename(
            columns={"symbol_pass_rate": "pass_rate"}
        ).assign(metric=f"Robust (≥{_floor_pct:.0%} combos)"),
        _sweep_df[["threshold", "symbol_any_pass_rate"]].rename(
            columns={"symbol_any_pass_rate": "pass_rate"}
        ).assign(metric="Any combo passes"),
    ], ignore_index=True)
    _fig = px.line(
        _tidy, x="threshold", y="pass_rate", color="metric",
        title=(
            f"Symbol pass rate vs Min {_metric_label}  "
            f"({_n_symbols} coins, each = {_n_per_coin} combos pooled across {_n_timeframes} TFs)"
        ),
        labels={
            "threshold": f"Min {_metric_label}",
            "pass_rate": f"Symbol pass rate  (% of {_n_symbols} coins)",
            "metric":    "Criterion",
        },
        color_discrete_map={
            f"Robust (≥{_floor_pct:.0%} combos)": "#2196F3",
            "Any combo passes":                    "#FF9800",
        },
    )
    _fig.add_vline(
        x=float(_active_val), line_dash="dash", line_color="white",
        annotation_text="current threshold", annotation_position="top right",
    )
    _fig.update_layout(yaxis_range=[0, 1.05], yaxis_tickformat=".0%")
    st.plotly_chart(_fig, use_container_width=True)

# ── Store report for sidebar save button ──────────────────────────────────────
_run_ts = datetime.now().strftime("%Y-%m-%d_%H%M")
_report_str = _format_phase1_report(
    label=label,
    results_dir=results_dir,
    run_ts=_run_ts,
    cfg=cfg,
    sym_rates=sym_rates,
    tf_rates=tf_rates,
    tog_freq=tog_freq,
    n_total=_n_total,
    n_passing=_n_passing,
    n_symbols=_n_symbols,
    n_timeframes=_n_timeframes,
    n_param_sets=_n_param_sets,
    df=df,
    sweep_data=_sweep_results_for_report,
)
st.session_state["_report_str"]             = _report_str
st.session_state["_report_filename_default"] = f"{_run_ts}_{label}_phase1.md"

# ── Inline save button (main content area) ───────────────────────────────────
st.divider()
st.subheader("💾 Save Report")
_inline_fname_default = st.session_state.get("_report_filename_default", f"{_run_ts}_{label}_phase1.md")
_inline_fname = st.text_input(
    "Filename", value=_inline_fname_default, key="p1_inline_save_fname",
)
if st.button("💾 Save as Markdown", type="primary", key="p1_inline_save_btn"):
    try:
        _rd = st.session_state.get("committed", {}).get("results_dir", "")
        _dest = Path(_rd).expanduser().resolve() if _rd else Path(".")
        _dest.mkdir(parents=True, exist_ok=True)
        _fpath = _dest / (_inline_fname.strip() or _inline_fname_default)
        _fpath.write_text(_report_str, encoding="utf-8")
        st.success(f"✅ Saved → `{_fpath}`")
    except Exception as _e:
        st.error(f"Save failed: {_e}")
