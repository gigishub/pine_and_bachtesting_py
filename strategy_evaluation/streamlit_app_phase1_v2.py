"""Streamlit Phase 1 dashboard — exclusive-mode sweep analysis (v2).

Sections (each expandable, numbered 1–6):
  1. Performance per Timeframe    — per-TF combo pass-rate bar charts (diagnostic)
  2. Universal Combos per TF     — cross-coin combo overlap
  3. Weighted Robustness Score   — decision driver; pick the winning signature here
  4. Parameter Stability         — toggle frequency in top-5 combos
  5. Top Passing Combos          — raw metric table for passing rows
  6. Threshold Sweep             — sensitivity analysis with absolute-count robustness slider

Changes from v1:
  - §1 Overall Effectiveness removed (redundant with §3 Weighted Score)
  - Coverage Summary removed from §2 per-TF charts (redundant with §3 breadth)
  - "Min combo pass rate (%)" sidebar slider removed
  - §6 Threshold Sweep: "Robust" line controlled by per-sweep absolute-count slider

Run with:
    streamlit run strategy_evaluation/streamlit_app_phase1_v2.py
"""

from __future__ import annotations

import dataclasses
import sys
from pathlib import Path

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
from strategy_evaluation.scoring import compute_combo_weighted_scores
from strategy_evaluation.sig_alias import sig_to_alias

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Strategy Robustness — Phase 1 v2",
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


# ── Section 1 — Per-TF charts ─────────────────────────────────────────────────

def _section_per_tf_charts(cfg: RobustnessConfig, df: pd.DataFrame) -> None:
    """Section 1 — one bar chart per tested timeframe showing pass rate per coin.

    No pass/fail floor coloring; diagnostic only — shows *why* §3 scores are
    high or low on specific timeframes.
    """
    n_total           = len(df)
    n_symbols         = df[cfg.col_symbol].nunique()
    n_tfs             = df[cfg.col_timeframe].nunique()
    n_params          = n_total // (n_symbols * n_tfs) if (n_symbols * n_tfs) else 0
    n_per_coin_per_tf = n_total // (n_tfs * n_symbols) if (n_tfs * n_symbols) else 0
    col_sym           = cfg.col_symbol
    col_tf            = cfg.col_timeframe

    _info(
        f"```\n"
        f"data: {n_symbols} coins × {n_tfs} TFs × {n_params} params = {n_total:,} combos\n"
        f"each bar: n_pass / {n_per_coin_per_tf} combos for that (coin, TF)\n\n"
        f"use this chart to see which TF or coin is dragging scores down\n"
        f"decision: go to §3 Weighted Robustness Score to pick the winning signature\n"
        f"```\n"
        f"⚙️ `SQN≥{cfg.min_sqn}  PF≥{cfg.min_profit_factor}  trades≥{cfg.min_trades}  "
        f"win%≥{cfg.min_win_rate:.0f}  sharpe≥{cfg.min_sharpe}  max_dd≤{cfg.max_max_drawdown:.0f}%`"
    )

    timeframes  = sorted(df[col_tf].unique())
    all_symbols = sorted(df[col_sym].unique())

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
            rows.append({
                "Symbol":          sym,
                "Combo pass rate": float(coin_rates.get(sym, 0)),
                "n_total":         n_sym_total,
                "n_pass":          n_sym_pass,
            })

        df_tf = pd.DataFrame(rows)
        fig = px.bar(
            df_tf, x="Symbol", y="Combo pass rate",
            color_discrete_sequence=["#3498db"],
            title=f"TF {tf} — combo pass rate per coin  ({n_per_coin_per_tf} combos / coin)",
            labels={"Combo pass rate": f"Pass rate  (100% = {n_per_coin_per_tf} combos)"},
            custom_data=["n_total", "n_pass"],
        )
        fig.update_traces(
            hovertemplate="%{x}: %{customdata[1]} / %{customdata[0]} pass  (%{y:.0%})<extra></extra>"
        )
        fig.update_layout(yaxis_range=[0, 1.05], yaxis_tickformat=".0%", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)


# ── Section 2 — Universal combos per TF ──────────────────────────────────────

