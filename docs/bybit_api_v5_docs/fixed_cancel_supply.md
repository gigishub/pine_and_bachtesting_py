# Cancel Supply Order

> **Source:** https://bybit-exchange.github.io/docs/v5/new-crypto-loan/fixed/cancel-supply

---

  * [](https://bybit-exchange.github.io/docs/)
  * Crypto Loan (New)
  * Fixed Loan
  * Cancel Supply Order



On this page

# Cancel Supply Order

> Permission: "Spot trade"  
>  UID rate limit: 1 req / second

### HTTP Request​

POST`/v5/crypto-loan-fixed/supply-order-cancel`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
orderId| **true**|  string| Order ID of fixed supply order  
  
### Response Parameters​

None

### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    POST /v5/crypto-loan-fixed/supply-order-cancel HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: XXXXXX  
    X-BAPI-TIMESTAMP: 1752652612736  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    Content-Length: 26  
      
    {  
        "orderId": "13577"  
    }  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.cancel_lending_order_fixed_crypto_loan(  
        orderId="13577",  
    ))  
    
    
    
      
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "ok",  
        "result": {},  
        "retExtInfo": {},  
        "time": 1752652613638  
    }  
    

[PreviousCancel Borrow Order](https://bybit-exchange.github.io/docs/v5/new-crypto-loan/fixed/cancel-borrow)[NextGet Borrow Contract Info](https://bybit-exchange.github.io/docs/v5/new-crypto-loan/fixed/borrow-contract)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


