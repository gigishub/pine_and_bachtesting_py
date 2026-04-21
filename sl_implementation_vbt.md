# VBT-Native Stop-Loss Implementation Guide

Reference for replicating the entry-candle + swing trailing stop-loss pattern
from the Adaptive Momentum Strategy (AMS) in any new vectorbt-based strategy.

---

## Overview

The AMS precomputed exits (`close < stop_series`) still fire for explicit
strategy exits. The VBT-native SL fires on whichever comes first — the two
mechanisms are non-conflicting. When `use_vbt_sl=False` (default), behaviour
is identical to the original strategy.

---

## Files Changed / Created

### 1. `strategy/risk/stops_numba.py` — new file

Numba-compiled SL adjustment callbacks for VBT's `adjust_sl_func_nb`.

```python
@njit
def adjust_swing_sl_long_nb(c, swing_low_2d, atr_2d, n_atr_trail):
    """Ratchet long SL upward to swing_low[i] - n_atr * ATR[i]. Only tightens."""
    ...

@njit
def adjust_swing_sl_short_nb(c, swing_high_2d, atr_2d, n_atr_trail):
    """Ratchet short SL downward to swing_high[i] + n_atr * ATR[i]. Only tightens."""
    ...
```

**Rules:**
- Arrays must be 2D C-contiguous float64: `np.ascontiguousarray(arr.reshape(-1, 1))`
- Return `(new_frac, False)` to tighten, or `(c.curr_stop, c.curr_trail)` to hold
- Guard against `NaN` and invalid SL levels (SL crossing entry price)
- Floor the fraction at `0.001` (0.1% minimum SL distance)

---

### 2. `strategy/risk/stops.py` — additions

Pure-pandas functions to compute the initial SL fraction at entry.

```python
def compute_entry_candle_sl_long(high, low, close, atr, n_atr_init) -> pd.Series:
    # sl_frac = (close - (low - n_atr * ATR)) / close
    ...

def compute_entry_candle_sl_short(high, low, close, atr, n_atr_init) -> pd.Series:
    # sl_frac = ((high + n_atr * ATR) - close) / close
    ...

def compute_entry_candle_sl(high, low, close, atr, n_atr_init) -> tuple[pd.Series, pd.Series]:
    # Convenience wrapper returning (long_frac, short_frac)
    ...
```

---

### 3. `strategy/parameters.py` — 5 new fields

```python
# VBT-native SL (entry candle + swing trailing)
use_vbt_sl: bool = False            # off by default — backward compatible
sl_atr_period: int = 14
sl_n_atr_init: float = 0.5         # ATR buffer below entry candle low / above high
sl_n_atr_trail: float = 0.5        # ATR buffer below trailing swing low / above high
sl_swing_lookback: int = 10        # bars for rolling swing low / high
```

---

### 4. `backtest/vectorbt/runner.py` — wiring in `run()`

Before the `from_signals()` call, build SL arrays conditionally:

```python
sl_stop_long = sl_stop_short = None
adjust_sl_func_long = adjust_sl_func_short = None
adjust_sl_args_long = adjust_sl_args_short = None

if p.use_vbt_sl:
    atr = pta.atr(high, low, close, length=p.sl_atr_period)
    sl_frac_long, sl_frac_short = compute_entry_candle_sl(
        high, low, close, atr, n_atr_init=p.sl_n_atr_init
    )

    # Shift by 1 bar to match fill_at_next_open entry alignment
    if fill_at_next_open:
        sl_frac_long  = sl_frac_long.shift(1).bfill()
        sl_frac_short = sl_frac_short.shift(1).bfill()

    swing_low  = low.rolling(p.sl_swing_lookback).min()
    swing_high = high.rolling(p.sl_swing_lookback).max()

    # VBT Numba callbacks require 2D C-contiguous float64 arrays
    swing_low_2d  = np.ascontiguousarray(swing_low.values.reshape(-1, 1))
    swing_high_2d = np.ascontiguousarray(swing_high.values.reshape(-1, 1))
    atr_2d        = np.ascontiguousarray(atr.values.reshape(-1, 1))

    sl_stop_long  = sl_frac_long.values
    sl_stop_short = sl_frac_short.values
    adjust_sl_func_long  = adjust_swing_sl_long_nb
    adjust_sl_func_short = adjust_swing_sl_short_nb
    adjust_sl_args_long  = (swing_low_2d,  atr_2d, p.sl_n_atr_trail)
    adjust_sl_args_short = (swing_high_2d, atr_2d, p.sl_n_atr_trail)
```

