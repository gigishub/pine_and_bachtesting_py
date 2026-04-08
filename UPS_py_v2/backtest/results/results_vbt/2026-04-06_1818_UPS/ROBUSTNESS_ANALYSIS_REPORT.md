# Robustness Analysis Report
## Backtest Results: 2026-04-06_1818_UPS

### Executive Summary
The robustness analysis evaluated 1,152 parameter signatures across 20 cryptocurrency/timeframe conditions. Only 46 signatures (4%) appeared in 3 or more conditions, indicating low overall robustness. However, the most consistent signatures show promising performance with positive returns and reasonable risk metrics.

### Key Statistics
- **Total parameter signatures analyzed**: 1,152
- **Total conditions (crypto/timeframe pairs)**: 20
- **Signatures with ≥3 appearances (≥15% consistency)**: 46 (4%)
- **Signatures with ≥5 appearances (≥25% consistency)**: 7 (0.6%)
- **Most consistent signature**: Appeared in 7/20 conditions (35%)

### Top 5 Most Robust Parameter Signatures

1. **Rank 1** (7 appearances, 35% consistency):
   - `use_iq_filter=1|use_sq_boost=1|enable_ec=1|enable_bullish_engulfing=0|enable_shooting_star=0|enable_hammer=0|use_rsi_filter=1|use_adx_filter=1|use_volume_filter=1|risk_reward_multiplier=2.7000`
   - Avg Return: 2.43% ± 8.20
   - Avg Profit Factor: 1.316 ± 0.803
   - Avg Win Rate: 33.1% ± 12.4
   - Avg Max Drawdown: 6.9% ± 3.6
   - Avg # Trades: 21

2. **Rank 2** (6 appearances, 30% consistency):
   - `use_iq_filter=0|use_sq_boost=1|enable_ec=1|enable_bullish_engulfing=0|enable_shooting_star=0|enable_hammer=0|use_rsi_filter=1|use_adx_filter=1|use_volume_filter=1|risk_reward_multiplier=2.7000`
   - Avg Return: 3.18% ± 9.83
   - Avg Profit Factor: 1.294 ± 0.571
   - Avg Win Rate: 33.9% ± 9.1
   - Avg Max Drawdown: 7.5% ± 3.6
   - Avg # Trades: 26

3. **Rank 3** (6 appearances, 30% consistency):
   - `use_iq_filter=1|use_sq_boost=1|enable_ec=1|enable_bullish_engulfing=0|enable_shooting_star=0|enable_hammer=0|use_rsi_filter=0|use_adx_filter=1|use_volume_filter=1|risk_reward_multiplier=2.7000`
   - Avg Return: 2.45% ± 7.81
   - Avg Profit Factor: 1.308 ± 0.791
   - Avg Win Rate: 32.9% ± 12.2
   - Avg Max Drawdown: 6.8% ± 3.2
   - Avg # Trades: 22

### Performance Analysis

#### Consistency vs Performance Correlations
- **Consistency vs Return**: 0.325 (moderate positive)
- **Consistency vs Profit Factor**: 0.346 (moderate positive)
- **Consistency vs Win Rate**: -0.189 (slight negative)
- **Consistency vs Max Drawdown**: -0.369 (moderate negative)

**Interpretation**: More consistent signatures tend to have better returns, higher profit factors, and lower drawdowns, but slightly lower win rates.

#### Performance of Robust Signatures (≥3 appearances)
- **Average Return**: -0.48%
- **Median Return**: 0.04%
- **Average Profit Factor**: 1.060
- **Average Win Rate**: 29.3%
- **Average Max Drawdown**: 6.6%

#### Performance of Highly Robust Signatures (≥5 appearances)
- **Average Return**: 2.19%
- **Median Return**: 2.43%
- **Average Profit Factor**: 1.255
- **Average Win Rate**: 32.3%
- **Average Max Drawdown**: 7.1%
- **All 7 signatures show positive returns**

### Parameter Pattern Analysis

#### Common Features in Top 10 Robust Signatures:
- **enable_ec=1**: 90% (9/10)
- **use_sq_boost=1**: 80% (8/10)
- **use_volume_filter=1**: 100% (10/10)
- **risk_reward_multiplier=2.7000**: 90% (9/10)
- **enable_bullish_engulfing=0**: 100% (10/10)
- **enable_shooting_star=0**: 90% (9/10)
- **enable_hammer=0**: 100% (10/10)

**Key Insight**: The most robust configurations use Elliott Wave (enable_ec=1), Squeeze Momentum (use_sq_boost=1), and volume filtering, with candlestick patterns disabled and a 2.7 risk/reward ratio.

### Risk Assessment

#### Volatility Concerns:
- **High volatility signatures** (top 25% std dev): 288 signatures
  - Avg Return: -10.19%
  - Avg Std Dev: 13.43
- **Signatures with >10% avg drawdown**: 567 signatures (49%)
  - Avg Drawdown: 15.4%

#### Trade Analysis for Top Signature:
- **Total trades analyzed**: 59 (from ETH_1H and XRP_1H)
- **Win Rate**: 44.1% (26/59)
- **Average Return**: 0.65%
- **Median Return**: -1.47% (indicating positive skew)
- **Max Win**: 14.86%
- **Max Loss**: -7.89%
- **Average Trade Duration**: 34.5 hours
- **3 trades longer than 1 week** (potential exit logic issues)

### Strengths
1. **Positive correlation** between consistency and performance metrics
2. **Highly consistent signatures** (≥5 appearances) all show positive returns
3. **Clear parameter patterns** emerge in robust configurations
4. **Reasonable drawdowns** for top signatures (6-8% average)
5. **Strategy works across multiple cryptocurrencies** (ADA, ETH, XRP, DOGE, SOL)

### Weaknesses & Concerns
1. **Low overall robustness**: Only 4% of signatures appear in ≥3 conditions
2. **Low win rates**: Average ~30% for robust signatures
3. **High volatility**: Many signatures show high standard deviation of returns
4. **Trade duration issues**: Some trades remain open for >1 week
5. **Negative median return** in trade analysis suggests dependency on few large wins

### Recommendations

#### For Strategy Improvement:
1. **Focus on parameter combinations** with `enable_ec=1`, `use_sq_boost=1`, `use_volume_filter=1`
2. **Use risk_reward_multiplier=2.7** as it appears in most robust signatures
3. **Consider disabling candlestick patterns** (bullish_engulfing, shooting_star, hammer)
4. **Review exit logic** to address long-duration trades (>1 week)
5. **Implement position sizing** to manage volatility and drawdowns

#### For Further Testing:
1. **Test top signatures** on out-of-sample data
2. **Analyze market regime dependency** - when does strategy work best?
3. **Optimize RSI and ADX filter settings** (currently mixed results)
4. **Consider adding volatility filters** to reduce drawdowns
5. **Test with different risk/reward ratios** around 2.7

#### Risk Management:
1. **Monitor drawdowns closely** - implement circuit breakers
2. **Consider correlation risk** across cryptocurrencies
3. **Implement trade duration limits** (e.g., max 5 days)
4. **Use volatility-adjusted position sizing**

### Conclusion
The strategy shows promise with specific parameter configurations, particularly those using Elliott Wave, Squeeze Momentum, and volume filtering with a 2.7 risk/reward ratio. However, robustness is low overall, and the strategy appears to rely on a few large wins to overcome many small losses (positive skew). Further refinement of exit logic and risk management is recommended before live deployment.

**Overall Robustness Score**: 6/10 (promising but needs refinement)