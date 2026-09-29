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

## Round 3 — swing trend in both directions, any timeframe (declared before any run; frozen)
User goal: follow the big up and down moves, long and short, on any timeframe. No idea count limit here, but every cell is logged.
Universe: the 22 Bybit perps with local candles (`../crypto_data/data/`), each coin traded on its own signal, equal-weight average of the coins
listed that day. Timeframes 1h, 4h, 1d. Position in {-1, 0, +1}, decided on the bar close, earns the next bar.
Costs: 0.10% per side of turnover (perp taker fee + slippage) plus the real Bybit funding (long pays, short receives the settled rate).
Families, each with horizon N = 5, 20, 60 days (converted to bars): F1 Donchian stop-and-reverse (break of N-bar high = long, low = short, hold until
the opposite break); F2 SMA cross (N/4 vs N); F3 chandelier reversal (flip when close is 3 ATR(N/4, min 10 bars) from the extreme since the flip);
F4 time-series momentum (sign of N-bar return). Each shown as both legs, long-only and short-only. 4 × 3 × 3 = 36 cells; all reported.
Calibration: a hindsight zigzag (20% reversal, daily BTC) gives the ceiling of "the big moves" so we can see what share real-time rules capture.
Split: train 2021-01-01 → 2023-06-30, validation 2023-07-01 → 2024-09-30, test 2024-10-01 → now (once).
Train gates per cell (both legs): (1) net return after costs and funding > 0; (2) beats >= 95% of 200 circular shifts of its positions on Sharpe;
(3) the neighbouring horizons of the same family and timeframe are also positive. Judged on cells, not on the best one: a real edge is a plateau.
Cells passing go to validation (gates 1 and 2 plus the win rule with capture), survivors to test once. 36 cells counted against any winner.

## Round 4 — EMA + ATR entry, both directions (user's idea; declared before any run; frozen)
Same universe, costs, funding, splits and gates as Round 3 (`swing_band.py` reuses `swing_trend.py`). n = EMA and ATR window in days (10 or 20).
- Variant A (band breakout): long when close > EMA(n) + x·ATR(n), short when close < EMA(n) - x·ATR(n), x in {1, 1.5, 2}.
- Variant B (volatility expansion): long when close > EMA(n) and ATR(n) >= x · mean(ATR(n) over the last n bars), short when close < EMA(n) and the same
  expansion, x in {1.25, 1.5}.
- Exit for both: close crosses back through the EMA (flat). No immediate reversal. Timeframes 1h, 4h, 1d. Cells: A 2×3×3 = 18, B 2×2×3 = 12; legs both/long/short shown.
- Gates as Round 3 (net > 0, beats >= 95% of shifted positions, neighbouring settings positive). 30 more cells counted against any winner (66 total in Rounds 3-4).

### Round 4b — exits for the band breakout (user asked; declared after seeing Round 4 train; frozen)
Round 4 train: variant A long leg is positive in 15 of 30 cells (+4% to +13%/yr, best on 1h/4h), short leg negative in all, variant B nothing. Only
variant A is followed up, with n in {10, 20} days, x in {1, 2} and these exits (entry as in Round 4):
- E1 trailing stop: exit when close < highest close since entry - m·ATR(n) (short mirrored), m in {2, 3}. Replaces the EMA exit.
- E2 fixed stop: exit when close < entry close - m·ATR(n) at entry, m in {2, 3}, or when close crosses back through the EMA.
- After any exit the entry signal must be false for one bar before a new entry.
Cells: 2 × 2 × 4 exits × 3 timeframes = 48, legs both/long/short. Shift test on both and long. The exit variants were chosen after
seeing train, so they count as extra cells (114 in Rounds 3 to 4b) and validation is the real test; nothing is tuned further on train.

Round 4b train result (after fixing the shift null, see Phase B): both legs 0 of 48 pass; long-only 1 of 48 passes gates 1-2 (1h, n=10, x=2, fixed stop m=3:
+12.3%/yr, maxDD -34.7%, `shift_p` 0.04), and its neighbours (x=2, n in 10/20, m in 2/3, 1h fixed stop) are all positive (+6% to +12%), so gate 3 passes.
Promoted to validation, long-only, as the plateau of those four cells, judged on the four together (about 2.4 false passes are expected by chance in 48 long cells):
1h, x=2, fixed stop, n in {10, 20}, m in {2, 3}. Validation win rule as in Rules; test only if the plateau holds.

