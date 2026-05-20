"""Bear Strategy — AMS-style grid backtest configuration.

Models BearGridConfig after adaptive_momentum_strategy/backtest/config.py
(MomentumGridConfig).  Key differences:
  - Only trigger + exit flags are in boolean_filter_ranges.
    Regime (RSI bear zone + funding bull guard) is always active; only its
    numeric params can be swept.
  - Data is multi-source: each symbol needs 1h + 1d + funding loaded separately.
  - Numeric sweeps cover regime params, trigger params, exit params, and
    stop/target ATR multiples.
"""

from __future__ import annotations

import dataclasses
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, NamedTuple

from bear_strategy.strategy.parameters import Parameters

# ---------------------------------------------------------------------------
# Audit helpers
# ---------------------------------------------------------------------------

# Trigger + exit flags that must be explicitly declared in boolean_filter_ranges.
# Regime flags are always active (no toggle), so they are excluded.
# use_exit_rsi is a legacy field and is excluded.
_AUDITABLE_BEAR_FLAGS: tuple[str, ...] = (
    "use_ema_200_regime",
    "use_vp_trigger",
    "use_fixed_tp",
    "use_rsi_exit",
    "use_macd_exit",
    "use_rsi_oversold_exit",
    "use_ema_reclaim_exit",
    "use_funding_exit",
    "use_ema_above_exit",
    "use_vwap_exit",
    "use_vwma_exit",
    "use_engulfing_exit",
    "use_hammer_exit",
    "use_bb_mean_reversion_exit",
    "use_atr_reversal_exit",
    "use_vbt_sl",
    "use_vbt_sl_trail",
)


class AuditEntry(NamedTuple):
    """One row in the param_audit() table."""
    name: str
    status: str   # swept | pinned_on | pinned_off | pinned | implicit
    values: tuple


# ---------------------------------------------------------------------------
# Grid config
# ---------------------------------------------------------------------------

