# RVOL Setup Edge Check

```text

── Per-Pair Results ──

  BTCUSDT
                     wr_%     pf   dur  n_trades
population                                      
regime_only         44.25  1.191  20.4     23544
rvol_spike          44.23  1.189  28.2      4434
rvol_spike_bearish  44.71  1.213  27.4      2431
rvol_spike_down     44.71  1.213  27.4      2431
    rvol_spike covers 18.8% of regime bars  ⚠️  LOW
    rvol_spike_bearish covers 10.3% of regime bars  ⚠️  LOW
    rvol_spike_down covers 10.3% of regime bars  ⚠️  LOW

  ETHUSDT
                     wr_%     pf   dur  n_trades
population                                      
regime_only         45.01  1.228  19.9     23904
rvol_spike          45.03  1.229  29.5      4364
rvol_spike_bearish  45.39  1.247  29.0      2463
rvol_spike_down     45.39  1.247  29.0      2463
    rvol_spike covers 18.3% of regime bars  ⚠️  LOW
    rvol_spike_bearish covers 10.3% of regime bars  ⚠️  LOW
    rvol_spike_down covers 10.3% of regime bars  ⚠️  LOW

  SOLUSDT
                     wr_%     pf   dur  n_trades
population                                      
regime_only         44.84  1.219  19.5     22371
rvol_spike          45.20  1.237  26.2      3958
rvol_spike_bearish  46.43  1.300  25.7      2240
rvol_spike_down     46.43  1.300  25.7      2240
    rvol_spike covers 17.7% of regime bars  ⚠️  LOW
    rvol_spike_bearish covers 10.0% of regime bars  ⚠️  LOW
    rvol_spike_down covers 10.0% of regime bars  ⚠️  LOW

  BNBUSDT
                     wr_%     pf   dur  n_trades
population                                      
regime_only         44.88  1.222  19.0     20243
rvol_spike          44.19  1.188  25.0      3632
rvol_spike_bearish  45.50  1.253  23.7      2013
rvol_spike_down     45.50  1.253  23.7      2013
    rvol_spike covers 17.9% of regime bars  ⚠️  LOW
    rvol_spike_bearish covers 9.9% of regime bars  ⚠️  LOW
    rvol_spike_down covers 9.9% of regime bars  ⚠️  LOW

  XRPUSDT
                     wr_%     pf   dur  n_trades
population                                      
regime_only         47.17  1.339  22.3     24598
rvol_spike          47.12  1.336  35.1      4143
rvol_spike_bearish  48.08  1.389  33.0      2398
rvol_spike_down     48.08  1.389  33.0      2398
    rvol_spike covers 16.8% of regime bars  ⚠️  LOW
    rvol_spike_bearish covers 9.7% of regime bars  ⚠️  LOW
    rvol_spike_down covers 9.7% of regime bars  ⚠️  LOW

── RVOL Setup Edge Verdict ──

  Baseline (regime_only):  avg WR 45.2%  avg PF 1.240
  RVOL config: threshold=1.5×  vol_ma_len=20  min_bars_active=1

  rvol_spike              avg WR lift -0.08pp  avg PF 1.236  avg PF lift -0.004  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 44.23%  lift -0.03pp / req 1.86pp  PF 1.189  lift -0.001 / req 0.100  trades 4,434  cov 18.8% ⚠️  ❌
    ETHUSDT     WR 45.03%  lift +0.02pp / req 1.88pp  PF 1.229  lift +0.001 / req 0.100  trades 4,364  cov 18.3% ⚠️  ❌
    SOLUSDT     WR 45.20%  lift +0.36pp / req 1.98pp  PF 1.237  lift +0.018 / req 0.100  trades 3,958  cov 17.7% ⚠️  ❌
    BNBUSDT     WR 44.19%  lift -0.69pp / req 2.06pp  PF 1.188  lift -0.034 / req 0.100  trades 3,632  cov 17.9% ⚠️  ❌
    XRPUSDT     WR 47.12%  lift -0.05pp / req 1.94pp  PF 1.336  lift -0.003 / req 0.100  trades 4,143  cov 16.8% ⚠️  ❌

  rvol_spike_bearish      avg WR lift +0.79pp  avg PF 1.280  avg PF lift +0.041  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 44.71%  lift +0.46pp / req 2.52pp  PF 1.213  lift +0.022 / req 0.100  trades 2,431  cov 10.3% ⚠️  ❌
    ETHUSDT     WR 45.39%  lift +0.38pp / req 2.51pp  PF 1.247  lift +0.019 / req 0.100  trades 2,463  cov 10.3% ⚠️  ❌
    SOLUSDT     WR 46.43%  lift +1.59pp / req 2.63pp  PF 1.300  lift +0.081 / req 0.100  trades 2,240  cov 10.0% ⚠️  ❌
    BNBUSDT     WR 45.50%  lift +0.62pp / req 2.77pp  PF 1.253  lift +0.031 / req 0.100  trades 2,013  cov 9.9% ⚠️  ❌
    XRPUSDT     WR 48.08%  lift +0.92pp / req 2.55pp  PF 1.389  lift +0.050 / req 0.100  trades 2,398  cov 9.7% ⚠️  ❌

  rvol_spike_down         avg WR lift +0.79pp  avg PF 1.280  avg PF lift +0.041  pairs ≥ threshold: 0/5  ❌
    BTCUSDT     WR 44.71%  lift +0.46pp / req 2.52pp  PF 1.213  lift +0.022 / req 0.100  trades 2,431  cov 10.3% ⚠️  ❌
    ETHUSDT     WR 45.39%  lift +0.38pp / req 2.51pp  PF 1.247  lift +0.019 / req 0.100  trades 2,463  cov 10.3% ⚠️  ❌
    SOLUSDT     WR 46.43%  lift +1.59pp / req 2.63pp  PF 1.300  lift +0.081 / req 0.100  trades 2,240  cov 10.0% ⚠️  ❌
    BNBUSDT     WR 45.50%  lift +0.62pp / req 2.77pp  PF 1.253  lift +0.031 / req 0.100  trades 2,013  cov 9.9% ⚠️  ❌
    XRPUSDT     WR 48.08%  lift +0.92pp / req 2.55pp  PF 1.389  lift +0.050 / req 0.100  trades 2,398  cov 9.7% ⚠️  ❌

  Thresholds: WR lift > 2.5×sqrt(p(1-p)/n),  PF lift > 0.02/0.05/0.10 by n,  trades > 500,  consistent across ≥ 4 of 5 pairs

  ❌  RVOL EDGE NOT CONFIRMED — no population clears all thresholds.
      Next steps:
        • Increase min_bars_active (reduces noise on lower TF)
        • Try rvol_threshold = 2.0 (stricter spike definition)
        • Try vol_ma_len = 10 or 50
        • Try a different entry_tf in config.py
        • Re-examine whether setup layer is needed before trigger layer
```
