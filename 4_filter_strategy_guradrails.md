To build a professional trading system that survives more than one market cycle, you must treat it as a **logical filter stack**. You are essentially moving from the "Macro" (market state) to the "Micro" (execution).

Here are the 4 general guidelines for building a robust, backtestable system:

---

### 1. Market Regime Classification (The "Why")
Before looking for a signal, you must define the current market environment. Strategies fail because they try to "trend-follow" in a sideways market or "mean-revert" during a breakout.
* **The Goal:** Filter out "garbage" price action where your strategy has no edge.
* **The Logic:** Use a **Volatility** or **Trend Strength** metric to categorize the chart as *Trending*, *Ranging*, or *Expanding*.
* **Backtest Tip:** Test your system only within its intended regime. If it's a momentum strategy, your code should automatically ignore data where volume or trend strength is below a certain threshold.

### 2. The Structural Setup (The "Where")
Identify the specific geometry or conditions that must exist before an entry is considered. This is the "pre-signal" phase.
* **The Goal:** Ensure you are entering at a point of **Asymmetry** (where the potential reward is much larger than the risk).
* **The Logic:** Look for "Coiling" (price compression), "Overextension" (price too far from the mean), or "Value" (price at a high-volume node).
* **Backtest Tip:** Define this setup using mathematical ratios (e.g., the ratio between two moving averages or a Bollinger Band width) rather than just "eye-balling" it.

### 3. The Execution Trigger (The "When")
This is the precise "Go" signal. It confirms that the setup identified in Step 2 is now actually moving in your favor.
* **The Goal:** Minimize "lag" and avoid entering too early (getting "front-run") or too late (chasing the move).
* **The Logic:** Use a **Momentum Oscillator cross**, a **Price Action break** (like a candle high/low), or a **Slope Change** in a fast moving average.
* **Backtest Tip:** Compare "Market Orders" vs. "Limit Orders" at the signal bar's high/low. This significantly impacts your slippage results in backtesting.py.

### 4. Risk & Exit Management (The "How Much")
This is the most critical part of professional systems. It determines your equity curve's smoothness.
* **The Goal:** Protect capital first, then harvest profit based on the market's behavior, not your emotions.
* **The Logic:**
    * **Invalidation (SL):** Where is the "Idea" proven wrong? (e.g., a volatility-based stop).
    * **Monetization (TP):** How do you scale out? (e.g., fixed multiples, trailing stops, or reaching a statistical extreme like a 3rd Standard Deviation).
* **Backtest Tip:** Use **Dynamic Trailing Stops** rather than fixed ones. In crypto, "Big Moves" often go much further than expected; a professional exit allows the market to take you out rather than you guessing the top.

---

### The "Logic Flow" for Your Backtester:
1.  **Is the market healthy for this logic?** (Regime)
2.  **Is price in a high-probability location?** (Setup)
3.  **Is momentum confirming the direction NOW?** (Trigger)
4.  **Where do I get out if I'm wrong, and how do I trail if I'm right?** (Exit)

By testing different indicators within these **four distinct slots**, you can swap a "Squeeze" for a "Linear Regression" without breaking the fundamental logic of your system.