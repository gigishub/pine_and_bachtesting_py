# Bear Strategy — Step 2: Setup Level Edge Check  (entry_tf=1h)

## Test Parameters

| Parameter | Value |
|-----------|-------|
| `entry_tf` | `1h` |
| `context_tf` | `1d` |
| `stop_atr_mult` | `2.0` |
| `target_atr_mult` | `3.0` |
| `atr_period` | `7` |
| `setup_distance_atr` | `0.5` |
| `vpvr_window` | `200` |

```text

── Per-Pair Results ──

  BTCUSDT
                  wr_%     pf   dur  n_trades
population                                   
all_regime       44.25  1.191  20.4     23544
near_setup       45.77  1.266  17.8      7074
away_from_setup  43.38  1.149  21.5     16350
vpvr_only        48.39  1.406  16.0      2513
vwap_only        45.71  1.263  18.7      5250

  ETHUSDT
                  wr_%     pf   dur  n_trades
population                                   
all_regime       45.01  1.228  19.9     23904
near_setup       47.42  1.353  17.8      7293
away_from_setup  43.93  1.175  20.9     16395
vpvr_only        44.81  1.218  17.9      2642
vwap_only        48.66  1.422  17.6      5316

  SOLUSDT
                  wr_%     pf   dur  n_trades
population                                   
all_regime       44.84  1.219  19.5     22371
near_setup       48.56  1.416  19.2      5805
away_from_setup  43.64  1.161  19.7     16470
vpvr_only        46.08  1.282  18.9      2435
vwap_only        49.21  1.453  18.8      4221

  BNBUSDT
                  wr_%     pf   dur  n_trades
population                                   
all_regime       44.88  1.222  19.0     20243
near_setup       49.04  1.443  18.3      5441
away_from_setup  43.46  1.153  19.3     14730
vpvr_only        50.72  1.544  18.0      1660
vwap_only        49.92  1.495  18.6      4257

  XRPUSDT
                  wr_%     pf   dur  n_trades
population                                   
all_regime       47.17  1.339  22.3     24598
near_setup       51.50  1.593  19.8      6344
away_from_setup  45.46  1.250  22.2     18182
vpvr_only        53.73  1.742  19.5      1476
vwap_only        51.94  1.621  19.5      5450

── Setup Level Edge Verdict ──

  Baseline (away_from_setup):  avg WR 44.0%  avg PF 1.178

  near_setup            avg WR lift +4.48pp  avg PF 1.414  avg PF lift +0.236  pairs ≥ threshold: 5/5  ✅
    BTCUSDT     WR 45.77%  lift +2.40pp / req 1.47pp  PF 1.266  lift +0.117 / req 0.100  trades 7,074  ✅
    ETHUSDT     WR 47.42%  lift +3.48pp / req 1.45pp  PF 1.353  lift +0.177 / req 0.100  trades 7,293  ✅
    SOLUSDT     WR 48.56%  lift +4.92pp / req 1.63pp  PF 1.416  lift +0.255 / req 0.100  trades 5,805  ✅
    BNBUSDT     WR 49.04%  lift +5.57pp / req 1.68pp  PF 1.443  lift +0.290 / req 0.100  trades 5,441  ✅
    XRPUSDT     WR 51.50%  lift +6.03pp / req 1.56pp  PF 1.593  lift +0.342 / req 0.100  trades 6,344  ✅

  vpvr_only             avg WR lift +4.77pp  avg PF 1.438  avg PF lift +0.261  pairs ≥ threshold: 4/5  ✅  ⚠️ WR 2p  ⚠️ low count 5p
    BTCUSDT     WR 48.39%  lift +5.01pp / req 2.47pp  PF 1.406  lift +0.257 / req 0.100  trades 2,513  ✅
    ETHUSDT     WR 44.81%  lift +0.88pp / req 2.41pp  PF 1.218  lift +0.043 / req 0.100  trades 2,642  ⚠️ WR  ❌
    SOLUSDT     WR 46.08%  lift +2.44pp / req 2.51pp  PF 1.282  lift +0.120 / req 0.100  trades 2,435  ⚠️ WR  ✅
    BNBUSDT     WR 50.72%  lift +7.26pp / req 3.04pp  PF 1.544  lift +0.391 / req 0.100  trades 1,660  ✅
    XRPUSDT     WR 53.73%  lift +8.26pp / req 3.24pp  PF 1.742  lift +0.491 / req 0.100  trades 1,476  ✅

  vwap_only             avg WR lift +5.12pp  avg PF 1.451  avg PF lift +0.273  pairs ≥ threshold: 5/5  ✅  ⚠️ low count 3p
    BTCUSDT     WR 45.71%  lift +2.34pp / req 1.71pp  PF 1.263  lift +0.114 / req 0.100  trades 5,250  ✅
    ETHUSDT     WR 48.66%  lift +4.73pp / req 1.70pp  PF 1.422  lift +0.247 / req 0.100  trades 5,316  ✅
    SOLUSDT     WR 49.21%  lift +5.57pp / req 1.91pp  PF 1.453  lift +0.292 / req 0.100  trades 4,221  ✅
    BNBUSDT     WR 49.92%  lift +6.46pp / req 1.90pp  PF 1.495  lift +0.342 / req 0.100  trades 4,257  ✅
    XRPUSDT     WR 51.94%  lift +6.48pp / req 1.69pp  PF 1.621  lift +0.371 / req 0.100  trades 5,450  ✅

  Thresholds: WR lift > 2.5×sqrt(p(1-p)/n),  PF lift > 0.02 if n>50k / 0.05 if n≥10k / 0.10 if n<10k,  consistent across ≥ 3 pairs

  ✅  SETUP EDGE CONFIRMED — at least one setup level creates predictive resistance.
      Best performer: vwap_only  (avg PF 1.451)
      Warnings (results valid but interpret with care):
        ⚠️  [vpvr_only] WR lift below threshold on: ETHUSDT, SOLUSDT
        ⚠️  [vpvr_only] low trade count (<30% of regime) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
        ⚠️  [vwap_only] low trade count (<30% of regime) on: SOLUSDT, BNBUSDT, XRPUSDT
      Proceed to Step 3 (trigger confirmation).

  ── Component Decision ──
      AVWAP outperforms combined → consider cutting VPVR.
```
