# Set Price Limit Behaviour

> **Source:** https://bybit-exchange.github.io/docs/v5/account/set-price-limit

---

  * [](https://bybit-exchange.github.io/docs/)
  * Account
  * Set Price Limit Behaviour



On this page

# Set Price Limit Behaviour

You can configure how the system behaves when your limit order price exceeds the highest bid or lowest ask price. You can query your current configuration with [Get Trade Behaviour Setting](https://bybit-exchange.github.io/docs/v5/account/get-user-setting-config). Learn more about the price limit for [spot](https://www.bybit.com/en/help-center/article/Bybit-Spot-Trading-Rules#A) and [futures](https://www.bybit.com/en/help-center/article?id=000002177#D) in the help centre.

* * *

Where x% is [priceLimitRatioX](https://bybit-exchange.github.io/docs/v5/market/instrument); and y% is the [priceLimitRatioY](https://bybit-exchange.github.io/docs/v5/market/instrument):

Spot

  * **Maximum buy price** : _Min[Max(Index Price, Index Price × (1 + x%) + 2-Minute Average Premium), Index Price × (1 + y%)]_
  * **Minimum sell price** : _Max[Min(Index Price, Index Price × (1 – x%) + 2-Minute Average Premium), Index Price × (1 – y%)]_



Futures

  * **Maximum buy price** : _Min (Max (Index Price, Mark Price × (1 + x%)), Mark Price × (1 + y%))_
  * **Minimum sell price** : _Max (Min (Index Price, Mark Price × (1 - x%)), Mark Price × (1 - y%))_



Default Setting

  * Spot: **modifyEnable = false.** If the order price exceeds the limit, the system rejects the request.   
Corresponds to [Get Limit Price Behaviour](https://bybit-exchange.github.io/docs/v5/account/get-user-setting-config), where **lpaSpot = false, lpaPerp = true**

  * Futures: **modifyEnable = true.** If the order price exceeds the limit, the system will automatically adjust the price to the nearest allowed price (i.e., highest bid or lowest ask).  
Corresponds to [Get Limit Price Behaviour](https://bybit-exchange.github.io/docs/v5/account/get-user-setting-config), where **lpaSpot = true, lpaPerp = false**

  * Setting either `linear` or `inverse` will set the behaviour for **all futures**.




### HTTP Request​

POST`/v5/account/set-limit-px-action`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
category| **true**|  string| `linear`, `inverse`, `spot`  
modifyEnable| **true**|  boolean| `true`: allow the system to modify the order price  
`false`: reject your order request  
  
### Response Parameters​

None

### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    POST /v5/account/set-limit-px-action HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: XXXXXX  
    X-BAPI-TIMESTAMP: 1753255927950  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    Content-Length: 52  
      
    {  
        "category": "spot",  
        "modifyEnable": true  
    }  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.set_limit_price_action(  
        category="spot",  
        modifyEnable=True,  
    ))  
    
    
    
      
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "success",  
        "result": {},  
        "retExtInfo": {},  
        "time": 1753255927952  
    }  
    

[PreviousSet Delta Neutral Mode](https://bybit-exchange.github.io/docs/v5/account/set-delta-mode)[NextRepay Liability](https://bybit-exchange.github.io/docs/v5/account/repay-liability)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


