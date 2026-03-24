# Get Borrow Quota (Spot)

> **Source:** https://bybit-exchange.github.io/docs/v5/order/spot-borrow-quota

---

  * [](https://bybit-exchange.github.io/docs/)
  * Trade
  * Get Borrow Quota (Spot)



On this page

# Get Borrow Quota (Spot)

Query the available balance for Spot trading and Margin trading

info

  * During periods of extreme market volatility, this interface may experience increased latency or temporary delays in data delivery



### HTTP Request​

GET`/v5/order/spot-borrow-check`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
[category](https://bybit-exchange.github.io/docs/v5/enum#category)| **true**|  string| Product type `spot`  
symbol| **true**|  string| Symbol name  
side| **true**|  string| Transaction side. `Buy`,`Sell`  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
symbol| string| Symbol name, like `BTCUSDT`, uppercase only  
side| string| Side  
maxTradeQty| string| The maximum base coin qty can be traded

  * If spot margin trade on and symbol is margin trading pair, it returns available balance + max.borrowable quantity = min(The maximum quantity that a single user can borrow on the platform, The maximum quantity that can be borrowed calculated by IMR MMR of UTA account, The available quantity of the platform's capital pool) 
  * Otherwise, it returns actual available balance
  * up to 4 decimals

  
maxTradeAmount| string| The maximum quote coin amount can be traded

  * If spot margin trade on and symbol is margin trading pair, it returns available balance + max.borrowable amount = min(The maximum amount that a single user can borrow on the platform, The maximum amount that can be borrowed calculated by IMR MMR of UTA account, The available amount of the platform's capital pool) 
  * Otherwise, it returns actual available balance
  * up to 8 decimals

  
spotMaxTradeQty| string| No matter your Spot margin switch on or not, it always returns actual qty of base coin you can trade or you have (borrowable qty is not included), up to 4 decimals  
spotMaxTradeAmount| string| No matter your Spot margin switch on or not, it always returns actual amount of quote coin you can trade or you have (borrowable amount is not included), up to 8 decimals  
borrowCoin| string| Borrow coin  
[RUN >>](https://bybit-exchange.github.io/docs/api-explorer/v5/trade/query-spot-quota)

* * *

### Request Example​

  * HTTP
  * Python
  * Java
  * Node.js


    
    
    GET /v5/order/spot-borrow-check?category=spot&symbol=BTCUSDT&side=Buy HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1672228522214  
    X-BAPI-RECV-WINDOW: 5000  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.get_borrow_quota(  
        category="spot",  
        symbol="BTCUSDT",  
        side="Buy",  
    ))  
    
    
    
    import com.bybit.api.client.config.BybitApiConfig;  
    import com.bybit.api.client.domain.trade.request.TradeOrderRequest;  
    import com.bybit.api.client.domain.*;  
    import com.bybit.api.client.domain.trade.*;  
    import com.bybit.api.client.service.BybitApiClientFactory;  
    var client = BybitApiClientFactory.newInstance("YOUR_API_KEY", "YOUR_API_SECRET", BybitApiConfig.TESTNET_DOMAIN).newTradeRestClient();  
    var getBorrowQuotaRequest = TradeOrderRequest.builder().category(CategoryType.SPOT).symbol("BTCUSDT").side(Side.BUY).build();  
    System.out.println(client.getBorrowQuota(getBorrowQuotaRequest));  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
        testnet: true,  
        key: 'xxxxxxxxxxxxxxxxxx',  
        secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
        .getSpotBorrowCheck('BTCUSDT', 'Buy')  
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
            "symbol": "BTCUSDT",  
            "maxTradeQty": "6.6065",  
            "side": "Buy",  
            "spotMaxTradeAmount": "9004.75628594",  
            "maxTradeAmount": "218014.01330797",  
            "borrowCoin": "USDT",  
            "spotMaxTradeQty": "0.2728"  
        },  
        "retExtInfo": {},  
        "time": 1698895841534  
    }  
    

[PreviousBatch Cancel Order](https://bybit-exchange.github.io/docs/v5/order/batch-cancel)[NextSet DCP](https://bybit-exchange.github.io/docs/v5/order/dcp)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


