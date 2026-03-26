"""Test suite for the refactored UPS_py_v2/live components.

Run with:
    source .venv/bin/activate && python -m pytest UPS_py_v2/live/test_live.py -v
or:
    source .venv/bin/activate && python UPS_py_v2/live/test_live.py
"""
from __future__ import annotations

import unittest
from decimal import Decimal
from io import StringIO
from unittest.mock import MagicMock, patch

import pandas as pd

from UPS_py_v2.live.bybit_client import InstrumentSpec
from UPS_py_v2.live.ups_runner.config import LiveConfig
from UPS_py_v2.live.ups_runner.common.live_logger import LiveLogger
from UPS_py_v2.live.ups_runner.common.types import Position, PositionUpdate, StrategySignals
from UPS_py_v2.live.ups_runner.order_manager.order_manager import OrderManager
from UPS_py_v2.live.ups_runner.strategy_runner.position_manager import PositionManager
from UPS_py_v2.live.ups_runner.strategy_runner.strategy_executor import StrategyExecutor


# ---------------------------------------------------------------------------
# Shared test helpers
# ---------------------------------------------------------------------------

def _cfg(**overrides) -> LiveConfig:
    defaults = dict(api_key="test_key", api_secret="test_secret", dry_run=True)
    defaults.update(overrides)
    return LiveConfig(**defaults)


def _instrument(tick_size: str = "0.5", qty_step: str = "0.001") -> InstrumentSpec:
    return InstrumentSpec(
        symbol="BTCUSDT",
        category="linear",
        tick_size=Decimal(tick_size),
        qty_step=Decimal(qty_step),
        min_order_qty=Decimal("0.001"),
        max_order_qty=Decimal("9999"),
    )


def _make_ohlcv(n: int = 10, base_price: float = 100.0) -> pd.DataFrame:
    dates = pd.date_range("2024-01-01", periods=n, freq="1min", tz="UTC")
    return pd.DataFrame(
        {
            "Open": [base_price + i for i in range(n)],
            "High": [base_price + i + 1.0 for i in range(n)],
            "Low": [base_price + i - 1.0 for i in range(n)],
            "Close": [base_price + i + 0.5 for i in range(n)],
            "Volume": [10.0] * n,
            "Timestamp": [int(d.timestamp() * 1000) for d in dates],
        },
        index=dates,
    )


def _signals(
    *,
    is_ready: bool = True,
    price_above_ma: bool = True,
    long_conditions_met: bool = False,
    bearish_pb: bool = False,
    long_entry_pattern: bool = False,
    short_conditions_met: bool = False,
    bullish_pb: bool = False,
    short_entry_pattern: bool = False,
    atr_value: float = 100.0,
) -> StrategySignals:
    return StrategySignals(
        is_ready=is_ready,
        price_above_ma=price_above_ma,
        long_conditions_met=long_conditions_met,
        bearish_pb=bearish_pb,
        long_entry_pattern=long_entry_pattern,
        short_conditions_met=short_conditions_met,
        bullish_pb=bullish_pb,
        short_entry_pattern=short_entry_pattern,
        atr_value=atr_value,
    )


# ---------------------------------------------------------------------------
# LiveLogger
# ---------------------------------------------------------------------------

class TestLiveLogger(unittest.TestCase):
    def test_log_writes_to_stdout(self):
        logger = LiveLogger()
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            logger.log("hello world")
            output = mock_out.getvalue()
        self.assertIn("UTC", output)
        self.assertIn("hello world", output)

    def test_log_format_contains_timestamp(self):
        logger = LiveLogger()
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            logger.log("test")
            output = mock_out.getvalue()
        # Expect format like [2024-01-01 00:00:00 UTC]
        self.assertRegex(output, r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} UTC\]")


# ---------------------------------------------------------------------------
# StrategySignals dataclass
# ---------------------------------------------------------------------------

class TestStrategySignals(unittest.TestCase):
    def test_construction(self):
        sig = _signals(is_ready=True, atr_value=250.0)
        self.assertTrue(sig.is_ready)
        self.assertEqual(sig.atr_value, 250.0)

    def test_defaults_are_sensible(self):
        sig = _signals()
        self.assertIsInstance(sig.price_above_ma, bool)
        self.assertIsInstance(sig.atr_value, float)


