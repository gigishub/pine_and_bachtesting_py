"""Population masks for the regime random-entry falsification test.

Builds boolean Series from a 15-min DataFrame that already carries
the mapped regime signals (added by signals.py):

    all_candles        — every bar (baseline / unrestricted)
    ema_200_slope      — EMA 200 slope is negative (downtrend)
    ema_below_50       — daily close < EMA 50
    ema_below_100      — daily close < EMA 100
    ema_below_150      — daily close < EMA 150

Each of the four regime conditions is tested independently against the
baseline — no combined filter.
"""

from __future__ import annotations

import pandas as pd


def build_population_masks(
    df: pd.DataFrame,
    ema_slope_period: int,
    ema_below_periods: list[int],
) -> dict[str, pd.Series]:
    """Return a boolean mask per population.

    Args:
        df: 15-min DataFrame with regime signal columns already attached
            by compute_regime_signals():
              - ``ema_{ema_slope_period}_slope_regime``
              - ``ema_below_{p}_regime`` for each p in ema_below_periods
        ema_slope_period: The EMA period used for slope detection (e.g. 200).
        ema_below_periods: EMA periods for close-below detection (e.g. [50, 100, 150]).

    Returns:
        dict mapping population name → boolean pd.Series aligned to df's index.
        True means the bar belongs to that population.
    """
    required = [f"ema_{ema_slope_period}_slope_regime"] + [
        f"ema_below_{p}_regime" for p in ema_below_periods
    ]
    _require_columns(df, required)

    masks: dict[str, pd.Series] = {
        "all_candles": pd.Series(True, index=df.index),
        f"ema_{ema_slope_period}_slope": df[f"ema_{ema_slope_period}_slope_regime"].astype(bool),
    }
    for period in ema_below_periods:
        masks[f"ema_below_{period}"] = df[f"ema_below_{period}_regime"].astype(bool)
        # Combined: slope + close-below both active
        masks[f"ema_{ema_slope_period}_slope_and_below_{period}"] = (
            df[f"ema_{ema_slope_period}_slope_regime"].astype(bool)
            & df[f"ema_below_{period}_regime"].astype(bool)
        )

    return masks


def _require_columns(df: pd.DataFrame, cols: list[str]) -> None:
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(
            f"DataFrame is missing required regime columns: {missing}. "
            "Run compute_regime_signals() first and attach the result to df."
        )
