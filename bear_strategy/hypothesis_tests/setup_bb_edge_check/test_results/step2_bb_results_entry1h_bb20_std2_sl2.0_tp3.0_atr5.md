# Bear Strategy — BB Widening Setup Edge Check  (entry_tf=1h)

## Test Parameters

| Parameter | Value |
|-----------|-------|
| `entry_tf` | `1h` |
| `stop_atr_mult` | `2.0` |
| `target_atr_mult` | `3.0` |
| `atr_period` | `5` |
| `bb_period` | `20` |
| `bb_std_mult` | `2.0` |

```text

── Per-Pair Results ──

  BTCUSDT
                       wr_%     pf   dur  n_trades
population                                        
regime_only           44.23  1.190  21.1     23544
bb_widening           44.21  1.189  24.9     11557
bb_widening_bearish   45.01  1.228  27.2      6437
bb_widening_breakout  46.41  1.299  39.3      1631
    bb_widening covers 49.1% of regime bars  

  ETHUSDT
                       wr_%     pf   dur  n_trades
population                                        
regime_only           44.86  1.220  20.5     23904
bb_widening           44.81  1.218  24.1     11686
bb_widening_bearish   45.23  1.239  25.8      6562
bb_widening_breakout  45.50  1.252  38.0      1679
    bb_widening covers 48.9% of regime bars  

  SOLUSDT
                       wr_%     pf   dur  n_trades
population                                        
regime_only           44.81  1.218  19.9     22370
bb_widening           45.73  1.264  23.6     10930
bb_widening_bearish   46.07  1.282  24.2      6242
bb_widening_breakout  47.88  1.378  33.4      1508
    bb_widening covers 48.9% of regime bars  

  BNBUSDT
                       wr_%     pf   dur  n_trades
population                                        
regime_only           44.62  1.209  19.3     20243
bb_widening           45.16  1.235  22.1      9914
bb_widening_bearish   46.00  1.278  23.2      5470
bb_widening_breakout  46.52  1.305  31.9      1277
    bb_widening covers 49.0% of regime bars  

  XRPUSDT
                       wr_%     pf   dur  n_trades
population                                        
regime_only           47.10  1.335  24.0     24597
bb_widening           47.43  1.353  30.9     11853
bb_widening_bearish   48.48  1.411  37.6      6770
bb_widening_breakout  46.56  1.307  71.8      1658
    bb_widening covers 48.2% of regime bars  

── BB Widening Setup Edge Verdict ──

  Baseline (regime_only):  avg WR 45.1%  avg PF 1.234

  bb_widening         avg WR lift +0.34pp  avg PF 1.252  avg PF lift +0.017  pairs ≥ threshold: 0/5  ❌  ⚠️ WR 5p
    BTCUSDT     WR 44.21%  lift -0.03pp / req 1.15pp  PF 1.189  lift -0.001 / req 0.050  trades 11,557  cov 49.1%  ⚠️ WR  ❌
    ETHUSDT     WR 44.81%  lift -0.05pp / req 1.15pp  PF 1.218  lift -0.003 / req 0.050  trades 11,686  cov 48.9%  ⚠️ WR  ❌
    SOLUSDT     WR 45.73%  lift +0.91pp / req 1.19pp  PF 1.264  lift +0.046 / req 0.050  trades 10,930  cov 48.9%  ⚠️ WR  ❌
    BNBUSDT     WR 45.16%  lift +0.54pp / req 1.25pp  PF 1.235  lift +0.026 / req 0.100  trades 9,914  cov 49.0%  ⚠️ WR  ❌
    XRPUSDT     WR 47.43%  lift +0.34pp / req 1.15pp  PF 1.353  lift +0.018 / req 0.050  trades 11,853  cov 48.2%  ⚠️ WR  ❌

  bb_widening_bearish  avg WR lift +1.03pp  avg PF 1.287  avg PF lift +0.053  pairs ≥ threshold: 0/5  ❌  ⚠️ WR 5p  ⚠️ low count 5p
    BTCUSDT     WR 45.01%  lift +0.77pp / req 1.55pp  PF 1.228  lift +0.038 / req 0.100  trades 6,437  ⚠️ WR  ❌
    ETHUSDT     WR 45.23%  lift +0.37pp / req 1.53pp  PF 1.239  lift +0.018 / req 0.100  trades 6,562  ⚠️ WR  ❌
    SOLUSDT     WR 46.07%  lift +1.26pp / req 1.57pp  PF 1.282  lift +0.064 / req 0.100  trades 6,242  ⚠️ WR  ❌
    BNBUSDT     WR 46.00%  lift +1.37pp / req 1.68pp  PF 1.278  lift +0.069 / req 0.100  trades 5,470  ⚠️ WR  ❌
    XRPUSDT     WR 48.48%  lift +1.38pp / req 1.52pp  PF 1.411  lift +0.076 / req 0.100  trades 6,770  ⚠️ WR  ❌

  bb_widening_breakout  avg WR lift +1.45pp  avg PF 1.308  avg PF lift +0.074  pairs ≥ threshold: 2/5  ❌  ⚠️ WR 5p  ⚠️ low count 5p
    BTCUSDT     WR 46.41%  lift +2.18pp / req 3.07pp  PF 1.299  lift +0.109 / req 0.100  trades 1,631  ⚠️ WR  ✅
    ETHUSDT     WR 45.50%  lift +0.64pp / req 3.03pp  PF 1.252  lift +0.032 / req 0.100  trades 1,679  ⚠️ WR  ❌
    SOLUSDT     WR 47.88%  lift +3.06pp / req 3.20pp  PF 1.378  lift +0.160 / req 0.100  trades 1,508  ⚠️ WR  ✅
    BNBUSDT     WR 46.52%  lift +1.89pp / req 3.48pp  PF 1.305  lift +0.096 / req 0.100  trades 1,277  ⚠️ WR  ❌
    XRPUSDT     WR 46.56%  lift -0.53pp / req 3.06pp  PF 1.307  lift -0.028 / req 0.100  trades 1,658  ⚠️ WR  ❌

  Thresholds: WR lift > 2.5×sqrt(p(1-p)/n),  PF lift > 0.02/0.05/0.10 by n,  consistent across ≥ 4 of 5 pairs

  ❌  BB WIDENING SETUP EDGE NOT CONFIRMED — no population clears all thresholds.
      Next steps:
        • Adjust bb_period (try 10 or 30)
        • Adjust bb_std_mult (try 1.5× or 2.5×)
        • Try a different entry_tf in config.py
        • Re-examine whether setup layer is needed before trigger layer
```
