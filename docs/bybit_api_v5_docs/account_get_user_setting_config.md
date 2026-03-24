# Get Trade Behaviour Config

> **Source:** https://bybit-exchange.github.io/docs/v5/account/get-user-setting-config

---

  * [](https://bybit-exchange.github.io/docs/)
  * Account
  * Get Trade Behaviour Config



On this page

# Get Trade Behaviour Config

You can get configuration how the system behaves when your limit order price exceeds the highest bid or lowest ask price. The response also includes whether [Delta Neutral mode](https://bybit-exchange.github.io/docs/v5/account/set-delta-mode) is enabled.

* * *

Where x% is [priceLimitRatioX](https://bybit-exchange.github.io/docs/v5/market/instrument); and y% is the [priceLimitRatioY](https://bybit-exchange.github.io/docs/v5/market/instrument):

Spot

  * **Maximum buy price** : _Min[Max(Index Price, Index Price × (1 + x%) + 2-Minute Average Premium), Index Price × (1 + y%)]_
  * **Minimum sell price** : _Max[Min(Index Price, Index Price × (1 – x%) + 2-Minute Average Premium), Index Price × (1 – y%)]_



Futures

  * **Maximum buy price** : _Min (Max (Index Price, Mark Price × (1 + x%)), Mark Price × (1 + y%))_
  * **Minimum sell price** : _Max (Min (Index Price, Mark Price × (1 - x%)), Mark Price × (1 - y%))_



Default Setting

  * Spot: **lpaSpot = false.** If the order price exceeds the limit, the system rejects the request.

  * Futures: **lpaPerp = false.** If the order price exceeds the limit, the system will automatically adjust the price to the nearest allowed price (i.e., highest bid or lowest ask).




### HTTP Request​

GET`/v5/account/user-setting-config`Copy

### Request Parameters​

None

### Response Parameters​

Parameter| Type| Comments  
---|---|---  
result| array| Object  
> lpaSpot| boolean| 

  * `true`: If the order price exceeds the limit, the system will automatically adjust the price to the nearest allowed price
  * `false`: If the order price exceeds the limit, the system rejects the request.

  
> lpaPerp| boolean| 

  * `true`: If the order price exceeds the limit, the system rejects the request.
  * `false`: If the order price exceeds the limit, the system will automatically adjust the price to the nearest allowed price.

  
> deltaEnable| boolean| Whether [Delta Neutral mode](https://bybit-exchange.github.io/docs/v5/account/set-delta-mode) is enabled. `true`: enabled; `false`: disabled  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/account/user-setting-config HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: XXXXXX  
    X-BAPI-TIMESTAMP: 1753255927950  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    Content-Length: 52  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.get_user_setting_config())  
    
    
    
      
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "OK",  
        "result": {  
            "lpaSpot": true,  
            "lpaPerp": false,  
            "deltaEnable": false  
        },  
        "retExtInfo": {},  
        "time": 1756794317787  
    }  
    

[PreviousGet SMP Group ID](https://bybit-exchange.github.io/docs/v5/account/smp-group)[NextSet Delta Neutral Mode](https://bybit-exchange.github.io/docs/v5/account/set-delta-mode)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


