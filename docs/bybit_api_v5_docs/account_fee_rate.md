# Get Fee Rate

> **Source:** https://bybit-exchange.github.io/docs/v5/account/fee-rate

---

  * [](https://bybit-exchange.github.io/docs/)
  * Account
  * Get Fee Rate



On this page

# Get Fee Rate

Get the trading fee rate.

### HTTP Request​

GET`/v5/account/fee-rate`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
category| **true**|  string| Product type. `spot`, `linear`, `inverse`, `option`  
symbol| false| string| Symbol name, like `BTCUSDT`, uppercase only. Valid for `linear`, `inverse`, `spot`  
baseCoin| false| string| Base coin, uppercase only. `SOL`, `BTC`, `ETH`. Valid for `option`  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
category| string| Product type. `spot`, `option`. _Derivatives does not have this field_  
list| array| Object  
> symbol| string| Symbol name. Keeps `""` for Options  
> baseCoin| string| Base coin. `SOL`, `BTC`, `ETH`

  * Spot and Derivatives does not have this field

  
> takerFeeRate| string| Taker fee rate  
> makerFeeRate| string| Maker fee rate  
[RUN >>](https://bybit-exchange.github.io/docs/api-explorer/v5/account/fee-rate)

* * *

### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/account/fee-rate?symbol=ETHUSDT HTTP/1.1  
    Host: api.bybit.com  
    X-BAPI-SIGN: XXXXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1676360412362  
    X-BAPI-RECV-WINDOW: 5000  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.get_fee_rates(  
        symbol="ETHUSDT",  
    ))  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
        testnet: true,  
        key: 'xxxxxxxxxxxxxxxxxx',  
        secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
        .getFeeRate({  
            category: 'linear',  
            symbol: 'ETHUSDT',  
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
        "retMsg": "OK",  
        "result": {  
            "list": [  
                {  
                    "symbol": "ETHUSDT",  
                    "takerFeeRate": "0.0006",  
                    "makerFeeRate": "0.0001"  
                }  
            ]  
        },  
        "retExtInfo": {},  
        "time": 1676360412576  
    }  
    

[PreviousManual Repay](https://bybit-exchange.github.io/docs/v5/account/repay)[NextGet Collateral Info](https://bybit-exchange.github.io/docs/v5/account/collateral-info)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


