# Bear Strategy — RSI Setup Edge Check  (entry_tf=1d)

```text

── Per-Pair Results ──

  BTCUSDT
               wr_%     pf   dur  n_trades
population                                
regime_only   32.41  0.719  20.4       975
rsi_30_50     33.09  0.742  18.9       810
rsi_below_50  32.35  0.717  21.0       878
rsi_above_30  33.08  0.741  18.4       907
    rsi_30_50 covers 83.1% of regime bars  

  ETHUSDT
               wr_%     pf   dur  n_trades
population                                
regime_only   36.45  0.860  19.4       985
rsi_30_50     39.30  0.971  19.2       832
rsi_below_50  38.18  0.926  20.0       888
rsi_above_30  37.35  0.894  18.7       929
    rsi_30_50 covers 84.5% of regime bars  

  SOLUSDT
               wr_%     pf   dur  n_trades
population                                
regime_only   37.15  0.887  24.3       891
rsi_30_50     39.06  0.961  23.6       763
rsi_below_50  37.95  0.917  25.4       809
rsi_above_30  38.11  0.924  22.6       845
    rsi_30_50 covers 85.6% of regime bars  

  BNBUSDT
               wr_%     pf   dur  n_trades
population                                
regime_only   41.13  1.048  22.4       817
rsi_30_50     41.88  1.081  21.6       671
rsi_below_50  40.61  1.026  23.4       724
rsi_above_30  42.28  1.099  20.7       764
    rsi_30_50 covers 82.1% of regime bars  

  XRPUSDT
               wr_%     pf   dur  n_trades
population                                
regime_only   36.79  0.873  32.1      1003
rsi_30_50     36.38  0.858  30.6       885
rsi_below_50  36.12  0.848  32.1       922
rsi_above_30  37.06  0.883  30.8       966
    rsi_30_50 covers 88.2% of regime bars  

── RSI Setup Edge Verdict ──

  Baseline (regime_only):  avg WR 36.8%  avg PF 0.877

  rsi_30_50       avg WR lift +1.16pp  avg PF 0.923  avg PF lift +0.045  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 33.09%  lift +0.68pp / req 4.11pp  PF 0.742  lift +0.022 / req 0.100  trades 810  cov 83.1%  ❌
    ETHUSDT     WR 39.30%  lift +2.86pp / req 4.17pp  PF 0.971  lift +0.111 / req 0.100  trades 832  cov 84.5%  ❌
    SOLUSDT     WR 39.06%  lift +1.91pp / req 4.37pp  PF 0.961  lift +0.075 / req 0.100  trades 763  cov 85.6%  ❌
    BNBUSDT     WR 41.88%  lift +0.75pp / req 4.75pp  PF 1.081  lift +0.033 / req 0.100  trades 671  cov 82.1%  ❌
    XRPUSDT     WR 36.38%  lift -0.41pp / req 4.05pp  PF 0.858  lift -0.015 / req 0.100  trades 885  cov 88.2%  ❌

  rsi_below_50    avg WR lift +0.25pp  avg PF 0.887  avg PF lift +0.009  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 32.35%  lift -0.06pp / req 3.95pp  PF 0.717  lift -0.002 / req 0.100  trades 878  ❌
    ETHUSDT     WR 38.18%  lift +1.73pp / req 4.04pp  PF 0.926  lift +0.066 / req 0.100  trades 888  ❌
    SOLUSDT     WR 37.95%  lift +0.80pp / req 4.25pp  PF 0.917  lift +0.031 / req 0.100  trades 809  ❌
    BNBUSDT     WR 40.61%  lift -0.52pp / req 4.57pp  PF 1.026  lift -0.022 / req 0.100  trades 724  ❌
    XRPUSDT     WR 36.12%  lift -0.67pp / req 3.97pp  PF 0.848  lift -0.025 / req 0.100  trades 922  ❌

  rsi_above_30    avg WR lift +0.79pp  avg PF 0.908  avg PF lift +0.031  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 33.08%  lift +0.67pp / req 3.89pp  PF 0.741  lift +0.022 / req 0.100  trades 907  ❌
    ETHUSDT     WR 37.35%  lift +0.91pp / req 3.95pp  PF 0.894  lift +0.034 / req 0.100  trades 929  ❌
    SOLUSDT     WR 38.11%  lift +0.96pp / req 4.16pp  PF 0.924  lift +0.037 / req 0.100  trades 845  ❌
    BNBUSDT     WR 42.28%  lift +1.15pp / req 4.45pp  PF 1.099  lift +0.051 / req 0.100  trades 764  ❌
    XRPUSDT     WR 37.06%  lift +0.27pp / req 3.88pp  PF 0.883  lift +0.010 / req 0.100  trades 966  ❌

  Thresholds: WR lift > 2.5×sqrt(p(1-p)/n),  PF lift > 0.02/0.05/0.10 by n,  trades > 1,000,  consistent across ≥ 4 of 5 pairs

  ❌  RSI SETUP EDGE NOT CONFIRMED — no RSI population clears all thresholds.
      Next steps:
        • Adjust rsi_upper (try 45 or 55)
        • Adjust rsi_lower (try 20 or 35)
        • Adjust rsi_period (try 7 or 21)
        • Try a different entry_tf in experiment_config.py
```
