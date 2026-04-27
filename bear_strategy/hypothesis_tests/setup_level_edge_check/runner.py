"""Vectorized outcome engine for the setup level edge check (Step 2).

For every bar in each population, enters a short at the bar's close and
scans forward until stop or target resolution.

Stop   = entry + stop_mult  × ATR_1h
Target = entry - target_mult × ATR_1h

Populations per pair:
    all_regime        — baseline (all Step-1-regime candles)
    near_setup        — regime + within 0.5 × ATR_4H of VPVR HVN or AVWAP
    away_from_setup   — regime + eligible but NOT near any setup level
    vpvr_only         — regime + near VPVR HVN
    vwap_only         — regime + near anchored VWAP

Look-ahead prevention:
    All 4H signals are shifted by 1 completed bar before merging onto the
    1-hour grid (see _align_4h_to_1h).  ATR_4H, VPVR HVN, and
    Anchored VWAP are all subject to that single shift.
"""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pandas as pd

from bear_strategy.hypothesis_tests.setup_level_edge_check.config import TestConfig
from bear_strategy.hypothesis_tests.setup_level_edge_check.entries import (
    build_population_masks,
)
from bear_strategy.strategy.indicators.setup.anchored_vwap import compute_anchored_vwap
from bear_strategy.strategy.indicators.setup.atr_4h import compute_atr_4h
from bear_strategy.strategy.indicators.setup.vpvr_hvn import compute_vpvr_hvn
from bear_strategy.strategy.parameters import Parameters
from bear_strategy.strategy.signals import compute_regime_signals

logger = logging.getLogger(__name__)

_POPULATION_ORDER = [
    "all_regime",
    "near_setup",
    "away_from_setup",
    "vpvr_only",
    "vwap_only",
]


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def run_test(config: TestConfig) -> pd.DataFrame:
    """Run the setup level edge check across all configured pairs.

    Args:
        config: TestConfig instance.

    Returns:
        DataFrame with columns (pair, population, win_rate, profit_factor,
        avg_duration, n_trades), indexed by (pair, population).
    """
    params = Parameters(
        ema_slope_period=config.ema_slope_period,
        ema_slope_lookback=config.ema_slope_lookback,
        ema_below_periods=config.ema_below_periods,
    )

    records: list[dict] = []
    for pair in config.pairs:
        logger.info("Processing %s", pair)
        try:
            records.extend(_process_pair(pair, config, params))
        except FileNotFoundError as exc:
            logger.warning("Skipping %s — data not found: %s", pair, exc)
        except Exception as exc:
            logger.error("Error processing %s: %s", pair, exc, exc_info=True)
            raise

    if not records:
        return pd.DataFrame(
            columns=["pair", "population", "win_rate", "profit_factor", "avg_duration", "n_trades"]
        )

    return pd.DataFrame(records).set_index(["pair", "population"])


# ---------------------------------------------------------------------------
# Per-pair processing
# ---------------------------------------------------------------------------


def _process_pair(
    pair: str,
    config: TestConfig,
    params: Parameters,
) -> list[dict]:
    df_1h = _load_parquet(config.data_dir, pair, config.entry_tf, config.start_date, config.end_date)
    df_4h = _load_parquet(config.data_dir, pair, config.context_tf, config.start_date, config.end_date)
    df_daily = _load_parquet(config.data_dir, pair, "1d", config.start_date, config.end_date)

    df_1h = _standardise_ohlcv(df_1h)
    df_4h = _standardise_ohlcv(df_4h)
    df_daily = _standardise_ohlcv(df_daily)

    # Regime signals onto 1h (same as Step 1 logic)
    regime = compute_regime_signals(df_1h, df_daily, params)
    df_1h = df_1h.copy()
    for col, series in regime.items():
        df_1h[col] = series.values

    # 4H indicators (pure, unshifted)
    df_4h_signals = pd.DataFrame(
        {
            "atr_4h": compute_atr_4h(df_4h, config.atr_4h_period),
            "vpvr_hvn": compute_vpvr_hvn(df_4h, config.vpvr_window, config.vpvr_bins),
            "anchored_vwap": compute_anchored_vwap(
                df_4h, config.swing_lookback, config.swing_confirmation_bars
            ),
        },
        index=df_4h.index,
    )

    # Align 4H → 1h with 1-bar shift (prevents any current-bar lookahead)
    aligned = _align_4h_to_1h(df_1h, df_4h_signals)
    for col in ("atr_4h", "vpvr_hvn", "anchored_vwap"):
        df_1h[col] = aligned[col].values

    # 1h ATR for stop/target sizing
    df_1h["atr"] = _atr(df_1h, config.atr_period).values

    masks = build_population_masks(df_1h, config)

    records = []
    for pop_name in _POPULATION_ORDER:
        mask = masks[pop_name]
        result = _compute_outcomes(df_1h, mask, config)
        records.append({"pair": pair, "population": pop_name, **result})
        logger.debug(
            "%s | %-18s | trades=%d  win=%.1f%%  PF=%.2f  dur=%.1f bars",
            pair,
            pop_name,
            result["n_trades"],
            result["win_rate"] * 100 if not np.isnan(result["win_rate"]) else float("nan"),
            result["profit_factor"],
            result["avg_duration"],
        )

    return records


# ---------------------------------------------------------------------------
# 4H → 1h alignment
# ---------------------------------------------------------------------------


