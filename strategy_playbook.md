# Strategy Development Playbook

A plain-language guide for taking a strategy idea from first concept through to a tested, evaluated implementation. Follow the phases in order. Each phase has a clear goal and a short checklist — the detailed how-to lives in the linked guides.

---

## Phase 0 — Idea & Concept

**Goal:** Define what the strategy is actually trying to do before a single line of code is written.

Write the idea out in plain language first. Then map it onto the 4-layer filter stack. If you cannot fill in all four layers, the idea is not ready yet.

| Layer | Question to answer | Example |
|-------|--------------------|---------|
| **Regime** | When is this market even tradeable? | ADX > 25 signals a trending market |
| **Setup** | Where is the entry zone? | Price breaks out of a compressed Donchian channel |
| **Trigger** | What confirms the move is real? | CMF crosses above 0.05 (buyers are committing) |
| **Exit** | How does the trade end? | Chandelier trailing stop ratchets upward |

Also decide:
- Long-only or long/short?
- Which market and timeframe(s) to start with?
- Can all conditions be computed from OHLCV data alone? (If not, flag what extra data is needed and whether it is available.)

**Checklist**
- [ ] Strategy idea written in plain language
- [ ] All 4 layers filled in
- [ ] Direction (long-only / both sides) decided
- [ ] Starting symbol and timeframe chosen
- [ ] Any non-OHLCV requirements documented

---

## Phase 1 — Build the Golden Path

**Goal:** Get one single working combination coded, tested, and validated. No alternatives yet — just the simplest version that proves the logic works.

This phase produces a Python module with the same structure as `adaptive_momentum_strategy/`. The strategy logic lives in `strategy/`, the backtest runner in `backtest/`, and tests in `tests/`.

Steps at a glance:
1. Set up the directory structure
2. Write `parameters.py` — one dataclass with all tunable defaults
3. Write one indicator file per layer
4. Write `risk/stops.py` and `risk/sizing.py`
5. Write `decision/entry.py` and `decision/exit.py`
6. Write `signals.py` — the single orchestrator that calls all indicators
7. Write `backtest/backtesting_py/strategy.py` and `runner.py`
8. Write tests for each layer
9. Run the backtest and check behavioural validation

→ *Detailed step-by-step: `strategy_conversion/01_translation_guide.md`*

**Behavioural validation targets (check before looking at profit)**

| Check | Target |
|-------|--------|
| Trades fired | > 0 |
| Exposure time | exists |
| Entry prices | Within bar OHLC range (no lookahead) |
| Stop movement | Only moves in the favourable direction, never loosens |

**Checklist**
- [ ] Directory structure matches the module template
- [ ] All indicator files written and tested
- [ ] Tests pass (indicators, decision, signals)
- [ ] Backtest fires trades and passes behavioural validation

---

## Phase 2 — Add Alternatives

**Goal:** Add multiple options for each layer so the grid search in Phase 3 has something to sweep.

For each layer, list every alternative from the strategy description and decide which ones are OHLCV-feasible. Add a boolean flag per option to `Parameters`. Write one new indicator file per option. Then update `signals.py` to compute all options and combine them with AND-logic (entry layers) and OR-logic (exit).

Validate that each individual flag combination fires trades and behaves sensibly before moving on.

→ *Detailed step-by-step: `strategy_conversion/02_adding_alternative_filters.md`*

**Logic rules**
- Entry layers (Regime, Setup, Trigger): AND — all active flags must pass before entry
- Exit layer: OR — whichever active stop is highest fires first

**Checklist**
- [ ] Alternative indicator feasibility table filled in
- [ ] One boolean flag per available option in `Parameters`
- [ ] One file per new indicator in `strategy/indicators/` or `strategy/risk/`
- [ ] `signals.py` computes all options and combines correctly
- [ ] Each individual flag combination tested and validated
- [ ] All existing tests still pass

---

## Phase 3 — Grid Search

**Goal:** Run the vectorbt engine across all valid flag combinations and get a ranked results table.

The grid searches every combination of boolean flags. Invalid combos (where any layer group is entirely off) are filtered out automatically. Results are saved as a CSV ranked by Expectancy.

Run command:
```bash
source .venv/bin/activate
python -m <strategy_name>.backtest.vectorbt.run
```

Results appear in:
```
<strategy_name>/backtest/results/results_vbt/<timestamp>/
```

→ *Detailed setup: `strategy_conversion/03_vectorbt_grid_search.md`*

**What to look for in the results**
- Combinations with positive Expectancy and > 20 trades
- Consistency across the top-ranked combos (do the same flags appear repeatedly?)
- Any combinations that produce zero trades (usually a warmup or threshold issue)

