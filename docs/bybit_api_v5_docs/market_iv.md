# Get Historical Volatility

> **Source:** https://bybit-exchange.github.io/docs/v5/market/iv

---

  * [](https://bybit-exchange.github.io/docs/)
  * Market
  * Get Historical Volatility



On this page

# Get Historical Volatility

Query option historical volatility

> **Covers: Option**

info

  * The data is hourly.
  * If both `startTime` and `endTime` are not specified, it will return the most recent 1 hours worth of data.
  * `startTime` and `endTime` are a pair of params. Either both are passed or they are not passed at all.
  * This endpoint can query the last 2 years worth of data, but make sure [`endTime` \- `startTime`] <= 30 days.



### HTTP Request​

GET`/v5/market/historical-volatility`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
category| **true**|  string| Product type. `option`  
baseCoin| false| string| Base coin, uppercase only. Default: return BTC data  
quoteCoin| false| string| Quote coin, `USD` or `USDT`. Default: return quoteCoin=USD  
[period](https://bybit-exchange.github.io/docs/v5/enum#optionperiod)| false| integer| Period. If not specified, it will return data with a 7-day average by default  
startTime| false| integer| The start timestamp (ms)  
endTime| false| integer| The end timestamp (ms)  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
category| string| Product type  
list| array| Object  
> period| integer| Period  
> value| string| Volatility  
> time| string| Timestamp (ms)  
[RUN >>](https://bybit-exchange.github.io/docs/api-explorer/v5/market/iv)

* * *

### Request Example​

  * HTTP
  * Python
  * Java
  * Node.js


    
    
    GET /v5/market/historical-volatility?category=option&baseCoin=ETH&period=30 HTTP/1.1  
    Host: api-testnet.bybit.com  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(testnet=True)  
    print(session.get_historical_volatility(  
        category="option",  
        baseCoin="ETH",  
        period=30,  
    ))  
    
    
    
    import com.bybit.api.client.domain.CategoryType;  
    import com.bybit.api.client.domain.market.*;  
    import com.bybit.api.client.domain.market.request.MarketDataRequest;  
    import com.bybit.api.client.service.BybitApiClientFactory;  
    var client = BybitApiClientFactory.newInstance().newAsyncMarketDataRestClient();  
    var historicalVolatilityRequest = MarketDataRequest.builder().category(CategoryType.OPTION).optionPeriod(7).build();  
    client.getHistoricalVolatility(historicalVolatilityRequest, System.out::println);  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
        testnet: true,  
    });  
      
    client  
        .getHistoricalVolatility({  
            category: 'option',  
            baseCoin: 'ETH',  
            period: 30,  
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
        "retMsg": "SUCCESS",  
        "category": "option",  
        "result": [  
            {  
                "period": 30,  
                "value": "0.45024716",  
                "time": "1672052400000"  
            }  
        ]  
    }  
    

[PreviousGet Open Interest](https://bybit-exchange.github.io/docs/v5/market/open-interest)[NextGet Insurance Pool](https://bybit-exchange.github.io/docs/v5/market/insurance)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


