# Strategy Translation Template

## How to go from a written strategy idea to structured, backtestable Python code

This template follows the architecture built in `adaptive_momentum_strategy/`. Every strategy maps onto the same 4-layer filter stack and the same directory layout. Fill in each section top-to-bottom before writing any code.

## Phase 1
---

## Step 0 — Parse the Strategy Idea

Read the strategy description and extract exactly four things. If you can't fill in all four, the strategy is not ready to code.

| Layer | Question | Source in description |
|-------|----------|-----------------------|
| **Regime** | *When is this market tradeable at all?* | Look for: trend filter, macro condition, market-phase check |
| **Setup** | *Where is the specific entry zone?* | Look for: price structure, pattern, level, range |
| **Trigger** | *What confirms commitment to the move?* | Look for: volume, momentum, order-flow confirmation |
| **Exit** | *What ends the trade?* | Look for: trailing stop, target, time-based close |

### Example extraction (from Strategy I)

| Layer | Raw description | Extracted condition |
|-------|----------------|---------------------|
| Regime | "ADX > 25 signals trend intensity" | `ADX(14) > 25.0` |
| Setup | "Donchian breakout from volatility squeeze" | `close >= donchian_upper * 0.99` AND channel width in bottom 25th pct |
| Trigger | "CMF cross above 0.05 confirms buyers" | `CMF(20) > 0.05` |
| Exit | "Chandelier SAR ratchets upward" | `close < rolling_high(22) - ATR(22) × 3.0` |

---

## Step 1 — Define the Directory Structure

Replace `<strategy_name>` with a lowercase snake_case name describing the strategy's core idea (e.g., `adaptive_momentum_strategy`, `mean_reversion_vwap`, `funding_rate_arb`).

```
<strategy_name>/
├── __init__.py
├── README.md
├── strategy/                   # Pure logic — zero I/O
│   ├── __init__.py
│   ├── parameters.py           # @dataclass with all tunable values
│   ├── signals.py              # compute_signals(df, params) → dict[str, Series]
│   ├── indicators/
│   │   ├── __init__.py
│   │   ├── <regime_indicator>.py
│   │   ├── <setup_indicator>.py
│   │   └── <trigger_indicator>.py
│   ├── decision/
│   │   ├── __init__.py
│   │   ├── entry.py            # should_buy(regime, setup, trigger, in_position) → bool
│   │   └── exit.py             # should_sell(close, trail_stop, in_position) → bool
│   └── risk/
│       ├── __init__.py
│       ├── stops.py            # stop series + ratchet helper
│       └── sizing.py           # compute_position_size(entry, stop, equity, risk_pct)
├── backtest/
│   ├── __init__.py
│   ├── config.py               # BacktestConfig + MomentumGridConfig dataclasses
│   ├── simple_config.py        # User-facing config — only file you should edit
│   ├── runner.py               # Backward-compat shim → imports from backtesting_py/
│   └── backtesting_py/         # Single-run backtesting.py engine (Phase 1 reference)
│       ├── __init__.py
│       ├── strategy.py         # Strategy class with boolean flag class attrs
│       ├── runner.py           # load_data() + run_backtest()
│       └── run.py              # __main__ entry point
└── tests/
    ├── __init__.py
    ├── test_indicators.py
    ├── test_decision.py
    └── test_signals.py
```

**Rules:**
- `strategy/` must have zero I/O and zero backtesting imports. It is tested standalone.
- `backtest/` and `live/` are the only consumers of `strategy/`.
- One file = one responsibility. Never mix data loading, indicator math, and decision logic.

---

## Step 2 — Write `parameters.py`

One `@dataclass` with every tunable value and its golden-path default. No logic here.

```python
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Parameters:
    # --- Regime ---
    <regime_param>: int = <default>          # e.g. adx_period: int = 14
    <regime_threshold>: float = <default>    # e.g. adx_threshold: float = 25.0

    # --- Setup ---
    <setup_param>: int = <default>
    <setup_param_2>: int = <default>

    # --- Trigger ---
    <trigger_param>: int = <default>
    <trigger_threshold>: float = <default>

    # --- Exit ---
    <exit_lookback>: int = <default>
    <exit_multiplier>: float = <default>

    # --- Sizing ---
    risk_pct: float = 1.0                    # % of equity risked per trade
```

---

## Step 3 — Write Each Indicator Module

### 3a — Regime indicator (`indicators/<name>.py`)

