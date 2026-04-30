# VWAP Rejection Candle Setup Edge Check

```text

── Per-Pair Results ──

  BTCUSDT
                       wr_%     pf   dur  n_trades
population                                        
regime_only           44.25  1.191  20.4     23544
vwap_rejection        44.12  1.184  19.5      3173
vwap_rejection_clean  43.96  1.177  20.7       878
    vwap_rejection covers 13.5% of regime bars  
    vwap_rejection_clean covers 3.7% of regime bars  ⚠️  LOW

  ETHUSDT
                       wr_%     pf   dur  n_trades
population                                        
regime_only           45.01  1.228  19.9     23904
vwap_rejection        45.06  1.230  19.0      3136
vwap_rejection_clean  45.76  1.265  17.8       837
    vwap_rejection covers 13.1% of regime bars  
    vwap_rejection_clean covers 3.5% of regime bars  ⚠️  LOW

  SOLUSDT
                       wr_%     pf   dur  n_trades
population                                        
regime_only           44.84  1.219  19.5     22371
vwap_rejection        45.18  1.236  19.5      2873
vwap_rejection_clean  48.24  1.398  20.1       823
    vwap_rejection covers 12.8% of regime bars  
    vwap_rejection_clean covers 3.7% of regime bars  ⚠️  LOW

  BNBUSDT
                       wr_%     pf   dur  n_trades
population                                        
regime_only           44.88  1.222  19.0     20243
vwap_rejection        45.65  1.260  18.3      2572
vwap_rejection_clean  46.00  1.278  18.7       826
    vwap_rejection covers 12.7% of regime bars  
    vwap_rejection_clean covers 4.1% of regime bars  ⚠️  LOW

  XRPUSDT
                       wr_%     pf   dur  n_trades
population                                        
regime_only           47.17  1.339  22.3     24598
vwap_rejection        48.83  1.431  23.1      3281
vwap_rejection_clean  48.53  1.415  21.1       853
    vwap_rejection covers 13.3% of regime bars  
    vwap_rejection_clean covers 3.5% of regime bars  ⚠️  LOW

── VWAP Rejection Candle Edge Verdict ──

  Baseline (regime_only):  avg WR 45.2%  avg PF 1.240
  Config: vwap_anchor=daily  max_wick_ratio=0.20

  vwap_rejection            avg WR lift +0.54pp  avg PF 1.268  avg PF lift +0.029  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 44.12%  lift -0.13pp / req 2.20pp  PF 1.184  lift -0.006 / req 0.100  trades 3,173  cov 13.5%  ❌
    ETHUSDT     WR 45.06%  lift +0.05pp / req 2.22pp  PF 1.230  lift +0.002 / req 0.100  trades 3,136  cov 13.1%  ❌
    SOLUSDT     WR 45.18%  lift +0.34pp / req 2.32pp  PF 1.236  lift +0.017 / req 0.100  trades 2,873  cov 12.8%  ❌
    BNBUSDT     WR 45.65%  lift +0.76pp / req 2.45pp  PF 1.260  lift +0.038 / req 0.100  trades 2,572  cov 12.7%  ❌
    XRPUSDT     WR 48.83%  lift +1.66pp / req 2.18pp  PF 1.431  lift +0.092 / req 0.100  trades 3,281  cov 13.3%  ❌

  vwap_rejection_clean      avg WR lift +1.27pp  avg PF 1.307  avg PF lift +0.067  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 43.96%  lift -0.29pp / req 4.19pp  PF 1.177  lift -0.014 / req 0.100  trades 878  cov 3.7% ⚠️  ❌
    ETHUSDT     WR 45.76%  lift +0.75pp / req 4.30pp  PF 1.265  lift +0.038 / req 0.100  trades 837  cov 3.5% ⚠️  ❌
    SOLUSDT     WR 48.24%  lift +3.40pp / req 4.33pp  PF 1.398  lift +0.179 / req 0.100  trades 823  cov 3.7% ⚠️  ❌
    BNBUSDT     WR 46.00%  lift +1.12pp / req 4.33pp  PF 1.278  lift +0.056 / req 0.100  trades 826  cov 4.1% ⚠️  ❌
    XRPUSDT     WR 48.53%  lift +1.37pp / req 4.27pp  PF 1.415  lift +0.075 / req 0.100  trades 853  cov 3.5% ⚠️  ❌

  Thresholds: WR lift > 2.5×sqrt(p(1-p)/n),  PF lift > 0.02/0.05/0.10 by n,  trades > 500,  consistent across ≥ 4 of 5 pairs

  ❌  VWAP REJECTION EDGE NOT CONFIRMED — no pattern clears all thresholds.
      Next steps:
        • Try vwap_anchor = 'weekly' (VWAP as swing resistance)
        • Loosen max_wick_ratio (currently 0.20) → try 0.30
        • Try a different entry_tf in config.py
        • VWAP rejections may need a trigger filter (e.g. volume spike)
          before they produce consistent edge
```
