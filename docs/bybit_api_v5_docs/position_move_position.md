# Move Position

> **Source:** https://bybit-exchange.github.io/docs/v5/position/move-position

---

  * [](https://bybit-exchange.github.io/docs/)
  * Position
  * Move Position



On this page

# Move Position

You can move positions between sub-master, master-sub, or sub-sub UIDs when necessary

info

  * The endpoint can only be called by master UID api key
  * UIDs must be the same master-sub account relationship
  * The trades generated from move-position endpoint will not be displayed in the Recent Trade (Rest API & Websocket)
  * There is no trading fee
  * `fromUid` and `toUid` both should be Unified trading accounts, and they need to be one-way mode when moving the positions
  * Please note that once executed, you will get execType=`MovePosition` entry from [Get Trade History](https://bybit-exchange.github.io/docs/v5/order/execution), [Get Closed Pnl](https://bybit-exchange.github.io/docs/v5/position/close-pnl), and stream from [Execution](https://bybit-exchange.github.io/docs/v5/websocket/private/execution).



### HTTP Request​

POST`/v5/position/move-positions`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
fromUid| **true**|  string| From UID 

  * Must be UTA
  * Must be in one-way mode for Futures

  
toUid| **true**|  string| To UID 

  * Must be UTA
  * Must be in one-way mode for Futures

  
list| **true**|  array| Object. Up to 25 legs per request  
> [category](https://bybit-exchange.github.io/docs/v5/enum#category)| **true**|  string| Product type `linear`, `spot`, `option`,`inverse`  
> symbol| **true**|  string| Symbol name, like `BTCUSDT`, uppercase only  
> price| **true**|  string| Trade price 

  * `linear`&`inverse`: the price needs to be between [95% of mark price, 105% of mark price]
  * `spot`&`option`: the price needs to follow the price rule from [Instruments Info](https://bybit-exchange.github.io/docs/v5/market/instrument)

  
> side| **true**|  string| Trading side of `fromUid`

  * For example, `fromUid` has a long position, when side=`Sell`, then once executed, the position of `fromUid` will be reduced or open a short position depending on `qty` input

  
> qty| **true**|  string| Executed qty 

  * The value must satisfy the qty rule from [Instruments Info](https://bybit-exchange.github.io/docs/v5/market/instrument), in particular, category=`linear` is able to input `maxOrderQty` * 5

  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
retCode| integer| Result code. `0` means request is successfully accepted  
retMsg| string| Result message  
result| map| Object  
> blockTradeId| string| Block trade ID  
> status| string| Status. `Processing`, `Rejected`  
> rejectParty| string| 

  * `""` means initial validation is passed, please check the order status via [Get Move Position History](https://bybit-exchange.github.io/docs/v5/position/move-position-history)
  * `Taker`, `Maker` when status=`Rejected`
  * `bybit` means error is occurred on the Bybit side

  
  
### Request Example​

  * HTTP
  * Python
  * Java
  * Node.js


    
    
    POST /v5/position/move-positions HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1697447928051  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
      
    {  
        "fromUid": "100307601",  
        "toUid": "592324",  
        "list": [  
            {  
                "category": "spot",  
                "symbol": "BTCUSDT",  
                "price": "100",  
                "side": "Sell",  
                "qty": "0.01"  
            }  
        ]  
    }  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.move_position(  
        fromUid="100307601",  
        toUid="592324",  
        list=[  
            {  
                "category": "spot",  
                "symbol": "BTCUSDT",  
                "price": "100",  
                "side": "Sell",  
                "qty": "0.01",  
            }  
        ]  
    ))  
    
    
    
    import com.bybit.api.client.domain.*;  
    import com.bybit.api.client.domain.position.*;  
    import com.bybit.api.client.domain.position.request.*;  
    import com.bybit.api.client.service.BybitApiClientFactory;  
    var client = BybitApiClientFactory.newInstance().newAsyncPositionRestClient();  
    var movePositionsRequest = Arrays.asList(MovePositionDetailsRequest.builder().category(CategoryType.SPOT.getCategoryTypeId()).symbol("BTCUSDT").side(Side.SELL.getTransactionSide()).price("100").qty("0.01").build(),  
                    MovePositionDetailsRequest.builder().category(CategoryType.SPOT.getCategoryTypeId()).symbol("ETHUSDT").side(Side.SELL.getTransactionSide()).price("100").qty("0.01").build());  
    var batchMovePositionsRequest = BatchMovePositionRequest.builder().fromUid("123456").toUid("456789").list(movePositionsRequest).build();  
    System.out.println(client.batchMovePositions(batchMovePositionsRequest));  
    
    
    
      
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "OK",  
        "result": {  
            "blockTradeId": "e9bb926c95f54cf1ba3e315a58b8597b",  
            "status": "Processing",  
            "rejectParty": ""  
        }  
    }  
    

[PreviousGet Closed Options Positions (6 months)](https://bybit-exchange.github.io/docs/v5/position/close-position)[NextGet Move Position History](https://bybit-exchange.github.io/docs/v5/position/move-position-history)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


