# Phase C — Funding carry (long spot + short perp), Bybit

Run: `python carry_test.py`. Funding downloaded with `crypto_data/funding_downloader.py` (22 coins, 8h; BTC from
2020-03, most alts from 2021). Return per year of notional; costs 0.41% to open and close both legs (spot taker 0.1%,
perp taker 0.055%, 0.05% slippage per leg). Basis moves and liquidation risk not modelled.

## Funding carry BTC ETH: real but shrinking, about 5% a year and falling
| period | BTC always-on APR | ETH always-on APR | max DD (of the funding stream) |
|---|---|---|---|
| 2020 → 2022 | 22% | 28% | -1.7% / -2.0% |
| 2023 → 2024-09 | 10% | 10% | -0.3% |
| 2024-10 → now | 5% | 5% | -0.2% |

- Calendar years, BTC: 2021 +38%, 2022 +3%, 2023 +9%, 2024 +12%, 2025 +5%, 2026 (to Sep) +1.6%.
- Funding is mostly pinned at Bybit's 0.01% per 8h baseline (~11% APR). The 2021 bull market was the outlier;
  it decays toward zero in quiet markets. Current run rate is about 2–5% of notional.
- Costs are charged once at the very start and end of the full history, so the per-period APRs above exclude them
  (a 0.41% one-off, small against multi-year holds).
- Return on capital is lower than on notional: the perp leg needs margin, so at 1.5–2× notional as capital, recent
  return is roughly 1–3% a year.

## Funding carry alts: no better than BTC/ETH
- Equal-weight basket of the other 20 coins, always-on, no costs, survivors only: 5% / 10% / 2.5% APR in the three
  periods. Worse than BTC/ETH and more often negative (20–26% of 30-day windows in train and test). The alt
  basket also carries survivorship bias, so it is an upper bound.

## Funding carry smart filter: worse than always-on
- Hold only while trailing 7-day funding > 0.005%: BTC 16.6% / 4.5% / -1.8%, ETH 23.8% / 4.9% / -2.2% APR.
  Switching costs eat the gain and funding flips are not predictable enough. Rejected; always-on is better.

## Verdict
- Passes the "positive after costs in all three periods" bar for BTC and ETH always-on, with tiny drawdowns.
- Fails as a growth strategy: at today's funding it earns about what a savings account does, with exchange,
  liquidation and basis risk attached.
