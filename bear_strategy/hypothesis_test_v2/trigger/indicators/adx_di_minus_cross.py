"""
ADX + DI- cross trigger.

Fires when ADX is above a strength threshold and DI- crosses above DI+.
"""
from __future__ import annotations

import pandas as pd


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """Return True when ADX is strong and DI- crosses above DI+."""
    try:
        import pandas_ta as pta
    except ImportError as exc:
        raise ImportError("pandas_ta is required for adx_di_minus_cross; install with: pip install pandas-ta") from exc

    length = int(params.get("length", 14))
    adx_threshold = float(params.get("adx_threshold", 25.0))

    adx_df = pta.adx(
        high=df["high"],
        low=df["low"],
        close=df["close"],
        length=length,
    )

    adx_col = f"ADX_{length}"
    di_plus_col = f"DMP_{length}"
    di_minus_col = f"DMN_{length}"

    if adx_col not in adx_df.columns or di_plus_col not in adx_df.columns or di_minus_col not in adx_df.columns:
        raise ValueError("Expected ADX/DI columns not found in pandas_ta output")

    adx = adx_df[adx_col]
    di_plus = adx_df[di_plus_col]
    di_minus = adx_df[di_minus_col]

    strong_trend = adx > adx_threshold
    prev_di_plus = di_plus.shift(1)
    prev_di_minus = di_minus.shift(1)
    di_cross = (prev_di_minus <= prev_di_plus) & (di_minus > di_plus)

    return (strong_trend & di_cross).fillna(False)
