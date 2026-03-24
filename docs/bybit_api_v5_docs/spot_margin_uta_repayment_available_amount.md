# Get Available Amount to Repay

> **Source:** https://bybit-exchange.github.io/docs/v5/spot-margin-uta/repayment-available-amount

---

  * [](https://bybit-exchange.github.io/docs/)
  * Spot Margin Trade (UTA)
  * Get Available Amount to Repay



On this page

# Get Available Amount to Repay

### HTTP Request​

GET`/v5/spot-margin-trade/repayment-available-amount`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
currency| **true**|  string| Coin name, uppercase only  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
currency| string| Coin name, uppercase only  
lossLessRepaymentAmount| string| Repayment amount = min(spot coin available balance, coin borrow amount)  
  
* * *

### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/spot-margin-trade/repayment-available-amount?currency=BTC HTTP/1.1  
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
            "lossLessRepaymentAmount": "0.02000000",  
            "currency": "BTC"  
        },  
        "retExtInfo": {},  
        "time": 1756273388821  
    }  
    

[PreviousGet Coin State](https://bybit-exchange.github.io/docs/v5/spot-margin-uta/coinstate)[NextSet Auto Repay Mode](https://bybit-exchange.github.io/docs/v5/spot-margin-uta/set-auto-repay-mode)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


