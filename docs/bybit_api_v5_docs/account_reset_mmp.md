# Reset MMP

> **Source:** https://bybit-exchange.github.io/docs/v5/account/reset-mmp

---

  * [](https://bybit-exchange.github.io/docs/)
  * Account
  * Reset MMP



On this page

# Reset MMP

info

  * Once the mmp triggered, you can unfreeze the account by this endpoint, then `qtyLimit` and `deltaLimit` will be reset to 0.
  * If the account is not frozen, reset action can also remove previous accumulation, i.e., `qtyLimit` and `deltaLimit` will be reset to 0.



### HTTP Request​

POST`/v5/account/mmp-reset`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
baseCoin| **true**|  string| Base coin, uppercase only  
  
### Response Parameters​

None

### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    POST /v5/account/mmp-reset HTTP/1.1  
    Host: api.bybit.com  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1675842997277  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
      
    {  
        "baseCoin": "ETH"  
    }  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.reset_mmp(  
        baseCoin="ETH",  
    ))  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
        testnet: true,  
        key: 'xxxxxxxxxxxxxxxxxx',  
        secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
        .resetMMP('ETH')  
        .then((response) => {  
            console.log(response);  
        })  
        .catch((error) => {  
            console.error(error);  
        });  
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "success"  
    }  
    

[PreviousGet MMP State](https://bybit-exchange.github.io/docs/v5/account/get-mmp-state)[NextSet MMP](https://bybit-exchange.github.io/docs/v5/account/set-mmp)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


