# Bear Strategy -- Setup 2 Candle Trigger: KDE Upper (4h) + 1h bar quality  (entry_tf=1h  kde_tf=4h)

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
| `rvol_window` | `96` |
| `rvol_threshold` | `1.0` |
| `wick_ratio_threshold` | `0.5` |
| `breakdown_close_pct` | `0.25` |
| `roc_period` | `3` |

```text

-- Per-Pair Results (baseline = kde_upper_baseline on 1h) --

  BTCUSDT
                       wr_%     pf   dur  n_trades
population                                        
kde_upper_baseline    47.76  1.371  20.9      5272
bearish_rvol          50.74  1.545  33.1      1015
upper_wick_rejection  48.54  1.415  20.1       820
breakdown_bar         47.15  1.338  20.7      1228
roc_negative          48.49  1.412  22.8      2873
bearish_engulf        45.28  1.241  20.4       678

    bearish_rvol            covers 19.3% of baseline bars  !! LOW
    upper_wick_rejection    covers 15.6% of baseline bars  !! LOW
    breakdown_bar           covers 23.3% of baseline bars  !! LOW
    roc_negative            covers 54.5% of baseline bars
    bearish_engulf          covers 12.9% of baseline bars  !! LOW

  ETHUSDT

Updated confirmed inventory:

┌──────────────────┬────────┬────────┐
│ Signal           │ Avg PF │ Source │
├──────────────────┼────────┼────────┤
│ rsi_ma_below_50  │ 1.969  │ T4     │
├──────────────────┼────────┼────────┤
│ rsi_and_mfi      │ 1.901  │ T4     │
├──────────────────┼────────┼────────┤
│ signal_line_wall │ 1.893  │ T6     │
├──────────────────┼────────┼────────┤
│ squeeze_snap     │ 1.893  │ T5     │
├──────────────────┼────────┼────────┤
│ ema_tightening   │ 1.810  │ T7     │
├──────────────────┼────────┼────────┤
│ momentum_close   │ 1.862  │ T5     │
├──────────────────┼────────┼────────┤
│ rsi_below_50     │ 1.841  │ T4     │
├──────────────────┼────────┼────────┤
│ falling_tunnel   │ 1.763  │ T5     │
├──────────────────┼────────┼────────┤
│ mfi_below_50     │ 1.723  │ T4     │
├──────────────────┼────────┼────────┤
│ lower_expansion  │ 1.678  │ T5     │
└──────────────────┴────────┴────────┘


    bearish_rvol            covers 20.8% of baseline bars  !! LOW
    upper_wick_rejection    covers 15.6% of baseline bars  !! LOW
    breakdown_bar           covers 23.0% of baseline bars  !! LOW
    roc_negative            covers 55.9% of baseline bars
    bearish_engulf          covers 12.9% of baseline bars  !! LOW

  SOLUSDT
                       wr_%     pf   dur  n_trades
population                                        
kde_upper_baseline    48.91  1.436  18.8      5475
bearish_rvol          48.93  1.437  25.7      1073
upper_wick_rejection  49.14  1.449  17.1       816
breakdown_bar         49.36  1.462  19.6      1323
roc_negative          48.07  1.388  20.1      3075
bearish_engulf        46.74  1.316  19.1       721

    bearish_rvol            covers 19.6% of baseline bars  !! LOW
    upper_wick_rejection    covers 14.9% of baseline bars  !! LOW
    breakdown_bar           covers 24.2% of baseline bars  !! LOW
    roc_negative            covers 56.2% of baseline bars
    bearish_engulf          covers 13.2% of baseline bars  !! LOW

  BNBUSDT
                       wr_%     pf   dur  n_trades
population                                        
kde_upper_baseline    51.36  1.584  21.1      4367
bearish_rvol          47.49  1.357  29.4       798
upper_wick_rejection  50.70  1.542  22.5       647
breakdown_bar         48.50  1.413  20.5      1035
roc_negative          51.53  1.594  23.4      2393
bearish_engulf        49.30  1.459  21.0       574

    bearish_rvol            covers 18.3% of baseline bars  !! LOW
    upper_wick_rejection    covers 14.8% of baseline bars  !! LOW
    breakdown_bar           covers 23.7% of baseline bars  !! LOW
    roc_negative            covers 54.8% of baseline bars
    bearish_engulf          covers 13.1% of baseline bars  !! LOW

  XRPUSDT
                       wr_%     pf   dur  n_trades
population                                        
kde_upper_baseline    51.86  1.616  22.3      5195
bearish_rvol          50.88  1.554  31.4       969
upper_wick_rejection  51.84  1.615  19.7       733
breakdown_bar         50.80  1.549  20.7      1187
roc_negative          50.99  1.560  24.1      2842
bearish_engulf        47.90  1.379  22.2       691

    bearish_rvol            covers 18.7% of baseline bars  !! LOW
    upper_wick_rejection    covers 14.1% of baseline bars  !! LOW
    breakdown_bar           covers 22.8% of baseline bars  !! LOW
    roc_negative            covers 54.7% of baseline bars
    bearish_engulf          covers 13.3% of baseline bars  !! LOW


-- Setup 2 Candle Trigger (1h) -- Verdict --

  Baseline (kde_upper_baseline on 1h):  avg WR 50.7%  avg PF 1.551
  KDE (4h): window=200  bw=1  |  RVOL: 96 bars (24h) threshold=1  |  wick=0.5  breakdown=0.25  roc=3bars

  [Bar quality  ]  bearish_rvol            WR lift +0.2pp  avg PF 1.569  PF lift +0.018  2/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 50.7%  PF 1.545  lift +0.174 / req 0.10  n=1,015  WR!  cov 19%!  [OK]
    ETHUSDT     WR 56.5%  PF 1.952  lift +0.206 / req 0.10  n=1,093  WR!  cov 21%!  [OK]
    SOLUSDT     WR 48.9%  PF 1.437  lift +0.001 / req 0.10  n=1,073  WR!  cov 20%!  [--]
    BNBUSDT     WR 47.5%  PF 1.357  lift -0.227 / req 0.10  n=798  WR!  cov 18%!  [--]
    XRPUSDT     WR 50.9%  PF 1.554  lift -0.062 / req 0.10  n=969  WR!  cov 19%!  [--]
  [Bar quality  ]  upper_wick_rejection    WR lift -0.0pp  avg PF 1.548  PF lift -0.003  0/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 48.5%  PF 1.415  lift +0.043 / req 0.10  n=820  WR!  cov 16%!  [--]
    ETHUSDT     WR 53.4%  PF 1.719  lift -0.026 / req 0.10  n=822  WR!  cov 16%!  [--]
    SOLUSDT     WR 49.1%  PF 1.449  lift +0.013 / req 0.10  n=816  WR!  cov 15%!  [--]
    BNBUSDT     WR 50.7%  PF 1.542  lift -0.042 / req 0.10  n=647  WR!  cov 15%!  [--]
    XRPUSDT     WR 51.8%  PF 1.615  lift -0.001 / req 0.10  n=733  WR!  cov 14%!  [--]
  [Bar quality  ]  breakdown_bar           WR lift -0.7pp  avg PF 1.509  PF lift -0.042  0/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 47.1%  PF 1.338  lift -0.033 / req 0.10  n=1,228  WR!  cov 23%!  [--]
    ETHUSDT     WR 54.3%  PF 1.783  lift +0.037 / req 0.10  n=1,208  WR!  cov 23%!  [--]
    SOLUSDT     WR 49.4%  PF 1.462  lift +0.026 / req 0.10  n=1,323  WR!  cov 24%!  [--]
    BNBUSDT     WR 48.5%  PF 1.413  lift -0.171 / req 0.10  n=1,035  WR!  cov 24%!  [--]
    XRPUSDT     WR 50.8%  PF 1.549  lift -0.067 / req 0.10  n=1,187  WR!  cov 23%!  [--]
  [Momentum     ]  roc_negative            WR lift +0.1pp  avg PF 1.556  PF lift +0.006  0/5 pairs  [XX]  warn: WR 5p
    BTCUSDT     WR 48.5%  PF 1.412  lift +0.040 / req 0.10  n=2,873  WR!  cov 54%  [--]
    ETHUSDT     WR 54.9%  PF 1.826  lift +0.080 / req 0.10  n=2,938  WR!  cov 56%  [--]
    SOLUSDT     WR 48.1%  PF 1.388  lift -0.048 / req 0.10  n=3,075  WR!  cov 56%  [--]
    BNBUSDT     WR 51.5%  PF 1.594  lift +0.010 / req 0.10  n=2,393  WR!  cov 55%  [--]
    XRPUSDT     WR 51.0%  PF 1.560  lift -0.055 / req 0.10  n=2,842  WR!  cov 55%  [--]
  [Pattern      ]  bearish_engulf          WR lift -2.2pp  avg PF 1.422  PF lift -0.129  0/5 pairs  [XX]  warn: WR 5p, low# 5p
    BTCUSDT     WR 45.3%  PF 1.241  lift -0.130 / req 0.10  n=678  WR!  cov 13%!  [--]
    ETHUSDT     WR 53.3%  PF 1.713  lift -0.033 / req 0.10  n=679  WR!  cov 13%!  [--]
    SOLUSDT     WR 46.7%  PF 1.316  lift -0.120 / req 0.10  n=721  WR!  cov 13%!  [--]
    BNBUSDT     WR 49.3%  PF 1.459  lift -0.125 / req 0.10  n=574  WR!  cov 13%!  [--]
    XRPUSDT     WR 47.9%  PF 1.379  lift -0.237 / req 0.10  n=691  WR!  cov 13%!  [--]

  Thresholds: PF lift > 0.02/0.05/0.10 by n,  >= 3 of 5 pairs

  [XX]  SETUP 2 CANDLE TRIGGER (1h) -- no population improves on kde_upper_baseline.
        Baseline avg PF was 1.551  -- bar-quality signals add no measurable edge.
      Next steps:
        * Loosen wick threshold (currently 0.5 of bar range)
        * Raise RVOL threshold (currently 1x, window=96 bars)
        * Try longer ROC period (currently 3 bars)
```
