"""Streamlit dashboard for bear_strategy run_grid results.

Launch:
    streamlit run bear_strategy/backtest/strategy_evaluation/grid_dashboard.py

Tabs
----
🏆 Robustness  — weighted cross-symbol scores
🔍 Per-Symbol  — per-combo gate matrix + full metrics
🔀 Exit Flags  — toggle frequency + flag × combo heatmap
📊 Compare     — side-by-side two run directories
🗃️ Raw Data    — filterable table + CSV download
"""

from __future__ import annotations

import sys
from pathlib import Path

# ── Add project root so root-level packages are importable ────────────────────
sys.path.insert(0, str(Path(__file__).parents[3]))

import pandas as pd
import streamlit as st

from bear_strategy.backtest.strategy_evaluation.grid_loader import (
    detect_toggle_cols,
    list_run_dirs,
    load_run_dir,
    sig_short_label,
)
from bear_strategy.backtest.strategy_evaluation.grid_scoring import (
    DEFAULT_MAX_DD,
    DEFAULT_MIN_PF,
    DEFAULT_MIN_SQN,
    DEFAULT_MIN_TRADES,
    DEFAULT_MIN_WR,
    annotate,
    compute_weighted_scores,
)

# ── Paths ─────────────────────────────────────────────────────────────────────
_HERE = Path(__file__).parent
_RESULTS_ROOT = _HERE.parents[0] / "vectorbt" / "results"

# ── Streamlit page config ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="Bear Grid Evaluation",
    page_icon="🐻",
    layout="wide",
)

# ══════════════════════════════════════════════════════════════════════════════
# Helpers
# ══════════════════════════════════════════════════════════════════════════════

_METRIC_COLS = [
    "Return [%]", "SQN", "Profit Factor", "Expectancy [%]",
    "Win Rate [%]", "Max Drawdown [%]", "# Trades",
    "Sharpe Ratio", "Calmar Ratio",
]


@st.cache_data(show_spinner=False)
def _load(run_dir: str) -> pd.DataFrame:
    return load_run_dir(run_dir)


def _gate_sidebar_suffix(suffix: str = "") -> dict:
    """Render gate controls in sidebar, return kwargs dict."""
    sl = st.sidebar
    s = suffix
    return {
        "min_sqn":    sl.slider(f"Min SQN{s}",         -2.0, 5.0, float(DEFAULT_MIN_SQN), 0.1),
        "min_pf":     sl.slider(f"Min Profit Factor{s}", 0.5, 5.0, float(DEFAULT_MIN_PF),  0.1),
        "min_trades": sl.slider(f"Min # Trades{s}",       1, 200,  int(DEFAULT_MIN_TRADES), 1),
        "min_wr":     sl.slider(f"Min Win Rate %{s}",     0.0, 80.0, float(DEFAULT_MIN_WR), 0.5),
        "max_dd":     sl.slider(f"Max Drawdown %{s}",    10.0, 100.0, float(DEFAULT_MAX_DD), 1.0),
    }


def _gradient(df: pd.DataFrame, cols: list[str]) -> "pd.io.formats.style.Styler":
    """Apply green-red gradient on selected numeric columns."""
    available = [c for c in cols if c in df.columns]
    style = df.style
    for col in available:
        if col == "Max Drawdown [%]":
            style = style.background_gradient(subset=[col], cmap="RdYlGn_r")
        else:
            style = style.background_gradient(subset=[col], cmap="RdYlGn")
    return style.format({c: "{:.2f}" for c in available if c != "# Trades"})


def _metric_card(col, label: str, value: str, delta: str = "") -> None:
    col.metric(label=label, value=value, delta=delta or None)


# ══════════════════════════════════════════════════════════════════════════════
# Sidebar
# ══════════════════════════════════════════════════════════════════════════════

st.sidebar.header("🐻 Bear Grid Evaluation")

run_dirs = list_run_dirs(_RESULTS_ROOT)

