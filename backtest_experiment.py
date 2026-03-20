"""Backtesting.py experiment script: optimize and analyze close-to-win excursion metrics."""

from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import GOOG
import pandas as pd


class SmaCross(Strategy):
    fast = 10
    slow = 30

    def init(self):
        close = self.data.Close
        self.sma_fast = self.I(lambda: pd.Series(close).rolling(self.fast).mean().values)
        self.sma_slow = self.I(lambda: pd.Series(close).rolling(self.slow).mean().values)

    def next(self):
        if crossover(self.sma_fast, self.sma_slow):
            self.buy()
        elif crossover(self.sma_slow, self.sma_fast):
            self.position.close()


def run_baseline():
    bt = Backtest(
        GOOG,
        SmaCross,
        cash=10_000,
        commission=0.002,
        finalize_trades=True,
    )
    stats = bt.run()
    print("\n=== Baseline stats ===")
    print(stats)
    return bt, stats


def add_excursions(stats):
    trades = stats['_trades'].copy()
    trades['MAE'] = trades['EntryPrice'] - trades['Entry_\u03bb']
    trades['MFE'] = trades['Exit_\u03bb'] - trades['EntryPrice']
    trades['ratio_SL'] = (trades['MAE'] / (trades['EntryPrice'] - trades['SL'])).abs().clip(0, 1)
    trades['ratio_TP'] = (trades['MFE'] / (trades['TP'] - trades['EntryPrice'])).abs().clip(0, 1)
    trades[['ratio_SL', 'ratio_TP']] = trades[['ratio_SL', 'ratio_TP']].fillna(0)
    return trades


def optimize_strategy(bt):
    print("\n=== Optimizing strategy parameters ===")
    opt, heatmap = bt.optimize(
        fast=range(5, 21),
        slow=range(20, 61, 2),
        maximize='SQN',
        method='grid',
        constraint=lambda p: p.fast < p.slow,
        return_heatmap=True,
        random_state=42,
    )

    # Best result
    best = opt["_strategy"]
    print(f"\nBest setup : fast={best.fast}, slow={best.slow}")
    print(f"Return [%] : {opt['Return [%]']:.2f}")
    print(f"SQN        : {opt['SQN']:.4f}")
    print(f"Max DD [%] : {opt['Max. Drawdown [%]']:.2f}")

    # All combinations, sorted by SQN descending
    all_results = (
        heatmap
        .reset_index()
        .rename(columns={0: 'SQN'})
        .sort_values('SQN', ascending=False)
    )
    print(f"\n=== All {len(all_results)} tested setups (sorted by SQN) ===")
    print(all_results.to_string(index=False))

    return opt, heatmap


def main():
    bt, stats = run_baseline()
    trades = add_excursions(stats)
    print("\n=== Top 8 trades by ratio_TP (closest to target) ===")
    print(trades.sort_values('ratio_TP', ascending=False)
                 .head(8)
                 .loc[:, ['EntryBar', 'ExitBar', 'EntryPrice', 'ExitPrice', 'MAE', 'MFE', 'ratio_TP', 'PnL']]
                 .to_string(index=False))

    # optimization run to find better config
    optimize_strategy(bt)

if __name__ == '__main__':
    main()
