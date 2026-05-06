# hypothesis_test_v2 — Bear Strategy Hypothesis Testing Framework

## What this is

A structured, three-phase framework for testing whether a **short-entry filter** (regime gate, setup condition, or entry trigger) adds measurable edge over random entries. The goal is not to curve-fit — it is to **falsify** each hypothesis and only promote what survives.

---

## Workflow at a glance

```
Phase 1 — REGIME
  Baseline: all candles (random entry on every bar)
  Question: does this market-state filter capture a better population?
  Pass: PF lift ≥ 0.05 on most pairs
  Output: regime/results/phase_regime_entry{tf}_active.md

        ↓  promote winner → set as BASELINE in setup/config.py

Phase 2 — SETUP
  Baseline: bars where the regime filter fires (promoted from Phase 1)
  Question: does this setup condition sub-select an even better population?
  Pass: additional PF lift ≥ 0.05 above the new (regime) baseline
  Output: setup/results/phase_setup_entry{tf}_active.md

        ↓  promote winner → set as BASELINE in trigger/config.py

Phase 3 — TRIGGER
  Baseline: regime AND setup bars
  Question: does this specific entry trigger add lift above the combined filter?
  Output: trigger/results/phase_trigger_entry{tf}_active.md
```

Each phase is **self-contained**: its own `config.py`, `run.py`, `indicators/`, and `results/`.

---

## Directory structure

```
hypothesis_test_v2/
├── config.py                   # shared: pairs, dates, ATR exit params
├── batch_runner.py             # core engine — do not edit unless changing logic
│
├── engine/
│   ├── data_loader.py          # parquet → DataFrame, lowercases columns, date slice
│   ├── outcome_engine.py       # ATR stop/target forward-scan simulator
│   ├── alignment.py            # HTF→LTF alignment (shift+merge_asof, no lookahead)
│   └── baseline_cache.py       # CSV cache of baseline PF/WR per symbol/TF/window
│
├── reports/
│   ├── active_board.py         # writes phase_{phase}_entry{tf}_active.md
│   ├── phase_csv.py            # appends rows to phase_comparison.csv
│   └── rejected_archive.py     # rejected ideas go here, not deleted
│
├── regime/
│   ├── config.py               # baseline=all_candles, ideas list
│   ├── run.py                  # entry point: python -m bear_strategy.hypothesis_test_v2.regime.run
│   ├── indicators/             # one .py per signal
│   └── results/                # active board MDs, CSVs, baseline cache
│
├── setup/                      # same structure as regime/
├── trigger/                    # same structure as regime/
│
└── tests/
    ├── test_outcome_engine.py  # ATR, simulator, compute_outcomes
    └── test_alignment.py       # HTF alignment, no-lookahead validation
```

---

## Running the phases

```bash
source .venv/bin/activate

# Phase 1
python -m bear_strategy.hypothesis_test_v2.regime.run

# Phase 2 (after editing setup/config.py to set BASELINE to the promoted regime)
python -m bear_strategy.hypothesis_test_v2.setup.run

# Phase 3 (after editing trigger/config.py to set BASELINE to regime + setup)
python -m bear_strategy.hypothesis_test_v2.trigger.run
```

Each run **deletes previous results** for that phase before re-running (idempotent). Baseline cache files are reused across runs for speed.

---

## Reading the results

Open `{phase}/results/phase_{phase}_entry{tf}_active.md`. There are three sections:

### 1. Batch Summary
Quick overview — is the idea lifting PF across most pairs?

| idea | avg PF | avg PF lift | pairs OK | decision |
|------|--------|-------------|----------|----------|
| close_below_ema_200 | 1.078 | +0.043 | 3/5 | PENDING |

### 2. Per-Idea Detail
Per-pair breakdown. `[OK]` = lift ≥ 0.05 AND coverage ≥ 10%. `[--]` = fails either.

```
**close_below_ema_200**  avg PF 1.078  avg lift +0.043  3/5 pairs  PENDING
  BTCUSDT     WR 41.1%  PF 1.049  lift +0.066 / req 0.05  n=81,153  cov 47.9%  [OK]
  ETHUSDT     WR 41.6%  PF 1.068  lift +0.053 / req 0.05  n=78,267  cov 48.2%  [OK]
```

### 3. Population Comparison (per pair)
Baseline row first, then each idea sorted by PF lift. Mirrors the v2 methodology spec.

| population | wr_% | pf | dur | n_trades |
|------------|-----:|---:|----:|---------:|
| all_candles | 39.60 | 0.983 | 20.2 | 169,488 |
| close_below_ema_200 | 41.15 | 1.049 | 20.8 | 81,153 |

