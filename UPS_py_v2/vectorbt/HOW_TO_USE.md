# UPS Strategy — vectorbt Engine

`UPS_py_v2/vectorbt/` is a fast backtest engine for the UPS strategy built on
[vectorbt](https://vectorbt.dev).  It is a **parallel engine** to `UPS_py_v2/backtest/`
(the backtesting.py engine) — they share the strategy signal layer but are otherwise
completely independent.

---

## Why vectorbt?

| | backtesting.py | vectorbt |
|---|---|---|
| Simulation loop | Python (bar-by-bar) | Compiled numba (whole array at once) |
| Single backtest | ~1–5 s | ~0.1–0.5 s |
| Grid search (192 combos) | ~5–30 min | ~30 s – 3 min |
| Trailing stops | ✅ | ❌ (future work) |
| Intra-bar stop accuracy | Close-price only | Uses OHLC (more accurate) |

---

## Quick start — single backtest

```python
from UPS_py_v2.vectorbt.runner import run
from UPS_py_v2.vectorbt.metrics import extract_stats
from UPS_py_v2.strategy.strategy_parameters import StrategySettings
from UPS_py_v2.data.fetch import load_ohlcv

# 1. Load OHLCV data
df = load_ohlcv(
    source="bybit",
    symbol="BTCUSDT",
    market_type="futures",
    timeframe="1h",
    start_time="2023-01-01 00:00:00",
)

# 2. (Optional) customise strategy settings
settings = StrategySettings(
    ma_length=50,
    use_iq_filter=True,
    risk_reward_multiplier=2.0,
    stop_multiplier=1.0,
    risk_per_trade=1.0,
)

# 3. Run the backtest
pf = run(df, settings)

# 4. View results
print(pf.stats())          # raw vbt stats
print(extract_stats(pf))   # standardised metric names (same as robustness pipeline)

# 5. Plot (opens in browser)
pf.plot().show()
```

---

## Running the robustness grid

The grid search tests many parameter combinations across multiple symbols and timeframes.

**From the command line:**
```bash
source .venv/bin/activate
python -m UPS_py_v2.vectorbt.run_robustness
```

Results land in the same timestamped folder as the backtesting.py engine:
```
UPS_py_v2/backtest/robustness_v4/results/HHMM-DD-MM-YYYY_UPS/
  BTC_1H.csv
  BTC_4H.csv
  ETH_1H.csv
  ...
  ROBUSTNESS_SUMMARY.csv
  run_vbt.log
```

**To configure what gets tested**, edit:
```
UPS_py_v2/backtest/robustness_v4/simple_config.py
```
Both engines read the same config file — you can run both and compare their CSVs
side-by-side since they write the same column format.

---

## Architecture

```
UPS_py_v2/
│
├── strategy/                   ← SHARED — pure pandas/numpy, no engine dependency
│   ├── signals.py              build_strategy_series() — entry signals as bool Series
│   ├── indicators/             MA, IQ, RSI, ADX, volume, candlestick patterns
│   ├── risk/                   SL/TP helpers, position sizing, trailing stop helpers
│   └── strategy_parameters.py StrategySettings dataclass
│
├── data/                       ← SHARED — data loading, exchange API wrappers
│
├── backtest/                   ← backtesting.py ENGINE (existing)
│   ├── strategy.py             UPSStrategy(Strategy) — bar-by-bar Python loop
│   ├── runner.py               FractionalBacktest wrapper
│   └── robustness_v4/          Grid search, sequencer, reporter
│
└── vectorbt/                   ← vectorbt ENGINE (new)
    ├── signals.py              Adapts strategy signals → vbt array format
    ├── runner.py               vbt.Portfolio.from_signals() wrapper
    ├── metrics.py              Maps vbt stats → standardised metric names
    ├── pipeline.py             Own grid builder + result rows + ranking
    ├── sequencer.py            Own sequential runner with checkpoint resume
    ├── run_robustness.py       CLI entry-point
    └── tests/                  pytest coverage
```

The two engines **never import each other**.  The only shared code is `strategy/`
(signal/indicator logic) and the `RobustnessConfigV4` / `DatasetConfig` dataclasses
from `backtest/robustness_v4/config.py` (pure configuration, no engine code).

---

## How signals are converted to vbt format

`backtesting.py` handles SL/TP inside `Strategy.next()` as absolute price levels.
`vectorbt` wants SL/TP as **fractions from entry price** set before the simulation.

`vectorbt/signals.py` does the conversion in five steps:

1. **Entry signals** — calls `build_strategy_series()` to get `valid_long_entry`
   and `valid_short_entry` as boolean arrays.

2. **Vectorized SL** — applies the same ATR-based stop logic as `compute_long_stop()`
   but across all bars at once using `pandas.shift(1)` for the previous bar's high/low.

3. **Relative fractions** — converts absolute stop prices to fractions:
   ```
   sl_pct = (close - stop_price) / close      # for longs
   tp_pct = (tp_price - close)   / close      # for longs
   ```

4. **minimum_rr filter** — replicates the check in `Strategy.next()` that skips
   entries where the TP/SL ratio is below `minimum_rr`.

5. **Position sizing** — computes per-bar size fraction:
   ```
   size = risk_per_trade_pct / sl_pct
   ```
   This risks exactly `risk_per_trade%` of equity on each trade.

---

## Limitations vs the backtesting.py engine

| Feature | backtesting.py | vectorbt |
|---|---|---|
| Fixed SL / TP | ✅ | ✅ |
| Trailing stops (`trail_stop=True`) | ✅ | ❌ not implemented |
| Intra-bar stop accuracy | Close only | ✅ OHLC (more realistic) |
| Live runner compatibility | ✅ | ❌ (backtesting.py engine feeds live runner) |

If you run with `trail_stop=True` in `StrategySettings`, the vectorbt engine will
**silently ignore the trailing stop** and use a fixed TP instead.  Check the module
docstring in `vectorbt/signals.py` for context.

---

## Comparing both engines

Both engines write CSVs with the same column names.  To compare results:

```python
import pandas as pd

bt_results  = pd.read_csv("path/to/backtest_v4_results/BTC_1H.csv")
vbt_results = pd.read_csv("path/to/vbt_results/BTC_1H.csv")

# Merge on the shared parameter signature
merged = bt_results.merge(
    vbt_results,
    on="Parameter Signature",
    suffixes=("_bt", "_vbt"),
)

# Compare expectancy
print(merged[["Parameter Signature", "Expectancy [%]_bt", "Expectancy [%]_vbt"]].head(20))
```

Minor numeric differences between the two engines are expected because:
- vectorbt checks stops against the bar's high/low (intra-bar accuracy).
- backtesting.py only checks stops at the close of each bar.

---

## Running the tests

```bash
source .venv/bin/activate
python -m pytest UPS_py_v2/vectorbt/tests/ -v
```

Expected output: ~25 passed, 1 skipped (the skipped test requires trades to
have fired, which depends on the synthetic data producing entry signals).

---

## Adding a new parameter to the grid

1. Add the field to `StrategySettings` in `strategy/strategy_parameters.py`.
2. Pass it through `build_strategy_series()` in `strategy/signals.py`.
3. If needed, use it in `build_vbt_arrays()` in `vectorbt/signals.py`.
4. Register it in `simple_config.py` under `config.boolean_filter_ranges` or
   `config.set_optional_parameter_range(...)`.

No changes to `vectorbt/pipeline.py` or `vectorbt/sequencer.py` are required —
the grid builder reads all ranges dynamically from the config.
