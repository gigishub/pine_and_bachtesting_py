
I am creating a workflow where I am developing trading strategies from a written idea over a backtest of differnent parameter options to an evaulation of robustness through stratgy evaluation of the backtest with different options. 

general guide: 

Phase A:
what is the assumption that this strategy works ? 

we are starting with an idea of the strategy that should work from a macro to a micro level. 

1. some sort of regime Filter 
2. a set up detection 
3. a trigger that enters trades 
4. how to exits the trade with the ideal profit 



Phase B:

B1:
**First Development & Validation Checklist**

Develop and verify strategy logic on a small sample before full backtest.

**Execution Integrity**
- Enter at next candle Open after signal
- Fill must be within candle High-Low
- Simultaneous SL/TP = loss

**Bias Checks**
- No future data in signal logic
- Indicators calculated on closed candles only
- No repainting signals

**Logic Validation**
- Confirm signals trigger correct conditions
- Edge cases handled (gaps, no fills, partial data)
- Results explainable trade by trade

do that in backtest.py 

- we need a seperation in between long and short trades for rubusteness test on/flags in config
- we need on of flags to exclusive use  
- we need flags for individaul indicators 


Direction Separation

Long and short trades tested independently via enable_long / enable_short
Never mix long and short signals in the same test run
Validate each direction in isolation before combining

Exclusivity Rules

Each layer (regime, setup, trigger, exit) uses one flag at a time
Controlled via regime_exclusive, setup_exclusive, trigger_exclusive, exit_exclusive
Prevents compounding indicator signals masking individual performance

Individual Indicator Flags

Each indicator has its own boolean flag (e.g. use_adx, use_cmf, use_donchian)
Test each indicator in isolation before enabling combinations
A flag set to True is swept (on/off tested); False excludes it entirely from the grid