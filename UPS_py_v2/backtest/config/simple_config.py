from __future__ import annotations

from datetime import datetime
from pathlib import Path

from .default_config import RobustnessConfigV4

# Results root lives at backtest/results/ — one subdirectory per engine.
_HERE = Path(__file__).parent
_RESULTS_ROOT = _HERE.parent / "results"


def build_output_dir(engine: str, label: str = "UPS", suffix: str = "") -> Path:
    """Create (or resume) a timestamped run directory for the given engine.

    Format: YYYY-MM-DD_HHMM_LABEL[_SUFFIX]
    Example: 2026-04-06_1210_UPS  or  2026-04-06_1530_UPS_adx_test

    Year-first ordering means directories sort chronologically in any file
    explorer or shell glob — the last entry alphabetically is always the most
    recent run.

    On first run:  creates a new folder and writes its name to a per-engine
                   .current_run marker so checkpoint resume works on restart.
    On restart:    reads the marker and resumes the same folder, so the
                   sequencer's CSV-exists check skips already-finished conditions.

    To force a brand-new run, delete the .current_run marker file or change
    the label/suffix.

    Args:
        engine: Engine identifier used as the results subdirectory name,
                e.g. "vbt" → results/results_vbt/  or  "backtesting_py".
        label:  Short strategy name appended to the folder, e.g. "UPS".
        suffix: Optional extra tag, e.g. "adx_test".  Omit for standard runs.

    Returns:
        Path to the run directory (created if it does not exist).
    """
    engine_dir = _RESULTS_ROOT / f"results_{engine}"
    engine_dir.mkdir(parents=True, exist_ok=True)

    marker = engine_dir / ".current_run"
    if marker.exists():
        existing = marker.read_text().strip()
        candidate = engine_dir / existing
        if candidate.exists():
            return candidate
        # Marker points to a deleted folder — start fresh.

    now = datetime.now()
    folder_name = now.strftime("%Y-%m-%d_%H%M") + f"_{label}"
    if suffix:
        folder_name += f"_{suffix}"
    output_dir = engine_dir / folder_name
    output_dir.mkdir(parents=True, exist_ok=True)
    marker.write_text(folder_name)
    return output_dir


def build_simple_config(output_dir: Path | None = None) -> RobustnessConfigV4:
    """The only file you need to edit for a normal run.

    Change symbols, timeframes, and parameter ranges here.
    The sequencer processes every symbol × timeframe combination in order,
    saving one CSV per condition to a timestamped subdirectory.

    output_dir is provided by each engine's run.py via build_output_dir().
    If omitted (e.g. in tests), a temporary placeholder path is used.

    If a CSV already exists in the output directory, that condition is skipped
    (checkpoint resume).
    """
    # --- What to test ---
    # Each symbol × timeframe pair becomes one condition (one CSV file).
    # E.g. ["BTCUSDT", "ETHUSDT"] × ["1h", "4h"] → BTC_1H, BTC_4H, ETH_1H, ETH_4H
    # Top 10 pairs by market cap on Bybit (excluding stablecoins):
    symbols = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "BNBUSDT", "SOLUSDT",
               "TRXUSDT", "DOGEUSDT", "ADAUSDT", "AVAXUSDT", "LINKUSDT"]
    timeframes = ["1h", "4h"]
    # symbols = ["BTCUSDT"]
    # timeframes = ["1h"]

    config = RobustnessConfigV4(
        source="bybit",
        market_type="futures",
        symbols=symbols,
        timeframes=timeframes,
        start_time="2023-05-01 00:00:00",
        end_time="2025-10-31 23:59:59",
        # start_time="2021-01-01 00:00:00",
        # end_time=None,
        min_bars=150,           # skip conditions with fewer bars (avoids meaningless stats)
        consistency_top_n=20,   # a setup "appears" in a condition if its Rank <= this value
        output_dir=output_dir or Path("/tmp/ups_backtest_placeholder"),
        # n_jobs=1 is sequential (safe for debugging).
        # Set n_jobs=-1 to use all CPU cores, or n_jobs=4 for a fixed count.
        n_jobs=-1,
    )

    # --- Core grid: which entry filters to test on/off ---
    # Each filter gets tested as True AND False — 2^n combinations before R:R expansion.
    # To pin a filter (always on/off), pass only one value: (True,) or (False,)
    config.boolean_filter_ranges = {
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

    # --- Core grid: risk:reward values to test ---
    # More values = larger grid. Start with 3–4 well-spaced values.
    config.set_risk_reward_range(1.0, 1.8, 2.7)

    # --- Optional: sweep numeric parameters ---
    # Uncomment to expand the search space for specific parameters.
    #
    # config.set_optional_parameter_range("rsi_period", 10, 14, 20)
    # config.set_optional_parameter_range("rsi_overbought", 65.0, 70.0, 75.0)
    # config.set_optional_parameter_range("adx_period", 10, 14, 20)
    # config.set_optional_parameter_range("adx_min_strength", 15.0, 20.0, 25.0)
    # config.set_optional_parameter_range("volume_filter_multiplier", 1.0, 1.2, 1.5)
    #
    # config.set_optional_parameter_range("ma_length", 20, 50, 100)
    # config.set_optional_parameter_range("iq_lookback", 10, 20, 30)
    # config.set_optional_parameter_range("iq_min_score", 0.45, 0.55, 0.65)

    return config
