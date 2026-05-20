# How to Add a New Exit to the Bear Strategy

Five files, five steps. Each step is independent of the others — do them in order.

---

## Steps

### 1. `bear_strategy/strategy/parameters.py`
Add the flag and any numeric params:
```python
use_myexit_exit: bool  = False
my_param:        float = 1.0
```

### 2. `bear_strategy/backtest/vectorbt/exits/<name>_exit.py`
Create the module. Must expose `FLAG` and `compute()`:
```python
FLAG = "use_myexit_exit"

def compute(df_1h, df_1d, funding_df, params) -> pd.Series:
    # Return bool Series on df_1h.index — True where exit fires
    ...
```

### 3. `bear_strategy/backtest/vectorbt/exits/__init__.py`
Import the module and add to `EXIT_REGISTRY`:
```python
from . import myexit_exit
EXIT_REGISTRY = {
    ...
    myexit_exit.FLAG: myexit_exit.compute,
}
```

### 4. `bear_strategy/backtest/vectorbt/bear_grid_config.py`
Four places:
- `_AUDITABLE_BEAR_FLAGS` — add `"use_myexit_exit"`
- Default `boolean_filter_ranges` — add `"use_myexit_exit": (False,)`
- `_NUMERIC_MAP` — add `("my_param_range", "my_param")`
- `feature_dependencies` — add `"my_param": ("use_myexit_exit",)`
- New dataclass field: `my_param_range: tuple[float,...] = (1.0,)`

### 5. `bear_strategy/backtest/vectorbt/pipeline.py`
Add flag to `_EXIT_FLAGS` so the validity check counts it as a real exit:
```python
_EXIT_FLAGS = (..., "use_myexit_exit")
```

**Then patch every named config** in `configs/` to declare the new flag (pinned `(False,)` unless the config specifically tests it).

---

## Example — `use_rsi_oversold_exit`

| File | Change |
|------|--------|
| `parameters.py` | `use_rsi_oversold_exit: bool = False`, `rsi_oversold_level: float = 30.0` |
| `exits/rsi_oversold_exit.py` | `FLAG = "use_rsi_oversold_exit"` + `compute()` returning `close < oversold_level` |
| `exits/__init__.py` | `rsi_oversold_exit.FLAG: rsi_oversold_exit.compute` in registry |
| `bear_grid_config.py` | Flag in `_AUDITABLE_BEAR_FLAGS`, default OFF, `rsi_oversold_level_range` field + `_NUMERIC_MAP` entry |
| `pipeline.py` | `"use_rsi_oversold_exit"` in `_EXIT_FLAGS` |
