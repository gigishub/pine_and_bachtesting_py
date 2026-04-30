# Bear Strategy — EMA Cross-Below Setup Edge Check  (entry_tf=4h)

## Test Parameters

| Parameter | Value |
|-----------|-------|
| `entry_tf` | `4h` |
| `stop_atr_mult` | `2.0` |
| `target_atr_mult` | `3.0` |
| `atr_period` | `7` |
| `ema_period` | `10` |
| `min_bars_above` | `2` |

```text

── Per-Pair Results ──

  BTCUSDT
                    wr_%     pf   dur  n_trades
population                                     
regime_only        43.61  1.160  22.3      5886
ema_cross_below    46.48  1.303  20.7       540
ema_cross_below_N  45.03  1.229  21.0       362
    ema_cross_below covers 9.2% of regime bars  
    ema_cross_below_N covers 6.2% of regime bars  

  ETHUSDT
                    wr_%     pf   dur  n_trades
population                                     
regime_only        41.97  1.085  22.5      5976
ema_cross_below    45.04  1.229  20.4       575
ema_cross_below_N  43.96  1.177  21.3       389
    ema_cross_below covers 9.6% of regime bars  
    ema_cross_below_N covers 6.5% of regime bars  

  SOLUSDT
                    wr_%     pf   dur  n_trades
population                                     
regime_only        43.36  1.148  22.3      5581
ema_cross_below    40.87  1.037  20.2       504
ema_cross_below_N  41.45  1.062  21.4       345
    ema_cross_below covers 9.0% of regime bars  
    ema_cross_below_N covers 6.2% of regime bars  

  BNBUSDT
                    wr_%     pf   dur  n_trades
population                                     
regime_only        45.44  1.249  19.0      5046
ema_cross_below    47.94  1.381  17.2       509
ema_cross_below_N  43.57  1.158  18.7       342
    ema_cross_below covers 10.1% of regime bars  
    ema_cross_below_N covers 6.8% of regime bars  

  XRPUSDT
                    wr_%     pf   dur  n_trades
population                                     
regime_only        43.64  1.162  23.9      6141
ema_cross_below    45.56  1.255  20.9       608
ema_cross_below_N  42.86  1.125  22.1       385
    ema_cross_below covers 9.9% of regime bars  
    ema_cross_below_N covers 6.3% of regime bars  

── EMA Cross-Below Edge Verdict ──

  Baseline (regime_only):  avg WR 43.6%  avg PF 1.161
  EMA(10) cross config:  min_bars_above=2

  ema_cross_below         avg WR lift +1.57pp  avg PF 1.241  avg PF lift +0.080  pairs ≥ threshold: 3/5  ❌  ⚠️ WR 5p  ⚠️ low count 5p  ⚠️ weak regime 1p
    BTCUSDT     WR 46.48%  lift +2.87pp / req 5.34pp  PF 1.303  lift +0.143 / req 0.100  trades 540  cov 9.2%  ⚠️ WR  ✅
    ETHUSDT     WR 45.04%  lift +3.08pp / req 5.15pp  PF 1.229  lift +0.145 / req 0.100  trades 575  cov 9.6%  ⚠️ WR  ✅
    SOLUSDT     WR 40.87%  lift -2.49pp / req 5.52pp  PF 1.037  lift -0.111 / req 0.100  trades 504  cov 9.0%  ⚠️ WR  ❌
    BNBUSDT     WR 47.94%  lift +2.50pp / req 5.52pp  PF 1.381  lift +0.132 / req 0.100  trades 509  cov 10.1%  ⚠️ WR  ✅
    XRPUSDT     WR 45.56%  lift +1.92pp / req 5.03pp  PF 1.255  lift +0.094 / req 0.100  trades 608  cov 9.9%  ⚠️ WR  ❌

  ema_cross_below_N       avg WR lift -0.23pp  avg PF 1.150  avg PF lift -0.011  pairs ≥ threshold: 0/5  ❌  ⚠️ WR 5p  ⚠️ low count 5p  ⚠️ weak regime 1p
    BTCUSDT     WR 45.03%  lift +1.42pp / req 6.52pp  PF 1.229  lift +0.069 / req 0.100  trades 362  cov 6.2%  ⚠️ WR  ❌
    ETHUSDT     WR 43.96%  lift +1.99pp / req 6.26pp  PF 1.177  lift +0.092 / req 0.100  trades 389  cov 6.5%  ⚠️ WR  ❌
    SOLUSDT     WR 41.45%  lift -1.91pp / req 6.67pp  PF 1.062  lift -0.086 / req 0.100  trades 345  cov 6.2%  ⚠️ WR  ❌
    BNBUSDT     WR 43.57%  lift -1.87pp / req 6.73pp  PF 1.158  lift -0.091 / req 0.100  trades 342  cov 6.8%  ⚠️ WR  ❌
    XRPUSDT     WR 42.86%  lift -0.78pp / req 6.32pp  PF 1.125  lift -0.037 / req 0.100  trades 385  cov 6.3%  ⚠️ WR  ❌

  Thresholds: WR lift > 2.5×sqrt(p(1-p)/n),  PF lift > 0.02/0.05/0.10 by n,  consistent across ≥ 4 of 5 pairs

  ❌  EMA CROSS EDGE NOT CONFIRMED — no population clears all thresholds.
      Next steps:
        • Adjust min_bars_above (currently 2) — try 2 or 5
        • Try ema_period = 9 or 50 (currently 10)
        • Try a different entry_tf in config.py
        • EMA crosses may need volume confirmation to produce consistent edge
```
