# Get UID Wallet Type

> **Source:** https://bybit-exchange.github.io/docs/v5/user/wallet-type

---

  * [](https://bybit-exchange.github.io/docs/)
  * User
  * Get UID Wallet Type



On this page

# Get UID Wallet Type

Get available wallet types for the master account or sub account

tip

  * Master api key: you can get master account and appointed sub account available wallet types, and support up to 200 sub UID in one request.
  * Sub api key: you can get its own available wallet types



### HTTP Request​

GET`/v5/user/get-member-type`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
memberIds| false| string| 

  * Query itself wallet types when not passed
  * When use master api key to query sub UID, master UID data is always returned in the top of the array
  * Multiple sub UID are supported, separated by commas
  * This param is ignored when you use sub account api key

  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
accounts| array| Object  
> uid| string| Master/Sub user Id  
> [accountType](https://bybit-exchange.github.io/docs/v5/enum#accounttype)| array| Wallets array. `FUND`,`UNIFIED`  
[RUN >>](https://bybit-exchange.github.io/docs/api-explorer/v5/user/wallet-type)

* * *

### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/user/get-member-type HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1686884973961  
    X-BAPI-RECV-WINDOW: 5000  
    Content-Type: application/json  
    
    
    
      
    
    
    
    // https://api.bybit.com/v5/user/get-member-type  
      
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .getUIDWalletType({  
        memberIds: 'subUID1,subUID2',  
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
            "accounts": [  
                {  
                    "uid": "533285",  
                    "accountType": [  
                        "UNIFIED",  
                        "FUND"  
                    ]  
                }  
            ]  
        },  
        "retExtInfo": {},  
        "time": 1686884974151  
    }  
    

[PreviousGet Sub Account All API Keys](https://bybit-exchange.github.io/docs/v5/user/list-sub-apikeys)[NextModify Master API Key](https://bybit-exchange.github.io/docs/v5/user/modify-master-apikey)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


