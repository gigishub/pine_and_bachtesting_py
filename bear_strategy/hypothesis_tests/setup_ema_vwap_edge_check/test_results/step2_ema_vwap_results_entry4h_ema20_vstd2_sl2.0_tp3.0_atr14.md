# Bear Strategy — EMA20 / VWAP Setup Edge Check  (entry_tf=4h)

## Test Parameters

| Parameter | Value |
|-----------|-------|
| `entry_tf` | `4h` |
| `stop_atr_mult` | `2.0` |
| `target_atr_mult` | `3.0` |
| `atr_period` | `14` |
| `ema_period` | `20` |
| `vwap_anchor` | `daily` |
| `vwap_std_mult` | `2` |

```text

── Per-Pair Results ──

  BTCUSDT
                  wr_%     pf   dur  n_trades
regime_only      43.22  1.142  21.9      5886
below_ema20      42.82  1.123  22.6      3814
below_vwap       43.37  1.149  20.1      3048
below_both       42.89  1.127  20.4      2413
below_vwap_1std  44.59  1.207  19.4      1507
    below_ema20 covers 64.8% of regime bars  
    below_vwap covers 51.8% of regime bars  
    below_both covers 41.0% of regime bars  
    below_vwap_1std covers 25.6% of regime bars  ⚠️  LOW

  ETHUSDT
                  wr_%     pf   dur  n_trades
regime_only      42.00  1.086  22.0      5976
below_ema20      41.83  1.079  23.2      3770
below_vwap       43.15  1.138  20.0      3101
below_both       43.44  1.152  20.4      2394
below_vwap_1std  44.54  1.205  20.3      1466
    below_ema20 covers 63.1% of regime bars  
    below_vwap covers 51.9% of regime bars  
    below_both covers 40.1% of regime bars  
    below_vwap_1std covers 24.5% of regime bars  ⚠️  LOW

  SOLUSDT
                  wr_%     pf   dur  n_trades
regime_only      44.06  1.181  22.4      5581
below_ema20      44.61  1.208  23.7      3643
below_vwap       44.46  1.201  22.1      2960
below_both       44.91  1.223  22.9      2307
below_vwap_1std  45.06  1.230  21.4      1487
    below_ema20 covers 65.3% of regime bars  
    below_vwap covers 53.0% of regime bars  
    below_both covers 41.3% of regime bars  
    below_vwap_1std covers 26.6% of regime bars  ⚠️  LOW

  BNBUSDT
                  wr_%     pf   dur  n_trades
regime_only      45.07  1.231  19.0      5048
below_ema20      47.51  1.358  20.2      3149
below_vwap       46.23  1.290  19.0      2626
below_both       47.24  1.343  19.9      2032
below_vwap_1std  45.74  1.265  17.7      1257
    below_ema20 covers 62.4% of regime bars  
    below_vwap covers 52.0% of regime bars  
    below_both covers 40.3% of regime bars  
    below_vwap_1std covers 24.9% of regime bars  ⚠️  LOW

  XRPUSDT
                  wr_%     pf   dur  n_trades
regime_only      43.23  1.142  22.1      6144
below_ema20      43.85  1.172  23.7      4018
below_vwap       43.61  1.160  21.3      3222
below_both       43.80  1.169  21.6      2548
below_vwap_1std  44.13  1.185  20.5      1566
    below_ema20 covers 65.4% of regime bars  
    below_vwap covers 52.4% of regime bars  
    below_both covers 41.5% of regime bars  
    below_vwap_1std covers 25.5% of regime bars  ⚠️  LOW

── EMA20 / VWAP Setup Edge Verdict ──

  Baseline (regime_only):  avg WR 43.5%  avg PF 1.156

  below_ema20     avg WR lift +0.61pp  avg PF 1.188  avg PF lift +0.031  pairs ≥ threshold: 1/5  ❌  ⚠️ WR 4p  ⚠️ weak regime 1p
    BTCUSDT     WR 42.82%  lift -0.41pp / req 2.01pp  PF 1.123  lift -0.019 / req 0.100  trades 3,814  cov 64.8%  ⚠️ WR  ❌
    ETHUSDT     WR 41.83%  lift -0.17pp / req 2.01pp  PF 1.079  lift -0.008 / req 0.100  trades 3,770  cov 63.1%  ⚠️ WR  ❌
    SOLUSDT     WR 44.61%  lift +0.55pp / req 2.06pp  PF 1.208  lift +0.026 / req 0.100  trades 3,643  cov 65.3%  ⚠️ WR  ❌
    BNBUSDT     WR 47.51%  lift +2.44pp / req 2.22pp  PF 1.358  lift +0.127 / req 0.100  trades 3,149  cov 62.4%  ✅
    XRPUSDT     WR 43.85%  lift +0.62pp / req 1.95pp  PF 1.172  lift +0.029 / req 0.100  trades 4,018  cov 65.4%  ⚠️ WR  ❌

  below_vwap      avg WR lift +0.65pp  avg PF 1.188  avg PF lift +0.031  pairs ≥ threshold: 0/5  ❌  ⚠️ WR 5p  ⚠️ weak regime 1p
    BTCUSDT     WR 43.37%  lift +0.15pp / req 2.24pp  PF 1.149  lift +0.007 / req 0.100  trades 3,048  cov 51.8%  ⚠️ WR  ❌
    ETHUSDT     WR 43.15%  lift +1.15pp / req 2.22pp  PF 1.138  lift +0.052 / req 0.100  trades 3,101  cov 51.9%  ⚠️ WR  ❌
    SOLUSDT     WR 44.46%  lift +0.40pp / req 2.28pp  PF 1.201  lift +0.019 / req 0.100  trades 2,960  cov 53.0%  ⚠️ WR  ❌
    BNBUSDT     WR 46.23%  lift +1.16pp / req 2.43pp  PF 1.290  lift +0.059 / req 0.100  trades 2,626  cov 52.0%  ⚠️ WR  ❌
    XRPUSDT     WR 43.61%  lift +0.38pp / req 2.18pp  PF 1.160  lift +0.018 / req 0.100  trades 3,222  cov 52.4%  ⚠️ WR  ❌

  below_both      avg WR lift +0.94pp  avg PF 1.203  avg PF lift +0.046  pairs ≥ threshold: 1/5  ❌  ⚠️ WR 5p  ⚠️ weak regime 1p
    BTCUSDT     WR 42.89%  lift -0.33pp / req 2.52pp  PF 1.127  lift -0.015 / req 0.100  trades 2,413  cov 41.0%  ⚠️ WR  ❌
    ETHUSDT     WR 43.44%  lift +1.44pp / req 2.52pp  PF 1.152  lift +0.066 / req 0.100  trades 2,394  cov 40.1%  ⚠️ WR  ❌
    SOLUSDT     WR 44.91%  lift +0.85pp / req 2.58pp  PF 1.223  lift +0.041 / req 0.100  trades 2,307  cov 41.3%  ⚠️ WR  ❌
    BNBUSDT     WR 47.24%  lift +2.18pp / req 2.76pp  PF 1.343  lift +0.113 / req 0.100  trades 2,032  cov 40.3%  ⚠️ WR  ✅
    XRPUSDT     WR 43.80%  lift +0.57pp / req 2.45pp  PF 1.169  lift +0.027 / req 0.100  trades 2,548  cov 41.5%  ⚠️ WR  ❌

  below_vwap_1std  avg WR lift +1.30pp  avg PF 1.218  avg PF lift +0.062  pairs ≥ threshold: 1/5  ❌  ⚠️ WR 5p  ⚠️ low count 5p  ⚠️ weak regime 1p
    BTCUSDT     WR 44.59%  lift +1.37pp / req 3.19pp  PF 1.207  lift +0.065 / req 0.100  trades 1,507  cov 25.6% ⚠️  ⚠️ WR  ❌
    ETHUSDT     WR 44.54%  lift +2.54pp / req 3.22pp  PF 1.205  lift +0.119 / req 0.100  trades 1,466  cov 24.5% ⚠️  ⚠️ WR  ✅
    SOLUSDT     WR 45.06%  lift +1.00pp / req 3.22pp  PF 1.230  lift +0.049 / req 0.100  trades 1,487  cov 26.6% ⚠️  ⚠️ WR  ❌
    BNBUSDT     WR 45.74%  lift +0.68pp / req 3.51pp  PF 1.265  lift +0.034 / req 0.100  trades 1,257  cov 24.9% ⚠️  ⚠️ WR  ❌
    XRPUSDT     WR 44.13%  lift +0.90pp / req 3.13pp  PF 1.185  lift +0.042 / req 0.100  trades 1,566  cov 25.5% ⚠️  ⚠️ WR  ❌

  Thresholds: WR lift > 2.5×sqrt(p(1-p)/n),  PF lift > 0.02/0.05/0.10 by n,  consistent across ≥ 4 of 5 pairs

  ❌  EMA20/VWAP EDGE NOT CONFIRMED — no filter clears all thresholds.
      Next steps:
        • Try ema_period = 10 or 50
        • Try a different entry_tf in config.py
        • Note: in a strong bear regime most bars are already below EMA20
          — high coverage may dilute the signal vs the baseline
```
