# Repay

> **Source:** https://bybit-exchange.github.io/docs/v5/new-crypto-loan/flexible/repay

---

  * [](https://bybit-exchange.github.io/docs/)
  * Crypto Loan (New)
  * Flexible Loan
  * Repay



On this page

# Repay

Fully or partially repay a loan. If interest is due, that is paid off first, with the loaned amount being paid off only after due interest.

> Permission: "Spot trade"  
>  UID rate limit: 1 req / second

info

  * The repaid amount will be deducted from the Funding wallet.
  * The collateral amount will not be auto returned when you don't fully repay the debt, but you can also adjust collateral amount



### HTTP Request​

POST`/v5/crypto-loan-flexible/repay`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
loanCurrency| **true**|  string| Loan coin name  
amount| **true**|  string| Amount to repay  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
repayId| string| Repayment transaction ID  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    POST /v5/crypto-loan-flexible/repay HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: XXXXXX  
    X-BAPI-TIMESTAMP: 1752569628364  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    Content-Length: 52  
      
    {  
        "loanCurrency": "BTC",  
        "amount": "0.005"  
    }  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.repay_flexible_crypto_loan(  
        loanCurrency="BTC",  
        loanAmount="0.005",  
    ))  
    
    
    
      
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "ok",  
        "result": {  
            "repayId": "1771"  
        },  
        "retExtInfo": {},  
        "time": 1752569614549  
    }  
    

[PreviousBorrow](https://bybit-exchange.github.io/docs/v5/new-crypto-loan/flexible/borrow)[NextCollateral Repayment](https://bybit-exchange.github.io/docs/v5/new-crypto-loan/flexible/repay-collateral)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


