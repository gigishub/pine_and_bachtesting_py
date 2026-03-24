# Set Delta Neutral Mode

> **Source:** https://bybit-exchange.github.io/docs/v5/account/set-delta-mode

---

  * [](https://bybit-exchange.github.io/docs/)
  * Account
  * Set Delta Neutral Mode



On this page

# Set Delta Neutral Mode

Delta Neutral Mode is designed to enhance the trading experience for users running delta-neutral strategies. When enabled, positions that meet the Delta Neutral criteria are ranked lower in the ADL (Auto-Deleveraging) queue, reducing the risk of being auto-deleveraged during extreme market conditions. For more details, refer to the [Delta Neutral Mode](https://www.bybit.com/en/help-center/article?id=1772092051700) help article.

You can turn on/off the Delta Neutral mode. To query the current status, use the [Get Trade Behaviour Config](https://bybit-exchange.github.io/docs/v5/account/get-user-setting-config) endpoint and check the `deltaEnable` field in the response.

### HTTP Request​

POST`/v5/account/set-delta-mode`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
deltaEnable| **true**|  string| `1`: Enable; `0`: Disable  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
resultStatus| integer| `success`;`failed`  
  
* * *

### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    POST /v5/account/set-delta-mode HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1773113846000  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    Content-Length: 20  
      
    {  
        "deltaEnable": "1"  
    }  
    
    
    
      
    
    
    
      
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "success",  
        "result": {},  
        "retExtInfo": {},  
        "time": 1773113846355  
    }  
    

[PreviousGet Trade Behaviour Config](https://bybit-exchange.github.io/docs/v5/account/get-user-setting-config)[NextSet Price Limit Behaviour](https://bybit-exchange.github.io/docs/v5/account/set-price-limit)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


