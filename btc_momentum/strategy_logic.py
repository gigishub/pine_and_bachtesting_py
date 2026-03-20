from __future__ import annotations

import pandas as pd

from indicators import ind_atr, ind_ema, non_repainting_htf_ema


def build_strategy_series(
    df: pd.DataFrame,
    higher_timeframe: str,
    ema_length: int,
    atr_length: int,
    bb_length: int,      # reserved — kept for optimizer compatibility
    bb_mult: float,      # reserved — kept for optimizer compatibility
    trail_stop_source: str,
    trail_stop_lookback: int) -> dict[str, pd.Series]:
    
    """Build precomputed indicator/signal series used by the strategy runtime.

    The function does not place orders; it only transforms OHLCV columns into
    reusable pandas Series so execution logic can stay separate.
    """
    close = df["Close"]
    high = df["High"]
    low = df["Low"]

    # Core indicators
    atr_value = ind_atr(high, low, close, atr_length)
    ema_value = ind_ema(close, ema_length)
    htf_ema_value = non_repainting_htf_ema(close, higher_timeframe, ema_length)

    # Direction filter: price above the higher-timeframe EMA means the macro trend is up.
    is_bullish = close > htf_ema_value

    # Caution flag: true when a wide-range bar recently printed (high-low > 1.5 ATR)
    # OR price has dropped back below the local EMA — i.e. momentum is overextended/stalling.
    # The 7-bar lookback matches the Pine source; loosen it here if you want a shorter memory.
    CAUTION_LOOKBACK = 7
    highest_price_n = high.rolling(CAUTION_LOOKBACK).max()
    is_caution = is_bullish & (((highest_price_n - low) > (atr_value * 1.5)) | (close < ema_value))

    # Trailing source can be Low (default) or another OHLCV column name.
    trail_col = trail_stop_source
    trail_src = low if trail_col.lower() == "low" else df[trail_col]
    highest_trail_src = trail_src.rolling(trail_stop_lookback).max()

    # Data-ready flag: only allow signal/position logic when all required indicators are non-null.
    is_ready = (
        atr_value.notna()
        & ema_value.notna()
        & htf_ema_value.notna()
        & highest_trail_src.notna()
    )

    return {
        "atr_value": atr_value,
        "htf_ema_value": htf_ema_value,
        "is_bullish": is_bullish.fillna(False),
        "is_caution": is_caution.fillna(False),
        "highest_trail_src": highest_trail_src,
        "is_ready": is_ready,
    }
