Building to Test a Hypothesis

## Purpose

A hypothesis has been written. The goal now is to attack it and try to prove it wrong. Testing happens layer by layer, starting from the most foundational assumption.

Every piece of code built during this process has one of two destinies: it either becomes part of the permanent strategy, or it gets deleted once it has served its testing purpose. The structure below keeps those two things from mixing.

---

## Strategy structure overview

The strategy is organized so permanent strategy code and hypothesis test modules both have a stable home. Individual test folders can still be deleted any time after a verdict.

### Permanent code side

Everything that may survive and become part of the final strategy goes into its permanent location immediately. Name directories and files after what they do, not after the test they are currently supporting.

```text
<strategy_name>/
├── __init__.py
├── README.md
├── strategy/                        # Pure logic — zero I/O, zero backtest imports
│   ├── __init__.py
│   ├── parameters.py                # @dataclass — all tunable values, no logic
│   ├── signals.py                   # compute_signals(df, params) -> dict[str, Series]
│   ├── indicators/
│   │   ├── __init__.py
│   │   ├── regime/                  # One file per indicator
│   │   ├── setup/
│   │   └── trigger/
│   ├── decision/
│   │   ├── __init__.py
│   │   ├── entry.py                 # Entry gate: regime + setup + trigger -> bool
│   │   └── exit.py                  # Exit gate: stop / target / trailing -> bool
│   └── risk/
│       ├── __init__.py
│       ├── stops.py                 # Stop level series + ratchet helper
│       └── sizing.py                # Position size from entry, stop, equity, risk %
├── backtest/
│   ├── __init__.py
│   ├── config.py                    # Shared base dataclasses (dataset, costs, date range)
│   ├── backtesting_py/
│   │   ├── __init__.py
│   │   ├── strategy.py              # backtesting.py Strategy wrapper
│   │   ├── runner.py                # Single-run execution
│   │   ├── run.py                   # CLI entry for backtesting.py
│   │   ├── results/
│   │   │   └──                      # backtesting.py outputs only
│   │   └── configs/                 # Engine-specific configs only
│   │       ├── __init__.py
│   │       └── default.py
│   ├── vectorbt/
│   │   ├── __init__.py
│   │   ├── signals.py               # Build vectorized entries/exits/size arrays
│   │   ├── runner.py                # Portfolio execution
│   │   ├── pipeline.py              # Grid/sequence logic
│   │   ├── metrics.py
│   │   ├── run.py                   # CLI entry for vectorbt
│   │   ├── results/
│   │   │   └──                      # vectorbt outputs only
│   │   └── configs/                 # Engine-specific configs only
│   │       ├── __init__.py
│   │       └── default.py
│   ├── hypothesis_test/
│   │   ├── __init__.py
│   │   ├── <test_name>/             # Generic hypothesis test module (descriptive name)
│   │   │   ├── __init__.py
│   │   │   ├── config.py            # Test-specific settings
│   │   │   ├── entries.py           # Population / entry logic for this test
│   │   │   ├── runner.py            # Test harness
│   │   │   └── run.py               # CLI entry for this test
│   │   └── hypothesis_test_output/
│   │       ├── __init__.py
│   │       ├── runner.py            # Shared raw outcome-engine helpers
│   │       ├── run.py               # CLI entry for raw runners
│   │       ├── results/
│   │       │   └──                  # raw outcome-engine outputs only
│   │       └── configs/
│   │           ├── __init__.py
│   │           └── default.py
│   ├── reporting/
│   │   ├── __init__.py
│   │   └── output.py                # Shared report formatting/export helpers
└── tests/
    ├── __init__.py
    ├── test_indicators.py           # Unit tests for every indicator module
    ├── test_decision.py
    └── test_signals.py
```

**Core rules:**
- `strategy/` is pure logic — zero I/O, zero backtest imports. It can be tested in isolation.
- `backtest/` is the only consumer of `strategy/`. Nothing else reaches in.
- Each file has one responsibility. Never mix indicator math, decision logic, and I/O in the same file.
- Backtest engines (`backtesting_py/` and `vectorbt/`) do not import each other. Each writes to its own `results/` directory.

### Hypothesis test module pattern

Inside `backtest/hypothesis_test/`, each hypothesis check uses the same generic folder pattern with descriptive names.

```text
└── hypothesis_test/
	├── <test_name_a>/               # e.g. regime directional-skew check
	├── <test_name_b>/               # e.g. setup edge isolation check
	├── <test_name_c>/               # e.g. trigger confirmation check
	└── hypothesis_test_output/
		└── results/
```
