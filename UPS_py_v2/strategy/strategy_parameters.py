from __future__ import annotations

from dataclasses import dataclass


@dataclass
class StrategySettings:
    # MA
    ma_length: int = 50
    max_candles_beyond_ma: int = 1
    ma_consolidation_lookback: int = 10
    ma_consolidation_count: int = 4
    ma_breach_lookback: int = 5

    # IQ filter
    use_iq_filter: bool = True
    iq_lookback: int = 20
    iq_min_score: float = 0.55
    iq_slope_atr_scale: float = 1.5
    iq_er_weight: float = 0.5
    iq_slope_weight: float = 0.3
    iq_bias_weight: float = 0.2
    use_sq_boost: bool = True
    sq_boost_weight: float = 0.3
    sq_vol_lookback: int = 20

    # Trade direction
    long_trades: bool = True
    short_trades: bool = True

    # Entry patterns
    enable_ec: bool = True
    enable_bullish_engulfing: bool = True
    enable_shooting_star: bool = True
    ec_wick: bool = False
    enable_hammer: bool = True
    atr_max_size: float = 2.5
    rejection_wick_max_size: float = 0.0
    hammer_fib: float = 0.3
    hammer_size: float = 0.1

    # Stops and targets
    stop_multiplier: float = 1.0
    risk_reward_multiplier: float = 1.0
    minimum_rr: float = 0.0
    pb_reference: str = "Close"
    sl_reference: str = "High/Low"

    # Trailing
    trail_stop: bool = True
    trail_stop_size: float = 1.0
    trail_source: str = "High/Low"

    # Lookback / misc
    lookback: int = 5
    atr_length: int = 14
    point_allowance: int = 0

    # RSI filter
    use_rsi_filter: bool = False
    rsi_period: int = 14
    rsi_overbought: float = 70.0

    # ADX filter
    use_adx_filter: bool = False
    adx_period: int = 14
    adx_min_strength: float = 20.0

    # Volume filter
    use_volume_filter: bool = False
    volume_filter_lookback: int = 20
    volume_filter_multiplier: float = 1.0

    # Backtester sizing
    risk_per_trade: float = 1.0
