# DRAFT — On-chain "big money" data: can we get it, can we trust it in a backtest?

Idea: large holders moving coins **onto** exchanges (to sell) or **off** exchanges (to hold) may lead price.
Use it as a filter on a price-based long/short rule, e.g. block longs while exchange inflows spike.

## What is available for free (checked by querying the APIs)

| Source | What | Coins | History | Cost |
|---|---|---|---|---|
| Coin Metrics Community API (`community-api.coinmetrics.io/v4`, no key, 10 req / 6 s) | `FlowInExNtv`, `FlowOutExNtv`, `SplyExNtv` (+ USD versions): daily flows into/out of exchanges, coins held on exchanges | **BTC, ETH only** | BTC 2011+, ETH 2015+ | free, CC BY-NC |
| same | `CapMVRVCur` (market cap / realized cap, a valuation gauge) | BTC, ETH, ... | 2010+ | free |
| same | `SplyCur` for USDT / USDC (stablecoin supply = cash waiting to buy) | stablecoins | 2014+ / 2018+ | free |
| Binance archive `data.binance.vision/data/futures/um/daily/metrics/` | open interest, top-trader long/short ratio, taker buy/sell ratio (not on-chain, but "big money" positioning) | every USDT perp | 2022-01 confirmed; exact start not checked | free |

Not free: whale-cohort metrics (`AdrBalNtv10KCnt`, `SplyAdrTop1Pct`), adjusted transfer volume, NVT (Coin Metrics
returns "forbidden"). Glassnode, CryptoQuant and Whale Alert history are paid. Raw chains (Google BigQuery public
datasets, Dune) are free-ish, but then we would have to label exchange wallets ourselves. That is a project on its own.

## The big catch: look-ahead bias in exchange flows

Exchange flows depend on knowing which addresses belong to exchanges. Providers add labels over time and
**recompute the whole history**. Checked: BTC `FlowInExNtv` for 2020-03-10 has status-time 2026-04-09, so it was
recomputed six years later with today's labels. A backtest on this series uses knowledge nobody had in 2020.
Point-in-time (unrevised) versions are paid products.

So a backtest on these flows will look **better than the signal was live**. The only honest test is paper trading
forward, which is what the long/short draft already asks for as the final holdout.

## What the evidence says

- Per-transaction whale alerts: about coin-flip for direction. They relate more to **volatility** and jumps
  (arXiv 2211.08281; Scaillet et al.) than to direction.
- Aggregate exchange netflow and reserves: widely cited, mostly anecdotal ("outflows up 40%, then BTC +28%").
  No convincing out-of-sample direction edge found.

## Verdict

- **Feasible:** yes, for BTC and ETH daily, free, back to before the perp data starts.
- **Worth it:** only as a cheap add-on test. Because of the hindsight labels, a backtest pass is weak evidence.
  A backtest fail is strong evidence. Most useful on the **short side**: BTC is the regime filter, and inflow spikes
  in crashes are the plausible mechanism.
- **Order:** after a price-only long/short family is understood. Test one or two simple filters (e.g. 7-day
  netflow z-score > 2 blocks longs / allows shorts), with the same pass criteria as everything else.
- Binance positioning metrics (open interest, long/short ratio) have no labelling problem and cover every coin.
  They may be the better "big money" signal to try first.
