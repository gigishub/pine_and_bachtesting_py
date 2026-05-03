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
| `rsi_threshold` | `50.0` |
| `mfi_period` | `14` |
| `mfi_threshold` | `50.0` |
| `rsi_ma_period` | `9` |
| `rsi_ma_type` | `ema` |
| `rsi_ma_threshold` | `50.0` |

```text

-- Per-Pair Results (baseline = kde_upper_baseline on 4h) --

  BTCUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  46.74  1.316  18.2      1318
rsi_below_50        50.83  1.551  21.0       600
mfi_below_50        48.87  1.434  19.6       620
rsi_ma_below_50     50.00  1.500  20.5       510
rsi_below_ma        50.07  1.504  19.4       721

    rsi_below_50        covers 45.5% of baseline bars
    mfi_below_50        covers 47.0% of baseline bars
    rsi_ma_below_50     covers 38.7% of baseline bars
    rsi_below_ma        covers 54.7% of baseline bars  !! HIGH

  ETHUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  48.63  1.420  22.0      1314
rsi_below_50        50.87  1.553  28.7       574
mfi_below_50        56.43  1.943  28.5       560
rsi_ma_below_50     48.62  1.420  32.2       436
rsi_below_ma        50.52  1.532  24.3       768

    rsi_below_50        covers 43.7% of baseline bars
    mfi_below_50        covers 42.6% of baseline bars
    rsi_ma_below_50     covers 33.2% of baseline bars
    rsi_below_ma        covers 58.4% of baseline bars  !! HIGH

  SOLUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  47.02  1.331  19.9      1359
rsi_below_50        46.29  1.293  21.5       620
mfi_below_50        49.82  1.489  21.5       564
rsi_ma_below_50     45.38  1.246  21.2       498
rsi_below_ma        48.10  1.390  20.0       765

    rsi_below_50        covers 45.6% of baseline bars
    mfi_below_50        covers 41.5% of baseline bars
    rsi_ma_below_50     covers 36.6% of baseline bars
    rsi_below_ma        covers 56.3% of baseline bars  !! HIGH

  BNBUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  50.18  1.511  19.2      1082
rsi_below_50        58.80  2.141  28.1       466
mfi_below_50        56.25  1.929  21.2       448
rsi_ma_below_50     59.94  2.245  29.1       362
rsi_below_ma        50.65  1.539  21.3       616

    rsi_below_50        covers 43.1% of baseline bars
    mfi_below_50        covers 41.4% of baseline bars
    rsi_ma_below_50     covers 33.5% of baseline bars
    rsi_below_ma        covers 56.9% of baseline bars  !! HIGH

  XRPUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  52.78  1.677  18.6      1294
rsi_below_50        60.32  2.280  20.4       625
mfi_below_50        52.28  1.644  18.9       635
rsi_ma_below_50     63.86  2.651  18.8       523
rsi_below_ma        54.43  1.792  20.1       790

    rsi_below_50        covers 48.3% of baseline bars
    mfi_below_50        covers 49.1% of baseline bars
    rsi_ma_below_50     covers 40.4% of baseline bars
    rsi_below_ma        covers 61.1% of baseline bars  !! HIGH


-- Setup 2 Trigger 4 (4h) -- Verdict --

  Baseline (kde_upper_baseline on 4h):  avg WR 49.1%  avg PF 1.451
  KDE (4h): window=200  bw=1  |  RSI(14)h50  MFI(14)h50  RSI/EMA(9)h50  RSI<EMA(9)

  [Oscillator  ]  rsi_below_50        WR lift +4.4pp  avg PF 1.764  PF lift +0.312  4/5 pairs  [OK]  warn: WR 3p
    BTCUSDT     WR 50.8%  PF 1.551  lift +0.235 / req 0.10  n=600  WR!  cov 46%  [OK]
    ETHUSDT     WR 50.9%  PF 1.553  lift +0.133 / req 0.10  n=574  WR!  cov 44%  [OK]
    SOLUSDT     WR 46.3%  PF 1.293  lift -0.038 / req 0.10  n=620  WR!  cov 46%  [--]
    BNBUSDT     WR 58.8%  PF 2.141  lift +0.629 / req 0.10  n=466  cov 43%  [OK]
    XRPUSDT     WR 60.3%  PF 2.280  lift +0.603 / req 0.10  n=625  cov 48%  [OK]
  [Volume      ]  mfi_below_50        WR lift +3.7pp  avg PF 1.688  PF lift +0.237  4/5 pairs  [OK]  warn: WR 3p
    BTCUSDT     WR 48.9%  PF 1.434  lift +0.118 / req 0.10  n=620  WR!  cov 47%  [OK]
    ETHUSDT     WR 56.4%  PF 1.943  lift +0.523 / req 0.10  n=560  cov 43%  [OK]
    SOLUSDT     WR 49.8%  PF 1.489  lift +0.158 / req 0.10  n=564  WR!  cov 42%  [OK]
    BNBUSDT     WR 56.2%  PF 1.929  lift +0.417 / req 0.10  n=448  cov 41%  [OK]
    XRPUSDT     WR 52.3%  PF 1.644  lift -0.033 / req 0.10  n=635  WR!  cov 49%  [--]
  [Oscillator  ]  rsi_ma_below_50     WR lift +4.5pp  avg PF 1.812  PF lift +0.361  3/5 pairs  [OK]  warn: WR 3p
    BTCUSDT     WR 50.0%  PF 1.500  lift +0.184 / req 0.10  n=510  WR!  cov 39%  [OK]
    ETHUSDT     WR 48.6%  PF 1.420  lift -0.000 / req 0.10  n=436  WR!  cov 33%  [--]
    SOLUSDT     WR 45.4%  PF 1.246  lift -0.085 / req 0.10  n=498  WR!  cov 37%  [--]
    BNBUSDT     WR 59.9%  PF 2.245  lift +0.734 / req 0.10  n=362  cov 33%  [OK]
    XRPUSDT     WR 63.9%  PF 2.651  lift +0.974 / req 0.10  n=523  cov 40%  [OK]
  [Oscillator  ]  rsi_below_ma        WR lift +1.7pp  avg PF 1.551  PF lift +0.100  3/5 pairs  [OK]  warn: WR 5p
    BTCUSDT     WR 50.1%  PF 1.504  lift +0.188 / req 0.10  n=721  WR!  cov 55%  [OK]
    ETHUSDT     WR 50.5%  PF 1.532  lift +0.112 / req 0.10  n=768  WR!  cov 58%  [OK]
    SOLUSDT     WR 48.1%  PF 1.390  lift +0.059 / req 0.10  n=765  WR!  cov 56%  [--]
    BNBUSDT     WR 50.6%  PF 1.539  lift +0.028 / req 0.10  n=616  WR!  cov 57%  [--]
    XRPUSDT     WR 54.4%  PF 1.792  lift +0.115 / req 0.10  n=790  WR!  cov 61%  [OK]

  Thresholds: PF lift > 0.02/0.05/0.10 by n,  >= 3 of 5 pairs

  [OK]  SETUP 2 TRIGGER 4 (4h) CONFIRMED -- populations below improve on kde_upper_baseline.
        Base: avg PF 1.451  |  Best: rsi_ma_below_50  (avg PF 1.812)

  Warnings (results valid -- interpret with care):
    !! [rsi_below_50] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT
    !! [mfi_below_50] WR lift below threshold on: BTCUSDT, SOLUSDT, XRPUSDT
    !! [rsi_ma_below_50] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT
    !! [rsi_below_ma] WR lift below threshold on: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT

  -- Confirmed populations --
    [Oscillator]
      [OK] rsi_below_50          avg PF 1.764
      [OK] rsi_below_ma          avg PF 1.551
      [OK] rsi_ma_below_50       avg PF 1.812
    [Volume]
      [OK] mfi_below_50          avg PF 1.688

  Proceed using confirmed positional filter(s) for setup 3 construction.
```
