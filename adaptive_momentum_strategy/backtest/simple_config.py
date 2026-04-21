"""Simple config — the ONLY file you need to edit for a grid-search run.

No algorithm code here.  Toggle flags, set numeric sweeps, and tune execution
settings, then run:

    source .venv/bin/activate
    python -m adaptive_momentum_strategy.backtest.vectorbt.run

For a single backtesting.py run (with plot):
    python -m adaptive_momentum_strategy.backtest.backtesting_py.run

Results are saved to a timestamped subdirectory inside:
    adaptive_momentum_strategy/backtest/results/results_vbt/

Checkpoint resume: if the run is interrupted, re-running picks up from the
last completed condition (CSV-exists check).  Delete the .current_run marker
file in the results folder to force a brand-new run.

Boolean flag semantics
----------------------
  True  -> (False, True)  -- sweep: both off and on are tested
  None  -> (True,)        -- pin on: always active, not swept
  False -> (False,)       -- pin off: always inactive, not swept

At least one flag per active direction's layer group must be True.

Numeric sweep semantics
-----------------------
  (25.0,)          -- single value → pinned at that value
  (20.0, 25.0, 30.0) -- multiple values → swept across the grid
"""

from __future__ import annotations

from pathlib import Path

from .config import MomentumGridConfig


