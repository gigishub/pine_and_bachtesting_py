# Bear Strategy — RVOL Setup Edge Check  (entry_tf=15m)

## Test Parameters

| Parameter | Value |
|-----------|-------|
| `entry_tf` | `15m` |
| `stop_atr_mult` | `2.0` |
| `target_atr_mult` | `3.0` |
| `atr_period` | `7` |
| `rvol_threshold` | `1.2` |
| `vol_ma_len` | `20` |
| `min_bars_active` | `1` |

```text

── Per-Pair Results ──

  BTCUSDT
                     wr_%     pf   dur  n_trades
population                                      
regime_only         42.67  1.116  21.1     94176
rvol_spike          43.38  1.149  27.4     24108
rvol_spike_bearish  42.65  1.116  25.9     12430
rvol_spike_down     42.65  1.116  25.9     12430
    rvol_spike covers 25.6% of regime bars  
    rvol_spike_bearish covers 13.2% of regime bars  ⚠️  LOW
    rvol_spike_down covers 13.2% of regime bars  ⚠️  LOW

  ETHUSDT
                     wr_%     pf   dur  n_trades
population                                      
regime_only         43.60  1.159  20.1     95616
rvol_spike          44.28  1.192  25.6     24676
rvol_spike_bearish  44.67  1.211  24.5     12940
rvol_spike_down     44.67  1.211  24.5     12940
    rvol_spike covers 25.8% of regime bars  
    rvol_spike_bearish covers 13.5% of regime bars  ⚠️  LOW
    rvol_spike_down covers 13.5% of regime bars  ⚠️  LOW

  SOLUSDT
                     wr_%     pf   dur  n_trades
population                                      
regime_only         43.90  1.174  20.1     89549
rvol_spike          44.65  1.210  24.6     23685
rvol_spike_bearish  44.56  1.206  23.6     12422
rvol_spike_down     44.56  1.206  23.6     12422
    rvol_spike covers 26.4% of regime bars  
    rvol_spike_bearish covers 13.9% of regime bars  ⚠️  LOW
    rvol_spike_down covers 13.9% of regime bars  ⚠️  LOW

  BNBUSDT
                     wr_%     pf   dur  n_trades
population                                      
regime_only         43.39  1.150  18.4     81006
rvol_spike          43.39  1.150  22.4     21591
rvol_spike_bearish  43.34  1.147  22.3     10946
rvol_spike_down     43.34  1.147  22.3     10946
    rvol_spike covers 26.7% of regime bars  
    rvol_spike_bearish covers 13.5% of regime bars  ⚠️  LOW
    rvol_spike_down covers 13.5% of regime bars  ⚠️  LOW

  XRPUSDT
                     wr_%     pf   dur  n_trades
population                                      
regime_only         45.23  1.239  21.8     98398
rvol_spike          45.42  1.248  27.7     25566
rvol_spike_bearish  45.40  1.247  26.4     13643
rvol_spike_down     45.40  1.247  26.4     13643
    rvol_spike covers 26.0% of regime bars  
    rvol_spike_bearish covers 13.9% of regime bars  ⚠️  LOW
    rvol_spike_down covers 13.9% of regime bars  ⚠️  LOW

── RVOL Setup Edge Verdict ──

  Baseline (regime_only):  avg WR 43.8%  avg PF 1.168
  RVOL config: threshold=1.2×  vol_ma_len=20  min_bars_active=1

  rvol_spike              avg WR lift +0.47pp  avg PF 1.190  avg PF lift +0.022  pairs ≥ threshold: 0/5  ❌  ⚠️ WR 5p  ⚠️ low count 5p
    BTCUSDT     WR 43.38%  lift +0.71pp / req 0.80pp  PF 1.149  lift +0.033 / req 0.050  trades 24,108  cov 25.6%  ⚠️ WR  ❌
    ETHUSDT     WR 44.28%  lift +0.68pp / req 0.79pp  PF 1.192  lift +0.033 / req 0.050  trades 24,676  cov 25.8%  ⚠️ WR  ❌
    SOLUSDT     WR 44.65%  lift +0.75pp / req 0.81pp  PF 1.210  lift +0.036 / req 0.050  trades 23,685  cov 26.4%  ⚠️ WR  ❌
    BNBUSDT     WR 43.39%  lift +0.00pp / req 0.84pp  PF 1.150  lift +0.000 / req 0.050  trades 21,591  cov 26.7%  ⚠️ WR  ❌
    XRPUSDT     WR 45.42%  lift +0.19pp / req 0.78pp  PF 1.248  lift +0.010 / req 0.050  trades 25,566  cov 26.0%  ⚠️ WR  ❌

  rvol_spike_bearish      avg WR lift +0.37pp  avg PF 1.185  avg PF lift +0.018  pairs ≥ threshold: 1/5  ❌  ⚠️ WR 5p  ⚠️ low count 5p
    BTCUSDT     WR 42.65%  lift -0.02pp / req 1.11pp  PF 1.116  lift -0.001 / req 0.050  trades 12,430  cov 13.2% ⚠️  ⚠️ WR  ❌
    ETHUSDT     WR 44.67%  lift +1.07pp / req 1.09pp  PF 1.211  lift +0.051 / req 0.050  trades 12,940  cov 13.5% ⚠️  ⚠️ WR  ✅
    SOLUSDT     WR 44.56%  lift +0.66pp / req 1.11pp  PF 1.206  lift +0.032 / req 0.050  trades 12,422  cov 13.9% ⚠️  ⚠️ WR  ❌
    BNBUSDT     WR 43.34%  lift -0.05pp / req 1.18pp  PF 1.147  lift -0.002 / req 0.050  trades 10,946  cov 13.5% ⚠️  ⚠️ WR  ❌
    XRPUSDT     WR 45.40%  lift +0.17pp / req 1.07pp  PF 1.247  lift +0.008 / req 0.050  trades 13,643  cov 13.9% ⚠️  ⚠️ WR  ❌

  rvol_spike_down         avg WR lift +0.37pp  avg PF 1.185  avg PF lift +0.018  pairs ≥ threshold: 1/5  ❌  ⚠️ WR 5p  ⚠️ low count 5p
    BTCUSDT     WR 42.65%  lift -0.02pp / req 1.11pp  PF 1.116  lift -0.001 / req 0.050  trades 12,430  cov 13.2% ⚠️  ⚠️ WR  ❌
    ETHUSDT     WR 44.67%  lift +1.07pp / req 1.09pp  PF 1.211  lift +0.051 / req 0.050  trades 12,940  cov 13.5% ⚠️  ⚠️ WR  ✅
    SOLUSDT     WR 44.56%  lift +0.66pp / req 1.11pp  PF 1.206  lift +0.032 / req 0.050  trades 12,422  cov 13.9% ⚠️  ⚠️ WR  ❌
    BNBUSDT     WR 43.34%  lift -0.05pp / req 1.18pp  PF 1.147  lift -0.002 / req 0.050  trades 10,946  cov 13.5% ⚠️  ⚠️ WR  ❌
    XRPUSDT     WR 45.40%  lift +0.17pp / req 1.07pp  PF 1.247  lift +0.008 / req 0.050  trades 13,643  cov 13.9% ⚠️  ⚠️ WR  ❌

  Thresholds: WR lift > 2.5×sqrt(p(1-p)/n),  PF lift > 0.02/0.05/0.10 by n,  consistent across ≥ 4 of 5 pairs

  ❌  RVOL EDGE NOT CONFIRMED — no population clears all thresholds.
      Next steps:
        • Increase min_bars_active (reduces noise on lower TF)
        • Try rvol_threshold = 2.0 (stricter spike definition)
        • Try vol_ma_len = 10 or 50
        • Try a different entry_tf in config.py
        • Re-examine whether setup layer is needed before trigger layer
```