if not run_dirs:
    st.error(
        f"No run directories found under `{_RESULTS_ROOT}`.\n\n"
        "Run `python -m bear_strategy.backtest.vectorbt.run_grid --config default` first."
    )
    st.stop()

dir_labels = {d.name: d for d in run_dirs}

st.sidebar.subheader("Primary run")
primary_name = st.sidebar.selectbox("Select run", list(dir_labels.keys()), index=0)
primary_dir  = dir_labels[primary_name]

st.sidebar.subheader("Gates")
gates = _gate_sidebar_suffix()

st.sidebar.subheader("Minimum symbols passing")
min_symbols = st.sidebar.slider("Min symbols", 1, 20, 2, 1)

# Load + annotate
try:
    raw_df = _load(str(primary_dir))
except Exception as exc:
    st.error(f"Failed to load '{primary_name}': {exc}")
    st.stop()

df = annotate(raw_df, **gates)

# Symbol filter
all_symbols = sorted(str(s) for s in df["Symbol"].dropna().unique()) if "Symbol" in df.columns else []
selected_symbols = st.sidebar.multiselect(
    "Filter symbols", all_symbols, default=all_symbols
)
if selected_symbols:
    df = df[df["Symbol"].isin(selected_symbols)]

# ══════════════════════════════════════════════════════════════════════════════
# Tabs
# ══════════════════════════════════════════════════════════════════════════════

tab_robust, tab_sym, tab_flags, tab_compare, tab_raw = st.tabs([
    "🏆 Robustness", "🔍 Per-Symbol", "🔀 Exit Flags", "📊 Compare", "🗃️ Raw Data"
])

# ─────────────────────────────────────────────────────────────────────────────
# Tab 1: Robustness
# ─────────────────────────────────────────────────────────────────────────────
with tab_robust:
    st.header("Weighted Robustness Scores")
    st.caption(
        "final_score = avg_score × (symbols_passing / N_total)  "
        "· avg_score uses SQN 30%, PF 25%, Exp 25%, Sharpe 10%, DD 10%"
    )

    scores_df = compute_weighted_scores(df)

    if scores_df.empty:
        st.warning("No combos pass all gates across any symbols with current settings.")
    else:
        # Filter by min_symbols
        filtered = scores_df[scores_df["symbols_passing"] >= min_symbols]

        if filtered.empty:
            st.warning(f"No combos pass gates on ≥ {min_symbols} symbols.")
        else:
            # Top-3 cards
            top3 = filtered.head(3)
            cols_card = st.columns(min(3, len(top3)))
            for i, (_, row) in enumerate(top3.iterrows()):
                _metric_card(
                    cols_card[i],
                    label=f"#{i+1}  {sig_short_label(str(row['Parameter Signature']))}",
                    value=f"{row['final_score']:.3f}",
                    delta=f"{row['symbols_passing']}/{row['N_total']} symbols",
                )

            st.divider()

            display = filtered.copy()
            display["short_label"] = display["Parameter Signature"].apply(sig_short_label)
            show_cols = [
                "short_label", "final_score", "avg_score",
                "symbols_passing", "breadth", "Parameter Signature",
            ]
            show_cols = [c for c in show_cols if c in display.columns]
            st.dataframe(
                _gradient(display[show_cols], ["final_score", "avg_score", "breadth"])
                .format({"final_score": "{:.4f}", "avg_score": "{:.4f}", "breadth": "{:.2%}"}),
                use_container_width=True,
            )