```python
import pandas as pd

def compute_<regime>(high, low, close, period: int = 14) -> pd.Series:
    """Return the raw indicator value as a float Series."""
    ...

def regime_is_<condition>(series: pd.Series, threshold: float) -> pd.Series:
    """Return a boolean Series: True when regime is valid for trading."""
    return series > threshold
```

### 3b — Setup indicator (`indicators/<name>.py`)

```python
import pandas as pd

def compute_<setup_level>(price: pd.Series, lookback: int) -> pd.Series:
    """Return the structural price level (e.g. rolling high, VWAP, etc.)."""
    ...

def setup_is_active(close, level, <squeeze_or_qualifier>) -> pd.Series:
    """Return True when price is at the structural entry zone."""
    ...
```

### 3c — Trigger indicator (`indicators/<name>.py`)

```python
import pandas as pd

def compute_<trigger>(high, low, close, volume, period: int) -> pd.Series:
    """Return confirmation oscillator (momentum, flow, delta, etc.)."""
    ...

def trigger_is_active(series: pd.Series, threshold: float) -> pd.Series:
    """Return True when confirmation condition is met."""
    return series > threshold
```

### Key indicator rules

- All functions accept `pd.Series`, return `pd.Series` of the same length.
- NaN during warmup — never fill or forward-fill indicator warmup NaNs.
- No lookahead — use `.rolling(n).max()` not `.rolling(n, center=True).max()`.
- Current bar is included — `next()` sees a closed bar, so no `.shift(1)` needed on the indicator itself. The entry fills at the **next** bar's open.

---

## Step 4 — Write `risk/stops.py` and `risk/sizing.py`

### stops.py

```python
def compute_<stop>_series(high, low, close, lookback, multiplier) -> pd.Series:
    """Precompute the stop candidate for every bar.
    
    This is the raw level before ratcheting. The runner ratchets it upward
    bar-by-bar while a position is open so it never loosens.
    """
    ...

def ratchet_stop(
    current_stop: float | None,
    candidate_stop: float,
    position_size: float,
) -> float | None:
    """Never loosen the stop. Return None when no position is held."""
    if position_size <= 0:
        return None
    if current_stop is None:
        return float(candidate_stop)
    return float(max(current_stop, candidate_stop))
```

### sizing.py

```python
def compute_position_size(
    entry_price: float,
    stop_price: float,
    equity: float,
    risk_pct: float = 1.0,
) -> float:
    """Return fraction of equity to deploy (0.0 – 0.9999).
    
    Fraction is passed directly to backtesting.py self.buy(size=fraction).
    """
    stop_distance = entry_price - stop_price
    if stop_distance <= 0 or equity <= 0:
        return 0.0
    risk_cash = equity * risk_pct / 100
    units = risk_cash / stop_distance
    fraction = (units * entry_price) / equity
    return min(fraction, 0.9999)
```

---

## Step 5 — Write `decision/entry.py` and `decision/exit.py`

These are pure boolean functions with no pandas, no state.

```python
# entry.py
def should_buy(regime: bool, setup: bool, trigger: bool, in_position: bool) -> bool:
    """All three filters must pass. No re-entry while already in trade."""
    if in_position:
        return False
    return regime and setup and trigger

# exit.py
def should_sell(close: float, trail_stop: float | None, in_position: bool) -> bool:
    """Exit when close falls below the active trailing stop."""
    if not in_position or trail_stop is None:
        return False
    return close < trail_stop
```

---

## Step 6 — Write `signals.py`

This is the single orchestrator called once in `Strategy.init()`. It precomputes all indicator Series and returns them as a dict. The runner calls nothing else from `strategy/`.

