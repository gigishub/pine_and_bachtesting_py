# Bear Strategy -- Setup 2 Trigger 4  (entry_tf=1h  kde_tf=4h)

## Test Parameters

| Parameter | Value |
|-----------|-------|
| `entry_tf` | `1h` |
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

-- Per-Pair Results (baseline = kde_upper_baseline on 1h) --

  BTCUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  47.76  1.371  20.9      5272
rsi_below_50        56.39  1.940  31.5      1158
mfi_below_50        53.96  1.758  25.7      1742
rsi_ma_below_50     57.91  2.063  33.2       955
rsi_below_ma        48.08  1.389  22.5      2993

    rsi_below_50        covers 22.0% of baseline bars
    mfi_below_50        covers 33.0% of baseline bars
    rsi_ma_below_50     covers 18.1% of baseline bars
    rsi_below_ma        covers 56.8% of baseline bars  !! HIGH

  ETHUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  53.79  1.746  21.0      5256
rsi_below_50        62.33  2.482  34.8      1261
mfi_below_50        56.91  1.981  27.6      1998
rsi_ma_below_50     66.01  2.913  37.1      1071
rsi_below_ma        54.09  1.767  21.9      3084

    rsi_below_50        covers 24.0% of baseline bars
    mfi_below_50        covers 38.0% of baseline bars
    rsi_ma_below_50     covers 20.4% of baseline bars
    rsi_below_ma        covers 58.7% of baseline bars  !! HIGH

  SOLUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  48.91  1.436  18.8      5475
rsi_below_50        53.88  1.752  24.3      1264
mfi_below_50        52.34  1.647  20.7      2010
rsi_ma_below_50     56.12  1.918  23.2      1046
rsi_below_ma        47.24  1.343  20.1      3192

    rsi_below_50        covers 23.1% of baseline bars
    mfi_below_50        covers 36.7% of baseline bars
    rsi_ma_below_50     covers 19.1% of baseline bars
    rsi_below_ma        covers 58.3% of baseline bars  !! HIGH

  BNBUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  51.36  1.584  21.1      4367
rsi_below_50        52.15  1.635  31.4       905
mfi_below_50        52.18  1.637  24.7      1608
rsi_ma_below_50     51.25  1.577  30.8       722
rsi_below_ma        50.97  1.559  22.9      2533

    rsi_below_50        covers 20.7% of baseline bars
    mfi_below_50        covers 36.8% of baseline bars
    rsi_ma_below_50     covers 16.5% of baseline bars
    rsi_below_ma        covers 58.0% of baseline bars  !! HIGH

  XRPUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  51.86  1.616  22.3      5195
rsi_below_50        48.22  1.397  35.0       981
mfi_below_50        51.52  1.594  27.0      1815
rsi_ma_below_50     47.75  1.371  38.0       800
rsi_below_ma        51.31  1.580  23.4      2949

    rsi_below_50        covers 18.9% of baseline bars
    mfi_below_50        covers 34.9% of baseline bars
    rsi_ma_below_50     covers 15.4% of baseline bars
    rsi_below_ma        covers 56.8% of baseline bars  !! HIGH


