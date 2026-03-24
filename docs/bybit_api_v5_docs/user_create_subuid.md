# Create Sub UID

> **Source:** https://bybit-exchange.github.io/docs/v5/user/create-subuid

---

  * [](https://bybit-exchange.github.io/docs/)
  * User
  * Create Sub UID



On this page

# Create Sub UID

Create a new sub user id. Use **master** account's api key.

tip

The API key must have one of the below permissions in order to call this endpoint

  * master API key: "Account Transfer", "Subaccount Transfer", "Withdrawal"



info

Custody account, like copper, fireblock are not supported to create subaccount via this API

### HTTP Request​

POST`/v5/user/create-sub-member`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
username| **true**|  string| Username of the new sub user. 

  * 6-16 characters, must include both numbers and letters.
  * Cannot be the same as the existing or deleted usernames.

  
password| false| string| Password for the new sub user. 

  * 8-30 characters, must include numbers, upper and lowercase letters.

  
memberType| **true**|  integer| `1`: normal subaccount, `6`: [custodial subaccount](https://www.bybit.com/en/help-center/article?id=000001683)  
switch| false| integer| 

  * `0`: turn off quick login (default)
  * `1`: turn on quick login.

  
isUta| false| boolean| **Deprecated** param, always UTA account  
note| false| string| Set a remark  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
uid| string| Sub user Id  
username| string| Username of the new sub user. 

  * 6-16 characters, must include both numbers and letters.
  * Cannot be the same as the existing or deleted usernames.

  
memberType| integer| `1`: normal subaccount, `6`: [custodial subaccount](https://www.bybit.com/en/help-center/article?id=000001683)  
status| integer| The status of the user account

  * `1`: normal
  * `2`: login banned
  * `4`: frozen 

  
remark| string| The remark  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    POST /v5/user/create-sub-member HTTP/1.1  
    Host: api.bybit.com  
    X-BAPI-SIGN: XXXXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1676429344202  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
      
    {  
        "username": "xxxxx",  
        "memberType": 1,  
        "switch": 1,  
        "note": "test"  
    }  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.create_sub_uid(  
        username="xxxxx",  
        memberType=1,  
        switch=1,  
        note="test",  
    ))  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .createSubMember({  
        username: 'xxxxx',  
        memberType: 1,  
        switch: 1,  
        note: 'test',  
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
        "retMsg": "",  
        "result": {  
            "uid": "53888000",  
            "username": "xxxxx",  
            "memberType": 1,  
            "status": 1,  
            "remark": "test"  
        },  
        "retExtInfo": {},  
        "time": 1676429344734  
    }  
    

[PreviousSign Agreement](https://bybit-exchange.github.io/docs/v5/user/sign-agreement)[NextCreate Sub UID API Key](https://bybit-exchange.github.io/docs/v5/user/create-subuid-apikey)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


