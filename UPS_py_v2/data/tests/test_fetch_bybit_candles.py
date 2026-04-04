from __future__ import annotations

import pandas as pd

from UPS_py_v2.data import fetch_bybit_candles as module


def test_fetch_all_bybit_candles_handles_descending_chunks(monkeypatch) -> None:
    step_ms = 60 * 60 * 1000
    start_ts = 1735689600000  # 2025-01-01 00:00:00 UTC

    first_chunk = [
        [str(start_ts + offset * step_ms), str(offset), str(offset), str(offset), str(offset), str(offset), "0"]
        for offset in range(199, -1, -1)
    ]
    second_chunk = [
        [str(start_ts + 201 * step_ms), "201", "201", "201", "201", "201", "0"],
        [str(start_ts + 200 * step_ms), "200", "200", "200", "200", "200", "0"],
    ]

    calls: list[tuple[str | None, str | None]] = []

    def fake_fetch(symbol, market_type, timeframe, start_time, end_time):
        calls.append((start_time, end_time))
        if len(calls) == 1:
            return first_chunk
        if len(calls) == 2:
            return second_chunk
        return []

    monkeypatch.setattr(module, "fetch_bybit_candles_chunk", fake_fetch)

    df = module.fetch_all_bybit_candles(
        symbol="BTCUSDT",
        market_type="futures",
        timeframe="1h",
        start_time="2025-01-01 00:00:00",
        end_time="2025-01-09 09:00:00",
    )

    assert len(calls) == 2
    assert len(df) == 202
    assert list(df["Close"].head(3)) == [0.0, 1.0, 2.0]
    assert list(df["Close"].tail(3)) == [199.0, 200.0, 201.0]
    assert df.index[0] == pd.Timestamp("2025-01-01 00:00:00+00:00")
    assert df.index[-1] == pd.Timestamp("2025-01-09 09:00:00+00:00")