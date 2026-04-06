# Adding Indicators, Entry Signals & Exit Signals

A step-by-step guide for extending the UPS strategy with new indicators, entry filters, or exit logic — and wiring them into the robustness backtest grid.

---

## Architecture overview

```
strategy/indicators/          ← pure computation modules (one responsibility each)
strategy/signals.py           ← orchestrator: calls all indicators, returns dict of Series
strategy/strategy_parameters.py  ← StrategySettings dataclass (all parameter defaults)
strategy/decision/entry.py    ← entry gate logic (pure booleans)
strategy/decision/exit.py     ← exit gate logic (pure booleans)
backtest/robustness_v4/config.py       ← grid ranges, feature dependencies
backtest/robustness_v4/simple_config.py ← the only file you edit for a normal run
```

---

## Step 1 — Write the indicator module

Create a new file in `strategy/indicators/` (or add a function to an existing one if the scope is small).

Rules:
- Pure functions only — no `print()`, no side effects, no imports from decision or backtest layers.
- Return a `dict[str, pd.Series]` so `signals.py` can unpack it with `**`.
- Type-hint every signature.
- Add a docstring explaining what the indicator measures and what each returned key means.

**Example — `strategy/indicators/rsi.py`:**

```python
from __future__ import annotations

import pandas as pd


def compute_rsi_filter(
    close: pd.Series,
    period: int,
    threshold: float,
    use_rsi_filter: bool,
) -> dict[str, pd.Series]:
    """RSI trend-bias filter.

    Returns:
        rsi_value:        raw RSI series
        rsi_long_filter:  True when RSI > threshold (bullish bias)
        rsi_short_filter: True when RSI < (100 - threshold) (bearish bias)
    """
    if not use_rsi_filter:
        true_s = pd.Series(True, index=close.index)
        return {
            "rsi_value": pd.Series(50.0, index=close.index),
            "rsi_long_filter": true_s,
            "rsi_short_filter": true_s,
        }

    delta = close.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = (-delta.clip(upper=0)).rolling(period).mean()
    rs = gain / loss.replace(0, float("nan"))
    rsi = 100 - (100 / (1 + rs))

    return {
        "rsi_value": rsi,
        "rsi_long_filter": rsi > threshold,
        "rsi_short_filter": rsi < (100 - threshold),
    }
```

> **Tip:** When `use_X_filter=False`, return a neutral Series (`True` for filters, `0.0` for values) so downstream code never receives NaN.

---

## Step 2 — Wire into `signals.py`

Open `strategy/signals.py` and make three edits:

### 2a. Import the new function
```python
from .indicators.rsi import compute_rsi_filter
```

### 2b. Add parameters to `build_strategy_series()` signature
```python
def build_strategy_series(
    df: pd.DataFrame,
    # ... existing params ...
    # RSI filter
    use_rsi_filter: bool,
    rsi_period: int,
    rsi_threshold: float,
) -> dict[str, pd.Series]:
```

### 2c. Call the function and merge its output
```python
rsi = compute_rsi_filter(
    close=close,
    period=rsi_period,
    threshold=rsi_threshold,
    use_rsi_filter=use_rsi_filter,
)

return {
    **base,
    **iq,
    **pullback,
    **patterns,
    **rsi,          # ← add here
    "long_stop_price": zero_float,
    ...
}
```

If the new filter affects entry logic, pass the relevant Series into `compute_long_pattern_and_entry_series()` (in `candlestick_patterns.py`) so it gates entry signals.

---

## Step 3 — Add defaults to `StrategySettings`

Open `strategy/strategy_parameters.py` and add the new parameters with sensible defaults:

```python
@dataclass
class StrategySettings:
    # ... existing fields ...

    # RSI filter
    use_rsi_filter: bool = False          # off by default — grid will test both
    rsi_period: int = 14
    rsi_threshold: float = 55.0
```

> Keep new filters `False` by default so existing baselines are unchanged.

---

## Step 4 — Register in the robustness grid

### 4a. Declare feature dependencies (if needed)

Open `backtest/robustness_v4/config.py`. If child parameters only matter when a parent flag is `True`, add entries to `DEFAULT_FEATURE_DEPENDENCIES`. This prevents the grid from generating duplicate combinations when the parent is off.

