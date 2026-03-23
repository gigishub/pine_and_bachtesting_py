from __future__ import annotations

import pandas as pd

from indicators import zen_bars_above_ma, zen_bars_below_ma


def compute_iq_filter_series(
    close: pd.Series,
    open_: pd.Series,
    high: pd.Series,
    low: pd.Series,
    volume: pd.Series,
    ma1: pd.Series,
    atr_value: pd.Series,
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
) -> dict[str, pd.Series]:
    net_move = (close - close.shift(iq_lookback)).abs()
    total_move = close.diff().abs().rolling(iq_lookback, min_periods=iq_lookback).sum()
    efficiency_ratio = (net_move / total_move.replace(0.0, pd.NA)).fillna(0.0).clip(lower=0.0, upper=1.0)

    slope_raw = ((ma1 - ma1.shift(iq_lookback)).abs() / atr_value.replace(0.0, pd.NA)).fillna(0.0)
    slope_score = (slope_raw / max(iq_slope_atr_scale, 1e-12)).clip(lower=0.0, upper=1.0)

    bias_long_score = (zen_bars_above_ma(close, ma1, iq_lookback).astype(float) / float(iq_lookback)).clip(lower=0.0, upper=1.0)
    bias_short_score = (zen_bars_below_ma(close, ma1, iq_lookback).astype(float) / float(iq_lookback)).clip(lower=0.0, upper=1.0)

    weight_sum = iq_er_weight + iq_slope_weight + iq_bias_weight
    if weight_sum > 0:
        long_trend_score = (
            (efficiency_ratio * iq_er_weight)
            + (slope_score * iq_slope_weight)
            + (bias_long_score * iq_bias_weight)
        ) / weight_sum
        short_trend_score = (
            (efficiency_ratio * iq_er_weight)
            + (slope_score * iq_slope_weight)
            + (bias_short_score * iq_bias_weight)
        ) / weight_sum
    else:
        long_trend_score = pd.Series(0.0, index=close.index, dtype=float)
        short_trend_score = pd.Series(0.0, index=close.index, dtype=float)
    long_trend_score = long_trend_score.clip(lower=0.0, upper=1.0)
    short_trend_score = short_trend_score.clip(lower=0.0, upper=1.0)

    candle_range = high - low
    sq_candle_strength = ((close - open_).abs() / candle_range.replace(0.0, pd.NA)).fillna(0.0).clip(lower=0.0, upper=1.0)

    sq_vol_avg = volume.rolling(sq_vol_lookback, min_periods=sq_vol_lookback).mean()
    sq_vol_score = (
        (volume / sq_vol_avg.replace(0.0, pd.NA))
        .clip(upper=2.0)
        .div(2.0)
        .fillna(0.5)
        .clip(lower=0.0, upper=1.0)
    )

    sq_ma_proximity = (
        1.0 - ((close - ma1).abs() / ((atr_value * 2.0).replace(0.0, pd.NA))).clip(upper=1.0)
    ).fillna(0.0).clip(lower=0.0, upper=1.0)

    signal_quality = ((sq_candle_strength + sq_vol_score + sq_ma_proximity) / 3.0).clip(lower=0.0, upper=1.0)
    sq_boost = (sq_boost_weight * signal_quality) if use_sq_boost else pd.Series(0.0, index=close.index, dtype=float)

    iq_long_filter = (~pd.Series(use_iq_filter, index=close.index, dtype=bool)) | ((long_trend_score + sq_boost) >= iq_min_score)
    iq_short_filter = (~pd.Series(use_iq_filter, index=close.index, dtype=bool)) | ((short_trend_score + sq_boost) >= iq_min_score)

    return {
        "efficiency_ratio": efficiency_ratio,
        "slope_score": slope_score,
        "bias_long_score": bias_long_score,
        "bias_short_score": bias_short_score,
        "long_trend_score": long_trend_score,
        "short_trend_score": short_trend_score,
        "sq_candle_strength": sq_candle_strength,
        "sq_vol_score": sq_vol_score,
        "sq_ma_proximity": sq_ma_proximity,
        "signal_quality": signal_quality,
        "sq_boost": sq_boost,
        "iq_long_filter": iq_long_filter.fillna(False),
        "iq_short_filter": iq_short_filter.fillna(False),
    }
