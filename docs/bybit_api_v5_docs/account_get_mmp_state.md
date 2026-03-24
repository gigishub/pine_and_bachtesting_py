# Get MMP State

> **Source:** https://bybit-exchange.github.io/docs/v5/account/get-mmp-state

---

  * [](https://bybit-exchange.github.io/docs/)
  * Account
  * Get MMP State



On this page

# Get MMP State

### HTTP Request​

GET`/v5/account/mmp-state`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
baseCoin| **true**|  string| Base coin, uppercase only  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
result| array| Object  
> baseCoin| string| Base coin  
> mmpEnabled| boolean| Whether the account is enabled mmp  
> window| string| Time window (ms)  
> frozenPeriod| string| Frozen period (ms)  
> qtyLimit| string| Trade qty limit  
> deltaLimit| string| Delta limit  
> mmpFrozenUntil| string| Unfreeze timestamp (ms)  
> mmpFrozen| boolean| Whether the mmp is triggered. 

  * `true`: mmpFrozenUntil is meaningful
  * `false`: please ignore the value of mmpFrozenUntil

  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    POST /v5/account/mmp-reset HTTP/1.1  
    Host: api.bybit.com  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1675842997277  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
      
    {  
        "baseCoin": "ETH"  
    }  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.get_mmp_state(  
        baseCoin="ETH",  
    ))  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
        testnet: true,  
        key: 'xxxxxxxxxxxxxxxxxx',  
        secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
        .getMMPState('ETH')  
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
            "result": [  
                {  
                    "baseCoin": "BTC",  
                    "mmpEnabled": true,  
                    "window": "5000",  
                    "frozenPeriod": "100000",  
                    "qtyLimit": "0.01",  
                    "deltaLimit": "0.01",  
                    "mmpFrozenUntil": "1675760625519",  
                    "mmpFrozen": false  
                }  
            ]  
        },  
        "retExtInfo": {},  
        "time": 1675843188984  
    }  
    

[PreviousGet Coin Greeks](https://bybit-exchange.github.io/docs/v5/account/coin-greeks)[NextReset MMP](https://bybit-exchange.github.io/docs/v5/account/reset-mmp)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


