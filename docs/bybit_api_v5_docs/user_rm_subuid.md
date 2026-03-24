# Delete Sub UID

> **Source:** https://bybit-exchange.github.io/docs/v5/user/rm-subuid

---

  * [](https://bybit-exchange.github.io/docs/)
  * User
  * Delete Sub UID



On this page

# Delete Sub UID

Delete a sub UID. If a sub-account’s asset balance is greater than 0.001 USDT, it cannot be deleted.  
Use **master** user's api key**.

tip

The API key must have one of the below permissions in order to call this endpoint

  * master API key: "Account Transfer", "Subaccount Transfer", "Withdrawal"



### HTTP Request​

POST`/v5/user/del-submember`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
subMemberId| **true**|  string| Sub UID  
  
### Response Parameters​

None

### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    POST /v5/user/del-submember HTTP/1.1  
    Host: api.bybit.com  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1698907012755  
    X-BAPI-RECV-WINDOW: 5000  
    X-BAPI-SIGN: XXXXXX  
    Content-Type: application/json  
    Content-Length: 34  
      
    {  
        "subMemberId": "112725187"  
    }  
    
    
    
      
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .deleteSubMember({  
        subMemberId: 'subUID',  
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
        "retMsg": "OK",  
        "result": {},  
        "retExtInfo": {},  
        "time": 1698907012962  
    }  
    

[PreviousModify Sub API Key](https://bybit-exchange.github.io/docs/v5/user/modify-sub-apikey)[NextDelete Master API Key](https://bybit-exchange.github.io/docs/v5/user/rm-master-apikey)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


