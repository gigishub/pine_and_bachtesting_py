# Delete Sub API Key

> **Source:** https://bybit-exchange.github.io/docs/v5/user/rm-sub-apikey

---

  * [](https://bybit-exchange.github.io/docs/)
  * User
  * Delete Sub API Key



On this page

# Delete Sub API Key

Delete the api key of sub account. Use the sub api key pending to be delete to call the endpoint or use the master api key to delete corresponding sub account api key

tip

The API key must have one of the below permissions in order to call this endpoint.

  * sub API key: "Account Transfer", "Sub Member Transfer"
  * master API Key: "Account Transfer", "Sub Member Transfer", "Withdrawal"



danger

BE CAREFUL! The Sub account API key will be invalid immediately after calling the endpoint.

### HTTP Request​

POST`/v5/user/delete-sub-api`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
apikey| false| string| Sub account api key 

  * You must pass this param when you use master account manage sub account api key settings
  * If you use corresponding sub uid api key call this endpoint, `apikey` param cannot be passed, otherwise throwing an error

  
  
### Response Parameters​

None

### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    POST /v5/user/delete-sub-api HTTP/1.1  
    Host: api.bybit.com  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1676431922953  
    X-BAPI-RECV-WINDOW: 5000  
    X-BAPI-SIGN: XXXXXX  
    Content-Type: application/json  
      
    {  
      
    }  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.delete_sub_api_key())  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .deleteSubApiKey()  
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
        "time": 1676431924719  
    }  
    

[PreviousDelete Master API Key](https://bybit-exchange.github.io/docs/v5/user/rm-master-apikey)[NextGet Friend Referrals](https://bybit-exchange.github.io/docs/v5/user/friend-referral)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


