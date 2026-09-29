# Edge search — PLAN

Find a crypto strategy that makes money on unseen data, tested as a whole portfolio (not per-signal).
Inspired by the UPS_py_v2 review: its grid search had no out-of-sample test and its live results were negative.
Earlier arcs: `../swing_research/`, `../long_short_research/` (read their VERIFICATION_INDEX first).

## Start
- Point-in-time Binance daily panel incl. delisted coins (`../swing_research/rotation_pit.py: load_panel`).
- Known so far: BTC trend filter long-only ~30%/yr but drawdown ~45–63%; funding carry ~5%/yr and falling;
  coin-level trend and shorts add nothing; mean reversion fails.
- UPS_py_v2: no evidence of edge (see chat review; grid best = noise, live net negative).

## Goal
Know which of 10 pre-declared ideas (if any) is profitable after costs on unseen data.
A clear "none" is a valid result.

## Done when
- All 10 ideas have a train verdict; survivors have a validation verdict; finalists ran once on test.
- Result is a written verdict per idea in `VERIFICATION_PHASE_A.md`.

## Win condition (user, fixed)
On validation AND test, after costs, the portfolio must satisfy **either**:
- (a) CAGR ≥ 20% and max drawdown ≤ 20%, **or**
- (b) beats BTC buy-and-hold on both CAGR and max drawdown (strict: higher return, smaller drawdown).
1h timeframe only if the edge is massive. Spot and futures (long/short) allowed.

## Rules (fixed before testing)
- Universe per day: top 10 by 180-day median dollar volume, ≥ 180 days listed, delisted included.
- Splits: train start → 2022-12-31; validation 2023-01-01 → 2024-09-30; test 2024-10-01 → now (run once).
- Decide on the daily close, trade next open. Cost 0.15% per side of turnover (fee + slippage).
  Funding on perps is ignored at first; anything that survives gets funding added (M-later).
- Each idea has fixed parameters written before the run. No grid search. Only a ×0.5 / ×2 lookback check
  for robustness, and it is reported, never used to pick a winner.
- Gates on train, in order: (1) return after costs > 0, (2) beats ≥ 95% of 200 circular time-shifts of its own
  weights on Calmar, (3) robust: both lookback variants still positive.
- Only ideas passing train go to validation; only ideas passing validation go to test.
- Every idea tried is logged, including failures. Ideas added later count against the winner
  (a winner among N ideas must clear the bar for N ideas).

## Ideas (10)
- [x] A — Control: BTC trend (close > SMA200 and 20d return > -3%), long BTC → pass train, fail valid
- [x] B — Cross-sectional momentum: top 3 of 10 by 60d return, cash when BTC filter off → pass train, fail valid (loses money)
- [x] C — Time-series momentum basket: each coin long if 60d return > 0 and close > SMA100, equal slots → fail train
- [x] D — C with inverse-vol weights, vol target 30%, no leverage → fail train
- [x] E — Low-vol tilt: 3 lowest 60d-vol coins, cash when BTC filter off → pass train, fail valid
- [x] F — Pullback in uptrend (UPS-inspired): coin > SMA100 and RSI(2) < 10, hold 5 days → fail train
- [x] G — Squeeze breakout (UPS-inspired): low Bollinger-width percentile then close > upper band, exit < SMA20 → fail train
- [x] H — Long/short momentum: long top 3, short bottom 3 by 60d return, dollar neutral, weekly → pass train, fail valid
- [x] I — Breadth regime: long equal-weight universe when > 50% of coins are above their SMA50 → fail train
- [x] J — Risk-managed beta: equal-weight universe, weekly, vol target 30%, cash when BTC filter off → fail train

## Milestones
- [x] M1 — Engine + sanity checks (random weights = no edge; peeking = edge; buy-and-hold matches)
- [x] M2 — Ideas A–J on train, verdicts logged
- [x] M3 — Survivors on validation
- [ ] M4 — Finalists on test once, then funding and 4h/1h follow-up if any pass
  - **Status:** no finalists (nothing passed validation). Test untouched. Next step decided at a checkpoint.

## Open / deferred
- Perp funding for shorts (H) and levered legs.
- 4h data for finalists (Bybit local data is 2020+, picked coins only).
