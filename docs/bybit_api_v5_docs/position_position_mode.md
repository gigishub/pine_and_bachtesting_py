# Switch Position Mode

> **Source:** https://bybit-exchange.github.io/docs/v5/position/position-mode

---

  * [](https://bybit-exchange.github.io/docs/)
  * Position
  * Switch Position Mode



On this page

# Switch Position Mode

It supports to switch the position mode for **USDT perpetual** and **Inverse futures**. If you are in one-way Mode, you can only open one position on Buy or Sell side. If you are in hedge mode, you can open both Buy and Sell side positions simultaneously.

tip

  * Priority for configuration to take effect: symbol > coin > system default
  * System default: one-way mode
  * If the request is by coin (settleCoin), then all symbols based on this setteCoin that do not have position and open order will be batch switched, and new listed symbol based on this settleCoin will be the same mode you set.



### Example​

| System default| coin| symbol  
---|---|---|---  
Initial setting| one-way| never configured| never configured  
Result| All USDT perpetual trading pairs are one-way mode  
**Change 1**|  -| -| Set BTCUSDT to hedge-mode  
Result| BTCUSDT becomes hedge-mode, and all other symbols keep one-way mode  
list new symbol ETHUSDT| ETHUSDT is one-way mode (inherit default rules)   
**Change 2**|  -| Set USDT to hedge-mode| -  
Result| All current trading pairs with no positions or orders are hedge-mode, and no adjustments will be made for trading pairs with positions and orders  
list new symbol SOLUSDT| SOLUSDT is hedge-mode (Inherit coin rule)  
**Change 3**|  -| -| Set ASXUSDT to one-mode  
Take effect result| AXSUSDT is one-way mode, other trading pairs have no change  
list new symbol BITUSDT| BITUSDT is hedge-mode (Inherit coin rule)  
  
### The position-switch ability for each contract​

| UTA2.0  
---|---  
USDT perpetual| **Support one-way & hedge-mode**  
USDT futures| Support one-way **only**  
USDC perpetual| Support one-way **only**  
Inverse perpetual| Support one-way **only**  
Inverse futures| Support one-way **only**  
  
### HTTP Request​

POST`/v5/position/switch-mode`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
[category](https://bybit-exchange.github.io/docs/v5/enum#category)| **true**|  string| Product type `linear`, USDT Contract  
symbol| false| string| Symbol name, like `BTCUSDT`, uppercase only. Either `symbol` or `coin` is **required**. `symbol` has a higher priority  
coin| false| string| Coin, uppercase only  
mode| **true**|  integer| Position mode. `0`: Merged Single. `3`: Both Sides  
[RUN >>](https://bybit-exchange.github.io/docs/api-explorer/v5/position/position-mode)

* * *

### Response Parameters​

None

### Request Example​

  * HTTP
  * Python
  * Java
  * Node.js


    
    
    POST /v5/position/switch-mode HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1675249072041  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    Content-Length: 87  
      
    {  
        "category":"inverse",  
        "symbol":"BTCUSDH23",  
        "coin": null,  
        "mode": 0  
    }  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.switch_position_mode(  
        category="inverse",  
        symbol="BTCUSDH23",  
        mode=0,  
    ))  
    
    
    
    import com.bybit.api.client.domain.*;  
    import com.bybit.api.client.domain.position.*;  
    import com.bybit.api.client.domain.position.request.*;  
    import com.bybit.api.client.service.BybitApiClientFactory;  
    var client = BybitApiClientFactory.newInstance().newPositionRestClient();  
    var switchPositionMode = PositionDataRequest.builder().category(CategoryType.LINEAR).symbol("BTCUSDT").positionMode(PositionMode.BOTH_SIDES).build();  
    System.out.println(client.switchPositionMode(switchPositionMode));  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
        testnet: true,  
        key: 'xxxxxxxxxxxxxxxxxx',  
        secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
        .switchPositionMode({  
            category: 'inverse',  
            symbol: 'BTCUSDH23',  
            mode: 0,  
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
        "result": {},  
        "retExtInfo": {},  
        "time": 1675249072814  
    }  
    

[PreviousSet Leverage](https://bybit-exchange.github.io/docs/v5/position/leverage)[NextSet Trading Stop](https://bybit-exchange.github.io/docs/v5/position/trading-stop)

  * Example
  * The position-switch ability for each contract
  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


