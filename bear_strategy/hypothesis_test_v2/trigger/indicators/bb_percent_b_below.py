"""
Bollinger %B dropping below threshold trigger.

Fires when %B dips below a level such as 0.5.
"""
from __future__ import annotations

import pandas as pd


def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """Return True when Bollinger %B drops below a threshold."""
    try:
        import pandas_ta as pta
    except ImportError as exc:
        raise ImportError("pandas_ta is required for bb_percent_b_below; install with: pip install pandas-ta") from exc

    length = int(params.get("length", 20))
    std = float(params.get("std", 2.0))
    threshold = float(params.get("threshold", 0.5))

    bb = pta.bbands(df["close"], length=length, std=std)
    bbp_col = f"BBP_{length}_{std}"
    if bbp_col not in bb.columns:
        # Some pandas_ta versions may name the column differently.
        bbp_col = next((c for c in bb.columns if c.startswith("BBP_")), None)
        if bbp_col is None:
            raise ValueError("Could not locate Bollinger %B column in bbands output")

    bbp = bb[bbp_col]
    return (bbp < threshold).fillna(False)
