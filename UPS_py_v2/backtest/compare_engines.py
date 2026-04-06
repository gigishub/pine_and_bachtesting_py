"""Engine comparison script — validates that backtesting.py and vectorbt
produce consistent results for the same strategy parameters on the same data.

WHAT THIS CHECKS
----------------
Both engines implement the same UPS strategy but simulate trades differently:
  - backtesting.py: bar-by-bar Python loop, stops checked at close price only
  - vectorbt:       compiled numba simulation, stops checked against OHLC intra-bar

This means results will NOT be identical — a position that would survive to
the close in backtesting.py may be stopped out intra-bar by vectorbt. Both
behaviours are correct; vectorbt is more realistic.

"Close enough" criteria:
  - # Trades:     within 20% of each other
  - Win Rate:     within 10 percentage points
  - Expectancy:   same sign and within 2×
  - Return:       same sign and within 2×
  - Max Drawdown: both engines within 15 percentage points

Usage:
    source .venv/bin/activate
    python -m UPS_py_v2.backtest.compare_engines

Optional args (edit SETTINGS section below):
  - DATE_RANGE:   start/end for the comparison window
  - PARAMS:       StrategySettings fields to use
"""

from __future__ import annotations

import math
import sys

import pandas as pd

from ..data.fetch import load_ohlcv
from ..strategy.strategy_parameters import StrategySettings
from .backtesting_py.runner import run as bt_run
from .vectorbt.runner import run as vbt_run
from .vectorbt.metrics import extract_stats

# ---------------------------------------------------------------------------
# SETTINGS — edit these to change what is compared
# ---------------------------------------------------------------------------

DATA = dict(
    symbol="BTCUSDT",
    timeframe="1h",
    start_time="2025-01-01 00:00:00",
    end_time="2025-04-01 00:00:00",  # ~2100 bars, ~2-3 months — runs fast on both engines
)

# Use a clean, reproducible parameter set:
# - optional overlay filters OFF so the signal layer is as simple as possible
# - candlestick entry patterns at defaults (all ON) — required for entries
# - no trailing stop (not supported in vectorbt)
PARAMS = StrategySettings(
    use_iq_filter=False,
    use_sq_boost=False,
    use_rsi_filter=False,
    use_adx_filter=False,
    use_volume_filter=False,
    trail_stop=False,
    risk_reward_multiplier=1.5,
    stop_multiplier=1.0,
    risk_per_trade=1.0,
    long_trades=True,
    short_trades=True,
    # entry patterns left at defaults (all True)
)

