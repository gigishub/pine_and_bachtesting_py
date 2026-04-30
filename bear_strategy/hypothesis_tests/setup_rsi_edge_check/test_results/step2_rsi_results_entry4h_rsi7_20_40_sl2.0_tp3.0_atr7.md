# Bear Strategy — RSI Setup Edge Check  (entry_tf=4h)

## Test Parameters

| Parameter | Value |
|-----------|-------|
| `entry_tf` | `4h` |
| `stop_atr_mult` | `2.0` |
| `target_atr_mult` | `3.0` |
| `atr_period` | `7` |
| `rsi_period` | `7` |
| `rsi_lower` | `20` |
| `rsi_upper` | `40` |

```text

── Per-Pair Results ──

  BTCUSDT
               wr_%     pf   dur  n_trades
regime_only   43.61  1.160  22.3      5886
rsi_20_40     42.43  1.105  22.1      1855
rsi_below_40  42.34  1.102  25.3      2187
rsi_above_20  43.72  1.165  21.1      5554
    rsi_20_40 covers 31.5% of regime bars  

  ETHUSDT
               wr_%     pf   dur  n_trades
regime_only   41.97  1.085  22.5      5976
rsi_20_40     44.24  1.190  22.9      1822
rsi_below_40  43.55  1.157  26.4      2211
rsi_above_20  42.08  1.090  21.1      5587
    rsi_20_40 covers 30.5% of regime bars  

  SOLUSDT
               wr_%     pf   dur  n_trades
regime_only   43.36  1.148  22.3      5581
rsi_20_40     46.81  1.320  21.8      1880
rsi_below_40  45.91  1.273  26.2      2165
rsi_above_20  43.54  1.157  20.6      5296
    rsi_20_40 covers 33.7% of regime bars  

  BNBUSDT
               wr_%     pf   dur  n_trades
regime_only   45.44  1.249  19.0      5046
rsi_20_40     49.83  1.490  20.8      1481
rsi_below_40  49.26  1.456  21.9      1754
rsi_above_20  45.40  1.247  18.5      4773
    rsi_20_40 covers 29.3% of regime bars  

  XRPUSDT
               wr_%     pf   dur  n_trades
regime_only   43.64  1.162  23.9      6141
rsi_20_40     44.32  1.194  24.7      1891
rsi_below_40  43.26  1.143  31.4      2187
rsi_above_20  44.00  1.179  21.4      5845
    rsi_20_40 covers 30.8% of regime bars  

── RSI Setup Edge Verdict ──

  Baseline (regime_only):  avg WR 43.6%  avg PF 1.161

  rsi_20_40       avg WR lift +1.92pp  avg PF 1.260  avg PF lift +0.099  pairs ≥ threshold: 3/5  ❌  ⚠️ WR 3p  ⚠️ low count 1p  ⚠️ weak regime 1p
    BTCUSDT     WR 42.43%  lift -1.19pp / req 2.88pp  PF 1.105  lift -0.055 / req 0.100  trades 1,855  cov 31.5%  ⚠️ WR  ❌
    ETHUSDT     WR 44.24%  lift +2.27pp / req 2.89pp  PF 1.190  lift +0.105 / req 0.100  trades 1,822  cov 30.5%  ⚠️ WR  ✅
    SOLUSDT     WR 46.81%  lift +3.45pp / req 2.86pp  PF 1.320  lift +0.172 / req 0.100  trades 1,880  cov 33.7%  ✅
    BNBUSDT     WR 49.83%  lift +4.39pp / req 3.23pp  PF 1.490  lift +0.241 / req 0.100  trades 1,481  cov 29.3%  ✅
    XRPUSDT     WR 44.32%  lift +0.67pp / req 2.85pp  PF 1.194  lift +0.032 / req 0.100  trades 1,891  cov 30.8%  ⚠️ WR  ❌

  rsi_below_40    avg WR lift +1.26pp  avg PF 1.226  avg PF lift +0.066  pairs ≥ threshold: 2/5  ❌  ⚠️ WR 4p  ⚠️ weak regime 1p
    BTCUSDT     WR 42.34%  lift -1.27pp / req 2.65pp  PF 1.102  lift -0.059 / req 0.100  trades 2,187  ⚠️ WR  ❌
    ETHUSDT     WR 43.55%  lift +1.59pp / req 2.62pp  PF 1.157  lift +0.073 / req 0.100  trades 2,211  ⚠️ WR  ❌
    SOLUSDT     WR 45.91%  lift +2.55pp / req 2.66pp  PF 1.273  lift +0.125 / req 0.100  trades 2,165  ⚠️ WR  ✅
    BNBUSDT     WR 49.26%  lift +3.82pp / req 2.97pp  PF 1.456  lift +0.207 / req 0.100  trades 1,754  ✅
    XRPUSDT     WR 43.26%  lift -0.39pp / req 2.65pp  PF 1.143  lift -0.018 / req 0.100  trades 2,187  ⚠️ WR  ❌

  rsi_above_20    avg WR lift +0.14pp  avg PF 1.168  avg PF lift +0.007  pairs ≥ threshold: 0/5  ❌  ⚠️ WR 5p  ⚠️ weak regime 1p
    BTCUSDT     WR 43.72%  lift +0.10pp / req 1.66pp  PF 1.165  lift +0.005 / req 0.100  trades 5,554  ⚠️ WR  ❌
    ETHUSDT     WR 42.08%  lift +0.11pp / req 1.65pp  PF 1.090  lift +0.005 / req 0.100  trades 5,587  ⚠️ WR  ❌
    SOLUSDT     WR 43.54%  lift +0.18pp / req 1.70pp  PF 1.157  lift +0.008 / req 0.100  trades 5,296  ⚠️ WR  ❌
    BNBUSDT     WR 45.40%  lift -0.04pp / req 1.80pp  PF 1.247  lift -0.002 / req 0.100  trades 4,773  ⚠️ WR  ❌
    XRPUSDT     WR 44.00%  lift +0.36pp / req 1.62pp  PF 1.179  lift +0.017 / req 0.100  trades 5,845  ⚠️ WR  ❌

  Thresholds: WR lift > 2.5×sqrt(p(1-p)/n),  PF lift > 0.02/0.05/0.10 by n,  consistent across ≥ 4 of 5 pairs

  ❌  RSI SETUP EDGE NOT CONFIRMED — no RSI population clears all thresholds.
      Next steps:
        • Adjust rsi_upper (try 45 or 55)
        • Adjust rsi_lower (try 20 or 35)
        • Adjust rsi_period (try 7 or 21)
        • Try a different entry_tf in config.py
```