# ---------------------------------------------------------------------------
# OrderManager
# ---------------------------------------------------------------------------

class TestOrderManager(unittest.TestCase):
    def _make(self, **cfg_overrides) -> tuple[OrderManager, MagicMock]:
        cfg = _cfg(**cfg_overrides)
        client = MagicMock()
        om = OrderManager(client, cfg, _instrument(), LiveLogger())
        return om, client

    # get_current_position
    def test_get_position_flat(self):
        om, client = self._make()
        client.get_position.return_value = [{"side": "None", "size": "0"}]
        self.assertIsNone(om.get_current_position())

    def test_get_position_empty_list(self):
        om, client = self._make()
        client.get_position.return_value = []
        self.assertIsNone(om.get_current_position())

    def test_get_position_long(self):
        om, client = self._make(dry_run=False)
        client.get_position.return_value = [{"side": "Buy", "size": "0.01", "avgPrice": "50000"}]
        pos = om.get_current_position()
        self.assertIsNotNone(pos)
        self.assertEqual(pos.side, "Buy")
        self.assertAlmostEqual(pos.size, 0.01)
        self.assertAlmostEqual(pos.avg_price, 50000.0)

    def test_get_position_short(self):
        om, client = self._make(dry_run=False)
        client.get_position.return_value = [{"side": "Sell", "size": "0.02", "avgPrice": "45000"}]
        pos = om.get_current_position()
        self.assertIsNotNone(pos)
        self.assertEqual(pos.side, "Sell")

    # compute_qty
    def test_compute_qty_fixed(self):
        om, _ = self._make(fixed_order_qty=0.05)
        qty = om.compute_qty(50000.0, 49000.0)
        self.assertEqual(qty, Decimal("0.05"))

    def test_compute_qty_risk_based(self):
        # balance=10000, risk=1%, risk_usdt=100, distance=1000 -> qty=0.1
        om, client = self._make(dry_run=False, risk_per_trade_pct=1.0, fixed_order_qty=0.0)
        client.get_wallet_balance.return_value = 10_000.0
        qty = om.compute_qty(50000.0, 49000.0)
        self.assertAlmostEqual(float(qty), 0.1)

    def test_compute_qty_zero_distance(self):
        om, _ = self._make(fixed_order_qty=0.0)
        qty = om.compute_qty(50000.0, 50000.0)
        self.assertEqual(qty, Decimal("0"))

    def test_compute_qty_below_notional(self):
        # tiny balance * pct -> effectively zero notional
        om, client = self._make(risk_per_trade_pct=0.0001, fixed_order_qty=0.0, min_notional_usdt=5.0)
        client.get_wallet_balance.return_value = 1.0  # $1 balance * 0.0001% -> negligible
        qty = om.compute_qty(50000.0, 49900.0)
        self.assertEqual(qty, Decimal("0"))

    # place_entry
    def test_place_entry_dry_run_no_api_call(self):
        om, client = self._make(dry_run=True)
        order_id = om.place_entry("Buy", Decimal("0.01"), ref_price=50000.0)
        self.assertIsNotNone(order_id)
        client.create_order.assert_not_called()

    def test_place_entry_live_calls_api(self):
        om, client = self._make(dry_run=False)
        client.create_order.return_value = {"result": {"orderId": "abc123"}}
        order_id = om.place_entry("Sell", Decimal("0.01"), ref_price=50000.0)
        self.assertEqual(order_id, "abc123")
        client.create_order.assert_called_once()
        payload = client.create_order.call_args[1]["payload"] if "payload" in client.create_order.call_args[1] else client.create_order.call_args[0][0]
        self.assertEqual(payload["side"], "Sell")

    def test_place_entry_non_fatal_rejection_returns_false(self):
        om, client = self._make(dry_run=False)
        client.create_order.side_effect = RuntimeError("Bybit error 110007: ab not enough for new order")
        order_id = om.place_entry("Buy", Decimal("0.01"), ref_price=50000.0)
        self.assertIsNone(order_id)

    # update_stops
    def test_update_stops_dry_run_no_api_call(self):
        om, client = self._make(dry_run=True)
        om.update_stops(stop_loss=49000.0, take_profit=52000.0, position_size=0.01, position_side="Buy")
        client.set_trading_stop.assert_not_called()

    def test_update_stops_skips_spot(self):
        om, client = self._make(category="spot", dry_run=False)
        om.update_stops(stop_loss=49000.0, take_profit=None, position_size=0.01, position_side="Buy")
        client.set_trading_stop.assert_not_called()

    def test_update_stops_live_calls_api(self):
        om, client = self._make(dry_run=False, category="linear")
        client.set_trading_stop.return_value = {"retCode": 0}
        om.update_stops(stop_loss=49000.0, take_profit=52000.0, position_size=0.01, position_side="Buy")
        client.set_trading_stop.assert_called_once()

    def test_update_stops_partial_tpsl_10001_fallbacks_full(self):
        om, client = self._make(dry_run=False, category="linear", tp_as_limit=True, sl_as_market=True)
        # first attempt fails with invalid param (10001), fallback should attempt full mode and succeed
        client.set_trading_stop.side_effect = [RuntimeError("Bybit error 10001: request parameter error"), {"retCode": 0}]
        om.update_stops(stop_loss=49000.0, take_profit=52000.0, position_size=0.01, position_side="Buy")
        self.assertEqual(client.set_trading_stop.call_count, 2)

    def test_update_stops_partial_then_full_10001_uses_emergency_sl_only(self):
        om, client = self._make(dry_run=False, category="linear", tp_as_limit=True, sl_as_market=True)
        client.set_trading_stop.side_effect = [
            RuntimeError("Bybit error 10001: request parameter error"),
            RuntimeError("Bybit error 10001: request parameter error"),
            {"retCode": 0},
        ]
        ok = om.update_stops(stop_loss=49000.0, take_profit=52000.0, position_size=0.01, position_side="Buy")
        self.assertTrue(ok)
        self.assertEqual(client.set_trading_stop.call_count, 3)

    def test_update_stops_partial_then_sl_fails_uses_emergency_tp_only(self):
        """TP-only succeeds after SL rejected: returns False so runner queues SL retry."""
        om, client = self._make(dry_run=False, category="linear", tp_as_limit=True, sl_as_market=True)
        client.set_trading_stop.side_effect = [
            RuntimeError("Bybit error 10001: request parameter error"),
            RuntimeError("Bybit error 10001: request parameter error"),
            RuntimeError("Bybit error 10001: request parameter error"),
            {"retCode": 0},
        ]
        ok = om.update_stops(stop_loss=49000.0, take_profit=52000.0, position_size=0.01, position_side="Buy")
        self.assertFalse(ok)  # SL not set — runner must keep retrying
        self.assertEqual(client.set_trading_stop.call_count, 4)

    def test_update_stops_tp_34040_after_sl_fails_still_retries(self):
        """On retry, TP returns 34040 (already set) but SL still unset: returns False to keep retrying."""
        om, client = self._make(dry_run=False, category="linear", tp_as_limit=True, sl_as_market=True)
        # partial fails, full fails, SL-only fails, TP-only returns 34040 (already set from previous call)
        client.set_trading_stop.side_effect = [
            RuntimeError("Bybit error 10001: request parameter error"),
            RuntimeError("Bybit error 10001: request parameter error"),
            RuntimeError("Bybit error 10001: request parameter error"),
            RuntimeError("Bybit error 34040: order unchanged"),
        ]
        ok = om.update_stops(stop_loss=49000.0, take_profit=52000.0, position_size=0.01, position_side="Buy")
        self.assertFalse(ok)  # TP already on exchange, SL still missing — keep retrying
        self.assertEqual(client.set_trading_stop.call_count, 4)