Then pass to `from_signals()` using the `**sl_kwargs` pattern:

```python
# ⚠ Critical: VBT rejects adjust_sl_func_nb=None — never pass None directly.
# Only include these kwargs when the SL was successfully built.
active_sl_stop = sl_stop_long if p.use_long else sl_stop_short
active_sl_func = adjust_sl_func_long if p.use_long else adjust_sl_func_short
active_sl_args = adjust_sl_args_long if p.use_long else adjust_sl_args_short

sl_kwargs: dict = {}
if active_sl_stop is not None and active_sl_func is not None:
    sl_kwargs = {
        "sl_stop":           active_sl_stop,
        "adjust_sl_func_nb": active_sl_func,
        "adjust_sl_args":    active_sl_args,
    }

return vbt.Portfolio.from_signals(
    ...,
    **sl_kwargs,
)
```

---

### 5. `backtest/config.py` — `MomentumGridConfig` additions

**New sweep range fields:**

```python
sl_n_atr_init_range:    tuple[float, ...] = (0.5,)
sl_n_atr_trail_range:   tuple[float, ...] = (0.5,)
sl_swing_lookback_range: tuple[int, ...]  = (10,)
```

**Wire into `parameter_names` and `parameter_ranges`:**

```python
if len(self.sl_n_atr_init_range) > 1:
    names.append("sl_n_atr_init")
if len(self.sl_n_atr_trail_range) > 1:
    names.append("sl_n_atr_trail")
if len(self.sl_swing_lookback_range) > 1:
    names.append("sl_swing_lookback")
```

**Wire into `feature_dependencies`** (deduplicates when `use_vbt_sl=False`):

```python
"sl_n_atr_init":     ("use_vbt_sl",),
"sl_n_atr_trail":    ("use_vbt_sl",),
"sl_swing_lookback": ("use_vbt_sl",),
```

**Wire into `param_audit`:**

```python
("sl_n_atr_init",    self.sl_n_atr_init_range),
("sl_n_atr_trail",   self.sl_n_atr_trail_range),
("sl_swing_lookback", self.sl_swing_lookback_range),
```

**Add to the default `boolean_filter_ranges`:**

```python
"use_vbt_sl": (False,),   # off by default; set (False, True) to sweep
```

---

### 6. All existing phase configs

Every file in `backtest/configs/` that passes an explicit `boolean_filter_ranges`
must include `use_vbt_sl`, because `validate_coverage()` (called by the sequencer)
checks every `bool` field in `Parameters`.

```python
"use_vbt_sl": (False,),   # pinned off in existing phases
```

---

### 7. Tests — `tests/test_pipeline.py`

Add `"use_vbt_sl"` to the `_ALL_AUDITABLE` list and update the comment:

```python
# All 20 auditable flags (10 long + 9 short + 1 VBT SL)
_ALL_AUDITABLE = [
    ...existing 19 flags...,
    "use_vbt_sl",
]
```

---

## Checklist for a New Strategy

- [ ] Copy `stops_numba.py` as-is — it is generic
- [ ] Copy the three SL functions from `stops.py` — they are generic
- [ ] Add the 5 SL fields to your `Parameters` dataclass
- [ ] Add the 3 range fields + `feature_dependencies` entries to your grid config
- [ ] Add `"use_vbt_sl": (False,)` to the default `boolean_filter_ranges` in the grid config
- [ ] Add `"use_vbt_sl": (False,)` to every existing phase config's `boolean_filter_ranges`
- [ ] Use the `**sl_kwargs` pattern in `runner.py` — never pass `None` to VBT
- [ ] Update `_ALL_AUDITABLE` in tests

---

## Test Config (`backtest/configs/sl_sweep_test.py`)

Minimal smoke test: 3 symbols × 2 timeframes × 28 combos ≈ 8 minutes.

```
use_vbt_sl:         (False, True)       # baseline vs SL enabled
sl_n_atr_init:      (0.25, 0.5, 1.0)   # initial buffer
sl_n_atr_trail:     (0.25, 0.5, 1.0)   # trailing buffer
sl_swing_lookback:  (5, 10, 20)         # lookback bars
```

Feature dependencies collapse all `use_vbt_sl=False` combos to 1, so the
effective grid is 1 + 27 = 28 unique combos per condition.

Run with:

```bash
source .venv/bin/activate
python -m adaptive_momentum_strategy.backtest.vectorbt.run --config sl_sweep_test
```
