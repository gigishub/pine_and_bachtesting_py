# Get Max Borrowable Amount

> **Source:** https://bybit-exchange.github.io/docs/v5/spot-margin-uta/max-borrowable

---

  * [](https://bybit-exchange.github.io/docs/)
  * Spot Margin Trade (UTA)
  * Get Max Borrowable Amount



On this page

# Get Max Borrowable Amount

### HTTP Request​

GET`/v5/spot-margin-trade/max-borrowable`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
currency| **true**|  string| Coin name, uppercase only  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
currency| string| Coin name, uppercase only  
maxLoan| string| Max borrowable amount  
  
* * *

### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/spot-margin-trade/max-borrowable?currency=BTC HTTP/1.1  
    Host: api.bybit.com  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1692696840996  
    X-BAPI-RECV-WINDOW: 5000  
    
    
    
      
    
    
    
      
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "Success",  
        "result": {  
            "maxLoan": "17.54689892",  
            "currency": "BTC"  
        },  
        "retExtInfo": {},  
        "time": 1756261353733  
    }  
    

[PreviousGet Status And Leverage](https://bybit-exchange.github.io/docs/v5/spot-margin-uta/status)[NextGet Position Tiers](https://bybit-exchange.github.io/docs/v5/spot-margin-uta/position-tiers)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


