"""Phase 2 — Date Range Sensitivity (trade-log slicing approach).

One full-period backtest is enough.  Trade logs (saved under ``trades/`` by
the sequencer) contain one row per trade with ``Parameter Signature``,
``Symbol``, ``EntryTime``, ``Return [%]``.  Slicing those logs by date window
lets us recompute SQN / Profit Factor / Win Rate / Expectancy for each
(signature, coin, window) without re-running any backtest.

Limitation: trade logs are only saved for the top-N combos per condition
(``trade_logs_top_n`` in ``RobustnessConfigV4``, default 5).  Signatures that
rank outside top-N on a condition will show 0 trades for that (sig, coin).
Increase ``trade_logs_top_n`` before re-running if you need deeper coverage.

Public API
----------
load_trade_logs(run_dir)                            → pd.DataFrame
compute_trade_metrics(trades)                        → dict[str, float]
passes_trade_thresholds(metrics, cfg, min_trades)    → bool
slice_trades(trades, start, end)                     → pd.DataFrame
evaluate_window(trades, signatures, start, end, cfg, min_trades_per_coin)
                                                     → pd.DataFrame
verdict_table(window_evals, min_coins_pass, min_windows_pass)
                                                     → pd.DataFrame
short_sig(sig, max_len)                              → str
sig_to_alias(sig)                                    → str
get_trade_timeframes(trades)                         → list[str]
filter_trades_by_timeframe(trades, tf)               → pd.DataFrame
cross_tf_consensus(tf_verdicts)                      → pd.DataFrame
coin_window_breakdown(trades, signatures, windows_cfg, cfg, min_trades_per_coin)
                                                     → pd.DataFrame
"""

from __future__ import annotations

import logging
import math
from pathlib import Path
from typing import Any

import pandas as pd

from strategy_evaluation.config import RobustnessConfig
from strategy_evaluation.sig_alias import sig_to_alias  # noqa: F401  (re-exported)

logger = logging.getLogger(__name__)


# ── Trade log I/O ─────────────────────────────────────────────────────────────

def load_trade_logs(run_dir: str | Path) -> pd.DataFrame:
    """Load all ``*_trade_log.csv`` files from the ``trades/`` sub-folder.

    Returns a combined DataFrame with parsed ``EntryTime`` / ``ExitTime``
    columns (UTC-aware).  Returns an empty DataFrame if no trade logs are found
    so callers can check ``df.empty`` instead of catching exceptions.
    """
    trades_dir = Path(run_dir) / "trades"
    if not trades_dir.exists():
        logger.warning("No trades/ directory found in %s", run_dir)
        return pd.DataFrame()

    files = sorted(trades_dir.glob("*_trade_log.csv"))
    if not files:
        logger.warning("trades/ directory exists but contains no *_trade_log.csv files")
        return pd.DataFrame()

    frames: list[pd.DataFrame] = []
    for path in files:
        try:
            df = pd.read_csv(path)
            if not df.empty:
                frames.append(df)
        except Exception:
            logger.warning("Failed to read trade log %s", path.name, exc_info=True)

    if not frames:
        return pd.DataFrame()

    combined = pd.concat(frames, ignore_index=True)

    for col in ("EntryTime", "ExitTime"):
        if col in combined.columns:
            combined[col] = pd.to_datetime(combined[col], utc=True, errors="coerce")

    logger.info(
        "Loaded %d trades from %d trade-log file(s) in %s",
        len(combined), len(frames), Path(run_dir).name,
    )
    return combined


# ── Metric computation from trade records ─────────────────────────────────────

