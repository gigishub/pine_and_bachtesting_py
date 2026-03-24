# Get Risk Limit

> **Source:** https://bybit-exchange.github.io/docs/v5/market/risk-limit

---

  * [](https://bybit-exchange.github.io/docs/)
  * Market
  * Get Risk Limit



On this page

# Get Risk Limit

Query for the [risk limit](https://www.bybit.com/en/help-center/article/Risk-Limit-Perpetual-and-Futures) margin parameters. This information is also displayed on the website [here](https://www.bybit.com/en/announcement-info/margin-parameters/).

> **Covers: USDT contract / USDC contract / Inverse contract**

info

  * category=`linear` returns a data set of 15 symbols in each response. Please use the `cursor` param to get the next data set.
  * `symbol` support `Trading` status and `PreLaunch` [Pre-Market contracts](https://www.bybit.com/en/help-center/article/Introduction-to-Pre-Market-Perpetual) status trading pairs.
  * During periods of extreme market volatility, this interface may experience increased latency or temporary delays in data delivery



### HTTP Request​

GET`/v5/market/risk-limit`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
[category](https://bybit-exchange.github.io/docs/v5/enum#category)| **true**|  string| Product type. `linear`,`inverse`  
symbol| false| string| Symbol name, like `BTCUSDT`, uppercase only  
cursor| false| string| Cursor. Use the `nextPageCursor` token from the response to retrieve the next page of the data set  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
category| string| Product type  
list| array| Object  
> id| integer| Risk ID  
> symbol| string| Symbol name  
> riskLimitValue| string| Position limit  
> maintenanceMargin| number| Maintain margin rate  
> initialMargin| number| Initial margin rate  
> isLowestRisk| integer| `1`: true, `0`: false  
> maxLeverage| string| Allowed max leverage  
> mmDeduction| string| The maintenance margin deduction value when risk limit tier changed  
nextPageCursor| string| Refer to the `cursor` request parameter  
[RUN >>](https://bybit-exchange.github.io/docs/api-explorer/v5/market/risk-limit)

* * *

### Request Example​

  * HTTP
  * Python
  * GO
  * Java
  * Node.js


    
    
    GET /v5/market/risk-limit?category=inverse&symbol=BTCUSD HTTP/1.1  
    Host: api-testnet.bybit.com  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(testnet=True)  
    print(session.get_risk_limit(  
        category="inverse",  
        symbol="BTCUSD",  
    ))  
    
    
    
    import (  
        "context"  
        "fmt"  
        bybit "github.com/bybit-exchange/bybit.go.api"  
    )  
    client := bybit.NewBybitHttpClient("", "", bybit.WithBaseURL(bybit.TESTNET))  
    params := map[string]interface{}{"category": "linear", "symbol": "BTCUSDT"}  
    client.NewUtaBybitServiceWithParams(params).GetMarketRiskLimits(context.Background())  
    
    
    
    import com.bybit.api.client.domain.CategoryType;  
    import com.bybit.api.client.domain.market.request.MarketDataRequest;  
    import com.bybit.api.client.service.BybitApiClientFactory;  
    var client = BybitApiClientFactory.newInstance().newAsyncMarketDataRestClient();  
    var riskMimitRequest = MarketDataRequest.builder().category(CategoryType.INVERSE).symbol("ADAUSD").build();  
    client.getRiskLimit(riskMimitRequest, System.out::println);  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
        testnet: true,  
    });  
      
    client  
        .getRiskLimit({  
            category: 'inverse',  
            symbol: 'BTCUSD',  
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
            "category": "inverse",  
            "list": [  
                {  
                    "id": 1,  
                    "symbol": "BTCUSD",  
                    "riskLimitValue": "150",  
                    "maintenanceMargin": "0.5",  
                    "initialMargin": "1",  
                    "isLowestRisk": 1,  
                    "maxLeverage": "100.00",  
                    "mmDeduction": ""  
                },  
            ....  
            ]  
        },  
        "retExtInfo": {},  
        "time": 1672054488010  
    }  
    

[PreviousGet Insurance Pool](https://bybit-exchange.github.io/docs/v5/market/insurance)[NextGet Delivery Price](https://bybit-exchange.github.io/docs/v5/market/delivery-price)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


