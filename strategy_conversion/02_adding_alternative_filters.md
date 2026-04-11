# Phase 2 Guide: Adding and Testing Alternative Filter Options

How to extend a strategy built with `01_translation_guide.md` by adding multiple
options for each layer (Regime / Setup / Trigger / Exit) and verifying they all
work independently before running a combination grid-search.

---

## When to use this guide

After Phase 1 (single golden-path combination working and validated), use this
guide when the strategy description lists multiple indicator alternatives per
layer and you want to test every valid combination.

---

## Step 1 — Audit the strategy spec for alternatives

Re-read the strategy description. For each layer, list every option and classify
it as implementable from OHLCV or not.

| Layer | Option | OHLCV-feasible? | Notes |
|-------|--------|-----------------|-------|
| Regime | Option A (e.g. ADX) | ✅ already built | Phase 1 default |
| Regime | Option B (e.g. MVRV Z-Score) | ❌ | Requires on-chain API (Glassnode) |
| Regime | Option C (e.g. EMA Ribbon) | ✅ | Add this |
| Setup | Option A (e.g. Donchian) | ✅ already built | Phase 1 default |
| Setup | Option B (e.g. Volume Profile VAH) | ✅ | Add this |
| Setup | Option C (e.g. Relative Strength) | ✅ needs benchmark data | Add this, extra arg required |
| Trigger | Option A (e.g. CMF) | ✅ already built | Phase 1 default |
| Trigger | Option B (e.g. CVD) | ❌ | Requires tick-level trade data |
| Trigger | Option C (e.g. Power Candle) | ✅ | Add this |
| Exit | Option A (e.g. Chandelier) | ✅ already built | Phase 1 default |
| Exit | Option B (e.g. Parabolic SAR) | ✅ | Add this |
| Exit | Option C (e.g. Bollinger Band) | ✅ | Add this |

**Rule:** never include an option that requires unavailable data. Document why it
was excluded in both `parameters.py` and `signals.py`.

---

## Step 2 — Add boolean flags to `Parameters`

Add one `bool` field per available option.  The flags are **independent** — any
combination can be active simultaneously.  Keep the Phase 1 option defaulting to
`True` so nothing changes unless you explicitly turn it off.

```python
@dataclass
class Parameters:
    # --- Regime flags (at least one must be True) ---
    use_adx:            bool = True    # ADX(14) > threshold
    use_ema_ribbon:     bool = False   # EMA(20) > EMA(50) > EMA(200)

    # --- Setup flags (at least one must be True) ---
    use_donchian:       bool = True    # Donchian breakout + volatility squeeze
    use_volume_profile: bool = False   # Rolling VAH breakout
    # use_relative_strength: bool  # excluded — requires benchmark DataFrame

    # --- Trigger flags (at least one must be True) ---
    use_cmf:            bool = True    # CMF(20) > threshold
    use_power_candle:   bool = False   # Close > High(N) + high volume

    # --- Exit flags (at least one must be True) ---
    use_chandelier:     bool = True    # ATR trailing stop (ratcheted)
    use_psar:           bool = False   # Parabolic SAR (self-managing)
    use_bbands:         bool = False   # Bollinger Band upper (self-managing)

    # Add params for every new indicator here, even when not the default.
    # They are ignored when their flag is False.
    ema_fast_period:  int   = 20
    ema_mid_period:   int   = 50
    ema_slow_period:  int   = 200
    # ... etc
```

**Rules:**
- All boolean flags for all options live in the same `Parameters` dataclass.
- Unused params are simply ignored when their flag is False.
- Never use string selectors (`regime_mode: str = "adx"`) — booleans compose
  without branching and are safely serialisable to CSV by vectorbt.

---

## Step 3 — Create one file per new indicator

One file per option.  Same function signature pattern as Phase 1 indicators:
- `compute_<indicator>(...)` → raw float `Series`
- `<layer>_is_<condition>(...)` → boolean `Series`

New files go in `strategy/indicators/` (for regime/setup/trigger options) or
`strategy/risk/` (for exit options).

