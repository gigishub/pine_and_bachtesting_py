# Fast Execution

> **Source:** https://bybit-exchange.github.io/docs/v5/websocket/private/fast-execution

---

  * [](https://bybit-exchange.github.io/docs/)
  * WebSocket Stream
  * Private
  * Fast Execution



On this page

# Fast Execution

Fast execution stream significantly reduces data latency compared original "execution" stream. However, it pushes limited execution type of trades, and fewer data fields.

**All-In-One Topic:** `execution.fast`  
**Categorised Topic:** `execution.fast.linear`, `execution.fast.inverse`, `execution.fast.spot`, `execution.fast.option`  


info

  * Supports all Perps, Futures, Spot and Options exceution
  * You can only receive [execType](https://bybit-exchange.github.io/docs/v5/enum#exectype)=Trade update



### Response Parameters​

Parameter| Type| Comments  
---|---|---  
topic| string| Topic name  
creationTime| number| Data created timestamp (ms)  
data| array| Object  
> [category](https://bybit-exchange.github.io/docs/v5/enum#category)| string| Product type `linear`, `inverse`, `spot`, `option`  
> symbol| string| Symbol name  
> orderId| string| Order ID  
> isMaker| boolean| `true`: Maker, `false`: Taker  
> orderLinkId| string| User customized order ID 

  * maker trade is always `""`
  * If a maker order in the orderbook is converted to taker (by price amend), orderLinkId is also `""`
  * For option: maker trade is always `""`, taker trade is always orderLinkId

  
> execId| string| Execution ID  
> execPrice| string| Execution price  
> execQty| string| Execution qty  
> side| string| Side. `Buy`,`Sell`  
> execTime| string| Executed timestamp (ms)  
> seq| long| Cross sequence, used to associate each fill and each position update

  * The seq will be the same when conclude multiple transactions at the same time
  * Different symbols may have the same seq, please use seq + symbol to check unique

  
  
### Subscribe Example​
    
    
    {  
        "op": "subscribe",  
        "args": [  
            "execution.fast"  
        ]  
    }  
    

### Stream Example​
    
    
    {  
        "topic": "execution.fast",  
        "creationTime": 1716800399338,  
        "data": [  
            {  
                "category": "linear",  
                "symbol": "ICPUSDT",  
                "execId": "3510f361-0add-5c7b-a2e7-9679810944fc",  
                "execPrice": "12.015",  
                "execQty": "3000",  
                "orderId": "443d63fa-b4c3-4297-b7b1-23bca88b04dc",  
                "isMaker": false,  
                "orderLinkId": "test-00001",  
                "side": "Sell",  
                "execTime": "1716800399334",  
                "seq": 34771365464  
            }  
        ]  
    }  
    

[PreviousExecution](https://bybit-exchange.github.io/docs/v5/websocket/private/execution)[NextOrder](https://bybit-exchange.github.io/docs/v5/websocket/private/order)

  * Response Parameters
  * Subscribe Example
  * Stream Example


