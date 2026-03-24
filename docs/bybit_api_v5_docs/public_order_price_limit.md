# Order Price Limit

> **Source:** https://bybit-exchange.github.io/docs/v5/websocket/public/order-price-limit

---

  * [](https://bybit-exchange.github.io/docs/)
  * WebSocket Stream
  * Public
  * Order Price Limit



On this page

# Order Price Limit

Subscribe to Get Order Price Limit.

For derivative trading order price limit, refer to [announcement](https://announcements.bybit.com/en/article/adjustments-to-bybit-s-derivative-trading-limit-order-mechanism-blt469228de1902fff6/)  
For spot trading order price limit, refer to [announcement](https://announcements.bybit.com/en/article/title-adjustments-to-bybit-s-spot-trading-limit-order-mechanism-blt786c0c5abf865983/)  


Push frequency: **300ms**

**Topic:**  
`priceLimit.{symbol}`  


### Response Parameters​

Parameter| Type| Comments  
---|---|---  
topic| string| Topic name  
ts| number| The timestamp (ms) that the system generates the data  
data| array| Object.  
> symbol| string| Symbol name  
> buyLmt| string| Highest Bid Price  
> sellLmt| string| Lowest Ask Price  
  
### Subscribe Example​

  * JSON
  * Python


    
    
    {  
        "op": "subscribe",  
        "args": [  
            "priceLimit.BTCUSDT"  
        ]  
    }  
    
    
    
    from pybit.unified_trading import WebSocket  
    from time import sleep  
    ws = WebSocket(  
        testnet=True,  
        channel_type="linear",  
    )  
    def handle_message(message):  
        print(message)  
    ws.price_limit_stream(  
        symbol="BTCUSDT",  
        callback=handle_message  
    )  
    while True:  
        sleep(1)  
    

### Response Example​
    
    
    {  
        "topic": "priceLimit.BTCUSDT",  
        "data": {  
            "symbol": "BTCUSDT",  
            "buyLmt": "114450.00",  
            "sellLmt": "103550.00"  
        },  
        "ts": 1750059683782  
    }  
    

[PreviousInsurance Pool](https://bybit-exchange.github.io/docs/v5/websocket/public/insurance-pool)[NextADL Alert](https://bybit-exchange.github.io/docs/v5/websocket/public/adl-alert)

  * Response Parameters
  * Subscribe Example
  * Response Example


