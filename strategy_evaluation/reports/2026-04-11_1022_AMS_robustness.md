# ⚠️ Robustness Report — AMS

_Generated: 2026-04-11 10:22_

- Short run: `adaptive_momentum_strategy/backtest/results/results_vbt/2026-04-10_2220_AMS`
- Long run:  `adaptive_momentum_strategy/backtest/results/results_vbt/2026-04-10_2329_AMS`

## Verdict

**⚠️ MARGINAL**

- Timeframe pass rate 43% below robust threshold (60%).

## Key Metrics
- **Symbol pass rate**: 80% (8/10 symbols)
- **Timeframe pass rate**: 43%
- **Avg SQN (short run)**: 0.07
- **Avg SQN (long run)**: 1.07
- **Decay flags**: 1 symbol/TF pairs

## Symbol Consistency
| Symbol | Passes |
|--------|--------|
| ADAUSDT | ✅ |
| AVAXUSDT | ❌ |
| BNBUSDT | ✅ |
| BTCUSDT | ✅ |
| DOGEUSDT | ✅ |
| ETHUSDT | ✅ |
| LINKUSDT | ❌ |
| SOLUSDT | ✅ |
| TRXUSDT | ✅ |
| XRPUSDT | ✅ |

## Timeframe Consistency
| Timeframe | Pass Rate |
|-----------|-----------|
| 1D | 20% |
| 1h | 30% |
| 4H | 80% |

## Top Toggle Frequency (top-5 combos per symbol/TF)
_Toggles that appear most in top-ranked combos are likely the most impactful filters._

| Toggle | Count |
|--------|-------|
| use_cmf | 138 |
| use_trailing_stop | 102 |
| use_volume_profile | 97 |
| use_ema_ribbon | 85 |
| use_psar | 75 |
| use_adx | 65 |
| use_chandelier | 63 |
| use_donchian | 53 |
| use_bbands | 27 |
| use_power_candle | 12 |

## Short vs Long Decay
_Positive SQN delta = strategy holds up over longer period. Flagged rows dropped > 30 %._

| Symbol | TF | SQN Short | SQN Long | Δ SQN | Decayed |
|--------|----|-----------|----------|-------|---------|
| ADAUSDT | 1D | 0.46 | 0.51 | 0.05 | ✅ |
| ADAUSDT | 1h | -0.65 | 0.35 | 1.00 | ✅ |
| ADAUSDT | 4H | -0.03 | 1.24 | 1.27 | ✅ |
| AVAXUSDT | 1D | -0.12 | 1.08 | 1.20 | ✅ |
| AVAXUSDT | 1h | 0.46 | 0.90 | 0.44 | ✅ |
| AVAXUSDT | 4H | 1.59 | 0.88 | -0.71 | ⚠️ |
| BNBUSDT | 1D | 0.44 | 0.82 | 0.38 | ✅ |
| BNBUSDT | 1h | -2.66 | 0.18 | 2.84 | ✅ |
| BNBUSDT | 4H | 0.72 | 1.45 | 0.74 | ✅ |
| BTCUSDT | 1D | -0.29 | 2.56 | 2.85 | ✅ |
| BTCUSDT | 1h | -1.48 | 1.46 | 2.94 | ✅ |
| BTCUSDT | 4H | 0.49 | 1.09 | 0.60 | ✅ |
| DOGEUSDT | 1D | 0.44 | 0.90 | 0.46 | ✅ |
| DOGEUSDT | 1h | 0.96 | 1.72 | 0.76 | ✅ |
| DOGEUSDT | 4H | 1.92 | 1.73 | -0.18 | ✅ |
| ETHUSDT | 1D | 0.17 | 1.23 | 1.06 | ✅ |
| ETHUSDT | 1h | -0.58 | 0.75 | 1.33 | ✅ |
| ETHUSDT | 4H | 0.44 | 2.15 | 1.71 | ✅ |
| LINKUSDT | 1D | -0.71 | 1.25 | 1.96 | ✅ |
| LINKUSDT | 1h | -1.28 | -0.68 | 0.60 | ✅ |
| LINKUSDT | 4H | 0.47 | 0.52 | 0.06 | ✅ |
| SOLUSDT | 1D | — | 0.91 | — | ✅ |
| SOLUSDT | 1h | -0.33 | 1.57 | 1.91 | ✅ |
| SOLUSDT | 4H | 0.71 | 1.43 | 0.72 | ✅ |
| TRXUSDT | 1D | — | 1.67 | — | ✅ |
| TRXUSDT | 1h | -0.04 | 0.53 | 0.58 | ✅ |
| TRXUSDT | 4H | 0.66 | 1.04 | 0.38 | ✅ |
| XRPUSDT | 1D | 0.09 | 0.51 | 0.42 | ✅ |
| XRPUSDT | 1h | -0.34 | 1.12 | 1.46 | ✅ |
| XRPUSDT | 4H | 0.57 | 1.32 | 0.74 | ✅ |