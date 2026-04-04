# Robustness V3 How To Use

This version is meant to be adjusted in files, not through CLI flags.

## Main idea

V3 has only two steps:

1. Step 1 optimizes Boolean entry filters plus a small Risk:Reward set on one primary dataset.
2. Step 2 takes the best Step 1 candidates and validates them across multiple assets and at least three timeframes.

## Files you edit

Normal setup file:
[UPS_py_v2/backtest/robustness_v3/simple_config.py](/root/projects/pine_and_bachtesting_py/UPS_py_v2/backtest/robustness_v3/simple_config.py)

Core config model:
[UPS_py_v2/backtest/robustness_v3/config.py](/root/projects/pine_and_bachtesting_py/UPS_py_v2/backtest/robustness_v3/config.py)

Simple runner:
[UPS_py_v2/backtest/run_v3.py](/root/projects/pine_and_bachtesting_py/UPS_py_v2/backtest/run_v3.py)

## What to change in simple_config.py

Primary optimization dataset:
- `primary_symbol`
- `primary_timeframe`

Validation matrix:
- `validation_symbols`
- `validation_timeframes`

Core search space:
- `config.boolean_filter_ranges`
- `config.set_risk_reward_range(...)`

Optional parameters only when needed:
- `config.set_optional_parameter_range("ma_length", 20, 50, 100)`
- `config.set_optional_parameter_range("iq_lookback", 10, 20, 30)`

If you do not add an optional parameter range, v3 uses the default value from `StrategySettings` and does not expand the optimization grid for it.

## Why DEFAULT_FEATURE_DEPENDENCIES exists

That map is there to stop invalid or useless optimization combinations.

Example:
- If `use_iq_filter=False`, then `iq_lookback`, `iq_min_score`, and other IQ-only values should not create extra combinations.
- If `enable_hammer=False`, then `hammer_fib` and `hammer_size` should stay at their default baseline values.

Without that dependency map, the optimizer would test many duplicate combinations that behave the same way because the parent feature is turned off.

So the rule is:
- parent filter off = child parameter stays at default
- parent filter on = child parameter can be optimized if you provided a range

## Practical examples

### Example 1: Only Boolean filters + RR

Leave `optional_parameter_ranges` empty in [UPS_py_v2/backtest/robustness_v3/simple_config.py](/root/projects/pine_and_bachtesting_py/UPS_py_v2/backtest/robustness_v3/simple_config.py).

This gives the simplest v3 workflow.

### Example 2: Add MA optimization

In [UPS_py_v2/backtest/robustness_v3/simple_config.py](/root/projects/pine_and_bachtesting_py/UPS_py_v2/backtest/robustness_v3/simple_config.py), add:

```python
config.set_optional_parameter_range("ma_length", 20, 50, 100)
```

Now Step 1 will test those MA values together with the Boolean filters and RR values.

### Example 3: Add IQ internals only when IQ is relevant

In [UPS_py_v2/backtest/robustness_v3/simple_config.py](/root/projects/pine_and_bachtesting_py/UPS_py_v2/backtest/robustness_v3/simple_config.py), add:

```python
config.set_optional_parameter_range("iq_lookback", 10, 20, 30)
config.set_optional_parameter_range("iq_min_score", 0.45, 0.55, 0.65)
```

These values only expand the grid when `use_iq_filter=True`.

When `use_iq_filter=False`, v3 automatically falls back to the default baseline IQ values.

## Recommended workflow

1. Edit [UPS_py_v2/backtest/robustness_v3/simple_config.py](/root/projects/pine_and_bachtesting_py/UPS_py_v2/backtest/robustness_v3/simple_config.py).
2. Keep the first version simple: Boolean filters plus the four RR values.
3. Add optional parameter ranges only after the simple version produces stable candidates.
4. Use the matrix summary to judge whether the same setup survives across assets and timeframes.

## How to run

From the project root, use one of these:

```bash
python -m UPS_py_v2.backtest.run_v3
```

or:

```bash
python UPS_py_v2/backtest/run_v3.py
```

If you want the CLI-based version later, use:

```bash
python -m UPS_py_v2.backtest.optimize_v3
```

Important:
- `python -m UPS_py_v2/backtest/optimize_v3.py` is wrong because `-m` expects dots, not slashes.
- `UPS_py_v2/backtest/optimize_v3.py` by itself is not executable unless you add a shebang and execute permission.

## Output meaning

Step 1 output:
- ranked results on the primary dataset
- top `top_n` candidates are kept for Step 2

Step 2 output:
- validation results for each candidate across the matrix
- summary table showing coverage and how many datasets kept positive expectancy and return

## Notes

- The CLI file [UPS_py_v2/backtest/optimize_v3.py](/root/projects/pine_and_bachtesting_py/UPS_py_v2/backtest/optimize_v3.py) still exists for later advanced use.
- The normal v3 workflow should start from [UPS_py_v2/backtest/robustness_v3/simple_config.py](/root/projects/pine_and_bachtesting_py/UPS_py_v2/backtest/robustness_v3/simple_config.py) and [UPS_py_v2/backtest/run_v3.py](/root/projects/pine_and_bachtesting_py/UPS_py_v2/backtest/run_v3.py).