# Long/short trend — PLAN

Brief and lessons: `DRAFT_long_short_trend.md`. On-chain data is dropped (`DRAFT_onchain_data.md`).

## Start
- Long-only BTC trend filter (EMA240 + 20-day return ≥ -3%) is the only edge found so far (`../swing_research/`).
- Point-in-time Binance spot daily data for all USDT pairs incl. delisted (`../crypto_data/data_binance/1d/`).
- Execution venue: **Bybit linear perps** (user trades on Bybit). Local Bybit data (`../crypto_data/data/`, 22 coins,
  2020+) is picked today, so it is used for the full backtest and funding, not for finding the edge.
- Top-down edge method from `bear_strategy/hypothesis_test_v2/`: regime → setup → trigger, each must lift
  profit factor over its baseline, then the frozen stack is tested once on unseen data.

## Goal
Know whether a trend rule that goes long **and** short on the largest coins has an edge that survives unseen data.
A clear "no" is a valid result.

## Done when
- Every layer idea has a pass/fail verdict on train, and the promoted stack has been run once on validation and test.
- If a stack passes: full backtest net of fees and funding beats the long-only benchmark (criteria in the draft).

## Rules (fixed before testing)
- Universe per day: top 10 by 180-day median dollar volume, ≥ 180 days listed, delisted coins included.
- Train: start → 2022-12-31. Validation: 2023-01-01 → 2024-09-30. Test: 2024-10-01 → now (run once).
- Signal on the daily close, enter next open. Edge metric: forward 20-day return per signal day
  (5 and 10 days shown too), net of 0.2% round trip. PF = gains / losses.
- Layer pass (train, each side separately): PF lift ≥ 0.05 vs baseline, beats ≥ 95% of random time-shifts of the
  same signal, lift > 0 on ≥ 60% of coins and ≥ 60% of years.

## Milestones
- [x] M1 — Edge check engine + sanity checks (shuffled future = no edge; known answers)
- [ ] M2 — Regime layer (BTC-level), long and short separately
- [ ] M3 — Setup layer (coin-level trend) on top of the promoted regime
- [ ] M4 — Frozen stack on validation, then test once
- [ ] M5 — Full backtest with fees + funding vs benchmarks (only if M4 passes)

## Open / deferred
- 4h candles (only if the short side shows an edge on 1d).
- Bybit funding rates (`../crypto_data/fetch_bybit_funding_rates.py`): needed for M5 only.
- Shorts before ~2020 are hypothetical (few perps existed); 2018 is kept for signal evidence only.
