# EMA20 / VWAP Setup Edge Check

```text

── Per-Pair Results ──

  BTCUSDT
                  wr_%     pf   dur  n_trades
population                                   
regime_only      42.73  1.119  20.3     94176
below_ema20      43.32  1.147  20.3     48643
below_vwap       43.56  1.158  20.5     48584
below_both       43.36  1.148  20.4     40881
below_vwap_1std  41.12  1.048  20.8      5396
    below_ema20 covers 51.7% of regime bars  
    below_vwap covers 51.6% of regime bars  
    below_both covers 43.4% of regime bars  
    below_vwap_1std covers 5.7% of regime bars  ⚠️  LOW

  ETHUSDT
                  wr_%     pf   dur  n_trades
population                                   
regime_only      43.61  1.160  19.5     95616
below_ema20      45.40  1.247  19.1     49643
below_vwap       45.61  1.258  19.4     49301
below_both       45.74  1.265  19.3     41561
below_vwap_1std  44.13  1.185  19.6      5264
    below_ema20 covers 51.9% of regime bars  
    below_vwap covers 51.6% of regime bars  
    below_both covers 43.5% of regime bars  
    below_vwap_1std covers 5.5% of regime bars  ⚠️  LOW

  SOLUSDT
                  wr_%     pf   dur  n_trades
population                                   
regime_only      43.85  1.171  19.6     89548
below_ema20      44.98  1.226  19.9     47496
below_vwap       44.76  1.215  19.9     47506
below_both       44.95  1.225  20.0     40183
below_vwap_1std  42.46  1.107  21.9      5754
    below_ema20 covers 53.0% of regime bars  
    below_vwap covers 53.1% of regime bars  
    below_both covers 44.9% of regime bars  
    below_vwap_1std covers 6.4% of regime bars  ⚠️  LOW

  BNBUSDT
                  wr_%     pf   dur  n_trades
population                                   
regime_only      43.35  1.148  17.8     81004
below_ema20      44.65  1.210  17.8     41308
below_vwap       44.68  1.211  17.9     42043
below_both       45.01  1.228  17.9     34756
below_vwap_1std  44.21  1.189  18.0      5444
    below_ema20 covers 51.0% of regime bars  
    below_vwap covers 51.9% of regime bars  
    below_both covers 42.9% of regime bars  
    below_vwap_1std covers 6.7% of regime bars  ⚠️  LOW

  XRPUSDT
                  wr_%     pf   dur  n_trades
population                                   
regime_only      45.40  1.247  21.1     98400
below_ema20      45.41  1.248  22.0     51678
below_vwap       45.50  1.252  21.3     51552
below_both       45.22  1.238  21.5     43217
below_vwap_1std  44.64  1.209  20.2      6255
    below_ema20 covers 52.5% of regime bars  
    below_vwap covers 52.4% of regime bars  
    below_both covers 43.9% of regime bars  
    below_vwap_1std covers 6.4% of regime bars  ⚠️  LOW

── EMA20 / VWAP Setup Edge Verdict ──

  Baseline (regime_only):  avg WR 43.8%  avg PF 1.169

  below_ema20     avg WR lift +0.96pp  avg PF 1.216  avg PF lift +0.046  pairs ≥ threshold: 3/5  ❌
    BTCUSDT     WR 43.32%  lift +0.59pp / req 0.56pp  PF 1.147  lift +0.027 / req 0.050  trades 48,643  cov 51.7%  ❌
    ETHUSDT     WR 45.40%  lift +1.79pp / req 0.56pp  PF 1.247  lift +0.087 / req 0.050  trades 49,643  cov 51.9%  ✅
    SOLUSDT     WR 44.98%  lift +1.13pp / req 0.57pp  PF 1.226  lift +0.055 / req 0.050  trades 47,496  cov 53.0%  ✅
    BNBUSDT     WR 44.65%  lift +1.30pp / req 0.61pp  PF 1.210  lift +0.062 / req 0.050  trades 41,308  cov 51.0%  ✅
    XRPUSDT     WR 45.41%  lift +0.01pp / req 0.55pp  PF 1.248  lift +0.001 / req 0.020  trades 51,678  cov 52.5%  ❌

  below_vwap      avg WR lift +1.03pp  avg PF 1.219  avg PF lift +0.050  pairs ≥ threshold: 2/5  ❌
    BTCUSDT     WR 43.56%  lift +0.83pp / req 0.56pp  PF 1.158  lift +0.038 / req 0.050  trades 48,584  cov 51.6%  ❌
    ETHUSDT     WR 45.61%  lift +2.00pp / req 0.56pp  PF 1.258  lift +0.098 / req 0.050  trades 49,301  cov 51.6%  ✅
    SOLUSDT     WR 44.76%  lift +0.91pp / req 0.57pp  PF 1.215  lift +0.044 / req 0.050  trades 47,506  cov 53.1%  ❌
    BNBUSDT     WR 44.68%  lift +1.33pp / req 0.60pp  PF 1.211  lift +0.064 / req 0.050  trades 42,043  cov 51.9%  ✅
    XRPUSDT     WR 45.50%  lift +0.10pp / req 0.55pp  PF 1.252  lift +0.005 / req 0.020  trades 51,552  cov 52.4%  ❌

  below_both      avg WR lift +1.07pp  avg PF 1.221  avg PF lift +0.052  pairs ≥ threshold: 3/5  ❌
    BTCUSDT     WR 43.36%  lift +0.62pp / req 0.61pp  PF 1.148  lift +0.029 / req 0.050  trades 40,881  cov 43.4%  ❌
    ETHUSDT     WR 45.74%  lift +2.13pp / req 0.61pp  PF 1.265  lift +0.105 / req 0.050  trades 41,561  cov 43.5%  ✅
    SOLUSDT     WR 44.95%  lift +1.10pp / req 0.62pp  PF 1.225  lift +0.053 / req 0.050  trades 40,183  cov 44.9%  ✅
    BNBUSDT     WR 45.01%  lift +1.66pp / req 0.66pp  PF 1.228  lift +0.080 / req 0.050  trades 34,756  cov 42.9%  ✅
    XRPUSDT     WR 45.22%  lift -0.17pp / req 0.60pp  PF 1.238  lift -0.009 / req 0.050  trades 43,217  cov 43.9%  ❌

  below_vwap_1std  avg WR lift -0.48pp  avg PF 1.147  avg PF lift -0.022  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 41.12%  lift -1.61pp / req 1.68pp  PF 1.048  lift -0.072 / req 0.100  trades 5,396  cov 5.7% ⚠️  ❌
    ETHUSDT     WR 44.13%  lift +0.52pp / req 1.71pp  PF 1.185  lift +0.025 / req 0.100  trades 5,264  cov 5.5% ⚠️  ❌
    SOLUSDT     WR 42.46%  lift -1.39pp / req 1.64pp  PF 1.107  lift -0.065 / req 0.100  trades 5,754  cov 6.4% ⚠️  ❌
    BNBUSDT     WR 44.21%  lift +0.87pp / req 1.68pp  PF 1.189  lift +0.041 / req 0.100  trades 5,444  cov 6.7% ⚠️  ❌
    XRPUSDT     WR 44.64%  lift -0.76pp / req 1.57pp  PF 1.209  lift -0.038 / req 0.100  trades 6,255  cov 6.4% ⚠️  ❌

  Thresholds: WR lift > 2.5×sqrt(p(1-p)/n),  PF lift > 0.02/0.05/0.10 by n,  trades > 500,  consistent across ≥ 4 of 5 pairs

  ❌  EMA20/VWAP EDGE NOT CONFIRMED — no filter clears all thresholds.
      Next steps:
        • Try ema_period = 10 or 50
        • Try a different entry_tf in config.py
        • Note: in a strong bear regime most bars are already below EMA20
          — high coverage may dilute the signal vs the baseline
```
