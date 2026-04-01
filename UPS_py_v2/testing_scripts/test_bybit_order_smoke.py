from __future__ import annotations

from decimal import Decimal
from pathlib import Path
import os
import sys

from UPS_py_v2.live.bybit_client import BybitV5Client, floor_to_step, fmt_decimal, to_decimal


def load_dotenv(dotenv_path: Path) -> None:
    if not dotenv_path.exists():
        return
    for raw in dotenv_path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        # Some shells export empty placeholders; replace only when missing/empty.
        if not os.getenv(key):
            os.environ[key] = value


def main() -> int:
    load_dotenv(Path(__file__).resolve().parents[2] / ".env")

    api_key = os.getenv("BYBIT_API_KEY", "")
    # Backward-compatible fallback for typoed key name found in local .env.
    api_secret = os.getenv("BYBIT_API_SECRET", "") or os.getenv("BYBIT_SECTRET", "")
    if not api_key or not api_secret:
        print("RESULT: FAILED - Missing BYBIT_API_KEY/BYBIT_API_SECRET")
        return 1

    testnet = str(os.getenv("BYBIT_TESTNET", "0")).lower() in {"1", "true", "yes", "on"}
    client = BybitV5Client(api_key, api_secret, testnet=testnet)

    category = "linear"
    symbol = "XRPUSDT"

    server_ms = client.get_server_time_ms()
    spec = client.get_instrument_spec(category=category, symbol=symbol)
    klines = client.get_kline(category=category, symbol=symbol, interval="1", limit=2)
    if not klines:
        print("RESULT: FAILED - No kline data returned")
        return 1

    last_close = float(klines[0][4])

    # Deliberately non-marketable buy price to avoid immediate execution.
    limit_price = floor_to_step(to_decimal(last_close * 0.85), spec.tick_size)

    # Keep notional above minimum by targeting ~10 USDT.
    target_notional = Decimal("10")
    qty = floor_to_step(target_notional / limit_price, spec.qty_step)
    if qty < spec.min_order_qty:
        qty = spec.min_order_qty

    payload = {
        "category": category,
        "symbol": symbol,
        "side": "Buy",
        "orderType": "Limit",
        "qty": fmt_decimal(qty),
        "price": fmt_decimal(limit_price),
        "timeInForce": "PostOnly",
        "positionIdx": 0,
    }

    create_resp = client.create_order(payload)
    order_id = create_resp.get("result", {}).get("orderId")
    if not order_id:
        print(f"RESULT: FAILED - Missing orderId in response: {create_resp}")
        return 1

    open_orders = client.get_open_orders(category=category, symbol=symbol, open_only=0)
    listed = any(str(o.get("orderId")) == str(order_id) for o in open_orders)

    cancel_resp = client.cancel_order({
        "category": category,
        "symbol": symbol,
        "orderId": order_id,
    })

    open_after = client.get_open_orders(category=category, symbol=symbol, open_only=0)
    still_open = any(str(o.get("orderId")) == str(order_id) for o in open_after)

    print("BYBIT ACCESS: OK")
    print(f"TESTNET: {testnet}")
    print(f"SERVER_TIME_MS: {server_ms}")
    print(f"SYMBOL: {symbol}")
    print(f"LAST_CLOSE: {last_close}")
    print(f"TEST_ORDER_ID: {order_id}")
    print(f"OPEN_LISTED_BEFORE_CANCEL: {listed}")
    print(f"CANCEL_RET_CODE: {cancel_resp.get('retCode', 'n/a')}")
    print(f"OPEN_AFTER_CANCEL: {still_open}")

    if still_open:
        print("RESULT: WARNING - order still open, check manually")
        return 2

    print("RESULT: SUCCESS - placed and canceled non-marketable order")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
