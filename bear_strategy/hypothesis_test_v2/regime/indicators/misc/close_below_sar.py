"""
close_below_sar — Regime indicator.

What it measures
----------------
Identifies downtrend regime bars using Parabolic SAR. When the SAR
generates a downtrend signal, the market structure is considered bearish.

Why it matters
--------------
Parabolic SAR is a trend-following regime filter: the indicator flips
when the trend changes, making it a good candidate for regime-level
bearish gating.

Signal contract
---------------
Returns a boolean Series (same index as df).
True  = PSAR indicates a downtrend.
False = uptrend, reversal, or warm-up.
"""

from __future__ import annotations

import pandas as pd


def _compute_parabolic_sar_trend(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    af_initial: float,
    af_step: float,
    af_max: float,
) -> pd.Series:
    n = len(close)
    if n < 3:
        return pd.Series(False, index=close.index, dtype=bool)

    trend_is_down = close.iloc[1] <= close.iloc[0]
    sar_values: list[float] = []
    trend: list[bool] = []

    if trend_is_down:
        sar = float(high.iloc[0])
        ep = float(low.iloc[0])
    else:
        sar = float(low.iloc[0])
        ep = float(high.iloc[0])

    af = af_initial
    sar_values.append(sar)
    trend.append(trend_is_down)

    for i in range(1, n):
        prev_sar = sar_values[-1]
        if trend_is_down:
            candidate_sar = prev_sar + af * (ep - prev_sar)
            if i >= 2:
                candidate_sar = max(candidate_sar, float(high.iloc[i - 1]), float(high.iloc[i - 2]))
            else:
                candidate_sar = max(candidate_sar, float(high.iloc[i - 1]))

            if float(high.iloc[i]) > candidate_sar:
                trend_is_down = False
                sar = ep
                ep = float(high.iloc[i])
                af = af_initial
            else:
                sar = candidate_sar
                if float(low.iloc[i]) < ep:
                    ep = float(low.iloc[i])
                    af = min(af + af_step, af_max)
        else:
            candidate_sar = prev_sar + af * (ep - prev_sar)
            if i >= 2:
                candidate_sar = min(candidate_sar, float(low.iloc[i - 1]), float(low.iloc[i - 2]))
            else:
                candidate_sar = min(candidate_sar, float(low.iloc[i - 1]))

            if float(low.iloc[i]) < candidate_sar:
                trend_is_down = True
                sar = ep
                ep = float(low.iloc[i])
                af = af_initial
            else:
                sar = candidate_sar
                if float(high.iloc[i]) > ep:
                    ep = float(high.iloc[i])
                    af = min(af + af_step, af_max)

        sar_values.append(sar)
        trend.append(trend_is_down)

    return pd.Series(trend, index=close.index, dtype=bool)


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """Return True when PSAR indicates a downtrend regime."""
    af_initial = float(params.get("af_initial", 0.02))
    af_step = float(params.get("af_step", 0.02))
    af_max = float(params.get("af_max", 0.20))

    return _compute_parabolic_sar_trend(
        df["high"],
        df["low"],
        df["close"],
        af_initial,
        af_step,
        af_max,
    )
