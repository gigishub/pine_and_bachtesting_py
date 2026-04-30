# Bear Strategy — RVOL Setup Edge Check  (entry_tf=1h)

## Test Parameters

| Parameter | Value |
|-----------|-------|
| `entry_tf` | `1h` |
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
regime_only         44.25  1.191  20.4     23544
rvol_spike          44.54  1.205  26.7      6354
rvol_spike_bearish  45.38  1.246  26.4      3391
rvol_spike_down     45.38  1.246  26.4      3391
    rvol_spike covers 27.0% of regime bars  
    rvol_spike_bearish covers 14.4% of regime bars  ⚠️  LOW
    rvol_spike_down covers 14.4% of regime bars  ⚠️  LOW

  ETHUSDT
                     wr_%     pf   dur  n_trades
population                                      
regime_only         45.01  1.228  19.9     23904
rvol_spike          45.06  1.230  26.7      6403
rvol_spike_bearish  46.14  1.285  26.5      3513
rvol_spike_down     46.14  1.285  26.5      3513
    rvol_spike covers 26.8% of regime bars  
    rvol_spike_bearish covers 14.7% of regime bars  ⚠️  LOW
    rvol_spike_down covers 14.7% of regime bars  ⚠️  LOW

  SOLUSDT
                     wr_%     pf   dur  n_trades
population                                      
regime_only         44.84  1.219  19.5     22371
rvol_spike          44.82  1.218  24.1      5951
rvol_spike_bearish  45.50  1.252  23.8      3253
rvol_spike_down     45.50  1.252  23.8      3253
    rvol_spike covers 26.6% of regime bars  
    rvol_spike_bearish covers 14.5% of regime bars  ⚠️  LOW
    rvol_spike_down covers 14.5% of regime bars  ⚠️  LOW

  BNBUSDT
                     wr_%     pf   dur  n_trades
population                                      
regime_only         44.88  1.222  19.0     20243
rvol_spike          44.31  1.194  23.4      5274
rvol_spike_bearish  44.62  1.208  22.5      2786
rvol_spike_down     44.62  1.208  22.5      2786
    rvol_spike covers 26.1% of regime bars  
    rvol_spike_bearish covers 13.8% of regime bars  ⚠️  LOW
    rvol_spike_down covers 13.8% of regime bars  ⚠️  LOW

  XRPUSDT
                     wr_%     pf   dur  n_trades
population                                      
regime_only         47.17  1.339  22.3     24598
rvol_spike          46.93  1.327  30.1      6403
rvol_spike_bearish  47.48  1.356  29.1      3578
rvol_spike_down     47.48  1.356  29.1      3578
    rvol_spike covers 26.0% of regime bars  
    rvol_spike_bearish covers 14.5% of regime bars  ⚠️  LOW
    rvol_spike_down covers 14.5% of regime bars  ⚠️  LOW

── RVOL Setup Edge Verdict ──

  Baseline (regime_only):  avg WR 45.2%  avg PF 1.240
  RVOL config: threshold=1.2×  vol_ma_len=20  min_bars_active=1

  rvol_spike              avg WR lift -0.10pp  avg PF 1.235  avg PF lift -0.005  pairs ≥ threshold: 0/5  ❌  ⚠️ WR 5p  ⚠️ low count 5p
    BTCUSDT     WR 44.54%  lift +0.29pp / req 1.56pp  PF 1.205  lift +0.014 / req 0.100  trades 6,354  cov 27.0%  ⚠️ WR  ❌
    ETHUSDT     WR 45.06%  lift +0.05pp / req 1.55pp  PF 1.230  lift +0.002 / req 0.100  trades 6,403  cov 26.8%  ⚠️ WR  ❌
    SOLUSDT     WR 44.82%  lift -0.02pp / req 1.61pp  PF 1.218  lift -0.001 / req 0.100  trades 5,951  cov 26.6%  ⚠️ WR  ❌
    BNBUSDT     WR 44.31%  lift -0.57pp / req 1.71pp  PF 1.194  lift -0.028 / req 0.100  trades 5,274  cov 26.1%  ⚠️ WR  ❌
    XRPUSDT     WR 46.93%  lift -0.24pp / req 1.56pp  PF 1.327  lift -0.013 / req 0.100  trades 6,403  cov 26.0%  ⚠️ WR  ❌

  rvol_spike_bearish      avg WR lift +0.59pp  avg PF 1.270  avg PF lift +0.030  pairs ≥ threshold: 0/5  ❌  ⚠️ WR 5p  ⚠️ low count 5p
    BTCUSDT     WR 45.38%  lift +1.13pp / req 2.13pp  PF 1.246  lift +0.056 / req 0.100  trades 3,391  cov 14.4% ⚠️  ⚠️ WR  ❌
    ETHUSDT     WR 46.14%  lift +1.13pp / req 2.10pp  PF 1.285  lift +0.057 / req 0.100  trades 3,513  cov 14.7% ⚠️  ⚠️ WR  ❌
    SOLUSDT     WR 45.50%  lift +0.66pp / req 2.18pp  PF 1.252  lift +0.033 / req 0.100  trades 3,253  cov 14.5% ⚠️  ⚠️ WR  ❌
    BNBUSDT     WR 44.62%  lift -0.27pp / req 2.36pp  PF 1.208  lift -0.013 / req 0.100  trades 2,786  cov 13.8% ⚠️  ⚠️ WR  ❌
    XRPUSDT     WR 47.48%  lift +0.32pp / req 2.09pp  PF 1.356  lift +0.017 / req 0.100  trades 3,578  cov 14.5% ⚠️  ⚠️ WR  ❌

  rvol_spike_down         avg WR lift +0.59pp  avg PF 1.270  avg PF lift +0.030  pairs ≥ threshold: 0/5  ❌  ⚠️ WR 5p  ⚠️ low count 5p
    BTCUSDT     WR 45.38%  lift +1.13pp / req 2.13pp  PF 1.246  lift +0.056 / req 0.100  trades 3,391  cov 14.4% ⚠️  ⚠️ WR  ❌
    ETHUSDT     WR 46.14%  lift +1.13pp / req 2.10pp  PF 1.285  lift +0.057 / req 0.100  trades 3,513  cov 14.7% ⚠️  ⚠️ WR  ❌
    SOLUSDT     WR 45.50%  lift +0.66pp / req 2.18pp  PF 1.252  lift +0.033 / req 0.100  trades 3,253  cov 14.5% ⚠️  ⚠️ WR  ❌
    BNBUSDT     WR 44.62%  lift -0.27pp / req 2.36pp  PF 1.208  lift -0.013 / req 0.100  trades 2,786  cov 13.8% ⚠️  ⚠️ WR  ❌
    XRPUSDT     WR 47.48%  lift +0.32pp / req 2.09pp  PF 1.356  lift +0.017 / req 0.100  trades 3,578  cov 14.5% ⚠️  ⚠️ WR  ❌

  Thresholds: WR lift > 2.5×sqrt(p(1-p)/n),  PF lift > 0.02/0.05/0.10 by n,  consistent across ≥ 4 of 5 pairs

  ❌  RVOL EDGE NOT CONFIRMED — no population clears all thresholds.
      Next steps:
        • Increase min_bars_active (reduces noise on lower TF)
        • Try rvol_threshold = 2.0 (stricter spike definition)
        • Try vol_ma_len = 10 or 50
        • Try a different entry_tf in config.py
        • Re-examine whether setup layer is needed before trigger layer
```