# ─────────────────────────────────────────────────────────────────────────────
# Tab 2: Per-Symbol
# ─────────────────────────────────────────────────────────────────────────────
with tab_sym:
    st.header("Per-Symbol Gate Matrix")

    if df.empty:
        st.info("No data loaded.")
    else:
        all_sigs = sorted(df["Parameter Signature"].unique().tolist())
        passing_sigs = sorted(df[df["_passes"]]["Parameter Signature"].unique().tolist())

        show_mode = st.radio("Combos to show", ["Passing only", "All"], horizontal=True)
        sig_pool = passing_sigs if show_mode == "Passing only" else all_sigs

        if not sig_pool:
            st.warning("No combos in selection.")
        else:
            # Build pass matrix: rows = signatures, cols = symbols
            pivot = (
                df[df["Parameter Signature"].isin(sig_pool)]
                .pivot_table(
                    index="Parameter Signature",
                    columns="Symbol",
                    values="_passes",
                    aggfunc="max",
                )
                .fillna(False)
                .astype(bool)
            )
            pivot.index = [sig_short_label(s) for s in pivot.index]
            st.subheader("Pass / Fail matrix")
            st.dataframe(
                pivot.style.map(lambda v: "background-color:#1a7a3b;color:white" if v else "background-color:#8b1a1a;color:white"),
                use_container_width=True,
            )

            st.divider()
            chosen_sig = st.selectbox("Inspect combo metrics", sig_pool)
            combo_df = df[df["Parameter Signature"] == chosen_sig][
                ["Symbol"] + [c for c in _METRIC_COLS if c in df.columns] + ["_passes", "_score"]
            ].sort_values("Symbol")

            st.dataframe(
                _gradient(combo_df, _METRIC_COLS),
                use_container_width=True,
            )

