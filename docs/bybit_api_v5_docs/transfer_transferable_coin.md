# Get Transferable Coin

> **Source:** https://bybit-exchange.github.io/docs/v5/asset/transfer/transferable-coin

---

  * [](https://bybit-exchange.github.io/docs/)
  * Asset
  * Transfer
  * Get Transferable Coin



On this page

# Get Transferable Coin

Query the transferable coin list between each [account type](https://bybit-exchange.github.io/docs/v5/enum#accounttype)

### HTTP Request​

GET`/v5/asset/transfer/query-transfer-coin-list`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
[fromAccountType](https://bybit-exchange.github.io/docs/v5/enum#accounttype)| **true**|  string| From account type  
[toAccountType](https://bybit-exchange.github.io/docs/v5/enum#accounttype)| **true**|  string| To account type  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
list| array| A list of coins (as strings)  
[RUN >>](https://bybit-exchange.github.io/docs/api-explorer/v5/asset/transferable-coin)

* * *

### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/asset/transfer/query-transfer-coin-list?fromAccountType=UNIFIED&toAccountType=CONTRACT HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1672144322595  
    X-BAPI-RECV-WINDOW: 5000  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.get_transferable_coin(  
        fromAccountType="UNIFIED",  
        toAccountType="CONTRACT",  
    ))  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .getTransferableCoinList('UNIFIED', 'CONTRACT')  
      .then((response) => {  
        console.log(response);  
      })  
      .catch((error) => {  
        console.error(error);  
      });  
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "success",  
        "result": {  
            "list": [  
                "BTC",  
                "ETH"  
            ]  
        },  
        "retExtInfo": {},  
        "time": 1672144322954  
    }  
    

[PreviousGet Universal Transfer Records](https://bybit-exchange.github.io/docs/v5/asset/transfer/unitransfer-list)[NextSet Deposit Account](https://bybit-exchange.github.io/docs/v5/asset/deposit/set-deposit-acct)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


