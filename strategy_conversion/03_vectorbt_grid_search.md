# Phase 3 — vectorbt Grid-Search Engine

## Goal

Replace the single-run `backtesting.py` backtest with a vectorbt engine that can
grid-search all filter flag combinations in one pass.  This phase makes it possible
to answer: **"Which combination of Regime / Setup / Trigger / Exit flags performs
best, and is that result consistent across symbols and timeframes?"**

---

## Why vectorbt for the grid search?

| Concern | backtesting.py | vectorbt |
|---------|---------------|----------|
| Speed per combo | ~10–20 s (Python loop) | ~8–12 s first run (numba JIT warmup), faster on repeats |
| Grid search | Manual loop or Backtest.optimize() | Native via pre-computed arrays |
| Trailing stops | Full support (next() logic) | Approximated — see caveat below |
| Use case | Reference / precise single run | Grid search / robustness |

For this strategy the exit layer already produces a pre-computed `stop_series`
(chandelier / psar / bbands combined via OR-max).  vectorbt can consume this as
`exits = close < stop_series` without needing the bar-by-bar ratchet.

---

## Architecture

```
backtest/
├── config.py              ← BacktestConfig + DatasetConfig + MomentumGridConfig
├── simple_config.py       ← User-facing config (only file you should edit)
├── runner.py              ← Backward-compat shim → imports from backtesting_py/
├── backtesting_py/        ← Single-run reference engine
│   ├── __init__.py
│   ├── strategy.py
│   ├── runner.py
│   └── run.py
└── vectorbt/
    ├── __init__.py        ← exposes run()
    ├── signals.py         ← build_vbt_arrays(df, params) → entries/exits/size
    ├── runner.py          ← run(df, params) → vbt.Portfolio
    ├── metrics.py         ← extract_stats(pf) → pd.Series
    ├── pipeline.py        ← build_parameter_grid + run_condition + ranking
    ├── sequencer.py       ← run_sequential(config) → list[Path]
    └── run.py             ← __main__ entry point
```

The pattern mirrors `UPS_py_v2/backtest/vectorbt/` with three changes:
1. `DatasetConfig` + `MomentumGridConfig` live in the strategy's own `backtest/config.py`.
2. `run_backtest_vbt()` constructs `Parameters` (not `StrategySettings`).
3. No short entries — this is a long-only strategy.

---

## Key design decisions

### Entry / exit arrays (not sl_stop / tp_stop)

UPS vectorbt uses `sl_stop` + `tp_stop` fractions because its stops are fixed
percentages anchored at entry.  The Adaptive Momentum stop is a trailing indicator
series (`chandelier_stop`, `psar_stop`, `bb_upper` combined via OR-max).

Instead of converting to a fraction (which would be stale by exit time), we use:

```python
entries = is_ready & regime_filter & setup_signal & trigger_signal
exits   = close < stop_series
```

This correctly fires the exit on the bar the price crosses below the stop.

### Known approximation: no ratchet in vbt

In `backtesting.py`, the chandelier stop is ratcheted (`stop = max(stop, candidate)`)
inside `next()` so it only ever moves up.  In vectorbt, the raw `stop_series` is
used directly.  The formula `rolling_max(high, 22) - ATR * mult` is generally
non-decreasing in uptrends, but can drop when ATR spikes.  This is an acceptable
approximation for grid-search purposes; the backtesting.py engine remains the
precise reference.

### Position sizing

```python
size_frac = risk_pct / 100 / stop_dist_pct
stop_dist_pct = (close - stop_series) / close
```

Clipped to `[0, 0.9999]`.  `size_type="percent"` in `from_signals()` = fraction of
available cash.

### fill_at_next_open = True (default)

All signal arrays are shifted one bar forward and `Open` is used as the fill price.
This matches `backtesting.py`'s default `exclusive_orders=True` fill logic and
eliminates look-ahead bias.

### Grid: 512 total → 189 valid combinations (9 boolean flags, all enabled)

| Layer | Flags | Default in simple_config.py |
|-------|-------|----------------------------|
| Regime | `use_adx`, `use_ema_ribbon` | both enabled (swept) |
| Setup | `use_donchian`, `use_volume_profile` | both enabled (swept) |
| Trigger | `use_cmf`, `use_power_candle` | both enabled (swept) |
| Exit | `use_chandelier`, `use_psar`, `use_bbands` | all enabled (swept) |

With all 9 flags swept: 2^9 = **512 total** combinations.
After removing combos where any layer group is entirely False: **189 valid**.

`"relative_strength"` is excluded from the grid (requires a benchmark DataFrame).
`"mvrv"` and `"cvd"` are excluded (on-chain / tick data required).

The `_is_valid_combo()` filter in `pipeline.py` removes invalid combos automatically
before any computation.

---

## Parameters / config

`MomentumGridConfig` (in `backtest/config.py`) drives the entire run.  You never
need to edit it directly — `simple_config.py` is the user-facing interface:

