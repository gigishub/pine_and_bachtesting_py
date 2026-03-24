I want to translate the Pine script [UPS_itellegent_filter.pine] into a Python backtesting.py strategy in this workspace, using the same architecture style as btc_momentum.

Important constraints:
- Work step by step, not all at once.
- After each step, stop and show:
  1. what Pine logic was translated,
  2. what assumptions were made,
  3. what is still missing,
  4. how to verify this step before moving on.
- Do not guess backtesting.py APIs. Read the local docs under docs/backtesting/ first.
- Follow the style already used in btc_momentum:
  - pandas/precomputed indicator series in strategy_logic-style code,
  - small pure functions for entry/exit/trailing rules,
  - thin Strategy.init() and Strategy.next().
- Unless I explicitly ask for shorts, start with long-only translation first for simplicity short later.
- Keep changes minimal and testable.
- Add debug outputs or temporary comparison columns when useful so we can validate parity with Pine logic.
- If a Pine feature cannot map 1:1 to backtesting.py, stop and explain the mismatch before coding around it.

Target workflow:
Step 1: Read the Pine file and produce a translation map only. No coding yet.
The map must include:
- inputs/parameters,
- indicators,
- stateful variables,
- entry conditions,
- exit conditions,
- stop/target logic,
- time/date filters,
- features that are optional or too complex for first pass.

Step 2: Create Python file/module scaffolding only.
Match the btc_momentum layout as closely as practical.

Step 3: Implement indicators and precomputed series only.
No order placement yet.
Then explain how to verify indicator correctness on sample data.

Step 3A: Base indicators + warmup

Implement only:
ma1 (EMA)
atr_value
price_above_ma
atr_max_size_check
is_ready
No IQ filter, no pullback state, no patterns yet.
Verification:

Confirm no NaN beyond warmup for ma1, atr_value.
Spot-check 20 random bars: price_above_ma == (Close > ma1).
Spot-check ATR candle-size filter with manual formula abs(High-Low) <= atr*atr_max_size.
Step 3B: MA context counters (Zen bars*MA)

Implement:
candles_below_ma (barsBelowMA)
candles_above_ma (barsAboveMA)
ma_cross_count (barsCrossedMA)
ma_cross_filter
Keep logic exactly loop-equivalent to Zen library semantics (lookback from i=1..lookback).
Verification:

Build a tiny deterministic test DataFrame (10-20 rows) and manually count expected values.
Compare Python outputs vs manual table for at least 5 bars.
Ensure counters are integer-like and bounded [0, lookback].
Step 3C: IQ filter chain

Implement:
efficiency_ratio, slope_score
bias_long_score
long_trend_score
SQ components: sq_candle_strength, sq_vol_score, sq_ma_proximity, signal_quality, sq_boost
iq_long_filter
Long-only branch only (skip short IQ outputs for now).
Verification:

Assert all score series are within [0, 1] where expected.
Check weight normalization and no divide-by-zero issues.
Print sample rows showing each IQ component and final iq_long_filter.
Step 3D: Pullback state machine (long side only)

Implement stateful series equivalents for:
bullishClosePB, bullishHighPB, bullishLowPB
pbLookbackBullish
bearishPB (used by long entry)
Reproduce Pine bar-by-bar transitions with explicit iterative loop over rows.
Verification:

Add debug columns for state transitions (reset/set events).
Validate on a small slice bar-by-bar (first 150 bars) with printed checkpoint rows.
Confirm no forward-looking behavior.
Step 3E: Pattern primitives + Step 3 integration outputs

Implement only precomputed pattern booleans for long side:
bullish_engulfing
hammer_candle
long_entry_pattern
Also return:
long_conditions_met
valid_long_entry (precomputed signal only, still no order placement in Step 3)
Verification:

Add temporary debug columns for each sub-condition.
Count how many bars pass each layer (funnel check).
Inspect first 20 valid_long_entry=True rows with full component columns.



Step 4: Implement long entry logic only.
Then explain how to verify entries bar-by-bar.

Step 5: Implement stop loss / target / trailing logic .
Then explain how to verify state transitions.

Step 6: Implement exits and wire into backtesting.py.
Then explain fill-model caveats such as trade_on_close and bar-close behavior.

Step 7: Run or prepare a validation pass.
Report:
- trade count,
- first 10 entries,
- first 10 exits,
- obvious mismatches vs Pine expectations,
- remaining gaps.

Rules for output:
- Do not dump large code all at once.
- For each step, either modify files or provide a precise plan for that one step only.
- Always list verification checks before moving to the next step.
- If you need my decision on an ambiguity, ask a focused question and stop.