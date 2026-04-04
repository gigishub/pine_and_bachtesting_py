from __future__ import annotations

from .config import OptimizationConfigV3


def build_simple_config() -> OptimizationConfigV3:
    """Edit this file for the normal v3 workflow instead of passing CLI flags."""

    symbols = ["BTCUSDT"]
    timeframes = ["1day"]

    config = OptimizationConfigV3(
        start_time="2025-01-01 00:00:00",
        min_bars=150,
        top_n=10,
    )
    config.set_matrix_scope(symbols=symbols, timeframes=timeframes)

    # Step 1 core grid: True/False entry filters.
    config.boolean_filter_ranges = {
        "use_iq_filter": (False, True),
        "use_sq_boost": (False, True),
        "enable_ec": (False, True),
        "enable_bullish_engulfing": (False, True),
        "enable_shooting_star": (False, True),
        "enable_hammer": (False, True),
    }

    # Step 1 core grid: four easy-to-edit risk:reward values.
    config.set_risk_reward_range(1, 2.0)

    # Optional ranges are empty by default.
    # Add them only when you want that filter's internal values optimized.
    # Examples:
    config.set_optional_parameter_range("ma_length", 20, 50, 100)
    # config.set_optional_parameter_range("iq_lookback", 10, 20, 30)

    return config