# Trade

> **Source:** https://bybit-exchange.github.io/docs/v5/spread/websocket/public/trade

---

  * [](https://bybit-exchange.github.io/docs/)
  * Spread Trading
  * Websocket Stream
  * Public
  * Trade



On this page

# Trade

Subscribe to the public trades stream.

After subscription, you will be pushed trade messages in real-time.

Push frequency: **real-time**

**Topic:**  
`publicTrade.{symbol}`

### Response Parameters​

Parameter| Type| Comments  
---|---|---  
topic| string| Topic name  
type| string| Data type. `snapshot`  
ts| number| The timestamp (ms) that the system generates the data  
data| array| Object. Sorted by the time the trade was matched in ascending order  
> T| number| The timestamp (ms) that the order is filled  
> s| string| Symbol name  
> S| string| Side of taker. `Buy`,`Sell`  
> v| string| Trade size  
> p| string| Trade price  
> [L](https://bybit-exchange.github.io/docs/v5/enum#tickdirection)| string| Direction of price change  
> i| string| Trade ID  
> seq| integer| Cross sequence  
  
### Subscribe Example​
    
    
    {  
        "op": "subscribe",  
        "id": "test-001-perp",  
        "args": [  
            "publicTrade.SOLUSDT_SOL/USDT"  
        ]  
    }  
    

### Response Example​
    
    
    {  
        "topic": "publicTrade.SOLUSDT_SOL/USDT",  
        "ts": 1744170142723,  
        "type": "snapshot",  
        "data": [  
            {  
                "T": 1744170142720,  
                "s": "SOLUSDT_SOL/USDT",  
                "S": "Sell",  
                "v": "2.5",  
                "p": "19.3928",  
                "L": "MinusTick",  
                "i": "31d0fc58-933b-57b3-8378-f73da06da843",  
                "seq": 1783284617  
            }  
        ]  
    }  
    

[PreviousOrderbook](https://bybit-exchange.github.io/docs/v5/spread/websocket/public/orderbook)[NextTicker](https://bybit-exchange.github.io/docs/v5/spread/websocket/public/ticker)

  * Response Parameters
  * Subscribe Example
  * Response Example


