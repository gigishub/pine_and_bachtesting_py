from __future__ import annotations

import pandas as pd

try:
    from ..indicators import ind_atr, ind_ema, zen_bars_above_ma, zen_bars_below_ma, zen_bars_crossed_ma
except ImportError:  # Backward-compatible when imported as top-level `strategy_logic`
    from indicators import ind_atr, ind_ema, zen_bars_above_ma, zen_bars_below_ma, zen_bars_crossed_ma


def compute_base_and_ma_context(
    df: pd.DataFrame,
    ma_length: int,
    ma_breach_lookback: int,
    ma_consolidation_lookback: int,
    ma_consolidation_count: int,
    atr_length: int,
    atr_max_size: float,
) -> dict[str, pd.Series]:
    close = df["Close"].astype(float)
    open_ = df["Open"].astype(float)
    high = df["High"].astype(float)
    low = df["Low"].astype(float)

    ma1 = ind_ema(close, ma_length)
    atr_value = ind_atr(high, low, close, atr_length)
    price_above_ma = (close > ma1).fillna(False)
    atr_max_size_check = (atr_max_size == 0.0) | ((high - low).abs() <= (atr_value * atr_max_size))

    candles_below_ma = zen_bars_below_ma(close, ma1, ma_breach_lookback)
    candles_above_ma = zen_bars_above_ma(close, ma1, ma_breach_lookback)
    ma_cross_count = zen_bars_crossed_ma(open_, close, ma1, ma_consolidation_lookback)
    ma_cross_filter = ma_cross_count < ma_consolidation_count

    is_ready = ma1.notna() & atr_value.notna()

    return {
        "ma1": ma1,
        "atr_value": atr_value,
        "price_above_ma": price_above_ma,
        "atr_max_size_check": atr_max_size_check.fillna(False),
        "candles_below_ma": candles_below_ma,
        "candles_above_ma": candles_above_ma,
        "ma_cross_count": ma_cross_count,
        "ma_cross_filter": ma_cross_filter.fillna(False),
        "is_ready": is_ready.fillna(False),
    }
