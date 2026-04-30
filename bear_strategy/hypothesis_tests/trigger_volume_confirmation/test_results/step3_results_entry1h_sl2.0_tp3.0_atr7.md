# Bear Strategy — Step 3: Trigger Volume Confirmation  (entry_tf=1h)

## Test Parameters

| Parameter | Value |
|-----------|-------|
| `entry_tf` | `1h` |
| `stop_atr_mult` | `2.0` |
| `target_atr_mult` | `3.0` |
| `atr_period` | `7` |
| `volume_window` | `20` |
| `volume_mult` | `1.5` |

```text

── Per-Pair Results ──

  BTCUSDT
                   wr_%     pf   dur  n_trades
population                                    
all_regime        44.25  1.191  20.4     23544
volume_triggered  44.18  1.187  28.3      4572
not_triggered     44.27  1.192  18.5     18972

  ETHUSDT
                   wr_%     pf   dur  n_trades
population                                    
all_regime        45.01  1.228  19.9     23904
volume_triggered  45.13  1.234  29.2      4520
not_triggered     44.98  1.226  17.8     19384

  SOLUSDT
                   wr_%     pf   dur  n_trades
population                                    
all_regime        44.84  1.219  19.5     22371
volume_triggered  45.17  1.236  26.2      4120
not_triggered     44.76  1.216  18.0     18251

  BNBUSDT
                   wr_%     pf   dur  n_trades
population                                    
all_regime        44.88  1.222  19.0     20243
volume_triggered  43.85  1.171  24.9      3756
not_triggered     45.12  1.233  17.7     16487

── Trigger Volume Confirmation Verdict ──

  Baseline (not_triggered):  avg WR 44.8%  avg PF 1.217

  volume_triggered        avg WR lift -0.20pp  avg PF 1.207  avg PF lift -0.010  pairs ≥ threshold: 0/4  ❌  ⚠️ WR 4p  ⚠️ low count 4p
    BTCUSDT     WR 44.18%  lift -0.09pp / req 1.84pp  PF 1.187  lift -0.004 / req 0.100  trades 4,572  ⚠️ WR  ❌
    ETHUSDT     WR 45.13%  lift +0.15pp / req 1.85pp  PF 1.234  lift +0.008 / req 0.100  trades 4,520  ⚠️ WR  ❌
    SOLUSDT     WR 45.17%  lift +0.41pp / req 1.94pp  PF 1.236  lift +0.020 / req 0.100  trades 4,120  ⚠️ WR  ❌
    BNBUSDT     WR 43.85%  lift -1.27pp / req 2.03pp  PF 1.171  lift -0.062 / req 0.100  trades 3,756  ⚠️ WR  ❌

  Thresholds: WR lift > 2.5×sqrt(p(1-p)/n),  PF lift > 0.02 if n>50k / 0.05 if n≥10k / 0.10 if n<10k,  consistent across ≥ 3 pairs

  ❌  VOLUME TRIGGER NOT CONFIRMED — does not clear all thresholds.
      Consider:
        • Adjusting volume_mult (try 1.2×, 1.5×, 2.0×)
        • Adjusting volume_window (try 10 or 50 bars)
        • Proceeding to Step 4 on raw all_regime population
```