```
strategy/indicators/
    ema_ribbon.py        # Regime C
    volume_profile.py    # Setup B
    relative_strength.py # Setup C
    power_candle.py      # Trigger C

strategy/risk/
    psar.py              # Exit B
    bbands.py            # Exit C
```

### Exit-specific: ratchet vs direct update

Not all exit indicators should be ratcheted.  Ask: does the indicator self-manage
its direction, or does it need to be prevented from loosening?

| Exit option | Update style | Why |
|-------------|-------------|-----|
| Chandelier SAR | Ratchet (`max(current, candidate)`) | Raw stop can decrease; must lock in gains |
| Parabolic SAR | Direct (`_trail_stop = candidate`) | PSAR self-accelerates toward price; ratcheting would override its logic |
| Bollinger Band upper | Direct | Upper band is meant to move dynamically |

Record this decision in the runner (see Step 5).

---

## Step 4 — Update `signals.py` with collect-and-AND logic

Rewrite `compute_signals()` to compute **every option unconditionally**, then
combine active signals using AND-logic per entry layer and OR-logic for exits.
Never branch on which options are active — always compute all of them.

```
compute ALL indicators
    │
    ├─ regime:  compute adx AND ema_ribbon
    ├─ setup:   compute donchian AND vah AND relative_strength
    ├─ trigger: compute cmf AND power_candle
    └─ exit:    compute chandelier AND psar AND bbands
         │
         ▼
collect active signals per layer (based on flags):
    regime_signals  ← [adx_regime  if use_adx,  ema_aligned if use_ema_ribbon]
    setup_signals   ← [donchian_sig if use_donchian, vah_sig if use_volume_profile]
    trigger_signals ← [cmf_sig if use_cmf, power_candle_sig if use_power_candle]
    exit_stops      ← [chandelier if use_chandelier, psar_stop if use_psar,
                        bb_upper if use_bbands]
         │
         ▼
combine:
    regime_filter  ← _and_signals(regime_signals)   # ALL active must be True
    setup_signal   ← _and_signals(setup_signals)
    trigger_signal ← _and_signals(trigger_signals)
    stop_series    ← max(exit_stops, axis=1)         # OR-logic: highest stop fires first
```

### Why AND for entry layers, OR for exit?

- **Entry (AND):** each active filter adds conviction.  If both ADX and EMA Ribbon
  are enabled, price must satisfy *both* before entering.  More conditions = more
  selective.
- **Exit (OR):** any active stop firing first protects the position.  If Chandelier
  and PSAR are both enabled, whichever stop is higher at any bar is the active stop.
  The position closes as soon as price crosses the nearest stop.

### Helper: `_and_signals()`

```python
def _and_signals(signals: list[pd.Series]) -> pd.Series:
    """AND a list of float 0/1 Series into one float 0/1 Series."""
    if not signals:
        raise ValueError("No active signals to combine — at least one flag must be True")
    result = signals[0].astype(bool)
    for s in signals[1:]:
        result = result & s.astype(bool)
    return result.astype(float)
```

### Exit OR-logic

```python
active_stops = [
    s for s, flag in [
        (chandelier_stop, params.use_chandelier),
        (psar_stop,       params.use_psar),
        (bb_upper,        params.use_bbands),
    ] if flag
]
if not active_stops:
    raise ValueError("At least one exit flag must be True")
# pd.concat + max = OR-logic: highest active stop fires first
stop_series = pd.concat(active_stops, axis=1).max(axis=1)
```

### Canonical output keys (consumed by runner — never change these names)

| Key | Type | Description |
|-----|------|-------------|
| `regime_filter` | float 0/1 | AND of all active regime flags |
| `setup_signal` | float 0/1 | AND of all active setup flags |
| `trigger_signal` | float 0/1 | AND of all active trigger flags |
| `stop_series` | float | OR-max of all active exit stops |
| `is_ready` | float 0/1 | All indicators warmed up |

### Warmup gate — always use all warmup conditions

