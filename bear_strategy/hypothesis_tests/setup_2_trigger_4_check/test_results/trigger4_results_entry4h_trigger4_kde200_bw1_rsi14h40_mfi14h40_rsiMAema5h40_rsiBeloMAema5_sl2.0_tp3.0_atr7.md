# Bear Strategy -- Setup 2 Trigger 4  (entry_tf=4h  kde_tf=4h)

## Test Parameters

| Parameter | Value |
|-----------|-------|
| `entry_tf` | `4h` |
| `kde_tf` | `4h` |
| `stop_atr_mult` | `2.0` |
| `target_atr_mult` | `3.0` |
| `atr_period` | `7` |
| `kde_window` | `200` |
| `kde_bandwidth_mult` | `1.0` |
| `rsi_period` | `14` |
| `rsi_threshold` | `40` |
| `mfi_period` | `14` |
| `mfi_threshold` | `40` |
| `rsi_ma_period` | `5` |
| `rsi_ma_type` | `ema` |
| `rsi_ma_threshold` | `40` |

```text

-- Per-Pair Results (baseline = kde_upper_baseline on 4h) --

  BTCUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  46.74  1.316  18.2      1318
rsi_below_50        57.63  2.040  28.0       236
mfi_below_50        50.78  1.547  20.8       386
rsi_ma_below_50     52.20  1.638  25.6       182
rsi_below_ma        48.92  1.436  19.7       738

    rsi_below_50        covers 17.9% of baseline bars
    mfi_below_50        covers 29.3% of baseline bars
    rsi_ma_below_50     covers 13.8% of baseline bars
    rsi_below_ma        covers 56.0% of baseline bars  !! HIGH

  ETHUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  48.63  1.420  22.0      1314
rsi_below_50        50.00  1.500  51.3       196
mfi_below_50        52.66  1.669  36.5       338
rsi_ma_below_50     46.15  1.286  67.3       130
rsi_below_ma        50.32  1.519  24.1       793

    rsi_below_50        covers 14.9% of baseline bars
    mfi_below_50        covers 25.7% of baseline bars
    rsi_ma_below_50     covers 9.9% of baseline bars
    rsi_below_ma        covers 60.4% of baseline bars  !! HIGH

  SOLUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  47.02  1.331  19.9      1359
rsi_below_50        53.30  1.712  20.1       212
mfi_below_50        49.50  1.470  21.7       301
rsi_ma_below_50     55.69  1.885  19.0       167
rsi_below_ma        47.62  1.364  20.0       800

    rsi_below_50        covers 15.6% of baseline bars
    mfi_below_50        covers 22.1% of baseline bars
    rsi_ma_below_50     covers 12.3% of baseline bars
    rsi_below_ma        covers 58.9% of baseline bars  !! HIGH

  BNBUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  50.18  1.511  19.2      1082
rsi_below_50        53.07  1.696  35.3       179
mfi_below_50        57.68  2.044  24.2       293
rsi_ma_below_50     55.56  1.875  36.2       135
rsi_below_ma        50.62  1.538  20.8       646

    rsi_below_50        covers 16.5% of baseline bars
    mfi_below_50        covers 27.1% of baseline bars
    rsi_ma_below_50     covers 12.5% of baseline bars
    rsi_below_ma        covers 59.7% of baseline bars  !! HIGH

  XRPUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  52.78  1.677  18.6      1294
rsi_below_50        46.58  1.308  24.6       161
mfi_below_50        52.59  1.664  21.5       348
rsi_ma_below_50     45.92  1.274  22.2        98
rsi_below_ma        53.63  1.735  19.8       798

    rsi_below_50        covers 12.4% of baseline bars
    mfi_below_50        covers 26.9% of baseline bars
    rsi_ma_below_50     covers 7.6% of baseline bars
    rsi_below_ma        covers 61.7% of baseline bars  !! HIGH


-- Setup 2 Trigger 4 (4h) -- Verdict --

  Baseline (kde_upper_baseline on 4h):  avg WR 49.1%  avg PF 1.451
  KDE (4h): window=200  bw=1  |  RSI(14)h40  MFI(14)h40  RSI/EMA(5)h40  RSI<EMA(5)

  [Oscillator  ]  rsi_below_50        WR lift +3.0pp  avg PF 1.651  PF lift +0.200  3/5 pairs  [OK]  warn: WR 4p, low# 5p
    BTCUSDT     WR 57.6%  PF 2.040  lift +0.724 / req 0.10  n=236  cov 18%!  [OK]
    ETHUSDT     WR 50.0%  PF 1.500  lift +0.080 / req 0.10  n=196  WR!  cov 15%!  [--]
    SOLUSDT     WR 53.3%  PF 1.712  lift +0.381 / req 0.10  n=212  WR!  cov 16%!  [OK]
    BNBUSDT     WR 53.1%  PF 1.696  lift +0.185 / req 0.10  n=179  WR!  cov 17%!  [OK]
    XRPUSDT     WR 46.6%  PF 1.308  lift -0.369 / req 0.10  n=161  WR!  cov 12%!  [--]
  [Volume      ]  mfi_below_50        WR lift +3.6pp  avg PF 1.679  PF lift +0.228  4/5 pairs  [OK]  warn: WR 4p, low# 5p
    BTCUSDT     WR 50.8%  PF 1.547  lift +0.231 / req 0.10  n=386  WR!  cov 29%!  [OK]
    ETHUSDT     WR 52.7%  PF 1.669  lift +0.249 / req 0.10  n=338  WR!  cov 26%!  [OK]
    SOLUSDT     WR 49.5%  PF 1.470  lift +0.139 / req 0.10  n=301  WR!  cov 22%!  [OK]
    BNBUSDT     WR 57.7%  PF 2.044  lift +0.533 / req 0.10  n=293  cov 27%!  [OK]
    XRPUSDT     WR 52.6%  PF 1.664  lift -0.013 / req 0.10  n=348  WR!  cov 27%!  [--]
  [Oscillator  ]  rsi_ma_below_50     WR lift +2.0pp  avg PF 1.591  PF lift +0.140  3/5 pairs  [OK]  warn: WR 5p, low# 5p
    BTCUSDT     WR 52.2%  PF 1.638  lift +0.322 / req 0.10  n=182  WR!  cov 14%!  [OK]
    ETHUSDT     WR 46.2%  PF 1.286  lift -0.134 / req 0.10  n=130  WR!  cov 10%!  [--]
    SOLUSDT     WR 55.7%  PF 1.885  lift +0.554 / req 0.10  n=167  WR!  cov 12%!  [OK]
    BNBUSDT     WR 55.6%  PF 1.875  lift +0.364 / req 0.10  n=135  WR!  cov 12%!  [OK]
    XRPUSDT     WR 45.9%  PF 1.274  lift -0.403 / req 0.10  n=98  WR!  cov 8%!  [--]
  [Oscillator  ]  rsi_below_ma        WR lift +1.2pp  avg PF 1.518  PF lift +0.067  1/5 pairs  [XX]  warn: WR 5p
    BTCUSDT     WR 48.9%  PF 1.436  lift +0.120 / req 0.10  n=738  WR!  cov 56%  [OK]
    ETHUSDT     WR 50.3%  PF 1.519  lift +0.099 / req 0.10  n=793  WR!  cov 60%  [--]
    SOLUSDT     WR 47.6%  PF 1.364  lift +0.033 / req 0.10  n=800  WR!  cov 59%  [--]
    BNBUSDT     WR 50.6%  PF 1.538  lift +0.026 / req 0.10  n=646  WR!  cov 60%  [--]
    XRPUSDT     WR 53.6%  PF 1.735  lift +0.058 / req 0.10  n=798  WR!  cov 62%  [--]

  Thresholds: PF lift > 0.02/0.05/0.10 by n,  >= 3 of 5 pairs

  [OK]  SETUP 2 TRIGGER 4 (4h) CONFIRMED -- populations below improve on kde_upper_baseline.
        Base: avg PF 1.451  |  Best: mfi_below_50  (avg PF 1.679)

  Warnings (results valid -- interpret with care):
    !! [rsi_below_50] WR lift below threshold on: ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [rsi_below_50] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [mfi_below_50] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT
    !! [mfi_below_50] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [rsi_ma_below_50] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [rsi_ma_below_50] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [rsi_below_ma] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT

  -- Confirmed populations --
    [Oscillator]
      [OK] rsi_below_50          avg PF 1.651
      [OK] rsi_ma_below_50       avg PF 1.591
      [--] rsi_below_ma
    [Volume]
      [OK] mfi_below_50          avg PF 1.679

  Proceed using confirmed positional filter(s) for setup 3 construction.
```
