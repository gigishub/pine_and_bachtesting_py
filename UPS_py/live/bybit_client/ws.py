from __future__ import annotations

import json
import queue
import threading
import time
from typing import Any

try:
    import websocket
except ImportError:  # pragma: no cover - optional runtime dependency
    websocket = None


class BybitPublicKlineStream:
    """Public kline websocket stream for low-latency closed-candle processing."""

    def __init__(
        self,
        *,
        ws_url: str,
        symbol: str,
        interval: str,
        ping_every_s: int = 20,
        reconnect_delay_s: float = 2.0,
    ) -> None:
        if websocket is None:
            raise RuntimeError("Missing dependency: websocket-client. Install with `pip install websocket-client`")

        self.ws_url = ws_url
        self.symbol = symbol
        self.interval = interval
        self.ping_every_s = ping_every_s
        self.reconnect_delay_s = reconnect_delay_s

        self._closed_queue: queue.Queue[dict[str, Any]] = queue.Queue()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._last_emitted_start: int | None = None

    def _topic(self) -> str:
        return f"kline.{self.interval}.{self.symbol}"

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run_loop, name="bybit-kline-ws", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop_event.set()

    def get_next_closed_kline(self, timeout_s: float) -> dict[str, Any] | None:
        try:
            return self._closed_queue.get(timeout=timeout_s)
        except queue.Empty:
            return None

    def _run_loop(self) -> None:
        while not self._stop_event.is_set():
            hb_stop = threading.Event()

            def on_open(ws_app: websocket.WebSocketApp) -> None:
                sub = {"op": "subscribe", "args": [self._topic()]}
                ws_app.send(json.dumps(sub))

                def heartbeat() -> None:
                    while not hb_stop.is_set() and not self._stop_event.is_set():
                        try:
                            ws_app.send(json.dumps({"op": "ping"}))
                        except Exception:
                            break
                        hb_stop.wait(self.ping_every_s)

                threading.Thread(target=heartbeat, name="bybit-kline-ping", daemon=True).start()

            def on_message(_: websocket.WebSocketApp, message: str) -> None:
                try:
                    payload = json.loads(message)
                except json.JSONDecodeError:
                    return

                if payload.get("op") in {"ping", "pong", "auth", "subscribe"}:
                    return
                if payload.get("success") is not None and payload.get("op"):
                    return

                topic = str(payload.get("topic") or "")
                if not topic.startswith("kline."):
                    return

                for row in payload.get("data") or []:
                    if not bool(row.get("confirm")):
                        continue
                    start = int(row.get("start") or 0)
                    if start <= 0:
                        continue
                    if self._last_emitted_start is not None and start <= self._last_emitted_start:
                        continue
                    self._last_emitted_start = start
                    self._closed_queue.put(row)

            def on_error(_: websocket.WebSocketApp, __: Any) -> None:
                return

            def on_close(_: websocket.WebSocketApp, __: Any, ___: Any) -> None:
                hb_stop.set()

            ws_app = websocket.WebSocketApp(
                self.ws_url,
                on_open=on_open,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close,
            )

            try:
                ws_app.run_forever(skip_utf8_validation=True)
            except Exception:
                hb_stop.set()

            if self._stop_event.is_set():
                break
            time.sleep(self.reconnect_delay_s)
