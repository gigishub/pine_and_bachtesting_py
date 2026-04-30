"""Population masks for the SuperTrend Setup Edge Check.

SuperTrend is computed by pandas_ta on entry_tf bars at bar close.  No
higher-TF alignment is needed — this is a single-timeframe test.

No-lookahead:
    pandas_ta.supertrend() uses ATR(st_length) computed at bar t with only
    bars ≤ t.  Bar t's signal uses bar t's close — correct because we
    signal and enter at close.
    Warmup bars (where the ST line is NaN) are excluded from all populations.

Populations (regime_only is the eligible baseline post-warmup):
    regime_only         — EMA-50 bear regime + ST/ATR warm (eligible baseline).

    st_bear             — regime_only AND SuperTrend direction = −1.
                          The ST line is above close and acts as overhead
                          resistance, confirming an active downtrend.

    st_near_resistance  — st_bear AND close is within
                          proximity_atr_mult × ATR(atr_period) of the ST line.
                          Entry is close to the resistance level — the classic
                          "sell the ceiling" setup where risk is well-defined.

    st_extended         — st_bear AND close is more than
                          proximity_atr_mult × ATR(atr_period) below the ST line.
                          Price has already moved away from the resistance;
                          entry may be catching a move in progress.

Note: st_near_resistance and st_extended are mutually exclusive subsets of
st_bear.  Comparing both against regime_only answers: does proximity to the
ST resistance line add incremental edge beyond just requiring ST bearish?
"""

from __future__ import annotations

import pandas as pd
import pandas_ta as ta  # type: ignore[import]

from bear_strategy.hypothesis_tests.setup_supertrend_edge_check.config import TestConfig


def build_population_masks(
    df: pd.DataFrame,
    config: TestConfig,
) -> dict[str, pd.Series]:
    """Return a boolean mask per population.

    Args:
        df: Entry-TF DataFrame with regime signal, ATR column, and
            SuperTrend columns already attached by the runner.
        config: TestConfig providing all filter parameters.

    Returns:
        dict with keys: ``regime_only``, ``st_bear``,
        ``st_near_resistance``, ``st_extended``.
        All values are boolean pd.Series aligned to df's index.
    """
    st_col = config.st_col()
    st_dir_col = config.st_dir_col()
    _require_columns(df, [config.regime_col, "Close", "atr", st_col, st_dir_col])

    close = df["Close"]
    regime = df[config.regime_col].astype(bool)
    atr = df["atr"]
    st_line = df[st_col]    # resistance line value (above close when direction=-1)
    st_dir = df[st_dir_col]

    # Eligibility: SuperTrend and ATR must be warmed before any bar counts.
    st_ready = st_line.notna() & st_dir.notna()
    atr_ready = atr.notna()
    eligible = regime & st_ready & atr_ready

    # When direction=-1, ST line is the upper band = resistance above price.
    st_bear = st_dir == -1
    # Distance from close up to the resistance line (positive when ST is above).
    distance_to_st = st_line - close

    proximity_threshold = config.proximity_atr_mult * atr

    return {
        "regime_only": eligible,
        # Primary: ST confirms active downtrend.
        "st_bear": eligible & st_bear,
        # Selling near the ST resistance line — well-defined overhead supply.
        "st_near_resistance": eligible & st_bear & (distance_to_st <= proximity_threshold),
        # Price already extended below resistance — momentum continuation entry.
        "st_extended": eligible & st_bear & (distance_to_st > proximity_threshold),
    }


def compute_supertrend(df: pd.DataFrame, config: TestConfig) -> pd.DataFrame:
    """Compute SuperTrend columns via pandas_ta and return them as a DataFrame.

    Args:
        df: OHLCV DataFrame with High, Low, Close columns.
        config: TestConfig with st_length and st_multiplier.

    Returns:
        DataFrame with four pandas_ta SuperTrend columns indexed like df.
    """
    result = ta.supertrend(
        df["High"],
        df["Low"],
        df["Close"],
        length=config.st_length,
        multiplier=config.st_multiplier,
    )
    # pandas_ta returns None if the input is too short to warm up.
    if result is None:
        raise ValueError(
            f"pandas_ta.supertrend returned None — DataFrame may be too short "
            f"(need > {config.st_length} bars)."
        )
    return result


def _require_columns(df: pd.DataFrame, cols: list[str]) -> None:
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(
            f"DataFrame is missing required columns: {missing}. "
            "Run runner._process_pair() to attach regime signals, ATR, and "
            "SuperTrend columns before calling build_population_masks()."
        )
