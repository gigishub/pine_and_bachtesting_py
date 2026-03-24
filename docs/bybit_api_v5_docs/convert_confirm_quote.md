# Confirm a Quote

> **Source:** https://bybit-exchange.github.io/docs/v5/asset/convert/confirm-quote

---

  * [](https://bybit-exchange.github.io/docs/)
  * Asset
  * Convert
  * Confirm a Quote



On this page

# Confirm a Quote

info

  1. The exchange is async; please check the final status by calling the query result API.
  2. Make sure you confirm the quote before it expires.



### HTTP Request​

POST`/v5/asset/exchange/convert-execute`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
quoteTxId| **true**|  string| The quote tx ID from [Request a Quote](https://bybit-exchange.github.io/docs/v5/asset/convert/apply-quote#response-parameters)  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
quoteTxId| string| Quote transaction ID  
exchangeStatus| string| Exchange status 

  * init
  * processing
  * success
  * failure

  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    POST /v5/asset/exchange/convert-execute HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1720071899789  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    Content-Length: 52  
      
    {  
        "quoteTxId": "10100108106409343501030232064"  
    }  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.confirm_a_quote(  
        quoteTxId="10100108106409343501030232064",  
    ))  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .confirmConvertQuote({  
        quoteTxId: '10100108106409343501030232064',  
      })  
      .then((response) => {  
        console.log(response);  
      })  
      .catch((error) => {  
        console.error(error);  
      });  
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "ok",  
        "result": {  
            "exchangeStatus": "processing",  
            "quoteTxId": "10100108106409343501030232064"  
        },  
        "retExtInfo": {},  
        "time": 1720071900529  
    }  
    

[PreviousRequest a Quote](https://bybit-exchange.github.io/docs/v5/asset/convert/apply-quote)[NextGet Convert Status](https://bybit-exchange.github.io/docs/v5/asset/convert/get-convert-result)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


