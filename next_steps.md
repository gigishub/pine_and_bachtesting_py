

- Automated execution using Bash scripts, including:
    - Auto-restart functionality.
    - Scripts to kill/stop processes.
    - Live tracking of active vs. inactive runs.
    - Automated logging/moving of completed runs from "active" to "inactive" status for analysis.
    - how to keep track of what is running and what not in an orgnized human readable struture



- Setting up OpenClaw to monitor active trades and system health:
    - Monitoring output logs for errors.
    - Alerting on unusual activities that could cause performance or financial issues.

- Identifying advanced filtering methods to determine market state:
    - explroe Distinguishing between trending and sideways/ranging markets.
    - explosre Trade-by-trade probability: Assessing the likelihood of a "winner" or "loser" based on historical metrics.

- Validation and Testing Strategy:
    - How to verify these filters? (Backtesting).
    - Recommended Workflow: Backtest first to establish a baseline, then execute Forward Testing (Paper Trading) to verify real-world performance.

- Integrating advanced AI filtering via OpenClaw or other LLM tools:
    - Is it possible to backtest AI filters?
    - Workflow: 
        1. Feed raw backtest results to an LLM.
        2. Let the LLM analyze patterns and draw conclusions/optimizations.
        3. Forward test the AI-refined strategy to see if the win rate or profit factor improves.