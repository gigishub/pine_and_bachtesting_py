# Bear Strategy — RSI Setup Edge Check  (entry_tf=4h)

```text

── Per-Pair Results ──

  BTCUSDT
               wr_%     pf   dur  n_trades
population                                
regime_only   43.61  1.160  22.3      5886
rsi_30_50     44.05  1.181  28.7      1026
rsi_below_50  43.89  1.173  30.0      1039
rsi_above_30  43.64  1.161  22.1      5873
    rsi_30_50 covers 17.4% of regime bars  ⚠️  LOW COVERAGE

  ETHUSDT
               wr_%     pf   dur  n_trades
population                                
regime_only   41.97  1.085  22.5      5976
rsi_30_50     46.94  1.327  29.6      1063
rsi_below_50  46.74  1.316  30.3      1072
rsi_above_30  42.00  1.086  22.4      5967
    rsi_30_50 covers 17.8% of regime bars  ⚠️  LOW COVERAGE

  SOLUSDT
               wr_%     pf   dur  n_trades
population                                
regime_only   43.36  1.148  22.3      5581
rsi_30_50     46.54  1.306  33.8       982
rsi_below_50  46.54  1.306  33.8       982
rsi_above_30  43.36  1.148  22.3      5581
    rsi_30_50 covers 17.6% of regime bars  ⚠️  LOW COVERAGE

  BNBUSDT
               wr_%     pf   dur  n_trades
population                                
regime_only   45.44  1.249  19.0      5046
rsi_30_50     49.30  1.459  23.4       787
rsi_below_50  48.99  1.441  23.6       796
rsi_above_30  45.48  1.251  18.9      5037
    rsi_30_50 covers 15.6% of regime bars  ⚠️  LOW COVERAGE

  XRPUSDT
               wr_%     pf   dur  n_trades
population                                
regime_only   43.64  1.162  23.9      6141
rsi_30_50     41.40  1.060  45.8       983
rsi_below_50  41.28  1.054  46.6       986
rsi_above_30  43.66  1.163  23.8      6138
    rsi_30_50 covers 16.0% of regime bars  ⚠️  LOW COVERAGE

── RSI Setup Edge Verdict ──

  Baseline (regime_only):  avg WR 43.6%  avg PF 1.161

  rsi_30_50       avg WR lift +2.04pp  avg PF 1.267  avg PF lift +0.106  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 44.05%  lift +0.44pp / req 3.87pp  PF 1.181  lift +0.021 / req 0.100  trades 1,026  cov 17.4% ⚠️  ❌
    ETHUSDT     WR 46.94%  lift +4.97pp / req 3.78pp  PF 1.327  lift +0.242 / req 0.100  trades 1,063  cov 17.8% ⚠️  ❌
    SOLUSDT     WR 46.54%  lift +3.18pp / req 3.95pp  PF 1.306  lift +0.157 / req 0.100  trades 982  cov 17.6% ⚠️  ❌
    BNBUSDT     WR 49.30%  lift +3.86pp / req 4.44pp  PF 1.459  lift +0.209 / req 0.100  trades 787  cov 15.6% ⚠️  ❌
    XRPUSDT     WR 41.40%  lift -2.24pp / req 3.95pp  PF 1.060  lift -0.102 / req 0.100  trades 983  cov 16.0% ⚠️  ❌

  rsi_below_50    avg WR lift +1.88pp  avg PF 1.258  avg PF lift +0.097  pairs ≥ threshold: 1/5  ❌
    BTCUSDT     WR 43.89%  lift +0.28pp / req 3.85pp  PF 1.173  lift +0.013 / req 0.100  trades 1,039  ❌
    ETHUSDT     WR 46.74%  lift +4.77pp / req 3.77pp  PF 1.316  lift +0.231 / req 0.100  trades 1,072  ✅
    SOLUSDT     WR 46.54%  lift +3.18pp / req 3.95pp  PF 1.306  lift +0.157 / req 0.100  trades 982  ❌
    BNBUSDT     WR 48.99%  lift +3.55pp / req 4.41pp  PF 1.441  lift +0.192 / req 0.100  trades 796  ❌
    XRPUSDT     WR 41.28%  lift -2.36pp / req 3.95pp  PF 1.054  lift -0.107 / req 0.100  trades 986  ❌

  rsi_above_30    avg WR lift +0.02pp  avg PF 1.162  avg PF lift +0.001  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 43.64%  lift +0.03pp / req 1.62pp  PF 1.161  lift +0.001 / req 0.100  trades 5,873  ❌
    ETHUSDT     WR 42.00%  lift +0.03pp / req 1.60pp  PF 1.086  lift +0.001 / req 0.100  trades 5,967  ❌
    SOLUSDT     WR 43.36%  lift +0.00pp / req 1.66pp  PF 1.148  lift +0.000 / req 0.100  trades 5,581  ❌
    BNBUSDT     WR 45.48%  lift +0.04pp / req 1.75pp  PF 1.251  lift +0.002 / req 0.100  trades 5,037  ❌
    XRPUSDT     WR 43.66%  lift +0.02pp / req 1.58pp  PF 1.163  lift +0.001 / req 0.100  trades 6,138  ❌

  Thresholds: WR lift > 2.5×sqrt(p(1-p)/n),  PF lift > 0.02/0.05/0.10 by n,  trades > 1,000,  consistent across ≥ 4 of 5 pairs

  ❌  RSI SETUP EDGE NOT CONFIRMED — no RSI population clears all thresholds.
      Next steps:
        • Adjust rsi_upper (try 45 or 55)
        • Adjust rsi_lower (try 20 or 35)
        • Adjust rsi_period (try 7 or 21)
        • Try a different entry_tf in config.py
```
