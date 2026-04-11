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
