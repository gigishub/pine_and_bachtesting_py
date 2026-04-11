"""Unit tests for the decision (entry/exit) modules."""

from __future__ import annotations

import pytest

from adaptive_momentum_strategy.strategy.decision.entry import should_buy
from adaptive_momentum_strategy.strategy.decision.exit import should_sell


# ---------------------------------------------------------------------------
# Entry: should_buy
# ---------------------------------------------------------------------------

class TestShouldBuy:
    def test_all_true_no_position(self):
        assert should_buy(True, True, True, False) is True

    def test_false_when_in_position(self):
        assert should_buy(True, True, True, True) is False

    def test_false_when_regime_missing(self):
        assert should_buy(False, True, True, False) is False

    def test_false_when_setup_missing(self):
        assert should_buy(True, False, True, False) is False

    def test_false_when_trigger_missing(self):
        assert should_buy(True, True, False, False) is False

    def test_all_false(self):
        assert should_buy(False, False, False, True) is False


# ---------------------------------------------------------------------------
# Exit: should_sell
# ---------------------------------------------------------------------------

class TestShouldSell:
    def test_sells_when_close_below_stop(self):
        assert should_sell(close=49_000, trail_stop=50_000, in_position=True) is True

    def test_holds_when_close_above_stop(self):
        assert should_sell(close=51_000, trail_stop=50_000, in_position=True) is False

    def test_no_sell_when_not_in_position(self):
        assert should_sell(close=49_000, trail_stop=50_000, in_position=False) is False

    def test_no_sell_when_stop_is_none(self):
        assert should_sell(close=49_000, trail_stop=None, in_position=True) is False

    def test_no_sell_at_exact_stop(self):
        # Stop fires on LESS THAN, not less-than-or-equal.
        assert should_sell(close=50_000, trail_stop=50_000, in_position=True) is False
