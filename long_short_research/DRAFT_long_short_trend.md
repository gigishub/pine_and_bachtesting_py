# DRAFT — Long/short trend-following search (prompt)

Paste this into a new session, or say: "Follow long_short_research/DRAFT_long_short_trend.md".

---

## Task

Find a trend-following strategy that makes money on the way **up (long)** and on the way **down (short)**,
on **daily or 4h** candles, on the **largest crypto coins**. Prove it has an edge on training data, then
confirm it on data it has never seen. Stop when one strategy passes every check below, or when the evidence
says no such strategy exists here. Both outcomes are fine; a clear "no" is a result.

Follow `CLAUDE.md` (restate the task back first, checkpoints, stop after ~2 failed attempts, PLAN/VERIFICATION
docs, commit only when a milestone ticks, never push).

## Read first

1. `../swing_research/VERIFICATION_INDEX.md` (Current truths), then `VERIFICATION_PHASE_A.md` and `_B.md` there.
2. Reuse, don't rebuild (import from `../swing_research/`): `rotation_pit.py` (point-in-time universe, delisting handling, day-by-day engine),
   `common.py` (metrics), `binance_universe.py` (downloader pattern), `../crypto_data/` (Bybit funding rates).

## Lessons already paid for (do not repeat)

- **Survivorship bias.** A coin list picked today inflated results from +14% to +228%/yr. Use a
  point-in-time universe that includes delisted coins. Large caps = top 10 by 180-day median dollar volume.
- **Ticker reuse.** Split a symbol at data gaps > 7 days (old LUNA vs new LUNA).
- **Timing luck.** One weekly rotation swung between -8% and +22%/yr depending on the rebalance weekday.
  Every result must hold across bar/weekday offsets.
- **A good test period can flatter.** Per-coin trend rules looked great in test only because the test market
  was kinder. Always compare with buy & hold of the same coins in the same period.
- **Pumps.** Ranking by recent volume or return picks pump-and-dumps. Prefer slow, stable universes.
- **The existing edge.** The BTC trend filter (EMA240 + 20-day return ≥ -3%) is what works now. It is the
  benchmark to beat, not something to rediscover.

## Data

- Shorting needs perpetual futures. Use **Binance USD-M futures** from the public archive
  (`data.binance.vision/data/futures/um/monthly/klines/` and `.../fundingRate/`), including delisted
  contracts. If that archive is not enough, fall back to Bybit linear (`../crypto_data/`).
- Daily and 4h klines, plus funding rates, for every USDT perpetual that was ever in the large-cap universe.
- Sample: from the earliest perp data (~2019/2020) to now.

## Test rules (fixed before any test)

- **Three periods:** tune on **train** (start → 2022-12-31), choose on **validation** (2023-01-01 → 2024-09-30),
  and run **test** (2024-10-01 → now) **once per finalist**. The test period has been looked at in earlier
  phases, so the real final check is a **paper-trading holdout** from the day the rules are frozen.
- Decide on the closed bar, fill at the next bar's open. Never use an unclosed candle.
- Costs per side: 0.05% taker fee + 0.05% slippage. **Funding is paid or received every 8h** on the open
  position (longs pay positive funding, shorts receive it). Report results with and without funding.
- A position in a contract that stops trading is closed at its last price.
- Check the engine with known answers before trusting it: buy & hold through the engine = price ratio minus
  fees; a synthetic short on a falling series; a synthetic delisting.

## Benchmarks every candidate must be compared with

1. The current bot's long-only rule with the BTC filter, on the same coins (the bar to beat).
2. Buy & hold of the same coins, equal weight.
3. The candidate's **long side alone** and **short side alone**. The short side must earn its place:
   positive net of fees and funding on its own, and it must improve the combined result.
4. Random entries with the same number of trades, holding time and long/short mix (≥ 100 runs).
   The candidate must beat ≥ 95% of them.

## Candidate families (start simple; add a family only when the previous one is understood)

- Price vs a slow moving average: long above, short below (optionally flat in a neutral band).
- Donchian breakout in both directions (N-bar high → long, N-bar low → short), exit on the opposite M-bar extreme.
- Time-series momentum sign: long if the N-day return > 0, short if < 0, checked on a slow schedule.
- ATR trailing stop / Supertrend-style: flip long/short when price crosses the trailing line.
- **Asymmetric rules.** Crypto drifts up, so shorts may need a stricter regime (e.g. short only while BTC is
  below its EMA240 and its 20-day return is negative). Test symmetric and asymmetric versions.
- On-chain exchange flows (BTC/ETH only): see `DRAFT_onchain_data.md`. Test only after a price-only
  family is understood, as a filter on top of it, not as a standalone signal.
- Sizing: equal weight vs volatility targeting (size ∝ 1/ATR%). Volatility targeting cut drawdowns about
  15 points in Phase A.
- 1d vs 4h: 4h added nothing for long-only; check whether it helps the short side (crashes are fast).

## Pass criteria (all must hold)

- Better **Sharpe and a smaller max drawdown** than benchmark 1, in validation **and** test.
- Positive net of costs and funding on **≥ 7 of 10** coins in validation and in test.
- **≥ 70% of neighbouring parameter settings** are also positive in validation (no single lucky setting).
- Holds across bar/weekday offsets and at **2× costs**.
- Per-year table: no single year delivers most of the profit.
- Short side alone is positive net of funding in validation and test.

## Output

- All docs and code for this arc live in `long_short_research/`.
- `PLAN.md` for this arc (Start / Goal / Done when, milestones that grow as you learn).
- `VERIFICATION_INDEX.md` + `VERIFICATION_PHASE_A.md` (and later letters) in this folder: one header per finding with searchable terms; update
  **Current truths** in this folder's `VERIFICATION_INDEX.md`; mark overridden findings with `Supersedes` /
  `Superseded by`.
- For every candidate, a one-line verdict: pass / fail, and why.
- For a winner: the exact rules, parameters, expected return / drawdown / trades per year, and the stop
  criteria for live use, written before any live money.
