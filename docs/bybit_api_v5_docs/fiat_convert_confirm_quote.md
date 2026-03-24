# Confirm a Quote

> **Source:** https://bybit-exchange.github.io/docs/v5/asset/fiat-convert/confirm-quote

---

  * [](https://bybit-exchange.github.io/docs/)
  * Asset
  * Fiat-Convert
  * Confirm a Quote



On this page

# Confirm a Quote

info

  1. The exchange is async; please check the final status by calling the convert history API.
  2. Make sure you confirm the quote before it expires.



### HTTP Request​

POST`/v5/fiat/trade-execute`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
quoteTxId| **true**|  string| The quote tx ID from [Request a Quote](https://bybit-exchange.github.io/docs/v5/asset/fiat-convert/quote-apply#response-parameters)  
subUserId| **true**|  string| The user's sub userId in bybit  
webhookUrl| false| string| API URL to call when order is successful or failed (max 256 characters)  
MerchantRequestId| false| string| Customised request ID(maximum length of 36)

  * Generally it is useless, but it is convenient to track the quote request internally if you fill this field

  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
tradeNo| string| Trade order No  
merchantRequestId| string| Customised request ID  
  
### Request Example​

  * HTTP


    
    
    POST /v5/fiat/trade-execute HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1720071899789  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    Content-Length: 52  
      
    {  
        "quoteTxId": "QuoteTaxId123456",  
        "subUserId":"43456"  
    }  
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "success",  
        "result": {  
            "tradeNo": "TradeNo123456",  
            "merchantRequestId": ""  
        }  
    }  
    

[PreviousRequest a Quote](https://bybit-exchange.github.io/docs/v5/asset/fiat-convert/quote-apply)[NextGet Convert Status](https://bybit-exchange.github.io/docs/v5/asset/fiat-convert/query-trade)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


