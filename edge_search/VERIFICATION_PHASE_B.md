# Edge search — VERIFICATION_PHASE_B

Funding and open-interest work on the shorter Bybit-era data.

## M10 funding as a filter: a short-side lift that never turns the shorts profitable
Run by `../long_short_research/funding_filter.py` (top-40 point-in-time universe, signal uses only settlements
before the daily close, 40 fixed variants per split, results in `../long_short_research/results/funding_filter_*.csv`).
- Train (2021 → 2022): 1 of 40 passes: in BTC-bull days, dropping short days with very negative funding
  ("no cold", abs 3d funding > 0.03% / < 0). Short PF 1.47 vs base 1.35, lift +0.12, `p_shift` 0.04, 30 of 38 coins.
- Validation: the same variant passes again (lift +0.13, `p_shift` 0.00) plus one z-score variant, but the short PF is
  **0.91** (base 0.78): the filter improves a losing leg, it does not make it profitable.
- Test: same variant lift +0.03, `p_shift` 0.085, short PF **0.97** → fail.
- Every "avoid longs when funding is hot" variant fails on train. Hot funding as a short signal fails.
- Verdict: no funding-filter edge. Funding is not a usable entry or short signal on the daily top coins.
- Caveats: about 39% of universe coin-days have no funding (delisted coins have no Bybit perp), so the sample leans to
  survivors. All 40 variants were also run on the test window, so that window is no longer untouched for
  funding-filter ideas of this kind. Forward-return PF metric, not the portfolio engine.

## Round 2 train: no crowding overlay passes, every overlay is indistinguishable from a shifted one
Ideas K–T (declared in `PLAN.md`, "Round 2"), run once with `run_round2.py train` (train 2020-11-15 → 2023-06-30, daily
funding and OI, results in `results/round2_train.csv`). Baseline A on this window: CAGR 28.2%, maxDD -49.3%, Calmar 0.57
(BTC buy-and-hold 27.6% / -76.6%).
- Sanity first: a peeking overlay (cash before down days) gives CAGR 483% with `shift_p` 0.00; a shuffled overlay gives
  `shift_p` 0.44 → the runner detects edge when there is one and not when there isn't.
- Gate 2 (overlay beats ≥ 95% of shifted overlays) fails for all ten: `shift_p` 0.47 to 0.92. Nothing beats the timing of a random overlay.
- Cutting on funding (K, L, O), OI stall (M), OI z-score (N), or market-wide funding (Q) all lower or keep CAGR while
  drawdown falls only when the overlay sits in cash a lot (L: 17% of days, CAGR 8%, maxDD -34%; Q: 26% of days, CAGR 0.3%).
  That is de-risking by being out of the market, not a crash signal.
- K, M, N cut only 3% of days and change little (M: 27.4% / -48.4% vs A 28.2% / -49.3%).
- R (equal-weight funding coins, K overlay) and T (50% L + 50% BTC funding carry) beat A on Calmar and drawdown (R 0.76,
  maxDD -37.8%; T 1.09, maxDD -14.6%, CAGR 15.9%) but fail gate 2 — the gain is the basket (R) and the carry sleeve (T), not the overlay.
  S (vol-targeted, cut on funding or OI stall) loses money (-1.3%).
- Verdict: none of K–T passes train; validation and test untouched by this round. Crowding overlays on a BTC trend baseline
  add nothing that timing luck doesn't.
- Caveat: BTC-only overlays; OI lagged one day; train is 2.6 years with 15 non-overlapping 30-day BTC-down blocks.

## Round 3 train: no long/short trend system on 1h, 4h or 1d makes money after costs and funding
Superseded by: Round 3 to 4b: shift test fixed (the `shift_p` values quoted here were all 1.0 because of a NaN bug; the verdict itself stands, since no both-leg cell is positive)
36 cells (Donchian stop-and-reverse, SMA cross, chandelier reversal, time-series momentum × horizons 5/20/60 days × 1h/4h/1d),
22 Bybit perps (11 have 1h), 0.10% per side plus real funding, train 2021-01-01 → 2023-06-30 (`swing_trend.py train`,
`results/round3_train.csv`). BTC buy-and-hold on the window 2.1%/yr, maxDD -77%; equal-weight 22 coins -6.6%/yr, maxDD -83%.
- Both legs: **0 of 36** cells have positive CAGR; 0 of 36 pass the shift gate (`shift_p` ≈ 1.0: real timing is no better than shifted timing).
- Long-only: 3 of 36 positive (4h F1/20 +3.2%, 4h F2/20 +3.2%, 1d F2/20 +0.7%); short-only: **0 of 36**.
- Lower timeframes are worse, not better: 1h chandelier (F3) loses 64–77%/yr (about 50+ trades a year per coin at 0.10% + whipsaw).
- Hindsight ceiling, daily BTC train: a zigzag riding every ≥20% swing both ways would make ~1,700%/yr (19 swings). The moves are real
  and visible on a chart, but no real-time rule here captures them: the rules enter after the move and exit after the reversal.
