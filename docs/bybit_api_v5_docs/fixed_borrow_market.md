# Get Borrowing Market

> **Source:** https://bybit-exchange.github.io/docs/v5/new-crypto-loan/fixed/borrow-market

---

  * [](https://bybit-exchange.github.io/docs/)
  * Crypto Loan (New)
  * Fixed Loan
  * Get Borrowing Market



On this page

# Get Borrowing Market

info

Does not need authentication.

If you want to borrow, you can use this endpoint to check whether there are any suitable counterparty supply orders available.

### HTTP Request​

GET`/v5/crypto-loan-fixed/borrow-order-quote`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
orderCurrency| **true**|  string| Coin name  
orderBy| **true**|  string| Order by, `apy`: annual rate; `term`; `quantity`  
term| false| string| Fixed term `7`: 7 days; `14`: 14 days; `30`: 30 days; `90`: 90 days; `180`: 180 days  
sort| false| integer| `0`: ascend, default; `1`: descend  
limit| false| integer| Limit for data size per page. [`1`, `100`]. Default: `10`  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
list| array| Object  
> orderCurrency| string| Coin name  
> term| integer| Fixed term `7`: 7 days; `14`: 14 days; `30`: 30 days; `90`: 90 days; `180`: 180 days  
> annualRate| string| Annual rate  
> qty| string| Quantity  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/crypto-loan-fixed/borrow-order-quote?orderCurrency=USDT&orderBy=apy HTTP/1.1  
    Host: api-testnet.bybit.com  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.get_borrowing_market_fixed_crypto_loan(  
        orderCurrency="USDT",  
        orderBy="apy",  
    ))  
    
    
    
      
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "ok",  
        "result": {  
            "list": [  
                {  
                    "annualRate": "0.04",  
                    "orderCurrency": "USDT",  
                    "qty": "988.78",  
                    "term": 14  
                }  
            ]  
        },  
        "retExtInfo": {},  
        "time": 1752719158890  
    }  
    

[PreviousGet Lending Market](https://bybit-exchange.github.io/docs/v5/new-crypto-loan/fixed/supply-market)[NextCreate Borrow Order](https://bybit-exchange.github.io/docs/v5/new-crypto-loan/fixed/borrow)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


