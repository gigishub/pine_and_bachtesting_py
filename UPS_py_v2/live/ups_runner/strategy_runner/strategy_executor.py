from __future__ import annotations

import pandas as pd

from ....strategy.signals import build_strategy_series
from ..config import LiveConfig
from ..common.types import StrategySignals


class StrategyExecutor:
    """Wraps signal computation, hiding all 40+ strategy configuration parameters."""

    def __init__(self, cfg: LiveConfig) -> None:
        self.cfg = cfg

    def compute(self, df: pd.DataFrame) -> StrategySignals:
        """Run strategy indicators on the full OHLCV DataFrame and return scalar values for the last bar."""
        series = build_strategy_series(
            df=df[["Open", "High", "Low", "Close", "Volume"]],
            ma_length=self.cfg.ma_length,
            max_candles_beyond_ma=self.cfg.max_candles_beyond_ma,
            ma_consolidation_lookback=self.cfg.ma_consolidation_lookback,
            ma_consolidation_count=self.cfg.ma_consolidation_count,
            ma_breach_lookback=self.cfg.ma_breach_lookback,
            use_iq_filter=self.cfg.use_iq_filter,
            iq_lookback=self.cfg.iq_lookback,
            iq_min_score=self.cfg.iq_min_score,
            iq_slope_atr_scale=self.cfg.iq_slope_atr_scale,
            iq_er_weight=self.cfg.iq_er_weight,
            iq_slope_weight=self.cfg.iq_slope_weight,
            iq_bias_weight=self.cfg.iq_bias_weight,
            use_sq_boost=self.cfg.use_sq_boost,
            sq_boost_weight=self.cfg.sq_boost_weight,
            sq_vol_lookback=self.cfg.sq_vol_lookback,
            long_trades=self.cfg.long_trades,
            short_trades=self.cfg.short_trades,
            enable_ec=self.cfg.enable_ec,
            enable_bullish_engulfing=self.cfg.enable_bullish_engulfing,
            enable_shooting_star=self.cfg.enable_shooting_star,
            ec_wick=self.cfg.ec_wick,
            enable_hammer=self.cfg.enable_hammer,
            atr_max_size=self.cfg.atr_max_size,
            rejection_wick_max_size=self.cfg.rejection_wick_max_size,
            hammer_fib=self.cfg.hammer_fib,
            hammer_size=self.cfg.hammer_size,
            stop_multiplier=self.cfg.stop_multiplier,
            risk_reward_multiplier=self.cfg.risk_reward_multiplier,
            minimum_rr=self.cfg.minimum_rr,
            pb_reference=self.cfg.pb_reference,
            sl_reference=self.cfg.sl_reference,
            trail_stop=self.cfg.trail_stop,
            trail_stop_size=self.cfg.trail_stop_size,
            trail_source=self.cfg.trail_source,
            lookback=self.cfg.lookback,
            atr_length=self.cfg.atr_length,
            point_allowance=self.cfg.point_allowance,
        )
        i = -1
        return StrategySignals(
            is_ready=bool(series["is_ready"].iloc[i]),
            price_above_ma=bool(series["price_above_ma"].iloc[i]),
            long_conditions_met=bool(series["long_conditions_met"].iloc[i]),
            bearish_pb=bool(series["bearish_pb"].iloc[i]),
            long_entry_pattern=bool(series["long_entry_pattern"].iloc[i]),
            short_conditions_met=bool(series["short_conditions_met"].iloc[i]),
            bullish_pb=bool(series["bullish_pb"].iloc[i]),
            short_entry_pattern=bool(series["short_entry_pattern"].iloc[i]),
            atr_value=float(series["atr_value"].iloc[i]),
        )
