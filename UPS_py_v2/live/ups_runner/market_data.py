from __future__ import annotations

import time
from typing import Any

import pandas as pd

from ..bybit_client import BybitV5Client
from .config import LiveConfig


class LiveMarketDataService:
    """Handles candle timing and OHLCV history management for the live loop."""

    def __init__(self, client: BybitV5Client, cfg: LiveConfig, interval: str, interval_ms: int) -> None:
        self.client = client
        self.cfg = cfg
        self.interval = interval
        self.interval_ms = interval_ms

    def sleep_until_next_close(self) -> None:
        server_ms = self.client.get_server_time_ms()
        remainder = server_ms % self.interval_ms
        wait_ms = self.interval_ms - remainder + self.cfg.poll_ahead_ms
        if wait_ms > 250:
            time.sleep((wait_ms - 150) / 1000)
        while True:
            now_ms = self.client.get_server_time_ms()
            if (now_ms % self.interval_ms) <= self.cfg.poll_ahead_ms:
                break
            time.sleep(0.05)

    def fetch_ohlcv(self) -> pd.DataFrame:
        rows = self.client.get_kline(
            category=self.cfg.category,
            symbol=self.cfg.symbol,
            interval=self.interval,
            limit=max(50, self.cfg.warmup_bars),
        )
        if not rows:
            raise RuntimeError("No kline data returned")

        # Bybit returns reverse chronological list.
        rows_sorted = sorted(rows, key=lambda x: int(x[0]))
        records = []
        for row in rows_sorted:
            records.append(
                {
                    "Timestamp": int(row[0]),
                    "Open": float(row[1]),
                    "High": float(row[2]),
                    "Low": float(row[3]),
                    "Close": float(row[4]),
                    "Volume": float(row[5]),
                }
            )

        df = pd.DataFrame(records)
        df["Date"] = pd.to_datetime(df["Timestamp"], unit="ms", utc=True)
        return df.set_index("Date")[["Open", "High", "Low", "Close", "Volume", "Timestamp"]]

    def closed_df(self, df: pd.DataFrame) -> pd.DataFrame:
        server_ms = self.client.get_server_time_ms()
        is_closed = (df["Timestamp"] + self.interval_ms) <= server_ms
        out = df[is_closed].copy()
        if out.empty:
            raise RuntimeError("No closed candle available yet")
        return out

    def bootstrap_closed_history(self) -> pd.DataFrame:
        raw_df = self.fetch_ohlcv()
        closed_df = self.closed_df(raw_df)
        if len(closed_df) > self.cfg.warmup_bars:
            return closed_df.tail(self.cfg.warmup_bars).copy()
        return closed_df.copy()

    def append_closed_ws_kline(self, history: pd.DataFrame, row: dict[str, Any]) -> pd.DataFrame:
        start_ms = int(row["start"])
        date_idx = pd.to_datetime(start_ms, unit="ms", utc=True)
        new_row = pd.DataFrame(
            [
                {
                    "Open": float(row["open"]),
                    "High": float(row["high"]),
                    "Low": float(row["low"]),
                    "Close": float(row["close"]),
                    "Volume": float(row["volume"]),
                    "Timestamp": start_ms,
                }
            ],
            index=[date_idx],
        )

        merged = pd.concat([history, new_row])
        merged = merged[~merged.index.duplicated(keep="last")].sort_index()
        keep_n = max(300, self.cfg.warmup_bars + 20)
        return merged.tail(keep_n).copy()
