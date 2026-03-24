## 🔥 Short execution prompt (one-liner style)

Keep `build_series.py` as single strategy core.
In `ups_backtest.py` and `ups_runner/runner.py`:
- call `build_strategy_series(...)`
- apply same entry/exit guards (`should_open_*`, `should_close_*`)
- compute stops/targets (`compute_*_stop`, `compute_*_target`, trail state)
- use engine-specific execution:
  - backtest: `self.buy/self.sell` + `self.position.close()`
  - live: `BybitV5Client.create_order()` + `set_trading_stop()`
- Move order side effects into `bybit_trading_functions.py` to keep runner "thin".

---

## 📐 Full refactor plan — Unified strategy with clean separation

### Target structure

```
UPS_py/
  # Pure strategy (no I/O, no execution)
  strategy/
    __init__.py
    types.py               # StrategySettings dataclass
    signals.py             # build_strategy_series (orchestrator)
    
    decision/
      __init__.py
      entry.py             # should_open_long, should_open_short
      exit.py              # should_close_long, should_close_short
    
    indicators/
      __init__.py
      ma.py                # (from base.py)
      atr.py               # (from base.py)
      iq.py
      candlestick_patterns.py  # (from patterns.py, hammers/engulfings)
      pullback.py
    
    risk/
      __init__.py
      sizing.py            # position_sizing.py → here
      sl_tp.py             # sl.py + tp.py combined
      trailing.py          # trail_rules.py
  
  # Data sources (exchange-agnostic)
  data/
    __init__.py
    types.py
    fetch.py               # KuCoin + Bybit → unified interface
  
  # Live execution
  live/
    __init__.py
    config.py
    market_data.py
    trade_state.py
    ups_live_runner.py              # UPSLiveRunner
    bybit_client/
      __init__.py
      types.py
      rest.py
      ws.py
  
  # Backtesting
  backtest/
    __init__.py
    strategy.py            # UPSStrategy class isolated
    backtest_runner.py              # run() function + CLI entry point
  
  __init__.py

# Remove (consolidate into structure above)
- entry_exit/
- SL_TP/
- position_sizing.py
- indicators.py
- strategy_logic/ (keep logic, reorganize files)
- fetch_data/ → data/
```

### `strategy/types.py` content

```python
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class StrategySettings:
    """All strategy parameters (indicators + decision rules + risk).
    
    Used by both backtest and live runner.
    Engine-agnostic configuration.
    """
    # MA
    ma_length: int = 50
    max_candles_beyond_ma: int = 1
    ma_consolidation_lookback: int = 10
    ma_consolidation_count: int = 4
    ma_breach_lookback: int = 5
    
    # IQ filter
    use_iq_filter: bool = True
    iq_lookback: int = 20
    iq_min_score: float = 0.55
    iq_slope_atr_scale: float = 1.5
    iq_er_weight: float = 0.5
    iq_slope_weight: float = 0.3
    iq_bias_weight: float = 0.2
    
    use_sq_boost: bool = True
    sq_boost_weight: float = 0.3
    sq_vol_lookback: int = 20
    
    # Trade direction
    long_trades: bool = True
    short_trades: bool = True
    
    # Candlestick patterns (entry patterns)
    enable_ec: bool = True
    enable_bullish_engulfing: bool = True
    enable_shooting_star: bool = True
    ec_wick: bool = False
    enable_hammer: bool = True
    atr_max_size: float = 2.5
    rejection_wick_max_size: float = 0.0
    hammer_fib: float = 0.3
    hammer_size: float = 0.1
    
    # Stops & targets
    stop_multiplier: float = 1.0
    risk_reward_multiplier: float = 1.0
    minimum_rr: float = 0.0
    pb_reference: str = "Close"
    sl_reference: str = "High/Low"
    
    # Trailing
    trail_stop: bool = True
    trail_stop_size: float = 1.0
    trail_source: str = "High/Low"
    
    # Lookback / misc
    lookback: int = 5
    atr_length: int = 14
    point_allowance: int = 0
    
    # Backtester sizing (backtest-specific but belongs here for reuse)
    risk_per_trade: float = 1.0
```

---

## 🛠️ Step-by-step execution plan with verification

### Phase 1: Create new directory structure (non-breaking)

