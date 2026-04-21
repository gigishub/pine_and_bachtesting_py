"""Backtest configuration — data source, fees, and execution assumptions."""

from __future__ import annotations

import dataclasses
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, NamedTuple

from ..strategy.parameters import Parameters

# ---------------------------------------------------------------------------
# Audit helpers
# ---------------------------------------------------------------------------

# All Parameters boolean fields that must be explicitly declared in
# boolean_filter_ranges.  use_long / use_short are handled separately via
# enable_long / enable_short so they are excluded from this set.
_AUDITABLE_BOOL_FLAGS: tuple[str, ...] = tuple(
    f.name
    for f in dataclasses.fields(Parameters)
    if f.type == "bool" and f.name not in ("use_long", "use_short")
)


class AuditEntry(NamedTuple):
    """One row in the param_audit() table."""
    name: str
    status: str   # swept | pinned_on | pinned_off | implicit
    values: tuple  # effective range or single value

# ---------------------------------------------------------------------------
# Single-run config (used by backtesting.py runner)
# ---------------------------------------------------------------------------


@dataclass
class BacktestConfig:
    # --- Data ---
    symbol: str = "SOLUSDT"
    market_type: str = "linear"   # Bybit linear (USDT-margined perpetual)
    timeframe: str = "1h"
    # 6 months of data + 11 days warmup buffer (squeeze_history=240 bars ≈ 10 days)
    start_time: str = "2024-09-01 00:00:00"
    end_time: str | None = None    # None → current UTC time

    # --- Execution ---
    initial_cash: float = 10_000.0
    commission: float = 0.001      # 0.10% taker fee (Bybit standard)
    slippage: float = 0.0          # backtesting.py models slippage via commission

    # --- Display ---
    plot: bool = True


# ---------------------------------------------------------------------------
# Dataset descriptor (one symbol × timeframe fetch request)
# ---------------------------------------------------------------------------

_TF_LABELS: dict[str, str] = {
    "1m": "1M", "5m": "5M", "15m": "15M", "30m": "30M",
    "1h": "1H", "2h": "2H", "4h": "4H", "6h": "6H", "12h": "12H",
    "1d": "1D", "1w": "1W",
}


@dataclass(frozen=True)
class DatasetConfig:
    """Immutable descriptor for one pair/timeframe fetch request."""

    source: str = "bybit"
    symbol: str = "SOLUSDT"
    market_type: str = "linear"
    timeframe: str = "1h"
    start_time: str = "2024-09-01 00:00:00"
    end_time: str | None = None

    @property
    def condition_key(self) -> str:
        """Filesystem-safe key, e.g. 'SOLUSDT_1H'."""
        tf = _TF_LABELS.get(self.timeframe, self.timeframe.upper())
        return f"{self.symbol}_{tf}"

    @property
    def dataset_key(self) -> str:
        return self.condition_key


# ---------------------------------------------------------------------------
# Grid config (used by vectorbt pipeline / sequencer)
# ---------------------------------------------------------------------------