```python
def compute_signals(df: pd.DataFrame, params: Parameters) -> dict[str, pd.Series]:
    high   = df["High"].astype(float)
    low    = df["Low"].astype(float)
    close  = df["Close"].astype(float)
    volume = df["Volume"].fillna(0.0).astype(float)

    # 1. Compute raw indicators
    <regime_series>  = compute_<regime>(high, low, close, params.<regime_param>)
    <setup_level>    = compute_<setup>(high, params.<setup_param>)
    <trigger_series> = compute_<trigger>(high, low, close, volume, params.<trigger_param>)
    <stop_series>    = compute_<stop>_series(high, low, close, params.<exit_lookback>, params.<exit_mult>)

    # 2. Compute boolean signals
    regime_filter  = regime_is_<condition>(<regime_series>, params.<regime_threshold>)
    setup_signal   = setup_is_active(close, <setup_level>, ...)
    trigger_signal = trigger_is_active(<trigger_series>, params.<trigger_threshold>)

    # 3. Warmup gate — True only once ALL indicators have enough history
    #    Use .notna() checks, never use a signal boolean as a warmup proxy.
    <warmup_check> = <some_rolling_series>.notna()
    is_ready = (
        <regime_series>.notna()
        & <setup_level>.notna()
        & <warmup_check>          # for any indicator needing extra history
        & <trigger_series>.notna()
        & <stop_series>.notna()
    )

    def _f(s): return s.astype(float)

    return {
        "<regime_key>":  <regime_series>,
        "<setup_key>":   <setup_level>,
        "<trigger_key>": <trigger_series>,
        "<stop_key>":    <stop_series>,
        "regime_filter": _f(regime_filter),
        "setup_signal":  _f(setup_signal),
        "trigger_signal":_f(trigger_signal),
        "is_ready":      _f(is_ready),
    }
```

### ⚠️ Warmup gate anti-pattern

```python
# ❌ WRONG — uses a signal boolean as a warmup proxy.
#    is_ready will be False whenever the signal is False, not just during warmup.
is_ready = some_indicator.notna() & setup_signal

# ✅ CORRECT — use the underlying rolling series' notna() check.
_width = donchian_upper - donchian_lower
squeeze_ready = _width.rolling(params.squeeze_history).quantile(0.25).notna()
is_ready = some_indicator.notna() & squeeze_ready
```

---

## Step 7 — Write `backtest/backtesting_py/strategy.py` and `runner.py`

The single-run backtesting.py engine lives in `backtest/backtesting_py/`:

```
backtest/backtesting_py/
├── __init__.py
├── strategy.py     ← Strategy class (boolean flag class attrs)
├── runner.py       ← load_data() + run_backtest()
└── run.py          ← __main__ entry point
```

`backtest/runner.py` is a backward-compat shim that re-exports everything from
`backtesting_py/` for any code that imports from the old path.

### `strategy.py`

```python
from backtesting import Backtest, Strategy
from <strategy_name>.strategy.parameters import Parameters
from <strategy_name>.strategy.signals import compute_signals
from <strategy_name>.strategy.decision.entry import should_buy
from <strategy_name>.strategy.decision.exit import should_sell
from <strategy_name>.strategy.risk.stops import ratchet_stop
from <strategy_name>.strategy.risk.sizing import compute_position_size

class <StrategyName>Strategy(Strategy):
    # Expose every Parameters boolean flag as a class attribute so
    # backtesting.py can sweep them with Backtest.optimize().
    use_<regime_a>:  bool = True
    use_<regime_b>:  bool = False
    use_<setup_a>:   bool = True
    use_<setup_b>:   bool = False
    use_<trigger_a>: bool = True
    use_<trigger_b>: bool = False
    use_<exit_a>:    bool = True
    use_<exit_b>:    bool = False
    # Numeric params also exposed here:
    <numeric_param>: <type> = <default>

    def init(self) -> None:
        params = Parameters(
            use_<regime_a>=self.use_<regime_a>,
            use_<regime_b>=self.use_<regime_b>,
            # ... all other flags
        )
        signals = compute_signals(self.data.df.copy(), params)

        # Register each series with self.I() using the default-arg lambda pattern.
        # The s=signals[key] default arg captures the current value, avoiding
        # Python closure capture bugs when registering multiple lambdas in a loop.
        def _reg(key):
            return self.I(lambda s=signals[key]: s.values.copy(), name=key)

        self._regime   = _reg("regime_filter")
        self._setup    = _reg("setup_signal")
        self._trigger  = _reg("trigger_signal")
        self._stop_raw = _reg("stop_series")
        self._is_ready = _reg("is_ready")

        self._trail_stop: float | None = None
        # Ratchet only for exits that can loosen (e.g. chandelier ATR).
        # Self-managing exits (psar, bbands) are assigned directly.
        self._ratchet_stop = params.use_<exit_a>

    def next(self) -> None:
        if not self._is_ready[-1]:
            return

        in_position = self.position.size > 0
        close = self.data.Close[-1]
        stop_candidate = float(self._stop_raw[-1])

        # --- Update trailing stop ---
        if in_position:
            if not math.isnan(stop_candidate):
                if self._ratchet_stop:
                    self._trail_stop = ratchet_stop(
                        self._trail_stop, stop_candidate, self.position.size
                    )
                else:
                    self._trail_stop = stop_candidate
            if self._trail_stop is not None:
                for trade in self.trades:
                    trade.sl = self._trail_stop

        # --- Exit check ---
        if should_sell(close, self._trail_stop, in_position):
            self.position.close()
            self._trail_stop = None
            return

        # --- Entry check ---
        if should_buy(
            bool(self._regime[-1]),
            bool(self._setup[-1]),
            bool(self._trigger[-1]),
            in_position,
        ):
            if math.isnan(stop_candidate) or stop_candidate <= 0:
                return
            size = compute_position_size(close, stop_candidate, self.equity, self.risk_pct)
            if size > 0:
                self.buy(size=size, sl=stop_candidate)
                self._trail_stop = stop_candidate
```

