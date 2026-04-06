"""Vectorized signal and stop arrays for the UPS strategy (vectorbt engine).

WHY THIS FILE EXISTS
--------------------
backtesting.py runs bar-by-bar in Python (Strategy.next() is called once per candle).
vectorbt avoids that loop entirely: you hand it numpy arrays and it simulates the
whole portfolio in a single compiled pass (numba under the hood).

This module is the "adapter layer" between our strategy logic and vectorbt's API:
  1. It calls build_strategy_series() to get all entry/filter signals as pandas Series
     (this is exactly the same data computed in backtesting.py's Strategy.init()).
  2. It vectorizes the SL/TP math that was previously done bar-by-bar in next().
  3. It converts absolute price levels → relative fractions, which is what
     vbt.Portfolio.from_signals() expects for sl_stop and tp_stop.
  4. It computes per-bar position sizing using the same risk-per-trade formula.

KEY DIFFERENCE FROM backtesting.py
-----------------------------------
In the backtesting.py engine:
    - SL/TP are computed at run-time inside next() using the live trade price.
    - The stop is an absolute price level, updated each bar.

In the vectorbt engine:
    - SL/TP fractions are pre-computed for EVERY bar before simulation starts.
    - vbt reads the fraction at the entry bar, anchors it to the actual entry price,
      and handles the stop natively (checking high/low each bar for intra-bar hits).
    - Values at non-entry bars are ignored by vbt.

NOTE: trail_stop is intentionally set to False and ignored.
Trailing stops require vbt.Portfolio.from_order_func() with a numba-compiled
order function — a significantly more complex implementation left for a future phase.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from ..strategy.signals import build_strategy_series
from ..strategy.strategy_parameters import StrategySettings


def build_vbt_arrays(
    df: pd.DataFrame,
    settings: StrategySettings | None = None,
) -> dict[str, pd.Series]:
    """Build all arrays needed for vbt.Portfolio.from_signals().

    This is the main entry point for the vectorbt engine. It produces five
    parallel arrays that describe WHAT to trade, WHEN to trade, and HOW MUCH:

      entries        - bool Series: True where a long entry signal fires
      short_entries  - bool Series: True where a short entry signal fires
      sl_stop        - float Series: stop-loss as a FRACTION from entry price
                       (e.g. 0.02 = stop 2% below entry for longs, 2% above for shorts)
      tp_stop        - float Series: take-profit as a FRACTION from entry price
      size           - float Series: position size as a fraction of available cash

    vbt reads sl_stop/tp_stop/size ONLY at bars where entries/short_entries are True.
    The values at all other bars are irrelevant and have no effect on the simulation.

    Args:
        df:       OHLCV DataFrame with columns Open/High/Low/Close/Volume and DatetimeIndex.
        settings: Strategy parameters. Defaults to StrategySettings().
    """
    s = settings or StrategySettings()

    signals = build_strategy_series(
        df=df,
        ma_length=s.ma_length,
        max_candles_beyond_ma=s.max_candles_beyond_ma,
        ma_consolidation_lookback=s.ma_consolidation_lookback,
        ma_consolidation_count=s.ma_consolidation_count,
        ma_breach_lookback=s.ma_breach_lookback,
        use_iq_filter=s.use_iq_filter,
        iq_lookback=s.iq_lookback,
        iq_min_score=s.iq_min_score,
        iq_slope_atr_scale=s.iq_slope_atr_scale,
        iq_er_weight=s.iq_er_weight,
        iq_slope_weight=s.iq_slope_weight,
        iq_bias_weight=s.iq_bias_weight,
        use_sq_boost=s.use_sq_boost,
        sq_boost_weight=s.sq_boost_weight,
        sq_vol_lookback=s.sq_vol_lookback,
        use_rsi_filter=s.use_rsi_filter,
        rsi_period=s.rsi_period,
        rsi_overbought=s.rsi_overbought,
        use_adx_filter=s.use_adx_filter,
        adx_period=s.adx_period,
        adx_min_strength=s.adx_min_strength,
        use_volume_filter=s.use_volume_filter,
        volume_filter_lookback=s.volume_filter_lookback,
        volume_filter_multiplier=s.volume_filter_multiplier,
        long_trades=s.long_trades,
        short_trades=s.short_trades,
        enable_ec=s.enable_ec,
        enable_bullish_engulfing=s.enable_bullish_engulfing,
        enable_shooting_star=s.enable_shooting_star,
        ec_wick=s.ec_wick,
        enable_hammer=s.enable_hammer,
        atr_max_size=s.atr_max_size,
        rejection_wick_max_size=s.rejection_wick_max_size,
        hammer_fib=s.hammer_fib,
        hammer_size=s.hammer_size,
        stop_multiplier=s.stop_multiplier,
        risk_reward_multiplier=s.risk_reward_multiplier,
        minimum_rr=s.minimum_rr,
        pb_reference=s.pb_reference,
        sl_reference=s.sl_reference,
        # Trailing not supported in vbt path — disable to avoid confusion
        trail_stop=False,
        trail_stop_size=s.trail_stop_size,
        trail_source=s.trail_source,
        lookback=s.lookback,
        atr_length=s.atr_length,
        point_allowance=s.point_allowance,
    )

    close = df["Close"].astype(float)
    open_ = df["Open"].astype(float)
    high = df["High"].astype(float)
    low = df["Low"].astype(float)
    atr = signals["atr_value"]

    # shift(1) gives the previous bar's value — mirrors low[1] / high[1] in Pine Script
    low_prev = low.shift(1).fillna(low)
    high_prev = high.shift(1).fillna(high)

    # ----------------------------------------------------------------
    # STEP 1: Vectorized SL source selection
    # Mirrors strategy/risk/sl_tp.py compute_long_stop / compute_short_stop
    # but applied to entire arrays instead of one bar at a time.
    # ----------------------------------------------------------------
    ref = s.sl_reference.strip().lower()
    if ref == "high/low":
        # Long SL anchors below the lowest of this bar and the previous bar
        long_src = np.minimum(low.values, low_prev.values)
        # Short SL anchors above the highest of this bar and the previous bar
        short_src = np.maximum(high.values, high_prev.values)
    elif ref == "open":
        long_src = open_.values
        short_src = open_.values
    else:  # "close"
        long_src = close.values
        short_src = close.values

    # Absolute stop price = anchor ± ATR * multiplier
    long_stop = long_src - atr.values * s.stop_multiplier
    short_stop = short_src + atr.values * s.stop_multiplier

    # ----------------------------------------------------------------
    # STEP 2: Convert absolute stop prices → relative fractions
    # vbt.Portfolio.from_signals() expects sl_stop as a FRACTION of entry price:
    #   sl_stop = 0.05  →  stop triggers when price moves 5% against the trade
    #
    # We assume entry at close price, so:
    #   sl_long_pct  = (close - long_stop)  / close
    #   sl_short_pct = (short_stop - close) / close
    # ----------------------------------------------------------------
    cl = close.values
    safe_cl = np.where(cl > 0, cl, np.nan)  # avoid division by zero on malformed data

    sl_long_pct = (cl - long_stop) / safe_cl
    sl_short_pct = (short_stop - cl) / safe_cl

    # Risk distance in price terms (used to scale the TP symmetrically)
    long_risk = cl - long_stop
    short_risk = short_stop - cl

    # TP = entry + risk * RR multiplier  (same math as compute_long_target)
    long_target = cl + long_risk * s.risk_reward_multiplier
    short_target = cl - short_risk * s.risk_reward_multiplier

    tp_long_pct = (long_target - cl) / safe_cl
    tp_short_pct = (cl - short_target) / safe_cl

    # Guard against degenerate bars (zero ATR, missing data, etc.)
    sl_long_pct = np.clip(np.nan_to_num(sl_long_pct, nan=0.05), 1e-6, 1.0)
    sl_short_pct = np.clip(np.nan_to_num(sl_short_pct, nan=0.05), 1e-6, 1.0)
    tp_long_pct = np.clip(np.nan_to_num(tp_long_pct, nan=0.0), 0.0, 100.0)
    tp_short_pct = np.clip(np.nan_to_num(tp_short_pct, nan=0.0), 0.0, 100.0)

    # ----------------------------------------------------------------
    # STEP 3: Position sizing
    # Target: risk exactly risk_per_trade% of current equity on each trade.
    #
    # Derivation (same as strategy/risk/sizing.py but vectorized):
    #   risk_cash   = equity * (risk_per_trade / 100)
    #   units       = risk_cash / (entry_price * sl_pct)   ← stop distance in price
    #   notional    = units * entry_price
    #   size_frac   = notional / equity
    #              = risk_per_trade / 100 / sl_pct
    #
    # size_type="percent" in vbt means "percent of available cash".
    # Since we use exclusive orders (one trade at a time), available cash ≈ equity
    # at every entry bar, so this fraction is accurate.
    # ----------------------------------------------------------------
    rpt = max(s.risk_per_trade, 0.0) / 100.0
    size_long = np.clip(rpt / np.maximum(sl_long_pct, 1e-6), 0.0, 0.9999)
    size_short = np.clip(rpt / np.maximum(sl_short_pct, 1e-6), 0.0, 0.9999)

    valid_long = signals["valid_long_entry"].values.astype(bool)
    valid_short = signals["valid_short_entry"].values.astype(bool)

    # ----------------------------------------------------------------
    # STEP 4: minimum_rr filter
    # In backtesting.py this check lives in next(); replicated here so the
    # same trade-filtering logic applies in both engines.
    # ----------------------------------------------------------------
    if s.minimum_rr > 0.0:
        rr_long = tp_long_pct / np.maximum(sl_long_pct, 1e-6)
        rr_short = tp_short_pct / np.maximum(sl_short_pct, 1e-6)
        valid_long = valid_long & (rr_long >= s.minimum_rr)
        valid_short = valid_short & (rr_short >= s.minimum_rr)

    # ----------------------------------------------------------------
    # STEP 5: Combine into single arrays
    # vbt takes one sl_stop / tp_stop / size array for the whole portfolio.
    # At a long entry bar we want long values; at a short entry bar we want
    # short values.  np.where does this with no Python loop.
    #
    # Because entries and short_entries are mutually exclusive (exclusive_orders),
    # the two arrays never overlap, so the where() condition is unambiguous.
    # ----------------------------------------------------------------
    sl_pct = np.where(valid_short, sl_short_pct, sl_long_pct)
    tp_pct = np.where(valid_short, tp_short_pct, tp_long_pct)
    size_arr = np.where(valid_short, size_short, size_long)

    idx = df.index
    return {
        "entries": pd.Series(valid_long, index=idx, dtype=bool),
        "short_entries": pd.Series(valid_short, index=idx, dtype=bool),
        "sl_stop": pd.Series(sl_pct, index=idx, dtype=float),
        "tp_stop": pd.Series(tp_pct, index=idx, dtype=float),
        "size": pd.Series(size_arr, index=idx, dtype=float),
    }
