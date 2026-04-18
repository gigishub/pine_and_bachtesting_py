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
        f"**{n_total:,} total combos split across {n_symbols} coins → {n_per_coin} combos per coin**  \n"
        f"({n_tfs} timeframes × {n_params} parameter sets per coin)\n\n"
        f"**Bar height** = fraction of those {n_per_coin} combos that pass all thresholds.  \n"
        f"**100%** = every combo works on every TF.  **0%** = no combo works on any TF — skip that coin.\n\n"
        f"**Floor line:** ≥ **{floor:.0%}** of combos must pass → ✅ Pass   |   Below → ❌ Fail"
    )

    combo_rates = (
        df.groupby(cfg.col_symbol)["_passes"].mean()
        if "_passes" in df.columns
        else pd.Series(dtype=float)
    )
    rows = [
        {"Symbol": sym, "Combo pass rate": float(combo_rates.get(sym, 0))}
        for sym in sorted(combo_rates.index)
    ]
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
        f"**Same {n_total:,} combos — now split by timeframe:** {n_per_tf:,} combos per TF  \n"
        f"= {n_symbols} coins × {n_params} parameter sets\n\n"
        f"**Each chart below = one timeframe.** Bar = fraction of the coin's  \n"
        f"{n_per_coin_per_tf} combos on THAT timeframe that pass all thresholds.  \n"
        f"**100%** = all {n_per_coin_per_tf} combos pass.  **0%** = none pass on this TF.\n\n"
        f"Use these charts to find which (coin, TF) pairs actually work."
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
            {"Symbol": sym, "Combo pass rate": float(coin_rates.get(sym, 0))}
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
        "**What this shows:** Which indicator toggles appear most often in the best-performing "
        "parameter combinations across all symbols and timeframes.\n\n"
        "**How to use it:** A toggle that shows up everywhere is a key ingredient. "
        "One that barely appears is probably not helping — consider removing it to simplify "
        "the strategy.\n\n"
        "If no single toggle dominates and results are scattered, the strategy may be fragile: "
        "its performance depends on a very specific combination of conditions."
    )
    if not result.toggle_frequency:
        st.info("No toggle data available.")
        return
    df_tog = pd.DataFrame(
        [{"Toggle": k, "Count": v} for k, v in result.toggle_frequency.items()]
    ).sort_values("Count")
    fig = px.bar(
        df_tog, x="Count", y="Toggle", orientation="h",
        title="Toggle frequency in top-5 combos per symbol/timeframe",
        color="Count", color_continuous_scale="Blues",
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"}, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)



def _section_toggle_consensus(tc_df: pd.DataFrame) -> None:
    _info(
        "**What this shows:** A cross-check of all three toggle signals in one table.\n\n"
        "- **Freq (top combos)** \u2014 how often this toggle appears in the top-5 passing combos "
        "per symbol/timeframe *(threshold-sensitive)*.\n"
        "- **OLS Coeff** \u2014 average change in SQN when toggle is ON across *all* combos. "
        "Positive = helps. \u2705 = statistically significant (p < 0.05).\n"
        "- **SHAP Mean** \u2014 signed mean SHAP when toggle is ON. Positive = raises SQN.\n\n"
        "**Verdicts:**\n"
        "- \u2705 **Keep ON** \u2014 all three signals agree the toggle helps.\n"
        "- \u274c **Remove** \u2014 all three signals agree the toggle hurts.\n"
        "- \u26a0\ufe0f **Conflict** \u2014 frequency and OLS/SHAP disagree. The toggle may be present "
        "incidentally in passing combos but not actually driving performance.\n"
        "- \u2014 **Neutral** \u2014 insufficient signal to make a recommendation."
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
    st.dataframe(display, use_container_width=True, hide_index=True)


def _section_rf_importance(imp: ImportanceResult | None) -> None:
    _info(
        "**What this shows:** A Random Forest model was trained on all parameter combinations "
        "to predict SQN. The bars show how much each toggle reduces prediction error — "
        "a longer bar means that toggle explains more of the performance difference between "
        "combinations.\n\n"
        "**OOB R\u00b2** = how much of the total SQN variance the toggles explain together. "
        "Close to 1.0 = toggles drive most of the performance. Close to 0 = performance "
        "is mostly random or driven by something the toggles don't capture.\n\n"
        "**How to use it:** Focus development effort on the top-ranked toggles. "
        "The bottom ones are probably not worth fine-tuning."
    )
    if imp is None:
        st.info("Not enough data to compute toggle importance.")
        return
    df_imp = imp.importances.reset_index()
    df_imp.columns = pd.Index(["Toggle", "Importance"])
    fig = px.bar(
        df_imp, x="Importance", y="Toggle", orientation="h",
        color="Importance", color_continuous_scale="Blues",
        title=f"Toggle Importance \u2192 SQN  (OOB R\u00b2={imp.r2_score:.3f}, n={imp.n_combos:,} combos)",
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"}, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)


def _section_shap(shap_result: ShapResult | None) -> None:
    _info(
        "**What this shows:** SHAP (SHapley Additive exPlanations) adds **direction** to "
        "the Random Forest importance — does enabling this toggle raise or lower SQN?\n\n"
        "- \U0001f7e2 **Green bar (positive)** \u2192 enabling this toggle *increases* SQN on average\n"
        "- \U0001f534 **Red bar (negative)** \u2192 enabling this toggle *decreases* SQN on average\n"
        "- Bar length = size of the effect\n\n"
        "**How to use it:** Green bars are filters you should keep ON. Red bars are filters "
        "that are actively hurting performance — consider removing them. "
        "This is more informative than the Random Forest importance alone because it shows "
        "whether a toggle is helping or hurting, not just whether it matters."
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

    fig = px.bar(
        df_shap, x="Mean SHAP", y="Toggle", orientation="h",
        color="Direction",
        color_discrete_map={"Helps SQN \u2191": "#2ecc71", "Hurts SQN \u2193": "#e74c3c"},
        title=f"Toggle Impact (SHAP) \u2192 SQN  (n={shap_result.n_combos:,} combos)",
    )
    fig.add_vline(x=0, line_color="white", line_width=1)
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)


def _section_ols(ols_result: OLSResult | None) -> None:
    _info(
        "**What this shows:** A statistical test (OLS regression) checks whether each "
        "toggle's effect on SQN is *real* or could be random noise.\n\n"
        "- **Coefficient** = the average change in SQN when that toggle is switched ON. "
        "  Positive = it helps. Negative = it hurts.\n"
        "- **p-value** = probability the effect is due to chance. "
        "  \u2705 p < 0.05 = statistically significant (real effect). "
        "  \u26a0\ufe0f p \u2265 0.05 = the effect could be noise.\n"
        "- **R\u00b2** = how much of all SQN variance is explained by the toggles together.\n\n"
        "**How to use it:** Only trust toggles marked \u2705. A toggle with a positive "
        "coefficient but \u26a0\ufe0f could be a false positive from backtesting noise — "
        "do not rely on it. Focus on \u2705 toggles with the largest positive coefficients; "
        "those are your most reliable filters."
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
    st.dataframe(display.reset_index(drop=True), use_container_width=True)


def _section_top_combos(df: pd.DataFrame, cfg: RobustnessConfig) -> None:
    _info(
        "**What this shows:** Every toggle combination that passed all your thresholds, "
        "sorted by composite score (best SQN + Profit Factor + Sharpe together).\n\n"
        "**How to use it:** Pick the top 3\u20135 combinations and carry them forward to "
        "walk-forward testing or paper trading — these are your most promising setups. "
        "If the list is very short (< 5 combos total), the strategy is too restrictive; "
        "consider relaxing some thresholds. If it is very long (> 50), tighten them."
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
    st.subheader("Thresholds")
    min_sqn      = st.slider("Min SQN",           0.0,  3.0,  1.0,  0.1,
        help="System Quality Number — how consistently the strategy makes money. "
             "1.0 = minimum viable; ≥2.0 = excellent.")
    min_pf       = st.slider("Min Profit Factor",  1.0,  5.0,  1.5,  0.1,
        help="Gross profit ÷ gross loss. 1.5 means you earn $1.50 for every $1 lost. "
             "Below 1.0 = net loser.")
    min_trades   = st.slider("Min # Trades",       1,    50,   10,   1,
        help="Minimum number of trades a combo must have to count — filters out "
             "combos with so few trades that stats are meaningless.")
    min_win_rate = st.slider("Min Win Rate (%)",   0.0,  70.0, 30.0, 1.0,
        help="Percentage of trades that close in profit. Low win rate is acceptable "
             "if average winner is much larger than average loser.")
    min_sharpe   = st.slider("Min Sharpe",         0.0,  2.0,  0.5,  0.05,
        help="Risk-adjusted return (return ÷ volatility). 0.5 = acceptable; "
             "≥1.0 = good; ≥2.0 = exceptional.")
    max_max_dd   = st.slider("Max Drawdown (%)",   10.0, 80.0, 40.0, 1.0,
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
        trades_sweep_range = st.slider("Trades sweep range", 1,   50,  (5, 40),    1,
            help="Range of Min # Trades values to sweep over in Section 8.")
        sweep_steps        = st.slider("Sweep steps",        5,   30,  15,         1,
            help="Number of evenly-spaced threshold values to evaluate per metric.")

    st.markdown("---")
    st.subheader("🔧 Toggle Pre-filter")
    _prev_raw = st.session_state.get("_raw_df")
    if _prev_raw is not None:
        _all_toggle_cols = sorted(c for c in _prev_raw.columns if c.startswith("use_"))
        forced_off_toggles = st.multiselect(
            "Force toggles OFF",
            _all_toggle_cols,
            help=(
                "Exclude every combo where any of these toggles is ON before running "
                "analysis. Useful for re-testing without a specific indicator. "
                "RF, SHAP, and OLS will all recompute on the filtered subset. "
                "Hit ▶ Run analysis to apply."
            ),
        )
    else:
        forced_off_toggles: list[str] = []
        st.caption("📎 Toggle filter available after the first run.")

    run_btn = st.button("▶ Run analysis", type="primary", use_container_width=True)


# ── Main ─────────────────────────────────────────────────────────────────────────
st.title("\U0001f4ca Strategy Robustness Evaluator")
st.markdown(
    "Evaluates backtest results across symbols and timeframes to determine "
    "whether a strategy is worth continued development."
)

if not run_btn:
    st.info("Enter a results directory in the sidebar and click **\u25b6 Run analysis**.")
    st.stop()

if not results_dir:
    st.error("Please provide a results directory.")
    st.stop()

cfg = RobustnessConfig(
    min_sqn=min_sqn,
    min_profit_factor=min_pf,
    min_trades=int(min_trades),
    min_win_rate=min_win_rate,
    min_sharpe=min_sharpe,
    max_max_drawdown=max_max_dd,
    min_combo_pass_rate=min_combo_pass_rate,
)

# ── Load + heavy compute (cached by results_dir + toggle filter) ─────────────
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

raw_df = st.session_state["_raw_df"]

# Step 2: apply toggle pre-filter (RF/SHAP/OLS are recomputed when it changes).
_filter_key      = tuple(sorted(forced_off_toggles))
_analysis_key    = (results_dir, _filter_key)

if st.session_state.get("_cached_analysis_key") != _analysis_key:
    with st.spinner("Running analysis…"):
        _analysis_raw = raw_df
        for _t in forced_off_toggles:
            if _t in _analysis_raw.columns:
                _analysis_raw = _analysis_raw[_analysis_raw[_t] == 0]
        _cfg0 = RobustnessConfig()
        st.session_state["_imp"]                = compute_toggle_importance(_analysis_raw, _cfg0)
        st.session_state["_shap_result"]        = compute_shap_importance(_analysis_raw, _cfg0)
        st.session_state["_ols_result"]         = compute_ols_significance(_analysis_raw, _cfg0)
        st.session_state["_cached_analysis_key"] = _analysis_key

imp         = st.session_state["_imp"]
shap_result = st.session_state["_shap_result"]
ols_result  = st.session_state["_ols_result"]

# Step 3: build the working df — filter raw rows, then annotate with thresholds.
_analysis_raw = raw_df
for _t in forced_off_toggles:
    if _t in _analysis_raw.columns:
        _analysis_raw = _analysis_raw[_analysis_raw[_t] == 0]

_n_raw_total = len(raw_df)  # unfiltered total (for banner when filter is active)

# Annotate with current threshold cfg (fast — no ML, no regression)
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
if forced_off_toggles:
    _n_excluded    = _n_raw_total - _n_total
    _filter_labels = ", ".join(f"`{t}=OFF`" for t in forced_off_toggles)
    st.info(
        f"📊 **{_n_total:,} combos after filter** "
        f"({_n_excluded:,} excluded — {_filter_labels}).  "
        f"With current thresholds: **{_n_passing:,} pass ({_pct_passing:.1%})**."
    )
else:
    st.info(
        f"📊 **{_n_total:,} total combos** — {_n_symbols} symbols × {_n_timeframes} timeframes × "
        f"{_n_param_sets} parameter sets.  "
        f"With current thresholds: **{_n_passing:,} pass ({_pct_passing:.1%})**."
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
st.subheader("4. Toggle Consensus")
_section_toggle_consensus(toggle_consensus_df)

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
    f"**Your {_n_total:,} combos come from:**  \n"
    f"  {_n_symbols} coins × {_n_timeframes} TFs × {_n_param_sets} parameter sets\n\n"
    f"**For each coin, we pool ALL timeframes together:**\n"
    f"{_tf_lines}\n"
    f"  {'─' * 34}\n"
    f"  Total: **{_n_per_coin} combos per coin**\n\n"
    f"A coin **passes** if ≥ **{_floor_pct:.0%}** of its {_n_per_coin} combos pass the threshold being swept.\n"
    f"**Symbol Pass Rate** = passing coins ÷ {_n_symbols}\n\n"
    "The chart shows: as you tighten a threshold (left → right), how many of the "
    f"{_n_symbols} coins still pass?  \n"
    "A **steep drop** = cliff edge — small changes exclude many coins.  \n"
    "A **flat line** = stable zone — threshold can be safely moved here."
)

_SWEEP_EXPLANATIONS = {
    "SQN": (
        "**Min SQN (System Quality Number)** measures how *consistently* the strategy profits. "
        "Below 1.0 = not viable; 1–2 = acceptable; ≥ 2 = strong. "
        "Raising this floor filters out lucky one-off backtests and keeps only strategies "
        "that profit steadily across many trades."
    ),
    "Profit Factor": (
        "**Min Profit Factor** = gross profit ÷ gross loss across all trades in a combo. "
        "1.5 means you earn $1.50 for every $1.00 lost. "
        "Increasing this rewards strategies with a large win/loss ratio — "
        "useful when win rate is low but winners are much bigger than losers."
    ),
    "# Trades": (
        "**Min # Trades** — any combo that made fewer than this many total trades over "
        "the full test period is **excluded entirely** (cutoff filter, not a penalty).  \n"
        "A combo that only fired 8 times in 3 years cannot be judged — skill or luck?  \n"
        "Raising this threshold keeps only combos with enough trade history to be statistically "
        "meaningful.  A steep drop here means many combos barely traded enough to count."
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

# ── Auto-save report ──────────────────────────────────────────────────────────
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
try:
    _save_path = Path(results_dir).expanduser().resolve()
    _saved = save_report(report_str, label=f"{label}_{_threshold_tag}", output_dir=_save_path)
    st.divider()
    st.caption(f"📄 Report auto-saved → `{_saved}`")
except Exception as _exc:
    st.warning(f"Report could not be saved: {_exc}")
