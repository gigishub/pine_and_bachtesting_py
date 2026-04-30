# SuperTrend Setup Edge Check

```text

── Per-Pair Results ──

  BTCUSDT
                     wr_%     pf  dur  n_trades
population                                     
regime_only         36.21  1.135  7.6     23544
st_bear             36.10  1.130  7.6     13933
st_near_resistance  29.38  0.832  9.5       439
st_extended         36.32  1.141  7.5     13494
    st_bear covers 59.2% of regime bars  

  ETHUSDT
                     wr_%     pf   dur  n_trades
population                                      
regime_only         37.03  1.176   7.1     23904
st_bear             36.90  1.170   7.1     14210
st_near_resistance  38.21  1.237  13.8       513
st_extended         36.85  1.167   6.9     13697
    st_bear covers 59.4% of regime bars  

  SOLUSDT
                     wr_%     pf  dur  n_trades
population                                     
regime_only         37.49  1.199  7.0     22390
st_bear             36.86  1.167  7.0     13349
st_near_resistance  32.45  0.961  8.0       416
st_extended         37.00  1.175  7.0     12933
    st_bear covers 59.6% of regime bars  

  BNBUSDT
                     wr_%     pf  dur  n_trades
population                                     
regime_only         36.49  1.149  6.8     20249
st_bear             36.57  1.153  6.6     11811
st_near_resistance  30.52  0.879  7.3       403
st_extended         36.78  1.164  6.6     11408
    st_bear covers 58.3% of regime bars  

  XRPUSDT
                     wr_%     pf   dur  n_trades
population                                      
regime_only         39.15  1.287   7.7     24600
st_bear             39.60  1.311   8.0     14782
st_near_resistance  42.09  1.454  23.2       468
st_extended         39.51  1.307   7.5     14314
    st_bear covers 60.1% of regime bars  

── SuperTrend Setup Edge Verdict ──

  Baseline (regime_only):  avg WR 37.3%  avg PF 1.189

  st_bear               avg WR lift -0.07pp  avg PF 1.186  avg PF lift -0.003  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 36.10%  lift -0.11pp / req 1.02pp  PF 1.130  lift -0.005 / req 0.050  trades 13,933  cov 59.2%  ❌
    ETHUSDT     WR 36.90%  lift -0.12pp / req 1.01pp  PF 1.170  lift -0.006 / req 0.050  trades 14,210  cov 59.4%  ❌
    SOLUSDT     WR 36.86%  lift -0.63pp / req 1.05pp  PF 1.167  lift -0.032 / req 0.050  trades 13,349  cov 59.6%  ❌
    BNBUSDT     WR 36.57%  lift +0.08pp / req 1.11pp  PF 1.153  lift +0.004 / req 0.050  trades 11,811  cov 58.3%  ❌
    XRPUSDT     WR 39.60%  lift +0.45pp / req 1.00pp  PF 1.311  lift +0.024 / req 0.050  trades 14,782  cov 60.1%  ❌

  st_near_resistance    avg WR lift -2.74pp  avg PF 1.072  avg PF lift -0.117  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 29.38%  lift -6.83pp / req 5.73pp  PF 0.832  lift -0.303 / req 0.100  trades 439  ❌
    ETHUSDT     WR 38.21%  lift +1.18pp / req 5.33pp  PF 1.237  lift +0.061 / req 0.100  trades 513  ❌
    SOLUSDT     WR 32.45%  lift -5.04pp / req 5.93pp  PF 0.961  lift -0.239 / req 0.100  trades 416  ❌
    BNBUSDT     WR 30.52%  lift -5.97pp / req 6.00pp  PF 0.879  lift -0.271 / req 0.100  trades 403  ❌
    XRPUSDT     WR 42.09%  lift +2.94pp / req 5.64pp  PF 1.454  lift +0.167 / req 0.100  trades 468  ❌

  st_extended           avg WR lift +0.02pp  avg PF 1.191  avg PF lift +0.001  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 36.32%  lift +0.11pp / req 1.03pp  PF 1.141  lift +0.005 / req 0.050  trades 13,494  ❌
    ETHUSDT     WR 36.85%  lift -0.17pp / req 1.03pp  PF 1.167  lift -0.009 / req 0.050  trades 13,697  ❌
    SOLUSDT     WR 37.00%  lift -0.49pp / req 1.06pp  PF 1.175  lift -0.025 / req 0.050  trades 12,933  ❌
    BNBUSDT     WR 36.78%  lift +0.29pp / req 1.13pp  PF 1.164  lift +0.014 / req 0.050  trades 11,408  ❌
    XRPUSDT     WR 39.51%  lift +0.36pp / req 1.02pp  PF 1.307  lift +0.020 / req 0.050  trades 14,314  ❌

  Thresholds: WR lift > 2.5×sqrt(p(1-p)/n),  PF lift > 0.02/0.05/0.10 by n,  trades > 1,000,  consistent across ≥ 4 of 5 pairs

  ❌  SUPERTREND SETUP EDGE NOT CONFIRMED — no population clears all thresholds.
      Next steps:
        • Adjust st_length (try 7 or 14)
        • Adjust st_multiplier (try 2.0 or 4.0)
        • Adjust proximity_atr_mult (try 1.0 or 0.25)
        • Try a different entry_tf in config.py
        • Re-examine whether setup layer is needed before trigger layer
```
