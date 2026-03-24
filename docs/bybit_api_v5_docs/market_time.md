# Get Bybit Server Time

> **Source:** https://bybit-exchange.github.io/docs/v5/market/time

---

  * [](https://bybit-exchange.github.io/docs/)
  * Market
  * Get Bybit Server Time



On this page

# Get Bybit Server Time

info

  * During periods of extreme market volatility, this interface may experience increased latency or temporary delays in data delivery



### HTTP Request​

GET`/v5/market/time`Copy

### Request Parameters​

None

### Response Parameters​

Parameter| Type| Comments  
---|---|---  
timeSecond| string| Bybit server timestamp (sec)  
timeNano| string| Bybit server timestamp (nano)  
[RUN >>](https://bybit-exchange.github.io/docs/api-explorer/v5/market/time)

* * *

### Request Example​

  * HTTP
  * Python
  * Java
  * Go
  * Node.js


    
    
    GET /v5/market/time HTTP/1.1  
    Host: api.bybit.com  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(testnet=True)  
    print(session.get_server_time())  
    
    
    
    import com.bybit.api.client.service.BybitApiClientFactory;  
    var client = BybitApiClientFactory.newInstance().newAsyncMarketDataRestClient();  
    client.getServerTime(System.out::println);  
    
    
    
    import (  
        "context"  
        "fmt"  
        bybit "github.com/bybit-exchange/bybit.go.api"  
    )  
    client := bybit.NewBybitHttpClient("", "", bybit.WithBaseURL(bybit.TESTNET))  
    client.NewUtaBybitServiceNoParams().GetServerTime(context.Background())  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
    });  
      
    client  
      .getServerTime()  
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
            "timeSecond": "1688639403",  
            "timeNano": "1688639403423213947"  
        },  
        "retExtInfo": {},  
        "time": 1688639403423  
    }  
    

[PreviousGet System Status](https://bybit-exchange.github.io/docs/v5/system-status)[NextGet Kline](https://bybit-exchange.github.io/docs/v5/market/kline)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


