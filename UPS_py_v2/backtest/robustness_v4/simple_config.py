from __future__ import annotations

from datetime import datetime
from pathlib import Path

from .config import RobustnessConfigV4

# Results land inside this package folder, not the CWD, so they're always findable
# regardless of where the script is launched from.
_HERE = Path(__file__).parent
_RESULTS_DIR = _HERE / "results"


def build_timestamped_output_dir(label: str = "UPS") -> Path:
    """Create (or resume) a timestamped run directory in results/.

    Format: HHmm-DD-MM-YYYY_LABEL (e.g., 0900-21-12-2025_UPS)

    On first run:  creates a new folder and writes its name to results/.current_run.
    On restart:    reads results/.current_run and resumes into the same folder,
                   so checkpoint skip logic in the sequencer finds existing CSVs.

    To force a brand-new run (discard the checkpoint), delete results/.current_run
    or call this with a different label.

    Args:
        label: Short name for the run (e.g., "UPS", "v2", "test").

    Returns:
        Path to the run directory.
    """
    marker = _RESULTS_DIR / ".current_run"
    _RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    if marker.exists():
        existing = marker.read_text().strip()
        candidate = _RESULTS_DIR / existing
        if candidate.exists():
            return candidate
        # Marker points to a deleted folder — start fresh.

    now = datetime.now()
    folder_name = now.strftime("%H%M-%d-%m-%Y") + f"_{label}"
    output_dir = _RESULTS_DIR / folder_name
    output_dir.mkdir(parents=True, exist_ok=True)
    marker.write_text(folder_name)
    return output_dir


def build_simple_config() -> RobustnessConfigV4:
    """The only file you need to edit for a normal V4 run.

    Change symbols, timeframes, and parameter ranges here.
    The sequencer will process every symbol/timeframe combination in order,
    saving one CSV per condition to a timestamped subdirectory in results/.
    
    If a CSV already exists in the output directory, that condition is skipped
    (checkpoint resume).
    """
    
    # --- Output directory with timestamp ---
    # Each run gets its own folder: 0900-21-12-2025_UPS, 1530-22-12-2025_UPS, etc.
    # To use a different label or disable timestamping, edit build_timestamped_output_dir() call.
    output_dir = build_timestamped_output_dir(label="UPS")

    # --- What to test ---
    # Each symbol × timeframe pair becomes one condition (one CSV file).
    # E.g. ["BTCUSDT", "ETHUSDT"] × ["1h", "4h"] → BTC_1H, BTC_4H, ETH_1H, ETH_4H
    # Top 10 pairs by market cap on Bybit (excluding stablecoins)
    symbols = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "BNBUSDT", "SOLUSDT", 
               "TRXUSDT", "DOGEUSDT", "ADAUSDT", "AVAXUSDT", "LINKUSDT"]
    timeframes = ["1h", "4h"]

    config = RobustnessConfigV4(
        source="bybit",
        market_type="futures",
        symbols=symbols,
        timeframes=timeframes,
        start_time="2020-11-01 00:00:00",
        end_time="2025-12-31 23:59:59",
        min_bars=150,           # skip conditions with fewer bars (avoids meaningless stats)
        consistency_top_n=20,   # a setup "appears" in a condition if its Rank <= this value
        output_dir=output_dir,
        # n_jobs=1 is sequential (safe for debugging).
        # Set n_jobs=-1 to use all CPU cores, or n_jobs=4 for a fixed count.
        n_jobs=-1,
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
        # New orthogonal filters — all start False/True so the grid tests their value
        "use_rsi_filter": (False, True),
        "use_adx_filter": (False, True),
        "use_volume_filter": (False, True),
    }

    # --- Core grid: risk:reward values to test ---
    # More values = larger grid. Start with 3–4 well-spaced values.
    config.set_risk_reward_range(1, 1.5)

    # --- Optional: sweep numeric parameters for the new filters ---
    # These only create new combinations when their parent filter is on (see feature_dependencies).
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
