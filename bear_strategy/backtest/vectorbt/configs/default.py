"""Bear Strategy — vectorbt backtest configuration.

★  THIS IS THE ONLY FILE YOU NEED TO EDIT FOR A RUN  ★

Edit the values inside ``build_config()`` then run:

    source .venv/bin/activate
    python -m bear_strategy.backtest.vectorbt.run

CLI flags always override what is set here, so you can keep this as a
baseline and experiment quickly from the terminal:

    python -m bear_strategy.backtest.vectorbt.run \\
        --pairs BTCUSDT ETHUSDT \\
        --start 2021-01-01 --end 2023-11-01 \\
        --sl-mult 1.5 --tp-mult 2.5 \\
        --min-sl-pct 0.008

Results are saved to:
    bear_strategy/backtest/vectorbt/results/<YYYY-MM-DD_HHMM>/

──────────────────────────────────────────────────────────────────────
STRATEGY RECAP  (short-only, 1h entry / 1d regime)
──────────────────────────────────────────────────────────────────────
  Regime  : RSI(14) EMA(9) bear zone (30–50) on daily bars
  Guard   : Funding-rate EMA(3) > threshold on hourly bars
            (skips shorts when longs are already paying a premium)
  Trigger : Session Volume Profile — POC failed-reclaim OR HVN cross-below
  Risk    : ATR(atr_period)-based stop and target expressed as multiples
  Sizing  : risk_pct of equity per trade
            (size = equity × risk_pct / sl_distance)
  Filter  : min_sl_pct — skips entries whose stop distance is too small
            relative to price (prevents taker-fee dominated trades)
──────────────────────────────────────────────────────────────────────
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from bear_strategy.strategy.parameters import Parameters


# ─────────────────────────────────────────────────────────────────────────────
# Config dataclass
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class VbtRunConfig:
    """Complete configuration for one vectorbt multi-pair backtest run.

    Edit ``build_config()`` at the bottom of this file rather than changing
    the defaults here — that keeps all your customisations in one place.
    """

    # ── Pairs ──────────────────────────────────────────────────────────────
    # Any Bybit USDT-margined perp that has parquet files in data_dir.
    # Full OOS-validated universe:
    #   ["ADAUSDT", "BNBUSDT", "BTCUSDT", "DOTUSDT", "ETHUSDT",
    #    "LTCUSDT", "SOLUSDT", "XLMUSDT", "XRPUSDT"]
    pairs: list[str] = field(default_factory=lambda: ["BTCUSDT", "ETHUSDT", "SOLUSDT"])

    # ── Date window ────────────────────────────────────────────────────────
    # ISO-8601 strings; both ends inclusive.
    #   dev (in-sample)    : "2021-01-01" → "2023-11-01"
    #   oos (out-of-sample): "2023-11-02" → "2026-04-22"
    start_date: str = "2021-01-01"
    end_date:   str = "2023-11-22"

    # ── Stop-loss and take-profit ───────────────────────────────────────────
    # Both are ATR multiples (ATR period = atr_period below).
    # SHORT mechanics:
    #   SL fires when price RISES  stop_atr_mult   × ATR above entry price
    #   TP fires when price FALLS  target_atr_mult × ATR below entry price
    # Baseline (validated OOS): SL=2×, TP=3×  (R:R = 1.5).
    # Tighter SL (e.g. 1.5×) → smaller stop, size increases (same risk_pct).
    # Wider TP  (e.g. 4×)    → fewer wins but larger when they hit.
    stop_atr_mult:   float = 2.0
    target_atr_mult: float = 3.0

    # ATR period for stop, target, and the min-SL filter
    atr_period: int = 7

    # ── Minimum SL distance filter ─────────────────────────────────────────
    # Fraction of price (e.g. 0.005 = 0.5%).
    # Entries where ATR-based stop distance < min_sl_pct are skipped.
    # Rationale: at 0.08% round-trip taker, a 0.5% SL means fees ≤ 16% of R.
    # Raise to 0.008–0.01 for high-volatility-only entries (fewer, wider trades).
    min_sl_pct: float = 0.005

    # ── Position sizing ────────────────────────────────────────────────────
    # Fraction of equity at risk per trade.
    # Position size = equity × risk_pct / sl_distance_fraction.
    # Each losing trade costs at most risk_pct × equity regardless of SL width.
    risk_pct: float = 0.01   # 1 % of equity per trade

    # ── Entry throttling ───────────────────────────────────────────────────
    # Keep every Nth trigger. entry_phase selects the kept hit in each cycle.
    entry_every_n: int = 1
    entry_phase: int = 1

    # ── Exit mode (SL is always active) ────────────────────────────────────
    # fixed_tp                  — ATR-based TP (baseline)
    # rsi_cross_up              — daily RSI crosses above exit_rsi_level
    # fixed_tp_or_rsi_cross_up  — whichever fires first
    # macd_hist_cross_zero      — 1h MACD histogram crosses negative→≥0
    # rsi_oversold              — 1h RSI drops below rsi_oversold_level
    # ema_reclaim               — 1h close crosses back above EMA(exit_ema_period)
    # funding_regime_shift      — EMA-smoothed funding drops ≤ funding_threshold
    #                             (carry tailwind gone); keeps fixed TP as safety net
    use_exit_rsi: bool = False   # legacy; exit_mode alone controls behaviour
    exit_mode: str = "fixed_tp"
    exit_rsi_period: int = 14    # RSI period for rsi_cross_up + rsi_oversold
    exit_rsi_level: float = 50.0  # daily RSI cross-up threshold
    rsi_oversold_level: float = 30.0  # 1h RSI oversold threshold (rsi_oversold mode)

    # ── MACD exit parameters (macd_hist_cross_zero) ────────────────────────
    macd_fast_period:   int = 12
    macd_slow_period:   int = 26
    macd_signal_period: int = 9

    # ── EMA reclaim exit (ema_reclaim) ─────────────────────────────────────
    exit_ema_period: int = 21

    # ── Execution costs ────────────────────────────────────────────────────
    # Round-trip taker fee fraction.
    #   0.0008 = 0.08% — Bybit standard for top-tier pairs (BTC, ETH, SOL …)
    #   0.001  = 0.10% — use for smaller / less-liquid alts
    fees: float = 0.0008
    init_cash: float = 10_000.0   # Starting cash in quote currency (USDT)

    # ── Regime: RSI bear zone (1d bars) ────────────────────────────────────
    # Keep at validated defaults unless re-running hypothesis tests.
    rsi_period:    int   = 14
    rsi_ma_period: int   = 9
    rsi_lower:     float = 30.0   # RSI below this: oversold — shorts allowed
    rsi_upper:     float = 50.0   # RSI above this: bullish momentum — no shorts

    # ── Funding-rate guard (1h bars) ────────────────────────────────────────
    # EMA(funding_ma_period) of 8h funding rate must exceed funding_threshold.
    # threshold=0.0 → any positive funding allows the short
    #                 (longs are paying → market leans bullish, avoid shorting)
    funding_threshold: float = 0.0
    funding_ma_period: int   = 3

    # ── Volume Profile trigger ─────────────────────────────────────────────
    vp_price_bins: int = 50

    # ── Data directory ─────────────────────────────────────────────────────
    # Relative to the project root where you invoke the run command.
    data_dir: str = "crypto_data/data"

    # ── Output directory ───────────────────────────────────────────────────
    results_root: Path = field(
        default_factory=lambda: Path("bear_strategy/backtest/vectorbt/results")
    )

    # ─────────────────────────────────────────────────────────────────────
    # Helpers
    # ─────────────────────────────────────────────────────────────────────

    def to_parameters(self) -> Parameters:
        """Build a ``Parameters`` instance from this config.

        This is the bridge between the user-facing config and the internal
        strategy logic that accepts a ``Parameters`` dataclass.
        """
        return Parameters(
            rsi_period          = self.rsi_period,
            rsi_ma_period       = self.rsi_ma_period,
            rsi_lower           = self.rsi_lower,
            rsi_upper           = self.rsi_upper,
            funding_threshold   = self.funding_threshold,
            funding_ma_period   = self.funding_ma_period,
            vp_price_bins       = self.vp_price_bins,
            atr_period          = self.atr_period,
            stop_atr_mult       = self.stop_atr_mult,
            target_atr_mult     = self.target_atr_mult,
            min_sl_pct          = self.min_sl_pct,
            risk_pct            = self.risk_pct,
            entry_every_n       = self.entry_every_n,
            entry_phase         = self.entry_phase,
            use_exit_rsi        = self.use_exit_rsi,
            exit_mode           = self.exit_mode,
            exit_rsi_period     = self.exit_rsi_period,
            exit_rsi_level      = self.exit_rsi_level,
            rsi_oversold_level  = self.rsi_oversold_level,
            macd_fast_period    = self.macd_fast_period,
            macd_slow_period    = self.macd_slow_period,
            macd_signal_period  = self.macd_signal_period,
            exit_ema_period     = self.exit_ema_period,
            data_dir            = self.data_dir,
        )

    def summary_lines(self) -> list[str]:
        """Human-readable run-header lines printed before the backtest starts."""
        # Build exit detail based on mode
        mode = self.exit_mode
        if mode == "macd_hist_cross_zero":
            exit_detail = f"MACD({self.macd_fast_period},{self.macd_slow_period},{self.macd_signal_period}) hist→0"
        elif mode == "rsi_oversold":
            exit_detail = f"1h RSI({self.exit_rsi_period}) < {self.rsi_oversold_level:.0f}"
        elif mode == "ema_reclaim":
            exit_detail = f"1h EMA({self.exit_ema_period}) reclaim"
        elif mode == "funding_regime_shift":
            exit_detail = f"EMA({self.funding_ma_period}) funding ≤ {self.funding_threshold} + ATR TP safety"
        elif "rsi_cross_up" in mode:
            exit_detail = f"daily RSI({self.exit_rsi_period}) > {self.exit_rsi_level:.0f}"
        else:
            exit_detail = f"ATR TP: {self.target_atr_mult}×ATR"

        return [
            f"  Pairs    : {', '.join(self.pairs)}",
            f"  Window   : {self.start_date} → {self.end_date}",
            f"  SL       : {self.stop_atr_mult}×ATR({self.atr_period})  |  "
            f"TP: {self.target_atr_mult}×ATR({self.atr_period})",
            f"  Min SL   : {self.min_sl_pct*100:.2f}%  |  "
            f"Risk: {self.risk_pct*100:.1f}%/trade",
            f"  Entry    : every {self.entry_every_n} trigger(s), phase {self.entry_phase}",
            f"  Exit     : {mode}  ({exit_detail})",
            f"  Fees     : {self.fees*100:.3f}%  |  Cash: ${self.init_cash:,.0f}",
        ]


# ─────────────────────────────────────────────────────────────────────────────
# ★  EDIT THIS FUNCTION to configure your run
# ─────────────────────────────────────────────────────────────────────────────

def build_config() -> VbtRunConfig:
    """Return the configuration for the next vectorbt run.

    Adjust pairs, the date window, SL/TP multiples, and execution settings
    here.  CLI flags passed to run.py always take precedence over these values.
    """

    # ── Pairs ──────────────────────────────────────────────────────────────
    # Reduce the list to a single pair for quick sanity checks.
    # Use the full validated universe for a proper robustness run.
    pairs = [
        "BTCUSDT",
        "ETHUSDT",
        "SOLUSDT",
        "XRPUSDT",
        "BNBUSDT",
        "ADAUSDT",
        "DOTUSDT",
        "LTCUSDT",
        "XLMUSDT",
    ]

    # ── Date window ────────────────────────────────────────────────────────
    # dev  (in-sample)    : "2021-01-01" → "2023-11-01"
    # oos  (out-of-sample): "2023-11-02" → "2026-04-22"
    start_date = "2020-11-02"
    end_date   = "2023-11-22"

    # ── Stop-loss / take-profit ────────────────────────────────────────────
    # Validated baseline (promoted from hypothesis_test_v2):  SL=2×ATR, TP=3×ATR.
    # Try 1.5/2.5 for a tighter R:R or 2.5/4.0 for wider swings.
    stop_atr_mult   = 2.0
    target_atr_mult = 3.0
    atr_period      = 7

    # ── Minimum SL distance ────────────────────────────────────────────────
    # 0.005 (0.5%) validated default.
    # Increase to 0.008 to avoid low-volatility entries dominated by fees.
    min_sl_pct = 0.005

    # ── Sizing & execution ─────────────────────────────────────────────────
    risk_pct  = 0.01      # 1% of equity at risk per trade
    fees      = 0.0011    # 0.11% round-trip taker (Bybit standard)
    init_cash = 10_000.0  # Starting cash in USDT

    # ── Trigger sampling / exits ───────────────────────────────────────────
    entry_every_n   = 1
    entry_phase     = 1
    use_exit_rsi    = False
    exit_mode       = "fixed_tp"
    exit_rsi_period = 14
    exit_rsi_level  = 50.0

    # ── Indicator exit params ──────────────────────────────────────────────
    # macd_hist_cross_zero: exit when 1h MACD histogram crosses negative→≥0
    macd_fast_period   = 12
    macd_slow_period   = 26
    macd_signal_period = 9
    # rsi_oversold: exit when 1h RSI(exit_rsi_period) drops below this level
    rsi_oversold_level = 30.0
    # ema_reclaim: exit when 1h close crosses back above EMA(exit_ema_period)
    exit_ema_period    = 21

    return VbtRunConfig(
        pairs              = pairs,
        start_date         = start_date,
        end_date           = end_date,
        stop_atr_mult      = stop_atr_mult,
        target_atr_mult    = target_atr_mult,
        atr_period         = atr_period,
        min_sl_pct         = min_sl_pct,
        risk_pct           = risk_pct,
        entry_every_n      = entry_every_n,
        entry_phase        = entry_phase,
        use_exit_rsi       = use_exit_rsi,
        exit_mode          = exit_mode,
        exit_rsi_period    = exit_rsi_period,
        exit_rsi_level     = exit_rsi_level,
        rsi_oversold_level = rsi_oversold_level,
        macd_fast_period   = macd_fast_period,
        macd_slow_period   = macd_slow_period,
        macd_signal_period = macd_signal_period,
        exit_ema_period    = exit_ema_period,
        fees               = fees,
        init_cash          = init_cash,
    )
