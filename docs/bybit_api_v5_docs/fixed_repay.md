# Repay

> **Source:** https://bybit-exchange.github.io/docs/v5/new-crypto-loan/fixed/repay

---

  * [](https://bybit-exchange.github.io/docs/)
  * Crypto Loan (New)
  * Fixed Loan
  * Repay



On this page

# Repay

> Permission: "Spot trade"  
>  UID rate limit: 1 req / second

### HTTP Request​

POST`/v5/crypto-loan-fixed/fully-repay`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
loanId| false| string| Loan contract ID. Either `loanId` or `loanCurrency` needs to be passed  
loanCurrency| false| string| Loan coin. Either `loanId` or `loanCurrency` needs to be passed  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
repayId| string| Repayment transaction ID  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    POST /v5/crypto-loan-fixed/fully-repay HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: XXXXXX  
    X-BAPI-TIMESTAMP: 1752656296791  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    Content-Length: 50  
      
    {  
        "loanId": "570",  
        "loanCurrency": "ETH"  
    }  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.repay_fixed_crypto_loan(  
        loanId="570",  
        loanCurrency="ETH",  
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
    

[PreviousGet Supply Order Info](https://bybit-exchange.github.io/docs/v5/new-crypto-loan/fixed/supply-order)[NextCollateral Repayment](https://bybit-exchange.github.io/docs/v5/new-crypto-loan/fixed/repay-collateral)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


