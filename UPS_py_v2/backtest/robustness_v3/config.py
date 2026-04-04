from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import TypeAlias

from ...strategy.strategy_parameters import StrategySettings

ParameterValue: TypeAlias = bool | int | float | str
ParameterRange: TypeAlias = tuple[ParameterValue, ...]

# Some parameters only make sense when a parent Boolean filter is enabled.
# Example: iq_lookback should not create extra optimization combinations when
# use_iq_filter is False. The dependency map lets v3 fall back to the baseline
# defaults for those child parameters until the parent feature is turned on.
DEFAULT_FEATURE_DEPENDENCIES: dict[str, tuple[str, ...]] = {
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

DEFAULT_BOOLEAN_FILTER_RANGES: dict[str, ParameterRange] = {
    "use_iq_filter": (False, True),
    "use_sq_boost": (False, True),
    "enable_ec": (False, True),
    "enable_bullish_engulfing": (False, True),
    "enable_shooting_star": (False, True),
    "enable_hammer": (False, True),
}

DEFAULT_RISK_REWARD_RANGE: ParameterRange = (1.5, 2.0, 3.0, 5.0)


@dataclass(frozen=True)
class DatasetConfig:
    source: str = "bybit"
    symbol: str = "BTCUSDT"
    market_type: str = "futures"
    timeframe: str = "1h"
    start_time: str = "2025-01-01 00:00:00"
    end_time: str | None = None

    @property
    def dataset_key(self) -> str:
        return f"{self.symbol} {self.timeframe}"


@dataclass
class OptimizationConfigV3:
    """Simple file-based config for the two-step robustness workflow.

    Step 1 optimizes the primary dataset.
    Step 2 validates the best Step 1 candidates across the matrix.
    """

    source: str = "bybit"
    market_type: str = "futures"
    primary_symbol: str = "BTCUSDT"
    primary_timeframe: str = "1h"
    validation_symbols: list[str] = field(default_factory=lambda: ["BTCUSDT", "ETHUSDT", "SOLUSDT"])
    validation_timeframes: list[str] = field(default_factory=lambda: ["1h", "4h", "1day"])
    start_time: str = "2025-01-01 00:00:00"
    end_time: str | None = None
    min_bars: int = 150
    top_n: int = 10
    baseline_settings: StrategySettings = field(default_factory=StrategySettings)
    boolean_filter_ranges: dict[str, ParameterRange] = field(default_factory=lambda: dict(DEFAULT_BOOLEAN_FILTER_RANGES))
    risk_reward_range: ParameterRange = DEFAULT_RISK_REWARD_RANGE
    optional_parameter_ranges: dict[str, ParameterRange] = field(default_factory=dict)
    feature_dependencies: dict[str, tuple[str, ...]] = field(default_factory=lambda: dict(DEFAULT_FEATURE_DEPENDENCIES))

    def build_baseline_params(self) -> dict[str, object]:
        return asdict(self.baseline_settings)

    def build_primary_dataset(self) -> DatasetConfig:
        return DatasetConfig(
            source=self.source,
            symbol=self.primary_symbol,
            market_type=self.market_type,
            timeframe=self.primary_timeframe,
            start_time=self.start_time,
            end_time=self.end_time,
        )

    def build_validation_datasets(self) -> list[DatasetConfig]:
        return [
            DatasetConfig(
                source=self.source,
                symbol=symbol,
                market_type=self.market_type,
                timeframe=timeframe,
                start_time=self.start_time,
                end_time=self.end_time,
            )
            for symbol in self.validation_symbols
            for timeframe in self.validation_timeframes
        ]

    @property
    def parameter_ranges(self) -> dict[str, ParameterRange]:
        ranges: dict[str, ParameterRange] = {
            **self.boolean_filter_ranges,
            "risk_reward_multiplier": self.risk_reward_range,
        }
        ranges.update(self.optional_parameter_ranges)
        return ranges

    @property
    def parameter_names(self) -> tuple[str, ...]:
        return tuple(self.parameter_ranges.keys())

    def set_primary_dataset(self, *, symbol: str | None = None, timeframe: str | None = None) -> None:
        if symbol:
            self.primary_symbol = symbol
        if timeframe:
            self.primary_timeframe = timeframe

    def set_validation_symbols(self, *symbols: str) -> None:
        cleaned = [symbol for symbol in symbols if symbol]
        if not cleaned:
            raise ValueError("At least one validation symbol must remain")
        self.validation_symbols = cleaned

    def set_validation_timeframes(self, *timeframes: str) -> None:
        cleaned = [timeframe for timeframe in timeframes if timeframe]
        if not cleaned:
            raise ValueError("At least one validation timeframe must remain")
        self.validation_timeframes = cleaned

    def set_matrix_scope(
        self,
        *,
        symbols: list[str],
        timeframes: list[str],
        primary_symbol: str | None = None,
        primary_timeframe: str | None = None,
    ) -> None:
        cleaned_symbols = [symbol for symbol in symbols if symbol]
        cleaned_timeframes = [timeframe for timeframe in timeframes if timeframe]
        if not cleaned_symbols:
            raise ValueError("At least one symbol must be provided")
        if not cleaned_timeframes:
            raise ValueError("At least one timeframe must be provided")

        self.validation_symbols = cleaned_symbols
        self.validation_timeframes = cleaned_timeframes
        self.primary_symbol = primary_symbol or cleaned_symbols[0]
        self.primary_timeframe = primary_timeframe or cleaned_timeframes[0]

    def set_boolean_filter_range(self, name: str, *values: bool) -> None:
        if not values:
            raise ValueError(f"Boolean filter range for {name} cannot be empty")
        self.boolean_filter_ranges[name] = tuple(bool(value) for value in values)

    def set_risk_reward_range(self, *values: float) -> None:
        if not values:
            raise ValueError("risk_reward_range cannot be empty")
        self.risk_reward_range = tuple(float(value) for value in values)

    def set_optional_parameter_range(self, name: str, *values: ParameterValue) -> None:
        if not values:
            raise ValueError(f"Parameter range for {name} cannot be empty")
        self.optional_parameter_ranges[name] = tuple(values)

    def remove_parameter(self, name: str) -> None:
        if name == "risk_reward_multiplier":
            raise ValueError("risk_reward_multiplier is part of the fixed v3 core grid")
        self.boolean_filter_ranges.pop(name, None)
        self.optional_parameter_ranges.pop(name, None)


DEFAULT_OPTIMIZATION_CONFIG_V3 = OptimizationConfigV3()


def build_baseline_params(config: OptimizationConfigV3 = DEFAULT_OPTIMIZATION_CONFIG_V3) -> dict[str, object]:
    return config.build_baseline_params()


def build_primary_dataset(config: OptimizationConfigV3 = DEFAULT_OPTIMIZATION_CONFIG_V3) -> DatasetConfig:
    return config.build_primary_dataset()


def build_validation_datasets(config: OptimizationConfigV3 = DEFAULT_OPTIMIZATION_CONFIG_V3) -> list[DatasetConfig]:
    return config.build_validation_datasets()