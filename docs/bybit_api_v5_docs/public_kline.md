# Kline

> **Source:** https://bybit-exchange.github.io/docs/v5/websocket/public/kline

---

  * [](https://bybit-exchange.github.io/docs/)
  * WebSocket Stream
  * Public
  * Kline



On this page

# Kline

Subscribe to the klines stream.

tip

If `confirm`=true, this means that the candle has closed. Otherwise, the candle is still open and updating.

**Available intervals:**  


  * `1` `3` `5` `15` `30` (min)
  * `60` `120` `240` `360` `720` (min)
  * `D` (day)
  * `W` (week)
  * `M` (month)



**Push frequency:** 1-60s

**Topic:**  
`kline.{interval}.{symbol}` e.g., kline.30.BTCUSDT

### Response Parameters​

Parameter| Type| Comments  
---|---|---  
topic| string| Topic name  
type| string| Data type. `snapshot`  
ts| number| The timestamp (ms) that the system generates the data  
data| array| Object  
> start| number| The start timestamp (ms)  
> end| number| The end timestamp (ms)  
> [interval](https://bybit-exchange.github.io/docs/v5/enum#interval)| string| Kline interval  
> open| string| Open price  
> close| string| Close price  
> high| string| Highest price  
> low| string| Lowest price  
> volume| string| Trade volume  
> turnover| string| Turnover  
> confirm| boolean| Whether the tick is ended or not  
> timestamp| number| The timestamp (ms) of the last matched order in the candle  
  
### Subscribe Example​
    
    
    from pybit.unified_trading import WebSocket  
    from time import sleep  
    ws = WebSocket(  
        testnet=True,  
        channel_type="linear",  
    )  
    def handle_message(message):  
        print(message)  
    ws.kline_stream(  
        interval=5,  
        symbol="BTCUSDT",  
        callback=handle_message  
    )  
    while True:  
        sleep(1)  
    

### Response Example​
    
    
    {  
        "topic": "kline.5.BTCUSDT",  
        "data": [  
            {  
                "start": 1672324800000,  
                "end": 1672325099999,  
                "interval": "5",  
                "open": "16649.5",  
                "close": "16677",  
                "high": "16677",  
                "low": "16608",  
                "volume": "2.081",  
                "turnover": "34666.4005",  
                "confirm": false,  
                "timestamp": 1672324988882  
            }  
        ],  
        "ts": 1672324988882,  
        "type": "snapshot"  
    }  
    

[PreviousTicker](https://bybit-exchange.github.io/docs/v5/websocket/public/ticker)[NextAll Liquidation](https://bybit-exchange.github.io/docs/v5/websocket/public/all-liquidation)

  * Response Parameters
  * Subscribe Example
  * Response Example


