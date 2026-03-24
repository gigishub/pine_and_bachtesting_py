# Get RPI Orderbook

> **Source:** https://bybit-exchange.github.io/docs/v5/market/rpi-orderbook

---

  * [](https://bybit-exchange.github.io/docs/)
  * Market
  * Get RPI Orderbook



On this page

# Get RPI Orderbook

Query for orderbook depth data.

> **Covers: Spot / USDT contract / USDC contract / Inverse contract /**

  * Contract: 50-level of RPI orderbook data
  * Spot: 50-level of RPI orderbook data



info

  * The response is in the snapshot format.



### HTTP Request​

GET`/v5/market/rpi_orderbook`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
[category](https://bybit-exchange.github.io/docs/v5/enum#category)| false| string| Product type. `spot`, `linear`, `inverse`  
symbol| **true**|  string| Symbol name, like `BTCUSDT`, uppercase only  
limit| **true**|  integer| Limit size for each bid and ask: [1, 50]  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
s| string| Symbol name  
> b| array| Bids. For `snapshot` stream. Sorted by price in descending order  
>> b[0]| string| Bid price  
>> b[1]| string| None RPI bid size 

  * The delta data has size=0, which means that all quotations for this price have been filled or cancelled

  
>> b[2]| string| RPI bid size 

  * When a bid RPI order crosses with a non-RPI ask price, the quantity of the bid RPI becomes invalid and is hidden

  
> a| array| Asks. For `snapshot` stream. Sorted by price in ascending order  
>> a[0]| string| Ask price  
>> a[1]| string| None RPI ask size 

  * The delta data has size=0, which means that all quotations for this price have been filled or cancelled

  
>> a[2]| string| RPI ask size 

  * When an ask RPI order crosses with a non-RPI bid price, the quantity of the ask RPI becomes invalid and is hidden

  
ts| integer| The timestamp (ms) that the system generates the data  
u| integer| Update ID, is always in sequence corresponds to `u` in the 50-level [WebSocket RPI orderbook stream](https://bybit-exchange.github.io/docs/v5/websocket/public/orderbook-rpi)  
seq| integer| Cross sequence 

  * You can use this field to compare different levels orderbook data, and for the smaller seq, then it means the data is generated earlier. 

  
cts| integer| The timestamp from the matching engine when this orderbook data is produced. It can be correlated with `T` from [public trade channel](https://bybit-exchange.github.io/docs/v5/websocket/public/trade)  
  
* * *

### Request Example​

  * HTTP
  * Python
  * Go
  * Java
  * Node.js


    
    
    GET /v5/market/rpi_orderbook?category=spot&symbol=BTCUSDT HTTP/1.1  
    Host: api-testnet.bybit.com  
    
    
    
      
    
    
    
      
    
    
    
      
    
    
    
      
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "OK",  
        "result": {  
            "s": "BTCUSDT",  
            "a": [  
                [  
                    "116600.00",  
                    "4.428",  
                    "0.000"  
                ]  
            ],  
            "b": [  
                [  
                    "116599.90",  
                    "3.721",  
                    "0.000"  
                ]  
            ],  
            "ts": 1758078286128,  
            "u": 28419362,  
            "seq": 454803359210,  
            "cts": 1758078286118  
        },  
        "retExtInfo": {},  
        "time": 1758078286162  
    }  
    

[PreviousGet Orderbook](https://bybit-exchange.github.io/docs/v5/market/orderbook)[NextGet Tickers](https://bybit-exchange.github.io/docs/v5/market/tickers)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


