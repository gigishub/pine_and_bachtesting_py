# Bear Strategy — RSI Setup Edge Check  (entry_tf=1h)

```text

── Per-Pair Results ──

  BTCUSDT
               wr_%     pf   dur  n_trades
population                                
regime_only   44.25  1.191  20.4     23544
rsi_30_50     44.48  1.202  28.0      3291
rsi_below_50  44.54  1.205  29.6      3307
rsi_above_30  44.25  1.190  20.2     23528
    rsi_30_50 covers 14.0% of regime bars  ⚠️  LOW COVERAGE

  ETHUSDT
               wr_%     pf   dur  n_trades
population                                
regime_only   45.01  1.228  19.9     23904
rsi_30_50     47.43  1.353  24.8      3498
rsi_below_50  47.50  1.357  26.2      3518
rsi_above_30  45.00  1.227  19.7     23884
    rsi_30_50 covers 14.6% of regime bars  ⚠️  LOW COVERAGE

  SOLUSDT
               wr_%     pf   dur  n_trades
population                                
regime_only   44.84  1.219  19.5     22371
rsi_30_50     45.55  1.255  25.5      3295
rsi_below_50  45.50  1.252  25.6      3310
rsi_above_30  44.85  1.220  19.5     22356
    rsi_30_50 covers 14.7% of regime bars  ⚠️  LOW COVERAGE

  BNBUSDT
               wr_%     pf   dur  n_trades
population                                
regime_only   44.88  1.222  19.0     20243
rsi_30_50     47.30  1.346  23.9      2776
rsi_below_50  47.51  1.358  24.0      2791
rsi_above_30  44.85  1.220  19.0     20228
    rsi_30_50 covers 13.7% of regime bars  ⚠️  LOW COVERAGE

  XRPUSDT
               wr_%     pf   dur  n_trades
population                                
regime_only   47.17  1.339  22.3     24598
rsi_30_50     47.88  1.378  37.5      3262
rsi_below_50  47.86  1.377  38.1      3270
rsi_above_30  47.17  1.339  22.2     24590
    rsi_30_50 covers 13.3% of regime bars  ⚠️  LOW COVERAGE

── RSI Setup Edge Verdict ──

  Baseline (regime_only):  avg WR 45.2%  avg PF 1.240

  rsi_30_50       avg WR lift +1.30pp  avg PF 1.307  avg PF lift +0.067  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 44.48%  lift +0.23pp / req 2.16pp  PF 1.202  lift +0.011 / req 0.100  trades 3,291  cov 14.0% ⚠️  ❌
    ETHUSDT     WR 47.43%  lift +2.42pp / req 2.10pp  PF 1.353  lift +0.125 / req 0.100  trades 3,498  cov 14.6% ⚠️  ❌
    SOLUSDT     WR 45.55%  lift +0.71pp / req 2.17pp  PF 1.255  lift +0.036 / req 0.100  trades 3,295  cov 14.7% ⚠️  ❌
    BNBUSDT     WR 47.30%  lift +2.41pp / req 2.36pp  PF 1.346  lift +0.125 / req 0.100  trades 2,776  cov 13.7% ⚠️  ❌
    XRPUSDT     WR 47.88%  lift +0.72pp / req 2.19pp  PF 1.378  lift +0.039 / req 0.100  trades 3,262  cov 13.3% ⚠️  ❌

  rsi_below_50    avg WR lift +1.35pp  avg PF 1.310  avg PF lift +0.070  pairs ≥ threshold: 2/5  ❌
    BTCUSDT     WR 44.54%  lift +0.29pp / req 2.16pp  PF 1.205  lift +0.014 / req 0.100  trades 3,307  ❌
    ETHUSDT     WR 47.50%  lift +2.49pp / req 2.10pp  PF 1.357  lift +0.129 / req 0.100  trades 3,518  ✅
    SOLUSDT     WR 45.50%  lift +0.66pp / req 2.16pp  PF 1.252  lift +0.033 / req 0.100  trades 3,310  ❌
    BNBUSDT     WR 47.51%  lift +2.63pp / req 2.35pp  PF 1.358  lift +0.136 / req 0.100  trades 2,791  ✅
    XRPUSDT     WR 47.86%  lift +0.69pp / req 2.18pp  PF 1.377  lift +0.038 / req 0.100  trades 3,270  ❌

  rsi_above_30    avg WR lift -0.01pp  avg PF 1.239  avg PF lift -0.000  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 44.25%  lift -0.01pp / req 0.81pp  PF 1.190  lift -0.000 / req 0.050  trades 23,528  ❌
    ETHUSDT     WR 45.00%  lift -0.01pp / req 0.80pp  PF 1.227  lift -0.001 / req 0.050  trades 23,884  ❌
    SOLUSDT     WR 44.85%  lift +0.01pp / req 0.83pp  PF 1.220  lift +0.000 / req 0.050  trades 22,356  ❌
    BNBUSDT     WR 44.85%  lift -0.03pp / req 0.87pp  PF 1.220  lift -0.002 / req 0.050  trades 20,228  ❌
    XRPUSDT     WR 47.17%  lift +0.00pp / req 0.80pp  PF 1.339  lift +0.000 / req 0.050  trades 24,590  ❌

  Thresholds: WR lift > 2.5×sqrt(p(1-p)/n),  PF lift > 0.02/0.05/0.10 by n,  trades > 1,000,  consistent across ≥ 4 of 5 pairs

  ❌  RSI SETUP EDGE NOT CONFIRMED — no RSI population clears all thresholds.
      Next steps:
        • Adjust rsi_upper (try 45 or 55)
        • Adjust rsi_lower (try 20 or 35)
        • Adjust rsi_period (try 7 or 21)
        • Try a different entry_tf in config.py
```
