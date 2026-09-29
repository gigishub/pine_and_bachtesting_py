# Edge search — Phase A: ten pre-declared ideas on the point-in-time top-10, daily

Setup as in `PLAN.md`: top-10 by 180d dollar volume incl. delisted, cost 0.15% per side of turnover,
train → 2022-12-31, validation 2023-01-01 → 2024-09-30, test not touched. Code: `engine.py`, `ideas.py`, `run_split.py`.

## Engine sanity: buy-and-hold, peeking, random weights
- BTC buy-and-hold in the engine = raw price move on train (1.206 vs 1.206).
- Peeking at tomorrow's return: CAGR 38,852%, max DD -0.2% (engine can see an edge when one exists).
- 40 random sticky-position portfolios: 0 passed the time-shift test at p ≤ 0.05 (about 2 expected; no false edge).

## Train: A, B, E, H pass all gates; C, D, F, G, I, J rejected
Benchmarks on train: BTC buy-and-hold CAGR 3.8% / max DD -81%; equal-weight top-10 CAGR -11% / DD -91%.

| idea | CAGR% | maxDD% | calmar | shift_p | variants (k0.5 / k2) CAGR% | verdict |
|---|---|---|---|---|---|---|
| A BTC trend (control) | 34.3 | -48.1 | 0.71 | 0.05 | 32.7 / 57.0 | pass |
| B cross-sectional momentum, BTC filter | 66.7 | -55.4 | 1.20 | 0.04 | 66.4 / 70.7 | pass |
| C time-series momentum basket | 15.5 | -70.2 | 0.22 | 0.45 | 33.0 / 14.9 | reject (not better than time-shifts) |
| D C with inverse-vol + vol target | 0.9 | -56.8 | 0.02 | 0.70 | 7.2 / 8.5 | reject |
| E low-vol tilt, BTC filter | 58.6 | -37.6 | 1.56 | 0.01 | 49.0 / 80.0 | pass |
| F pullback in uptrend RSI(2) | 4.3 | -25.2 | 0.17 | 0.42 | 0.1 / 7.7 | reject |
| G squeeze breakout | 15.8 | -36.7 | 0.43 | 0.14 | 15.7 / 21.9 | reject |
| H long/short momentum | 29.5 | -32.5 | 0.91 | 0.03 | 29.2 / 16.3 | pass |
| I breadth regime | 30.7 | -48.6 | 0.63 | 0.10 | 48.4 / 21.5 | reject |
| J risk-managed EW beta | 19.7 | -27.9 | 0.71 | 0.07 | 18.2 / 39.3 | reject |

Caveats: train contains the 2018 crash, so "beats buy-and-hold" is easy on train; the BTC filter in A, B, E was found
on this same period in earlier arcs (`../swing_research`), so train passes for those are not fully clean.
A's shift p is 0.05, on the line.

## Validation: nothing survives; B loses money, all trail buy-and-hold
Benchmarks on validation: BTC buy-and-hold CAGR 115% / max DD -26%; equal-weight top-10 CAGR 53% / DD -47%.

| idea | CAGR% | maxDD% | calmar | shift_p | k0.5 / k2 CAGR% | win (a) 20%/20% | win (b) beats B&H |
|---|---|---|---|---|---|---|---|
| A | 19.1 | -33.6 | 0.57 | 0.89 | 17.9 / 29.3 | no | no |
| B | -4.9 | -54.5 | -0.09 | 0.91 | -10.5 / 12.6 | no | no |
| E | 13.3 | -48.9 | 0.27 | 0.88 | 6.0 / 27.0 | no | no |
| H | 2.7 | -26.4 | 0.10 | 0.44 | -8.4 / 8.5 | no | no |

Validation was a strong bull, so trend/filter strategies that sit in cash part of the time were always going to lag.
Even so, none has a max drawdown under 20% (best -26%), and every time-shift p is high: the train edge was not
timing skill. B's +67% train CAGR turned into -5%: the classic sign of a train fit.
Per the rules, none goes to test. Test is untouched.

## Verdict for the ten ideas (daily, top-10, costs 0.15%/side)
No idea meets the win condition on validation. Test was not run.

## Capture ratios: trend ideas protect in real bear markets but validation had no crash to protect against
Method (`capture.py`): non-overlapping 30-day blocks, strategy block return vs BTC buy-and-hold block return, train and validation only.
Train has 31 BTC-up blocks (avg +21%) and 30 BTC-down blocks (avg -16%, worst -41%). Validation has 14 up (avg +15%) and 8 down (avg -6%, worst -11%).

| idea | train up / down capture % | validation up / down capture % |
|---|---|---|
| A BTC trend | 53 / 27 | 52 / 125 |
| B momentum | 72 / 22 | 41 / 144 |
| E low-vol | 66 / 24 | 49 / 116 |
| C, I | 52 / 37, 63 / 40 | 39 / 92, 44 / 92 |
| H long/short | 18 / -10 | -5 / -37 |
| F, G | 10 / 8, 26 / 16 | 11 / 18, 10 / -5 |

- Train: A, B, E keep 53–72% of BTC's upside and take only 22–27% of the downside. That is the asymmetry the win condition asks for, but no train block with BTC down was positive for them (0–7% of down blocks).
- Validation: the same ideas take 116–144% of the downside and only 41–52% of the upside. There was no crash (worst BTC block -11%); the down blocks were shallow dips inside a bull market, and slow filters (SMA200, 60d momentum) exit after the dip and re-enter late, so they pay for the dip and miss the rebound.
- H is the only idea with negative down capture (positive in 5 of 8 down blocks on validation) but it gives up the upside (-5%).
- Reading: slow trend filters help in long bear markets and hurt in choppy bull markets. Validation cannot confirm or refute crash protection because it holds no crash. Test (since 2024-10) is untouched and may.