- Funding is a first-order cost, not a detail: always-long BTC perp = -14.8%/yr vs +2.1% spot buy-and-hold on this window (longs paid
  ~18%/yr on average). BTC F1/20 is -6.1% net and +10.6% without funding. Long-biased perp systems start ~15 points behind.
- Engine checks: peeking (knows next bar) → absurd return; always-long = buy-and-hold minus funding. Signal inversion does not rescue
  it (inverted also loses on ETH and the 22-coin average) → whipsaw and volatility drag, not a sign error.
- Single-coin exceptions, not evidence: BTC time-series momentum 60d makes +20.7% net (its inverse -51.8%), but ETH and the coin average do not.
- Verdict: none of the 36 cells passes train; validation and test untouched.
- Caveat: fixed grid of 3 horizons per family; the plan did not tune stops, filters or coin selection. Train includes the 2021 alt
  blow-off and the 2022 bear, both hard for trend systems with 5–20 day horizons.

## Round 3 to 4b: shift test fixed (funding NaN bug), verdicts re-checked
Supersedes: Round 3 train, its statements "0 of 36 pass the shift gate (`shift_p` ≈ 1.0: real timing is no better than shifted timing)".
- Bug: funding was NaN on bars without data, which made the Sharpe NaN in `shift_p()`, so real and null both became -inf and every `shift_p` was 1.0
  (the peek check also gave 1.0). Fixed in `swing_trend.py` (`np.nan_to_num`); peek now gives 0.00. Rounds 3, 4 and 4b re-run on train.
- Round 3 (36 cells): both legs 0 of 36 positive; long-only 3 of 36 barely positive (+0.7% to +3.2%, shift not computed for long-only in this round). Verdict unchanged.
- Round 4 (EMA ± x·ATR band and ATR expansion, 30 cells, 10–20 day windows): both legs 0 of 30 positive; short-only 0 of 30; long-only band breakout (A) positive in
  15 of 30 (+4% to +13%/yr, best on 1h/4h) but 0 pass the shift gate; expansion variant (B) nothing. The exit "close back through the EMA" is used.
- Round 4b (band breakout with trailing or fixed stops, 48 cells): both legs 0 of 48 pass (1 positive); trailing stops are worse than the EMA exit;
  fixed stops help long-only on 1h and 4h. Long-only: 19 of 48 positive, 1 passes gates 1 and 2 (1h, n=10, x=2, fixed stop m=3: +12.3%, maxDD -34.7%, `shift_p` 0.04);
  its neighbours (1h, x=2, fixed stop, n 10/20, m 2/3) are all positive on train (+6% to +12%) while x=1 cells are negative. One pass in ~48 long cells is about what chance gives (2.4 expected).

## Round 4b validation: the long-only plateau makes 35% with -19% drawdown but is not better than BTC and fails the shift gate; shorts lose 25–28%
Validation 2023-07-01 → 2024-09-30, the four long-only cells (1h, x=2, fixed stop, n in 10/20, m in 2/3), `swing_exit.py valid 1h 2.0 fixed`, `results/round4b_valid_plateau.csv`.
- Long-only: CAGR +35% to +37%, maxDD -18.9% to -20.4%, Sharpe 1.0–1.1, 25–39 trades/yr per coin. Rule (a) (CAGR ≥ 20% and maxDD ≤ 20%) met by 3 of 4 cells (the fourth has -20.4%).
- Gate 2 fails: `shift_p` 0.08 to 0.18 (needs ≤ 0.05). Fifteen months is short, so power is low, but the gate is the declared one.
- Versus the window: BTC buy-and-hold +79%/yr, maxDD -32%, Sharpe 1.5 (11-coin equal weight +80%, -46%). The system earns less than BTC and has a lower Sharpe; rule (b) fails.
  It behaves like a partial-exposure long book: capture up 61% / down 82% in 30-day blocks (only 9 down blocks, all shallow).
