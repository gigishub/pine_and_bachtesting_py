# Set Rate Limit

> **Source:** https://bybit-exchange.github.io/docs/v5/rate-limit/rules-for-pros/apilimit-set

---

  * [](https://bybit-exchange.github.io/docs/)
  * Rate Limit
  * API Rate Limit Rules for PROs
  * Set Rate Limit



On this page

# Set Rate Limit

> API rate limit: 50 req per second

info

  * If the UID requesting this endpoint is a master account, UIDs passed to the `uids` parameter must be subaccounts of the master account.
  * If the UID requesting this endpoint is not a master account, the UID passed to the `uids` parameter must be the UID of the subaccount requesting this endpoint.
  * Only institutional users can request this endpoint.



### HTTP Request​

POST`/v5/apilimit/set`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
list| **true**|  array| Object  
> uids| **true**|  string| Multiple UIDs separated by commas  
> [bizType](https://bybit-exchange.github.io/docs/v5/enum#biztype)| **true**|  string| Business type  
> rate| **true**|  integer| API rate limit per second  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
list| array| Object  
> uids| string| Multiple UIDs separated by commas  
> [bizType](https://bybit-exchange.github.io/docs/v5/enum#biztype)| string| Business type  
> rate| integer| API rate limit per second  
> success| boolean| Whether or not the request was successful  
> [msg](https://bybit-exchange.github.io/docs/v5/enum#msg)| string| Result message  
  
### Request Example​
    
    
    POST /v5/apilimit/set HTTP/1.1  
    Host: api.bybit.com  
    X-BAPI-SIGN: XXXXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1711420489915  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
      
    {  
        "list": [  
            {  
                "uids": "106293838",  
                "bizType": "DERIVATIVES",  
                "rate": 50  
            }  
        ]  
    }  
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "success",  
        "result": {  
            "result": [  
                {  
                    "uids": "290118",  
                    "bizType": "SPOT",  
                    "rate": 600,  
                    "success": true,  
                    "msg": "API limit updated successfully"  
                }  
            ]  
        },  
        "retExtInfo": {},  
        "time": 1754894296913  
    }  
    

[PreviousIntroduction](https://bybit-exchange.github.io/docs/v5/rate-limit/rules-for-pros/introduction)[NextGet Rate Limit](https://bybit-exchange.github.io/docs/v5/rate-limit/rules-for-pros/apilimit-query)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


