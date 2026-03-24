# Set Leverage

> **Source:** https://bybit-exchange.github.io/docs/v5/spot-margin-uta/set-leverage

---

  * [](https://bybit-exchange.github.io/docs/)
  * Spot Margin Trade (UTA)
  * Set Leverage



On this page

# Set Leverage

Set the user's maximum leverage in spot cross margin

caution

Your account needs to activate spot margin first; i.e., you must have finished the quiz on web / app.   
The updated leverage must be less than or equal to the maximum leverage of the currency

### HTTP Request​

POST`/v5/spot-margin-trade/set-leverage`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
leverage| **true**|  string| Leverage. [`2`, `10`].  
currency| false| string| Coin name, uppercase only  
[RUN >>](https://bybit-exchange.github.io/docs/api-explorer/v5/spot-margin-uta/set-leverage)

* * *

### Response Parameters​

None

### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    POST /v5/spot-margin-trade/set-leverage HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1672299806626  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
      
    {  
        "leverage": "4"  
    }  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.spot_margin_trade_set_leverage(  
        leverage="4",  
    ))  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .setSpotMarginLeverage('4')  
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
        "result": {},  
        "retExtInfo": {},  
        "time": 1672710944282  
    }  
    

[PreviousToggle Margin Trade](https://bybit-exchange.github.io/docs/v5/spot-margin-uta/switch-mode)[NextGet Status And Leverage](https://bybit-exchange.github.io/docs/v5/spot-margin-uta/status)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