- Short leg: -26% to -28%/yr in every cell; both legs together +0% to +3%. Short trend-following loses in train and validation, in every cell tested this session (0 of 114).
- Verdict: fail. Test window untouched by Rounds 3–4b. What remains is a long-only 1h breakout that reduces drawdown but earns less than holding BTC in this window
  and in train earned +12% while BTC earned +2% and the coin average lost 10%; it is a risk-managed long, not a two-directional edge.
- Caveat: exit variants were chosen after seeing train (counted in the 114 cells); 11 coins only on 1h; 0.10% per side may be optimistic for a 1h system trading 25–40 times a year per coin.

## Round 5 other coins: the long-only 1h breakout does not generalize on train, works as de-levered alt beta on validation, and good coins cannot be picked in advance
Frozen rule (1h, long-only, x=2, fixed stop m in 2/3, n in 10/20 days) applied to every Bybit perp with funding and 1h candles: 22 original + 112 downloaded to `../crypto_data/data_extra/`
(ZILUSDT and RVNUSDT failed to download; 82 coins have >= 90 days in train, 107 in validation). `swing_coins.py`, `results/round5_*.csv`. Original-11 = the coins the rule was chosen on.
- Train (2021 → 2023-06): original coins +6% to +12%/yr (as before). New coins **-0.7% and -1.6%** for n=10 and **-19% to -23%** for n=20; only 18–30% of coins are positive.
  Equal-weight buy-and-hold of the same coins: -20%/yr, maxDD -88%. The rule cuts the drawdown to -37% to -63% but does not make money on the new coins.
- Validation (2023-07 → 2024-09): all sets positive. New coins +41% to +48%/yr, maxDD -22% to -32%, Sharpe 1.14–1.21, `shift_p` 0.02–0.04 (gate 2 passes); equal-weight buy-and-hold
  of the same coins +73%, maxDD -65%, Sharpe 1.10. Liquid-20 set: +46% to +59%, maxDD -28% to -33%, but `shift_p` 0.28–0.35 (gate 2 fails).
- Rule (a) fails (maxDD 22% to 33% on the wider sets; the original 11 coins meet it in 3 of 4 cells); rule (b) fails (CAGR far below buy-and-hold).
  Sharpe is equal to buy-and-hold in validation and lower in train: this is roughly half-exposure beta, not extra alpha.
- Can good coins be picked in advance? No: rank correlation of per-coin CAGR train vs validation is 0.01 to 0.06 (n=10) and -0.10 (n=20); the top train quartile earned a median +9.3% in
  validation vs -2.0% for the rest, which is not a stable selection rule. Share of coins with positive CAGR: 30% in train, 54% in validation (a market effect).
- Verdict: gate 3 (neighbours) fails on train (n=20 cells negative); no promotion to test. The 1h breakout is a risk-managed long that follows the market, not a coin-picking edge.
- Caveats: survivorship (Bybit lists only perps that still exist, which flatters long-only results); liquid-20 shift test is approximate (mask applied inside the shift).

