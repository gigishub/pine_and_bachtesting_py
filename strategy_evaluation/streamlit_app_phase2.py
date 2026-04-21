"""Streamlit Phase 2 dashboard — Date Range Sensitivity (trade-log slicing).

One full-period backtest is all that is needed.  Trade logs saved by the
sequencer (``trades/*_trade_log.csv``) are sliced by date window and quality
metrics are recomputed per (signature, coin, window).

Sections (expandable, numbered):
    1. Trade Log Status       — confirm logs were found and show coverage
    2. Signature Selection    — auto-load top-N from Phase 1 scores
    3. Per-Window Metrics     — tabbed view: metrics for each window
    4. Cross-Window Heatmaps  — coins_passing, SQN, Profit Factor grids
    5. Phase 2 Verdict        — PASS / FAIL per signature

Run with:
    streamlit run strategy_evaluation/streamlit_app_phase2.py
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import plotly.express as px
import streamlit as st

from strategy_evaluation.config import RobustnessConfig
from strategy_evaluation.loader import load_run_dir
from strategy_evaluation.metrics import annotate_dataframe
from strategy_evaluation.phase2 import (
    coin_window_breakdown,
    cross_tf_consensus,
    evaluate_window,
    filter_trades_by_timeframe,
    get_trade_timeframes,
    load_trade_logs,
    short_sig,
    slice_trades,
    verdict_table,
)
from strategy_evaluation.scoring import compute_combo_weighted_scores
from strategy_evaluation.sig_alias import sig_to_alias

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Strategy Robustness — Phase 2",
    page_icon="📅",
    layout="wide",
)

# ── Helpers ───────────────────────────────────────────────────────────────────

def _info(text: str, label: str = "ℹ️ How to read this") -> None:
    with st.expander(label):
        st.markdown(text)


def _mtime(path: str) -> float:
    p = Path(path)
    if not p.exists():
        return 0.0
    mtimes = [f.stat().st_mtime for f in p.glob("*.csv")]
    return max(mtimes, default=0.0)


@st.cache_data(show_spinner=False)
def _load_results_cached(path: str, _mt: float) -> pd.DataFrame:  # noqa: ARG001
    return load_run_dir(path)


@st.cache_data(show_spinner=False)
def _load_trades_cached(path: str, _mt: float) -> pd.DataFrame:  # noqa: ARG001
    return load_trade_logs(path)


def _render_tf_analysis(
    trades_tf: pd.DataFrame,
    selected_sigs: list[str],
    sig_labels: list[str],
    windows_cfg: dict[str, tuple[str | None, str | None]],
    cfg: RobustnessConfig,
    min_trades_per_coin: int,
    min_coins_pass: int,
    min_windows_pass: int,
    min_sqn: float,
) -> tuple[dict[str, pd.DataFrame], pd.DataFrame]:
    """Render Per-Window Metrics, Heatmaps, and Verdict for one slice of trades."""
    eval_results: dict[str, pd.DataFrame] = {
        label: evaluate_window(trades_tf, selected_sigs, start, end, cfg, min_trades_per_coin)
        for label, (start, end) in windows_cfg.items()
    }
    regime_windows = {k: v for k, v in eval_results.items() if k != "Full Period"}

    with st.expander("2. Per-Window Metrics", expanded=False):
        _info(
            "```\n"
            "Each tab = one date window.\n"
            "Metrics are computed from trades whose EntryTime falls in the window.\n\n"
            "sig_present = False → signature had no trade logs for this coin/period\n"
            "# Trades < min      → coin doesn't count toward coins_passing\n"
            "```"
        )
        show_cols = ["Parameter Signature", "sig_present", "coins_passing"] + _METRIC_COLS
        win_tabs = st.tabs(list(eval_results.keys()))
        for win_tab, label in zip(win_tabs, eval_results.keys()):
            with win_tab:
                eval_df = eval_results[label]
                if eval_df.empty:
                    st.info("No data.")
                    continue
                disp = eval_df[[c for c in show_cols if c in eval_df.columns]].copy()
                disp.insert(
                    disp.columns.get_loc("Parameter Signature"),
                    "Alias",
                    disp["Parameter Signature"].apply(sig_to_alias),
                )
                st.dataframe(disp, use_container_width=True, hide_index=True)

    with st.expander("3. Cross-Window Heatmaps", expanded=True):
        _info(
            "```\n"
            "Rows = selected signatures.  Columns = date windows.\n"
            "Full Period is shown as reference only (not used in verdict).\n\n"
            "coins_passing heatmap : brighter = more coins passing in that regime\n"
            "SQN heatmap           : quality of the edge in each window\n"
            "Profit Factor heatmap : PF > 1 = positive edge\n"
            "```"
        )

        def _build_matrix(metric: str, fill: float = 0.0) -> pd.DataFrame:
            rows = []
            for sig, sig_lbl in zip(selected_sigs, sig_labels):
                row_vals = []
                for label in eval_results:
                    df = eval_results[label]
                    if df.empty or "Parameter Signature" not in df.columns:
                        row_vals.append(fill)
                    else:
                        match = df[df["Parameter Signature"] == sig]
                        val = match[metric].iloc[0] if (not match.empty and metric in match.columns) else fill
                        row_vals.append(float(val) if not pd.isna(val) else fill)
                rows.append(row_vals)
            return pd.DataFrame(rows, index=sig_labels, columns=list(eval_results.keys()))

        _h = max(300, 60 * len(selected_sigs))

        df_coins = _build_matrix("coins_passing")
        fig1 = px.imshow(
            df_coins,
            color_continuous_scale=[[0,"#1a1a2e"],[0.01,"#c0392b"],[0.4,"#e74c3c"],
                                     [0.7,"#f39c12"],[1.0,"#2ecc71"]],
            aspect="auto", title="Coins Passing per Signature × Window",
            labels={"x":"Window","y":"Signature","color":"Coins"},
            text_auto=True,
        )
        fig1.update_xaxes(side="top")
        fig1.update_layout(height=_h)
        st.plotly_chart(fig1, use_container_width=True)

        col_a, col_b = st.columns(2)
        with col_a:
            df_sqn = _build_matrix("SQN", fill=0.0)
            fig2 = px.imshow(
                df_sqn,
                color_continuous_scale="RdYlGn",
                aspect="auto", title="SQN per Signature × Window",
                labels={"x":"Window","y":"Signature","color":"SQN"},
                text_auto=".2f",
                zmin=0, zmax=3,
            )
            fig2.update_xaxes(side="top")
            fig2.update_layout(height=_h)
            st.plotly_chart(fig2, use_container_width=True)

        with col_b:
            df_pf = _build_matrix("Profit Factor", fill=0.0)
            fig3 = px.imshow(
                df_pf,
                color_continuous_scale="RdYlGn",
                aspect="auto", title="Profit Factor per Signature × Window",
                labels={"x":"Window","y":"Signature","color":"PF"},
                text_auto=".2f",
                zmin=0.8, zmax=3.0,
            )
            fig3.update_xaxes(side="top")
            fig3.update_layout(height=_h)
            st.plotly_chart(fig3, use_container_width=True)

        score_rows: list[dict] = []
        for sig, sig_lbl in zip(selected_sigs, sig_labels):
            for label in eval_results:
                df = eval_results[label]
                if df.empty or "Parameter Signature" not in df.columns:
                    sqn_val = 0.0
                else:
                    match = df[df["Parameter Signature"] == sig]
                    sqn_val = (
                        float(match["SQN"].iloc[0])
                        if not match.empty and "SQN" in match.columns and not pd.isna(match["SQN"].iloc[0])
                        else 0.0
                    )
                score_rows.append({"Signature": sig_lbl, "Window": label, "SQN": sqn_val})

        df_bar = pd.DataFrame(score_rows)
        fig_bar = px.bar(
            df_bar, x="Signature", y="SQN", color="Window", barmode="group",
            color_discrete_map=_WINDOW_COLOURS,
            title="SQN per Signature × Window",
        )
        fig_bar.add_hline(y=min_sqn, line_dash="dash", line_color="white",
                          annotation_text=f"min SQN={min_sqn}", annotation_position="top left")
        fig_bar.update_layout(xaxis_tickangle=-25)
        st.plotly_chart(fig_bar, use_container_width=True)

    v_table = pd.DataFrame()
    with st.expander("4. Coin Performance by Window", expanded=False):
        _info(
            "```\n"
            "Rows = coins, columns = analysis windows.\n"
            "pass_rate = fraction of selected signatures where this coin passes.\n"
            "Green = passes on most/all selected signatures.\n"
            "Red   = fails on most/all selected signatures.\n"
            "```"
        )
        cp_df = coin_window_breakdown(
            trades_tf, selected_sigs, windows_cfg, cfg, min_trades_per_coin
        )
        if cp_df.empty:
            st.info("No coin-level data available.")
        else:
            pivot_rate = cp_df.pivot(index="Symbol", columns="Window", values="pass_rate")
            pivot_pass = cp_df.pivot(index="Symbol", columns="Window", values="sigs_passing")
            n_sigs = cp_df["sigs_total"].iloc[0] if not cp_df.empty else 1
            text_vals = [
                [
                    f"{int(v)}/{n_sigs}" if not pd.isna(v) else "—"
                    for v in row
                ]
                for _, row in pivot_pass.iterrows()
            ]
            fig_cp = px.imshow(
                pivot_rate,
                color_continuous_scale=[[0, "#c0392b"], [0.5, "#f39c12"], [1.0, "#2ecc71"]],
                aspect="auto",
                title="Coin Pass Rate per Window (fraction of selected signatures passing)",
                labels={"x": "Window", "y": "Coin", "color": "Pass rate"},
                zmin=0,
                zmax=1,
            )
            fig_cp.update_traces(
                text=text_vals, texttemplate="%{text}", textfont_size=12
            )
            fig_cp.update_xaxes(side="top")
            fig_cp.update_layout(height=max(300, 40 * len(pivot_rate)))
            st.plotly_chart(fig_cp, use_container_width=True)

            st.dataframe(
                cp_df[["Window", "Symbol", "sigs_passing", "sigs_total", "pass_rate"]]
                .sort_values(["Window", "pass_rate"], ascending=[True, False]),
                use_container_width=True,
                hide_index=True,
            )

    with st.expander("5. Phase 2 Verdict", expanded=True):
        _info(
            f"```\n"
            f"Pass criteria : ≥ {min_coins_pass} coins in ≥ {min_windows_pass}/3 regime windows\n"
            f"Full Period   : shown as reference, not counted in verdict\n\n"
            f"<window>_coins  : coins_passing in that window\n"
            f"<window>_trades : total trades in that window (all coins combined)\n"
            f"windows_passing : regime windows where coins ≥ {min_coins_pass}\n"
            f"verdict         : ✅ PASS if windows_passing ≥ {min_windows_pass}\n"
            f"```"
        )
        v_table = verdict_table(regime_windows, min_coins_pass, min_windows_pass)

        if v_table.empty:
            st.info("No verdict data.")
        else:
            n_pass  = int((v_table["verdict"] == "✅ PASS").sum())
            n_total = len(v_table)
            if n_pass == n_total:
                st.success(f"🎉 All {n_total} signature(s) pass Phase 2!")
            elif n_pass == 0:
                st.error(
                    f"❌ None of the {n_total} signature(s) pass Phase 2 "
                    f"(≥{min_coins_pass} coins, ≥{min_windows_pass}/3 windows)."
                )
            else:
                st.warning(f"⚠️ {n_pass} / {n_total} signature(s) pass Phase 2.")

            disp_v = v_table.copy()
            disp_v.insert(
                disp_v.columns.get_loc("Parameter Signature"),
                "Alias",
                disp_v["Parameter Signature"].apply(sig_to_alias),
            )
            st.dataframe(disp_v, use_container_width=True, hide_index=True)

            st.markdown("---")
            coin_cols = [c for c in v_table.columns if c.endswith("_coins")]
            for _, row in v_table.iterrows():
                verdict_str = str(row["verdict"])
                sig_short   = sig_to_alias(str(row["Parameter Signature"]))
                n_win       = int(row["windows_passing"])
                coins_detail = "  ·  ".join(
                    f"{c.replace('_coins','')}: **{int(row[c])}** coins / "
                    f"**{int(row.get(c.replace('_coins','_trades'), 0))}** trades"
                    for c in coin_cols
                )
                msg = (
                    f"**{sig_short}** — {verdict_str}  "
                    f"({n_win}/{len(coin_cols)} windows)  ·  {coins_detail}"
                )
                (st.success if "PASS" in verdict_str else st.error)(msg)

    return eval_results, v_table


def _render_cross_tf_section(
    tf_verdicts: dict[str, pd.DataFrame],
    selected_sigs: list[str],
    sig_labels: list[str],
) -> None:
    """Render Cross-TF Consensus section after per-TF tabs."""
    consensus = cross_tf_consensus(tf_verdicts)
    if consensus.empty:
        return

    st.markdown("---")
    with st.expander("🌐 Cross-TF Consensus", expanded=True):
        _info(
            "```\n"
            "Shows which signatures pass Phase 2 on each timeframe.\n\n"
            "✅ ALL  = passes on every TF detected in the trade logs\n"
            "⚠️ SOME = passes on at least one TF (but not all)\n"
            "❌ NONE = fails on every TF\n"
            "```"
        )

        n_all   = int((consensus["cross_verdict"] == "✅ ALL").sum())
        n_some  = int((consensus["cross_verdict"] == "⚠️ SOME").sum())
        n_total = len(consensus)

        if n_all == n_total:
            st.success(f"🎉 All {n_total} signature(s) pass on ALL timeframes.")
        elif n_all > 0:
            st.info(
                f"✅ {n_all} / {n_total} signature(s) pass on ALL timeframes  ·  "
                f"{n_some} pass on some."
            )
        else:
            st.warning(f"⚠️ No signature passes on ALL timeframes  ·  {n_some} pass on at least one.")

        disp = consensus.copy()
        disp.insert(
            disp.columns.get_loc("Parameter Signature"),
            "Alias",
            disp["Parameter Signature"].apply(sig_to_alias),
        )
        st.dataframe(disp, use_container_width=True, hide_index=True)

        # Heatmap: Signature × Timeframe (green=pass, red=fail)
        tfs = list(tf_verdicts.keys())
        hm_data: list[list[int]] = []
        y_labels: list[str] = []
        for _, row in consensus.iterrows():
            hm_data.append([1 if row.get(tf, False) else 0 for tf in tfs])
            y_labels.append(sig_to_alias(str(row["Parameter Signature"])))

        df_hm = pd.DataFrame(hm_data, index=y_labels, columns=tfs)
        text_vals = [["✅" if v else "❌" for v in row_data] for row_data in hm_data]
        fig = px.imshow(
            df_hm,
            color_continuous_scale=[[0, "#c0392b"], [1, "#2ecc71"]],
            aspect="auto",
            title="Pass / Fail per Signature × Timeframe",
            labels={"x": "Timeframe", "y": "Signature", "color": "Pass"},
            zmin=0, zmax=1,
        )
        fig.update_traces(text=text_vals, texttemplate="%{text}", textfont_size=16)
        fig.update_xaxes(side="top")
        fig.update_layout(height=max(300, 60 * len(y_labels)), coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)


# ── Default windows ───────────────────────────────────────────────────────────

_DEFAULT_WINDOWS: dict[str, tuple[str | None, str | None]] = {
    "Bear":        ("2022-01-01", "2023-01-01"),
    "Recovery":    ("2023-01-01", "2024-01-01"),
    "Bull":        ("2024-01-01", "2025-09-01"),
    "Full Period": (None, None),
}
_WINDOW_COLOURS: dict[str, str] = {
    "Bear":        "#e74c3c",
    "Recovery":    "#f39c12",
    "Bull":        "#2ecc71",
    "Full Period": "#3498db",
}
_METRIC_COLS = ["# Trades", "Win Rate [%]", "Profit Factor", "Expectancy [%]", "SQN"]


# ── Report formatting ─────────────────────────────────────────────────────────

def _format_phase2_report(
    results_dir: str,
    run_ts: str,
    cfg: RobustnessConfig,
    trades: pd.DataFrame,
    eval_results: dict[str, pd.DataFrame],
    v_table: pd.DataFrame,
    windows_cfg: dict[str, tuple[str | None, str | None]],
    min_trades_per_coin: int,
    min_coins_pass: int,
    min_windows_pass: int,
    selected_sigs: list[str],
    sig_labels: list[str],
    period: tuple[str, str] | None = None,
) -> str:
    """Generate a Markdown Phase 2 report matching all visible sections."""
    lines: list[str] = []

    def h(text: str, level: int = 2) -> None:
        lines.append(f"\n{'#' * level} {text}\n")

    def _fmt(value: object) -> str:
        if isinstance(value, float):
            return f"{value:.3g}"
        return str(value)

    # ── Header ─────────────────────────────────────────────────────────────────
    _period_line = (
        f"  \n**Data period:** {period[0]} → {period[1]}"
        if period else ""
    )
    lines.append("# Phase 2 — Date Range Sensitivity Report")
    lines.append(f"\n**Generated:** {run_ts}  \n**Results dir:** `{results_dir}`{_period_line}\n")

    # ── Pass Criteria ──────────────────────────────────────────────────────────
    h("Pass Criteria")
    lines.append("| Criterion | Value |")
    lines.append("|-----------|-------|")
    lines.append(f"| Min SQN | {cfg.min_sqn} |")
    lines.append(f"| Min Profit Factor | {cfg.min_profit_factor} |")
    lines.append(f"| Min Win Rate | {cfg.min_win_rate:.0f}% |")
    lines.append(f"| Min trades per coin per window | {min_trades_per_coin} |")
    lines.append(f"| Min coins passing per window | {min_coins_pass} |")
    lines.append(f"| Min windows passing (excl. Full Period) | {min_windows_pass} |")
    lines.append("")

    # ── 1. Trade Log Status ───────────────────────────────────────────────────
    h("1. Trade Log Status")
    n_trades      = len(trades)
    sigs_in_logs  = trades["Parameter Signature"].nunique() if "Parameter Signature" in trades.columns else 0
    coins_in_logs = trades["Symbol"].nunique() if "Symbol" in trades.columns else 0
    _et_min = trades["EntryTime"].min() if "EntryTime" in trades.columns else None
    _et_max = trades["EntryTime"].max() if "EntryTime" in trades.columns else None
    _trade_period = (
        f"{_et_min.strftime('%Y-%m-%d')} → {_et_max.strftime('%Y-%m-%d')}"
        if _et_min is not None and _et_max is not None else "unknown"
    )
    lines.append(f"- **Total trades:** {n_trades:,}")
    lines.append(f"- **Unique signatures:** {sigs_in_logs}")
    lines.append(f"- **Coins covered:** {coins_in_logs}")
    lines.append(f"- **Period:** {_trade_period}")
    lines.append("")
    lines.append("| Window | Date Range | # Trades | # Signatures |")
    lines.append("|--------|------------|----------|--------------|")
    for win_label, (start, end) in windows_cfg.items():
        wt     = slice_trades(trades, start, end)
        n_wt   = len(wt)
        n_wsig = wt["Parameter Signature"].nunique() if "Parameter Signature" in wt.columns else 0
        lines.append(f"| {win_label} | {start or 'start'} → {end or 'now'} | {n_wt:,} | {n_wsig} |")
    lines.append("")

    # ── 2. Per-Window Metrics ─────────────────────────────────────────────────
    h("2. Per-Window Metrics")
    show_cols = ["Parameter Signature", "sig_present", "coins_passing"] + _METRIC_COLS
    for win_label, eval_df in eval_results.items():
        h(f"Window: {win_label}", 3)
        if eval_df.empty:
            lines.append("_No data._\n")
            continue
        avail  = [c for c in show_cols if c in eval_df.columns]
        header = " | ".join(avail)
        sep    = " | ".join("---" for _ in avail)
        lines.append(f"| {header} |")
        lines.append(f"|{sep}|")
        for _, r in eval_df[avail].iterrows():
            cells = [_fmt(r[c]) for c in avail]
            lines.append(f"| {' | '.join(cells)} |")
        lines.append("")

    # ── 3. Cross-Window Heatmaps (as tables) ──────────────────────────────────
    h("3. Cross-Window Heatmaps")
    win_labels_list = list(eval_results.keys())

    def _matrix_md(metric: str, fill: float = 0.0) -> list[str]:
        header = " | ".join(["Signature"] + win_labels_list)
        sep    = " | ".join("---" for _ in range(len(win_labels_list) + 1))
        rows   = [f"| {header} |", f"|{sep}|"]
        for sig, sig_lbl in zip(selected_sigs, sig_labels):
            vals = []
            for wl in win_labels_list:
                df  = eval_results[wl]
                val = fill
                if not df.empty and "Parameter Signature" in df.columns:
                    match = df[df["Parameter Signature"] == sig]
                    if not match.empty and metric in match.columns:
                        raw = match[metric].iloc[0]
                        val = float(raw) if not pd.isna(raw) else fill
                vals.append(val)
            rows.append(f"| `{sig_lbl}` | {' | '.join(f'{v:.2g}' for v in vals)} |")
        return rows

    lines.append("#### Coins Passing\n")
    lines.extend(_matrix_md("coins_passing"))
    lines.append("")
    lines.append("#### SQN\n")
    lines.extend(_matrix_md("SQN"))
    lines.append("")
    lines.append("#### Profit Factor\n")
    lines.extend(_matrix_md("Profit Factor"))
    lines.append("")

    # ── 4. Phase 2 Verdict ────────────────────────────────────────────────────
    h("4. Phase 2 Verdict")
    lines.append(
        f"_Pass: ≥ {min_coins_pass} coins in ≥ {min_windows_pass} "
        f"regime windows (Full Period excluded from verdict)_\n"
    )
    if not v_table.empty:
        n_pass  = int((v_table["verdict"] == "✅ PASS").sum())
        n_total = len(v_table)
        lines.append(f"**{n_pass} / {n_total} signature(s) pass Phase 2.**\n")
        v_cols = list(v_table.columns)
        lines.append(f"| {' | '.join(v_cols)} |")
        lines.append(f"|{'|'.join('---' for _ in v_cols)}|")
        for _, r in v_table.iterrows():
            cells = [_fmt(r[c]) for c in v_cols]
            lines.append(f"| {' | '.join(cells)} |")
        lines.append("")
        lines.append("### Signature Summary\n")
        coin_cols_v = [c for c in v_table.columns if c.endswith("_coins")]
        for _, row in v_table.iterrows():
            verdict_str  = str(row["verdict"])
            sig_short    = sig_to_alias(str(row["Parameter Signature"]))
            n_win        = int(row["windows_passing"])
            coins_detail = "  ·  ".join(
                f"{c.replace('_coins', '')}: **{int(row[c])}** coins"
                for c in coin_cols_v
            )
            lines.append(
                f"- **{sig_short}** — {verdict_str} "
                f"({n_win}/{len(coin_cols_v)} windows) · {coins_detail}"
            )
        lines.append("")
    else:
        lines.append("_No verdict data._\n")

    return "\n".join(lines)

# ── Sidebar ───────────────────────────────────────────────────────────────────

st.sidebar.header("Phase 2 — Date Range Sensitivity")

results_dir = st.sidebar.text_input(
    "📁 Phase 1 results directory",
    placeholder="path/to/full_period_results",
    help="The VBT backtest output folder that contains both the per-symbol CSVs "
         "and the trades/ subfolder with trade log files.",
)

with st.sidebar.expander("📆 Window Definitions", expanded=True):
    st.caption(
        "Edit start / end dates for each window.  "
        "Leave **Full Period** blank to use all available trades as a reference."
    )
    windows_cfg: dict[str, tuple[str | None, str | None]] = {}
    for label, (default_start, default_end) in _DEFAULT_WINDOWS.items():
        col_a, col_b = st.columns(2)
        s = col_a.text_input(f"{label} start", value=default_start or "", key=f"w_start_{label}")
        e = col_b.text_input(f"{label} end",   value=default_end   or "", key=f"w_end_{label}")
        windows_cfg[label] = (s.strip() or None, e.strip() or None)

    st.divider()
    st.caption("**Custom periods** — added to analysis alongside the windows above.")
    st.session_state.setdefault("n_custom_windows", 0)
    c_add, c_rem = st.columns(2)
    if c_add.button("➕ Add period", use_container_width=True):
        st.session_state["n_custom_windows"] += 1
        st.rerun()
    if c_rem.button(
        "➖ Remove last",
        use_container_width=True,
        disabled=st.session_state["n_custom_windows"] == 0,
    ):
        st.session_state["n_custom_windows"] -= 1
        st.rerun()

    for i in range(st.session_state["n_custom_windows"]):
        st.divider()
        cw_label = st.text_input("Label", value=f"Custom {i + 1}", key=f"cw_label_{i}")
        cw_col_a, cw_col_b = st.columns(2)
        cw_start = cw_col_a.text_input("Start", value="", key=f"cw_start_{i}", placeholder="YYYY-MM-DD")
        cw_end   = cw_col_b.text_input("End",   value="", key=f"cw_end_{i}",   placeholder="YYYY-MM-DD")
        key = cw_label.strip() or f"Custom {i + 1}"
        windows_cfg[key] = (cw_start.strip() or None, cw_end.strip() or None)

with st.sidebar.expander("⚙️ Quality Thresholds", expanded=False):
    min_sqn    = st.slider("Min SQN",           0.0, 3.0,  1.0, 0.1)
    min_pf     = st.slider("Min Profit Factor", 1.0, 4.0,  1.3, 0.1)
    min_wr     = st.slider("Min Win Rate (%)",  0.0, 80.0, 30.0, 5.0)
    st.caption(
        "Sharpe Ratio and Max Drawdown are not evaluated in Phase 2 — they "
        "require the equity curve, which is not available in the trade logs."
    )

cfg = RobustnessConfig(
    min_sqn=min_sqn,
    min_profit_factor=min_pf,
    min_win_rate=min_wr,
    min_combo_pass_rate=0.0,
)

with st.sidebar.expander("🏁 Pass Criteria", expanded=True):
    min_trades_per_coin = st.slider("Min trades per coin per window", 2, 30, 5, 1,
        help="Fewer trades → metrics unreliable.  Trades below this count → coin doesn't pass.")
    min_coins_pass   = st.slider("Min coins passing per window", 1, 10, 4, 1)
    _n_verdict_windows = max(1, sum(1 for k in windows_cfg if k != "Full Period"))
    min_windows_pass = st.slider(
        "Min windows passing (excl. Full Period)",
        1, _n_verdict_windows, min(2, _n_verdict_windows), 1,
    )
    top_n_sigs       = st.slider("Top-N signatures to pre-load", 3, 20, 10, 1)
    st.caption(
        f"**PASS** = ≥ {min_coins_pass} coins in ≥ {min_windows_pass} / {_n_verdict_windows} regime windows."
    )

load_button = st.sidebar.button("▶ Load & Analyze", type="primary")
if st.sidebar.button("🗑 Clear cache"):
    st.cache_data.clear()
    st.rerun()

if st.session_state.get("_p2_report_str"):
    st.sidebar.markdown("---")
    _p2_save_btn = st.sidebar.button("💾 Save Report", use_container_width=True)
    _p2_fname_sb = st.session_state.get("_p2_report_filename_default", "phase2_report.md")
    _p2_save_fname_sb = st.sidebar.text_input("Filename", key="p2_sidebar_save_fname", value=_p2_fname_sb)
    if _p2_save_btn:
        try:
            _rd   = st.session_state.get("p2_dir", "")
            _dest = Path(_rd).expanduser().resolve() if _rd else Path(".")
            _dest.mkdir(parents=True, exist_ok=True)
            _fpath = _dest / (_p2_save_fname_sb.strip() or _p2_fname_sb)
            _fpath.write_text(st.session_state["_p2_report_str"], encoding="utf-8")
            st.sidebar.success(f"Saved → `{_fpath}`")
        except Exception as _e:
            st.sidebar.error(f"Save failed: {_e}")

# ── Main ──────────────────────────────────────────────────────────────────────

st.title("📅 Phase 2 — Date Range Sensitivity")
st.caption(
    "One backtest, three regimes.  Trade logs from the full run are sliced by "
    "date window and quality metrics are recomputed per signature × coin."
)

if not load_button and "p2_trades" not in st.session_state:
    st.info(
        "👈 Point the sidebar at your Phase 1 results directory "
        "(must contain a ``trades/`` subfolder), then click **Load & Analyze**."
    )
    st.stop()

# ── Load on button press ──────────────────────────────────────────────────────

if load_button:
    path = results_dir.strip()
    if not path:
        st.error("Please enter the Phase 1 results directory path.")
        st.stop()
    if not Path(path).exists():
        st.error(f"Directory not found: `{path}`")
        st.stop()

    with st.spinner("Loading trade logs…"):
        mt = _mtime(path)
        trades  = _load_trades_cached(path, mt)
        results = pd.DataFrame()
        try:
            results = _load_results_cached(path, mt)
        except Exception:
            pass  # results CSVs are optional; used only for top-sig pre-loading

    # Compute top-N signatures from Phase 1 scores
    top_sigs: list[str] = []
    if not results.empty:
        ann = annotate_dataframe(results, cfg)
        scored = compute_combo_weighted_scores(ann, cfg)
        if not scored.empty:
            top_sigs = scored["Parameter Signature"].head(top_n_sigs).tolist()

    # Fall back to signatures present in the trade logs
    if not top_sigs and not trades.empty and "Parameter Signature" in trades.columns:
        top_sigs = trades["Parameter Signature"].unique().tolist()[:top_n_sigs]

    st.session_state.update({
        "p2_trades":   trades,
        "p2_top_sigs": top_sigs,
        "p2_dir":      path,
    })

# ── Recover from session state ────────────────────────────────────────────────

trades: pd.DataFrame   = st.session_state.get("p2_trades",   pd.DataFrame())
top_sigs: list[str]    = st.session_state.get("p2_top_sigs", [])

if trades.empty:
    st.error(
        "No trade logs found.  Make sure the results directory contains a "
        "``trades/`` subfolder with ``*_trade_log.csv`` files.  "
        "Check that ``save_trade_logs=True`` in your ``RobustnessConfigV4``."
    )
    st.stop()

# ── Pair filter ───────────────────────────────────────────────────────────────

st.markdown("---")
_all_symbols = sorted(trades["Symbol"].unique().tolist()) if "Symbol" in trades.columns else []

if _all_symbols:
    selected_symbols: list[str] = st.multiselect(
        "🪙 Pairs — select which coins to include in the analysis:",
        options=_all_symbols,
        default=_all_symbols,
        help="All pairs are included by default. Remove a coin to exclude all its trades "
             "from every window, heatmap, and verdict.",
    )
    if not selected_symbols:
        st.info("Select at least one pair to continue.")
        st.stop()
    if len(selected_symbols) < len(_all_symbols):
        trades = trades[trades["Symbol"].isin(selected_symbols)].reset_index(drop=True)

# ── Signature selection ────────────────────────────────────────────────────────

st.markdown("---")
all_options = top_sigs.copy()
if "Parameter Signature" in trades.columns:
    for s in trades["Parameter Signature"].unique():
        if s not in all_options:
            all_options.append(s)

if not all_options:
    st.warning("No signatures found in the trade logs.")
    st.stop()

selected_sigs: list[str] = st.multiselect(
    "🔬 Select signatures to evaluate (pre-loaded from Phase 1 top-N by weighted score):",
    options=all_options,
    default=all_options[:min(5, len(all_options))],
    format_func=sig_to_alias,
    help="Signatures are ordered by Phase 1 weighted robustness score (highest first). "
         "Hover over charts to see the full signature.",
)

if not selected_sigs:
    st.info("Select at least one signature to continue.")
    st.stop()

sig_labels = [sig_to_alias(s) for s in selected_sigs]

# ── Section 1 — Trade log status (reflects current pair + signature selection) ─

with st.expander("1. Trade Log Status", expanded=True):
    _info(
        "```\n"
        "Stats reflect the currently selected pairs and signatures.\n\n"
        "Trade logs are saved for the top-N parameter combos per condition\n"
        "(controlled by trade_logs_top_n in RobustnessConfigV4, default 5).\n\n"
        "A signature that ranks outside top-N on a condition will show 0 trades\n"
        "for that coin.  Increase trade_logs_top_n and re-run if needed.\n"
        "```"
    )

    n_trades = len(trades)
    coins_in_logs = trades["Symbol"].nunique() if "Symbol" in trades.columns else 0

    et_min = trades["EntryTime"].min() if "EntryTime" in trades.columns else None
    et_max = trades["EntryTime"].max() if "EntryTime" in trades.columns else None
    period_str = (
        f"{et_min.strftime('%Y-%m-%d')} → {et_max.strftime('%Y-%m-%d')}"
        if et_min is not None and et_max is not None
        else "unknown"
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total trades", f"{n_trades:,}")
    c2.metric("Selected pairs", coins_in_logs)
    c3.metric("Selected signatures", len(selected_sigs))
    c4.metric("Period", period_str)

    # Per-window breakdown showing total vs selected-sig trade counts
    window_counts: list[dict] = []
    for label, (start, end) in windows_cfg.items():
        wt = slice_trades(trades, start, end)
        sig_wt = (
            wt[wt["Parameter Signature"].isin(selected_sigs)]
            if "Parameter Signature" in wt.columns
            else wt
        )
        window_counts.append({
            "Window": label,
            "Date Range": f"{start or 'start'} → {end or 'now'}",
            "# Trades (total)": len(wt),
            "# Trades (selected sigs)": len(sig_wt),
            "# Coins": wt["Symbol"].nunique() if "Symbol" in wt.columns else 0,
        })
    st.dataframe(pd.DataFrame(window_counts), use_container_width=True, hide_index=True)

    # Per-selected-signature trade coverage
    if "Parameter Signature" in trades.columns:
        st.caption("**Trade coverage per selected signature:**")
        cov_rows: list[dict] = []
        for sig in selected_sigs:
            sig_trades = trades[trades["Parameter Signature"] == sig]
            row: dict = {
                "Alias": sig_to_alias(sig),
                "# Trades": len(sig_trades),
                "# Coins": sig_trades["Symbol"].nunique() if "Symbol" in sig_trades.columns else 0,
            }
            for label, (start, end) in windows_cfg.items():
                row[label] = len(slice_trades(sig_trades, start, end))
            cov_rows.append(row)
        st.dataframe(pd.DataFrame(cov_rows), use_container_width=True, hide_index=True)

    # Per-TF breakdown when multiple timeframes are present
    tfs_detected = get_trade_timeframes(trades)
    if len(tfs_detected) > 1:
        st.caption(f"**{len(tfs_detected)} timeframe(s) detected:** {', '.join(tfs_detected)}")
        tf_counts: list[dict] = []
        for tf in tfs_detected:
            tf_trades = filter_trades_by_timeframe(trades, tf)
            tf_counts.append({
                "Timeframe": tf,
                "# Trades": len(tf_trades),
                "# Symbols": tf_trades["Symbol"].nunique() if "Symbol" in tf_trades.columns else 0,
                "# Signatures": tf_trades["Parameter Signature"].nunique() if "Parameter Signature" in tf_trades.columns else 0,
            })
        st.dataframe(pd.DataFrame(tf_counts), use_container_width=True, hide_index=True)

# ── TF detection + routing ────────────────────────────────────────────────────

tfs = get_trade_timeframes(trades)

if len(tfs) <= 1:
    eval_results, v_table = _render_tf_analysis(
        trades, selected_sigs, sig_labels, windows_cfg, cfg,
        min_trades_per_coin, min_coins_pass, min_windows_pass, min_sqn,
    )
else:
    st.info(
        f"**{len(tfs)} timeframe(s) detected:** {', '.join(tfs)} — "
        "showing a separate analysis per timeframe."
    )
    tf_tabs = st.tabs(tfs)
    tf_verdicts: dict[str, pd.DataFrame] = {}
    eval_results: dict[str, pd.DataFrame] = {}
    v_table: pd.DataFrame = pd.DataFrame()

    for tf, tab in zip(tfs, tf_tabs):
        with tab:
            trades_tf = filter_trades_by_timeframe(trades, tf)
            er, vt = _render_tf_analysis(
                trades_tf, selected_sigs, sig_labels, windows_cfg, cfg,
                min_trades_per_coin, min_coins_pass, min_windows_pass, min_sqn,
            )
            tf_verdicts[tf] = vt
            if not eval_results:  # keep first TF's data for the report
                eval_results, v_table = er, vt

    _render_cross_tf_section(tf_verdicts, selected_sigs, sig_labels)

# ── Generate and store Phase 2 report ────────────────────────────────────────
_p2_run_ts  = datetime.now().strftime("%Y-%m-%d_%H%M")
_p2_et_min  = trades["EntryTime"].min() if "EntryTime" in trades.columns else None
_p2_et_max  = trades["EntryTime"].max() if "EntryTime" in trades.columns else None
_p2_period  = (
    (_p2_et_min.strftime("%Y-%m-%d"), _p2_et_max.strftime("%Y-%m-%d"))
    if _p2_et_min is not None and _p2_et_max is not None else None
)
_p2_period_str   = f"_{_p2_period[0]}_{_p2_period[1]}" if _p2_period else ""
_p2_dir_name     = Path(st.session_state.get("p2_dir", results_dir)).name
_p2_fname_default = f"{_p2_run_ts}_{_p2_dir_name}{_p2_period_str}_phase2.md"

_p2_report_str = _format_phase2_report(
    results_dir=st.session_state.get("p2_dir", results_dir),
    run_ts=_p2_run_ts,
    cfg=cfg,
    trades=trades,
    eval_results=eval_results,
    v_table=v_table,
    windows_cfg=windows_cfg,
    min_trades_per_coin=min_trades_per_coin,
    min_coins_pass=min_coins_pass,
    min_windows_pass=min_windows_pass,
    selected_sigs=selected_sigs,
    sig_labels=sig_labels,
    period=_p2_period,
)
st.session_state["_p2_report_str"]             = _p2_report_str
st.session_state["_p2_report_filename_default"] = _p2_fname_default

# ── Inline save button ────────────────────────────────────────────────────────
st.divider()
st.subheader("💾 Save Phase 2 Report")
_p2_inline_fname = st.text_input(
    "Filename", value=_p2_fname_default, key="p2_inline_save_fname",
)
if st.button("💾 Save as Markdown", type="primary", key="p2_inline_save_btn"):
    try:
        _rd   = st.session_state.get("p2_dir", "")
        _dest = Path(_rd).expanduser().resolve() if _rd else Path(".")
        _dest.mkdir(parents=True, exist_ok=True)
        _fpath = _dest / (_p2_inline_fname.strip() or _p2_fname_default)
        _fpath.write_text(_p2_report_str, encoding="utf-8")
        st.success(f"✅ Saved → `{_fpath}`")
    except Exception as _e:
        st.error(f"Save failed: {_e}")
