# Set Margin Mode

> **Source:** https://bybit-exchange.github.io/docs/v5/account/set-margin-mode

---

  * [](https://bybit-exchange.github.io/docs/)
  * Account
  * Set Margin Mode



On this page

# Set Margin Mode

Default is regular margin mode

### HTTP Request​

POST`/v5/account/set-margin-mode`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
setMarginMode| **true**|  string| `ISOLATED_MARGIN`, `REGULAR_MARGIN`(i.e. Cross margin), `PORTFOLIO_MARGIN`  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
reasons| array| Object. If requested successfully, it is an empty array  
> reasonCode| string| Fail reason code  
> reasonMsg| string| Fail reason msg  
[RUN >>](https://bybit-exchange.github.io/docs/api-explorer/v5/account/set-margin-mode)

* * *

### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    POST /v5/account/set-margin-mode HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1672134396332  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
      
    {  
        "setMarginMode": "PORTFOLIO_MARGIN"  
    }  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.set_margin_mode(  
        setMarginMode="PORTFOLIO_MARGIN",  
    ))  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
        testnet: true,  
        key: 'xxxxxxxxxxxxxxxxxx',  
        secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
        .setMarginMode('PORTFOLIO_MARGIN')  
        .then((response) => {  
            console.log(response);  
        })  
        .catch((error) => {  
            console.error(error);  
        });  
    

### Response Example​
    
    
    {  
        "retCode": 3400045,  
        "retMsg": "Set margin mode failed",  
        "result": {  
            "reasons": [  
                {  
                    "reasonCode": "3400000",  
                    "reasonMsg": "Equity needs to be equal to or greater than 1000 USDC"  
                }  
            ]  
        }  
    }  
    

[PreviousSet Collateral Coin](https://bybit-exchange.github.io/docs/v5/account/set-collateral)[NextSet Spot Hedging](https://bybit-exchange.github.io/docs/v5/account/set-spot-hedge)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