@dataclass
class BearGridConfig:
    """Configuration for the Bear Strategy AMS-style vectorbt grid search.

    The grid is the Cartesian product of all boolean flag ranges (trigger +
    exit only) plus any numeric parameter sweeps.  Each flag in
    boolean_filter_ranges maps to a tuple of values to test:
      - (False, True)  → sweep both off and on
      - (False,)       → always off (excluded from grid)
      - (True,)        → always on  (pinned, not swept)

    Regime (RSI bear zone + funding bull guard) is structural — it is always
    active; only its numeric params can be swept.

    Invalid combos (all triggers False OR all exits False) are filtered
    before running.
    """

    # --- Data ---
    symbols: list[str] = field(default_factory=lambda: ["BTCUSDT", "ETHUSDT", "SOLUSDT"])
    start_date: str = "2021-01-01"
    end_date: str = "2023-11-01"
    data_dir: str = "crypto_data/data"

    # --- Grid: boolean flag ranges (trigger + exit only; regime is always active) ---
    boolean_filter_ranges: dict[str, tuple[bool, ...]] = field(
        default_factory=lambda: {
            # Trigger
            "use_vp_trigger":        (True,),      # pinned on — only trigger currently
            # Exit
            "use_fixed_tp":          (False, True),
            "use_rsi_exit":          (False, True),
            "use_macd_exit":         (False, True),
            "use_rsi_oversold_exit": (False, True),
            "use_ema_reclaim_exit":  (False, True),
            "use_funding_exit":      (False, True),
            # New indicator exits (off by default in the base grid)
            "use_ema_above_exit":    (False,),
            "use_vwap_exit":         (False,),
            "use_vwma_exit":         (False,),
            "use_engulfing_exit":    (False,),
            "use_hammer_exit":       (False,),
            "use_bb_mean_reversion_exit": (False,),
            "use_atr_reversal_exit": (False,),
            # VBT-native trailing stop (off by default in the base grid)
            "use_vbt_sl":            (False,),
            "use_vbt_sl_trail":      (False,),
        }
    )

    # --- Grid: numeric sweep ranges (single value = pinned at baseline) ---

    # Stop / target
    sl_mult_range: tuple[float, ...] = (2.0,)
    tp_mult_range: tuple[float, ...] = (3.0,)
    atr_period_range: tuple[int, ...] = (7,)

    # Exit indicator numeric params
    exit_rsi_level_range:      tuple[float, ...] = (50.0,)
    rsi_oversold_level_range:  tuple[float, ...] = (30.0,)
    exit_ema_period_range:     tuple[int, ...]   = (21,)
    macd_fast_range:           tuple[int, ...]   = (12,)
    macd_slow_range:           tuple[int, ...]   = (26,)

    # Trigger numeric params
    vp_price_bins_range:        tuple[int, ...] = (50,)

    # Regime numeric params
    rsi_lower_range:            tuple[float, ...] = (30.0,)
    rsi_upper_range:            tuple[float, ...] = (50.0,)
    funding_threshold_range:    tuple[float, ...] = (0.0,)

    # VBT trailing stop params (active only when use_vbt_sl=True)
    sl_n_atr_init_range:      tuple[float, ...] = (0.5,)
    sl_n_atr_trail_range:     tuple[float, ...] = (0.5,)
    sl_swing_lookback_range:  tuple[int, ...]   = (10,)

    # New exit indicator numeric params
    ema_above_period_range:   tuple[int, ...]   = (20,)
    vwap_anchor_hours_range:  tuple[int, ...]   = (24,)
    vwma_period_range:        tuple[int, ...]   = (20,)
    engulfing_ratio_range:    tuple[float, ...] = (1.0,)
    hammer_wick_ratio_range:  tuple[float, ...] = (2.0,)
    bb_period_range:          tuple[int, ...]   = (20,)
    bb_num_std_range:         tuple[float, ...] = (2.0,)
    atr_reversal_mult_range:  tuple[float, ...] = (1.5,)
    atr_reversal_period_range: tuple[int, ...] = (14,)

    # Entry throttle: regime-aware starting position (1 = 1st trigger, 2 = 2nd, …)
    entry_regime_offset_range: tuple[int, ...] = (2,)

    # --- Exclusive mode ---
    trigger_exclusive: bool = False   # test each trigger alone
    exit_exclusive:    bool = False   # test each exit alone

    # --- Execution ---
    initial_cash: float = 10_000.0
    fees: float = 0.0008
    n_jobs: int = 1       # 1 = sequential by default (multi-source data setup)
    min_bars: int = 500

    # --- Output ---
    output_dir: Path = field(
        default_factory=lambda: Path("bear_strategy/backtest/vectorbt/results")
    )
    consistency_top_n: int = 10
    save_trade_logs: bool = True
    trade_logs_top_n: int = 5

    # ------------------------------------------------------------------
    # Internal mapping: config range field → Parameters field name
    # ------------------------------------------------------------------
    _NUMERIC_MAP: tuple[tuple[str, str], ...] = field(
        default=None,  # type: ignore[assignment]
        init=False,
        repr=False,
        compare=False,
    )

    def __post_init__(self) -> None:
        # Freeze the mapping as a class-level constant (set once after init)
        object.__setattr__(self, "_NUMERIC_MAP", (
            ("sl_mult_range",             "stop_atr_mult"),
            ("tp_mult_range",             "target_atr_mult"),
            ("atr_period_range",          "atr_period"),
            ("vp_price_bins_range",       "vp_price_bins"),
            ("exit_rsi_level_range",      "exit_rsi_level"),
            ("rsi_oversold_level_range",  "rsi_oversold_level"),
            ("exit_ema_period_range",     "exit_ema_period"),
            ("macd_fast_range",           "macd_fast_period"),
            ("macd_slow_range",           "macd_slow_period"),
            ("rsi_lower_range",           "rsi_lower"),
            ("rsi_upper_range",           "rsi_upper"),
            ("funding_threshold_range",   "funding_threshold"),
            ("sl_n_atr_init_range",       "sl_n_atr_init"),
            ("sl_n_atr_trail_range",      "sl_n_atr_trail"),
            ("sl_swing_lookback_range",   "sl_swing_lookback"),
            ("ema_above_period_range",    "ema_above_period"),
            ("vwap_anchor_hours_range",   "vwap_anchor_hours"),
            ("vwma_period_range",         "vwma_period"),
            ("engulfing_ratio_range",     "engulfing_ratio"),
            ("hammer_wick_ratio_range",   "hammer_wick_ratio"),
            ("bb_period_range",           "bb_period"),
            ("bb_num_std_range",          "bb_num_std"),
            ("atr_reversal_mult_range",   "atr_reversal_mult"),
            ("atr_reversal_period_range", "atr_reversal_period"),
            ("entry_regime_offset_range", "entry_regime_offset"),
        ))

    # ------------------------------------------------------------------
    # Core API
    # ------------------------------------------------------------------

    def build_baseline_params(self) -> dict[str, Any]:
        """Return a dict of all Parameters fields at their default values.

        Single-value boolean pins and numeric pins are applied here so they
        override Parameters() defaults.  Without this a (False,) pin on a
        True-defaulting flag would silently run as True because single-value
        ranges are excluded from parameter_names and therefore never written
        into grid candidates.
        """
        params = asdict(Parameters())

        # Apply single-value boolean pins
        for name, rng in self.boolean_filter_ranges.items():
            if len(rng) == 1:
                params[name] = rng[0]

        # Apply single-value numeric pins
        for range_field, param_name in self._NUMERIC_MAP:
            rng = getattr(self, range_field)
            if len(rng) == 1:
                params[param_name] = rng[0]

        return params

    def validate_coverage(self) -> None:
        """Raise ValueError if any auditable boolean flag is absent from boolean_filter_ranges.

        Call this before starting a run to catch incomplete configs early rather
        than silently inheriting Parameters() defaults for undeclared flags.
        """
        missing = [f for f in _AUDITABLE_BEAR_FLAGS if f not in self.boolean_filter_ranges]
        if missing:
            raise ValueError(
                "BearGridConfig is missing explicit declarations for the following "
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
        """
        defaults = {f.name: f.default for f in dataclasses.fields(Parameters)}
        entries: list[AuditEntry] = []

        for name in _AUDITABLE_BEAR_FLAGS:
            rng = self.boolean_filter_ranges.get(name)
            if rng is None:
                status = "implicit"
                values = (defaults.get(name),)
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

        for range_field, param_name in self._NUMERIC_MAP:
            rng = getattr(self, range_field)
            status = "swept" if len(rng) > 1 else "pinned"
            entries.append(AuditEntry(param_name, status, rng))

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
        for range_field, param_name in self._NUMERIC_MAP:
            if len(getattr(self, range_field)) > 1:
                names.append(param_name)
        return tuple(names)

    @property
    def parameter_ranges(self) -> dict[str, tuple]:
        """Values to test for each parameter in parameter_names."""
        ranges: dict[str, tuple] = {
            name: rng
            for name, rng in self.boolean_filter_ranges.items()
            if len(rng) > 1
        }
        for range_field, param_name in self._NUMERIC_MAP:
            rng = getattr(self, range_field)
            if len(rng) > 1:
                ranges[param_name] = rng
        return ranges

    @property
    def feature_dependencies(self) -> dict[str, tuple[str, ...]]:
        """Numeric params that are irrelevant when their parent flag is off.

        Prevents duplicate runs: e.g. exit_rsi_level=45 vs 50 are identical
        when use_rsi_exit=False, so they collapse to the same deduped combo.
        """
        return {
            "vp_price_bins":      ("use_vp_trigger",),
            "exit_rsi_level":     ("use_rsi_exit",),
            "rsi_oversold_level": ("use_rsi_oversold_exit",),
            "exit_ema_period":    ("use_ema_reclaim_exit",),
            "macd_fast_period":   ("use_macd_exit",),
            "macd_slow_period":   ("use_macd_exit",),
            # tp_mult irrelevant when use_fixed_tp=False
            "target_atr_mult":    ("use_fixed_tp",),
            # Entry-candle SL params irrelevant when use_vbt_sl=False
            "sl_n_atr_init":      ("use_vbt_sl",),
            # Trailing SL params irrelevant when use_vbt_sl_trail=False
            # (trail works on top of either SL mode, so depends only on trail flag)
            "sl_n_atr_trail":     ("use_vbt_sl_trail",),
            "sl_swing_lookback":  ("use_vbt_sl_trail",),
            # New exit numeric params — irrelevant when their exit is off
            "ema_above_period":   ("use_ema_above_exit",),
            "vwap_anchor_hours":  ("use_vwap_exit",),
            "vwma_period":        ("use_vwma_exit",),
            "engulfing_ratio":    ("use_engulfing_exit",),
            "hammer_wick_ratio":  ("use_hammer_exit",),
            "bb_period":          ("use_bb_mean_reversion_exit",),
            "bb_num_std":         ("use_bb_mean_reversion_exit",),
            "atr_reversal_mult":  ("use_atr_reversal_exit",),
            "atr_reversal_period": ("use_atr_reversal_exit",),
        }
