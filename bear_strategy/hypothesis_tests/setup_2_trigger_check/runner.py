"""Vectorized outcome engine for Setup 2 Trigger: KDE Upper (4h) + 15m signals.

Entry TF  : 15m
KDE TF    : 4h  (shifted 1 completed 4h bar, forward-filled to 15m)
Reference : 1d  (VPVR HVN shifted 1 day, forward-filled to 15m)
                (daily VWAP computed on 15m bars, resets at midnight)
RVOL      : 15m rolling window (default 96 bars = 24h)

Baseline  : regime AND kde_upper — all populations are subsets of this.
"""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pandas as pd

from bear_strategy.hypothesis_tests.setup_kde_edge_check.entries import _compute_kde_signals
from bear_strategy.hypothesis_tests.setup_2_trigger_check.config import TestConfig
from bear_strategy.hypothesis_tests.setup_2_trigger_check.entries import build_population_masks
from bear_strategy.strategy.indicators.setup.vpvr_hvn import compute_vpvr_hvn
from bear_strategy.strategy.signals import compute_regime_signals
from bear_strategy.strategy.parameters import Parameters

logger = logging.getLogger(__name__)

_POPULATION_ORDER = [
    "kde_upper_baseline",
    "vwap_only",
    "vpvr_only",
    "near_setup",
    "rvol_only",
    "vwap_and_rvol",
    "vpvr_and_rvol",
    "near_and_rvol",
]


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def run_test(config: TestConfig) -> pd.DataFrame:
    """Run the setup 2 trigger check across all configured pairs."""
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
    df_entry = _load_parquet(config.data_dir, pair, config.entry_tf, config.start_date, config.end_date)
    df_4h = _load_parquet(config.data_dir, pair, config.kde_tf, config.start_date, config.end_date)
    df_daily = _load_parquet(config.data_dir, pair, config.context_tf, config.start_date, config.end_date)

    df_entry = _standardise_ohlcv(df_entry)
    df_4h = _standardise_ohlcv(df_4h)
    df_daily = _standardise_ohlcv(df_daily)

    # Regime computed on 15m bars with 1d reference
    regime = compute_regime_signals(df_entry, df_daily, params)
    df_entry = df_entry.copy()
    for col, series in regime.items():
        df_entry[col] = series.values

    # ATR on 15m bars — used for stop/target sizing and proximity threshold
    df_entry["atr"] = _atr(df_entry, config.atr_period).values

    # VPVR HVN from 1d bars: shift 1 day then align to 15m
    vpvr_1d = compute_vpvr_hvn(df_daily, config.vpvr_window, config.vpvr_n_bins)
    aligned_vpvr = _align_to_entry_tf(df_entry, vpvr_1d.shift(1).rename("vpvr_hvn_1d"))
    df_entry["vpvr_hvn_1d"] = aligned_vpvr.values

    # KDE signals on 4h bars: compute, shift 1 bar, align to 15m
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
    kde_upper_4h = pd.Series(
        kde_result["setup_active_upper"], index=df_4h.index, name="kde_upper"
    ).shift(1).to_frame()

    aligned_kde = _align_to_entry_tf(df_entry, kde_upper_4h)
    df_entry["kde_upper"] = aligned_kde["kde_upper"].values

    masks = build_population_masks(df_entry, config)

    records = []
    for pop_name in _POPULATION_ORDER:
        mask = masks[pop_name]
        result = _compute_outcomes(df_entry, mask, config)
        records.append({"pair": pair, "population": pop_name, **result})
        logger.debug(
            "%s | %-22s | trades=%d  win=%.1f%%  PF=%.2f  dur=%.1f bars",
            pair,
            pop_name,
            result["n_trades"],
            result["win_rate"] * 100 if not np.isnan(result["win_rate"]) else float("nan"),
            result["profit_factor"],
            result["avg_duration"],
        )

    return records


# ---------------------------------------------------------------------------
# Higher-TF -> entry-TF alignment
# ---------------------------------------------------------------------------


def _align_to_entry_tf(
    df_entry: pd.DataFrame,
    series_or_df,
) -> pd.DataFrame:
    """Forward-fill a higher-TF signal onto the entry-TF grid via merge_asof."""
    if isinstance(series_or_df, pd.Series):
        right = series_or_df.to_frame().sort_index()
    else:
        right = series_or_df.sort_index()

    return pd.merge_asof(
        df_entry[[]].sort_index(),
        right,
        left_index=True,
        right_index=True,
        direction="backward",
    )


# ---------------------------------------------------------------------------
# Outcome engine
# ---------------------------------------------------------------------------


def _compute_outcomes(
    df: pd.DataFrame,
    entry_mask: pd.Series,
    config: TestConfig,
) -> dict:
    """Vectorized forward-scan: short at entry bar close, exit at ATR stop/target."""
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

        for fwd in range(1, len(closes) - idx):
            bar = idx + fwd
            if highs[bar] >= stop:
                losses.append(config.stop_atr_mult)
                durations.append(fwd)
                break
            if lows[bar] <= target:
                wins.append(config.target_atr_mult)
                durations.append(fwd)
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

    return {
        "win_rate": n_wins / n_trades,
        "profit_factor": sum(wins) / sum(losses) if losses else float("inf"),
        "avg_duration": sum(durations) / len(durations),
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
