# Bear Strategy — Step 3: Trigger Volume Confirmation  (entry_tf=15m)

## Test Parameters

| Parameter | Value |
|-----------|-------|
| `entry_tf` | `15m` |
| `stop_atr_mult` | `2.0` |
| `target_atr_mult` | `3.0` |
| `atr_period` | `7` |
| `volume_window` | `20` |
| `volume_mult` | `1.2` |

```text

── Per-Pair Results ──

  BTCUSDT
                   wr_%     pf   dur  n_trades
population                                    
all_regime        42.67  1.116  21.1     94176
volume_triggered  43.27  1.144  27.6     24426
not_triggered     42.46  1.107  18.8     69750

  ETHUSDT
                   wr_%     pf   dur  n_trades
population                                    
all_regime        43.60  1.159  20.1     95616
volume_triggered  44.27  1.192  25.7     25006
not_triggered     43.36  1.148  18.2     70610

  SOLUSDT
                   wr_%     pf   dur  n_trades
population                                    
all_regime        43.90  1.174  20.1     89549
volume_triggered  44.58  1.207  24.6     24057
not_triggered     43.64  1.162  18.4     65492

  BNBUSDT
                   wr_%     pf   dur  n_trades
population                                    
all_regime        43.39  1.150  18.4     81006
volume_triggered  43.51  1.155  22.5     21778
not_triggered     43.34  1.148  16.9     59228

  XRPUSDT
                   wr_%     pf   dur  n_trades
population                                    
all_regime        45.23  1.239  21.8     98398
volume_triggered  45.49  1.252  27.9     25880
not_triggered     45.14  1.234  19.6     72518

── Trigger Volume Confirmation Verdict ──

  Baseline (not_triggered):  avg WR 43.6%  avg PF 1.160

  volume_triggered        avg WR lift +0.63pp  avg PF 1.190  avg PF lift +0.030  pairs ≥ threshold: 0/5  ❌  ⚠️ WR 2p
    BTCUSDT     WR 43.27%  lift +0.80pp / req 0.79pp  PF 1.144  lift +0.037 / req 0.050  trades 24,426  ❌
    ETHUSDT     WR 44.27%  lift +0.92pp / req 0.78pp  PF 1.192  lift +0.044 / req 0.050  trades 25,006  ❌
    SOLUSDT     WR 44.58%  lift +0.94pp / req 0.80pp  PF 1.207  lift +0.045 / req 0.050  trades 24,057  ❌
    BNBUSDT     WR 43.51%  lift +0.16pp / req 0.84pp  PF 1.155  lift +0.008 / req 0.050  trades 21,778  ⚠️ WR  ❌
    XRPUSDT     WR 45.49%  lift +0.34pp / req 0.77pp  PF 1.252  lift +0.017 / req 0.050  trades 25,880  ⚠️ WR  ❌

  Thresholds: WR lift > 2.5×sqrt(p(1-p)/n),  PF lift > 0.02 if n>50k / 0.05 if n≥10k / 0.10 if n<10k,  consistent across ≥ 3 pairs

  ❌  VOLUME TRIGGER NOT CONFIRMED — does not clear all thresholds.
      Consider:
        • Adjusting volume_mult (try 1.2×, 1.5×, 2.0×)
        • Adjusting volume_window (try 10 or 50 bars)
        • Proceeding to Step 4 on raw all_regime population
```
