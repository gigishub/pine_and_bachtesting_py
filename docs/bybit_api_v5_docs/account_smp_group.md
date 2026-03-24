# Get SMP Group ID

> **Source:** https://bybit-exchange.github.io/docs/v5/account/smp-group

---

  * [](https://bybit-exchange.github.io/docs/)
  * Account
  * Get SMP Group ID



On this page

# Get SMP Group ID

Query the SMP group ID of self match prevention

### HTTP Request​

GET`/v5/account/smp-group`Copy

### Request Parameters​

None

### Response Parameters​

Parameter| Type| Comments  
---|---|---  
smpGroup| integer| Smp group ID. If the UID has no group, it is `0` by default  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/account/smp-group HTTP/1.1  
    Host: api.bybit.com  
    X-BAPI-SIGN: XXXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1702363848192  
    X-BAPI-RECV-WINDOW: 5000  
    
    
    
      
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .getSMPGroup()  
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
            "smpGroup": 0  
        },  
        "retExtInfo": {},  
        "time": 1702363848539  
    }  
    

[PreviousSet MMP](https://bybit-exchange.github.io/docs/v5/account/set-mmp)[NextGet Trade Behaviour Config](https://bybit-exchange.github.io/docs/v5/account/get-user-setting-config)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