def compute_trade_metrics(trades: pd.DataFrame) -> dict[str, float]:
    """Compute SQN, Profit Factor, Win Rate, Expectancy and # Trades from trade records.

    Sharpe Ratio and Max Drawdown are *not* computed here because they require
    the equity curve (time-series returns), which is not available from trade logs.

    Returns NaN for quality metrics when fewer than 2 trades are present
    (SQN is undefined for N < 2).
    """
    _nan = float("nan")
    n = len(trades)

    if n == 0:
        return {"# Trades": 0, "Win Rate [%]": _nan, "Profit Factor": _nan,
                "Expectancy [%]": _nan, "SQN": _nan}

    if "Return [%]" not in trades.columns:
        return {"# Trades": n, "Win Rate [%]": _nan, "Profit Factor": _nan,
                "Expectancy [%]": _nan, "SQN": _nan}

    returns = trades["Return [%]"].dropna()
    n_valid = len(returns)

    if n_valid == 0:
        return {"# Trades": n, "Win Rate [%]": _nan, "Profit Factor": _nan,
                "Expectancy [%]": _nan, "SQN": _nan}

    wins   = returns[returns > 0]
    losses = returns[returns <= 0]

    win_rate   = len(wins) / n_valid * 100.0
    gross_win  = float(wins.sum())
    gross_loss = abs(float(losses.sum()))
    pf         = gross_win / gross_loss if gross_loss > 0 else (float("inf") if gross_win > 0 else _nan)
    expectancy = float(returns.mean())

    if n_valid >= 2:
        std = float(returns.std(ddof=1))
        sqn = float((n_valid ** 0.5) * expectancy / std) if std > 0 else _nan
    else:
        sqn = _nan

    return {
        "# Trades":       n_valid,
        "Win Rate [%]":   round(win_rate, 2),
        "Profit Factor":  round(min(pf, 99.9), 4),  # cap to avoid inf display
        "Expectancy [%]": round(expectancy, 4),
        "SQN":            round(sqn, 4) if not math.isnan(sqn) else _nan,
    }


def passes_trade_thresholds(
    metrics: dict[str, float],
    cfg: RobustnessConfig,
    min_trades: int = 5,
) -> bool:
    """Return True if trade metrics meet the Phase 2 pass criteria.

    Uses SQN, Profit Factor, Win Rate and # Trades.  Sharpe and Max Drawdown
    are excluded because they are not computable from trade records alone.
    """
    n  = metrics.get("# Trades", 0)
    sqn = metrics.get("SQN", float("nan"))
    pf  = metrics.get("Profit Factor", float("nan"))
    wr  = metrics.get("Win Rate [%]", float("nan"))

    if any(math.isnan(x) for x in [sqn, pf, wr]):
        return False
    return (
        n   >= min_trades
        and sqn >= cfg.min_sqn
        and pf  >= cfg.min_profit_factor
        and wr  >= cfg.min_win_rate
    )


# ── Trade slicing ──────────────────────────────────────────────────────────────

def slice_trades(
    trades: pd.DataFrame,
    start: str | None,
    end: str | None,
) -> pd.DataFrame:
    """Return trades whose EntryTime falls in [start, end).

    Parameters
    ----------
    start, end:
        ISO date strings (``"YYYY-MM-DD"``).  ``None`` means no bound on that side.
    """
    if trades.empty or "EntryTime" not in trades.columns:
        return trades

    result = trades
    if start:
        result = result[result["EntryTime"] >= pd.Timestamp(start, tz="UTC")]
    if end:
        result = result[result["EntryTime"] < pd.Timestamp(end, tz="UTC")]
    return result


# ── Window evaluation ─────────────────────────────────────────────────────────

def evaluate_window(
    trades: pd.DataFrame,
    signatures: list[str],
    start: str | None,
    end: str | None,
    cfg: RobustnessConfig,
    min_trades_per_coin: int = 5,
) -> pd.DataFrame:
    """Evaluate pinned signatures against one date window using trade logs.

    For each (sig, coin) pair, compute trade metrics and check whether they
    meet the pass criteria.  ``coins_passing`` counts coins where the sig passes.

    Parameters
    ----------
    trades:
        Combined trade log DataFrame from ``load_trade_logs``.
    signatures:
        List of ``Parameter Signature`` strings to evaluate.
    start, end:
        Window bounds (ISO date strings).  ``None`` = open-ended.
    cfg:
        Threshold config (SQN, PF, Win Rate used; Sharpe/MaxDD skipped).
    min_trades_per_coin:
        Minimum trades in the window for a (sig, coin) to be counted as passing.

    Returns
    -------
    pd.DataFrame
        One row per signature with columns:
        Parameter Signature, sig_present, coins_passing, # Trades,
        Win Rate [%], Profit Factor, Expectancy [%], SQN.
        Signatures with no trade log data get sig_present=False and zeros.
    """
    if not signatures:
        return pd.DataFrame()

    col_sig = "Parameter Signature"
    col_sym = "Symbol"

    window_trades = slice_trades(trades, start, end)
    all_symbols   = sorted(trades[col_sym].unique()) if col_sym in trades.columns else []
    n_coins       = len(all_symbols)

    records: list[dict[str, Any]] = []
    for sig in signatures:
        has_sig_col = col_sig in trades.columns
        sig_present = bool(has_sig_col and (trades[col_sig] == sig).any())

        sig_window = (
            window_trades[window_trades[col_sig] == sig]
            if has_sig_col else pd.DataFrame()
        )

        # Per-coin pass check
        coins_passing = 0
        for sym in all_symbols:
            if col_sym in sig_window.columns:
                coin_trades = sig_window[sig_window[col_sym] == sym]
                if passes_trade_thresholds(
                    compute_trade_metrics(coin_trades), cfg, min_trades_per_coin
                ):
                    coins_passing += 1

        # Aggregate metrics across all coins for this window
        agg = compute_trade_metrics(sig_window)

        records.append({
            "Parameter Signature": sig,
            "sig_present":         sig_present,
            "coins_passing":       coins_passing,
            **agg,
        })

    return pd.DataFrame(records)


