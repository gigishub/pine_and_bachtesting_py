# Get Borrowing History

> **Source:** https://bybit-exchange.github.io/docs/v5/new-crypto-loan/flexible/loan-orders

---

  * [](https://bybit-exchange.github.io/docs/)
  * Crypto Loan (New)
  * Flexible Loan
  * Get Borrowing History



On this page

# Get Borrowing History

> Permission: "Spot trade"  
>  UID rate limit: 5 req / second

### HTTP Request​

GET`/v5/crypto-loan-flexible/borrow-history`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
orderId| false| string| Loan order ID  
loanCurrency| false| string| Loan coin name  
limit| false| string| Limit for data size per page. [`1`, `100`]. Default: `10`  
cursor| false| string| Cursor. Use the `nextPageCursor` token from the response to retrieve the next page of the result set  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
list| array| Object  
> borrowTime| long| The timestamp to borrow  
> initialLoanAmount| string| Loan amount  
> loanCurrency| string| Loan coin  
> orderId| string| Loan order ID  
> status| integer| Loan order status `1`: success; `2`: processing; `3`: fail  
nextPageCursor| string| Refer to the `cursor` request parameter  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/crypto-loan-flexible/borrow-history?limit=2 HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: XXXXXX  
    X-BAPI-TIMESTAMP: 1752570519918  
    X-BAPI-RECV-WINDOW: 5000  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.get_borrowing_history_flexible_crypto_loan(  
        limit="2",  
    ))  
    
    
    
      
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "ok",  
        "result": {  
            "list": [  
                {  
                    "borrowTime": 1752569950643,  
                    "initialLoanAmount": "0.006",  
                    "loanCurrency": "BTC",  
                    "orderId": "1364",  
                    "status": 1  
                },  
                {  
                    "borrowTime": 1752569209643,  
                    "initialLoanAmount": "0.1",  
                    "loanCurrency": "BTC",  
                    "orderId": "1363",  
                    "status": 1  
                }  
            ],  
            "nextPageCursor": "1363"  
        },  
        "retExtInfo": {},  
        "time": 1752570519414  
    }  
    

[PreviousGet Flexible Loans](https://bybit-exchange.github.io/docs/v5/new-crypto-loan/flexible/unpaid-loan-order)[NextGet Repayment History](https://bybit-exchange.github.io/docs/v5/new-crypto-loan/flexible/repay-orders)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


