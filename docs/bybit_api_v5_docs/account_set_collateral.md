# Set Collateral Coin

> **Source:** https://bybit-exchange.github.io/docs/v5/account/set-collateral

---

  * [](https://bybit-exchange.github.io/docs/)
  * Account
  * Set Collateral Coin



On this page

# Set Collateral Coin

You can decide whether the assets in the Unified account needs to be collateral coins.

### HTTP Request​

POST`/v5/account/set-collateral-switch`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
coin| **true**|  string| Coin name, uppercase only 

  * You can get collateral coin from [here](https://bybit-exchange.github.io/docs/v5/account/collateral-info)
  * USDT, USDC cannot be set

  
collateralSwitch| **true**|  string| `ON`: switch on collateral, `OFF`: switch off collateral  
  
### Response Parameters​

None

[RUN >>](https://bybit-exchange.github.io/docs/api-explorer/v5/account/set-collateral)

* * *

### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    POST /v5/account/set-collateral-switch HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1690513916181  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    Content-Length: 55  
      
    {  
        "coin": "BTC",  
        "collateralSwitch": "ON"  
    }  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.set_collateral_coin(  
        coin="BTC",  
        collateralSwitch="ON"  
    ))  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .setCollateralCoin({  
        coin: 'BTC',  
        collateralSwitch: 'ON',  
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
        "retMsg": "SUCCESS",  
        "result": {},  
        "retExtInfo": {},  
        "time": 1690515818656  
    }  
    

[PreviousGet DCP Info](https://bybit-exchange.github.io/docs/v5/account/dcp-info)[NextSet Margin Mode](https://bybit-exchange.github.io/docs/v5/account/set-margin-mode)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


