# Cancel Borrow Order

> **Source:** https://bybit-exchange.github.io/docs/v5/new-crypto-loan/fixed/cancel-borrow

---

  * [](https://bybit-exchange.github.io/docs/)
  * Crypto Loan (New)
  * Fixed Loan
  * Cancel Borrow Order



On this page

# Cancel Borrow Order

> Permission: "Spot trade"  
>  UID rate limit: 1 req / second

### HTTP Request​

POST`/v5/crypto-loan-fixed/borrow-order-cancel`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
orderId| **true**|  string| Order ID of fixed borrow order  
  
### Response Parameters​

None

### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    POST /v5/crypto-loan-fixed/borrow-order-cancel HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: XXXXXX  
    X-BAPI-TIMESTAMP: 1752652457987  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    Content-Length: 26  
      
    {  
        "orderId": "13009"  
    }  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.create_lending_order_fixed_crypto_loan(  
        orderId="13009",  
    ))  
    
    
    
      
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "ok",  
        "result": {},  
        "retExtInfo": {},  
        "time": 1752652458684  
    }  
    

[PreviousCreate Supply Order](https://bybit-exchange.github.io/docs/v5/new-crypto-loan/fixed/supply)[NextCancel Supply Order](https://bybit-exchange.github.io/docs/v5/new-crypto-loan/fixed/cancel-supply)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


