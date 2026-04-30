# Bear Strategy — BB Range Setup Edge Check  (entry_tf=1d)

```text

── Per-Pair Results ──

  BTCUSDT
                 wr_%     pf   dur  n_trades
population                                  
regime_only     32.58  0.725  20.5       970
price_in_bands  31.41  0.687  18.8       882
below_upper     32.50  0.722  20.5       963
above_lower     31.50  0.690  18.8       889
    price_in_bands covers 90.9% of regime bars  

  ETHUSDT
                 wr_%     pf   dur  n_trades
population                                  
regime_only     36.78  0.873  19.6       976
price_in_bands  36.16  0.850  18.2       885
below_upper     36.87  0.876  19.6       971
above_lower     36.07  0.846  18.2       890
    price_in_bands covers 90.7% of regime bars  

  SOLUSDT
                 wr_%     pf   dur  n_trades
population                                  
regime_only     37.32  0.893  24.4       887
price_in_bands  37.91  0.916  22.6       802
below_upper     37.41  0.897  24.5       882
above_lower     37.79  0.911  22.5       807
    price_in_bands covers 90.4% of regime bars  

  BNBUSDT
                 wr_%     pf   dur  n_trades
population                                  
regime_only     41.38  1.059  22.5       812
price_in_bands  41.25  1.053  22.1       720
below_upper     41.44  1.061  22.6       806
above_lower     41.18  1.050  22.0       726
    price_in_bands covers 88.7% of regime bars  

  XRPUSDT
                 wr_%     pf   dur  n_trades
population                                  
regime_only     37.07  0.884  22.7       990
price_in_bands  38.56  0.941  21.2       900
below_upper     37.20  0.888  22.7       984
above_lower     38.41  0.935  21.2       906
    price_in_bands covers 90.9% of regime bars  

── BB Range Setup Edge Verdict ──

  Baseline (regime_only):  avg WR 37.0%  avg PF 0.887

  price_in_bands    avg WR lift +0.03pp  avg PF 0.889  avg PF lift +0.003  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 31.41%  lift -1.17pp / req 3.95pp  PF 0.687  lift -0.038 / req 0.100  trades 882  cov 90.9%  ❌
    ETHUSDT     WR 36.16%  lift -0.62pp / req 4.05pp  PF 0.850  lift -0.023 / req 0.100  trades 885  cov 90.7%  ❌
    SOLUSDT     WR 37.91%  lift +0.59pp / req 4.27pp  PF 0.916  lift +0.023 / req 0.100  trades 802  cov 90.4%  ❌
    BNBUSDT     WR 41.25%  lift -0.13pp / req 4.59pp  PF 1.053  lift -0.006 / req 0.100  trades 720  cov 88.7%  ❌
    XRPUSDT     WR 38.56%  lift +1.48pp / req 4.02pp  PF 0.941  lift +0.058 / req 0.100  trades 900  cov 90.9%  ❌

  below_upper       avg WR lift +0.06pp  avg PF 0.889  avg PF lift +0.002  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 32.50%  lift -0.07pp / req 3.78pp  PF 0.722  lift -0.002 / req 0.100  trades 963  ❌
    ETHUSDT     WR 36.87%  lift +0.09pp / req 3.87pp  PF 0.876  lift +0.003 / req 0.100  trades 971  ❌
    SOLUSDT     WR 37.41%  lift +0.10pp / req 4.07pp  PF 0.897  lift +0.004 / req 0.100  trades 882  ❌
    BNBUSDT     WR 41.44%  lift +0.06pp / req 4.34pp  PF 1.061  lift +0.003 / req 0.100  trades 806  ❌
    XRPUSDT     WR 37.20%  lift +0.12pp / req 3.85pp  PF 0.888  lift +0.005 / req 0.100  trades 984  ❌

  above_lower       avg WR lift -0.03pp  avg PF 0.887  avg PF lift +0.000  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 31.50%  lift -1.08pp / req 3.93pp  PF 0.690  lift -0.035 / req 0.100  trades 889  ❌
    ETHUSDT     WR 36.07%  lift -0.72pp / req 4.04pp  PF 0.846  lift -0.027 / req 0.100  trades 890  ❌
    SOLUSDT     WR 37.79%  lift +0.48pp / req 4.26pp  PF 0.911  lift +0.018 / req 0.100  trades 807  ❌
    BNBUSDT     WR 41.18%  lift -0.19pp / req 4.57pp  PF 1.050  lift -0.008 / req 0.100  trades 726  ❌
    XRPUSDT     WR 38.41%  lift +1.34pp / req 4.01pp  PF 0.935  lift +0.052 / req 0.100  trades 906  ❌

  Thresholds: WR lift > 2.5×sqrt(p(1-p)/n),  PF lift > 0.02/0.05/0.10 by n,  trades > 1,000,  consistent across ≥ 4 of 5 pairs

  ❌  BB RANGE SETUP EDGE NOT CONFIRMED — no in-band population clears all thresholds.
      Next steps:
        • Adjust bb_std_mult (try 1.5× or 2.5×)
        • Adjust bb_period (try 10 or 30)
        • Compare with setup_bb_edge_check: edge may lie in the broken-below zone
        • Try a different entry_tf in experiment_config.py
```
