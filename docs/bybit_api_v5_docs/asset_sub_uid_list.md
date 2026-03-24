# Get Sub UID

> **Source:** https://bybit-exchange.github.io/docs/v5/asset/sub-uid-list

---

  * [](https://bybit-exchange.github.io/docs/)
  * Asset
  * Get Sub UID



On this page

# Get Sub UID

Query the sub UIDs under a main UID. It returns up to 2000 sub accounts, if you need more, please call this [endpoint](https://bybit-exchange.github.io/docs/v5/user/page-subuid).

info

Query by the master UID's api key **only**

### HTTP Request​

GET`/v5/asset/transfer/query-sub-member-list`Copy

### Request Parameters​

None

### Response Parameters​

Parameter| Type| Comments  
---|---|---  
subMemberIds| array<string>| All sub UIDs under the main UID  
transferableSubMemberIds| array<string>| All sub UIDs that have universal transfer enabled  
[RUN >>](https://bybit-exchange.github.io/docs/api-explorer/v5/asset/sub-uid-list)

* * *

### Request Example​

  * HTTP
  * Python
  * Node.js


    
    
    GET /v5/asset/transfer/query-sub-member-list HTTP/1.1  
    Host: api-testnet.bybit.com  
    X-BAPI-SIGN: XXXXX  
    X-BAPI-API-KEY: xxxxxxxxxxxxxxxxxx  
    X-BAPI-TIMESTAMP: 1672147239931  
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
      .getSubUID()  
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
            "subMemberIds": [  
                "554117",  
                "592324",  
                "592334",  
                "1055262",  
                "1072055",  
                "1119352"  
            ],  
            "transferableSubMemberIds": [  
                "554117",  
                "592324"  
            ]  
        },  
        "retExtInfo": {},  
        "time": 1672147241320  
    }  
    

[PreviousGet Coin Info](https://bybit-exchange.github.io/docs/v5/asset/coin-info)[NextGet Single Coin Balance](https://bybit-exchange.github.io/docs/v5/asset/balance/account-coin-balance)

  * HTTP Request
  * Request Parameters
  * Response Parameters
  * Request Example
  * Response Example


