# Collateral Repayment

> **Source:** https://bybit-exchange.github.io/docs/v5/new-crypto-loan/fixed/repay-collateral

---

  * [](https://bybit-exchange.github.io/docs/)
  * Crypto Loan (New)
  * Fixed Loan
  * Collateral Repayment



On this page

# Collateral Repayment

> Permission: "Spot trade"  
>  UID rate limit: 1 req / second

There are limits on the repayment amount in a single transaction. Please read this [announcement](https://announcements.bybit.com/article/crypto-loan-manual-repayment-update-bltde33509ddde5e8fd/) before repaying with collateral.   
When repaying with collateral, Bybit will charge a repayment fee. The applicable fee rate is the higher of the repayment fee rates for the collateral asset and the debt asset. You can call this endpoint: [View fee rates by asset](https://www.bybit.com/x-api/spot/api/fixed-loan/v1/coin-config) to get "reapyFee" where "pledgeEnable" = 1 for coins' repayment fee rates.

info

**fixed currency offset logic**

  *     1. From Currency Perspective 
       * Orders with the closest maturity date will be sorted in descending order.
       * If the maturity date is the same, the order with the higher interest rate will be prioritized.
       * If the interest rates are the same, the order will be processed randomly.Orders will be processed sequentially. Within an order, interest will be repaid first, followed by principal.
  *     2. From Order Perspective 
       * Interest will be repaid first, followed by principal.



### HTTP Request​

POST`/v5/crypto-loan-fixed/repay-collateral`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
loanId| false| string| Loan contract ID. If not passed, the fixed currency offset logic will apply.  
loanCurrency| **true**|  string| Loan coin name  
collateralCoin| **true**|  string| Collateral currencies: Use commas to separate multiple collateral currencies  
amount| **true**|  string| Repay amount  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
  
None

### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    POST /v5/crypto-loan-fixed/repay-collateral HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: XXXXXX  
    X-BAPI-TIMESTAMP: 1752656296791  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    Content-Length: 50  
    {  
      "loanCurrency": "ETH",  
      "amount": "0.1",  
      "collateralCoin":"USDT"  
    }  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.collateral_repayment_fixed_crypto_loan(  
        loanCurrency="ETH",  
        amount="0.1",  
        collateralCoin="USDT",  
    ))  
    
    
    
      
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "ok",  
        "result": {},  
        "retExtInfo": {},  
        "time": 1756973819393  
    }  
    

[PreviousRepay](https://bybit-exchange.github.io/docs/v5/new-crypto-loan/fixed/repay)[NextGet Repayment History](https://bybit-exchange.github.io/docs/v5/new-crypto-loan/fixed/repay-history)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


