from __future__ import annotations

"""Compatibility facade.

This file keeps the old import path working while the code lives in focused modules:
- REST client: bybit_client/rest.py
- WebSocket stream: bybit_client/ws.py
- Shared types/helpers: bybit_client/types.py
"""

from .bybit_client import BybitPublicKlineStream, BybitV5Client, InstrumentSpec, floor_to_step, fmt_decimal, to_decimal

__all__ = [
    "BybitPublicKlineStream",
    "BybitV5Client",
    "InstrumentSpec",
    "floor_to_step",
    "fmt_decimal",
    "to_decimal",
]
