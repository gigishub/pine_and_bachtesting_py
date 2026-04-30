# RVOL Setup Edge Check

```text

── Per-Pair Results ──

  BTCUSDT
                     wr_%     pf   dur  n_trades
population                                      
regime_only         42.21  1.096  18.5    282528
rvol_spike          42.25  1.098  25.2     48680
rvol_spike_bearish  41.59  1.068  23.6     25118
rvol_spike_down     41.59  1.068  23.6     25118
    rvol_spike covers 17.2% of regime bars  ⚠️  LOW
    rvol_spike_bearish covers 8.9% of regime bars  ⚠️  LOW
    rvol_spike_down covers 8.9% of regime bars  ⚠️  LOW

── RVOL Setup Edge Verdict ──

  Baseline (regime_only):  avg WR 42.2%  avg PF 1.096
  RVOL config: threshold=1.5×  vol_ma_len=20  min_bars_active=1

  rvol_spike              avg WR lift +0.04pp  avg PF 1.098  avg PF lift +0.002  pairs ≥ threshold: 0/1  ❌
    BTCUSDT     WR 42.25%  lift +0.04pp / req 0.56pp  PF 1.098  lift +0.002 / req 0.050  trades 48,680  cov 17.2% ⚠️  ❌

  rvol_spike_bearish      avg WR lift -0.62pp  avg PF 1.068  avg PF lift -0.028  pairs ≥ threshold: 0/1  ❌
    BTCUSDT     WR 41.59%  lift -0.62pp / req 0.78pp  PF 1.068  lift -0.028 / req 0.050  trades 25,118  cov 8.9% ⚠️  ❌

  rvol_spike_down         avg WR lift -0.62pp  avg PF 1.068  avg PF lift -0.028  pairs ≥ threshold: 0/1  ❌
    BTCUSDT     WR 41.59%  lift -0.62pp / req 0.78pp  PF 1.068  lift -0.028 / req 0.050  trades 25,118  cov 8.9% ⚠️  ❌

  Thresholds: WR lift > 2.5×sqrt(p(1-p)/n),  PF lift > 0.02/0.05/0.10 by n,  trades > 500,  consistent across ≥ 4 of 5 pairs

  ❌  RVOL EDGE NOT CONFIRMED — no population clears all thresholds.
      Next steps:
        • Increase min_bars_active (reduces noise on lower TF)
        • Try rvol_threshold = 2.0 (stricter spike definition)
        • Try vol_ma_len = 10 or 50
        • Try a different entry_tf in config.py
        • Re-examine whether setup layer is needed before trigger layer
```
