# Get Move Position History

> **Source:** https://bybit-exchange.github.io/docs/v5/position/move-position-history

---

  * [](https://bybit-exchange.github.io/docs/)
  * Position
  * Get Move Position History



On this page

# Get Move Position History

You can query moved position data by master UID api key

### HTTP Request​

GET`/v5/position/move-history`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
[category](https://bybit-exchange.github.io/docs/v5/enum#category)| false| string| Product type `linear`, `inverse`, `spot`, `option`  
symbol| false| string| Symbol name, like `BTCUSDT`, uppercase only  
startTime| false| number| The order creation start timestamp. The interval is 7 days  
endTime| false| number| The order creation end timestamp. The interval is 7 days  
status| false| string| Order status. `Processing`, `Filled`, `Rejected`  
blockTradeId| false| string| Block trade ID  
limit| false| string| Limit for data size per page. [`1`, `200`]. Default: `20`  
cursor| false| string| Cursor. Use the `nextPageCursor` token from the response to retrieve the next page of the result set  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
list| array| Object  
> blockTradeId| string| Block trade ID  
> [category](https://bybit-exchange.github.io/docs/v5/enum#category)| string| Product type. `linear`, `spot`, `option`  
> orderId| string| Bybit order ID  
> userId| integer| User ID  
> symbol| string| Symbol name  
> side| string| Order side from taker's perspective. `Buy`, `Sell`  
> price| string| Order price  
> qty| string| Order quantity  
> execFee| string| The fee for taker or maker in the base currency paid to the Exchange executing the block trade  
> status| string| Block trade status. `Processing`, `Filled`, `Rejected`  
> execId| string| The unique trade ID from the exchange  
> resultCode| integer| The result code of the order. `0` means success  
> resultMessage| string| The error message. `""` when resultCode=0  
> createdAt| number| The timestamp (ms) when the order is created  
> updatedAt| number| The timestamp (ms) when the order is updated  
> rejectParty| string| 

  * `""` means the status=`Filled`
  * `Taker`, `Maker` when status=`Rejected`
  * `bybit` means error is occurred on the Bybit side

  
nextPageCursor| string| Used to get the next page data  
  
### Request Example​

  * HTTP
  * Python
  * Java
  * Node.js


    
    
    GET /v5/position/move-history?limit=1&status=Filled HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1697523024244  
    X-BAPI-RECV-WINDOW: 5000  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.get_move_position_history(  
        limit="1",  
        status="Filled",  
    ))  
    
    
    
    import com.bybit.api.client.domain.*;  
    import com.bybit.api.client.domain.position.*;  
    import com.bybit.api.client.domain.position.request.*;  
    import com.bybit.api.client.service.BybitApiClientFactory;  
    var client = BybitApiClientFactory.newInstance().newAsyncPositionRestClient();  
    var movePositionsHistoryRequest = PositionDataRequest.builder().category(CategoryType.LINEAR).symbol("BTCUSDT").status(MovePositionStatus.Processing).build();  
    System.out.println(client.getMovePositionHistory(movePositionsHistoryRequest));  
    
    
    
      
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "OK",  
        "result": {  
            "list": [  
                {  
                    "blockTradeId": "1a82e5801af74b67b7ad71ba00a7391a",  
                    "category": "option",  
                    "orderId": "8e09c5b8-f651-4cec-968d-52764cac11ec",  
                    "userId": 592324,  
                    "symbol": "BTC-14OCT23-27000-C",  
                    "side": "Buy",  
                    "price": "6",  
                    "qty": "0.99",  
                    "execFee": "0",  
                    "status": "Filled",  
                    "execId": "677ad344-6bb4-4ace-baca-128fcffcaca7",  
                    "resultCode": 0,  
                    "resultMessage": "",  
                    "createdAt": 1697186522865,  
                    "updatedAt": 1697186523289,  
                    "rejectParty": ""  
                }  
            ],  
            "nextPageCursor": "page_token%3D1241742%26"  
        },  
        "retExtInfo": {},  
        "time": 1697523024386  
    }  
    

[PreviousMove Position](https://bybit-exchange.github.io/docs/v5/position/move-position)[NextConfirm New Risk Limit](https://bybit-exchange.github.io/docs/v5/position/confirm-mmr)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


