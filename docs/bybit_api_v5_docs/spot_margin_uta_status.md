# Get Status And Leverage

> **Source:** https://bybit-exchange.github.io/docs/v5/spot-margin-uta/status

---

  * [](https://bybit-exchange.github.io/docs/)
  * Spot Margin Trade (UTA)
  * Get Status And Leverage



On this page

# Get Status And Leverage

Query the Spot margin status and leverage

### HTTP Request​

GET`/v5/spot-margin-trade/state`Copy

### Request Parameters​

None

### Response Parameters​

Parameter| Type| Comments  
---|---|---  
spotLeverage| string| Spot margin leverage. Returns `""` if the margin trade is turned off  
spotMarginMode| string| Spot margin status. `1`: on, `0`: off  
effectiveLeverage| string| actual leverage ratio. Precision retains 2 decimal places, truncate downwards  
[RUN >>](https://bybit-exchange.github.io/docs/api-explorer/v5/spot-margin-uta/status)

* * *

### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/spot-margin-trade/state HTTP/1.1  
    Host: api.bybit.com  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1692696840996  
    X-BAPI-RECV-WINDOW: 5000  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.spot_margin_trade_get_status_and_leverage())  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .getSpotMarginState()  
      .then((response) => {  
        console.log(response);  
      })  
      .catch((error) => {  
        console.error(error);  
      });  
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "OK",  
        "result": {  
            "spotLeverage": "10",  
            "spotMarginMode": "1",  
            "effectiveLeverage": "1"  
        },  
        "retExtInfo": {},  
        "time": 1692696841231  
    }  
    

[PreviousSet Leverage](https://bybit-exchange.github.io/docs/v5/spot-margin-uta/set-leverage)[NextGet Max Borrowable Amount](https://bybit-exchange.github.io/docs/v5/spot-margin-uta/max-borrowable)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