**Step 1.1: Create `strategy/` folder and `types.py`**
- [ ] Create `/UPS_py/strategy/` directory
- [ ] Create `/UPS_py/strategy/__init__.py`
- [ ] Move `Settings` dataclass from `ups_backtest.py` → `/UPS_py/strategy/types.py` as `StrategySettings`
- **Verify:** `python -c "from UPS_py.strategy.types import StrategySettings; print('OK')"`

**Step 1.2: Create `decision/` folder and split entry/exit**
- [ ] Create `/UPS_py/strategy/decision/` directory
- [ ] Create `/UPS_py/strategy/decision/__init__.py`
- [ ] Move `entry_exit/entry_rules.py` → `/UPS_py/strategy/decision/entry.py`
- [ ] Move `entry_exit/exit_rules.py` → `/UPS_py/strategy/decision/exit.py`
- [ ] Update imports in both files (if any cross-imports)
- **Verify:** 
  ```bash
  python -c "from UPS_py.strategy.decision.entry import should_open_long; print('OK')"
  python -c "from UPS_py.strategy.decision.exit import should_close_long; print('OK')"
  ```

**Step 1.3: Create `risk/` folder and consolidate risk modules**
- [ ] Create `/UPS_py/strategy/risk/` directory
- [ ] Create `/UPS_py/strategy/risk/__init__.py`
- [ ] Move `position_sizing.py` → `/UPS_py/strategy/risk/sizing.py`
- [ ] Combine `SL_TP/sl.py` + `SL_TP/tp.py` → `/UPS_py/strategy/risk/sl_tp.py`
- [ ] Move `SL_TP/trail_rules.py` → `/UPS_py/strategy/risk/trailing.py`
- [ ] Update all imports in combined files
- **Verify:**
  ```bash
  python -c "from UPS_py.strategy.risk.sizing import compute_long_size_fraction; print('OK')"
  python -c "from UPS_py.strategy.risk.sl_tp import compute_long_stop, compute_long_target; print('OK')"
  python -c "from UPS_py.strategy.risk.trailing import compute_long_trail_candidate; print('OK')"
  ```

**Step 1.4: Reorganize `indicators/` folder**
- [ ] Move `strategy_logic/base.py` → `/UPS_py/strategy/indicators/ma.py` (MA logic)
- [ ] Move `strategy_logic/base.py` → `/UPS_py/strategy/indicators/atr.py` (ATR logic, split if mixed)
- [ ] Move `strategy_logic/iq.py` → `/UPS_py/strategy/indicators/iq.py`
- [ ] Move `strategy_logic/patterns.py` → `/UPS_py/strategy/indicators/candlestick_patterns.py`
- [ ] Move `strategy_logic/pullback.py` → `/UPS_py/strategy/indicators/pullback.py`
- [ ] Update internal imports in each file
- **Verify:**
  ```bash
  python -m py_compile UPS_py/strategy/indicators/*.py
  ```

**Step 1.5: Move strategy signal orchestrator**
- [ ] Move `strategy_logic/build_series.py` → `/UPS_py/strategy/signals.py`
- [ ] Update imports (now references `strategy.indicators.*`, `strategy.risk.*`)
- **Verify:**
  ```bash
  python -c "from UPS_py.strategy.signals import build_strategy_series; print('OK')"
  ```

---

### Phase 2: Create backtest split (no impact on runtime yet)

**Step 2.1: Create `backtest/` folder and move strategy class**
- [ ] Create `/UPS_py/backtest/` directory
- [ ] Create `/UPS_py/backtest/__init__.py`
- [ ] Extract `UPSStrategy` class from `ups_backtest.py`
- [ ] Save as `/UPS_py/backtest/strategy.py`
- [ ] Update imports to use new `strategy/` locations
- [ ] Update imports to use `StrategySettings` from `strategy.types`
- **Verify:**
  ```bash
  python -c "from UPS_py.backtest.strategy import UPSStrategy; print('OK')"
  ```

**Step 2.2: Create backtest runner**
- [ ] Extract `run()` function + `Settings` → `/UPS_py/backtest/runner.py`
- [ ] Extract CLI `if __name__ == "__main__"` block → `/UPS_py/backtest/runner.py`
- [ ] Extract `_load_csv()` helper to `data/fetch.py` or keep local
- [ ] Import `StrategySettings` from `strategy.types`
- [ ] Import `UPSStrategy` from `.strategy`
- **Verify:**
  ```bash
  python -c "from UPS_py.backtest.runner import run; print('OK')"
  ```

