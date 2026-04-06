from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import TypeAlias

from ...strategy.strategy_parameters import StrategySettings

# Type aliases — keep param values and ranges explicit so type checkers catch mistakes.
ParameterValue: TypeAlias = bool | int | float | str
ParameterRange: TypeAlias = tuple[ParameterValue, ...]

# Maps child parameters → the parent flag(s) that must be True for the child to matter.
# When a parent is False the child collapses to its baseline value, preventing
# duplicate grid combinations (e.g. iq_lookback=10 vs 20 is meaningless if use_iq_filter=False).
# To add a new dependent param: add an entry here and a range in optional_parameter_ranges.
DEFAULT_FEATURE_DEPENDENCIES: dict[str, tuple[str, ...]] = {
    "iq_lookback": ("use_iq_filter",),
    "iq_min_score": ("use_iq_filter",),
    "iq_slope_atr_scale": ("use_iq_filter",),
    "iq_er_weight": ("use_iq_filter",),
    "iq_slope_weight": ("use_iq_filter",),
    "iq_bias_weight": ("use_iq_filter",),
    "use_sq_boost": ("use_iq_filter",),           # sq_boost only has effect when IQ is on
    "sq_boost_weight": ("use_iq_filter", "use_sq_boost"),
    "sq_vol_lookback": ("use_iq_filter", "use_sq_boost"),
    "hammer_fib": ("enable_hammer",),
    "hammer_size": ("enable_hammer",),
    "ec_wick": ("enable_ec",),
    # RSI child params only matter when use_rsi_filter=True
    "rsi_period": ("use_rsi_filter",),
    "rsi_overbought": ("use_rsi_filter",),
    # ADX child params only matter when use_adx_filter=True
    "adx_period": ("use_adx_filter",),
    "adx_min_strength": ("use_adx_filter",),
    # Volume child params only matter when use_volume_filter=True
    "volume_filter_lookback": ("use_volume_filter",),
    "volume_filter_multiplier": ("use_volume_filter",),
}

# Default on/off grid for entry filters — each gets tested both True and False.
# Remove an entry to pin that filter at its StrategySettings baseline.
DEFAULT_BOOLEAN_FILTER_RANGES: dict[str, ParameterRange] = {
    "use_iq_filter": (False, True),
    "use_sq_boost": (False, True),
    "enable_ec": (False, True),
    "enable_bullish_engulfing": (False, True),
    "enable_shooting_star": (False, True),
    "enable_hammer": (False, True),
    "use_rsi_filter": (False, True),
    "use_adx_filter": (False, True),
    "use_volume_filter": (False, True),
}

# Default R:R values tested in every grid run.
# Add/remove values here to change the R:R search space globally.
DEFAULT_RISK_REWARD_RANGE: ParameterRange = (1.5, 2.0, 3.0, 5.0)

# Lookup table for turning exchange timeframe strings into clean file-safe labels.
# Add new timeframes here if the exchange uses a different string format.
_TIMEFRAME_LABELS: dict[str, str] = {
    "1m": "1M", "5m": "5M", "15m": "15M", "30m": "30M",
    "1h": "1H", "2h": "2H", "4h": "4H", "6h": "6H", "12h": "12H",
    "1d": "1D", "1day": "1DAY", "3d": "3D",
    "1w": "1W",
}


@dataclass(frozen=True)
class DatasetConfig:
    """Immutable descriptor for one pair/timeframe fetch request.

    Frozen so it can be used as a dict key and passed safely between functions.
    """

    source: str = "bybit"
    symbol: str = "BTCUSDT"
    market_type: str = "futures"
    timeframe: str = "1h"
    start_time: str = "2025-01-01 00:00:00"
    end_time: str | None = None  # None = fetch up to the latest available bar

    @property
    def condition_key(self) -> str:
        """Human-readable, file-safe label: BTC_1H, ETH_4H, SOL_1DAY etc.

        Used as the CSV filename stem and as the Streamlit dropdown label.
        Strip USDT/BUSD/PERP suffixes so labels are short and consistent.
        """
        tf_label = _TIMEFRAME_LABELS.get(self.timeframe.lower(), self.timeframe.upper())
        symbol_label = (
            self.symbol
            .replace("USDT", "")
            .replace("BUSD", "")
            .replace("PERP", "")
        )
        return f"{symbol_label}_{tf_label}"

    @property
    def dataset_key(self) -> str:
        """Verbose label used in log messages: 'BTCUSDT 1h'."""
        return f"{self.symbol} {self.timeframe}"


