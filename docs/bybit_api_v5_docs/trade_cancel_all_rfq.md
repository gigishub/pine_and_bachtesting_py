# Cancel All RFQs

> **Source:** https://bybit-exchange.github.io/docs/v5/rfq/trade/cancel-all-rfq

---

  * [](https://bybit-exchange.github.io/docs/)
  * RFQ Trading
  * Trade
  * Cancel All RFQs



On this page

# Cancel All RFQs

Cancel all active RFQs. **Up to 50 requests per second**

info

  * Inquirer cancels order: Cancel the inquiry, all its corresponding quotes becoming invalid
  * Quoter cancels the order: The inquiry is not affected, but the quote becomes invalid



### HTTP Request​

POST`/v5/rfq/cancel-all-rfq`Copy

### Request Parameters​

None

### Response Parameters​

Parameter| Type| Comments  
---|---|---  
result| array of objects|   
> rfqId| string| Inquiry ID  
> rfqLinkId| string| Custom inquiry ID  
> code| string| Whether or not the cancellations were a success, `0`: success  
> msg| string| Cancellation failure reason  
  
### Request Example​
    
    
    POST /v5/rfq/cancel-all-rfq HTTP/1.1  
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
                "rfqId": "175766967076315412093641573648082",  
                "rfqLinkId": "",  
                "code": 0,  
                "msg": ""  
            }  
        ],  
        "retExtInfo": {},  
        "time": 1757669676581  
    }  
      
    

[PreviousCancel RFQ](https://bybit-exchange.github.io/docs/v5/rfq/trade/cancel-rfq)[NextAccept non-LP Quote](https://bybit-exchange.github.io/docs/v5/rfq/trade/accept-other-quote)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


