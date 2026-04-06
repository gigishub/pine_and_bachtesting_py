# UPS Strategy — Backtest System

Everything needed to test, optimise, and validate the UPS strategy lives in this
`backtest/` directory.

---

## Directory overview

```
backtest/
│
├── config/              ← THE ONE PLACE YOU EDIT
│   ├── simple_config.py       ← change this to control every run
│   ├── default_config.py      RobustnessConfigV4 dataclass + grid builder
│   └── sensitivity_config.py  stub — future stability testing (Phase 2)
│
├── reporting/           ← results presentation (touch only for UI changes)
│   ├── reporter.py            builds ROBUSTNESS_SUMMARY.csv after a run
│   ├── models.py              defines metric column names used in all CSVs
│   └── streamlit_viewer.py    interactive browser for results
│
├── backtesting_py/      ← ENGINE 1 — accurate, supports trailing stops
│   └── run.py                 entry point
│
├── vectorbt/            ← ENGINE 2 — fast, best for grid search
│   └── run.py                 entry point
│
└── results/
    ├── results_backtesting_py/
    └── results_vbt/
```

---

## How to run a grid search

**Step 1 — edit `config/simple_config.py`**

This is the only file you need to touch for a normal run. Key sections:

```python
# Which markets to test
symbols    = ["BTCUSDT", "ETHUSDT"]
timeframes = ["1h", "4h"]

# Date range (None = up to today)
start_time = "2023-01-01 00:00:00"
end_time   = None

# Which filters to test on/off — each (False, True) doubles the grid
config.boolean_filter_ranges = {
    "use_iq_filter":            (False, True),
    "use_adx_filter":           (False, True),
    "use_rsi_filter":           (False, True),
    "use_volume_filter":        (False, True),
    "enable_bullish_engulfing": (False, True),
    # Pin a filter off: (False,)   Pin it on: (True,)
}

# Risk:reward ratios to sweep
config.set_risk_reward_range(1.0, 1.5, 2.0)
```

**Step 2 — choose an engine and run**

| Engine | Command | Use when |
|---|---|---|
| vectorbt (fast) | `python -m UPS_py_v2.backtest.vectorbt.run` | grid search, filter testing |
| backtesting.py | `python -m UPS_py_v2.backtest.backtesting_py.run` | trailing stops, verification |

Both engines read the same `simple_config.py` and write the same CSV format.

```bash
source .venv/bin/activate
python -m UPS_py_v2.backtest.vectorbt.run
```

**Step 3 — view results**

Results land in a timestamped folder:
```
results/results_vbt/2026-04-06_1210_UPS/
  BTCUSDT_1H.csv
  BTCUSDT_4H.csv
  ETHUSDT_1H.csv
  ROBUSTNESS_SUMMARY.csv    ← ranked by consistency across all conditions
  run_vbt.log
```

Launch the interactive viewer:
```bash
streamlit run UPS_py_v2/backtest/reporting/streamlit_viewer.py
```

---

## Results directory naming

Format: `YYYY-MM-DD_HHMM_UPS[_suffix]`

- Standard run:     `2026-04-06_1210_UPS`
- Labelled run:     `2026-04-06_1530_UPS_adx_test`

Year-first means directories always sort chronologically — the last entry is
always the most recent run.

To add a suffix for a specific test (e.g. testing only ADX):
```python
# In backtest/vectorbt/run.py, change:
output_dir = build_output_dir("vbt", "UPS", suffix="adx_test")
```

---

## Checkpoint resume

If a run is interrupted, just re-run the same command. The sequencer checks
whether a CSV already exists for each condition and skips it. A `.current_run`
marker file in each engine's results directory tracks the active run folder.

To **force a brand-new run** (discard the checkpoint):
```bash
rm results/results_vbt/.current_run
```

---

## Comparing both engines

Both engines write CSVs with identical column names. To compare:

```python
import pandas as pd

bt  = pd.read_csv("results/results_backtesting_py/2026-04-06_1210_UPS/BTCUSDT_1H.csv")
vbt = pd.read_csv("results/results_vbt/2026-04-06_1210_UPS/BTCUSDT_1H.csv")

merged = bt.merge(vbt, on="Parameter Signature", suffixes=("_bt", "_vbt"))
print(merged[["Parameter Signature", "Expectancy [%]_bt", "Expectancy [%]_vbt"]])
```

Minor numeric differences are expected: vectorbt checks stops against the bar's
high/low (intra-bar); backtesting.py checks stops at the close only.

---

## How the grid works

The grid is built from `boolean_filter_ranges` + `set_risk_reward_range()`.

- Each filter with `(False, True)` doubles the grid.
- Nine filters → 2⁹ = 512 filter combos × 2 R:R values = **1024 combos**.
- Each combo is one full backtest on one symbol/timeframe.

To reduce grid size, pin filters you're not interested in:
```python
"use_adx_filter": (False,),   # always off — not tested
```

The ROBUSTNESS_SUMMARY ranks combos by **Consistency Score** — how often a
setup appears in the top 20 across all conditions. A setup that ranks well on
BTC/1H, BTC/4H, ETH/1H, and ETH/4H has a higher consistency than one that only
works on a single market.

---

## Adding a new filter to the grid

1. Add the field to `StrategySettings` in `strategy/strategy_parameters.py`.
2. Wire it into `build_strategy_series()` in `strategy/signals.py`.
3. Add it to `boolean_filter_ranges` in `config/simple_config.py`.

No changes to `pipeline.py`, `sequencer.py`, or either engine are required.

---

## Future phases

| Phase | Location | Status |
|---|---|---|
| Grid search | `vectorbt/run.py` or `backtesting_py/run.py` | ✅ implemented |
| Sensitivity (stability around best params) | `config/sensitivity_config.py` | 🔲 stub only |
| Monte Carlo | — | 🔲 future |
| Forward / walk-forward test | — | 🔲 future |

All future phases will use the same `config/`, `reporting/`, and engine layers.

---

## Running the tests

```bash
source .venv/bin/activate
python -m pytest UPS_py_v2/backtest/vectorbt/tests/ -v
# 25 passed, 1 skipped
```
