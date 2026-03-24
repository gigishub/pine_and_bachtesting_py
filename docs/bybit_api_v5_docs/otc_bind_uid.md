# Bind Or Unbind UID

> **Source:** https://bybit-exchange.github.io/docs/v5/otc/bind-uid

---

  * [](https://bybit-exchange.github.io/docs/)
  * Institutional Loan
  * Bind Or Unbind UID



On this page

# Bind Or Unbind UID

For the institutional loan product, you can bind new UIDs to the risk unit or unbind UID from the risk unit.

info

  * The risk unit designated UID cannot be unbound.
  * The UID you want to bind must be upgraded to UTA Pro.



### HTTP Request​

POST`/v5/ins-loan/association-uid`Copy

### Request Parameters​

Parameter| Required| Type| Comments  
---|---|---|---  
uid| **true**|  string| UID 

  * **Bind**  
a) the key used must be from one of UIDs in the risk unit;   
b) input UID must not have an INS loan
  * **Unbind**  
a) the key used must be from one of UIDs in the risk unit;   
b) input UID cannot be the same as the UID used to access the API

  
operate| **true**|  string| `0`: bind, `1`: unbind  
  
### Response Parameters​

Parameter| Type| Comments  
---|---|---  
uid| string| UID  
operate| string| `0`: bind, `1`: unbind  
  
### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    POST /v5/ins-loan/association-uid HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1699257853101  
    X-BAPI-RECV-WINDOW: 5000  
    X-BAPI-SIGN: XXXXX  
    Content-Type: application/json  
    Content-Length: 43  
      
    {  
        "uid": "592324",  
        "operate": "0"  
    }  
    
    
    
    from pybit.unified_trading import HTTP  
    session = HTTP(  
        testnet=True,  
        api_key="xxxxxxxxxxxxxxxxxx",  
        api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
    )  
    print(session.bind_or_unbind_uid(uid="592324", operate="0"))  
    
    
    
    const { RestClientV5 } = require('bybit-api');  
      
    const client = new RestClientV5({  
      testnet: true,  
      key: 'xxxxxxxxxxxxxxxxxx',  
      secret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  
    });  
      
    client  
      .bindOrUnbindUID({  
        uid: 'yourUID',  
        operate: '0', // 0 for bind, 1 for unbind  
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
        "result": {  
            "uid": "592324",  
            "operate": "0"  
        },  
        "retExtInfo": {},  
        "time": 1699257746135  
    }  
    

[PreviousGet LTV](https://bybit-exchange.github.io/docs/v5/otc/ltv-convert)[NextRepay](https://bybit-exchange.github.io/docs/v5/otc/repay)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


