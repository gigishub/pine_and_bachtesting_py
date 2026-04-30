# ROC Exhaustion Setup Edge Check

```text

── Per-Pair Results ──

  BTCUSDT
                 wr_%     pf   dur  n_trades
population                                  
regime_only     32.58  0.725  20.5       970
roc_post_bull   19.78  0.370  14.6       273
roc_bear_trend  32.67  0.728  25.4       101
roc_post_bear   39.06  0.961  22.6       553
    roc_post_bull covers 28.1% of regime bars  
    roc_bear_trend covers 10.4% of regime bars  ⚠️  LOW
    roc_post_bear covers 57.0% of regime bars  

  ETHUSDT
                 wr_%     pf   dur  n_trades
population                                  
regime_only     36.63  0.867  19.5       980
roc_post_bull   35.06  0.810  15.6       251
roc_bear_trend  37.39  0.896  24.6       115
roc_post_bear   38.03  0.920  20.5       568
    roc_post_bull covers 25.6% of regime bars  
    roc_bear_trend covers 11.7% of regime bars  ⚠️  LOW
    roc_post_bear covers 58.0% of regime bars  

  SOLUSDT
                 wr_%     pf   dur  n_trades
population                                  
regime_only     37.32  0.893  24.4       887
roc_post_bull   30.22  0.650  19.1       225
roc_bear_trend  44.21  1.189  30.9        95
roc_post_bear   39.61  0.984  25.9       515
    roc_post_bull covers 25.4% of regime bars  
    roc_bear_trend covers 10.7% of regime bars  ⚠️  LOW
    roc_post_bear covers 58.1% of regime bars  

  BNBUSDT
                 wr_%     pf   dur  n_trades
population                                  
regime_only     41.28  1.054  22.5       814
roc_post_bull   45.42  1.248  15.7       273
roc_bear_trend  38.46  0.938  28.0        91
roc_post_bear   40.35  1.015  26.1       404
    roc_post_bull covers 33.5% of regime bars  
    roc_bear_trend covers 11.2% of regime bars  ⚠️  LOW
    roc_post_bear covers 49.6% of regime bars  

  XRPUSDT
                 wr_%     pf   dur  n_trades
population                                  
regime_only     36.94  0.879  27.1       999
roc_post_bull   45.61  1.258  20.8       285
roc_bear_trend  29.25  0.620  24.8       106
roc_post_bear   33.76  0.764  23.7       548
    roc_post_bull covers 28.5% of regime bars  
    roc_bear_trend covers 10.6% of regime bars  ⚠️  LOW
    roc_post_bear covers 54.9% of regime bars  

── ROC Exhaustion Setup Edge Verdict ──

  Baseline (regime_only):  avg WR 36.9%  avg PF 0.884

  roc_post_bull         avg WR lift -1.73pp  avg PF 0.867  avg PF lift -0.016  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 19.78%  lift -12.80pp / req 7.09pp  PF 0.370  lift -0.355 / req 0.100  trades 273  cov 28.1%  ❌
    ETHUSDT     WR 35.06%  lift -1.57pp / req 7.60pp  PF 0.810  lift -0.057 / req 0.100  trades 251  cov 25.6%  ❌
    SOLUSDT     WR 30.22%  lift -7.09pp / req 8.06pp  PF 0.650  lift -0.243 / req 0.100  trades 225  cov 25.4%  ❌
    BNBUSDT     WR 45.42%  lift +4.14pp / req 7.45pp  PF 1.248  lift +0.194 / req 0.100  trades 273  cov 33.5%  ❌
    XRPUSDT     WR 45.61%  lift +8.68pp / req 7.15pp  PF 1.258  lift +0.379 / req 0.100  trades 285  cov 28.5%  ❌

  roc_bear_trend        avg WR lift -0.55pp  avg PF 0.874  avg PF lift -0.010  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 32.67%  lift +0.10pp / req 11.66pp  PF 0.728  lift +0.003 / req 0.100  trades 101  cov 10.4% ⚠️  ❌
    ETHUSDT     WR 37.39%  lift +0.76pp / req 11.23pp  PF 0.896  lift +0.029 / req 0.100  trades 115  cov 11.7% ⚠️  ❌
    SOLUSDT     WR 44.21%  lift +6.89pp / req 12.41pp  PF 1.189  lift +0.296 / req 0.100  trades 95  cov 10.7% ⚠️  ❌
    BNBUSDT     WR 38.46%  lift -2.82pp / req 12.90pp  PF 0.938  lift -0.117 / req 0.100  trades 91  cov 11.2% ⚠️  ❌
    XRPUSDT     WR 29.25%  lift -7.69pp / req 11.72pp  PF 0.620  lift -0.259 / req 0.100  trades 106  cov 10.6% ⚠️  ❌

  roc_post_bear         avg WR lift +1.21pp  avg PF 0.929  avg PF lift +0.045  pairs ≥ threshold: 1/5  ❌
    BTCUSDT     WR 39.06%  lift +6.48pp / req 4.98pp  PF 0.961  lift +0.237 / req 0.100  trades 553  cov 57.0%  ✅
    ETHUSDT     WR 38.03%  lift +1.40pp / req 5.05pp  PF 0.920  lift +0.053 / req 0.100  trades 568  cov 58.0%  ❌
    SOLUSDT     WR 39.61%  lift +2.29pp / req 5.33pp  PF 0.984  lift +0.091 / req 0.100  trades 515  cov 58.1%  ❌
    BNBUSDT     WR 40.35%  lift -0.93pp / req 6.12pp  PF 1.015  lift -0.040 / req 0.100  trades 404  cov 49.6%  ❌
    XRPUSDT     WR 33.76%  lift -3.18pp / req 5.15pp  PF 0.764  lift -0.114 / req 0.100  trades 548  cov 54.9%  ❌

  Thresholds: WR lift > 2.5×sqrt(p(1-p)/n),  PF lift > 0.02/0.05/0.10 by n,  trades > 500,  consistent across ≥ 4 of 5 pairs

  ❌  ROC EXHAUSTION EDGE NOT CONFIRMED — no population clears all thresholds.
      Next steps:
        • Adjust roc_len (try 5 or 20)
        • Adjust drift_bars (try 2 or 4)
        • Adjust accel_thresh (try 0.2% or 1.0%)
        • Try a different entry_tf in config.py
        • Re-examine whether setup layer is needed before trigger layer
```