## Round 5 — the long-only 1h band breakout on other coins (user asked; declared before any run; frozen)
Rule unchanged from the Round 4b plateau: long-only, 1h, entry close > EMA(n) + 2·ATR(n), fixed stop at entry - m·ATR(n) or close back below EMA, n in {10, 20} days,
m in {2, 3} (four cells, no retuning). Coins: every Bybit perp that has funding data and 1h candles (`../crypto_data/data_extra/` downloaded now, plus the 11 already used).
Same costs (0.10% per side + funding) and splits. Question: does it work better on other coins, and can good coins be picked in advance?
- Judged on the whole set: basket CAGR, maxDD and Sharpe vs the equal-weight buy-and-hold of the same coins, `shift_p` (gate 2), and the share of coins with positive CAGR.
  The original 11 coins and the new coins are reported separately (the 11 were used to choose the rule, the new coins were not).
- Coin picking: a coin's train result must predict its validation result (rank correlation of per-coin CAGR, train vs validation) before any "best coins" subset is used.
  Any subset rule is declared on train only and then judged on validation, never chosen on validation.
- Test window run once, and only if the whole-set result passes validation (gate 2 and rule (a) or (b)).
- Caveat that cannot be removed: Bybit only lists perps that still exist, so delisted coins are missing; that flatters any long-only result (survivorship).

Round 5 addition (user, before any run): also report a **liquid set** = at each bar the 20 coins with the highest 90-day median dollar volume (close × volume) among the
coins with data, standing in for "enough market cap to trade". Chosen by liquidity only, never by results; positions are forced flat in coins outside the set.

