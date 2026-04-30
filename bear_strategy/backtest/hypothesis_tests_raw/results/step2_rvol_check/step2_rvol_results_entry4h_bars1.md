# RVOL Setup Edge Check

```text

── Per-Pair Results ──

  BTCUSDT
                     wr_%     pf   dur  n_trades
population                                      
regime_only         43.59  1.159  22.4      5877
rvol_spike          41.42  1.061  27.9      1142
rvol_spike_bearish  42.88  1.126  29.3       695
rvol_spike_down     42.88  1.126  29.3       695
    rvol_spike covers 19.4% of regime bars  ⚠️  LOW
    rvol_spike_bearish covers 11.8% of regime bars  ⚠️  LOW
    rvol_spike_down covers 11.8% of regime bars  ⚠️  LOW

  ETHUSDT
                     wr_%     pf   dur  n_trades
population                                      
regime_only         41.96  1.084  22.5      5975
rvol_spike          41.70  1.073  29.7      1120
rvol_spike_bearish  43.82  1.170  28.9       696
rvol_spike_down     43.82  1.170  28.9       696
    rvol_spike covers 18.7% of regime bars  ⚠️  LOW
    rvol_spike_bearish covers 11.6% of regime bars  ⚠️  LOW
    rvol_spike_down covers 11.6% of regime bars  ⚠️  LOW

  SOLUSDT
                     wr_%     pf   dur  n_trades
population                                      
regime_only         43.46  1.153  22.3      5568
rvol_spike          42.32  1.101  32.4       964
rvol_spike_bearish  42.78  1.122  36.0       582
rvol_spike_down     42.78  1.122  36.0       582
    rvol_spike covers 17.3% of regime bars  ⚠️  LOW
    rvol_spike_bearish covers 10.5% of regime bars  ⚠️  LOW
    rvol_spike_down covers 10.5% of regime bars  ⚠️  LOW

  BNBUSDT
                     wr_%     pf   dur  n_trades
population                                      
regime_only         45.51  1.253  19.0      5038
rvol_spike          43.34  1.147  23.9       893
rvol_spike_bearish  44.62  1.208  23.7       520
rvol_spike_down     44.62  1.208  23.7       520
    rvol_spike covers 17.7% of regime bars  ⚠️  LOW
    rvol_spike_bearish covers 10.3% of regime bars  ⚠️  LOW
    rvol_spike_down covers 10.3% of regime bars  ⚠️  LOW

  XRPUSDT
                     wr_%     pf   dur  n_trades
population                                      
regime_only         43.64  1.162  23.9      6141
rvol_spike          41.70  1.073  36.8       952
rvol_spike_bearish  41.97  1.085  35.3       579
rvol_spike_down     41.97  1.085  35.3       579
    rvol_spike covers 15.5% of regime bars  ⚠️  LOW
    rvol_spike_bearish covers 9.4% of regime bars  ⚠️  LOW
    rvol_spike_down covers 9.4% of regime bars  ⚠️  LOW

── RVOL Setup Edge Verdict ──

  Baseline (regime_only):  avg WR 43.6%  avg PF 1.162
  RVOL config: threshold=1.5×  vol_ma_len=20  min_bars_active=1

  rvol_spike              avg WR lift -1.54pp  avg PF 1.091  avg PF lift -0.071  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 41.42%  lift -2.18pp / req 3.67pp  PF 1.061  lift -0.099 / req 0.100  trades 1,142  cov 19.4% ⚠️  ❌
    ETHUSDT     WR 41.70%  lift -0.26pp / req 3.69pp  PF 1.073  lift -0.012 / req 0.100  trades 1,120  cov 18.7% ⚠️  ❌
    SOLUSDT     WR 42.32%  lift -1.14pp / req 3.99pp  PF 1.101  lift -0.052 / req 0.100  trades 964  cov 17.3% ⚠️  ❌
    BNBUSDT     WR 43.34%  lift -2.18pp / req 4.17pp  PF 1.147  lift -0.106 / req 0.100  trades 893  cov 17.7% ⚠️  ❌
    XRPUSDT     WR 41.70%  lift -1.94pp / req 4.02pp  PF 1.073  lift -0.089 / req 0.100  trades 952  cov 15.5% ⚠️  ❌

  rvol_spike_bearish      avg WR lift -0.42pp  avg PF 1.142  avg PF lift -0.020  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 42.88%  lift -0.72pp / req 4.70pp  PF 1.126  lift -0.033 / req 0.100  trades 695  cov 11.8% ⚠️  ❌
    ETHUSDT     WR 43.82%  lift +1.86pp / req 4.68pp  PF 1.170  lift +0.086 / req 0.100  trades 696  cov 11.6% ⚠️  ❌
    SOLUSDT     WR 42.78%  lift -0.68pp / req 5.14pp  PF 1.122  lift -0.031 / req 0.100  trades 582  cov 10.5% ⚠️  ❌
    BNBUSDT     WR 44.62%  lift -0.90pp / req 5.46pp  PF 1.208  lift -0.045 / req 0.100  trades 520  cov 10.3% ⚠️  ❌
    XRPUSDT     WR 41.97%  lift -1.67pp / req 5.15pp  PF 1.085  lift -0.077 / req 0.100  trades 579  cov 9.4% ⚠️  ❌

  rvol_spike_down         avg WR lift -0.42pp  avg PF 1.142  avg PF lift -0.020  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 42.88%  lift -0.72pp / req 4.70pp  PF 1.126  lift -0.033 / req 0.100  trades 695  cov 11.8% ⚠️  ❌
    ETHUSDT     WR 43.82%  lift +1.86pp / req 4.68pp  PF 1.170  lift +0.086 / req 0.100  trades 696  cov 11.6% ⚠️  ❌
    SOLUSDT     WR 42.78%  lift -0.68pp / req 5.14pp  PF 1.122  lift -0.031 / req 0.100  trades 582  cov 10.5% ⚠️  ❌
    BNBUSDT     WR 44.62%  lift -0.90pp / req 5.46pp  PF 1.208  lift -0.045 / req 0.100  trades 520  cov 10.3% ⚠️  ❌
    XRPUSDT     WR 41.97%  lift -1.67pp / req 5.15pp  PF 1.085  lift -0.077 / req 0.100  trades 579  cov 9.4% ⚠️  ❌

  Thresholds: WR lift > 2.5×sqrt(p(1-p)/n),  PF lift > 0.02/0.05/0.10 by n,  trades > 500,  consistent across ≥ 4 of 5 pairs

  ❌  RVOL EDGE NOT CONFIRMED — no population clears all thresholds.
      Next steps:
        • Increase min_bars_active (reduces noise on lower TF)
        • Try rvol_threshold = 2.0 (stricter spike definition)
        • Try vol_ma_len = 10 or 50
        • Try a different entry_tf in config.py
        • Re-examine whether setup layer is needed before trigger layer
```
