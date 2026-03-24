# Insurance Pool

> **Source:** https://bybit-exchange.github.io/docs/v5/websocket/public/insurance-pool

---

  * [](https://bybit-exchange.github.io/docs/)
  * WebSocket Stream
  * Public
  * Insurance Pool



On this page

# Insurance Pool

Subscribe to get the update of insurance pool balance 

Push frequency: **1s**

**Topic:**  
USDT contracts: `insurance.USDT`  
USDC contracts: `insurance.USDC` (**note** : all USDC Perpetuals, USDC Futures have their own shared insurance pools)  
Inverse contracts: `insurance.inverse`

info

  * Shared insurance pool data is **not** pushed, please refer to Rest API [Get Insurance](https://bybit-exchange.github.io/docs/v5/market/insurance) to understand which symbols belong to isolated or shared insurance pools.
  * No event will be published if the balances of all insurance pools remain unchanged.



### Response Parameters​

Parameter| Type| Comments  
---|---|---  
topic| string| Topic name  
type| string| Data type. `snapshot`, `delta`  
ts| number| The timestamp (ms) that the system generates the data  
data| Object|   
> coin| string| Insurance pool coin  
> symbols| string| Symbol name  
> balance| string| Balance  
> updateTime| string| Data updated timestamp (ms)  
  
### Subscribe Example​

  * JSON
  * Python


    
    
    {  
        "op": "subscribe",  
        "args": [  
            "insurance.USDT",  
            "insurance.USDC"  
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
    ws.insurance_pool_stream(  
        contract_group=["USDT", "USDC"],  
        callback=handle_message  
    )  
    while True:  
        sleep(1)  
    

### Response Example​
    
    
    {  
        "topic": "insurance.USDT",  
        "type": "delta",  
        "ts": 1747722930000,  
        "data": [  
            {  
                "coin": "USDT",  
                "symbols": "GRIFFAINUSDT",  
                "balance": "25614.92972633",  
                "updateTime": "1747722930000"  
            },  
            {  
                "coin": "USDT",  
                "symbols": "CGPTUSDT",  
                "balance": "100000.27064825",  
                "updateTime": "1747722930000"  
            },  
            {  
                "coin": "USDT",  
                "symbols": "GOATUSDT",  
                "balance": "20352.32665441",  
                "updateTime": "1747722930000"  
            },  
            {  
                "coin": "USDT",  
                "symbols": "XTERUSDT",  
                "balance": "19998.81533291",  
                "updateTime": "1747722930000"  
            }  
        ]  
    }  
    

[PreviousAll Liquidation](https://bybit-exchange.github.io/docs/v5/websocket/public/all-liquidation)[NextOrder Price Limit](https://bybit-exchange.github.io/docs/v5/websocket/public/order-price-limit)

  * Response Parameters
  * Subscribe Example
  * Response Example


