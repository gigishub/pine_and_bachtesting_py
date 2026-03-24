# Get Hourly Yield History

> **Source:** https://bybit-exchange.github.io/docs/v5/earn/hourly-yield

---

  * [](https://bybit-exchange.github.io/docs/)
  * Earn
  * Get Hourly Yield History



On this page

# Get Hourly Yield History

info

API key needs "Earn" permission

### HTTP Request​

GET`/v5/earn/hourly-yield`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
category| **true**|  string| `FlexibleSaving`  
productId| false| string| Product ID  
startTime| false| integer| The start timestamp (ms).

  * 1\. If both are not provided, the default is to return data from the last 7 days.
  * 2\. If both are provided, the difference between the endTime and startTime must be less than or equal to 7 days. 

  
endTime| false| integer| The endTime timestamp (ms)  
limit| false| integer| Limit for data size per page. Range: [1, 100]. Default: 50  
cursor| false| string| Cursor, use the returned `nextPageCursor` to query data for the next page.  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
nextPageCursor| string| Refer to the `cursor` request parameter  
list| array| Object  
> productId| string| Product ID  
> coin| string| Coin name: "BTC", "ETH"  
> id| string| Unique key (guaranteed to be unique only under the same user)  
> amount| string| Yield Amount. Example: 10  
> effectiveStakingAmount| string| Effective staking amount, e.g., 1000.00  
> status| string| Order status: `Pending`, `Success`, `Fail`  
> hourlyDate| string| Hourly yield time(ms) eg: 1755478800000  
> createdAt| string| Order creation time in milliseconds, e.g., 1684738540561  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/earn/hourly-yield?category=FlexibleSaving HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1739937044221  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    
    
    
      
    
    
    
      
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "",  
        "result": {  
            "list": [  
                {  
                    "productId": "428",  
                    "coin": "USDT",  
                    "amount": "0.060810502283105022",  
                    "effectiveStakingAmount": "1000",  
                    "hourlyDate": "1759989600000",  
                    "status": "Success",  
                    "createdAt": "1759989603000"  
                }  
            ],  
            "nextPageCursor": ""  
        },  
        "retExtInfo": {},  
        "time": 1759993045287  
    }  
    

[PreviousGet Yield History](https://bybit-exchange.github.io/docs/v5/earn/yield-history)[NextGet APR History](https://bybit-exchange.github.io/docs/v5/earn/apr-history)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


