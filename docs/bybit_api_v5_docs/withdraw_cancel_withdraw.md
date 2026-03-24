# Cancel Withdrawal

> **Source:** https://bybit-exchange.github.io/docs/v5/asset/withdraw/cancel-withdraw

---

  * [](https://bybit-exchange.github.io/docs/)
  * Asset
  * Withdraw
  * Cancel Withdrawal



On this page

# Cancel Withdrawal

Cancel the withdrawal

### HTTP Request​

POST`/v5/asset/withdraw/cancel`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
id| **true**|  string| Withdrawal ID  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
status| integer| `0`: fail. `1`: success  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    POST /v5/asset/withdraw/cancel HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1672197227732  
    X-BAPI-RECV-WINDOW: 5000  
    X-BAPI-SIGN: XXXXX  
    Content-Type: application/json  
      
    {  
        "id": "10197"  
    }  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.cancel_withdrawal(  
        id="10197",  
    ))  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .cancelWithdrawal('10197')  
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
            "status": 1  
        },  
        "retExtInfo": {},  
        "time": 1672197228408  
    }  
    

[PreviousWithdraw](https://bybit-exchange.github.io/docs/v5/asset/withdraw)[NextGuideline](https://bybit-exchange.github.io/docs/v5/asset/convert/guideline)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


