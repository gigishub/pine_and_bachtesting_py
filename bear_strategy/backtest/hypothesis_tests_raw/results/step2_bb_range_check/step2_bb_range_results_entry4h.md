# Bear Strategy — BB Range Setup Edge Check  (entry_tf=4h)

```text

── Per-Pair Results ──

  BTCUSDT
                 wr_%     pf   dur  n_trades
population                                  
regime_only     43.59  1.159  22.4      5877
price_in_bands  43.62  1.161  21.5      5192
below_upper     43.70  1.164  22.4      5673
above_lower     43.51  1.156  21.5      5396
    price_in_bands covers 88.3% of regime bars  

  ETHUSDT
                 wr_%     pf   dur  n_trades
population                                  
regime_only     41.96  1.084  22.5      5975
price_in_bands  41.45  1.062  21.1      5266
below_upper     41.61  1.069  22.5      5761
above_lower     41.84  1.079  21.2      5480
    price_in_bands covers 88.1% of regime bars  

  SOLUSDT
                 wr_%     pf   dur  n_trades
population                                  
regime_only     43.46  1.153  22.3      5568
price_in_bands  43.17  1.139  21.1      4946
below_upper     43.33  1.147  22.4      5364
above_lower     43.32  1.146  21.1      5150
    price_in_bands covers 88.8% of regime bars  

  BNBUSDT
                 wr_%     pf   dur  n_trades
population                                  
regime_only     45.51  1.253  19.0      5038
price_in_bands  45.42  1.248  18.3      4417
below_upper     45.51  1.253  19.0      4843
above_lower     45.42  1.249  18.4      4612
    price_in_bands covers 87.7% of regime bars  

  XRPUSDT
                 wr_%     pf   dur  n_trades
population                                  
regime_only     43.64  1.162  23.9      6141
price_in_bands  43.77  1.168  21.5      5449
below_upper     43.65  1.162  24.1      5947
above_lower     43.75  1.167  21.4      5643
    price_in_bands covers 88.7% of regime bars  

── BB Range Setup Edge Verdict ──

  Baseline (regime_only):  avg WR 43.6%  avg PF 1.162

  price_in_bands    avg WR lift -0.15pp  avg PF 1.156  avg PF lift -0.007  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 43.62%  lift +0.03pp / req 1.72pp  PF 1.161  lift +0.001 / req 0.100  trades 5,192  cov 88.3%  ❌
    ETHUSDT     WR 41.45%  lift -0.50pp / req 1.70pp  PF 1.062  lift -0.022 / req 0.100  trades 5,266  cov 88.1%  ❌
    SOLUSDT     WR 43.17%  lift -0.30pp / req 1.76pp  PF 1.139  lift -0.014 / req 0.100  trades 4,946  cov 88.8%  ❌
    BNBUSDT     WR 45.42%  lift -0.10pp / req 1.87pp  PF 1.248  lift -0.005 / req 0.100  trades 4,417  cov 87.7%  ❌
    XRPUSDT     WR 43.77%  lift +0.13pp / req 1.68pp  PF 1.168  lift +0.006 / req 0.100  trades 5,449  cov 88.7%  ❌

  below_upper       avg WR lift -0.08pp  avg PF 1.159  avg PF lift -0.003  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 43.70%  lift +0.10pp / req 1.65pp  PF 1.164  lift +0.005 / req 0.100  trades 5,673  ❌
    ETHUSDT     WR 41.61%  lift -0.35pp / req 1.63pp  PF 1.069  lift -0.016 / req 0.100  trades 5,761  ❌
    SOLUSDT     WR 43.33%  lift -0.14pp / req 1.69pp  PF 1.147  lift -0.006 / req 0.100  trades 5,364  ❌
    BNBUSDT     WR 45.51%  lift -0.01pp / req 1.79pp  PF 1.253  lift -0.000 / req 0.100  trades 4,843  ❌
    XRPUSDT     WR 43.65%  lift +0.01pp / req 1.61pp  PF 1.162  lift +0.001 / req 0.100  trades 5,947  ❌

  above_lower       avg WR lift -0.06pp  avg PF 1.159  avg PF lift -0.003  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 43.51%  lift -0.08pp / req 1.69pp  PF 1.156  lift -0.004 / req 0.100  trades 5,396  ❌
    ETHUSDT     WR 41.84%  lift -0.12pp / req 1.67pp  PF 1.079  lift -0.005 / req 0.100  trades 5,480  ❌
    SOLUSDT     WR 43.32%  lift -0.14pp / req 1.73pp  PF 1.146  lift -0.007 / req 0.100  trades 5,150  ❌
    BNBUSDT     WR 45.42%  lift -0.09pp / req 1.83pp  PF 1.249  lift -0.004 / req 0.100  trades 4,612  ❌
    XRPUSDT     WR 43.75%  lift +0.11pp / req 1.65pp  PF 1.167  lift +0.005 / req 0.100  trades 5,643  ❌

  Thresholds: WR lift > 2.5×sqrt(p(1-p)/n),  PF lift > 0.02/0.05/0.10 by n,  trades > 1,000,  consistent across ≥ 4 of 5 pairs

  ❌  BB RANGE SETUP EDGE NOT CONFIRMED — no in-band population clears all thresholds.
      Next steps:
        • Adjust bb_std_mult (try 1.5× or 2.5×)
        • Adjust bb_period (try 10 or 30)
        • Compare with setup_bb_edge_check: edge may lie in the broken-below zone
        • Try a different entry_tf in experiment_config.py
```