# ─────────────────────────────────────────────────────────────────────────────
# Tab 3: Exit Flags
# ─────────────────────────────────────────────────────────────────────────────
with tab_flags:
    st.header("Exit Flag Analysis")

    toggle_cols = detect_toggle_cols(df)

    if not toggle_cols:
        st.info("No `use_*` toggle columns detected in this run's results.")
    else:
        try:
            import plotly.express as px
        except ImportError:
            st.error("Install plotly: `pip install plotly`")
            st.stop()

        col_l, col_r = st.columns(2)

        # Left: frequency bar chart (what fraction of passing combos use each flag)
        with col_l:
            st.subheader("Flag frequency in passing combos")
            passing = df[df["_passes"]]
            if passing.empty:
                st.info("No passing combos.")
            else:
                freq = {
                    col: float(passing[col].mean())
                    for col in toggle_cols
                    if col in passing.columns
                }
                freq_df = (
                    pd.DataFrame.from_dict(freq, orient="index", columns=["freq"])
                    .sort_values("freq", ascending=False)
                    .reset_index()
                    .rename(columns={"index": "flag"})
                )
                fig = px.bar(
                    freq_df, x="flag", y="freq",
                    labels={"freq": "Fraction active (passing combos)"},
                    color="freq", color_continuous_scale="RdYlGn",
                    range_color=[0, 1],
                )
                fig.update_layout(coloraxis_showscale=False, height=360)
                st.plotly_chart(fig, use_container_width=True)

        # Right: flag × signature heatmap
        with col_r:
            st.subheader("Flag × Signature heatmap (passing, top 20 by score)")
            if passing.empty:
                st.info("No passing combos.")
            else:
                top_sigs = (
                    passing.groupby("Parameter Signature")["_score"]
                    .mean()
                    .nlargest(20)
                    .index.tolist()
                )
                heat = (
                    passing[passing["Parameter Signature"].isin(top_sigs)]
                    .groupby("Parameter Signature")[toggle_cols]
                    .mean()
                    .reset_index()
                )
                heat["sig_label"] = heat["Parameter Signature"].apply(sig_short_label)
                heat = heat.set_index("sig_label")[toggle_cols]

                fig2 = px.imshow(
                    heat, color_continuous_scale="RdYlGn",
                    zmin=0, zmax=1, aspect="auto",
                )
                fig2.update_layout(height=420)
                st.plotly_chart(fig2, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# Tab 4: Compare
# ─────────────────────────────────────────────────────────────────────────────
with tab_compare:
    st.header("Run Comparison")

    if len(dir_labels) < 2:
        st.info("Only one run directory found. Run another config to compare.")
    else:
        other_options = [n for n in dir_labels if n != primary_name]
        compare_name = st.selectbox("Compare run", other_options)
        compare_dir  = dir_labels[compare_name]

        try:
            cmp_raw = _load(str(compare_dir))
            cmp_df  = annotate(cmp_raw, **gates)
        except Exception as exc:
            st.error(f"Failed to load compare run: {exc}")
            cmp_df = pd.DataFrame()

        if not cmp_df.empty:
            def _top_scores(annotated: pd.DataFrame, label: str) -> pd.DataFrame:
                sc = compute_weighted_scores(annotated)
                if sc.empty:
                    return pd.DataFrame(columns=["Parameter Signature", "final_score", "avg_score", "symbols_passing"])
                sc = sc.head(10).copy()
                sc["short_label"] = sc["Parameter Signature"].apply(sig_short_label)
                sc["run"] = label
                return sc

            sc_prim = _top_scores(df,     primary_name)
            sc_cmp  = _top_scores(cmp_df, compare_name)

            col_a, col_b = st.columns(2)
            with col_a:
                st.subheader(f"🏆 {primary_name}")
                if sc_prim.empty:
                    st.info("No passing combos.")
                else:
                    st.dataframe(
                        sc_prim[["short_label","final_score","avg_score","symbols_passing"]],
                        use_container_width=True,
                    )
            with col_b:
                st.subheader(f"🏆 {compare_name}")
                if sc_cmp.empty:
                    st.info("No passing combos.")
                else:
                    st.dataframe(
                        sc_cmp[["short_label","final_score","avg_score","symbols_passing"]],
                        use_container_width=True,
                    )

            # Shared signatures
            st.subheader("Shared signatures")
            if not sc_prim.empty and not sc_cmp.empty:
                shared = set(sc_prim["Parameter Signature"]) & set(sc_cmp["Parameter Signature"])
                if shared:
                    merged = (
                        sc_prim[sc_prim["Parameter Signature"].isin(shared)]
                        [["Parameter Signature","short_label","final_score"]]
                        .rename(columns={"final_score": f"score_{primary_name[:20]}"})
                        .merge(
                            sc_cmp[sc_cmp["Parameter Signature"].isin(shared)]
                            [["Parameter Signature","final_score"]]
                            .rename(columns={"final_score": f"score_{compare_name[:20]}"}),
                            on="Parameter Signature",
                        )
                        .sort_values(f"score_{primary_name[:20]}", ascending=False)
                    )
                    st.dataframe(merged, use_container_width=True)
                else:
                    st.info("No signatures in common between the two runs' top-10.")

# ─────────────────────────────────────────────────────────────────────────────
# Tab 5: Raw Data
# ─────────────────────────────────────────────────────────────────────────────
with tab_raw:
    st.header("Raw Results")

    filt_opts = st.radio("Show rows", ["All", "Passing only", "Failing only"], horizontal=True)
    view_df   = df.copy()
    if filt_opts == "Passing only":
        view_df = view_df[view_df["_passes"]]
    elif filt_opts == "Failing only":
        view_df = view_df[~view_df["_passes"]]

    metric_filter_cols = [c for c in _METRIC_COLS if c in view_df.columns]
    show_cols_raw = ["Symbol", "Parameter Signature"] + metric_filter_cols + ["_passes", "_score"]
    show_cols_raw = [c for c in show_cols_raw if c in view_df.columns]

    st.write(f"**{len(view_df):,}** rows")
    st.dataframe(
        _gradient(view_df[show_cols_raw], metric_filter_cols),
        use_container_width=True,
    )

    csv_bytes = view_df[show_cols_raw].to_csv(index=False).encode()
    st.download_button(
        label="⬇️ Download as CSV",
        data=csv_bytes,
        file_name=f"{primary_name}_filtered.csv",
        mime="text/csv",
    )
