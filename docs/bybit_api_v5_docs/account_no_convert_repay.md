# Manual Repay Without Asset Conversion

> **Source:** https://bybit-exchange.github.io/docs/v5/account/no-convert-repay

---

  * [](https://bybit-exchange.github.io/docs/)
  * Account
  * Manual Repay Without Asset Conversion



On this page

# Manual Repay Without Asset Conversion

info

  * If `coin` is passed in input parameter and `amount` is not, the repayment amount will be the available spot balance of that coin.



important

  1. When repaying, system will only use the spot available balance of the debt currency. Users can perform a manual repay without converting their other assets.
  2. To check the spot available amount to repay, you can call this API: [Get Available Amount to Repay](https://bybit-exchange.github.io/docs/v5/spot-margin-uta/repayment-available-amount)
  3. Repayment is prohibited between 04:00 and 05:30 per hour. Interest is calculated based on the BorrowAmount at 05:00 per hour.
  4. System repays floating-rate liabilities first, followed by fixed-rate
  5. Starting Mar 17, 2026 (gradual rollout, fully released on Mar 24, 2026), BYUSDT can be used for repayment.



### HTTP Request​

POST`/v5/account/no-convert-repay`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
coin| **true**|  string| coin name, uppercase only  
amount| false| string| Repay amount. If `coin` is not passed in input parameter, `amount` can not be passed in input parameter  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
result| array| Object  
> resultStatus| string| 

  * `P`: Processing
  * `SU`: Success
  * `FA`: Failed

  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    POST /v5/account/no-convert-repay HTTP/1.1  
    Host: api.bybit.com  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1675842997277  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
      
    {  
        "coin":"BTC",  
        "amount":"0.01"  
    }  
    
    
    
      
    
    
    
      
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "success",  
        "result": {  
            "resultStatus": "P"  
        },  
        "retExtInfo": {},  
        "time": 1756295680801  
    }  
    

[PreviousManual Borrow](https://bybit-exchange.github.io/docs/v5/account/borrow)[NextManual Repay](https://bybit-exchange.github.io/docs/v5/account/repay)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


