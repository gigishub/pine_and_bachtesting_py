## OOS Test: BEAR STRATEGY  |  Entry TF: 4h
_OOS window: 2023-11-02 → 2026-04-22  |  Baseline: random (all candles)  |  Updated: 2026-05-07_

> **Purpose**: verify that the promoted strategy (regime + setup + trigger)
> generalises to completely unseen data.  The baseline is every warmed candle
> — a pure random entry.  PASS requires PF lift ≥ 0.05 AND WR z-score ≥ 2.5.

### Summary
| strategy | avg PF | avg PF lift | pairs OK | verdict |
|----------|--------|-------------|----------|---------|
| bear_rsi_kde_macd_downward | 1.247 | +0.189 | 1/6 | PASS |

### Per-Strategy Detail

**bear_rsi_kde_macd_downward**  avg PF 1.247  avg lift +0.189  1/6 pairs  PASS
  ADAUSDT     WR 46.2%  PF 1.288  lift +0.143 / req 0.05  z=0.7 / req 2.5  n=158  cov 2.9%  [--]
  BATUSDT     WR 59.7%  PF 2.219  lift +1.157 / req 0.05  z=4.0 / req 2.5  n=119  cov 2.2%  [OK]
  DOTUSDT     WR 38.8%  PF 0.953  lift -0.221 / req 0.05  z=-1.1 / req 2.5  n=121  cov 2.4%  [--]
  ETHUSDT     WR 43.3%  PF 1.144  lift +0.249 / req 0.05  z=1.4 / req 2.5  n=141  cov 2.6%  [--]
  LTCUSDT     WR 32.5%  PF 0.724  lift -0.264 / req 0.05  z=-1.6 / req 2.5  n=126  cov 2.3%  [--]
  XRPUSDT     WR 43.5%  PF 1.154  lift +0.069 / req 0.05  z=0.4 / req 2.5  n=184  cov 3.4%  [--]

### Population Comparison

#### ADAUSDT

| population | wr_% | pf | n_trades |
|------------|-----:|---:|---------:|
| random_all_candles | 43.3% | 1.145 | 5,384 |
| bear_rsi_kde_macd_downward | 46.2% | 1.288 | 158 |

#### BATUSDT

| population | wr_% | pf | n_trades |
|------------|-----:|---:|---------:|
| random_all_candles | 41.4% | 1.062 | 5,398 |
| bear_rsi_kde_macd_downward | 59.7% | 2.219 | 119 |

#### DOTUSDT

| population | wr_% | pf | n_trades |
|------------|-----:|---:|---------:|
| random_all_candles | 43.9% | 1.174 | 5,374 |
| bear_rsi_kde_macd_downward | 38.8% | 0.953 | 121 |

#### ETHUSDT

| population | wr_% | pf | n_trades |
|------------|-----:|---:|---------:|
| random_all_candles | 37.4% | 0.895 | 5,383 |
| bear_rsi_kde_macd_downward | 43.3% | 1.144 | 141 |

#### LTCUSDT

| population | wr_% | pf | n_trades |
|------------|-----:|---:|---------:|
| random_all_candles | 39.7% | 0.988 | 5,378 |
| bear_rsi_kde_macd_downward | 32.5% | 0.724 | 126 |

#### XRPUSDT

| population | wr_% | pf | n_trades |
|------------|-----:|---:|---------:|
| random_all_candles | 42.0% | 1.085 | 5,381 |
| bear_rsi_kde_macd_downward | 43.5% | 1.154 | 184 |