`dur` = average bars held per resolved trade (short trade found stop or target).

---

## Global settings (`config.py`)

```python
SHARED = {
    "pairs":           ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT"],
    "start":           "2021-01-01",
    "end":             "2025-11-01",
    "stop_atr_mult":   2.0,
    "target_atr_mult": 3.0,
    "atr_period":      7,
    "data_dir":        "crypto_data/data",
}
```

Change `start`/`end` here — it applies to **all phases**.

---

## Adding a new indicator

1. Create `{phase}/indicators/my_indicator.py`. Copy the template from `close_below_ema.py`.
2. Required contract:

```python
def signal(df: pd.DataFrame, params: dict) -> pd.Series:
    """Returns a boolean Series on df.index.  True = condition active."""
    ...
```

3. Add an entry to `{phase}/config.py → IDEAS`:

```python
{
    "name":             "my_indicator_name",
    "enabled":          True,
    "decision":         "PENDING",
    "indicator_module": "bear_strategy.hypothesis_test_v2.{phase}.indicators.my_indicator",
    "params":           {"param_a": 14},
    # Optional: compute signal on a different TF (e.g. "1d", "4h"):
    # "context_tf":     "1d",
}
```

4. Re-run the phase. The old CSV and active boards are wiped automatically.

---

## Multi-timeframe (context_tf)

Any idea can compute its signal on a **higher timeframe** and have it aligned to the entry bars without lookahead:

```python
{
    "name":             "close_below_ema_50_1d",
    "indicator_module": "...close_below_ema",
    "params":           {"period": 50},
    "context_tf":       "1d",   # signal on daily, entries on 15m/1h
}
```

Alignment is: `HTF_signal.shift(1)` → `merge_asof(direction="backward")` onto entry bars.  
This means each entry bar only sees **closed** HTF bars. The currently-forming HTF bar is never visible.

The same `context_tf` key works in the `BASELINE` dict when promoting a regime.

---

## Promoting a winner to the next phase

### Regime → Setup

1. In `regime/config.py`, change the winning idea's `"decision"` to `"PROMOTED"`.
2. In `setup/config.py`, set:

```python
BASELINE = {
    "type":   "indicator",
    "label":  "close_below_ema_200",   # name shown in results
    "module": "bear_strategy.hypothesis_test_v2.regime.indicators.close_below_ema",
    "params": {"period": 200},
    # "context_tf": "1d",   # include if the regime used it
}
```

The setup phase will now compare its ideas against the **regime-filtered** population.

### Setup → Trigger

Same pattern. In `trigger/config.py`:

```python
BASELINE = {
    "type": "indicators",
    "label": "regime_ema200__setup_rsi_range",
    "list": [
        {"module": "...regime.indicators.close_below_ema", "params": {"period": 200}},
        {"module": "...setup.indicators.rsi_range",        "params": {"period": 14, "low": 30, "high": 60}},
    ],
}
```

---

## Lookahead sanity check

Before trusting any results, run the built-in sanity check to confirm the baseline is not inflated by lookahead:

```bash
python -m bear_strategy.hypothesis_test_v2.sanity_check
```

This runs three comparisons:

| Test | What it does | Expected |
|------|-------------|----------|
| **Future shuffle** | Shuffles the price series randomly, re-runs baseline | PF ≈ 1.0 (no edge from structure) |
| **Shifted entry** | Enters 100 bars *before* the signal fires (pure future data) | PF should drop vs real signal |
| **Reported vs recomputed** | Re-reads the cached baseline and recomputes it from scratch | Values must match within 0.001 |

If future-shuffled prices give a high PF, the outcome engine has a lookahead bug.  
If shifted entries give *better* results than real entries, there is a data-alignment bug.

**Typical healthy output:**
```
[PASS] Future shuffle baseline PF: 0.981 (expected ~1.0)
[PASS] Shifted-entry PF 0.962 < real-entry PF 1.049 — no lookahead from future data
[PASS] Cached baseline 0.983 matches recomputed 0.983
```

---

## Known design decisions

| Decision | Reason |
|----------|--------|
| No `max_bars` trade timeout | Both sides compared fairly; trades run until stop or target. Open trades at data-end are excluded from both sides. |
| Baseline uses `all_candles` in regime phase | Fixes the v1 bug where regime was compared against itself (inflated results). |
| `shift(1)` on HTF before alignment | The currently-forming HTF bar is never visible at entry time. |
| CSV deleted on each run | Prevents duplicate rows from re-runs accumulating. |
| Baseline is cached to CSV | Avoids recomputing the large random-entry baseline on every run. Cache is keyed by symbol + TF + date window + label. |
