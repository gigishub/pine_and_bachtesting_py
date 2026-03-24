# Get Account Info

> **Source:** https://bybit-exchange.github.io/docs/v5/account/account-info

---

  * [](https://bybit-exchange.github.io/docs/)
  * Account
  * Get Account Info



On this page

# Get Account Info

Query the account information, like margin mode, account mode, etc.

### HTTP Request​

GET`/v5/account/info`Copy

### Request Parameters​

None

### Response Parameters​

Parameter| Type| Comments  
---|---|---  
[unifiedMarginStatus](https://bybit-exchange.github.io/docs/v5/enum#unifiedmarginstatus)| integer| Account status  
marginMode| string| `ISOLATED_MARGIN`, `REGULAR_MARGIN`, `PORTFOLIO_MARGIN`  
isMasterTrader| boolean| Whether this account is a leader (copytrading). `true`, `false`  
spotHedgingStatus| string| Whether the unified account enables Spot hedging. `ON`, `OFF`  
updatedTime| string| Account data updated timestamp (ms)  
dcpStatus| string| deprecated, always `OFF`. Please use [Get DCP Info](https://bybit-exchange.github.io/docs/v5/account/dcp-info)  
timeWindow| integer| deprecated, always `0`. Please use [Get DCP Info](https://bybit-exchange.github.io/docs/v5/account/dcp-info)  
smpGroup| integer| deprecated, always `0`. Please query [Get SMP Group ID](https://bybit-exchange.github.io/docs/v5/account/smp-group) endpoint  
[RUN >>](https://bybit-exchange.github.io/docs/api-explorer/v5/account/account-info)

* * *

### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/account/info HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1672129307221  
    X-BAPI-RECV-WINDOW: 5000  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.get_account_info())  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
        testnet: true,  
        key: 'xxxxxxxxxxxxxxxxxx',  
        secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
        .getAccountInfo()  
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
            "marginMode": "REGULAR_MARGIN",  
            "updatedTime": "1697078946000",  
            "unifiedMarginStatus": 4,  
            "dcpStatus": "OFF",  
            "timeWindow": 10,  
            "smpGroup": 0,  
            "isMasterTrader": false,  
            "spotHedgingStatus": "OFF"  
        }  
    }  
    

[PreviousGet Transaction Log (UTA)](https://bybit-exchange.github.io/docs/v5/account/transaction-log)[NextGet Account Instruments Info](https://bybit-exchange.github.io/docs/v5/account/instrument)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


