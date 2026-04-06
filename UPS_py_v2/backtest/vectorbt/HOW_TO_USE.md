# UPS Strategy — vectorbt Engine

`UPS_py_v2/backtest/vectorbt/` is a fast backtest engine for the UPS strategy
built on [vectorbt](https://vectorbt.dev). It is a **parallel engine** to
`backtest/backtesting_py/` — they share the strategy signal layer, config, and
reporting but are otherwise completely independent.

---

## Why vectorbt?

| | backtesting.py | vectorbt |
|---|---|---|
| Simulation loop | Python (bar-by-bar) | Compiled numba (whole array at once) |
| Single backtest | ~1–5 s | ~0.1–0.5 s |
| Grid search (768 combos) | ~30–60 min | ~3–5 min |
| Trailing stops | ✅ | ❌ (future work) |
| Intra-bar stop accuracy | Close-price only | Uses OHLC (more accurate) |

---

## Quick start — single backtest

```python
from UPS_py_v2.backtest.vectorbt.runner import run
from UPS_py_v2.backtest.vectorbt.metrics import extract_stats
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
print(pf.stats())           # raw vbt stats
print(extract_stats(pf))    # standardised metric names (same as robustness pipeline)

# 5. Plot (opens in browser)
pf.plot().show()
```

---

## Running the robustness grid

The grid search tests many parameter combinations across multiple symbols and timeframes.

**From the command line:**
```bash
source .venv/bin/activate
python -m UPS_py_v2.backtest.vectorbt.run
```

Results land in a timestamped folder (format: `YYYY-MM-DD_HHMM_UPS`):
```
UPS_py_v2/backtest/results/results_vbt/2026-04-06_1210_UPS/
  BTC_1H.csv
  BTC_4H.csv
  ETH_1H.csv
  ...
  ROBUSTNESS_SUMMARY.csv
  run_vbt.log
```

For the backtesting.py engine (supports trailing stops):
```bash
python -m UPS_py_v2.backtest.backtesting_py.run
# → results land in backtest/results/results_backtesting_py/
```

**To configure what gets tested**, edit:
```
UPS_py_v2/backtest/config/simple_config.py
```
Both engines read the same config file and write results with the same CSV column
format — you can compare their outputs side-by-side.

**To add a run label/suffix** (useful when testing specific filters):
```python
# In each engine's run.py:
output_dir = build_output_dir("vbt", "UPS", suffix="adx_test")
```
Result: `results_vbt/2026-04-06_1530_UPS_adx_test/`

---

## Architecture

```
UPS_py_v2/
│
├── strategy/                    ← SHARED — pure pandas/numpy signal logic
├── data/                        ← SHARED — OHLCV loading
│
└── backtest/
    │
    ├── config/                  ← SHARED — what to test
    │   ├── default_config.py    RobustnessConfigV4, DatasetConfig, grid builder
    │   ├── simple_config.py     ← THE ONE FILE YOU EDIT PER RUN
    │   └── sensitivity_config.py  stub for future Phase 2
    │
    ├── reporting/               ← SHARED — how to present results
    │   ├── models.py            metric column definitions
    │   ├── reporter.py          ROBUSTNESS_SUMMARY.csv builder
    │   └── streamlit_viewer.py  interactive results browser
    │
    ├── backtesting_py/          ← ENGINE 1 — trailing stops, live-runner compatible
    │   ├── strategy.py
    │   ├── runner.py
    │   ├── pipeline.py
    │   ├── sequencer.py
    │   └── run.py
    │
    ├── vectorbt/                ← ENGINE 2 — fast grid search (this package)
    │   ├── signals.py
    │   ├── runner.py
    │   ├── metrics.py
    │   ├── pipeline.py
    │   ├── sequencer.py
    │   └── run.py
    │
    └── results/
        ├── results_backtesting_py/
        └── results_vbt/
```

The two engines **never import each other**. Both import from `config/` and
`reporting/` (pure config/data, no engine code).

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
silently ignore the trailing stop and use a fixed TP instead. Use the
backtesting.py engine when trailing stops are required.

---

## Comparing both engines

Both engines write CSVs with the same column names. To compare results:

```python
import pandas as pd

bt_results  = pd.read_csv("backtest/results/results_backtesting_py/.../BTC_1H.csv")
vbt_results = pd.read_csv("backtest/results/results_vbt/.../BTC_1H.csv")

merged = bt_results.merge(
    vbt_results,
    on="Parameter Signature",
    suffixes=("_bt", "_vbt"),
)
print(merged[["Parameter Signature", "Expectancy [%]_bt", "Expectancy [%]_vbt"]].head(20))
```

Minor numeric differences are expected: vectorbt checks stops against the bar's
high/low (intra-bar accuracy); backtesting.py only checks stops at the close.

---

## Running the tests

```bash
source .venv/bin/activate
python -m pytest UPS_py_v2/backtest/vectorbt/tests/ -v
```

Expected output: 25 passed, 1 skipped.

---

## How to configure the grid

Edit `backtest/config/simple_config.py`. Key sections:

```python
# Which filters to toggle on/off in the grid
config.boolean_filter_ranges = {
    "use_iq_filter":   (False, True),   # tests both — doubles the grid
    "use_adx_filter":  (False,),        # pinned off — excluded from grid
    "use_rsi_filter":  (True,),         # pinned on  — always enabled
}

# Risk:reward values to test
config.set_risk_reward_range(1.0, 1.5, 2.0)

# Optional: sweep numeric parameters
# config.set_optional_parameter_range("rsi_period", 10, 14, 20)
```

No changes to `pipeline.py` or `sequencer.py` are needed — the grid builder
reads all ranges dynamically from the config.