**Checklist**
- [ ] `simple_config.py` updated with symbols, timeframes, and date range
- [ ] Grid runs to completion without errors
- [ ] Results CSV saved and top combos reviewed
- [ ] Zero-trade combos investigated

---

## Phase 4 — Robustness Evaluation

**Goal:** Verify the strategy holds up across multiple symbols and timeframes, not just the development asset.

Run the `strategy_evaluation` module against two result sets: a short data window and a longer one. This tells you whether the strategy works broadly or was just fitted to one market condition.

Run command:
```bash
# CLI
python -m strategy_evaluation <short_results_dir> <long_results_dir> --label <StrategyName>

# Streamlit dashboard
streamlit run strategy_evaluation/streamlit_app.py
```

→ *How to read every section of the report: `strategy_conversion/04_reading_and_refining_results.md`*

**What the report tells you**

| Metric | What it measures | Target |
|--------|-----------------|--------|
| Symbol pass rate | % of symbols where the top combo is profitable | ≥ 70% |
| Timeframe pass rate | % of timeframes where the top combo passes | ≥ 60% |
| Top toggle frequency | Which flags appear most in top-ranked combos | Guides Phase 5 |

**Verdict interpretation**
- ✅ **Robust** — meets both pass rate targets
- ⚠️ **Marginal** — meets one target; refine before going live
- ❌ **Weak** — fails both targets; revisit Phase 2 alternatives

**Checklist**
- [ ] Grid search results exist for both a short and a long date range
- [ ] `strategy_evaluation` run and report generated
- [ ] Symbol pass rate and timeframe pass rate noted
- [ ] Top toggle frequency table reviewed

---

## Phase 5 — Refine

**Goal:** Use the robustness report to decide what to improve next, then loop back through the relevant earlier phase.

The robustness report contains four analytical lenses (Toggle Frequency, RandomForest importance, SHAP impact, OLS significance). They must be read together — each one alone is misleading. The decision matrix in `strategy_conversion/04_reading_and_refining_results.md` maps every signal pattern to a concrete action.

**Common refinement actions**

| Finding | Action |
|---------|--------|
| Timeframe pass rate low | Try wider indicator periods; test additional timeframes |
| Symbol pass rate low | Check if failures share a characteristic (e.g. low-liquidity assets) |
| One flag dominates top combos | Pin that flag to `True` in `simple_config.py`; remove its alternative |
| No flag pattern visible | The strategy may not have a consistent edge — revisit Phase 0 |

After making changes, re-run Phase 3 (grid search) and Phase 4 (robustness evaluation). Make exactly one change per iteration so you can attribute the effect. Repeat until the verdict is Robust or you decide the strategy needs a different concept.

When toggle decisions are stable, switch from toggle changes to numerical parameter sweep. See Section 5 of `strategy_conversion/04_reading_and_refining_results.md` for the sweep workflow.

**Checklist**
- [ ] Top toggle frequency reviewed
- [ ] Refinement action chosen and applied
- [ ] Grid search re-run after changes
- [ ] Robustness evaluation re-run and compared to previous report

---

## Phase 6 — Live Deployment

**Goal:** Wire the best-performing, robustly-validated combo into the live runner.

This phase uses the live infrastructure in `UPS_py_v2/live/`. The strategy parameters from the best grid-search combo are translated into the live runner's config.

> **Only start this phase once the robustness evaluation verdict is ✅ Robust.**

Steps at a glance:
1. Identify the best combo from the robustness-validated results
2. Set the corresponding flags in the live runner config
3. Run in dry-run mode first and verify signals match backtest expectations
4. Monitor the first live trades carefully — compare entry/exit prices to backtest fills

**Checklist**
- [ ] Robustness verdict is ✅ Robust
- [ ] Best combo flags identified and configured
- [ ] Dry-run verified (signals fire, no errors)
- [ ] Live trading started and first few trades reviewed

---

## Quick Reference

| Phase | Output | Done when... |
|-------|--------|--------------|
| 0 — Idea | 4-layer filter table | All layers filled in, OHLCV-feasibility checked |
| 1 — Build | Working backtest module | Tests pass, behavioural validation passes |
| 2 — Alternatives | Extended Parameters + signals | All flag combos fire trades in isolation |
| 3 — Grid Search | Ranked results CSV | Grid runs clean, top combos identified |
| 4 — Robustness | Robustness report | Pass rates measured, toggle frequency reviewed |
| 5 — Refine | Updated strategy | Verdict improves toward ✅ Robust |
| 6 — Live | Running live strategy | Dry-run validated, first live trades reviewed |