## Round 6 — BTC as the leader for other coins (user asked; declared before any run; frozen)
Universe: the liquid set above (top 20 by 90-day median dollar volume), BTC excluded from the traded coins, timeframes 1h, 4h, 1d, same costs, funding and splits.
Rules (BTC state = BTC's own Round 4b band breakout: +1 long / -1 short / 0 flat, x = 2, fixed stop m = 3, n in {10, 20} days):
- R0 reference: alt's own band breakout, long-only (n = 20, x = 2, m = 3), no BTC input.
- R1: R0 but only while BTC passes the trend filter (close > SMA200 and 20-day return > -3%, previous fully closed day).
- R2: R0 but only while BTC state is +1.
- R3 follow-BTC entry: go long the alt when BTC state flips 0 -> +1 (whatever the alt is doing), exit when BTC state is not +1 or at entry - 3·ATR(n); mirror short when BTC state flips to -1.
- R4 surge follow: long every alt while BTC's 5-day return > +8%, short while < -8% (state-based); R4 legs long/short/both.
- Lead-lag statistic (no trading): pooled OLS of the alt's next-w-bar return on its own past-w-bar return and BTC's past-w-bar return, w = 1 day and 5 days (1d bars) and 4 hours and 1 day (1h bars);
  the coefficient on BTC is judged against 200 circular shifts of BTC's series (`shift_p` <= 0.05 and the same sign in train and validation).
Cells: R1-R3 × n {10, 20} × 3 timeframes, R0 × 3, R4 × 3, plus the statistic. Legs both/long/short. Gates as Round 3-5 (net > 0, `shift_p` <= 0.05 on the basket, neighbours positive).
The 114 cells of Rounds 3-4b plus these count against any winner. Test window run once, only for a cell family that passes train and validation.

## Round 7 — what makes the BTC/SOL bot work, and which coins to add (user asked options 1 and 2; declared before any run; frozen)
Data: Binance daily, all USDT pairs incl. delisted (a gap > 7 days splits a coin), point-in-time universe = top 30 by 180-day median dollar volume, >= 180 days listed.
Rule: the live bot's own strategy code (`../swing_research/bot_baseline.py: bot_position`, live parameters) with the BTC 20-day-return entry filter (>= -3%, prior close vs 20 closes before)
applied to every coin, cost 0.15% per side, open-to-open. Splits: train 2018 → 2022-12-31, validation 2023-01-01 → 2024-09-30, test 2024-10-01 → now (run once). Code: `bot_coins.py`.
- Option 1, traits: at each quarter start (every 91 days from 2019-01-01) and for each eligible coin with >= 365 days listed, six traits from the trailing 365 days: liquidity (log 180d median
  dollar volume), volatility (std of daily returns), trend efficiency (mean 20-day Kaufman efficiency ratio), persistence (autocorrelation of 5-day returns at lag 5), BTC correlation (daily returns),
  age (days listed). Outcome: the rule's summed log return over the next 91 days. Per quarter the Spearman rank correlation trait vs outcome; averaged per split.
  A trait passes if its mean correlation has the same sign in train and validation, |mean| >= 0.05 in both, and t-stat over quarters >= 2 in train. Top-minus-bottom tercile spread must be positive
  (in the passing direction) in train and validation. Where BTC and SOL sit on each trait is reported. Passing traits define an ex-ante subset (top tercile in the train direction) judged on validation, then test once.
- Option 2, walk-forward admission: at each quarter start a coin is admitted if over its trailing 730 days the rule had >= 8 trades, profit factor >= 1.5, and a positive return in each 365-day half.
  Admitted coins are equal-weighted for the next quarter (cash if none). Compared with: BTC alone, BTC + SOL (from 2020-08), and every eligible coin equal-weighted, all with the same rule.
- Both options are judged as portfolios on validation, then test once, against those baselines and BTC buy-and-hold, with the win rule (a) or (b). Nothing is tuned after seeing results;
  the thresholds above are the only ones tried. Limits: overlapping trailing windows, ~28 train quarters and ~7 validation quarters give low power.

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
- [x] M6 — Round 3 swing trend both directions, 36 cells on 1h/4h/1d: none passes train (see Phase B)
- [x] M7 — Rounds 4 and 4b (EMA/ATR band breakout, exits) on train and the promoted plateau on validation: fails (see Phase B)
- [x] M8 — Round 5 (long-only breakout on other coins, liquid set): no promotion, good coins cannot be picked (see Phase B)
- [x] M9 — Round 6 (BTC as leader): no rule passes train, lead-lag sign flips (see Phase B)
- [x] M10 — Round 7 (traits and walk-forward coin admission for the BTC/SOL bot): neither works (see Phase B)
- [ ] M4 — Finalists on test once, then funding and 4h/1h follow-up if any pass
  - **Status:** no finalists (nothing passed validation). Test untouched. Next step decided at a checkpoint.

## Next (for the new session)
- Read `VERIFICATION_INDEX.md` (Current truths) first. Seven rounds, ~150 pre-declared ideas and cells; nothing beats BTC (and SOL) with the bot rule and the BTC 20-day filter.
- Checkpoint after Round 7: the end goal (a strategy that catches big moves on any tradable coin) is not supported by the evidence: shorts lose everywhere, breakouts on other coins only follow the market,
  BTC does not reliably lead alts, coin traits and track records do not select coins forward. **Recommendation: pivot** from finding a new strategy to running what works:
  finish the live bot's switch day (`../swing_research/PLAN.md` M2.4–M2.5), keep BTC (+ SOL) only, and stop the search unless a new data source or a concrete setup from the user is available.
- Ideas still untested that are not price rules: listing / unlock / news events, cross-exchange basis, liquidation data, maker-fee versions of the 4-hour BTC-reversal effect.
- Code move of `swing_research/` and `long_short_research/` into this folder is deferred (would break imports).

## Open / deferred
- Perp funding for shorts (H) and levered legs.
- 4h data for finalists (Bybit local data is 2020+, picked coins only).
- Carried over from swing arc: live-bot switch day and go-live (M2.4–M2.5), swing candidates on 4h/daily (M3), trade-quality filter (M4),
  ALGO/XLM 4h retry, real market-cap filter for rotation. See `../swing_research/PLAN.md`.
- Carried over from long/short arc: mean-reversion setup layer (M7–M8 in `../long_short_research/PLAN2.md`), M10 funding filter,
  basis/margin risk and Bybit spot fees for carry.
