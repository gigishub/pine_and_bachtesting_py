# Bear Strategy

Short-side systematic strategy for crypto bear markets.

## Layers

| Layer | Indicator | Timeframe |
|-------|-----------|-----------|
| Regime | EMA 200, VATS (slope/ATR) | Daily |
| Setup | VPVR HVN, Anchored VWAP from swing high | 4H |
| Trigger | Volume spike vs 20-bar avg, True CVD divergence | 15min / 1min |
| Exit | ATR stop at swing high + 1×ATR_4H, volatility-scaled ATR target | 15min |

## Hypothesis Testing

Each layer is tested independently before combining. Test harnesses live in
`hypothesis_tests/` and are deleted once resolved. Permanent indicator code
lives in `strategy/indicators/` from day one.

## Running the Step 1 Test

```bash
source .venv/bin/activate
python -m bear_strategy.hypothesis_tests.regime_random_entry_check.run
```

## Structure

```
bear_strategy/
├── strategy/          # Pure logic — no I/O, no backtest imports
│   ├── parameters.py
│   ├── signals.py
│   ├── indicators/regime/
│   ├── decision/
│   └── risk/
├── backtest/          # Engine wrappers (backtesting.py, vectorbt)
├── hypothesis_tests/  # Temporary falsification harnesses
└── tests/             # Permanent unit tests
```
