# Orderbook

> **Source:** https://bybit-exchange.github.io/docs/v5/websocket/public/orderbook

---

  * [](https://bybit-exchange.github.io/docs/)
  * WebSocket Stream
  * Public
  * Orderbook



On this page

# Orderbook

Subscribe to the orderbook stream. Supports different depths.

info

[Retail Price Improvement (RPI)](https://www.bybit.com/en/help-center/article/Retail-Price-Improvement-RPI-Order) orders will not be included in the messages.

### Depths​

**Linear & inverse:**  
Level 1 data, push frequency: **10ms**  
Level 50 data, push frequency: **20ms**  
Level 200 data, push frequency: **100ms**  
Level 1000 data, push frequency: **200ms**  


**Spot:**  
Level 1 data, push frequency: **10ms**  
Level 50 data, push frequency: **20ms**  
Level 200 data, push frequency: **100ms**  
Level 1000 data, push frequency: **200ms**  


**Option:**  
Level 25 data, push frequency: **20ms**  
Level 100 data, push frequency: **100ms**  


**Topic:**  
`orderbook.{depth}.{symbol}` e.g., orderbook.1.BTCUSDT

### Process snapshot/delta​

To process `snapshot` and `delta` messages, please follow these rules:

Once you have subscribed successfully, you will receive a `snapshot`. The WebSocket will keep pushing `delta` messages every time the orderbook changes. If you receive a new `snapshot` message, you will have to reset your local orderbook. If there is a problem on Bybit's end, a `snapshot` will be re-sent, which is guaranteed to contain the latest data.

To apply `delta` updates:

  * If you receive an amount that is `0`, delete the entry
  * If you receive an amount that does not exist, insert it
  * If the entry exists, you simply update the value



See working code examples of this logic in the [FAQ](https://bybit-exchange.github.io/docs/faq#how-can-i-process-websocket-snapshot-and-delta-messages).

info

  * Linear, inverse, spot level 1 data: if 3 seconds have elapsed without a change in the orderbook, a `snapshot` message will be pushed again, and the field `u` will be the same as that in the previous message.
  * **Linear, inverse, spot level 1 data has`snapshot` message only**
  * **PreLaunch contracts** : there is no feed until `ContinuousTrading` stage



reminder

  * Spot (all levels) & Futures (Level 1): the "ts" field appears **before** the "type" field in the JSON message, e.g., `{"toptic": "orderbook.1.BTCUSDT", "ts": "1772694601512", "type": "snapshot", ...}`
  * Futures (all other levels): the "ts" field appears **after** the "type" field in the JSON message, e.g., `{"toptic": "orderbook.50.BTCUSDT", "type": "delta", "ts": "1772694601512", ...}`



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
  * For level 1 of linear, inverse Perps and Futures, the snapshot data will be pushed again when there is no change in 3 seconds, and the "u" will be the same as that in the previous message

  
> seq| integer| Cross sequence 

  * You can use this field to compare different levels orderbook data, and for the smaller seq, then it means the data is generated earlier. 

  
cts| number| The timestamp from the matching engine when this orderbook data is produced. It can be correlated with `T` from [public trade channel](https://bybit-exchange.github.io/docs/v5/websocket/public/trade)  
  
### Subscribe Example​
    
    
    from pybit.unified_trading import WebSocket  
    from time import sleep  
    ws = WebSocket(  
        testnet=True,  
        channel_type="linear",  
    )  
    def handle_message(message):  
        print(message)  
    ws.orderbook_stream(  
        depth=50,  
        symbol="BTCUSDT",  
        callback=handle_message  
    )  
    while True:  
        sleep(1)  
    

### Response Example​

  * Snapshot
  * Delta


    
    
    {  
        "topic": "orderbook.50.BTCUSDT",  
        "type": "snapshot",  
        "ts": 1672304484978,  
        "data": {  
            "s": "BTCUSDT",  
            "b": [  
                ...,  
                [  
                    "16493.50",  
                    "0.006"  
                ],  
                [  
                    "16493.00",  
                    "0.100"  
                ]  
            ],  
            "a": [  
                [  
                    "16611.00",  
                    "0.029"  
                ],  
                [  
                    "16612.00",  
                    "0.213"  
                ],  
                ...,  
            ],  
        "u": 18521288,  
        "seq": 7961638724  
        },  
        "cts": 1672304484976  
    }  
    
    
    
    {  
        "topic": "orderbook.50.BTCUSDT",  
        "type": "delta",  
        "ts": 1687940967466,  
        "data": {  
            "s": "BTCUSDT",  
            "b": [  
                [  
                    "30247.20",  
                    "30.028"  
                ],  
                [  
                    "30245.40",  
                    "0.224"  
                ],  
                [  
                    "30242.10",  
                    "1.593"  
                ],  
                [  
                    "30240.30",  
                    "1.305"  
                ],  
                [  
                    "30240.00",  
                    "0"  
                ]  
            ],  
            "a": [  
                [  
                    "30248.70",  
                    "0"  
                ],  
                [  
                    "30249.30",  
                    "0.892"  
                ],  
                [  
                    "30249.50",  
                    "1.778"  
                ],  
                [  
                    "30249.60",  
                    "0"  
                ],  
                [  
                    "30251.90",  
                    "2.947"  
                ],  
                [  
                    "30252.20",  
                    "0.659"  
                ],  
                [  
                    "30252.50",  
                    "4.591"  
                ]  
            ],  
            "u": 177400507,  
            "seq": 66544703342  
        },  
        "cts": 1687940967464  
    }  
    

[PreviousConnect](https://bybit-exchange.github.io/docs/v5/ws/connect)[NextRPI Orderbook](https://bybit-exchange.github.io/docs/v5/websocket/public/orderbook-rpi)

  * Depths
  * Process snapshot/delta
  * Response Parameters
  * Subscribe Example
  * Response Example


