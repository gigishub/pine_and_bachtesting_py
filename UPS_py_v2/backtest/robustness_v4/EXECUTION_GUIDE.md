# Robustness V4 — Execution Guide

## What is V4?

V4 tests one pair + one timeframe at a time, saves the full results as a CSV,
moves to the next condition, and at the end builds a robustness summary across
all conditions.

The core question: **"Which filter setup survives across multiple conditions?"**
Not the best setup on BTC — the one that works on BTC AND ETH AND SOL, on 1h AND 4h.

---

## Quick Start (3 steps)

```bash
# 1. Edit your symbols, timeframes, and parameter ranges
nano UPS_py_v2/backtest/robustness_v4/simple_config.py

# 2. Run the full pipeline
python -m UPS_py_v2.backtest.run_v4

# 3. Open the viewer
streamlit run UPS_py_v2/backtest/robustness_v4/streamlit_viewer.py
```

---

## The Flow

```
simple_config.py
      ↓
sequencer.py   runs BTC_1H → saves results/BTC_1H.csv
               runs BTC_4H → saves results/BTC_4H.csv
               runs ETH_1H → saves results/ETH_1H.csv
               ...
      ↓
reporter.py    loads all CSVs → scores consistency → saves ROBUSTNESS_SUMMARY.csv
      ↓
streamlit      explore overview / per-condition / trace a setup across all conditions
```

---

## Step 1 — Edit simple_config.py

This is the only file you need to edit for a normal run.

```python
symbols    = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
timeframes = ["1h", "4h"]
```

This creates 6 conditions: BTC_1H, BTC_4H, ETH_1H, ETH_4H, SOL_1H, SOL_4H.

### Core parameter grid

Always tested — no need to change these unless you know why:

```python
config.boolean_filter_ranges = {
    "use_iq_filter":           (False, True),
    "use_sq_boost":            (False, True),
    "enable_ec":               (False, True),
    "enable_bullish_engulfing": (False, True),
    "enable_shooting_star":    (False, True),
    "enable_hammer":           (False, True),
}
config.set_risk_reward_range(1.5, 2.0, 3.0, 5.0)
```

### Optional parameter ranges

Add these only when you want to expand the search to internal parameter values:

```python
config.set_optional_parameter_range("ma_length", 20, 50, 100)
config.set_optional_parameter_range("iq_lookback", 10, 20, 30)
```

Note: child parameters (like `iq_lookback`) are automatically ignored when
their parent filter (`use_iq_filter`) is off — no wasted combinations.

---

## Step 2 — Run the pipeline

```bash
python -m UPS_py_v2.backtest.run_v4
```

You'll see progress logged per condition:

```
INFO: [1/6] Running BTC_1H ...
INFO:   ✓ Saved BTC_1H (256 rows) → results/BTC_1H.csv
INFO: [2/6] Running BTC_4H ...
INFO:   ✓ Saved BTC_4H (256 rows) → results/BTC_4H.csv
...
INFO: Robustness summary saved → results/ROBUSTNESS_SUMMARY.csv
```

---

## Intervention Points

### Stop after a specific condition

Useful when you want to inspect results before continuing:

```python
from UPS_py_v2.backtest.robustness_v4.sequencer import run_sequential
from UPS_py_v2.backtest.robustness_v4.simple_config import build_simple_config

config = build_simple_config()
saved = run_sequential(config, stop_after="BTC_1H")

# Review results/BTC_1H.csv now.
# Re-run without stop_after to continue.
```

### Re-run a single condition

The sequencer overwrites a CSV if it already exists. So to re-run just one:

```python
import pandas as pd
from pathlib import Path
from UPS_py_v2.backtest.robustness_v4.pipeline import run_condition, load_dataset, ensure_min_bars

config = build_simple_config()
datasets = {d.condition_key: d for d in config.build_datasets()}
dataset = datasets["ETH_4H"]

df = ensure_min_bars(load_dataset(dataset), dataset=dataset, min_bars=config.min_bars)
results = run_condition(df, dataset, config)
results.to_csv(Path("results/ETH_4H.csv"), index=False)
```

### Rebuild the summary only (without re-running backtests)

```python
from pathlib import Path
from UPS_py_v2.backtest.robustness_v4.reporter import build_robustness_summary

summary = build_robustness_summary(Path("results"), consistency_top_n=20)
```

---

## Step 3 — Understanding the output

### Per-condition CSVs: `results/BTC_1H.csv`

One row per parameter combination. Every combination is saved — not just top N.
Key columns:

| Column | Meaning |
|---|---|
| Rank | 1 = best for this condition |
| Parameter Signature | Encoded key for the full parameter set |
| Expectancy [%] | Average edge per trade |
| Return [%] | Total return over the period |
| Profit Factor | Gross wins / gross losses |
| Max Drawdown [%] | Worst peak-to-trough |
| # Trades | Number of trades taken |
| SQN | System Quality Number (> 2 = good) |
| Sharpe Ratio | Risk-adjusted return |

All individual filter toggle columns (e.g. `use_iq_filter`, `enable_ec`) are also
included, so you can filter/group directly in Excel or the Streamlit viewer.

### Robustness Summary: `results/ROBUSTNESS_SUMMARY.csv`

One row per unique parameter signature, aggregated across all conditions.

| Column | Meaning |
|---|---|
| Robustness Rank | 1 = most robust overall |
| Consistency Score | How many conditions it appeared in top N (e.g. 7/9) |
| Consistency [%] | Same as a percentage |
| Expectancy [%] Mean | Average expectancy across all conditions |
| Expectancy [%] Std | Low Std = stable edge, high Std = possibly lucky |
| Return [%] Std | Low = consistent, high = volatile across conditions |
| Conditions Appeared In | Comma-separated list of top-N appearances |

**A high Consistency Score + low Std = robustly good setup.**
**A high Consistency Score + high Std = good on average but some conditions are drag.**
**A low Consistency Score = may be a lucky shot on one or two conditions.**

---

## Step 4 — Explore in Streamlit

```bash
streamlit run UPS_py_v2/backtest/robustness_v4/streamlit_viewer.py
```

Three tabs:

- **Robustness Overview** — filter by consistency score and expectancy, see top setups
- **Per Condition** — drill into any single BTC_1H / ETH_4H result
- **Deep Dive** — pick any parameter signature and trace it across every condition

---

## FAQ

**Q: The grid is too large and takes too long.**
A: Reduce the number of `boolean_filter_ranges` to just the ones you care about.
   Remove any optional parameter ranges. Each boolean you remove halves the grid.

**Q: A condition has too few trades to be meaningful.**
A: Check the `# Trades` column. If it's < 20, the results are not statistically
   meaningful. Consider a longer `start_time` or a smaller timeframe.

**Q: Can I add more symbols/timeframes later without re-running everything?**
A: Yes. The sequencer only produces CSVs — if `BTC_1H.csv` exists it will be
   overwritten, but others are untouched. Just add the new symbol/timeframe and
   re-run. Then rebuild the summary.

**Q: What does `consistency_top_n` mean?**
A: The number of top-ranked rows from each condition that count as "in top N".
   With `consistency_top_n=20`, a setup scores a point for each condition where
   it appeared in the top 20 ranked parameter sets. Raise this if your grid is
   very large; lower it to be stricter.
