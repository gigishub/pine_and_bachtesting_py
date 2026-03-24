# Confirm a Quote

> **Source:** https://bybit-exchange.github.io/docs/v5/asset/convert-small-balance/confirm-quote

---

  * [](https://bybit-exchange.github.io/docs/)
  * Asset
  * Convert Small Balances
  * Confirm a Quote



On this page

# Confirm a Quote

info

  * API key permission: `Convert`
  * API rate limit: `5 req /s`
  * The exchange is async; please check the final status by calling the query [Get Exchange History](https://bybit-exchange.github.io/docs/v5/asset/convert-small-balance/exchange-history).
  * Make sure you confirm the quote before it expires.



### HTTP Request​

POST`/v5/asset/covert/small-balance-execute`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
quoteId| **true**|  string| The quote ID from [Request a Quote](https://bybit-exchange.github.io/docs/v5/asset/convert-small-balance/request-quote#response-parameters)  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
quoteId| string| Quote ID  
exchangeTxId| string| Exchange ID, the same value as `quoteId`  
submitTime| string| Submit ts  
status| string| `init`, `processing`, `success`, `failure`, `partial_fulfillment`  
msg| string| By default is `""`  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    POST /v5/asset/covert/small-balance-execute HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-API-KEY: XXXXXX  
    X-BAPI-TIMESTAMP: 1766128195297  
    X-BAPI-RECV-WINDOW: 5000  
    X-BAPI-SIGN: XXXXXX  
    Content-Type: application/json  
    Content-Length: 49  
      
    {  
        "quoteId": "1010075157602517596339322880"  
    }  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.confirm_a_quote_small_balance(  
        quoteId="1010075157602517596339322880",  
    ))  
    
    
    
      
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "ok",  
        "result": {  
            "quoteId": "1010075157602517596339322880",  
            "exchangeTxId": "1010075157602517596339322880",  
            "submitTime": "1766128195512",  
            "status": "processing",  
            "msg": ""  
        },  
        "retExtInfo": {},  
        "time": 1766128195512  
    }  
    

[PreviousRequest a Quote](https://bybit-exchange.github.io/docs/v5/asset/convert-small-balance/request-quote)[NextGet Exchange History](https://bybit-exchange.github.io/docs/v5/asset/convert-small-balance/exchange-history)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


