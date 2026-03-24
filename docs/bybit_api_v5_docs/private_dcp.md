# Dcp

> **Source:** https://bybit-exchange.github.io/docs/v5/websocket/private/dcp

---

  * [](https://bybit-exchange.github.io/docs/)
  * WebSocket Stream
  * Private
  * Dcp



On this page

# Dcp

Subscribe to the dcp stream to trigger DCP function.

For example, connection A subscribes "dcp.xxx", connection B does not and connection C subscribes "dcp.xxx".

  1. If A is alive, B is dead, C is alive, then this case will not trigger DCP.
  2. If A is alive, B is dead, C is dead, then this case will not trigger DCP.
  3. If A is dead, B is alive, C is dead, then DCP is triggered when reach the timeWindow threshold



To sum up, for those private connections subscribing "dcp" topic are all dead, then DCP will be triggered.

**Topic:** `dcp.future`, `dcp.spot`, `dcp.option`

### Subscribe Example​
    
    
    {  
        "op": "subscribe",  
        "args": [  
            "dcp.future"  
        ]  
    }  
    

[PreviousGreek](https://bybit-exchange.github.io/docs/v5/websocket/private/greek)[NextWebsocket Trade Guideline](https://bybit-exchange.github.io/docs/v5/websocket/trade/guideline)

  * Subscribe Example


