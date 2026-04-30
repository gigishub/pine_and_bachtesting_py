# Bear Strategy — BB Range Setup Edge Check  (entry_tf=1h)

```text

── Per-Pair Results ──

  BTCUSDT
                 wr_%     pf   dur  n_trades
population                                  
regime_only     44.25  1.191  20.4     23544
price_in_bands  43.98  1.178  19.2     20776
below_upper     44.17  1.187  20.2     22464
above_lower     44.07  1.182  19.5     21856
    price_in_bands covers 88.2% of regime bars  

  ETHUSDT
                 wr_%     pf   dur  n_trades
population                                  
regime_only     45.01  1.228  19.9     23904
price_in_bands  44.89  1.222  18.6     21090
below_upper     44.98  1.226  19.6     22839
above_lower     44.92  1.224  19.0     22155
    price_in_bands covers 88.2% of regime bars  

  SOLUSDT
                 wr_%     pf   dur  n_trades
population                                  
regime_only     44.84  1.219  19.5     22371
price_in_bands  44.67  1.211  18.5     19831
below_upper     44.88  1.221  19.2     21394
above_lower     44.63  1.209  18.9     20808
    price_in_bands covers 88.6% of regime bars  

  BNBUSDT
                 wr_%     pf   dur  n_trades
population                                  
regime_only     44.88  1.222  19.0     20243
price_in_bands  44.76  1.215  18.1     18053
below_upper     44.92  1.223  18.7     19379
above_lower     44.73  1.214  18.5     18917
    price_in_bands covers 89.2% of regime bars  

  XRPUSDT
                 wr_%     pf   dur  n_trades
population                                  
regime_only     47.17  1.339  22.3     24598
price_in_bands  47.30  1.347  20.0     21808
below_upper     47.27  1.345  22.1     23536
above_lower     47.19  1.340  20.3     22870
    price_in_bands covers 88.7% of regime bars  

── BB Range Setup Edge Verdict ──

  Baseline (regime_only):  avg WR 45.2%  avg PF 1.240

  price_in_bands    avg WR lift -0.11pp  avg PF 1.234  avg PF lift -0.005  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 43.98%  lift -0.27pp / req 0.86pp  PF 1.178  lift -0.013 / req 0.050  trades 20,776  cov 88.2%  ❌
    ETHUSDT     WR 44.89%  lift -0.12pp / req 0.86pp  PF 1.222  lift -0.006 / req 0.050  trades 21,090  cov 88.2%  ❌
    SOLUSDT     WR 44.67%  lift -0.17pp / req 0.88pp  PF 1.211  lift -0.008 / req 0.050  trades 19,831  cov 88.6%  ❌
    BNBUSDT     WR 44.76%  lift -0.13pp / req 0.93pp  PF 1.215  lift -0.006 / req 0.050  trades 18,053  cov 89.2%  ❌
    XRPUSDT     WR 47.30%  lift +0.14pp / req 0.85pp  PF 1.347  lift +0.007 / req 0.050  trades 21,808  cov 88.7%  ❌

  below_upper       avg WR lift +0.01pp  avg PF 1.241  avg PF lift +0.001  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 44.17%  lift -0.08pp / req 0.83pp  PF 1.187  lift -0.004 / req 0.050  trades 22,464  ❌
    ETHUSDT     WR 44.98%  lift -0.03pp / req 0.82pp  PF 1.226  lift -0.001 / req 0.050  trades 22,839  ❌
    SOLUSDT     WR 44.88%  lift +0.04pp / req 0.85pp  PF 1.221  lift +0.002 / req 0.050  trades 21,394  ❌
    BNBUSDT     WR 44.92%  lift +0.04pp / req 0.89pp  PF 1.223  lift +0.002 / req 0.050  trades 19,379  ❌
    XRPUSDT     WR 47.27%  lift +0.11pp / req 0.81pp  PF 1.345  lift +0.006 / req 0.050  trades 23,536  ❌

  above_lower       avg WR lift -0.12pp  avg PF 1.234  avg PF lift -0.006  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 44.07%  lift -0.18pp / req 0.84pp  PF 1.182  lift -0.009 / req 0.050  trades 21,856  ❌
    ETHUSDT     WR 44.92%  lift -0.08pp / req 0.84pp  PF 1.224  lift -0.004 / req 0.050  trades 22,155  ❌
    SOLUSDT     WR 44.63%  lift -0.21pp / req 0.86pp  PF 1.209  lift -0.010 / req 0.050  trades 20,808  ❌
    BNBUSDT     WR 44.73%  lift -0.16pp / req 0.90pp  PF 1.214  lift -0.008 / req 0.050  trades 18,917  ❌
    XRPUSDT     WR 47.19%  lift +0.02pp / req 0.83pp  PF 1.340  lift +0.001 / req 0.050  trades 22,870  ❌

  Thresholds: WR lift > 2.5×sqrt(p(1-p)/n),  PF lift > 0.02/0.05/0.10 by n,  trades > 1,000,  consistent across ≥ 4 of 5 pairs

  ❌  BB RANGE SETUP EDGE NOT CONFIRMED — no in-band population clears all thresholds.
      Next steps:
        • Adjust bb_std_mult (try 1.5× or 2.5×)
        • Adjust bb_period (try 10 or 30)
        • Compare with setup_bb_edge_check: edge may lie in the broken-below zone
        • Try a different entry_tf in experiment_config.py
```
