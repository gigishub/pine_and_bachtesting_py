# ROC Exhaustion Setup Edge Check

```text

── Per-Pair Results ──

  BTCUSDT
                 wr_%     pf   dur  n_trades
population                                  
regime_only     44.25  1.191  20.4     23544
roc_post_bull   43.28  1.145  18.3      9931
roc_bear_trend  47.14  1.337  27.0      1519
roc_post_bear   44.65  1.210  21.1     10863
    roc_post_bull covers 42.2% of regime bars  
    roc_bear_trend covers 6.5% of regime bars  ⚠️  LOW
    roc_post_bear covers 46.1% of regime bars  

  ETHUSDT
                 wr_%     pf   dur  n_trades
population                                  
regime_only     45.01  1.228  19.9     23904
roc_post_bull   44.08  1.182  18.0      9427
roc_bear_trend  46.50  1.304  24.4      1686
roc_post_bear   45.83  1.269  20.5     11402
    roc_post_bull covers 39.4% of regime bars  
    roc_bear_trend covers 7.1% of regime bars  ⚠️  LOW
    roc_post_bear covers 47.7% of regime bars  

  SOLUSDT
                 wr_%     pf   dur  n_trades
population                                  
regime_only     44.84  1.219  19.5     22371
roc_post_bull   45.62  1.258  18.4      8714
roc_bear_trend  46.74  1.316  21.8      1746
roc_post_bear   44.28  1.192  20.0     10391
    roc_post_bull covers 39.0% of regime bars  
    roc_bear_trend covers 7.8% of regime bars  ⚠️  LOW
    roc_post_bear covers 46.4% of regime bars  

  BNBUSDT
                 wr_%     pf   dur  n_trades
population                                  
regime_only     44.88  1.222  19.0     20243
roc_post_bull   45.21  1.238  17.8      8249
roc_bear_trend  48.55  1.415  21.6      1380
roc_post_bear   44.00  1.179  19.1      9470
    roc_post_bull covers 40.7% of regime bars  
    roc_bear_trend covers 6.8% of regime bars  ⚠️  LOW
    roc_post_bear covers 46.8% of regime bars  

  XRPUSDT
                 wr_%     pf   dur  n_trades
population                                  
regime_only     47.17  1.339  22.3     24598
roc_post_bull   48.30  1.401  19.0      9911
roc_bear_trend  48.55  1.416  30.6      1833
roc_post_bear   46.09  1.283  23.7     11349
    roc_post_bull covers 40.3% of regime bars  
    roc_bear_trend covers 7.5% of regime bars  ⚠️  LOW
    roc_post_bear covers 46.1% of regime bars  

── ROC Exhaustion Setup Edge Verdict ──

  Baseline (regime_only):  avg WR 45.2%  avg PF 1.240

  roc_post_bull         avg WR lift +0.06pp  avg PF 1.245  avg PF lift +0.005  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 43.28%  lift -0.97pp / req 1.25pp  PF 1.145  lift -0.046 / req 0.100  trades 9,931  cov 42.2%  ❌
    ETHUSDT     WR 44.08%  lift -0.93pp / req 1.28pp  PF 1.182  lift -0.046 / req 0.100  trades 9,427  cov 39.4%  ❌
    SOLUSDT     WR 45.62%  lift +0.78pp / req 1.33pp  PF 1.258  lift +0.039 / req 0.100  trades 8,714  cov 39.0%  ❌
    BNBUSDT     WR 45.21%  lift +0.32pp / req 1.37pp  PF 1.238  lift +0.016 / req 0.100  trades 8,249  cov 40.7%  ❌
    XRPUSDT     WR 48.30%  lift +1.13pp / req 1.25pp  PF 1.401  lift +0.062 / req 0.100  trades 9,911  cov 40.3%  ❌

  roc_bear_trend        avg WR lift +2.26pp  avg PF 1.358  avg PF lift +0.118  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 47.14%  lift +2.88pp / req 3.19pp  PF 1.337  lift +0.147 / req 0.100  trades 1,519  cov 6.5% ⚠️  ❌
    ETHUSDT     WR 46.50%  lift +1.49pp / req 3.03pp  PF 1.304  lift +0.076 / req 0.100  trades 1,686  cov 7.1% ⚠️  ❌
    SOLUSDT     WR 46.74%  lift +1.90pp / req 2.98pp  PF 1.316  lift +0.097 / req 0.100  trades 1,746  cov 7.8% ⚠️  ❌
    BNBUSDT     WR 48.55%  lift +3.67pp / req 3.35pp  PF 1.415  lift +0.194 / req 0.100  trades 1,380  cov 6.8% ⚠️  ❌
    XRPUSDT     WR 48.55%  lift +1.39pp / req 2.91pp  PF 1.416  lift +0.077 / req 0.100  trades 1,833  cov 7.5% ⚠️  ❌

  roc_post_bear         avg WR lift -0.26pp  avg PF 1.226  avg PF lift -0.013  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 44.65%  lift +0.39pp / req 1.19pp  PF 1.210  lift +0.019 / req 0.050  trades 10,863  cov 46.1%  ❌
    ETHUSDT     WR 45.83%  lift +0.82pp / req 1.16pp  PF 1.269  lift +0.041 / req 0.050  trades 11,402  cov 47.7%  ❌
    SOLUSDT     WR 44.28%  lift -0.56pp / req 1.22pp  PF 1.192  lift -0.027 / req 0.050  trades 10,391  cov 46.4%  ❌
    BNBUSDT     WR 44.00%  lift -0.88pp / req 1.28pp  PF 1.179  lift -0.043 / req 0.100  trades 9,470  cov 46.8%  ❌
    XRPUSDT     WR 46.09%  lift -1.07pp / req 1.17pp  PF 1.283  lift -0.057 / req 0.050  trades 11,349  cov 46.1%  ❌

  Thresholds: WR lift > 2.5×sqrt(p(1-p)/n),  PF lift > 0.02/0.05/0.10 by n,  trades > 1,000,  consistent across ≥ 4 of 5 pairs

  ❌  ROC EXHAUSTION EDGE NOT CONFIRMED — no population clears all thresholds.
      Next steps:
        • Adjust roc_len (try 5 or 20)
        • Adjust drift_bars (try 2 or 4)
        • Adjust accel_thresh (try 0.2% or 1.0%)
        • Try a different entry_tf in config.py
        • Re-examine whether setup layer is needed before trigger layer
```
