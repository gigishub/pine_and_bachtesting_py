# Phase B — momentum rotation, point-in-time universe with delisted coins

Data: Binance spot daily candles for every USDT pair (478 listed + 192 delisted, `binance_universe.py`),
2018-01-01 → 2026-09-27. Stablecoins, fiat, leveraged tokens and wrapped BTC/ETH removed. A symbol with a
>7-day data gap is split into separate coins (e.g. old LUNA ends 2022-05-13 at ~0; new LUNA starts 2022-05-31).
Engine: `rotation_pit.py`. Decide on close, trade next open, holdings drift between rebalances, 0.15% per side
(fee + slippage), a coin that stops trading is sold at its last close. Study: `rotation_study.py`.
Engine checks: BTC buy & hold through the engine = price ratio minus one fee (exact); synthetic delisting test
exits at the last close; BTC-timed yearly returns recomputed independently (2024: engine +22%, independent +17%).

## Universe with delisted coins LUNA FTT EOS MATIC
267 coins were in the top-30-by-volume universe at some point since 2018; 66 of them no longer trade.
The Phase A test only had coins that survived to 2026.

## Rotation top 30 by 30d volume fails
Supersedes: [Phase A: Momentum rotation survivorship bias](VERIFICATION_PHASE_A.md#momentum-rotation-survivorship-bias)
30d lookback, top 3, weekly, BTC filter: +14%/yr train, -46%/yr test, max DD -98%.
All profit is from 2020–2021 (+559%, +794%); every other year negative.
- Median pick had already risen 84% in 30 days; 43% of picks were up >100%. Median next-week return -2.3%.
  Volume ranking admits coins because they are pumping (LOOM, SYN, TUT, LAYER pump-and-dumps).
- vs 100 random picks from the same universe: beats 81% (train) but only 14% (test).
- Same rules on each of the 7 weekdays: full-period CAGR -8% to +22%. The result is mostly timing luck.
- 150-setting grid (lookback 7–90, top 1–10, universe 10–50, volume window 30/180d): only 19% of settings
  beat simply holding BTC with the same filter (+29%/yr, max DD -67%) over the full period.

## Rotation stable universe top 10 by 180d volume
Top 10 coins by 180-day median dollar volume ≈ large caps, point in time. 30d lookback, top 3, BTC filter.
Universe choice made after seeing the grid (180d beat 30d at every universe size), so treat as best case.
- Momentum beats random picks from the same 10: 86% (train), 98% (test), 98% (full). Selection is real here.
- Full period: +33%/yr, max DD -78%. BTC-only with the same filter: +31%/yr, max DD -63%.
- 7 weekdays: +31% to +56%/yr, max DD -58% to -80%. Always ≥ BTC-only in return, worse drawdown in 6 of 7.
- Verdict: about the same return as timed BTC for more risk. Not a clear improvement on its own.
