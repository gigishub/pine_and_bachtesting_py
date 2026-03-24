# Set Auto Add Margin

> **Source:** https://bybit-exchange.github.io/docs/v5/position/auto-add-margin

---

  * [](https://bybit-exchange.github.io/docs/)
  * Position
  * Set Auto Add Margin



On this page

# Set Auto Add Margin

Turn on/off auto-add-margin for **isolated** margin position

### HTTP Request​

POST`/v5/position/set-auto-add-margin`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
[category](https://bybit-exchange.github.io/docs/v5/enum#category)| **true**|  string| Product type `linear` (USDT Contract, USDC Contract)  
symbol| **true**|  string| Symbol name, like `BTCUSDT`, uppercase only  
autoAddMargin| **true**|  integer| Turn on/off. `0`: off. `1`: on  
[positionIdx](https://bybit-exchange.github.io/docs/v5/enum#positionidx)| false| integer| Used to identify positions in different position modes. For hedge mode position, this param is **required**

  * `0`: one-way mode
  * `1`: hedge-mode Buy side
  * `2`: hedge-mode Sell side

  
  
### Response Parameters​

None

[RUN >>](https://bybit-exchange.github.io/docs/api-explorer/v5/position/auto-add-margin)

* * *

### Request Example​

  * HTTP
  * Python
  * Java
  * Node.js


    
    
    POST /v5/position/set-auto-add-margin HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN-TYPE: 2  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1675255134857  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
      
    {  
        "category": "linear",  
        "symbol": "BTCUSDT",  
        "autoAddmargin": 1,  
        "positionIdx": null  
    }  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.set_auto_add_margin(  
        category="linear",  
        symbol="BTCUSDT",  
        autoAddmargin=1,  
    ))  
    
    
    
    import com.bybit.api.client.domain.*;  
    import com.bybit.api.client.domain.position.*;  
    import com.bybit.api.client.domain.position.request.*;  
    import com.bybit.api.client.service.BybitApiClientFactory;  
    var client = BybitApiClientFactory.newInstance().newAsyncPositionRestClient();  
    var setAutoAddMarginRequest = PositionDataRequest.builder().category(CategoryType.LINEAR).symbol("BTCUSDT").autoAddMargin(AutoAddMargin.ON).build();  
    client.setAutoAddMargin(setAutoAddMarginRequest, System.out::println);  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
        testnet: true,  
        key: 'xxxxxxxxxxxxxxxxxx',  
        secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
        .setAutoAddMargin({  
            category: 'linear',  
            symbol: 'BTCUSDT',  
            autoAddMargin: 1,  
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
        "time": 1675255135069  
    }  
    

[PreviousSet Trading Stop](https://bybit-exchange.github.io/docs/v5/position/trading-stop)[NextAdd Or Reduce Margin](https://bybit-exchange.github.io/docs/v5/position/manual-add-margin)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


