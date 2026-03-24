# ADL Alert

> **Source:** https://bybit-exchange.github.io/docs/v5/websocket/public/adl-alert

---

  * [](https://bybit-exchange.github.io/docs/)
  * WebSocket Stream
  * Public
  * ADL Alert



On this page

# ADL Alert

Subscribe to ADL alerts and insurance pool information.

> **Covers: USDT Perpetual / USDT Delivery / USDC Perpetual / USDC Delivery / Inverse Contracts**

Push frequency: **1s**

**Topic:**  
`adlAlert.{coin}`

Available filters:

  * `adlAlert.USDT` for USDT Perpetual/Delivery
  * `adlAlert.USDC` for USDC Perpetual/Delivery
  * `adlAlert.inverse` for Inverse contracts.



For more information on how ADL is triggered, see the [ADL endpoint](https://bybit-exchange.github.io/docs/v5/market/adl-alert).

### Response Parameters​

Parameter| Type| Comments  
---|---|---  
list| array| Object  
> c| string| Token of the insurance pool  
> s| string| Trading pair name  
> b| string| Balance of the insurance fund. Used to determine if ADL is triggered. For shared insurance pool, the "b" field will follow a T+1 refresh mechanism and will be updated daily at 00:00 UTC.  
> mb| string| Deprecated, always return "". Maximum balance of the insurance pool in the last 8 hours  
> i_pr| string| PnL ratio threshold for triggering **contract PnL drawdown ADL**

  * ADL is triggered when the symbol's PnL drawdown ratio in the last 8 hours exceeds this value

  
> pr| string| Symbol's PnL drawdown ratio in the last 8 hours. Used to determine whether ADL is triggered or stopped  
> adl_tt| string| Trigger threshold for **contract PnL drawdown ADL**

  * This condition is only effective when the insurance pool balance is greater than this value; if so, an 8 hours drawdown exceeding n% may trigger ADL

  
> adl_sr| string| Stop ratio threshold for **contract PnL drawdown ADL**

  * ADL stops when the symbol's 8 hours drawdown ratio falls below this value

  
  
### Subscribe Example​
    
    
    {"op": "subscribe", "args": ["adlAlert.USDT"]}  
    

### Response Example​
    
    
    {  
      "topic": "adlAlert.USDT",  
      "type": "snapshot",  
      "ts": 1757736794000,  
      "data": [  
        {  
          "c": "USDT",  
          "s": "FWOGUSDT",  
          "b": -5421.29889888,  
          "mb": -5421.29889888,  
          "i_pr": -0.3,  
          "pr": 0,  
          "adl_tt": 10000,  
          "adl_sr": -0.25  
        },  
        {  
          "c": "USDT",  
          "s": "ZORAUSDT",  
          "b": 19873.46255153,  
          "mb": 19874.97612833,  
          "i_pr": -0.3,  
          "pr": 0.000174,  
          "adl_tt": 10000,  
          "adl_sr": -0.25  
        },  
        {  
          "c": "USDT",  
          "s": "BERAUSDT",  
          "b": 453.36427074,  
          "mb": 453.36427074,  
          "i_pr": -0.3,  
          "pr": 0.24576,  
          "adl_tt": 10000,  
          "adl_sr": -0.25  
        },  
        ...,  
      ]  
    }  
    

[PreviousOrder Price Limit](https://bybit-exchange.github.io/docs/v5/websocket/public/order-price-limit)[NextPosition](https://bybit-exchange.github.io/docs/v5/websocket/private/position)

  * Response Parameters
  * Subscribe Example
  * Response Example


