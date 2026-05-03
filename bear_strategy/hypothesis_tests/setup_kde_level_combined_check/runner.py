"""Vectorized outcome engine for the KDE + Level Proximity Combined Check.

Entry TF  : 1h
KDE TF    : 4h  (KDE gate computed on 4h bars, shifted 1 bar, aligned to 1h)
Reference : 1d  (VPVR HVN computed from trailing 1d bars, shifted 1 bar)
                (daily VWAP computed directly on 1h bars, reset at midnight)

Look-ahead prevention:
    4h KDE signals are computed on 4h bars, shifted by 1 completed 4h bar,
    then forward-filled onto the 1h grid via merge_asof.
    VPVR HVN is computed on 1d bars, shifted by 1 daily bar, then
    forward-filled to 1h.
    Daily VWAP accumulates within each calendar day -- fully causal.
"""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pandas as pd

from bear_strategy.hypothesis_tests.setup_kde_edge_check.entries import _compute_kde_signals
from bear_strategy.hypothesis_tests.setup_kde_level_combined_check.config import TestConfig
from bear_strategy.hypothesis_tests.setup_kde_level_combined_check.entries import (
    build_population_masks,
)
from bear_strategy.strategy.indicators.setup.vpvr_hvn import compute_vpvr_hvn
from bear_strategy.strategy.signals import compute_regime_signals
from bear_strategy.strategy.parameters import Parameters

logger = logging.getLogger(__name__)

_POPULATION_ORDER = [
    "regime_only",
    "kde_gate",
    "kde_upper",
    "kde_lower_fresh",
    "vwap_only",
    "vpvr_only",
    "near_setup",
    "kde_gate_and_vwap",
    "kde_gate_and_vpvr",
    "kde_gate_and_near",
    "kde_upper_and_vwap",
    "kde_upper_and_vpvr",
    "kde_upper_and_near",
    "kde_lower_and_vwap",
    "kde_lower_and_vpvr",
    "kde_lower_and_near",
]


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def run_test(config: TestConfig) -> pd.DataFrame:
    """Run the combined KDE + level check across all configured pairs.

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
            logger.warning("Skipping %s -- data not found: %s", pair, exc)
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
    df_4h = _load_parquet(config.data_dir, pair, config.kde_tf, config.start_date, config.end_date)
    df_daily = _load_parquet(config.data_dir, pair, config.context_tf, config.start_date, config.end_date)

    df_1h = _standardise_ohlcv(df_1h)
    df_4h = _standardise_ohlcv(df_4h)
    df_daily = _standardise_ohlcv(df_daily)

    # Regime signals on 1h (uses 1d daily for EMA slope reference)
    regime = compute_regime_signals(df_1h, df_daily, params)
    df_1h = df_1h.copy()
    for col, series in regime.items():
        df_1h[col] = series.values

    # 1h ATR for stop/target sizing and proximity threshold
    df_1h["atr"] = _atr(df_1h, config.atr_period).values

    # VPVR HVN from 1d bars: shift by 1 daily bar then align to 1h
    vpvr_1d = compute_vpvr_hvn(df_daily, config.vpvr_window, config.vpvr_n_bins)
    aligned_vpvr = _align_higher_to_1h(df_1h, vpvr_1d.shift(1).rename("vpvr_hvn_1d"))
    df_1h["vpvr_hvn_1d"] = aligned_vpvr.values

    # KDE signals on 4h bars: compute, shift by 1 4h bar, align to 1h
    kde_result = _compute_kde_signals(
        close=df_4h["Close"].to_numpy(dtype=float),
        open_=df_4h["Open"].to_numpy(dtype=float),
        window=config.kde_window,
        bandwidth_mult=config.kde_bandwidth_mult,
        kde_n_points=config.kde_n_points,
        value_area_pct=config.kde_value_area_pct,
        lower_duration=config.kde_lower_duration,
        index=df_4h.index,
    )
    df_4h_kde = pd.DataFrame(
        {
            "kde_upper": kde_result["setup_active_upper"],
            "kde_lower_fresh": kde_result["setup_active_lower"],
        },
        index=df_4h.index,
    )
    # Shift by 1 completed 4h bar before aligning to prevent lookahead
    df_4h_kde_shifted = df_4h_kde.shift(1)

    aligned_kde = _align_higher_to_1h(df_1h, df_4h_kde_shifted)
    df_1h["kde_upper"] = aligned_kde["kde_upper"].values
    df_1h["kde_lower_fresh"] = aligned_kde["kde_lower_fresh"].values

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
# Higher-TF -> 1h alignment
# ---------------------------------------------------------------------------


def _align_higher_to_1h(
    df_1h: pd.DataFrame,
    series_or_df,
) -> pd.DataFrame:
    """Forward-fill a higher-TF signal onto the 1-hour grid via merge_asof.

    Args:
        df_1h: 1h DataFrame with sorted DatetimeIndex.
        series_or_df: pd.Series or pd.DataFrame (already shifted) with
            sorted DatetimeIndex.

    Returns:
        DataFrame (or single-column DF) indexed like df_1h, forward-filled.
    """
    if isinstance(series_or_df, pd.Series):
        right = series_or_df.to_frame().sort_index()
    else:
        right = series_or_df.sort_index()

    merged = pd.merge_asof(
        df_1h[[]].sort_index(),
        right,
        left_index=True,
        right_index=True,
        direction="backward",
    )
    return merged


# ---------------------------------------------------------------------------
# Outcome engine
# ---------------------------------------------------------------------------


def _compute_outcomes(
    df: pd.DataFrame,
    entry_mask: pd.Series,
    config: TestConfig,
) -> dict:
    """Vectorized forward-scan outcome engine.

    Enters a short at every True bar's close. Scans forward until stop
    (entry + stop_mult * ATR_1h) or target (entry - target_mult * ATR_1h).
    Unresolved trades (data ends) are excluded.
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
# Data helpers
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
    return pd.read_parquet(candidates[0])


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
