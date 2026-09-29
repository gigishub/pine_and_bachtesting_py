# Edge search — PLAN

Find a crypto strategy that makes money on unseen data, tested as a whole portfolio (not per-signal).
Inspired by the UPS_py_v2 review: its grid search had no out-of-sample test and its live results were negative.
This arc now also carries the conclusions of the two earlier arcs (summarised in Start below and in
`VERIFICATION_INDEX.md` Current truths). Their code and phase docs stay where they are and are linked, not copied:
`../swing_research/` (live bot, BTC filter, rotation) and `../long_short_research/` (long/short trend, chop, funding carry).

## Start
- Point-in-time Binance daily panel incl. delisted coins (`../swing_research/rotation_pit.py: load_panel`).
- Known so far: BTC trend filter long-only ~30%/yr but drawdown ~45–63%; funding carry ~5%/yr and falling;
  coin-level trend and shorts add nothing; mean reversion fails.
- Swing arc: the live bot works on BTC/SOL only; the BTC 20-day-return filter is the one robust improvement
  (already wired into the live bot's dry run, see `../swing_research/PLAN.md` M2.4–M2.5). Rotation on large caps
  ≈ BTC with trend filter, worse drawdown.
- Long/short arc: no directional long/short, coin-trend or chop/mean-reversion edge passed. Funding carry
  (long spot + short perp) on BTC/ETH is real but ~5%/yr and falling.
- Data now local: Bybit funding for 22 coins in `../crypto_data/data/<SYM>/` (TON stops 2026-06-15) plus 114 more
  perps in `../crypto_data/data_funding/`. Daily open interest (`*_oi_1d_*.parquet`, same folders) is downloaded for the 22 coins, no gaps; BTC OI starts 2020-08-05, HYPE 2024-12, TON only 2026-01 → 2026-06.
  Caveat: ~39% of top-40 coin-days have no funding (delisted coins have no Bybit perp), so funding tests lean to survivors.
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

**Decided later (user): rule (b) is judged on capture ratios, not full-period return.** In non-overlapping 30-day
blocks vs BTC buy-and-hold (`capture.py`): a small loss when BTC crashes counts as a win (-1% vs -40%).
Proposed thresholds, **still to confirm with the user before any test-period run**: up capture ≥ 70% and down capture ≤ 30%,
on validation and test, with enough BTC-down blocks (validation had only 8, all shallow, so it cannot judge this;
consider a crash-heavy window such as 2018 and 2022 from train as extra evidence, not as the pass gate).
Rule (a) is unchanged.

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

## Split for funding / open-interest ideas (declared before any run)
Bybit data is short (BTC from 2020-03, most coins 2021, HYPE 2024-12), so ideas that use funding or OI use their own split.
Ideas A–J above keep the Binance split.
- Train: each coin's first Bybit date (BTC 2020-03-25) → 2023-06-30 (keeps the 2022 bear).
- Validation: 2023-07-01 → 2024-09-30. Test: 2024-10-01 → now, run once (same test window as above).
- Universe: only coins with Bybit funding on that day; report the share of top-10/top-40 coin-days dropped
  and read every result as "survivors only".
- Gates are the same as in Rules. Extra gate tightening for the short train is **still to declare before the first run**.
- Nothing in this section has been run yet.

## Round 2 — crowding overlays (declared before any run; frozen)
Baseline sleeve = idea A (long BTC when close > SMA200 and 20d return > -3%). An overlay multiplies A's weight by
0 (cash) or 0.5; it never adds an entry. Signals at the daily close; funding uses only settlements strictly before the close;
open interest is lagged one extra day (the 1d bar timestamp is not known to be start or end of the interval).
Funding = mean per-8h rate over the last 7 days (F7). OI change = OI(t-1) / OI(t-8) - 1 (O7). z = vs trailing 90 days.
Ideas (fixed parameters, no grid):
- [x] K — cash when F7 z > 2 → fail train (shift_p 0.81)
- [x] L — cash when F7 > 0.03% per 8h (about 33%/yr) → fail train (0.81)
- [x] M — cash when O7 > +25% and BTC 7d return < +2% (OI up, price stalls) → fail train (0.47)
- [x] N — cash when O7 z > 2 → fail train (0.68)
- [x] O — half size when F7 z > 1 (cash when z > 2) → fail train (0.67)
- [x] P — cash when L or M → fail train (0.78)
- [x] Q — cash when the median F7 of the top-10 coins that have funding > 0.02% per 8h → fail train (0.87)
- [x] R — as K but the baseline is equal-weight top-10 ∩ funding coins, weekly, BTC filter on → fail train (0.92; gain is the basket)
- [x] S — as P with the baseline vol-targeted to 30% (no leverage) → fail train (loses money)
- [x] T — blend: 50% of L + 50% BTC funding carry (spot long + perp short, earns F, entry/exit cost 0.6%) → fail train (0.53; gain is the carry sleeve)
Split: train 2020-11-15 → 2023-06-30 (after OI and z warm-up), validation 2023-07-01 → 2024-09-30, test 2024-10-01 → now, once.
Gates on train (all four): (1) return after costs > 0; (2) overlay beats >= 95% of 200 circular shifts of the *overlay multiplier*
against price on Calmar (baseline A's trend timing is kept, so this tests the overlay only); (3) both ×0.5 and ×2 lookback
variants positive; (4) Calmar and max drawdown both better than baseline A on the same window.
Validation: gates 1, 2 and 4 again, plus win rule (a), or (b) on strict buy-and-hold or on capture ratios (up >= 70%, down <= 30%).
Test: survivors once. Stop rule: this is round 1 of the two allowed; a clear "none" is a valid result.
Caveat: test-window dates were already used by M10 (other ideas); any survivor there is weaker evidence.

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
- [x] M5 — Round 2 crowding overlays K–T on train: none passes (see Phase B)
- [ ] M4 — Finalists on test once, then funding and 4h/1h follow-up if any pass
  - **Status:** no finalists (nothing passed validation). Test untouched. Next step decided at a checkpoint.

## Next (for the new session)
- Read `VERIFICATION_INDEX.md` (Current truths) first. Rounds 1 and 2 (20 ideas) done; none passes validation; test untouched by these ideas.
- Checkpoint after round 2: closer to the goal? The goal itself needs a decision. Every pre-declared idea fails; what works
  is BTC trend (~28–30%/yr, drawdown ~45–50%) and carry (real, shrinking). The win rule (20%/20% or beat BTC on return and
  drawdown, or 70%/30% capture) is very hard in windows where BTC roughly doubles (validation). Recommendation: **simplify**.
  Either accept "the BTC 20-day-return filter on the live bot is the result" and stop searching, or relax the win rule.
- One more round is allowed by the stop rule. Only worth running if declared as sleeve blends (trend + carry, fixed weights)
  and judged on drawdown-adjusted return, since that is where the train data pointed (T: 15.9%/-14.6%). Expect it to fail
  validation on return because carry has faded to ~5%/yr.
- Code move of `swing_research/` and `long_short_research/` into this folder is deferred (would break imports).

## Open / deferred
- Perp funding for shorts (H) and levered legs.
- 4h data for finalists (Bybit local data is 2020+, picked coins only).
- Carried over from swing arc: live-bot switch day and go-live (M2.4–M2.5), swing candidates on 4h/daily (M3), trade-quality filter (M4),
  ALGO/XLM 4h retry, real market-cap filter for rotation. See `../swing_research/PLAN.md`.
- Carried over from long/short arc: mean-reversion setup layer (M7–M8 in `../long_short_research/PLAN2.md`), M10 funding filter,
  basis/margin risk and Bybit spot fees for carry.
