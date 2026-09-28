# Phase A — live bot baseline, filters, first candidates

Setup for everything below: Bybit linear perp candles, 22 coins (1d) / 20 coins (4h), train = data
start → 2024-09-30, test = 2024-10-01 → 2026-09-27. Fees 0.1% per side, signal on close, fill at next open.
Coin list was picked in 2026, so every "all coins" number has survivorship bias.

## Live bot baseline BTC SOL 22 coins
Script: `bot_baseline.py` (runs the bot's own `strategy.py`, exchange stubbed).
Checked: compounding the individual trades gives the same return as the equity curve (ADA test: -51.4% both).

| | train PF | test PF | train CAGR | test CAGR | maxDD (full) |
|---|---|---|---|---|---|
| BTC | 2.25 | 2.52 | 48% | 25% | -44% |
| SOL | 2.44 | 2.29 | 46% | 31% | -52% |
| median of 22 coins | 1.26 | 1.46 | 0% | 8% | ~-52% |

Top 5 trades are 75% (BTC) and 104% (SOL) of total profit, so exits must not cut big winners.

## Winner vs loser features at entry
Script: `trade_features.py` (620 trades, 11 coins, quartile edges from train).
Consistent in train and test: high ATR% (>8%) and BTC 20-day return < -3% mark the worst trades.
Most other features flip between train and test (noise).

## BTC trend entry filter btc_ret_20 robust
Rule: only open a new trade if BTC's 20-day return ≥ -3% (checked on the prior close).
Script: `improvements.py`, `robustness.py`.
- Beats the live bot on 19/22 coins (train) and 18/22 (test). Median CAGR 0 → 13% (train), 8 → 16% (test).
- BTC test: PF 2.52 → 4.83, maxDD -24% → -12%. SOL test: CAGR 31% → 25% (slightly worse).
- Grid lookback {10,20,30,60} × threshold {-6,-3,0,+3}%: all 16 settings improve the median coin in
  both train and test (12–19 of 22 coins each). Not a lucky parameter.

## Volatility sizing ATR drawdown
Rule: position size = min(1, 4.5% / ATR14%) chosen at entry.
Median maxDD -52% → -36% (train), -55% → -38% (test); CAGR equal or better; 18/22 coins better in test.
Combined with both filters (variant `5_both+sizing`): median maxDD -33% in both periods,
CAGR 0 → 13% (train), 8 → 16% (test). The ATR>8% filter alone was not grid-checked.

## Donchian and tsmom per coin fail in train
Script: `candidates.py`. Donchian 20/10, 55/20, 100/50 and tsmom 30/60/90 day (weekly check), 1d and 4h.
Good in test only because the test market was better (median buy&hold +3% test vs -49% train).
Train median CAGR -19% to +8%. Dropped.

## Momentum rotation survivorship bias
Weekly: hold top-k coins by lookback return, only while BTC's lookback return > 0.
- All 22 coins, 1d, 30d/top3: +50%/yr train, +228%/yr test. Test is driven by coins in the list only
  because they pumped (ZEC, HYPE, ...).
- 2021 majors only (BTC ETH SOL XRP BNB ADA AVAX LINK DOGE LTC), 1d, 30d/top3: +48%/yr train, +63%/yr test,
  maxDD -64% / -52%. 4h is similar, no advantage.
- Not better than the live bot on BTC (48%/yr, -44% DD). Main open question: does it add as a
  diversifier, and do BTC filter + vol sizing tame its drawdown?

## Trend filter vs ret20 filter supplement not replace BTC
Script: `regime_variants.py`. Slow trend EMA {240, 150, 100, none} × fast BTC ret20 ≥ -3% filter {off, on}.
- ret20 improves every EMA variant in train and test, on BTC and on the median of 22 coins.
- Replacing the EMA with ret20 alone: best BTC train CAGR (63%) but test maxDD doubles (-12% → -25%),
  and median-coin maxDD goes to -65%. The two filters do different jobs (long bear market vs short sell-off).
- EMA150+ret20 vs EMA240+ret20 on BTC: 60%/-34% vs 55%/-38% train, 27%/-12% vs 36%/-12% test — noise.
  Keep EMA240 (already live).
- Per year, EMA240+ret20 vs live on BTC: better or equal in 6 of 7 years (2024 worse: +81% vs +96%).
