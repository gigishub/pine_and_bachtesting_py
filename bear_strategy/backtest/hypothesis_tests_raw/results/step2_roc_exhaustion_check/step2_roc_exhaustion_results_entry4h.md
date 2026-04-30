# ROC Exhaustion Setup Edge Check

```text

── Per-Pair Results ──

  BTCUSDT
                 wr_%     pf   dur  n_trades
population                                  
regime_only     43.61  1.160  22.3      5886
roc_post_bull   43.37  1.149  19.8      2098
roc_bear_trend  43.30  1.145  30.8       455
roc_post_bear   43.95  1.176  22.8      2985
    roc_post_bull covers 35.6% of regime bars  
    roc_bear_trend covers 7.7% of regime bars  ⚠️  LOW
    roc_post_bear covers 50.7% of regime bars  

  ETHUSDT
                 wr_%     pf   dur  n_trades
population                                  
regime_only     41.97  1.085  22.5      5976
roc_post_bull   39.12  0.964  19.0      2339
roc_bear_trend  41.20  1.051  27.2       500
roc_post_bear   44.53  1.204  24.7      2753
    roc_post_bull covers 39.1% of regime bars  
    roc_bear_trend covers 8.4% of regime bars  ⚠️  LOW
    roc_post_bear covers 46.1% of regime bars  

  SOLUSDT
                 wr_%     pf   dur  n_trades
population                                  
regime_only     43.39  1.150  22.3      5577
roc_post_bull   42.22  1.096  18.0      1883
roc_bear_trend  48.93  1.437  28.3       515
roc_post_bear   43.85  1.171  24.5      2803
    roc_post_bull covers 33.8% of regime bars  
    roc_bear_trend covers 9.2% of regime bars  ⚠️  LOW
    roc_post_bear covers 50.3% of regime bars  

  BNBUSDT
                 wr_%     pf   dur  n_trades
population                                  
regime_only     45.44  1.249  19.0      5046
roc_post_bull   43.24  1.143  16.9      1915
roc_bear_trend  49.89  1.494  20.6       461
roc_post_bear   47.38  1.351  20.4      2328
    roc_post_bull covers 38.0% of regime bars  
    roc_bear_trend covers 9.1% of regime bars  ⚠️  LOW
    roc_post_bear covers 46.1% of regime bars  

  XRPUSDT
                 wr_%     pf   dur  n_trades
population                                  
regime_only     43.64  1.162  23.9      6141
roc_post_bull   45.88  1.271  19.1      2304
roc_bear_trend  43.90  1.174  42.4       492
roc_post_bear   42.11  1.091  24.6      2973
    roc_post_bull covers 37.5% of regime bars  
    roc_bear_trend covers 8.0% of regime bars  ⚠️  LOW
    roc_post_bear covers 48.4% of regime bars  

── ROC Exhaustion Setup Edge Verdict ──

  Baseline (regime_only):  avg WR 43.6%  avg PF 1.161

  roc_post_bull         avg WR lift -0.85pp  avg PF 1.125  avg PF lift -0.037  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 43.37%  lift -0.24pp / req 2.71pp  PF 1.149  lift -0.011 / req 0.100  trades 2,098  cov 35.6%  ❌
    ETHUSDT     WR 39.12%  lift -2.85pp / req 2.55pp  PF 0.964  lift -0.121 / req 0.100  trades 2,339  cov 39.1%  ❌
    SOLUSDT     WR 42.22%  lift -1.17pp / req 2.86pp  PF 1.096  lift -0.054 / req 0.100  trades 1,883  cov 33.8%  ❌
    BNBUSDT     WR 43.24%  lift -2.20pp / req 2.84pp  PF 1.143  lift -0.107 / req 0.100  trades 1,915  cov 38.0%  ❌
    XRPUSDT     WR 45.88%  lift +2.24pp / req 2.58pp  PF 1.271  lift +0.110 / req 0.100  trades 2,304  cov 37.5%  ❌

  roc_bear_trend        avg WR lift +1.83pp  avg PF 1.260  avg PF lift +0.099  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 43.30%  lift -0.32pp / req 5.81pp  PF 1.145  lift -0.015 / req 0.100  trades 455  cov 7.7% ⚠️  ❌
    ETHUSDT     WR 41.20%  lift -0.77pp / req 5.52pp  PF 1.051  lift -0.034 / req 0.100  trades 500  cov 8.4% ⚠️  ❌
    SOLUSDT     WR 48.93%  lift +5.54pp / req 5.46pp  PF 1.437  lift +0.287 / req 0.100  trades 515  cov 9.2% ⚠️  ❌
    BNBUSDT     WR 49.89%  lift +4.45pp / req 5.80pp  PF 1.494  lift +0.244 / req 0.100  trades 461  cov 9.1% ⚠️  ❌
    XRPUSDT     WR 43.90%  lift +0.26pp / req 5.59pp  PF 1.174  lift +0.012 / req 0.100  trades 492  cov 8.0% ⚠️  ❌

  roc_post_bear         avg WR lift +0.75pp  avg PF 1.199  avg PF lift +0.038  pairs ≥ threshold: 1/5  ❌
    BTCUSDT     WR 43.95%  lift +0.34pp / req 2.27pp  PF 1.176  lift +0.016 / req 0.100  trades 2,985  cov 50.7%  ❌
    ETHUSDT     WR 44.53%  lift +2.57pp / req 2.35pp  PF 1.204  lift +0.120 / req 0.100  trades 2,753  cov 46.1%  ✅
    SOLUSDT     WR 43.85%  lift +0.45pp / req 2.34pp  PF 1.171  lift +0.021 / req 0.100  trades 2,803  cov 50.3%  ❌
    BNBUSDT     WR 47.38%  lift +1.94pp / req 2.58pp  PF 1.351  lift +0.101 / req 0.100  trades 2,328  cov 46.1%  ❌
    XRPUSDT     WR 42.11%  lift -1.53pp / req 2.27pp  PF 1.091  lift -0.070 / req 0.100  trades 2,973  cov 48.4%  ❌

  Thresholds: WR lift > 2.5×sqrt(p(1-p)/n),  PF lift > 0.02/0.05/0.10 by n,  trades > 500,  consistent across ≥ 4 of 5 pairs

  ❌  ROC EXHAUSTION EDGE NOT CONFIRMED — no population clears all thresholds.
      Next steps:
        • Adjust roc_len (try 5 or 20)
        • Adjust drift_bars (try 2 or 4)
        • Adjust accel_thresh (try 0.2% or 1.0%)
        • Try a different entry_tf in config.py
        • Re-examine whether setup layer is needed before trigger layer
```
