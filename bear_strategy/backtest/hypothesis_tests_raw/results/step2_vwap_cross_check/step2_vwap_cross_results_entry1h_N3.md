# VWAP Cross-Below Setup Edge Check

```text

── Per-Pair Results ──

  BTCUSDT
                     wr_%     pf   dur  n_trades
population                                      
regime_only         44.25  1.191  20.4     23544
vwap_cross_below    43.75  1.167  18.7      2489
vwap_cross_below_N  43.46  1.153  18.8      1254
    vwap_cross_below covers 10.6% of regime bars  
    vwap_cross_below_N covers 5.3% of regime bars  

  ETHUSDT
                     wr_%     pf   dur  n_trades
population                                      
regime_only         45.01  1.228  19.9     23904
vwap_cross_below    45.00  1.227  18.1      2440
vwap_cross_below_N  45.00  1.227  19.2      1231
    vwap_cross_below covers 10.2% of regime bars  
    vwap_cross_below_N covers 5.1% of regime bars  

  SOLUSDT
                     wr_%     pf   dur  n_trades
population                                      
regime_only         44.84  1.219  19.5     22371
vwap_cross_below    45.19  1.237  18.4      2297
vwap_cross_below_N  44.16  1.186  18.9      1164
    vwap_cross_below covers 10.3% of regime bars  
    vwap_cross_below_N covers 5.2% of regime bars  

  BNBUSDT
                     wr_%     pf   dur  n_trades
population                                      
regime_only         44.88  1.222  19.0     20243
vwap_cross_below    45.60  1.257  17.7      2011
vwap_cross_below_N  44.72  1.214  18.0      1042
    vwap_cross_below covers 9.9% of regime bars  
    vwap_cross_below_N covers 5.1% of regime bars  

  XRPUSDT
                     wr_%     pf   dur  n_trades
population                                      
regime_only         47.17  1.339  22.3     24598
vwap_cross_below    49.02  1.442  21.2      2558
vwap_cross_below_N  49.13  1.449  22.7      1323
    vwap_cross_below covers 10.4% of regime bars  
    vwap_cross_below_N covers 5.4% of regime bars  

── VWAP Cross-Below Edge Verdict ──

  Baseline (regime_only):  avg WR 45.2%  avg PF 1.240
  Config: vwap_anchor=daily  min_bars_above=3

  vwap_cross_below          avg WR lift +0.48pp  avg PF 1.266  avg PF lift +0.026  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 43.75%  lift -0.50pp / req 2.49pp  PF 1.167  lift -0.024 / req 0.100  trades 2,489  cov 10.6%  ❌
    ETHUSDT     WR 45.00%  lift -0.01pp / req 2.52pp  PF 1.227  lift -0.000 / req 0.100  trades 2,440  cov 10.2%  ❌
    SOLUSDT     WR 45.19%  lift +0.35pp / req 2.59pp  PF 1.237  lift +0.017 / req 0.100  trades 2,297  cov 10.3%  ❌
    BNBUSDT     WR 45.60%  lift +0.71pp / req 2.77pp  PF 1.257  lift +0.036 / req 0.100  trades 2,011  cov 9.9%  ❌
    XRPUSDT     WR 49.02%  lift +1.86pp / req 2.47pp  PF 1.442  lift +0.103 / req 0.100  trades 2,558  cov 10.4%  ❌

  vwap_cross_below_N        avg WR lift +0.06pp  avg PF 1.246  avg PF lift +0.006  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 43.46%  lift -0.79pp / req 3.51pp  PF 1.153  lift -0.038 / req 0.100  trades 1,254  cov 5.3%  ❌
    ETHUSDT     WR 45.00%  lift -0.01pp / req 3.54pp  PF 1.227  lift -0.000 / req 0.100  trades 1,231  cov 5.1%  ❌
    SOLUSDT     WR 44.16%  lift -0.68pp / req 3.64pp  PF 1.186  lift -0.033 / req 0.100  trades 1,164  cov 5.2%  ❌
    BNBUSDT     WR 44.72%  lift -0.16pp / req 3.85pp  PF 1.214  lift -0.008 / req 0.100  trades 1,042  cov 5.1%  ❌
    XRPUSDT     WR 49.13%  lift +1.96pp / req 3.43pp  PF 1.449  lift +0.110 / req 0.100  trades 1,323  cov 5.4%  ❌

  Thresholds: WR lift > 2.5×sqrt(p(1-p)/n),  PF lift > 0.02/0.05/0.10 by n,  trades > 500,  ≥ 4 of 5 pairs

  ❌  VWAP CROSS EDGE NOT CONFIRMED — no population clears all thresholds.
      Next steps:
        • Adjust min_bars_above (currently 3) — try 2 or 5
        • Try vwap_anchor = 'weekly' (currently 'daily')
        • Try a different entry_tf in config.py
        • VWAP crosses may need volume confirmation for consistent edge
```
