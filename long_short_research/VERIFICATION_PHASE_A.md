# Phase A — Top-down edge check, point-in-time top 10, daily

Run: `python sanity.py`, then `python run_layers.py` (from `long_short_research/`, with `../.venv`).

## Engine sanity: random, peek, delisting
- Universe: top 10 Binance spot USDT pairs by 180-day median dollar volume, ≥ 180 days listed. 57 coins were ever
  in it (incl. delisted BCC, BCHABC, BTT, LUNA, FTM, MATIC and memecoins PEPE, BONK, WIF, TRUMP, NEIRO, 1000SATS).
- Known answer: BTC 20-day forward return matches a hand calculation. Delisted coins exit at their last close.
- Random 50% signal: lift 0.000 long / -0.001 short, p_shift ≈ 0.5 → fail (correct).
- Peeking signal (sign of the future return): lift huge, 22/22 and 25/25 coins, 5/5 years → pass (correct).
- **Drift baseline (train 2018–2022, 20-day hold, 0.2% round trip):** long PF 1.24 (mean +2.0%), short PF 0.77
  (mean -2.4%). A short signal must turn a losing population into a winning one.
- Bug fixed: PF with no losing samples returned NaN instead of infinity.