# ── Cross-window verdict ───────────────────────────────────────────────────────

def verdict_table(
    window_evals: dict[str, pd.DataFrame],
    min_coins_pass: int,
    min_windows_pass: int,
) -> pd.DataFrame:
    """Compute Phase 2 pass/fail verdict for each signature.

    Parameters
    ----------
    window_evals:
        Mapping of window label → ``evaluate_window`` output.
    min_coins_pass:
        Minimum coins_passing required for a window to count as a "pass".
    min_windows_pass:
        Minimum number of passing windows for an overall ``✅ PASS`` verdict.

    Returns
    -------
    pd.DataFrame
        Columns: Parameter Signature, <label>_coins, <label>_trades,
        windows_passing, verdict.  Sorted by windows_passing descending.
    """
    if not window_evals:
        return pd.DataFrame()

    all_sigs: list[str] = []
    for df in window_evals.values():
        if not df.empty and "Parameter Signature" in df.columns:
            for s in df["Parameter Signature"].tolist():
                if s not in all_sigs:
                    all_sigs.append(s)

    records: list[dict[str, Any]] = []
    for sig in all_sigs:
        row: dict[str, Any] = {"Parameter Signature": sig}
        windows_passing = 0

        for label, eval_df in window_evals.items():
            if eval_df.empty or "Parameter Signature" not in eval_df.columns:
                coins  = 0
                trades = 0
            else:
                match = eval_df[eval_df["Parameter Signature"] == sig]
                if match.empty:
                    coins  = 0
                    trades = 0
                else:
                    coins  = int(match["coins_passing"].iloc[0])
                    trades = int(match.get("# Trades", pd.Series([0])).iloc[0])

            row[f"{label}_coins"]  = coins
            row[f"{label}_trades"] = trades
            if coins >= min_coins_pass:
                windows_passing += 1

        row["windows_passing"] = windows_passing
        row["verdict"]         = "✅ PASS" if windows_passing >= min_windows_pass else "❌ FAIL"
        records.append(row)

    return (
        pd.DataFrame(records)
        .sort_values("windows_passing", ascending=False)
        .reset_index(drop=True)
    )


# ── Display helper ────────────────────────────────────────────────────────────

def short_sig(sig: str, max_len: int = 50) -> str:
    """Return a shortened parameter signature string for chart labels."""
    if len(sig) <= max_len:
        return sig
    return sig[:max_len] + "…"


# ── Timeframe helpers ─────────────────────────────────────────────────────────

def get_trade_timeframes(trades: pd.DataFrame) -> list[str]:
    """Return a sorted list of unique timeframes found in the *Condition* column.

    Timeframe is the last ``_``-separated segment of each ``Condition`` value
    (e.g. ``BTCUSDT_4H`` → ``4H``).  Returns an empty list when the column is
    absent or empty.
    """
    if trades.empty or "Condition" not in trades.columns:
        return []

    tfs = (
        trades["Condition"]
        .dropna()
        .str.rsplit("_", n=1)
        .str[-1]
        .unique()
        .tolist()
    )
    return sorted(tf for tf in tfs if tf)


def filter_trades_by_timeframe(trades: pd.DataFrame, tf: str) -> pd.DataFrame:
    """Return only rows whose *Condition* ends with ``_<tf>``.

    Returns an empty DataFrame when the column is absent or no rows match.
    """
    if trades.empty or "Condition" not in trades.columns:
        return pd.DataFrame(columns=trades.columns)

    mask = trades["Condition"].str.rsplit("_", n=1).str[-1] == tf
    return trades[mask].reset_index(drop=True)