def _section_combo_overlap(cfg: RobustnessConfig, df: pd.DataFrame) -> None:
    """Section 2 — for each TF, which exact parameter signatures pass on multiple coins?"""
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

        disp = pd.DataFrame(index=pivot.index)
        for sym in coin_cols:
            disp[sym] = pivot[sym].map({1: "✅", 0: ""})
        disp["# Coins"] = pivot["# Coins"]
        disp.index.name = col_sig
        st.dataframe(disp.reset_index(), use_container_width=True, hide_index=True)


# ── Section 3 — Weighted Robustness Score ────────────────────────────────────

def _section_weighted_score(cfg: RobustnessConfig, df: pd.DataFrame) -> pd.DataFrame:
    """Section 3 — weighted robustness score per parameter signature.

    Returns the scored DataFrame for the report generator.
    """
    n_coins  = df[cfg.col_symbol].nunique()
    n_tfs    = df[cfg.col_timeframe].nunique()
    max_score = 1.0 * 1.0 * (1.5 ** (n_tfs - 1))

    _info(
        f"```\n"
        f"Final Score = avg_score × (coins_passing / {n_coins}) × 1.5^(n_TFs − 1)\n"
        f"\n"
        f"avg_score     : mean quality score (_score) of all passing rows for this signature\n"
        f"breadth       : coins_passing / {n_coins}  — fraction of coins where sig passes on ≥1 TF\n"
        f"tf_multiplier : 1.5^(n_TFs − 1)  — exponential bonus for cross-TF validity\n"
        f"               1 TF → ×1.0  |  2 TFs → ×1.5  |  3 TFs → ×2.25\n"
        f"\n"
        f"high final_score  =  high quality  +  many coins  +  many TFs\n"
        f"max possible ≈ 1.0 × 1.0 × {1.5 ** (n_tfs - 1):.3f} = {max_score:.3f} "
        f"(all {n_coins} coins, all {n_tfs} TFs, perfect _score)\n"
        f"```"
    )

    scored = compute_combo_weighted_scores(df, cfg)

    if scored.empty:
        st.info("No passing combos — relax the thresholds.")
        return scored

    top_n = st.slider(
        "Show top N signatures",
        min_value=5, max_value=min(50, len(scored)),
        value=min(20, len(scored)), step=1,
        key="weighted_top_n",
    )
    display = scored.head(top_n).copy()
    display["Alias"] = display["Parameter Signature"].apply(sig_to_alias)

    fig_bar = px.bar(
        display,
        x="final_score",
        y="Alias",
        orientation="h",
        color="n_TFs",
        color_continuous_scale="Viridis",
        title=f"Top {top_n} signatures by Weighted Robustness Score",
        labels={
            "final_score": "Final Score",
            "Alias": "",
            "n_TFs": "# TFs",
        },
        custom_data=["avg_score", "coins_passing", "n_TFs", "tf_multiplier", "breadth", "Parameter Signature"],
    )
    fig_bar.update_traces(
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Full sig: %{customdata[5]}<br>"
            "Final Score: %{x:.4f}<br>"
            "Avg _score: %{customdata[0]:.4f}<br>"
            "Coins passing: %{customdata[1]} / " + str(n_coins) + "  (breadth %{customdata[4]:.0%})<br>"
            "TFs: %{customdata[2]}  →  ×%{customdata[3]:.3f}<extra></extra>"
        )
    )
    fig_bar.update_layout(
        yaxis={"categoryorder": "total ascending"},
        coloraxis_colorbar_title="# TFs",
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    fig_scatter = px.scatter(
        display,
        x="breadth",
        y="avg_score",
        size="final_score",
        color="n_TFs",
        color_continuous_scale="Viridis",
        hover_name="Parameter Signature",
        title="Quality vs Breadth  (bubble size = Final Score, colour = # TFs)",
        labels={
            "breadth":   f"Breadth  (coins passing / {n_coins})",
            "avg_score": "Avg Quality Score",
            "n_TFs":     "# TFs",
        },
        hover_data={"final_score": ":.4f", "tf_multiplier": ":.3f", "Alias": True},
    )
    fig_scatter.update_layout(xaxis_range=[-0.05, 1.05])
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.dataframe(display, use_container_width=True, hide_index=True)
    st.caption(
        f"{len(scored)} signatures with ≥1 passing combo.  "
        f"Max possible Final Score ≈ **{max_score:.3f}** "
        f"({n_coins} coins × {n_tfs} TFs, perfect quality)."
    )

    return scored


# ── Section 4 — Toggle frequency ─────────────────────────────────────────────

def _section_toggle_frequency(tog_freq: dict[str, int]) -> None:
    """Section 4 — toggle frequency in top-5 combos per symbol/timeframe."""
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


# ── Section 5 — Top passing combos ───────────────────────────────────────────

def _section_top_combos(df: pd.DataFrame, cfg: RobustnessConfig) -> None:
    """Section 5 — all combos that pass current thresholds."""
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
    tbl = view[available].sort_values(sort_col, ascending=False).reset_index(drop=True)
    if cfg.col_param_sig in tbl.columns:
        tbl.insert(
            tbl.columns.get_loc(cfg.col_param_sig),
            "Alias",
            tbl[cfg.col_param_sig].apply(sig_to_alias),
        )
    st.dataframe(tbl, use_container_width=True)
    st.caption(f"{len(view)} passing combos shown.")


# ── Report formatting ─────────────────────────────────────────────────────────

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
    tog_freq: dict[str, int],
    n_total: int,
    n_passing: int,
    n_symbols: int,
    n_timeframes: int,
    n_param_sets: int,
    sweep_min_passing_combos: int = 1,
    df: pd.DataFrame | None = None,
    sweep_data: dict[str, tuple[pd.DataFrame, float]] | None = None,
    weighted_scores: pd.DataFrame | None = None,
    data_period: tuple[str, str] | None = None,
) -> str:
    """Generate a Markdown Phase 1 report matching all visible sections.

    Sections:
        Header / Passing Criteria / Overview
        1.  Performance per Timeframe       (per-coin per-TF bar charts)
        2.  Universal Combos per TF         (cross-coin combo overlap)
        3.  Weighted Robustness Score       (final_score = quality × breadth × TF)
        4.  Parameter Stability             (toggle frequency by category)
        5.  Top Passing Combos              (full table sorted by _score)
        6.  Threshold Sweep                 (SQN, PF, # Trades sensitivity)
    """
    pct_pass   = f"{n_passing / n_total:.1%}" if n_total else "—"
    n_per_cpt  = n_total // (n_symbols * n_timeframes) if (n_symbols * n_timeframes) else 0
    # Combos per coin pooled across all TFs (used in sweep floor description)
    n_per_coin = n_total // n_symbols if n_symbols else 0
    floor_pct  = sweep_min_passing_combos / n_per_coin if n_per_coin else 0.0

    lines: list[str] = []

    def h(text: str, level: int = 2) -> None:
        lines.append(f"\n{'#' * level} {text}\n")

    # ── Header ─────────────────────────────────────────────────────────────────
    lines.append(f"# Phase 1 Robustness Report — {label}")
    _period_line = (
        f"  \n**Data period:** {data_period[0]} → {data_period[1]}"
        if data_period else ""
    )
    lines.append(f"\n**Generated:** {run_ts}  \n**Results dir:** `{results_dir}`{_period_line}\n")

    # ── Passing Criteria ───────────────────────────────────────────────────────
    h("Passing Criteria")
    lines.append(
        "> A **combo passes** if ALL thresholds below are met simultaneously.\n"
    )
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")
    lines.append(f"| Min SQN | {cfg.min_sqn} |")
    lines.append(f"| Min Profit Factor | {cfg.min_profit_factor} |")
    lines.append(f"| Min # Trades | {cfg.min_trades} |")
    lines.append(f"| Min Win Rate | {cfg.min_win_rate:.0f}% |")
    lines.append(f"| Min Sharpe | {cfg.min_sharpe} |")
    lines.append(f"| Max Drawdown | {cfg.max_max_drawdown:.0f}% |")
    lines.append(f"| Sweep robustness floor | ≥ {sweep_min_passing_combos} combos per symbol |")
    lines.append("")
    lines.append("```")
    lines.append("combo passes if:")
    lines.append(f"  SQN ≥ {cfg.min_sqn}  AND  PF ≥ {cfg.min_profit_factor}  AND  trades ≥ {cfg.min_trades}")
    lines.append(f"  AND  win_rate ≥ {cfg.min_win_rate:.0f}%  AND  sharpe ≥ {cfg.min_sharpe}  AND  max_dd ≤ {cfg.max_max_drawdown:.0f}%")
    lines.append("```")

    # ── Overview ───────────────────────────────────────────────────────────────
    h("Overview")
    lines.append(
        f"**{n_total:,} total combos** — "
        f"{n_symbols} symbols × {n_timeframes} timeframes × {n_param_sets} parameter sets  \n"
        f"**{n_passing:,} pass ({pct_pass})** with current thresholds"
    )

    # ── 1. Performance per Timeframe ──────────────────────────────────────────
    h("1. Performance per Timeframe")
    lines.append(
        "_How to read:_\n"
        "```\n"
        f"data: {n_symbols} coins × {n_timeframes} TFs × {n_param_sets} params = {n_total:,} combos\n"
        f"each bar: n_pass / {n_per_cpt} combos for that (coin, TF)\n"
        f"use this chart to see which TF or coin is dragging scores down\n"
        "```\n"
    )
    if df is not None and "_passes" in df.columns:
        col_sym    = cfg.col_symbol
        col_tf     = cfg.col_timeframe
        timeframes = sorted(df[col_tf].unique())
        all_symbols = sorted(df[col_sym].unique())

        for tf in timeframes:
            tf_df = df[df[col_tf] == tf]
            lines.append(f"### TF {tf}\n")
            lines.append("| Symbol | Pass Rate | Passes | Total |")
            lines.append("|--------|-----------|--------|-------|")
            for sym in all_symbols:
                sym_tf = tf_df[tf_df[col_sym] == sym]
                n_st   = len(sym_tf)
                n_sp   = int(sym_tf["_passes"].sum()) if n_st else 0
                rate   = n_sp / n_st if n_st else 0.0
                lines.append(f"| {sym} | {rate:.0%} | {n_sp} | {n_st} |")
            lines.append("")
    else:
        lines.append("_DataFrame not available._\n")

    # ── 2. Universal Combos per TF ─────────────────────────────────────────────
    h("2. Universal Combos per Timeframe")
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

    # ── 3. Weighted Robustness Score ──────────────────────────────────────────
    h("3. Weighted Robustness Score")
    _n_tfs_rep   = n_timeframes
    _max_score   = 1.0 * 1.0 * (1.5 ** (_n_tfs_rep - 1))
    lines.append(
        "_How to read:_\n"
        "```\n"
        f"Final Score = avg_score × (coins_passing / {n_symbols}) × 1.5^(n_TFs − 1)\n"
        f"\n"
        f"avg_score     : mean _score of all passing rows for this signature\n"
        f"breadth       : coins_passing / {n_symbols}  — fraction of coins where sig passes on ≥1 TF\n"
        f"tf_multiplier : 1.5^(n_TFs − 1)  — exponential bonus for cross-TF validity\n"
        f"               1 TF → ×1.0  |  2 TFs → ×1.5  |  3 TFs → ×2.25\n"
        f"\n"
        f"high final_score  =  high quality  +  many coins  +  many TFs\n"
        f"max possible ≈ {_max_score:.3f}  (all {n_symbols} coins, {_n_tfs_rep} TFs, perfect quality)\n"
        "```\n"
    )
    if weighted_scores is not None and not weighted_scores.empty:
        ws_cols = ["Parameter Signature", "avg_score", "coins_passing", "n_TFs",
                   "breadth", "tf_multiplier", "final_score"]
        ws_avail = [c for c in ws_cols if c in weighted_scores.columns]
        header = " | ".join(ws_avail)
        sep    = " | ".join("---" for _ in ws_avail)
        lines.append(f"| {header} |")
        lines.append(f"|{sep}|")
        for _, r in weighted_scores.iterrows():
            cells = [_fmt_cell(r[c]) for c in ws_avail]
            lines.append(f"| {' | '.join(cells)} |")
        lines.append(f"\n_{len(weighted_scores)} signatures ranked.  "
                     f"Max possible Final Score ≈ **{_max_score:.3f}**._\n")
    else:
        lines.append("_No weighted score data available._\n")

    # ── 4. Parameter Stability ─────────────────────────────────────────────────
    h("4. Parameter Stability (Toggle Frequency)")
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

    # ── 5. Top Passing Combos ──────────────────────────────────────────────────
    h("5. Top Passing Combos")
    lines.append(
        "_How to read:_\n"
        f"```\n"
        f"combos that pass ALL thresholds  ({n_passing} / {n_total})\n"
        f"SQN ≥ {cfg.min_sqn}  AND  PF ≥ {cfg.min_profit_factor}  AND  trades ≥ {cfg.min_trades}\n"
        f"AND  win_rate ≥ {cfg.min_win_rate:.0f}%  AND  sharpe ≥ {cfg.min_sharpe}  AND  max_dd ≤ {cfg.max_max_drawdown:.0f}%\n\n"
        f"sorted by _score  (composite SQN + PF + Sharpe)\n"
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

    # ── 6. Threshold Sweep ─────────────────────────────────────────────────────
    h("6. Threshold Sweep")
    _robust_label = (
        f"Any combo passes  (N=1)"
        if sweep_min_passing_combos == 1
        else f"Robust (≥{sweep_min_passing_combos} combos)"
    )
    lines.append(
        "_How to read:_\n"
        "```\n"
        f"'{_robust_label}' line : coin ✅ if ≥ {sweep_min_passing_combos} of its combos pass\n"
        f"'Any combo passes' line       : coin ✅ if ≥ 1 combo passes\n\n"
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
            lines.append(f"| Min {metric_label} | {_robust_label} | Any combo passes | |")
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

    with st.expander("⚙️ Sweep settings"):
        sqn_sweep_range    = st.slider("SQN sweep range",    0.0, 3.0, (0.5, 2.0), 0.1,
            help="Range of Min SQN values to sweep over in Section 6.")
        pf_sweep_range     = st.slider("PF sweep range",     1.0, 5.0, (1.2, 3.0), 0.1,
            help="Range of Min Profit Factor values to sweep over in Section 6.")
        trades_sweep_range = st.slider("Trades sweep range", 1,   150,  (5, 40),    1,
            help="Range of Min # Trades values to sweep over in Section 6.")
        sweep_steps        = st.slider("Sweep steps",        5,   30,  15,         1,
            help="Number of evenly-spaced threshold values to evaluate per metric.")

    _prev_raw = st.session_state.get("_raw_df")

    with st.expander("🕐 Timeframe Filter", expanded=_prev_raw is not None):
        if _prev_raw is not None:
            _tf_col  = RobustnessConfig().col_timeframe
            _all_tfs = sorted(_prev_raw[_tf_col].dropna().unique().tolist())
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
            _all_syms_raw = sorted(_prev_raw[_sym_col_raw].dropna().unique().tolist())
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

    if st.session_state.get("_report_str"):
        st.markdown("---")
        _save_btn = st.button("💾 Save Report", use_container_width=True)
        _fname_default = st.session_state.get("_report_filename_default", f"{label}_phase1_v2.md")
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
st.title("📊 Strategy Robustness — Phase 1 v2")
st.markdown(
    "Sweep analysis across symbols and timeframes.  \n"
    "**Flow:** §3 → pick winning signature · §2 → verify which coins it breaks on · "
    "§4 → confirm key toggles · §5 → inspect raw metrics · §1 → diagnose per-TF breakdown · "
    "§6 → check threshold sensitivity."
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

# min_combo_pass_rate=0 means any passing combo counts — the sweep section uses its own floor.
cfg = RobustnessConfig(
    min_sqn=min_sqn,
    min_profit_factor=min_pf,
    min_trades=int(min_trades),
    min_win_rate=min_win_rate,
    min_sharpe=min_sharpe,
    max_max_drawdown=max_max_dd,
    min_combo_pass_rate=0.0,
)

# ── Load raw CSV (cached by directory path) ───────────────────────────────────
if st.session_state.get("_cached_dir") != results_dir:
    with st.spinner("Loading backtest results…"):
        try:
            _raw_df = load_run_dir(results_dir)
        except Exception as exc:
            st.error(f"Failed to load results directory: {exc}")
            st.stop()
        st.session_state["_raw_df"]      = _raw_df
        st.session_state["_cached_dir"]  = results_dir
        st.session_state["_data_period"] = load_data_period(results_dir)
        st.rerun()

raw_df = st.session_state["_raw_df"]
_data_period: tuple[str, str] | None = st.session_state.get("_data_period")

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

tog_freq = toggle_frequency(df, cfg)

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
        f"  AND  win_rate ≥ {min_win_rate:.0f}%  AND  sharpe ≥ {min_sharpe}  AND  max_dd ≤ {max_max_dd:.0f}%",
        language=None,
    )

# ── Sections ──────────────────────────────────────────────────────────────────

with st.expander("1. Performance per Timeframe", expanded=True):
    _section_per_tf_charts(cfg, df)

with st.expander("2. Universal Combos per Timeframe", expanded=True):
    _section_combo_overlap(cfg, df)

with st.expander("3. Weighted Robustness Score", expanded=True):
    _weighted_scored = _section_weighted_score(cfg, df)

with st.expander("4. Parameter Stability (Toggle Frequency)", expanded=True):
    _section_toggle_frequency(tog_freq)

with st.expander("5. Top Passing Combos", expanded=True):
    _section_top_combos(df, cfg)

# ── Section 6: Threshold Sweep ────────────────────────────────────────────────
with st.expander("6. Threshold Sweep", expanded=True):
    # Combos per symbol pooled across all TFs — used as slider max.
    _n_per_coin = _n_total // _n_symbols if _n_symbols else 1

    _sweep_min_combos = st.slider(
        "Min passing combos to count as 'robust'",
        min_value=1,
        max_value=_n_per_coin,
        value=1,
        step=1,
        key="sweep_min_combos",
        help=(
            f"A symbol counts as 'robust' if at least this many of its {_n_per_coin} combos "
            f"(pooled across all {_n_timeframes} TF(s)) pass all thresholds.  "
            f"1 = any passing combo counts (same as the 'Any combo passes' line).  "
            f"{_n_per_coin} = every single combo must pass."
        ),
    )
    _local_floor_pct = _sweep_min_combos / _n_per_coin
    _sweep_cfg = dataclasses.replace(cfg, min_combo_pass_rate=_local_floor_pct)

    _robust_label = (
        "Any combo passes  (N=1)"
        if _sweep_min_combos == 1
        else f"Robust (≥{_sweep_min_combos} combos)"
    )

    if _sweep_min_combos == 1:
        st.caption(
            "ℹ️ At N=1 the 'Robust' and 'Any combo passes' lines are identical. "
            "Increase the slider to see the gap widen."
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
            f"**Trades sweep** — cutoff filter (combos below excluded entirely).  "
            f"Too few trades → can't distinguish skill from luck.  "
            f"Active: `trades ≥ {min_trades}`"
        ),
    }

    _info(
        f"```\n"
        f"data: {_n_total:,} combos — {_n_symbols} coins × {_n_timeframes} TFs × {_n_param_sets} params\n"
        f"'{_robust_label}' line: coin ✅ if ≥ {_sweep_min_combos} of its {_n_per_coin} combos pass\n"
        f"'Any combo passes' line: coin ✅ if ≥ 1 combo passes\n"
        f"y = passing coins ÷ {_n_symbols}\n\n"
        f"steep drop  →  threshold sensitive  →  small change excludes many coins\n"
        f"flat line   →  stable zone  →  safe to move threshold here\n"
        f"```"
    )

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
            _sweep_df = sweep_threshold(df, _metric_col, _values, _sweep_cfg, comparison=_cmp)
        _sweep_results_for_report[_metric_label] = (_sweep_df, float(_active_val))

        _tidy = pd.concat([
            _sweep_df[["threshold", "symbol_pass_rate"]].rename(
                columns={"symbol_pass_rate": "pass_rate"}
            ).assign(metric=_robust_label),
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
                _robust_label:       "#2196F3",
                "Any combo passes":  "#FF9800",
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
_period_str = (
    f"_{_data_period[0]}_{_data_period[1]}"
    if _data_period else ""
)
_report_str = _format_phase1_report(
    label=label,
    results_dir=results_dir,
    run_ts=_run_ts,
    cfg=cfg,
    tog_freq=tog_freq,
    n_total=_n_total,
    n_passing=_n_passing,
    n_symbols=_n_symbols,
    n_timeframes=_n_timeframes,
    n_param_sets=_n_param_sets,
    sweep_min_passing_combos=_sweep_min_combos,
    df=df,
    sweep_data=_sweep_results_for_report,
    weighted_scores=_weighted_scored,
    data_period=_data_period,
)
st.session_state["_report_str"]             = _report_str
st.session_state["_report_filename_default"] = f"{_run_ts}_{label}{_period_str}_phase1_v2.md"

# ── Inline save button ────────────────────────────────────────────────────────
st.divider()
st.subheader("💾 Save Report")
_inline_fname_default = st.session_state.get("_report_filename_default", f"{_run_ts}_{label}_phase1_v2.md")
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
