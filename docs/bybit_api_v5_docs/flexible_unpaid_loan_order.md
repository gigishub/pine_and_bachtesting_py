# Get Flexible Loans

> **Source:** https://bybit-exchange.github.io/docs/v5/new-crypto-loan/flexible/unpaid-loan-order

---

  * [](https://bybit-exchange.github.io/docs/)
  * Crypto Loan (New)
  * Flexible Loan
  * Get Flexible Loans



On this page

# Get Flexible Loans

Query for your ongoing loans

> Permission: "Spot trade"  
>  UID rate limit: 5 req / second

### HTTP Request​

GET`/v5/crypto-loan-flexible/ongoing-coin`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
loanCurrency| false| string| Loan coin name  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
list| array| Object  
> hourlyInterestRate| string| Latest hourly flexible interest rate  
> loanCurrency| string| Loan coin  
> totalDebt| string| Unpaid principal and interest  
> unpaidAmount| string| Unpaid principal  
> unpaidInterest| string| Unpaid interest  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/crypto-loan-flexible/ongoing-coin?loanCurrency=BTC HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: XXXXXX  
    X-BAPI-TIMESTAMP: 1752570124973  
    X-BAPI-RECV-WINDOW: 5000  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.get_flexible_loans_flexible_crypto_loan(  
        loanCurrency="BTC",  
    ))  
    
    
    
      
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "ok",  
        "result": {  
            "list": [  
                {  
                    "hourlyInterestRate": "0.0000018847396",  
                    "loanCurrency": "ETH",  
                    "totalDebt": "0.10000019",  
                    "unpaidAmount": "0.1",  
                    "unpaidInterest": "0.00000019"  
                }  
            ]  
        },  
        "retExtInfo": {},  
        "time": 1760452029499  
    }  
    

[PreviousCollateral Repayment](https://bybit-exchange.github.io/docs/v5/new-crypto-loan/flexible/repay-collateral)[NextGet Borrowing History](https://bybit-exchange.github.io/docs/v5/new-crypto-loan/flexible/loan-orders)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


