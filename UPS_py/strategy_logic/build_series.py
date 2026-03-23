from __future__ import annotations

import pandas as pd

from .base import compute_base_and_ma_context
from .iq import compute_iq_filter_series
from .patterns import compute_long_pattern_and_entry_series
from .pullback import compute_pullback_state_series


def build_strategy_series(
    df: pd.DataFrame,
    # MA
    ma_length: int,
    max_candles_beyond_ma: int,
    ma_consolidation_lookback: int,
    ma_consolidation_count: int,
    ma_breach_lookback: int,
    # IQ filter
    use_iq_filter: bool,
    iq_lookback: int,
    iq_min_score: float,
    iq_slope_atr_scale: float,
    iq_er_weight: float,
    iq_slope_weight: float,
    iq_bias_weight: float,
    use_sq_boost: bool,
    sq_boost_weight: float,
    sq_vol_lookback: int,
    # Trade direction + patterns
    long_trades: bool,
    short_trades: bool,
    enable_ec: bool,
    enable_bullish_engulfing: bool,
    enable_shooting_star: bool,
    ec_wick: bool,
    enable_hammer: bool,
    atr_max_size: float,
    rejection_wick_max_size: float,
    hammer_fib: float,
    hammer_size: float,
    # Stops & targets
    stop_multiplier: float,
    risk_reward_multiplier: float,
    minimum_rr: float,
    pb_reference: str,
    sl_reference: str,
    # Trailing
    trail_stop: bool,
    trail_stop_size: float,
    trail_source: str,
    # Misc
    lookback: int,
    atr_length: int,
    point_allowance: int,
) -> dict[str, pd.Series]:
    """Build all precomputed series used by runtime strategy logic.

    This module orchestrates per-domain functionality split into:
      - base.py (EMA/ATR + MA context counters)
      - iq.py (Intelligent Trend Filter chain)
      - pullback.py (state-machine pullback tracking)
    """
    close = df["Close"].astype(float)
    open_ = df["Open"].astype(float)
    high = df["High"].astype(float)
    low = df["Low"].astype(float)
    volume = df["Volume"].fillna(0.0).astype(float)

    base = compute_base_and_ma_context(
        df=df,
        ma_length=ma_length,
        ma_breach_lookback=ma_breach_lookback,
        ma_consolidation_lookback=ma_consolidation_lookback,
        ma_consolidation_count=ma_consolidation_count,
        atr_length=atr_length,
        atr_max_size=atr_max_size,
    )

    iq = compute_iq_filter_series(
        close=close,
        open_=open_,
        high=high,
        low=low,
        volume=volume,
        ma1=base["ma1"],
        atr_value=base["atr_value"],
        use_iq_filter=use_iq_filter,
        iq_lookback=iq_lookback,
        iq_min_score=iq_min_score,
        iq_slope_atr_scale=iq_slope_atr_scale,
        iq_er_weight=iq_er_weight,
        iq_slope_weight=iq_slope_weight,
        iq_bias_weight=iq_bias_weight,
        use_sq_boost=use_sq_boost,
        sq_boost_weight=sq_boost_weight,
        sq_vol_lookback=sq_vol_lookback,
    )

    pullback = compute_pullback_state_series(
        close=close,
        open_=open_,
        high=high,
        low=low,
        ma1=base["ma1"],
        lookback=lookback,
    )

    patterns = compute_long_pattern_and_entry_series(
        close=close,
        open_=open_,
        high=high,
        low=low,
        ma1=base["ma1"],
        atr_value=base["atr_value"],
        atr_max_size_check=base["atr_max_size_check"],
        ma_cross_filter=base["ma_cross_filter"],
        iq_long_filter=iq["iq_long_filter"],
        iq_short_filter=iq["iq_short_filter"],
        candles_below_ma=base["candles_below_ma"],
        candles_above_ma=base["candles_above_ma"],
        price_above_ma=base["price_above_ma"],
        bullish_pb=pullback["bullish_pb"],
        bearish_pb=pullback["bearish_pb"],
        bullish_close_pb=pullback["bullish_close_pb"],
        bullish_low_pb=pullback["bullish_low_pb"],
        bearish_close_pb=pullback["bearish_close_pb"],
        bearish_high_pb=pullback["bearish_high_pb"],
        long_trades=long_trades,
        short_trades=short_trades,
        enable_ec=enable_ec,
        enable_bullish_engulfing=enable_bullish_engulfing,
        enable_shooting_star=enable_shooting_star,
        ec_wick=ec_wick,
        enable_hammer=enable_hammer,
        rejection_wick_max_size=rejection_wick_max_size,
        hammer_fib=hammer_fib,
        hammer_size=hammer_size,
        max_candles_beyond_ma=max_candles_beyond_ma,
        point_allowance=point_allowance,
    )

    zero_float = pd.Series(0.0, index=df.index, dtype=float)

    return {
        **base,
        **iq,
        **pullback,
        **patterns,
        # Placeholders (Step 5+)
        "long_stop_price": zero_float,
        "long_target_price": zero_float,
        "short_stop_price": zero_float,
        "short_target_price": zero_float,
    }
