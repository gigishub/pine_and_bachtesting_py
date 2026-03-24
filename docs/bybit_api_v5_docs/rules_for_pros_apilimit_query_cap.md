# Get Rate Limit Cap

> **Source:** https://bybit-exchange.github.io/docs/v5/rate-limit/rules-for-pros/apilimit-query-cap

---

  * [](https://bybit-exchange.github.io/docs/)
  * Rate Limit
  * API Rate Limit Rules for PROs
  * Get Rate Limit Cap



On this page

# Get Rate Limit Cap

> API rate limit: 50 req per second

info

  * Get your institutions's total rate limit usage and cap, across the board.
  * Main UIDs or sub UIDs can query this endpoint, but a main UID can only see the rate limits of subs below it, and not the subs of other main UIDs.



### HTTP Request​

GET`/v5/apilimit/query-cap`Copy

### Request Parameters​

None

### Response Parameters​

Parameter| Type| Comments  
---|---|---  
list| array| Object  
> [bizType](https://bybit-exchange.github.io/docs/v5/enum#biztype)| string| Business type  
> totalRate| integer| Total API rate limit usage accross all subaccounts and master account  
> insCap| integer| Institutional-level API rate limit per second (depends on your pro level)  
> uidCap| integer| UID-level API rate limit per second  
  
### Request Example​
    
    
    GET /v5/apilimit/query-cap HTTP/1.1  
    Host: api.bybit.com  
    X-BAPI-SIGN: XXXXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1728460942776  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    Content-Length: 2  
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "success",  
        "result": {  
            "list": [  
                {  
                    "insCap": "30000",  
                    "uidCap": "600",  
                    "totalRate": "29882",  
                    "bizType": "SPOT"  
                },  
                {  
                    "insCap": "30000",  
                    "uidCap": "600",  
                    "totalRate": "29882",  
                    "bizType": "OPTIONS"  
                },  
                {  
                    "insCap": "40000",  
                    "uidCap": "800",  
                    "totalRate": "39932",  
                    "bizType": "DERIVATIVES"  
                }  
            ]  
        },  
        "retExtInfo": {},  
        "time": 1758857589872  
    }  
    

[PreviousGet Rate Limit](https://bybit-exchange.github.io/docs/v5/rate-limit/rules-for-pros/apilimit-query)[NextGet All Rate Limits](https://bybit-exchange.github.io/docs/v5/rate-limit/rules-for-pros/apilimit-query-all)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