def cross_tf_consensus(
    tf_verdicts: dict[str, pd.DataFrame],
) -> pd.DataFrame:
    """Summarise which signatures pass Phase 2 on each timeframe.

    Parameters
    ----------
    tf_verdicts:
        Mapping of ``timeframe → verdict_table`` DataFrames produced by
        :func:`verdict_table`.  Each DataFrame must have a
        ``Parameter Signature`` column and a ``verdict`` column.

    Returns
    -------
    pd.DataFrame
        One row per unique signature with columns:
        ``Parameter Signature``, one ``<tf>`` bool column per timeframe,
        ``tfs_passing`` (int count) and ``cross_verdict`` (✅ ALL / ⚠️ SOME / ❌ NONE).
        Sorted by ``tfs_passing`` descending.
        Returns an empty DataFrame when *tf_verdicts* is empty or all inputs
        are empty.
    """
    if not tf_verdicts:
        return pd.DataFrame()

    col_sig = "Parameter Signature"

    # Collect all unique signatures across all TF verdicts
    all_sigs: list[str] = []
    for vt in tf_verdicts.values():
        if vt.empty or col_sig not in vt.columns:
            continue
        for s in vt[col_sig].tolist():
            if s not in all_sigs:
                all_sigs.append(s)

    if not all_sigs:
        return pd.DataFrame()

    n_tfs = len(tf_verdicts)
    records: list[dict[str, Any]] = []

    for sig in all_sigs:
        row: dict[str, Any] = {col_sig: sig}
        tf_pass_count = 0

        for tf, vt in tf_verdicts.items():
            if vt.empty or col_sig not in vt.columns:
                passed = False
            else:
                match = vt[vt[col_sig] == sig]
                passed = (
                    not match.empty
                    and "verdict" in match.columns
                    and "PASS" in str(match["verdict"].iloc[0])
                )
            row[tf] = passed
            if passed:
                tf_pass_count += 1

        row["tfs_passing"] = tf_pass_count
        if tf_pass_count == n_tfs:
            row["cross_verdict"] = "✅ ALL"
        elif tf_pass_count > 0:
            row["cross_verdict"] = "⚠️ SOME"
        else:
            row["cross_verdict"] = "❌ NONE"

        records.append(row)

    return (
        pd.DataFrame(records)
        .sort_values("tfs_passing", ascending=False)
        .reset_index(drop=True)
    )


# ── Coin-level breakdown ───────────────────────────────────────────────────────

def coin_window_breakdown(
    trades: pd.DataFrame,
    signatures: list[str],
    windows_cfg: dict[str, tuple[str | None, str | None]],
    cfg: RobustnessConfig,
    min_trades_per_coin: int = 5,
) -> pd.DataFrame:
    """Count passing signatures per (window, coin) across the selected signatures.

    For each analysis window and each coin, checks how many of the given
    signatures pass quality thresholds for that coin in that window.

    Parameters
    ----------
    trades:
        Combined trade log DataFrame.
    signatures:
        Signatures (``Parameter Signature`` strings) to evaluate.
    windows_cfg:
        Ordered mapping of label → (start, end) as used by ``evaluate_window``.
    cfg:
        Threshold config forwarded to ``passes_trade_thresholds``.
    min_trades_per_coin:
        Minimum trades required for a (sig, coin, window) cell to count as passing.

    Returns
    -------
    pd.DataFrame
        Columns: ``Window``, ``Symbol``, ``sigs_passing``, ``sigs_total``,
        ``pass_rate``.  One row per (Window × Symbol), ordered Window then Symbol.
        Returns empty DataFrame when *trades* is empty or *signatures* is empty.
    """
    col_sig = "Parameter Signature"
    col_sym = "Symbol"

    if trades.empty or col_sym not in trades.columns or not signatures:
        return pd.DataFrame()

    all_symbols = sorted(trades[col_sym].unique().tolist())
    records: list[dict[str, Any]] = []

    for win_label, (start, end) in windows_cfg.items():
        window_trades = slice_trades(trades, start, end)

        for sym in all_symbols:
            sigs_pass = 0
            for sig in signatures:
                if col_sig in window_trades.columns:
                    coin_trades = window_trades[
                        (window_trades[col_sig] == sig) & (window_trades[col_sym] == sym)
                    ]
                else:
                    coin_trades = pd.DataFrame()
                if passes_trade_thresholds(
                    compute_trade_metrics(coin_trades), cfg, min_trades_per_coin
                ):
                    sigs_pass += 1

            records.append({
                "Window": win_label,
                "Symbol": sym,
                "sigs_passing": sigs_pass,
                "sigs_total": len(signatures),
                "pass_rate": sigs_pass / len(signatures),
            })

    return pd.DataFrame(records)

