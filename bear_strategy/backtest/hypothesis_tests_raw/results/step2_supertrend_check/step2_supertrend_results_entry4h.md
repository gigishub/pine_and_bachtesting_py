# SuperTrend Setup Edge Check

```text

── Per-Pair Results ──

  BTCUSDT
                     wr_%     pf  dur  n_trades
population                                     
regime_only         37.02  1.176  7.4      5886
st_bear             37.01  1.175  7.6      4258
st_near_resistance  32.35  0.957  6.3       102
st_extended         37.13  1.181  7.6      4156
    st_bear covers 72.3% of regime bars  

  ETHUSDT
                     wr_%     pf  dur  n_trades
population                                     
regime_only         38.22  1.237  7.4      5976
st_bear             36.77  1.163  7.7      4594
st_near_resistance  51.28  2.105  9.8        78
st_extended         36.51  1.150  7.6      4516
    st_bear covers 76.9% of regime bars  

  SOLUSDT
                     wr_%     pf  dur  n_trades
population                                     
regime_only         38.04  1.228  7.3      5594
st_bear             38.42  1.248  7.7      3967
st_near_resistance  40.91  1.385  8.3        66
st_extended         38.37  1.245  7.7      3901
    st_bear covers 70.9% of regime bars  

  BNBUSDT
                     wr_%     pf  dur  n_trades
population                                     
regime_only         37.95  1.223  7.2      5064
st_bear             37.57  1.204  7.4      3678
st_near_resistance  16.67  0.400  9.5        84
st_extended         38.06  1.229  7.4      3594
    st_bear covers 72.6% of regime bars  

  XRPUSDT
                     wr_%     pf  dur  n_trades
population                                     
regime_only         40.57  1.365  7.9      6148
st_bear             37.46  1.198  7.8      4268
st_near_resistance  48.61  1.892  9.3        72
st_extended         37.27  1.188  7.8      4196
    st_bear covers 69.4% of regime bars  

── SuperTrend Setup Edge Verdict ──

  Baseline (regime_only):  avg WR 38.4%  avg PF 1.246

  st_bear               avg WR lift -0.91pp  avg PF 1.198  avg PF lift -0.048  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 37.01%  lift -0.01pp / req 1.85pp  PF 1.175  lift -0.000 / req 0.100  trades 4,258  cov 72.3%  ❌
    ETHUSDT     WR 36.77%  lift -1.45pp / req 1.79pp  PF 1.163  lift -0.074 / req 0.100  trades 4,594  cov 76.9%  ❌
    SOLUSDT     WR 38.42%  lift +0.38pp / req 1.93pp  PF 1.248  lift +0.020 / req 0.100  trades 3,967  cov 70.9%  ❌
    BNBUSDT     WR 37.57%  lift -0.38pp / req 2.00pp  PF 1.204  lift -0.020 / req 0.100  trades 3,678  cov 72.6%  ❌
    XRPUSDT     WR 37.46%  lift -3.10pp / req 1.88pp  PF 1.198  lift -0.167 / req 0.100  trades 4,268  cov 69.4%  ❌

  st_near_resistance    avg WR lift -0.40pp  avg PF 1.348  avg PF lift +0.102  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 32.35%  lift -4.67pp / req 11.95pp  PF 0.957  lift -0.219 / req 0.100  trades 102  ❌
    ETHUSDT     WR 51.28%  lift +13.06pp / req 13.76pp  PF 2.105  lift +0.868 / req 0.100  trades 78  ❌
    SOLUSDT     WR 40.91%  lift +2.87pp / req 14.94pp  PF 1.385  lift +0.157 / req 0.100  trades 66  ❌
    BNBUSDT     WR 16.67%  lift -21.29pp / req 13.24pp  PF 0.400  lift -0.823 / req 0.100  trades 84  ❌
    XRPUSDT     WR 48.61%  lift +8.05pp / req 14.47pp  PF 1.892  lift +0.527 / req 0.100  trades 72  ❌

  st_extended           avg WR lift -0.89pp  avg PF 1.199  avg PF lift -0.047  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 37.13%  lift +0.11pp / req 1.87pp  PF 1.181  lift +0.005 / req 0.100  trades 4,156  ❌
    ETHUSDT     WR 36.51%  lift -1.70pp / req 1.81pp  PF 1.150  lift -0.087 / req 0.100  trades 4,516  ❌
    SOLUSDT     WR 38.37%  lift +0.33pp / req 1.94pp  PF 1.245  lift +0.017 / req 0.100  trades 3,901  ❌
    BNBUSDT     WR 38.06%  lift +0.11pp / req 2.02pp  PF 1.229  lift +0.006 / req 0.100  trades 3,594  ❌
    XRPUSDT     WR 37.27%  lift -3.29pp / req 1.90pp  PF 1.188  lift -0.177 / req 0.100  trades 4,196  ❌

  Thresholds: WR lift > 2.5×sqrt(p(1-p)/n),  PF lift > 0.02/0.05/0.10 by n,  trades > 1,000,  consistent across ≥ 4 of 5 pairs

  ❌  SUPERTREND SETUP EDGE NOT CONFIRMED — no population clears all thresholds.
      Next steps:
        • Adjust st_length (try 7 or 14)
        • Adjust st_multiplier (try 2.0 or 4.0)
        • Adjust proximity_atr_mult (try 1.0 or 0.25)
        • Try a different entry_tf in config.py
        • Re-examine whether setup layer is needed before trigger layer
```
