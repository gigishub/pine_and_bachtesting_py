from __future__ import annotations

from dataclasses import asdict, dataclass

from ...strategy.strategy_parameters import StrategySettings


@dataclass(frozen=True)
class DataConfig:
    source: str = "bybit"
    symbol: str = "BTCUSDT"
    market_type: str = "futures"
    timeframe: str = "1day"
    start_time: str = "2025-01-01 00:00:00"
    end_time: str | None = None

    @property
    def dataset_key(self) -> str:
        return f"{self.symbol} {self.timeframe}"


@dataclass(frozen=True)
class MatrixConfig:
    source: str = "bybit"
    market_type: str = "futures"
    symbols: tuple[str, ...] = ("BTCUSDT", "ETHUSDT", "SOLUSDT")
    timeframes: tuple[str, ...] = ("1h", "4h", "1day")
    start_time: str = "2025-01-01 00:00:00"
    end_time: str | None = None
    in_sample_ratio: float = 0.8
    min_bars: int = 150
    top_n: int = 10
    ma_length_choices: tuple[int, ...] = (20, 30, 50, 100)
    risk_reward_choices: tuple[float, ...] = (1.5, 2.0, 3.0, 5.0)
    filter_names: tuple[str, ...] = (
        "use_iq_filter",
        "use_sq_boost",
        "enable_ec",
        "enable_bullish_engulfing",
        "enable_shooting_star",
        "enable_hammer",
    )


BASELINE_SETTINGS = StrategySettings()


PARAMETER_FEATURE_FLAGS: dict[str, tuple[str, ...]] = {
    "iq_lookback": ("use_iq_filter",),
    "iq_min_score": ("use_iq_filter",),
    "iq_slope_atr_scale": ("use_iq_filter",),
    "iq_er_weight": ("use_iq_filter",),
    "iq_slope_weight": ("use_iq_filter",),
    "iq_bias_weight": ("use_iq_filter",),
    "use_sq_boost": ("use_iq_filter",),
    "sq_boost_weight": ("use_iq_filter", "use_sq_boost"),
    "sq_vol_lookback": ("use_iq_filter", "use_sq_boost"),
    "hammer_fib": ("enable_hammer",),
    "hammer_size": ("enable_hammer",),
    "ec_wick": ("enable_ec",),
}

DEFAULT_DATA_CONFIG = DataConfig()
DEFAULT_MATRIX_CONFIG = MatrixConfig()


def build_baseline_params() -> dict[str, object]:
    """Return the configured baseline strategy settings as plain backtest kwargs."""
    return asdict(BASELINE_SETTINGS)


def build_matrix_datasets(matrix_config: MatrixConfig = DEFAULT_MATRIX_CONFIG) -> list[DataConfig]:
    """Expand the asset and timeframe matrix into concrete dataset configs."""
    return [
        DataConfig(
            source=matrix_config.source,
            symbol=symbol,
            market_type=matrix_config.market_type,
            timeframe=timeframe,
            start_time=matrix_config.start_time,
            end_time=matrix_config.end_time,
        )
        for symbol in matrix_config.symbols
        for timeframe in matrix_config.timeframes
    ]


def is_parameter_active(param_name: str, params: dict[str, object]) -> bool:
    """Return True when a parameter is relevant for the current feature toggles."""
    required_flags = PARAMETER_FEATURE_FLAGS.get(param_name, ())
    return all(bool(params.get(flag, False)) for flag in required_flags)