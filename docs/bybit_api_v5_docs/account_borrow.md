# Manual Borrow

> **Source:** https://bybit-exchange.github.io/docs/v5/account/borrow

---

  * [](https://bybit-exchange.github.io/docs/)
  * Account
  * Manual Borrow



On this page

# Manual Borrow

info

Borrowing via OpenAPI endpoint supports variable rate borrowing only.

### HTTP Request​

POST`/v5/account/borrow`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
coin| **true**|  string| coin name, uppercase only  
amount| **true**|  string| Borrow amount  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
result| array| Object  
> coin| string| coin name, uppercase only  
> amount| string| Borrow amount  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    POST /v5/account/borrow HTTP/1.1  
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
            "coin": "BTC",  
            "amount": "0.01"  
        },  
        "retExtInfo": {},  
        "time": 1756197991955  
    }  
    

[PreviousGet Account Instruments Info](https://bybit-exchange.github.io/docs/v5/account/instrument)[NextManual Repay Without Asset Conversion](https://bybit-exchange.github.io/docs/v5/account/no-convert-repay)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


