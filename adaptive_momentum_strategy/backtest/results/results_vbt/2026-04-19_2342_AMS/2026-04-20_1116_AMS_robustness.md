# ❌ Robustness Report — AMS

_Generated: 2026-04-20 11:28_

- Results: `/Users/andre/Documents/Python_local/pine_script/adaptive_momentum_strategy/backtest/results/results_vbt/2026-04-19_2342_AMS`
- Data period: **2022-09-12** → **2025-09-01**

## Passing Criteria
```
combo passes if:
  SQN ≥ 1.0  AND  PF ≥ 1.5  AND  trades ≥ 30
  AND  win_rate ≥ 30.0%  AND  sharpe ≥ 0.5  AND  max_dd ≤ 20.0%

symbol/TF ✅  if  pass_rate ≥ 20%  of its combos
```

## Combo Summary
- **Total combos:** 336  (6 symbols × 2 timeframes × 28 parameter sets)
- **Passing combos:** 36  (10.7% of total, with current thresholds)

## Symbol Consistency
_Combo pass rate per coin (all timeframes combined). 100% = 56 combos. Floor: ≥ 20% → ✅_

| Symbol | Pass Rate | Status |
|--------|-----------|--------|
| ADAUSDT | 14% | ❌ |
| DOGEUSDT | 17% | ❌ |
| ETHUSDT | 17% | ❌ |
| SOLUSDT | 14% | ❌ |
| TRXUSDT | 5% | ❌ |
| XRPUSDT | 19% | ❌ |

## Timeframe Consistency
_Per-coin combo pass rate per timeframe. 100% = 28 combos per coin per TF. Floor: ≥ 20% → ✅_

| Symbol | 1h | 4H |
|--------|--- | ---|
| ADAUSDT | 0% ❌ | 29% ✅ |
| DOGEUSDT | 33% ✅ | 0% ❌ |
| ETHUSDT | 0% ❌ | 33% ✅ |
| SOLUSDT | 0% ❌ | 29% ✅ |
| TRXUSDT | 10% ❌ | 0% ❌ |
| XRPUSDT | 0% ❌ | 38% ✅ |

**TF Coverage per coin:**
- ⚠️ 1/2 TFs: ADAUSDT, DOGEUSDT, ETHUSDT, SOLUSDT, XRPUSDT
- ❌ 0 TFs: TRXUSDT

## Top Toggle Frequency (top-5 combos per symbol/TF)
_Toggles that appear most in top-ranked combos are likely the most impactful filters._


### Regime
| Toggle | Count |
|--------|-------|
| use_adx | 19 |
| use_ema_ribbon | 12 |

### Risk & Exit
| Toggle | Count |
|--------|-------|
| use_trailing_stop | 20 |
| use_psar | 14 |
| use_chandelier | 13 |

## Toggle Importance (RandomForest)
_Target: `SQN` | OOB R²: -0.132 | Trained on 216 combos._


### Regime
| Toggle | Importance |
|--------|-----------|
| use_adx | 0.2209 |
| use_ema_ribbon | 0.1876 |

### Risk & Exit
| Toggle | Importance |
|--------|-----------|
| use_chandelier | 0.2488 |
| use_psar | 0.1940 |
| use_trailing_stop | 0.1487 |

## Toggle Impact (SHAP)
_Target: `SQN` | n=216 combos._

_+ = toggle ON raises SQN.  − = toggle ON lowers SQN._


### Regime
| Toggle | Mean SHAP | Direction |
|--------|-----------|-----------|
| use_adx | -0.0486 | ↓ |
| use_ema_ribbon | 0.0085 | ↑ |

### Risk & Exit
| Toggle | Mean SHAP | Direction |
|--------|-----------|-----------|
| use_chandelier | -0.0587 | ↓ |
| use_psar | 0.0114 | ↑ |
| use_trailing_stop | -0.0120 | ↓ |

## Toggle Consensus
_Freq = % of top combos this toggle is ON.  OLS Coeff = avg SQN change when ON.  SHAP Mean = RF-predicted SQN impact._


### Regime
| Toggle | Freq | OLS Coeff | OLS Sig | SHAP Mean | Consensus |
|--------|------|-----------|---------|-----------|-----------|
| use_adx | 70% | -0.15 | ⚠️ | -0.05 | ⚠️ Present in top combos but signals say it hurts |
| use_ema_ribbon | 44% | 0.01 | ⚠️ | 0.01 | — Neutral |

### Risk & Exit
| Toggle | Freq | OLS Coeff | OLS Sig | SHAP Mean | Consensus |
|--------|------|-----------|---------|-----------|-----------|
| use_trailing_stop | 74% | -0.06 | ⚠️ | -0.01 | — Neutral |
| use_psar | 52% | 0.02 | ⚠️ | 0.01 | — Neutral |
| use_chandelier | 48% | -0.21 | ✅ | -0.06 | ⚠️ Present in top combos but signals say it hurts |

## Toggle Significance (OLS)
_Target: `SQN` | R²: 0.043 | n=216 combos._

_coeff > 0 → ON raises SQN.  ✅ p < 0.05 = real effect._


### Regime
| Toggle | Coefficient | p-value | Significant |
|--------|-------------|---------|-------------|
| use_adx | -0.15 | 0.1012 | ⚠️ |
| use_ema_ribbon | 0.01 | 0.9016 | ⚠️ |

### Risk & Exit
| Toggle | Coefficient | p-value | Significant |
|--------|-------------|---------|-------------|
| use_chandelier | -0.21 | 0.0240 | ✅ |
| use_trailing_stop | -0.06 | 0.5103 | ⚠️ |
| use_psar | 0.02 | 0.7408 | ⚠️ |

## Threshold Sweep
_Symbol Pass Rate = % of 6 coins where ≥ 20% of the coin's 56 combos (all 2 TFs pooled) pass the threshold.  ◀ current = value active when this report was saved._


### Sweep — Min SQN
| Min SQN | Symbol pass rate | |
|---|---|---|
| 0.5 | 50% | |
| 0.607 | 33% | |
| 0.714 | 33% | |
| 0.821 | 17% | |
| 0.929 | 17% | |
| 1.04 | 0% | ◀ current |
| 1.14 | 0% | |
| 1.25 | 0% | |
| 1.36 | 0% | |
| 1.46 | 0% | |
| 1.57 | 0% | |
| 1.68 | 0% | |
| 1.79 | 0% | |
| 1.89 | 0% | |
| 2 | 0% | |

### Sweep — Min Profit Factor
| Min Profit Factor | Symbol pass rate | |
|---|---|---|
| 1.2 | 50% | |
| 1.33 | 50% | |
| 1.46 | 0% | ◀ current |
| 1.59 | 0% | |
| 1.71 | 0% | |
| 1.84 | 0% | |
| 1.97 | 0% | |
| 2.1 | 0% | |
| 2.23 | 0% | |
| 2.36 | 0% | |
| 2.49 | 0% | |
| 2.61 | 0% | |
| 2.74 | 0% | |
| 2.87 | 0% | |
| 3 | 0% | |

### Sweep — Min # Trades
| Min # Trades | Symbol pass rate | |
|---|---|---|
| 5 | 67% | |
| 7.5 | 67% | |
| 10 | 67% | |
| 12.5 | 67% | |
| 15 | 67% | |
| 17.5 | 67% | |
| 20 | 67% | |
| 22.5 | 50% | |
| 25 | 33% | |
| 27.5 | 33% | |
| 30 | 0% | ◀ current |
| 32.5 | 0% | |
| 35 | 0% | |
| 37.5 | 0% | |
| 40 | 0% | |