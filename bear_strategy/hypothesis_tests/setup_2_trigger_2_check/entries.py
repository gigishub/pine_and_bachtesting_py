"""Population masks for Setup 2 – Trigger 2: momentum-flip crossover signals.

Baseline: regime AND kde_upper (4h). All populations are strict subsets.

All six signals are instantaneous crossover conditions — no state machine.
They are computed purely from the entry-TF OHLCV and tested on the same bar.

No-lookahead guarantee:
    The aligned 4h kde_upper gate originates from runner.py where the 4h KDE
    output is .shift(1) before merge_asof alignment.
    All crossover conditions use .shift(1) on the prior-bar value — no
    forward-looking data is accessed.

Signal definitions
──────────────────
cmf_cross     : CMF(period) crosses below 0
willr_cross   : Williams %R(period) crosses below threshold (default -20)
roc_cross     : ROC(period) crosses below 0
trix_cross    : TRIX(period) crosses below signal(signal_period) from above 0
fisher_cross  : Fisher(period) drops below Fisher.shift(1) while prior > extreme
ema_cross     : Close crosses below EMA(ema_cross_period)
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from bear_strategy.hypothesis_tests.setup_2_trigger_2_check.config import TestConfig


def build_population_masks(
    df: pd.DataFrame,
    config: TestConfig,
) -> dict[str, pd.Series]:
    """Return one boolean mask per population.

    Args:
        df: Entry-TF DataFrame with regime, atr, kde_upper (bool), and OHLCV.
        config: TestConfig instance.

    Returns:
        dict mapping population name -> boolean pd.Series on df's index.
    """
    _require_columns(
        df,
        [config.regime_col, "Open", "High", "Low", "Close", "Volume", "atr", "kde_upper"],
    )

    regime    = df[config.regime_col].astype(bool)
    kde_upper = df["kde_upper"].infer_objects(copy=False).fillna(False).astype(bool)
    atr       = df["atr"]

    baseline = regime & kde_upper & atr.notna()

    h  = df["High"]
    lo = df["Low"]
    c  = df["Close"]
    v  = df["Volume"]

    # ------------------------------------------------------------------
    # 1. CMF cross below 0
    # ------------------------------------------------------------------
    cmf   = _compute_cmf(h, lo, c, v, config.cmf_period)
    cmf_cross = (cmf < 0) & (cmf.shift(1) >= 0)

    # ------------------------------------------------------------------
    # 2. Williams %R cross below threshold
    # ------------------------------------------------------------------
    willr       = _compute_willr(h, lo, c, config.willr_period)
    willr_cross = (willr < config.willr_threshold) & (willr.shift(1) >= config.willr_threshold)

    # ------------------------------------------------------------------
    # 3. ROC cross below 0
    # ------------------------------------------------------------------
    roc       = _compute_roc(c, config.roc_period)
    roc_cross = (roc < 0) & (roc.shift(1) >= 0)

    # ------------------------------------------------------------------
    # 4. TRIX signal-line cross from above 0
    # ------------------------------------------------------------------
    trix, trix_signal = _compute_trix(c, config.trix_period, config.trix_signal_period)
    trix_cross = (
        (trix < trix_signal)
        & (trix.shift(1) >= trix_signal.shift(1))
        & (trix.shift(1) > 0)  # was rolling over from a positive peak
    )

    # ------------------------------------------------------------------
    # 5. Fisher Transform trigger cross from extreme high
    # ------------------------------------------------------------------
    fisher        = _compute_fisher(h, lo, config.fisher_period)
    fisher_trigger = fisher.shift(1)
    fisher_cross  = (fisher < fisher_trigger) & (fisher_trigger > config.fisher_extreme)

    # ------------------------------------------------------------------
    # 6. Price crosses below EMA
    # ------------------------------------------------------------------
    ema       = c.ewm(span=config.ema_cross_period, adjust=False).mean()
    ema_cross = (c < ema) & (c.shift(1) >= ema.shift(1))

    return {
        "kde_upper_baseline": baseline,
        "cmf_cross":          baseline & cmf_cross,
        "willr_cross":        baseline & willr_cross,
        "roc_cross":          baseline & roc_cross,
        "trix_cross":         baseline & trix_cross,
        "fisher_cross":       baseline & fisher_cross,
        "ema_cross":          baseline & ema_cross,
    }


# ---------------------------------------------------------------------------
# Indicator helpers
# ---------------------------------------------------------------------------


def _compute_cmf(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    volume: pd.Series,
    period: int,
) -> pd.Series:
    """Chaikin Money Flow: rolling sum(MFV) / rolling sum(volume)."""
    hl_range = (high - low).replace(0, np.nan)
    mfm = ((close - low) - (high - close)) / hl_range
    mfv = mfm * volume
    return (
        mfv.rolling(period, min_periods=period).sum()
        / volume.rolling(period, min_periods=period).sum()
    )


def _compute_willr(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    period: int,
) -> pd.Series:
    """Williams %R: -100 × (HH - close) / (HH - LL). Range [0, -100]."""
    hh = high.rolling(period, min_periods=period).max()
    ll = low.rolling(period, min_periods=period).min()
    denom = (hh - ll).replace(0, np.nan)
    return -100.0 * (hh - close) / denom


def _compute_roc(close: pd.Series, period: int) -> pd.Series:
    """Rate of Change: (close / close.shift(period) - 1) × 100."""
    prev = close.shift(period)
    return ((close - prev) / prev.replace(0, np.nan)) * 100.0


def _compute_trix(
    close: pd.Series,
    period: int,
    signal_period: int,
) -> tuple[pd.Series, pd.Series]:
    """TRIX = pct_change of triple EMA × 100. Signal = EMA of TRIX."""
    ema1 = close.ewm(span=period, adjust=False).mean()
    ema2 = ema1.ewm(span=period, adjust=False).mean()
    ema3 = ema2.ewm(span=period, adjust=False).mean()
    trix = ema3.pct_change() * 100.0
    signal = trix.ewm(span=signal_period, adjust=False).mean()
    return trix, signal


def _compute_fisher(
    high: pd.Series,
    low: pd.Series,
    period: int,
) -> pd.Series:
    """Fisher Transform: converts hl2 into a Gaussian-distributed oscillator."""
    hl2 = (high + low) / 2.0
    hh  = hl2.rolling(period, min_periods=period).max()
    ll  = hl2.rolling(period, min_periods=period).min()
    denom = (hh - ll).replace(0, np.nan)
    value = (2.0 * (hl2 - ll) / denom - 1.0).clip(-0.999, 0.999)
    return 0.5 * np.log((1.0 + value) / (1.0 - value))


def _require_columns(df: pd.DataFrame, cols: list[str]) -> None:
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(
            f"DataFrame is missing required columns: {missing}. "
            "Ensure runner._process_pair() attaches all signals first."
        )
