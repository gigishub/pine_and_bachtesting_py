from __future__ import annotations

import hashlib
import hmac
import json
import time
from decimal import Decimal
from typing import Any

import requests

from .bybit_types import InstrumentSpec


class BybitV5Client:
    """Thin REST client for the Bybit V5 API."""

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        *,
        testnet: bool = False,
        recv_window: int = 5000,
        timeout: int = 10,
    ) -> None:
        self.api_key = api_key
        self.api_secret = api_secret
        self.recv_window = recv_window
        self.timeout = timeout
        self.base_url = "https://api-testnet.bybit.com" if testnet else "https://api.bybit.com"
        self.session = requests.Session()

    def public_ws_url(self, category: str) -> str:
        domain = "stream-testnet.bybit.com" if self.base_url.endswith("testnet.bybit.com") else "stream.bybit.com"
        return f"wss://{domain}/v5/public/{category}"

    @staticmethod
    def _now_ms() -> int:
        return int(time.time() * 1000)

    def _sign(self, payload: str, timestamp_ms: int) -> str:
        raw = f"{timestamp_ms}{self.api_key}{self.recv_window}{payload}"
        return hmac.new(
            self.api_secret.encode("utf-8"),
            raw.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
        auth: bool = False,
    ) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        headers: dict[str, str] = {}
        body_json: str | None = None

        if method.upper() != "GET":
            # Serialize once so the exact byte string used for signing is also sent on the wire.
            body_json = json.dumps(body or {}, separators=(",", ":"))

        if auth:
            ts = self._now_ms()
            if method.upper() == "GET":
                payload = ""
                if params:
                    # Bybit signs query-string bytes exactly in request order.
                    payload = "&".join(f"{k}={v}" for k, v in params.items())
            else:
                payload = body_json or "{}"

            headers.update(
                {
                    "X-BAPI-API-KEY": self.api_key,
                    "X-BAPI-TIMESTAMP": str(ts),
                    "X-BAPI-RECV-WINDOW": str(self.recv_window),
                    "X-BAPI-SIGN": self._sign(payload, ts),
                }
            )

        if method.upper() == "GET":
            resp = self.session.get(url, params=params, headers=headers, timeout=self.timeout)
        else:
            headers["Content-Type"] = "application/json"
            resp = self.session.post(url, data=body_json or "{}", headers=headers, timeout=self.timeout)

        resp.raise_for_status()
        data = resp.json()
        if data.get("retCode") != 0:
            raise RuntimeError(f"Bybit error {data.get('retCode')}: {data.get('retMsg')} | {data}")
        return data

    def get_server_time_ms(self) -> int:
        data = self._request("GET", "/v5/market/time")
        result = data.get("result", {})
        time_nano = result.get("timeNano")
        if time_nano:
            return int(int(time_nano) / 1_000_000)
        return int(result.get("timeSecond", "0")) * 1000

    def get_kline(
        self,
        *,
        category: str,
        symbol: str,
        interval: str,
        limit: int,
    ) -> list[list[str]]:
        data = self._request(
            "GET",
            "/v5/market/kline",
            params={
                "category": category,
                "symbol": symbol,
                "interval": interval,
                "limit": limit,
            },
        )
        return data.get("result", {}).get("list", [])

    def get_instrument_spec(self, *, category: str, symbol: str) -> InstrumentSpec:
        data = self._request(
            "GET",
            "/v5/market/instruments-info",
            params={"category": category, "symbol": symbol},
        )
        items = data.get("result", {}).get("list", [])
        if not items:
            raise RuntimeError(f"No instrument info for {category}:{symbol}")

        item = items[0]
        lot = item.get("lotSizeFilter", {})
        price_filter = item.get("priceFilter", {})

        return InstrumentSpec(
            symbol=symbol,
            category=category,
            tick_size=Decimal(str(price_filter.get("tickSize", "0.01"))),
            qty_step=Decimal(str(lot.get("qtyStep", lot.get("basePrecision", "0.0001")))),
            min_order_qty=Decimal(str(lot.get("minOrderQty", "0.0001"))),
            max_order_qty=Decimal(str(lot.get("maxOrderQty", "99999999"))),
        )

    def create_order(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._request("POST", "/v5/order/create", body=payload, auth=True)

    def cancel_order(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._request("POST", "/v5/order/cancel", body=payload, auth=True)

    def get_open_orders(self, *, category: str, symbol: str, open_only: int = 0) -> list[dict[str, Any]]:
        data = self._request(
            "GET",
            "/v5/order/realtime",
            params={"category": category, "symbol": symbol, "openOnly": open_only},
            auth=True,
        )
        return data.get("result", {}).get("list", [])

    def get_position(self, *, category: str, symbol: str) -> list[dict[str, Any]]:
        data = self._request(
            "GET",
            "/v5/position/list",
            params={"category": category, "symbol": symbol},
            auth=True,
        )
        return data.get("result", {}).get("list", [])

    def set_trading_stop(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._request("POST", "/v5/position/trading-stop", body=payload, auth=True)

    def set_leverage(self, *, category: str, symbol: str, leverage: float) -> dict[str, Any]:
        lev = str(leverage)
        return self._request(
            "POST",
            "/v5/position/set-leverage",
            body={
                "category": category,
                "symbol": symbol,
                "buyLeverage": lev,
                "sellLeverage": lev,
            },
            auth=True,
        )

    def get_wallet_balance(self, *, account_type: str = "UNIFIED", coin: str = "USDT") -> float:
        """Return available wallet balance for *coin* in USDT."""
        data = self._request(
            "GET",
            "/v5/account/wallet-balance",
            params={"accountType": account_type, "coin": coin},
            auth=True,
        )
        accounts = data.get("result", {}).get("list", [])
        for account in accounts:
            for c in account.get("coin", []):
                if c.get("coin") == coin:
                    return float(c.get("availableToWithdraw") or c.get("walletBalance") or 0)
        return 0.0
