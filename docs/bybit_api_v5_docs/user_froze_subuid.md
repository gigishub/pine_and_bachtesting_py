# Freeze Sub UID

> **Source:** https://bybit-exchange.github.io/docs/v5/user/froze-subuid

---

  * [](https://bybit-exchange.github.io/docs/)
  * User
  * Freeze Sub UID



On this page

# Freeze Sub UID

Freeze Sub UID. Use **master user's api key** **only**.

tip

The API key must have one of the below permissions in order to call this endpoint..

  * master API key: "Account Transfer", "Subaccount Transfer", "Withdrawal"



### HTTP Request​

POST`/v5/user/frozen-sub-member`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
subuid| **true**|  integer| Sub user Id  
frozen| **true**|  integer| `0`: unfreeze, `1`: freeze  
  
### Response Parameters​

None

### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    POST /v5/user/frozen-sub-member HTTP/1.1  
    Host: api.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1676430842094  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
      
    {  
        "subuid": 53888001,  
        "frozen": 1  
    }  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.freeze_sub_uid(  
        subuid=53888001,  
        frozen=1,  
    ))  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .setSubUIDFrozenState(53888001, 1)  
      .then((response) => {  
        console.log(response);  
      })  
      .catch((error) => {  
        console.error(error);  
      });  
    

### Response Example​
    
    
    {  
        "retCode": 0,  
        "retMsg": "",  
        "result": {},  
        "retExtInfo": {},  
        "time": 1676430697553  
    }  
    

[PreviousGet Fund Custodial Sub Acct](https://bybit-exchange.github.io/docs/v5/user/fund-subuid-list)[NextGet API Key Information](https://bybit-exchange.github.io/docs/v5/user/apikey-info)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


