Step 1: The Core Single-Input Function
Create a function that accepts exactly one Asset (Pair) and one Timeframe as inputs and returns a standard set of performance metrics (Return, Sharpe, Max Drawdown).

Step 2: The Multi-Dataset Wrapper
Build a wrapper script that takes a List of Assets and a List of Timeframes as inputs, calling the Core Function for every possible combination in the grid.

Step 3: The Parameter Injection
Modify the wrapper to allow a Dictionary of Parameters (Filter Toggles and R:R Ratios) to be passed into the backtest engine for each individual run.

Step 4: The Loop Automation
Execute the wrapper to cycle through the entire dataset grid using the same fixed parameter set, ensuring the logic remains identical across all environments.

Step 5: The "Winner" Logger
Store the output of every loop iteration into a structured format (like a CSV or DataFrame) to enable side-by-side comparison of the results.

Step 6: The Manual Override
Add a simple configuration step at the start of the process where you can manually adjust the parameter values before triggering a new "Grid Run."