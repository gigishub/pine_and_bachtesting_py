# Cancel Quote

> **Source:** https://bybit-exchange.github.io/docs/v5/rfq/trade/cancel-quote

---

  * [](https://bybit-exchange.github.io/docs/)
  * RFQ Trading
  * Trade
  * Cancel Quote



On this page

# Cancel Quote

Cancel a quote. **Up to 50 requests per second**

info

  * You must pass one of the following params: quoteId, rfqId, and quoteLinkId.
  * If quoteId, rfqId, and quoteLinkId are all passed, they are read in this priority: quoteId > quoteLinkId > rfqId.



### HTTP Request​

POST`/v5/rfq/cancel-quote`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
quoteId|  _false_|  string| Quote ID  
rfqId|  _false_|  string| Inquiry ID  
quoteLinkId|  _false_|  string| Custom quote ID  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
result| object|   
rfqId| string| Inquiry ID  
quoteId| string| Quote ID  
quoteLinkId| string| Custom quote ID  
  
### Request Example​
    
    
    POST /v5/rfq/cancel-quote HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: XXXXXX  
    X-BAPI-TIMESTAMP: 1744083949347  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    Content-Length: 115  
      
    {  
        "quoteId":"1754364447601610516653123084412812"    
    }  
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "OK",  
        "result": {  
            "rfqId": "175740723913299909861293671607573",  
            "quoteId": "1757407443083427576602342578477746",  
            "quoteLinkId": ""  
        },  
        "retExtInfo": {},  
        "time": 1757407457635  
    }  
    

[PreviousExecute Quote](https://bybit-exchange.github.io/docs/v5/rfq/trade/execute-quote)[NextCancel All Quotes](https://bybit-exchange.github.io/docs/v5/rfq/trade/cancel-all-quotes)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


