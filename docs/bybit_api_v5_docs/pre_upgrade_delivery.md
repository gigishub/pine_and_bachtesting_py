# Get Pre-upgrade Delivery Record

> **Source:** https://bybit-exchange.github.io/docs/v5/pre-upgrade/delivery

---

  * [](https://bybit-exchange.github.io/docs/)
  * Pre-upgrade
  * Get Pre-upgrade Delivery Record



On this page

# Get Pre-upgrade Delivery Record

Query delivery records of Options before you upgraded the account to a Unified account, sorted by `deliveryTime` in descending order

info

  * By `category`="option", you can query Options delivery data occurred during classic account
  * Supports the recent 6 months Options delivery data. Please download older data via GUI



### HTTP Request​

GET`/v5/pre-upgrade/asset/delivery-record`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
[category](https://bybit-exchange.github.io/docs/v5/enum#category)| **true**|  string| Product type `option`  
symbol| false| string| Symbol name, uppercase only  
expDate| false| string| Expiry date. `25MAR22`. Default: return all  
limit| false| integer| Limit for data size per page. [`1`, `50`]. Default: `20`  
cursor| false| string| Cursor. Used for pagination  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
category| string| Product type  
list| array| Object  
> deliveryTime| number| Delivery time (ms)  
> symbol| string| Symbol name  
> side| string| `Buy`,`Sell`  
> position| string| Executed size  
> deliveryPrice| string| Delivery price  
> strike| string| Exercise price  
> fee| string| Trading fee  
> deliveryRpl| string| Realized PnL of the delivery  
nextPageCursor| string| Cursor. Used for pagination  
  
### Request Example​

  * HTTP
  * Python


    
    
    GET /v5/pre-upgrade/asset/delivery-record?category=option HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1686809005774  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    
    
    
      
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "OK",  
        "result": {  
            "nextPageCursor": "21%3A0%2C21%3A0",  
            "category": "option",  
            "list": [  
                {  
                    "symbol": "ETH-14JUN23-1750-C",  
                    "side": "Buy",  
                    "deliveryTime": 1686729604507,  
                    "strike": "1750",  
                    "fee": "0",  
                    "position": "0.5",  
                    "deliveryPrice": "1740.25036667",  
                    "deliveryRpl": "0.175"  
                }  
            ]  
        },  
        "retExtInfo": {},  
        "time": 1686796328492  
    }  
    

[PreviousGet Pre-upgrade Transaction Log](https://bybit-exchange.github.io/docs/v5/pre-upgrade/transaction-log)[NextGet Pre-upgrade USDC Session Settlement](https://bybit-exchange.github.io/docs/v5/pre-upgrade/settlement)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


