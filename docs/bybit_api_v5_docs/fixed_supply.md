# Create Supply Order

> **Source:** https://bybit-exchange.github.io/docs/v5/new-crypto-loan/fixed/supply

---

  * [](https://bybit-exchange.github.io/docs/)
  * Crypto Loan (New)
  * Fixed Loan
  * Create Supply Order



On this page

# Create Supply Order

> Permission: "Spot trade"  
>  UID rate limit: 1 req / second

### HTTP Request​

POST`/v5/crypto-loan-fixed/supply`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
orderCurrency| **true**|  string| Currency to supply  
orderAmount| **true**|  string| Amount to supply  
annualRate| **true**|  string| Customizable annual interest rate, e.g., `0.02` means 2%  
term| **true**|  string| Fixed term `7`: 7 days; `14`: 14 days; `30`: 30 days; `90`: 90 days; `180`: 180 days  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
orderId| string| Supply order ID  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    POST /v5/crypto-loan-fixed/supply HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: XXXXXX  
    X-BAPI-TIMESTAMP: 1752652261840  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    Content-Length: 104  
      
    {  
        "orderCurrency": "USDT",  
        "orderAmount": "2002.21",  
        "annualRate": "0.35",  
        "term": "7"  
    }  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.create_lending_order_fixed_crypto_loan(  
        orderCurrency="USDT",  
        orderAmount="2002.21",  
        annualRate="0.35",  
        term="7",  
    ))  
    
    
    
      
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "ok",  
        "result": {  
            "orderId": "13007"  
        },  
        "retExtInfo": {},  
        "time": 1752633650147  
    }  
    

[PreviousRenew Borrow Order](https://bybit-exchange.github.io/docs/v5/new-crypto-loan/fixed/renew)[NextCancel Borrow Order](https://bybit-exchange.github.io/docs/v5/new-crypto-loan/fixed/cancel-borrow)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