```python
DEFAULT_FEATURE_DEPENDENCIES: dict[str, tuple[str, ...]] = {
    # ... existing entries ...
    "rsi_period":    ("use_rsi_filter",),
    "rsi_threshold": ("use_rsi_filter",),
}
```

### 4b. Add to `simple_config.py`

This is the only file you need to edit for a normal run:

```python
# Toggle the filter on/off in the grid
config.boolean_filter_ranges["use_rsi_filter"] = (False, True)

# Optionally sweep numeric parameters (only tested when use_rsi_filter=True)
config.set_optional_parameter_range("rsi_period", 10, 14, 20)
config.set_optional_parameter_range("rsi_threshold", 50.0, 55.0, 60.0)
```

> **Grid size warning:** every boolean filter doubles the combination count (2^n).  
> 6 boolean filters × 2 R:R values = 128 combinations per condition.  
> Adding a 7th filter → 256. Keep the numeric sweep small to compensate.

---

## Step 5 — Adding a new entry pattern

Entry patterns live in `strategy/indicators/candlestick_patterns.py` inside `compute_long_pattern_and_entry_series()`.

1. Add the boolean flag parameter: `enable_my_pattern: bool`
2. Compute the pattern Series using OHLC logic.
3. OR it into `long_entry_pattern` / `short_entry_pattern`:
   ```python
   long_entry_pattern = long_entry_pattern | (enable_my_pattern & my_pattern_long)
   ```
4. Add `enable_my_pattern: bool` to `build_strategy_series()` in `signals.py` and pass it through.
5. Add it to `StrategySettings` with a default.
6. Add it to `boolean_filter_ranges` in `simple_config.py`.

---

## Step 6 — Adding a new exit signal

Exit logic lives in `strategy/decision/exit.py` and is called bar-by-bar by the backtest strategy class.

1. Add a new function or parameter to `exit.py`.
2. Wire the parameter through `StrategySettings`.
3. If it is a pure on/off toggle, add it to `boolean_filter_ranges` in `simple_config.py`.
4. If it is numeric (e.g. a trailing stop multiplier), use `set_optional_parameter_range()`.

---

## Quick reference checklist

| Task | File(s) to edit |
|---|---|
| New indicator computation | `strategy/indicators/<name>.py` (new file) |
| Wire indicator into pipeline | `strategy/signals.py` |
| Add parameter defaults | `strategy/strategy_parameters.py` |
| **Declare class variables on the strategy** | **`backtest/strategy.py`** — add as class variable AND pass in `init()` |
| Declare parent/child dependencies | `backtest/robustness_v4/config.py` → `DEFAULT_FEATURE_DEPENDENCIES` |
| Configure the robustness run | `backtest/robustness_v4/simple_config.py` |
| New entry pattern | `strategy/indicators/candlestick_patterns.py` + signals.py + parameters |
| New exit signal | `strategy/decision/exit.py` + signals.py (if precomputed) + parameters |

---

## ⚠️ Common mistake: missing class variable in `strategy.py`

`backtesting.py` requires **every parameter passed to `Backtest.run()`** to be declared as a class-level variable on the `Strategy` class. If you forget this step you will see:

```
Strategy 'UPSStrategy' is missing parameter '<name>'.
Strategy class should define parameters as class variables before they can be optimized or run with.
```

**Two things must be done in `backtest/strategy.py` for every new parameter:**

### 1. Declare the class variable (matches the default in `StrategySettings`)
```python
class UPSStrategy(Strategy):
    # ... existing params ...

    # RSI filter
    use_rsi_filter = False
    rsi_period = 14
    rsi_overbought = 70.0
```

### 2. Pass it to `build_strategy_series()` inside `init()`
```python
def init(self) -> None:
    signals = build_strategy_series(
        ...
        use_rsi_filter=self.use_rsi_filter,
        rsi_period=self.rsi_period,
        rsi_overbought=self.rsi_overbought,
        ...
    )
```

> **Rule of thumb:** every key in `StrategySettings` must have a matching class variable in `UPSStrategy` with the same name and default value.

---

## Testing

Add a test for every non-trivial indicator function in `strategy/tests/test_indicators.py` (create the file if it doesn't exist). Cover at minimum:
- Normal inputs produce expected output shape and dtype.
- `use_X_filter=False` returns all-True filter Series (no NaN).
- Edge case: all-NaN close, single-bar DataFrame.
