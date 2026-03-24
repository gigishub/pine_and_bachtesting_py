# Cancel All Orders

> **Source:** https://bybit-exchange.github.io/docs/v5/order/cancel-all

---

  * [](https://bybit-exchange.github.io/docs/)
  * Trade
  * Cancel All Orders



On this page

# Cancel All Orders

Cancel all open orders

info

  * Support cancel orders by `symbol`/`baseCoin`/`settleCoin`. If you pass multiple of these params, the system will process one of param, which priority is `symbol` > `baseCoin` > `settleCoin`.
  * **NOTE** : category=_option_ , you can cancel all option open orders without passing any of those three params. However, for "linear" and "inverse", you must specify one of those three params.
  * **NOTE** : category=_spot_ , you can cancel all spot open orders (normal order by default) without passing other params.



info

**Spot** : no limit  
**Futures** : cancel up to 500 orders (System **picks up 500 orders randomly to cancel** when you have over 500 orders)  
**Options** : no limit

### HTTP Request​

POST`/v5/order/cancel-all`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
[category](https://bybit-exchange.github.io/docs/v5/enum#category)| **true**|  string| Product type. `linear`, `inverse`, `spot`, `option`  
symbol| false| string| Symbol name, like `BTCUSDT`, uppercase only  
`linear`&`inverse`: **Required** if not passing baseCoin or settleCoin  
baseCoin| false| string| Base coin, uppercase only. `linear` & `inverse`: If cancel all by baseCoin, it will cancel all of the corresponding category's orders. **Required** if not passing symbol or settleCoin  
settleCoin| false| string| Settle coin, uppercase only 

  * `linear` & `inverse`: **Required** if not passing symbol or baseCoin
  * `option`: USDT or USDC
  * Not support `spot`

  
orderFilter| false| string| 

  * category=`spot`, you can pass `Order`, `tpslOrder`, `StopOrder`, `OcoOrder`, `BidirectionalTpslOrder`  
If not passed, `Order` by default
  * category=`linear` or `inverse`, you can pass `Order`, `StopOrder`,`OpenOrder`  
If not passed, all kinds of orders will be cancelled, like active order, conditional order, TP/SL order and trailing stop order
  * category=`option`, you can pass `Order`,`StopOrder`  
If not passed, all kinds of orders will be cancelled, like active order, conditional order, TP/SL order and trailing stop order

  
[stopOrderType](https://bybit-exchange.github.io/docs/v5/enum#stopordertype)| false| string| Stop order type `Stop`

  * Only used for category=`linear` or `inverse` and orderFilter=`StopOrder`,you can cancel conditional orders except TP/SL order and Trailing stop orders with this param

  
  
info

The acknowledgement of create/amend/cancel order requests indicates that the request was sucessfully accepted. The request is asynchronous so please use the websocket to confirm the order status.

[RUN >>](https://bybit-exchange.github.io/docs/api-explorer/v5/trade/cancel-all)

* * *

### Response Parameters​

Parameter| Type| Comments  
---|---|---  
list| array| Object  
> orderId| string| Order ID  
> orderLinkId| string| User customised order ID  
success| string| "1": success, "0": fail. [UTA1.0](https://bybit-exchange.github.io/docs/v5/acct-mode#uta-10) (inverse) does not return this field  
  
### Request Example​

  * HTTP
  * Python
  * Java
  * .Net
  * Node.js


    
    
    POST /v5/order/cancel-all HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1672219779140  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
      
    {  
      "category": "linear",  
      "symbol": null,  
      "settleCoin": "USDT"  
    }  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.cancel_all_orders(  
        category="linear",  
        settleCoin="USDT",  
    ))  
    
    
    
    import com.bybit.api.client.restApi.BybitApiTradeRestClient;  
    import com.bybit.api.client.domain.*;  
    import com.bybit.api.client.domain.trade.*;  
    import com.bybit.api.client.service.BybitApiClientFactory;  
    BybitApiClientFactory factory = BybitApiClientFactory.newInstance("YOUR_API_KEY", "YOUR_API_SECRET");  
    BybitApiAsyncTradeRestClient client = factory.newAsyncTradeRestClient();  
    var cancelAllOrdersRequest = TradeOrderRequest.builder().category(ProductType.LINEAR).baseCoin("USDT").build();  
    client.cancelAllOrder(cancelAllOrdersRequest, System.out::println);  
    
    
    
    using bybit.net.api.ApiServiceImp;  
    using bybit.net.api.Models.Trade;  
    BybitTradeService tradeService = new(apiKey: "xxxxxxxxxxxxxx", apiSecret: "xxxxxxxxxxxxxxxxxxxxx");  
    var orderInfoString = await TradeService.CancelAllOrder(category: Category.LINEAR, baseCoin:"USDT");  
    Console.WriteLine(orderInfoString);  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
        testnet: true,  
        key: 'xxxxxxxxxxxxxxxxxx',  
        secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
        .cancelAllOrders({  
        category: 'linear',  
        settleCoin: 'USDT',  
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
            "list": [  
                {  
                    "orderId": "1616024329462743808",  
                    "orderLinkId": "1616024329462743809"  
                },  
                {  
                    "orderId": "1616024287544869632",  
                    "orderLinkId": "1616024287544869633"  
                }  
            ],  
            "success": "1"  
        },  
        "retExtInfo": {},  
        "time": 1707381118116  
    }  
    

[PreviousGet Open & Closed Orders](https://bybit-exchange.github.io/docs/v5/order/open-order)[NextGet Order History (2 years)](https://bybit-exchange.github.io/docs/v5/order/order-list)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


