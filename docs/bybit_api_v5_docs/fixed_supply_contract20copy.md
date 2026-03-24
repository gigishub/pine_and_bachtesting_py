# Get Supply Contract Info

> **Source:** https://bybit-exchange.github.io/docs/v5/new-crypto-loan/fixed/supply-contract%20copy

---

  * [](https://bybit-exchange.github.io/docs/)
  * Crypto Loan (New)
  * Fixed Loan
  * Get Supply Contract Info



On this page

# Get Supply Contract Info

> Permission: "Spot trade"  
>  UID rate limit: 5 req / second

### HTTP Request​

GET`/v5/crypto-loan-fixed/supply-contract-info`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
orderId| false| string| Supply order ID  
supplyId| false| string| Supply contract ID  
supplyCurrency| false| string| Supply coin name  
term| false| string| Fixed term `7`: 7 days; `14`: 14 days; `30`: 30 days; `90`: 90 days; `180`: 180 days  
limit| false| string| Limit for data size per page. [`1`, `100`]. Default: `10`  
cursor| false| string| Cursor. Use the `nextPageCursor` token from the response to retrieve the next page of the result set  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
list| array| Object  
> annualRate| string| Annual rate for the supply  
> supplyCurrency| string| Supply coin  
> supplyTime| string| Supply timestamp  
> supplyAmount| string| Supply amount  
> interestPaid| string| Paid interest  
> supplyId| string| Supply contract ID  
> orderId| string| Supply order ID  
> redemptionTime| string| Planned time to redeem  
> penaltyInterest| string| Overdue interest  
> actualRedemptionTime| string| Actual time to redeem  
> status| integer| Supply contract status `1`: Supplying; `2`: Redeemed  
> term| string| Fixed term `7`: 7 days; `14`: 14 days; `30`: 30 days; `90`: 90 days; `180`: 180 days  
nextPageCursor| string| Refer to the `cursor` request parameter  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/crypto-loan-fixed/supply-contract-info?supplyCurrency=USDT HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: XXXXXX  
    X-BAPI-TIMESTAMP: 1752654376532  
    X-BAPI-RECV-WINDOW: 5000  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.get_lending_contract_info_fixed_crypto_loan(  
        supplyCurrency="USDT",  
    ))  
    
    
    
      
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "ok",  
        "result": {  
            "list": [  
                {  
                    "actualRedemptionTime": "1753087596082",  
                    "annualRate": "0.01",  
                    "interest": "0.13041095890410959",  
                    "orderId": "13564",  
                    "penaltyInterest": "0",  
                    "redemptionTime": "1753087596082",  
                    "status": 1,  
                    "supplyAmount": "800",  
                    "supplyCurrency": "USDT",  
                    "supplyId": "567",  
                    "supplyTime": "1752482796082",  
                    "term": "7"  
                }  
            ],  
            "nextPageCursor": "567"  
        },  
        "retExtInfo": {},  
        "time": 1752654377461  
    }  
    

[PreviousGet Borrow Contract Info](https://bybit-exchange.github.io/docs/v5/new-crypto-loan/fixed/borrow-contract)[NextGet Borrow Order Info](https://bybit-exchange.github.io/docs/v5/new-crypto-loan/fixed/borrow-order)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


