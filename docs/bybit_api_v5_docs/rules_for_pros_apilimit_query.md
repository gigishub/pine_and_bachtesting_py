# Get Rate Limit

> **Source:** https://bybit-exchange.github.io/docs/v5/rate-limit/rules-for-pros/apilimit-query

---

  * [](https://bybit-exchange.github.io/docs/)
  * Rate Limit
  * API Rate Limit Rules for PROs
  * Get Rate Limit



On this page

# Get Rate Limit

> API rate limit: 50 req per second

info

  * A master account can query its own and its subaccounts' API rate limit.
  * A subaccount can only query its own API rate limit.



### HTTP Request​

GET`/v5/apilimit/query`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
uids| **true**|  string| Multiple UIDs separated by commas  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
list| array| Object  
> uids| string| Multiple UIDs separated by commas  
> [bizType](https://bybit-exchange.github.io/docs/v5/enum#biztype)| string| Business type  
> rate| integer| API rate limit per second  
  
### Request Example​
    
    
    GET /v5/apilimit/query?uids=290118 HTTP/1.1  
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
                    "uids": "290118",  
                    "bizType": "SPOT",  
                    "rate": 600  
                },  
                {  
                    "uids": "290118",  
                    "bizType": "DERIVATIVES",  
                    "rate": 400  
                }  
            ]  
        },  
        "retExtInfo": {},  
        "time": 1754894341984  
    }  
    

[PreviousSet Rate Limit](https://bybit-exchange.github.io/docs/v5/rate-limit/rules-for-pros/apilimit-set)[NextGet Rate Limit Cap](https://bybit-exchange.github.io/docs/v5/rate-limit/rules-for-pros/apilimit-query-cap)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


