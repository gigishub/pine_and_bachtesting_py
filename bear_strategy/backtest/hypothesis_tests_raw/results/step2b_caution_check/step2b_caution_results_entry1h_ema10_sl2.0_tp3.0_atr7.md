# Bear Strategy — Step 2b: Caution Exclusion Filter  (entry_tf=1h)

## Test Parameters

| Parameter | Value |
|-----------|-------|
| `entry_tf` | `1h` |
| `stop_atr_mult` | `2.0` |
| `target_atr_mult` | `3.0` |
| `atr_period` | `7` |
| `ema20_period` | `10` |
| `range_period` | `7` |
| `range_atr_mult` | `1.2` |

```text

── Per-Pair Results ──

  BTCUSDT
               wr_%     pf   dur  n_trades  mask_count
regime_only   44.25  1.191  20.4     23544       23544
ema10_filter  45.40  1.247  21.5     12452       12452
range_filter  44.12  1.185  18.2      5106        5106
no_caution    44.66  1.211  18.8      4460        4460
    no_caution keeps 18.9% of regime bars  ⚠️  LOW COVERAGE

  ETHUSDT
               wr_%     pf   dur  n_trades  mask_count
regime_only   45.01  1.228  19.9     23904       23904
ema10_filter  46.23  1.290  20.3     12785       12785
range_filter  45.74  1.265  17.6      5098        5098
no_caution    46.09  1.282  17.9      4487        4487
    no_caution keeps 18.8% of regime bars  ⚠️  LOW COVERAGE

  SOLUSDT
               wr_%     pf   dur  n_trades  mask_count
regime_only   44.84  1.219  19.5     22371       22393
ema10_filter  45.66  1.260  19.6     12307       12313
range_filter  44.71  1.213  17.7      5468        5470
no_caution    44.71  1.213  18.0      4979        4980
    no_caution keeps 22.2% of regime bars  ⚠️  LOW COVERAGE

  BNBUSDT
               wr_%     pf   dur  n_trades  mask_count
regime_only   44.88  1.222  19.0     20243       20256
ema10_filter  45.56  1.255  19.3     10508       10519
range_filter  44.91  1.223  18.1      4355        4358
no_caution    45.18  1.236  18.3      3858        3861
    no_caution keeps 19.1% of regime bars  ⚠️  LOW COVERAGE

  XRPUSDT
               wr_%     pf   dur  n_trades  mask_count
regime_only   47.17  1.339  22.3     24598       24600
ema10_filter  48.49  1.412  24.7     13331       13333
range_filter  46.33  1.295  18.3      5282        5283
no_caution    46.27  1.292  18.5      4724        4725
    no_caution keeps 19.2% of regime bars  ⚠️  LOW COVERAGE

── Caution Exclusion Verdict ──

  Baseline (regime_only):  avg WR 45.2%  avg PF 1.240

  ema10_filter    avg WR lift +1.04pp  avg PF 1.293  avg PF lift +0.053  pairs ≥ threshold: 3/5  ❌
    BTCUSDT     WR 45.40%  lift +1.15pp / req 1.11pp  PF 1.247  lift +0.056 / req 0.050  trades 12,452  ✅
    ETHUSDT     WR 46.23%  lift +1.22pp / req 1.10pp  PF 1.290  lift +0.062 / req 0.050  trades 12,785  ✅
    SOLUSDT     WR 45.66%  lift +0.82pp / req 1.12pp  PF 1.260  lift +0.041 / req 0.050  trades 12,307  ❌
    BNBUSDT     WR 45.56%  lift +0.67pp / req 1.21pp  PF 1.255  lift +0.034 / req 0.050  trades 10,508  ❌
    XRPUSDT     WR 48.49%  lift +1.32pp / req 1.08pp  PF 1.412  lift +0.073 / req 0.050  trades 13,331  ✅

  range_filter    avg WR lift -0.07pp  avg PF 1.236  avg PF lift -0.004  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 44.12%  lift -0.13pp / req 1.74pp  PF 1.185  lift -0.006 / req 0.100  trades 5,106  ❌
    ETHUSDT     WR 45.74%  lift +0.73pp / req 1.74pp  PF 1.265  lift +0.037 / req 0.100  trades 5,098  ❌
    SOLUSDT     WR 44.71%  lift -0.12pp / req 1.68pp  PF 1.213  lift -0.006 / req 0.100  trades 5,468  ❌
    BNBUSDT     WR 44.91%  lift +0.03pp / req 1.88pp  PF 1.223  lift +0.001 / req 0.100  trades 4,355  ❌
    XRPUSDT     WR 46.33%  lift -0.84pp / req 1.72pp  PF 1.295  lift -0.044 / req 0.100  trades 5,282  ❌

  no_caution      avg WR lift +0.15pp  avg PF 1.247  avg PF lift +0.007  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 44.66%  lift +0.41pp / req 1.86pp  PF 1.211  lift +0.020 / req 0.100  trades 4,460  cov 18.9% ⚠️  ❌
    ETHUSDT     WR 46.09%  lift +1.08pp / req 1.86pp  PF 1.282  lift +0.055 / req 0.100  trades 4,487  cov 18.8% ⚠️  ❌
    SOLUSDT     WR 44.71%  lift -0.13pp / req 1.76pp  PF 1.213  lift -0.006 / req 0.100  trades 4,979  cov 22.2% ⚠️  ❌
    BNBUSDT     WR 45.18%  lift +0.29pp / req 2.00pp  PF 1.236  lift +0.015 / req 0.100  trades 3,858  cov 19.1% ⚠️  ❌
    XRPUSDT     WR 46.27%  lift -0.89pp / req 1.82pp  PF 1.292  lift -0.047 / req 0.100  trades 4,724  cov 19.2% ⚠️  ❌

  Thresholds: WR lift > 2.5×sqrt(p(1-p)/n),  PF lift > 0.02/0.05/0.10 by n,  trades > 1,000,  consistent across ≥ 4 of 5 pairs

  ❌  CAUTION EXCLUSION NOT CONFIRMED — no improvement over regime baseline.

      No component shows edge — caution exclusion hypothesis rejected.

  Next steps:
    • Adjust range_atr_mult (try 1.2× or 2.0×)
    • Adjust ema20_period (try 10 or 30)
    • Try a different entry_tf in config.py
    • Re-examine whether a setup layer is needed before the trigger layer
```