-- Setup 2 Trigger 4 (1h) -- Verdict --

  Baseline (kde_upper_baseline on 1h):  avg WR 50.7%  avg PF 1.551
  KDE (4h): window=200  bw=1  |  RSI(14)h40  MFI(14)h40  RSI/EMA(5)h40  RSI<EMA(5)

  [Oscillator  ]  rsi_below_50        WR lift +3.9pp  avg PF 1.841  PF lift +0.290  3/5 pairs  [OK]  warn: WR 2p, low# 5p
    BTCUSDT     WR 56.4%  PF 1.940  lift +0.568 / req 0.10  n=1,158  cov 22%!  [OK]
    ETHUSDT     WR 62.3%  PF 2.482  lift +0.736 / req 0.10  n=1,261  cov 24%!  [OK]
    SOLUSDT     WR 53.9%  PF 1.752  lift +0.316 / req 0.10  n=1,264  cov 23%!  [OK]
    BNBUSDT     WR 52.2%  PF 1.635  lift +0.051 / req 0.10  n=905  WR!  cov 21%!  [--]
    XRPUSDT     WR 48.2%  PF 1.397  lift -0.219 / req 0.10  n=981  WR!  cov 19%!  [--]
  [Volume      ]  mfi_below_50        WR lift +2.6pp  avg PF 1.723  PF lift +0.173  3/5 pairs  [OK]  warn: WR 2p
    BTCUSDT     WR 54.0%  PF 1.758  lift +0.387 / req 0.10  n=1,742  cov 33%  [OK]
    ETHUSDT     WR 56.9%  PF 1.981  lift +0.235 / req 0.10  n=1,998  cov 38%  [OK]
    SOLUSDT     WR 52.3%  PF 1.647  lift +0.211 / req 0.10  n=2,010  cov 37%  [OK]
    BNBUSDT     WR 52.2%  PF 1.637  lift +0.053 / req 0.10  n=1,608  WR!  cov 37%  [--]
    XRPUSDT     WR 51.5%  PF 1.594  lift -0.022 / req 0.10  n=1,815  WR!  cov 35%  [--]
  [Oscillator  ]  rsi_ma_below_50     WR lift +5.1pp  avg PF 1.969  PF lift +0.418  3/5 pairs  [OK]  warn: WR 2p, low# 5p
    BTCUSDT     WR 57.9%  PF 2.063  lift +0.692 / req 0.10  n=955  cov 18%!  [OK]
    ETHUSDT     WR 66.0%  PF 2.913  lift +1.168 / req 0.10  n=1,071  cov 20%!  [OK]
    SOLUSDT     WR 56.1%  PF 1.918  lift +0.482 / req 0.10  n=1,046  cov 19%!  [OK]
    BNBUSDT     WR 51.2%  PF 1.577  lift -0.007 / req 0.10  n=722  WR!  cov 17%!  [--]
    XRPUSDT     WR 47.8%  PF 1.371  lift -0.245 / req 0.10  n=800  WR!  cov 15%!  [--]
  [Oscillator  ]  rsi_below_ma        WR lift -0.4pp  avg PF 1.528  PF lift -0.023  0/5 pairs  [XX]  warn: WR 5p
    BTCUSDT     WR 48.1%  PF 1.389  lift +0.018 / req 0.10  n=2,993  WR!  cov 57%  [--]
    ETHUSDT     WR 54.1%  PF 1.767  lift +0.021 / req 0.10  n=3,084  WR!  cov 59%  [--]
    SOLUSDT     WR 47.2%  PF 1.343  lift -0.093 / req 0.10  n=3,192  WR!  cov 58%  [--]
    BNBUSDT     WR 51.0%  PF 1.559  lift -0.025 / req 0.10  n=2,533  WR!  cov 58%  [--]
    XRPUSDT     WR 51.3%  PF 1.580  lift -0.035 / req 0.10  n=2,949  WR!  cov 57%  [--]

  Thresholds: PF lift > 0.02/0.05/0.10 by n,  >= 3 of 5 pairs

  [OK]  SETUP 2 TRIGGER 4 (1h) CONFIRMED -- populations below improve on kde_upper_baseline.
        Base: avg PF 1.551  |  Best: rsi_ma_below_50  (avg PF 1.969)

  Warnings (results valid -- interpret with care):
    !! [rsi_below_50] WR lift below threshold on: BNBUSDT, XRPUSDT
    !! [rsi_below_50] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [mfi_below_50] WR lift below threshold on: BNBUSDT, XRPUSDT
    !! [rsi_ma_below_50] WR lift below threshold on: BNBUSDT, XRPUSDT
    !! [rsi_ma_below_50] low trade count (<30% baseline) on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [rsi_below_ma] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT

  -- Confirmed populations --
    [Oscillator]
      [OK] rsi_below_50          avg PF 1.841
      [OK] rsi_ma_below_50       avg PF 1.969
      [--] rsi_below_ma
    [Volume]
      [OK] mfi_below_50          avg PF 1.723

  Proceed using confirmed positional filter(s) for setup 3 construction.
```
