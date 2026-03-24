# Get Pre-upgrade Transaction Log

> **Source:** https://bybit-exchange.github.io/docs/v5/pre-upgrade/transaction-log

---

  * [](https://bybit-exchange.github.io/docs/)
  * Pre-upgrade
  * Get Pre-upgrade Transaction Log



On this page

# Get Pre-upgrade Transaction Log

Query transaction logs which occurred in the USDC Derivatives wallet before the account was upgraded to a Unified account.

By category="linear", you can query USDC Perps transaction logs occurred during classic account By category="option", you can query Options transaction logs occurred during classic account

You can get USDC Perpetual, Option records.

info

USDC Perpeual & Option support the recent 6 months data. Please download older data via GUI

### HTTP Request​

GET`/v5/pre-upgrade/account/transaction-log`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
[category](https://bybit-exchange.github.io/docs/v5/enum#category)| **true**|  string| Product type `linear`, `option`  
baseCoin| false| string| BaseCoin, uppercase only. e.g., BTC of BTCPERP  
[type](https://bybit-exchange.github.io/docs/v5/enum#type)| false| string| Types of transaction logs  
startTime| false| integer| The start timestamp (ms) 

  * startTime and endTime are not passed, return 7 days by default
  * Only startTime is passed, return range between startTime and startTime+7 days
  * Only endTime is passed, return range between endTime-7 days and endTime
  * If both are passed, the rule is endTime - startTime <= 7 days

  
endTime| false| integer| The end timestamp (ms)  
limit| false| integer| Limit for data size per page. [`1`, `50`]. Default: `20`  
cursor| false| string| Cursor. Used for pagination  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
list| array| Object  
> symbol| string| Symbol name  
> category| string| Product type  
> side| string| Side. `Buy`,`Sell`,`None`  
> transactionTime| string| Transaction timestamp (ms)  
> [type](https://bybit-exchange.github.io/docs/v5/enum#type)| string| Type  
> qty| string| Quantity  
> size| string| Size  
> currency| string| USDC、USDT、BTC、ETH  
> tradePrice| string| Trade price  
> funding| string| Funding fee 

  * Positive value means receiving funding fee
  * Negative value means deducting funding fee

  
> fee| string| Trading fee 

  * Positive fee value means expense
  * Negative fee value means rebates

  
> cashFlow| string| Cash flow  
> change| string| Change  
> cashBalance| string| Cash balance  
> feeRate| string| 

  * When type=`TRADE`, then it is trading fee rate
  * When type=`SETTLEMENT`, it means funding fee rate. For side=Buy, feeRate=market fee rate; For side=Sell, feeRate= - market fee rate

  
> bonusChange| string| The change of bonus  
> tradeId| string| Trade ID  
> orderId| string| Order ID  
> orderLinkId| string| User customised order ID  
nextPageCursor| string| Cursor. Used for pagination  
  
### Request Example​

  * HTTP
  * Python


    
    
    GET /v5/pre-upgrade/account/transaction-log?category=option HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1686808288265  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    
    
    
      
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "OK",  
        "result": {  
            "nextPageCursor": "21%3A0%2C21%3A0",  
            "list": [  
                {  
                    "symbol": "ETH-14JUN23-1750-C",  
                    "side": "Buy",  
                    "funding": "",  
                    "orderLinkId": "",  
                    "orderId": "",  
                    "fee": "0",  
                    "change": "0",  
                    "cashFlow": "0",  
                    "transactionTime": "1686729604507",  
                    "type": "DELIVERY",  
                    "feeRate": "0",  
                    "bonusChange": "",  
                    "size": "0",  
                    "qty": "0.5",  
                    "cashBalance": "1001.1438885",  
                    "currency": "USDC",  
                    "category": "option",  
                    "tradePrice": "1740.25036667",  
                    "tradeId": ""  
                }  
            ]  
        },  
        "retExtInfo": {},  
        "time": 1686809006792  
    }  
    

[PreviousGet Pre-upgrade Closed PnL](https://bybit-exchange.github.io/docs/v5/pre-upgrade/close-pnl)[NextGet Pre-upgrade Delivery Record](https://bybit-exchange.github.io/docs/v5/pre-upgrade/delivery)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


