"""Cross-symbol and cross-timeframe consistency analysis."""

from __future__ import annotations

from collections import Counter

import pandas as pd

from strategy_evaluation.config import RobustnessConfig
from strategy_evaluation.metrics import annotate_dataframe


def symbol_pass_rate(df: pd.DataFrame, cfg: RobustnessConfig) -> dict[str, float]:
    """Return fraction of symbols that have ≥ 1 passing combo.

    Returns
    -------
    dict mapping symbol name → 1.0 if any combo passes, else 0.0
    """
    annotated = annotate_dataframe(df, cfg)
    result: dict[str, float] = {}
    for symbol, group in annotated.groupby(cfg.col_symbol):
        result[str(symbol)] = 1.0 if group["_passes"].any() else 0.0
    return result


def timeframe_pass_rate(df: pd.DataFrame, cfg: RobustnessConfig) -> dict[str, float]:
    """Return fraction of (symbol, timeframe) pairs per timeframe that pass.

    For each timeframe, counts the proportion of symbols where ≥ 1 combo
    passes, giving a normalised 0–1 rate per timeframe.
    """
    annotated = annotate_dataframe(df, cfg)
    tf_symbol_pass: dict[str, set[str]] = {}
    tf_symbol_total: dict[str, set[str]] = {}

    for (symbol, tf), group in annotated.groupby([cfg.col_symbol, cfg.col_timeframe]):
        tf_str = str(tf)
        tf_symbol_total.setdefault(tf_str, set()).add(str(symbol))
        if group["_passes"].any():
            tf_symbol_pass.setdefault(tf_str, set()).add(str(symbol))

    return {
        tf: len(tf_symbol_pass.get(tf, set())) / len(total)
        for tf, total in tf_symbol_total.items()
    }


def top_combo_overlap(df: pd.DataFrame, cfg: RobustnessConfig, top_n: int = 5) -> dict[str, int]:
    """Count how often each Parameter Signature appears in the top-N ranked combos.

    High counts indicate that a parameter set generalises well across symbols
    and timeframes.  Low counts (every symbol has a unique top combo) indicate
    fragility — the strategy is over-fit to individual instruments.

    Only qualifying combos (``_passes=True``) are considered so that low-trade
    outliers with inflated Expectancy do not dominate the frequency count.

    Returns
    -------
    dict mapping Parameter Signature → count of appearances, sorted descending.
    """
    source = df[df["_passes"]].copy() if "_passes" in df.columns else df.copy()
    top_rows = (
        source.sort_values(cfg.col_rank)
        .groupby([cfg.col_symbol, cfg.col_timeframe])
        .head(top_n)
    )
    counter: Counter[str] = Counter(top_rows[cfg.col_param_sig].dropna())
    return dict(counter.most_common())


def toggle_frequency(df: pd.DataFrame, cfg: RobustnessConfig, top_n: int = 5) -> dict[str, int]:
    """Count how often each boolean toggle appears enabled in top-N combos.

    Useful for identifying which indicator filters consistently appear in the
    best-performing combos — high frequency = likely important signal.
    Zero-frequency toggles may be noise.

    Only qualifying combos (``_passes=True``) are considered so that low-trade
    outliers with inflated Expectancy do not skew toggle importance.
    """
    source = df[df["_passes"]].copy() if "_passes" in df.columns else df.copy()
    top_rows = (
        source.sort_values(cfg.col_rank)
        .groupby([cfg.col_symbol, cfg.col_timeframe])
        .head(top_n)
    )
    # Boolean / 0-1 columns that are not metadata
    exclude = {
        cfg.col_symbol, cfg.col_timeframe, cfg.col_param_sig, cfg.col_rank,
        cfg.col_sqn, cfg.col_pf, cfg.col_trades, cfg.col_win_rate,
        cfg.col_sharpe, cfg.col_return,
        "Condition", "Expectancy [%]", "Avg Trade [%]", "Best Trade [%]",
        "Worst Trade [%]", "Avg Win Trade [%]", "Avg Loss Trade [%]",
        "Max Drawdown [%]", "Max Drawdown Duration", "Exposure Time [%]",
        "Calmar Ratio", "_passes", "_score",
    }
    toggle_cols = [c for c in top_rows.columns if c not in exclude]

    counts: dict[str, int] = {}
    for col in toggle_cols:
        enabled = top_rows[col]
        # Support both bool and 0/1 int columns
        try:
            enabled = enabled.astype(float).fillna(0)
            counts[col] = int((enabled == 1).sum())
        except (ValueError, TypeError):
            pass

    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))
