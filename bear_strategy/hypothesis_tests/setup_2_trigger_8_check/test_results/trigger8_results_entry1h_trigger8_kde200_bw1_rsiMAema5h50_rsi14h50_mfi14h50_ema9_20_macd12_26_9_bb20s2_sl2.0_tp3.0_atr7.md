# Bear Strategy -- Setup 2 Trigger 8  (entry_tf=1h  kde_tf=4h  rsi_ma_baseline=ema5<50.0)

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
| `rsi_ma_period` | `5` |
| `rsi_ma_type` | `ema` |
| `rsi_ma_threshold` | `50.0` |
| `rsi_threshold` | `50.0` |
| `mfi_period` | `14` |
| `mfi_threshold` | `50.0` |
| `ema_fast` | `9` |
| `ema_slow` | `20` |
| `macd_fast` | `12` |
| `macd_slow` | `26` |
| `macd_signal` | `9` |
| `bb_period` | `20` |
| `bb_std` | `2.0` |

```text

-- Per-Pair Results (new base = rsi_ma_baseline on 1h) --

  BTCUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  47.76  1.371  20.9      5272
rsi_ma_baseline     50.24  1.515  23.5      2490
rsi_below_50        50.89  1.554  24.1      2307
mfi_below_50        51.57  1.597  24.2      2071
rsi_and_mfi         52.23  1.640  24.8      1972
close_below_ema     50.94  1.557  24.3      2234
ema_bearish_order   50.35  1.521  23.8      2395
macd_signal_wall    52.57  1.663  26.7      1613
lower_bb_declining  51.61  1.600  26.6      1804

    rsi_below_50                covers 92.7% of rsi_ma_baseline bars
    mfi_below_50                covers 83.2% of rsi_ma_baseline bars
    rsi_and_mfi                 covers 79.2% of rsi_ma_baseline bars
    close_below_ema             covers 89.7% of rsi_ma_baseline bars
    ema_bearish_order           covers 96.2% of rsi_ma_baseline bars
    macd_signal_wall            covers 64.8% of rsi_ma_baseline bars
    lower_bb_declining          covers 72.4% of rsi_ma_baseline bars

  ETHUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  53.79  1.746  21.0      5256
rsi_ma_baseline     58.23  2.091  24.9      2528
rsi_below_50        58.27  2.095  25.5      2370
mfi_below_50        57.70  2.046  26.1      2208
rsi_and_mfi         57.81  2.055  26.8      2114
close_below_ema     58.16  2.085  25.6      2342
ema_bearish_order   58.40  2.106  25.1      2457
macd_signal_wall    58.52  2.116  28.9      1702
lower_bb_declining  58.27  2.094  28.2      1929

    rsi_below_50                covers 93.8% of rsi_ma_baseline bars
    mfi_below_50                covers 87.3% of rsi_ma_baseline bars
    rsi_and_mfi                 covers 83.6% of rsi_ma_baseline bars
    close_below_ema             covers 92.6% of rsi_ma_baseline bars
    ema_bearish_order           covers 97.2% of rsi_ma_baseline bars
    macd_signal_wall            covers 67.3% of rsi_ma_baseline bars
    lower_bb_declining          covers 76.3% of rsi_ma_baseline bars

  SOLUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  48.91  1.436  18.8      5475
rsi_ma_baseline     52.60  1.665  19.7      2673
rsi_below_50        52.58  1.663  19.9      2516
mfi_below_50        53.31  1.713  20.3      2311
rsi_and_mfi         53.25  1.708  20.5      2218
close_below_ema     52.58  1.663  20.1      2438
ema_bearish_order   53.00  1.692  19.8      2596
macd_signal_wall    53.16  1.702  21.8      1742
lower_bb_declining  52.34  1.648  22.0      1920

    rsi_below_50                covers 94.1% of rsi_ma_baseline bars
    mfi_below_50                covers 86.5% of rsi_ma_baseline bars
    rsi_and_mfi                 covers 83.0% of rsi_ma_baseline bars
    close_below_ema             covers 91.2% of rsi_ma_baseline bars
    ema_bearish_order           covers 97.1% of rsi_ma_baseline bars
    macd_signal_wall            covers 65.2% of rsi_ma_baseline bars
    lower_bb_declining          covers 71.8% of rsi_ma_baseline bars

  BNBUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  51.36  1.584  21.1      4367
rsi_ma_baseline     54.50  1.797  23.9      2143
rsi_below_50        54.14  1.771  24.3      1991
mfi_below_50        53.62  1.734  24.6      1807
rsi_and_mfi         53.46  1.723  25.0      1721
close_below_ema     53.71  1.740  24.4      1942
ema_bearish_order   54.48  1.795  23.9      2076
macd_signal_wall    53.43  1.721  26.8      1413
lower_bb_declining  53.61  1.734  26.3      1578

    rsi_below_50                covers 92.9% of rsi_ma_baseline bars
    mfi_below_50                covers 84.3% of rsi_ma_baseline bars
    rsi_and_mfi                 covers 80.3% of rsi_ma_baseline bars
    close_below_ema             covers 90.6% of rsi_ma_baseline bars
    ema_bearish_order           covers 96.9% of rsi_ma_baseline bars
    macd_signal_wall            covers 65.9% of rsi_ma_baseline bars
    lower_bb_declining          covers 73.6% of rsi_ma_baseline bars

  XRPUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  51.86  1.616  22.3      5195
rsi_ma_baseline     51.47  1.591  25.3      2788
rsi_below_50        50.47  1.529  25.8      2534
mfi_below_50        51.39  1.586  25.6      2302
rsi_and_mfi         50.67  1.541  26.3      2151
close_below_ema     50.55  1.533  25.8      2461
ema_bearish_order   51.40  1.587  25.6      2673
macd_signal_wall    51.53  1.595  28.1      1828
lower_bb_declining  52.36  1.649  28.6      1906

    rsi_below_50                covers 90.9% of rsi_ma_baseline bars
    mfi_below_50                covers 82.6% of rsi_ma_baseline bars
    rsi_and_mfi                 covers 77.2% of rsi_ma_baseline bars
    close_below_ema             covers 88.3% of rsi_ma_baseline bars
    ema_bearish_order           covers 95.9% of rsi_ma_baseline bars
    macd_signal_wall            covers 65.6% of rsi_ma_baseline bars
    lower_bb_declining          covers 68.4% of rsi_ma_baseline bars


-- Setup 2 Trigger 8 (1h) -- Verdict --

  [ref]  kde_upper_baseline (1h):        avg WR 50.7%  avg PF 1.551
  [base] rsi_ma_baseline (ema5<50):  avg WR 53.4%  avg PF 1.732  [lift vs kde ref: +0.181]
  KDE (4h): window=200  bw=1  |  RSI(14)  MFI(14)  EMA(9,20)  BB(20)

  [Momentum   ]  rsi_below_50                WR lift -0.1pp  avg PF 1.722  PF lift -0.009  0/5 pairs  [XX]  warn: WR 5p
    BTCUSDT     WR 50.9%  PF 1.554  lift +0.040 / req 0.10  n=2,307  WR!  cov 93%  [--]
    ETHUSDT     WR 58.3%  PF 2.095  lift +0.004 / req 0.10  n=2,370  WR!  cov 94%  [--]
    SOLUSDT     WR 52.6%  PF 1.663  lift -0.001 / req 0.10  n=2,516  WR!  cov 94%  [--]
    BNBUSDT     WR 54.1%  PF 1.771  lift -0.026 / req 0.10  n=1,991  WR!  cov 93%  [--]
    XRPUSDT     WR 50.5%  PF 1.529  lift -0.062 / req 0.10  n=2,534  WR!  cov 91%  [--]
  [Momentum   ]  mfi_below_50                WR lift +0.1pp  avg PF 1.735  PF lift +0.004  0/5 pairs  [XX]  warn: WR 5p
    BTCUSDT     WR 51.6%  PF 1.597  lift +0.083 / req 0.10  n=2,071  WR!  cov 83%  [--]
    ETHUSDT     WR 57.7%  PF 2.046  lift -0.045 / req 0.10  n=2,208  WR!  cov 87%  [--]
    SOLUSDT     WR 53.3%  PF 1.713  lift +0.048 / req 0.10  n=2,311  WR!  cov 86%  [--]
    BNBUSDT     WR 53.6%  PF 1.734  lift -0.062 / req 0.10  n=1,807  WR!  cov 84%  [--]
    XRPUSDT     WR 51.4%  PF 1.586  lift -0.005 / req 0.10  n=2,302  WR!  cov 83%  [--]
  [Confluence ]  rsi_and_mfi                 WR lift +0.1pp  avg PF 1.733  PF lift +0.002  1/5 pairs  [XX]  warn: WR 5p
    BTCUSDT     WR 52.2%  PF 1.640  lift +0.126 / req 0.10  n=1,972  WR!  cov 79%  [OK]
    ETHUSDT     WR 57.8%  PF 2.055  lift -0.036 / req 0.10  n=2,114  WR!  cov 84%  [--]
    SOLUSDT     WR 53.2%  PF 1.708  lift +0.044 / req 0.10  n=2,218  WR!  cov 83%  [--]
    BNBUSDT     WR 53.5%  PF 1.723  lift -0.074 / req 0.10  n=1,721  WR!  cov 80%  [--]
    XRPUSDT     WR 50.7%  PF 1.541  lift -0.050 / req 0.10  n=2,151  WR!  cov 77%  [--]
  [Trend      ]  close_below_ema             WR lift -0.2pp  avg PF 1.716  PF lift -0.016  0/5 pairs  [XX]  warn: WR 5p
    BTCUSDT     WR 50.9%  PF 1.557  lift +0.043 / req 0.10  n=2,234  WR!  cov 90%  [--]
    ETHUSDT     WR 58.2%  PF 2.085  lift -0.006 / req 0.10  n=2,342  WR!  cov 93%  [--]
    SOLUSDT     WR 52.6%  PF 1.663  lift -0.001 / req 0.10  n=2,438  WR!  cov 91%  [--]
    BNBUSDT     WR 53.7%  PF 1.740  lift -0.057 / req 0.10  n=1,942  WR!  cov 91%  [--]
    XRPUSDT     WR 50.5%  PF 1.533  lift -0.058 / req 0.10  n=2,461  WR!  cov 88%  [--]
  [Trend      ]  ema_bearish_order           WR lift +0.1pp  avg PF 1.740  PF lift +0.009  0/5 pairs  [XX]  warn: WR 5p
    BTCUSDT     WR 50.4%  PF 1.521  lift +0.007 / req 0.10  n=2,395  WR!  cov 96%  [--]
    ETHUSDT     WR 58.4%  PF 2.106  lift +0.015 / req 0.10  n=2,457  WR!  cov 97%  [--]
    SOLUSDT     WR 53.0%  PF 1.692  lift +0.027 / req 0.10  n=2,596  WR!  cov 97%  [--]
    BNBUSDT     WR 54.5%  PF 1.795  lift -0.002 / req 0.10  n=2,076  WR!  cov 97%  [--]
    XRPUSDT     WR 51.4%  PF 1.587  lift -0.004 / req 0.10  n=2,673  WR!  cov 96%  [--]
  [MACD       ]  macd_signal_wall            WR lift +0.4pp  avg PF 1.759  PF lift +0.028  1/5 pairs  [XX]  warn: WR 5p
    BTCUSDT     WR 52.6%  PF 1.663  lift +0.148 / req 0.10  n=1,613  WR!  cov 65%  [OK]
    ETHUSDT     WR 58.5%  PF 2.116  lift +0.025 / req 0.10  n=1,702  WR!  cov 67%  [--]
    SOLUSDT     WR 53.2%  PF 1.702  lift +0.038 / req 0.10  n=1,742  WR!  cov 65%  [--]
    BNBUSDT     WR 53.4%  PF 1.721  lift -0.076 / req 0.10  n=1,413  WR!  cov 66%  [--]
    XRPUSDT     WR 51.5%  PF 1.595  lift +0.004 / req 0.10  n=1,828  WR!  cov 66%  [--]
  [Volatility ]  lower_bb_declining          WR lift +0.2pp  avg PF 1.745  PF lift +0.013  0/5 pairs  [XX]  warn: WR 5p
    BTCUSDT     WR 51.6%  PF 1.600  lift +0.085 / req 0.10  n=1,804  WR!  cov 72%  [--]
    ETHUSDT     WR 58.3%  PF 2.094  lift +0.004 / req 0.10  n=1,929  WR!  cov 76%  [--]
    SOLUSDT     WR 52.3%  PF 1.648  lift -0.017 / req 0.10  n=1,920  WR!  cov 72%  [--]
    BNBUSDT     WR 53.6%  PF 1.734  lift -0.063 / req 0.10  n=1,578  WR!  cov 74%  [--]
    XRPUSDT     WR 52.4%  PF 1.649  lift +0.058 / req 0.10  n=1,906  WR!  cov 68%  [--]

  Thresholds: PF lift > 0.02/0.05/0.10 by n,  >= 3 of 5 pairs  (vs rsi_ma_baseline)

  [XX]  SETUP 2 TRIGGER 8 (1h) -- no condition improves on rsi_ma_baseline.
        rsi_ma_baseline avg PF was 1.732.
      Tuning ideas:
        * Lower rsi_ma_threshold (currently 50.0)
        * Try rsi_ma_type='sma' (currently ema)
        * Adjust ema_slow (currently 20)

  Warnings (results valid -- interpret with care):
    !! [rsi_below_50] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [mfi_below_50] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [rsi_and_mfi] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [close_below_ema] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [ema_bearish_order] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [macd_signal_wall] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
    !! [lower_bb_declining] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT
```
