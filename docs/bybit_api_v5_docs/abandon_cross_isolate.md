# Switch Cross/Isolated Margin

> **Source:** https://bybit-exchange.github.io/docs/v5/abandon/cross-isolate

---

  * [](https://bybit-exchange.github.io/docs/)
  * Abandoned Endpoints
  * Switch Cross/Isolated Margin



On this page

# Switch Cross/Isolated Margin

Select cross margin mode or isolated margin mode per symbol level

### HTTP Request​

POST`/v5/position/switch-isolated`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
[category](https://bybit-exchange.github.io/docs/v5/enum#category)| **true**|  string| Product type 

  * [UTA2.0](https://bybit-exchange.github.io/docs/v5/acct-mode#uta-20): not supported
  * [UTA1.0](https://bybit-exchange.github.io/docs/v5/acct-mode#uta-10): `inverse`
  * Classic: `linear`(USDT Preps), `inverse`

  
symbol| **true**|  string| Symbol name, like `BTCUSDT`, uppercase only  
tradeMode| **true**|  integer| `0`: cross margin. `1`: isolated margin  
buyLeverage| **true**|  string| The value must be equal to `sellLeverage` value  
sellLeverage| **true**|  string| The value must be equal to `buyLeverage` value  
[RUN >>](https://bybit-exchange.github.io/docs/api-explorer/v5/position/cross-isolate)

* * *

### Response Parameters​

None

### Request Example​

  * HTTP
  * Python
  * Java
  * Node.js


    
    
    POST /v5/position/switch-isolated HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN-TYPE: 2  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1675248447965  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    Content-Length: 121  
      
    {  
        "category": "linear",  
        "symbol": "ETHUSDT",  
        "tradeMode": 1,  
        "buyLeverage": "10",  
        "sellLeverage": "10"  
    }  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.switch_margin_mode(  
        category="linear",  
        symbol="ETHUSDT",  
        tradeMode=1,  
        buyLeverage="10",  
        sellLeverage="10",  
    ))  
    
    
    
    import com.bybit.api.client.domain.*;  
    import com.bybit.api.client.domain.position.*;  
    import com.bybit.api.client.domain.position.request.*;  
    import com.bybit.api.client.service.BybitApiClientFactory;  
    var client = BybitApiClientFactory.newInstance().newAsyncPositionRestClient();  
    var switchMarginRequest = PositionDataRequest.builder().category(CategoryType.LINEAR).symbol("BTC-31MAR23").tradeMode(MarginMode.CROSS_MARGIN).buyLeverage("5").sellLeverage("5").build();  
    client.swithMarginRequest(switchMarginRequest, System.out::println);  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
        testnet: true,  
        key: 'xxxxxxxxxxxxxxxxxx',  
        secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
        .switchIsolatedMargin({  
            category: 'linear',  
            symbol: 'ETHUSDT',  
            tradeMode: 1,  
            buyLeverage: '10',  
            sellLeverage: '10',  
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
        "time": 1675248433635  
    }  
    

[PreviousGet Lending Account Info](https://bybit-exchange.github.io/docs/v5/abandon/account-info)[NextSet Risk Limit](https://bybit-exchange.github.io/docs/v5/abandon/set-risk-limit)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


