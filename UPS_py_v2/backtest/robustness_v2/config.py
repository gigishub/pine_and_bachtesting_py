from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import TypeAlias

from ...strategy.strategy_parameters import StrategySettings

ParameterValue: TypeAlias = bool | int | float | str
ParameterRange: TypeAlias = tuple[ParameterValue, ...]

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

DEFAULT_PARAMETER_RANGES: dict[str, ParameterRange] = {
    "ma_length": (20, 30, 50, 100),
    "risk_reward_multiplier": (1.5, 2.0, 3.0, 5.0),
    "use_iq_filter": (False, True),
    "use_sq_boost": (False, True),
    "enable_ec": (False, True),
    "enable_bullish_engulfing": (False, True),
    "enable_shooting_star": (False, True),
    "enable_hammer": (False, True),
}


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
class OptimizationConfig:
    """Configuration for Step 1 (parameter ranges) + Step 2 (multi-asset/timeframe matrix)."""
    source: str = "bybit"
    market_type: str = "futures"
    symbols: list[str] = field(default_factory=lambda: ["BTCUSDT"])
    timeframes: list[str] = field(default_factory=lambda: ["1h"])
    start_time: str = "2025-01-01 00:00:00"
    end_time: str | None = None
    in_sample_ratio: float = 0.8
    min_bars: int = 150
    top_n: int = 10
    baseline_settings: StrategySettings = field(default_factory=StrategySettings)
    parameter_ranges: dict[str, ParameterRange] = field(default_factory=lambda: dict(DEFAULT_PARAMETER_RANGES))
    feature_dependencies: dict[str, tuple[str, ...]] = field(default_factory=lambda: dict(DEFAULT_FEATURE_DEPENDENCIES))

    def build_baseline_params(self) -> dict[str, object]:
        return asdict(self.baseline_settings)

    def build_datasets(self) -> list[DatasetConfig]:
        return [
            DatasetConfig(
                source=self.source,
                symbol=symbol,
                market_type=self.market_type,
                timeframe=timeframe,
                start_time=self.start_time,
                end_time=self.end_time,
            )
            for symbol in self.symbols
            for timeframe in self.timeframes
        ]

    @property
    def parameter_names(self) -> tuple[str, ...]:
        return tuple(self.parameter_ranges.keys())

    def add_symbol(self, symbol: str) -> None:
        if symbol and symbol not in self.symbols:
            self.symbols.append(symbol)

    def remove_symbol(self, symbol: str) -> None:
        self.symbols = [s for s in self.symbols if s != symbol]
        if not self.symbols:
            raise ValueError("At least one symbol must remain")

    def add_timeframe(self, timeframe: str) -> None:
        if timeframe and timeframe not in self.timeframes:
            self.timeframes.append(timeframe)

    def remove_timeframe(self, timeframe: str) -> None:
        self.timeframes = [t for t in self.timeframes if t != timeframe]
        if not self.timeframes:
            raise ValueError("At least one timeframe must remain")

    def set_parameter_range(self, name: str, *values: ParameterValue) -> None:
        if not values:
            raise ValueError(f"Parameter range for {name} cannot be empty")
        self.parameter_ranges[name] = tuple(values)

    def remove_parameter(self, name: str) -> None:
        self.parameter_ranges.pop(name, None)


DEFAULT_OPTIMIZATION_CONFIG = OptimizationConfig()


def build_baseline_params(config: OptimizationConfig = DEFAULT_OPTIMIZATION_CONFIG) -> dict[str, object]:
    return config.build_baseline_params()


def build_datasets(config: OptimizationConfig = DEFAULT_OPTIMIZATION_CONFIG) -> list[DatasetConfig]:
    return config.build_datasets()


def is_parameter_active(
    param_name: str,
    params: dict[str, object],
    feature_dependencies: dict[str, tuple[str, ...]],
) -> bool:
    required_flags = feature_dependencies.get(param_name, ())
    return all(bool(params.get(flag, False)) for flag in required_flags)
