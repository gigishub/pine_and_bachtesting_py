from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from ...bybit_client import InstrumentSpec, floor_to_step, fmt_decimal, to_decimal
from ..config import LiveConfig


@dataclass(frozen=True)
class TradingStopPlan:
    """Prepared TP/SL payloads for primary, fallback, and emergency attempts."""

    use_partial_tp_limit: bool
    clear_take_profit: bool
    payload: dict[str, Any]
    full_payload: dict[str, Any]
    sl_only_payload: dict[str, Any] | None
    tp_only_payload: dict[str, Any] | None


def _tp_limit_price(cfg: LiveConfig, instrument: InstrumentSpec, take_profit: float, position_side: str) -> float:
    """Build TP limit price from trigger using configured tick offset."""
    offset_ticks = max(0, int(cfg.tp_limit_offset_ticks))
    offset = float(instrument.tick_size) * offset_ticks
    raw = take_profit + offset if position_side == "Buy" else take_profit - offset
    rounded = floor_to_step(to_decimal(raw), instrument.tick_size)
    return float(rounded)


def _build_single_side_stop_payload(
    cfg: LiveConfig,
    *,
    stop_loss: float | None = None,
    take_profit: float | None = None,
    clear_take_profit: bool = False,
) -> dict[str, Any] | None:
    if stop_loss is None and take_profit is None and not clear_take_profit:
        return None

    payload: dict[str, Any] = {
        "category": cfg.category,
        "symbol": cfg.symbol,
        "positionIdx": cfg.position_idx,
        "tpslMode": "Full",
    }
    if stop_loss is not None:
        payload["stopLoss"] = str(stop_loss)
        payload["slTriggerBy"] = "MarkPrice"
    if clear_take_profit:
        # Bybit uses takeProfit="0" to clear previously attached TP state.
        payload["takeProfit"] = "0"
    if take_profit is not None:
        payload["takeProfit"] = str(take_profit)
        payload["tpTriggerBy"] = "MarkPrice"
    return payload


def build_trading_stop_plan(
    cfg: LiveConfig,
    instrument: InstrumentSpec,
    *,
    stop_loss: float | None,
    take_profit: float | None,
    position_size: float,
    position_side: str,
) -> TradingStopPlan:
    """Create all TP/SL request payloads needed by live stop update flow."""
    clear_take_profit = cfg.trail_stop and take_profit is None

    use_partial_tp_limit = (
        cfg.tp_as_limit
        and cfg.sl_as_market
        and (not cfg.trail_stop)
        and stop_loss is not None
        and take_profit is not None
        and position_size > 0
    )

    payload: dict[str, Any] = {
        "category": cfg.category,
        "symbol": cfg.symbol,
        "positionIdx": cfg.position_idx,
        "tpslMode": "Partial" if use_partial_tp_limit else "Full",
    }

    if use_partial_tp_limit:
        assert take_profit is not None
        size = floor_to_step(to_decimal(position_size), instrument.qty_step)
        payload["tpSize"] = fmt_decimal(size)
        payload["slSize"] = fmt_decimal(size)
        payload["tpOrderType"] = "Limit"
        payload["slOrderType"] = "Market"
        payload["tpLimitPrice"] = str(_tp_limit_price(cfg, instrument, take_profit, position_side))

    if stop_loss is not None:
        payload["stopLoss"] = str(stop_loss)
        payload["slTriggerBy"] = "MarkPrice"
    if clear_take_profit:
        payload["takeProfit"] = "0"
    if take_profit is not None:
        payload["takeProfit"] = str(take_profit)
        payload["tpTriggerBy"] = "MarkPrice"

    full_payload = payload.copy()
    full_payload["tpslMode"] = "Full"
    for key in ["tpSize", "slSize", "tpOrderType", "slOrderType", "tpLimitPrice"]:
        full_payload.pop(key, None)

    sl_only_payload = _build_single_side_stop_payload(cfg, stop_loss=stop_loss)
    tp_only_payload = _build_single_side_stop_payload(
        cfg,
        take_profit=take_profit,
        clear_take_profit=clear_take_profit,
    )

    return TradingStopPlan(
        use_partial_tp_limit=use_partial_tp_limit,
        clear_take_profit=clear_take_profit,
        payload=payload,
        full_payload=full_payload,
        sl_only_payload=sl_only_payload,
        tp_only_payload=tp_only_payload,
    )