### `runner.py` + `run.py`

```python
# runner.py
def load_data(cfg: BacktestConfig) -> pd.DataFrame: ...

def run_backtest(cfg: BacktestConfig | None = None) -> bt.backtesting._Stats:
    cfg = cfg or BacktestConfig()
    df = load_data(cfg)
    bt = Backtest(df, <StrategyName>Strategy, cash=cfg.initial_cash,
                  commission=cfg.commission, exclusive_orders=True)
    stats = bt.run()
    print(stats)
    if cfg.plot:
        bt.plot()
    return stats

# run.py  (__main__)
if __name__ == "__main__":
    run_backtest()
```

Run with:

```bash
python -m <strategy_name>.backtest.backtesting_py.run
```

---

## Step 8 — Write the Tests

Write **one test file per layer**. Each test uses a synthetic OHLCV DataFrame built with `numpy.random.default_rng(seed)` — deterministic, no network calls.

### Minimum test checklist

**`test_indicators.py`**
- [ ] Output length matches input length
- [ ] NaN during warmup period
- [ ] Values within valid mathematical range
- [ ] Boolean outputs contain only `{True, False}`
- [ ] Shifting input changes output (no hardcoded result / no lookahead)

**`test_decision.py`**
- [ ] All filters True + not in position → `should_buy` returns True
- [ ] Any filter False → `should_buy` returns False
- [ ] Already in position → `should_buy` returns False
- [ ] Close below stop + in position → `should_sell` returns True
- [ ] `trail_stop=None` → `should_sell` returns False
- [ ] Not in position → `should_sell` returns False

**`test_signals.py`**
- [ ] All expected keys returned
- [ ] All Series match input DataFrame length
- [ ] `is_ready` is False for first N bars, True later
- [ ] `regime_filter` / `setup_signal` / `trigger_signal` are binary (0.0 / 1.0)
- [ ] Stop series is always below/above the relevant price boundary
- [ ] `ratchet_stop` never loosens
- [ ] `compute_position_size` returns 0 when stop ≥ entry

---

## Step 9 — Behavioural Validation Checklist

Run the backtest and check these **before** looking at profit metrics:

| Check | Pass condition |
|-------|---------------|
| Trades fired | `# Trades > 0` (strategy is entering) |
| No cancelled orders | Zero "insufficient margin" warnings in output |
| Exposure time sensible | Between 5–40% for a selective momentum strategy |
| Trade durations realistic | Not all 1-bar (stop too tight) or all max-duration (stop too loose) |
| Win rate in expected range | 25–45% for trend-following |
| No lookahead artefact | Entry prices fall within bar's OHLC range |
| Stop moves only upward | All `trade.sl` values are non-decreasing per trade |

---

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| `initial_cash` too small for asset price | Use a cheaper asset (e.g. SOL instead of BTC) or scale `initial_cash` up |
| `is_ready` gates on a signal, not on warmup | Use `.notna()` on the underlying rolling series, not the boolean signal |
| Closure bug in `self.I()` loop | Always use `lambda s=series: s.values.copy()` default-arg pattern |
| Stop loosens mid-trade | Always `max(current, candidate)` — never assign candidate directly |
| NaN stop on entry | Guard: `if math.isnan(stop_candidate) or stop_candidate <= 0: return` |
| `compute_position_size` returns fraction > 1 | Clip to `min(fraction, 0.9999)` |
| Missing warmup buffer in `start_time` | Add `squeeze_history` bars before the analysis window (e.g. 10 extra days) |
