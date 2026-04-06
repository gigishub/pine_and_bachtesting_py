"""
Streamlit dashboard for V4 robustness results.

Launch with:
    streamlit run UPS_py_v2/backtest/reporting/streamlit_viewer.py

Or from the project root after running the sequencer:
    streamlit run UPS_py_v2/backtest/reporting/streamlit_viewer.py
"""
from __future__ import annotations

import re
from pathlib import Path

import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Robustness V4 Viewer",
    page_icon="📊",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

SUMMARY_FILENAME = "ROBUSTNESS_SUMMARY.csv"

# Results root is always relative to this file's location, regardless of cwd.
_HERE = Path(__file__).parent
_RESULTS_ROOT = _HERE.parent / "results"

_ENGINE_DIRS: dict[str, str] = {
    "results_vbt": "vbt",
    "results_backtesting_py": "bpy",
}

_RUN_DIR_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}_\d{4}")


def _discover_runs() -> list[tuple[str, Path]]:
    """Return all timestamped run directories across both engines, newest first.

    Each entry is (display_label, path) where label is e.g. "[vbt] 2026-04-06_1501_UPS".
    """
    runs: list[tuple[str, Path]] = []
    for dir_name, short in _ENGINE_DIRS.items():
        engine_dir = _RESULTS_ROOT / dir_name
        if not engine_dir.exists():
            continue
        for sub in engine_dir.iterdir():
            if sub.is_dir() and _RUN_DIR_PATTERN.match(sub.name):
                runs.append((f"[{short}] {sub.name}", sub))
    # Sort newest first (YYYY-MM-DD_HHMM prefix sorts lexicographically).
    runs.sort(key=lambda t: t[0], reverse=True)
    return runs


def _resolve_default_dir() -> Path:
    """Return the most recent run directory, preferring the .current_run marker."""
    # Check vbt marker first.
    vbt_dir = _RESULTS_ROOT / "results_vbt"
    marker = vbt_dir / ".current_run"
    if marker.exists():
        name = marker.read_text().strip()
        candidate = vbt_dir / name
        if candidate.exists():
            return candidate

    # Fall back to any discovered run (already sorted newest-first).
    runs = _discover_runs()
    if runs:
        return runs[0][1]

    # Last resort: old relative default.
    return Path("results")


@st.cache_data
def _load_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def _load_conditions(results_dir: Path) -> dict[str, pd.DataFrame]:
    frames: dict[str, pd.DataFrame] = {}
    for p in sorted(results_dir.glob("*.csv")):
        if p.name == SUMMARY_FILENAME:
            continue
        frames[p.stem] = _load_csv(p)
    return frames


def _load_summary(results_dir: Path) -> pd.DataFrame | None:
    p = results_dir / SUMMARY_FILENAME
    if p.exists():
        return _load_csv(p)
    return None


def _metric_cols(df: pd.DataFrame) -> list[str]:
    candidates = [
        "Return [%]", "Expectancy [%]", "Profit Factor",
        "Win Rate [%]", "Max Drawdown [%]", "# Trades", "SQN",
    ]
    return [c for c in candidates if c in df.columns]


# ---------------------------------------------------------------------------
# Sidebar: run picker
# ---------------------------------------------------------------------------

st.sidebar.title("📂 Select run")

discovered = _discover_runs()
default_dir = _resolve_default_dir()

if discovered:
    # Build display list; pre-select whichever entry matches the default dir.
    labels = [label for label, _ in discovered]
    paths = [path for _, path in discovered]

    default_index = 0
    for i, p in enumerate(paths):
        if p.resolve() == default_dir.resolve():
            default_index = i
            break

    selected_label = st.sidebar.selectbox(
        "Run directory",
        options=labels,
        index=default_index,
    )
    results_dir = paths[labels.index(selected_label)]
else:
    st.sidebar.info("No timestamped run directories found yet.")
    results_dir = default_dir

with st.sidebar.expander("⚙️ Custom path"):
    custom_input = st.text_input("Override path", value="", placeholder=str(results_dir))
    if custom_input.strip():
        results_dir = Path(custom_input.strip())

if not results_dir.exists():
    st.error(f"Directory not found: `{results_dir}`")
    st.stop()

condition_frames = _load_conditions(results_dir)
summary_df = _load_summary(results_dir)

if not condition_frames and summary_df is None:
    st.warning(f"No CSV files found in `{results_dir}`. Run the sequencer first.")
    st.stop()

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Conditions loaded:** {len(condition_frames)}")
if summary_df is not None:
    st.sidebar.markdown(f"**Summary rows:** {len(summary_df)}")
else:
    st.sidebar.markdown("_No summary yet. Run reporter._")

# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------

tab_overview, tab_condition, tab_deep_dive = st.tabs([
    "📈 Robustness Overview",
    "🔍 Per Condition",
    "🧪 Deep Dive",
])

# ---------------------------------------------------------------------------
# Tab 1: Robustness Overview
# ---------------------------------------------------------------------------

