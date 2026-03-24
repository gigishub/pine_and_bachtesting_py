# Cancel RFQ

> **Source:** https://bybit-exchange.github.io/docs/v5/rfq/trade/cancel-rfq

---

  * [](https://bybit-exchange.github.io/docs/)
  * RFQ Trading
  * Trade
  * Cancel RFQ



On this page

# Cancel RFQ

Cancel RFQ. **Up to 50 requests per second**

info

  * You must pass either rfqId or rfqLinkId.
  * If both rfqId and rfqLinkId are passed, only rfqId is considered.



### HTTP Request​

POST`/v5/rfq/cancel-rfq`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
rfqId|  _false_|  string| Inquiry ID  
rfqLinkId|  _false_|  string| Custom inquiry ID  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
rfqId| string| Inquiry ID  
rfqLinkId| string| Custom inquiry ID  
  
### Request Example​
    
    
    POST /v5/rfq/cancel-rfq HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: XXXXXX  
    X-BAPI-TIMESTAMP: 1744083949347  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    Content-Length: 115  
      
    {  
        "rfqId": "1756871488168105512459181956436945"  
    }  
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "OK",  
        "result": {  
            "rfqId": "1756871488168105512459181956436945",  
            "rfqLinkId": ""  
        },  
        "retExtInfo": {},  
        "time": 1756871494507  
    }  
    

[PreviousGet RFQ Configuration](https://bybit-exchange.github.io/docs/v5/rfq/trade/rfq-config)[NextCancel All RFQs](https://bybit-exchange.github.io/docs/v5/rfq/trade/cancel-all-rfq)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


