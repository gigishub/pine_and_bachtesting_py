"""Standalone volume filter for the UPS strategy.

Confirms entries only when volume is above a rolling average threshold.
Separates volume confirmation from the IQ SQ boost so it can be toggled
independently in the robustness grid.
Pure pandas functions — no side effects.
"""

from __future__ import annotations

import pandas as pd


def compute_volume_filter(
    volume: pd.Series,
    use_volume_filter: bool,
    volume_filter_lookback: int,
    volume_filter_multiplier: float,
) -> dict[str, pd.Series]:
    """Volume above rolling-average filter.

    Returns True when the current bar's volume exceeds
    `volume_filter_multiplier × rolling_mean(volume, lookback)`.

    Applies to both long and short entries (volume is non-directional).
    When use_volume_filter=False returns all-True filter.

    Args:
        volume:                   Volume series.
        use_volume_filter:        Master on/off switch; wired into the robustness grid.
        volume_filter_lookback:   Rolling window for average volume (default 20).
        volume_filter_multiplier: Required volume as a multiple of the average (default 1.0).
                                  E.g. 1.2 = volume must be 20% above average.
    """
    true_s = pd.Series(True, index=volume.index, dtype=bool)

    if not use_volume_filter:
        return {
            "volume_avg": pd.Series(0.0, index=volume.index, dtype=float),
            "volume_filter": true_s.copy(),
        }

    vol_avg = volume.rolling(volume_filter_lookback, min_periods=volume_filter_lookback).mean()
    required = vol_avg * volume_filter_multiplier

    return {
        "volume_avg": vol_avg.fillna(0.0),
        # fillna(True): don't block trades during warmup period where avg is unavailable
        "volume_filter": (volume >= required).fillna(True),
    }
