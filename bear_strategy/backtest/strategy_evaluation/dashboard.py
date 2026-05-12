"""Bear Strategy — sweep evaluation dashboard.

Launch from the project root:
    streamlit run bear_strategy/backtest/strategy_evaluation/dashboard.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

_ROOT = Path(__file__).parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from bear_strategy.backtest.strategy_evaluation.scoring import (
    score_row, passes_gates, combo_label,
    DEFAULT_MIN_SQN, DEFAULT_MIN_PF, DEFAULT_MIN_TRADES, DEFAULT_MIN_WR,
)
from bear_strategy.backtest.strategy_evaluation.analyse import load_sweep, find_latest_sweep, analyse
from bear_strategy.backtest.strategy_evaluation.report import build_report, save_report

# ─────────────────────────────────────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Bear Strategy — Evaluation",
    page_icon="🐻",
    layout="wide",
)

# ─────────────────────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────────────────────
_RESULTS_ROOT = Path("bear_strategy/backtest/vectorbt/results")

_ALL_METRICS = [
    "Return [%]", "SQN", "Profit Factor", "Expectancy [%]",
    "Win Rate [%]", "Max. Drawdown [%]", "Sharpe Ratio", "Sortino Ratio",
    "Calmar Ratio", "# Trades", "Best Trade [%]", "Worst Trade [%]",
    "Avg. Win Trade [%]", "Avg. Loss Trade [%]",
]

_HEATMAP_METRICS = [
    "Return [%]", "SQN", "Profit Factor", "Expectancy [%]",
    "Win Rate [%]", "Max. Drawdown [%]", "Sharpe Ratio",
]


def _find_sweeps() -> list[Path]:
    if not _RESULTS_ROOT.exists():
        return []
    return sorted(_RESULTS_ROOT.glob("*_SWEEP/sweep_summary.csv"), reverse=True)


def _colour(val: object, col: str) -> str:
    """Return CSS colour string for a cell value given its column name."""
    try:
        v = float(val)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return ""
    inverted = col in ("Max. Drawdown [%]", "Worst Trade [%]")
    positive = v < 0 if inverted else v > 0
    if col == "Profit Factor":
        positive = v >= 1.0
    return "color: #22c55e" if positive else "color: #ef4444"


# ─────────────────────────────────────────────────────────────────────────────
# Sidebar — file, gates, pair filter
# ─────────────────────────────────────────────────────────────────────────────
st.sidebar.title("🐻 Bear Strategy")
st.sidebar.header("Sweep file")

sweeps = _find_sweeps()
if not sweeps:
    st.error("No sweep results found.  Run `sweep_run.py` first.")
    st.stop()

sweep_labels = [p.parent.name for p in sweeps]
chosen_idx   = st.sidebar.selectbox(
    "Select sweep run", range(len(sweep_labels)),
    format_func=lambda i: sweep_labels[i],
)
csv_path = sweeps[chosen_idx]
df_raw   = load_sweep(csv_path)

st.sidebar.divider()
st.sidebar.header("Pass / Fail gates")
st.sidebar.caption("A combo appears in the Ranked tab only when it clears **all** gates on the required number of pairs.")
min_sqn    = st.sidebar.slider("Min SQN",          -2.0, 5.0,  DEFAULT_MIN_SQN,  0.1)
min_pf     = st.sidebar.slider("Min Profit Factor",  0.5, 3.0,  DEFAULT_MIN_PF,   0.05)
min_trades = st.sidebar.number_input("Min # Trades",   1, 500,  DEFAULT_MIN_TRADES, 1)
min_wr     = st.sidebar.slider("Min Win Rate %",     0.0, 80.0, DEFAULT_MIN_WR,   1.0)
min_pairs  = st.sidebar.number_input(
    "Min pairs that must pass", 1, len(df_raw["Symbol"].str.strip().unique()), 1, 1
)

st.sidebar.divider()
st.sidebar.header("Pairs to include")
all_symbols  = sorted(df_raw["Symbol"].str.strip().unique())
chosen_pairs = st.sidebar.multiselect("Pairs", all_symbols, default=all_symbols)
if chosen_pairs:
    df_raw = df_raw[df_raw["Symbol"].isin(chosen_pairs)]

n_pairs = len(chosen_pairs) if chosen_pairs else len(all_symbols)

# ─────────────────────────────────────────────────────────────────────────────
# Run analysis (live — re-runs on every sidebar change)
# ─────────────────────────────────────────────────────────────────────────────
ranked_all, ranked_passing, per_pair = analyse(
    df_raw,
    min_sqn        = min_sqn,
    min_pf         = min_pf,
    min_trades      = int(min_trades),
    min_wr         = min_wr,
    min_pairs_pass  = int(min_pairs),
)

# Add _label to df_raw for heatmap and raw tabs
df_raw = df_raw.copy()
df_raw["_label"]  = df_raw.apply(
    lambda r: combo_label(
        r["sl_mult"], r["tp_mult"],
        r.get("exit_mode", "fixed_tp") or "fixed_tp",
        r.get("exit_rsi_level") if pd.notna(r.get("exit_rsi_level")) else None,
    ),
    axis=1,
)
df_raw["_passes"] = df_raw.apply(
    lambda r: passes_gates(r, min_sqn, min_pf, int(min_trades), min_wr), axis=1
)

# ─────────────────────────────────────────────────────────────────────────────
# Page header
# ─────────────────────────────────────────────────────────────────────────────
st.title("🐻 Bear Strategy — Sweep Evaluation")
st.caption(f"`{csv_path}`  ·  {n_pairs} pairs  ·  {len(df_raw['_label'].unique())} combos total")

# ── Report button (always visible, outside tabs) ──────────────────────────────
_gates = dict(
    min_sqn=min_sqn, min_pf=min_pf,
    min_trades=int(min_trades), min_wr=min_wr, min_pairs=int(min_pairs),
)
_report_md = build_report(
    csv_path       = csv_path,
    ranked_all     = ranked_all,
    ranked_passing = ranked_passing,
    per_pair       = per_pair,
    df_raw         = df_raw,
    gates          = _gates,
    chosen_pairs   = list(chosen_pairs or all_symbols),
)

col_dl, col_save, _ = st.columns([1, 1, 6])
with col_dl:
    st.download_button(
        "📄 Download report (.md)",
        data        = _report_md,
        file_name   = "analysis_report.md",
        mime        = "text/markdown",
        help        = "Download the report as a markdown file.",
    )
with col_save:
    if st.button("💾 Save report to results dir", help=f"Saves to {csv_path.parent}/analysis_report.md"):
        saved = save_report(_report_md, csv_path)
        st.success(f"Saved → `{saved}`")

tab_ranked, tab_pair, tab_heatmap, tab_raw = st.tabs(
    ["🏆 Ranked", "🔍 Per-Pair Drill-Down", "🔥 Heatmaps", "🗃️ Raw data"]
)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — Ranked (two sub-views)
# ─────────────────────────────────────────────────────────────────────────────
with tab_ranked:
    if ranked_all.empty:
        st.warning(
            "⚠️  No combo cleared the gates with the current thresholds.  "
            "Relax the sliders in the sidebar or lower **Min pairs that must pass**."
        )
    else:
        avg_ret_col = "Avg Return [%]"

        def _style_ranked(df_: pd.DataFrame) -> "pd.io.formats.style.Styler":
            styled = df_.style
            if avg_ret_col in df_.columns:
                styled = styled.map(
                    lambda v: _colour(v, "Return [%]"), subset=[avg_ret_col]
                )
            return styled

        sub_all, sub_pass = st.tabs([
            "📊 All pairs averaged",
            "✅ Passing pairs averaged",
        ])

        with sub_all:
            st.caption(
                "Metrics are averaged over **all** pairs — including those that fail the gates.  "
                "Reflects the raw combo performance across the full universe."
            )
            st.dataframe(
                _style_ranked(ranked_all),
                use_container_width=True,
                height=min(600, 40 * len(ranked_all) + 50),
            )

        with sub_pass:
            st.caption(
                "Metrics are averaged **only over pairs that passed all gates** for each combo.  "
                "Reflects what you would see if you traded only those pairs."
            )
            st.dataframe(
                _style_ranked(ranked_passing),
                use_container_width=True,
                height=min(600, 40 * len(ranked_passing) + 50),
            )

        # Top-3 cards — use passing view as the reference
        st.divider()
        top = ranked_passing.head(3)
        cols = st.columns(len(top))
        for i, (_, row) in enumerate(top.iterrows()):
            with cols[i]:
                pairs_col = [c for c in row.index if c.startswith("Pairs")][0]
                st.metric(
                    label=f"#{i + 1}  {row['Signature']}",
                    value=f"Score {row['Breadth Score']:.4f}",
                    delta=row[pairs_col],
                )

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — Per-Pair Drill-Down
# ─────────────────────────────────────────────────────────────────────────────
with tab_pair:
    st.subheader("Per-pair breakdown for a selected combo")
    st.caption(
        "**✅ rows** pass all gates.  **❌ rows** fail at least one.  "
        "Use this to decide which pairs to carry forward."
    )

    all_combos    = sorted(per_pair["Signature"].unique())
    passed_combos = ranked_all["Signature"].tolist() if not ranked_all.empty else []

    show_all = st.toggle("Show all combos (including failed)", value=False)
    combo_pool = all_combos if show_all else (passed_combos if passed_combos else all_combos)

    if not combo_pool:
        st.info("No combos to display.  Relax the gates or enable 'Show all combos'.")
    else:
        selected = st.selectbox("Combo", combo_pool)
        detail   = per_pair[per_pair["Signature"] == selected].drop(columns=["Signature"])
        detail   = detail.sort_values("Pass", ascending=False).reset_index(drop=True)

        passing_pairs = detail[detail["Pass"] == "✅"]["Symbol"].tolist()
        failing_pairs = detail[detail["Pass"] == "❌"]["Symbol"].tolist()

        col_left, col_right = st.columns([1, 2])
        with col_left:
            st.metric("Passing pairs", f"{len(passing_pairs)} / {len(detail)}")
            if passing_pairs:
                st.success("✅  " + ",  ".join(passing_pairs))
            if failing_pairs:
                st.error("❌  " + ",  ".join(failing_pairs))

        with col_right:
            # Gate breakdown per pair
            gate_rows = []
            for _, r in detail.iterrows():
                gate_rows.append({
                    "Symbol":   r["Symbol"],
                    "Overall":  r["Pass"],
                    f"SQN≥{min_sqn}":      "✅" if (not pd.isna(r.get("SQN")) and float(r.get("SQN", -99)) >= min_sqn)        else "❌",
                    f"PF≥{min_pf}":        "✅" if (not pd.isna(r.get("Profit Factor")) and float(r.get("Profit Factor", 0)) >= min_pf) else "❌",
                    f"Trades≥{min_trades}":"✅" if (not pd.isna(r.get("# Trades")) and int(r.get("# Trades", 0)) >= min_trades)  else "❌",
                    f"WR≥{min_wr}%":       "✅" if (not pd.isna(r.get("Win Rate [%]")) and float(r.get("Win Rate [%]", 0)) >= min_wr) else "❌",
                })
            st.dataframe(pd.DataFrame(gate_rows), use_container_width=True, hide_index=True)

        st.divider()
        st.markdown("**Full metric table**")

        metric_cols = ["Symbol", "Pass", "Score"] + [
            c for c in _ALL_METRICS if c in detail.columns
        ]
        display = detail[[c for c in metric_cols if c in detail.columns]]

        def _style_detail(df_: pd.DataFrame) -> pd.io.formats.style.Styler:
            def row_bg(row: pd.Series) -> list[str]:
                bg = "background-color: #14532d22" if row.get("Pass") == "✅" else "background-color: #7f1d1d22"
                return [bg] * len(row)
            return df_.style.apply(row_bg, axis=1)

        st.dataframe(
            _style_detail(display),
            use_container_width=True,
            hide_index=True,
        )

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — Heatmaps
# ─────────────────────────────────────────────────────────────────────────────
with tab_heatmap:
    st.subheader("Pivot heatmaps — SL× (rows) × TP× (cols)")

    avail_metrics = [m for m in _HEATMAP_METRICS if m in df_raw.columns]
    chosen_metric = st.selectbox("Metric", avail_metrics)
    pair_choice   = st.radio(
        "Aggregate across", ["All pairs (mean)"] + list(chosen_pairs or all_symbols),
        horizontal=True,
    )

    heat_df = df_raw if pair_choice == "All pairs (mean)" else df_raw[df_raw["Symbol"] == pair_choice]
    if heat_df.empty:
        st.warning("No data for selected pair.")
    else:
        pivot = heat_df.pivot_table(
            index="sl_mult", columns="tp_mult", values=chosen_metric, aggfunc="mean"
        ).round(3)
        cmap = "RdYlGn_r" if chosen_metric == "Max. Drawdown [%]" else "RdYlGn"
        st.dataframe(
            pivot.style.background_gradient(cmap=cmap, axis=None),
            use_container_width=True,
        )

        st.divider()
        bar = df_raw.groupby("_label")[chosen_metric].mean().sort_values(ascending=False)
        st.caption(f"Average {chosen_metric} per combo across all pairs")
        st.bar_chart(bar, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 — Raw data
# ─────────────────────────────────────────────────────────────────────────────
with tab_raw:
    st.subheader("Raw sweep rows")
    sym_filter = st.multiselect("Filter by symbol", all_symbols, default=list(chosen_pairs or all_symbols))
    raw_view = df_raw[df_raw["Symbol"].isin(sym_filter)].drop(
        columns=["_label", "_passes"], errors="ignore"
    )
    st.dataframe(raw_view, use_container_width=True, height=600)
    st.download_button(
        "⬇️ Download filtered CSV",
        raw_view.to_csv(index=False),
        file_name="filtered_sweep.csv",
        mime="text/csv",
    )
