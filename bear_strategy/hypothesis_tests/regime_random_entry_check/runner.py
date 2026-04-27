"""Vectorized outcome engine for the regime random-entry falsification test.

For every bar in a population, enters a short at the bar's close and
scans forward until either:
  - price touches the stop level  (entry + stop_mult × ATR)   → loss
  - price touches the target level (entry - target_mult × ATR) → win
  - the data ends without resolution                           → excluded

Metrics computed per population per pair:
  win_rate       — fraction of resolved trades that hit target first
  profit_factor  — gross wins / gross losses (in ATR units; symmetric stops
                   and targets make this independent of position size)
  avg_duration   — mean bars held until resolution
  n_trades       — number of resolved trades
"""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pandas as pd

from bear_strategy.hypothesis_tests.regime_random_entry_check.config import TestConfig
from bear_strategy.hypothesis_tests.regime_random_entry_check.entries import (
    build_population_masks,
)
from bear_strategy.strategy.parameters import Parameters
from bear_strategy.strategy.signals import compute_regime_signals

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def run_test(config: TestConfig) -> pd.DataFrame:
    """Run the regime random-entry check across all configured pairs.

    Args:
        config: TestConfig with pairs, date range, ATR multiples, etc.

    Returns:
        DataFrame indexed by (pair, population) with columns:
        win_rate, profit_factor, avg_duration, n_trades.
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
            pair_records = _process_pair(pair, config, params)
            records.extend(pair_records)
        except FileNotFoundError as exc:
            logger.warning("Skipping %s — data not found: %s", pair, exc)
        except Exception as exc:
            logger.error("Error processing %s: %s", pair, exc, exc_info=True)
            raise

    if not records:
        return pd.DataFrame(
            columns=["pair", "population", "win_rate", "profit_factor", "avg_duration", "n_trades"]
        )

    df = pd.DataFrame(records).set_index(["pair", "population"])
    return df


# ---------------------------------------------------------------------------
# Per-pair processing
# ---------------------------------------------------------------------------


def _process_pair(pair: str, config: TestConfig, params: Parameters) -> list[dict]:
    df_15m = _load_parquet(config.data_dir, pair, "15m", config.start_date, config.end_date)
    df_daily = _load_parquet(config.data_dir, pair, "1d", config.start_date, config.end_date)

    df_15m = _standardise_ohlcv(df_15m)
    df_daily = _standardise_ohlcv(df_daily)

    # Compute regime signals and attach to the 15-min frame
    regime = compute_regime_signals(df_15m, df_daily, params)
    df_15m = df_15m.copy()
    for col, series in regime.items():
        df_15m[col] = series.values

    # ATR on 15-min data (used for stop and target sizing)
    atr_15m = _atr(df_15m, config.atr_period)
    df_15m["atr"] = atr_15m.values

    masks = build_population_masks(df_15m, config.ema_slope_period, config.ema_below_periods)
    population_names = (
        ["all_candles", f"ema_{config.ema_slope_period}_slope"]
        + [f"ema_below_{p}" for p in config.ema_below_periods]
        + [f"ema_{config.ema_slope_period}_slope_and_below_{p}" for p in config.ema_below_periods]
    )

    records = []
    for pop_name in population_names:
        mask = masks[pop_name]
        result = _compute_outcomes(df_15m, mask, config)
        records.append(
            {
                "pair": pair,
                "population": pop_name,
                **result,
            }
        )
        logger.debug(
            "%s | %-14s | trades=%d  win=%.1f%%  PF=%.2f  dur=%.1f bars",
            pair,
            pop_name,
            result["n_trades"],
            result["win_rate"] * 100,
            result["profit_factor"],
            result["avg_duration"],
        )

    return records


# ---------------------------------------------------------------------------
# Outcome computation
# ---------------------------------------------------------------------------


def _compute_outcomes(
    df: pd.DataFrame,
    entry_mask: pd.Series,
    config: TestConfig,
) -> dict:
    """Vectorize forward-scan for all entry bars in the mask.

    Each entry is a short at the bar's close price.  We scan forward bar by
    bar and stop when the low ≤ target or the high ≥ stop.  Ties (both hit
    on the same bar) are resolved as a loss (conservative).

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
        stop_level = entry_price + config.stop_atr_mult * atrs[idx]
        target_level = entry_price - config.target_atr_mult * atrs[idx]

        resolved = False
        for fwd in range(1, len(closes) - idx):
            bar = idx + fwd
            # Stop hit (loss) takes priority on the same bar
            if highs[bar] >= stop_level:
                losses.append(config.stop_atr_mult)
                durations.append(fwd)
                resolved = True
                break
            if lows[bar] <= target_level:
                wins.append(config.target_atr_mult)
                durations.append(fwd)
                resolved = True
                break

        # Unresolved trades (end of data) are excluded from statistics
        if not resolved:
            continue

    n_wins = len(wins)
    n_losses = len(losses)
    n_trades = n_wins + n_losses

    if n_trades == 0:
        return {"win_rate": float("nan"), "profit_factor": float("nan"), "avg_duration": float("nan"), "n_trades": 0}

    win_rate = n_wins / n_trades
    gross_wins = sum(wins)
    gross_losses = sum(losses)
    profit_factor = gross_wins / gross_losses if gross_losses > 0 else float("inf")
    avg_duration = sum(durations) / len(durations)

    return {
        "win_rate": win_rate,
        "profit_factor": profit_factor,
        "avg_duration": avg_duration,
        "n_trades": n_trades,
    }


# ---------------------------------------------------------------------------
# Data loading helpers
# ---------------------------------------------------------------------------


def _load_parquet(
    data_dir: Path,
    symbol: str,
    timeframe: str,
    start_date: str,
    end_date: str,
) -> pd.DataFrame:
    """Load a parquet file from the crypto_data store.

    Expects files at: data_dir/<symbol>/<symbol>_<tf>_start_<date>_end_<date>.parquet
    Tries an exact filename match first, then falls back to scanning the
    directory for the closest date range covering [start_date, end_date].
    """
    symbol_dir = data_dir / symbol
    if not symbol_dir.exists():
        raise FileNotFoundError(f"No data directory for {symbol}: {symbol_dir}")

    # Exact match
    exact = symbol_dir / f"{symbol}_{timeframe}_start_{start_date}_end_{end_date}.parquet"
    if exact.exists():
        return pd.read_parquet(exact)

    # Fallback: use the first parquet file found for this symbol + timeframe
    candidates = sorted(symbol_dir.glob(f"{symbol}_{timeframe}_*.parquet"))
    if not candidates:
        raise FileNotFoundError(
            f"No parquet file for {symbol}/{timeframe} in {symbol_dir}. "
            f"Expected pattern: {symbol}_{timeframe}_start_*_end_*.parquet"
        )

    path = candidates[0]
    logger.debug("Exact file not found; using %s", path.name)
    return pd.read_parquet(path)


def _standardise_ohlcv(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure the DataFrame has Open/High/Low/Close/Volume columns and a DatetimeIndex."""
    # Rename common Bybit column names to standard OHLCV
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
    """ATR(period) computed from OHLCV DataFrame."""
    high = df["High"]
    low = df["Low"]
    prev_close = df["Close"].shift(1)

    tr = pd.concat(
        [high - low, (high - prev_close).abs(), (low - prev_close).abs()],
        axis=1,
    ).max(axis=1)

    return tr.ewm(span=period, adjust=False).mean()