def _align_4h_to_1h(
    df_1h: pd.DataFrame,
    df_4h_signals: pd.DataFrame,
) -> pd.DataFrame:
    """Forward-fill 4H signals onto the 1-hour grid.

    Shifts ALL 4H signals by 1 completed bar before merging so that every
    1-hour bar sees only fully closed 4H bar data — regardless of whether
    the 4H timestamp represents bar open or bar close time in the parquet.

    Args:
        df_1h: 1h DataFrame with a sorted DatetimeIndex.
        df_4h_signals: DataFrame of 4H signals indexed by the same convention.

    Returns:
        DataFrame indexed like df_1h with 4H signal columns forward-filled.
    """
    # Shift by 1: at row t, the value now reflects bar t-1 (previously closed)
    shifted = df_4h_signals.shift(1)

    aligned = pd.merge_asof(
        df_1h[[]].sort_index(),
        shifted.sort_index(),
        left_index=True,
        right_index=True,
        direction="backward",
    )
    return aligned


# ---------------------------------------------------------------------------
# Outcome engine (identical forward-scan logic as Step 1)
# ---------------------------------------------------------------------------


def _compute_outcomes(
    df: pd.DataFrame,
    entry_mask: pd.Series,
    config: TestConfig,
) -> dict:
    """Vectorized forward-scan outcome engine.

    Enters a short at every True bar's close.  Scans forward until stop
    (entry + stop_mult × ATR_1h) or target (entry - target_mult × ATR_1h).
    Ties on the same bar resolve as losses (conservative).
    Unresolved trades (data ends) are excluded.

    Returns dict with win_rate, profit_factor, avg_duration, n_trades.
    """
    closes = df["Close"].to_numpy(dtype=float)
    highs = df["High"].to_numpy(dtype=float)
    lows = df["Low"].to_numpy(dtype=float)
    atrs = df["atr"].to_numpy(dtype=float)
    mask_arr = entry_mask.to_numpy(dtype=bool)

    entry_indices = np.where(mask_arr)[0]
    wins: list[float] = []
    losses: list[float] = []
    durations: list[int] = []

    for idx in entry_indices:
        if np.isnan(atrs[idx]) or atrs[idx] == 0:
            continue
        entry_price = closes[idx]
        stop = entry_price + config.stop_atr_mult * atrs[idx]
        target = entry_price - config.target_atr_mult * atrs[idx]

        resolved = False
        for fwd in range(1, len(closes) - idx):
            bar = idx + fwd
            if highs[bar] >= stop:
                losses.append(config.stop_atr_mult)
                durations.append(fwd)
                resolved = True
                break
            if lows[bar] <= target:
                wins.append(config.target_atr_mult)
                durations.append(fwd)
                resolved = True
                break

        if not resolved:
            continue

    n_wins = len(wins)
    n_losses = len(losses)
    n_trades = n_wins + n_losses

    if n_trades == 0:
        return {
            "win_rate": float("nan"),
            "profit_factor": float("nan"),
            "avg_duration": float("nan"),
            "n_trades": 0,
        }

    win_rate = n_wins / n_trades
    profit_factor = sum(wins) / sum(losses) if losses else float("inf")
    avg_duration = sum(durations) / len(durations)

    return {
        "win_rate": win_rate,
        "profit_factor": profit_factor,
        "avg_duration": avg_duration,
        "n_trades": n_trades,
    }


# ---------------------------------------------------------------------------
# Data loading helpers (same as Step 1)
# ---------------------------------------------------------------------------


def _load_parquet(
    data_dir: Path,
    symbol: str,
    timeframe: str,
    start_date: str,
    end_date: str,
) -> pd.DataFrame:
    symbol_dir = data_dir / symbol
    if not symbol_dir.exists():
        raise FileNotFoundError(f"No data directory for {symbol}: {symbol_dir}")

    exact = symbol_dir / f"{symbol}_{timeframe}_start_{start_date}_end_{end_date}.parquet"
    if exact.exists():
        return pd.read_parquet(exact)

    candidates = sorted(symbol_dir.glob(f"{symbol}_{timeframe}_*.parquet"))
    if not candidates:
        raise FileNotFoundError(
            f"No parquet file for {symbol}/{timeframe} in {symbol_dir}."
        )

    path = candidates[0]
    logger.debug("Exact file not found; using %s", path.name)
    return pd.read_parquet(path)


def _standardise_ohlcv(df: pd.DataFrame) -> pd.DataFrame:
    rename_map = {
        "open": "Open", "high": "High", "low": "Low",
        "close": "Close", "volume": "Volume",
        "Open time": "timestamp", "open_time": "timestamp",
    }
    df = df.rename(columns=rename_map)
    if not isinstance(df.index, pd.DatetimeIndex):
        for col in ("timestamp", "date", "Datetime"):
            if col in df.columns:
                df = df.set_index(pd.to_datetime(df[col])).drop(columns=[col], errors="ignore")
                break
    return df.sort_index()


def _atr(df: pd.DataFrame, period: int) -> pd.Series:
    high = df["High"]
    low = df["Low"]
    prev_close = df["Close"].shift(1)
    tr = pd.concat(
        [high - low, (high - prev_close).abs(), (low - prev_close).abs()],
        axis=1,
    ).max(axis=1)
    return tr.ewm(span=period, adjust=False).mean()