# ---------------------------------------------------------------------------
# PositionManager
# ---------------------------------------------------------------------------

class TestPositionManager(unittest.TestCase):
    def _make(self, **cfg_overrides) -> PositionManager:
        cfg = _cfg(**cfg_overrides)
        return PositionManager(cfg, Decimal("0.5"), LiveLogger())

    def test_on_entry_sets_state(self):
        pm = self._make()
        pm.on_entry(stop_price=49000.0, target_price=52000.0)
        self.assertEqual(pm.state.trade_stop_price, 49000.0)
        self.assertEqual(pm.state.trade_target_price, 52000.0)
        self.assertEqual(pm.state.active_stop_price, 49000.0)
        self.assertIsNone(pm.state.trail_stop_price)
        self.assertFalse(pm.state.look_for_exit)
        self.assertIsNone(pm.state.last_stop_sent)

    def test_on_flat_resets_state(self):
        pm = self._make()
        pm.on_entry(49000.0, 52000.0)
        pm.on_flat()
        self.assertIsNone(pm.state.trade_stop_price)
        self.assertIsNone(pm.state.active_stop_price)
        self.assertFalse(pm.state.look_for_exit)

    def test_first_update_triggers_stop_submission(self):
        pm = self._make(trail_stop=False)
        pm.on_entry(stop_price=49000.0, target_price=52000.0)
        pos = Position(side="Buy", size=0.01, avg_price=50000.0)
        df = _make_ohlcv(5)
        update = pm.update_for_closed_bar(df, _signals(), pos)
        self.assertTrue(update.should_update_stops)
        self.assertEqual(update.new_stop_price, 49000.0)

    def test_second_update_same_stop_no_submission(self):
        pm = self._make(trail_stop=False)
        pm.on_entry(stop_price=49000.0, target_price=52000.0)
        pos = Position(side="Buy", size=0.01, avg_price=50000.0)
        df = _make_ohlcv(5)
        pm.update_for_closed_bar(df, _signals(), pos)  # first update sent
        update2 = pm.update_for_closed_bar(df, _signals(), pos)
        self.assertFalse(update2.should_update_stops)

    def test_recovery_path_when_state_missing(self):
        pm = self._make(trail_stop=False)
        # No on_entry called — simulate restart
        pos = Position(side="Buy", size=0.01, avg_price=50000.0)
        df = _make_ohlcv(5)
        update = pm.update_for_closed_bar(df, _signals(), pos)
        self.assertIsNotNone(pm.state.trade_stop_price)
        self.assertTrue(update.should_update_stops)

    def test_look_for_exit_activates_when_target_breached_long(self):
        pm = self._make(trail_stop=True)
        pm.on_entry(stop_price=49000.0, target_price=51000.0)
        pos = Position(side="Buy", size=0.01, avg_price=50000.0)
        df = _make_ohlcv(10, base_price=50000.0)
        # Force last candle High above target
        df.loc[df.index[-1], "High"] = 51500.0
        pm.update_for_closed_bar(df, _signals(atr_value=200.0), pos)
        self.assertTrue(pm.state.look_for_exit)

    def test_look_for_exit_activates_when_target_breached_short(self):
        pm = self._make(trail_stop=True)
        pm.on_entry(stop_price=51000.0, target_price=49000.0)
        pos = Position(side="Sell", size=0.01, avg_price=50000.0)
        df = _make_ohlcv(10, base_price=50000.0)
        df.loc[df.index[-1], "Low"] = 48500.0
        pm.update_for_closed_bar(df, _signals(atr_value=200.0), pos)
        self.assertTrue(pm.state.look_for_exit)

    def test_non_trailing_update_includes_take_profit(self):
        pm = self._make(trail_stop=False)
        pm.on_entry(stop_price=49000.0, target_price=52000.0)
        pos = Position(side="Buy", size=0.01, avg_price=50000.0)
        df = _make_ohlcv(5)
        update = pm.update_for_closed_bar(df, _signals(), pos)
        self.assertEqual(update.new_take_profit, 52000.0)

    def test_trailing_update_omits_take_profit(self):
        pm = self._make(trail_stop=True)
        pm.on_entry(stop_price=49000.0, target_price=52000.0)
        pos = Position(side="Buy", size=0.01, avg_price=50000.0)
        df = _make_ohlcv(5)
        update = pm.update_for_closed_bar(df, _signals(), pos)
        self.assertIsNone(update.new_take_profit)

    def test_tick_size_threshold_suppresses_small_changes(self):
        # tick_size=10, so changes < 10 should not trigger an update
        pm = PositionManager(_cfg(trail_stop=False), Decimal("10"), LiveLogger())
        pm.on_entry(stop_price=49000.0, target_price=52000.0)
        pm.state.last_stop_sent = 49005.0  # simulate prev send
        pm.state.active_stop_price = 49009.0  # change < tick_size=10
        update = pm._build_update()
        self.assertFalse(update.should_update_stops)


