# Get Broker Earning

> **Source:** https://bybit-exchange.github.io/docs/v5/abandon/earning

---

  * [](https://bybit-exchange.github.io/docs/)
  * Abandoned Endpoints
  * Get Broker Earning



On this page

# Get Broker Earning

danger

This endpoint has been deprecated, please move to new [Get Exchange Broker Earning](https://bybit-exchange.github.io/docs/v5/broker/exchange-broker/exchange-earning)

info

  * Use exchange broker master account to query
  * The data can support up to past 6 months until T-1
  * `startTime` & `endTime` are either entered at the same time or not entered



### HTTP Request​

GET`/v5/broker/earning-record`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
bizType| false| string| Business type. `SPOT`, `DERIVATIVES`, `OPTIONS`  
startTime| false| integer| The start timestamp(ms)  
endTime| false| integer| The end timestamp(ms)  
limit| false| integer| Limit for data size per page. [`1`, `1000`]. Default: `1000`  
cursor| false| string| Cursor. Use the `nextPageCursor` token from the response to retrieve the next page of the result set  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
list| array| Object  
> userId| string| UID  
> bizType| string| Business type  
> symbol| string| Symbol name  
> coin| string| Coin name. The currency of earning  
> earning| string| Commission  
> orderId| string| Order ID  
> execTime| string| Execution timestamp (ms)  
nextPageCursor| string| Refer to the `cursor` request parameter  
  
### Request Example​

  * HTTP
  * Python


    
    
    GET /v5/broker/earning-record?bizType=SPOT&startTime=1686240000000&endTime=1686326400000&limit=1 HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1686708862669  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    
    
    
      
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "success",  
        "result": {  
            "list": [  
                {  
                    "userId": "xxxx",  
                    "bizType": "SPOT",  
                    "symbol": "BTCUSDT",  
                    "coin": "BTC",  
                    "earning": "0.000015",  
                    "orderId": "1531607271849858304",  
                    "execTime": "1686306035957"  
                }  
            ],  
            "nextPageCursor": "0%2C1"  
        },  
        "retExtInfo": {},  
        "time": 1686708863283  
    }  
    

[PreviousBorrow](https://bybit-exchange.github.io/docs/v5/abandon/borrow)[NextGet Order Records](https://bybit-exchange.github.io/docs/v5/abandon/order-record)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


