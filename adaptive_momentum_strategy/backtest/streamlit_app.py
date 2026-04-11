"""
Streamlit app to visualize grid backtest results and trade logs.

Usage:
  pip install streamlit plotly pandas
  streamlit run adaptive_momentum_strategy/backtest/streamlit_app.py

This script expects the VectorBT results folder structure used by the project:
<results_folder>/BTCUSDT_1H.csv
<results_folder>/SOLUSDT_1H.csv
<results_folder>/trades/*_trade_log.csv

The app shows: top parameter combos, scatter of Return vs Drawdown, parameter impact bars,
and an equity curve for a selected parameter signature using trade logs.
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import List, Optional, Tuple

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Default results path (adjust if needed)
DEFAULT_RESULTS_DIR = Path(
    "/Users/andre/Documents/Python_local/pine_script/adaptive_momentum_strategy/backtest/results/results_vbt/2026-04-10_1114_AMS"
)

st.set_page_config(page_title="Grid Backtest Explorer", layout="wide")


@st.cache_data
def list_result_csvs(results_dir: Path) -> List[Path]:
    if not results_dir.exists():
        return []
    return sorted([p for p in results_dir.glob("*.csv") if "_trade_log" not in p.name])


@st.cache_data
def load_results_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    # Normalize column names (strip)
    df.columns = [c.strip() for c in df.columns]
    # Convert obvious numeric columns
    for col in df.columns:
        if df[col].dtype == object:
            try:
                df[col] = pd.to_numeric(df[col], errors="ignore")
            except Exception:
                pass
    return df


@st.cache_data
def list_trade_logs(results_dir: Path) -> List[Path]:
    trades_dir = results_dir / "trades"
    if not trades_dir.exists():
        return []
    return sorted(list(trades_dir.glob("*.csv")))


@st.cache_data
def load_trade_log(path: Path) -> pd.DataFrame:
    # Trade logs have EntryTime and ExitTime columns
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]
    # parse datetimes if present
    for tcol in ("EntryTime", "ExitTime"):
        if tcol in df.columns:
            df[tcol] = pd.to_datetime(df[tcol], utc=True, errors="coerce")
    # ensure PnL numeric
    for col in ("PnL", "Return [%]"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def symbol_from_result_file(path: Path) -> str:
    # e.g. BTCUSDT_1H.csv -> BTCUSDT
    return path.stem.split("_")[0]


def show_sidebar_controls(result_files: List[Path]) -> Tuple[Path, str]:
    st.sidebar.header("Data & Selection")
    results_dir = st.sidebar.text_input("Results folder", str(DEFAULT_RESULTS_DIR))
    results_dir = Path(results_dir)

    available = result_files
    if not available:
        st.sidebar.error("No result CSVs found in folder")
        return Path(), ""

    names = [p.name for p in available]
    sel_name = st.sidebar.selectbox("Choose results CSV", names, index=0)
    sel_path = next(p for p in available if p.name == sel_name)
    symbol = symbol_from_result_file(sel_path)
    return sel_path, symbol


def parameter_columns(df: pd.DataFrame) -> List[str]:
    return [c for c in df.columns if c.startswith("use_")]


def main() -> None:
    st.title("Grid Backtest Explorer")
    st.markdown(
        "Use this app to explore grid-search results and trade logs produced by the adaptive momentum strategy backtester."
    )

    results_dir = st.sidebar.text_input("Results directory", str(DEFAULT_RESULTS_DIR))
    results_path = Path(results_dir)

    result_files = list_result_csvs(results_path)
    trade_logs = list_trade_logs(results_path)

    if not result_files:
        st.error(f"No result CSV files found in {results_path}")
        return

    # Sidebar selection
    sel_path, symbol = show_sidebar_controls(result_files)
    if not sel_path.exists():
        st.error("Selected results file not found")
        return

    df = load_results_csv(sel_path)

    # Main layout: left = controls + metrics, right = plots
    left_col, right_col = st.columns((1, 2))

    with left_col:
        st.subheader("Results summary")
        st.write(f"File: {sel_path.name}")
        st.write(f"Rows (combos): {len(df)}")

        # metrics selection
        numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
        x_metric = st.selectbox("X metric", options=numeric_cols, index=numeric_cols.index("Return [%]") if "Return [%]" in numeric_cols else 0)
        y_metric = st.selectbox("Y metric", options=numeric_cols, index=numeric_cols.index("Max Drawdown [%]") if "Max Drawdown [%]" in numeric_cols else 1)
        color_metric = st.selectbox("Color by", options=[None] + numeric_cols, index=0)

        top_n = st.number_input("Top N combos to show", min_value=5, max_value=200, value=10)

        # show top combos by Rank if available else by Return
        if "Rank" in df.columns:
            df_sorted = df.sort_values("Rank").head(top_n)
        else:
            df_sorted = df.sort_values("Return [%]", ascending=False).head(top_n)

        st.dataframe(df_sorted[["Parameter Signature"] + [x_metric, y_metric, color_metric] if color_metric else ["Parameter Signature", x_metric, y_metric]])

    with right_col:
        st.subheader("Scatter: combos")
        fig = px.scatter(
            df,
            x=x_metric,
            y=y_metric,
            color=color_metric if color_metric in df.columns else None,
            hover_data=["Parameter Signature", "Rank"] if "Rank" in df.columns else ["Parameter Signature"],
            height=600,
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Parameter impact analysis
    st.subheader("Parameter impact (mean Return [%])")
    params = parameter_columns(df)
    if params:
        impact = {p: df.groupby(p)["Return [%]"].mean().to_dict() if p in df.columns else {} for p in params}
        imp_df = pd.DataFrame(
            [
                {
                    "parameter": p,
                    "enabled_mean": impact[p].get(True, float("nan")),
                    "disabled_mean": impact[p].get(False, float("nan")),
                }
                for p in params
            ]
        ).sort_values("enabled_mean", ascending=False)
        st.dataframe(imp_df)
        bar_fig = go.Figure()
        bar_fig.add_trace(go.Bar(x=imp_df["parameter"], y=imp_df["enabled_mean"], name="enabled (mean Return [%])"))
        bar_fig.add_trace(go.Bar(x=imp_df["parameter"], y=imp_df["disabled_mean"], name="disabled (mean Return [%])"))
        bar_fig.update_layout(barmode="group", height=400)
        st.plotly_chart(bar_fig, use_container_width=True)
    else:
        st.info("No parameter columns (use_*) detected in results CSV")

    st.markdown("---")

    # Trade-log / equity curve area
    st.subheader("Trade log & equity curve")

    trades_by_symbol = [p for p in trade_logs if symbol in p.name]
    if not trades_by_symbol:
        st.info("No trade logs found for selected symbol in trades/ subfolder")
        st.stop()

    # pick latest trade log for this symbol
    trade_log_path = trades_by_symbol[-1]
    df_trades = load_trade_log(trade_log_path)

    st.write(f"Using trade log: {trade_log_path.name} — {len(df_trades)} trades")

    # choose parameter signature to inspect
    signatures = df["Parameter Signature"].astype(str).unique().tolist()
    default_sig = signatures[0] if signatures else None
    selected_sig = st.selectbox("Parameter Signature (show trades for)", signatures, index=0)

    trades_for_sig = df_trades[df_trades["Parameter Signature"] == selected_sig].copy()

    if trades_for_sig.empty:
        st.warning("No trades found for that parameter signature in the trade log.")
    else:
        # sort by ExitTime if present else EntryTime
        time_col = "ExitTime" if "ExitTime" in trades_for_sig.columns else "EntryTime"
        trades_for_sig = trades_for_sig.sort_values(by=time_col)

        # cumulative PnL
        if "PnL" in trades_for_sig.columns:
            trades_for_sig["PnL"] = pd.to_numeric(trades_for_sig["PnL"], errors="coerce").fillna(0)
            trades_for_sig["cumPnL"] = trades_for_sig["PnL"].cumsum()
            starting_capital = st.number_input("Starting capital for equity curve", value=10000)
            trades_for_sig["equity"] = starting_capital + trades_for_sig["cumPnL"]

            eq_fig = px.line(trades_for_sig, x=time_col, y="equity", title="Equity curve (by trade exit)")
            st.plotly_chart(eq_fig, use_container_width=True)

            st.markdown("**Trade table (filtered)**")
            st.dataframe(trades_for_sig)

            # summary stats
            st.markdown("**Selected signature summary**")
            total_pnl = trades_for_sig["PnL"].sum()
            total_return_pct = (trades_for_sig["equity"].iloc[-1] - starting_capital) / starting_capital * 100
            st.metric("Total PnL", f"{total_pnl:.2f}")
            st.metric("Net return [%]", f"{total_return_pct:.2f}")
        else:
            st.info("Trade log does not contain a 'PnL' column; showing raw trades instead.")
            st.dataframe(trades_for_sig)

    st.markdown("---")
    st.caption("Streamlit Grid Backtest Explorer — generated by the Copilot CLI helper")


if __name__ == "__main__":
    main()
