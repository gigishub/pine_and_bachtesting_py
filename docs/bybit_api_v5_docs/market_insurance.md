# Get Insurance Pool

> **Source:** https://bybit-exchange.github.io/docs/v5/market/insurance

---

  * [](https://bybit-exchange.github.io/docs/)
  * Market
  * Get Insurance Pool



On this page

# Get Insurance Pool

Query for Bybit [insurance pool](https://www.bybit.com/en/announcement-info/insurance-fund/) data (BTC/USDT/USDC etc)

info

  * The isolated insurance pool balance is updated every 1 minute, and shared insurance pool balance is updated every 24 hours
  * Please note that you may receive data from the previous minute. This is due to multiple backend containers starting at different times, which may cause a slight delay. You can always rely on the latest minute data for accuracy.
  * During periods of extreme market volatility, this interface may experience increased latency or temporary delays in data delivery



### HTTP Request​

GET`/v5/market/insurance`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
coin| false| string| coin, uppercase only. Default: return all insurance coins  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
updatedTime| string| Data updated time (ms)  
list| array| Object  
> coin| string| Coin  
> symbols| string| 

  * symbols with `"BTCUSDT,ETHUSDT,SOLUSDT"` mean these contracts are shared with one insurance pool
  * For an isolated insurance pool, it returns one contract

  
> balance| string| Balance  
> value| string| USD value  
[RUN >>](https://bybit-exchange.github.io/docs/api-explorer/v5/market/insurance)

* * *

### Request Example​

  * HTTP
  * Python
  * GO
  * Java
  * Node.js


    
    
    GET /v5/market/insurance?coin=USDT HTTP/1.1  
    Host: api-testnet.bybit.com  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(testnet=True)  
    print(session.get_insurance(  
        coin="USDT",  
    ))  
    
    
    
    import (  
        "context"  
        "fmt"  
        bybit "github.com/bybit-exchange/bybit.go.api"  
    )  
    client := bybit.NewBybitHttpClient("", "", bybit.WithBaseURL(bybit.TESTNET))  
    params := map[string]interface{}{"category": "linear", "symbol": "BTCUSDT"}  
    client.NewUtaBybitServiceWithParams(params).GetMarketInsurance(context.Background())  
    
    
    
    import com.bybit.api.client.domain.market.request.MarketDataRequest;  
    import com.bybit.api.client.service.BybitApiClientFactory;  
    var client = BybitApiClientFactory.newInstance().newAsyncMarketDataRestClient();  
    var insuranceRequest = MarketDataRequest.builder().coin("BTC").build();  
    var insuranceData = client.getInsurance(insuranceRequest);  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
        testnet: true,  
    });  
      
    client  
        .getInsurance({  
            coin: 'USDT',  
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
            "updatedTime": "1714003200000",  
            "list": [  
                {  
                    "coin": "USDT",  
                    "symbols": "MERLUSDT,10000000AIDOGEUSDT,ZEUSUSDT",  
                    "balance": "902178.57602476",  
                    "value": "901898.0963091522"  
                },  
                {  
                    "coin": "USDT",  
                    "symbols": "SOLUSDT,OMNIUSDT,ALGOUSDT",  
                    "balance": "14454.51626125",  
                    "value": "14449.515598975464"  
                },  
                {  
                    "coin": "USDT",  
                    "symbols": "XLMUSDT,WUSDT",  
                    "balance": "23.45018235",  
                    "value": "22.992864174376344"  
                },  
                {  
                    "coin": "USDT",  
                    "symbols": "AGIUSDT,WIFUSDT",  
                    "balance": "10002",  
                    "value": "9998.896846613574"  
                }  
            ]  
        },  
        "retExtInfo": {},  
        "time": 1714028451228  
    }  
    

[PreviousGet Historical Volatility](https://bybit-exchange.github.io/docs/v5/market/iv)[NextGet Risk Limit](https://bybit-exchange.github.io/docs/v5/market/risk-limit)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


