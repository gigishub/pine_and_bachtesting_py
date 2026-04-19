"""Streamlit robustness dashboard for strategy backtest evaluation.

Run with:
    streamlit run strategy_evaluation/streamlit_app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure the project root is on sys.path so `strategy_evaluation` is importable
# regardless of the working directory when `streamlit run` is invoked.
sys.path.insert(0, str(Path(__file__).parent.parent))

import math
from collections import defaultdict
from datetime import datetime
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

from strategy_evaluation.config import RobustnessConfig
from strategy_evaluation.consistency import symbol_pass_rate, timeframe_pass_rate, toggle_frequency, sweep_threshold, compute_toggle_consensus
from strategy_evaluation.importance import (
    ImportanceResult,
    ShapResult,
    compute_shap_importance,
    compute_toggle_importance,
)
from strategy_evaluation.loader import load_data_period, load_run_dir, validate_columns
from strategy_evaluation.metrics import annotate_dataframe
from strategy_evaluation.report import format_report, save_report
from strategy_evaluation.scorer import RobustnessResult, aggregate_verdict
from strategy_evaluation.significance import OLSResult, compute_ols_significance

# ── Page config ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Strategy Robustness Evaluator",
    page_icon="\U0001f4ca",
    layout="wide",
)

_VERDICT_COLOUR = {"ROBUST": "#2ecc71", "MARGINAL": "#f39c12", "WEAK": "#e74c3c"}
_VERDICT_ICON   = {"ROBUST": "\u2705",  "MARGINAL": "\u26a0\ufe0f", "WEAK": "\u274c"}


# ── Helpers ──────────────────────────────────────────────────────────────────────

def _info(text: str, label: str = "\u2139\ufe0f How to read this") -> None:
    with st.expander(label):
        st.markdown(text)


def _verdict_banner(result: RobustnessResult) -> None:
    colour = _VERDICT_COLOUR[result.verdict]
    icon   = _VERDICT_ICON[result.verdict]
    st.markdown(
        f'<div style="background:{colour};padding:1rem 1.5rem;border-radius:8px;margin-bottom:0.6rem;">' +
        f'<h3 style="color:white;margin:0;">{icon} Verdict: {result.verdict}</h3></div>',
        unsafe_allow_html=True,
    )
    for note in result.notes:
        st.markdown(f"- {note}")


# ── Toggle categorisation ────────────────────────────────────────────────────
# All 4 categories come from the strategy's modular filter stack (strategy_1.md).
# Every use_* column must fall into exactly one; last category is the catch-all.
# Keywords are matched against the lowercase column name (prefix "use_" stripped).
_TOGGLE_CATEGORIES: dict[str, list[str]] = {
    # Step 1 — Market Regime Filter
    "Regime": [
        "adx", "mvrv", "ema", "ribbon", "ma_align", "ma_ribbon", "trend",
        "regime", "htf", "higher_tf", "bull", "bear", "market",
        "rsi_regime", "atr_regime", "vix", "hurst",
        "moving_avg", "moving_average", "sma_align", "dema", "tema",
    ],
    # Step 2 — Structural Setup
    "Setup": [
        "donchian", "channel", "breakout", "squeeze", "bb_squeeze",
        "vah", "val", "vpoc", "volume_profile", "value_area", "lvn",
        "rel_strength", "relative_strength", "ratio", "btc_ratio",
        "structure", "swing", "pattern", "level", "zone",
        "support", "resistance", "consol", "consolidat",
    ],
    # Step 3 — Execution Trigger
    "Execution Trigger": [
        "cmf", "chaikin", "cvd", "delta", "order_flow",
        "power_candle", "power_bar", "volume_spike", "vol_spike",
        "trigger", "entry", "signal", "confirm",
        "rsi", "stoch", "macd", "cross", "crossover",
        "engulf", "candle", "bar_pattern", "momentum",
        "diver", "divergen",
    ],
    # Step 4 — Risk & Exit Management (catch-all for anything not matched above)
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
    """Map a ``use_*`` column name to its strategy phase.

    Checks keywords in priority order; last category (Risk & Exit) is the
    catch-all so that every toggle lands in one of the 4 phases.
    """
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
    n_total      = len(df)
    n_symbols    = df[cfg.col_symbol].nunique()
    n_tfs        = df[cfg.col_timeframe].nunique()
    n_params     = n_total // (n_symbols * n_tfs) if (n_symbols * n_tfs) else 0
    n_per_coin   = n_total // n_symbols if n_symbols else 0
    floor        = cfg.min_combo_pass_rate

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
    from collections import defaultdict

    n_total          = len(df)
    n_symbols        = df[cfg.col_symbol].nunique()
    n_tfs            = df[cfg.col_timeframe].nunique()
    n_params         = n_total // (n_symbols * n_tfs) if (n_symbols * n_tfs) else 0
    n_per_tf         = n_total // n_tfs if n_tfs else 0
    n_per_coin_per_tf = n_per_tf // n_symbols if n_symbols else 0
    floor            = cfg.min_combo_pass_rate
    col_sym          = cfg.col_symbol
    col_tf           = cfg.col_timeframe

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

    timeframes = sorted(df[col_tf].unique())
    all_symbols = sorted(df[col_sym].unique())
    # coin → list of TFs it passes
    coin_tf_pass: dict[str, list[str]] = {sym: [] for sym in all_symbols}

    for tf in timeframes:
        tf_df      = df[df[col_tf] == tf]
        coin_rates = (
            tf_df.groupby(col_sym)["_passes"].mean()
            if "_passes" in tf_df.columns
            else pd.Series(dtype=float)
        )
        n_pass = int((coin_rates >= floor).sum())

        rows = [
            {
                "Symbol": sym,
                "Combo pass rate": float(coin_rates.get(sym, 0)),
                "n_total": int((tf_df[col_sym] == sym).sum()),
                "n_pass": int(tf_df[tf_df[col_sym] == sym]["_passes"].sum()) if "_passes" in tf_df.columns else 0,
            }
            for sym in all_symbols
        ]
        df_plot = pd.DataFrame(rows)
        df_plot["Status"] = df_plot["Combo pass rate"].apply(
            lambda r: "✅ Pass" if r >= floor else "❌ Fail"
        )

        st.markdown(f"##### TF: {tf}")
        fig = px.bar(
            df_plot, x="Symbol", y="Combo pass rate",
            color="Status",
            color_discrete_map={"✅ Pass": "#2ecc71", "❌ Fail": "#e74c3c"},
            title=f"{tf} — combo pass rate per coin",
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
        st.caption(f"**{tf}:** {n_pass} of {n_symbols} coins pass the {floor:.0%} floor")

        for sym in all_symbols:
            if coin_rates.get(sym, 0) >= floor:
                coin_tf_pass[sym].append(str(tf))

    # ── Coverage Summary ────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("**📊 TF Coverage per coin** — which timeframes does each coin pass?")

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


def _section_toggle_frequency(result: RobustnessResult) -> None:
    _info(
        "```\n"
        "# top-5 combos per (coin, TF) — from passing combos only  ⚙️ threshold-sensitive\n"
        "count = how often toggle is ON in those selections\n\n"
        "count → high  →  toggle in most passing combos  →  likely key ingredient\n"
        "count → low   →  toggle barely appears  →  probably not helping → consider removing\n\n"
        "no clear winner?  →  performance requires very specific combination  →  fragile signal\n"
        "```"
    )
    if not result.toggle_frequency:
        st.info("No toggle data available.")
        return
    df_tog = pd.DataFrame(
        [{"Toggle": k, "Count": v} for k, v in result.toggle_frequency.items()]
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



def _section_toggle_consensus(tc_df: pd.DataFrame) -> None:
    _info(
        "```\n"
        "Freq (top combos)\n"
        "  % of top-5 passing combos (per coin × TF) where this toggle is ON.\n"
        "  ⚙️ threshold-sensitive: changes when you move the SQN/PF/trades sliders.\n"
        "  High (≥60%) → toggle is consistently present when the strategy wins.\n"
        "  Low  (≤20%) → toggle is absent from winning combos — likely not contributing.\n"
        "\n"
        "OLS Coeff\n"
        "  Average change in SQN when the toggle switches OFF → ON, measured across ALL combos.\n"
        "  +0.32 means turning it ON raises SQN by 0.32 on average.\n"
        "  −0.67 means turning it ON lowers SQN by 0.67 on average.\n"
        "  — = unmeasurable: toggle was constant across all combos (always ON or always OFF),\n"
        "      OR perfectly correlated with another toggle → OLS had to drop it to avoid\n"
        "      a maths error. Use SHAP Mean as the only available direction signal instead.\n"
        "\n"
        "OLS p-value\n"
        "  Confidence that the OLS Coeff is real and not random noise.\n"
        "  < 0.05  → effect is real (less than 5% chance it's luck).\n"
        "  ≥ 0.05  → could be noise — don't act on OLS Coeff alone.\n"
        "  Very small values (e.g. 1e-21) → extremely strong evidence.\n"
        "\n"
        "OLS Sig\n"
        "  ✅ Yes → p < 0.05: trust the OLS Coeff direction.\n"
        "  ⚠️ No  → p ≥ 0.05: effect too weak or noisy to rely on alone.\n"
        "\n"
        "SHAP Mean\n"
        "  Signed average impact this toggle has on predicted SQN, from a Random Forest\n"
        "  trained on ALL combos (threshold-independent).\n"
        "  + → toggle ON pushes predicted SQN up   → probably helpful.\n"
        "  − → toggle ON pushes predicted SQN down → probably harmful.\n"
        "  Unlike OLS, SHAP captures non-linear effects and interactions between toggles.\n"
        "  — = toggle has zero variance in the dataset → RF can't assign any impact.\n"
        "```"
    )
    if tc_df.empty:
        st.info("No passing combos found \u2014 consensus unavailable.")
        return
    display = tc_df.copy()
    display["freq_pct"] = display["freq_pct"].map(lambda x: f"{x:.0%}")
    display["ols_coeff"] = display["ols_coeff"].map(
        lambda x: f"{x:+.4f}" if pd.notna(x) else "\u2014"
    )
    display["shap_mean"] = display["shap_mean"].map(
        lambda x: f"{x:+.3f}" if pd.notna(x) else "\u2014"
    )
    display["ols_sig"] = display["ols_sig"].map(
        lambda x: "\u2705 Yes" if x else "\u26a0\ufe0f No"
    )
    display = display.rename(columns={
        "toggle": "Toggle",
        "freq_pct": "Freq (top combos)",
        "ols_coeff": "OLS Coeff",
        "ols_p": "OLS p-value",
        "ols_sig": "OLS Sig",
        "shap_mean": "SHAP Mean",
        "consensus": "Consensus",
    })
    display = _add_category_col(display)
    st.dataframe(display, use_container_width=True, hide_index=True)
    _missing_ols = tc_df[tc_df["ols_coeff"].isna()]["toggle"].tolist()
    if _missing_ols:
        st.caption(
            f"\u2139\ufe0f **OLS `\u2014`** for {', '.join(f'`{t}`' for t in _missing_ols)}: "
            "toggle was constant across all combos (always ON or always OFF) or perfectly "
            "correlated with another toggle \u2014 OLS dropped it. "
            "SHAP direction is the only available signal for these."
        )


def _section_rf_importance(imp: ImportanceResult | None) -> None:
    _info(
        "```\n"
        "# Random Forest → predicts SQN from toggle values\n"
        "# ⚠️ threshold-independent: uses all combos, not just passing ones\n\n"
        "bar      →  % of SQN variance this toggle explains\n"
        "OOB R²   →  0 = toggles random  |  1 = toggles drive everything\n\n"
        "long bar  →  tune this toggle first\n"
        "short bar →  safe to deprioritise\n"
        "```"
    )
    if imp is None:
        st.info("Not enough data to compute toggle importance.")
        return
    df_imp = imp.importances.reset_index()
    df_imp.columns = pd.Index(["Toggle", "Importance"])
    df_imp = _add_category_col(df_imp)
    fig = px.bar(
        df_imp, x="Importance", y="Toggle", orientation="h",
        color="Category",
        color_discrete_map=_CATEGORY_COLOURS,
        category_orders={"Category": _CATEGORY_ORDER},
        title=f"Toggle Importance \u2192 SQN  (OOB R\u00b2={imp.r2_score:.3f}, n={imp.n_combos:,} combos)",
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)


def _section_shap(shap_result: ShapResult | None) -> None:
    _info(
        "```\n"
        "# RF importance + direction  (threshold-independent: all combos)\n\n"
        "🟢 SHAP > 0  →  toggle ON raises SQN  →  keep ON\n"
        "🔴 SHAP < 0  →  toggle ON lowers SQN  →  consider removing\n\n"
        "bar length = effect size\n"
        "confirm with OLS for statistical significance\n"
        "```"
    )
    if shap_result is None:
        st.info("SHAP analysis not available (shap package not installed or insufficient data).")
        return

    df_shap = pd.DataFrame(
        {"Toggle": shap_result.mean_shap.index, "Mean SHAP": shap_result.mean_shap.values}
    ).sort_values("Mean SHAP")
    df_shap["Direction"] = df_shap["Mean SHAP"].apply(
        lambda x: "Helps SQN \u2191" if x >= 0 else "Hurts SQN \u2193"
    )
    df_shap = _add_category_col(df_shap)

    fig = px.bar(
        df_shap, x="Mean SHAP", y="Toggle", orientation="h",
        color="Direction",
        color_discrete_map={"Helps SQN \u2191": "#2ecc71", "Hurts SQN \u2193": "#e74c3c"},
        title=f"Toggle Impact (SHAP) \u2192 SQN  (n={shap_result.n_combos:,} combos)",
        hover_data={"Category": True},
    )
    fig.add_vline(x=0, line_color="white", line_width=1)
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)


def _section_ols(ols_result: OLSResult | None) -> None:
    _info(
        "```\n"
        "# linear regression: toggle ON/OFF → SQN  (threshold-independent: all combos)\n\n"
        "coeff > 0  →  toggle ON  →  SQN ↑  (helps)\n"
        "coeff < 0  →  toggle ON  →  SQN ↓  (hurts)\n\n"
        "✅ p < 0.05  →  effect is real\n"
        "⚠️ p ≥ 0.05  →  could be noise  →  don't rely on alone\n\n"
        "R² = % of SQN variance explained by all toggles together\n"
        "```"
    )
    if ols_result is None:
        st.info("OLS analysis not available (statsmodels not installed or insufficient data).")
        return

    st.caption(
        f"OLS: SQN ~ toggles | R\u00b2={ols_result.r_squared:.3f} | n={ols_result.n_combos:,} combos"
    )

    display = ols_result.table.copy()
    display["significant"] = display["significant"].map({True: "\u2705 Yes", False: "\u26a0\ufe0f No"})
    display["coefficient"] = display["coefficient"].map(lambda x: f"{x:+.4f}")
    display["p_value"]     = display["p_value"].map(lambda x: f"{x:.4f}")
    display["std_err"]     = display["std_err"].map(lambda x: f"{x:.4f}")
    display["t_stat"]      = display["t_stat"].map(lambda x: f"{x:.2f}")
    display = display.rename(columns={
        "toggle": "Toggle", "coefficient": "Coefficient", "std_err": "Std Error",
        "t_stat": "t-stat", "p_value": "p-value", "significant": "Significant?",
    })
    display = _add_category_col(display)
    st.dataframe(display.reset_index(drop=True), use_container_width=True)


def _section_top_combos(df: pd.DataFrame, cfg: RobustnessConfig) -> None:
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


# ── Sidebar ──────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("\u2699\ufe0f Configuration")

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
            help="Range of Min SQN values to sweep over in Section 8.")
        pf_sweep_range     = st.slider("PF sweep range",     1.0, 5.0, (1.2, 3.0), 0.1,
            help="Range of Min Profit Factor values to sweep over in Section 8.")
        trades_sweep_range = st.slider("Trades sweep range", 1,   150,  (5, 40),    1,
            help="Range of Min # Trades values to sweep over in Section 8.")
        sweep_steps        = st.slider("Sweep steps",        5,   30,  15,         1,
            help="Number of evenly-spaced threshold values to evaluate per metric.")

    _prev_raw = st.session_state.get("_raw_df")

    with st.expander("🕐 Timeframe Filter"):
        if _prev_raw is not None:
            _tf_col  = RobustnessConfig().col_timeframe
            _all_tfs = sorted(_prev_raw[_tf_col].unique().tolist())
            active_timeframes: list | None = [
                tf for tf in _all_tfs
                if st.checkbox(str(tf), value=True, key=f"tf_{tf}")
            ]
        else:
            active_timeframes = None  # data not yet loaded; sentinel = no filter
            st.caption("📎 Timeframe filter available after the first run.")

    with st.expander("🔧 Toggle Pre-filter"):
        if _prev_raw is not None:
            _all_toggle_cols = sorted(c for c in _prev_raw.columns if c.startswith("use_"))
            # Group toggles by strategy phase
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

    with st.expander("🪙 Symbol Filter"):
        if _prev_raw is not None:
            _sym_col_raw  = RobustnessConfig().col_symbol
            _all_syms_raw = sorted(_prev_raw[_sym_col_raw].unique().tolist())
            _sym_mode = st.radio(
                "Mode", ["All", "1 pair", "Custom"],
                horizontal=True, key="sym_mode",
            )
            if _sym_mode == "All":
                selected_symbols = None  # no filter
            elif _sym_mode == "1 pair":
                _one_sym = st.selectbox("Select pair", _all_syms_raw, key="sym_one")
                selected_symbols = [_one_sym]
            else:  # Custom
                selected_symbols = st.multiselect(
                    "Select pairs", options=_all_syms_raw, default=_all_syms_raw, key="sym_custom",
                )
        else:
            selected_symbols = None  # sentinel: no filter until data loads
            st.caption("📎 Symbol filter available after the first run.")

    run_btn = st.button("▶ Run analysis", type="primary", use_container_width=True)

    # ── Save report (manual, on-demand) ──────────────────────────────────────
    if st.session_state.get("_report_str"):
        st.markdown("---")
        _save_btn = st.button("💾 Save Report", use_container_width=True)
        _fname_default = st.session_state.get("_report_filename_default", f"{label}_robustness.md")
        # If a new run just committed, reset the filename suggestion
        if st.session_state.pop("_reset_report_filename", False):
            if "report_filename_input" in st.session_state:
                del st.session_state["report_filename_input"]
        _save_fname = st.text_input("Filename", key="report_filename_input", value=_fname_default)
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

# ── Commit all sidebar values on Run click ───────────────────────────────────────
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
    # Signal sidebar save section to reset filename to the new default on next render
    st.session_state["_reset_report_filename"] = True


# ── Main ─────────────────────────────────────────────────────────────────────────
st.title("\U0001f4ca Strategy Robustness Evaluator")
st.markdown(
    "Evaluates backtest results across symbols and timeframes to determine "
    "whether a strategy is worth continued development."
)

# All analysis reads from the last committed snapshot — never from live sidebar values.
committed = st.session_state.get("committed")
if committed is None:
    st.info("Enter a results directory in the sidebar and click **\u25b6 Run analysis**.")
    st.stop()

c = committed

# Unpack committed values so the rest of the file can use the same variable names.
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
c_active_tfs       = c["active_timeframes"]  # None = data not loaded yet; [] = all deselected
c_selected_symbols = c.get("selected_symbols")  # None = all symbols; [] = user cleared all

if not results_dir:
    st.error("Please provide a results directory.")
    st.stop()

# Guard: user explicitly deselected every timeframe ([] vs None which means not yet loaded)
if isinstance(c_active_tfs, list) and len(c_active_tfs) == 0:
    st.warning(
        "No timeframes selected — tick at least one in **🕐 Timeframe Filter** and re-run."
    )
    st.stop()

# Guard: user explicitly cleared all symbols from the multiselect
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

# ── Load + heavy compute (cached by results_dir + filter key) ────────────────
# Step 1: load raw CSV — cached by directory path only (no ML).
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

# Step 2: run ML/SHAP/OLS — recompute only when committed filter selection changes.
_filter_key   = (
    tuple(sorted(c_forced_on)),
    tuple(sorted(c_forced_off)),
    tuple(sorted(str(t) for t in c_active_tfs)) if c_active_tfs else (),
    tuple(sorted(c_selected_symbols)) if c_selected_symbols else (),
)
_analysis_key = (results_dir, _filter_key)

if st.session_state.get("_cached_analysis_key") != _analysis_key:
    with st.spinner("Running analysis…"):
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
        _cfg0 = RobustnessConfig()
        st.session_state["_imp"]                 = compute_toggle_importance(_analysis_raw, _cfg0)
        st.session_state["_shap_result"]         = compute_shap_importance(_analysis_raw, _cfg0)
        st.session_state["_ols_result"]          = compute_ols_significance(_analysis_raw, _cfg0)
        st.session_state["_cached_analysis_key"] = _analysis_key

imp         = st.session_state["_imp"]
shap_result = st.session_state["_shap_result"]
ols_result  = st.session_state["_ols_result"]

# Step 3: build working df — apply same filters, then annotate with threshold cfg.
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

_n_raw_total = len(raw_df)  # unfiltered total (for banner when filter is active)

# Annotate with committed threshold cfg (fast — no ML, no regression)
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

sym_rates = symbol_pass_rate(df, cfg)
tf_rates  = timeframe_pass_rate(df, cfg)
tog_freq  = toggle_frequency(df, cfg)

result    = aggregate_verdict(sym_rates, tf_rates, tog_freq, pd.DataFrame(), df, df, cfg,
                              ols_result=ols_result, shap_result=shap_result)
toggle_consensus_df = compute_toggle_consensus(df, cfg, ols_result, shap_result)

# Combo count summary — computed once, reused in multiple sections
_n_total      = len(df)
_n_symbols    = df[cfg.col_symbol].nunique()
_n_timeframes = df[cfg.col_timeframe].nunique()
_n_param_sets = _n_total // (_n_symbols * _n_timeframes) if (_n_symbols * _n_timeframes) else 0
_n_passing    = int(df["_passes"].sum()) if "_passes" in df.columns else 0
_pct_passing  = _n_passing / _n_total if _n_total else 0

# ── 1. Verdict ────────────────────────────────────────────────────────────────
_all_raw_symbols   = set(raw_df[cfg.col_symbol].unique())
_is_sym_filtered   = c_selected_symbols is not None and set(c_selected_symbols) != _all_raw_symbols
_filter_active = bool(c_forced_off or c_forced_on or c_active_tfs or _is_sym_filtered)
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
st.subheader("3. Parameter Stability")
_section_toggle_frequency(result)

st.divider()
st.subheader("5. Toggle Importance (RandomForest)")
_section_rf_importance(imp)

st.divider()
st.subheader("6. Toggle Impact (SHAP)")
_section_shap(shap_result)

st.divider()
st.subheader("7. Toggle Significance (OLS)")
_section_ols(ols_result)

st.divider()
st.subheader("4. Toggle Consensus")
_section_toggle_consensus(toggle_consensus_df)

st.divider()
st.subheader("8. Top Passing Combos")
_section_top_combos(df, cfg)

st.divider()
st.subheader("9. Threshold Sweep")

# Build per-TF/per-coin combo counts for the explanation
_n_per_coin      = _n_total // _n_symbols if _n_symbols else 0
_n_per_cpt       = _n_total // (_n_symbols * _n_timeframes) if (_n_symbols * _n_timeframes) else 0
_tfs_sorted      = sorted(df[cfg.col_timeframe].unique())
_tf_lines        = "\n".join(f"  All {_n_per_cpt} combos on {tf}" for tf in _tfs_sorted)
_floor_pct       = cfg.min_combo_pass_rate

_info(
    f"```\n"
    f"# data: {_n_total:,} combos — {_n_symbols} coins × {_n_timeframes} TFs × {_n_param_sets} params\n"
    f"# coin ✅ if ≥ {_floor_pct:.0%} of its {_n_per_coin} combos pass the threshold being swept\n"
    f"# y = passing coins ÷ {_n_symbols}\n\n"
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
_sweep_results: dict[str, tuple[object, float]] = {}
for _metric_label, _metric_col, _sweep_range, _active_val, _cmp in _sweep_specs:
    st.markdown(_SWEEP_EXPLANATIONS[_metric_label])
    _lo, _hi = float(_sweep_range[0]), float(_sweep_range[1])
    _values = [float(v) for v in np.linspace(_lo, _hi, sweep_steps)]
    with st.spinner(f"Sweeping {_metric_label}…"):
        _sweep_df = sweep_threshold(df, _metric_col, _values, cfg, comparison=_cmp)
    _sweep_results[_metric_label] = (_sweep_df, float(_active_val))
    _sym_df = _sweep_df[["threshold", "symbol_pass_rate"]].rename(
        columns={"symbol_pass_rate": "Symbol pass rate"}
    )
    _fig = px.line(
        _sym_df, x="threshold", y="Symbol pass rate",
        title=(
            f"Symbol pass rate vs Min {_metric_label}  "
            f"({_n_symbols} coins, each = {_n_per_coin} combos pooled across {_n_timeframes} TFs)"
        ),
        labels={
            "threshold":        f"Min {_metric_label}",
            "Symbol pass rate": f"Symbol pass rate  (% of {_n_symbols} coins)",
        },
    )
    _fig.add_vline(
        x=float(_active_val), line_dash="dash", line_color="white",
        annotation_text="current threshold", annotation_position="top right",
    )
    _fig.update_layout(yaxis_range=[0, 1.05], yaxis_tickformat=".0%")
    st.plotly_chart(_fig, use_container_width=True)

# ── Store report for manual save via sidebar ──────────────────────────────────
_threshold_tag = f"sqn{min_sqn}_pf{min_pf}_trades{min_trades}_dd{max_max_dd}"
_thresholds = {
    "Min SQN":            (min_sqn,      "System Quality Number — consistency of returns. 1.0 = minimum viable; ≥2.0 = excellent."),
    "Min Profit Factor":  (min_pf,       "Gross profit ÷ gross loss. 1.5 = earn $1.50 per $1 lost. Below 1.0 = net loser."),
    "Min # Trades":       (min_trades,   "Minimum trades per combo — filters out statistically meaningless results."),
    "Min Win Rate (%)":   (min_win_rate, "% of trades that close in profit. Low is OK if winners are much larger than losers."),
    "Min Sharpe":         (min_sharpe,   "Risk-adjusted return. 0.5 = acceptable; ≥1.0 = good; ≥2.0 = exceptional."),
    "Max Drawdown (%)":   (max_max_dd,   "Maximum peak-to-trough equity drop allowed. Combos above this are excluded."),
}
report_str = format_report(
    result,
    label=label,
    results_path=results_dir,
    importance=imp,
    shap=shap_result,
    ols=ols_result,
    top_combos=df[df["_passes"]].copy() if "_passes" in df.columns else None,
    thresholds=_thresholds,
    data_period=load_data_period(results_dir),
    sweep_results=_sweep_results,
    toggle_consensus=toggle_consensus_df,
    combo_summary={
        "n_total": _n_total,
        "n_passing": _n_passing,
        "n_symbols": _n_symbols,
        "n_timeframes": _n_timeframes,
        "n_param_sets": _n_param_sets,
    },
    df=df,
    cfg=cfg,
)
_report_ts = datetime.now().strftime("%Y-%m-%d_%H%M")
st.session_state["_report_str"]             = report_str
st.session_state["_report_filename_default"] = f"{_report_ts}_{label}_robustness.md"
