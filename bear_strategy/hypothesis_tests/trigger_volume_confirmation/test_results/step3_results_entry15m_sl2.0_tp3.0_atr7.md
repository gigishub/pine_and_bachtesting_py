# Bear Strategy — Step 3: Trigger Volume Confirmation  (entry_tf=15m)

## Test Parameters

| Parameter | Value |
|-----------|-------|
| `entry_tf` | `15m` |
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
all_regime        42.67  1.116  21.1     94176
volume_triggered  43.39  1.150  29.2     17177
not_triggered     42.51  1.109  19.3     76999

  ETHUSDT
                   wr_%     pf   dur  n_trades
population                                    
all_regime        43.60  1.159  20.1     95616
volume_triggered  44.41  1.198  27.6     17618
not_triggered     43.41  1.151  18.5     77998

  SOLUSDT
                   wr_%     pf   dur  n_trades
population                                    
all_regime        43.90  1.174  20.1     89549
volume_triggered  44.80  1.218  26.1     16322
not_triggered     43.69  1.164  18.7     73227

  BNBUSDT
                   wr_%     pf   dur  n_trades
population                                    
all_regime        43.39  1.150  18.4     81006
volume_triggered  43.33  1.147  23.6     15819
not_triggered     43.40  1.150  17.1     65187

── Trigger Volume Confirmation Verdict ──

  Baseline (not_triggered):  avg WR 43.3%  avg PF 1.144

  volume_triggered        avg WR lift +0.73pp  avg PF 1.178  avg PF lift +0.035  pairs ≥ threshold: 1/4  ❌  ⚠️ WR 2p  ⚠️ low count 4p
    BTCUSDT     WR 43.39%  lift +0.88pp / req 0.94pp  PF 1.150  lift +0.041 / req 0.050  trades 17,177  ⚠️ WR  ❌
    ETHUSDT     WR 44.41%  lift +1.00pp / req 0.93pp  PF 1.198  lift +0.047 / req 0.050  trades 17,618  ❌
    SOLUSDT     WR 44.80%  lift +1.11pp / req 0.97pp  PF 1.218  lift +0.054 / req 0.050  trades 16,322  ✅
    BNBUSDT     WR 43.33%  lift -0.08pp / req 0.99pp  PF 1.147  lift -0.004 / req 0.050  trades 15,819  ⚠️ WR  ❌

  Thresholds: WR lift > 2.5×sqrt(p(1-p)/n),  PF lift > 0.02 if n>50k / 0.05 if n≥10k / 0.10 if n<10k,  consistent across ≥ 3 pairs

  ❌  VOLUME TRIGGER NOT CONFIRMED — does not clear all thresholds.
      Consider:
        • Adjusting volume_mult (try 1.2×, 1.5×, 2.0×)
        • Adjusting volume_window (try 10 or 50 bars)
        • Proceeding to Step 4 on raw all_regime population
```
