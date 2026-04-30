# Bear Strategy — RSI Setup Edge Check  (entry_tf=15m)

```text

── Per-Pair Results ──

  BTCUSDT
               wr_%     pf   dur  n_trades
population                                
regime_only   42.67  1.116  21.1     94176
rsi_30_50     43.46  1.153  27.7     10372
rsi_below_50  43.49  1.155  28.5     10434
rsi_above_30  42.67  1.116  21.0     94114
    rsi_30_50 covers 11.0% of regime bars  ⚠️  LOW COVERAGE

  ETHUSDT
               wr_%     pf   dur  n_trades
population                                
regime_only   43.60  1.159  20.1     95616
rsi_30_50     45.80  1.267  25.2     11243
rsi_below_50  45.88  1.272  25.7     11303
rsi_above_30  43.59  1.159  20.1     95556
    rsi_30_50 covers 11.8% of regime bars  ⚠️  LOW COVERAGE

  SOLUSDT
               wr_%     pf   dur  n_trades
population                                
regime_only   43.90  1.174  20.1     89549
rsi_30_50     44.78  1.216  25.0     10601
rsi_below_50  44.76  1.215  25.2     10644
rsi_above_30  43.90  1.174  20.0     89506
    rsi_30_50 covers 11.8% of regime bars  ⚠️  LOW COVERAGE

  BNBUSDT
               wr_%     pf   dur  n_trades
population                                
regime_only   43.39  1.150  18.4     81006
rsi_30_50     44.88  1.221  24.1      9132
rsi_below_50  44.90  1.222  24.4      9185
rsi_above_30  43.38  1.149  18.3     80953
    rsi_30_50 covers 11.3% of regime bars  ⚠️  LOW COVERAGE

  XRPUSDT
               wr_%     pf   dur  n_trades
population                                
regime_only   45.23  1.239  21.8     98398
rsi_30_50     45.26  1.240  28.8     11166
rsi_below_50  45.20  1.237  28.9     11209
rsi_above_30  45.24  1.239  21.8     98355
    rsi_30_50 covers 11.3% of regime bars  ⚠️  LOW COVERAGE

── RSI Setup Edge Verdict ──

  Baseline (regime_only):  avg WR 43.8%  avg PF 1.168

  rsi_30_50       avg WR lift +1.08pp  avg PF 1.220  avg PF lift +0.052  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 43.46%  lift +0.79pp / req 1.21pp  PF 1.153  lift +0.037 / req 0.050  trades 10,372  cov 11.0% ⚠️  ❌
    ETHUSDT     WR 45.80%  lift +2.20pp / req 1.17pp  PF 1.267  lift +0.108 / req 0.050  trades 11,243  cov 11.8% ⚠️  ❌
    SOLUSDT     WR 44.78%  lift +0.88pp / req 1.20pp  PF 1.216  lift +0.043 / req 0.050  trades 10,601  cov 11.8% ⚠️  ❌
    BNBUSDT     WR 44.88%  lift +1.49pp / req 1.30pp  PF 1.221  lift +0.071 / req 0.100  trades 9,132  cov 11.3% ⚠️  ❌
    XRPUSDT     WR 45.26%  lift +0.03pp / req 1.18pp  PF 1.240  lift +0.001 / req 0.050  trades 11,166  cov 11.3% ⚠️  ❌

  rsi_below_50    avg WR lift +1.09pp  avg PF 1.220  avg PF lift +0.053  pairs ≥ threshold: 1/5  ❌
    BTCUSDT     WR 43.49%  lift +0.82pp / req 1.21pp  PF 1.155  lift +0.038 / req 0.050  trades 10,434  ❌
    ETHUSDT     WR 45.88%  lift +2.28pp / req 1.17pp  PF 1.272  lift +0.112 / req 0.050  trades 11,303  ✅
    SOLUSDT     WR 44.76%  lift +0.86pp / req 1.20pp  PF 1.215  lift +0.042 / req 0.050  trades 10,644  ❌
    BNBUSDT     WR 44.90%  lift +1.51pp / req 1.29pp  PF 1.222  lift +0.073 / req 0.100  trades 9,185  ❌
    XRPUSDT     WR 45.20%  lift -0.04pp / req 1.18pp  PF 1.237  lift -0.002 / req 0.050  trades 11,209  ❌

  rsi_above_30    avg WR lift -0.00pp  avg PF 1.168  avg PF lift -0.000  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 42.67%  lift -0.00pp / req 0.40pp  PF 1.116  lift -0.000 / req 0.020  trades 94,114  ❌
    ETHUSDT     WR 43.59%  lift -0.01pp / req 0.40pp  PF 1.159  lift -0.001 / req 0.020  trades 95,556  ❌
    SOLUSDT     WR 43.90%  lift +0.00pp / req 0.41pp  PF 1.174  lift +0.000 / req 0.020  trades 89,506  ❌
    BNBUSDT     WR 43.38%  lift -0.00pp / req 0.44pp  PF 1.149  lift -0.000 / req 0.020  trades 80,953  ❌
    XRPUSDT     WR 45.24%  lift +0.01pp / req 0.40pp  PF 1.239  lift +0.000 / req 0.020  trades 98,355  ❌

  Thresholds: WR lift > 2.5×sqrt(p(1-p)/n),  PF lift > 0.02/0.05/0.10 by n,  trades > 1,000,  consistent across ≥ 4 of 5 pairs

  ❌  RSI SETUP EDGE NOT CONFIRMED — no RSI population clears all thresholds.
      Next steps:
        • Adjust rsi_upper (try 45 or 55)
        • Adjust rsi_lower (try 20 or 35)
        • Adjust rsi_period (try 7 or 21)
        • Try a different entry_tf in config.py
```