# ---------------------------------------------------------------------------
# StrategyExecutor
# ---------------------------------------------------------------------------

class TestStrategyExecutor(unittest.TestCase):
    def test_compute_returns_strategy_signals_instance(self):
        cfg = _cfg()
        executor = StrategyExecutor(cfg)
        # Need enough bars to pass the warmup checks
        n = cfg.ma_length + cfg.ma_consolidation_lookback + 30
        df = _make_ohlcv(n)
        result = executor.compute(df)
        self.assertIsInstance(result, StrategySignals)
        self.assertIsInstance(result.atr_value, float)
        self.assertIsInstance(result.is_ready, bool)
        self.assertIsInstance(result.price_above_ma, bool)

    def test_compute_not_ready_below_warmup(self):
        cfg = _cfg()
        executor = StrategyExecutor(cfg)
        # Very few bars → is_ready should be False
        df = _make_ohlcv(5)
        result = executor.compute(df)
        self.assertFalse(result.is_ready)


# ---------------------------------------------------------------------------
# LiveRunner._process_closed_bar  (integration test with mocked subsystems)
# ---------------------------------------------------------------------------

class TestLiveRunnerProcessBar(unittest.TestCase):
    def _make_runner(self):
        from UPS_py_v2.live.ups_runner.strategy_runner.runner import LiveRunner

        cfg = _cfg(dry_run=True, use_ws_kline=False)
        with patch("UPS_py_v2.live.ups_runner.strategy_runner.runner.live_runner.BybitV5Client") as MockClient:
            mock_client = MagicMock()
            mock_client.get_instrument_spec.return_value = _instrument()
            MockClient.return_value = mock_client
            runner = LiveRunner(cfg)

        # Replace subsystems with mocks for isolated testing
        runner.strategy = MagicMock()
        runner.orders = MagicMock()
        runner.position = MagicMock()
        return runner

    def test_skips_when_not_ready(self):
        runner = self._make_runner()
        runner.strategy.compute.return_value = _signals(is_ready=False)
        runner._process_closed_bar(_make_ohlcv(5), last_ts=1_000_000)
        runner.orders.get_current_position.assert_not_called()
        self.assertEqual(runner.last_processed_ts, 1_000_000)

    def test_flat_no_signal_no_entry(self):
        runner = self._make_runner()
        runner.strategy.compute.return_value = _signals(
            is_ready=True, long_conditions_met=False, long_entry_pattern=False
        )
        runner.orders.get_current_position.return_value = None
        runner._process_closed_bar(_make_ohlcv(5), last_ts=2_000_000)
        runner.orders.place_entry.assert_not_called()
        self.assertEqual(runner.last_processed_ts, 2_000_000)

    def test_rejected_entry_does_not_mark_in_memory_position(self):
        runner = self._make_runner()
        runner.strategy.compute.return_value = _signals(
            is_ready=True,
            long_conditions_met=False,
            bearish_pb=True,
            long_entry_pattern=True,
            price_above_ma=True,
        )
        runner.orders.get_current_position.return_value = None
        runner.orders.compute_qty.return_value = Decimal("0.01")
        runner.orders.place_entry.return_value = None
        runner._process_closed_bar(_make_ohlcv(10), last_ts=2_500_000)
        runner.position.on_entry.assert_not_called()
        runner.orders.update_stops.assert_not_called()

    def test_unfilled_accepted_entry_defers_state_and_stops(self):
        runner = self._make_runner()
        runner.cfg.dry_run = False
        runner.strategy.compute.return_value = _signals(
            is_ready=True,
            long_conditions_met=False,
            bearish_pb=True,
            long_entry_pattern=True,
            price_above_ma=True,
        )
        # First call: before _try_entry, second call: after sleep in _process_closed_bar,
        # third call: _try_entry immediate fill check.
        runner.orders.get_current_position.side_effect = [None, None, None]
        runner.orders.compute_qty.return_value = Decimal("0.01")
        runner.orders.place_entry.return_value = "entry-123"
        runner._process_closed_bar(_make_ohlcv(10), last_ts=2_600_000)
        runner.position.on_entry.assert_not_called()
        runner.orders.update_stops.assert_not_called()

    def test_pending_fill_attaches_stops_immediately(self):
        runner = self._make_runner()
        runner.strategy.compute.return_value = _signals(is_ready=True)
        runner.pending_entry_order_id = "entry-123"
        runner.pending_entry_bar_ts = 2_500_000
        runner.pending_entry_stop_price = 49000.0
        runner.pending_entry_target_price = 52000.0
        pos = Position(side="Sell", size=0.02, avg_price=50000.0)
        runner.orders.get_current_position.return_value = pos
        runner.position.update_for_closed_bar.return_value = PositionUpdate(should_update_stops=False)

        runner._process_closed_bar(_make_ohlcv(10), last_ts=2_700_000)

        runner.position.on_entry.assert_called_once_with(49000.0, 52000.0)
        runner.orders.update_stops.assert_called_once_with(
            stop_loss=49000.0,
            take_profit=52000.0,
            position_size=0.02,
            position_side="Sell",
        )
        self.assertIsNone(runner.pending_entry_order_id)
        self.assertIsNone(runner.pending_entry_bar_ts)
        self.assertIsNone(runner.pending_entry_stop_price)
        self.assertIsNone(runner.pending_entry_target_price)

    def test_open_position_calls_position_manager(self):
        runner = self._make_runner()
        runner.strategy.compute.return_value = _signals(is_ready=True)
        pos = Position(side="Buy", size=0.01, avg_price=50000.0)
        runner.orders.get_current_position.return_value = pos
        runner.position.update_for_closed_bar.return_value = PositionUpdate(
            should_update_stops=True, new_stop_price=49000.0, new_take_profit=None
        )
        runner._process_closed_bar(_make_ohlcv(5), last_ts=3_000_000)
        runner.position.update_for_closed_bar.assert_called_once()
        runner.orders.update_stops.assert_called_once_with(
            stop_loss=49000.0,
            take_profit=None,
            position_size=0.01,
            position_side="Buy",
        )

    def test_open_position_no_update_when_not_needed(self):
        runner = self._make_runner()
        runner.strategy.compute.return_value = _signals(is_ready=True)
        pos = Position(side="Buy", size=0.01, avg_price=50000.0)
        runner.orders.get_current_position.return_value = pos
        runner.position.update_for_closed_bar.return_value = PositionUpdate(should_update_stops=False)
        runner._process_closed_bar(_make_ohlcv(5), last_ts=4_000_000)
        runner.orders.update_stops.assert_not_called()

    def test_last_processed_ts_always_updated(self):
        runner = self._make_runner()
        runner.strategy.compute.return_value = _signals(is_ready=False)
        runner._process_closed_bar(_make_ohlcv(5), last_ts=9_999_999)
        self.assertEqual(runner.last_processed_ts, 9_999_999)


# ---------------------------------------------------------------------------
# Module-level import smoke test
# ---------------------------------------------------------------------------

class TestImports(unittest.TestCase):
    def test_live_runner_importable(self):
        from UPS_py_v2.live.ups_runner.strategy_runner.runner import LiveRunner, UPSLiveRunner
        self.assertIs(UPSLiveRunner, LiveRunner)

    def test_live_package_exports(self):
        from UPS_py_v2.live import LiveRunner, LiveConfig
        self.assertTrue(callable(LiveRunner))
        self.assertTrue(callable(LiveConfig))


if __name__ == "__main__":
    unittest.main(verbosity=2)
