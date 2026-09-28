"""Backtest the live bot by running its own strategy code on historical daily candles."""

from __future__ import annotations

import sys
import types
from pathlib import Path

import pandas as pd

BOT_DIR = Path(__file__).resolve().parent.parent / "btc_sol_hetzner_momentum_bot"

# Stub the exchange and credentials so the bot's strategy module imports offline.
sys.modules["config"] = types.SimpleNamespace(LOOKBACK_BARS=700)
sys.modules["exchange_client"] = types.SimpleNamespace(ExchangeClient=lambda: None)
sys.modules["pandas_ta"] = types.SimpleNamespace()  # imported but unused by the bot
sys.path.insert(0, str(BOT_DIR))
from strategy import TradingStrategy  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import available_symbols, load, report  # noqa: E402

LIVE_PARAMS = dict(atr_length_sl=5, atr_length_vola=5, ema_trend_length=240, ema_is_bullish_length=10,
                   lookback_high=7, atr_vol_multiplier=1.6)


class FilteredStrategy(TradingStrategy):
    """Bot strategy where new entries also need entry_ok on that bar."""

    entry_ok: pd.Series = None

    def set_in_trade(self, i: int):
        if self.entry_ok is None or self.entry_ok.iloc[i]:
            super().set_in_trade(i)


def bot_position(df: pd.DataFrame, p: dict = LIVE_PARAMS, entry_ok: pd.Series | None = None) -> pd.Series:
    """Position held on each bar, as the live bot would hold it (fills at that bar's open).

    entry_ok must already be aligned like the bot's signal: row i uses data up to the close of bar i-1.
    """
    s = FilteredStrategy.__new__(FilteredStrategy)
    s.entry_ok = None if entry_ok is None else entry_ok.reindex(df.index).fillna(False).astype(bool)
    s.df = df[["open", "close", "high", "low"]].copy()
    s.calculate_indicators(p["atr_length_sl"], p["atr_length_vola"], p["ema_trend_length"], p["ema_is_bullish_length"])
    s.get_signal(p["lookback_high"], p["atr_vol_multiplier"])
    for i in range(1, len(s.df)):
        s.check_sl(i)
        if not s.df["sl_hit"].iloc[i]:
            s.handle_signal(i)
            s.update_trail_sl(i)
            s.set_in_trade(i)
    return s.df["in_trade"].astype(int)


if __name__ == "__main__":
    import logging
    logging.disable(logging.CRITICAL)
    syms = available_symbols("1d")
    report({sym: bot_position(load(sym, "1d")) for sym in syms}, "1d", "Live bot (daily), net of 0.1% fees")
