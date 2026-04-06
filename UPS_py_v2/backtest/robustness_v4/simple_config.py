from __future__ import annotations

from pathlib import Path

from .config import RobustnessConfigV4

# Results land inside this package folder, not the CWD, so they're always findable
# regardless of where the script is launched from.
_HERE = Path(__file__).parent
_RESULTS_DIR = _HERE / "results"


def build_simple_config() -> RobustnessConfigV4:
    """The only file you need to edit for a normal V4 run.

    Change symbols, timeframes, and parameter ranges here.
    The sequencer will process every symbol/timeframe combination in order,
    saving one CSV per condition to robustness_v4/results/.
    """

    # --- What to test ---
    # Each symbol × timeframe pair becomes one condition (one CSV file).
    # E.g. ["BTCUSDT", "ETHUSDT"] × ["1h", "4h"] → BTC_1H, BTC_4H, ETH_1H, ETH_4H
    symbols = ["BTCUSDT"]
    timeframes = ["1h", "4h"]

    config = RobustnessConfigV4(
        source="bybit",
        market_type="futures",
        symbols=symbols,
        timeframes=timeframes,
        start_time="2026-01-01 00:00:00",
        # end_time=None means fetch up to the latest available bar.
        min_bars=150,           # skip conditions with fewer bars (avoids meaningless stats)
        consistency_top_n=20,   # a setup "appears" in a condition if its Rank <= this value
        output_dir=_RESULTS_DIR,
    )

    # --- Core grid: which entry filters to test on/off ---
    # Each filter gets tested as True AND False — 2^n combinations before R:R expansion.
    # To pin a filter (always on/off), pass only one value: set_boolean_filter_range("enable_ec", True)
    config.boolean_filter_ranges = {
        "use_iq_filter": (False, True),
        "use_sq_boost": (False, True),
        "enable_ec": (False, True),
        "enable_bullish_engulfing": (False, True),
        "enable_shooting_star": (False, True),
        "enable_hammer": (False, True),
    }

    # --- Core grid: risk:reward values to test ---
    # More values = larger grid. Start with 3–4 well-spaced values.
    config.set_risk_reward_range(1.5, 2.0)

    # --- Optional: add internal parameter ranges ---
    # These only create new combinations when their parent filter is on (see feature_dependencies).
    # Uncomment to expand the grid for specific parameters.
    #
    # config.set_optional_parameter_range("ma_length", 20, 50, 100)
    # config.set_optional_parameter_range("iq_lookback", 10, 20, 30)
    # config.set_optional_parameter_range("iq_min_score", 0.45, 0.55, 0.65)

    return config
