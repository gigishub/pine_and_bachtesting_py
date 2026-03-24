# Modify Position

> **Source:** https://bybit-exchange.github.io/docs/v5/earn/modify-position

---

  * [](https://bybit-exchange.github.io/docs/)
  * Earn
  * Modify Position



On this page

# Modify Position

info

API key needs "Earn" permission

note

Only positions with `duration` = `Fixed` support setting auto-reinvestment. You can get the `duration` value from the response of [GET /v5/earn/product?category=OnChain](https://bybit-exchange.github.io/docs/v5/earn/product-info).

### HTTP Request​

POST`/v5/earn/position/modify`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
category| **true**|  string| Product category. Fixed value: `OnChain`  
productId| **true**|  integer| Product ID. Obtained from [GET /v5/earn/product](https://bybit-exchange.github.io/docs/v5/earn/product-info)  
positionId| **true**|  integer| Position ID. Obtained from [GET /v5/earn/position](https://bybit-exchange.github.io/docs/v5/earn/position)  
autoReinvest| **true**|  integer| Auto-reinvestment switch. `0`: Off, `1`: On  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
retCode| integer| Return code. `0` means success  
retMsg| string| Return message. Empty string `""` on success  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    POST /v5/earn/position/modify HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1773732693000  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
      
    {  
        "category": "OnChain",  
        "productId": 8,  
        "positionId": 326,  
        "autoReinvest": 1  
    }  
    
    
    
      
    
    
    
      
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "",  
        "result": {},  
        "retExtInfo": {},  
        "time": 1773732693032  
    }  
    

[PreviousGet Staked Position](https://bybit-exchange.github.io/docs/v5/earn/position)[NextGet Yield History](https://bybit-exchange.github.io/docs/v5/earn/yield-history)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


