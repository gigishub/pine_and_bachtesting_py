"""Population masks for the trigger volume confirmation test (Step 3).

Classifies regime-confirmed 1-hour bars into volume_triggered and
not_triggered populations.

Volume trigger definition:
    volume_triggered — bar volume > volume_mult × 20-bar rolling average
    not_triggered    — bar volume ≤ volume_mult × 20-bar rolling average

Look-ahead prevention:
    pandas .rolling(N).mean() at bar t includes bar t itself in the window.
    We shift the rolling average by 1 so bar t is compared against the
    average of bars t-N through t-1 only (all previously completed bars).

Warmup guard:
    Bars within the first volume_window candles have NaN rolling averages
    and are excluded from both populations via the ``valid`` mask.

Required columns: regime_col (from config), Volume.
"""

from __future__ import annotations

import pandas as pd

from bear_strategy.hypothesis_tests.trigger_volume_confirmation.config import TestConfig


def build_population_masks(
    df: pd.DataFrame,
    config: TestConfig,
) -> dict[str, pd.Series]:
    """Return a boolean mask per population.

    Args:
        df: 1h DataFrame with regime column and Volume already attached.
        config: TestConfig providing ``regime_col``, ``volume_window``, and
            ``volume_mult``.

    Returns:
        dict with keys ``all_regime``, ``volume_triggered``, ``not_triggered``.
        All values are boolean pd.Series aligned to df's index.
    """
    _require_columns(df, [config.regime_col, "Volume"])

    regime = df[config.regime_col].astype(bool)

    # Shift by 1: bar t sees avg of bars [t-window, t-1], not [t-window+1, t]
    rolling_avg = (
        df["Volume"]
        .rolling(window=config.volume_window, min_periods=config.volume_window)
        .mean()
        .shift(1)
    )

    # Exclude warmup bars where the shifted avg is still NaN (first window+1 bars)
    valid = rolling_avg.notna()

    vol_spike = df["Volume"] > (config.volume_mult * rolling_avg)

    return {
        "all_regime": regime,
        "volume_triggered": regime & valid & vol_spike,
        "not_triggered": regime & valid & ~vol_spike,
    }


def _require_columns(df: pd.DataFrame, cols: list[str]) -> None:
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(
            f"DataFrame is missing required columns: {missing}. "
            "Ensure the DataFrame has regime signals and Volume attached before "
            "calling build_population_masks()."
        )
