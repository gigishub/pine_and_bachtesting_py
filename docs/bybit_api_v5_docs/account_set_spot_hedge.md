# Set Spot Hedging

> **Source:** https://bybit-exchange.github.io/docs/v5/account/set-spot-hedge

---

  * [](https://bybit-exchange.github.io/docs/)
  * Account
  * Set Spot Hedging



On this page

# Set Spot Hedging

You can turn on/off Spot hedging feature in Portfolio margin

### HTTP Request​

POST`/v5/account/set-hedging-mode`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
setHedgingMode| **true**|  string| `ON`, `OFF`  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
retCode| integer| Result code  
retMsg| string| Result message  
[RUN >>](https://bybit-exchange.github.io/docs/api-explorer/v5/account/set-spot-hedge)

* * *

### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    POST /v5/account/set-hedging-mode HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1700117968580  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    Content-Length: 31  
      
    {  
        "setHedgingMode": "OFF"  
    }  
    
    
    
      
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .setSpotHedging({  
        setHedgingMode: 'ON' | 'OFF',  
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
        "retMsg": "SUCCESS"  
    }  
    

[PreviousSet Margin Mode](https://bybit-exchange.github.io/docs/v5/account/set-margin-mode)[NextGet Borrow History (2 years)](https://bybit-exchange.github.io/docs/v5/account/borrow-history)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


