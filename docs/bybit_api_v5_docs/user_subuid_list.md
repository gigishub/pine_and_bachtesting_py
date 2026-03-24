# Get Sub UID List (Limited)

> **Source:** https://bybit-exchange.github.io/docs/v5/user/subuid-list

---

  * [](https://bybit-exchange.github.io/docs/)
  * User
  * Get Sub UID List (Limited)



On this page

# Get Sub UID List (Limited)

Get at most 10k sub UID of master account. Use **master user's api key** **only**.

tip

The API key must have one of the below permissions in order to call this endpoint..

  * master API key: "Account Transfer", "Subaccount Transfer", "Withdrawal"



### HTTP Request​

GET`/v5/user/query-sub-members`Copy

### Request Parameters​

None

### Response Parameters​

Parameter| Type| Comments  
---|---|---  
subMembers| array| Object  
> uid| string| Sub user Id  
> username| string| Username  
> memberType| integer| `1`: normal subaccount, `6`: custodial sub account  
> status| integer| The status of the user account

  * `1`: normal
  * `2`: login banned
  * `4`: frozen 

  
> accountMode| integer| The account mode of the user account

  * `1`: Classic Account
  * `3`: UTA1.0
  * `4`: UTA1.0 Pro
  * `5`: UTA2.0
  * `6`: UTA2.0 Pro

  
> remark| string| The remark  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/user/query-sub-members HTTP/1.1  
    Host: api.bybit.com  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1676430318405  
    X-BAPI-RECV-WINDOW: 5000  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.get_sub_uid())  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .getSubUIDList()  
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
        "result": {  
            "subMembers": [  
                {  
                    "uid": "106314365",  
                    "username": "xxxx02",  
                    "memberType": 1,  
                    "status": 1,  
                    "remark": "",  
                    "accountMode": 5  
                },  
                {  
                    "uid": "106279879",  
                    "username": "xxxx01",  
                    "memberType": 1,  
                    "status": 1,  
                    "remark": "",  
                    "accountMode": 6  
                }  
            ]  
        },  
        "retExtInfo": {},  
        "time": 1760388036728  
    }  
    

[PreviousCreate Sub UID API Key](https://bybit-exchange.github.io/docs/v5/user/create-subuid-apikey)[NextGet Sub UID List (Unlimited)](https://bybit-exchange.github.io/docs/v5/user/page-subuid)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


