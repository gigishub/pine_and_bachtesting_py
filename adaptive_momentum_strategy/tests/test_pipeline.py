"""Tests for grid construction and the exclusive-flag filter."""

from __future__ import annotations

import pytest

from adaptive_momentum_strategy.backtest.config import MomentumGridConfig
from adaptive_momentum_strategy.backtest.vectorbt.pipeline import (
    _is_exclusive_combo,
    _is_valid_combo,
    build_parameter_grid,
)


# ---------------------------------------------------------------------------
# build_baseline_params — single-value pin regression tests
# ---------------------------------------------------------------------------


class TestBuildBaselineParams:
    """Regression tests for the single-value boolean pin bug.

    Root cause: build_baseline_params() seeded from Parameters() defaults.
    Single-value ranges (len == 1) are excluded from parameter_names, so
    they were never applied to candidates — a (False,) pin on a True-defaulting
    flag like use_donchian silently ran as True for every combo.
    """

    def test_false_pin_overrides_true_default(self):
        # use_donchian defaults to True in Parameters(); pin must force False.
        cfg = MomentumGridConfig(
            boolean_filter_ranges={"use_donchian": (False,)},
        )
        baseline = cfg.build_baseline_params()
        assert baseline["use_donchian"] is False

    def test_true_pin_preserved_when_already_true_default(self):
        # use_cmf defaults to True; a (True,) pin should keep it True.
        cfg = MomentumGridConfig(
            boolean_filter_ranges={"use_cmf": (True,)},
        )
        baseline = cfg.build_baseline_params()
        assert baseline["use_cmf"] is True

    def test_false_pin_preserved_when_already_false_default(self):
        # use_power_candle defaults to False; (False,) pin is a no-op but must not error.
        cfg = MomentumGridConfig(
            boolean_filter_ranges={"use_power_candle": (False,)},
        )
        baseline = cfg.build_baseline_params()
        assert baseline["use_power_candle"] is False

    def test_grid_all_combos_respect_donchian_false_pin(self):
        # Every combo produced by the grid must have use_donchian=False.
        cfg = MomentumGridConfig(
            boolean_filter_ranges={
                "use_adx":           (False, True),
                "use_ema_ribbon":    (False, True),
                "use_donchian":      (False,),          # pinned OFF
                "use_volume_profile":(False, True),
                "use_cmf":           (False, True),
                "use_power_candle":  (False, True),
                "use_chandelier":    (False, True),
                "use_psar":          (False, True),
                "use_bbands":        (False, True),
                "use_trailing_stop": (False, True),
            },
        )
        baseline = cfg.build_baseline_params()
        grid = build_parameter_grid(baseline, cfg)
        assert len(grid) > 0, "Grid must not be empty"
        assert all(combo["use_donchian"] is False for combo in grid), (
            "Some combo has use_donchian=True despite (False,) pin"
        )


# ---------------------------------------------------------------------------
# _is_valid_combo
# ---------------------------------------------------------------------------


class TestIsValidCombo:
    def _base(self, **overrides: bool) -> dict:
        """All-True baseline; overrides turn individual flags off."""
        params: dict = {
            "use_adx": True, "use_ema_ribbon": True,
            "use_donchian": True, "use_volume_profile": True,
            "use_cmf": True, "use_power_candle": True,
            "use_chandelier": True, "use_psar": True, "use_bbands": True,
        }
        params.update(overrides)
        return params

    def test_all_true_is_valid(self):
        assert _is_valid_combo(self._base())

    def test_all_regime_false_is_invalid(self):
        assert not _is_valid_combo(self._base(use_adx=False, use_ema_ribbon=False))

    def test_all_setup_false_is_invalid(self):
        assert not _is_valid_combo(self._base(use_donchian=False, use_volume_profile=False))

    def test_all_trigger_false_is_invalid(self):
        assert not _is_valid_combo(self._base(use_cmf=False, use_power_candle=False))

    def test_all_exit_false_is_invalid(self):
        assert not _is_valid_combo(
            self._base(use_chandelier=False, use_psar=False, use_bbands=False)
        )

    def test_one_flag_per_layer_is_valid(self):
        params = {
            "use_adx": True, "use_ema_ribbon": False,
            "use_donchian": True, "use_volume_profile": False,
            "use_cmf": True, "use_power_candle": False,
            "use_chandelier": True, "use_psar": False, "use_bbands": False,
        }
        assert _is_valid_combo(params)


# ---------------------------------------------------------------------------
# _is_exclusive_combo
# ---------------------------------------------------------------------------


