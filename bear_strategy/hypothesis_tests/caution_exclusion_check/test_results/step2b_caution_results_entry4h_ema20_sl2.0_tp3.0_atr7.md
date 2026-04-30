# Bear Strategy — Step 2b: Caution Exclusion Filter  (entry_tf=4h)

## Test Parameters

| Parameter | Value |
|-----------|-------|
| `entry_tf` | `4h` |
| `stop_atr_mult` | `2.0` |
| `target_atr_mult` | `3.0` |
| `atr_period` | `7` |
| `ema20_period` | `20` |
| `range_period` | `7` |
| `range_atr_mult` | `1.3` |

```text

── Per-Pair Results ──

  BTCUSDT
               wr_%     pf   dur  n_trades  mask_count
regime_only   43.61  1.160  22.3      5886        5886
ema20_filter  42.89  1.127  23.7      3814        3814
range_filter  42.77  1.121  20.4      1819        1819
no_caution    41.55  1.066  21.4      1603        1603
    no_caution keeps 27.2% of regime bars  ⚠️  LOW COVERAGE

  ETHUSDT
               wr_%     pf   dur  n_trades  mask_count
regime_only   41.97  1.085  22.5      5976        5976
ema20_filter  42.02  1.087  24.6      3770        3770
range_filter  42.64  1.115  19.4      1766        1766
no_caution    42.38  1.103  20.2      1496        1496
    no_caution keeps 25.0% of regime bars  ⚠️  LOW COVERAGE

  SOLUSDT
               wr_%     pf   dur  n_trades  mask_count
regime_only   43.36  1.148  22.3      5581        5599
ema20_filter  43.96  1.177  24.3      3644        3654
range_filter  42.98  1.131  21.0      1887        1892
no_caution    43.29  1.145  21.7      1661        1665
    no_caution keeps 29.7% of regime bars  ⚠️  LOW COVERAGE

  BNBUSDT
               wr_%     pf   dur  n_trades  mask_count
regime_only   45.44  1.249  19.0      5046        5064
ema20_filter  48.14  1.392  20.3      3147        3155
range_filter  47.69  1.368  19.0      1495        1499
no_caution    48.94  1.438  20.3      1275        1277
    no_caution keeps 25.2% of regime bars  ⚠️  LOW COVERAGE

  XRPUSDT
               wr_%     pf   dur  n_trades  mask_count
regime_only   43.64  1.162  23.9      6141        6150
ema20_filter  44.04  1.180  26.9      4017        4022
range_filter  47.42  1.353  21.2      1805        1808
no_caution    46.58  1.308  22.0      1550        1553
    no_caution keeps 25.3% of regime bars  ⚠️  LOW COVERAGE

── Caution Exclusion Verdict ──

  Baseline (regime_only):  avg WR 43.6%  avg PF 1.161

  ema20_filter    avg WR lift +0.61pp  avg PF 1.193  avg PF lift +0.032  pairs ≥ threshold: 1/5  ❌  ⚠️ WR 4p  ⚠️ weak regime 1p
    BTCUSDT     WR 42.89%  lift -0.72pp / req 2.01pp  PF 1.127  lift -0.033 / req 0.100  trades 3,814  ⚠️ WR  ❌
    ETHUSDT     WR 42.02%  lift +0.05pp / req 2.01pp  PF 1.087  lift +0.002 / req 0.100  trades 3,770  ⚠️ WR  ❌
    SOLUSDT     WR 43.96%  lift +0.60pp / req 2.05pp  PF 1.177  lift +0.028 / req 0.100  trades 3,644  ⚠️ WR  ❌
    BNBUSDT     WR 48.14%  lift +2.70pp / req 2.22pp  PF 1.392  lift +0.143 / req 0.100  trades 3,147  ✅
    XRPUSDT     WR 44.04%  lift +0.40pp / req 1.96pp  PF 1.180  lift +0.019 / req 0.100  trades 4,017  ⚠️ WR  ❌

  range_filter    avg WR lift +1.10pp  avg PF 1.217  avg PF lift +0.057  pairs ≥ threshold: 2/5  ❌  ⚠️ WR 4p  ⚠️ low count 3p  ⚠️ weak regime 1p
    BTCUSDT     WR 42.77%  lift -0.84pp / req 2.91pp  PF 1.121  lift -0.039 / req 0.100  trades 1,819  ⚠️ WR  ❌
    ETHUSDT     WR 42.64%  lift +0.67pp / req 2.94pp  PF 1.115  lift +0.030 / req 0.100  trades 1,766  ⚠️ WR  ❌
    SOLUSDT     WR 42.98%  lift -0.38pp / req 2.85pp  PF 1.131  lift -0.018 / req 0.100  trades 1,887  ⚠️ WR  ❌
    BNBUSDT     WR 47.69%  lift +2.25pp / req 3.22pp  PF 1.368  lift +0.118 / req 0.100  trades 1,495  ⚠️ WR  ✅
    XRPUSDT     WR 47.42%  lift +3.78pp / req 2.92pp  PF 1.353  lift +0.191 / req 0.100  trades 1,805  ✅

  no_caution      avg WR lift +0.94pp  avg PF 1.212  avg PF lift +0.051  pairs ≥ threshold: 2/5  ❌  ⚠️ WR 4p  ⚠️ low count 5p  ⚠️ weak regime 1p
    BTCUSDT     WR 41.55%  lift -2.06pp / req 3.10pp  PF 1.066  lift -0.094 / req 0.100  trades 1,603  cov 27.2% ⚠️  ⚠️ WR  ❌
    ETHUSDT     WR 42.38%  lift +0.41pp / req 3.19pp  PF 1.103  lift +0.018 / req 0.100  trades 1,496  cov 25.0% ⚠️  ⚠️ WR  ❌
    SOLUSDT     WR 43.29%  lift -0.07pp / req 3.04pp  PF 1.145  lift -0.003 / req 0.100  trades 1,661  cov 29.7% ⚠️  ⚠️ WR  ❌
    BNBUSDT     WR 48.94%  lift +3.50pp / req 3.49pp  PF 1.438  lift +0.188 / req 0.100  trades 1,275  cov 25.2% ⚠️  ✅
    XRPUSDT     WR 46.58%  lift +2.94pp / req 3.15pp  PF 1.308  lift +0.146 / req 0.100  trades 1,550  cov 25.3% ⚠️  ⚠️ WR  ✅

  Thresholds: WR lift > 2.5×sqrt(p(1-p)/n),  PF lift > 0.02/0.05/0.10 by n,  consistent across ≥ 4 of 5 pairs

  ❌  CAUTION EXCLUSION NOT CONFIRMED — no improvement over regime baseline.

      No component shows edge — caution exclusion hypothesis rejected.

  Next steps:
    • Adjust range_atr_mult (try 1.2× or 2.0×)
    • Adjust ema20_period (try 10 or 30)
    • Try a different entry_tf in config.py
    • Re-examine whether a setup layer is needed before the trigger layer
```
