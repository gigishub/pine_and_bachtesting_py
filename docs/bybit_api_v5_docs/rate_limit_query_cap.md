# Get Rate Limit Cap

> **Source:** https://bybit-exchange.github.io/docs/v5/broker/exchange-broker/rate-limit/query-cap

---

  * [](https://bybit-exchange.github.io/docs/)
  * Broker
  * Exchange Broker
  * Rate Limit Setup
  * Get Rate Limit Cap



On this page

# Get Rate Limit Cap

> API rate limit: 5 req per second

info

  * Get your exchange broker account entity total rate limit usage and cap, across the board
  * Only Main UIDs can query this endpoint
  * Only exchange broker account can call this endpoint
  * If you never apply for a specifical config via account manager, it gives empty response.



### HTTP Request​

GET`/v5/broker/apilimit/query-cap`Copy

### Request Parameters​

None

### Response Parameters​

Parameter| Type| Comments  
---|---|---  
list| array| Object  
> [bizType](https://bybit-exchange.github.io/docs/v5/enum#biztype)| string| Business type  
> totalRate| string| Total API rate limit usage accross all subaccounts and master account  
> ebCap| string| Entity-level API rate limit per second  
> uidCap| string| UID-level API rate limit per second  
  
### Request Example​
    
    
    GET /v5/broker/apilimit/query-cap HTTP/1.1  
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
                    "ebCap": "900",  
                    "uidCap": "100",  
                    "totalRate": "825",  
                    "bizType": "SPOT"  
                },  
                {  
                    "ebCap": "900",  
                    "uidCap": "100",  
                    "totalRate": "760",  
                    "bizType": "OPTIONS"  
                },  
                {  
                    "ebCap": "900",  
                    "uidCap": "100",  
                    "totalRate": "760",  
                    "bizType": "DERIVATIVES"  
                }  
            ]  
        },  
        "retExtInfo": {},  
        "time": 1770610126806  
    }  
    

[PreviousSet Rate Limit](https://bybit-exchange.github.io/docs/v5/broker/exchange-broker/rate-limit/set)[NextGet All Rate Limits](https://bybit-exchange.github.io/docs/v5/broker/exchange-broker/rate-limit/query-all)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