class TestIsExclusiveCombo:
    def _exit_params(self, chandelier: bool, psar: bool, bbands: bool) -> dict:
        return {
            "use_adx": True, "use_ema_ribbon": False,
            "use_donchian": True, "use_volume_profile": False,
            "use_cmf": True, "use_power_candle": False,
            "use_chandelier": chandelier,
            "use_psar": psar,
            "use_bbands": bbands,
        }

    def test_empty_exclusive_layers_always_passes(self):
        params = self._exit_params(True, True, True)
        assert _is_exclusive_combo(params, frozenset())

    def test_single_exit_flag_passes_exclusive(self):
        for chandelier, psar, bbands in [(True, False, False), (False, True, False), (False, False, True)]:
            params = self._exit_params(chandelier, psar, bbands)
            assert _is_exclusive_combo(params, frozenset(["exit"]))

    def test_two_exit_flags_blocked_by_exclusive(self):
        params = self._exit_params(True, True, False)
        assert not _is_exclusive_combo(params, frozenset(["exit"]))

    def test_all_exit_flags_blocked_by_exclusive(self):
        params = self._exit_params(True, True, True)
        assert not _is_exclusive_combo(params, frozenset(["exit"]))

    def test_non_exclusive_layer_unaffected(self):
        # exit exclusive, but two regime flags → regime not checked
        params = {
            "use_adx": True, "use_ema_ribbon": True,   # two regime flags — OK
            "use_donchian": True, "use_volume_profile": False,
            "use_cmf": True, "use_power_candle": False,
            "use_chandelier": True, "use_psar": False, "use_bbands": False,
        }
        assert _is_exclusive_combo(params, frozenset(["exit"]))

    def test_multiple_exclusive_layers_both_enforced(self):
        # regime exclusive + exit exclusive; two regime flags → blocked
        params = {
            "use_adx": True, "use_ema_ribbon": True,   # two regime flags
            "use_donchian": True, "use_volume_profile": False,
            "use_cmf": True, "use_power_candle": False,
            "use_chandelier": True, "use_psar": False, "use_bbands": False,
        }
        assert not _is_exclusive_combo(params, frozenset(["regime", "exit"]))

    def test_all_layers_exclusive_single_flags_pass(self):
        params = {
            "use_adx": True, "use_ema_ribbon": False,
            "use_donchian": True, "use_volume_profile": False,
            "use_cmf": True, "use_power_candle": False,
            "use_chandelier": True, "use_psar": False, "use_bbands": False,
        }
        assert _is_exclusive_combo(
            params, frozenset(["regime", "setup", "trigger", "exit"])
        )


# ---------------------------------------------------------------------------
# build_parameter_grid with exclusive mode
# ---------------------------------------------------------------------------


class TestBuildParameterGridExclusive:
    _ALL_FLAGS = [
        "use_adx", "use_ema_ribbon",
        "use_donchian", "use_volume_profile",
        "use_cmf", "use_power_candle",
        "use_chandelier", "use_psar", "use_bbands", "use_trailing_stop",
    ]

    def _all_on_config(self, **exclusive_overrides: bool) -> MomentumGridConfig:
        """Config with all 10 flags (including trailing stop) swept (False, True)."""
        return MomentumGridConfig(
            boolean_filter_ranges={flag: (False, True) for flag in self._ALL_FLAGS},
            **exclusive_overrides,
        )

    def _baseline(self, config: MomentumGridConfig) -> dict:
        return config.build_baseline_params()

    def _exit_active_counts(self, grid: list[dict]) -> list[int]:
        exit_flags = ("use_chandelier", "use_psar", "use_bbands", "use_trailing_stop")
        return [sum(bool(c.get(f)) for f in exit_flags) for c in grid]

    def test_no_exclusive_default_405_combos(self):
        # 2 regime × 2 setup × 2 trigger × 4 exit valid non-zero combos
        config = self._all_on_config()
        grid = build_parameter_grid(self._baseline(config), config)
        assert len(grid) == 405

    def test_exit_exclusive_all_combos_have_one_exit_flag(self):
        config = self._all_on_config(exit_exclusive=True)
        grid = build_parameter_grid(self._baseline(config), config)
        counts = self._exit_active_counts(grid)
        assert all(c == 1 for c in counts), f"Got exit flag counts: {set(counts)}"

    def test_exit_exclusive_reduces_grid_size(self):
        config = self._all_on_config(exit_exclusive=True)
        grid = build_parameter_grid(self._baseline(config), config)
        default_grid = build_parameter_grid(self._baseline(config), self._all_on_config())
        assert len(grid) < len(default_grid)

    def test_all_exclusive_gives_32_combos(self):
        # 2 regime × 2 setup × 2 trigger × 4 exit = 32
        config = self._all_on_config(
            regime_exclusive=True,
            setup_exclusive=True,
            trigger_exclusive=True,
            exit_exclusive=True,
        )
        grid = build_parameter_grid(self._baseline(config), config)
        assert len(grid) == 32

    def test_all_exclusive_each_layer_has_exactly_one_flag(self):
        config = self._all_on_config(
            regime_exclusive=True,
            setup_exclusive=True,
            trigger_exclusive=True,
            exit_exclusive=True,
        )
        grid = build_parameter_grid(self._baseline(config), config)
        for combo in grid:
            for layer, flags in [
                ("regime",  ("use_adx", "use_ema_ribbon")),
                ("setup",   ("use_donchian", "use_volume_profile")),
                ("trigger", ("use_cmf", "use_power_candle")),
                ("exit",    ("use_chandelier", "use_psar", "use_bbands", "use_trailing_stop")),
            ]:
                active = sum(bool(combo.get(f)) for f in flags)
                assert active == 1, f"{layer} has {active} active flags in combo {combo}"


