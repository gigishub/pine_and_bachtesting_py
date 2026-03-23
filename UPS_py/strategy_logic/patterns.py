from __future__ import annotations

import numpy as np
import pandas as pd


def compute_long_pattern_and_entry_series(
    close: pd.Series,
    open_: pd.Series,
    high: pd.Series,
    low: pd.Series,
    ma1: pd.Series,
    atr_value: pd.Series,
    # Prior-step signals
    atr_max_size_check: pd.Series,
    ma_cross_filter: pd.Series,
    iq_long_filter: pd.Series,
    iq_short_filter: pd.Series,
    candles_below_ma: pd.Series,
    candles_above_ma: pd.Series,
    price_above_ma: pd.Series,
    bullish_pb: pd.Series,
    bearish_pb: pd.Series,
    bullish_close_pb: pd.Series,
    bullish_low_pb: pd.Series,
    bearish_close_pb: pd.Series,
    bearish_high_pb: pd.Series,
    # Inputs
    long_trades: bool,
    short_trades: bool,
    enable_ec: bool,
    enable_bullish_engulfing: bool,
    enable_shooting_star: bool,
    ec_wick: bool,
    enable_hammer: bool,
    rejection_wick_max_size: float,
    hammer_fib: float,
    hammer_size: float,
    max_candles_beyond_ma: int,
    point_allowance: int,
) -> dict[str, pd.Series]:
    """Compute Step 3E long pattern primitives and integrated entry booleans."""

    # NOTE: Pine uses syminfo.mintick * pointAllowance.  We currently treat
    # pointAllowance as a direct price offset because instrument tick size is
    # unavailable at this precompute layer.
    allowance = float(point_allowance)

    prev_open = open_.shift(1)
    prev_close = close.shift(1)
    prev_high = high.shift(1)
    prev_low = low.shift(1)

    body = (close - open_).abs()
    highest_body = pd.Series(np.maximum(close.to_numpy(dtype=float), open_.to_numpy(dtype=float)), index=close.index, dtype=float)
    lowest_body = pd.Series(np.minimum(close.to_numpy(dtype=float), open_.to_numpy(dtype=float)), index=close.index, dtype=float)
    top_wick = (high - highest_body).clip(lower=0.0)
    bottom_wick = (lowest_body - low).clip(lower=0.0)
    top_wick_to_body = top_wick / body.replace(0.0, pd.NA)
    bottom_wick_to_body = bottom_wick / body.replace(0.0, pd.NA)

    bullish_ec_base = (
        (prev_close <= prev_open)
        & (close >= prev_open)
        & (open_ <= (prev_close + allowance))
    )
    if ec_wick:
        bullish_ec_base = bullish_ec_base & (close >= prev_high)

    if rejection_wick_max_size == 0.0:
        rejection_ok = pd.Series(True, index=close.index, dtype=bool)
    else:
        rejection_ok = (top_wick_to_body < rejection_wick_max_size).fillna(False)

    bullish_engulfing = (
        bullish_ec_base
        & rejection_ok
        & (close < bullish_close_pb)
        & ((low == bullish_low_pb) | (low.shift(1) == bullish_low_pb))
    ).fillna(False)

    bearish_ec_base = (
        (prev_close >= prev_open)
        & (close <= prev_open)
        & (open_ >= (prev_close - allowance))
    )
    if ec_wick:
        bearish_ec_base = bearish_ec_base & (close <= prev_low)

    if rejection_wick_max_size == 0.0:
        bearish_rejection_ok = pd.Series(True, index=close.index, dtype=bool)
    else:
        bearish_rejection_ok = (bottom_wick_to_body < rejection_wick_max_size).fillna(False)

    bearish_engulfing = (
        bearish_ec_base
        & bearish_rejection_ok
        & (close > bearish_close_pb)
        & ((high == bearish_high_pb) | (high.shift(1) == bearish_high_pb))
    ).fillna(False)

    bull_fib = (low - high) * hammer_fib + high
    bear_fib = (high - low) * hammer_fib + low
    lowest_body = pd.Series(np.minimum(close.to_numpy(dtype=float), open_.to_numpy(dtype=float)), index=close.index, dtype=float)
    highest_body = pd.Series(np.maximum(close.to_numpy(dtype=float), open_.to_numpy(dtype=float)), index=close.index, dtype=float)
    is_hammer = (lowest_body >= bull_fib).fillna(False)
    is_star = (highest_body <= bear_fib).fillna(False)
    three_bar_low = low.rolling(3, min_periods=3).min()
    three_bar_high = high.rolling(3, min_periods=3).max()
    hammer_candle = (
        is_hammer
        & ((high - low) >= (hammer_size * atr_value))
        & (low == bullish_low_pb)
        & (low == three_bar_low)
    ).fillna(False)
    star_candle = (
        is_star
        & ((high - low) >= (hammer_size * atr_value))
        & (high == bearish_high_pb)
        & (high == three_bar_high)
    ).fillna(False)

    engulfing_enabled = pd.Series(bool(enable_ec and enable_bullish_engulfing), index=close.index, dtype=bool)
    hammer_enabled = pd.Series(bool(enable_hammer), index=close.index, dtype=bool)
    star_enabled = pd.Series(bool(enable_shooting_star), index=close.index, dtype=bool)

    long_entry_pattern = (
        (engulfing_enabled & bullish_engulfing)
        | (hammer_enabled & hammer_candle)
    ).fillna(False)
    short_entry_pattern = (
        (pd.Series(bool(enable_ec), index=close.index, dtype=bool) & bearish_engulfing)
        | (star_enabled & star_candle)
    ).fillna(False)

    general_conditions_met = (
        atr_max_size_check.astype(bool)
        & ma_cross_filter.astype(bool)
        & atr_value.notna()
        & ma1.notna()
    )
    candles_below_gate = candles_below_ma.astype(float) <= float(max_candles_beyond_ma)
    candles_above_gate = candles_above_ma.astype(float) <= float(max_candles_beyond_ma)
    long_conditions_met = (
        general_conditions_met
        & iq_long_filter.astype(bool)
        & candles_below_gate
        & pd.Series(bool(long_trades), index=close.index, dtype=bool)
    ).fillna(False)
    short_conditions_met = (
        general_conditions_met
        & iq_short_filter.astype(bool)
        & candles_above_gate
        & pd.Series(bool(short_trades), index=close.index, dtype=bool)
    ).fillna(False)

    valid_long_entry = (
        price_above_ma.astype(bool)
        & long_conditions_met
        & bearish_pb.astype(bool)
        & long_entry_pattern
    ).fillna(False)
    valid_short_entry = (
        (~price_above_ma.astype(bool))
        & short_conditions_met
        & bullish_pb.astype(bool)
        & short_entry_pattern
    ).fillna(False)

    return {
        "bullish_engulfing": bullish_engulfing,
        "bearish_engulfing": bearish_engulfing,
        "hammer_candle": hammer_candle,
        "star_candle": star_candle,
        "long_entry_pattern": long_entry_pattern,
        "short_entry_pattern": short_entry_pattern,
        "long_conditions_met": long_conditions_met,
        "short_conditions_met": short_conditions_met,
        "valid_long_entry": valid_long_entry,
        "valid_short_entry": valid_short_entry,
        # Debug columns for funnel/subcondition validation.
        "dbg_general_conditions_met": general_conditions_met.fillna(False),
        "dbg_candles_below_gate": candles_below_gate.fillna(False),
        "dbg_candles_above_gate": candles_above_gate.fillna(False),
        "dbg_price_above_ma": price_above_ma.astype(bool).fillna(False),
        "dbg_bearish_pb": bearish_pb.astype(bool).fillna(False),
        "dbg_bullish_pb": bullish_pb.astype(bool).fillna(False),
    }
