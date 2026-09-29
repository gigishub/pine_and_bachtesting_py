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

## Bot settings tune: exits, earlier entries, longer holds — no variant beats the live settings
Script `bot_tune.py`. Live bot rules on 22 coins (1d), BTC 20-day filter on all coins, one setting changed at a time (14 variants, none tuned further).
Median-coin CAGR train / test: live 13.3 / 15.9%. Every variant is lower in both periods (best: ema_trend=100 test 20.1 but train -0.2; trail_lookback=14 10.0 / 11.7).
- Slower stop (trail_lookback 14–21): median maxDD improves ~5–9 points (-49 → -40/-44) but return falls; BTC test CAGR 36 → 26 at 21.
- Earlier entry (ema_fast 3/5, ema_trend 100/150, no vol-spike filter): more coins win in train, median return falls, drawdown does not improve.
- Live settings are a local optimum on the median coin, and were fit on this data, so the ranking is if anything flattering to them.

## Hourly phase test: the live rule shifted by 0–23 hours; UTC midnight is at or near the best phase for BTC and SOL
Script `bot_hourly_size.py`, 13 coins with 1h data, BTC 20-day filter on, 0.1% fee. Same daily rule run on 24-hour-offset daily candles; "ens24" = average of the 24 phases (a bot that checks every hour with 1/24 tranches).
- Median coin CAGR train / test: live (00:00 UTC) 15.6 / 16.6%, ens24 9.8 / 7.8%. Checking hourly / entering earlier on average is worse, not better.
- Phase spread is large: BTC train 37–58%, test 10–35%; SOL train 36–62%, test -3 to 25%. The live phase gives BTC test 34.9% (= the best phase) and SOL 23.3%, while the 24-phase average gives 19.4% / 11.4%. Expect less than the backtest.

## Volatility sizing at entry (min(1, 4.5%/ATR14%)), daily bot, all coins, BTC filter on
Median CAGR train / test: 13.3 / 15.9% → 13.4 / 14.1%; median maxDD -49 / -49% → -35 / -35%. SOL maxDD -41 → -30 (train), -26 → -21 (test); BTC maxDD -38 → -32 (train), -12 → -12 (test), CAGR -1 to -2 points.
