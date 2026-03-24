# Get Order Price Limit

> **Source:** https://bybit-exchange.github.io/docs/v5/market/order-price-limit

---

  * [](https://bybit-exchange.github.io/docs/)
  * Market
  * Get Order Price Limit



On this page

# Get Order Price Limit

For derivative trading order price limit, refer to [announcement](https://announcements.bybit.com/en/article/adjustments-to-bybit-s-derivative-trading-limit-order-mechanism-blt469228de1902fff6/)  
For spot trading order price limit, refer to [announcement](https://announcements.bybit.com/en/article/title-adjustments-to-bybit-s-spot-trading-limit-order-mechanism-blt786c0c5abf865983/)  


### HTTP Request​

GET`/v5/market/price-limit`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
[category](https://bybit-exchange.github.io/docs/v5/enum#category)| false| string| Product type. `spot`,`linear`,`inverse`

  * When `category` is not passed, use `linear` by default

  
[symbol](https://bybit-exchange.github.io/docs/v5/enum#symbol)| **true**|  string| Symbol name, like `BTCUSDT`, uppercase only  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
symbol| string| Symbol name  
buyLmt| string| Highest Bid Price  
sellLmt| string| Lowest Ask Price  
ts| string| timestamp in milliseconds  
  
### Request Example​

  * HTTP
  * Python
  * Go
  * Java
  * Node.js


    
    
    GET /v5/market/price-limit?category=linear&symbol=BTCUSDT HTTP/1.1  
    Host: api-testnet.bybit.com  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
    )  
    print(session.get_price_limit(  
        category="linear",  
        symbol="BTCUSDT",  
    ))  
    
    
    
      
    
    
    
      
    
    
    
      
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "",  
        "result": {  
            "symbol": "BTCUSDT",  
            "buyLmt": "105878.10",  
            "sellLmt": "103781.60",  
            "ts": "1750302284491"  
        },  
        "retExtInfo": {},  
        "time": 1750302285376  
    }  
    

[PreviousGet Index Price Components](https://bybit-exchange.github.io/docs/v5/market/index-components)[NextGet ADL Alert](https://bybit-exchange.github.io/docs/v5/market/adl-alert)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


