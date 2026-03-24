# Obtain Max Loan Amount

> **Source:** https://bybit-exchange.github.io/docs/v5/new-crypto-loan/max-loan-amt

---

  * [](https://bybit-exchange.github.io/docs/)
  * Crypto Loan (New)
  * Obtain Max Loan Amount



On this page

# Obtain Max Loan Amount

> Permission: "Spot trade"  
>  UID rate limit: 5 req / second

### HTTP Request​

POST`/v5/crypto-loan-common/max-loan`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
currency| **true**|  string| Coin to borrow  
collateralList| false| array<object>|   
> amount| **true**|  string| Collateral amount. Only check funding account balance  
> ccy| **true**|  string| Collateral coin. Both `amount` & `ccy` are required, when you pass "collateralList"  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
currency| string| Coin to borrow  
maxLoan| string| Based on your current collateral, and with the option to add more collateral, you can borrow up to `maxLoan`  
notionalUsd| string| Nontional USD value  
remainingQuota| string| The **remaining** individual platform borrowing limit (shared between main and sub accounts)  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    POST /v5/crypto-loan-common/max-loan HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: XXXXXX  
    X-BAPI-TIMESTAMP: 1768532512103  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    Content-Length: 208  
      
    {  
        "currency": "BTC",  
        "collateralList": [  
            {  
                "ccy": "XRP",  
                "amount": "1000"  
            },  
            {  
                "ccy": "USDT",  
                "amount": "1000"  
            }  
        ]  
    }  
    
    
    
      
    
    
    
      
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "ok",  
        "result": {  
            "currency": "BTC",  
            "maxLoan": "0.1722",  
            "notionalUsd": "16456.06",  
            "remainingQuota": "9999999.9421"  
        },  
        "retExtInfo": {},  
        "time": 1768533990031  
    }  
    

[PreviousGet Crypto Loan Position](https://bybit-exchange.github.io/docs/v5/new-crypto-loan/crypto-loan-position)[NextBorrow](https://bybit-exchange.github.io/docs/v5/new-crypto-loan/flexible/borrow)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


