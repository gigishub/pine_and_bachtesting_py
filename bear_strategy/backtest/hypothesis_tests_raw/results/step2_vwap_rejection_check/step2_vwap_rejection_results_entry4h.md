# VWAP Rejection Candle Setup Edge Check

```text

── Per-Pair Results ──

  BTCUSDT
                       wr_%     pf   dur  n_trades
population                                        
regime_only           43.61  1.160  22.3      5886
vwap_rejection        44.96  1.225  22.0      1668
vwap_rejection_clean  43.02  1.132  20.5       351
    vwap_rejection covers 28.3% of regime bars  
    vwap_rejection_clean covers 6.0% of regime bars  

  ETHUSDT
                       wr_%     pf   dur  n_trades
population                                        
regime_only           41.97  1.085  22.5      5976
vwap_rejection        42.69  1.117  21.5      1661
vwap_rejection_clean  42.64  1.115  24.1       333
    vwap_rejection covers 27.8% of regime bars  
    vwap_rejection_clean covers 5.6% of regime bars  

  SOLUSDT
                       wr_%     pf   dur  n_trades
population                                        
regime_only           43.36  1.148  22.3      5581
vwap_rejection        44.47  1.201  23.2      1565
vwap_rejection_clean  44.53  1.204  22.0       375
    vwap_rejection covers 28.0% of regime bars  
    vwap_rejection_clean covers 6.7% of regime bars  

  BNBUSDT
                       wr_%     pf   dur  n_trades
population                                        
regime_only           45.44  1.249  19.0      5046
vwap_rejection        47.34  1.348  18.9      1352
vwap_rejection_clean  45.10  1.232  18.7       306
    vwap_rejection covers 26.8% of regime bars  
    vwap_rejection_clean covers 6.1% of regime bars  

  XRPUSDT
                       wr_%     pf   dur  n_trades
population                                        
regime_only           43.64  1.162  23.9      6141
vwap_rejection        43.91  1.174  24.0      1715
vwap_rejection_clean  50.00  1.500  20.7       342
    vwap_rejection covers 27.9% of regime bars  
    vwap_rejection_clean covers 5.6% of regime bars  

── VWAP Rejection Candle Edge Verdict ──

  Baseline (regime_only):  avg WR 43.6%  avg PF 1.161
  Config: vwap_anchor=daily  max_wick_ratio=0.20

  vwap_rejection            avg WR lift +1.07pp  avg PF 1.213  avg PF lift +0.052  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 44.96%  lift +1.35pp / req 3.04pp  PF 1.225  lift +0.065 / req 0.100  trades 1,668  cov 28.3%  ❌
    ETHUSDT     WR 42.69%  lift +0.72pp / req 3.03pp  PF 1.117  lift +0.032 / req 0.100  trades 1,661  cov 27.8%  ❌
    SOLUSDT     WR 44.47%  lift +1.11pp / req 3.13pp  PF 1.201  lift +0.053 / req 0.100  trades 1,565  cov 28.0%  ❌
    BNBUSDT     WR 47.34%  lift +1.90pp / req 3.39pp  PF 1.348  lift +0.099 / req 0.100  trades 1,352  cov 26.8%  ❌
    XRPUSDT     WR 43.91%  lift +0.27pp / req 2.99pp  PF 1.174  lift +0.013 / req 0.100  trades 1,715  cov 27.9%  ❌

  vwap_rejection_clean      avg WR lift +1.45pp  avg PF 1.237  avg PF lift +0.076  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 43.02%  lift -0.59pp / req 6.62pp  PF 1.133  lift -0.028 / req 0.100  trades 351  cov 6.0%  ❌
    ETHUSDT     WR 42.64%  lift +0.67pp / req 6.76pp  PF 1.115  lift +0.030 / req 0.100  trades 333  cov 5.6%  ❌
    SOLUSDT     WR 44.53%  lift +1.17pp / req 6.40pp  PF 1.204  lift +0.056 / req 0.100  trades 375  cov 6.7%  ❌
    BNBUSDT     WR 45.10%  lift -0.34pp / req 7.12pp  PF 1.232  lift -0.017 / req 0.100  trades 306  cov 6.1%  ❌
    XRPUSDT     WR 50.00%  lift +6.36pp / req 6.70pp  PF 1.500  lift +0.338 / req 0.100  trades 342  cov 5.6%  ❌

  Thresholds: WR lift > 2.5×sqrt(p(1-p)/n),  PF lift > 0.02/0.05/0.10 by n,  trades > 500,  consistent across ≥ 4 of 5 pairs

  ❌  VWAP REJECTION EDGE NOT CONFIRMED — no pattern clears all thresholds.
      Next steps:
        • Try vwap_anchor = 'weekly' (VWAP as swing resistance)
        • Loosen max_wick_ratio (currently 0.20) → try 0.30
        • Try a different entry_tf in config.py
        • VWAP rejections may need a trigger filter (e.g. volume spike)
          before they produce consistent edge
```