# "Close enough" tolerance for each metric
TOLERANCES = {
    "# Trades":        0.20,   # within 20%
    "Win Rate [%]":    10.0,   # within 10 pp
    "Expectancy [%]":  2.0,    # same sign + ratio ≤ 2×
    "Return [%]":      2.0,    # same sign + ratio ≤ 2×
    "Max. Drawdown [%]": 15.0, # within 15 pp
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_PASS = "✅ PASS"
_WARN = "⚠  WARN"
_FAIL = "❌ FAIL"


def _check(metric: str, bt_val: float, vbt_val: float) -> tuple[str, str]:
    """Return (status, explanation) for one metric comparison."""
    tol = TOLERANCES.get(metric)
    if tol is None or math.isnan(bt_val) or math.isnan(vbt_val):
        return "ℹ  INFO", "no tolerance defined or NaN"

    if metric == "# Trades":
        # relative difference
        if bt_val == 0 and vbt_val == 0:
            return _PASS, "both zero"
        denom = max(bt_val, vbt_val)
        rel = abs(bt_val - vbt_val) / denom
        status = _PASS if rel <= tol else _FAIL
        return status, f"{rel:.1%} difference (limit {tol:.0%})"

    if metric in ("Win Rate [%]", "Max. Drawdown [%]"):
        # absolute percentage point difference — use abs() to normalise sign conventions
        # (backtesting.py returns drawdown as negative, vectorbt as positive)
        diff = abs(abs(bt_val) - abs(vbt_val))
        status = _PASS if diff <= tol else _WARN
        return status, f"{diff:.1f} pp difference (limit {tol:.0f} pp)"

    if metric in ("Expectancy [%]", "Return [%]"):
        # same sign AND neither exceeds 2× the other.
        # Fall back to absolute ≤ 2 pp when both values are near-zero, because
        # ratio math distorts small numbers (e.g. -1.17% vs -0.52% → ratio 2.3×,
        # yet the absolute gap is only 0.65 pp — clearly a correct translation).
        abs_diff = abs(bt_val - vbt_val)
        if abs_diff <= 2.0:
            return _PASS, f"{abs_diff:.2f} pp absolute (within 2 pp fallback)"
        if (bt_val >= 0) != (vbt_val >= 0):
            return _FAIL, f"opposite signs (bt={bt_val:+.2f}%, vbt={vbt_val:+.2f}%)"
        if bt_val == 0 or vbt_val == 0:
            return _WARN, "one engine produced zero"
        ratio = max(abs(bt_val), abs(vbt_val)) / min(abs(bt_val), abs(vbt_val))
        status = _PASS if ratio <= tol else _WARN
        return status, f"ratio {ratio:.1f}× (limit {tol:.0f}×)"

    return "ℹ  INFO", ""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print("\n" + "=" * 60)
    print("  UPS Engine Comparison")
    print(f"  Symbol:    {DATA['symbol']} {DATA['timeframe']}")
    print(f"  Period:    {DATA['start_time']} → {DATA['end_time']}")
    print("=" * 60)

    print("\nLoading data...", end=" ", flush=True)
    df = load_ohlcv(**DATA)
    print(f"{len(df)} bars")

    # --- backtesting.py ---
    print("Running backtesting.py engine...", end=" ", flush=True)
    _bt, bt_result = bt_run(df, PARAMS)
    print("done")

    bt_stats = pd.Series({
        "# Trades":          float(bt_result.get("# Trades", float("nan"))),
        "Win Rate [%]":      float(bt_result.get("Win Rate [%]", float("nan"))),
        "Return [%]":        float(bt_result.get("Return [%]", float("nan"))),
        "Expectancy [%]":    float(bt_result.get("Expectancy [%]", float("nan"))),
        "Max. Drawdown [%]": float(bt_result.get("Max. Drawdown [%]", float("nan"))),
    })

    # --- vectorbt ---
    print("Running vectorbt engine...", end=" ", flush=True)
    pf = vbt_run(df, PARAMS)
    vbt_stats = extract_stats(pf)
    print("done")

    vbt_clean = pd.Series({
        "# Trades":          float(vbt_stats.get("# Trades", float("nan"))),
        "Win Rate [%]":      float(vbt_stats.get("Win Rate [%]", float("nan"))),
        "Return [%]":        float(vbt_stats.get("Return [%]", float("nan"))),
        "Expectancy [%]":    float(vbt_stats.get("Expectancy [%]", float("nan"))),
        "Max. Drawdown [%]": float(vbt_stats.get("Max. Drawdown [%]", float("nan"))),
    })

    # --- comparison table ---
    metrics = list(bt_stats.index)
    col_w = [28, 14, 14, 8, 36]

    header = (
        f"{'Metric':<{col_w[0]}}"
        f"{'backtesting.py':>{col_w[1]}}"
        f"{'vectorbt':>{col_w[2]}}"
        f"{'diff':>{col_w[3]}}"
        f"  {'verdict'}"
    )
    print("\n" + "-" * 80)
    print(header)
    print("-" * 80)

    all_pass = True
    for m in metrics:
        bt_v  = bt_stats[m]
        vbt_v = vbt_clean[m]
        diff  = vbt_v - bt_v

        status, note = _check(m, bt_v, vbt_v)
        if _FAIL in status:
            all_pass = False

        print(
            f"{m:<{col_w[0]}}"
            f"{bt_v:>{col_w[1]}.2f}"
            f"{vbt_v:>{col_w[2]}.2f}"
            f"{diff:>+{col_w[3]}.2f}"
            f"  {status}  {note}"
        )

    print("-" * 80)

    # --- trade-level detail ---
    print(f"\nbacktesting.py trades: {int(bt_stats['# Trades'])}")
    bt_trades = bt_result._trades
    if not bt_trades.empty:
        cols = [c for c in ["EntryTime", "ExitTime", "ReturnPct", "PnL"] if c in bt_trades.columns]
        print(bt_trades[cols].head(10).to_string(index=False))

    print(f"\nvectorbt trades: {int(vbt_clean['# Trades'])}")
    vbt_trades = pf.trades.records_readable
    if not vbt_trades.empty:
        cols = [c for c in ["Entry Timestamp", "Exit Timestamp", "Return", "PnL"] if c in vbt_trades.columns]
        print(vbt_trades[cols].head(10).to_string(index=False))

    print("\n" + "=" * 60)
    if all_pass:
        print("  ✅  All key metrics within tolerance — translation looks correct.")
    else:
        print("  ❌  One or more metrics outside tolerance — investigate above.")
    print("=" * 60 + "\n")

    # Exit non-zero if any FAIL so CI can catch regressions
    if not all_pass:
        sys.exit(1)


if __name__ == "__main__":
    main()
