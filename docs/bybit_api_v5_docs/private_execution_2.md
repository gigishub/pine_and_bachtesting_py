# Execution

> **Source:** https://bybit-exchange.github.io/docs/v5/websocket/private/execution

---

  * [](https://bybit-exchange.github.io/docs/)
  * WebSocket Stream
  * Private
  * Execution



On this page

# Execution

Subscribe to the execution stream to see your executions in **real-time**.

tip

You may have multiple executions for one order in a single message.

**All-In-One Topic:** `execution`  
**Categorised Topic:** `execution.spot`, `execution.linear`, `execution.inverse`, `execution.option`

info

  * All-In-One topic and Categorised topic **cannot** be in the same subscription request
  * All-In-One topic: Allow you to listen to all categories (spot, linear, inverse, option) websocket updates
  * Categorised Topic: Allow you to listen only to specific category websocket updates



### Response Parameters​

Parameter| Type| Comments  
---|---|---  
id| string| Message ID  
topic| string| Topic name  
creationTime| number| Data created timestamp (ms)  
data| array| Object  
> [category](https://bybit-exchange.github.io/docs/v5/enum#category)| string| Product type `spot`, `linear`, `inverse`, `option`  
> symbol| string| Symbol name  
> isLeverage| string| Whether to borrow. `0`: false, `1`: true  
> orderId| string| Order ID  
> orderLinkId| string| User customized order ID  
> side| string| Side. `Buy`,`Sell`  
> orderPrice| string| Order price  
> orderQty| string| Order qty  
> leavesQty| string| The remaining qty not executed  
> [createType](https://bybit-exchange.github.io/docs/v5/enum#createtype)| string| Order create type 

  * Spot, Option do not have this key

  
> [orderType](https://bybit-exchange.github.io/docs/v5/enum#ordertype)| string| Order type. `Market`,`Limit`  
> [stopOrderType](https://bybit-exchange.github.io/docs/v5/enum#stopordertype)| string| Stop order type. If the order is not stop order, any type is not returned  
> execFee| string| Executed trading fee. You can get spot fee currency instruction [here](https://bybit-exchange.github.io/docs/v5/enum#spot-fee-currency-instruction)  
  
> execId| string| Execution ID  
> execPrice| string| Execution price  
> execQty| string| Execution qty  
> execPnl| string| Profit and Loss for each close position execution. The value keeps consistent with the field "cashFlow" in the [Get Transaction Log](https://bybit-exchange.github.io/docs/v5/account/transaction-log)  
> [execType](https://bybit-exchange.github.io/docs/v5/enum#exectype)| string| Executed type  
> execValue| string| Executed order value  
> execTime| string| Executed timestamp (ms)  
> isMaker| boolean| Is maker order. `true`: maker, `false`: taker  
> feeRate| string| Trading fee rate  
> tradeIv| string| Implied volatility. valid for `option`  
> markIv| string| Implied volatility of mark price. valid for `option`  
> markPrice| string| The mark price of the symbol when executing. valid for `option`  
> indexPrice| string| The index price of the symbol when executing. valid for `option`  
> underlyingPrice| string| The underlying price of the symbol when executing. valid for `option`  
> blockTradeId| string| Paradigm block trade ID  
> closedSize| string| Closed position size  
> extraFees| List| Extra trading fee information. Currently, this data is returned only for kyc=Indian user or spot orders placed on the Indonesian site or spot fiat currency orders placed on the EU site. In other cases, an empty string is returned. Enum: [feeType](https://bybit-exchange.github.io/docs/v5/enum#extrafeesfeetype), [subFeeType](https://bybit-exchange.github.io/docs/v5/enum#extrafeessubfeetype)  
> seq| long| Cross sequence, used to associate each fill and each position update

  * The seq will be the same when conclude multiple transactions at the same time
  * Different symbols may have the same seq, please use seq + symbol to check unique

  
> feeCurrency| string| Trading fee currency  
  
### Subscribe Example​
    
    
    {  
        "op": "subscribe",  
        "args": [  
            "execution"  
        ]  
    }  
    
    
    
    from pybit.unified_trading import WebSocket  
    from time import sleep  
    ws = WebSocket(  
        testnet=True,  
        channel_type="private",  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    def handle_message(message):  
        print(message)  
    ws.execution_stream(callback=handle_message)  
    while True:  
        sleep(1)  
    

### Stream Example​
    
    
    {  
        "topic": "execution",  
        "id": "386825804_BTCUSDT_140612148849382",  
        "creationTime": 1746270400355,  
        "data": [  
            {  
                "category": "linear",  
                "symbol": "BTCUSDT",  
                "closedSize": "0.5",  
                "execFee": "26.3725275",  
                "execId": "0ab1bdf7-4219-438b-b30a-32ec863018f7",  
                "execPrice": "95900.1",  
                "execQty": "0.5",  
                "execType": "Trade",  
                "execValue": "47950.05",  
                "feeRate": "0.00055",  
                "tradeIv": "",  
                "markIv": "",  
                "blockTradeId": "",  
                "markPrice": "95901.48",  
                "indexPrice": "",  
                "underlyingPrice": "",  
                "leavesQty": "0",  
                "orderId": "9aac161b-8ed6-450d-9cab-c5cc67c21784",  
                "orderLinkId": "",  
                "orderPrice": "94942.5",  
                "orderQty": "0.5",  
                "orderType": "Market",  
                "stopOrderType": "UNKNOWN",  
                "side": "Sell",  
                "execTime": "1746270400353",  
                "isLeverage": "0",  
                "isMaker": false,  
                "seq": 140612148849382,  
                "marketUnit": "",  
                "execPnl": "0.05",  
                "createType": "CreateByUser",  
                "extraFees":[{"feeCoin":"USDT","feeType":"GST","subFeeType":"IND_GST","feeRate":"0.0000675","fee":"0.006403779"}],  
                "feeCurrency": "USDT"  
            }  
        ]  
    }  
    

[PreviousPosition](https://bybit-exchange.github.io/docs/v5/websocket/private/position)[NextFast Execution](https://bybit-exchange.github.io/docs/v5/websocket/private/fast-execution)

  * Response Parameters
  * Subscribe Example
  * Stream Example


