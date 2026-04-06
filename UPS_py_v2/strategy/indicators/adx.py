"""ADX (Average Directional Index) filter for the UPS strategy.

Pine-compatible implementation using Wilder/RMA smoothing.
ADX is non-directional: it measures trend *strength* regardless of direction.
Pure pandas functions — no side effects.
"""

from __future__ import annotations

import pandas as pd

from .atr import ind_rma


def compute_adx(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    period: int,
) -> dict[str, pd.Series]:
    """Pine-compatible ADX (+DI, -DI, ADX).

    Matches Pine Script's ta.adx(high, low, close, period).

    Returns:
        adx_plus_di:  Positive directional indicator (+DI).
        adx_minus_di: Negative directional indicator (-DI).
        adx_value:    ADX smoothed directional index [0, 100].
    """
    prev_high = high.shift(1)
    prev_low = low.shift(1)
    prev_close = close.shift(1)

    # True range components
    tr = pd.concat(
        [(high - low), (high - prev_close).abs(), (low - prev_close).abs()],
        axis=1,
    ).max(axis=1)

    # Directional movement: +DM fires when upward move > downward move
    up_move = high - prev_high
    down_move = prev_low - low
    plus_dm = up_move.where((up_move > down_move) & (up_move > 0), 0.0)
    minus_dm = down_move.where((down_move > up_move) & (down_move > 0), 0.0)

    smoothed_tr = ind_rma(tr, period)
    smoothed_plus_dm = ind_rma(plus_dm, period)
    smoothed_minus_dm = ind_rma(minus_dm, period)

    plus_di = 100.0 * smoothed_plus_dm / smoothed_tr.replace(0.0, float("nan"))
    minus_di = 100.0 * smoothed_minus_dm / smoothed_tr.replace(0.0, float("nan"))

    di_sum = (plus_di + minus_di).replace(0.0, float("nan"))
    dx = 100.0 * (plus_di - minus_di).abs() / di_sum
    adx = ind_rma(dx.fillna(0.0), period)

    return {
        "adx_plus_di": plus_di.fillna(0.0),
        "adx_minus_di": minus_di.fillna(0.0),
        "adx_value": adx.fillna(0.0),
    }


def compute_adx_filter(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    use_adx_filter: bool,
    adx_period: int,
    adx_min_strength: float,
) -> dict[str, pd.Series]:
    """ADX trend-strength filter for the UPS strategy.

    Rejects entries in directionless / choppy markets where
    the pullback setup is statistically less reliable.
    ADX > adx_min_strength for both long and short (non-directional).

    When use_adx_filter=False returns all-True filter and zero ADX series.

    Args:
        use_adx_filter:   Master on/off switch; wired into the robustness grid.
        adx_period:       ADX smoothing period (default 14).
        adx_min_strength: Minimum ADX to allow entry (default 20).
                          Commonly: 20=weak trend, 25=moderate, 30=strong.
    """
    true_s = pd.Series(True, index=close.index, dtype=bool)

    if not use_adx_filter:
        return {
            "adx_plus_di": pd.Series(0.0, index=close.index, dtype=float),
            "adx_minus_di": pd.Series(0.0, index=close.index, dtype=float),
            "adx_value": pd.Series(0.0, index=close.index, dtype=float),
            "adx_filter": true_s.copy(),
        }

    adx_series = compute_adx(high, low, close, adx_period)
    adx_filter = (adx_series["adx_value"] > adx_min_strength).fillna(False)

    return {
        **adx_series,
        "adx_filter": adx_filter,
    }