# ---------------------------------------------------------------------------
# validate_coverage and param_audit
# ---------------------------------------------------------------------------

# All 20 auditable flags (10 long + 9 short + 1 VBT SL)
_ALL_AUDITABLE = [
    "use_adx", "use_ema_ribbon", "use_donchian", "use_volume_profile",
    "use_cmf", "use_power_candle", "use_chandelier", "use_psar",
    "use_bbands", "use_trailing_stop",
    "use_vbt_sl",
    "use_ema_ribbon_short", "use_donchian_short", "use_volume_profile_short",
    "use_cmf_short", "use_power_candle_short", "use_chandelier_short",
    "use_psar_short", "use_bbands_short", "use_trailing_stop_short",
]


class TestConfigAudit:
    def _full_config(self, **overrides) -> MomentumGridConfig:
        """Config with all 19 flags explicitly declared."""
        ranges = {f: (False, True) for f in _ALL_AUDITABLE}
        ranges.update(overrides)
        return MomentumGridConfig(boolean_filter_ranges=ranges)

    def _partial_config(self, missing: list[str]) -> MomentumGridConfig:
        """Config with some flags removed from boolean_filter_ranges."""
        ranges = {f: (False, True) for f in _ALL_AUDITABLE if f not in missing}
        return MomentumGridConfig(boolean_filter_ranges=ranges)

    # --- validate_coverage ---

    def test_validate_coverage_passes_when_all_declared(self):
        cfg = self._full_config()
        cfg.validate_coverage()  # must not raise

    def test_validate_coverage_raises_on_single_missing_flag(self):
        cfg = self._partial_config(missing=["use_donchian"])
        with pytest.raises(ValueError, match="use_donchian"):
            cfg.validate_coverage()

    def test_validate_coverage_raises_listing_all_missing_flags(self):
        cfg = self._partial_config(missing=["use_donchian", "use_cmf"])
        with pytest.raises(ValueError) as exc_info:
            cfg.validate_coverage()
        msg = str(exc_info.value)
        assert "use_donchian" in msg
        assert "use_cmf" in msg

    def test_validate_coverage_default_config_passes(self):
        # MomentumGridConfig() default boolean_filter_ranges declares all 19 flags.
        MomentumGridConfig().validate_coverage()

    # --- param_audit ---

    def test_param_audit_swept_flag_has_status_swept(self):
        cfg = self._full_config(use_adx=(False, True))
        audit = {e.name: e for e in cfg.param_audit()}
        assert audit["use_adx"].status == "swept"
        assert audit["use_adx"].values == (False, True)

    def test_param_audit_true_pin_has_status_pinned_on(self):
        cfg = self._full_config(use_cmf=(True,))
        audit = {e.name: e for e in cfg.param_audit()}
        assert audit["use_cmf"].status == "pinned_on"

    def test_param_audit_false_pin_has_status_pinned_off(self):
        cfg = self._full_config(use_donchian=(False,))
        audit = {e.name: e for e in cfg.param_audit()}
        assert audit["use_donchian"].status == "pinned_off"

    def test_param_audit_implicit_flag_has_status_implicit(self):
        # Manually omit use_bbands from the ranges dict after construction
        cfg = self._full_config()
        cfg.boolean_filter_ranges.pop("use_bbands")
        audit = {e.name: e for e in cfg.param_audit()}
        assert audit["use_bbands"].status == "implicit"

    def test_param_audit_includes_all_19_bool_flags(self):
        cfg = self._full_config()
        audit_names = [e.name for e in cfg.param_audit() if e.name.startswith("use_")]
        for flag in _ALL_AUDITABLE:
            assert flag in audit_names, f"{flag} missing from param_audit()"

    def test_param_audit_includes_numeric_params(self):
        cfg = self._full_config()
        audit_names = {e.name for e in cfg.param_audit()}
        for name in ("adx_threshold", "chandelier_atr_mult", "cmf_threshold", "trail_atr_mult"):
            assert name in audit_names

    def test_param_audit_numeric_pinned_when_single_value(self):
        cfg = self._full_config()
        # All numeric ranges default to single values
        audit = {e.name: e for e in cfg.param_audit()}
        assert audit["adx_threshold"].status == "pinned"

    def test_param_audit_numeric_swept_when_multi_value(self):
        cfg = self._full_config()
        cfg.adx_threshold_range = (20.0, 25.0, 30.0)
        audit = {e.name: e for e in cfg.param_audit()}
        assert audit["adx_threshold"].status == "swept"
