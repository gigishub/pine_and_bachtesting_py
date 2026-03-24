# Adjust Collateral Amount

> **Source:** https://bybit-exchange.github.io/docs/v5/new-crypto-loan/adjust-collateral

---

  * [](https://bybit-exchange.github.io/docs/)
  * Crypto Loan (New)
  * Adjust Collateral Amount



On this page

# Adjust Collateral Amount

You can increase or reduce your collateral amount. When you reduce, please obey the [Get Max. Allowed Collateral Reduction Amount](https://bybit-exchange.github.io/docs/v5/new-crypto-loan/reduce-max-collateral-amt)

> Permission: "Spot trade"  
>  UID rate limit: 1 req / second

info

  * The adjusted collateral amount will be returned to or deducted from the Funding wallet.



### HTTP Request​

POST`/v5/crypto-loan-common/adjust-ltv`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
currency| **true**|  string| Collateral coin  
amount| **true**|  string| Adjustment amount  
direction| **true**|  string| `0`: add collateral; `1`: reduce collateral  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
adjustId| long| Collateral adjustment transaction ID  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    POST /v5/crypto-loan-common/adjust-ltv HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: XXXXXX  
    X-BAPI-TIMESTAMP: 1752627997649  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    Content-Length: 69  
      
    {  
        "currency": "BTC",  
        "amount": "0.08",  
        "direction": "1"  
    }  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.adjust_collateral_amount_new_crypto_loan(  
        currency="BTC",  
        amount="0.08",  
        direction="1",  
    ))  
    
    
    
      
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "ok",  
        "result": {  
            "adjustId": 27511  
        },  
        "retExtInfo": {},  
        "time": 1752627997915  
    }  
    

[PreviousGet Max. Allowed Collateral Reduction Amount](https://bybit-exchange.github.io/docs/v5/new-crypto-loan/reduce-max-collateral-amt)[NextGet Collateral Adjustment History](https://bybit-exchange.github.io/docs/v5/new-crypto-loan/ltv-adjust-history)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