def build_simple_config(output_dir: Path | None = None) -> MomentumGridConfig:
    """Edit this function to configure a grid-search run.

    Each symbol x timeframe pair becomes one condition (one CSV file).
    The grid is the Cartesian product of all enabled flag ranges plus any
    numeric parameter sweeps you uncomment below.

    There are separate long and short trade configurations so you can test
    each direction independently for robustness.

    Each indicator or signal has its own flag, and flags can be combined
    or isolated through the "exclusive" settings below.

    A flag set to True is swept (tested both off and on).
    A flag set to False is excluded (always off, not tested).
    """

    # ------------------------------------------------------------------ #
    # What to test
    # ------------------------------------------------------------------ #
    symbols = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "BNBUSDT", "SOLUSDT",
               "TRXUSDT", "DOGEUSDT", "ADAUSDT", "AVAXUSDT", "LINKUSDT"]
    timeframes = ["1h","4H","1D"]
    # Expand to more pairs / timeframes for robustness:
    # symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "AVAXUSDT"]
    # timeframes = ["1h", "4h"]

    start_time = "2022-09-01 00:00:00"
    end_time = "2025-09-01 00:00:00" # None -> fetch up to current UTC time

    # ------------------------------------------------------------------ #
    # Direction toggles
    # ------------------------------------------------------------------ #
    enable_long  = True   # Test long-side trades
    enable_short = False  # Test short-side trades

    # ------------------------------------------------------------------ #
    # Long regime layer  (at least one must be True when enable_long=True)
    # ------------------------------------------------------------------ #
    # Long and short trade logic are kept separated so each direction can be
    # tested independently. Enable long-only or short-only runs by toggling
    # enable_long / enable_short.
    use_adx_regime = True   # Option A -- ADX(14) > threshold
    use_ema_ribbon = True   # Option C -- EMA(20) > EMA(50) > EMA(200)

    regime_exclusive = True  # True → only one regime flag per combo (isolation testing)

    # ------------------------------------------------------------------ #
    # Long setup layer   (at least one must be True when enable_long=True)
    # ------------------------------------------------------------------ #
    use_donchian_setup = True   # Option A -- Donchian channel breakout + squeeze
    use_volume_profile = True   # Option B -- Rolling VAH breakout
    # use_relative_strength = False  # Option C -- excluded: requires benchmark data

    setup_exclusive = True   # True → only one setup flag per combo

    # ------------------------------------------------------------------ #
    # Long trigger layer (at least one must be True when enable_long=True)
    # ------------------------------------------------------------------ #
    use_cmf_trigger  = True   # Option A -- CMF(20) > threshold
    use_power_candle = True   # Option C -- Close > High(N) + high volume

    trigger_exclusive = True    # True → only one trigger flag per combo

    # ------------------------------------------------------------------ #
    # Long exit layer    (at least one must be True when enable_long=True)
    # ------------------------------------------------------------------ #
    use_chandelier_exit  = True   # Option A -- Chandelier ATR trailing stop (ratcheted)
    use_psar_exit        = True   # Option B -- Parabolic SAR (self-managing)
    use_bbands_exit      = True   # Option C -- Bollinger Band upper (self-managing)
    use_trailing_stop    = True  # Option D -- btc_momentum-style: rolling_max(low,N)-ATR*mult

    exit_exclusive = False   # True → only one exit flag per combo

    # ------------------------------------------------------------------ #
    # Short regime layer  (at least one must be True when enable_short=True)
    # ADX (use_adx_regime above) is shared — non-directional, reused for shorts.
    # Short direction flags are isolated from long-side flags to support robust
    # directional testing.
    # ------------------------------------------------------------------ #
    use_ema_ribbon_short = True   # EMA(20) < EMA(50) < EMA(200) -- bearish stacking

    short_regime_exclusive = True   # True → only one short regime flag per combo

    # ------------------------------------------------------------------ #
    # Short setup layer   (at least one must be True when enable_short=True)
    # ------------------------------------------------------------------ #
    use_donchian_short       = True   # Close < Donchian lower band (breakdown)
    use_volume_profile_short = True  # Close below Value Area Low

    short_setup_exclusive = True

    # ------------------------------------------------------------------ #
    # Short trigger layer (at least one must be True when enable_short=True)
    # ------------------------------------------------------------------ #
    use_cmf_short          = True   # CMF < -threshold (distribution confirmed)
    use_power_candle_short = True  # Bearish power candle

    short_trigger_exclusive = True

    # ------------------------------------------------------------------ #
    # Short exit layer    (at least one must be True when enable_short=True)
    # ------------------------------------------------------------------ #
    use_chandelier_short = True   # lowest_low(N) + ATR*mult (ratcheted downward)
    use_psar_short       = True  # Parabolic SAR short
    use_bbands_short     = True  # BB lower band re-entry
    use_trailing_stop_short = True  # rolling_min(high,N)+ATR*mult (ratcheted downward)

    short_exit_exclusive = True

    # ------------------------------------------------------------------ #
    # Build boolean_filter_ranges
    # True  -> (False, True): flag is swept in the grid
    # False -> (False,): flag is always off, excluded from grid
    # Each indicator or rule has its own flag so you can enable/disable
    # individual signals independently.
    # Short flags are only swept when enable_short=True; long flags are
    # separate and will not be included in short-only runs when enable_short
    # is False.
    # ------------------------------------------------------------------ #
    def _flag_range(flag_val: bool | None, direction_enabled: bool) -> tuple[bool, ...]:
        """Convert a flag setting to a boolean range tuple.

        flag_val:
            True  → sweep (False, True)
            None  → pin on (True,)
            False → pin off (False,)
        direction_enabled:
            When False the flag is always pinned off regardless of flag_val.
        """
        if not direction_enabled:
            return (False,)
        if flag_val is True:
            return (False, True)
        if flag_val is None:
            return (True,)
        return (False,)

    boolean_filter_ranges = {
        # Long flags
        "use_adx":            _flag_range(use_adx_regime, enable_long),
        "use_ema_ribbon":     _flag_range(use_ema_ribbon, enable_long),
        "use_donchian":       _flag_range(use_donchian_setup, enable_long),
        "use_volume_profile": _flag_range(use_volume_profile, enable_long),
        "use_cmf":            _flag_range(use_cmf_trigger, enable_long),
        "use_power_candle":   _flag_range(use_power_candle, enable_long),
        "use_chandelier":     _flag_range(use_chandelier_exit, enable_long),
        "use_psar":           _flag_range(use_psar_exit, enable_long),
        "use_bbands":         _flag_range(use_bbands_exit, enable_long),
        "use_trailing_stop":  _flag_range(use_trailing_stop, enable_long),
        # Short flags (only swept when enable_short=True)
        "use_ema_ribbon_short":     _flag_range(use_ema_ribbon_short, enable_short),
        "use_donchian_short":       _flag_range(use_donchian_short, enable_short),
        "use_volume_profile_short": _flag_range(use_volume_profile_short, enable_short),
        "use_cmf_short":            _flag_range(use_cmf_short, enable_short),
        "use_power_candle_short":   _flag_range(use_power_candle_short, enable_short),
        "use_chandelier_short":     _flag_range(use_chandelier_short, enable_short),
        "use_psar_short":           _flag_range(use_psar_short, enable_short),
        "use_bbands_short":         _flag_range(use_bbands_short, enable_short),
        "use_trailing_stop_short":  _flag_range(use_trailing_stop_short, enable_short),
    }

    # ------------------------------------------------------------------ #
    # Numeric parameter sweeps
    # Single value = pinned; multiple values = swept in the grid.
    # Each extra value multiplies the grid size.
    # ------------------------------------------------------------------ #

    # ADX threshold — only active in combos where use_adx = True
    adx_threshold: tuple[float, ...] = (25.0,)
    # adx_threshold = (20.0, 25.0, 30.0)

    # CMF threshold — only active in combos where use_cmf = True
    cmf_threshold: tuple[float, ...] = (0.05,)
    # cmf_threshold = (0.0, 0.05, 0.10)

    # Chandelier ATR multiplier — only active where use_chandelier = True
    chandelier_atr_mult: tuple[float, ...] = (3.0,)
    # chandelier_atr_mult = (2.5, 3.0, 3.5)

    # Trailing stop ATR multiplier — only active where use_trailing_stop = True
    trail_atr_mult: tuple[float, ...] = (2.0,)
    # trail_atr_mult = (1.5, 2.0, 2.5)

    # EMA ribbon periods — only active in combos where use_ema_ribbon = True
    ema_fast: tuple[int, ...] = (20,)
    # ema_fast = (10, 20)
    ema_mid: tuple[int, ...] = (50,)
    # ema_mid = (50,)
    ema_slow: tuple[int, ...] = (200,)
    # ema_slow = (100, 150, 200)

    # ------------------------------------------------------------------ #
    # Execution & output
    # ------------------------------------------------------------------ #
    initial_cash: float = 10_000.0
    commission: float = 0.001      # 0.10% taker fee (Bybit standard)
    # n_jobs: 1 = sequential (safe for debugging); -1 = all CPU cores
    n_jobs: int = -1
    min_bars: int = 500            # skip conditions with fewer bars than this

    consistency_top_n: int = 10   # top-N combos shown in cross-condition summary
    save_trade_logs: bool = True   # write per-combo trade log CSVs
    trade_logs_top_n: int = 5     # number of top combos to save trade logs for

    # slippage and plot are single-run settings — see backtesting_py/runner.py
    # (BacktestConfig.slippage, BacktestConfig.plot)

    config = MomentumGridConfig(
        source="bybit",
        market_type="linear",
        symbols=symbols,
        timeframes=timeframes,
        start_time=start_time,
        end_time=end_time,
        boolean_filter_ranges=boolean_filter_ranges,
        enable_long=enable_long,
        enable_short=enable_short,
        regime_exclusive=regime_exclusive,
        setup_exclusive=setup_exclusive,
        trigger_exclusive=trigger_exclusive,
        exit_exclusive=exit_exclusive,
        short_regime_exclusive=short_regime_exclusive,
        short_setup_exclusive=short_setup_exclusive,
        short_trigger_exclusive=short_trigger_exclusive,
        short_exit_exclusive=short_exit_exclusive,
        adx_threshold_range=adx_threshold,
        cmf_threshold_range=cmf_threshold,
        chandelier_atr_mult_range=chandelier_atr_mult,
        trail_atr_mult_range=trail_atr_mult,
        ema_fast_range=ema_fast,
        ema_mid_range=ema_mid,
        ema_slow_range=ema_slow,
        initial_cash=initial_cash,
        fees=commission,
        n_jobs=n_jobs,
        output_dir=output_dir or Path("/tmp/ams_backtest_placeholder"),
        min_bars=min_bars,
        consistency_top_n=consistency_top_n,
        save_trade_logs=save_trade_logs,
        trade_logs_top_n=trade_logs_top_n,
    )

    return config