with tab_overview:
    st.header("Robustness Summary")
    st.caption(
        "A parameter setup is **robust** if it performs well across many conditions (pairs + timeframes), "
        "not just one. High Consistency Score = appears in the top results across multiple conditions."
    )

    if summary_df is None:
        st.info(
            "No `ROBUSTNESS_SUMMARY.csv` found. "
            "Run `build_robustness_summary(results_dir)` from `reporter.py` to generate it."
        )
    else:
        col1, col2, col3 = st.columns(3)
        total_conditions = len(condition_frames)
        col1.metric("Conditions", total_conditions)
        col2.metric("Parameter Signatures", len(summary_df))
        if "Consistency Score" in summary_df.columns:
            max_consistency = summary_df["Consistency Score"].max()
            col3.metric("Max Consistency Score", f"{max_consistency}/{total_conditions}")

        st.subheader("Filter")
        col_a, col_b = st.columns(2)
        with col_a:
            min_consistency = st.slider(
                "Min Consistency Score",
                min_value=0,
                max_value=total_conditions,
                value=max(0, total_conditions // 2),
            )
        with col_b:
            min_expectancy = st.number_input("Min Expectancy Mean [%]", value=0.0, step=0.1)

        filtered = summary_df.copy()
        if "Consistency Score" in filtered.columns:
            filtered = filtered[filtered["Consistency Score"] >= min_consistency]
        if "Expectancy [%] Mean" in filtered.columns:
            filtered = filtered[filtered["Expectancy [%] Mean"] >= min_expectancy]

        st.markdown(f"**{len(filtered)} setups** match these filters.")
        st.dataframe(filtered, use_container_width=True)

        if not filtered.empty and "Parameter Signature" in filtered.columns:
            st.subheader("Top Setup Breakdown")
            top_sig = filtered.iloc[0]["Parameter Signature"]
            st.code(top_sig.replace("|", "\n"), language="text")

# ---------------------------------------------------------------------------
# Tab 2: Per Condition
# ---------------------------------------------------------------------------

with tab_condition:
    st.header("Per Condition Results")

    if not condition_frames:
        st.info("No per-condition CSVs found.")
    else:
        selected_condition = st.selectbox("Select condition", sorted(condition_frames.keys()))
        df = condition_frames[selected_condition]

        st.caption(f"Full grid results for **{selected_condition}** — {len(df)} parameter combinations.")

        col1, col2 = st.columns(2)
        with col1:
            top_n = st.slider("Show top N rows", min_value=5, max_value=min(100, len(df)), value=20)
        with col2:
            sort_by = st.selectbox("Sort by", options=_metric_cols(df), index=1)

        display_cols = ["Rank", "Parameter Signature"] + _metric_cols(df)
        display_cols = [c for c in display_cols if c in df.columns]

        top_df = df.nsmallest(top_n, "Rank")[display_cols]
        st.dataframe(top_df, use_container_width=True)

# ---------------------------------------------------------------------------
# Tab 3: Deep Dive — trace one parameter signature across all conditions
# ---------------------------------------------------------------------------

with tab_deep_dive:
    st.header("Deep Dive: Trace a Setup Across Conditions")
    st.caption(
        "Pick a parameter signature and see exactly how it performed on every "
        "pair/timeframe. This reveals whether a result is a one-off or genuinely robust."
    )

    if not condition_frames:
        st.info("No condition data loaded.")
    else:
        all_sigs: list[str] = []
        if summary_df is not None and "Parameter Signature" in summary_df.columns:
            # Pre-populate with top signatures from the summary.
            all_sigs = summary_df["Parameter Signature"].dropna().tolist()
        else:
            all_sigs = (
                pd.concat(condition_frames.values(), ignore_index=True)["Parameter Signature"]
                .dropna()
                .unique()
                .tolist()
            )

        selected_sig = st.selectbox("Parameter Signature", all_sigs)

        if selected_sig:
            rows = []
            for condition, df in condition_frames.items():
                match = df[df["Parameter Signature"] == selected_sig]
                if match.empty:
                    continue
                row = match.iloc[0].to_dict()
                row["Condition"] = condition
                rows.append(row)

            if rows:
                trace_df = pd.DataFrame(rows)
                display_cols = (
                    ["Condition", "Rank"]
                    + _metric_cols(trace_df)
                )
                display_cols = [c for c in display_cols if c in trace_df.columns]

                st.dataframe(trace_df[display_cols], use_container_width=True)

                # Summary stats for this signature.
                st.subheader("Stats across all conditions")
                metric_df = trace_df[[c for c in _metric_cols(trace_df) if c in trace_df.columns]]
                st.dataframe(
                    metric_df.describe().round(4),
                    use_container_width=True,
                )

                st.subheader("Parameter breakdown")
                st.code(selected_sig.replace("|", "\n"), language="text")
            else:
                st.warning("This signature was not found in any condition CSV.")
