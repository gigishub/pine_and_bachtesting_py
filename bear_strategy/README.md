# Bear Strategy — Idea to Live

```
hypothesis_test_v2/  →  backtest/vectorbt/  →  live/
   statistical edge       full simulation      execution
```

The process moves in one direction. Each stage has a pass gate — only promote what clears it.

---

## Stage 1 — Hypothesis Testing

Test whether a condition has a statistical edge before committing to a full backtest.  
Three sequential phases. Each phase asks: *does this filter improve the baseline?*

### Phases

| Phase | Question | Baseline |
|-------|----------|----------|
| Regime | Does this market-state filter select a better population than all candles? | All candles |
| Setup | Does this condition improve the regime? | Promoted regime |
| Trigger | Does this entry signal improve regime + setup? | Promoted regime + setup |

**Pass gate**: the filter produces a meaningful PF lift over its baseline, consistently across symbols.

### How to test an idea

1. Write the indicator — a function that takes a DataFrame and returns a boolean Series.
2. Register it in the phase config with `"decision": "PENDING"`.
3. Run the phase: `python -m bear_strategy.hypothesis_test_v2.<phase>.run`
4. Read the results markdown in `<phase>/results/`.
5. Promote (set `"decision": "PROMOTED"`) or discard.

**Multi-timeframe**: any condition can be computed on a higher timeframe. The framework handles alignment without lookahead — set `context_tf` in the idea config.

### Sanity check

Run before trusting any results:
```bash
python -m bear_strategy.hypothesis_test_v2.sanity_check
```
Verifies: shuffled-future data has no edge, shifted entries perform worse than real, cache matches recompute.

---

## Stage 2 — Backtest

Translate the promoted hypothesis into a full simulation with realistic fills, position sizing, stops, and exits. Sweep parameter ranges to find robust settings.

### Running a backtest
```bash
# Single named config
python -m bear_strategy.backtest.vectorbt.run_grid --config <name>

# Sweep a parameter range
python -m bear_strategy.backtest.vectorbt.run_grid --config <name> 

```

Named configs live in `backtest/vectorbt/configs/`. Copy an existing one and edit the parameter ranges.

### Evaluating results

Pass gates (all must be met): SQN, PF, minimum trade count, win rate.  
Composite score: SQN 30% · PF 25% · Expectancy 25% · Sharpe 10% · Max DD 10%.

```bash
python -m bear_strategy.backtest.strategy_evaluation.scoring
python -m bear_strategy.backtest.strategy_evaluation.grid_dashboard
```

A config that passes gates in-sample should be validated out-of-sample on a held-out date range before going live.

---

## Stage 3 — Live Trading

The live runner reads its config entirely from environment variables. Each "profile" is a `.env` file that defines the symbol, timeframe, and strategy parameters.

### Create a profile
```bash
cd bear_strategy/live/control
./runctl.sh profile-save SYMBOL_tf --symbol SYMBOLUSDT --timeframe 1h --category linear --dry-run yes
```
This creates `profiles/SYMBOL_tf.env`. Edit it to add the strategy parameters determined in the backtest.  
**Always test dry-run first** — confirm signals and orders look correct before setting `DRY_RUN=false`.

### Process management
```bash
./runctl.sh start-all        # start every profile
./runctl.sh stop-all         # stop all and remove from reboot list
./runctl.sh status           # show running state + reboot list
./runctl.sh stop <name>      # stop one run
./runctl.sh restart <name>   # stop + restart one run
./runctl.sh resurrect        # restart anything in reboot list that is not running
```

Supervisors restart crashed children automatically. On Ubuntu, `install-systemd` wires `resurrect` to run at boot.

Logs: `registry/active/<name>/<run_id>/run.log`  
Finished runs move to: `registry/inactive/<name>/`

---

## Decision flow

```
Write indicator
      ↓
Regime test — does it select a better population?
      ↓  (pass)
Setup test  — does it improve the regime?
      ↓  (pass)
Trigger test — does it add lift to regime + setup?
      ↓  (pass)
Backtest — does it hold up with real fills, stops, and position sizing?
      ↓  (pass, OOS validated)
Live — dry-run → inspect → go live
```

Discard at any stage. A hypothesis that fails early saves the cost of a full backtest.
