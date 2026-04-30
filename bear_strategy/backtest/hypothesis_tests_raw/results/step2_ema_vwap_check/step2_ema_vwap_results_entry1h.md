# EMA20 / VWAP Setup Edge Check

```text

── Per-Pair Results ──

  BTCUSDT
                  wr_%     pf   dur  n_trades
population                                   
regime_only      44.38  1.197  19.3     23544
below_ema20      45.25  1.240  19.7     13016
below_vwap       44.66  1.211  19.2     12113
below_both       44.97  1.226  19.4     10125
below_vwap_1std  42.82  1.124  18.7      2662
    below_ema20 covers 55.3% of regime bars  
    below_vwap covers 51.4% of regime bars  
    below_both covers 43.0% of regime bars  
    below_vwap_1std covers 11.3% of regime bars  ⚠️  LOW

  ETHUSDT
                  wr_%     pf   dur  n_trades
population                                   
regime_only      45.28  1.241  18.9     23904
below_ema20      46.00  1.278  18.7     13184
below_vwap       46.33  1.295  18.4     12335
below_both       46.31  1.294  18.5     10431
below_vwap_1std  44.97  1.226  18.6      2586
    below_ema20 covers 55.2% of regime bars  
    below_vwap covers 51.6% of regime bars  
    below_both covers 43.6% of regime bars  
    below_vwap_1std covers 10.8% of regime bars  ⚠️  LOW

  SOLUSDT
                  wr_%     pf   dur  n_trades
population                                   
regime_only      44.84  1.219  18.9     22370
below_ema20      45.89  1.272  18.6     12803
below_vwap       45.16  1.235  18.4     11884
below_both       45.32  1.243  18.5     10099
below_vwap_1std  43.37  1.149  19.4      2769
    below_ema20 covers 57.2% of regime bars  
    below_vwap covers 53.1% of regime bars  
    below_both covers 45.1% of regime bars  
    below_vwap_1std covers 12.4% of regime bars  ⚠️  LOW

  BNBUSDT
                  wr_%     pf   dur  n_trades
population                                   
regime_only      44.93  1.224  18.6     20243
below_ema20      45.79  1.267  18.1     10902
below_vwap       45.86  1.271  18.1     10477
below_both       46.30  1.293  17.9      8719
below_vwap_1std  45.18  1.236  17.8      2457
    below_ema20 covers 53.9% of regime bars  
    below_vwap covers 51.8% of regime bars  
    below_both covers 43.1% of regime bars  
    below_vwap_1std covers 12.1% of regime bars  ⚠️  LOW

  XRPUSDT
                  wr_%     pf   dur  n_trades
population                                   
regime_only      47.29  1.346  20.9     24600
below_ema20      48.00  1.385  22.2     13953
below_vwap       48.00  1.385  20.6     12918
below_both       48.60  1.418  20.7     10938
below_vwap_1std  47.40  1.352  21.5      2947
    below_ema20 covers 56.7% of regime bars  
    below_vwap covers 52.5% of regime bars  
    below_both covers 44.5% of regime bars  
    below_vwap_1std covers 12.0% of regime bars  ⚠️  LOW

── EMA20 / VWAP Setup Edge Verdict ──

  Baseline (regime_only):  avg WR 45.3%  avg PF 1.245

  below_ema20     avg WR lift +0.84pp  avg PF 1.288  avg PF lift +0.043  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 45.25%  lift +0.87pp / req 1.09pp  PF 1.240  lift +0.043 / req 0.050  trades 13,016  cov 55.3%  ❌
    ETHUSDT     WR 46.00%  lift +0.73pp / req 1.08pp  PF 1.278  lift +0.037 / req 0.050  trades 13,184  cov 55.2%  ❌
    SOLUSDT     WR 45.89%  lift +1.05pp / req 1.10pp  PF 1.272  lift +0.053 / req 0.050  trades 12,803  cov 57.2%  ❌
    BNBUSDT     WR 45.79%  lift +0.86pp / req 1.19pp  PF 1.267  lift +0.043 / req 0.050  trades 10,902  cov 53.9%  ❌
    XRPUSDT     WR 48.00%  lift +0.71pp / req 1.06pp  PF 1.385  lift +0.039 / req 0.050  trades 13,953  cov 56.7%  ❌

  below_vwap      avg WR lift +0.66pp  avg PF 1.279  avg PF lift +0.034  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 44.66%  lift +0.28pp / req 1.13pp  PF 1.211  lift +0.014 / req 0.050  trades 12,113  cov 51.4%  ❌
    ETHUSDT     WR 46.33%  lift +1.05pp / req 1.12pp  PF 1.295  lift +0.054 / req 0.050  trades 12,335  cov 51.6%  ❌
    SOLUSDT     WR 45.16%  lift +0.32pp / req 1.14pp  PF 1.235  lift +0.016 / req 0.050  trades 11,884  cov 53.1%  ❌
    BNBUSDT     WR 45.86%  lift +0.93pp / req 1.21pp  PF 1.271  lift +0.047 / req 0.050  trades 10,477  cov 51.8%  ❌
    XRPUSDT     WR 48.00%  lift +0.71pp / req 1.10pp  PF 1.385  lift +0.039 / req 0.050  trades 12,918  cov 52.5%  ❌

  below_both      avg WR lift +0.96pp  avg PF 1.295  avg PF lift +0.050  pairs ≥ threshold: 1/5  ❌
    BTCUSDT     WR 44.97%  lift +0.58pp / req 1.23pp  PF 1.226  lift +0.029 / req 0.050  trades 10,125  cov 43.0%  ❌
    ETHUSDT     WR 46.31%  lift +1.04pp / req 1.22pp  PF 1.294  lift +0.053 / req 0.050  trades 10,431  cov 43.6%  ❌
    SOLUSDT     WR 45.32%  lift +0.48pp / req 1.24pp  PF 1.243  lift +0.024 / req 0.050  trades 10,099  cov 45.1%  ❌
    BNBUSDT     WR 46.30%  lift +1.37pp / req 1.33pp  PF 1.293  lift +0.070 / req 0.100  trades 8,719  cov 43.1%  ❌
    XRPUSDT     WR 48.60%  lift +1.31pp / req 1.19pp  PF 1.418  lift +0.072 / req 0.050  trades 10,938  cov 44.5%  ✅

  below_vwap_1std  avg WR lift -0.59pp  avg PF 1.217  avg PF lift -0.028  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 42.82%  lift -1.56pp / req 2.41pp  PF 1.124  lift -0.074 / req 0.100  trades 2,662  cov 11.3% ⚠️  ❌
    ETHUSDT     WR 44.97%  lift -0.30pp / req 2.45pp  PF 1.226  lift -0.015 / req 0.100  trades 2,586  cov 10.8% ⚠️  ❌
    SOLUSDT     WR 43.37%  lift -1.46pp / req 2.36pp  PF 1.149  lift -0.070 / req 0.100  trades 2,769  cov 12.4% ⚠️  ❌
    BNBUSDT     WR 45.18%  lift +0.25pp / req 2.51pp  PF 1.236  lift +0.012 / req 0.100  trades 2,457  cov 12.1% ⚠️  ❌
    XRPUSDT     WR 47.40%  lift +0.11pp / req 2.30pp  PF 1.352  lift +0.006 / req 0.100  trades 2,947  cov 12.0% ⚠️  ❌

  Thresholds: WR lift > 2.5×sqrt(p(1-p)/n),  PF lift > 0.02/0.05/0.10 by n,  trades > 500,  consistent across ≥ 4 of 5 pairs

  ❌  EMA20/VWAP EDGE NOT CONFIRMED — no filter clears all thresholds.
      Next steps:
        • Try ema_period = 10 or 50
        • Try a different entry_tf in config.py
        • Note: in a strong bear regime most bars are already below EMA20
          — high coverage may dilute the signal vs the baseline
```
