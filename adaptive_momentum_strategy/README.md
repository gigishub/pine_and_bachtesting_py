# Adaptive Momentum Strategy

Strategy I from the Systematic Frameworks document — **Adaptive Time-Series Momentum and Volatility-Weighted Trend Following**.

## Overview

A modular 4-filter trend-following strategy for crypto markets. Each trade must pass four independent gates before execution:

| Step | Filter | Implementation |
|------|--------|---------------|
| 1 — Regime | ADX(14) > 25 | `strategy/indicators/adx.py` |
| 2 — Setup | Donchian breakout from squeeze | `strategy/indicators/donchian.py` |
| 3 — Trigger | CMF(20) > 0.05 | `strategy/indicators/cmf.py` |
| 4 — Exit | Chandelier SAR trailing stop | `strategy/risk/stops.py` |

## Project Structure

```
adaptive_momentum_strategy/
├── strategy/               # Pure logic — no I/O, no backtesting imports
│   ├── parameters.py       # @dataclass Parameters (all tunable values)
│   ├── signals.py          # compute_signals(df, params) → dict of Series
│   ├── indicators/
│   │   ├── adx.py          # ADX computation + regime filter
│   │   ├── donchian.py     # Donchian channel + squeeze detector
│   │   └── cmf.py          # Chaikin Money Flow + trigger
│   ├── decision/
│   │   ├── entry.py        # should_buy()
│   │   └── exit.py         # should_sell()
│   └── risk/
│       ├── stops.py        # Chandelier stop series + ratchet_stop()
│       └── sizing.py       # Risk-based position sizing
├── backtest/
│   ├── config.py           # BacktestConfig dataclass
│   └── runner.py           # backtesting.py Strategy class + __main__
└── tests/
    ├── test_indicators.py
    ├── test_decision.py
    └── test_signals.py
```

## Quick Start

```bash
# From project root
source .venv/bin/activate

# Run tests
python -m pytest adaptive_momentum_strategy/tests/ -v

# Run backtest (fetches SOL/USDT 1h data from Bybit, cached to parquet)
python -m adaptive_momentum_strategy.backtest.runner
```

## Configuration

Edit `backtest/config.py` to change the instrument, timeframe, or fees:

```python
@dataclass
class BacktestConfig:
    symbol: str = "SOLUSDT"          # Any Bybit linear symbol
    market_type: str = "linear"
    timeframe: str = "1h"
    start_time: str = "2024-09-01 00:00:00"  # 6 months + warmup buffer
    initial_cash: float = 10_000.0
    commission: float = 0.001        # 0.10% taker fee
```

Edit `strategy/parameters.py` to tune indicator settings:

```python
@dataclass
class Parameters:
    adx_period: int = 14
    adx_threshold: float = 25.0
    donchian_lookback: int = 20
    squeeze_history: int = 240       # bars — 10 days at 1h
    cmf_period: int = 20
    cmf_threshold: float = 0.05
    chandelier_lookback: int = 22
    chandelier_atr_mult: float = 3.0
    risk_pct: float = 1.0            # % of equity risked per trade
```

## Data

Data is fetched via `UPS_py_v2/data/fetch.py` using the Bybit REST API and cached locally as parquet files. Closed date ranges are cached permanently; open-ended fetches expire after 24 hours.

## Behavioural Validation Results (SOL/USDT, Sep 2024 – Apr 2026)

| Metric | Result | Notes |
|--------|--------|-------|
| Trades fired | 66 | Selective — 3-filter stack working correctly |
| Exposure Time | 8.3% | Strategy stays out of choppy markets |
| Buy & Hold | −37% | SOL declined in this period |
| Strategy Return | −7.5% | Avoiding the worst of the drawdown |
| Max Trade Duration | 2 days | Short-lived entries indicate tight stop discipline |

> **Note:** Profit optimisation is Phase 2. This phase validates behavioural correctness only — no lookahead bias, realistic fills, and sensible position sizing.

## Architecture Notes

- `strategy/` is purely functional — all functions are deterministic given inputs
- `compute_signals()` precomputes all pandas Series once in `Strategy.init()`
- Each Series is registered via `self.I(lambda s=series: s.values.copy(), name=key)` — the `s=series` default-arg pattern avoids Python closure capture bugs
- The Chandelier stop is **ratcheted upward** bar-by-bar in `next()` via `ratchet_stop()` — it never loosens
- `is_ready` gates all entry logic until all indicators have completed their warmup periods (~240 bars at 1h)
