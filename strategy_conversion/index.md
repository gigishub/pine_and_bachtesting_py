# Strategy Conversion — Phase Index

Step-by-step guides for turning a written strategy idea into tested, backtestable Python code.
Each phase builds on the previous. Complete them in order for a new strategy.

---

| # | File | Phase | Goal |
|---|------|-------|------|
| 1 | [01_translation_guide.md](01_translation_guide.md) | **Build** | Parse the strategy spec → directory layout → indicators → signals → runner → tests → behavioural validation |
| 2 | [02_adding_alternative_filters.md](02_adding_alternative_filters.md) | **Extend** | Add all alternative Regime / Setup / Trigger / Exit options as mode selectors; verify each option works in isolation |
| 3 | [03_vectorbt_grid_search.md](03_vectorbt_grid_search.md) | **Grid Search** | Add a vectorbt engine that grid-searches all mode combinations; ranks results by Expectancy |


---

## How to add a new phase

1. Create `0N_<short_description>.md` in this folder.
2. Add a row to the table above.
3. Start the file with a one-paragraph summary of the phase goal and a checklist at the end.
