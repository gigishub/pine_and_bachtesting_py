# Set TP/SL Mode

> **Source:** https://bybit-exchange.github.io/docs/v5/abandon/tpsl-mode

---

  * [](https://bybit-exchange.github.io/docs/)
  * Abandoned Endpoints
  * Set TP/SL Mode (deprecated)



On this page

# Set TP/SL Mode

tip

 _To some extent, this endpoint is**deprecated** because now tpsl is based on order level. This API was used for position level change before._

_However, you still can use it to set an implicit tpsl mode for a certain symbol because when you don't pass "tpslMode" in the place order or trading stop request, system will get the tpslMode by the default setting._

Set TP/SL mode to Full or Partial

info

For partial TP/SL mode, you can set the TP/SL size smaller than position size.

### HTTP Request​

POST`/v5/position/set-tpsl-mode`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
[category](https://bybit-exchange.github.io/docs/v5/enum#category)| **true**|  string| Product type `linear`, `inverse`  
symbol| **true**|  string| Symbol name, like `BTCUSDT`, uppercase only  
tpSlMode| **true**|  string| TP/SL mode. `Full`,`Partial`  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
tpSlMode| string| `Full`,`Partial`  
[RUN >>](https://bybit-exchange.github.io/docs/api-explorer/v5/position/tpsl-mode)

* * *

### Request Example​

  * HTTP
  * Python
  * Java
  * Node.js


    
    
    POST /v5/position/set-tpsl-mode HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1672279325035  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
      
    {  
        "symbol": "XRPUSDT",  
        "category": "linear",  
        "tpSlMode": "Full"  
    }  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.set_tp_sl_mode(  
        symbol="XRPUSDT",  
        category="linear",  
        tpSlMode="Full",  
    ))  
    
    
    
    import com.bybit.api.client.domain.*;  
    import com.bybit.api.client.domain.position.*;  
    import com.bybit.api.client.domain.position.request.*;  
    import com.bybit.api.client.service.BybitApiClientFactory;  
    var client = BybitApiClientFactory.newInstance().newAsyncPositionRestClient();  
    var setTpSlRequest = PositionDataRequest.builder().category(CategoryType.LINEAR).symbol("BTCUSDT").tpslMode(TpslMode.PARTIAL).build();  
    client.swithMarginRequest(setTpSlRequest, System.out::println);  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
        testnet: true,  
        key: 'xxxxxxxxxxxxxxxxxx',  
        secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
        .setTPSLMode({  
            symbol: 'XRPUSDT',  
            category: 'linear',  
            tpSlMode: 'Full',  
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
            "tpSlMode": "Full"  
        },  
        "retExtInfo": {},  
        "time": 1672279322666  
    }  
    

[PreviousGet Transaction Log (Classic)](https://bybit-exchange.github.io/docs/v5/abandon/contract-transaction-log)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


