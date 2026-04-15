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

import pandas as pd
import plotly.express as px
import streamlit as st

from strategy_evaluation.config import RobustnessConfig
from strategy_evaluation.consistency import symbol_pass_rate, timeframe_pass_rate, toggle_frequency
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

def _section_symbol_consistency(result: RobustnessResult, cfg: RobustnessConfig) -> None:
    _info(
        "**What this shows:** The fraction of toggle combinations that pass all thresholds "
        "for each coin.\n\n"
        "**How to use it:** A robust strategy should pass on most coins, not just one or two. "
        "If only 2 of 10 coins pass, the strategy may be specific to those coins and unlikely "
        "to generalise. Aim for at least 6 of 10 \u2705.\n\n"
        "**The dashed threshold line** shows the minimum pass rate you set (default 60%)."
    )
    rows = [{"Symbol": sym, "Pass rate": rate} for sym, rate in sorted(result.symbol_pass_rates.items())]
    df_sym = pd.DataFrame(rows)
    fig = px.bar(
        df_sym, x="Symbol", y="Pass rate",
        color="Pass rate",
        color_continuous_scale=["#e74c3c", "#f39c12", "#2ecc71"],
        range_color=[0, 1],
        title="Pass rate per symbol (fraction of timeframes where \u22651 combo passes)",
    )
    fig.add_hline(
        y=cfg.robust_symbol_rate, line_dash="dash", line_color="white",
        annotation_text="Threshold", annotation_position="top right",
    )
    fig.update_layout(coloraxis_showscale=False, yaxis_range=[0, 1.05])
    st.plotly_chart(fig, use_container_width=True)

    passing = sum(1 for v in result.symbol_pass_rates.values() if v > 0)
    c1, c2, c3 = st.columns(3)
    c1.metric("Symbols passing", f"{passing} / {len(result.symbol_pass_rates)}")
    c2.metric("Symbol pass rate", f"{result.symbol_rate:.0%}")
    c3.metric("Threshold", f"{cfg.robust_symbol_rate:.0%}")


def _section_tf_consistency(result: RobustnessResult, cfg: RobustnessConfig) -> None:
    _info(
        "**What this shows:** For each timeframe (1H, 4H, 1D) the fraction of symbols where "
        "at least one combo passes thresholds.\n\n"
        "**How to use it:** A strategy that only works on the 1H but not 4H or 1D may be "
        "curve-fitted to short-term noise. A robust strategy should work across at least two "
        "timeframes. The bar should be above the dashed threshold line."
    )
    rows = [{"Timeframe": tf, "Pass rate": rate} for tf, rate in sorted(result.tf_pass_rates.items())]
    df_tf = pd.DataFrame(rows)
    fig = px.bar(
        df_tf, x="Timeframe", y="Pass rate",
        color="Pass rate",
        color_continuous_scale=["#e74c3c", "#f39c12", "#2ecc71"],
        range_color=[0, 1],
        title="Pass rate per timeframe (fraction of symbols where \u22651 combo passes)",
    )
    fig.add_hline(
        y=cfg.robust_tf_rate, line_dash="dash", line_color="white",
        annotation_text="Threshold", annotation_position="top right",
    )
    fig.update_layout(coloraxis_showscale=False, yaxis_range=[0, 1.05])
    st.plotly_chart(fig, use_container_width=True)


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

    run_btn = st.button("\u25b6 Run analysis", type="primary", use_container_width=True)


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
)

with st.spinner("Loading backtest results\u2026"):
    try:
        df = annotate_dataframe(load_run_dir(results_dir), cfg)
    except Exception as exc:
        st.error(f"Failed to load results directory: {exc}")
        st.stop()

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
result    = aggregate_verdict(sym_rates, tf_rates, tog_freq, pd.DataFrame(), df, df, cfg)

# ── 1. Verdict ────────────────────────────────────────────────────────────────
_verdict_banner(result)
_info(
    "**ROBUST** \u2705 \u2014 \u2265 60% of symbols pass, \u2265 60% of timeframes pass, avg SQN \u2265 1.0. "
    "Worth investing more development time.\n\n"
    "**MARGINAL** \u26a0\ufe0f \u2014 Passes some tests but not all. Promising but not proven. "
    "Identify the weak area and address it before going live.\n\n"
    "**WEAK** \u274c \u2014 Fails key thresholds. Not reliable enough to trade. "
    "Revisit the strategy logic or parameters.",
    label="\u2139\ufe0f What do ROBUST / MARGINAL / WEAK mean?",
)
passing_syms = sum(1 for v in result.symbol_pass_rates.values() if v > 0)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Symbols passing",  f"{passing_syms}/{len(result.symbol_pass_rates)}")
c2.metric("Symbol pass rate", f"{result.symbol_rate:.0%}")
c3.metric("TF pass rate",     f"{result.tf_rate:.0%}")
c4.metric("Avg SQN (top-1)", f"{result.avg_sqn_long:.2f}")

st.divider()
st.subheader("1. Symbol Consistency")
_section_symbol_consistency(result, cfg)

st.divider()
st.subheader("2. Timeframe Consistency")
_section_tf_consistency(result, cfg)

st.divider()
st.subheader("3. Parameter Stability")
_section_toggle_frequency(result)

st.divider()
st.subheader("4. Toggle Importance (RandomForest)")
with st.spinner("Training RandomForest\u2026"):
    imp = compute_toggle_importance(df, cfg)
_section_rf_importance(imp)

st.divider()
st.subheader("5. Toggle Impact (SHAP)")
with st.spinner("Computing SHAP values\u2026"):
    shap_result = compute_shap_importance(df, cfg)
_section_shap(shap_result)

st.divider()
st.subheader("6. Toggle Significance (OLS)")
ols_result = compute_ols_significance(df, cfg)
_section_ols(ols_result)

st.divider()
st.subheader("7. Top Passing Combos")
_section_top_combos(df, cfg)

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
)
try:
    _save_path = Path(results_dir).expanduser().resolve()
    _saved = save_report(report_str, label=f"{label}_{_threshold_tag}", output_dir=_save_path)
    st.divider()
    st.caption(f"📄 Report auto-saved → `{_saved}`")
except Exception as _exc:
    st.warning(f"Report could not be saved: {_exc}")
