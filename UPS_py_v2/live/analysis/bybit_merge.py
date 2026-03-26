from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Callable, TypeVar

from pybit.unified_trading import HTTP

from ..ups_runner.config import build_config_from_env


_WINDOW_MS = 7 * 24 * 60 * 60 * 1000 - 1
_T = TypeVar("_T")


def build_bybit_client() -> tuple[HTTP, str]:
    cfg = build_config_from_env()
    client = HTTP(testnet=cfg.testnet, api_key=cfg.api_key, api_secret=cfg.api_secret)
    return client, cfg.category


def parse_float(raw: Any) -> float | None:
    if raw in (None, "", "None"):
        return None
    try:
        return float(raw)
    except (TypeError, ValueError):
        return None


def parse_int(raw: Any) -> int | None:
    if raw in (None, "", "None"):
        return None
    try:
        return int(raw)
    except (TypeError, ValueError):
        return None


def iso_utc_from_ms(raw: Any) -> str | None:
    value = parse_int(raw)
    if value is None:
        return None
    return datetime.fromtimestamp(value / 1000, tz=timezone.utc).isoformat()


def window_ranges(start_ms: int, end_ms: int) -> list[tuple[int, int]]:
    if end_ms < start_ms:
        return []
    windows: list[tuple[int, int]] = []
    cursor = start_ms
    while cursor <= end_ms:
        window_end = min(cursor + _WINDOW_MS, end_ms)
        windows.append((cursor, window_end))
        cursor = window_end + 1
    return windows


def _paginate(fetch_page: Callable[[str | None], dict[str, Any]], list_key: str = "list") -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    seen_cursors: set[str] = set()
    cursor: str | None = None

    while True:
        response = fetch_page(cursor)
        result = response.get("result", {})
        page_items = result.get(list_key, []) or []
        items.extend(page_items)
        next_cursor = result.get("nextPageCursor")
        if not next_cursor or next_cursor in seen_cursors:
            break
        seen_cursors.add(next_cursor)
        cursor = next_cursor

    return items


def _response_dict(raw: Any) -> dict[str, Any]:
    """Coerce pybit responses to dict for stable runtime handling and typing."""
    if isinstance(raw, dict):
        return raw
    return {}


def _dedupe(items: list[dict[str, Any]], key_fn: Callable[[dict[str, Any]], _T]) -> list[dict[str, Any]]:
    unique: dict[_T, dict[str, Any]] = {}
    for item in items:
        unique[key_fn(item)] = item
    return list(unique.values())


def fetch_symbol_bundle(
    client: HTTP,
    *,
    category: str,
    symbol: str,
    start_ms: int,
    end_ms: int,
) -> dict[str, list[dict[str, Any]]]:
    orders: list[dict[str, Any]] = []
    executions: list[dict[str, Any]] = []
    closed_pnl: list[dict[str, Any]] = []

    for window_start, window_end in window_ranges(start_ms, end_ms):
        orders.extend(
            _paginate(
                lambda cursor: _response_dict(
                    client.get_order_history(
                        category=category,
                        symbol=symbol,
                        startTime=window_start,
                        endTime=window_end,
                        limit=50,
                        cursor=cursor,
                    )
                )
            )
        )
        executions.extend(
            _paginate(
                lambda cursor: _response_dict(
                    client.get_executions(
                        category=category,
                        symbol=symbol,
                        startTime=window_start,
                        endTime=window_end,
                        limit=100,
                        cursor=cursor,
                    )
                )
            )
        )
        closed_pnl.extend(
            _paginate(
                lambda cursor: _response_dict(
                    client.get_closed_pnl(
                        category=category,
                        symbol=symbol,
                        startTime=window_start,
                        endTime=window_end,
                        limit=100,
                        cursor=cursor,
                    )
                )
            )
        )

    return {
        "orders": _dedupe(orders, lambda item: str(item.get("orderId") or item)),
        "executions": _dedupe(executions, lambda item: str(item.get("execId") or item)),
        "closed_pnl": _dedupe(closed_pnl, lambda item: str(item.get("orderId") or item)),
    }