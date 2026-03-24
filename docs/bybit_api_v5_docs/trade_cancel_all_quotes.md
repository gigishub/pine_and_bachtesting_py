# Cancel All Quotes

> **Source:** https://bybit-exchange.github.io/docs/v5/rfq/trade/cancel-all-quotes

---

  * [](https://bybit-exchange.github.io/docs/)
  * RFQ Trading
  * Trade
  * Cancel All Quotes



On this page

# Cancel All Quotes

Cancel all active quotes. **Up to 50 requests per second**

### HTTP Request​

POST`/v5/rfq/cancel-all-quotes`Copy

### Request Parameters​

None

### Response Parameters​

Parameter| Type| Comments  
---|---|---  
result| Object|   
> rfqId| string| Inquiry ID  
> quoteId| string| Quote ID  
> quoteLinkId| string| Custom quote ID  
> code| string| Whether or not cancellation was a success, `0`: success  
> msg| string| Cancellation failure reason  
  
### Request Example​
    
    
    POST /v5/rfq/cancel-all-quotes HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: XXXXXX  
    X-BAPI-TIMESTAMP: 1744083949347  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    Content-Length: 115  
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "OK",  
        "result": [  
            {  
                "rfqId": "175740723913299909861293671607573",  
                "quoteLinkId": "",  
                "quoteId": "1757407497684679708210572531298710",  
                "code": 0,  
                "msg": ""  
            }  
        ],  
        "retExtInfo": {},  
        "time": 1757407503982  
    }  
    

[PreviousCancel Quote](https://bybit-exchange.github.io/docs/v5/rfq/trade/cancel-quote)[NextGet RFQs (real-time)](https://bybit-exchange.github.io/docs/v5/rfq/trade/rfq-realtime)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


