# Set Risk Limit

> **Source:** https://bybit-exchange.github.io/docs/v5/abandon/set-risk-limit

---

  * [](https://bybit-exchange.github.io/docs/)
  * Abandoned Endpoints
  * Set Risk Limit



On this page

# Set Risk Limit

**Since bybit has launched auto risk limit on 12 March 2024, please click[here](https://announcements.bybit.com/en/article/risk-limit-update-transitioning-from-manual-to-auto-adjustment-bltf0fa535064561d9d/) to learn more, so it will not take effect even you set it successfully.**

### HTTP Request​

POST`/v5/position/set-risk-limit`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
[category](https://bybit-exchange.github.io/docs/v5/enum#category)| **true**|  string| Product type 

  * Unified account: `linear`, `inverse`
  * Classic account: `linear`, `inverse`. _Please note that`category` is **not** involved with business logic_

  
symbol| **true**|  string| Symbol name, like `BTCUSDT`, uppercase only  
riskId| **true**|  integer| Risk limit ID  
[positionIdx](https://bybit-exchange.github.io/docs/v5/enum#positionidx)| false| integer| Used to identify positions in different position modes. For hedge mode, it is **required**

  * `0`: one-way mode
  * `1`: hedge-mode Buy side
  * `2`: hedge-mode Sell side

  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
category| string| Product type  
riskId| integer| Risk limit ID  
riskLimitValue| string| The position limit value corresponding to this risk ID  
[RUN >>](https://bybit-exchange.github.io/docs/api-explorer/v5/position/set-risk-limit)

* * *

### Request Example​

  * HTTP
  * Python
  * Java
  * Node.js


    
    
    POST /v5/position/set-risk-limit HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1672282269774  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
      
    {  
        "category": "linear",  
        "symbol": "BTCUSDT",  
        "riskId": 4,  
        "positionIdx": null  
    }  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.set_risk_limit(  
        category="linear",  
        symbol="BTCUSDT",  
        riskId=4,  
    ))  
    
    
    
    import com.bybit.api.client.domain.*;  
    import com.bybit.api.client.domain.position.*;  
    import com.bybit.api.client.domain.position.request.*;  
    import com.bybit.api.client.service.BybitApiClientFactory;  
    var client = BybitApiClientFactory.newInstance().newAsyncPositionRestClient();  
    var setRiskLimitRequest = PositionDataRequest.builder().category(CategoryType.LINEAR).symbol("BTCUSDT").riskId(4).build();  
    client.setRiskLimit(setRiskLimitRequest, System.out::println);  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
        testnet: true,  
        key: 'xxxxxxxxxxxxxxxxxx',  
        secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
        .setRiskLimit({  
            category: 'linear',  
            symbol: 'BTCUSDT',  
            riskId: 4,  
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
            "riskId": 4,  
            "riskLimitValue": "8000000",  
            "category": "linear"  
        },  
        "retExtInfo": {},  
        "time": 1672282270571  
    }  
    

[PreviousSwitch Cross/Isolated Margin](https://bybit-exchange.github.io/docs/v5/abandon/cross-isolate)[NextGet Transaction Log (Classic)](https://bybit-exchange.github.io/docs/v5/abandon/contract-transaction-log)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


