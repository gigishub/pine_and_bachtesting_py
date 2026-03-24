# Get Pre-upgrade USDC Session Settlement

> **Source:** https://bybit-exchange.github.io/docs/v5/pre-upgrade/settlement

---

  * [](https://bybit-exchange.github.io/docs/)
  * Pre-upgrade
  * Get Pre-upgrade USDC Session Settlement



On this page

# Get Pre-upgrade USDC Session Settlement

Query session settlement records of USDC perpetual before you upgrade the account to Unified account.

info

  * By category="option", you can query USDC Perps settlement data occurred during classic account
  * USDC Perpeual support the recent 6 months data. Please download older data via GUI



### HTTP Request​

GET`/v5/pre-upgrade/asset/settlement-record`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
[category](https://bybit-exchange.github.io/docs/v5/enum#category)| **true**|  string| Product type `linear`  
symbol| false| string| Symbol name, like `BTCUSDT`, uppercase only  
limit| false| integer| Limit for data size per page. [`1`, `50`]. Default: `20`  
cursor| false| string| Cursor. Used for pagination  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
category| string| Product type  
list| array| Object  
> symbol| string| Symbol name  
> side| string| `Buy`,`Sell`  
> size| string| Position size  
> sessionAvgPrice| string| Settlement price  
> markPrice| string| Mark price  
> realisedPnl| string| Realised PnL  
> createdTime| string| Created time (ms)  
nextPageCursor| string| Cursor. Used for pagination  
  
### Request Example​

  * HTTP
  * Python


    
    
    GET /v5/pre-upgrade/asset/settlement-record?category=linear&symbol=ETHPERP&limit=1 HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1686809850982  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    
    
    
      
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "OK",  
        "result": {  
            "nextPageCursor": "25%3A0%2C25%3A0",  
            "category": "linear",  
            "list": [  
                {  
                    "realisedPnl": "45.76",  
                    "symbol": "ETHPERP",  
                    "side": "Sell",  
                    "markPrice": "1668.44",  
                    "size": "-0.5",  
                    "createdTime": "1686787200000",  
                    "sessionAvgPrice": "1668.41"  
                }  
            ]  
        },  
        "retExtInfo": {},  
        "time": 1686809851749  
    }  
    

[PreviousGet Pre-upgrade Delivery Record](https://bybit-exchange.github.io/docs/v5/pre-upgrade/delivery)[NextGet Wallet Balance](https://bybit-exchange.github.io/docs/v5/account/wallet-balance)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


