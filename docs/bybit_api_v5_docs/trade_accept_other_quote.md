# Accept non-LP Quote

> **Source:** https://bybit-exchange.github.io/docs/v5/rfq/trade/accept-other-quote

---

  * [](https://bybit-exchange.github.io/docs/)
  * RFQ Trading
  * Trade
  * Accept non-LP Quote



On this page

# Accept non-LP Quote

Accept non-LP Quote. **Up to 50 requests** per second.

info

  * Accepts non-LP quotes.



### HTTP Request​

POST`/v5/rfq/accept-other-quote`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
rfqId| **true**|  string| Inquiry ID  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
result| object|   
> rfqId| string| Inquiry ID  
  
### Request Example​
    
    
    POST /v5/rfq/accept-other-quote HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: XXXXXX  
    X-BAPI-TIMESTAMP: 1744083949347  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    Content-Length: 115  
      
    {  
      "rfqId":"1754364447601610516653123084412812",   
    }  
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "OK",  
        "result": {  
            "rfqId": "1754364447601610516653123084412812"  
        },  
        "retExtInfo": {},  
        "time": 1757405933132  
    }  
    

[PreviousCancel All RFQs](https://bybit-exchange.github.io/docs/v5/rfq/trade/cancel-all-rfq)[NextCreate Quote](https://bybit-exchange.github.io/docs/v5/rfq/trade/create-quote)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


