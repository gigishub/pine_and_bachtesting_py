"""Unit tests for the setup KDE lower indicator."""

from __future__ import annotations

import pandas as pd

from bear_strategy.hypothesis_test_v2.setup.indicators.kde_lower import signal as kde_lower_signal


def test_kde_lower_first_5_bars_only() -> None:
    idx = pd.date_range("2021-01-01", periods=26, freq="D")
    closes = pd.Series(
        [100.0, 101.0, 99.0, 102.0, 98.0, 103.0, 97.0, 104.0, 96.0, 105.0,
         100.0, 101.0, 99.0, 102.0, 98.0, 103.0, 97.0, 104.0, 96.0, 105.0,
         90.0, 90.0, 90.0, 90.0, 90.0, 90.0],
        index=idx,
    )
    df = pd.DataFrame({"close": closes})

    result = kde_lower_signal(df, {"bandwidth": 0.15, "lookback_bars": 20, "max_bars": 5})

    assert result.dtype == bool
    assert result.iloc[:20].sum() == 0
    assert result.iloc[20:25].all(), "The first five below-lower-bar entries should be True"
    assert not result.iloc[25], "The sixth consecutive below-lower bar should be False"
