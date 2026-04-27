Building to Test a Hypothesis

## Purpose

A hypothesis has been written. The goal now is to attack it and try to prove it wrong. Testing happens layer by layer, starting from the most foundational assumption.

Every piece of code built during this process has one of two destinies: it either becomes part of the permanent strategy, or it gets deleted once it has served its testing purpose. The structure below keeps those two things from mixing.

---

## The permanent strategy structure

Everything that may survive and become part of the final strategy goes into its permanent location immediately. Name directories and files after what they do, not after the test they are currently supporting.

```text
<strategy_name>/
├── __init__.py
├── README.md
├── strategy/                        # Pure logic — zero I/O, zero backtest imports
│   ├── __init__.py
│   ├── parameters.py                # @dataclass — all tunable values, no logic
│   ├── signals.py                   # compute_signals(df, params) → dict[str, Series]
│   ├── indicators/
│   │   ├── __init__.py
│   │   ├── regime/                  # One file per indicator
│   │   ├── setup/
│   │   └── trigger/
│   ├── decision/
│   │   ├── __init__.py
│   │   ├── entry.py                 # Entry gate: regime + setup + trigger → bool
│   │   └── exit.py                  # Exit gate: stop / target / trailing → bool
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
│   ├── hypothesis_tests_raw/
│   │   ├── __init__.py
│   │   ├── runner.py                # Pure NumPy/pandas forward-scan — no framework dependency
│   │   ├── run.py                   # CLI entry for raw runners
│   │   ├── results/
│   │   │   └──                      # raw outcome-engine outputs only
│   │   └── configs/
│   │       ├── __init__.py
│   │       └── default.py
│   ├── reporting/
│   │   ├── __init__.py
│   │   └── output.py                # Shared report formatting/export helpers
└── tests/
    ├── __init__.py
    ├── test_indicators.py           # Unit tests for every indicator module
    ├── test_decision.py
    └── test_signals.py
```

**Hard rules for permanent code:**
- `strategy/` has zero I/O and zero backtest-framework imports. It can be tested in isolation.
- `backtest/` is the only consumer of `strategy/`. Nothing else reaches in.
- One file, one responsibility. Indicator math, decision logic, and I/O never share a file.
- Each indicator in `indicators/regime/`, `indicators/setup/`, `indicators/trigger/` gets its own file, named after what it computes.

**Hard rules for backtest engine separation:**
- `backtest/backtesting_py/` and `backtest/vectorbt/` are separate engines. They do not import each other.
- Each engine has its own `configs/` directory. Do not place vectorbt configs in backtesting.py config paths, or the reverse.
- Each engine writes only to its own local `results/` directory:
    - `backtest/backtesting_py/results/`
    - `backtest/vectorbt/results/`
    - `backtest/hypothesis_tests_raw/results/`
- Shared helpers (report formatting, common serialization, common path builders) belong in `backtest/reporting/` or `backtest/config.py`, not inside an engine folder.
- Step 1 (single-run falsification) uses `backtesting_py` by default. Use `vectorbt` when you move to broad sweeps and robustness grids.
- Use `hypothesis_tests_raw/` when the test requires no framework at all — vectorised NumPy/pandas forward-scans, outcome engines, statistical checks. No `Backtest` class, no `Portfolio` object. This is also where hypothesis test runners that have graduated to permanent status live if they don't belong in either framework.

---

## The one-way dependency rule

Temporary test code may import from permanent strategy code.

Permanent strategy code must never import from temporary test code.

This is the only rule that needs to be enforced. Everything else follows from it.

---

## The hypothesis test structure

Anything built only to attack, compare, falsify, or measure a hypothesis goes into a dedicated temporary directory. Name it after the question being investigated.

```text
<strategy_name>/
└── hypothesis_tests/
    └── <descriptive_name>/          # Named after the question, not a step number
        ├── __init__.py
        ├── config.py                # Test-specific settings (random entries, fixed stops, etc.)
        ├── entries.py               # Throwaway entry logic for this specific test
        ├── runner.py                # Test harness — not the production backtest
        └── run.py                   # Entry point: python -m <strategy>.hypothesis_tests.<name>.run
```

Examples of well-named test directories:

```text
hypothesis_tests/
├── regime_random_entry_check/       # Does the regime filter create directional skew?
├── regime_indicator_isolation/      # EMA alone vs VATS alone vs combined
├── setup_level_edge_check/          # Are setup levels better than random resistance?
├── trigger_volume_confirmation/     # Does volume spike add information beyond setup?
└── exit_atr_multiplier_sweep/       # Which ATR target multiplier maximises profit factor?
```

---

## The placement question

Before writing any code, ask:

> **If this hypothesis survives, would this code still belong in the strategy?**

- **Yes, and it uses a framework** → put it in `backtest/backtesting_py/` or `backtest/vectorbt/`.
- **Yes, but it uses no framework** → put it in `backtest/hypothesis_tests_raw/`.
- **Yes, and it is pure logic with no I/O** → put it in `strategy/`.
- **No** → put it in `hypothesis_tests/<descriptive_name>/`.

Indicator math, signal computation, and risk logic almost always belong in `strategy/`. Entry harnesses, comparison runners, random entry generators, and reporting scripts almost never do.

---

## Promotion rule

If something inside a hypothesis test directory turns out to be genuinely reusable, extract only the pure logic into `strategy/`. Do not move the whole test harness. Only the part that has a permanent job gets promoted.

---

## Cleanup

Once a hypothesis is resolved — passed or failed — delete the test directory. The permanent code stays. The scaffolding is gone.

```bash
rm -rf <strategy_name>/hypothesis_tests/<descriptive_name>/
```

If the hypothesis failed, update or remove the corresponding indicator from `strategy/indicators/`. Leave no dead code.