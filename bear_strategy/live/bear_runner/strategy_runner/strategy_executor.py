from __future__ import annotations

import logging

import pandas as pd

from bear_strategy.backtest.vectorbt.entry.regime import compute_regime_filter
from bear_strategy.backtest.vectorbt.signals import _apply_regime_aware_throttle
from bear_strategy.strategy.indicators.trigger.vp_session_poc_or_hvn_break import compute_vp_signal
from bear_strategy.strategy.parameters import Parameters
from bear_strategy.strategy.signals import compute_atr
from ..common.types import BearSignals
from ..config import BearLiveConfig

logger = logging.getLogger(__name__)


def _make_params(cfg: BearLiveConfig) -> Parameters:
    """Build a Parameters instance from BearLiveConfig OOS fields."""
    return Parameters(
        stop_atr_mult=cfg.stop_atr_mult,
        target_atr_mult=cfg.target_atr_mult,
        atr_period=cfg.atr_period,
        vp_price_bins=cfg.vp_price_bins,
        entry_regime_offset=cfg.entry_regime_offset,
        rsi_period=cfg.rsi_period,
        rsi_ma_period=cfg.rsi_ma_period,
        rsi_lower=cfg.rsi_lower,
        rsi_upper=cfg.rsi_upper,
        funding_threshold=cfg.funding_threshold,
        funding_ma_period=cfg.funding_ma_period,
        use_ema_200_regime=cfg.use_ema_200_regime,
        min_sl_pct=cfg.min_sl_pct,
    )


class BearStrategyExecutor:
    """Compute bear strategy signals for the last closed 1h bar.

    The same vectorised pipeline used in backtesting is run on the full
    history buffer so the regime-aware throttle behaves identically to the OOS
    test.  Only the final row (``iloc[-1]``) is extracted and returned.
    """

    def __init__(self, cfg: BearLiveConfig) -> None:
        self.cfg = cfg
        self._params = _make_params(cfg)

    def compute(
        self,
        df_1h: pd.DataFrame,
        df_1d: pd.DataFrame,
        funding_df: pd.DataFrame,
    ) -> BearSignals:
        """Run the full signal pipeline; return signals for the last bar.

        Args:
            df_1h:       Closed 1h OHLCV history (lowercase columns, UTC index).
            df_1d:       Closed 1d OHLCV history (lowercase columns, UTC index).
            funding_df:  Funding rate history ('fundingrate' column, UTC index).

        Returns:
            BearSignals — is_ready=False when ATR/RSI warmup is insufficient.
        """
        params = self._params

        atr = compute_atr(df_1h, params.atr_period)
        last_atr = atr.iloc[-1]

        if pd.isna(last_atr):
            logger.debug("ATR warmup not complete; skipping bar.")
            return BearSignals(is_ready=False, entry_signal=False, atr_value=0.0, regime_active=False)

        # Full vectorised regime + trigger computation on history buffer
        regime = compute_regime_filter(df_1h, df_1d, funding_df, params)
        raw_trigger = compute_vp_signal(df_1h, params.vp_price_bins)

        throttled = _apply_regime_aware_throttle(raw_trigger, regime, params.entry_regime_offset)

        # Min SL filter
        close = df_1h["close"].astype(float)
        sl_pct = (params.stop_atr_mult * atr / close.where(close > 0)).fillna(0.0)
        min_sl_mask = sl_pct >= params.min_sl_pct

        entry_signal = bool((throttled & min_sl_mask).iloc[-1])
        regime_active = bool(regime.iloc[-1])

        return BearSignals(
            is_ready=True,
            entry_signal=entry_signal,
            atr_value=float(last_atr),
            regime_active=regime_active,
        )