@dataclass
class RobustnessConfigV4:
    """All settings for one V4 robustness run.

    Normal usage: edit simple_config.py instead of this class directly.
    This class is the authoritative source of parameter ranges and build logic.
    """

    source: str = "bybit"
    market_type: str = "futures"
    symbols: list[str] = field(default_factory=lambda: ["BTCUSDT"])
    timeframes: list[str] = field(default_factory=lambda: ["1h"])
    start_time: str = "2025-01-01 00:00:00"
    end_time: str | None = None
    min_bars: int = 150  # skip a condition if it has fewer bars than this
    # Top N cutoff for counting consistency in the robustness summary.
    # A setup scores 1 point per condition where its Rank <= consistency_top_n.
    consistency_top_n: int = 20
    # Parallel workers for the backtest grid.
    #   1  = sequential (safe for debugging, default)
    #  -1  = use all available CPU cores
    #   N  = use exactly N worker processes
    n_jobs: int = 1
    # Default output dir; simple_config.py overrides this to sit inside the v4 folder.
    output_dir: Path = field(default_factory=lambda: Path("results"))
    baseline_settings: StrategySettings = field(default_factory=StrategySettings)
    boolean_filter_ranges: dict[str, ParameterRange] = field(
        default_factory=lambda: dict(DEFAULT_BOOLEAN_FILTER_RANGES)
    )
    risk_reward_range: ParameterRange = DEFAULT_RISK_REWARD_RANGE
    # Optional ranges are empty by default; add them via set_optional_parameter_range().
    optional_parameter_ranges: dict[str, ParameterRange] = field(default_factory=dict)
    feature_dependencies: dict[str, tuple[str, ...]] = field(
        default_factory=lambda: dict(DEFAULT_FEATURE_DEPENDENCIES)
    )

    def build_baseline_params(self) -> dict[str, object]:
        """Convert StrategySettings dataclass → flat dict for backtest.run(**params)."""
        return asdict(self.baseline_settings)

    def build_datasets(self) -> list[DatasetConfig]:
        """Build all conditions in sequential order: all timeframes per symbol, then next symbol.

        Order: BTC_1H, BTC_4H, ETH_1H, ETH_4H ... (symbols outer, timeframes inner).
        """
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
    def parameter_ranges(self) -> dict[str, ParameterRange]:
        """Merge all range dicts into one ordered dict used to build the grid.

        Order: boolean filters first, then risk_reward, then any optional params.
        """
        ranges: dict[str, ParameterRange] = {
            **self.boolean_filter_ranges,
            "risk_reward_multiplier": self.risk_reward_range,
        }
        ranges.update(self.optional_parameter_ranges)
        return ranges

    @property
    def parameter_names(self) -> tuple[str, ...]:
        """Ordered tuple of all parameter names — matches parameter_ranges key order."""
        return tuple(self.parameter_ranges.keys())

    # --- Mutation helpers (use these instead of editing dicts directly) ---

    def set_boolean_filter_range(self, name: str, *values: bool) -> None:
        """Pin a boolean filter to one value or test both. E.g. set_boolean_filter_range('enable_ec', True) to always enable."""
        if not values:
            raise ValueError(f"Boolean filter range for {name} cannot be empty")
        self.boolean_filter_ranges[name] = tuple(bool(v) for v in values)

    def set_risk_reward_range(self, *values: float) -> None:
        """Set the R:R values to test. E.g. set_risk_reward_range(1.5, 2.0, 3.0)."""
        if not values:
            raise ValueError("risk_reward_range cannot be empty")
        self.risk_reward_range = tuple(float(v) for v in values)

    def set_optional_parameter_range(self, name: str, *values: ParameterValue) -> None:
        """Add an internal parameter to the grid search.

        Child parameters (e.g. iq_lookback) are automatically ignored when their
        parent feature is off — see feature_dependencies for the dependency map.
        """
        if not values:
            raise ValueError(f"Parameter range for {name} cannot be empty")
        self.optional_parameter_ranges[name] = tuple(values)

    def remove_parameter(self, name: str) -> None:
        """Remove a parameter from the grid so it stays at its baseline default."""
        if name == "risk_reward_multiplier":
            raise ValueError("risk_reward_multiplier is part of the fixed V4 core grid")
        self.boolean_filter_ranges.pop(name, None)
        self.optional_parameter_ranges.pop(name, None)