```python
# Collect notna() from every indicator unconditionally.
# Gate opens when the slowest indicator warms up.
warmup_conditions = [
    adx.notna(),
    ema_slow.notna(),
    donchian_upper.notna(),
    squeeze_ready,           # rolling quantile over longer window
    vah.notna(),
    cmf.notna(),
    power_candle_lookback.notna(),
    chandelier_stop.notna(),
    psar_stop.notna(),
    bb_upper.notna(),
]
is_ready = pd.concat(warmup_conditions, axis=1).all(axis=1).astype(float)
```

⚠️ **Anti-pattern:** `regime_ready = regime_filter.astype(bool)` — this is False
both during warmup AND whenever the condition is not met.  Use `.notna()` on the
underlying raw Series, never on the boolean signal.

### Validate flags early

Add a `_validate_flags(params)` function that raises `ValueError` when any layer
has all flags off.  Call it at the top of `compute_signals()`.

```python
_LAYER_GROUPS = {
    "regime":  ("use_adx", "use_ema_ribbon"),
    "setup":   ("use_donchian", "use_volume_profile"),
    "trigger": ("use_cmf", "use_power_candle"),
    "exit":    ("use_chandelier", "use_psar", "use_bbands"),
}

def _validate_flags(params: Parameters) -> None:
    for layer, flags in _LAYER_GROUPS.items():
        if not any(getattr(params, f) for f in flags):
            raise ValueError(
                f"At least one {layer} flag must be True. "
                f"Got all False for: {flags}"
            )
```

---

## Step 5 — Update the runner

### Expose boolean flags as class attributes

```python
class MyStrategy(Strategy):
    use_adx:            bool = True
    use_ema_ribbon:     bool = False
    use_donchian:       bool = True
    use_volume_profile: bool = False
    use_cmf:            bool = True
    use_power_candle:   bool = False
    use_chandelier:     bool = True
    use_psar:           bool = False
    use_bbands:         bool = False
    # Numeric params also exposed here:
    adx_threshold:      float = 25.0
    # ...
```

### Handle exit ratchet decision in `init()`

```python
def init(self) -> None:
    params = Parameters(
        use_adx=self.use_adx,
        use_ema_ribbon=self.use_ema_ribbon,
        # ... all other flags
    )
    signals = compute_signals(self.data.df.copy(), params)
    # ...
    # Ratchet only when chandelier is active — it's the only stop that can loosen.
    # psar and bbands self-manage their direction and are assigned directly.
    self._ratchet_stop = params.use_chandelier
```

### Use the flag in `next()`

```python
if in_position and not math.isnan(stop_candidate):
    if self._ratchet_stop:
        self._trail_stop = ratchet_stop(
            self._trail_stop, stop_candidate, self.position.size
        )
    else:
        self._trail_stop = stop_candidate  # psar / bbands manage their own direction
```

---

## Step 6 — Write tests for each new indicator and each flag combination

### New indicator tests (`test_indicators.py`)

For each new indicator file, add a test class with at minimum:

- Output length matches input length
- NaN during warmup period (first N bars)
- Values within valid mathematical range
- Boolean output contains only `{True, False}`
- Signal fires in a synthetic scenario designed to trigger it

```python
class TestEMARibbon:
    def test_returns_three_series(self): ...
    def test_aligned_on_strong_trend(self): ...    # monotonically rising price → all True
    def test_not_aligned_in_downtrend(self): ...   # monotonically falling price → all False
    def test_output_is_boolean(self): ...
```

### Flag combination tests (`test_signals.py`)

Add tests that verify AND-logic for entry layers and OR-logic for exits:

