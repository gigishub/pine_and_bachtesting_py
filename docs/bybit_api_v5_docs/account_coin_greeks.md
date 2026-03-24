# Get Coin Greeks

> **Source:** https://bybit-exchange.github.io/docs/v5/account/coin-greeks

---

  * [](https://bybit-exchange.github.io/docs/)
  * Account
  * Get Coin Greeks



On this page

# Get Coin Greeks

Get current account Greeks information

info

  * During periods of extreme market volatility, this interface may experience increased latency or temporary delays in data delivery



### HTTP Request​

GET`/v5/asset/coin-greeks`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
baseCoin| false| string| Base coin, uppercase only. If not passed, all supported base coin greeks will be returned by default  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
list| array| Object  
> baseCoin| string| Base coin. e.g.,`BTC`,`ETH`,`SOL`  
> totalDelta| string| Delta value  
> totalGamma| string| Gamma value  
> totalVega| string| Vega value  
> totalTheta| string| Theta value  
[RUN >>](https://bybit-exchange.github.io/docs/api-explorer/v5/account/coin-greeks)

* * *

### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/asset/coin-greeks?baseCoin=BTC HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1672287887610  
    X-BAPI-RECV-WINDOW: 5000  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.get_coin_greeks(  
        baseCoin="BTC",  
    ))  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
        testnet: true,  
        key: 'xxxxxxxxxxxxxxxxxx',  
        secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
        .getCoinGreeks('BTC')  
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
            "list": [  
                {  
                    "baseCoin": "BTC",  
                    "totalDelta": "0.00004001",  
                    "totalGamma": "-0.00000009",  
                    "totalVega": "-0.00039689",  
                    "totalTheta": "0.01243824"  
                }  
            ]  
        },  
        "retExtInfo": {},  
        "time": 1672287887942  
    }  
    

[PreviousBatch Set Collateral Coin](https://bybit-exchange.github.io/docs/v5/account/batch-set-collateral)[NextGet MMP State](https://bybit-exchange.github.io/docs/v5/account/get-mmp-state)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