**Step 2.3: Test backtest still works (full runtime test)**
- [ ] Run backtest with CSV: 
  ```bash
  source .venv/bin/activate && python -m UPS_py.backtest.runner --csv <test_csv> --no-plot
  ```
  OR if keeping as top-level:
  ```bash
  source .venv/bin/activate && python UPS_py/backtest/runner.py --csv <test_csv> --no-plot
  ```
- **Verify:** backtest produces same results as before (compare output stats)
- [ ] Spot-check: trade count, equity curve shape, Sharpe ratio should be identical

---

### Phase 3: Update live runner to use unified strategy (reuse verification)

**Step 3.1: Update live runner imports**
- [ ] In `/UPS_py/live/ups_runner/runner.py`:
  - Change `from strategy_logic import build_strategy_series` 
  - To `from UPS_py.strategy.signals import build_strategy_series`
  - Update all `SL_TP/`, `entry_exit/`, `position_sizing/` imports to use new paths
- **Verify:**
  ```bash
  python -m py_compile UPS_py/live/ups_runner/runner.py
  ```

**Step 3.2: Verify live runner still compiles**
- [ ] Run compilation test on all live modules:
  ```bash
  python -m py_compile UPS_py/live/ups_runner/*.py UPS_py/live/bybit_client/*.py
  ```
- [ ] Dry-run test (if test key available):
  ```bash
  DRY_RUN=1 python -m UPS_py.live.ups_runner.runner
  ```

---

### Phase 4: Consolidate top-level (optional cleanup)

**Step 4.1: Archive old structure**
- [ ] Move old folders to `_archive/` or delete if confident:
  - `/UPS_py/entry_exit/` → `/UPS_py/_archive/entry_exit/`
  - `/UPS_py/SL_TP/` → `/UPS_py/_archive/SL_TP/`
  - `/UPS_py/strategy_logic/` → `/UPS_py/_archive/strategy_logic/`
  - `/UPS_py/fetch_data/` → Move logic to `/UPS_py/data/fetch.py`
  - `/UPS_py/position_sizing.py` → now in `strategy/risk/sizing.py`
  - `/UPS_py/indicators.py` → now in `strategy/indicators/`

**Step 4.2: Create top-level convenience exports** (optional)
- [ ] In `/UPS_py/strategy/__init__.py`:
  ```python
  from .signals import build_strategy_series
  from .types import StrategySettings
  ```
- [ ] In `/UPS_py/backtest/__init__.py`:
  ```python
  from .runner import run
  from .strategy import UPSStrategy
  ```

---

### Phase 5: Full integration test

**Step 5.1: Run both engines side-by-side**
- [ ] Test backtest:
  ```bash
  source .venv/bin/activate && python UPS_py/backtest/runner.py --csv <test_csv> --no-plot
  ```
  Compare results with previous run (should be identical)

- [ ] Test live (dry-run):
  ```bash
  DRY_RUN=1 python -m UPS_py.live.ups_runner.runner
  ```
  Should startup without import errors, detect same signals

**Step 5.2: Verify strategy reuse**
- [ ] Check that both import `build_strategy_series` from same location:
  ```bash
  grep -r "from.*signals import" UPS_py/backtest/ UPS_py/live/
  ```
  Should show same import path for both

**Step 5.3: Git commit milestones**
- [ ] After each phase, commit with clear message:
  - `git add -A && git commit -m "refactor: create strategy/ folder with types, indicators, risk"`
  - `git commit -m "refactor: split backtest into strategy.py and runner.py"`
  - `git commit -m "refactor: update live runner imports to use unified strategy"`
  - etc.

---

### Rollback plan (if needed)

If any step breaks existing logic:
1. Check git log for last working commit
2. Review import paths in error message
3. Verify file was actually moved (not just renamed in editor)
4. Re-run compilation test after each file move

---

## Benefits summary

✅ **Single strategy logic** — one `build_strategy_series()`, used by backtest + live  
✅ **Clear folder hierarchy** — `strategy/`, `data/`, `backtest/`, `live/`  
✅ **Type-safe config** — `StrategySettings` reused, no duplication  
✅ **Easy testing** — can unit test decision functions, risk math in isolation  
✅ **Low risk** — verification at each step ensures no silent breaks  
✅ **Scalable** — easy to add new strategies, new exchanges, new patterns later