```python
class TestRegimeFlags:
    def test_only_adx_active(self):
        params = Parameters(use_adx=True, use_ema_ribbon=False)
        out = compute_signals(df, params)
        pd.testing.assert_series_equal(
            out["regime_filter"], out["adx_regime"], check_names=False
        )

    def test_both_flags_true_gives_and(self):
        params = Parameters(use_adx=True, use_ema_ribbon=True)
        out = compute_signals(df, params)
        expected = (
            out["adx_regime"].astype(bool) & out["ema_ribbon_regime"].astype(bool)
        ).astype(float)
        pd.testing.assert_series_equal(out["regime_filter"], expected, check_names=False)

    def test_all_regime_flags_false_raises(self):
        with pytest.raises(ValueError, match="regime"):
            compute_signals(df, Parameters(use_adx=False, use_ema_ribbon=False))


class TestExitFlags:
    def test_stop_is_max_of_chandelier_and_psar(self):
        params = Parameters(use_chandelier=True, use_psar=True, use_bbands=False)
        out = compute_signals(df, params)
        expected = pd.concat(
            [out["chandelier_stop"], out["psar_stop"]], axis=1
        ).max(axis=1)
        pd.testing.assert_series_equal(out["stop_series"], expected, check_names=False)

    def test_single_exit_active(self):
        # When only one exit is active, stop_series equals that exit's raw series.
        params = Parameters(use_chandelier=True, use_psar=False, use_bbands=False)
        out = compute_signals(df, params)
        pd.testing.assert_series_equal(
            out["stop_series"], out["chandelier_stop"], check_names=False
        )
```

---

## Step 7 — Validate each flag combination individually before running a full grid

Run the backtest once per meaningful combination to confirm it fires trades and
behaves sensibly.  Use the behavioural checklist from `01_translation_guide.md` Step 9.

```bash
# Default (Phase 1 — ADX + Donchian + CMF + Chandelier)
python -m <strategy>.backtest.backtesting_py.run

# Then test alternatives by editing BacktestConfig or Parameters defaults:
use_ema_ribbon=True, use_adx=False   → still fires trades?
use_volume_profile=True, use_donchian=False  → stop updates correctly?
use_psar=True, use_chandelier=False  → no NaN errors?
```

Any combination that fires zero trades needs investigation before being included
in a grid-search.  Common causes:
- Warmup too long (not enough data)
- Threshold too strict for the symbol/timeframe
- `is_ready` gating incorrectly (warmup anti-pattern above)

---

## Step 8 — Count valid combinations and plan the grid-search

Count only the OHLCV-feasible options.  With boolean flags, the total grid size is:

```
2^(regime_flags) × 2^(setup_flags) × 2^(trigger_flags) × 2^(exit_flags)
```

Minus invalid combos (any layer group entirely False).  The valid-combo filter in
`pipeline.py` removes these automatically before running.

Example (Adaptive Momentum Strategy):
- 2 regime flags × 2 setup flags × 2 trigger flags × 3 exit flags = 2×2×2×8 = 64 per layer-product
- Total with Cartesian product of all 9 flags: 2^9 = 512
- After removing combos where any layer group is all False: **189 valid combos**

Note any combinations that require extra data (e.g. `relative_strength` needs a
benchmark DataFrame).  Handle those separately or exclude from the automated grid.

The grid-search itself is Phase 3 (`03_vectorbt_grid_search.md`).  This phase only
establishes that every individual flag combination works correctly in isolation.

---

## Checklist before moving to Phase 3 (grid-search)

- [ ] One file per new indicator, all following the same function signature pattern
- [ ] `Parameters` has boolean flag fields with Phase 1 defaults (`True`)
- [ ] `signals.py` computes all options unconditionally
- [ ] `_and_signals()` used for entry layer combination (AND-logic)
- [ ] `pd.concat(...).max(axis=1)` used for exit combination (OR-logic)
- [ ] `_validate_flags()` raises `ValueError` when any layer group is all False
- [ ] `stop_series` canonical key is the OR-max of all active exit stops
- [ ] Runner reads boolean flag class attrs; `_ratchet_stop = params.use_chandelier`
- [ ] New indicator tests: length, warmup NaN, valid range, boolean output, fires in synthetic scenario
- [ ] Flag combination tests: single flag matches raw series; both flags → AND result; all-False → raises
- [ ] Exit OR-logic test: stop_series == max of active stops
- [ ] All tests pass
- [ ] Default (Phase 1) backtest re-run and produces same result as before Phase 2
