# Get Max. Allowed Collateral Reduction Amount

> **Source:** https://bybit-exchange.github.io/docs/v5/new-crypto-loan/reduce-max-collateral-amt

---

  * [](https://bybit-exchange.github.io/docs/)
  * Crypto Loan (New)
  * Get Max. Allowed Collateral Reduction Amount



On this page

# Get Max. Allowed Collateral Reduction Amount

Retrieve the maximum redeemable amount of your collateral asset based on LTV.

> Permission: "Spot trade"  
>  UID rate limit: 5 req / second

### HTTP Request​

GET`/v5/crypto-loan-common/max-collateral-amount`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
currency| **true**|  string| Collateral coin  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
maxCollateralAmount| string| Maximum reduction amount  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/crypto-loan-common/max-collateral-amount?currency=BTC HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: XXXXXX  
    X-BAPI-TIMESTAMP: 1752627687351  
    X-BAPI-RECV-WINDOW: 5000  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.get_max_allowed_collateral_reduction_amount_new_crypto_loan(  
        collateralCurrency="BTC",  
    ))  
    
    
    
      
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "ok",  
        "result": {  
            "maxCollateralAmount": "0.08585184"  
        },  
        "retExtInfo": {},  
        "time": 1752627687596  
    }  
    

[PreviousGet Collateral Coins](https://bybit-exchange.github.io/docs/v5/new-crypto-loan/collateral-coin)[NextAdjust Collateral Amount](https://bybit-exchange.github.io/docs/v5/new-crypto-loan/adjust-collateral)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


