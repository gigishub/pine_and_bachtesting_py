# Set Deposit Account

> **Source:** https://bybit-exchange.github.io/docs/v5/asset/deposit/set-deposit-acct

---

  * [](https://bybit-exchange.github.io/docs/)
  * Asset
  * Deposit
  * Set Deposit Account



On this page

# Set Deposit Account

Set auto transfer account after deposit. The same function as the setting for Deposit on [web GUI](https://www.bybit.com/app/user/settings)

info

  * Your funds will be deposited into `FUND` wallet by default. You can set the wallet for auto-transfer after deposit by this API.
  * Only **main** UID can access.



### HTTP Request​

POST`/v5/asset/deposit/deposit-to-account`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
[accountType](https://bybit-exchange.github.io/docs/v5/enum#accounttype)| **true**|  string| Account type `UNIFIED`, `FUND`  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
status| integer| Request result: 

  * `1`: SUCCESS
  * `0`: FAIL

  
[RUN >>](https://bybit-exchange.github.io/docs/api-explorer/v5/asset/set-deposit-acct)

* * *

### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    POST /v5/asset/deposit/deposit-to-account HTTP/1.1  
    Host: api.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1676887913670  
    X-BAPI-RECV-WINDOW: 50000  
    Content-Type: application/json  
      
    {  
        "accountType": "CONTRACT"  
    }  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.set_deposit_account(  
        accountType="CONTRACT",  
    ))  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .setDepositAccount({  
        accountType: 'CONTRACT'  
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
        "retMsg": "success",  
        "result": {  
            "status": 1  
        },  
        "retExtInfo": {},  
        "time": 1676887914363  
    }  
    

[PreviousGet Transferable Coin](https://bybit-exchange.github.io/docs/v5/asset/transfer/transferable-coin)[NextGet Deposit Records (on-chain)](https://bybit-exchange.github.io/docs/v5/asset/deposit/deposit-record)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


