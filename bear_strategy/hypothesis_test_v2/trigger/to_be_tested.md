Entry-specific triggers worth testing
Price action based — cleanest signals, no lag:
1. Lower high formation — current bar's high is lower than the previous bar's high, and close is below the open. Pure structure: the rally attempt failed. Directly relevant to your pullback context.
2. Inside bar break — price breaks below the low of an inside bar (a bar whose range is contained within the prior bar). These compress before expanding — a break down after compression in a bearish pullback is a high-conviction entry event.
3. Candle body momentum — close is below the midpoint of the prior bar's range. Not a cross, not an average — just "did this bar close in the weak half of the previous bar." Very low noise.

Structure based — where is price relative to recent range:
4. N-bar low break — close below the lowest close of the last N bars (e.g. 3, 5, 8). This directly says "price just accepted a new low." Test multiple N values since the best N will differ by pair. This is probably your highest-probability new test.
5. Pivot low break — price breaks below the most recent local swing low (e.g. lowest low of the prior 3 bars on each side). More selective than N-bar low, fires less, but when it fires the structure is unambiguous.

Momentum with direction lock — unlike your current MACD tests:
6. RSI slope — not a cross, but RSI declining for 2+ consecutive bars while below 50. Continuous momentum confirmation rather than a single cross event. Stays in the trade context rather than firing once.
7. Stochastic %K cross below %D while both below 50 — double condition: the cross itself plus both lines already being in bearish territory. The "below 50" gate is what your current RSI cross lacks — it filters out crosses that happen from overbought and are likely to mean-revert.
8. CCI crossing below zero from positive — CCI is sensitive and crosses zero frequently enough to give you reasonable n, but the zero cross from positive specifically catches the transition from "above average momentum" to "below average" which is exactly the pullback continuation you want.



**`lower_high_formation` (trigger_3)**
Directly matches your use case. Price tried to rally within the pullback, failed to make a new high, then closed bearishly below the lower-high bar's open. This is structural — it tells you the counter-rally is dead. High conviction, event-based, reasonable n expected.

**`zone_touch_bar_low_violation` (trigger_4)**
When price closes below the low of the bar that first touched your KDE zone, every buyer from that bar is underwater. Clean structural rejection confirmation. Very precise entry signal.

**`roc_cross_below_zero`**
ROC crossing below zero means price is now lower than it was N bars ago — velocity just turned negative. It's a clean event (cross, not state), gives decent n, and directly measures "the move has started" rather than re-filtering the regime.

**`trix_cross`**
The filter that TRIX must still be above zero when it crosses below its signal is what makes this valuable. It catches the rollover from a peak rather than firing mid-move. That's exactly the exhaustion signal you want at a trigger level.

**`cmf_cross_below_zero`**
Chaikin Money Flow crossing zero means volume-weighted money flow just flipped to distribution. More meaningful than raw RVOL (which you already tested and was weak) because it accounts for *where* price closed within the bar, not just how much volume traded.


**`histogram_peak_roll`**
Histogram turning down while still positive is an early warning — fires before the MACD cross, so n will be higher than your `macd_lines_cross` test. The problem is it fires in both trend directions equally, so the setup context has to do the filtering work.

**`falling_tunnel`** (both BB bands moving down together)
Cleaner than `lower_expansion` alone. If both bands shift down simultaneously the entire price structure is moving — not just volatility expanding one side.

**`atr_expansion_bearish_turn` (trigger_1)**
Bar range expands AND closes below open AND below prior close. This is a momentum burst confirmation — it fires selectively and when it does fire the move usually has follow-through. Should give you better lift than RVOL because it combines range expansion with directional close.