```python
config = MomentumGridConfig(
    symbols=["SOLUSDT"],
    timeframes=["1h"],
    start_time="2024-09-01 00:00:00",
    boolean_filter_ranges={
        "use_adx":            (False, True),   # sweep both off and on
        "use_ema_ribbon":     (False, True),
        "use_donchian":       (False, True),
        "use_volume_profile": (False, True),
        "use_cmf":            (False, True),
        "use_power_candle":   (False, True),
        "use_chandelier":     (False, True),
        "use_psar":           (False, True),
        "use_bbands":         (False, True),
    },
    initial_cash=10_000.0,
    fees=0.001,            # 0.10% taker fee
    n_jobs=1,              # 1 = sequential; -1 = all cores
    min_bars=500,
    consistency_top_n=10,
    save_trade_logs=True,
    trade_logs_top_n=5,
)
```

Flag range semantics:
- `(False, True)` — sweep: tests both off and on
- `(False,)`      — pinned off: always excluded from grid
- `(True,)`       — pinned on: always on, not swept

Optional numeric sweeps (add to `simple_config.py` to expand the grid):
- `adx_threshold_range=(25.0, 30.0)` — only affects combos where `use_adx=True`
- `chandelier_atr_mult_range=(3.0, 4.0)` — only affects combos where `use_chandelier=True`
- `cmf_threshold_range=(0.05, 0.10)` — only affects combos where `use_cmf=True`

---

## User-facing config: `simple_config.py`

`simple_config.py` is the only file you should edit before running a grid search:

```python
# --- What to test ---
symbols    = ["SOLUSDT"]
timeframes = ["1h"]
start_time = "2024-09-01 00:00:00"

# --- Regime layer  (at least one must be True) ---
use_adx_regime = True
use_ema_ribbon = True

# --- Setup layer   (at least one must be True) ---
use_donchian_setup = True
use_volume_profile = True

# --- Trigger layer (at least one must be True) ---
use_cmf_trigger  = True
use_power_candle = True

# --- Exit layer    (at least one must be True) ---
use_chandelier_exit = True
use_psar_exit       = True
use_bbands_exit     = True

# --- Execution & output ---
initial_cash: float = 10_000.0
commission: float   = 0.001      # 0.10% taker fee (Bybit standard)
n_jobs: int         = 1          # 1 = sequential; -1 = all CPU cores
min_bars: int       = 500
consistency_top_n: int  = 10
save_trade_logs: bool   = True
trade_logs_top_n: int   = 5
# Note: slippage and plot are single-run settings (see backtesting_py/runner.py)
```

Setting a flag to `True` → `(False, True)`: included in grid, tested both off and on.
Setting a flag to `False` → `(False,)`: always off, excluded from grid entirely.

---

## Running

```bash
# Full grid run (saves CSV per condition)
source .venv/bin/activate
python -m adaptive_momentum_strategy.backtest.vectorbt.run

# Single reference run (with plot)
python -m adaptive_momentum_strategy.backtest.backtesting_py.run

# Results appear in:
# adaptive_momentum_strategy/backtest/results/results_vbt/<timestamp>/SOLUSDT_1H.csv
```

Output CSV columns (one row per combo):

| Column | Meaning |
|--------|---------|
| `Rank` | 1 = best (sorted by Expectancy) |
| `use_adx`, `use_ema_ribbon`, `use_donchian`, `use_volume_profile`, `use_cmf`, `use_power_candle`, `use_chandelier`, `use_psar`, `use_bbands` | Boolean flag values for this combo |
| `# Trades` | Closed trades |
| `Return [%]` | Total return over the period |
| `Expectancy [%]` | Avg % gain per trade (primary ranking metric) |
| `Profit Factor` | Gross wins / gross losses |
| `Win Rate [%]` | % of winning trades |
| `Max Drawdown [%]` | Worst peak-to-trough |
| `SQN` | System Quality Number |
| `Sharpe Ratio` | Risk-adjusted return |

---

## Sample output (SOLUSDT 1H, Sep 2024 → present)

```
Rank  use_adx  use_ema_ribbon  use_donchian  use_volume_profile  use_cmf  use_power_candle  use_chandelier  use_psar  use_bbands  # Trades  Return [%]  Expectancy [%]
1     False    True            False         True                True     False             True            False     False             64      16.15          0.36
2     False    True            True          False               True     False             False           False     True              22      -0.47         -0.01
3     True     False           True          False               True     False             True            False     False             57       9.83         -0.03
...
```

---

## Checklist

- [x] `backtest/config.py` — `DatasetConfig` + `MomentumGridConfig` with `boolean_filter_ranges`
- [x] `backtest/simple_config.py` — user-facing toggles + execution settings
- [x] `backtest/vectorbt/__init__.py` — exposes `run`
- [x] `backtest/vectorbt/signals.py` — `build_vbt_arrays()` with entries/exits/size
- [x] `backtest/vectorbt/runner.py` — `run()` with `fill_at_next_open` shift
- [x] `backtest/vectorbt/metrics.py` — `extract_stats()` matching backtesting.py keys
- [x] `backtest/vectorbt/pipeline.py` — grid build + `_is_valid_combo()` filter + `run_condition()` + ranking
- [x] `backtest/vectorbt/sequencer.py` — `run_sequential()` with checkpoint-resume
- [x] `backtest/vectorbt/run.py` — `__main__` entry point
- [x] End-to-end verified: 189 valid combos (from 512 total) ran on SOLUSDT 1H, results ranked and printed