@dataclass
class MomentumGridConfig:
    """Configuration for the vectorbt combination grid-search.

    The grid is the Cartesian product of all boolean flag ranges plus any
    numeric parameter sweeps.  Each flag in boolean_filter_ranges maps to a
    tuple of values to test:
      - (False, True)  → sweep both off and on
      - (False,)       → always off (excluded from grid)
      - (True,)        → always on  (pinned, not swept)

    Invalid combos (any flag group entirely False) are filtered before running.

    Excluded options from the grid:
      - "relative_strength": requires a benchmark DataFrame (not in OHLCV)
      - "mvrv": requires Glassnode on-chain API
      - "cvd": requires tick-level trade data
    """

    # --- What to test ---
    source: str = "bybit"
    market_type: str = "linear"
    symbols: list[str] = field(default_factory=lambda: ["SOLUSDT"])
    timeframes: list[str] = field(default_factory=lambda: ["1h"])
    start_time: str = "2024-09-01 00:00:00"
    end_time: str | None = None

    # --- Grid: boolean flag ranges ---
    # Keys are Parameters field names; values are the tuple of bool values to test.
    boolean_filter_ranges: dict[str, tuple[bool, ...]] = field(
        default_factory=lambda: {
            # Long-side flags
            "use_adx":            (False, True),
            "use_ema_ribbon":     (False, True),
            "use_donchian":       (False, True),
            "use_volume_profile": (False, True),
            "use_cmf":            (False, True),
            "use_power_candle":   (False, True),
            "use_chandelier":     (False, True),
            "use_psar":           (False, True),
            "use_bbands":         (False, True),
            "use_trailing_stop":  (False, True),
            # VBT-native SL — off by default; set (False, True) to sweep
            "use_vbt_sl":         (False,),
            # Short-side flags (all off by default — enabled via enable_short)
            "use_ema_ribbon_short":     (False,),
            "use_donchian_short":       (False,),
            "use_volume_profile_short": (False,),
            "use_cmf_short":            (False,),
            "use_power_candle_short":   (False,),
            "use_chandelier_short":     (False,),
            "use_psar_short":           (False,),
            "use_bbands_short":         (False,),
            "use_trailing_stop_short":  (False,),
        }
    )

    # --- Grid: optional numeric sweeps (single value = pinned at baseline) ---
    adx_threshold_range:       tuple[float, ...] = (25.0,)
    chandelier_atr_mult_range: tuple[float, ...] = (3.0,)
    cmf_threshold_range:       tuple[float, ...] = (0.05,)
    trail_atr_mult_range:      tuple[float, ...] = (2.0,)
    # EMA ribbon periods — only matter when use_ema_ribbon / use_ema_ribbon_short is True;
    # deduplication in the grid builder collapses them to one combo when the flag is off.
    ema_fast_range: tuple[int, ...] = (20,)
    ema_mid_range:  tuple[int, ...] = (50,)
    ema_slow_range: tuple[int, ...] = (200,)

    # --- Grid: VBT-native SL numeric sweeps (only matter when use_vbt_sl=True) ---
    sl_n_atr_init_range:    tuple[float, ...] = (0.5,)
    sl_n_atr_trail_range:   tuple[float, ...] = (0.5,)
    sl_swing_lookback_range: tuple[int, ...]  = (10,)

    # --- Direction ---
    # enable_long/enable_short control whether long and short flags are swept.
    # Setting enable_short=True populates short boolean_filter_ranges with (False, True).
    enable_long:  bool = True
    enable_short: bool = False

    # --- Exclusive mode (long) ---
    # When True for a layer, only combos where exactly ONE flag in that layer is
    # True are tested.  Useful for isolating individual indicator performance
    # before running full combination grid.  All default False (no restriction).
    regime_exclusive:  bool = False
    setup_exclusive:   bool = False
    trigger_exclusive: bool = False
    exit_exclusive:    bool = False

    # --- Exclusive mode (short) ---
    short_regime_exclusive:  bool = False
    short_setup_exclusive:   bool = False
    short_trigger_exclusive: bool = False
    short_exit_exclusive:    bool = False

    # --- Execution ---
    initial_cash: float = 10_000.0
    fees: float = 0.001
    n_jobs: int = -1           # 1 = sequential; -1 = all cores
    min_bars: int = 500

    # --- Output ---
    output_dir: Path = field(default_factory=lambda: Path("adaptive_momentum_strategy/backtest/results/results_vbt"))
    consistency_top_n: int = 10
    save_trade_logs: bool = True
    trade_logs_top_n: int = 5

    def build_datasets(self) -> list[DatasetConfig]:
        """Return one DatasetConfig per symbol × timeframe combination."""
        return [
            DatasetConfig(
                source=self.source,
                symbol=symbol,
                market_type=self.market_type,
                timeframe=tf,
                start_time=self.start_time,
                end_time=self.end_time,
            )
            for symbol in self.symbols
            for tf in self.timeframes
        ]

    def build_baseline_params(self) -> dict[str, Any]:
        """Return a dict of all Parameters fields at their default values.

        Overrides use_long / use_short from enable_long / enable_short so the
        grid runner always uses the config-level direction setting.

        Single-value boolean pins (len(rng) == 1) are applied here so they
        override Parameters() defaults.  Without this a (False,) pin on a
        True-defaulting flag (e.g. use_donchian) would silently run as True
        because single-value ranges are excluded from parameter_names and
        therefore never written into grid candidates.
        """
        from dataclasses import asdict
        params = asdict(Parameters())
        params["use_long"]  = self.enable_long
        params["use_short"] = self.enable_short
        for name, rng in self.boolean_filter_ranges.items():
            if len(rng) == 1:
                params[name] = rng[0]
        return params

    def validate_coverage(self) -> None:
        """Raise ValueError if any auditable boolean flag is absent from boolean_filter_ranges.

        Auditable flags are all Parameters bool fields except use_long / use_short
        (those are controlled via enable_long / enable_short).

        Call this before starting a run to catch incomplete configs early rather
        than silently inheriting Parameters() defaults.
        """
        missing = [f for f in _AUDITABLE_BOOL_FLAGS if f not in self.boolean_filter_ranges]
        if missing:
            raise ValueError(
                "MomentumGridConfig is missing explicit declarations for the following "
                "boolean flags.  Add them to boolean_filter_ranges as a swept range "
                "(False, True) or a single-value pin (True,) / (False,).\n"
                "Missing: " + ", ".join(missing)
            )

    def param_audit(self) -> list[AuditEntry]:
        """Return a structured audit of every parameter's effective configuration.

        Boolean flags are categorised as:
          swept      — range has >1 value (e.g. (False, True))
          pinned_on  — single-value pin (True,)
          pinned_off — single-value pin (False,)
          implicit   — not declared; runs at Parameters() default (⚠ unintentional)

        Numeric sweep params are also included (swept vs pinned).

        Use this to inspect the effective config before a run, or to generate
        the run_manifest.txt record saved alongside CSVs.
        """
        defaults = {f.name: f.default for f in dataclasses.fields(Parameters)}
        entries: list[AuditEntry] = []

        for name in _AUDITABLE_BOOL_FLAGS:
            rng = self.boolean_filter_ranges.get(name)
            if rng is None:
                status = "implicit"
                values = (defaults[name],)
            elif len(rng) > 1:
                status = "swept"
                values = rng
            elif rng[0] is True:
                status = "pinned_on"
                values = rng
            else:
                status = "pinned_off"
                values = rng
            entries.append(AuditEntry(name, status, values))

        _numeric = [
            ("adx_threshold",       self.adx_threshold_range),
            ("chandelier_atr_mult", self.chandelier_atr_mult_range),
            ("cmf_threshold",       self.cmf_threshold_range),
            ("trail_atr_mult",      self.trail_atr_mult_range),
            ("ema_fast",            self.ema_fast_range),
            ("ema_mid",             self.ema_mid_range),
            ("ema_slow",            self.ema_slow_range),
            ("sl_n_atr_init",       self.sl_n_atr_init_range),
            ("sl_n_atr_trail",      self.sl_n_atr_trail_range),
            ("sl_swing_lookback",   self.sl_swing_lookback_range),
        ]
        for name, rng in _numeric:
            status = "swept" if len(rng) > 1 else "pinned"
            entries.append(AuditEntry(name, status, rng))

        return entries

    @property
    def parameter_names(self) -> tuple[str, ...]:
        """Names of parameters being swept in the grid (in grid-product order).

        Includes boolean flags whose range has more than one value, followed
        by any numeric sweeps with more than one value.
        """
        names: list[str] = [
            name
            for name, rng in self.boolean_filter_ranges.items()
            if len(rng) > 1
        ]
        if len(self.adx_threshold_range) > 1:
            names.append("adx_threshold")
        if len(self.chandelier_atr_mult_range) > 1:
            names.append("chandelier_atr_mult")
        if len(self.cmf_threshold_range) > 1:
            names.append("cmf_threshold")
        if len(self.trail_atr_mult_range) > 1:
            names.append("trail_atr_mult")
        if len(self.ema_fast_range) > 1:
            names.append("ema_fast")
        if len(self.ema_mid_range) > 1:
            names.append("ema_mid")
        if len(self.ema_slow_range) > 1:
            names.append("ema_slow")
        if len(self.sl_n_atr_init_range) > 1:
            names.append("sl_n_atr_init")
        if len(self.sl_n_atr_trail_range) > 1:
            names.append("sl_n_atr_trail")
        if len(self.sl_swing_lookback_range) > 1:
            names.append("sl_swing_lookback")
        return tuple(names)

    @property
    def parameter_ranges(self) -> dict[str, tuple]:
        """Values to test for each parameter in parameter_names."""
        ranges: dict[str, tuple] = {
            name: rng
            for name, rng in self.boolean_filter_ranges.items()
            if len(rng) > 1
        }
        if len(self.adx_threshold_range) > 1:
            ranges["adx_threshold"] = self.adx_threshold_range
        if len(self.chandelier_atr_mult_range) > 1:
            ranges["chandelier_atr_mult"] = self.chandelier_atr_mult_range
        if len(self.cmf_threshold_range) > 1:
            ranges["cmf_threshold"] = self.cmf_threshold_range
        if len(self.trail_atr_mult_range) > 1:
            ranges["trail_atr_mult"] = self.trail_atr_mult_range
        if len(self.ema_fast_range) > 1:
            ranges["ema_fast"] = self.ema_fast_range
        if len(self.ema_mid_range) > 1:
            ranges["ema_mid"] = self.ema_mid_range
        if len(self.ema_slow_range) > 1:
            ranges["ema_slow"] = self.ema_slow_range
        if len(self.sl_n_atr_init_range) > 1:
            ranges["sl_n_atr_init"] = self.sl_n_atr_init_range
        if len(self.sl_n_atr_trail_range) > 1:
            ranges["sl_n_atr_trail"] = self.sl_n_atr_trail_range
        if len(self.sl_swing_lookback_range) > 1:
            ranges["sl_swing_lookback"] = self.sl_swing_lookback_range
        return ranges

    @property
    def feature_dependencies(self) -> dict[str, tuple[str, ...]]:
        """Numeric params that are irrelevant when their parent flag is False.

        Prevents duplicate runs: e.g. adx_threshold=20 vs 25 are identical
        when use_adx=False, so they collapse to the same deduped combo.
        """
        return {
            "adx_threshold":        ("use_adx",),
            "cmf_threshold":        ("use_cmf",),
            "chandelier_atr_mult":  ("use_chandelier",),
            "trail_atr_mult":       ("use_trailing_stop",),
            # EMA periods collapse to baseline when use_ema_ribbon is off.
            # In long-only runs this is exact; in combined runs the short EMA
            # ribbon may still be active — an acceptable minor under-deduplication.
            "ema_fast":             ("use_ema_ribbon",),
            "ema_mid":              ("use_ema_ribbon",),
            "ema_slow":             ("use_ema_ribbon",),
            # SL numeric params are irrelevant when use_vbt_sl=False.
            "sl_n_atr_init":        ("use_vbt_sl",),
            "sl_n_atr_trail":       ("use_vbt_sl",),
            "sl_swing_lookback":    ("use_vbt_sl",),
        }
