# Bear Strategy — BB Widening Setup Edge Check  (entry_tf=4h)

## Test Parameters

| Parameter | Value |
|-----------|-------|
| `entry_tf` | `4h` |
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
regime_only           43.07  1.135  22.4      5876
bb_widening           41.53  1.065  24.3      2798
bb_widening_bearish   40.51  1.022  26.4      1792
bb_widening_breakout  41.79  1.077  38.1       457
    bb_widening covers 47.6% of regime bars  

  ETHUSDT
                       wr_%     pf   dur  n_trades
population                                        
regime_only           42.25  1.097  22.6      5974
bb_widening           43.70  1.164  26.6      2856
bb_widening_bearish   43.34  1.147  30.6      1779
bb_widening_breakout  41.56  1.067  45.4       474
    bb_widening covers 47.8% of regime bars  

  SOLUSDT
                       wr_%     pf   dur  n_trades
population                                        
regime_only           43.45  1.152  22.6      5572
bb_widening           44.96  1.225  26.0      2718
bb_widening_bearish   45.95  1.275  29.3      1754
bb_widening_breakout  43.77  1.167  47.8       393
    bb_widening covers 48.8% of regime bars  

  BNBUSDT
                       wr_%     pf   dur  n_trades
population                                        
regime_only           45.48  1.251  19.0      5040
bb_widening           46.87  1.323  21.3      2430
bb_widening_bearish   49.18  1.451  23.1      1521
bb_widening_breakout  46.38  1.297  29.0       414
    bb_widening covers 48.2% of regime bars  

  XRPUSDT
                       wr_%     pf   dur  n_trades
population                                        
regime_only           43.77  1.168  24.0      6139
bb_widening           42.69  1.117  29.3      2893
bb_widening_bearish   43.89  1.173  34.9      1834
bb_widening_breakout  40.80  1.034  60.2       473
    bb_widening covers 47.1% of regime bars  

── BB Widening Setup Edge Verdict ──

  Baseline (regime_only):  avg WR 43.6%  avg PF 1.161

  bb_widening         avg WR lift +0.35pp  avg PF 1.179  avg PF lift +0.018  pairs ≥ threshold: 0/5  ❌  ⚠️ WR 5p  ⚠️ weak regime 1p
    BTCUSDT     WR 41.53%  lift -1.54pp / req 2.34pp  PF 1.065  lift -0.070 / req 0.100  trades 2,798  cov 47.6%  ⚠️ WR  ❌
    ETHUSDT     WR 43.70%  lift +1.45pp / req 2.31pp  PF 1.164  lift +0.067 / req 0.100  trades 2,856  cov 47.8%  ⚠️ WR  ❌
    SOLUSDT     WR 44.96%  lift +1.51pp / req 2.38pp  PF 1.225  lift +0.073 / req 0.100  trades 2,718  cov 48.8%  ⚠️ WR  ❌
    BNBUSDT     WR 46.87%  lift +1.40pp / req 2.53pp  PF 1.323  lift +0.072 / req 0.100  trades 2,430  cov 48.2%  ⚠️ WR  ❌
    XRPUSDT     WR 42.69%  lift -1.08pp / req 2.31pp  PF 1.117  lift -0.050 / req 0.100  trades 2,893  cov 47.1%  ⚠️ WR  ❌

  bb_widening_bearish  avg WR lift +0.97pp  avg PF 1.214  avg PF lift +0.053  pairs ≥ threshold: 2/5  ❌  ⚠️ WR 4p  ⚠️ low count 2p  ⚠️ weak regime 1p
    BTCUSDT     WR 40.51%  lift -2.56pp / req 2.92pp  PF 1.022  lift -0.113 / req 0.100  trades 1,792  ⚠️ WR  ❌
    ETHUSDT     WR 43.34%  lift +1.09pp / req 2.93pp  PF 1.147  lift +0.050 / req 0.100  trades 1,779  ⚠️ WR  ❌
    SOLUSDT     WR 45.95%  lift +2.50pp / req 2.96pp  PF 1.275  lift +0.123 / req 0.100  trades 1,754  ⚠️ WR  ✅
    BNBUSDT     WR 49.18%  lift +3.70pp / req 3.19pp  PF 1.451  lift +0.200 / req 0.100  trades 1,521  ✅
    XRPUSDT     WR 43.89%  lift +0.12pp / req 2.90pp  PF 1.173  lift +0.006 / req 0.100  trades 1,834  ⚠️ WR  ❌

  bb_widening_breakout  avg WR lift -0.74pp  avg PF 1.129  avg PF lift -0.032  pairs ≥ threshold: 0/5  ❌  ⚠️ WR 5p  ⚠️ low count 5p  ⚠️ weak regime 1p
    BTCUSDT     WR 41.79%  lift -1.28pp / req 5.79pp  PF 1.077  lift -0.058 / req 0.100  trades 457  ⚠️ WR  ❌
    ETHUSDT     WR 41.56%  lift -0.69pp / req 5.67pp  PF 1.067  lift -0.031 / req 0.100  trades 474  ⚠️ WR  ❌
    SOLUSDT     WR 43.77%  lift +0.32pp / req 6.25pp  PF 1.167  lift +0.015 / req 0.100  trades 393  ⚠️ WR  ❌
    BNBUSDT     WR 46.38%  lift +0.90pp / req 6.12pp  PF 1.297  lift +0.046 / req 0.100  trades 414  ⚠️ WR  ❌
    XRPUSDT     WR 40.80%  lift -2.97pp / req 5.70pp  PF 1.034  lift -0.134 / req 0.100  trades 473  ⚠️ WR  ❌

  Thresholds: WR lift > 2.5×sqrt(p(1-p)/n),  PF lift > 0.02/0.05/0.10 by n,  consistent across ≥ 4 of 5 pairs

  ❌  BB WIDENING SETUP EDGE NOT CONFIRMED — no population clears all thresholds.
      Next steps:
        • Adjust bb_period (try 10 or 30)
        • Adjust bb_std_mult (try 1.5× or 2.5×)
        • Try a different entry_tf in config.py
        • Re-examine whether setup layer is needed before trigger layer
```
