# Get Transaction Log

> **Source:** https://bybit-exchange.github.io/docs/v5/abandon/contract-transaction-log

---

  * [](https://bybit-exchange.github.io/docs/)
  * Abandoned Endpoints
  * Get Transaction Log (Classic)



On this page

# Get Transaction Log

Query transaction logs in the derivatives wallet (classic account), and inverse derivatives account (upgraded to UTA)

> **Permission** : "Contract - Position"  
>  **Apply to** : classic account, [UTA1.0](https://bybit-exchange.github.io/docs/v5/acct-mode#uta-10)(inverse)

### HTTP Request​

GET`/v5/account/contract-transaction-log`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
currency| false| string| Currency, uppercase only  
baseCoin| false| string| BaseCoin, uppercase only. e.g., BTC of BTCPERP  
[type](https://bybit-exchange.github.io/docs/v5/enum#typecontract-translog)| false| string| Types of transaction logs  
startTime| false| integer| The start timestamp (ms) 

  * startTime and endTime are not passed, return 7 days by default
  * Only startTime is passed, return range between startTime and startTime+7 days
  * Only endTime is passed, return range between endTime-7 days and endTime
  * If both are passed, the rule is endTime - startTime <= 7 days

  
endTime| false| integer| The end timestamp (ms)  
limit| false| integer| Limit for data size per page. [`1`, `50`]. Default: `20`  
cursor| false| string| Cursor. Use the `nextPageCursor` token from the response to retrieve the next page of the result set  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
list| array| Object  
> id| string| Unique id  
> symbol| string| Symbol name  
> category| string| Product type  
> side| string| Side. `Buy`,`Sell`,`None`  
> transactionTime| string| Transaction timestamp (ms)  
> [type](https://bybit-exchange.github.io/docs/v5/enum#type)| string| Type  
> qty| string| Quantity 

  * Perps & Futures: it is the quantity for each trade entry and it does not have direction

  
> size| string| Size. The rest position size after the trade is executed, and it has direction, i.e., short with "-"  
> currency| string| currency  
> tradePrice| string| Trade price  
> funding| string| Funding fee 

  * Positive value means deducting funding fee
  * Negative value means receiving funding fee

  
> fee| string| Trading fee 

  * Positive fee value means expense
  * Negative fee value means rebates

  
> cashFlow| string| Cash flow, e.g., (1) close the position, and unRPL converts to RPL, (2) transfer in or transfer out. This does not include trading fee, funding fee  
> change| string| Change = cashFlow - funding - fee  
> cashBalance| string| Cash balance. This is the wallet balance after a cash change  
> feeRate| string| 

  * When type=`TRADE`, then it is trading fee rate
  * When type=`SETTLEMENT`, it means funding fee rate. For side=Buy, feeRate=market fee rate; For side=Sell, feeRate= - market fee rate

  
> bonusChange| string| The change of bonus  
> tradeId| string| Trade ID  
> orderId| string| Order ID  
> orderLinkId| string| User customised order ID  
nextPageCursor| string| Refer to the `cursor` request parameter  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/account/contract-transaction-log?limit=1&symbol=BTCUSD HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1714035117255  
    X-BAPI-RECV-WINDOW: 5000  
    
    
    
      
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .getClassicTransactionLogs({  
        limit: 1,  
        symbol: 'BTCUSD',  
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
                    "id": "467153",  
                    "symbol": "BTCUSD",  
                    "category": "inverse",  
                    "side": "Sell",  
                    "transactionTime": "1714032000000",  
                    "type": "SETTLEMENT",  
                    "qty": "1000",  
                    "size": "-1000",  
                    "currency": "BTC",  
                    "tradePrice": "63974.88",  
                    "funding": "-0.00000156",  
                    "fee": "",  
                    "cashFlow": "0.00000000",  
                    "change": "0.00000156",  
                    "cashBalance": "1.1311",  
                    "feeRate": "-0.00010000",  
                    "bonusChange": "",  
                    "tradeId": "423a565c-f1b6-4c81-bc62-760cd7dd89e7",  
                    "orderId": "",  
                    "orderLinkId": ""  
                }  
            ],  
            "nextPageCursor": "cursor_id%3D467153%26"  
        },  
        "retExtInfo": {},  
        "time": 1714035117258  
    }  
    

[PreviousSet Risk Limit](https://bybit-exchange.github.io/docs/v5/abandon/set-risk-limit)[NextSet TP/SL Mode (deprecated)](https://bybit-exchange.github.io/docs/v5/abandon/tpsl-mode)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


