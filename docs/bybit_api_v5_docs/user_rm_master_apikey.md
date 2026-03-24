# Delete Master API Key

> **Source:** https://bybit-exchange.github.io/docs/v5/user/rm-master-apikey

---

  * [](https://bybit-exchange.github.io/docs/)
  * User
  * Delete Master API Key



On this page

# Delete Master API Key

Delete the api key of master account. Use the api key pending to be delete to call the endpoint. Use **master user's api key** **only**.

tip

The API key must have one of the below permissions in order to call this endpoint..

  * master API key: "Account Transfer", "Subaccount Transfer", "Withdrawal"



danger

BE CAREFUL! The API key used to call this interface will be invalid immediately.

### HTTP Request​

POST`/v5/user/delete-api`Copy

### Request Parameters​

None

### Response Parameters​

None

### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    POST /v5/user/delete-api HTTP/1.1  
    Host: api.bybit.com  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1676431576621  
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
    print(session.delete_master_api_key())  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .deleteMasterApiKey()  
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
        "time": 1676431577675  
    }  
    

[PreviousDelete Sub UID](https://bybit-exchange.github.io/docs/v5/user/rm-subuid)[NextDelete Sub API Key](https://bybit-exchange.github.io/docs/v5/user/rm-sub-apikey)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


