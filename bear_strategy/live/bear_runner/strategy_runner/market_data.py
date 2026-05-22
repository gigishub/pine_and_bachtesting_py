from __future__ import annotations

import time
from typing import Any

import pandas as pd

from UPS_py_v2.live.bybit_client import BybitV5Client
from ..config import BearLiveConfig


# Bybit 1h interval code
_INTERVAL_1H = "60"
# Bybit daily interval code
_INTERVAL_1D = "D"
# 1h bar duration in milliseconds
_INTERVAL_1H_MS = 3_600_000


def _kline_rows_to_df(rows: list[list[Any]], lowercase_cols: bool = True) -> pd.DataFrame:
    """Convert Bybit kline list (reverse-chron) to a UTC-indexed OHLCV DataFrame.

    Bybit returns rows as [timestamp_ms, open, high, low, close, volume, turnover].
    Output uses lowercase column names for consistency with bear strategy indicators.
    """
    rows_sorted = sorted(rows, key=lambda x: int(x[0]))
    records = [
        {
            "Timestamp": int(r[0]),
            "open": float(r[1]),
            "high": float(r[2]),
            "low": float(r[3]),
            "close": float(r[4]),
            "volume": float(r[5]),
        }
        for r in rows_sorted
    ]
    df = pd.DataFrame(records)
    df["Date"] = pd.to_datetime(df["Timestamp"], unit="ms", utc=True)
    return df.set_index("Date")[["open", "high", "low", "close", "volume", "Timestamp"]]


class BearMarketDataService:
    """Fetch and manage OHLCV and funding history for the bear live runner.

    Three datasets are maintained:
      - 1h OHLCV:        Entry timeframe data (VP + ATR + funding guard)
      - 1d OHLCV:        Regime timeframe data (RSI bear zone)
      - Funding rates:   8h funding settlements (bull guard)
    """

    def __init__(self, client: BybitV5Client, cfg: BearLiveConfig) -> None:
        self.client = client
        self.cfg = cfg

    # ── Timing ────────────────────────────────────────────────────────────────

    def sleep_until_next_1h_close(self) -> None:
        """Block until just after the next 1h bar closes."""
        server_ms = self.client.get_server_time_ms()
        remainder = server_ms % _INTERVAL_1H_MS
        wait_ms = _INTERVAL_1H_MS - remainder + self.cfg.poll_ahead_ms
        if wait_ms > 250:
            time.sleep((wait_ms - 150) / 1000)
        # Tight spin until the bar boundary passes
        while True:
            now_ms = self.client.get_server_time_ms()
            if (now_ms % _INTERVAL_1H_MS) <= self.cfg.poll_ahead_ms:
                break
            time.sleep(0.05)

    # ── REST fetches ──────────────────────────────────────────────────────────

    def fetch_ohlcv_1h(self, limit: int | None = None) -> pd.DataFrame:
        limit = limit or max(50, self.cfg.warmup_bars)
        rows = self.client.get_kline(
            category=self.cfg.category,
            symbol=self.cfg.symbol,
            interval=_INTERVAL_1H,
            limit=limit,
        )
        if not rows:
            raise RuntimeError(f"No 1h kline data returned for {self.cfg.symbol}")
        return _kline_rows_to_df(rows)

    def fetch_ohlcv_1d(self) -> pd.DataFrame:
        rows = self.client.get_kline(
            category=self.cfg.category,
            symbol=self.cfg.symbol,
            interval=_INTERVAL_1D,
            limit=self.cfg.warmup_bars_1d,
        )
        if not rows:
            raise RuntimeError(f"No 1d kline data returned for {self.cfg.symbol}")
        return _kline_rows_to_df(rows)

    def fetch_funding_history(self) -> pd.DataFrame:
        """Return a DataFrame with 'fundingrate' column indexed by UTC settlement time.

        The funding_bull_guard indicator requires:
          - DatetimeIndex (UTC)
          - 'fundingrate' column (float)
        """
        records = self.client.get_funding_rate_history(
            category=self.cfg.category,
            symbol=self.cfg.symbol,
            limit=self.cfg.warmup_bars_funding,
        )
        if not records:
            raise RuntimeError(f"No funding data returned for {self.cfg.symbol}")
        rows = [
            {
                "Date": pd.to_datetime(int(r["fundingRateTimestamp"]), unit="ms", utc=True),
                "fundingrate": float(r["fundingRate"]),
            }
            for r in records
        ]
        df = pd.DataFrame(rows).sort_values("Date").set_index("Date")
        return df

    # ── Bar management ────────────────────────────────────────────────────────

    def closed_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """Filter to confirmed closed bars only."""
        server_ms = self.client.get_server_time_ms()
        is_closed = (df["Timestamp"] + _INTERVAL_1H_MS) <= server_ms
        out = df[is_closed].copy()
        if out.empty:
            raise RuntimeError("No closed 1h candle available yet")
        return out

    def bootstrap_closed_history(self) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Fetch and return (df_1h_closed, df_1d, funding_df) for the WS warmup."""
        raw_1h = self.fetch_ohlcv_1h()
        closed_1h = self.closed_df(raw_1h)
        if len(closed_1h) > self.cfg.warmup_bars:
            closed_1h = closed_1h.tail(self.cfg.warmup_bars).copy()

        df_1d = self.fetch_ohlcv_1d()
        funding_df = self.fetch_funding_history()
        return closed_1h, df_1d, funding_df

    def append_closed_ws_kline(
        self,
        history: pd.DataFrame,
        row: dict[str, Any],
    ) -> pd.DataFrame:
        """Append one closed WS kline to the 1h history buffer."""
        start_ms = int(row["start"])
        date_idx = pd.to_datetime(start_ms, unit="ms", utc=True)
        new_row = pd.DataFrame(
            [
                {
                    "open": float(row["open"]),
                    "high": float(row["high"]),
                    "low": float(row["low"]),
                    "close": float(row["close"]),
                    "volume": float(row["volume"]),
                    "Timestamp": start_ms,
                }
            ],
            index=[date_idx],
        )
        merged = pd.concat([history, new_row])
        merged = merged[~merged.index.duplicated(keep="last")].sort_index()
        keep_n = max(300, self.cfg.warmup_bars + 20)
        return merged.tail(keep_n).copy()