## Round 6 BTC as the leader: no trading rule passes; the 1–5 day lead-lag flips sign between train and validation
Rules R0–R4 (alts' own breakout, gated by BTC trend filter or BTC breakout state, follow-BTC entry, BTC surge follow) on the liquid-20 alts, `swing_lead.py`, `results/round6_*.csv`.
- Train: 0 of 21 cells have `shift_p` <= 0.05 and CAGR > 0. Near misses: 1h R2 (alt breakout while BTC is in breakout) +18.8% (p 0.07); 4h R0 +10.6% (0.08); 1h R3 both legs +25.8% (0.08).
  R3 (enter alts when BTC breaks out) has a positive long leg in all 6 cells (+5% to +20%) but none is significant (p 0.08–0.18); its short leg loses in 5 of 6. R1 (BTC trend filter) and R4 (BTC surge) do not help.
  Liquid-set buy-and-hold on train: 1.3% (1d), 5% (4h), -35% (1h, wide set), maxDD -82% to -94%, so any timing out of alts looks good against it.
- Lead-lag statistic (alt's next-w return on its own past-w return and BTC's past-w return, non-overlapping bars, circular-shift null):
  train 1d 5-day +0.12 (p 0.04), 4h 1-day +0.08 (p 0.00), 4h 1-bar -0.04 (p 0.01); validation 1d 5-day -0.05 (0.68), 4h 1-day -0.09 (0.07), 4h 1-bar -0.055 (0.03), 1h 4-bar -0.07 (0.01), 1h 24-bar -0.16 (0.01).
  Sign flips for horizons of a day or more (positive in train, negative in validation). The only sign that holds in both is small and negative at 4h to 1h horizons (alts give back part of a BTC move):
  a 1% BTC move implies about 0.05% on the alt, less than the 0.10% per side cost, so it is not tradeable as is.
- Verdict: BTC does not reliably lead alts in a way that survives a split; BTC as a *gate* (R1, R2) does not add a robust edge. Test untouched.
- Caveat: R3 pattern (all six long legs positive) is one BTC signal seen through six views, not six independent confirmations.

## Round 7 what makes the BTC/SOL bot work: no coin trait predicts where the bot rule works, and admitting coins from their track record does not beat BTC alone
Binance daily, all USDT pairs incl. delisted, point-in-time top 30 by 180-day dollar volume (138 coin segments ever eligible), the live bot's own strategy code (`bot_baseline.py: bot_position`)
with the BTC 20-day filter on every coin, 0.15% per side (`bot_coins.py`, `results/round7_*.csv`). Sanity: BTC 25% / 49% / 33% CAGR and maxDD -44% / -23% / -12% (train / validation / test),
SOL 239% / 95% / 32%; consistent with the live-bot baseline (test drawdown -12%).
- Option 1 (traits): quarterly rank correlation between a trait and the rule's next-91-day log return. No trait passes: the largest train t-stat is 0.78 (needed >= 2) and train mean rho is -0.06 to +0.03 for all six.
  Validation shows large correlations for age (+0.22, t 2.7), BTC correlation (+0.21, t 6.9) and volatility (-0.26, t -2.5) but train is about zero (0.02, 0.03, 0.01), so the sign does not carry over;
  these describe the 2023–24 bull market, not a stable coin property.
  BTC and SOL do share traits (percentile among eligible coins on 2026-06-23): liquidity 96 / 89, BTC correlation 96 / 89 (by construction for SOL), volatility 4 / 26 (low), age 93 / 48.
  They are the most liquid, least volatile coins, but that does not predict which other coins the rule works on.
- Option 2 (walk-forward admission: >= 8 trades, PF >= 1.5 and a positive return in each 365-day half of the trailing 730 days), equal weight of admitted coins, next 91 days (2019 onward):
  | | CAGR / maxDD / Sharpe train | validation | test |
  |---|---|---|---|
  | admitted coins | 34% / -31% / 0.98 | 39% / -37% / 1.08 | -4% / -38% / -0.04 |
  | BTC only (bot + filter) | 37% / -44% / 0.97 | 49% / -23% / 1.40 | 35% / -12% / 1.48 |
  | BTC + SOL | 88% / -44% / 1.63 | 76% / -20% / 1.72 | 35% / -13% / 1.34 |
  | all eligible coins | 60% / -27% / 1.43 | 16% / -32% / 0.73 | 5% / -39% / 0.32 |
  | BTC buy-and-hold | 45% / -77% / 0.88 | 110% / -26% / 1.76 | 18% / -53% / 0.59 |
  Admission trails BTC alone on validation and test; on average 5 (train), 3 (validation) and 6 (test) coins are admitted. Selecting coins from their own history does not work forward.
- BTC + SOL is itself a hindsight choice (SOL is the coin that happened to work in train), and in test it equals BTC alone (35%).
- Win rule reference (not a Round 7 selection): BTC alone with the bot rule and BTC filter meets rule (a) on test (35% CAGR, maxDD -12%) and rule (b) on test (beats buy-and-hold on CAGR and drawdown);
  on validation it misses (a) (maxDD -23%) and (b) (buy-and-hold made 110%).
- Verdict: neither option finds a rule for adding coins to the bot. What holds up is BTC (and SOL) alone.
- Caveats: only ~15 train and 7 validation quarters, so weak power; overlapping trailing windows; the admission script printed the test split in the same table as validation, so the test window was
  seen at the same time and not held back (the result is negative either way, so no decision depends on it); the trait table also printed test-period correlations, which were not used.
