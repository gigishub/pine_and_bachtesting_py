# Bear Strategy -- Setup 2 Trigger: KDE Upper (4h) + 4h signals  (entry_tf=4h  kde_tf=4h)

## Test Parameters

| Parameter | Value |
|-----------|-------|
| `entry_tf` | `4h` |
| `kde_tf` | `4h` |
| `context_tf` | `1d` |
| `stop_atr_mult` | `2.0` |
| `target_atr_mult` | `3.0` |
| `atr_period` | `7` |
| `kde_window` | `200` |
| `kde_bandwidth_mult` | `1.0` |
| `vwap_anchor` | `weekly` |
| `vpvr_window` | `50` |
| `vpvr_n_bins` | `50` |
| `setup_distance_atr` | `1.0` |
| `rvol_window` | `20` |
| `rvol_threshold` | `1.4` |

```text

-- Per-Pair Results (baseline = kde_upper_baseline on 4h) --

  BTCUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  46.74  1.316  18.2      1318
vwap_only           45.92  1.274  18.7       699
vpvr_only           45.83  1.269  18.7       192
near_setup          45.31  1.243  18.8       799
rvol_only           46.33  1.295  26.1       300
vwap_and_rvol       48.75  1.427  26.6       160
vpvr_and_rvol       41.18  1.050  24.3        34
near_and_rvol       46.29  1.293  26.5       175

    vwap_only               covers 53.0% of baseline bars
    vpvr_only               covers 14.6% of baseline bars  !! LOW
    near_setup              covers 60.6% of baseline bars
    rvol_only               covers 22.8% of baseline bars  !! LOW
    vwap_and_rvol           covers 12.1% of baseline bars  !! LOW
    vpvr_and_rvol           covers 2.6% of baseline bars  !! LOW
    near_and_rvol           covers 13.3% of baseline bars  !! LOW

  ETHUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  48.63  1.420  22.0      1314
vwap_only           49.72  1.483  20.9       710
vpvr_only           44.94  1.224  18.8       178
near_setup          49.13  1.449  21.1       802
rvol_only           46.79  1.319  31.8       312
vwap_and_rvol       46.88  1.324  27.9       192
vpvr_and_rvol       46.88  1.324  26.3        32
near_and_rvol       47.12  1.336  28.7       208

    vwap_only               covers 54.0% of baseline bars
    vpvr_only               covers 13.5% of baseline bars  !! LOW
    near_setup              covers 61.0% of baseline bars
    rvol_only               covers 23.7% of baseline bars  !! LOW
    vwap_and_rvol           covers 14.6% of baseline bars  !! LOW
    vpvr_and_rvol           covers 2.4% of baseline bars  !! LOW
    near_and_rvol           covers 15.8% of baseline bars  !! LOW

  SOLUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  47.02  1.331  19.9      1359
vwap_only           44.81  1.218  19.0       723
vpvr_only           42.58  1.112  15.7       209
near_setup          45.29  1.242  18.5       839
rvol_only           51.81  1.612  21.9       249
vwap_and_rvol       45.04  1.229  18.4       131
vpvr_and_rvol       60.00  2.250  16.6        40
near_and_rvol       48.05  1.388  18.4       154

    vwap_only               covers 53.2% of baseline bars
    vpvr_only               covers 15.4% of baseline bars  !! LOW
    near_setup              covers 61.7% of baseline bars
    rvol_only               covers 18.3% of baseline bars  !! LOW
    vwap_and_rvol           covers 9.6% of baseline bars  !! LOW
    vpvr_and_rvol           covers 2.9% of baseline bars  !! LOW
    near_and_rvol           covers 11.3% of baseline bars  !! LOW

  BNBUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  50.18  1.511  19.2      1082
vwap_only           51.19  1.573  21.5       588
vpvr_only           63.64  2.625  16.0       132
near_setup          52.54  1.661  20.9       649
rvol_only           49.79  1.487  25.5       233
vwap_and_rvol       52.63  1.667  27.8       114
vpvr_and_rvol       61.90  2.438  29.4        21
near_and_rvol       54.03  1.763  27.7       124

    vwap_only               covers 54.3% of baseline bars
    vpvr_only               covers 12.2% of baseline bars  !! LOW
    near_setup              covers 60.0% of baseline bars
    rvol_only               covers 21.5% of baseline bars  !! LOW
    vwap_and_rvol           covers 10.5% of baseline bars  !! LOW
    vpvr_and_rvol           covers 1.9% of baseline bars  !! LOW
    near_and_rvol           covers 11.5% of baseline bars  !! LOW

  XRPUSDT
                     wr_%     pf   dur  n_trades
population                                      
kde_upper_baseline  52.78  1.677  18.6      1294
vwap_only           52.52  1.659  19.2       695
vpvr_only           53.33  1.714  17.8       150
near_setup          53.32  1.714  18.9       767
rvol_only           50.46  1.528  26.8       218
vwap_and_rvol       49.18  1.452  25.2       122
vpvr_and_rvol       48.28  1.400  19.2        29
near_and_rvol       51.09  1.567  24.6       137

    vwap_only               covers 53.7% of baseline bars
    vpvr_only               covers 11.6% of baseline bars  !! LOW
    near_setup              covers 59.3% of baseline bars
    rvol_only               covers 16.8% of baseline bars  !! LOW
    vwap_and_rvol           covers 9.4% of baseline bars  !! LOW
    vpvr_and_rvol           covers 2.2% of baseline bars  !! LOW
    near_and_rvol           covers 10.6% of baseline bars  !! LOW


-- Setup 2 Trigger (4h) -- Verdict --

  Baseline (kde_upper_baseline on 4h):  avg WR 49.1%  avg PF 1.451
  KDE (4h): window=200  bw=1  |  dist=1xATR(4h)  |  RVOL: 20 bars (5h) threshold=1.4


  [Level only   ]  vwap_only               WR lift -0.2pp  avg PF 1.441  PF lift -0.010  0/5 pairs  [XX]  warn: WR 5p
    BTCUSDT     WR 45.9%  PF 1.274  lift -0.042 / req 0.10  n=699  WR!  cov 53%  [--]
    ETHUSDT     WR 49.7%  PF 1.483  lift +0.063 / req 0.10  n=710  WR!  cov 54%  [--]
    SOLUSDT     WR 44.8%  PF 1.218  lift -0.113 / req 0.10  n=723  WR!  cov 53%  [--]
    BNBUSDT     WR 51.2%  PF 1.573  lift +0.062 / req 0.10  n=588  WR!  cov 54%  [--]
    XRPUSDT     WR 52.5%  PF 1.659  lift -0.018 / req 0.10  n=695  WR!  cov 54%  [--]
  [Level only   ]  vpvr_only               WR lift +1.0pp  avg PF 1.589  PF lift +0.138  1/5 pairs  [XX]  warn: WR 4p, low# 5p
    BTCUSDT     WR 45.8%  PF 1.269  lift -0.047 / req 0.10  n=192  WR!  cov 15%!  [--]
    ETHUSDT     WR 44.9%  PF 1.224  lift -0.196 / req 0.10  n=178  WR!  cov 14%!  [--]
    SOLUSDT     WR 42.6%  PF 1.113  lift -0.219 / req 0.10  n=209  WR!  cov 15%!  [--]
    BNBUSDT     WR 63.6%  PF 2.625  lift +1.114 / req 0.10  n=132  cov 12%!  [OK]
    XRPUSDT     WR 53.3%  PF 1.714  lift +0.038 / req 0.10  n=150  WR!  cov 12%!  [--]
  [Level only   ]  near_setup              WR lift +0.0pp  avg PF 1.461  PF lift +0.010  1/5 pairs  [XX]  warn: WR 5p
    BTCUSDT     WR 45.3%  PF 1.243  lift -0.074 / req 0.10  n=799  WR!  cov 61%  [--]
    ETHUSDT     WR 49.1%  PF 1.449  lift +0.029 / req 0.10  n=802  WR!  cov 61%  [--]
    SOLUSDT     WR 45.3%  PF 1.242  lift -0.089 / req 0.10  n=839  WR!  cov 62%  [--]
    BNBUSDT     WR 52.5%  PF 1.661  lift +0.150 / req 0.10  n=649  WR!  cov 60%  [OK]
    XRPUSDT     WR 53.3%  PF 1.714  lift +0.037 / req 0.10  n=767  WR!  cov 59%  [--]

  [RVOL only    ]  rvol_only               WR lift -0.0pp  avg PF 1.448  PF lift -0.003  1/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 46.3%  PF 1.295  lift -0.021 / req 0.10  n=300  WR!  cov 23%!  [--]
    ETHUSDT     WR 46.8%  PF 1.319  lift -0.101 / req 0.10  n=312  WR!  cov 24%!  [--]
    SOLUSDT     WR 51.8%  PF 1.613  lift +0.281 / req 0.10  n=249  WR!  cov 18%!  [OK]
    BNBUSDT     WR 49.8%  PF 1.487  lift -0.024 / req 0.10  n=233  WR!  cov 22%!  [--]
    XRPUSDT     WR 50.5%  PF 1.528  lift -0.149 / req 0.10  n=218  WR!  cov 17%!  [--]

  [Level + RVOL ]  vwap_and_rvol           WR lift -0.6pp  avg PF 1.420  PF lift -0.032  2/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 48.8%  PF 1.427  lift +0.111 / req 0.10  n=160  WR!  cov 12%!  [OK]
    ETHUSDT     WR 46.9%  PF 1.324  lift -0.096 / req 0.10  n=192  WR!  cov 15%!  [--]
    SOLUSDT     WR 45.0%  PF 1.229  lift -0.102 / req 0.10  n=131  WR!  cov 10%!  [--]
    BNBUSDT     WR 52.6%  PF 1.667  lift +0.156 / req 0.10  n=114  WR!  cov 11%!  [OK]
    XRPUSDT     WR 49.2%  PF 1.452  lift -0.225 / req 0.10  n=122  WR!  cov 9%!  [--]
  [Level + RVOL ]  vpvr_and_rvol           WR lift +2.6pp  avg PF 1.692  PF lift +0.241  2/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 41.2%  PF 1.050  lift -0.266 / req 0.10  n=34  WR!  cov 3%!  [--]
    ETHUSDT     WR 46.9%  PF 1.324  lift -0.096 / req 0.10  n=32  WR!  cov 2%!  [--]
    SOLUSDT     WR 60.0%  PF 2.250  lift +0.919 / req 0.10  n=40  WR!  cov 3%!  [OK]
    BNBUSDT     WR 61.9%  PF 2.438  lift +0.926 / req 0.10  n=21  WR!  cov 2%!  [OK]
    XRPUSDT     WR 48.3%  PF 1.400  lift -0.277 / req 0.10  n=29  WR!  cov 2%!  [--]
  [Level + RVOL ]  near_and_rvol           WR lift +0.2pp  avg PF 1.469  PF lift +0.018  1/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 46.3%  PF 1.293  lift -0.024 / req 0.10  n=175  WR!  cov 13%!  [--]
    ETHUSDT     WR 47.1%  PF 1.336  lift -0.084 / req 0.10  n=208  WR!  cov 16%!  [--]
    SOLUSDT     WR 48.1%  PF 1.387  lift +0.056 / req 0.10  n=154  WR!  cov 11%!  [--]
    BNBUSDT     WR 54.0%  PF 1.763  lift +0.252 / req 0.10  n=124  WR!  cov 11%!  [OK]
    XRPUSDT     WR 51.1%  PF 1.567  lift -0.110 / req 0.10  n=137  WR!  cov 11%!  [--]

  Thresholds: PF lift > 0.02/0.05/0.10 by n,  >= 3 of 5 pairs

  [XX]  SETUP 2 TRIGGER (4h) -- no population improves on kde_upper_baseline.
        Baseline avg PF was 1.451  -- 15m filters add no measurable edge.
      Next steps:
        * Widen proximity (currently 1 x ATR(4h))
        * Raise RVOL threshold (currently 1.4x, window=20 bars)
```
