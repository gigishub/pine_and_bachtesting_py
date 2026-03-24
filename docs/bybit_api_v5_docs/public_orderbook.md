# Orderbook

> **Source:** https://bybit-exchange.github.io/docs/v5/spread/websocket/public/orderbook

---

  * [](https://bybit-exchange.github.io/docs/)
  * Spread Trading
  * Websocket Stream
  * Public
  * Orderbook



On this page

# Orderbook

Subscribe to the spread orderbook stream.

### Depths​

Level 25 data, push frequency: **20ms**

**Topic:**  
`orderbook.{depth}.{symbol}` e.g., orderbook.25.SOLUSDT_SOL/USDT

### Process snapshot/delta​

To process `snapshot` and `delta` messages, please follow these rules:

Once you have subscribed successfully, you will receive a `snapshot`. The WebSocket will keep pushing `delta` messages every time the orderbook changes. If you receive a new `snapshot` message, you will have to reset your local orderbook. If there is a problem on Bybit's end, a `snapshot` will be re-sent, which is guaranteed to contain the latest data.

To apply `delta` updates:

  * If you receive an amount that is `0`, delete the entry
  * If you receive an amount that does not exist, insert it
  * If the entry exists, you simply update the value



See working code examples of this logic in the [FAQ](https://bybit-exchange.github.io/docs/faq#how-can-i-process-websocket-snapshot-and-delta-messages).

### Response Parameters​

Parameter| Type| Comments  
---|---|---  
topic| string| Topic name  
type| string| Data type. `snapshot`,`delta`  
ts| number| The timestamp (ms) that the system generates the data  
data| map| Object  
> s| string| Symbol name  
> b| array| Bids. For `snapshot` stream. Sorted by price in descending order  
>> b[0]| string| Bid price  
>> b[1]| string| Bid size 

  * The delta data has size=0, which means that all quotations for this price have been filled or cancelled

  
> a| array| Asks. For `snapshot` stream. Sorted by price in ascending order  
>> a[0]| string| Ask price  
>> a[1]| string| Ask size 

  * The delta data has size=0, which means that all quotations for this price have been filled or cancelled

  
> u| integer| Update ID

  * Occasionally, you'll receive "u"=1, which is a snapshot data due to the restart of the service. So please overwrite your local orderbook

  
> seq| integer| Cross sequence  
cts| number| The timestamp from the matching engine when this orderbook data is produced. It can be correlated with `T` from [public trade channel](https://bybit-exchange.github.io/docs/v5/spread/websocket/public/trade)  
  
### Subscribe Example​
    
    
    {  
        "op": "subscribe",  
        "args": ["orderbook.25.SOLUSDT_SOL/USDT"]  
    }  
    

### Event Example​
    
    
    {  
        "topic": "orderbook.25.SOLUSDT_SOL/USDT",  
        "ts": 1744165512257,  
        "type": "delta",  
        "data": {  
            "s": "SOLUSDT_SOL/USDT",  
            "b": [],  
            "a": [  
                [  
                    "22.3755",  
                    "4.7"  
                ]  
            ],  
            "u": 64892,  
            "seq": 299084  
        },  
        "cts": 1744165512234  
    }  
    

[PreviousConnect](https://bybit-exchange.github.io/docs/v5/ws/connect)[NextTrade](https://bybit-exchange.github.io/docs/v5/spread/websocket/public/trade)

  * Depths
  * Process snapshot/delta
  * Response Parameters
  * Subscribe Example
  * Event Example


