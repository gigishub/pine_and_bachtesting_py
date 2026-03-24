# Get USDC Session Settlement

> **Source:** https://bybit-exchange.github.io/docs/v5/asset/settlement

---

  * [](https://bybit-exchange.github.io/docs/)
  * Asset
  * Get USDC Session Settlement (2 years)



On this page

# Get USDC Session Settlement

Query session settlement records of USDC perpetual and futures

info

  * During periods of extreme market volatility, this interface may experience increased latency or temporary delays in data delivery



### HTTP Request​

GET`/v5/asset/settlement-record`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
[category](https://bybit-exchange.github.io/docs/v5/enum#category)| **true**|  string| Product type `linear`(USDC contract)  
symbol| false| string| Symbol name, like `BTCPERP`, uppercase only  
startTime| false| integer| The start timestamp (ms) 

  * startTime and endTime are not passed, return 30 days by default
  * Only startTime is passed, return range between startTime and startTime + 30 days 
  * Only endTime is passed, return range between endTime-30 days and endTime
  * If both are passed, the rule is endTime - startTime <= 30 days

  
endTime| false| integer| The end time. timestamp (ms)  
limit| false| integer| Limit for data size per page. [`1`, `50`]. Default: `20`  
cursor| false| string| Cursor. Use the `nextPageCursor` token from the response to retrieve the next page of the result set  
  
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
nextPageCursor| string| Refer to the `cursor` request parameter  
[RUN >>](https://bybit-exchange.github.io/docs/api-explorer/v5/asset/settlement)

* * *

### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/asset/settlement-record?category=linear HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1672284883483  
    X-BAPI-RECV-WINDOW: 5000  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.get_usdc_contract_settlement(  
        category="linear",  
    ))  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .getSettlementRecords({ category: 'linear' })  
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
            "nextPageCursor": "116952%3A1%2C116952%3A1",  
            "category": "linear",  
            "list": [  
                {  
                    "realisedPnl": "-71.28",  
                    "symbol": "BTCPERP",  
                    "side": "Buy",  
                    "markPrice": "16620",  
                    "size": "1.5",  
                    "createdTime": "1672214400000",  
                    "sessionAvgPrice": "16620"  
                }  
            ]  
        },  
        "retExtInfo": {},  
        "time": 1672284884285  
    }  
    

[PreviousGet Delivery Record (2 years)](https://bybit-exchange.github.io/docs/v5/asset/delivery)[NextGet Coin Exchange Records](https://bybit-exchange.github.io/docs/v5/asset/exchange)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


