# Get Order History

> **Source:** https://bybit-exchange.github.io/docs/v5/spread/trade/order-history

---

  * [](https://bybit-exchange.github.io/docs/)
  * Spread Trading
  * Trade
  * Get Order History



On this page

# Get Order History

info

  * orderId & orderLinkId has a higher priority than startTime & endTime
  * Fully cancelled orders are stored for up to 24 hours.



**Single leg orders can also be found with "createType"=`CreateByFutureSpread` via [Get Order History](https://bybit-exchange.github.io/docs/v5/order/order-list)**

### HTTP Request​

GET`/v5/spread/order/history`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
symbol| false| string| Spread combination symbol name  
baseCoin| false| string| Base coin  
orderId| false| string| Spread combination order ID  
orderLinkId| false| string| User customised order ID  
startTime| false| long| The start timestamp (ms)

  * startTime and endTime are not passed, return 7 days by default
  * Only startTime is passed, return range between startTime and startTime+7 days
  * Only endTime is passed, return range between endTime-7 days and endTime
  * If both are passed, the rule is endTime - startTime <= 7 days

  
endTime| false| long| The end timestamp (ms)  
limit| false| integer| Limit for data size per page. [`1`, `50`]. Default: `20`  
cursor| false| string| Cursor. Use the `nextPageCursor` token from the response to retrieve the next page of the result set  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
list| array<object>| Order info  
> symbol| string| Spread combination symbol name  
> orderType| string| Order type, `Market`, `Limit`  
> orderLinkId| string| User customised order ID  
> orderId| string| Spread combination order ID  
> contractType| string| Combo type 

  * `FundingRateArb`: perpetual & spot combination
  * `CarryTrade`: futures & spot combination
  * `FutureSpread`: different expiry futures combination
  * `PerpBasis`: futures & perpetual

  
> [cxlRejReason](https://bybit-exchange.github.io/docs/v5/enum#rejectreason)| string| Reject reason  
> [orderStatus](https://bybit-exchange.github.io/docs/v5/enum#orderstatus)| string| Order status, `Rejected`, `Cancelled`, `Filled`  
> price| string| Order price  
> orderQty| string| Order qty  
> timeInForce| string| Time in force, `GTC`, `FOK`, `IOC`, `PostOnly`  
> baseCoin| string| Base coin  
> createdAt| string| Order created timestamp (ms)  
> updatedAt| string| Order updated timestamp (ms)  
> side| string| Side, `Buy`, `Sell`  
> leavesQty| string| The remaining qty not executed. It is meaningless for a cancelled order  
> settleCoin| string| Settle coin  
> cumExecQty| string| Cumulative executed order qty  
> qty| string| Order qty  
> leg1Symbol| string| Leg1 symbol name  
> leg1ProdType| string| Leg1 product type, `Futures`, `Spot`  
> leg1OrderId| string| Leg1 order ID  
> leg1Side| string| Leg1 order side  
> leg2ProdType| string| Leg2 product type, `Futures`, `Spot`  
> leg2OrderId| string| Leg2 order ID  
> leg2Symbol| string| Leg2 symbol name  
> leg2Side| string| Leg2 orde side  
nextPageCursor| string| Refer to the `cursor` request parameter  
  
### Request Example​
    
    
    GET /v5/spread/order/history?orderId=aaaee090-fab3-42ea-aea0-c9fbfe6c4bc4 HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: XXXXXX  
    X-BAPI-TIMESTAMP: 1744100522465  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "Success",  
        "result": {  
            "nextPageCursor": "aaaee090-fab3-42ea-aea0-c9fbfe6c4bc4%3A1744096099767%2Caaaee090-fab3-42ea-aea0-c9fbfe6c4bc4%3A1744096099767",  
            "list": [  
                {  
                    "symbol": "SOLUSDT_SOL/USDT",  
                    "orderType": "Limit",  
                    "orderLinkId": "",  
                    "orderId": "aaaee090-fab3-42ea-aea0-c9fbfe6c4bc4",  
                    "contractType": "FundingRateArb",  
                    "orderStatus": "Cancelled",  
                    "createdAt": "1744096099767",  
                    "price": "-4",  
                    "leg2Symbol": "SOLUSDT",  
                    "orderQty": "0.1",  
                    "timeInForce": "PostOnly",  
                    "baseCoin": "SOL",  
                    "updatedAt": "1744098396079",  
                    "side": "Buy",  
                    "leg2Side": "Sell",  
                    "leavesQty": "0",  
                    "leg1Side": "Buy",  
                    "settleCoin": "USDT",  
                    "cumExecQty": "0",  
                    "qty": "0.1",  
                    "leg1OrderId": "82335b0a-b7d9-4ea5-9230-e71271a65100",  
                    "leg2OrderId": "1924011967786517249",  
                    "leg2ProdType": "Spot",  
                    "leg1ProdType": "Futures",  
                    "leg1Symbol": "SOLUSDT"  
                }  
            ]  
        },  
        "retExtInfo": {},  
        "time": 1744102655725  
    }  
    

[PreviousGet Open Orders](https://bybit-exchange.github.io/docs/v5/spread/trade/open-order)[NextGet Trade History](https://bybit-exchange.github.io/docs/v5/spread/trade/trade-history)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


